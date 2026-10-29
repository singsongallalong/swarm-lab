# Task: a new $family look for $skill

You are one of several designers each making a look for the same skill, independently.
Make one strong look, render it, check it, and stop. Everything you need is in this
file and in `.swarm/DIRECTION.md` (read that last: it's your starting stance).

This is a dark, gothic Roblox action RPG: always night, a faint silver-blue moon, warm
amber lamps, low mist. Colour and glow are reserved for gameplay. Players see it from a
high camera (pitch 50, zoom 35).

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these files, only as described:**
$files_section
2. **Data only.** No new kinds, no changes to code, specs, scripts or docs. If the kind
   you want doesn't exist, make the best look you can with the kinds below.
3. **New rows start with `$skill`** (for example `${skill}Frost`). Never change an
   existing row other than `$skill`'s own `SkillVisuals` row. Every new row needs an
   `about` (one plain sentence: what it looks like) and must not be marked `spare`.
4. **Keep the part count flat as power grows** (SE3): grow sizes, reach, brightness,
   never counts. Use `perPower` for growth.
5. **Don't read files outside this pack** unless a command below fails and its error
   names one. Don't browse the web. Don't explore the repo.
6. **Stop after at most two revisions** of your first attempt.

## The brief

$brief

The look it replaces: `$current_look` (shown under "Current rows").
Colour to start from (0–255 RGB): $color. You may tune it in `$skill`'s SkillVisuals row.

## Current rows

$current_rows

## Examples of good rows

Ground Slam is the benchmark (SE2): its look and feel are the yardstick.

$examples

## The $family kinds you can use

$kinds

## The rules

These are the art direction's rules, quoted whole. Every finding against your look will
cite one of them.

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only
`<YourLook>` with the name of your new row.

Render the reference once:

```
$ref_cmds
```

Render your look (again after each revision, with a new `r<n>` in the name):

```
$render_cmds
```

Then **look at every image you rendered** with your Read tool. Judge the game-camera
view first. Compare power 0, 4 and 8, and compare against the reference. Ask: does it
have volume (SE6)? Is it in its own hue (SE7)? Does it read apart from telegraph red,
status tints and loot (SE8)? Is anything big near the camera (SE10)?

Check the specs (a failing spec means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "<YourLook>",
  "rows_added": ["<every new row name, in any file>"],
  "intent": "<one sentence: what it looks like and how it grows with power>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0
}
```

No report, no summary in chat. The manifest is the only thing read.
