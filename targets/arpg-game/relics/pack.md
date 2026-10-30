# Task: relics, the pure core and the first three

You are one of several engineers, each independently building the same thing for a Roblox
action RPG written in strict Luau: **relics**, an endgame power layer, as a pure system
module and its first three content rows. The contract, its spec and the checks on the rows
are written already; your work must meet them exactly. Build it, check it, and stop. Your
stance is in `.swarm/DIRECTION.md` (read it last).

## The game's rules (from its CLAUDE.md)

- Luau, `--!strict` at the top of every file. Explicit types on every function's
  parameters and return values.
- `shared/systems` stays pure: no `game`, no Instances, no yielding. Data in, data out.
  Randomness only from the rng it is given (`rng:NextNumber()`; the offline stand-in has no
  `NextInteger`).
- All stats flow through the stat system: every effect is a modifier
  `{ stat, kind: "flat" | "increased" | "more", value, source }`.
- Content is data, logic is code: relic rows are data; nothing in the system names one.
- Small modules; comments say why, not what. PascalCase for modules and types, camelCase
  for functions and locals.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **`src/shared/systems/Relics.luau`** exports exactly the functions the contract lists,
   with those signatures and that behaviour. It requires only `../RelicTypes` and
   `../SkillTypes`.
3. **Three rows** in `data/Relics.luau`, `WardensSigil`, `GaleFeather` and
   `EmberHeart`, each as `rows.<Name> = { ... }` above the `return`. The brief describes each.
4. **Don't change the contract, the specs or any other file.** If the contract seems wrong,
   meet it anyway and say so in the manifest's `requests`.
5. **Don't read files outside this pack** unless a command fails and names one. No web.
6. Read the contract's every line before you write code: the specs you can see aren't all
   the tests that will be run.

## The brief

$brief

## The contract

$contract

## The spec your system must pass

$spec

## The checks on every row

$rows_spec

## Where the rows go

$data

## How rows are written in this game

$supports

## Stats, modifiers and conditions

$skill_types

## Commands

Run every command from the worktree root, exactly as written. Format first:

```
stylua src/shared/systems/Relics.luau src/shared/data/Relics.luau
```

Run the specs. `explain` prints each failing check's values:

```
lune run .swarm/tools/explain Relics
lune run .swarm/tools/explain RelicRows
```

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "Relics",
  "rows_added": ["WardensSigil", "GaleFeather", "EmberHeart"],
  "intent": "<one sentence: how you built it and how the three relics play>",
  "renders": [],
  "revisions": 0,
  "requests": ["<optional: anything in the contract that seemed wrong or missing, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
