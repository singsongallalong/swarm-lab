--!strict
-- Crowwood's colours (the crow-haunted birch wood in first snow, swarm-lab palettes job):
-- pale birch bark and one blue-white snowed path laid over near-black leaf mould, dark
-- green undergrowth, a faded oxblood of rowan berries and tied ribbons as the one accent,
-- cold low mist. The ground is darker than the snow so the first snow and the pale bark
-- define the place at night, not the moss.
local Palette = require("../../systems/Palette")

local crowwood: Palette.Palette = {
	name = "PaletteCrowwood",
	about = "A crow-haunted birch wood in first snow: pale bark and thin snow over dark leaf mould, berries and old ribbons the only colour.",
	words = "pale grey birch bark, thin blue-white snow on the trodden path over near-black mossy leaf mould, dark green birch undergrowth, a faded oxblood of rowan berries and tied ribbons as the one accent, cold low mist, desaturated, matte, no highlights",
	walk = { material = "Ground", color = { 50, 53, 45 } },
	road = { material = "Snow", color = { 84, 88, 89 } },
	earth = { material = "Mud", color = { 30, 29, 26 } },
	rock = { material = "Basalt", color = { 38, 39, 36 } },
	far = { material = "LeafyGrass", color = { 33, 38, 31 } },
	bed = { material = "Ice", color = { 28, 33, 32 } },
	abyss = { material = "Slate", color = { 12, 13, 12 } },
	rockTint = { 80, 84, 86 },
	trim = { wood = { 94, 92, 86 }, metal = { 44, 46, 48 }, foliage = { 38, 42, 34 } },
	accent = {
		color = { 88, 51, 47 },
		carriers = "rowan berries, ribbons tied to branches, berry stains on the pale bark, rags left on the crows' stones",
	},
	lamp = { 255, 170, 100 },
	mist = { 140, 146, 154 },
	lighting = "mood",
}

return crowwood
