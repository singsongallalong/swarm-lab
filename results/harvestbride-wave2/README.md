# harvestbride-wave2: Farmland's country gown (wardrobe wave 2, Heartland, 2026-11-02)

Brief `targets/arpg-game/gowns/briefs/Harvestbride.toml` (Rhodri, arpg-game R039): what a farm
girl wears to the harvest festival or a village wedding, warm and homely beside the gothic dark;
wheat gold, apron linen, hearth red, field green, dark walnut; a real flare from the hip and slim
sleeves; `figure = "feminine"`. Six DeepSeek Flash generators on `harvestbride-directions.txt`,
run off-peak on arpg-game main (100-part set budget in the run's base).

- **Run:** 6 of 6 survived, no resume needed. Rework from the first critic's notes: 6 of 6
  survived again (one generator hit its 40-turn rework cap; its set still passes).
- **Cost:** the harness says $2.33 (draft $1.65, rework $0.68). The real balance is shared with
  the parallel Grashan and Aor'lan sessions, so it is reported for the four Heartland runs
  together in `library/clothing/README.md`'s section, not per run.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): D 6.68, F 5.78, E 5.58, B 5.2, A 4.45, C 3.7. Pass 2 after
  the rework (`critique/`, the sheets here): D 6.85, B 6.1, F 5.98, E 5.65, A 5.03, C 4.63.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | D | HarvestbrideMilkmaid | 85 | straw hat with a red ribbon over a tiered field-green bell, a true cone from the side |
| 2 | B | HarvestbrideApron | 80 | wheat-gold apron skirt flaring from the waist, the warmest country colour |
| 3 | F | HarvestbrideWheatcrown | 87 | tall wheat-sheaf crown over a parted gold skirt |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/harvestbride-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`7c1c5fb` with the three sets applied; `Catalog`, `ContentCompleteness` and `DressBudget` pass.

The brief's main ask, slim sleeves, was not met: both critics found shoulder-width block sleeves
on every set. Words in the brief did not change it; a sleeve-width check like the shoulder check
would. E's wide flare and C's ruffled forearm cuffs are the ideas worth grafting.
