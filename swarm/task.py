"""Worker tasks: a Claude agent hands a bounded piece of work to a few DeepSeek workers.

A swarm job (targets/<t>/<job>/) is hand-made for a kind of content, with renders and a
critic. A task is ad hoc: one TOML file a Claude agent writes on the spot, saying what to
build, which files the workers may touch and how, what to show them, and which commands
must pass. `swarm task run` turns it into a one-off job under the run folder, starts the
workers from the agent's own commit, checks them like any run, and writes summary.md:
one patch per survivor, ranked. The agent reads the patches, applies the one it wants
(`swarm task apply`), and carries on. Nothing lands anywhere without it.

    title = "Catalog rows for the new sculpts"
    repo = "../arpg-game"          # default: the target's repo
    ref = "HEAD"                   # a commit the repo has: the agent's branch, not just main
    workers = 3                    # how many tries
    model = "flash"                # or "pro" (code only: it can't see images)
    turns = 60
    brief = '''What to do, why, and what good looks like.'''
    read = ["src/shared/data/Sculpts.luau"]          # quoted whole in the pack
    checks = ["lune run tests Catalog", "stylua --check src/shared/data/catalog"]
    directions = ["...", "..."]    # optional: one stance per worker
    [[files]]
    path = "src/shared/data/catalog/World.luau"
    mode = "add_lines"             # new_file | add_rows | add_lines | owned_row | edit | any
    pattern = '...'                # add_lines: a regex each added line must match
    [[held_out]]                   # optional: scored, never shown, kept outside the tree
    file = "~/.swarm-heldout/x/Y.spec.luau"
    dest = "tests/systems/Y.spec.luau"
    cmd = "lune run tests Y"
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

from . import check as check_mod
from . import config
from . import report as report_mod
from . import run as run_mod

MODELS = {"flash": "deepseek", "pro": "deepseek-pro"}

PACK = """# Task: $title

You are one of several workers, each doing the same task independently in your own copy of
a Roblox action RPG's repository (strict Luau). A Claude engineer wrote this task and will
review every worker's result and keep the best. Do the task, run every check until it
passes, and stop. Your stance, if you have one, is in `.swarm/DIRECTION.md` (read it last).

## Hard rules (a result that breaks one is discarded unread)

1. **Edit only these files, only as described:**
$files_section
2. **Every check below must pass.** Run them yourself before you stop.
3. **Don't read files outside this pack** unless a command fails and its error names one.
   No web, no exploring the repo.
4. **Stop when the checks pass** and the task is done; don't polish past the brief.

## The task

$brief

## The repo's rules

$rules

$context

## Checks

Run from the repository root, exactly as written:

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "$skill",
  "rows_added": [],
  "intent": "<one or two sentences: what you did and any choice the reviewer should know about>",
  "renders": [],
  "revisions": 0,
  "requests": ["<optional: anything in the task that seemed wrong, unclear or missing, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
"""


def _toml_str(s: str) -> str:
    return json.dumps(s)  # a JSON string is a valid TOML basic string


def _slug(title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    return "".join(w[:1].upper() + w[1:] for w in words)[:40] or "Task"


def prepare(task_path: Path, run_id: str) -> tuple[config.Target, str, Path]:
    """Write the one-off job for a task under runs/<run_id>/job; return the target (its
    ref set to the task's commit), the job's name relative to the target, and the run."""
    task = config.load_toml(task_path)
    t = config.target(task.get("target", "arpg-game"))
    if "repo" in task:
        t.repo = task["repo"]
    src = t.repo_path() or Path(t.repo)
    ref = task.get("ref", "HEAD")
    commit = subprocess.run(["git", "rev-parse", ref], cwd=src, text=True, capture_output=True, check=True).stdout.strip()
    t.ref = commit

    run_dir = config.ROOT / "runs" / run_id
    jdir = run_dir / "job"
    (jdir / "briefs").mkdir(parents=True, exist_ok=True)
    skill = task.get("name") or _slug(task["title"])

    files = task.get("files", [])
    if not files:
        raise SystemExit("a task must name the files its workers may touch ([[files]])")
    checks = task.get("checks", [])
    if not checks:
        raise SystemExit("a task must name at least one check that has to pass (checks = [...])")

    rules_file = t.dir / "worker-rules.md"
    rules = rules_file.read_text() if rules_file.is_file() else ""
    rules = "\n".join(("##" + l) if l.startswith("#") else l for l in rules.splitlines())

    lines = [
        f"# A worker task ({task_path.name}), written by swarm task on {datetime.now():%Y-%m-%d %H:%M}.",
        'template = "pack.md"',
        'directions = "directions.txt"',
        f"max_turns = {int(task.get('turns', 60))}",
        "renders = false",
        "rules = []",
        'tools = ["../../../targets/arpg-game/zones/tools/explain.luau"]' if t.name == "arpg-game" else "",
        "",
    ]
    for f in files:
        lines.append(f"[files.{_toml_str(f['path'])}]")
        lines.append(f"mode = {_toml_str(f.get('mode', 'edit'))}")
        if "pattern" in f:
            lines.append(f"pattern = '{f['pattern']}'")
        if "prefix" in f:
            lines.append(f"prefix = {_toml_str(f['prefix'])}")
        lines.append("")
    if task.get("purity"):
        p = task["purity"]
        lines.append("[purity]")
        for k, v in p.items():
            lines.append(f"{k} = {json.dumps(v)}")
        lines.append("")
    context_parts = []
    for i, rel in enumerate(task.get("read", [])):
        lines += [f"[quotes.q{i}]", f"file = {_toml_str(rel)}", f"note = {_toml_str('context')}", ""]
        context_parts.append(f"$q{i}")
    for i, cmd in enumerate(checks):
        lines += ["[[specs]]", f"name = {_toml_str(f'check {i + 1}')}", f"cmd = {_toml_str(cmd)}", ""]
    for h in task.get("held_out", []):
        lines += ["[[held_out]]", f"file = {_toml_str(h['file'])}", f"dest = {_toml_str(h['dest'])}",
                  f"cmd = {_toml_str(h['cmd'])}", ""]
    (jdir / "job.toml").write_text("\n".join(lines))

    context = ("## Files to know\n\n" + "\n\n".join(context_parts)) if context_parts else ""
    pack_text = (PACK.replace("$title", task["title"]).replace("$rules", rules.replace("$", "$$"))
                 .replace("$context", context))
    (jdir / "pack.md").write_text(pack_text)
    dirs = task.get("directions") or ["Do the task as plainly as it allows."]
    (jdir / "directions.txt").write_text("# This task's stances.\n" + "\n".join(dirs) + "\n")
    brief = ["# The task's brief.", f"skill = {_toml_str(skill)}", 'family = "code"',
             f"brief = {_toml_str(task['brief'])}"]
    (jdir / "briefs" / "Task.toml").write_text("\n".join(brief) + "\n")
    (run_dir / "task.toml").write_text(task_path.read_text())
    return t, str(Path("..", "..", "runs", run_id, "job")), run_dir


def run(task_path: Path, run_id: str | None = None, workers: int | None = None, model: str | None = None,
        offpeak: bool = False, concurrency: int = 6) -> Path:
    task = config.load_toml(task_path)
    run_id = run_id or f"task-{datetime.now():%Y%m%d-%H%M}-{task.get('name') or _slug(task['title'])}"[:60]
    t, job_name, _ = prepare(task_path, run_id)
    n = workers or int(task.get("workers", 3))
    prov = MODELS.get(model or task.get("model", "flash"), model or task.get("model", "flash"))
    if offpeak:
        from .__main__ import wait_offpeak
        wait_offpeak(f"{prov}:{n}")
    run_dir = run_mod.run(t.name, job_name, "Task", f"{prov}:{n}", run_id, concurrency, target_override=t)
    print("check:")
    check_mod.check(run_dir)
    report_mod.report(run_dir)
    summarise(run_dir)
    return run_dir


def summarise(run_dir: Path) -> Path:
    """summary.md: what each worker did, best first, with its patch's size and path."""
    gens = {g["gid"]: g for g in json.loads((run_dir / "generators.json").read_text())}
    chk = json.loads((run_dir / "check.json").read_text())
    rows = chk["generators"] if isinstance(chk, dict) and "generators" in chk else chk

    def score(r: dict) -> tuple:
        h = r.get("held_out") or {}
        total = (h.get("passed") or 0) + (h.get("failed") or 0)
        return (r.get("survived", False), (h.get("passed", 0) / total) if total else 0.0)

    out = [f"# {run_dir.name}", ""]
    task = config.load_toml(run_dir / "task.toml")
    out += [f"Task: {task['title']}", ""]
    total_cost = sum(g.get("cost_usd") or 0 for g in gens.values())
    survived = [r for r in rows if r.get("survived")]
    out += [f"{len(survived)} of {len(rows)} workers passed every check; estimated cost ${total_cost:.2f} "
            "(the estimate runs high; real spend has been about 1.2 cents per million tokens).", ""]
    for r in sorted(rows, key=score, reverse=True):
        g = gens.get(r["gid"], {})
        h = r.get("held_out")
        held = f", held-out {h['passed']}/{h['passed'] + h['failed']}" if h else ""
        head = f"## {r['gid']} ({g.get('provider')}): " + ("passed" if r.get("survived") else f"rejected: {r.get('reason')}")
        out += [head + held, ""]
        out.append(f"- turns {g.get('turns')}, {g.get('seconds')} s, ${g.get('cost_usd')}")
        m = r.get("manifest") or {}
        if m.get("intent"):
            out.append(f"- says: {m['intent']}")
        for req in m.get("requests", []) or []:
            if isinstance(req, str) and req.strip() and not req.startswith("<"):
                out.append(f"- asks: {req}")
        patch = run_dir / "gens" / r["gid"] / ".swarm" / "patch.diff"
        if r.get("survived") and patch.is_file():
            text = patch.read_text()
            adds = sum(1 for l in text.splitlines() if l.startswith("+") and not l.startswith("+++"))
            dels = sum(1 for l in text.splitlines() if l.startswith("-") and not l.startswith("---"))
            out.append(f"- patch: `{patch.relative_to(config.ROOT)}` (+{adds} -{dels}); "
                       f"apply with `python3 -m swarm task apply {run_dir.relative_to(config.ROOT)} {r['gid']}`")
        out.append("")
    path = run_dir / "summary.md"
    path.write_text("\n".join(out))
    print(f"summary: {path.relative_to(config.ROOT)}")
    return path


def apply(run_dir: Path, gid: str, to: Path | None = None) -> None:
    """Apply a worker's patch to the agent's own checkout (three-way, so it lands on a
    branch that moved since), leaving it uncommitted for the agent to review."""
    task = config.load_toml(run_dir / "task.toml")
    t = config.target(task.get("target", "arpg-game"))
    dest = to or (t.repo_path() or Path(task.get("repo", t.repo)))
    patch = (run_dir / "gens" / gid / ".swarm" / "patch.diff").resolve()
    if not patch.is_file():
        raise SystemExit(f"{gid} has no patch (did it pass?)")
    r = subprocess.run(["git", "apply", "-3", str(patch)], cwd=dest, text=True, capture_output=True)
    print((r.stdout + r.stderr).strip() or f"applied {gid}'s patch to {dest}, uncommitted")
    if r.returncode != 0:
        raise SystemExit(1)
