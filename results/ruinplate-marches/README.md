# ruinplate-marches: the Fetid Forest's armoured skirt (Drowned Marches pilot, 2026-11-01)

Brief `targets/arpg-game/gowns/briefs/Ruinplate.toml` (Rhodri, arpg-game R039): a knightly
woman's harness with a flared plate skirt, carved from the pale Grashan ruin stone, old bronze
and a little moss; `figure = "feminine"`. Six DeepSeek Flash generators on
`ruinplate-directions.txt`, run off-peak on arpg-game `a2b439d` (100-part set budget in the
run's base).

- **Run:** 6 of 6 finished and survived (no resume needed). Rework from the first critic's
  notes: 6 of 6 survived again (g03 hit its 40-turn cap in the rework; its set still passes).
- **Cost:** the harness says $2.83 (draft and rework); the real DeepSeek balance fell $2.85
  (34.54 to 31.69), which may include a little of the parallel Wispbride session's spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`: the
  gowns `select.md` rubric made render-only, weighted reads 0.35, elegance 0.3, skirt 0.2,
  parts 0.15). Pass 1 (`critique-1/`, `sheet-pass1.png`): F 7.2, D 6.65, B 6.55, C 5.9,
  E 5.2, A 4.05. Pass 2 after the rework (`critique/`, the sheets here): F 7.3, C 7.0,
  D 6.65, B 6.1, A 5.13, E 4.93.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | F | RuinplateQueen | 80 | pale-stone tiered bell with bronze lips and moss bands, a cinched waist, a prong crown |
| 2 | C | RuinplateZiggurat | 89 | a stepped skirt like a ruin's terraces; the most "carved from the ruins" outline |
| 3 | D | RuinplateStatue | 96 | the most courtly: V-neck cuirass, hooped tassets corded in bronze, moss at the hem |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/ruinplate-marches/`. Part counts are `ArmourLook.partCount` on arpg-game main
with all three renamed patches applied together; `Catalog`, `ContentCompleteness` and
`DressBudget` pass.

Shared flaws: square sleeve blocks about as wide as the torso (the shoulder check passes them,
both critics read them as broad), and dark grey backs that read as iron from behind.
