--!strict
-- Bone Plain's colours (a bone desert, the dead giant's plain): the ground is the
-- giant's own dust, a warm chalky bone-grey kept just under the bible's value cap
-- rather than the moor's brown heath or Rimeholt's blue snow; dark trodden earth
-- and a paler far land give the road and the rim their steps; wind-cut rock stays
-- neutral grey so bleached rib-stone reads against it; the one accent is a dry
-- dusk-rose on the grave cloth still knotted to the ribs, under a cold moon and a
-- low bone-dust haze.
local Palette = require("../../systems/Palette")

local bonePlain: Palette.Palette = {
	name = "PaletteBonePlain",
	about = "The bleached plain inside a dead giant's ribcage: a desert of bone dust, wind-cut grey rock and dry rose grave cloth under a cold moon.",
	words = "pale bone dust, dark trodden earth, bleached rib-stone and neutral wind-cut grey rock under a cold moon, a dry dusk-rose on faded grave cloth, desaturated, matte, no highlights",
	walk = { material = "Sand", color = { 88, 86, 80 } },
	road = { material = "Sandstone", color = { 52, 49, 43 } },
	earth = { material = "Ground", color = { 62, 58, 50 } },
	rock = { material = "Rock", color = { 54, 54, 51 } },
	far = { material = "Limestone", color = { 74, 72, 66 } },
	bed = { material = "Salt", color = { 36, 35, 32 } },
	abyss = { material = "Basalt", color = { 13, 13, 14 } },
	rockTint = { 68, 66, 60 },
	trim = { wood = { 58, 51, 43 }, metal = { 60, 61, 63 }, foliage = { 54, 52, 42 } },
	accent = {
		color = { 100, 69, 76 },
		carriers = "faded dusk-rose grave cloth knotted to the ribs, rose-quartz chips in the dust, dry rose tips on the thorn scrub",
	},
	lamp = { 255, 170, 92 },
	mist = { 148, 142, 133 },
	lighting = "wasteland",
}

return bonePlain
