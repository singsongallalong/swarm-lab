# The experiment: does a cheap generator swarm beat the current loop?

## Question

For arpg-game's skill effects, does generating wide with cheap models (many attempts,
filtered automatically, the best picked blind) give looks that win the daily playtest
at least as often as the current Claude actor-critic loop, for less orchestrator time,
or find looks the current loop wouldn't?

## Arms

| Arm | Generators | Then |
|---|---|---|
| A, control | the current `effect-critic-loop`, actor and critic both Claude | as today |
| B | `--gens deepseek:15` | blind sheet → orchestrator picks → `effect-critic-loop` on the pick |
| C | `--gens qwen:15` | the same |
| B+C (optional) | `--gens deepseek:8,qwen:7` in one run | the same; the sheet mixes them blind |

Same briefs for every arm: `ColdSnap`, `Sleet`, `Vault`, `SnareArrow` (the R036 skills
with borrowed looks; `targets/arpg-game/effects/briefs/`).

## Order

1. **Smoke run, one brief, 3 generators per provider.** Read every generator's log and
   pack-following by eye. Fix the pack before scaling. Expect the first problems to be
   the endpoint (does image reading work through it?) and generators wandering off the
   pack.
2. **Throughput.** Raise `--concurrency` until renders or the provider's rate limit
   slow things; note where.
3. **The four briefs, all arms**, over about a week. Ship winners from different arms
   on different days. Keep the arm hidden from the playtester until the week's end.
4. **Write the verdicts** in `results/ledger.csv`'s `playtest` column (keep / revise / cut
   plus a few words), then decide.

## What's recorded (`results/ledger.csv`, one line per run and provider)

Generators, finished, survived the filter, picked, tokens, cost, median seconds, the
most common rejection, and the playtest verdict (by hand). The orchestrator's own
token use isn't measured by the harness: note it from the session.

## Success

B or C wins the playtest at least as often as A at a lower total cost, or surfaces looks
A never tried. Failure is informative too: if survivors are all alike, strengthen the
directions; if few survive, read the rejections and fix the pack before blaming the model.

## Prices

Recorded 2026-10-28 in `providers.toml`, from price trackers that disagreed. DeepSeek's
current Flash model (V4.1-Flash-1017) had no price on its official page when checked.
Check every provider's own price page before a run; the report's costs are only as good
as these numbers.

## Open

- **Qwen and Kimi endpoints are unverified.** `providers.toml` guesses their
  Anthropic-compatible URLs. If either has none, it needs an OpenCode runtime
  (`runtime = "opencode"`), which isn't built.
- **No model has run through the harness yet.** It was tested end to end against the
  real arpg-game (real renders, real specs, real filter) with a scripted stand-in
  generator, never with a real model, because no provider key was at hand.
- **arpg-game's `docs/guides/claude-skills.md`** still says fafwa sees renders before
  anything else. If the orchestrator is now the gate, update that line.
- **Other jobs.** The same harness fits the set-piece and map loops (their previews are
  offline too) once each has a job folder: a pack template, allowed files, specs.
