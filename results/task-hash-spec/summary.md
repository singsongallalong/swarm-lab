# task-hash-spec

Task: A spec for systems/Hash

3 of 3 workers passed every check; estimated cost $0.12 (the estimate runs high; real spend has been about 1.2 cents per million tokens).

## g00 (deepseek): passed, held-out 4/6

- turns 19, 139.6 s, $0.0357
- says: Wrote tests/systems/Hash.spec.luau in the quoted house style, with one describe per function. It checks the [0, 1) range over 28 mixed negative, fractional and large inputs (21,952 triples per function), repeatability and per-input sensitivity over seven triples and three deltas, draw's floor behaviour on nine fractional triples, and three 4,096-draw streams for a mean near 0.5 with every tenth of the range hit.
- asks: draw is periodic mod 2^32, so changing an input by a multiple of 2^32 leaves the result unchanged; the sensitivity test uses steps of 1, -1 and 1000003.
- asks: The prescribed filter `lune run tests Hash.spec` also matches SpatialHash.spec, so that spec runs too (7 passed = 6 Hash tests + 1 SpatialHash test); harmless.
- patch: `runs/task-hash-spec/gens/g00/.swarm/patch.diff` (+162 -0); apply with `python3 -m swarm task apply runs/task-hash-spec g00`

## g01 (deepseek): passed, held-out 4/6

- turns 11, 201.7 s, $0.0494
- says: Added tests/systems/Hash.spec.luau covering both Hash.unit and Hash.draw: [0, 1) range over many negative/fractional/large inputs, repeatability (including out-of-order calls), and sensitivity to each of the three inputs. For draw it also checks flooring of fractional inputs including negatives, modulo-2^32 wrap (a full cycle is a no-op, negatives match their two's-complement twins), and over 4000 consecutive draws a mean within 0.02 of 0.5 with each tenth of the range holding 5-15% of draws.
- patch: `runs/task-hash-spec/gens/g01/.swarm/patch.diff` (+151 -0); apply with `python3 -m swarm task apply runs/task-hash-spec g01`

## g02 (deepseek): passed, held-out 4/6

- turns 13, 118.0 s, $0.0309
- says: Wrote tests/systems/Hash.spec.luau with six tests: both functions return numbers in [0, 1) across 1,331 triples each (negative, fractional and past-2^32 values), exact repeatability plus a different result when any one input moves, draw treating fractional inputs as their floors, and a 4,000-draw consecutive stream whose mean is within 0.01 of 0.5 and whose draws hit all ten tenths. The stream tolerance is deliberately tighter than sampling noise would need because draw is exact integer math (measured deviation 0.0032).
- asks: The check `lune run tests Hash.spec` also matches SpatialHash.spec by substring, so it reports 7 tests (my 6 plus SpatialHash's 1); harmless, both pass, but the filter is broader than it looks.
- patch: `runs/task-hash-spec/gens/g02/.swarm/patch.diff` (+93 -0); apply with `python3 -m swarm task apply runs/task-hash-spec g02`

## Notes (Claude, 2026-10-30)

- The first check rejected all three: the harness applied the swarm jobs' purity rule (a new file's requires) to a task that set none. Fixed in check.py; rechecked, 3 of 3 pass.
- Mutation score, all three: 4 of 6 mutants killed. One mutant ("draw doesn't floor a") was equivalent: bit32 floors its arguments anyway, so no spec can kill it; removed from mutants.sh. The one real survivor, a mix with its first xorshift dropped, is still a decent hash, so only a known-answer test (a pinned value of draw) catches it; none wrote one, and the brief didn't ask. Real score 4 of 5.
- Two workers noted the check filter `Hash.spec` also runs SpatialHash.spec (substring match). Harmless; a task writer should know the runner matches by substring.
- About 2-3 minutes and 11-19 turns per worker, about $0.12 for all three by the high estimate.
