# fortwarden-wave2: the town garrison's kit (wardrobe wave 2, Heartland, 2026-11-02)

Brief `targets/arpg-game/armour/briefs/Fortwarden.toml`: the fort's garrison round the town's
fort and tower in Farmland, the first real armour a new player sees on others; heraldic,
sturdy, honest; town blue and cream heraldry, steel, brown leather, a brass badge; one strong
silhouette idea; 64-part set budget. Six DeepSeek Flash generators on
`fortwarden-directions.txt`, run off-peak on arpg-game main.

- **Run:** 6 of 6 survived the draft (g01 exited 1, but its set passed, so no resume was
  needed). Rework from the first critic's notes: 6 of 6 survived again.
- **Cost:** the harness says $1.25 (draft $0.94, rework $0.31). The real balance is shared with
  the parallel Grashan and Aor'lan sessions, so it is reported for the four Heartland runs
  together in `library/clothing/README.md`'s section, not per run.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): F 7.55, D 7.18, E 7.05, A 6.85, C 6.28, B 6.18. Pass 2
  after the rework (`critique/`, the sheets here): D 7.35, F 7.30, A 7.00, E 6.20, B 5.90, C 5.85.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | D | FortwardenSergeant | 64 | quartered blue-and-cream surcoat, cream cross on the cap crown, the clearest heraldry from above |
| 2 | F | FortwardenGatewarden | 64 | crested sallet, cream-edged pauldrons and a big brass chest roundel |
| 3 | A | FortwardenMilitia | 60 | wide steel kettle-hat brim over a blue coat, the town watchman |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/fortwarden-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`7c1c5fb` with the three sets applied; `Catalog`, `ContentCompleteness` and `DressBudget` pass.
Sergeant and Gatewarden sit exactly on the 64-part budget, so a fix must trade parts, not add them.

Both critics put D, F and A in the top three, though not in the same order. The common weakness: the
heraldry sits on the chest front, where the high camera never looks; the pauldron tops and helm
crown should carry the town colours. E's back pavise was the idea worth grafting, but it never
read from above; B and C drift into iron with grey slab pauldrons.
