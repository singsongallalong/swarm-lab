# Task: lay out the $skill map

You are one of several designers, each independently writing the layout of the same new
map: one pure, seeded Luau module that returns a whole outdoor map (walkable ground, road,
rims, sites) and the landmarks it places itself. The game's own dressing code then covers
it in the area's look. Make one strong map, render it, check it, and stop. Everything you
need is in this file and in `.swarm/DIRECTION.md` (read that last: it's your starting
stance).

This is a dark, gothic Roblox action RPG seen from a high camera (pitch 50, zoom 35). A map
is generated afresh for every run, so it is a generator, not a drawing: it must make a good
map from **every** seed, and a different one from each.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **One layout module,** `src/shared/systems/draftedmaps/$skill<Something>.luau`, returning one
   `DraftedMap.Draft` (the contract below) whose `name` is its file name and its key, whose
   `tileset` is `"$tileset"`, and whose `generate(rng)` returns a `Heath.Map`.
3. **Register it** in `DraftedMaps.luau`: one `local <Name> = require("../systems/draftedmaps/<Name>")`
   line and one `<Name> = <Name>,` line in the table, under its comment. Nothing else in that
   file changes: keep the comment.
4. **Your own generator.** Read Heath (quoted below) to learn what a map holds and how the
   moor's is made, but write your own: calling `Heath.generate` fails the check. You may
   use its types and `Heath.onFloor`, and Grid, Noise and DistanceField.
5. **Seeded and pure.** Every random number comes from the `rng` you are given, and only
   through `rng:NextNumber()` (0 to 1) or `rng:NextNumber(lo, hi)`: the offline previews
   and tests run on a stand-in with **no `NextInteger`**, so use
   `math.floor(rng:NextNumber(lo, hi + 1))` for a whole number. No `Random.new`, no
   `math.random`. The module starts with `--!strict`, requires only
   `../DraftedMap`, `../Heath`, `../Grid`, `../Noise`, `../DistanceField` and
   `../../TerrainTypes`, and touches no game API. Loops are fine; one that never ends fails
   the specs' time limit.
6. **Optional new props** go as rows at the **end** of the `Sculpts` table, each named
   `${skill_lower}_<something>` with an existing kind, colours inline, and a catalog row
   `["sculpt:<name>"] = row("<one sentence>", MOOR),` in `catalog/World.luau`. Most maps
   need none: the area's sculpts already exist (`${tileset}_...` in Sculpts).
7. **Don't read files outside this pack** unless a command fails and its error names one.
   Don't browse the web. Don't explore the repo.
8. **Stop after at most two revisions** of your first working map.

## The brief

$brief

## What a sound map is

`DraftedMap.problems(map)` (in the contract below) lists every way a map breaks what the
dressing and the game assume, and the spec runs it on six seeds. In short:

- The grid is at most 160 x 128 cells, a cell 4 studs (the moor's is 96 x 96 or 128 x 96).
  `grid.cells`, `kinds` and `heights` each have width x depth entries.
- The outermost ring of cells is wall. At least 1,500 cells are walkable.
- A cell is floor exactly when its kind is `heath` or `road`. Walls are `void` (off the
  map), `outcrop` (rock inside it), `rim` (the edge, lining walkable ground) or `bluff`.
- All the walkable ground is **one region** (`Grid.keepLargestRegion` helps), and start
  and exit stand on road cells, joined by walkable ground.
- Every `rim` cell, and only those, has an edge kind in `edges` (`drop`, `cliff`,
  `thicket`, `ruin_wall`), and touches a floor cell.
- `road` is the centreline from start to exit, in fractional cells, at least two points.
- Sites (`ruin` or `graveyard`; leave manor, house, tower and labyrinthGate alone) are
  rectangles of even width and depth, wholly on floor, not overlapping. The dressing builds
  a ruin or a fenced graveyard on each.
- `heights` all 0 and `terraces = {}` is a flat map, and fine. Raised ground isn't part of
  this job.

A landmark is `{ sculpt, x, z, yaw?, scale?, sink? }` in fractional cells. It stands on the
ground there and the dressing keeps its smaller props clear of it. Put the brief's landmark on
open walkable ground where your road leads, scaled so it reads from above (a sculpt's size,
in studs at scale 1, is in its row in Sculpts; the brief names the ones to use).

## The contract

$contract

## The moor's layout, for reference

$heath

## The helpers

$grid

$noise

$distance

$terrain_types

## The rules

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only
`<YourLook>` with your draft's name.

Format first:

```
stylua src/shared/systems/draftedmaps src/shared/data/DraftedMaps.luau src/shared/data/Sculpts.luau src/shared/data/catalog/World.luau
```

Check your map is sound before you render it. This prints, for each seed, every rule
your map breaks, in plain words:

```
lune run .swarm/tools/explain DraftedMaps
```

Render the reference once: the moor's own layout in the same look, the map yours must
not merely repaint.

```
$ref_cmds
```

Render your map (again after each revision, with a new `r<n>` in the names):

```
$render_cmds
```

Then **look at every image you rendered** with your Read tool, `map-whole` first. Ask:

- From above, does each seed have a shape of its own that says what the brief's place is, apart
  from the moor's band?
- Does the road lead to the landmark, and does it read from above?
- Are the three seeds different maps, yet clearly the same place?
- Is there room to fight in (open ground), and does anything look broken: slivers of
  floor, rims floating in the open, sites crammed against walls?

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "<your draft's name>",
  "rows_added": ["<every new sculpt row, or nothing>"],
  "intent": "<one sentence: the map's shape and how it reads from above>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0,
  "requests": ["<optional: a cell kind, site kind, prop or tool the map wanted but couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
