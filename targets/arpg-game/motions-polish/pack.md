# Task: a cast motion, $skill

You are one of several animators, each independently polishing **one cast motion** for a dark,
gothic Roblox action RPG seen from a high camera. Characters are animated in code: a motion
is a few **key poses** on a timeline, and the rig plays them through muscles and gravity.
You don't write joint angles. A pose places **end effectors**: where the weapon's grip sits
from the right shoulder, which way the weapon's head points, how the chest twists and leans,
how far the hips drop. The rig solves the arms and legs. Key the motion, render it, read the
renders, revise, and stop. Your approach is in `.swarm/DIRECTION.md` (read it last).

## What is rewarded

A critic who sees **only your renders** judges, in this order:

1. **It reads as the brief** (most weight): every moment the brief describes is there, in
   order, recognisable in the stills.
2. **Weight and snap:** a gathered wind-up, a fast blow, an impact that lands with the body
   behind it, a settle. Not a smooth even wave.
3. **A clean body:** no arm through the chest or head, no haft through the head or thigh, no
   wrist flipping, feet planted, nothing bent past what a body does.
4. **The arc:** the weapon's head travels a clean path (over the top for an overhead), not
   through the body.
5. **The recovery:** it settles and hands back without a pop.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **Change only the row `CastDrafts.$skill`,** which is already in the file (the blocked
   motion). Its `plays`, `castTime`, `layer` and name stay; poses, keys, times, holds and
   kicks are yours to change as the brief says. No other row, local or line changes.
3. **The file is 60 KB: never read it whole.** Everything you need from it is quoted below.
   To see your row, `grep -n "CastDrafts.$skill" src/shared/data/CastDrafts.luau` and read
   that range.
4. **Don't read files outside this pack** unless a command fails and names one. No web.
5. **Stop after at most four revisions** of your first motion that plays.

## The brief

$brief

## Poses and the timeline

$vocab

$heavy

## Examples

$example

$example2

## The rules

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only `<YourLook>`
with `$skill`.

Format first:

```
stylua src/shared/data/CastDrafts.luau
```

Render the reference once: Ground Slam's one-handed swing, one of the game's best motions
(a different, faster move than yours; look at its weight and how clean the body stays):

```
$ref_cmds
```

Render yours (again after each revision, with a new `r<n>`):

```
$render_cmds
```

Each render is a grid: columns are moments (the label gives the time; the red bar marks the
blow), rows are views (side, front, three-quarter, and the game's own camera). The second
render is the blow up close. **The command also prints the lab's rule pass**: lines with `!`
are faults (an arm through the body, the wrist snapping, the haft through the head, the head
bouncing after the hit). Read them every time and fix what they name; the `~` lines are
readouts, not faults.

Then **look at both images** with your Read tool. Ask what the critic will ask: can I see each
moment of the brief; is the blow fast and heavy; does anything pass through the body; does
the head travel over the top.

Check everything (a failure means the run is discarded):

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "$skill",
  "rows_added": ["$skill"],
  "intent": "<one sentence: how your motion reads>",
  "faults": "<the lab's ! lines on your last render, or none>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0
}
```

No report, no summary in chat. The manifest is the only thing read.
