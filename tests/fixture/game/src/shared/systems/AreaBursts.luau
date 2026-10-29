--!strict
-- Where and when an area look fires its particles (fixture: a cut-down copy of
-- arpg-game's).
local AreaBursts = {}

-- Each kind's burst scale: how big its puffs are beside the row's own sizes.
AreaBursts.SCALE = {
	Wave = 0.5,
	Rocks = 0.5,
}

function AreaBursts.list(look: any, shape: any, rng: any): { any }
	local out = {}
	if look.kind == "Wave" then
		-- Every other point along the outer edge.
		table.insert(out, { at = 0.2 })
	end
	return out
end

return AreaBursts
