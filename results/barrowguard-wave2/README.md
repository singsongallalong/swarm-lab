# barrowguard-wave2: the Broken Barrows' grave armour (wardrobe wave 2, Heartland, 2026-11-02)

Brief `targets/arpg-game/armour/briefs/Barrowguard.toml`: the grave armour of an old barrow
king's guard, buried centuries ago, dug out, still faintly regal; tarnished bronze, grave-moss
green, bone, mould-black leather; one strong silhouette idea; 64-part set budget. Six DeepSeek
Flash generators on `barrowguard-directions.txt`, run off-peak on arpg-game main.

- **Run:** 5 of 6 survived the draft (g04 stopped with generator exit 1); one resume brought it
  to 6 of 6. Rework from the first critic's notes: 6 of 6 survived again (g02 exited 1 during its
  rework, but its set still passes).
- **Cost:** the harness says $1.57 (draft and resume $1.00, rework $0.57). The real balance is
  shared with the parallel Grashan and Aor'lan sessions, so it is reported for the four Heartland
  runs together in `library/clothing/README.md`'s section, not per run.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): D 7.58, E 7.08, B 6.93, C 6.78, F 6.45, A 6.20. Pass 2
  after the rework (`critique/`, the sheets here): A 7.30, C 6.90, D 6.80, B 6.35, F 6.20, E 5.50.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | A | BarrowguardBonewrap | 63 | bronze crown over a pale bone face mask, the clearest top-down read |
| 2 | D | BarrowguardKing | 55 | bone-spike crown and moss through bronze plate, the dug-up story told best |
| 3 | C | BarrowguardRoundel | 61 | black-and-bronze with a round grave-disc on the back, a palette nobody else owns |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/barrowguard-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`7c1c5fb` with the three sets applied; `Catalog`, `ContentCompleteness` and `DressBudget` pass.

The critics disagreed more than in the gown runs: A rose from last to first after its rework, and
E fell from second to last. No set makes tarnished bronze its main metal: A and D lean brown
towards leather, and E and F lean green towards fenscale. The second critic's graft: A's crown
and bone face on C's black-and-bronze palette, plus D's moss patches.
