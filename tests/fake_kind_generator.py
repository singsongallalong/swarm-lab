#!/usr/bin/env python3
"""A stand-in generator for the kinds job: writes a real drafted kind (a two-armed
frost spiral) against the real game, so a run exercises the contract spec, the purity
check, lint and format. Its worktree's name picks what it gets wrong:

    g00, g05+  good: the spiral, registered, with a row and the skill pointed at it
    g01        impure: its module calls task.wait
    g02        breaks the contract: a piece goes missing late in the look
    g03        tampers with the registry: changes the reference kind's line
    g04        requires a module that isn't on the job's list
"""
import json
import pathlib
import re
import subprocess

wt = pathlib.Path.cwd()
gid = wt.name
pack = (wt / ".swarm" / "PACK.md").read_text()
skill = re.search(r"# Task: invent a new kind of area look for (\w+)", pack).group(1)
name = f"{skill}Spiral"
look = f"{skill}SpiralLook"

MODULE = '''--!strict
-- Frost spirals: arms of thin ice winding out from the origin to the area's
-- edge, each piece appearing as the arm's head passes it, then fading.
local AreaLayout = require("../AreaLayout")
local DraftedTypes = require("../../DraftedTypes")
local SculptMath = require("../SculptMath")
local SkillTypes = require("../../SkillTypes")

type Piece = DraftedTypes.Piece
type AreaShape = SkillTypes.AreaShape

local Spiral = {}

Spiral.about = "Arms of thin ice winding out from the origin to the edge, then fading."

local function point(look: any, shape: AreaShape, arm: number, s: number): (number, number)
	local half = AreaLayout.halfAngle(shape)
	local turn = 2 * math.pi * (arm / look.arms + look.turns * s)
	-- A circle winds all the way round; a cone sways inside its width.
	local heading = if half >= math.pi then turn else half * math.sin(turn)
	local d = shape.radius * (0.15 + 0.85 * s)
	return math.cos(heading) * d, math.sin(heading) * d
end

function Spiral.count(look: any): number
	return math.floor(look.arms) * math.floor(look.segments)
end

function Spiral.lasts(look: any, _shape: AreaShape): number
	return look.sweep + look.hold + look.fade
end

function Spiral.plan(look: any, _shape: AreaShape, rng: Random): { number }
	local lift: { number } = {}
	for i = 1, Spiral.count(look) do
		lift[i] = rng:NextNumber(0.6, 1)
	end
	return lift
end

function Spiral.pose(look: any, shape: AreaShape, plan: { number }, age: number, color: { number }): { Piece }
	local out: { Piece } = {}
	local n = math.floor(look.segments)
	for arm = 0, math.floor(look.arms) - 1 do
		for i = 1, n do
			local s0, s1 = (i - 1) / n, i / n
			local f0, r0 = point(look, shape, arm, s0)
			local f1, r1 = point(look, shape, arm, s1)
			local df, dr = f1 - f0, r1 - f0 * 0 - r0
			local length = math.max(0.1, math.sqrt(df * df + dr * dr))
			local t = age - s0 * look.sweep
			local o = 0
			if t >= 0 and t < look.hold then
				o = 1
			elseif t >= look.hold and t < look.hold + look.fade then
				o = 1 - (t - look.hold) / look.fade
			end
			local h = look.height * plan[arm * n + i] * (0.5 + 0.5 * s1)
			table.insert(out, {
				shape = "Block",
				size = { length, h, look.width },
				position = { (r0 + r1) / 2, h / 2, -(f0 + f1) / 2 },
				rotation = SculptMath.alongX({ dr, 0, -df }),
				color = { color[1], color[2], color[3] },
				material = "Neon",
				transparency = 1 - 0.75 * o,
			})
		end
	end
	return out
end

return table.freeze(Spiral)
'''

if gid == "g01":
    MODULE = MODULE.replace("local out: { Piece } = {}\n", "local out: { Piece } = {}\n\ttask.wait()\n", 1)
if gid == "g02":
    MODULE = MODULE.replace("\treturn out\nend\n\nreturn table.freeze", "\tif age > 0.4 then\n\t\ttable.remove(out)\n\tend\n\treturn out\nend\n\nreturn table.freeze", 1)
if gid == "g04":
    MODULE = MODULE.replace('local SculptMath = require("../SculptMath")', 'local SculptMath = require("../SculptMath")\nlocal Net = require("../../net/Remotes")', 1)

(wt / "src/shared/systems/drafted" / f"{name}.luau").write_text(MODULE)

reg = wt / "src/shared/systems/DraftedKinds.luau"
r = reg.read_text()
line = f'\tShardBloom = require("./drafted/ShardBloom"),\n'
r = r.replace(line, line + f'\t{name} = require("./drafted/{name}"),\n', 1)
if gid == "g03":
    r = r.replace('\tShardBloom = require("./drafted/ShardBloom"),\n', '\tShardBloom = require("./drafted/ShardBloom"), -- mine now\n', 1)
reg.write_text(r)

de = wt / "src/shared/data/DrawnEffects.luau"
d = de.read_text()
row = (
    f"\t{look} = {{\n"
    '\t\tkind = "Drafted",\n'
    '\t\tabout = "Two arms of thin ice winding out from the caster to the edge, then fading.",\n'
    f'\t\tlayout = "{name}",\n'
    "\t\tarms = 2,\n\t\tsegments = 12,\n\t\tturns = 0.9,\n\t\tsweep = 0.3,\n\t\thold = 0.25,\n\t\tfade = 0.3,\n"
    "\t\theight = 0.9,\n\t\twidth = 0.35,\n"
    '\t\temitter = "SlamDust",\n'
    "\t\tperPower = { height = 0.1, width = 0.06 },\n"
    "\t},\n"
)
d = d.replace("local area: { [string]: AreaLook } = {\n", "local area: { [string]: AreaLook } = {\n" + row, 1)
de.write_text(d)

sv = wt / "src/shared/data/SkillVisuals.luau"
v = sv.read_text()
v = re.sub(rf"(\t{skill} = \{{.*?areaLook = )\"\w+\"", rf'\1"{look}"', v, count=1, flags=re.S)
sv.write_text(v)

subprocess.run("stylua src/shared/systems/drafted", shell=True, check=False)
cmds = re.search(r"Render your look.*?```\n(.*?)```", pack, re.S).group(1)
for cmd in cmds.splitlines():
    if cmd.strip() and not cmd.startswith("#"):
        subprocess.run(cmd.replace("<YourLook>", look), shell=True, check=False)

(wt / ".swarm" / "manifest.json").write_text(json.dumps({
    "skill": skill, "look": look, "layout": name,
    "idea": "A spiral: arms that wind out from the caster, which no existing kind draws.",
    "rows_added": [look], "intent": f"Two frost arms winding to the edge ({gid}).",
    "renders": [f".swarm/out/area-{look}-r1.png"], "revisions": 0,
}))
print(json.dumps({"type": "result", "is_error": False, "num_turns": 11,
                  "usage": {"input_tokens": 30000, "cache_read_input_tokens": 400000, "output_tokens": 15000}}))
