"""End to end against a fake game and fake generators: pack, run, check, sheet,
report, apply. Calls no model and needs no keys.

    python3 tests/test_end_to_end.py
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from swarm import apply, check, config, pack, report, run, sheet  # noqa: E402

FIX = ROOT / "tests" / "fixture"
TARGET = "_e2e"


def git(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def setup(tmp: Path) -> Path:
    game = tmp / "game"
    shutil.copytree(FIX / "game", game)
    os.chmod(FIX / "bin" / "lune", 0o755)
    git("init", "-q", "-b", "main", cwd=game)
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qam", "init", "--allow-empty", cwd=game)
    git("add", "-A", cwd=game)
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "fixture", cwd=game)

    tdir = ROOT / "targets" / TARGET
    shutil.rmtree(tdir, ignore_errors=True)
    tdir.mkdir(parents=True)
    (tdir / "target.toml").write_text(
        f'repo = "{game}"\nref = "main"\nsetup = ""\npath = ["{FIX / "bin"}"]\nshare = []\nhide = ["CLAUDE.md", ".claude"]\n'
    )
    shutil.copytree(ROOT / "targets" / "arpg-game" / "effects", tdir / "effects")
    # A figure whose check rejects any look that fires particles (only g04's does).
    fig = tdir / "figures" / "plain"
    fig.mkdir(parents=True)
    (fig / "figure.toml").write_text(
        'families = ["area"]\nguide = "guide.md"\nfiles = ["noburst.py"]\n[values]\nlimit = 0\n'
        '[[checks]]\nname = "noburst"\ncmd = "python3 {dir}/noburst.py {skill} {limit}"\n'
    )
    (fig / "guide.md").write_text("## The figure: plain\n\nAt most $limit bursts. Check with:\n\n```\n$figure_cmd\n```\n")
    (fig / "noburst.py").write_text(
        "import pathlib, subprocess, sys\n"
        "rel = 'src/shared/data/DrawnEffects.luau'\n"
        "before = subprocess.run(['git', 'show', 'HEAD:' + rel], capture_output=True, text=True).stdout\n"
        "added = pathlib.Path(rel).read_text().count('emitter =') - before.count('emitter =')\n"
        "sys.exit(1 if added > int(sys.argv[2]) else 0)\n"
    )

    provs = tmp / "providers.toml"
    provs.write_text(
        '[fake]\nruntime = "exec"\nmodel = "fake-1"\n'
        f'command = ["{sys.executable}", "{ROOT / "tests" / "fake_generator.py"}"]\n'
        "price_in = 0.30\nprice_cached = 0.03\nprice_out = 1.20\ntimeout_s = 60\n"
    )
    os.environ["SWARM_PROVIDERS"] = str(provs)
    return game


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="swarm-e2e-"))
    run_dir = ROOT / "runs" / "e2e"
    shutil.rmtree(run_dir, ignore_errors=True)
    ledger = ROOT / "results" / "ledger.csv"
    ledger_before = ledger.read_text() if ledger.exists() else None
    try:
        game = setup(tmp)
        t = config.target(TARGET)
        j = config.job(t, "effects")

        # The pack builds from the fixture, quotes the rules, and leaves no placeholder.
        text = pack.build(j, j.brief("ColdSnap"), game)
        assert "SE6" in text and "HeavedRocks" in text and "SweepWave" in text, "pack is missing quoted content"
        assert "$" not in text.replace("${", ""), "pack left a $placeholder"
        flight = pack.build(j, j.brief("Sleet"), game)
        assert "flightpreview" in flight and "-- Flight kinds" in flight

        # Particles: the format, the textures, and an honest line about whether renders
        # draw them, read from the game's own area preview.
        assert "## Particles" in text and "squash: Curve?" in text and "smoke_main.dds" in text, "particles section incomplete"
        assert "rbxassetid://124158244676542" in text, "painted textures missing"
        assert "named `ColdSnap...`" in text, "skill name not filled in"
        assert "Renders don't draw particles yet" in text
        assert "### What particles are for" in text and "### The game's burst rule, quoted" in text
        assert "function AreaBursts.list" in text, "burst rule not quoted"
        assert "end at 1.2 studs on screen: specks" in text, "worked example wrong"
        preview = game / "scripts" / "areapreview.luau"
        preview.parent.mkdir(exist_ok=True)
        preview.write_text('local Emitter = require("./motionlab/Emitter")\n')
        assert "Renders draw particle bursts" in pack.build(j, j.brief("ColdSnap"), game), "render detection missed"
        preview.unlink()

        run.run(TARGET, "effects", "ColdSnap", "fake:7", run_id="e2e", concurrency=3)
        res = check.check(run_dir)
        by = {g["gid"]: g for g in res["generators"]}
        assert by["g00"]["survived"] and by["g04"]["survived"] and by["g06"]["survived"], res
        assert by["g01"]["reason"].startswith("touched README.md"), by["g01"]
        assert "changed the existing row HeavedRocks" in by["g02"]["reason"], by["g02"]
        assert by["g03"]["reason"] == "no manifest", by["g03"]
        assert by["g05"]["reason"] == "spec DrawnEffects failed", by["g05"]

        # Counts come from the harness's own render: only g04 fires particles.
        assert by["g04"]["manifest"]["counts"] == {"parts": 21, "particles": 48}, by["g04"]["manifest"].get("counts")
        assert by["g00"]["manifest"]["counts"]["particles"] == 0

        assert sheet.sheet(run_dir).exists()
        assert "48 particles" in (run_dir / "select.md").read_text()
        key = json.loads((run_dir / "key.json").read_text())
        assert sorted(key) == ["A", "B", "C"]
        assert "Don't open `key.json`" in (run_dir / "select.md").read_text()

        # A figure: its guide follows the brief, demoted under it; its check joins the specs.
        figs = config.figures(t, j, j.brief("ColdSnap"), "plain")
        ftext = pack.build(j, j.brief("ColdSnap"), game, figs)
        assert "### The figure: plain" in ftext and "At most 0 bursts" in ftext, "figure guide missing"
        assert ftext.count("python3 .swarm/figure/plain/noburst.py ColdSnap 0") == 2, "figure check not in guide and specs"
        assert config.figures(t, j, {**j.brief("ColdSnap"), "figure": "plain"}, "none") == [], "none didn't win"
        try:
            config.figures(t, j, j.brief("ColdSnap"), "nosuch")
            raise AssertionError("unknown figure accepted")
        except KeyError:
            pass
        fig_dir = ROOT / "runs" / "e2e-fig"
        shutil.rmtree(fig_dir, ignore_errors=True)
        try:
            run.run(TARGET, "effects", "ColdSnap", "fake:5", run_id="e2e-fig", concurrency=3, figure="plain")
            assert json.loads((fig_dir / "meta.json").read_text())["figures"] == ["plain"]
            assert (fig_dir / "gens" / "g04" / ".swarm" / "figure" / "plain" / "noburst.py").exists()
            fby = {g["gid"]: g for g in check.check(fig_dir)["generators"]}
            assert fby["g00"]["survived"], fby["g00"]
            assert fby["g04"]["reason"] == "spec plain:noburst failed", fby["g04"]
        finally:
            shutil.rmtree(fig_dir, ignore_errors=True)

        letter = sorted(key)[0]
        (run_dir / "selection.json").write_text(json.dumps({"picked": [letter], "reasons": {letter: "test"}}))
        rows = report.report(run_dir)
        assert rows[0]["survived"] == 3 and rows[0]["picked"] == 1 and rows[0]["cost_usd"] > 0, rows
        assert rows[0]["with_particles"] == 1, rows

        apply.apply(run_dir, letter)
        branch = subprocess.run(["git", "branch", "--show-current"], cwd=game, capture_output=True, text=True).stdout.strip()
        assert branch == f"swarm/e2e-{letter}", branch
        diff = subprocess.run(["git", "diff", "--name-only"], cwd=game, capture_output=True, text=True).stdout.split()
        assert sorted(diff) == ["src/shared/data/DrawnEffects.luau", "src/shared/data/SkillVisuals.luau"], diff
        print("\nend-to-end: all checks passed")
    finally:
        shutil.rmtree(ROOT / "targets" / TARGET, ignore_errors=True)
        shutil.rmtree(run_dir, ignore_errors=True)
        shutil.rmtree(tmp, ignore_errors=True)
        if ledger_before is None:
            ledger.unlink(missing_ok=True)
        else:
            ledger.write_text(ledger_before)


if __name__ == "__main__":
    main()
