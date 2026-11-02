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

## Drowned Marches pilot (2026-11-01)

Eighteen more gown sets from the Drowned Marches wardrobe pilot (Rhodri, arpg-game R039), three
picks from each of six runs (two cloud sessions, three runs each), all on the `feminine` figure. Each run had two render-only
critic passes with one rework between them; run evidence is in `results/<run>/`. Same files
per set as above (`renamed.patch`, `original.patch`, `sheet.png`, `about.json`). Part counts
were measured with `ArmourLook.partCount` on arpg-game main `a2b439d`. All eighteen apply there
together (each also applies alone), and `Catalog`, `ContentCompleteness` and `DressBudget` pass.

| Set | Run | Zone | Pick | Parts | In short |
| --- | --- | --- | --- | --- | --- |
| WispbrideMourning | wispbride-marches (A) | Fen | 1 | 89 | pale mist bodice, flaring skirt, black hooded veil with wisp-blue prongs |
| WispbrideMoth | wispbride-marches (E) | Fen | 2 | 98 | the best A-line bell, pale from hip to mist hem, strand veil down the back |
| WispbrideKeeper | wispbride-marches (F) | Fen | 3 | 95 | mist skirt, willow-green laced bodice, a cold-blue hem that reads from above |
| ReedmailValkyrie | reedmail-marches (E) | Fen | 1 | 98 | ankle-length bell of reed-straw and green panels, bone V cuirass, winged reed circlet |
| ReedmailBark | reedmail-marches (D) | Fen | 2 | 88 | willow-bark lamellar battle skirt flaring band by band to a bone hem |
| ReedmailScale | reedmail-marches (A) | Fen | 3 | 92 | tiered fen-green eel-scale skirt edged in straw, fanned reed plume |
| MossveilFungal | mossveil-marches (D) | Fetid Forest | 1 | 85 | toadstool-cap bonnet, tiered skirt of lichen-yellow gill ruffles |
| MossveilFern | mossveil-marches (C) | Fetid Forest | 2 | 76 | the cleanest A-line: light moss front panel, stepped bone-and-lichen hem |
| MossveilOrchid | mossveil-marches (B) | Fetid Forest | 3 | 76 | flared moss bell under a black laced bodice, bone hem, orchid crown |
| RuinplateQueen | ruinplate-marches (F) | Fetid Forest | 1 | 80 | pale-stone tiered bell with bronze lips and moss bands, cinched waist, prong crown |
| RuinplateZiggurat | ruinplate-marches (C) | Fetid Forest | 2 | 89 | stepped skirt like a ruin's terraces; the most carved-from-the-ruins outline |
| RuinplateStatue | ruinplate-marches (D) | Fetid Forest | 3 | 96 | courtly statue knight: V-neck cuirass, hooped tassets corded in bronze, moss hem |
| TidewrackCorsair | tidewrack-marches (A) | Sunken Shelf | 1 | 92 | driftwood bodice over an ivory sailcloth A-line, shell-fan crest, teal only at the sash |
| TidewrackShell | tidewrack-marches (E) | Sunken Shelf | 2 | 86 | ivory bell skirt, dark stomacher at the waist, thin teal trims; best on the slim avatar |
| TidewrackSailcloth | tidewrack-marches (C) | Sunken Shelf | 3 | 88 | laced bodice and torn sailcloth drapes, all salt and ivory |
| FloodchoirNun | floodchoir-marches (B) | Drowned Parish | 1 | 99 | wimpled choir nun: full A-line to the floor, candle-amber wimple band, violet stole |
| FloodchoirChorister | floodchoir-marches (F) | Drowned Parish | 2 | 93 | black with a violet front panel and back bow, bone collar, crimson jewel |
| FloodchoirSteeple | floodchoir-marches (D) | Drowned Parish | 3 | 71 | a spire hat like the leaning church tower over a stained-glass bodice window |

All are under the raised gown budget of about 100 (Rhodri, 2026-11-01) and over the old 64.
The shared flaw in all eighteen is full-width block sleeves: the shoulder check passes them, but
critics read the top as broad. Narrowing the sleeves is the first fix for most of them
(`first_fix` in each `about.json`).

## Wave 2: Aor'lan (2026-11-02)

Wardrobe wave 2 for Aor'lan (Rhodri, arpg-game R039): two gown runs (`feminine` figure, slim
sleeves and a flared skirt asked for) and two armour runs, three picks from each, all from
swarm-lab briefs at `57474d7`. Each run had two render-only critic passes with one rework
between them; run evidence is in `results/<run>/`. Same files per set as above. Part counts are
`ArmourLook.partCount` on arpg-game main `20eaa41`, where every patch applies and `Catalog`,
`ContentCompleteness` and `DressBudget` pass. **EPIC** sets will get a worn particle effect in
the game later.

| Set | Run | Zone | Pick | Parts | In short |
| --- | --- | --- | --- | --- | --- |
| CinderveilObsidian | cinderveil-wave2 (C) | Aor'lan Mountain | 1 | 83 | obsidian court: fitted black bodice, ash corset, sulphur sash, wide charcoal bell with a magma-red hem |
| CinderveilCrystal | cinderveil-wave2 (A) | Aor'lan Mountain | 2 | 71 | black crystal crown, basalt bodice seamed with red cracks, the best flare from the hip |
| CinderveilFissure | cinderveil-wave2 (B) | Aor'lan Mountain | 3 | 66 | bright jagged magma cracks over basalt, ash stole and hem; the strongest lava read |
| CliffwindValkyrie | cliffwind-wave2 (A) | Aor'lan Cliffs | 1 | 75 | cliff valkyrie: pale sky-blue steel A-line with a real bell, white stomacher and cape, white bow-winged helm |
| CliffwindStorm | cliffwind-wave2 (B) | Aor'lan Cliffs | 2 | 80 | cloud-white skirt of jagged wind-cut panels flaring hard under grey-blue plate, winged helm |
| CliffwindEyrie | cliffwind-wave2 (D) | Aor'lan Cliffs | 3 | 74 | cloud-white bodice over a sky-blue skirt, tan leather, steel feather-crested half-helm |
<!-- wave2-aorlan-end -->

## Wave 2: Heartland (2026-11-02)

Wardrobe wave 2 for the Heartland (Rhodri, arpg-game R039): two gown runs and two armour runs,
three picks each, every run with two render-only critic passes and one rework between them; run
evidence is in `results/<run>/`. Same files per set as above. Part counts were measured with
`ArmourLook.partCount` on arpg-game main `7c1c5fb`, where each set's `renamed.patch` applies
and `Catalog`, `ContentCompleteness` and `DressBudget` pass. Gowns are on the `feminine`
figure under the 100-part gown budget; armour is under the 64-part budget. **EPIC** sets will
get a worn particle effect in the game.

| Set | Run | Zone | Pick | Parts | In short |
| --- | --- | --- | --- | --- | --- |
| HarvestbrideMilkmaid | harvestbride-wave2 (D) | Farmland | 1 | 85 | straw hat with a red ribbon over a tiered field-green bell, a true cone from the side |
| HarvestbrideApron | harvestbride-wave2 (B) | Farmland | 2 | 80 | wheat-gold apron skirt flaring from the waist, the warmest country colour |
| HarvestbrideWheatcrown | harvestbride-wave2 (F) | Farmland | 3 | 87 | tall wheat-sheaf crown over a parted gold skirt |
| AshveilGatekeeper **EPIC** | ashveil-wave2 (D) | Ashfields | 1 | 86 | ash A-line with a pale front panel and violet hem, violet gems at the waist and in a tall fan crown |
| AshveilGiantbone **EPIC** | ashveil-wave2 (E) | Ashfields | 2 | 81 | bone-spike crown over bone-and-charcoal rib pleats with violet seams |
| AshveilEmber **EPIC** | ashveil-wave2 (C) | Ashfields | 3 | 81 | the best bell from the hip: charred petal panels over a violet-glowing hem |
<!-- wave2-heartland-end -->

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
