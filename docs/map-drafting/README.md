# Map drafting: the platform the maps job needs

`0001-drafted-maps.patch` applies to arpg-game main (`166b53d`, 2026-10-29). Runs of the
`maps` job apply it to their own base clone only; the game repo is never touched.
It carries two things:

- **The Moonwell barrow glade** (candidate F of `results/moonwell-zones`): the `moonwell`
  tileset, its sculpts, the `moonwell` theme and set pieces, and their catalog rows. Drafted
  maps are drawn in it.
- **The drafted-map platform:**
  - `src/shared/systems/DraftedMap.luau`: the contract (a draft is a name, a tileset, a
    seeded `generate(rng) -> Heath.Map` and optional `landmarks(map, rng)`), `problems(map)`
    in plain words, and `dress()`, which runs MapDress with the landmarks kept clear and
    then adds them;
  - `src/shared/data/DraftedMaps.luau`: the registry, empty;
  - `src/shared/systems/draftedmaps/`: where drafts go;
  - `tests/systems/DraftedMaps.spec.luau`: six seeds each must be sound, deterministic,
    varied and within `PerfBudget.map`;
  - `scripts/dresspreview.luau`: `layout=<Name>` draws a draft, with a `landmark` kind;
  - `scripts/catalog/Families.luau`: DraftedMaps filed beside Terrain.

Untested in Roblox: only the offline previews and Lune specs have run it. Turning a draft
into a real map (a builder, a place, seams, packs) is a design question for fafwa first
(arpg-game docs/guides/adding-areas.md, "A new kind of map").
