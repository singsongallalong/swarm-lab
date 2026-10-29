# classic-gowns: gothic lolita for the classic blocky body (2026-10-29)

The `Classic` brief asked for the outfit from fan art fafwa shared: a classic yellow
Roblox figure in a black-and-crimson gothic lolita dress. It was built toy-like and chunky
for the blocky body, under the `feminine` figure and its shoulder check, with six takes on
one outfit (`targets/arpg-game/gowns/classic-directions.txt`). All 6 survived, and all
passed the shoulder check. Two ran out of turns at 100 and were resumed for 30 more.
$3.93 in total. `report.md` has the numbers.

`classic-gowns-6up-front-arpg-b229fe1.png` shows all six on arpg-game `b229fe1`, front and
the ARPG camera, at 520 px a view. In order: Faithful (A), Catalog minimal (C), Inverted (D),
Stitched doll (E), Clockwork (F), Long and solemn (B).

- **D, picked first:** Inverted, a crimson dress with black lace tiers and bows. It's the
  only set that reads as gothic lolita from the high camera.
- **B, picked second:** Long and solemn, an ankle-length tiered A-line with a veil. The best
  silhouette, but nearly all black from above.
- **F, picked third:** Clockwork, with a clock-face waist bow, a brass key and a studded
  lace band. 100 parts, at the budget.
- Passed over:
  - A (Faithful) and C (Catalog minimal) are clean, but black on black from above.
  - E (Stitched doll) has charming patches, but they're too small to read.

A shared flaw: on the classic body the arms hang at the hips, so the bell sleeves and the
upper skirt make one wide block at the waist. Only D's round, scalloped skirt flares past
it. `selection.json` has the reasons and the first fix for each.

As with the courtly gowns, every set is 55 to 100 parts, so it needs
`PerfBudget.armour.parts` raised in the game or cut to 64. All use the names
ClassicHeaddress, ClassicDress, ClassicSleeves and ClassicHem, so apply one patch at a time
on arpg-game `b229fe1`:

    git apply <swarm-lab>/results/classic-gowns/candidate-D.patch
