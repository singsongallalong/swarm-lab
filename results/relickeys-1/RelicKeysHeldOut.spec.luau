--!strict
-- Held out from the relickeys-1 workers: the contract's edge cases the visible spec skips.
local RelicKeyTypes = require("../../src/shared/RelicKeyTypes")
local RelicKeys = require("../../src/shared/systems/RelicKeys")
local TestApi = require("../TestApi")
-- Lune has no Random; this stands in with the same methods.
local Random = require("../../scripts/uisim/Random")

type Data = RelicKeyTypes.Data

local NAN = 0 / 0

local function tiers(): { RelicKeyTypes.TierDef }
	return {
		{
			tier = 1,
			gradeWeights = { Lesser = 80, Greater = 18, Exalted = 2 },
			rolls = 2,
			levelBonus = 0,
			twoChance = 1,
		},
		{
			tier = 2,
			gradeWeights = { Lesser = 70, Greater = 25, Exalted = 5 },
			rolls = 5,
			levelBonus = 3,
			twoChance = 0.5,
		},
		{
			tier = 3,
			gradeWeights = { Lesser = 60, Greater = 30, Exalted = 10 },
			rolls = 9,
			levelBonus = 6,
			twoChance = 1,
		},
	}
end

local function mod(name: string, minTier: number, excludes: { string }?): RelicKeyTypes.ModifierDef
	return { name = name, title = name, about = name, minTier = minTier, excludes = excludes }
end

-- Tier 1 allows only Kilo and Lima, which exclude each other (listed on the later side only).
-- Tier 2 adds six more; tier 3 adds Zulu, which every tier-2 name but Mike excludes.
local ORDER = { "Papa", "Kilo", "Oscar", "Lima", "Mike", "Quebec", "November", "Romeo", "Zulu" }
local function build(order: { string }): Data
	local defs: { [string]: RelicKeyTypes.ModifierDef } = {
		Kilo = mod("Kilo", 1),
		Lima = mod("Lima", 1, { "Kilo" }),
		Mike = mod("Mike", 2),
		November = mod("November", 2, { "Zulu" }),
		Oscar = mod("Oscar", 2, { "Zulu" }),
		Papa = mod("Papa", 2, { "Zulu" }),
		Quebec = mod("Quebec", 2, { "Zulu" }),
		Romeo = mod("Romeo", 2, { "Zulu" }),
		Zulu = mod("Zulu", 3, { "Kilo", "Lima" }),
	}
	local modifiers: { [string]: RelicKeyTypes.ModifierDef } = {}
	for _, name in order do
		modifiers[name] = defs[name]
	end
	return { tiers = tiers(), modifiers = modifiers }
end

local function copy(v: any): any
	if type(v) ~= "table" then
		return v
	end
	local out = {}
	for k, x in v do
		out[k] = copy(x)
	end
	return out
end

return function(api: TestApi.Api)
	local describe, it, expect = api.describe, api.it, api.expect
	local data = build(ORDER)

	describe("RelicKeys held out", function()
		it("refuses every tier that isn't a whole number in range", function()
			for _, t in { 0, 4, 2.5, -1, NAN, math.huge, -math.huge } do
				expect(RelicKeys.tierDef(data, t)).toBe(nil)
				expect(RelicKeys.allowed(data, t)).toEqual({})
				expect(RelicKeys.rollModifiers(data, t, Random.new(1) :: any)).toEqual({})
				expect(RelicKeys.runPay(data, t, 1, true)).toBe(0)
				expect(RelicKeys.partyShare(data, t, 3, Random.new(1) :: any)).toEqual({})
			end
			expect((RelicKeys.tierDef(data, 3) :: any).rolls).toBe(9)
		end)

		it("sorts allowed names whatever order the table was built in", function()
			expect(RelicKeys.allowed(data, 3)).toEqual({
				"Kilo",
				"Lima",
				"Mike",
				"November",
				"Oscar",
				"Papa",
				"Quebec",
				"Romeo",
				"Zulu",
			})
			local a = RelicKeys.allowed(data, 2)
			table.insert(a, "Junk")
			expect(#RelicKeys.allowed(data, 2)).toBe(8)
		end)

		it("treats unknown names as excluding only themselves", function()
			expect(RelicKeys.excludes(data, "Nope", "Kilo")).toBe(false)
			expect(RelicKeys.excludes(data, "Kilo", "Nope")).toBe(false)
			expect(RelicKeys.excludes(data, "Nope", "Nope")).toBe(true)
			expect(RelicKeys.excludes(data, "Kilo", "Lima")).toBe(true)
			expect(RelicKeys.excludes(data, "Kilo", "Zulu")).toBe(true)
			expect(RelicKeys.excludes(data, "Mike", "Zulu")).toBe(false)
		end)

		it("gives one when no second is possible", function()
			local rng = Random.new(11) :: any
			for _ = 1, 300 do
				local got = RelicKeys.rollModifiers(data, 1, rng)
				expect(#got).toBe(1)
				expect(got[1] == "Kilo" or got[1] == "Lima").toBe(true)
			end
			local lone: Data = { tiers = tiers(), modifiers = { Solo = mod("Solo", 1) } }
			expect(RelicKeys.rollModifiers(lone, 1, Random.new(2) :: any)).toEqual({ "Solo" })
			local none: Data = { tiers = tiers(), modifiers = { Late = mod("Late", 2) } }
			expect(RelicKeys.rollModifiers(none, 1, Random.new(2) :: any)).toEqual({})
		end)

		it("never pairs exclusions from either side and reaches every name", function()
			local rng = Random.new(5) :: any
			local seen: { [string]: number } = {}
			for _ = 1, 3000 do
				local got = RelicKeys.rollModifiers(data, 3, rng)
				expect(#got).toBe(2)
				expect(got[1] ~= got[2]).toBe(true)
				expect(RelicKeys.excludes(data, got[1], got[2])).toBe(false)
				for _, name in got do
					seen[name] = (seen[name] or 0) + 1
				end
			end
			for _, name in RelicKeys.allowed(data, 3) do
				expect((seen[name] or 0) > 0).toBe(true)
			end
			-- Zulu is the first pick 1 time in 9, and second after Mike 1 in 72 (1/8 of 1/9).
			-- Rejecting whole pairs instead would give it 1 in 28.
			expect((seen.Zulu :: number) / 3000).toBeNear(1 / 9 + 1 / 72, 0.03)
		end)

		it("takes the count from the first draw and is the same for the same seed", function()
			local twos = 0
			for i = 1, 400 do
				-- Spread out: the stand-in Random's first draw is tiny for small seeds.
				local seed = (i * 2654435761) % 4294967296
				local got = RelicKeys.rollModifiers(data, 2, Random.new(seed) :: any)
				local want = if Random.new(seed):NextNumber() < 0.5 then 2 else 1
				expect(#got).toBe(want)
				if #got == 2 then
					twos += 1
				end
				local shuffled =
					build({ "Zulu", "Romeo", "Quebec", "Papa", "Oscar", "November", "Mike", "Lima", "Kilo" })
				expect(RelicKeys.rollModifiers(shuffled, 2, Random.new(seed) :: any)).toEqual(got)
			end
			expect(twos / 400).toBeNear(0.5, 0.08)
		end)

		it("pays failures by clamped progress", function()
			expect(RelicKeys.runPay(data, 3, NAN, true)).toBe(9)
			expect(RelicKeys.runPay(data, 3, -5, true)).toBe(9)
			expect(RelicKeys.runPay(data, 3, NAN, false)).toBe(0)
			expect(RelicKeys.runPay(data, 3, -2, false)).toBe(0)
			expect(RelicKeys.runPay(data, 3, 7, false)).toBe(4)
			expect(RelicKeys.runPay(data, 3, math.huge, false)).toBe(4)
			expect(RelicKeys.runPay(data, 3, 0.6, false)).toBe(2)
			expect(RelicKeys.runPay(data, 1, 0.25, false)).toBe(1)
			expect(RelicKeys.runPay(data, 1, 0.2499, false)).toBe(0)
			expect(RelicKeys.runPay(data, 1, 1, false)).toBe(1)
		end)

		it("draws once per other member, in order", function()
			for i = 1, 50 do
				local seed = (i * 2654435761) % 4294967296
				local got = RelicKeys.partyShare(data, 2, 4, Random.new(seed) :: any)
				local r = Random.new(seed) :: any
				local want = { 5 }
				for _ = 2, 4 do
					table.insert(want, if r:NextNumber() < RelicKeyTypes.MEMBER_CHANCE then 1 else 0)
				end
				expect(got).toEqual(want)
			end
			expect(RelicKeys.partyShare(data, 2, 1, Random.new(1) :: any)).toEqual({ 5 })
			expect(#RelicKeys.partyShare(data, 2, 2.7, Random.new(1) :: any)).toBe(2)
			for _, n in { 0, 0.9, -3, NAN, math.huge } do
				expect(RelicKeys.partyShare(data, 2, n, Random.new(1) :: any)).toEqual({})
			end
		end)

		it("never changes the data it is given", function()
			local before = copy(data)
			local rng = Random.new(9) :: any
			for t = 1, 3 do
				RelicKeys.allowed(data, t)
				local got = RelicKeys.rollModifiers(data, t, rng)
				table.insert(got, "Junk")
				RelicKeys.runPay(data, t, 0.5, false)
				local share = RelicKeys.partyShare(data, t, 3, rng)
				share[1] = -1
			end
			expect(data).toEqual(before)
		end)
	end)
end
