# Handoff: importing the 2026-10-30 assets into arpg-game

For a Claude Code thread fafwa starts on the import and repairs of the assets DeepSeek made
on 2026-10-30. Read this, then arpg-game's `CLAUDE.md`, its stream
`docs/streams/map-features.md` (latest on `claude/map-features-sites`) and
`docs/guides/map-features.md`.

## What exists

**Merged into arpg-game main:**

| PR | What it is |
| --- | --- |
| #936 | The map feature contract: `systems/MapFeature`, `FeatureLook`, `FeatureDress`, `FeaturePad`, `MapVariety`, `data/MapFeatures`, the moor example `MoorBarrowRing`, and `dresspreview feature=<Name>` |
| #937 | `assembly`, the sculpt kind whose shape is data |
| #933 | Bible B12: the Eternal Domain is the one exception to night gothic, with `domain_` colour limits |
| #935 | Draft effects in the motion lab |
| #932 | The SmashBlock drafts (C393, passed by fafwa) |

**Open in arpg-game:**

| PR | Branch | What it is | State at handoff |
| --- | --- | --- | --- |
| #942 | `claude/map-features-sites` | Feature sites in the real generator: `systems/FeatureSites`, wired through `MapPlan.lay` and `MapWalk`. An area opts in with `features = { count, pool, spacing }`, and none does yet | CI's lune tests red. The orchestrator session's agent is fixing and merging it |
| #940 | `claude/domain-tileset` | The Domain kit (8 sculpts and set pieces from domain-kit-1), the `domain` outdoor tileset, its `domain` lighting preset, and check C394 | CI's type check red. The same agent is fixing and merging it |
| #934 | `claude/kit-builder-skill` | Skills updated from the runs: `kit-builder`, `deepseek-swarm`, the capability sheet, Lebègue's brief | docs only, CI running |

If #942 or #940 is still red when you start, you can read CI's logs from the PC, which the
cloud session can't. Repair it there: merge `origin/main` into the branch, never rebase.

**The shelves, in swarm-lab** (`library/`, committed, one folder per kept piece with
`patch.diff`, `sheet.png` and `about.json`; each `index.md` has the scores and the critic's
role for every piece):

| Shelf | Pieces | Made against | Needs in the game |
| --- | --- | --- | --- |
| `library/features/Moor/` | 7 features: hillfort, split barrow, sinkhole, peat cutting, drowned causeway, sheepfold, strike crater | main after #936 | nothing more |
| `library/features/Domain/` | 23 features: 8 from domain-features-1 (first table), 15 from domain-features-2 (second table) | `claude/domain-tileset` | #940 merged (the `domain` tileset and kit) |
| `library/kits/Domain/` | the Domain kit | already in #940 | none |
| `library/features/Rimeholt/` | 10 features | swarm-lab's own platform | **out of scope**: the game has no Rimeholt tileset |

## The import (your job)

1. On a branch from `origin/main`, **after #940 has merged**, from a swarm-lab clone:
   ```
   python3 -m swarm shelf - --into <arpg-game worktree> --patches library/features/Moor/*/patch.diff
   python3 -m swarm shelf - --into <arpg-game worktree> --patches library/features/Domain/*/patch.diff
   ```
   `--patches` lays each patch's added lines and new files in after the context line the
   patch shows, without the run's worker trees. Those are 18 GB and live only in the cloud
   session. It was tested by bringing the seven moor features onto main: every spec passed.
2. **Duplicate names across runs:** two workers may have used the same `domain_` sculpt, set
   piece or feature name (`domain_lamp`, a second `DomainThrone`). A duplicate dotted row
   silently overwrites. Grep `Sculpts.luau`, `SetPieces.luau`, `catalog/World.luau` and
   `MapFeatures.luau` for repeated keys, and rename the later one everywhere it's referenced.
3. `stylua src tests`, then run these specs: `MapFeatures`, `Sculpt`, `SetPiece`, `Catalog`,
   `ContentCompleteness`, `OutdoorTilesets`, `FeatureSites` (once #942 is in), and `selene`.
   If one feature fails a spec you can't fix quickly, leave it out and list it.
4. Look at a few features alone (`lune run scripts/dresspreview shots out.png 2 1
   feature=<Name>`) and at moor maps drawing from a pool (`mappreview ... features=...`,
   `dresspreview featuresite ... features=...`; the guide has the syntax).
5. Document the libraries in `docs/guides/map-features.md` ("Libraries": name, size, role,
   the critic's line) with a suggested starting moor pool:
   - small features weighted highest;
   - the drowned causeway left out, since crossings aren't placed yet.
6. PR it, wait for CI, and merge when green: it adds content and changes no live map.

## Studio (your thread can do this; the cloud session can't)

- **C394, the Domain's look and holy-day lighting:** a map lane with the stand-in map set to
  `domain`. The lighting values are guesses. It checks whether the rims read as cloud, and
  the dark moor ruins (known: the Domain needs its own building kit).
- **C395, map features in a real map once an area opts in:** before the moor's live opt-in.
  Known issue: `WalkStamp` doesn't block monster paths at landmarks marked `solid`, so
  monsters may walk through a feature's stones. Fix that before the opt-in.
- **The moor's live opt-in** (adding `features` to its terrain params and re-recording its
  golden hash) waits for C395 and fafwa's word.

## Not in this handoff

- **The Domain's own map plan:** platforms and causeways over cloud, assembled from the
  Domain shelf. It waits for fafwa's go.
- **Placing crossings on heath maps.** It would mean rerouting the road.
- **A Domain building kit,** to replace the moor ruins.

## Known caveats

- `FeatureSites.luau` is about 500 lines; it could be split.
- Sculpt preview panels print sculpt names, so a critic's "blind reading" sees them.
- Run costs and lessons: swarm-lab `docs/kit-process.md`, and arpg-game's
  `.claude/skills/kit-builder/SKILL.md`.
