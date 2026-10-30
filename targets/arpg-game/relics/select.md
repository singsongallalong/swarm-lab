# Review: relics, run $run

$count builds of `systems/Relics` and three relic rows passed the visible specs. Each
candidate's work is in its patch (letters only; don't open `key.json`).

$candidates

Review each as a senior engineer on this repo would, from its patch alone:

1. **Correct** (weight 4): does it do exactly what the contract in
   `base/src/shared/RelicTypes.luau` says, including the cases the visible spec doesn't
   test? Name any bug with the input that shows it.
2. **Fit to merge** (weight 3): strict types, purity, the repo's rules, readable, comments
   that say why, nothing clever for its own sake.
3. **The relics** (weight 3): do the three rows play as their briefs say, with sensible
   numbers that grow, interesting rather than flat?

Write `review.json`: for each letter `{correct, fit, relics, total, bugs: [..], why}`,
plus `ranking` and `notes`.
