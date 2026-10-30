# Critic: features for the moor ($skill), run $run

You judge $count map features for a dark, gothic night-time Roblox action RPG (high camera,
pitch 50). Judge **only the renders**: open `sheet.png` (the worked example as REF beside
each candidate) and each `sheet-<letter>.png`. Don't open `key.json`, patches, manifests or
code. The renders are flat boxes with haze; lights are small glowing cubes; effects and
particles show only in the set piece panel. The red 5-stud post is a person.

$candidates

Score each 0-10:

1. **Its own idea** (weight 3): does it bring something this game hasn't got: its own
   effect or particles, geometry with height and shape, detail worth a close look? A plain
   shape of ground with existing props scores low, however neat.
2. **The photograph** (weight 2.5): its best shot as a photo: subject, foreground, depth, scale.
3. **Topology across seeds** (weight 2): in its twelve-seed sheet (`feature-seeds`), do the
   seeds have different layouts, paths and obstructions, or is it one layout jittered?
4. **Look across seeds** (weight 1): does each seed read as visually distinct?
5. **Reads from the game camera** (weight 0.75).
6. **Usable in a map** (weight 0.75): a road through it, ground to fight on, nothing broken.

Write `critique/<letter>.md` for each, notes **to its builder**: one line on what to keep,
then at most three concrete changes, the biggest gain first, nothing about code. Then
`critique/scores.json` with each letter's scores, `total` (weighted mean), `best_shot`,
`why`, plus `ranking` and `notes`.
