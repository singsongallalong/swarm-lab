--!strict
-- Held out from the builders (swarm-lab relics job): edge cases of the contract in
-- RelicTypes they never saw tested. Scored, not gating.
local RelicTypes = require("../../src/shared/RelicTypes")
local Relics = require("../../src/shared/systems/Relics")
local TestApi = require("../TestApi")

local function rngOf(v: number): Random
	return {
		NextNumber = function(_self: any): number
			return v
		end,
	} :: any
end

local DEF: RelicTypes.RelicDef = {
	name = "Held",
	title = "Held Relic",
	about = "x",
	playstyle = "spell",
	effects = { { stat = "SpellDamage", kind = "increased", base = 0.1, perRank = 0.01, tags = { "Spell" } } },
	awakened = { { stat = "FireDamage", kind = "more", base = 0.05, perRank = 0.01 } },
}

local function near(a: number, b: number): boolean
	return math.abs(a - b) < 1e-9
end

return function(api: TestApi.Api)
	local describe, it, expect = api.describe, api.it, api.expect

	describe("held out: rollGrade", function()
		it("never rolls a grade with no weight", function()
			expect(Relics.rollGrade({ Lesser = 0, Greater = 1, Exalted = 0 }, rngOf(0))).toBe("Greater")
			expect(Relics.rollGrade({ Lesser = 1, Greater = 1 } :: any, rngOf(0.999))).toBe("Greater")
		end)
	end)

	describe("held out: addCopy", function()
		it("an upgrade also counts as a copy toward the next rank", function()
			local c = Relics.newCollection()
			c.relics.Held = { grade = "Lesser", rank = 2, spare = 1 }
			local r = Relics.addCopy(c, "Held", "Greater")
			expect(r.upgraded).toBe(true)
			expect(r.kind).toBe("rank") -- spare 1 + 1 = COPIES[3] = 2
			expect(c.relics.Held).toEqual({ grade = "Greater", rank = 3, spare = 0 })
		end)

		it("a higher copy on a relic at its old cap ranks on instead of turning to dust", function()
			local c = Relics.newCollection()
			c.relics.Held = { grade = "Lesser", rank = 5, spare = 0 }
			local r = Relics.addCopy(c, "Held", "Exalted")
			expect(r.upgraded).toBe(true)
			expect(r.kind).toBe("progress") -- COPIES[6] = 4
			expect(c.dust).toBe(0)
			expect(c.relics.Held).toEqual({ grade = "Exalted", rank = 5, spare = 1 })
		end)

		it("a lower copy never lowers the grade", function()
			local c = Relics.newCollection()
			c.relics.Held = { grade = "Exalted", rank = 10, spare = 0 }
			local r = Relics.addCopy(c, "Held", "Lesser")
			expect(r.upgraded).toBe(false)
			expect(r.kind).toBe("dust")
			expect(c.relics.Held.grade).toBe("Exalted")
		end)

		it("takes exactly 42 Exalted copies from nothing to rank 10, one rank at most each", function()
			local c = Relics.newCollection()
			local last = 0
			for n = 1, 42 do
				local r = Relics.addCopy(c, "Held", "Exalted")
				expect(r.rank - last <= 1).toBe(true)
				last = r.rank
				if n < 42 then
					expect(c.relics.Held.rank < 10).toBe(true)
				end
			end
			expect(c.relics.Held).toEqual({ grade = "Exalted", rank = 10, spare = 0 })
			expect(Relics.addCopy(c, "Held", "Exalted").kind).toBe("dust")
		end)
	end)

	describe("held out: copiesToMax", function()
		it("counts the copies left to the grade's cap, spare included", function()
			expect(Relics.copiesToMax({ grade = "Lesser", rank = 5, spare = 0 })).toBe(0)
			expect(Relics.copiesToMax({ grade = "Lesser", rank = 4, spare = 1 })).toBe(2) -- COPIES[5] = 3
			expect(Relics.copiesToMax({ grade = "Exalted", rank = 1, spare = 0 })).toBe(41)
		end)
	end)

	describe("held out: buyCopy", function()
		it("refuses without enough dust, unowned, or at the cap, changing nothing", function()
			local c = Relics.newCollection()
			c.dust = RelicTypes.DUST_COST - 1
			c.relics.Held = { grade = "Greater", rank = 2, spare = 0 }
			expect((Relics.buyCopy(c, "Held"))).toBe(false)
			c.dust = 100
			expect((Relics.buyCopy(c, "Missing"))).toBe(false)
			c.relics.Capped = { grade = "Lesser", rank = 5, spare = 0 }
			expect((Relics.buyCopy(c, "Capped"))).toBe(false)
			expect(c.dust).toBe(100)
		end)

		it("spends DUST_COST and adds a Lesser copy that never upgrades", function()
			local c = Relics.newCollection()
			c.dust = 25
			c.relics.Held = { grade = "Greater", rank = 2, spare = 0 }
			local ok, r = Relics.buyCopy(c, "Held")
			expect(ok).toBe(true)
			expect(c.dust).toBe(25 - RelicTypes.DUST_COST)
			expect((r :: any).upgraded).toBe(false)
			expect(c.relics.Held.grade).toBe("Greater")
		end)
	end)

	describe("held out: modifiers", function()
		it("gives none under rank 1 and caps the rank at 10", function()
			expect(#Relics.modifiers(DEF, 0)).toBe(0)
			local at10, at12 = Relics.modifiers(DEF, 10), Relics.modifiers(DEF, 12)
			expect(near(at12[1].value, at10[1].value)).toBe(true)
			expect(near(at10[2].value, 0.05 + 0.01 * (10 - RelicTypes.AWAKEN_RANK))).toBe(true)
		end)

		it("copies tags, leaves missing conditions nil, and never changes the def", function()
			local mods = Relics.modifiers(DEF, 6)
			expect(mods[1].tags).toEqual({ "Spell" })
			expect(mods[1].conditions).toBe(nil)
			mods[1].value = 99
			expect(DEF.effects[1].base).toBe(0.1)
			expect(near(Relics.modifiers(DEF, 6)[1].value, 0.15)).toBe(true)
		end)
	end)

	describe("held out: slots", function()
		it("refuses a fractional or zero index, and allows re-slotting in place", function()
			local c = Relics.newCollection()
			c.relics.Held = { grade = "Lesser", rank = 1, spare = 0 }
			local slots: RelicTypes.Slots = {}
			expect((Relics.slot(slots, 0, "Held", c))).toBe(false)
			expect((Relics.slot(slots, 1.5, "Held", c))).toBe(false)
			expect((Relics.slot(slots, 2, "Held", c))).toBe(true)
			expect((Relics.slot(slots, 2, "Held", c))).toBe(true)
			local ok, why = Relics.slot(slots, 3, "Held", c)
			expect(ok).toBe(false)
			expect(type(why)).toBe("string")
			Relics.unslot(slots, 2)
			expect(slots[2]).toBe(nil)
		end)
	end)

	describe("held out: synergy and loadout", function()
		it("bends at SYNERGY_BEND and counts whole steps only", function()
			expect(near(Relics.synergy(3), 0)).toBe(true)
			expect(near(Relics.synergy(23), 0.05)).toBe(true)
			expect(near(Relics.synergy(24), 0.055)).toBe(true)
			expect(near(Relics.synergy(40), 0.075)).toBe(true)
		end)

		it("skips unowned or unknown slotted relics and adds no synergy at 0", function()
			local c = Relics.newCollection()
			c.relics.Held = { grade = "Lesser", rank = 3, spare = 0 }
			local mods = Relics.loadout({ [2] = "Held", [3] = "Ghost", [4] = "NoDef" }, c, { Held = DEF })
			expect(#mods).toBe(1) -- rank 3: no awakened; 3 ranks: no synergy
			c.relics.NoDef = { grade = "Lesser", rank = 2, spare = 0 }
			mods = Relics.loadout({ [2] = "Held", [4] = "NoDef" }, c, { Held = DEF })
			expect(#mods).toBe(1)
		end)

		it("orders the slotted relics by slot, then the synergy", function()
			local other: RelicTypes.RelicDef = table.clone(DEF)
			other.title = "Other"
			local c = Relics.newCollection()
			c.relics.Held = { grade = "Exalted", rank = 4, spare = 0 }
			c.relics.Other = { grade = "Exalted", rank = 4, spare = 0 }
			local mods = Relics.loadout({ [3] = "Held", [1] = "Other" }, c, { Held = DEF, Other = other })
			expect(mods[1].source).toBe("Relic: Other")
			expect(mods[2].source).toBe("Relic: Held Relic")
			expect(mods[#mods].source).toBe(RelicTypes.SYNERGY_SOURCE)
		end)
	end)
end
