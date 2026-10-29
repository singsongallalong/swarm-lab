# courtly-gowns: the first gowns run (2026-10-29)

Six DeepSeek Flash generators each designed a full-body courtly gown (headpiece, gown,
cuffs, hem and shoes) in a different era, under a 100-part set budget raised for this
experiment only (the game keeps 64). 5 of 6 survived; the cathedral gown never finished.
Four stopped early on the first pass and were resumed in their own sessions. $2.91 in
total. `report.md` has the numbers.

- **E, picked first:** medieval: a tall wimpled hennin over a deep plum bell with a fur band.
- **C, picked second:** rococo: faded rose and dove grey, black bows, a tiered bell skirt, a tilted cap.
- **A, picked third:** Victorian mourning: a veiled broad-brimmed hat, high neck, bustle, tiered skirt.
- B (baroque, wine brocade) and D (gothic lolita, after fafwa's reference) passed over: their
  puffed shoulders read as pauldrons from above.

`selection.json` has the reasons and the first fix for each. Each `candidate-<letter>.patch`
is the whole set (four look files, registry lines and catalog rows) on arpg-game main
`41c9339`, plus the budget: **every gown is 90 to 100 parts, so it needs
`PerfBudget.armour.parts` raised to 100 in the game, or cutting by about a third, before
it can merge.** All name their files CourtlyHeaddress, CourtlyGown, CourtlyCuffs and
CourtlyHem, so apply one at a time:

    git apply <swarm-lab>/results/courtly-gowns/candidate-E.patch

They're looks only: a base or a hand-made item decides who wears them.
