# Task: design the $skill armour set: a courtly gown

You are one of several designers, each independently making a full set of four looks
(helm, chest, gloves, boots) that together dress the whole body as one gown, for the same
brief. Make one strong set, render it, check it, and
stop. Everything you need is in this file and in `.swarm/DIRECTION.md` (read that last:
it's your starting stance).

This is a dark, gothic Roblox action RPG: always night, a faint silver-blue moon, warm
amber lamps, low mist. Players see their character from a high camera (pitch 50, zoom
35), where armour reads by **colour and outline** before any detail.

## Hard rules (a run that breaks one is discarded unread)

1. **Edit only these, only as described:**
$files_section
2. **Four new look files**, one per slot (`slot = "Helm"`, `"Chest"`, `"Gloves"`,
   `"Boots"`), each `src/shared/data/armourLooks/$skill<Something>.luau`, each returning one
   `ArmourLookTypes.ArmourLook` whose `name` is exactly its file name and its key.
3. **Data only.** Each file starts with `--!strict`, requires only
   `require("../../ArmourLookTypes")` and `require("./Kit")`, and builds a table of parts.
   No other requires, no game API, no loops that could run forever. Local helper functions
   and colour tables of your own are fine (several existing looks have them).
4. **Register each look** in `ArmourLooks.luau`: one `local <Name> = require("./armourLooks/<Name>")`
   line and one `<Name> = <Name>,` line in the table. Nothing else in that file changes.
5. **Catalog each look** in `catalog/Gear.luau`: one line, after the other `armour:` rows,
   exactly `["armour:<Name>"] = row("<what it looks like, one sentence, under 90 characters>"),`
   (the formatter may wrap a long one onto three lines; that's fine).
6. **Stay within the part budget** (below): it's the one rule that's easy to break.
7. **No new base, numbers, drop weight or bag picture.** Looks only.
8. **Don't read files outside this pack** unless a command fails and its error names one.
   Don't browse the web. Don't explore the repo.
9. **Stop after at most two revisions** of your first working set.

## The brief

$brief

## The part budget (read this before you design)

Every player in a hub draws every other player's armour, so a set has a part cap. For this
set it's **100 parts** (raised from the game's usual 64 for gowns), and the spec counts it
harshly: it adds up the **heaviest look in each slot across every look in the game**,
yours included. The heaviest today are Helm 11, Chest 26, Gloves 12, Boots 12. So:

- `max(11, helm) + max(26, chest) + max(12, gloves) + max(12, boots)` must be **at most 100**.
- A split that works: **helm ≤ 18, chest ≤ 48, gloves ≤ 14, boots ≤ 20**. Move parts
  between slots if your design needs it, but keep that sum.
- A part is one entry in `parts`; a limb piece written once is drawn on both sides but
  counts as written. `Kit.studs` makes one part per stud, so studs are expensive.
- `armourpreview` prints each look's parts and the set's total. `lune run tests ArmourLooks`
  is the judge: if it says the heaviest set is over 100, cut parts.

Spend parts on the silhouette (the waist, the skirt's width and fall, the sleeves, the
headpiece), not on small detail no one sees from above.

## Dressing the whole body: which slot carries which part of the gown

A gown spans every slot, and each slot may only cover its own body parts (the guide's
"Body space"): Helm the `Head`; Chest the `UpperTorso`, `LowerTorso`, `UpperArm` and
`UpperLeg`; Gloves the `LowerArm` and `Hand`; Boots the `LowerLeg` and `Foot`. So:

- **Chest:** the bodice and collar on `UpperTorso`, the waist and any bustle or stomacher
  on `LowerTorso`, the sleeves' upper part on `UpperArm`, and the **upper skirt hung from
  the thighs** (`UpperLeg`), like `Kit.flaps` and the Linen Robe's panels.
- **Boots:** the **rest of the skirt and the hem**, continued on the shins (`LowerLeg`):
  petticoat edge, ruffles, the skirt's bottom tier, then the shoes on `Foot`.
- **Gloves:** the sleeves' lower part, cuffs and lace on `LowerArm`, gloves on `Hand`.
- **Helm:** bows, bonnets, veils, headdresses, hair ornaments on `Head`.

Hard truths of the rig, so the gown works when the character runs:

- **Nothing on `LowerTorso` may hang below its bottom** (a spec): anything rigid there ends
  up inside a striding thigh. Skirts hang from the thighs.
- **Each thigh and each shin moves on its own**, so the skirt is panels on each leg that
  part as the legs stride, as the Linen Robe's do. Make each leg's panels wide and set to
  the outside of the leg so, standing, the two legs' panels meet into one full skirt.
- **A thigh's panels should stop above the knee**, or they cut through the bending shin;
  carry the skirt on down with the shins' panels (the Boots look) so it reads as one long
  skirt standing still.
- A full, wide skirt reads from the high camera as a bell or a cone around the legs: that
  shape is what makes the family read. Width and fall matter more than detail.

## How a look is built

$types

$kit

### Examples, one per slot (the chest is the game's one robe, the nearest thing to a gown)

$example_helm

$example_chest

$example_gloves

$example_boots

$registry

## The rules

These are the art direction's rules and the guide for armour looks, quoted whole. Every
finding against your set will cite one of them. Read "Body space" and "Rules of thumb"
in the guide closely: where pieces sit, what each slot may cover, and why skirts hang
from the thighs.

$rules

## Commands

Run every command from the worktree root, exactly as written, replacing only
`<YourLook>` with your four looks, comma-separated, in the order Helm,Chest,Gloves,Boots
(for example `ReaverHelm,ReaverChest,ReaverGloves,ReaverBoots`).

Format first (the format check fails on unformatted files, and it also sorts the
registry's require lines for you):

```
stylua src/shared/data/armourLooks src/shared/data/ArmourLooks.luau src/shared/data/catalog/Gear.luau
```

Render every family's set once, as the reference your family must stand apart from:

```
$ref_cmds
```

Render your set (again after each revision, with a new `r<n>` in the names):

```
$render_cmds
```

The first render shows six views: front, back, side, three-quarter, **the ARPG camera**
and over the shoulder. `close` frames the body three times bigger; `fit` adds a taller,
slimmer avatar, to check pieces stretch without gaps or poking through.

Then **look at every image you rendered** with your Read tool, the ARPG column first.
Ask: does it read as its own family at a glance, apart from every row of the reference?
Does the outline say gown (a fitted waist, a full skirt, a headpiece) before any detail
does? Does the skirt read as one skirt standing, from the front and the ARPG camera, or
as separate leg panels with gaps? Is it elegant, and still aged a little at the edges?
Does anything float off the body, cut into it, or leave the body showing through a gap?
Does the slim avatar still look right?

Check everything (a failure means the run is discarded). The lint fails on **warnings**
too: a colour, helper or `Kit.colors` alias you declare and never use fails the run, so
declare only what that file uses.

```
$spec_cmds
```

## When you're done

Write `.swarm/manifest.json`, and then stop:

```json
{
  "skill": "$skill",
  "look": "<your four looks, comma-separated, Helm,Chest,Gloves,Boots>",
  "rows_added": ["<every look name>"],
  "intent": "<one sentence: the gown's era and look, and how it reads from the high camera>",
  "renders": ["<the paths of your final renders, the reference excluded>"],
  "revisions": 0,
  "requests": ["<optional: a colour, material or kind of piece the set wanted but couldn't have, one line each>"]
}
```

No report, no summary in chat. The manifest is the only thing read.
