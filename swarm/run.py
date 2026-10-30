"""Launch a swarm: a base clone, one worktree per generator, generators in parallel.

Layout of a run:
    runs/<run>/
        meta.json          target, job, brief, base commit, generators (provider, direction)
        base/              a clone of the game at the run's base commit, set up once
        pack.md            the context pack every generator gets
        gens/<gid>/        one worktree per generator
            .swarm/PACK.md, DIRECTION.md, manifest.json (the generator's), out/ (renders)
        logs/<gid>.json    the runtime's own output (usage, turns, result)
        logs/<gid>.err     its stderr
"""

from __future__ import annotations

import concurrent.futures as cf
import json
import os
import random
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from . import config, pack

STUB = """# Generator

You are a generator in a swarm, not a session on this game. Ignore any usual protocol
for this repo. Your whole task is in `.swarm/PACK.md`: read it first, then
`.swarm/DIRECTION.md`, then do the task.
"""

PROMPT = "Read .swarm/PACK.md, then .swarm/DIRECTION.md, and do the task they describe. Stop when the manifest is written."


def sh(cmd: list[str] | str, cwd: Path, env: dict | None = None, timeout: int | None = None, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=cwd, env=env, timeout=timeout, check=check, text=True, capture_output=True, shell=isinstance(cmd, str)
    )


def parse_gens(spec: str, provs: dict[str, config.Provider]) -> list[str]:
    """'deepseek:3,qwen:2' -> ['deepseek', 'deepseek', 'deepseek', 'qwen', 'qwen']"""
    out = []
    for part in spec.split(","):
        name, _, n = part.strip().partition(":")
        if name not in provs:
            raise SystemExit(f"unknown provider {name!r}; known: {', '.join(provs)}")
        out += [name] * int(n or 1)
    return out


def apply_platform(j: config.Job, base: Path, log) -> None:
    """A job may need game code that isn't merged yet (job.toml [platform]): when the
    file it needs is missing, apply its patches to the base clone and commit them
    there, so every worktree starts from the patched game. The real repo is never
    touched."""
    # A job may also change a few lines of its own base clone (job.toml [[base_edits]]:
    # a file, an exact `find` and its `replace`), say a budget raised for one experiment.
    # Committed in the clone, so worktrees and patches build on it; the real repo never
    # sees it, and a winner that relies on it says so.
    edits = j.data.get("base_edits", [])
    for e in edits:
        f = base / e["file"]
        text = f.read_text(encoding="utf-8")
        if e["find"] not in text:
            raise SystemExit(f"base edit: {e['find']!r} isn't in {e['file']} any more; update the job")
        f.write_text(text.replace(e["find"], e["replace"], 1), encoding="utf-8")
        log(f"base edit in {e['file']}: {e.get('why', '')}")
    if edits:
        sh(["git", "-c", "user.name=swarm-lab", "-c", "user.email=swarm-lab@localhost", "commit", "-qam",
            f"swarm-lab: base edits for the {j.name} job (not in the game)"], cwd=base)
    plat = j.data.get("platform")
    if not plat or (base / plat["needs"]).exists():
        return
    for rel in plat.get("patches", []):
        patch = (config.ROOT / rel).resolve()
        log(f"the game lacks {plat['needs']}: applying {rel} to the base clone")
        sh(["git", "apply", "--whitespace=nowarn", str(patch)], cwd=base)
    sh(["git", "add", "-A"], cwd=base)
    sh(["git", "-c", "user.name=swarm-lab", "-c", "user.email=swarm-lab@localhost", "commit", "-qm",
        f"swarm-lab: platform for the {j.name} job (not in the game yet)"], cwd=base)
    if not (base / plat["needs"]).exists():
        raise SystemExit(f"the platform patches didn't provide {plat['needs']}")


def apply_brief_patches(brief: dict, base: Path, log) -> None:
    """A brief may bring patches of its own (brief `patches`, paths in swarm-lab), applied to
    the base clone after the job's platform: say the area look a map is drawn in. Three-way,
    so a look made on an older main still lands."""
    rels = brief.get("patches", [])
    if not rels or (base / ".swarm-brief-patches").exists():
        return
    for rel in rels:
        log(f"brief patch: {rel}")
        sh(["git", "apply", "-3", "--whitespace=nowarn", str((config.ROOT / rel).resolve())], cwd=base)
    (base / ".swarm-brief-patches").write_text("\n".join(rels) + "\n")
    sh(["git", "add", "-A"], cwd=base)
    sh(["git", "-c", "user.name=swarm-lab", "-c", "user.email=swarm-lab@localhost", "commit", "-qm",
        f"swarm-lab: the brief's own patches ({', '.join(rels)})"], cwd=base)


def make_base(t: config.Target, run_dir: Path, log, j: config.Job | None = None) -> str:
    base = run_dir / "base"
    if not base.exists():
        src = t.repo_path()
        log(f"cloning {src or t.repo}")
        sh(["git", "clone", "--quiet", str(src or t.repo), str(base)], cwd=run_dir)
        # A local clone's origin is the local repo, which tracks the real origin's
        # branches as remotes; fetch them so refs like origin/main resolve.
        if src is not None:
            sh(["git", "fetch", "--quiet", str(src), "+refs/remotes/origin/*:refs/remotes/origin/*"], cwd=base, check=False)
        sh(["git", "checkout", "--quiet", "--detach", t.ref], cwd=base)
        if t.setup:
            log(f"setup: {t.setup}")
            r = sh(t.setup, cwd=base, env=t.env(), timeout=1800, check=False)
            (run_dir / "logs").mkdir(exist_ok=True)
            (run_dir / "logs" / "setup.log").write_text(r.stdout + r.stderr)
            if r.returncode != 0:
                log("setup reported problems (logs/setup.log); continuing")
        if j is not None:
            apply_platform(j, base, log)
    return sh(["git", "rev-parse", "HEAD"], cwd=base).stdout.strip()


def render_reference(t: config.Target, brief: dict, run_dir: Path, log) -> None:
    """Render the brief's reference commands once in the base clone, so the contact
    sheet's REF tile is drawn exactly as the brief says, whatever generators do."""
    base = run_dir / "base"
    (base / ".swarm" / "out").mkdir(parents=True, exist_ok=True)
    ref_cmds, _ = pack.render_commands(brief)
    for cmd in ref_cmds.splitlines():
        r = sh(cmd, cwd=base, env=t.env(), timeout=300, check=False)
        if r.returncode != 0:
            log(f"reference render failed: {cmd}\n{(r.stdout + r.stderr)[-400:]}")


def make_worktree(t: config.Target, run_dir: Path, gid: str, commit: str, pack_text: str, direction: str,
                  figures: list[config.Figure] | tuple = (), tools: list[Path] | tuple = ()) -> Path:
    base = run_dir / "base"
    wt = run_dir / "gens" / gid
    if wt.exists():
        return wt
    sh(["git", "worktree", "add", "--quiet", "--detach", str(wt), commit], cwd=base)
    for rel in t.hide:
        p = wt / rel
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()
    (wt / "CLAUDE.md").write_text(STUB)
    for rel in t.share:
        src, dst = base / rel, wt / rel
        if src.exists() and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.symlink_to(src.resolve(), target_is_directory=src.is_dir())
    sw = wt / ".swarm"
    (sw / "out").mkdir(parents=True, exist_ok=True)
    (sw / "PACK.md").write_text(pack_text)
    (sw / "DIRECTION.md").write_text(pack.direction_file(direction))
    # A job's own helper tools (job.toml `tools`), for generators to run from .swarm/tools/.
    for src in tools:
        (sw / "tools").mkdir(exist_ok=True)
        shutil.copy2(src, sw / "tools" / src.name)
    for f in figures:
        dst = wt / f.wt_dir()
        dst.mkdir(parents=True, exist_ok=True)
        for rel in f.data.get("files", []):
            shutil.copy2(f.dir / rel, dst / Path(rel).name)
    return wt


def runtime_argv(p: config.Provider, max_turns: int | None = None) -> list[str]:
    if p.runtime == "claude-code":
        return [
            "claude", "-p", PROMPT,
            "--output-format", "json",
            "--max-turns", str(max_turns or p.max_turns),
            "--model", p.model,
            "--permission-mode", "bypassPermissions",
            "--disallowedTools", "WebSearch", "WebFetch", "Task", "Agent", "NotebookEdit",
        ]
    if p.runtime == "exec":
        return list(p.command)
    raise SystemExit(f"runtime {p.runtime!r} isn't built yet (provider {p.name})")


CONFIG_DIR = config.ROOT / "runs" / ".claude-config"


def runtime_env(t: config.Target, p: config.Provider) -> dict[str, str]:
    env = t.env()
    if p.runtime == "claude-code":
        # When the harness itself runs inside a Claude Code session (a cloud session,
        # say), the child `claude` inherits that session's settings, some of which make
        # it ignore the provider's endpoint and key ("Authentication error"). Generators
        # start clean: none of the parent's Claude or Anthropic settings, and a config
        # folder of their own instead of the user's.
        for k in [k for k in env if k.startswith(("CLAUDE", "CCR_", "ANTHROPIC_"))]:
            del env[k]
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        env["CLAUDE_CONFIG_DIR"] = str(CONFIG_DIR)
        if p.base_url:
            env["ANTHROPIC_BASE_URL"] = p.base_url
            env["ANTHROPIC_AUTH_TOKEN"] = p.key()
            env.pop("ANTHROPIC_API_KEY", None)
        elif p.key():
            env["ANTHROPIC_API_KEY"] = p.key()
        env["ANTHROPIC_MODEL"] = p.model
        env["ANTHROPIC_SMALL_FAST_MODEL"] = p.small_model or p.model
        env["CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"] = "1"
    # The provider's own settings last, so they win (providers.toml, `env`).
    env.update({k: str(v) for k, v in p.env.items()})
    return env


class Budget:
    """Stops launching a provider's generators once its run budget is spent."""

    def __init__(self, provs: dict[str, config.Provider]):
        # None means no cap (budget_tokens = 0 or unset).
        self.left: dict[str, int | None] = {n: (p.budget_tokens or None) for n, p in provs.items()}
        self.lock = threading.Lock()

    def ok(self, name: str) -> bool:
        with self.lock:
            left = self.left.get(name)
            return left is None or left > 0

    def spend(self, name: str, tokens: int) -> None:
        with self.lock:
            if self.left.get(name) is not None:
                self.left[name] -= tokens


def total_tokens(usage: dict) -> int:
    return sum(int(usage.get(k, 0)) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens"))


def run_one(t, p, wt: Path, log_dir: Path, gid: str, budget: Budget, dry: bool, max_turns: int | None = None) -> dict:
    # A job may need more turns than the provider default (job.toml `max_turns`).
    argv = runtime_argv(p, max_turns)
    rec = {"gid": gid, "provider": p.name, "model": p.model, "argv": argv}
    if dry:
        rec["status"] = "dry-run"
        return rec
    if not budget.ok(p.name):
        rec["status"] = "skipped: provider budget spent"
        return rec
    if p.runtime == "claude-code" and p.key_env and not p.key():
        rec["status"] = f"skipped: {p.key_env} is not set"
        return rec
    t0 = time.time()
    try:
        r = subprocess.run(argv, cwd=wt, env=runtime_env(t, p), text=True, capture_output=True, timeout=p.timeout_s)
        out, err, code = r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err, code = f"timed out after {p.timeout_s}s", -1
    rec["seconds"] = round(time.time() - t0, 1)
    rec["exit"] = code
    (log_dir / f"{gid}.out").write_text(out)
    (log_dir / f"{gid}.err").write_text(err)
    usage = {}
    try:
        res = json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
        usage = res.get("usage", {}) or {}
        rec["turns"] = res.get("num_turns")
        rec["runtime_error"] = res.get("is_error", False)
    except (json.JSONDecodeError, IndexError):
        rec["runtime_error"] = True
    rec["usage"] = usage
    rec["tokens"] = total_tokens(usage)
    rec["cost_usd"] = round(p.cost(usage), 4)
    budget.spend(p.name, rec["tokens"])
    rec["status"] = "finished" if code == 0 else f"exit {code}"
    return rec


RESUME_PROMPT = (
    "You ran out of turns before finishing. Don't start over and don't revise the design "
    "again: format, render your final look once, run the checks in .swarm/PACK.md's "
    "Commands and fix only what fails, then write .swarm/manifest.json as the pack says, "
    "and stop."
)


def resume_one(t, p, wt: Path, log_dir: Path, gid: str, prior: dict, turns: int) -> dict:
    """Continue a stopped generator's own conversation (claude --resume), so its work so
    far is kept and only finishing it costs. Usage and time add to the first attempt's."""
    out_path = log_dir / f"{gid}.out"
    try:
        session = json.loads(out_path.read_text().strip().splitlines()[-1]).get("session_id")
    except (OSError, json.JSONDecodeError, IndexError):
        session = None
    if not session:
        # A generator killed at the wall-time cap printed no result, but its transcript
        # is in the shared config dir, named by session; take the newest for its worktree.
        proj = CONFIG_DIR / "projects" / str(wt.resolve()).replace("/", "-").replace(".", "-")
        logs = sorted(proj.glob("*.jsonl"), key=lambda f: f.stat().st_mtime)
        session = logs[-1].stem if logs else None
    rec = dict(prior)
    if not session:
        rec["status"] = "not resumed: no session recorded"
        return rec
    argv = runtime_argv(p, turns)
    argv[argv.index("-p") + 1] = RESUME_PROMPT
    argv += ["--resume", session]
    t0 = time.time()
    try:
        r = subprocess.run(argv, cwd=wt, env=runtime_env(t, p), text=True, capture_output=True, timeout=p.timeout_s)
        out, err, code = r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        err, code = f"timed out after {p.timeout_s}s", -1
    (log_dir / f"{gid}.resume.out").write_text(out)
    (log_dir / f"{gid}.resume.err").write_text(err)
    try:
        res = json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
    except (json.JSONDecodeError, IndexError):
        res = {}
    usage = res.get("usage", {}) or {}
    merged = dict(rec.get("usage") or {})
    for k, v in usage.items():
        if isinstance(v, (int, float)):
            merged[k] = merged.get(k, 0) + v
    rec["usage"] = merged
    rec["tokens"] = total_tokens(merged)
    rec["cost_usd"] = round(p.cost(merged), 4)
    rec["seconds"] = round(rec.get("seconds", 0) + time.time() - t0, 1)
    rec["turns"] = (rec.get("turns") or 0) + (res.get("num_turns") or 0)
    rec["resumed"] = True
    rec["status"] = "finished" if code == 0 else f"exit {code}"
    return rec


def resume(run_dir: Path, turns: int = 30, concurrency: int = 4) -> Path:
    """Resume every generator of a run that didn't finish and left no manifest."""
    meta = json.loads((run_dir / "meta.json").read_text())
    t = config.target(meta["target"])
    provs = config.providers()
    recs = {g["gid"]: g for g in json.loads((run_dir / "generators.json").read_text())}
    todo = [g for g in meta["generators"]
            if recs.get(g["gid"], {}).get("status") != "finished"
            and not (run_dir / "gens" / g["gid"] / ".swarm" / "manifest.json").exists()]
    log = lambda msg: print(f"[{meta['run']}] {msg}", flush=True)  # noqa: E731
    log(f"resuming {len(todo)}: " + ", ".join(g["gid"] for g in todo) + f" (up to {turns} more turns each)")
    with cf.ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        futs = {pool.submit(resume_one, t, provs[g["provider"]], run_dir / "gens" / g["gid"], run_dir / "logs",
                            g["gid"], recs.get(g["gid"], {}), turns): g for g in todo}
        for f in cf.as_completed(futs):
            rec = f.result()
            recs[rec["gid"]] = rec
            log(f"{rec['gid']} {rec['provider']}: {rec['status']}, total {rec.get('seconds')}s, ${rec.get('cost_usd')}")
    (run_dir / "generators.json").write_text(json.dumps([recs[k] for k in sorted(recs)], indent=2))
    return run_dir


def run(target_name: str, job_name: str, brief_name: str, gens: str, run_id: str | None = None,
        concurrency: int = 4, dry: bool = False, seed: int | None = None, figure: str | None = None) -> Path:
    t = config.target(target_name)
    j = config.job(t, job_name)
    brief = j.brief(brief_name)
    figs = config.figures(t, j, brief, figure)
    provs = config.providers()
    plan = parse_gens(gens, provs)

    run_id = run_id or f"{datetime.now().strftime('%Y%m%d-%H%M')}-{brief['skill']}"
    run_dir = config.ROOT / "runs" / run_id
    (run_dir / "logs").mkdir(parents=True, exist_ok=True)
    log = lambda msg: print(f"[{run_id}] {msg}", flush=True)  # noqa: E731

    make_base(t, run_dir, log, j)
    apply_brief_patches(brief, run_dir / "base", log)
    commit = sh(["git", "rev-parse", "HEAD"], cwd=run_dir / "base").stdout.strip()
    pack_text = pack.build(j, brief, run_dir / "base", figs)
    (run_dir / "pack.md").write_text(pack_text)
    log(f"pack: {len(pack_text):,} chars (~{len(pack_text) // 4:,} tokens)")
    if not dry:
        render_reference(t, brief, run_dir, log)

    rng = random.Random(seed if seed is not None else run_id)
    rng.shuffle(plan)  # mixed providers interleave, so a budget stop doesn't hit one arm
    directions = j.directions(brief)
    gens_meta = []
    for i, prov in enumerate(plan):
        gid = f"g{i:02d}"
        d = directions[i % len(directions)]
        make_worktree(t, run_dir, gid, commit, pack_text, d, figs, [j.dir / rel for rel in j.data.get("tools", [])])
        gens_meta.append({"gid": gid, "provider": prov, "model": provs[prov].model, "direction": d})

    meta = {
        "run": run_id, "target": target_name, "job": job_name, "brief": brief_name,
        "skill": brief["skill"], "family": brief["family"], "base": commit,
        "figures": [f.name for f in figs],
        "started": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "generators": gens_meta,
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    budget = Budget({n: provs[n] for n in set(plan)})
    log(f"{len(plan)} generators: " + ", ".join(f"{n}×{plan.count(n)}" for n in sorted(set(plan))) + (" (dry run)" if dry else ""))
    results = []
    with cf.ThreadPoolExecutor(max_workers=max(1, concurrency)) as pool:
        futs = {
            pool.submit(run_one, t, provs[g["provider"]], run_dir / "gens" / g["gid"], run_dir / "logs", g["gid"], budget, dry, j.data.get("max_turns")): g
            for g in gens_meta
        }
        for f in cf.as_completed(futs):
            rec = f.result()
            results.append(rec)
            log(f"{rec['gid']} {rec['provider']}: {rec['status']}" + (f", {rec.get('seconds')}s, ${rec.get('cost_usd')}" if "seconds" in rec else ""))
    results.sort(key=lambda r: r["gid"])
    (run_dir / "generators.json").write_text(json.dumps(results, indent=2))
    if dry:
        log("dry run: argv for g00 is " + " ".join(results[0]["argv"]) if results else "dry run: nothing to run")
    return run_dir
