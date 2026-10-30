# The kit process: DeepSeek makes the pieces, a Claude builder makes the map

> Started 2026-10-30, on the Eternal Domain (arpg-game `docs/roadmap/areas/eternal-domain.md`).
> fafwa: "having deepseek draw entire maps has so far been good, but not acceptable for the
> final game ... try having deepseek meaningfully help my builder build a map ... perhaps
> having deepseek generate features/cells".

## Why this split

What we measured:

- **Whole maps:** DeepSeek's are sound, but weak in composition and in how much their seeds
  vary. Critics scored them 4–6.
- **Narrow tasks:** these do best. One prop to a spec, or five poses on a fixed timeline,
  beat open briefs; a blocking pass won the motion pilot and looked good to fafwa in Studio.
- **Reworks:** these rarely raise a score. More first attempts beat more rounds.

So the **builder** (a Claude session in arpg-game) keeps what DeepSeek is weak at: the
layout, composition, which piece goes where, and the Studio lane. **Workers** make the many
pieces, each one bounded and checked by a spec. They work in the game's real data, as sculpt
rows and set piece rows, so there's no platform to merge first.

## The steps

| # | Who | What | Time |
| --- | --- | --- | --- |
| 0 | Builder | **The kit brief:** the look in numbers (palette, colour limits, materials, scale against the 5-stud person), a theme row for its effects, and the **kit list**, one line per piece the layout needs: landmarks (one per room), repeating props (columns, braziers), markers, wreckage. Usually 10–20 lines. | 20–30 min |
| 1 | Workers | **The kit run:** `python3 -m swarm run arpg-game kit <Area> --gens deepseek:<n> --offpeak`, one line of the list per worker (`directions.txt`). Each makes one to three sculpt rows and maybe one set piece, renders them and passes the specs. | ~30 min, ~$2 for 12 |
| 1b | Builder, meanwhile | **The layout:** the generator, or a new tileset on an existing one (the Labyrinth's storeys, a field's heath). It places **marks by role** (landmark, colonnade, lamp, marker, wreck) and doesn't yet know which sculpt fills each. | in parallel |
| 2 | One blind critic | **The shelf:** scores the pieces on renders only and picks which to keep. No reworks: a weak piece's line goes into the next run as a fresh attempt. | 5 min |
| 3 | Builder | **Apply the shelf:** `swarm apply` each kept candidate; rows only add, so they stack. Read every render before taking a piece. | 10 min |
| 4 | Builder | **Assemble:** a dressing table, role → shelf sculpts and set pieces, and the tileset's paints. Then the `map-critic-loop` skill's renders and critics, then a lane. | the builder's normal loop |

Runs repeat. A second kit list can cover what the first shelf lacks, and another area's kit
can run while the builder assembles this one.

## What the builder must not hand off

These stay with the builder:

- the layout and its topology;
- the composition: where the landmark stands and what the camera sees;
- the area's look decisions;
- saves, places, networking and anything under fafwa's word.

Workers also don't choose their own pieces: the kit list does.

## The blind reading (fafwa's idea, 2026-10-30)

The critic is never shown the piece's line. It first writes what it sees ("a seated giant
on a throne, gold crown"), and only then scores. A judge compares that description with the
hidden line. A piece whose description doesn't match its line doesn't read as itself, and
that is the most common failure from the high camera.

**As a stopping rule:** stop when the blind reading matches the line and the quality score
clears a floor, or after at most N attempts. The floor matters because a description can
match a plain, ugly piece. To be tried on the next run's critic. The Domain smoke test's
critic still sees the lines.

## The Eternal Domain smoke test (domain-kit-1)

- **Platform (trial):** `docs/kit/0001`. It adds a `domain` theme and colour limits for
  `domain_` sculpts: ivory stone up to value 0.92, gold up to saturation 0.55. The art bible
  says "always night, muted", so this needs **fafwa's amendment to the bible** before any of
  it merges.
- **The kit list:** 12 pieces in `targets/arpg-game/kit/directions.txt`: column, seated
  colossus, great gate, triumphal arch, spire, throne-dais, brazier, carved face, golden
  tree, pool of light, waystones, fallen god.
- **Log:** below.

## Log

- 2026-10-30: domain-kit-1 launched: 12 workers off-peak.
