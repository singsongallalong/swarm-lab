# Task: an area palette, $skill<Place>

You are one of several colourists, each independently making the palette of a different
future area for a dark, gothic Roblox action RPG seen from a high camera at night. A
palette is the colours a place is drawn from: its ground, rock, trim, its one accent and
its light. Areas don't exist yet: features, props and monsters will be made against your
palette later, so it must say *what place this is* in colour alone. Make one strong palette,
render it, check it, and stop. Your place is in `.swarm/DIRECTION.md` (read it last).

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **One palette module,** `src/shared/data/palettes/$skill<Place>.luau` (`<Place>` one or two
   words for your place, PascalCase), returning one `Palette.Palette` whose `name` is its file
   name and its key. It starts with `--!strict`, requires only `../../systems/Palette`, and
   says in a short comment at the top what the place is and why its colours are what they are.
3. **Register it** in `Palettes.luau`: one `local <Name> = require("./palettes/<Name>")` line
   and one `<Name> = <Name>,` line in the table, under its comment. Nothing else changes.
4. **`lighting` names an existing preset:** `mood` (the silver-blue night), `field` (warmer,
   lived-in night), `ashfields`, `barrows`, `shelf`, `wasteland`, `quarry`, `gorge`,
   `drownedParish`. Pick the one closest to your place's light.
5. **Inside the art bible's limits** (its section 2, quoted below): large ground at most
   saturation 0.20 and value 0.35 (0.35 saturation if `lived = true`, for living, inhabited
   ground only); trim at most 0.40 / 0.40; the accent at most 0.50 / 0.40; the bed and abyss
   dark. Terrain keeps **one colour per material**, so your seven grounds use different
   materials or share a colour. `Palette.problems` prints every break with the numbers.
6. **Don't read files outside this pack** unless a command fails and names one. No web.
7. **Stop after at most two revisions** of your first sound palette.

## The brief

$brief

## The contract

$contract

## The example

$example

## The rules

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only `<YourLook>`
with your palette's name. Format first:

```
stylua src/shared/data/palettes src/shared/data/Palettes.luau
```

Check it (prints the problems, with numbers):

```
lune run .swarm/tools/explain Palettes
```

Render the reference once (Rimeholt, the worked example):

```
$ref_cmds
```

Render yours (again after each revision, with a new `r<n>`):

```
$render_cmds
```

Then **look at every image** with your Read tool. The renders are flat boxes with haze; the
moor's own props keep their colours (a stand-in look), so judge the ground, rock, road and
mist. Ask:

- Does it read as *your* place, at night, and as none of the others (the moor's grey-brown
  heath, Rimeholt's blue-grey snow)?
- From the high camera, does the road read against the walkable ground, and the walkable
  ground against the rock and the far land?
- Is the accent one clear idea that things in the place will wear, and muted?
- Is it dark and matte, never washed out, never neon (saturation belongs to gameplay)?

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "<your palette's name>",
  "rows_added": [],
  "intent": "<one sentence: the place, and the colours that say it>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0,
  "requests": ["<optional: a lighting preset, material or role the palette wanted, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
