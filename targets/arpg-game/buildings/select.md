# Critic: building tilesets for $skill, run $run

You judge $count building tilesets for one area of a Roblox action RPG at night, seen from a
high camera (pitch 50). A tileset paints the game's generated buildings: walls, door and
window walls, corner posts, floors, roofs, and the broken stumps of ruins, plus trim parts
(beams, frames, shutters, rubble). The game today has two: the town's warm timber homes and
the moor's charcoal stone, both shown on `sheet.png` as REF. Every new one must give its area
buildings of its own. Judge **only the renders**: open `sheet.png` and each
`sheet-<letter>.png`. Each shows a house whole (two seeds), a cottage ruined (two seeds) and a
manor, from the front, the back and the top. The dark red 5-stud post is a person. Renders
are flat-shaded boxes in each part's colour: no materials, no lighting. Don't open
`key.json`, patches, manifests or code.

The area is described in the `## The brief` section of `$pack`: read that section only, not
the rest of the pack (it holds code).

$candidates

Score each 0-10:

1. **This area, no other** (weight 3): the buildings say the brief's place at a glance, and
   could not be the moor's stone or the town's timber repainted.
2. **Character in the trim** (weight 2.5): structure worth a close look at walls, posts,
   doors, windows and roof edges, not plain boxes in a new colour.
3. **Ruins** (weight 2): stumps and cut posts look like this material broken.
4. **Reads from above** (weight 1.5): walls, roofs, ridges and openings distinct.
5. **Restraint** (weight 1): Roblox-plain, night-dark, one muted accent, not busy.

Write `critique/<letter>.md` for each: one line on what to keep, at most three concrete
changes (colours, parts, proportions), nothing about code. Then `critique/scores.json` with
each letter's scores, `total` (weighted mean), `why`, and `ranking`.
