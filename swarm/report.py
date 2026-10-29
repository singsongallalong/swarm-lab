"""Summarise a run by provider and add it to the experiment ledger.

Writes runs/<run>/report.md, and appends one line per provider to
results/ledger.csv (committed: the experiment's record across runs). Run it again
after selection.json exists to record the picks; a rerun replaces the run's lines.
"""

from __future__ import annotations

import csv
import json
import statistics
from pathlib import Path

from . import config

FIELDS = ["run", "skill", "provider", "model", "gens", "finished", "survived", "picked",
          "tokens", "cost_usd", "median_s", "top_reject", "playtest"]


def report(run_dir: Path) -> list[dict]:
    meta = json.loads((run_dir / "meta.json").read_text())
    gens = {g["gid"]: g for g in json.loads((run_dir / "generators.json").read_text())} if (run_dir / "generators.json").exists() else {}
    checked = {g["gid"]: g for g in json.loads((run_dir / "check.json").read_text())["generators"]} if (run_dir / "check.json").exists() else {}
    key = json.loads((run_dir / "key.json").read_text()) if (run_dir / "key.json").exists() else {}
    sel = json.loads((run_dir / "selection.json").read_text()) if (run_dir / "selection.json").exists() else {}
    picked_gids = {key[l]["gid"] for l in sel.get("picked", []) if l in key}

    rows = []
    for prov in sorted({g["provider"] for g in meta["generators"]}):
        mine = [g for g in meta["generators"] if g["provider"] == prov]
        recs = [gens.get(g["gid"], {}) for g in mine]
        checks = [checked.get(g["gid"], {}) for g in mine]
        secs = [r["seconds"] for r in recs if "seconds" in r]
        rejects = [c["reason"] for c in checks if c and not c.get("survived")]
        top = max(set(rejects), key=rejects.count) if rejects else ""
        rows.append({
            "run": meta["run"], "skill": meta["skill"], "provider": prov, "model": mine[0]["model"],
            "gens": len(mine),
            "finished": sum(r.get("status") == "finished" for r in recs),
            "survived": sum(bool(c.get("survived")) for c in checks),
            "picked": sum(g["gid"] in picked_gids for g in mine),
            "tokens": sum(r.get("tokens", 0) for r in recs),
            "cost_usd": round(sum(r.get("cost_usd", 0.0) for r in recs), 4),
            "median_s": round(statistics.median(secs), 1) if secs else "",
            "top_reject": top,
            "playtest": "",
        })

    lines = [f"# Run {meta['run']}: {meta['skill']} ({meta['family']})", "",
             f"Base `{meta['base'][:10]}`, started {meta['started']}.", "",
             "| Provider | Model | Gens | Finished | Survived | Picked | Tokens | Cost | Median s | Most common rejection |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['provider']} | {r['model']} | {r['gens']} | {r['finished']} | {r['survived']} | {r['picked']} | "
                     f"{r['tokens']:,} | ${r['cost_usd']:.2f} | {r['median_s']} | {r['top_reject'] or '—'} |")
    if sel:
        lines += ["", "## Selection", ""] + [f"- **{l}** ({key.get(l, {}).get('provider', '?')}): {sel['reasons'].get(l, '')}" for l in sel.get("picked", [])]
    (run_dir / "report.md").write_text("\n".join(lines) + "\n")

    ledger = config.ROOT / "results" / "ledger.csv"
    ledger.parent.mkdir(exist_ok=True)
    old = []
    if ledger.exists():
        with open(ledger, newline="") as f:
            prior = list(csv.DictReader(f))
        old = [r for r in prior if r["run"] != meta["run"]]
        # Keep playtest verdicts already written by hand for this run.
        verdicts = {r["provider"]: r.get("playtest", "") for r in prior if r["run"] == meta["run"]}
        for r in rows:
            r["playtest"] = verdicts.get(r["provider"], "")
    with open(ledger, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(old + rows)
    print("\n".join(lines[4:]))
    return rows
