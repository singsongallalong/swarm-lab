# Select: the $skill armour set, run $run

You are choosing which of $count armour sets go forward. Each generator made a full set
(helm, chest, gloves, boots) from the same pack, and all passed the automatic checks: the
look specs, the part budget, purity, the catalog, lint and format. The pack, with the
brief and the rules, is `$pack`. Read its "The brief" and "The rules" sections first.

Candidates are labelled by letter only. **Don't open `key.json`**: it says which model
made which set, and the point is to judge the sets, not the models.

Open `sheet.png` (in this run's folder) first: every family's set as the reference, then
each candidate's set. Then `sheet-<letter>.png` for each candidate's close and slim-avatar
renders, and its files in its patch.

$candidates

Judge, in order:

1. **It reads as its own family from the ARPG camera.** Cover the details with your thumb:
   by colour and outline alone, is it a barbarian's, and is it apart from iron, leather,
   studded, linen and fenscale? A set that reads as "brown leather again" loses here.
2. **The fantasy:** half-armoured fury, hides and furs and trophies, worn and patched,
   in the same gothic, muted, night-lit world (the bible's colour caps).
3. **It sits on the body:** nothing floating, nothing cutting through a limb, no body
   showing through a gap, skirts hung from the thighs, and it still holds on the slim
   avatar (`fit`).
4. **Parts are spent well:** on the silhouette, not on detail no one sees from above.
5. **The files are fit to merge:** readable, comments that say why, parts built with Kit,
   colours that respect the bible.

Pick at most 3, fewer if fewer are worth it, and say so if none is. A set with a strong
family read and fixable flaws beats a safe set that reads as leather.

Write `selection.json` in this run's folder, exactly:

```json
{
  "picked": ["C", "F"],
  "reasons": {"C": "<one sentence>", "F": "<one sentence>"},
  "fixes": {"C": "<the main flaw to fix first, or none>"},
  "notes": "<anything the run taught about the pack or the directions, or empty>"
}
```

Then put the first pick on a branch with `python3 -m swarm apply runs/$run <letter>`. A
human then decides which bases wear it (a new base needs numbers and a bag picture).
