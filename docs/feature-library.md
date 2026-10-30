# Plan: a features library for drafted maps

Status: **plan, for fafwa's approval** (2026-10-30). Nothing here is built yet.

## Why

The loosened frozen-lake run (rimelake-open) showed where whole-map generators struggle.
Each builder wrote 900–1,300 lines and hit time limits. The critic found no subject to frame
a shot around, seeds that barely differed, and the same effect four times. The maps that read
as places had a *structure*: the cathedral's avenue of pillars, the crater's terraces. And every
builder asked for the same missing pieces: height per painted cell, and ground that glows.

So split the work: a swarm makes **features** (one structure each, judged alone), and map
builders **assemble** them. fafwa (2026-10-30): "a large standard library of each asset type
would help parallelize workflow". Features are the first library; monsters and props follow the
same pattern if it works.

## The pieces

### 1. Shared cell kinds (arpg-game, data)

`data/CellKinds.luau`: one row per kind of ground, tagged by area palette. A row holds:

- its surface: a material and colour;
- its lift;
- whether it clears the tileset's props;
- its prop scatter;
- **new:** `glow` (a light colour and range, for a breathing crack or a lit fall);
- **new:** per-cell height taken from the feature that paints it, so no more `ridge_low`, `ridge_mid` and `ridge_high` copies.

A draft's `cells` then names rows instead of inlining looks.

### 2. The feature contract (arpg-game, pure code)

`systems/MapFeature.luau`. A feature is a seeded function. Given a size class and an rng, it
returns:

- **footprint:** a small grid, about 8 × 8 to 48 × 48 cells, of cell kinds from CellKinds or the map's own, plus walkable or wall, and heights;
- **anchors:**
  - `road`: where a road may enter and leave, as edge points;
  - `camera`: one or two photo spots with a target;
  - `effect`: spots for set pieces;
  - `landmark`: optional sculpt spots;
- **tags:**
  - area or palette;
  - scale (`small`, `medium`, `centrepiece`);
  - role (`centrepiece`, `crossing`, `filler`, `boundary`, `hazard`);
  - mood words.

`MapFeature.problems(feature)` checks it: walkable cells joined up, every road anchor on
walkable ground, steps of 2 studs or less between walkable cells (or a bluff), and anchors
on the footprint.

`MapFeature.stamp(map, feature, x, z, rotation)` puts a feature onto a drafted map. It is used
by assemblers and tested in Lune.

### 3. A feature preview (arpg-game, script)

`scripts/featurepreview.luau <Name> <out.png> [seeds]` shows a feature stamped on a plain pad
of its area's ground, with the red 5-stud post, in four views:

- three-quarter;
- eye level from a road anchor;
- the feature's own camera anchor (its photo);
- top-down, with the anchors marked.

It shows three seeds and reuses dresspreview's renderer.

### 4. The features job (swarm-lab)

`targets/arpg-game/features/`:

- **Runs:** 12–20 builders per area, each with its own direction (a frozen fall, a pressure ridge, a spire cluster, a crater rim, a drowned grove, an ice bridge...), or one direction family per run.
- **What a builder writes:** one module, `features/<Area><Name>.luau`, plus optional CellKinds rows with the area's prefix.
- **Turns:** about 60. Features are small.
- **Critic:** a render-only critic per run. It weights the photo from the feature's camera, then how well the feature reads at game scale and how much its seeds vary. One rework round.
- **Shelf:** survivors that pass go to `library/features/<area>/<Name>/` in swarm-lab, with the patch, renders, critic scores and tags. A generated `library/features/index.md` and a contact-sheet gallery serve browsing.

### 5. Assembly (swarm-lab maps job, revised)

Map builders get the shelf's index and renders for their area, and write **layout and road
only**. Each map:

- places one centrepiece, two to five supporting features, and quieter ground between, with `MapFeature.stamp`;
- runs the road through the features' road anchors;
- takes its shots from the features' camera anchors, or its own.

A rule keeps maps varied: a centrepiece is used by one map at most. The photo critic then
judges the whole composition. A winning map's patch carries only the features it uses
(promotion).

### 6. Promotion into the game

Shelf content enters arpg-game **only when a map uses it**, through the usual path:

1. the map-critic-loop;
2. a Studio check and lane;
3. fafwa's eye;
4. a PR.

The shelf stays in swarm-lab, so the game repo doesn't grow with unused candidates, and
`ContentCompleteness` stays meaningful.

## Order of work

1. **Platform** (one trial branch in arpg-game, carried into runs as `docs/map-drafting/0004`, like 0003):
   - CellKinds;
   - MapFeature with `problems` and `stamp`;
   - featurepreview;
   - specs.
   About 4–6 files. Plan approval is this document.
2. **The features job** in swarm-lab, a dry run with a hand-made stand-in feature, then a
   Rimeholt pilot: about 12 builders. The estimate is about $0.30–0.50 each by the harness
   (real spend has run 3–4× lower).
3. **The shelf** (`library/`), index and gallery, from the pilot's survivors.
4. **Assembly:** the maps job revised to place features. Six maps from the Rimeholt shelf,
   judged by the same critic as rimelake-open, so the two runs compare like for like.
5. If assembled maps beat whole-map drafts, a skill update (`deepseek-swarm`) and the same
   pattern for the next libraries: props (sculpts) and monsters (with the monster-creation
   rules).

## Open questions for fafwa

- **Where the shelf lives:** swarm-lab (proposed) or a folder in arpg-game?
- **Who browses and vetoes shelf entries:** fafwa only, or the second person too?
- **Area palettes first:** should we define several palettes ahead of time (cheap) so features for future areas can be generated before those areas are designed?
