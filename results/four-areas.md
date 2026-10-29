# Four new areas: Brinewrack, Saltbarrow, Rimeholt, Blightfen (2026-10-29)

Four area looks from the zones job, three DeepSeek Flash generators each, on arpg-game
`166b53d` (Brinewrack, Saltbarrow) and `617e067` (Rimeholt, Blightfen).

Each brief set its own climate, palette and one accent hue, because the Moonwell run's six
generators had all picked the same cold green-grey:

| Area | Palette | Accent | Place |
| --- | --- | --- | --- |
| Brinewrack | wet slate shingle and black rock | sea-green | a drowned coast |
| Saltbarrow | pale salt and grey-beige dust | ochre | a salt desert of giant bones and tombs |
| Rimeholt | blue-grey snow | ice-blue | a frozen highland |
| Blightfen | brown-black mud, dead olive reeds | sickly yellow-green | a plague bog |

Each of an area's three generators took a different direction (`targets/arpg-game/zones/directions-<area>.txt`).

**Results:** eight finished within 100 turns, and four were resumed for 30 more. All 12
survived every check. The four palettes came out clearly apart. The ledger estimates $6.10;
the DeepSeek balance fell $1.25 (15.08 to 13.83). The zones job now gets 130 turns.

`four-areas-first-picks.png` shows each area's first pick in one row: the whole map from above
and three-quarters, the pool site, the effect from the game camera, and the props.
Each `<area>-zones/` folder has all three of its candidates side by side, the patches,
`selection.json` with reasons and first fixes, and the report.

| Area | First pick | Second pick |
| --- | --- | --- |
| Brinewrack | B, the wreck graveyard: hull ribs from the bones kind, driftwood, a sea-green tideglow coiling over the pools | A, the lighthouse headland: the only real landmark, a dead lighthouse |
| Saltbarrow | B, the giant's ribcage: a colossal skeleton and royal tombs on pale salt | C, the tomb road: the best effect, an ochre glow coiling up from the tombs |
| Rimeholt | C, the frozen lake: ice pools, runestones with ice-blue glints, a glow under the ice | B, the barrow field: barrows and drifting snow |
| Blightfen | C, the plague pit: the clearest yellow-green miasma over brown-black bog | B, the dead orchard: rows of dead trees across the ground |

**Common fixes:** several of the effects are faint or off to one side from the game camera,
and landmarks are scattered prop sets. The maps job (drafted layouts that place their own
landmarks) is the next step for any area worth a map.

All of an area's candidates share its file and row names, so apply one patch at a time:

    git apply <swarm-lab>/results/<area>-zones/candidate-<letter>.patch
