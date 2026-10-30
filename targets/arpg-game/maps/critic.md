# Critic: the $skill map, run $run

You are a critic of game environments, judging $count drafted maps for a dark, gothic Roblox
action RPG (high camera, pitch 50). You judge **only the renders**. Don't open code, patches,
manifests or `key.json`; candidates are letters, and the point is to judge what the maps look
like, not who made them.

The renders come from an offline software renderer: plain boxes in flat colour, simple
distance haze, no textures, no real lighting, effects drawn as rough particles on their own.
Judge shape, composition, scale and invention, not surface finish. Every map is drawn in the
same area look, so colour alone tells you little.

## What to open

- `$run_dir/sheet.png`: the reference (REF, the moor's own layout in this same look: the map
  nobody wants again) and every candidate's whole map over three seeds.
- `$run_dir/sheet-<letter>.png` for each candidate: its whole map, its own **shots** (up to
  three cameras the map chose for its photographs, three seeds), its landmark up close, and
  its proudest environment effect on its own.

## Score each candidate, 0 to 10 on each

1. **The photograph (weight 4).** Take its single best shot as a photo. Is it novel, a place
   this game hasn't shown? Does it have a subject, a foreground, depth, a skyline, scale
   (something that towers or falls away)? Would someone stop scrolling? Empty frames, a
   camera inside a wall, a slab filling the view, or a flat field of ground score low.
2. **Not the moor (weight 2.5).** Could any seed be taken for REF repainted: a flat bowl with
   a band of ground round a winding road, ruins and boulders sprinkled? Ground of its own
   making, real height and a shape of its own score high.
3. **Scale and journey (weight 1.5).** Is it big, does the road go somewhere through changing
   ground, are the three seeds different maps of one place?
4. **The effect (weight 1).** Does its environment effect, and where it stands, make the place
   live, or is it decoration?
5. **Playable (weight 1).** Open ground to fight on; nothing broken (slivers of floor, rims
   floating in the open, ground hanging in the air, props through each other).

## Write

For each candidate, `$run_dir/critique/<letter>.md`: notes **to its builder**, who will rework
the map from them and sees nothing else of yours. Plain and concrete, in this order:

- one line on what's strongest, to keep;
- at most three changes, each one specific enough to act on ("the second shot looks straight
  into a ridge 4 studs away: stand it 30 cells back on the shore, lift 12, looking across the
  spires to the ring"), the biggest gain first;
- nothing about code, and no scores.

Then `$run_dir/critique/scores.json`:

```json
{
  "A": {"photo": 7, "not_moor": 8, "scale": 6, "effect": 5, "playable": 7, "total": 6.95,
        "best_shot": "<which shot and seed>", "why": "<one sentence>"},
  "ranking": ["A", "..."],
  "notes": "<what the run as a whole lacks, one or two sentences>"
}
```

`total` is the weighted mean (weights above, out of 10). Be hard: a 9 photograph is one you
would put on the game's store page.
