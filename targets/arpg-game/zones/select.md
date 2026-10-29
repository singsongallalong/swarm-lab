# Select: the $skill area, run $run

You are choosing which of $count area looks go forward. Each generator made a whole look
(a tileset, its props, a theme and a set piece) from the same pack, and all passed the
automatic checks: the tileset, sculpt, set-piece, catalog and completeness specs, purity,
lint and format. The pack, with the brief and the rules, is `$pack`. Read its "The brief"
and "The rules" sections first.

Candidates are labelled by letter only. **Don't open `key.json`**: it says which model
made which look, and the point is to judge the looks, not the models.

Open `sheet.png` (in this run's folder) first: the Ashfields as the reference, then each
candidate's whole map from above. Then `sheet-<letter>.png` for each candidate's site
views, tileset pieces, props and set piece, and its files in its patch.

$candidates

Judge, in order:

1. **It reads as its own place from above.** In the `whole` view, by colour and mass
   alone, it matches the brief's palette and one accent hue, clearly apart from the
   Ashfields' grey ash and violet, and from the moor and field.
2. **The landmark pulls.** The brief's landmark, seen from the high camera, is something a
   player would walk toward (bible B11).
3. **The signature effect reads** from the game camera in `zone-setpiece`, stays low, and
   fits the brief.
4. **The props are worth their parts:** big enough to read past the grass (about
   3.5 studs and up beside the 5-stud post), varied over seeds, and none floating or cut
   into the ground in the site views.
5. **The files are fit to merge:** a tileset derived cleanly from Field or Moor, comments
   that say why, colours inside the bible's caps, existing textures only.

Pick at most 3, fewer if fewer are worth it, and say so if none is. A distinct place with
fixable flaws beats a safe recolour of the Ashfields.

Write `selection.json` in this run's folder, exactly:

```json
{
  "picked": ["C", "F"],
  "reasons": {"C": "<one sentence>", "F": "<one sentence>"},
  "fixes": {"C": "<the main flaw to fix first, or none>"},
  "notes": "<anything the run taught about the pack or the directions, or empty>"
}
```

Then put the first pick on a branch with `python3 -m swarm apply runs/$run <letter>`. It is a
look only: placing its set piece on a map, a lighting preset, and a field or map of its own
are later work a human plans (arpg-game docs/guides/adding-areas.md).
