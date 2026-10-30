# Select: the $skill map, run $run

You are choosing which of $count drafted maps go forward. Each generator wrote a whole
layout generator from the same pack, and all passed the automatic checks: every seed a sound
map (DraftedMap.problems), inside the phone budget, purity, the catalog, lint and format.
The pack, with the brief and the rules, is `$pack`. Read its "The brief" section first.

Candidates are labelled by letter only. **Don't open `key.json`**: it says which model made
which map, and the point is to judge the maps, not the models.

Open `sheet.png` (in this run's folder) first: the moor's own layout in the same look as the
reference, then each candidate's whole map over three seeds. Then `sheet-<letter>.png` for
its landmark up close, and its module in its patch.

$candidates

Judge, in order:

1. **A shape of its own.** From above, each seed says what the brief's place is, not the
   moor's band repainted.
2. **The landmark pulls.** The road leads to the brief's landmark, and it reads from above.
3. **Variety with identity.** Three seeds, three different maps, clearly the same place.
4. **Playable.** Open ground to fight on, no slivers or dead-end needles of floor, sites with
   room round them.
5. **The module is fit to merge:** readable, comments that say why, no magic left
   unexplained, no copy of Heath with numbers changed.

Pick at most 3, fewer if fewer are worth it, and say so if none is. A distinct map with
fixable flaws beats a safe one that reads as the moor.

Write `selection.json` in this run's folder, exactly:

```json
{
  "picked": ["C", "F"],
  "reasons": {"C": "<one sentence>", "F": "<one sentence>"},
  "fixes": {"C": "<the main flaw to fix first, or none>"},
  "notes": "<anything the run taught about the pack or the directions, or empty>"
}
```

A pick is a draft only: a builder, a place, seams and packs are later work a human plans
(arpg-game docs/guides/adding-areas.md).
