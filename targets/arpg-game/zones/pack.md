# Task: design the $skill area's look

You are one of several designers, each independently making the whole look of the same new
area of the game: its ground, rims, props, mist and lights (an outdoor tileset), the props
it needs (sculpts), and its signature environmental effect (a set piece). Make one strong
look, render it, check it, and stop. Everything you need is in this file and in
`.swarm/DIRECTION.md` (read that last: it's your starting stance).

This is a dark, gothic Roblox action RPG: always night, a faint silver-blue moon, warm
amber lamps, low mist. Players see the world from a high camera (pitch 50, zoom 35), where
an area reads by **colour, mass and landmarks** before any detail. Areas are generated:
a tileset dresses whatever layout the map draws, so a look must work over many seeds.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **One tileset file,** `src/shared/data/outdoorTilesets/$skill.luau`, returning one
   `OutdoorTypes.OutdoorTileset` whose `name` is `"$skill_lower"`. Derive it from `./Field`
   (or `./Moor`) the way the Ashfields' `Field2` derives from Field: clone, then change. Its
   `lighting` names an **existing** preset (`mood`, `field` or `ashfields`); a new preset
   isn't part of this job.
3. **Register it** in `OutdoorTilesets.luau`: exactly `local $skill = require("./outdoorTilesets/$skill")`
   and `$skill_lower = $skill,` in the table. Nothing else in that file changes.
4. **New sculpts are rows in the `Sculpts` table** (the big table literal at the top of
   `Sculpts.luau`), each named `${skill_lower}_<something>`, using an **existing kind**
   (the `Kind` list in the sculpt types below). A new kind would be code, which this job
   can't write. Put colours inline in the row: a new `local` outside the rows is a change
   outside your rows and fails the check.
5. **One theme** in `EnvThemes.luau` named `$skill_lower` (or starting with it), and **one
   or two set pieces** in `SetPieces.luau`'s `recipes`, each named `${skill_lower}_<something>`.
   A theme's `kit` may only name textures **already in `EnvThemes.luau`** (copy their
   `rbxassetid://` lines): there's no way to upload a new one.
   **Add every new row at the end of its table**, just before the table's closing `}`: a row
   slipped in between another row and the comment above it changes that row and fails.
   Write motions and swells inline in your rows: a new `local` outside the tables is a change
   outside your rows and fails the check.
6. **Catalog rows** in `catalog/World.luau` for each new sculpt (`["sculpt:<name>"]`) and the
   tileset (`["outdoor:$skill_lower"]`), with `row("<one sentence>", MOOR)` (the formatter
   may wrap a long one; that's fine). Set pieces and themes get theirs automatically from
   their `about`.
7. **Data only.** The tileset file starts with `--!strict`, requires only `./Field`, `./Moor`,
   `../LightingPresets`, `../../OutdoorTypes` and `../Sculpts`, and builds tables. Local
   helpers (like Field2's `with`) and colour tables of your own are fine there.
8. **Don't read files outside this pack** unless a command fails and its error names one.
   Don't browse the web. Don't explore the repo.
9. **Stop after at most two revisions** of your first working look.

## The brief

$brief

## What you can and can't show offline

- `dresspreview <kind> ... tileset=$skill_lower` dresses the moor's generated layouts in
  your tileset: ground, rims, props, ruins, lights (as small glowing dots). `whole` frames
  the whole map from above; `pool` and `ruin` frame a site from three-quarters, eye level
  and above. This is the main judge of your area.
- `tilesetpreview $skill_lower` shows every piece of your tileset one by one.
- `sculptpreview` shows your new props over three seeds, beside a red post 5 studs tall
  (a character's height).
- `setpiecepreview` shows your set piece from the game camera at two moments and from above.
- **Not shown offline:** mist, mana motes, light colour on surfaces and the lighting preset.
  Set them sensibly by the bible; a Studio check judges them later. Don't spend revisions
  on them.

## How a tileset is built

$types

The Ashfields' tileset, the worked example (derive yours the same way):

$example_tileset

The registry:

$registry

## Props: sculpts

$sculpt_types

## The signature effect: a theme and a set piece

The set-piece guide (quoted with the rules below) explains paths, looks and motions. Two
things matter most here:

- **The game camera looks down and sees nothing above the horizon.** Keep the effect low
  and near the ground: a worm of light winding over the area, wisps rising from water, a
  slow coil above a ruin. The Ashfields' aurora curtains hang outside the camera; don't
  copy them.
- **Budget:** within its radius a phone draws at most 220 parts, 3 lights and 10 particle
  emitters of set pieces. Keep yours well inside that.

$setpiece_types

$themes

$setpieces

## The rules

These are the art direction's rules and the guides, quoted whole. Every finding against
your area will cite one of them. Read the bible's colour caps, its landmark rules (B11)
and "one muted accent hue per zone" closely.

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only
`<Tileset>` with `$skill_lower`, `<Sculpts>` with your sculpts comma-separated, and
`<SetPiece>` with your main set piece's name.

Format first (the format check fails on unformatted files):

```
stylua src/shared/data/outdoorTilesets src/shared/data/OutdoorTilesets.luau src/shared/data/Sculpts.luau src/shared/data/EnvThemes.luau src/shared/data/SetPieces.luau src/shared/data/catalog/World.luau
```

Render the reference once, the Ashfields in the same views:

```
$ref_cmds
```

Render your area (again after each revision, with a new `r<n>` in the names):

```
$render_cmds
```

Then **look at every image you rendered** with your Read tool, `zone-whole` first. Ask:

- From above, does it read as its own place, apart from the Ashfields (grey ash, violet)?
- Is there a landmark that pulls a player across it, and one muted accent hue?
- Do the props stand out from the grass (anything under about 3.5 studs vanishes)?
- Does the set piece read from the game camera?
- Does anything float, cut into the ground, or block the walk?

Check everything (a failure means the run is discarded). The lint fails on **warnings**
too: a local you declare and never use fails the run.

When a spec fails with only "expected tables to be deeply equal", run it through the helper,
which prints what the check found (for the tileset spec, every rule your tileset breaks):

```
lune run .swarm/tools/explain OutdoorTilesets
```

The most common one: Field's living grass and earth are brighter than a new area may be
(only the field itself is allowed them), so **repaint every ground colour** your tileset
inherits, the way Field2's `ashen` does: `ground`, every edge's `ground`, `outcrop`,
`bluff`, `pools.bed`, `beyond` and `landmarks`.

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
  "sculpts": ["<every new sculpt name>"],
  "setpiece": "<your main set piece's name>",
  "rows_added": ["<every new row name: sculpts, theme, set pieces>"],
  "intent": "<one sentence: what the area looks like and how it reads from the high camera>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0,
  "requests": ["<optional: a prop kind, material, texture or effect the area wanted but couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
