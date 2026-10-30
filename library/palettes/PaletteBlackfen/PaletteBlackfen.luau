--!strict
-- Blackfen's colours (a peat bog of standing stones): black peat and wet brown moss for
-- ground, grey standing stones catching the moon, still black pools, and one cold
-- will-o'-wisp blue as the accent. The ground stays near-black so the pale stones, the
-- pools and the wisps are what read from the high camera; the light is a drowned parish's,
-- a wet grey night rather than the moor's.
local Palette = require("../../systems/Palette")

local blackfen: Palette.Palette = {
	name = "PaletteBlackfen",
	about = "A peat bog of standing stones, still black pools and drowned causeways, lit by cold will-o'-the-wisp flames.",
	words = "black peat and wet brown moss, grey standing stones, still black pools, a cold will-o'-wisp blue as the one accent, thick low mist, desaturated, matte, no highlights",
	walk = { material = "Ground", color = { 46, 43, 37 } },
	road = { material = "Cobblestone", color = { 78, 80, 78 } },
	earth = { material = "Mud", color = { 41, 37, 33 } },
	rock = { material = "Basalt", color = { 52, 54, 52 } },
	far = { material = "Grass", color = { 48, 52, 44 } },
	bed = { material = "Sand", color = { 30, 30, 28 } },
	abyss = { material = "Slate", color = { 12, 13, 14 } },
	rockTint = { 74, 76, 72 },
	trim = { wood = { 44, 38, 32 }, metal = { 56, 58, 60 }, foliage = { 44, 52, 36 } },
	accent = {
		color = { 52, 88, 100 },
		carriers = "will-o'-wisp flames over the pools, runes cut in the standing stones, pale bog-moss where the water lies",
	},
	lamp = { 255, 170, 96 },
	mist = { 128, 140, 142 },
	lighting = "drownedParish",
}

return blackfen
