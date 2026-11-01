# floodchoir-marches: the Drowned Parish's church gown (Drowned Marches pilot, 2026-11-01)

Brief `targets/arpg-game/gowns/briefs/Floodchoir.toml` (Rhodri, arpg-game R039): what the
flooded parish's choir, nuns or mourners might wear, black and solemn but beautiful, with
stained-glass or candle hints; black, slate, wet stone, candle amber, a touch of crimson or
violet; `figure = "feminine"`. Six DeepSeek Flash generators on `floodchoir-directions.txt`, run
off-peak on arpg-game `a2b439d` (100-part set budget in the run's base).

- **Run:** 6 of 6 survived (no resume needed: g04 exited after writing its manifest). Rework
  from the first critic's notes: 6 of 6 survived again (g03 hit its 40-turn cap in the rework;
  its set still passes).
- **Cost:** the harness says $2.88 (draft and rework); the real DeepSeek balance fell $2.68
  (29.04 to 26.36), which includes some of the parallel Mossveil session's spend.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): B 7.03, F 6.8, A 6.2, D 5.75, E 5.5, C 4.65. Pass 2
  after the rework (`critique/`, the sheets here): B 7.0, F 6.83, D 6.3, C 5.95, A 5.85, E 3.8.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | B | FloodchoirNun | 99 | wimpled choir nun: fitted waist, full A-line to the floor, candle-amber wimple band, violet stole |
| 2 | F | FloodchoirChorister | 93 | black with a violet front panel and back bow, bone collar, crimson jewel; best colour from above |
| 3 | D | FloodchoirSteeple | 71 | a spire hat like the leaning church tower over a stained-glass bodice window |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/floodchoir-marches/`. Part counts are `ArmourLook.partCount` on arpg-game main
with all nine pilot sets from this session (Ruinplate, Tidewrack, Floodchoir) applied together;
`Catalog`, `ContentCompleteness` and `DressBudget` pass.

Mostly black sets fight the night: from the high camera only bands of amber, violet or bone
carry them. The gothic-lolita take (E) came last both times (its hem became a hollow box, its
cap a bucket helm). C's candle crown is the best headpiece idea and worth grafting onto B.
