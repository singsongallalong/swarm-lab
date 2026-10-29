# Select: a new kind for $skill, run $run

You are choosing which of $count newly invented area kinds go forward. Each generator
wrote a pure Luau module that draws a new kind of look, and a row that uses it on the
skill. All passed the automatic checks: the contract spec, purity, lint, format and the
game's own specs. The pack they worked from, with the brief, the contract and the rules,
is `$pack`. Read its "The brief", "The contract" and "The rules" sections first.

Candidates are labelled by letter only. **Don't open `key.json`**: it says which model
made which, and the point is to judge the work, not the models.

Open `sheet.png` (in this run's folder) first: every candidate beside the references.
Then `sheet-<letter>.png` for a closer look, and each candidate's code in its patch.

$candidates

Judge, in order:

1. **Is it new?** It draws something no existing kind can (curves, spirals, branching,
   orbits, sweeps...). A disguised ring of spikes or a reskin of an existing kind loses
   here, however well made: novelty is why this lane exists.
2. **Does it read as this skill** at the game camera (pitch 50, zoom 35), in its element
   (SE7, SE8), with volume (SE6), power showing (SE3), never hiding the fight (SE10)?
3. **Is the code fit to go into the game?** Read the module:
   - `pose` is cheap: it runs 30 times a second for every cast on screen. No deep loops,
     no work for pieces it doesn't return, no rebuilding what `plan` could hold.
   - It's readable: clear names, comments that say why, numbers from the row (tunable
     without code changes) rather than magic constants.
   - Nothing the spec can't see: it uses the shape it's given (a cone looks like a cone),
     and the parts count is sensible (15 to 40 is the sweet spot; 60 is the ceiling).
4. **Taste:** would it sit beside Ground Slam's heave without looking cheaper (SE2)?

Pick at most 3, fewer if fewer are worth it, and say so if none is. A strong new idea
with fixable flaws beats a polished copy: the critic loop can fix flaws, not add ideas.

Write `selection.json` in this run's folder, exactly:

```json
{
  "picked": ["C", "F"],
  "reasons": {"C": "<one sentence>", "F": "<one sentence>"},
  "fixes": {"C": "<the main flaw to fix first: look or code, or none>"},
  "code_review": {"C": "<anything in the module that must change before it goes into the game, or fine>"},
  "notes": "<anything the run taught about the pack or the directions, or empty>"
}
```

Then put the first pick on a branch with `python3 -m swarm apply runs/$run <letter>`.
Until the game has merged the drafted-kinds platform, that branch also carries the
platform commit the run applied to its base.
