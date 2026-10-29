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

Needs Linux (a cloud container or WSL), Python 3.10+, git, Pillow, the `claude` CLI
(Claude Code, which needs a recent Node: Ubuntu 22.04's own `nodejs` is far too old,
see below) and the game's own toolchain (for arpg-game: `lune`, set up by its
`scripts/cloud-setup.sh`).

```bash
pip install pillow tomli      # tomli only matters on Python 3.10
cp .env.example .env          # then put your keys in .env (gitignored); the harness reads it itself

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

**The two jobs.** `effects` composes a look from the game's existing kinds: rows only,
cheap, safe, but the looks tend to converge. `kinds` invents new drawing: each generator
writes a small pure Luau module (a drafted kind: curves, spirals, branching...) that the
game and its preview draw generically. Same briefs, same commands:

```bash
python3 -m swarm run arpg-game kinds ColdSnap --gens deepseek:6 --concurrency 6
```

Until arpg-game merges the drafted-kinds platform (`docs/kind-drafting/`), a kinds run
applies it to its own base clone, never to your repo. (`swarm pack ... kinds ...` reads
your repo as it is, so it needs the platform merged; to see a kinds pack before that,
use `run --dry-run` and read `runs/<id>/pack.md`.)

Tests: `python3 tests/test_end_to_end.py` (the whole pipeline on a fake game) and
`python3 tests/test_checks.py` (the code and file rules).

## Setting up WSL (Ubuntu 22.04)

Work in the Linux home folder (`~/roblox`), not under `/mnt/c`: worktrees and symlinks
are slow or broken on the Windows side.

```bash
sudo apt update                                        # stale package lists give 404s
sudo apt install -y python3-pip git unzip curl
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs                             # Node 22, with npm; not Ubuntu's Node 12
sudo npm install -g @anthropic-ai/claude-code
pip install pillow tomli
```

If you run as root, add `IS_SANDBOX=1` to `.env`, or Claude Code refuses to run the
generators unattended.

## Layout

| Path | What |
|---|---|
| `swarm/` | the harness: `pack`, `run`, `check`, `sheet`, `report`, `apply` |
| `providers.toml` | endpoints, model ids, prices, caps per provider |
| `targets/arpg-game/target.toml` | where the game is, its setup, which files are hidden from generators |
| `targets/arpg-game/effects/` | the effects job: new looks from the existing kinds (rows only), with briefs |
| `targets/arpg-game/kinds/` | the kinds job: new kinds of drawing, each a pure Luau module (drafted kinds); shares the effects briefs |
| `docs/kind-drafting/` | the game-side platform the kinds job needs, as a patch and a handoff note |
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

Keys live in `.env` at swarm-lab's root (gitignored), one `NAME=value` per line. Every
`python3 -m swarm ...` command reads it on start, so there's nothing to export. A
variable already set in your shell wins over the file, for a one-off override. Never put
a key in `providers.toml`, a pack, a log or the game repo.
