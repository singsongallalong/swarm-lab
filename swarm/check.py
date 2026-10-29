"""Filter a run: reject what broke the rules, run the specs on the rest.

For each generator, in order (the first failure is the reason given):
  1. it finished and wrote a valid .swarm/manifest.json whose renders exist;
  2. it changed no file outside the job's allowlist (hidden files and .swarm/ aside);
  3. in each allowed file it changed only what that file's mode allows;
  4. the job's specs pass in its worktree.
Survivors get a patch of their allowed files, which `apply` puts on a branch later.
Writes runs/<run>/check.json.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from . import config, luarows, pack

MANIFEST_KEYS = {"skill", "look", "rows_added", "intent", "renders"}


def _git(args: list[str], cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, check=True).stdout


def changed_paths(wt: Path, hidden: list[str]) -> list[str]:
    """Tracked files changed and untracked files added, ignoring the launcher's own
    changes (hidden files, the stub CLAUDE.md, shared links, .swarm/)."""
    out = []
    for line in _git(["status", "--porcelain", "--untracked-files=all", "--no-renames"], wt).splitlines():
        path = line[3:].strip().strip('"')
        if path.startswith(".swarm/") or any(path == h or path.startswith(h.rstrip("/") + "/") for h in hidden):
            continue
        out.append(path)
    return out


def check_manifest(wt: Path, skill: str) -> tuple[dict | None, str | None]:
    p = wt / ".swarm" / "manifest.json"
    if not p.exists():
        return None, "no manifest"
    try:
        m = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        return None, f"manifest is not JSON ({e.msg})"
    missing = MANIFEST_KEYS - set(m)
    if missing:
        return m, f"manifest lacks {', '.join(sorted(missing))}"
    if m["skill"] != skill:
        return m, f"manifest is for {m['skill']!r}, not {skill!r}"
    renders = [r for r in m.get("renders", []) if (wt / r).is_file()]
    if not renders:
        return m, "no rendered image listed in the manifest exists"
    m["renders"] = renders
    return m, None


def _norm(text: str) -> str:
    """Ignore blank lines and trailing spaces, so placing a new row with an extra
    blank line around it isn't counted as an edit."""
    return "\n".join(l.rstrip() for l in text.splitlines() if l.strip())


def check_rows(rel: str, mode: str, before: str, after: str, skill: str) -> str | None:
    if mode == "owned_row":
        if _norm(luarows.without(before, {skill})) != _norm(luarows.without(after, {skill})):
            return f"{rel}: changed something besides the {skill} row"
        return None
    if mode == "add_rows":
        old, new = luarows.top_rows(before), luarows.top_rows(after)
        for name, row in old.items():
            if name not in new:
                return f"{rel}: removed the existing row {name}"
            if row.text(before) != new[name].text(after):
                return f"{rel}: changed the existing row {name}"
        added = set(new) - set(old)
        bad = sorted(n for n in added if not n.startswith(skill))
        if bad:
            return f"{rel}: new row {bad[0]} doesn't start with {skill}"
        if _norm(before) != _norm(luarows.without(after, added)):
            return f"{rel}: changed text outside its rows"
        return None
    return f"{rel}: unknown mode {mode!r}"


def run_specs(wt: Path, specs: list[dict], env: dict, timeout: int = 600) -> tuple[list[dict], str | None]:
    results = []
    for s in specs:
        try:
            r = subprocess.run(s["cmd"], cwd=wt, env=env, shell=True, text=True, capture_output=True, timeout=timeout)
            ok, tail = r.returncode == 0, (r.stdout + r.stderr)[-1500:]
        except subprocess.TimeoutExpired:
            ok, tail = False, f"timed out after {timeout}s"
        results.append({"name": s["name"], "ok": ok, "tail": tail})
        if not ok:
            return results, f"spec {s['name']} failed"
    return results, None


def skill_color(wt: Path, skill: str, fallback) -> list[int]:
    """The colour the candidate's SkillVisuals row gives the skill, so its final render
    shows the colour it chose."""
    try:
        row = luarows.get((wt / "src/shared/data/SkillVisuals.luau").read_text(encoding="utf-8"), skill)
        m = re.search(r"Color3\.fromRGB\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", row)
        if m:
            return [int(v) for v in m.groups()]
    except (OSError, KeyError, ValueError):
        pass
    return list(fallback)


def render_final(wt: Path, t: config.Target, meta: dict, manifest: dict) -> tuple[list[str], str | None]:
    """Re-render the candidate's look from the brief's own commands, so every tile on
    the sheet is drawn the same way however the generator rendered it."""
    j = config.job(t, meta["job"])
    brief = dict(j.brief(meta["brief"]))
    brief["color"] = skill_color(wt, meta["skill"], brief["color"])
    _, cmds = pack.render_commands(brief)
    out = []
    for cmd in cmds.splitlines():
        if not cmd.strip() or cmd.lstrip().startswith("#"):
            continue
        cmd = cmd.replace("<YourLook>", manifest["look"]).replace("-r1.png", "-final.png")
        r = subprocess.run(cmd, cwd=wt, env=t.env(), shell=True, text=True, capture_output=True, timeout=300)
        if r.returncode != 0:
            return out, f"its look didn't render ({(r.stdout + r.stderr).strip()[-200:]})"
        path = next((a for a in cmd.split() if a.endswith(".png")), None)
        if path and (wt / path).is_file():
            out.append(path)
    return out, None


def check_one(wt: Path, t: config.Target, j: config.Job, meta: dict, gen: dict, run_specs_too: bool) -> dict:
    skill, base = meta["skill"], meta["base"]
    rec = {"gid": gen["gid"], "provider": gen.get("provider"), "survived": False}
    if gen.get("status") not in (None, "finished"):
        rec["reason"] = f"generator {gen['status']}"
        return rec

    manifest, why = check_manifest(wt, skill)
    rec["manifest"] = manifest
    if why:
        rec["reason"] = why
        return rec

    hidden = list(t.hide) + list(t.share)
    allowed = set(j.files)
    changed = changed_paths(wt, hidden)
    stray = [p for p in changed if p not in allowed]
    if stray:
        rec["reason"] = f"touched {stray[0]}" + (f" and {len(stray) - 1} more" if len(stray) > 1 else "")
        return rec
    if not changed:
        rec["reason"] = "changed nothing"
        return rec

    for rel in changed:
        before = _git(["show", f"{base}:{rel}"], wt)
        after = (wt / rel).read_text(encoding="utf-8")
        try:
            why = check_rows(rel, j.files[rel]["mode"], before, after, skill)
        except ValueError as e:
            why = f"{rel}: couldn't read its rows ({e})"
        if why:
            rec["reason"] = why
            return rec

    if run_specs_too:
        rec["specs"], why = run_specs(wt, j.data.get("specs", []), t.env())
        if why:
            rec["reason"] = why
            return rec

    if run_specs_too:
        rendered, why = render_final(wt, t, meta, manifest)
        if why:
            rec["reason"] = why
            return rec
        manifest["renders"] = rendered + [r for r in manifest["renders"] if r not in rendered]

    patch = _git(["diff", base, "--", *sorted(changed)], wt)
    (wt / ".swarm" / "patch.diff").write_text(patch)
    rec["patch"] = str((wt / ".swarm" / "patch.diff").relative_to(wt.parent.parent))
    rec["changed"] = changed
    rec["survived"] = True
    return rec


def check(run_dir: Path, specs: bool = True) -> dict:
    meta = json.loads((run_dir / "meta.json").read_text())
    t = config.target(meta["target"])
    j = config.job(t, meta["job"])
    gens_path = run_dir / "generators.json"
    gens = {g["gid"]: g for g in json.loads(gens_path.read_text())} if gens_path.exists() else {}
    out = []
    for g in meta["generators"]:
        gen = {**g, **gens.get(g["gid"], {})}
        rec = check_one(run_dir / "gens" / g["gid"], t, j, meta, gen, specs)
        out.append(rec)
        print(f"  {rec['gid']} {rec['provider']}: " + ("survived" if rec["survived"] else f"rejected, {rec['reason']}"))
    result = {"run": meta["run"], "generators": out, "survivors": [r["gid"] for r in out if r["survived"]]}
    (run_dir / "check.json").write_text(json.dumps(result, indent=2))
    print(f"  {len(result['survivors'])} of {len(out)} survived")
    return result
