# Clothing package: every worn set DeepSeek made (ready to port)

For the Claude Code thread porting these into arpg-game. Seventeen full sets from three
swarm-lab runs on 2026-10-29. Each set is four armour looks (head, body, hands, feet) with
their `ArmourLooks.luau` registry lines and `catalog/Gear.luau` rows. None is in the game yet.

## What's here

One folder per set, `<run>/<SetName>/`:

| File | What it is |
| --- | --- |
| `renamed.patch` | **Use this one.** The set with unique look names (`ReaverAntlerHelm`, not `ReaverHelm`), so several sets can live in the game together |
| `original.patch` | The worker's patch as it was made. Every set in a run shares the same four names, so only one per run would fit |
| `sheet.png` | The set's renders from its run: front, back, close and fit, plus the ARPG camera |
| `about.json` | The run, letter, look names (new and old), pick rank, the worker's intent, the picker's reason, the first fix, the part count |

Run evidence (critic notes, `selection.json`, `report.md`, the six-up renders) is in
`results/<run>/`.

## The sets

Part counts were measured with the game's own `ArmourLook.partCount` on main (2026-11-01).
The phone budget is **64 parts** for a full set (`PerfBudget.armour.parts`). "Pick" is the
picker's rank in its run; the rest were passed over, with reasons in `about.json`.

| Set | Run | Pick | Parts | In short |
| --- | --- | --- | --- | --- |
| ReaverAntler | reaver-armour (D) | 1 | 61 | pale bone antlers over broad smoke-cured hide, ash-fur shoulders, scavenged iron and bone |
| ReaverSkull | reaver-armour (A) | 2 | 59 | horned beast-skull helm, wolf-fur mantle, bone trophies |
| ReaverPauldron | reaver-armour (E) | 3 | 61 | asymmetric beast-skull pauldron, the other arm bare |
| ReaverJawmask | reaver-armour (B) | — | 59 | near-bare, wolf-fur pauldron, bone jaw mask with horns |
| ReaverWolfpelt | reaver-armour (C) | — | 63 | grey wolf pelt mantle and hood over hide wraps |
| ReaverScrap | reaver-armour (F) | — | 60 | scavenged iron plates lashed onto hide, one big pauldron |
| CourtlyHennin | courtly-gowns (E) | 1 | 99 | late-medieval: tall wimpled hennin, deep plum bell gown, fur band |
| CourtlyRococo | courtly-gowns (C) | 2 | 98 | rococo: faded rose and dove grey, black bows, tiered bell, tilted cap |
| CourtlyMourning | courtly-gowns (A) | 3 | 92 | Victorian mourning: veiled broad-brimmed hat, high neck, bustle |
| CourtlyBaroque | courtly-gowns (B) | — | 91 | baroque wine brocade; puffed shoulders read as pauldrons from above |
| CourtlyLolita | courtly-gowns (D) | — | 93 | gothic lolita (fafwa's reference); same shoulder problem |
| ClassicInverted | classic-gowns (D) | 1 | 72 | crimson gothic-lolita dress with black lace tiers; the only one that reads as lolita from the high camera |
| ClassicSolemn | classic-gowns (B) | 2 | 88 | ankle-length tiered A-line with a veil; best silhouette, nearly all black from above |
| ClassicClockwork | classic-gowns (F) | 3 | 100 | clock-face waist bow, brass key, studded lace band |
| ClassicFaithful | classic-gowns (A) | — | 97 | the fan art as drawn; black on black from above |
| ClassicCatalog | classic-gowns (C) | — | 55 | minimal catalogue version; black on black from above |
| ClassicStitched | classic-gowns (E) | — | 94 | stitched-doll patches, too small to read |

The **Classic** sets were made for the classic blocky body (the `feminine` figure and its
shoulder check). The **Courtly** sets were made for the standard body.

## Porting notes

1. **Apply:** from a swarm-lab clone, onto a branch from arpg-game main:
   ```
   python3 -m swarm shelf - --into <arpg-game worktree> --patches library/clothing/<run>/<Set>/renamed.patch ...
   stylua src tests
   ```
   This was tested on 2026-11-01 with all 17 sets at once onto main: they all apply, and
   `Catalog`, `ContentCompleteness` and `DressBudget` pass.
2. **The budget is the one red spec.** `ArmourLooks.spec`'s "keeps the heaviest full set
   inside the phone budget" adds up the heaviest look of each slot across all looks: 116
   parts with everything in. Options, fafwa's call:
   - **Reaver sets fit as sets** (59–63). Mixing the heaviest pieces of different Reaver
     sets can still pass 64, so check with the spec after choosing which to bring.
   - **The gowns don't fit** (72–100). Either raise `PerfBudget.armour.parts` for the
     wardrobe (it's a performance decision: see `docs/design/` on budgets and the DressBudget
     spec), or cut each gown by about a third before it merges. The runs' first fixes in
     `about.json` say where each would cut.
3. **They're looks only.** Nothing wears them until a base, an item or a wardrobe entry
   names them (`docs/guides/adding-items.md`, the wardrobe and dressing design). The original
   runs left that to fafwa.
4. **Studio:** each set wants a look on a real avatar in a lane. Bare arms show the preview
   dummy's blue offline. Check the classic sets on the classic body.
5. **Unrelated to clothing:** the patches were made on older mains (`41c9339`, `b229fe1`). The
   shelf command lays added lines after their context, so the age didn't matter in the test.
