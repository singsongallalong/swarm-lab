# Select: $skill's $family look, run $run

You are choosing which of $count candidate looks go on to the effect critic loop. Each
was made independently by a generator from the same context pack, which holds the
brief and the rules: `$pack`. Read its "The brief" and "The rules" sections first.

The candidates are labelled by letter only. **Don't open `key.json`**: it says which
model made which look, and the point is to judge the looks, not the models.

Open `sheet.png` (in this run's folder) first: every candidate's first render beside
the reference. Then open `sheet-<letter>.png` for any candidate worth a closer look.

$candidates

Judge the game-camera view first (pitch 50, zoom 35), then power 0 against 4 against 8,
then the side view. What matters, in order:

1. It reads as this skill, in its element, at the game camera (SE7, SE8).
2. Volume, not a flat sheet: layers, out-of-plane motion (SE6).
3. Power shows, with a flat part count (SE3).
4. Particles earn their place: you can see what they add at the game camera (haze, a
   column, an after-beat, matter where it lands), not specks or nothing; the pack's
   "Particles" section has the measured sizes. Each candidate's line above gives its
   parts and particles; `0 particles` means none fired. Don't count particles as a
   virtue on their own: a look without them can still win, but a look whose particles
   visibly carry part of it is worth more than the same look without.
5. It never hides the fight: nothing big near the camera, nothing covering the body,
   including particle clouds that swallow the red post (SE10).
6. Taste: would it sit beside Ground Slam's heave without looking cheaper (SE2)?

A candidate that is good except for one fixable flaw beats a safe dull one: the critic
loop fixes flaws, it can't add an idea. Pick at most 3, and fewer if fewer are worth it.
If none is worth taking forward, say so.

Write `selection.json` in this run's folder, exactly:

```json
{
  "picked": ["C", "F"],
  "reasons": {"C": "<one sentence>", "F": "<one sentence>"},
  "fixes": {"C": "<the main flaw the critic loop should fix first, or none>"},
  "notes": "<anything the run taught about the pack or the directions, or empty>"
}
```

Then put the first pick on a branch with `python3 -m swarm apply runs/$run <letter>` and
run the game's effect-critic-loop on it from there.
