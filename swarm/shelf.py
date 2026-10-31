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


def _parse_patch(text: str) -> dict[str, dict]:
    """A unified diff of add-only changes, as {path: {"new": [lines]} or {"hunks": [...]}}.
    Each hunk is (old_start, [(anchor_before, [added lines])]): the context line right
    before each run of added lines (None when the run opens the hunk) and the run."""
    files: dict[str, dict] = {}
    cur = None
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("diff --git "):
            cur = None
        elif line.startswith("--- "):
            old = line[4:].strip()
            new = lines[i + 1][4:].strip()
            path = new[2:] if new.startswith("b/") else new
            cur = files.setdefault(path, {"new": [] if old == "/dev/null" else None, "hunks": []})
            i += 1
        elif line.startswith("@@") and cur is not None:
            start = int(line.split()[1].split(",")[0].lstrip("-"))
            runs, last_ctx, block = [], None, []
            i += 1
            while i < len(lines) and not lines[i].startswith(("@@", "diff --git ")):
                body = lines[i]
                if body.startswith("+"):
                    block.append(body[1:])
                elif body.startswith("-"):
                    raise SystemExit(f"{path}: the patch removes a line; shelf takes add-only patches")
                elif body.startswith("\\"):
                    pass
                else:
                    if block:
                        runs.append((last_ctx, block))
                        block = []
                    last_ctx = body[1:] if body.startswith(" ") else body
                i += 1
            if block:
                runs.append((last_ctx, block))
            if cur["new"] is not None:
                for _, b in runs:
                    cur["new"].extend(b)
            else:
                cur["hunks"].append((start, runs))
            continue
        i += 1
    return files


def shelf_patches(patches: list[Path], into: Path) -> list[str]:
    """Like `shelf`, from committed patches (library/<kind>/<Area>/<Name>/patch.diff) when the
    run's worker trees are gone: each added run of lines lands after the context line the
    patch shows before it, searched from the hunk's position onward."""
    report = []
    for patch in patches:
        files = _parse_patch(patch.read_text(encoding="utf-8"))
        name = patch.parent.name
        for rel, f in files.items():
            target = into / rel
            if f["new"] is not None:
                if target.exists():
                    raise SystemExit(f"{name}: {rel} is new in the patch but exists in {into}")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("".join(f["new"]), encoding="utf-8")
                report.append(f"{name}: new file {rel}")
                continue
            lines = target.read_text(encoding="utf-8").splitlines(keepends=True)
            added = 0
            # Bottom-up, so earlier positions hold.
            for start, runs in sorted(f["hunks"], key=lambda h: -h[0]):
                for anchor, block in reversed(runs):
                    pos = None
                    if anchor is None:
                        pos = max(0, start - 1)
                    else:
                        lo = max(0, start - 1 - 50)
                        for k in range(lo, len(lines)):
                            if lines[k] == anchor:
                                pos = k + 1
                                break
                        if pos is None:
                            for k in range(len(lines)):
                                if lines[k] == anchor:
                                    pos = k + 1
                                    break
                    if pos is None:
                        raise SystemExit(f"{name}: {rel}: anchor {anchor.strip()[:60]!r} not found in {into}")
                    lines[pos:pos] = block
                    added += len(block)
            target.write_text("".join(lines), encoding="utf-8")
            report.append(f"{name}: {added} lines into {rel}")
    return report
