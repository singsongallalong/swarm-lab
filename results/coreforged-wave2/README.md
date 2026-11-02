# coreforged-wave2: the Aor'lan Core's EPIC plate (wardrobe wave 2, 2026-11-02)

Brief `targets/arpg-game/armour/briefs/Coreforged.toml` (Rhodri, arpg-game R039): an **EPIC**
plate set forged in the Core, black plate split by glowing magma cracks, regal and dangerous;
basalt black, molten orange-red, ember gold; places for light to live (seams, gems, a crown),
Neon on two or three small parts, no particles (the game will add a worn effect later); 64-part
budget. Six DeepSeek Flash generators on `coreforged-directions.txt`, run off-peak on arpg-game
`20eaa41`.

- **Run:** 6 of 6 survived (no resume needed). Rework from the first critic's notes: 6 of 6
  survived again.
- **Cost:** the harness says $1.51 (draft and rework). The DeepSeek balance fell from 16.74 to
  15.26 over the run; the key is shared with the parallel Heartland and Grashan sessions, so
  that includes some of their spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`; the
  armour rubric plus an EPIC criterion: noticed across the field, places for light, not
  garish). Pass 1 (`critique-1/`, `sheet-pass1.png`): D 7.65, A 7.35, C 7.0, B 6.2, E 5.55,
  F 4.95. Pass 2 after the rework (`critique/`, the sheets here): A 7.65, C 7.475, D 7.025,
  B 7.0, E 6.6, F 5.875.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | A | CoreforgedKing | 64 | gold spiked crown, flared black pauldrons cut by molten seams, a cross crack on the breast, a black war-cape |
| 2 | C | CoreforgedHorned | 64 | long gold-capped horns, glowing eye slits, a burning diamond heart on the chest |
| 3 | D | CoreforgedVent | 64 | gold-crowned helm with a glowing chimney, vent chimneys rising from the shoulders |

A's generator named its slots Crown, Cuirass, Gauntlets and Greaves, so its looks are
`CoreforgedKingCrown`, `CoreforgedKingCuirass`, `CoreforgedKingGauntlets` and
`CoreforgedKingGreaves`.

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/coreforged-wave2/` (each `about.json` has `"epic": true`). Part counts are
`ArmourLook.partCount`; all twelve Aor'lan sets apply together, and each alone, on arpg-game
main `a45a052`, where `Catalog`, `ContentCompleteness` and `DressBudget` pass. All three sit
exactly at the 64-part budget.

The same three led both passes, the steadiest ranking in the wave. Black, molten orange and
gold carry the EPIC read from above far better than Basaltplate's black and red; the risk is
over-lighting (D) before the game's worn effect is added. Every set leaves the dummy's olive
hips showing.
