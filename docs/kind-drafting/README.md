# Kind drafting: handoff for arpg-game

**For the arpg-game thread.** This folder holds a prototype of the game-side platform the
swarm's `kinds` job needs: a way for one pure Luau module to be a new area kind, drawn by
both the game and the offline preview with no drawing code of its own. It was built and
tested against arpg-game `41c9339` (main, 2026-10-29 10:45; first built on `edb9b50` and rebased) in swarm-lab's workspace, and never
pushed. arpg-game is yours: take it, change it, or redo it from the contract.

## What it is

Today a new area kind means hand-wiring five places: a `DrawnEffects` type, a branch in
`AreaFx`, and three switches in `areapreview`, plus a spec. With this platform:

- A **drafted kind** is one module in `src/shared/systems/drafted/`, keeping the contract
  in `src/shared/DraftedTypes.luau`: `count`, `lasts`, `plan` (all randomness, once per
  cast), `pose` (every piece at any age, in the area's frame, same shapes in the same
  order at every age and power), and optionally `bursts`.
- It's listed by one line in `src/shared/systems/DraftedKinds.luau` and used by a
  `DrawnEffects.area` row of kind `Drafted` whose `layout` names it. The row's other fields
  are the module's own numbers, so `perPower` grows them like any row's.
- **`AreaFx` draws any drafted kind generically:** it lends `count` parts once, by the
  shapes of the first pose, and re-poses them by index every 1/30 s until `lasts`, the way
  Flames and Volley already work. `areapreview` has one matching generic branch.
- **`tests/systems/DraftedKinds.spec.luau`** holds every drafted row to the contract:
  count fixed across ages and powers (over a circle, two cones and a Line) and within `PerfBudget.castEffects.parts`, shapes
  stable by index, pieces near the area, invisible by `lasts`, deterministic per seed.
- `ShardBloom` is the reference kind (row `ShardBloomExample`, `spare`).

## The patch

`0001-drafted-area-kinds.patch`, 9 files, +578/-8:

| File | Change |
|---|---|
| `src/shared/DraftedTypes.luau` | new: the contract, the frame, the types |
| `src/shared/systems/DraftedKinds.luau` | new: the registry |
| `src/shared/systems/drafted/ShardBloom.luau` | new: the reference kind |
| `tests/systems/DraftedKinds.spec.luau` | new: the contract spec |
| `src/shared/data/DrawnEffects.luau` | the `Drafted` row type in `AreaLook`, its line in the kinds comment, the example row |
| `src/shared/systems/AreaBursts.luau` | drafted kinds burst where their module says (or once at the origin) |
| `src/shared/systems/AreaTint.luau` | `Drafted` in `PASSED` (AreaTint.spec fails on an unlisted kind) |
| `scripts/areapreview.luau` | one generic branch: stills over `lasts`, pieces turned into the preview's frame, faded toward the night |
| `src/client/primitives/AreaFx.luau` | `drafted()`: the generic drawer, and its line in the dispatch |

Apply it on a branch with `git am docs/kind-drafting/0001-drafted-area-kinds.patch`
(from a checkout of swarm-lab, or copy the file over).

## What was checked, and what wasn't

Checked (measured): `stylua --check` clean; `selene` 0 warnings on the changed sources;
`lune run tests` for DraftedKinds, AreaBursts, AreaTint, DrawnEffects, AreaLayout,
ContentCompleteness all pass; `areapreview ShardBloomExample` renders on a circle and an
18° cone (`shardbloom-example-circle8-p0-4-8.png`). The spec was shown to fail, with a
clear message, on four deliberately broken versions of the reference kind (a piece
vanishing mid-look, a piece changing shape, a piece past the area, a look that never
ends).

**Not checked:**
- **The type check** (`luau-lsp analyze`): the type definitions wouldn't download in that
  workspace. Watch the `Drafted` row type (props plus a `[string]: any` indexer inside the
  `AreaLook` union) and the narrowing at the `drafted()` call in `AreaFx`.
- **The client drawer has never run in Roblox.** It needs a lane: cast a skill pointed at
  `ShardBloomExample` (or set `AreaLookOverride` to it in Studio) and check the shards
  appear, lean out, fade, and are cleared; that Cylinders from `Draw.beam` take the posed
  size and CFrame; that Material changes apply; and the cast probe's frame time with
  several casts on screen (`pose` runs every 1/30 s per cast).
- **Pooling:** parts are lent by `Draw` per shape and returned with `Draw.clear`, as Flames
  does; confirm the pool's `cap` handles a few drafted casts at once.

## Why the contract is shaped like this

- **Fixed count and shapes:** the client lends parts once and re-poses them; a piece
  appearing or changing shape mid-look would need new parts every frame. It also keeps
  SE3 (grow, never multiply) checkable.
- **Randomness only in `plan`:** `pose` runs every frame, so it must give the same cast
  every time; and every client must draw the same cast from the same seed.
- **The frame** (`+X` right, `+Y` up, `-Z` ahead, origin where the area is centred) is
  exactly AreaFx's existing `frame * CFrame.new(p.r, 0, -p.f)`, so client positions drop
  straight in. The preview turns it half a turn about Y to its own convention.
- **Pure modules** (no game, Instances, task) keep them in `shared/systems` under rule 4,
  testable in Lune, and safe to accept from a swarm: swarm-lab's filter enforces purity
  statically before any spec runs (`targets/arpg-game/kinds/job.toml`, `[purity]`).
