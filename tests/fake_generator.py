#!/usr/bin/env python3
"""A stand-in generator for the end-to-end test. Its behaviour depends on its
worktree's name, so one run exercises every path through `check`:

    g00, g04, g06+  good: a new area row, the skill's row pointed at it, renders, manifest
    g01             also edits README.md (outside the allowlist)
    g02             changes the existing HeavedRocks row
    g03             writes no manifest
    g05             adds a row that makes the specs fail
"""
import json
import pathlib
import re
import subprocess
import sys

wt = pathlib.Path.cwd()
gid = wt.name
pack = (wt / ".swarm" / "PACK.md").read_text()
skill = re.search(r"# Task: a new \w+ look for (\w+)", pack).group(1)
look = f"{skill}Frost{gid[1:]}"
de = wt / "src/shared/data/DrawnEffects.luau"
sv = wt / "src/shared/data/SkillVisuals.luau"

# Every generator reads the stub, not the game's own CLAUDE.md.
assert "Generator" in (wt / "CLAUDE.md").read_text(), "the game's CLAUDE.md leaked into the worktree"

body = "BROKEN" if gid == "g05" else "frost"
row = (
    f"\t{look} = {{\n"
    f'\t\tkind = "Wave",\n'
    f'\t\tabout = "A ring of {body} bursting out to the edge.",\n'
    f"\t\ttravel = 50,\n\t\tsteps = 5,\n\t\tthickness = 0.4,\n\t\tfade = 0.2,\n"
    f"\t\tperPower = {{ thickness = 0.1 }},\n"
    f"\t}},\n"
)
src = de.read_text()
src = src.replace("local area: { [string]: AreaLook } = {\n", "local area: { [string]: AreaLook } = {\n" + row, 1)
if gid == "g02":
    src = src.replace("spacing = 2.6,", "spacing = 3.1,")
de.write_text(src)

v = sv.read_text()
v = re.sub(rf"(\t{skill} = \{{.*?areaLook = )\"\w+\"", rf'\1"{look}"', v, count=1, flags=re.S)
sv.write_text(v)

if gid == "g01":
    (wt / "README.md").write_text("I was not supposed to touch this.\n")

out = wt / ".swarm" / "out"
for cmd in (f"lune run scripts/areapreview HeavedRocks .swarm/out/ref-HeavedRocks.png",
            f"lune run scripts/areapreview {look} .swarm/out/area-{look}-r1.png"):
    subprocess.run(cmd, shell=True, check=True)

if gid != "g03":
    (wt / ".swarm" / "manifest.json").write_text(json.dumps({
        "skill": skill, "look": look, "rows_added": [look],
        "intent": f"A ring of frost bursting to the edge ({gid}).",
        "renders": [f".swarm/out/area-{look}-r1.png"], "revisions": 0,
    }))

# What `claude -p --output-format json` prints, so the cost report has numbers.
print(json.dumps({"type": "result", "is_error": False, "num_turns": 7,
                  "usage": {"input_tokens": 20000, "cache_read_input_tokens": 180000, "output_tokens": 9000}}))
