# Task: a kit piece for the $skill

You are one of several makers, each independently building **one piece of an area's kit**
for a Roblox action RPG seen from a high camera (pitch 50). A kit piece is a prop or a
landmark (a column, a statue, a gate, a brazier) made as a **sculpt**: a recipe of Roblox
parts that the game builds, varied by a seed. A builder will place your piece many times in
a generated dungeon. Make one strong piece, render it, check it, and stop. Your piece is in
`.swarm/DIRECTION.md` (read it last).

## What is rewarded

A critic who sees **only your renders** judges, in this order:

1. **It is the piece and it belongs to this place** (most weight): what the direction asks
   for, recognisable at a glance, in the area's look (below).
2. **Shape and detail:** a strong silhouette, with height, depth and detail worth a close
   look. One plain block scores low, however neat.
3. **It reads from the game camera:** from high above, it is still clearly what it is.
4. **Seeds:** the three seeds give three versions of the same piece (whole and broken,
   taller and shorter), not one shape repeated.
5. **Its effect,** if it has one: a set piece that makes the piece glow, burn or drift.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **Sculpts** are rows at the **end** of the `Sculpts` table, each named
   `${skill_lower}_<something>`, an **existing kind** (the sculpt types below), colours
   inline, each with a catalog row `["sculpt:<name>"] = row("<one sentence>", MOOR),` in
   `catalog/World.luau`. One to three rows.
3. **A set piece** (optional) is a row at the **end** of `SetPieces.luau`'s `recipes`,
   named `${skill_lower}_<something>`, with theme `domain`. Write motions inline in the row;
   a new `local` outside the tables fails the check.
4. **Inside the area's colour limits** (the brief). The `Sculpt` spec checks them.
5. **Don't read files outside this pack** unless a command fails and names one. No web.
6. **Stop after at most three revisions** of your first piece that renders.

## The brief

$brief

## Sculpts

$sculpt_types

$colossus

## Set pieces

$setpiece_types

$themes

$setpieces

## The rules

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only `<Sculpts>`
with your sculpt rows (a comma list, no spaces) and `<SetPiece>` with your set piece's name.
Skip the set piece render if you made none.

Format first:

```
stylua src/shared/data/Sculpts.luau src/shared/data/SetPieces.luau src/shared/data/catalog/World.luau
```

Check it (prints every rule a spec breaks, with numbers):

```
lune run .swarm/tools/explain Sculpt
```

Render the reference once (an existing colossus, a different place's look):

```
$ref_cmds
```

Render yours (again after each revision, with a new `r<n>`):

```
$render_cmds
```

Then **look at every image** with your Read tool. Ask what the critic will ask: is it the
piece; is it this place (ivory, gold, holy light, monumental); does it read from high
above; do the seeds differ; does the effect make it.

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "<your main sculpt's name>",
  "rows_added": ["<every new sculpt and set piece row>"],
  "sculpts": ["<your sculpt rows>"],
  "setpiece": "<your set piece, or empty>",
  "intent": "<one sentence: the piece, and how seeds vary it>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0,
  "requests": ["<optional: what the piece wanted and couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
