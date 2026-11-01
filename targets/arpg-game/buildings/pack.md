# Task: a building tileset, $skill

You are one of several makers, each independently writing **one building tileset** for a
Roblox action RPG seen from a high camera (pitch 50, looking down) at night. The game builds
its houses, cottages, manors, towers and walled yards from a grid plan, ruins some of them,
and paints every piece (walls, door and window walls, corner posts, floors, roof slopes,
ridges, broken stumps) from a **tileset**: one data file giving each slot a built-in
material, a colour and optional **trim** (extra parts: beams, frames, shutters, buttresses,
rubble, moss, caps). Today the game has two (the town's timber homes and the moor's charcoal
stone), and every area builds in that stone. Yours gives one area its own buildings. Your
area and stance are in `.swarm/DIRECTION.md` (read it last).

## What is rewarded

A critic who sees **only your renders** judges, in this order:

1. **It belongs to this area** (most weight): at a glance the buildings say the brief's
   place and nothing else; nobody would mistake them for the moor's stone or the town's
   timber.
2. **Character in the trim:** structure worth a close look (framing, courses, posts that
   carry the walls, a roof edge, details at doors and windows), not flat boxes painted a
   new colour. Read the timber homes' trim and go further.
3. **It ruins well:** the broken stumps and cut posts look like this material broken
   (charred, crumbled, splintered, cracked), with heaps at the foot where it fits.
4. **It reads from the game camera:** walls, roofs and openings stay distinct from above
   at night; roofs a shade apart from walls; ridges read.
5. **Restraint:** Roblox-plain parts (art bible B10), a dark night palette, one muted
   accent; nothing busy or noisy.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **The tileset** is `src/shared/data/tilesets/$skill.luau`, with `name = "$skill_lower"`
   and `contractVersion = 2`, filling **every required slot** (`joist` too, a timber beam).
   It requires only `../../ConstructionTypes`.
3. **Built-in materials and parts only:** `material` is an Enum.Material name (the spec
   lists them); no `materialVariant`, `mesh`, `texture` or asset ids.
4. **Inside the colour limits** the spec enforces (large surfaces and trim; Neon is for
   light only, a few small parts at most).
5. **At most six trim parts on any one variant:** towns sit near the phone's part budget.
6. **Register it** in `Tilesets.luau` (a require line and `$skill_lower = $skill,`) and give
   it one catalog row in `catalog/World.luau`, beside the other `tileset:` rows:
   `["tileset:$skill_lower"] = row("<one sentence>", MOOR),`.
7. **Don't read files outside this pack** unless a command fails and names one. No web.
8. **Every render goes under `.swarm/out/`.** A stray file in the repo root discards the run.
9. **Stop after at most three revisions** of your first tileset that renders.

## The brief

$brief

## The examples

$timber

$stone

## The types, slots and grid

$types

$contract

$grid

## The check

$spec

$registry

## The rules

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only `<Tileset>`
with your key, `$skill_lower`.

Format first:

```
stylua src/shared/data/tilesets src/shared/data/Tilesets.luau src/shared/data/catalog/World.luau
```

Check it (prints every rule a spec breaks):

```
lune run .swarm/tools/explain BuildingTilesets
```

Render the references once (the town's timber whole, the moor's stone ruined):

```
$ref_cmds
```

Render yours (again after each revision, with a new `r<n>`):

```
$render_cmds
```

Then **look at every image** with your Read tool, beside the references. The renders are
flat-shaded boxes: colour and shape show, materials don't, so the shapes of your trim must
carry the character. Ask what the critic will ask: is it this area; is there structure
worth a close look; do the ruins look like this material broken; does it read from above.

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "$skill_lower",
  "tileset": "$skill_lower",
  "rows_added": ["tileset:$skill_lower"],
  "intent": "<one sentence: the buildings, their materials and their trim>",
  "renders": ["<the paths of your final renders, the references excluded>"],
  "revisions": 0,
  "requests": ["<optional: what the tileset wanted and couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
