# relickeys-1: Flash x4 on the RelicKeys contract (2026-10-30)

The relics stream's step 1 (arpg-game `docs/streams/relics.md`): a test of the
`deepseek-workers` skill as an ordinary `swarm task` (`tasks/relickeys.toml`), from a cloud
session. Claude wrote the contract (`RelicKeyTypes.luau`, in `base.patch`, a local commit
never pushed to the game), the visible spec, a held-out spec of the contract's edge cases
(`RelicKeysHeldOut.spec.luau`, kept outside both repos during the run) and a reference
(`RelicKeys.reference.luau`) to prove both specs passable. Workers wrote
`systems/RelicKeys` (six pure functions, data passed in) and `data/RelicKeys` (5 tiers,
10 to 14 text-only run modifiers). Nothing landed in the game.

| Letter | Gen | Held-out | Turns | Seconds | Cost (est.) | Review: correct / fit / rows / total |
|---|---|---|---|---|---|---|
| A | g00 | 9/9 | 12 | 171.6 | $0.051 | 10 / 9 / 6 / 8.5 |
| B | g03 | 9/9 | 11 | 201.2 | $0.051 | 10 / 8 / 7 / 8.5 |
| C | g02 | 9/9 | 19 | 234.6 | $0.062 | 10 / 8.5 / 6 / 8.35 |
| D | g01 | 9/9 | 19 | 228.2 | $0.062 | 10 / 8 / 7.5 / 8.65 |

Findings:

- 4 of 4 passed every visible check and every held-out test, about 3–4 minutes each.
  relics-1 had misses; the difference is the contract: here it named every bad input
  and fixed the rng draw order, and the system took its data as an argument, so the
  held-out spec could use fixtures and pin exact draws.
- The blind review (`review.json`, letters only) traced NaN/inf/fractional tiers and
  member counts, progress clamping, either-side exclusions, draw order and aliasing, and
  found **no bugs in any of the four**. Scores split only on style and the rows.
- Rows are where judgement shows: two builds wrote modifiers that make runs *easier*,
  one named monsters and a speed stat against the brief, and the best set (D) still
  promised reward changes `runPay` doesn't make (Bitter Harvest, Double or Nothing).
- Requests found one real gap: whether `rollModifiers` spends its count draw on an
  invalid or empty tier (all chose not to; the contract should say so). One asked for an
  upper bound on `memberCount`.
- Real spend could not be measured: the balance fell from $2.29 to $1.74 over the run and
  kept falling after it ($1.61 a minute later) with nothing of this session running, so
  another user of the same key was spending at the same time. The estimate was $0.23 for
  2.52M tokens; at the sheet's rate of about $0.012 per million real cost was a few cents.
- The reviewer would take A's system and D's rows with those two reworded.
