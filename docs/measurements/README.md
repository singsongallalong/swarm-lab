# Measurements behind the packs' numbers

Renders made with arpg-game's own `scripts/areapreview` at `edb9b50` (main,
2026-10-29), on Cold Snap's 8-stud circle in Ice Spear's blue, from a scratch copy of
the game with probe rows added. The particle guide's size table
(`targets/arpg-game/effects/particles-guide.md`) comes from these. Remeasure if the
preview's particle drawing or `AreaBursts.SCALE` changes.

- `particle-sizes-wave-and-rocks-p0-edb9b50.png`, power 0, top to bottom:
  1. SweepWave with `SlamDust` as shipped (puffs end at 2.4 studs, × 0.5 for a Wave = 1.2): specks.
  2. A frost row ending at 1.2 studs (0.6 on screen): gone.
  3. Ending at 2.4 (1.2 on screen): specks.
  4. Ending at 4.8 (2.4 on screen): distinct puffs.
  5. Ending at 4.8, `lightEmission` 0.5: clearly visible at night, the biggest single gain.
  6. HeavedRocks with a full-scale `burst` (frost, ending 3.0, half-lit, 24 per burst): there,
     but mostly hidden among the stones from the game camera.
- `particle-rocks-burst-rising-p0-p8-edb9b50.png`: the same Rocks look with a burst that
  rises (speed 10 to 16, spread 35°, upward acceleration 3, ending 4.2 studs, half-lit). It
  shows as a column above the stones from 0.3 s and lingers after they sink. At power 8 the
  stones grow and swallow it, because the burst's own scale doesn't grow: give `burstScale`
  a `perPower` share, as Cave-in does (A33).

Caveats: the preview's particles are a simulation with procedural sprites, right on
timing, reach and spread but not on texture (`render/AreaParticles`), and they flatter
faint particles (A31-D9). These numbers are a floor to aim above, not a target.
