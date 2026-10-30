# Worker rules for arpg-game

Quoted into every worker task's pack (swarm task). Excerpted from arpg-game's CLAUDE.md; update when it changes.

## Stack

- Luau, `--!strict` at the top of every file. No exceptions.
- Lune runs the pure-logic tests: `lune run tests <filter>`. Selene lints (`selene <paths>`), StyLua formats (`stylua <paths>`).
- `src/shared/systems` is pure logic, `src/shared/data` content tables, `tests/systems` their specs. The offline test rng has only `NextNumber` (no `NextInteger`).

## Architecture rules

1. **Server is authoritative.** The client sends intent only ("use skill 3 at position X"). The server validates range, cooldown, resource cost and line of sight, then resolves hits, damage, drops and rewards. Never trust a number from the client.
2. **Content is data, logic is code.** New items, affixes, skills and monsters should be added by editing tables in `shared/data`, not by writing new branches in logic. If adding content requires a code change, flag it — the system is probably missing an abstraction.
3. **All stats flow through the stat system.** Every buff, affix, passive and debuff is a modifier: `{ stat, kind: "flat" | "increased" | "more", value }`. No ad-hoc stat math elsewhere.
4. **`shared/systems` stays pure.** No `game:GetService`, no Instances, no yielding. Takes data in, returns data out. This is what makes it testable in Lune.
5. **Randomness is seedable.** Loot and affix rolls take an RNG (`Random.new(seed)`) as a parameter so tests are deterministic.
6. **Networking goes through `shared/net`.** No creating RemoteEvents ad hoc.

## Conventions

- PascalCase for modules, services, types; camelCase for functions and locals.
- Explicit types on all function parameters and return values.
- Prefer small modules (<300 lines). Split when growing past that.
- No `wait()`, `spawn()`, `delay()` — use `task.*`.
- No global state outside services/controllers.
- Comments explain *why*, not *what*.

