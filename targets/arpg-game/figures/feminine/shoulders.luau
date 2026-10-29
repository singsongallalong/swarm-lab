--!strict
-- The feminine figure's shoulder check: how far a set's chest pieces stand out
-- past the shoulders, measured on the game's reference body.
--
-- Copied into each worktree as .swarm/figure/feminine/shoulders.luau and run
-- from the worktree root:
--
--   lune run .swarm/figure/feminine/shoulders <Prefix> [maxOut] [maxRise]
--
-- Every look whose name starts with <Prefix> is measured. "Out" is how far a
-- piece reaches sideways past the side of the torso or the outside of the upper
-- arm; "rise" is how far a piece out at the shoulders (not a collar at the neck)
-- stands above the top of the torso or the arm. Pieces are treated as boxes, so
-- a turned cylinder or ball counts a little wider than it draws. Exits 1 when a
-- look is over either limit.
local process = require("@lune/process")

local ArmourFit = require("../../../src/shared/data/ArmourFit")
local ArmourLook = require("../../../src/shared/systems/ArmourLook")
local ArmourLooks = require("../../../src/shared/data/ArmourLooks")
local SculptMath = require("../../../src/shared/systems/SculptMath")

-- Half the reference neck's width: a piece that stays inside it is a collar,
-- and may rise as high as it likes.
local NECK = 0.6

local prefix = process.args[1]
if prefix == nil then
	print("usage: lune run .swarm/figure/feminine/shoulders <Prefix> [maxOut] [maxRise]")
	process.exit(2)
end
local maxOut = tonumber(process.args[2]) or 0.15
local maxRise = tonumber(process.args[3]) or 0.15

local sizes: { [string]: { number } } = {}
for part, size in ArmourFit.reference do
	if ArmourFit.sided[part] then
		sizes["Right" .. part], sizes["Left" .. part] = size, size
	else
		sizes[part] = size
	end
end

-- Half the piece's extent along the body part's X and Y, once turned.
local function halfExtents(size: { number }, turn: { number }): (number, number)
	local m = SculptMath.mul(SculptMath.rotX(turn[1]), SculptMath.mul(SculptMath.rotY(turn[2]), SculptMath.rotZ(turn[3])))
	local hx = (math.abs(m[1]) * size[1] + math.abs(m[2]) * size[2] + math.abs(m[3]) * size[3]) / 2
	local hy = (math.abs(m[4]) * size[1] + math.abs(m[5]) * size[2] + math.abs(m[6]) * size[3]) / 2
	return hx, hy
end

local torso = ArmourFit.reference.UpperTorso
local arm = ArmourFit.reference.UpperArm

local names: { string } = {}
for name in ArmourLooks :: { [string]: any } do
	if string.sub(name, 1, #prefix) == prefix then
		table.insert(names, name)
	end
end
table.sort(names)
if #names == 0 then
	print(`no looks start with {prefix}`)
	process.exit(2)
end

local failed = false
for _, name in names do
	local out, rise = 0, 0
	local outWhy, riseWhy = "", ""
	for i, p in ArmourLook.place((ArmourLooks :: any)[name], sizes) do
		local hx, hy = halfExtents(p.size, p.turn)
		local o, r
		if p.bodyPart == "UpperTorso" then
			o = math.abs(p.at[1]) + hx - torso[1] / 2
			r = if math.abs(p.at[1]) + hx > NECK then p.at[2] + hy - torso[2] / 2 else 0
		elseif p.bodyPart == "RightUpperArm" then
			o = p.at[1] + hx - arm[1] / 2
			r = p.at[2] + hy - arm[2] / 2
		end
		if o and o > out then
			out, outWhy = o, `{p.bodyPart} piece {i}, a {p.shape}`
		end
		if r and r > rise then
			rise, riseWhy = r, `{p.bodyPart} piece {i}, a {p.shape}`
		end
	end
	local bad = out > maxOut + 1e-6 or rise > maxRise + 1e-6
	failed = failed or bad
	print(
		string.format(
			"%s %s: out %.2f (limit %.2f%s), rise %.2f (limit %.2f%s)",
			if bad then "OVER" else "ok  ",
			name,
			out,
			maxOut,
			if out > maxOut + 1e-6 then ", " .. outWhy else "",
			rise,
			maxRise,
			if rise > maxRise + 1e-6 then ", " .. riseWhy else ""
		)
	)
end
if failed then
	print("Shoulders too broad for this figure: narrow or lower the pieces named, and carry the width at the waist and hem.")
	process.exit(1)
end
