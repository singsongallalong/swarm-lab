# Task: invent a new kind of area look for $skill

You are one of several designers, each independently inventing a **new way of drawing**
for the same skill. Not a new row for an existing kind: a new kind, written as one small
pure Luau module that places and poses primitive parts over time. The game and its
offline preview both draw any such module the same way, so if yours is good, it can go
into the game as it is.

Everything you need is in this file and `.swarm/DIRECTION.md` (read that last: it's
your starting stance). This is a dark, gothic Roblox action RPG: always night, a faint
silver-blue moon, warm amber lamps, low mist. Colour and glow are reserved for gameplay.
Players see it from a high camera (pitch 50, zoom 35).

## Why this job exists

Looks made only from the existing kinds keep converging on the same few ideas (rings of
spikes, heaving rocks). Your kind must **draw something none of the existing kinds can**:
curves and arcs, spirals, forking or branching growth, sweeping blades, orbiting pieces,
lattices, tendrils, shattering panes, rising columns, a shape that travels and turns...
The existing kinds are listed below so you know what not to rebuild.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **Your module is pure** (it runs in the game's shared code and in tests): no `game`,
   `workspace`, `script`, `Instance`, `Enum`, `task`, `wait`, `spawn`, `delay`,
   coroutines, `os`, `debug`, `_G`, `shared`, `loadstring`, no `while true` or `repeat`
   loops. Only these requires, exactly as written: `require("../AreaLayout")`,
   `require("../SculptMath")`, `require("../../DraftedTypes")`, `require("../../SkillTypes")`,
   `require("../../SculptTypes")`. It starts with `--!strict` and stays under 300 lines.
3. **Keep the contract** (quoted below). Above all: `pose` returns exactly `count(look)`
   pieces, the same shapes in the same order at every age and every power; randomness only
   in `plan`; every piece invisible (`transparency = 1`) at `lasts` and after.
4. **Name everything for $skill:** the module file `src/shared/systems/drafted/${skill}<Name>.luau`,
   its registry key `${skill}<Name>`, its row `${skill}<Something>` in `DrawnEffects.area`,
   any particle rows `${skill}<Something>` in `Emitters`.
5. **Budget:** at most 60 parts (the cast budget, PerfBudget); aim for 15 to 40. `pose`
   runs 30 times a second for every cast on screen, so keep it cheap: no deep loops, build
   only the pieces you return.
6. **Don't read files outside this pack** unless a command fails and its error names one.
   Don't browse the web. Don't explore the repo.
7. **Stop after at most two revisions** of your first working attempt.

## The brief

$brief

The look it replaces: `$current_look`. Colour to start from (0-255 RGB): $color. You may
tune it in $skill's `SkillVisuals` row. Your module receives the skill's colour in `pose`.

$current_rows

## What to write, step by step

1. **Decide the idea in one sentence** before writing code: what it looks like, how it
   moves, how it grows with power. Check it isn't something an existing kind already draws.
2. **Write the module** `src/shared/systems/drafted/${skill}<Name>.luau`, modelled on the
   reference kind below: `about`, `count`, `lasts`, `plan`, `pose`, and `bursts` if it fires
   particles. Its numbers come from its row (`look.<field>`), so they can be tuned without
   touching code, and `perPower` can grow them.
3. **Register it**: add one line to `DraftedKinds.luau`, like the reference's.
4. **Add its row** in `DrawnEffects.luau`, inside `local area: { [string]: AreaLook } = {`,
   with `kind = "Drafted"`, `layout = "${skill}<Name>"`, an `about`, its numbers and a
   `perPower`. Not `spare`: it's used.
5. **Point the skill at it**: set `areaLook` in $skill's `SkillVisuals` row to your row's name.
6. **Format, render, look, test** (commands below). Fix what fails. Judge what you see.
7. **Write the manifest**, then stop.

## The contract

$contract

## The reference kind

Read it closely: it shows the plan/pose split, how pieces fade in and out, the frame
(`{ r, y, -f }`), leaning a piece with `SculptMath`, a flash, and particle bursts.

$example_module

$example_row

$registry

## Building blocks

$shapes

$sculptmath

$arealayout

## The existing kinds (don't rebuild these)

$kinds

## Particles

Your kind fires particles through its row's `emitter` and its module's `bursts` (where and
when, at what scale). Everything below applies.

$particles

## The rules

These are the art direction's rules, quoted whole. Every finding against your look will
cite one of them.

$rules

## The spec your kind must pass

$spec

## Commands

Run every command from the worktree root, exactly as written, replacing only
`<YourLook>` with your row's name.

Format your module first (the format check fails on unformatted code):

```
stylua src/shared/systems/drafted
```

Render the reference once:

```
$ref_cmds
```

Render your look (again after each revision, with a new `r<n>` in the name):

```
$render_cmds
```

Then **look at every image you rendered** with your Read tool, game-camera view first.
Compare power 0, 4 and 8, and against the references. Ask: is it something new, not a
ring of spikes again? Does it have volume (SE6)? Its own hue (SE7)? Does power show (SE3)?
Is anything big near the camera (SE10)? The preview's last line gives parts and particles.

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

A failing `DraftedKinds` spec names the piece, the age and the power that broke the
contract: fix exactly that.

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "<your row's name>",
  "layout": "<your module's registry name>",
  "idea": "<one sentence: the new thing your kind draws that no existing kind can>",
  "rows_added": ["<every new row name, in any file>"],
  "intent": "<one sentence: what it looks like and how it grows with power>",
  "renders": ["<the paths of your final renders, the references excluded>"],
  "revisions": 0,
  "requests": ["<optional: something the look wanted but couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
