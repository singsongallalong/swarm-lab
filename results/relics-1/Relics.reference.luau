--!strict
-- Reference implementation (Claude), to validate the specs. Not given to builders.
local RelicTypes = require("../RelicTypes")
local SkillTypes = require("../SkillTypes")

type Grade = RelicTypes.Grade
type Collection = RelicTypes.Collection
type Owned = RelicTypes.Owned

local Relics = {}

local function gradeIndex(g: Grade): number
	return table.find(RelicTypes.GRADES, g) or 0
end

function Relics.rollGrade(weights: { [Grade]: number }, rng: Random): Grade
	local total = 0
	for _, g in RelicTypes.GRADES do
		total += math.max((weights :: any)[g] or 0, 0)
	end
	local pick = rng:NextNumber() * total
	local last: Grade = RelicTypes.GRADES[1]
	for _, g in RelicTypes.GRADES do
		local w = math.max((weights :: any)[g] or 0, 0)
		if w > 0 then
			last = g
			if pick < w then
				return g
			end
			pick -= w
		end
	end
	return last
end

function Relics.newCollection(): Collection
	return { relics = {}, dust = 0 }
end

function Relics.addCopy(c: Collection, name: string, grade: Grade): RelicTypes.AddResult
	local held = c.relics[name]
	if not held then
		c.relics[name] = { grade = grade, rank = 1, spare = 0 }
		return { kind = "new", upgraded = false, rank = 1, dust = 0 }
	end
	local upgraded = gradeIndex(grade) > gradeIndex(held.grade)
	if upgraded then
		held.grade = grade
	end
	if held.rank >= RelicTypes.MAX_RANK[held.grade] then
		c.dust += RelicTypes.DUST_PER_SPARE
		return { kind = "dust", upgraded = upgraded, rank = held.rank, dust = RelicTypes.DUST_PER_SPARE }
	end
	held.spare += 1
	if held.spare >= RelicTypes.COPIES[held.rank + 1] then
		held.spare = 0
		held.rank += 1
		return { kind = "rank", upgraded = upgraded, rank = held.rank, dust = 0 }
	end
	return { kind = "progress", upgraded = upgraded, rank = held.rank, dust = 0 }
end

function Relics.copiesToMax(o: Owned): number
	local n = 0
	for r = o.rank + 1, RelicTypes.MAX_RANK[o.grade] do
		n += RelicTypes.COPIES[r]
	end
	return math.max(n - o.spare, 0)
end

function Relics.buyCopy(c: Collection, name: string): (boolean, RelicTypes.AddResult?)
	local held = c.relics[name]
	if not held or held.rank >= RelicTypes.MAX_RANK[held.grade] or c.dust < RelicTypes.DUST_COST then
		return false, nil
	end
	c.dust -= RelicTypes.DUST_COST
	return true, Relics.addCopy(c, name, "Lesser")
end

function Relics.modifiers(def: RelicTypes.RelicDef, rank: number): { SkillTypes.Modifier }
	local out: { SkillTypes.Modifier } = {}
	if rank < 1 then
		return out
	end
	rank = math.min(rank, 10)
	local function add(e: RelicTypes.RelicEffect, from: number)
		table.insert(out, {
			stat = e.stat,
			kind = e.kind,
			value = e.base + e.perRank * (rank - from),
			source = `Relic: {def.title}`,
			tags = if e.tags then table.clone(e.tags) else nil,
			conditions = if e.conditions then table.clone(e.conditions) else nil,
		})
	end
	for _, e in def.effects do
		add(e, 1)
	end
	if rank >= RelicTypes.AWAKEN_RANK then
		for _, e in def.awakened do
			add(e, RelicTypes.AWAKEN_RANK)
		end
	end
	return out
end

function Relics.slot(slots: RelicTypes.Slots, index: number, name: string, c: Collection): (boolean, string?)
	if index ~= math.floor(index) or index < 1 or index > RelicTypes.SLOTS then
		return false, "no such slot"
	elseif not c.relics[name] then
		return false, "not owned"
	end
	for i, n in slots do
		if n == name and i ~= index then
			return false, "already slotted"
		end
	end
	slots[index] = name
	return true, nil
end

function Relics.unslot(slots: RelicTypes.Slots, index: number)
	slots[index] = nil
end

function Relics.synergy(totalRanks: number): number
	local under = math.min(totalRanks, RelicTypes.SYNERGY_BEND)
	local over = math.max(totalRanks - RelicTypes.SYNERGY_BEND, 0)
	return RelicTypes.SYNERGY_STEP * (under // RelicTypes.SYNERGY_RANKS)
		+ RelicTypes.SYNERGY_STEP / 2 * (over // RelicTypes.SYNERGY_RANKS)
end

function Relics.loadout(
	slots: RelicTypes.Slots,
	c: Collection,
	defs: { [string]: RelicTypes.RelicDef }
): { SkillTypes.Modifier }
	local out: { SkillTypes.Modifier } = {}
	local total = 0
	for i = 1, RelicTypes.SLOTS do
		local name = slots[i]
		local held = if name then c.relics[name] else nil
		local def = if name then defs[name] else nil
		if held and def then
			total += held.rank
			for _, m in Relics.modifiers(def, held.rank) do
				table.insert(out, m)
			end
		end
	end
	local bonus = Relics.synergy(total)
	if bonus > 0 then
		table.insert(out, { stat = "Damage", kind = "increased", value = bonus, source = RelicTypes.SYNERGY_SOURCE })
		table.insert(out, { stat = "MaxLife", kind = "increased", value = bonus, source = RelicTypes.SYNERGY_SOURCE })
	end
	return out
end

return Relics
