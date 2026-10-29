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

    p = sub.add_parser("run", help="launch a swarm, then check, tile and report it")
    p.add_argument("target"), p.add_argument("job"), p.add_argument("brief")
    p.add_argument("--gens", required=True, help="providers and counts, e.g. deepseek:8,qwen:7")
    p.add_argument("--run-id")
    p.add_argument("--concurrency", type=int, default=4)
    p.add_argument("--dry-run", action="store_true", help="build worktrees and packs, call no model")
    p.add_argument("--no-specs", action="store_true", help="skip the specs in the check")

    for name, help_ in [("check", "filter a run's generators"), ("sheet", "tile the survivors blind"),
                        ("report", "summarise a run and update the ledger")]:
        p = sub.add_parser(name, help=help_)
        p.add_argument("run_dir", type=Path)
        if name == "check":
            p.add_argument("--no-specs", action="store_true")

    p = sub.add_parser("apply", help="put a picked candidate on a branch in the game repo")
    p.add_argument("run_dir", type=Path), p.add_argument("letter")

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
        text = pack.build(j, j.brief(a.brief), repo)
        if a.out:
            Path(a.out).write_text(text)
            print(f"{a.out}: {len(text):,} chars (~{len(text) // 4:,} tokens)")
        else:
            print(text)
    elif a.cmd == "run":
        run_dir = run_mod.run(a.target, a.job, a.brief, a.gens, a.run_id, a.concurrency, a.dry_run)
        if not a.dry_run:
            print("check:")
            res = check_mod.check(run_dir, specs=not a.no_specs)
            if res["survivors"]:
                sheet_mod.sheet(run_dir)
            report_mod.report(run_dir)
            print(f"\nNext: the orchestrator reads {run_dir.relative_to(config.ROOT)}/select.md")
    elif a.cmd == "check":
        check_mod.check(a.run_dir, specs=not a.no_specs)
    elif a.cmd == "sheet":
        sheet_mod.sheet(a.run_dir)
    elif a.cmd == "report":
        report_mod.report(a.run_dir)
    elif a.cmd == "apply":
        apply_mod.apply(a.run_dir, a.letter)
    elif a.cmd == "probe":
        probe(a.provider, a.image.resolve())


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
