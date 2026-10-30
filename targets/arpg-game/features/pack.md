# Task: a map feature, $skill<Something>

You are one of several designers, each independently making **one feature** for the maps of
a dark, gothic Roblox action RPG seen from a high camera (pitch 50, zoom 35) at night. A
feature is one structure of a map: a frozen fall, a heaved ridge, a drowned shrine, a field
of standing spears. It is made and judged on its own, alone on a pad of plain ground, and
later builders assemble maps from many features. Make one strong feature, render it, check
it, and stop. Your idea is in `.swarm/DIRECTION.md` (read it last).

## What is rewarded

fafwa, who owns the game: "reward novel features that create their own ideas, e.g.
environmental effects, particles, interesting geometry, or details in general." A critic who
sees **only your renders** judges, in this order:

1. **Its own idea** (most weight): something this game hasn't got. A feature that brings
   its own **effect** (a new set piece: drifting particles, a glow that breathes, sparks, a
   stream of motes), its own **geometry** (heights, lifted cells, new sculpts with a shape
   nobody has made), and **details** that reward a close look scores high. A plain shape of
   ground with the area's existing props scores low.
2. **Its photograph**: the best of your cameras, as a photo. A subject, a foreground, depth,
   scale (the red 5-stud post is a person). A camera inside a wall or staring at a slab
   wastes it.
3. **It reads from the game camera**: from high above at pitch 50, the idea is still clear.
4. **Seeds**: three seeds give three versions of the same idea, not one shape repeated.
5. **Usable in a map**: the road runs through it, there's ground to fight on, nothing broken.

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
2. **One feature module,** `src/shared/systems/features/$skill<Something>.luau`, returning one
   `MapFeature.Feature` whose `name` is its file name and its key, `palette = "$skill"`.
   It starts with `--!strict`, requires only `../DraftedMap`, `../MapFeature`, `../Grid`,
   `../Noise` and `../DistanceField`, and touches no game API.
3. **Register it** in `MapFeatures.luau`: one `local <Name> = require("../systems/features/<Name>")`
   line and one `<Name> = <Name>,` line in the table, under its comment. Nothing else changes.
4. **Seeded and pure.** Every random number comes from the `rng` you are given, only through
   `rng:NextNumber()` or `rng:NextNumber(lo, hi)` (no `NextInteger`: the offline stand-in
   lacks it). No `Random.new`, no `math.random`.
5. **New sculpts** (geometry, detail) are rows at the **end** of the `Sculpts` table, each
   named `${skill_lower}_<something>`, an **existing kind** (the sculpt types below), colours
   inline, with a catalog row `["sculpt:<name>"] = row("<one sentence>", MOOR),` in
   `catalog/World.luau`. Use them in your feature as landmarks (`marks`) or a cell kind's
   `props`.
6. **New set pieces** (effects, particles) are rows at the **end** of `SetPieces.luau`'s
   `recipes`, each named `${skill_lower}_<something>`, with an **existing theme** (`rimeholt`
   suits this area; any listed theme is allowed). Place them with your footprint's `effects`.
   Write motions inline in the row; a new `local` outside the tables fails the check.
7. **Inside the bible.** Your own ground colours are surfaces: saturation at most 0.50 and
   value at most 0.40. Light and effects may be bright. Terrain keeps one colour per
   material (`draftProblems` names the free ones).
8. **Don't read files outside this pack** unless a command fails and names one. No web.
9. **Stop after at most three revisions** of your first working feature.

## The brief

$brief

## What you can and can't show offline

- `dresspreview shots ... feature=<Name>` draws your feature on its pad from your own
  cameras, plus one in along the road. **This is your photograph.**
- `dresspreview whole ... feature=<Name>` draws the pad from three-quarters, eye level and
  straight above.
- `sculptpreview` draws your new sculpts beside the red 5-stud post; `setpiecepreview` your
  set piece from the game camera at two moments and from above, particles included.
- Lights draw as small glowing cubes; there is no real lighting or mist offline. Don't spend
  revisions on light colour on surfaces.

## The contract

$contract

## What your own cells can do

$drafted

## The worked example

$example

## Sculpts and set pieces

$sculpt_types

$setpiece_types

$setpieces

## The rules

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only `<YourLook>`
with your feature's name, `<Sculpts>` with your new sculpts (a comma list) and `<SetPiece>`
with your set piece's name. Skip the sculpt or set piece render if you made none.

Format first:

```
stylua src/shared/systems/features src/shared/data/MapFeatures.luau src/shared/data/Sculpts.luau src/shared/data/SetPieces.luau src/shared/data/catalog/World.luau
```

Check it (prints every rule it breaks, with numbers):

```
lune run .swarm/tools/explain MapFeatures
```

Render the reference once (the worked example):

```
$ref_cmds
```

Render yours (again after each revision, with a new `r<n>`):

```
$render_cmds
```

Then **look at every image** with your Read tool, `feature-shots` first. Ask what the critic
will ask: is it an idea of its own; would the best shot stop someone scrolling; does it
read from high above; do the seeds differ; can a road and a fight pass through it.

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "<your feature's name>",
  "rows_added": ["<every new sculpt and set piece row>"],
  "sculpts": ["<your new sculpts, or nothing>"],
  "setpiece": "<your set piece, or empty>",
  "variation": ["<axis: its options>", "..."],
  "intent": "<one sentence: the idea, and what makes it new>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0,
  "requests": ["<optional: what the feature wanted and couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
