# cliffwind-wave2: the Aor'lan Cliffs' armoured skirt (wardrobe wave 2, 2026-11-02)

Brief `targets/arpg-game/gowns/briefs/Cliffwind.toml` (Rhodri, arpg-game R039): an armoured
skirt set for a ridge-runner or cliff valkyrie, light armour over a flowing skirt the wind
catches; sky pale blue, cloud white, warm rock tan, steel; a real flare from the hip and slim
sleeves; `figure = "feminine"`. Six DeepSeek Flash generators on `cliffwind-directions.txt`, run
off-peak on arpg-game `20eaa41` (100-part set budget in the run's base).

- **Run:** 6 of 6 survived (no resume needed). Rework from the first critic's notes: 6 of 6
  survived again (g00 and g02 hit their 40-turn cap in the rework; both sets still pass).
- **Cost:** the harness says $2.82 (draft and rework). The DeepSeek balance fell from 22.73 to
  19.43 over this run; the key is shared with the parallel Heartland and Grashan sessions, so
  that includes some of their spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): A 7.13, B 6.33, F 5.1, D 4.65, E 4.05, C 3.33. Pass 2
  after the rework (`critique/`, the sheets here): A 7.35, B 7.0, D 5.6, E 4.95, F 4.45, C 3.75.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | A | CliffwindValkyrie | 75 | pale sky-blue steel A-line with a real bell, white stomacher and short cape, white bow-winged helm |
| 2 | B | CliffwindStorm | 80 | cloud-white skirt of jagged wind-cut panels flaring hard under grey-blue plate, winged helm |
| 3 | D | CliffwindEyrie | 74 | cloud-white bodice, sky-blue skirt, tan leather, steel feather-crested half-helm |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/cliffwind-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`20eaa41` with the six Aor'lan gown sets applied together; `Catalog`, `ContentCompleteness` and
`DressBudget` pass, and each patch also applies alone.

Again no set made slim sleeves. Most backs are dark and vanish at night, and the rock tan barely
appears; the pale sky-and-cloud palette reads far better from above than the wave's dark gowns.
