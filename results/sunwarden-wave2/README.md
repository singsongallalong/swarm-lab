# sunwarden-wave2: the Grashan sentinels' armour (wardrobe wave 2, 2026-11-02)

Brief `targets/arpg-game/armour/briefs/Sunwarden.toml` (Rhodri, arpg-game R039): the armour of
the ancient Grashan sentinels, the warriors the statues were carved after, for the Grashan Ruins
round the Statue Colossus (levels 16-20): massive, simple and heavy; old green-bronze, pale ruin
stone, sun gold; 64 parts. Six DeepSeek Flash generators on `sunwarden-directions.txt`, run
off-peak on arpg-game `a45a052` (no figure, standard 64-part budget).

- **Run:** 6 of 6 survived, no resume needed. Rework from the first critic's notes: 6 of 6
  survived again (g00, g02 and g05 hit their 40-turn cap in the rework; their sets still pass).
- **Cost:** the harness says $1.49 (draft and rework). The real DeepSeek balance fell $1.76 over
  the whole run (17.17 to 15.41), which includes the parallel Heartland and Aor'lan sessions'
  spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): C 7.8, A 7.0, F 6.7, D 6.35, E 6.2, B 5.7. Pass 2 after the
  rework (`critique/`, the sheets here): A 7.8, F 7.0, C 6.53, B 5.83, D 5.6, E 5.23.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | A | SunwardenSunburst | 63 | radiating gold sunburst crest, wide pale-stone shoulder slabs over dark old bronze |
| 2 | F | SunwardenSunwheel | 62 | muted olive bronze and pale stone, a big sun-wheel on the back that shows from above |
| 3 | C | SunwardenBoulder | 55 | round barrel pauldrons with gold caps like two carved boulders; the most massive outline |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/sunwarden-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`a45a052` with this session's Grashan sets applied; all three are within the 64-part budget, and
`Catalog`, `ContentCompleteness` and `DressBudget` pass.

Too little sun gold and too much olive across the run, which risks reading as fenscale from
above, and every set leaves the avatar's green trousers showing at the thighs. Worth combining:
A's crest (thickened), C's barrel pauldrons and F's back wheel drawn as rays.
