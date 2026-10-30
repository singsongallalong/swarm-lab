# Select: area palettes, run $run

$count palettes for future areas passed the checks (bible limits, one colour per material,
catalog, lint, format). The pack is `$pack`. Candidates are letters; don't open `key.json`.

Open `sheet.png`, then each `sheet-<letter>.png`: its swatches, the moor's map repainted in
it over two seeds, and a ruin up close.

$candidates

Judge each, 0-10:

1. **Its own place** (weight 3): at night, in colour alone, does it say what its place is, and
   could it be taken for the moor, the field, the Ashfields, Rimeholt, or another candidate?
2. **Reads from the camera** (weight 3): road against walkable ground, walkable against rock
   and far land, from the high view and at eye level.
3. **The accent** (weight 2): one clear, muted idea that things in the place can wear.
4. **Mood** (weight 2): dark, matte, gothic night; never washed out, never neon.

Keep every palette worth an area (no fixed count), and say which two are strongest.

Write `selection.json`:

```json
{
  "picked": ["C", "F"],
  "reasons": {"C": "<one sentence>"},
  "fixes": {"C": "<the main thing to change, or none>"},
  "notes": "<what the run taught, or empty>"
}
```
