--!strict
-- Particle emitters as data (fixture).
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
