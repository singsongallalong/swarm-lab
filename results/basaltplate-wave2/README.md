# basaltplate-wave2: Aor'lan Mountain's heavy plate (wardrobe wave 2, 2026-11-02)

Brief `targets/arpg-game/armour/briefs/Basaltplate.toml` (Rhodri, arpg-game R039): a heavy
plate set cut from the mountain, basalt slabs and black iron with red seams between plates, like
the basalt golems; basalt black, iron grey, magma red seams (colour, not Neon); 64-part budget.
Six DeepSeek Flash generators on `basaltplate-directions.txt`, run off-peak on arpg-game
`20eaa41`.

- **Run:** 6 of 6 survived (no resume needed). Rework from the first critic's notes: 6 of 6
  survived again. (A first launch at 05:31 UTC waited for off-peak hours and was lost when the
  container was recycled; the run started at 10:36 UTC.)
- **Cost:** the harness says $1.45 (draft and rework). The DeepSeek balance fell from 18.44 to
  16.74 over the run; the key is shared with the parallel Heartland and Grashan sessions, so
  that includes some of their spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`; the
  armour `select.md` rubric with the brief's families in place of the barbarian's). Pass 1
  (`critique-1/`, `sheet-pass1.png`): E 7.35, A 7.0, B 6.2, F 5.75, C 5.65, D 4.75. Pass 2 after
  the rework (`critique/`, the sheets here): B 7.65, C 7.3, D 6.9, A 6.5, F 6.25, E 5.85.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | B | BasaltplateTerrace | 64 | shoulders stacked into stepped basalt ledges with red seams, a chest crack, a low sealed helm with a red slit |
| 2 | C | BasaltplateCrag | 60 | one big raw basalt crag breaking out of the right pauldron: a mountain outline |
| 3 | D | BasaltplateCairn | 59 | clean slab plate, red undersides on sloped pauldrons, a cairn-stone helm |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/basaltplate-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`20eaa41` with the nine Aor'lan sets so far applied together; `Catalog`, `ContentCompleteness`
and `DressBudget` pass, and each patch also applies alone. All three fit the 64-part budget.

The two passes disagreed more than in any other wave-2 run: E and A led pass 1 and fell to
the bottom after the rework, while B, C and D all rose. All six are black slab plate with red
seams, so the shoulder idea carries the family. Every set leaves the dummy's green hips and legs
showing between plates.
