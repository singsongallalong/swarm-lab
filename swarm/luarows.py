"""Find named rows in the game's Luau data tables, as text.

A row is a line `<indent>Name = {` and everything up to its matching `}` (with a
trailing comma), plus the comment lines directly above it at the same indent. Strings
and comments are skipped when counting braces. This is enough for the data files the
swarm touches (SkillVisuals, DrawnEffects, Emitters); it is not a Luau parser.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

ROW_START = re.compile(r"^(?P<indent>[ \t]+)(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{")
# A row added after its table as a field assignment at the top of the file
# (`Sculpts.field_well = {`, as Sculpts.luau does after its table): named by the field.
DOTTED_START = re.compile(r"^(?P<indent>)[A-Za-z_][A-Za-z0-9_]*\.(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*\{")


@dataclass
class Row:
    name: str
    start: int  # index of the first character, comments above included
    end: int  # index just past the row's closing brace and trailing comma/newline
    indent: str

    def text(self, src: str) -> str:
        return src[self.start : self.end]


def _close(src: str, i: int) -> int:
    """Given src[i] == '{', return the index just past its matching '}'."""
    depth = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c == "-" and src.startswith("--", i):
            if src.startswith("--[[", i) or src.startswith("--[=[", i):
                j = src.find("]]", i)
                i = n if j < 0 else j + 2
            else:
                j = src.find("\n", i)
                i = n if j < 0 else j
            continue
        if c in "\"'":
            j = i + 1
            while j < n and src[j] != c:
                j += 2 if src[j] == "\\" else 1
            i = j + 1
            continue
        if c == "[" and (src.startswith("[[", i) or src.startswith("[=[", i)):
            j = src.find("]]", i)
            i = n if j < 0 else j + 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced braces")


def rows(src: str) -> list[Row]:
    """Every row at any indent, outermost first in file order. Nested fields that are
    tables (`size = { 0.7, 1.8 }`) are skipped because they sit inside a found row."""
    out: list[Row] = []
    lines = src.splitlines(keepends=True)
    offsets = []
    pos = 0
    for line in lines:
        offsets.append(pos)
        pos += len(line)
    k = 0
    while k < len(lines):
        m = ROW_START.match(lines[k]) or DOTTED_START.match(lines[k])
        if not m:
            k += 1
            continue
        brace = offsets[k] + m.end() - 1
        end = _close(src, brace)
        # trailing comma and the rest of the closing line
        nl = src.find("\n", end)
        end = len(src) if nl < 0 else nl + 1
        # comment lines directly above, at the same indent
        indent = m.group("indent")
        first = k
        while first > 0 and lines[first - 1].startswith(indent + "--") and (indent or not lines[first - 1].startswith("---")):
            first -= 1
        out.append(Row(m.group("name"), offsets[first], end, indent))
        # skip to the line after this row
        while k < len(lines) and offsets[k] < end:
            k += 1
    return out


def top_rows(src: str) -> dict[str, Row]:
    """Rows directly inside the file's tables: the shallowest indent that has rows,
    keyed by name. A name used twice keeps its first row."""
    found = rows(src)
    out: dict[str, Row] = {}
    # rows() only returns outermost rows, but a file's top-level `local X = {` line has
    # no indent and is not matched, so its children are what we get.
    for r in found:
        out.setdefault(r.name, r)
    return out


def get(src: str, name: str) -> str:
    r = top_rows(src).get(name)
    if r is None:
        raise KeyError(name)
    return r.text(src)


def without(src: str, names: set[str]) -> str:
    """The file with the named rows cut out, for comparing everything else."""
    cut = sorted((r for r in top_rows(src).values() if r.name in names), key=lambda r: r.start)
    out, pos = [], 0
    for r in cut:
        out.append(src[pos : r.start])
        pos = r.end
    out.append(src[pos:])
    return "".join(out)


def between(src: str, start_marker: str, end_marker: str) -> str:
    """From the line holding start_marker up to and including the line holding
    end_marker."""
    i = src.find(start_marker)
    if i < 0:
        raise KeyError(start_marker)
    i = src.rfind("\n", 0, i) + 1
    j = src.find(end_marker, i)
    if j < 0:
        raise KeyError(end_marker)
    nl = src.find("\n", j)
    return src[i : len(src) if nl < 0 else nl + 1]
