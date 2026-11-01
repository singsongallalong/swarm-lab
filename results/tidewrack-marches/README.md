# tidewrack-marches: the Sunken Shelf's gown (Drowned Marches pilot, 2026-11-01)

Brief `targets/arpg-game/gowns/briefs/Tidewrack.toml` (Rhodri, arpg-game R039): a shore woman's
or corsair's dress of salvage, shell and sailcloth, with a skirt that flares or drapes; salt
white, driftwood, wet sand, tarnished brass, a little Naga teal; `figure = "feminine"`. Six
DeepSeek Flash generators on `tidewrack-directions.txt`, run off-peak on arpg-game `a2b439d`
(100-part set budget in the run's base).

- **Run:** 6 of 6 finished and survived (no resume needed). Rework from the first critic's
  notes: 6 of 6 survived again (g00 hit its 40-turn cap in the rework; its set still passes).
- **Cost:** the harness says $2.51 (draft and rework); the real DeepSeek balance fell $2.65
  (31.69 to 29.04), which includes some of the parallel Reedmail session's spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): D 7.05, E 6.85, A 6.55, C 5.65, F 5.1, B 4.9. Pass 2
  after the rework (`critique/`, the sheets here): A 7.2, E 6.65, C 6.1, F 6.0, B 5.0, D 4.5.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | A | TidewrackCorsair | 92 | dark driftwood bodice over an ivory sailcloth A-line, shell-fan crest, teal only at the sash |
| 2 | E | TidewrackShell | 86 | ivory bell skirt, a dark stomacher at the waist, thin teal trims; best on the slim avatar |
| 3 | C | TidewrackSailcloth | 88 | laced bodice and torn sailcloth drapes, all salt and ivory; the most on-theme for the wrecks |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/tidewrack-marches/`. Part counts are `ArmourLook.partCount` on arpg-game main
with these three and the three Ruinplate sets applied together; `Catalog`,
`ContentCompleteness` and `DressBudget` pass.

The rework reshuffled the run: D (first after the draft, a flared tier skirt) lost its flare
and fell to last. F's corsair tricorn is the boldest headpiece and worth borrowing. Every set
keeps wide, boxy sleeves. Trap: g04 also wrote two look files outside its worktree (to
`swarm-lab/tidewrack-marches/`); they were deleted, never committed.
