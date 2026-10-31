"""swarm-lab command line: python3 -m swarm <command> ..."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import apply as apply_mod
from . import check as check_mod
from . import config, pack, report as report_mod, run as run_mod, sheet as sheet_mod


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="swarm", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pack", help="print a brief's context pack, built from the game repo as it is")
    p.add_argument("target"), p.add_argument("job"), p.add_argument("brief")
    p.add_argument("--repo", help="read the game from this path instead of target.toml's")
    p.add_argument("--out", help="write the pack here instead of printing it")
    p.add_argument("--figure", help="who wears it: a figure in targets/<target>/figures (comma list; none for none)")

    p = sub.add_parser("run", help="launch a swarm, then check, tile and report it")
    p.add_argument("target"), p.add_argument("job"), p.add_argument("brief")
    p.add_argument("--gens", required=True, help="providers and counts, e.g. deepseek:8,qwen:7")
    p.add_argument("--run-id")
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--dry-run", action="store_true", help="build worktrees and packs, call no model")
    p.add_argument("--no-specs", action="store_true", help="skip the specs in the check")
    p.add_argument("--figure", help="who wears it: overrides the brief's and job's figure (comma list; none for none)")
    p.add_argument("--offpeak", action="store_true",
                   help="wait, if need be, until the run can start and finish inside the providers' half-price hours")

    for name, help_ in [("check", "filter a run's generators"), ("sheet", "tile the survivors blind"),
                        ("report", "summarise a run and update the ledger")]:
        p = sub.add_parser(name, help=help_)
        p.add_argument("run_dir", type=Path)
        if name == "check":
            p.add_argument("--no-specs", action="store_true")

    p = sub.add_parser("apply", help="put a picked candidate on a branch in the game repo")
    p.add_argument("run_dir", type=Path), p.add_argument("letter")

    p = sub.add_parser("shelf", help="lay several kept candidates' added rows into the game repo's working tree")
    p.add_argument("run_dir", type=Path)
    p.add_argument("letters", nargs="*", help="the run's critic letters; or none, with --patches")
    p.add_argument("--into", type=Path, required=True, help="the game repo (its working tree is changed, not committed)")
    p.add_argument("--patches", type=Path, nargs="+", help="committed patches (library/.../patch.diff) instead of a run's worker trees; run_dir is then ignored")

    p = sub.add_parser("resume", help="continue a run's stopped generators, then check, tile and report it")
    p.add_argument("run_dir", type=Path)
    p.add_argument("--turns", type=int, default=30, help="more turns each (default 30)")
    p.add_argument("--concurrency", type=int, default=4)

    p = sub.add_parser("rework", help="send generators back with a critic's notes (critique/<gid>.md), then check, tile and report")
    p.add_argument("run_dir", type=Path)
    p.add_argument("--turns", type=int, default=40, help="turns each (default 40)")
    p.add_argument("--concurrency", type=int, default=6)

    p = sub.add_parser("task", help="hand a bounded task to a few DeepSeek workers (swarm/task.py)")
    tsub = p.add_subparsers(dest="task_cmd", required=True)
    tp = tsub.add_parser("run", help="run a task file: workers, checks, summary.md")
    tp.add_argument("task_file", type=Path)
    tp.add_argument("--workers", type=int)
    tp.add_argument("--model", choices=["flash", "pro"])
    tp.add_argument("--run-id")
    tp.add_argument("--offpeak", action="store_true")
    tp = tsub.add_parser("apply", help="apply a worker's patch to your checkout, uncommitted")
    tp.add_argument("run_dir", type=Path)
    tp.add_argument("gid")
    tp.add_argument("--to", type=Path)
    tp = tsub.add_parser("summary", help="rewrite a task run's summary.md")
    tp.add_argument("run_dir", type=Path)

    p = sub.add_parser("when", help="is it off-peak (half price) now, and when can a run of this length start and stay off-peak")
    p.add_argument("--provider", default="deepseek")
    p.add_argument("--minutes", type=int, default=0, help="the run's length (default: the provider's wall-time cap)")

    p = sub.add_parser("probe", help="check a provider works and can see images, with the settings generators get")
    p.add_argument("provider")
    p.add_argument("image", nargs="?", type=Path, default=config.ROOT / "tests" / "probe-heavedrocks.png")

    a = ap.parse_args(argv)
    if getattr(a, "run_dir", None) is not None:
        # Paths are reported relative to swarm-lab, so work from an absolute one.
        a.run_dir = a.run_dir.resolve()
    if a.cmd == "pack":
        t = config.target(a.target)
        j = config.job(t, a.job)
        repo = Path(a.repo) if a.repo else t.repo_path()
        if repo is None:
            sys.exit("target repo is a URL: pass --repo with a local checkout")
        brief = j.brief(a.brief)
        text = pack.build(j, brief, repo, config.figures(t, j, brief, a.figure))
        if a.out:
            Path(a.out).write_text(text)
            print(f"{a.out}: {len(text):,} chars (~{len(text) // 4:,} tokens)")
        else:
            print(text)
    elif a.cmd == "run":
        if a.offpeak and not a.dry_run:
            wait_offpeak(a.gens)
        run_dir = run_mod.run(a.target, a.job, a.brief, a.gens, a.run_id, a.concurrency, a.dry_run, figure=a.figure)
        if not a.dry_run:
            print("check:")
            res = check_mod.check(run_dir, specs=not a.no_specs)
            if res["survivors"]:
                sheet_mod.sheet(run_dir)
            report_mod.report(run_dir)
            print(f"\nNext: the orchestrator reads {run_dir.relative_to(config.ROOT)}/select.md")
    elif a.cmd == "shelf":
        from . import shelf
        lines = shelf.shelf_patches(a.patches, a.into) if a.patches else shelf.shelf(a.run_dir, a.letters, a.into)
        for line in lines:
            print(line)
    elif a.cmd == "check":
        check_mod.check(a.run_dir, specs=not a.no_specs)
    elif a.cmd == "sheet":
        sheet_mod.sheet(a.run_dir)
    elif a.cmd == "report":
        report_mod.report(a.run_dir)
    elif a.cmd == "apply":
        apply_mod.apply(a.run_dir, a.letter)
    elif a.cmd == "resume":
        run_mod.resume(a.run_dir, a.turns, a.concurrency)
        print("check:")
        res = check_mod.check(a.run_dir)
        if res["survivors"]:
            sheet_mod.sheet(a.run_dir)
        report_mod.report(a.run_dir)
    elif a.cmd == "rework":
        run_mod.rework(a.run_dir, a.turns, a.concurrency)
        print("check:")
        res = check_mod.check(a.run_dir)
        if res["survivors"]:
            sheet_mod.sheet(a.run_dir)
        report_mod.report(a.run_dir)
    elif a.cmd == "task":
        from . import task as task_mod
        if a.task_cmd == "run":
            task_mod.run(a.task_file.resolve(), a.run_id, a.workers, a.model, a.offpeak)
        elif a.task_cmd == "apply":
            task_mod.apply(a.run_dir, a.gid, a.to)
        else:
            task_mod.summarise(a.run_dir)
    elif a.cmd == "when":
        from datetime import datetime, timezone
        from . import offpeak
        prov = config.providers()[a.provider]
        print(offpeak.describe(prov, datetime.now(timezone.utc), a.minutes or prov.timeout_s // 60))
    elif a.cmd == "probe":
        probe(a.provider, a.image.resolve())


def wait_offpeak(gens: str) -> None:
    """Sleep until every provider in `gens` is off-peak for its whole wall-time cap."""
    import time
    from datetime import datetime, timezone
    from . import offpeak
    provs = config.providers()
    names = {part.split(":")[0] for part in gens.split(",") if part}
    while True:
        now = datetime.now(timezone.utc)
        starts = [offpeak.next_clear(provs[n], now, provs[n].timeout_s // 60) for n in names if n in provs]
        start = max(starts) if starts else now
        if start <= now:
            return
        print(f"waiting for half-price hours: starting at {start.astimezone().strftime('%a %H:%M %Z')}", flush=True)
        time.sleep(min((start - now).total_seconds(), 3600))


def probe(name: str, image: Path) -> None:
    """One short call through the same runtime and environment a generator gets."""
    import json
    import subprocess

    provs = config.providers()
    if name not in provs:
        sys.exit(f"unknown provider {name!r}; known: {', '.join(provs)}")
    p = provs[name]
    if p.key_env and not p.key():
        sys.exit(f"{p.key_env} is empty: put it in {config.ROOT / '.env'}")
    if not image.is_file():
        sys.exit(f"no image at {image}")
    env = run_mod.runtime_env(config.Target(name="probe", dir=config.ROOT, repo="", ref=""), p)
    question = (f"Read the image {image} and describe what it shows in two sentences. "
                "If you cannot see the image, say exactly: I CANNOT SEE IMAGES.")
    argv = ["claude", "-p", question, "--output-format", "json", "--max-turns", "3", "--model", p.model,
            "--allowedTools", "Read"]
    print(f"probing {name} ({p.model}) at {p.base_url or 'Anthropic'} ...", flush=True)
    r = subprocess.run(argv, env=env, text=True, capture_output=True, timeout=300)
    try:
        res = json.loads(r.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        sys.exit(f"no JSON back (exit {r.returncode}):\n{(r.stdout + r.stderr).strip()[-1500:]}")
    print("\n" + str(res.get("result", "")).strip() + "\n")
    usage = res.get("usage", {}) or {}
    print(f"turns {res.get('num_turns')}, tokens {run_mod.total_tokens(usage):,}, about ${p.cost(usage):.4f}")
    text = str(res.get("result", "")).lower()
    if res.get("is_error") or r.returncode != 0:
        sys.exit("FAILED: the call errored (above).")
    if "cannot see images" in text:
        sys.exit("FAILED: the model can't see images through this endpoint; generators would be blind.")
    print("OK if the description mentions rocks or slabs heaving up around a red post. "
          "If it describes something else, the image didn't reach the model.")


if __name__ == "__main__":
    main()
