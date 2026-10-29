"""Put a picked candidate on a branch in the real game repo.

    python3 -m swarm apply runs/<run> <letter>

Makes branch `swarm/<run>-<letter>` from the run's base commit in the target's local
repo and applies the candidate's patch there, so the game's own effect-critic-loop
can take over. Nothing is committed or pushed: the session that runs the critic loop
owns that, with the game's usual pass number and stream.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from . import config


def apply(run_dir: Path, letter: str) -> str:
    meta = json.loads((run_dir / "meta.json").read_text())
    key = json.loads((run_dir / "key.json").read_text())
    if letter not in key:
        raise SystemExit(f"no candidate {letter!r} in this run (have {', '.join(sorted(key))})")
    gid = key[letter]["gid"]
    patch = (run_dir / "gens" / gid / ".swarm" / "patch.diff").resolve()
    t = config.target(meta["target"])
    repo = t.repo_path()
    branch = f"swarm/{meta['run']}-{letter}"
    if repo is None:
        msg = (f"The target repo is a URL, so do this in your clone:\n"
               f"  git switch -c {branch} {meta['base']}\n  git apply {patch}")
        print(msg)
        return msg

    def git(*args):
        return subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True)

    if git("status", "--porcelain", "--untracked-files=no").stdout.strip():
        raise SystemExit(f"{repo} has uncommitted changes; commit or stash them first")
    # The base clone may hold a commit the real repo hasn't fetched yet.
    if git("cat-file", "-e", meta["base"]).returncode != 0:
        git("fetch", "--quiet", str(run_dir / "base"), meta["base"])
    r = git("switch", "-c", branch, meta["base"])
    if r.returncode != 0:
        raise SystemExit(r.stderr.strip())
    r = git("apply", str(patch))
    if r.returncode != 0:
        raise SystemExit(f"the patch didn't apply: {r.stderr.strip()}")
    msg = (f"{repo.name}: on branch {branch} with candidate {letter}'s rows applied (uncommitted). "
           f"Run the effect-critic-loop from here.")
    print(msg)
    return msg
