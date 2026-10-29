--!strict
-- Particle emitters as data (fixture).

-- A curve over a particle's life: { time 0–1, value } points, times
-- ascending from 0 to 1 (NumberSequence).
export type Curve = { { number } }

export type Emitter = {
	texture: string,
	count: number,
	size: Curve,
	squash: Curve?, -- -3 to 3
}

local Emitters = {
	-- Dust kicked out low and wide from a slam, slowing fast and settling.
	SlamDust = {
		texture = "rbxasset://textures/particles/smoke_main.dds",
		count = 24,
		lifetime = { 0.5, 0.9 },
		size = { { 0, 0.8 }, { 1, 2.4 } },
		color = { 150, 140, 125 },
	},
}

return Emitters
