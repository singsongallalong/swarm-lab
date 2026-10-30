--!strict
-- Frostvine's colours (a frost-killed vineyard), as a palette: frozen terraces of dark
-- plum-brown earth and near-black dead vine wood, pale cool grey cobble for the manor
-- road, violet-slate for terrace faces and the manor's broken walls, and the one accent a
-- deep muted wine-purple on what the estate left behind. Frost reads in the grey-violet
-- mist and the frozen basin, never in white snow; amber is only the manor's one lamp.
local Palette = require("../../systems/Palette")

local frostvine: Palette.Palette = {
	name = "PaletteFrostvine",
	about = "A frost-killed vineyard: terraced rows of dead vines below the broken walls of its manor, its cellars still stained with wine.",
	words = "frozen vineyard terraces of dark plum-brown earth, black dead vine wood, pale cool grey cobble, broken violet-slate manor walls, a deep muted wine-purple as the one accent, amber lamplight in a ruin, frost-grey mist, desaturated, matte, no highlights",
	walk = { material = "Ground", color = { 66, 58, 60 } },
	road = { material = "Cobblestone", color = { 84, 86, 89 } },
	earth = { material = "Mud", color = { 50, 44, 42 } },
	rock = { material = "Basalt", color = { 60, 58, 70 } },
	far = { material = "Slate", color = { 66, 66, 78 } },
	bed = { material = "Ice", color = { 44, 50, 58 } },
	abyss = { material = "Asphalt", color = { 14, 14, 18 } },
	rockTint = { 62, 60, 72 },
	trim = { wood = { 46, 38, 40 }, metal = { 54, 56, 64 }, foliage = { 38, 44, 38 } },
	accent = {
		color = { 88, 52, 68 },
		carriers = "the manor's ragged banners, its shutters and doors, wine stains on the press-house floor, bottles left in the cellar",
	},
	lamp = { 255, 174, 96 },
	mist = { 146, 140, 162 },
	lighting = "mood",
}

return frostvine
