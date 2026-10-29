#!/usr/bin/env python3
"""A stand-in generator for the armour job: writes a real four-piece set against the
real game, so a run exercises the look specs, the part budget, the registry and catalog
rules, purity, lint and format. Its worktree's name picks what it gets wrong:

    g00, g04+  good: four looks, registered, catalogued, formatted
    g01        over budget: a chest of 34 parts
    g02        edits an existing look's catalog row
    g03        a piece on a body part its slot may not cover
"""
import json
import pathlib
import re
import subprocess

wt = pathlib.Path.cwd()
gid = wt.name
pack = (wt / ".swarm" / "PACK.md").read_text()
p = re.search(r"# Task: design the (\w+) armour set", pack).group(1)

HIDE = "{ 96, 74, 54 }"
FUR = "{ 88, 80, 70 }"


def look(name, slot, parts, hides=False):
    body = "\n".join(f"\t\t{x}," for x in parts)
    extra = "\thidesHair = true,\n" if hides else ""
    return f'''--!strict
-- A stand-in look for swarm-lab's tests.
local ArmourLookTypes = require("../../ArmourLookTypes")
local Kit = require("./Kit")

local c = Kit.colors
local HIDE = {HIDE}
local FUR = {FUR}
local _ = {{ c, HIDE, FUR }} -- every look names all three, so lint sees each used

local look: ArmourLookTypes.ArmourLook = {{
\tname = "{name}",
\tslot = "{slot}",
{extra}\tparts = {{
{body}
\t}},
}}

return look
'''


chest_parts = [
    'Kit.box("UpperTorso", { 2.1, 1.7, 1.1 }, { 0, 0, 0 }, "Leather", HIDE)',
    'Kit.box("UpperTorso", { 2.4, 0.5, 1.3 }, { 0, 0.7, 0 }, "Fabric", FUR)',
    'Kit.box("UpperArm", { 1.1, 0.5, 1.1 }, { 0, 0.4, 0 }, "Fabric", FUR)',
    'Kit.box("LowerTorso", { 2.1, 0.3, 1.1 }, { 0, 0.3, 0 }, "Leather", c.leatherDark)',
]
if gid == "g01":
    chest_parts += [f'Kit.box("UpperTorso", {{ 0.2, 0.2, 0.1 }}, {{ {(-0.9 + i * 0.06):.2f}, -0.5, -0.56 }}, "Metal", c.iron)' for i in range(30)]
helm_on = "UpperArm" if gid == "g03" else "Head"
looks = {
    f"{p}Helm": look(f"{p}Helm", "Helm", [f'Kit.box("{helm_on}", {{ 1.3, 0.6, 1.3 }}, {{ 0, 0.35, 0 }}, "Fabric", FUR)',
                                        'Kit.wedge("Head", { 0.2, 0.8, 0.3 }, { 0.6, 0.8, 0 }, "Slate", c.bone, { 0, 0, -20 })'], hides=True),
    f"{p}Chest": look(f"{p}Chest", "Chest", chest_parts),
    f"{p}Gloves": look(f"{p}Gloves", "Gloves", ['Kit.box("LowerArm", { 1.08, 0.9, 1.08 }, { 0, -0.1, 0 }, "Leather", HIDE)']),
    f"{p}Boots": look(f"{p}Boots", "Boots", ['Kit.box("LowerLeg", { 1.08, 1.1, 1.08 }, { 0, -0.1, 0 }, "Fabric", FUR)',
                                          'Kit.box("Foot", { 1.08, 0.5, 1.4 }, { 0, -0.1, -0.15 }, "Leather", HIDE)']),
}
for name, text in looks.items():
    (wt / "src/shared/data/armourLooks" / f"{name}.luau").write_text(text)

reg = wt / "src/shared/data/ArmourLooks.luau"
r = reg.read_text()
anchor = 'local BoneTalisman = require("./armourLooks/BoneTalisman")\n'
r = r.replace(anchor, anchor + "".join(f'local {n} = require("./armourLooks/{n}")\n' for n in looks), 1)
table_anchor = "\tBoneTalisman = BoneTalisman,\n"
r = r.replace(table_anchor, table_anchor + "".join(f"\t{n} = {n},\n" for n in looks), 1)
reg.write_text(r)

gear = wt / "src/shared/data/catalog/Gear.luau"
g = gear.read_text()
anchor = '\t-- Offhands (A020), worn on the left forearm and hand\n'
g = g.replace(anchor, "".join(f'\t["armour:{n}"] = row("A barbarian\'s {n[len(p):].lower()} of hide and fur."),\n' for n in looks) + anchor, 1)
if gid == "g02":
    g = g.replace('row("A plain iron cap.")', 'row("A plain iron cap, now mine.")', 1)
gear.write_text(g)

subprocess.run("stylua src/shared/data/armourLooks src/shared/data/ArmourLooks.luau src/shared/data/catalog/Gear.luau", shell=True, check=False)
cmds = re.search(r"Render your set.*?```\n(.*?)```", pack, re.S).group(1)
set_names = ",".join(looks)
for cmd in cmds.splitlines():
    if cmd.strip():
        subprocess.run(cmd.replace("<YourLook>", set_names), shell=True, check=False)

(wt / ".swarm" / "manifest.json").write_text(json.dumps({
    "skill": p, "look": set_names, "rows_added": list(looks),
    "intent": f"A stand-in hide-and-fur set ({gid}).",
    "renders": [".swarm/out/armour-set-r1.png"], "revisions": 0,
}))
print(json.dumps({"type": "result", "is_error": False, "num_turns": 9,
                  "usage": {"input_tokens": 30000, "cache_read_input_tokens": 300000, "output_tokens": 12000}}))
