# quarrywright-wave2: the Charnel Quarry's dead quarrymen (wardrobe wave 2, 2026-11-02)

Brief `targets/arpg-game/armour/briefs/Quarrywright.toml` (Rhodri, arpg-game R039): the gear of
the dead quarrymen of the Charnel Quarry (levels 18-22) and the guards who drove them:
dust-white, tool-hung, funerary; pale quarry grey, stone dust white, rusted iron, linen wraps,
one cold dark slate; 64 parts. Six DeepSeek Flash generators on `quarrywright-directions.txt`,
run off-peak on arpg-game `a45a052` (no figure, standard 64-part budget).

- **Run:** 5 of 6 survived the draft: g00 (letter C) hit its 70-turn cap without a manifest and
  passed after one resume (40 turns). Rework from the first critic's notes: 6 of 6 survived.
- **Cost:** the harness says $1.49 (draft, resume and rework). The real DeepSeek balance fell
  $0.87 over the run (15.41 to 14.54), which includes any spend by the parallel sessions.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): F 7.5, E 7.1, C 6.55, A 6.15, B 5.9, D 4.6. Pass 2 after the
  rework (`critique/`, the sheets here): A 7.5, D 7.2, B 6.55, E 5.85, C 5.4, F 5.05.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | A | QuarrywrightCarrier | 53 | a wooden carrying yoke across the shoulders over a dust-masked, hand-wrapped quarryman |
| 2 | D | QuarrywrightWarden | 60 | dark slate box helm over a pale heavy body, a skull charm at the hip; the best fit |
| 3 | B | QuarrywrightDustcap | 59 | the most dust-white set: crossed straps under a strong slate cap |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/quarrywright-wave2/`. Part counts are `ArmourLook.partCount` on arpg-game main
`a45a052` with this session's twelve Grashan sets applied; all three are within the 64-part
budget, and `Catalog`, `ContentCompleteness` and `DressBudget` pass.

The critics disagreed more than in any other Grashan run. Pass 1's top two (F's stone-block mask,
E's niche hood) read as iron after the rework and fell to the bottom. A took first with the
shoulder yoke the first critic asked for (the draft's "Yoke" had none that read): the one rework
in this wave that clearly raised a set. Every set's pale grey body leans toward iron, and the
funerary half of the brief and readable tools are mostly missing.
