--!strict
-- The contract for Eternal Domain keys (docs/design/endgame-power.md section 3.4): the
-- types `data/RelicKeys` fills, the constants, and exactly what pure `systems/RelicKeys`
-- must do. Every number is a PLACEHOLDER for Rhodri.
--
-- A key has a tier, 1 to #data.tiers (I to V today; a season may add at most one). A higher
-- tier means harder monsters (levelBonus), better relic grade odds (gradeWeights) and more
-- relic rolls at the end (rolls). Each key rolls one or two modifiers for its run, from the
-- pool of modifiers allowed at its tier, shown before it's used.
--
-- systems/RelicKeys exports exactly these functions. Every one is pure: no Roblox API, no
-- yielding, no math.random or Random.new (randomness only from the rng passed in). None
-- changes `data`, and every list returned is a new table the caller may change (tierDef's
-- row is the one exception: it is data's own row, read-only to callers).
--
--   tierDef(data: Data, tier: number): TierDef?
--     The row for `tier`, or nil when `tier` is not a whole number from 1 to #data.tiers
--     (0, 6, 2.5, -1, NaN and math.huge are all nil).
--
--   allowed(data: Data, tier: number): { string }
--     The names of every modifier with minTier <= tier, sorted A to Z (string <). An
--     invalid tier (as tierDef) gives {}.
--
--   excludes(data: Data, a: string, b: string): boolean
--     True when a and b may not share a run: either one lists the other in its `excludes`.
--     A modifier always excludes itself (a == b is true). A name not in data.modifiers
--     excludes nothing but itself.
--
--   rollModifiers(data: Data, tier: number, rng: Random): { string }
--     The run's modifiers: 1 or 2 names, all from allowed(data, tier), never the same name
--     twice, never two that exclude each other. Its first draw sets the count: one
--     rng:NextNumber(), aiming for two when the draw < tierDef.twoChance, else one. The
--     first pick is uniform over allowed(data, tier); the second is uniform over the allowed
--     names that are neither the first nor excluded by it. Picks index allowed()'s sorted
--     list, so the same seed gives the same result however `data` was built. If no second
--     name is possible it returns just the first.
--     An invalid tier, or a tier that allows nothing, gives {}.
--
--   runPay(data: Data, tier: number, progress: number, cleared: boolean): number
--     The relic rolls the key holder gets. full = tierDef.rolls. A clear pays full, whatever
--     progress says. A failure pays math.floor(full * p * FAIL_SHARE), where p is progress
--     clamped to 0..1 (NaN counts as 0), and at least 1 once p >= MIN_PROGRESS. An invalid
--     tier pays 0.
--
--   partyShare(data: Data, tier: number, memberCount: number, rng: Random): { number }
--     Relic rolls for each member of a party that cleared the run, holder first: index 1 is
--     the holder with the tier's full rolls; each other member gets 1 roll with chance
--     MEMBER_CHANCE (one rng:NextNumber() draw per member, in order: 1 when the draw <
--     MEMBER_CHANCE), else 0. memberCount is floored; the list's length is the floored
--     count. memberCount below 1, NaN or not finite, or an invalid tier, gives {}.

export type Grade = "Lesser" | "Greater" | "Exalted"

-- Relative chances of each relic grade a roll from this tier gives; not percentages.
export type GradeWeights = { Lesser: number, Greater: number, Exalted: number }

export type TierDef = {
	tier: number, -- equals its index in Data.tiers
	gradeWeights: GradeWeights,
	rolls: number, -- relic rolls a clear pays the holder: a whole number, at least 1
	levelBonus: number, -- monster levels above the level cap: a whole number, at least 0
	twoChance: number, -- chance, 0..1, that the key rolls two modifiers rather than one
}

export type ModifierDef = {
	name: string, -- equals its key in Data.modifiers
	title: string, -- shown on the key: "Burning Floors"
	about: string, -- one line for the key's tooltip
	minTier: number, -- allowed on keys of this tier and above: a whole number, 1..#tiers
	excludes: { string }?, -- names it may never share a run with (either side may list it)
}

export type Data = {
	tiers: { TierDef }, -- tiers[i].tier == i
	modifiers: { [string]: ModifierDef },
}

local RelicKeyTypes = {}

RelicKeyTypes.GRADES = { "Lesser", "Greater", "Exalted" } :: { Grade }
RelicKeyTypes.FAIL_SHARE = 0.5 -- a failed run pays at most half the rolls
RelicKeyTypes.MIN_PROGRESS = 0.25 -- a failure this far in pays at least one roll
RelicKeyTypes.MEMBER_CHANCE = 0.15 -- each other party member's chance of one roll

return RelicKeyTypes
