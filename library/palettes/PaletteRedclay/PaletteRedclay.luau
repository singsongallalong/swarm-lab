--!strict
-- Redclay's colours (a red-clay badlands at night, palettes job direction): rust clay gone
-- dark under the moon (the bible's ground cap keeps it brown-rust, never orange), mesas a
-- shade deeper than the flats, dry wash beds running pale sand where the road goes, and the
-- one accent the faded turquoise of an old shrine's tiles; amber lamps the only other warmth.
local Palette = require("../../systems/Palette")

local redclay: Palette.Palette = {
	name = "PaletteRedclay",
	about = "A red-clay badlands at night: eroded rust mesas cut by dry wash beds, with one broken shrine's turquoise tiles.",
	words = "dark rust-red clay, eroded sandstone mesas, pale dry-wash sand, faded turquoise shrine tiles as the one accent, dry scrub and old timber, low dust, desaturated, matte, no highlights",
	walk = { material = "Sand", color = { 78, 69, 63 } },
	road = { material = "Cobblestone", color = { 89, 87, 81 } },
	earth = { material = "Ground", color = { 48, 43, 40 } },
	rock = { material = "Sandstone", color = { 56, 49, 45 } },
	far = { material = "Rock", color = { 68, 60, 56 } },
	bed = { material = "Mud", color = { 38, 40, 38 } },
	abyss = { material = "Slate", color = { 16, 14, 14 } },
	rockTint = { 62, 55, 50 },
	trim = { wood = { 52, 42, 34 }, metal = { 52, 62, 58 }, foliage = { 46, 52, 44 } },
	accent = {
		color = { 50, 94, 92 },
		carriers = "glazed shrine tiles, an altar band, inlaid doorframes and shards underfoot",
	},
	lamp = { 255, 168, 96 },
	mist = { 148, 142, 136 },
	lighting = "wasteland",
}

return redclay
