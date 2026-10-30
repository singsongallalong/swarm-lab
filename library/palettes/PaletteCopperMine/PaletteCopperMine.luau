--!strict
-- PaletteCopperMine, the copper-mine terrace: stepped spoil heaps of iron-stained rust-brown
-- ore dust and cool slag-grey stone, old timber props over dark burnt earth, and one
-- verdigris green — copper's own patina — on every pipe, bell and dome, under amber lanterns.
-- The rust is carried in hue, not saturation: the ground stays dark and inside the bible's caps.
local Palette = require("../../systems/Palette")

local copperMine: Palette.Palette = {
	name = "PaletteCopperMine",
	about = "A stepped copper-mine terrace of rust-brown spoil heaps and slag-grey stone, its old timber props and verdigris pipes left where the miners stopped.",
	words = "rust-brown ore dust over slag-grey stone, dark timber props, verdigris green on pipes and bell domes as the one accent, warm amber lanterns, desaturated, matte, no highlights",
	walk = { material = "Ground", color = { 78, 68, 63 } },
	road = { material = "Cobblestone", color = { 66, 72, 71 } },
	earth = { material = "Mud", color = { 50, 44, 41 } },
	rock = { material = "Rock", color = { 54, 58, 56 } },
	far = { material = "Slate", color = { 67, 71, 74 } },
	bed = { material = "Sand", color = { 40, 48, 46 } },
	abyss = { material = "Basalt", color = { 16, 17, 19 } },
	rockTint = { 60, 67, 63 },
	trim = { wood = { 66, 52, 40 }, metal = { 58, 56, 52 }, foliage = { 52, 58, 44 } },
	accent = {
		color = { 62, 100, 78 },
		carriers = "oxidised copper pipes, valve wheels, bell domes, pump housings, the patina in run-off channels",
	},
	lamp = { 255, 170, 96 },
	mist = { 116, 121, 126 },
	lighting = "quarry",
}

return copperMine
