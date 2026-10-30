# Critic: cast motions, run $run

You judge $count cast motions for a dark, gothic Roblox action RPG. All key the same brief.
Judge **only the renders**: open `sheet.png` (Ground Slam, a good motion of another
kind, as REF) and each `sheet-<letter>.png`. Each candidate has two renders: the whole cast
(columns are moments, labelled with the time; the red bar marks the blow; rows are side,
front, three-quarter and the game's camera) and the blow up close. The body is blocky on
purpose. Don't open `key.json`, patches, manifests or code.

Read the brief first: the section "The brief" in `$pack` (only that section).

$candidates

Score each 0-10:

1. **Reads as the brief** (weight 3): is each described moment there, in order, recognisable?
2. **Weight and snap** (weight 2.5): a gathered wind-up, a fast blow, an impact with the body
   behind it, a settle; not an even wave.
3. **A clean body** (weight 2): nothing through the chest, head or thighs; the wrist doesn't
   flip; the feet stay planted; no joint bent past what a body does.
4. **The arc** (weight 1.5): the head travels a clean path over the top, not through the body.
5. **The recovery** (weight 1): it settles and hands back without a pop.

Write `critique/<letter>.md` for each, notes **to its animator**: one line on what to keep,
then at most three concrete changes, the biggest gain first, each naming the moment (its time
on the render) and what should change in the body or the weapon there. Nothing about code.
Then `critique/scores.json` with each letter's scores, `total` (weighted mean), `why`, plus
`ranking` and `notes`.
