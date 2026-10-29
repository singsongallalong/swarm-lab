# swarm-lab

Wide generation for game content: many cheap generator agents try the same brief in
parallel, an automatic filter drops what breaks the rules or the specs, and a strong
orchestrator picks the best few from a blind contact sheet. The winners then go through
the game repo's usual actor-critic loop and the daily playtest.

This repo holds the harness only. Everything that describes a game lives under
`targets/<game>/` here for now and moves into the game's own repo once it settles
(see "Where things live").

```
brief ──► context pack ──► N generators (one worktree each, own model, own direction)
                                 │
                     allowlist + row rules + specs   (automatic, no one looks)
                                 │
                       blind contact sheet ──► orchestrator picks 2–3
                                 │
                 winner's patch ──► branch in the game repo ──► critic loop ──► playtest
```

## Quick start

Needs Linux (a cloud container or WSL), Python 3.11+, git, Pillow, the `claude` CLI
(Claude Code) and the game's own toolchain (for arpg-game: `lune`, set up by its
`scripts/cloud-setup.sh`).

```bash
pip install pillow            # the contact sheet's only dependency
cp .env.example .env          # add the provider keys you'll use; .env is gitignored
set -a; . ./.env; set +a

# 1. Look at the context pack a brief produces, before spending anything
python3 -m swarm pack arpg-game effects ColdSnap

# 2. Run a small swarm: 3 DeepSeek and 3 Qwen generators on Cold Snap
python3 -m swarm run arpg-game effects ColdSnap --gens deepseek:3,qwen:3

# 3. Filter, tile and summarise (run does these too; rerun any step alone)
python3 -m swarm check  runs/<run-id>
python3 -m swarm sheet  runs/<run-id>
python3 -m swarm report runs/<run-id>

# 4. The orchestrator reads runs/<run-id>/select.md, looks at the sheet and writes
#    runs/<run-id>/selection.json. Then put a winner on a branch in the game repo:
python3 -m swarm apply  runs/<run-id> C
```

`python3 -m swarm run ... --dry-run` builds the worktrees and packs and prints the
commands without calling any model.

## Layout

| Path | What |
|---|---|
| `swarm/` | the harness: `pack`, `run`, `check`, `sheet`, `report`, `apply` |
| `providers.toml` | endpoints, model ids, prices, caps per provider |
| `targets/arpg-game/target.toml` | where the game is, its setup, which files are hidden from generators |
| `targets/arpg-game/effects/` | the effects job: pack template, allowed files, specs, directions, briefs |
| `prompts/select.md` | the orchestrator's selection prompt |
| `docs/experiment.md` | the experiment plan: arms, metrics, what counts as success |
| `results/ledger.csv` | one line per finished run, committed: the experiment's record |
| `runs/` | worktrees, logs, renders, sheets (gitignored) |
| `tests/` | an end-to-end test against a fake game repo and a fake generator |

## How a generator is kept on task

- **One worktree each**, detached at the run's base commit, so generators can't see or
  clobber each other.
- **A closed task.** The game's `CLAUDE.md` and `.claude/` are removed from the
  worktree and replaced by a stub that points at `.swarm/PACK.md`. Repo bookkeeping
  (streams, pass numbers, coord notes, lanes) is the orchestrator's job, never a
  generator's.
- **The context pack** quotes the rules in full, shows the rows it may change and two
  good examples, and gives every command with paths filled in. It's identical for
  every generator in a run so the provider caches it; the per-generator direction is
  a separate file read last.
- **Enforced, not requested.** After a generator stops, `check` rejects the run if it
  touched any file outside the job's allowlist, changed an existing row it doesn't own,
  named a new row without the skill's prefix, or left no valid manifest. Then the specs
  run. Only survivors reach the sheet.
- **Caps**: turns and wall time per generator, and a run-level token budget per
  provider (`providers.toml`).

## Where things live

`targets/arpg-game/` describes the game: rule files, data files, render commands. When
the swarm proves itself, move that folder into the game repo (`arpg-game/swarm/`) and
point `target.toml`'s `job_dir` at it, so a renamed data file or a new rule changes in
the same PR as the game. Until then, check the job against the game after big changes
with `python3 -m swarm pack ...`, which fails loudly when a file or row it quotes is gone.

## Keys

Keys come from the environment only (`.env`, gitignored). Never put a key in
`providers.toml`, a pack, a log or the game repo.
