--!strict
-- Claude's reference for relickeys-1 (held out; never shown to workers).
local RelicKeyTypes = require("../RelicKeyTypes")

type Data = RelicKeyTypes.Data
type TierDef = RelicKeyTypes.TierDef

local RelicKeys = {}

function RelicKeys.tierDef(data: Data, tier: number): TierDef?
	if tier ~= tier or tier ~= math.floor(tier) or tier < 1 or tier > #data.tiers then
		return nil
	end
	return data.tiers[tier]
end

function RelicKeys.allowed(data: Data, tier: number): { string }
	local out = {}
	if RelicKeys.tierDef(data, tier) == nil then
		return out
	end
	for name, def in data.modifiers do
		if def.minTier <= tier then
			table.insert(out, name)
		end
	end
	table.sort(out)
	return out
end

local function lists(data: Data, a: string, b: string): boolean
	local def = data.modifiers[a]
	return def ~= nil and def.excludes ~= nil and table.find(def.excludes, b) ~= nil
end

function RelicKeys.excludes(data: Data, a: string, b: string): boolean
	return a == b or lists(data, a, b) or lists(data, b, a)
end

function RelicKeys.rollModifiers(data: Data, tier: number, rng: Random): { string }
	local def = RelicKeys.tierDef(data, tier)
	local pool = RelicKeys.allowed(data, tier)
	if def == nil or #pool == 0 then
		return {}
	end
	local two = rng:NextNumber() < def.twoChance
	local first = pool[rng:NextInteger(1, #pool)]
	if not two then
		return { first }
	end
	local rest = {}
	for _, name in pool do
		if not RelicKeys.excludes(data, first, name) then
			table.insert(rest, name)
		end
	end
	if #rest == 0 then
		return { first }
	end
	return { first, rest[rng:NextInteger(1, #rest)] }
end

function RelicKeys.runPay(data: Data, tier: number, progress: number, cleared: boolean): number
	local def = RelicKeys.tierDef(data, tier)
	if def == nil then
		return 0
	end
	if cleared then
		return def.rolls
	end
	local p = if progress ~= progress then 0 else math.clamp(progress, 0, 1)
	local pay = math.floor(def.rolls * p * RelicKeyTypes.FAIL_SHARE)
	if p >= RelicKeyTypes.MIN_PROGRESS then
		pay = math.max(pay, 1)
	end
	return pay
end

function RelicKeys.partyShare(data: Data, tier: number, memberCount: number, rng: Random): { number }
	local def = RelicKeys.tierDef(data, tier)
	if def == nil or memberCount ~= memberCount or memberCount == math.huge or memberCount < 1 then
		return {}
	end
	local out = { def.rolls }
	for _ = 2, math.floor(memberCount) do
		table.insert(out, if rng:NextNumber() < RelicKeyTypes.MEMBER_CHANCE then 1 else 0)
	end
	return out
end

return RelicKeys
