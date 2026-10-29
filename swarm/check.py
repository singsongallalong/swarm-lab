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
    return m, None


def check_renders(wt: Path, m: dict) -> str | None:
    """Checked after the files and code, so a run whose render crashed on bad code is
    rejected for the code, which is the reason worth reading."""
    renders = [r for r in m.get("renders", []) if (wt / r).is_file()]
    if not renders:
        return "no rendered image listed in the manifest exists"
    m["renders"] = renders
    return None


def _norm(text: str) -> str:
    """Ignore blank lines and trailing spaces, so placing a new row with an extra
    blank line around it isn't counted as an edit."""
    return "\n".join(l.rstrip() for l in text.splitlines() if l.strip())


def check_rows(rel: str, mode: str, before: str | None, after: str, skill: str, spec_pattern: str | None = None) -> str | None:
    if before is None and mode not in ("new_file",):
        return f"{rel}: is a new file, but this job only lets it be edited"
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
    if mode == "new_file":
        if before is not None:
            return f"{rel}: changed a file that already existed"
        return None
    if mode == "add_lines":
        # Lines may only be added, never changed or removed, and each added line must
        # match the rule's pattern (a registry entry for this skill's module).
        old = [l for l in before.splitlines() if l.strip()]
        new = [l for l in after.splitlines() if l.strip()]
        it = iter(new)
        if not all(any(o == n for n in it) for o in old):
            return f"{rel}: changed or removed an existing line"
        added = list(new)
        for o in old:
            added.remove(o)
        pattern = (spec_pattern or "").replace("{skill}", re.escape(skill))
        for line in added:
            if pattern and not re.fullmatch(pattern, line.strip()):
                return f"{rel}: added a line that isn't a {skill} entry: {line.strip()[:80]}"
        return None
    return f"{rel}: unknown mode {mode!r}"


def check_code(rel: str, text: str, purity: dict) -> str | None:
    """A generated module must be strict, small and pure (the game's CLAUDE.md, rule 4):
    no Roblox services or Instances, no yielding, nothing that loads or escapes code,
    and requires only from the job's list."""
    lines = text.splitlines()
    if purity.get("first_line") and (not lines or lines[0].strip() != purity["first_line"]):
        return f"{rel}: doesn't start with {purity['first_line']}"
    if purity.get("max_lines") and len(lines) > purity["max_lines"]:
        return f"{rel}: {len(lines)} lines, over {purity['max_lines']}"
    code = "\n".join(l.split("--", 1)[0] for l in lines)  # comments may say anything
    code = re.sub(r'"(?:[^"\\]|\\.)*"', '""', code)  # nor may strings trip a word
    for pattern in purity.get("forbid", []):
        m = re.search(pattern, code)
        if m:
            return f"{rel}: uses {m.group(0).strip()!r}, which a pure module mustn't"
    allowed = set(purity.get("requires", []))
    for req in re.findall(r'require\(\s*"([^"]+)"\s*\)', text):
        if req not in allowed:
            return f"{rel}: requires {req!r}, which isn't on the job's list"
    if re.search(r"require\(\s*[^\"\s]", text):
        return f"{rel}: requires something other than a plain path"
    return None


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


COUNTS = re.compile(r"(\d+) parts(?:, (\d+) particles)?")


def render_final(wt: Path, t: config.Target, meta: dict, manifest: dict) -> tuple[list[str], str | None]:
    """Re-render the candidate's look from the brief's own commands, so every tile on
    the sheet is drawn the same way however the generator rendered it. The preview's
    own count line (`<n> parts, <m> particles`) goes into the manifest as `counts`."""
    j = config.job(t, meta["job"])
    manifest.pop("counts", None)  # only the harness's own render counts, never the generator's say-so
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
        m = COUNTS.search(r.stdout)
        if m and "counts" not in manifest:
            manifest["counts"] = {"parts": int(m.group(1)), "particles": int(m.group(2) or 0)}
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
    changed = changed_paths(wt, hidden)
    stray = [p for p in changed if j.rule(p, skill) is None]
    if stray:
        rec["reason"] = f"touched {stray[0]}" + (f" and {len(stray) - 1} more" if len(stray) > 1 else "")
        return rec
    if not changed:
        rec["reason"] = "changed nothing"
        return rec

    for rel in changed:
        rule = j.rule(rel, skill)
        shown = subprocess.run(["git", "show", f"{base}:{rel}"], cwd=wt, text=True, capture_output=True)
        before = shown.stdout if shown.returncode == 0 else None
        if not (wt / rel).exists():
            rec["reason"] = f"{rel}: deleted"
            return rec
        after = (wt / rel).read_text(encoding="utf-8")
        try:
            why = check_rows(rel, rule["mode"], before, after, skill, rule.get("pattern"))
        except ValueError as e:
            why = f"{rel}: couldn't read its rows ({e})"
        if not why and rule["mode"] == "new_file":
            why = check_code(rel, after, j.data.get("purity", {}))
        if why:
            rec["reason"] = why
            return rec

    why = check_renders(wt, manifest)
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

    # New files are untracked, and a plain diff leaves them out; mark them as intended
    # first so the patch carries a new module whole.
    _git(["add", "--intent-to-add", "--", *sorted(changed)], wt)
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
