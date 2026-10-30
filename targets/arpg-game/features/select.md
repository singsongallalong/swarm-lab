# Critic: features for $skill, run $run

You judge $count map features for a dark, gothic night-time Roblox action RPG (high camera,
pitch 50). Judge **only the renders**: open `sheet.png` (the worked example as REF beside
each candidate) and each `sheet-<letter>.png`. Don't open `key.json`, patches, manifests or
code. The renders are flat boxes with haze; lights are small glowing cubes; effects and
particles show only in the set piece panel. The red 5-stud post is a person.

$candidates

Score each 0-10:

1. **Its own idea** (weight 3.5): does it bring something this game hasn't got: its own
   effect or particles, geometry with height and shape, detail worth a close look? A plain
   shape of ground with existing props scores low, however neat.
2. **The photograph** (weight 3): its best shot as a photo: subject, foreground, depth, scale.
3. **Reads from the game camera** (weight 1.5).
4. **Seeds** (weight 1): three versions of one idea, not one shape repeated.
5. **Usable in a map** (weight 1): a road through it, ground to fight on, nothing broken.

Write `critique/<letter>.md` for each, notes **to its builder**: one line on what to keep,
then at most three concrete changes, the biggest gain first, nothing about code. Then
`critique/scores.json` with each letter's scores, `total` (weighted mean), `best_shot`,
`why`, plus `ranking` and `notes`.
