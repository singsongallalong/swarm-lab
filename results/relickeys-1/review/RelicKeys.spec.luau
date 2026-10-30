--!strict
local RelicKeyTypes = require("../../src/shared/RelicKeyTypes")
local RelicKeys = require("../../src/shared/systems/RelicKeys")
local Rows = require("../../src/shared/data/RelicKeys")
local TestApi = require("../TestApi")
-- Lune has no Random; this stands in with the same methods.
local Random = require("../../scripts/uisim/Random")

type Data = RelicKeyTypes.Data

-- A small fixed table, so the system's rules are tested apart from the live rows.
local fixture: Data = {
	tiers = {
		{
			tier = 1,
			gradeWeights = { Lesser = 80, Greater = 18, Exalted = 2 },
			rolls = 2,
			levelBonus = 0,
			twoChance = 0,
		},
		{
			tier = 2,
			gradeWeights = { Lesser = 70, Greater = 25, Exalted = 5 },
			rolls = 4,
			levelBonus = 3,
			twoChance = 1,
		},
		{
			tier = 3,
			gradeWeights = { Lesser = 60, Greater = 30, Exalted = 10 },
			rolls = 6,
			levelBonus = 6,
			twoChance = 0.5,
		},
	},
	modifiers = {
		Alpha = { name = "Alpha", title = "Alpha", about = "a", minTier = 1 },
		Bravo = { name = "Bravo", title = "Bravo", about = "b", minTier = 1, excludes = { "Charlie" } },
		Charlie = { name = "Charlie", title = "Charlie", about = "c", minTier = 2 },
		Delta = { name = "Delta", title = "Delta", about = "d", minTier = 3 },
	},
}

local function isWhole(n: number): boolean
	return n == math.floor(n)
end

return function(api: TestApi.Api)
	local describe, it, expect = api.describe, api.it, api.expect

	describe("RelicKeys rules", function()
		it("finds tiers and the modifiers each allows", function()
			expect((RelicKeys.tierDef(fixture, 2) :: any).rolls).toBe(4)
			expect(RelicKeys.tierDef(fixture, 0)).toBe(nil)
			expect(RelicKeys.tierDef(fixture, 4)).toBe(nil)
			expect(RelicKeys.allowed(fixture, 1)).toEqual({ "Alpha", "Bravo" })
			expect(RelicKeys.allowed(fixture, 3)).toEqual({ "Alpha", "Bravo", "Charlie", "Delta" })
			expect(RelicKeys.allowed(fixture, 9)).toEqual({})
		end)

		it("reads exclusions from either side", function()
			expect(RelicKeys.excludes(fixture, "Bravo", "Charlie")).toBe(true)
			expect(RelicKeys.excludes(fixture, "Charlie", "Bravo")).toBe(true)
			expect(RelicKeys.excludes(fixture, "Alpha", "Bravo")).toBe(false)
			expect(RelicKeys.excludes(fixture, "Alpha", "Alpha")).toBe(true)
		end)

		it("rolls one modifier when twoChance is 0 and two when it is 1", function()
			local rng = Random.new(7) :: any
			for _ = 1, 200 do
				local one = RelicKeys.rollModifiers(fixture, 1, rng)
				expect(#one).toBe(1)
				local two = RelicKeys.rollModifiers(fixture, 2, rng)
				expect(#two).toBe(2)
				expect(two[1] ~= two[2]).toBe(true)
				expect(RelicKeys.excludes(fixture, two[1], two[2])).toBe(false)
			end
			expect(RelicKeys.rollModifiers(fixture, 4, rng)).toEqual({})
		end)

		it("pays a clear in full and a failure in part", function()
			expect(RelicKeys.runPay(fixture, 3, 0.1, true)).toBe(6)
			expect(RelicKeys.runPay(fixture, 3, 1, false)).toBe(3)
			expect(RelicKeys.runPay(fixture, 3, 0.5, false)).toBe(1)
			expect(RelicKeys.runPay(fixture, 3, 0.1, false)).toBe(0)
			expect(RelicKeys.runPay(fixture, 1, 0.3, false)).toBe(1)
			expect(RelicKeys.runPay(fixture, 7, 1, true)).toBe(0)
		end)

		it("gives the holder the rolls and the others a chance of one", function()
			local rng = Random.new(3) :: any
			local got = 0
			for _ = 1, 2000 do
				local share = RelicKeys.partyShare(fixture, 2, 3, rng)
				expect(#share).toBe(3)
				expect(share[1]).toBe(4)
				for i = 2, 3 do
					expect(share[i] == 0 or share[i] == 1).toBe(true)
					got += share[i]
				end
			end
			expect(got / 4000).toBeNear(RelicKeyTypes.MEMBER_CHANCE, 0.03)
			expect(RelicKeys.partyShare(fixture, 2, 0, rng)).toEqual({})
		end)
	end)

	describe("RelicKeys rows", function()
		it("has five tiers that get better in order", function()
			expect(#Rows.tiers).toBe(5)
			local first = Rows.tiers[1].gradeWeights
			expect({ first.Lesser, first.Greater, first.Exalted }).toEqual({ 80, 18, 2 })
			for i, row in Rows.tiers do
				expect(row.tier).toBe(i)
				expect(isWhole(row.rolls) and row.rolls >= 1).toBe(true)
				expect(isWhole(row.levelBonus) and row.levelBonus >= 0).toBe(true)
				expect(row.twoChance >= 0 and row.twoChance <= 1).toBe(true)
				for _, grade in RelicKeyTypes.GRADES do
					expect(row.gradeWeights[grade] >= 0).toBe(true)
				end
				if i > 1 then
					local prev = Rows.tiers[i - 1]
					expect(row.gradeWeights.Lesser < prev.gradeWeights.Lesser).toBe(true)
					expect(row.gradeWeights.Exalted > prev.gradeWeights.Exalted).toBe(true)
					expect(row.rolls >= prev.rolls).toBe(true)
					expect(row.levelBonus > prev.levelBonus).toBe(true)
					expect(row.twoChance >= prev.twoChance).toBe(true)
				end
			end
			expect(Rows.tiers[5].rolls > Rows.tiers[1].rolls).toBe(true)
		end)

		it("has a modifier pool with tiers and exclusions", function()
			local count, pairs, high = 0, 0, 0
			for key, mod in Rows.modifiers do
				count += 1
				expect(mod.name).toBe(key)
				expect(string.match(key, "^%u%w*$") ~= nil).toBe(true)
				expect(#mod.title > 0 and #mod.about > 0).toBe(true)
				expect(isWhole(mod.minTier) and mod.minTier >= 1 and mod.minTier <= #Rows.tiers).toBe(true)
				if mod.minTier >= 4 then
					high += 1
				end
				for _, other in mod.excludes or {} do
					expect(Rows.modifiers[other] ~= nil).toBe(true)
					expect(other ~= key).toBe(true)
					pairs += 1
				end
			end
			expect(count >= 10).toBe(true)
			expect(pairs >= 2).toBe(true)
			expect(high >= 1).toBe(true)
			expect(#RelicKeys.allowed(Rows, 1) >= 4).toBe(true)
		end)
	end)
end
