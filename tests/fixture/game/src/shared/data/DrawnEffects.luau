--!strict
-- The library of drawn effects (fixture: a cut-down copy of arpg-game's).

-- Area kinds (primitives/AreaFx draws them, laid out by systems/AreaLayout):
--   Wave      a band sweeping out across the area to its edge.
--   Rocks     stones that heave up out of the ground, nearest first, and sink.
export type Wave = {
	kind: "Wave",
	about: string,
	travel: number,
	steps: number,
	thickness: number,
	fade: number,
	emitter: string?,
}

export type AreaLook = Wave | Rocks

-- Flight kinds (SkillVfxController draws them):
--   Lance  a faceted shard `length` studs long pointing along its flight.
export type Lance = {
	kind: "Lance",
	about: string,
	length: number,
	width: number,
}
export type FlightLook = Lance

local area: { [string]: AreaLook } = {
	SweepWave = {
		kind = "Wave",
		about = "The impact ring bent to the area's shape, sweeping out to its edge with dust along it.",
		-- No longer spare: Cold Snap's placeholder.
		travel = 70,
		steps = 7,
		thickness = 0.5,
		fade = 0.18,
		emitter = "SlamDust",
	},
	HeavedRocks = {
		kind = "Rocks",
		about = "Broken slate heaving up out of the ground in a ripple to the edge, then sinking.",
		spacing = 2.6,
		size = { 0.7, 1.8 },
		color = { 112, 104, 96 },
		emitter = "SlamDust",
		-- Stones grow with the hit, never in number.
		perPower = { size = 0.12 },
	},
}

local flight: { [string]: FlightLook } = {
	IceLance = {
		kind = "Lance",
		about = "A long faceted lance of pale ice with a cold blue glow inside.",
		length = 4,
		width = 0.55,
		perPower = { length = 0.07, width = 0.07 },
	},
}

return table.freeze({ area = table.freeze(area), flight = table.freeze(flight) })
