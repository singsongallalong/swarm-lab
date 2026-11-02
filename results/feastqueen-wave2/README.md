# feastqueen-wave2: the Grashan Feast's epic gown (wardrobe wave 2, 2026-11-02)

**EPIC set.** Brief `targets/arpg-game/gowns/briefs/Feastqueen.toml` (Rhodri, arpg-game R039):
the most splendid dress of the ancient Grashan court, for the Grashan Feast rare map (levels
16-20), golden and candle-warm with a hint of the dream souring; rich gold, wine red, candle
amber, ivory, a little shade-black; places for light to live (a worn particle aura comes later
from the game), Neon on two or three small parts; a flared skirt and slim sleeves;
`figure = "feminine"`. Six DeepSeek Flash generators on `feastqueen-directions.txt`, drafted
off-peak on arpg-game `20eaa41` (100-part set budget in the run's base).

- **Run:** 6 of 6 survived, no resume needed. Rework from the first critic's notes (held for the
  off-peak window, started 10:37 UTC): 6 of 6 survived again (g00 and g02 hit their 40-turn cap
  in the rework; their sets still pass).
- **Cost:** the harness says $2.46 (draft and rework). The real DeepSeek balance fell $1.27 over
  the rework alone (18.44 to 17.17, which includes some of the parallel Heartland and Aor'lan
  sessions' spend). The draft overlapped the Grashanveil rework and the other sessions, so it
  can't be read off the balance alone.
- **Critics:** two fresh critic subagents judged the renders only (`critic-prompt.md`). Pass 1
  (`critique-1/`, `sheet-pass1.png`): F 6.53, B 6.08, A 5.35, E 5.08, D 4.8, C 4.6. Pass 2 after
  the rework (`critique/`, the sheets here): B 6.85, A 5.98, F 5.7, C 5.15, E 4.15, D 4.0.

## Picks

| Pick | Letter | Set (library name) | Parts | In short |
| --- | --- | --- | --- | --- |
| 1 | B | FeastqueenBanquet | 81 | wine bell skirt from the hip, gold butterfly bodice, candle crown; the richest epic read |
| 2 | A | FeastqueenIvory | 94 | gold bodice with a chain necklace over an ivory A-line, veil of candle spikes; the prettiest dress |
| 3 | F | FeastqueenSundisc | 95 | sun-disc crown and ruff collar over a pleated gold skirt flaring at the front |

`selection.json` has the reasons and first fixes. Renamed patches, sheets and part counts are in
`library/clothing/feastqueen-wave2/` (each `about.json` has `"epic": true`). Part counts are
`ArmourLook.partCount` on arpg-game main `a45a052` with this session's Grashan sets applied;
`Catalog`, `ContentCompleteness` and `DressBudget` pass.

Each set put Neon on about three small parts as asked, but from the camera the glow and the
shade-black souring barely show. All six keep shoulder-wide block sleeves. The best mix would be
B's skirt and bodice, F's crown and ruff, and A's necklace.
