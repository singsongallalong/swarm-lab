# cinderveil-wave2: Aor'lan Mountain's gown (wardrobe wave 2, 2026-11-02)

Brief `targets/arpg-game/gowns/briefs/Cinderveil.toml` (Rhodri, arpg-game R039): a mountain
gown, basalt-dark and elegant, made by the mountain's devotees, with the red of the lava cracks
running through it; basalt black, ash grey, magma red, a little sulphur; a real flare from the
hip and slim sleeves; `figure = "feminine"`. Six DeepSeek Flash generators on
`cinderveil-directions.txt`, run off-peak on arpg-game `20eaa41` (100-part set budget in the
run's base).

- **Run:** 6 of 6 survived (no resume needed). Rework from the first critic's notes: 6 of 6
  survived again (g00 and g05 hit their 40-turn cap in the rework; both sets still pass).
- **Cost:** the harness says $2.62 (draft and rework). The DeepSeek balance fell from 26.33 to
  22.73 over the run, but the key is shared with the parallel Heartland and Grashan sessions,
  so that $3.60 includes some of their spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): C 6.85, D 6.6, A 5.55, B 5.4, F 4.6, E 4.05. Pass 2
  after the rework (`critique/`, the sheets here): C 6.85, A 6.55, B 6.45, F 5.85, E 4.6, D 4.5.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | C | CinderveilObsidian | 83 | obsidian court: fitted black bodice, ash corset, sulphur sash, wide charcoal bell with a magma-red hem |
| 2 | A | CinderveilCrystal | 71 | black crystal crown, basalt bodice seamed with red cracks, the best flare from the hip |
| 3 | B | CinderveilFissure | 66 | bright jagged magma cracks over basalt, ash stole and hem; the strongest lava read |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/cinderveil-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`20eaa41` with the three sets applied together; `Catalog`, `ContentCompleteness` and
`DressBudget` pass, and each patch also applies alone.

No take made slim sleeves, though the brief asks twice: every set kept full-width arm blocks,
so this ask needs a check or an example in the pack, not words. D's stepped skirt led pass 1
and came last in pass 2 (a statue on a plinth after the rework). The best combination would be
C's outline with B's cracks and E's ash grey and sulphur.
