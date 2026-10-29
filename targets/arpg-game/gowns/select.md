# Select: the $skill gown, run $run

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

1. **It reads as a gown from the ARPG camera.** Cover the details with your thumb: by
   outline and colour alone, is it a dress (a fitted waist, a full skirt falling to the
   shins, a headpiece), and apart from iron, leather, studded, linen and fenscale?
2. **Elegance and era:** finery of standing, in its era's spirit (gothic, rococo, baroque,
   medieval...), aged a little, in the game's muted night palette (the bible's caps; pale
   trims as bone or ivory, not white).
3. **The skirt holds together:** standing, the legs' panels read as one skirt from the
   front and from above, the thigh panels hand over to the shin panels without a gap, and
   nothing cuts through the body or floats; it still holds on the slim avatar (`fit`).
4. **Parts are spent well:** on the silhouette, not on detail no one sees from above.
5. **The files are fit to merge:** readable, comments that say why, parts built with Kit,
   colours that respect the bible.

Pick at most 3, fewer if fewer are worth it, and say so if none is. A gown with a strong
silhouette and fixable flaws beats a safe set that reads as a robe.

Write `selection.json` in this run's folder, exactly:

```json
{
  "picked": ["C", "F"],
  "reasons": {"C": "<one sentence>", "F": "<one sentence>"},
  "fixes": {"C": "<the main flaw to fix first, or none>"},
  "notes": "<anything the run taught about the pack or the directions, or empty>"
}
```

Then put the first pick on a branch with `python3 -m swarm apply runs/$run <letter>`. It
was made under a 100-part set budget (the run's base raised it from 64), so it needs that
budget raised in the game, or trimming, before it can merge; and a human decides which
bases wear it.
