# relickeys-1

Task: RelicKeys: the Eternal Domain's key rules and rows

4 of 4 workers passed every check; estimated cost $0.23 (the estimate runs high; real spend has been about 1.2 cents per million tokens).

## g00 (deepseek): passed, held-out 9/9

- turns 12, 171.6 s, $0.051
- says: Wrote the six pure key rules in src/shared/systems/RelicKeys.luau to the full contract (NaN and infinite tiers/progress/member counts, sorted allowed() picks, seed-stable one-or-two modifier rolls, failure pay, party share) and src/shared/data/RelicKeys.luau with five placeholder tiers (I at 80/18/2 with 2 rolls, V at 30/35/35 with 7) and 13 placeholder run modifiers spread over tiers 1-5, including three contradiction exclusions (FloodedHalls/BurningFloors, QuietGraves/GraveEcho, EmptyHalls/PackedHalls).
- asks: The contract does not say whether rollModifiers consumes a count draw when the tier is invalid or allows nothing; it returns {} without drawing.
- patch: `runs/relickeys-1/gens/g00/.swarm/patch.diff` (+275 -0); apply with `python3 -m swarm task apply runs/relickeys-1 g00`

## g01 (deepseek): passed, held-out 9/9

- turns 19, 228.2 s, $0.0618
- says: Built systems/RelicKeys.luau as the six pure functions of the RelicKeyTypes contract, handling every named bad input (tiers that are 0, 6, 2.5, -1, NaN or infinite; NaN/non-finite memberCount; NaN/out-of-range progress) and drawing count first, then the first pick, then an optional second, all indexed from the sorted allowed list so a seed replays regardless of how data was built. Built data/RelicKeys.luau with five placeholder tiers (I is 80/18/2; Lesser falls 80 to 35, Exalted rises 2 to 25, rolls 2 to 7, levelBonus 0 to 10, twoChance 0.1 to 0.7) and 13 text-only modifiers, five allowed at tier I, two at tier IV or V, with three exclusion pairs (BurningFloors/GlassedGround, TightCorridors/SwarmingHorde, GildedCurse/BitterHarvest).
- asks: rollModifiers does not say whether the count draw is consumed when the tier is invalid or allows no modifiers; I return {} before any rng draw.
- patch: `runs/relickeys-1/gens/g01/.swarm/patch.diff` (+271 -0); apply with `python3 -m swarm task apply runs/relickeys-1 g01`

## g02 (deepseek): passed, held-out 9/9

- turns 19, 234.6 s, $0.0621
- says: Wrote the six pure rules in systems/RelicKeys and a five-tier, 13-modifier data table. Tier I is Lesser/Greater/Exalted 80/18/2 with twoChance 0; tiers scale to rolls 2/3/4/5/7 and levelBonus 0/2/4/7/10, tier V twoChance 1; three exclusion pairs (BurningFloors/DrownedHalls, RisingDead/QuietGrave, HeavyAir/Quickening); all numbers are marked placeholders.
- asks: rollModifiers returns {} for a valid tier whose allowed pool is empty without spending the count draw; the contract does not say whether that draw should still happen.
- asks: partyShare has no upper bound on a large finite memberCount, so a literal reading would build a list that long; only below 1, NaN and infinities are rejected.
- patch: `runs/relickeys-1/gens/g02/.swarm/patch.diff` (+274 -0); apply with `python3 -m swarm task apply runs/relickeys-1 g02`

## g03 (deepseek): passed, held-out 9/9

- turns 11, 201.2 s, $0.0514
- says: Built the six-function pure RelicKeys system to the contract and a placeholder data table with five monotone tiers (I at 80/18/2, V at 24/46/30, rolls 2 to 7) and 12 modifiers whose exclusions are mutual on both sides. Tier I allows exactly four modifiers, three modifiers are IV/V only, and the four exclusion pairs are fire/frost, slick stone/wind, dark/falling light, and rising slain/unmaking hour.
- asks: The contract does not say whether rollModifiers consumes a second-pick draw when no second name is possible; I skip that draw and return just the first name.
- patch: `runs/relickeys-1/gens/g03/.swarm/patch.diff` (+287 -0); apply with `python3 -m swarm task apply runs/relickeys-1 g03`
