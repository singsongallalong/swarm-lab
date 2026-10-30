"""Bring several kept candidates into the game repo at once.

`swarm apply` puts one candidate on a branch. A kit run's shelf is many candidates, and each
one added rows at the same places (the end of `Sculpts`, the end of `recipes`, the end of the
catalog), so applying their patches one after another conflicts. This takes each candidate's
**insertions** (every job file a kit or zones job touches is add-only) and lays them into the
game repo's working tree after the same anchor line, one candidate after another. Nothing is
committed. The builder formats, runs the specs and commits.

    python3 -m swarm shelf runs/<run> A C F --into ../arpg-game
"""

from __future__ import annotations

import difflib
import json
import subprocess
from pathlib import Path


def _inserts(before: list[str], after: list[str]) -> list[tuple[int, list[str]]]:
    """(index in `before` to insert at, lines) for each insertion; anything else is an error."""
    out = []
    sm = difflib.SequenceMatcher(a=before, b=after, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag != "insert":
            raise ValueError(f"not add-only near line {i1 + 1}: {tag}")
        out.append((i1, after[j1:j2]))
    return out


def _changed_files(gen: Path) -> list[str]:
    """The game files a candidate changed or made: modified tracked files, and new files
    under src/ (worktrees also hide the game's CLAUDE.md and link shared folders in, which
    aren't the candidate's work)."""
    r = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AM", "HEAD", "--", "src"], cwd=gen, text=True,
                       capture_output=True, check=True)
    new = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", "src"], cwd=gen, text=True,
                         capture_output=True, check=True)
    names = [n for n in (r.stdout + new.stdout).splitlines() if n and not n.startswith(".swarm")]
    return sorted(set(names))


def shelf(run_dir: Path, letters: list[str], into: Path) -> list[str]:
    key = json.loads((run_dir / "key.json").read_text())
    report = []
    for letter in letters:
        gid = key[letter]["gid"]
        gen = run_dir / "gens" / gid
        for rel in _changed_files(gen):
            cand = (gen / rel).read_text(encoding="utf-8").splitlines(keepends=True)
            base_text = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=gen, text=True, capture_output=True)
            target = into / rel
            if base_text.returncode != 0:
                # A new file the candidate made: copy it, unless the game already has one.
                if target.exists():
                    raise SystemExit(f"{letter} ({gid}): {rel} is new in the candidate but exists in {into}")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("".join(cand), encoding="utf-8")
                report.append(f"{letter} {gid}: new file {rel}")
                continue
            base = base_text.stdout.splitlines(keepends=True)
            try:
                inserts = _inserts(base, cand)
            except ValueError as e:
                raise SystemExit(f"{letter} ({gid}): {rel}: {e}")
            lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
            # Insert from the bottom up so earlier anchors keep their places. An insertion's
            # anchor is the base line before it; it lands right after that line in the target,
            # ahead of anything an earlier candidate put there.
            for at, block in sorted(inserts, key=lambda x: -x[0]):
                if at == 0:
                    pos = 0
                else:
                    anchor = base[at - 1]
                    nth = base[:at].count(anchor)
                    seen, pos = 0, None
                    for k, line in enumerate(lines):
                        if line == anchor:
                            seen += 1
                            if seen == nth:
                                pos = k + 1
                                break
                    if pos is None:
                        raise SystemExit(f"{letter} ({gid}): {rel}: anchor {anchor.strip()[:60]!r} not in {into}")
                lines[pos:pos] = block
            target.write_text("".join(lines), encoding="utf-8")
            report.append(f"{letter} {gid}: {sum(len(b) for _, b in inserts)} lines into {rel}")
    return report
