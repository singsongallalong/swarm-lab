# Critic: kit pieces for the $skill, run $run

You judge $count pieces of one area's kit: props and landmarks for the **Eternal Domain**, a
Roblox action RPG's endgame dungeon, the domain of the gods: colossal halls of ivory stone
and gold on cloud, holy light, monumental and a little terrible (the rest of the game is dark
night gothic; this is its opposite). A builder will place these pieces many times in a
generated dungeon seen from a high camera (pitch 50). Judge **only the renders**: open
`sheet.png` (an existing colossus from another place as REF) and each `sheet-<letter>.png`.
The sculpt render shows each sculpt over three seeds from three-quarters; the set piece
render shows its effect from the game camera at two moments, from three-quarters and from
above. The dark red 5-stud post is a person. Renders are flat-shaded boxes; there is no real
lighting. Don't open `key.json`, patches, manifests or code.

$candidates

Score each 0-10:

1. **The piece, in this place** (weight 3): recognisable as what its line asks for, and
   unmistakably the Domain (ivory, gold, holy, monumental).
2. **Shape and detail** (weight 2.5): silhouette, height, depth, detail worth a close look.
3. **Reads from the game camera** (weight 1.5).
4. **Seeds** (weight 1.5): three versions of the piece, not one shape repeated.
5. **Its effect** (weight 1.5): the set piece adds light or movement that makes the piece;
   score 5 if it has none and needs none, lower if it needed one.

Write `critique/<letter>.md` for each: one line on what to keep, at most three concrete
changes, nothing about code. Then `critique/scores.json` with each letter's scores, `total`
(weighted mean), `why`, `ranking`, and `"shelf"`: the letters a builder should take into the
dungeon (any number), each with one sentence on where in a dungeon it belongs.
