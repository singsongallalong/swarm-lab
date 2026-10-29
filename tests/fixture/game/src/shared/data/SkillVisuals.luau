--!strict
-- How each skill is drawn (fixture: a cut-down copy of arpg-game's).
export type SkillVisual = {
	color: Color3,
	areaLook: (string | false)?,
	flightLook: string?,
}

local SkillVisuals: { [string]: SkillVisual } = {
	default = { color = Color3.fromRGB(220, 220, 255), fiery = false, burstRadius = 2 },
	GroundSlam = {
		color = Color3.fromRGB(255, 220, 120),
		fiery = false,
		burstRadius = 2,
		-- The ground heaves over the cone the slam really hit.
		areaLook = "HeavedRocks",
	},
	-- Ice Spear's blue on the borrowed wave. PLACEHOLDER.
	ColdSnap = {
		color = Color3.fromRGB(170, 225, 255),
		fiery = false,
		burstRadius = 1.5,
		areaLook = "SweepWave",
	},
	Sleet = {
		color = Color3.fromRGB(170, 225, 255),
		fiery = false,
		burstRadius = 1,
		flightLook = "IceLance",
	},
}

return SkillVisuals
