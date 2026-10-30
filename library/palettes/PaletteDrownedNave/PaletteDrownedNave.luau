--!strict
-- DrownedNave's colours (the sunken cathedral marsh, swarm-lab palettes job): a drowned
-- nave standing in green-black water, reed beds between its piers, pale grey limestone
-- tracery breaking the surface, and a dim stained-glass amber as the one accent. The
-- grounds stay dark and green-black so the limestone reads pale as bone above them from
-- the high camera; the mist is green-grey marsh haze, not the moor's silver blue.
local Palette = require("../../systems/Palette")

local drownedNave: Palette.Palette = {
	name = "PaletteDrownedNave",
	about = "A sunken cathedral marsh, its drowned nave and broken tracery standing in green-black water with reed beds between the piers.",
	words = "green-black marsh water over dark silt, reed beds, pale grey limestone tracery breaking the surface, dark waterlogged timber, grey-green reeds, a dim stained-glass amber as the one accent, silver-blue night, low green-grey mist, desaturated, matte, no highlights",
	walk = { material = "Mud", color = { 32, 39, 34 } },
	road = { material = "Cobblestone", color = { 70, 75, 76 } },
	earth = { material = "Ground", color = { 48, 46, 40 } },
	rock = { material = "Limestone", color = { 84, 88, 85 } },
	far = { material = "Salt", color = { 52, 58, 52 } },
	bed = { material = "Slate", color = { 24, 30, 26 } },
	abyss = { material = "Basalt", color = { 14, 17, 16 } },
	rockTint = { 78, 82, 79 },
	trim = { wood = { 38, 35, 30 }, metal = { 54, 58, 52 }, foliage = { 46, 56, 38 } },
	accent = {
		color = { 97, 75, 49 },
		carriers = "the few glass panes left in the drowned windows, gilt on the tracery, wax stubs at the shrine niches, prayer ribbons at the water's edge",
	},
	lamp = { 255, 172, 96 },
	mist = { 122, 136, 124 },
	lighting = "drownedParish",
}

return drownedNave
