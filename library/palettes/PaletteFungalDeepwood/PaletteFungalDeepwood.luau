--!strict
-- The fungal deepwood's colours (a rotting old forest under a fungal bloom), as a
-- palette: dark loam and rot underfoot, bark near black, pale old flagstones sunk in
-- moss, wet mossy stone, a muted spore violet as the one accent on caps and gills,
-- a faint pale-violet fungus-light and a pale violet-grey spore mist.
local Palette = require("../../systems/Palette")

local fungalDeepwood: Palette.Palette = {
	name = "PaletteFungalDeepwood",
	about = "A dense deepwood of black rotting trunks and dark loam, lit faintly by pale fungus and drifting violet spores.",
	words = "dark loam and black rot underfoot, bark near black, pale old flagstones sunk in moss, wet mossy stone, a muted spore violet on cap gills and shelf fungus, a faint pale-violet fungus-light, violet-grey spore mist, desaturated, matte, no highlights",
	walk = { material = "LeafyGrass", color = { 49, 45, 40 } },
	road = { material = "Cobblestone", color = { 78, 75, 66 } },
	earth = { material = "Mud", color = { 40, 37, 33 } },
	rock = { material = "Slate", color = { 44, 47, 44 } },
	far = { material = "Grass", color = { 42, 40, 49 } },
	bed = { material = "Ground", color = { 26, 28, 24 } },
	abyss = { material = "Basalt", color = { 13, 13, 16 } },
	rockTint = { 46, 49, 46 },
	trim = { wood = { 26, 23, 29 }, metal = { 41, 43, 45 }, foliage = { 36, 52, 38 } },
	accent = {
		color = { 86, 66, 96 },
		carriers = "cap gills and spore dust, shelf fungus on the black bark, the pale caps themselves",
	},
	lamp = { 196, 190, 214 },
	mist = { 138, 132, 152 },
	lighting = "barrows",
}

return fungalDeepwood
