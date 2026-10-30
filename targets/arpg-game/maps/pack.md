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

## Seeds: different places, not one place jittered

The game draws a fresh map from a new seed every run, so a generator is judged on how
**different its seeds are**, in this order (fafwa, 2026-10-30):

1. **Topology, most of all:** different layouts, different paths through, branching ways,
   a different number and arrangement of obstructions. One wreck, then three; a straight
   wall, then a bend; a single crossing, then two.
2. **Look:** each seed reads as visually distinct: different cell kinds take the space,
   different heights.

How to get it: **let your first random draws choose the structure** (which arrangement,
how many of the big things, where they sit, how big the whole is), and only later draws
dress it. Before you write code, write `variation` in your manifest: three to five
structural axes your seeds vary along, each with its options ("shape: straight / bend /
twin", "outcrops: 0-3"). The worked example's header does this.

**It is measured.** The spec computes, over six seeds, a topology spread (how much of the
coarse layout and its counts differ, 0 to 1) and a look spread, and fails under 0.3
topology, under 0.12 between the two most alike seeds, or under 0.05 look; `explain`
prints the numbers and names the two seeds most alike. The `seedsheet` render shows twelve
seeds from above, four to a row: look at it first, every revision.

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
8. **Stop after at most three revisions** of your first working map.

## The brief

$brief

## What you're free to do (and what's judged)

The first frozen-lake run made six sound maps that were all **small, flat moor bowls with
no effect**: fafwa called them "a little boring". This run is loosened on purpose. A critic
who sees **only your renders** will judge you, and the most weight goes to **one striking,
novel photograph from inside your map** (your `shots`). Second: that no seed could be taken
for the moor. Then scale and journey, the environmental effect, and playability.

You may:

- **Make your own kinds of ground** (`draft.cells` and `draft.paint`, in the contract): a
  surface of your own material and colour, lifted off the ground or not, the tileset's
  props kept off it (`clear`), and your own scatter of sculpts. Paint them on walkable cells
  (an ice sheet, lifted at most 1 stud) or on wall cells (black open water sunk in the ice,
  pressure ridges of heaved ice 6-20 studs tall, a frozen waterfall, a forest of spires up
  to 60 studs). Roblox colours a terrain material once for the whole map, so a cell kind
  uses a material the tileset doesn't, or the tileset's own colour for it;
  `draftProblems` names the free ones.
- **Use height.** `heights` is studs per cell. Walkable neighbours may differ by at most 2
  studs (a ramp is a run of 2-stud steps); a bigger step needs a `bluff` cell (a wall) on its
  high side, and the dressing draws the cliff or retaining wall. Shelves, sunken basins,
  a road that climbs: all fine. `terraces = {}` can stay empty.
- **Go big.** Up to 240 x 200 cells (the moor is 96 x 96). Aim for a map that takes a
  while to cross, inside the phone budget the spec checks.
- **Place effects** (`draft.effects`): up to 8 environment set pieces from SetPieces, at
  fractional cells and a lift. Existing ones that suit this area: `rimeholt_underice` (a
  cold glow breathing under the ice, frost motes), `rimeholt_drift` (snow streaming low on
  the wind), `aurora_curtain` and `aurora_arc` (aurora in the sky), `barrow_wisps` and
  `barrow_pall` (ghost-lights and pall over barrows). Name the one you're proudest of as
  `setpiece` in the manifest: it is rendered on its own for the critic.
- **Choose your own photographs** (`draft.shots`): up to three cameras, `from` and `to` in
  fractional cells with a `lift` in studs over the ground there, and an optional `fov`.
  Compose them like a photographer: a subject, a foreground, depth, a skyline. Stand low on
  the ice looking up at what towers, or on a ridge looking down a frozen fall. A shot
  inside a wall or staring at a slab is wasted.

The boundary stays as the moor's and the fen's: an outer ring of wall, with `rim` cells
lining the walkable ground and an edge kind each (`drop` falls away into mist, `cliff`,
`thicket`, `ruin_wall`). It works well in the game; vary which edges you use, not the rule.

## What a sound map is

`DraftedMap.problems(map)` and `DraftedMap.draftProblems(draft, map, rng, tileset)` (in the
contract below) list every way a map breaks what the dressing and the game assume, and the
spec runs them on six seeds. In short:

- At most 240 x 200 cells, a cell 4 studs. `grid.cells`, `kinds` and `heights` each have
  width x depth entries.
- The outermost ring of cells is wall. At least 1,500 cells are walkable.
- A cell is floor exactly when its kind is `heath` or `road`. Walls are `void` (off the
  map), `outcrop` (rock inside it), `rim` (the edge, lining walkable ground) or `bluff`
  (the high side of a step).
- All the walkable ground is **one region** (`Grid.keepLargestRegion` helps), and start
  and exit stand on road cells, joined by walkable ground. Walkable neighbours at most 2
  studs apart.
- Every `rim` cell, and only those, has an edge kind in `edges`, and touches a floor cell.
- `road` is the centreline from start to exit, in fractional cells, at least two points.
- Sites (`ruin` or `graveyard`) are rectangles of even width and depth, wholly on floor,
  not overlapping. The dressing builds a ruin or a fenced graveyard on each.
- Cell kinds, effects and shots name things that exist and stay on the grid.

A landmark is `{ sculpt, x, z, yaw?, scale?, sink? }` in fractional cells. It stands on the
ground there and the dressing keeps its smaller props clear of it.

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

Then **look at every image you rendered** with your Read tool, `map-shots` first. The
renders are plain boxes in flat colour (no textures, simple haze), so judge shape,
composition and scale, not surface. Ask:

- Would one of your shots stop someone scrolling? Is it a place nobody has seen in this
  game: a subject, a foreground, depth, the effect or the strange ground in frame?
- From above, does each seed have a shape of its own that says what the brief's place is,
  nothing like the moor's band? Is it big, with height, more than one kind of ground?
- Are the three seeds different maps, yet clearly the same place?
- Is there room to fight in (open ground), and does anything look broken: slivers of
  floor, rims floating in the open, a shot inside a wall?

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
  "setpiece": "<the effect you're proudest of, a SetPieces name you place>",
  "variation": ["<axis: its options>", "..."],
  "intent": "<one sentence: the map's shape and how it reads from above>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0,
  "requests": ["<optional: a cell kind, site kind, prop or tool the map wanted but couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
