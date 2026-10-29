"""Tile the survivors' renders into one blind contact sheet, and write the
orchestrator's selection prompt.

Each survivor gets a random letter. The letter-to-generator key goes in key.json,
which the selector is told not to open, so it judges the looks and not the models.
Writes runs/<run>/sheet.png, sheet-<letter>.png per survivor (full size, for a closer
look), key.json and select.md.
"""

from __future__ import annotations

import json
import random
import string
from pathlib import Path
from string import Template

from . import config

# arpg-game's previews are wide strips (five moments and a side view per power row),
# so tiles are wide and two to a row; narrower and the panels stop being readable.
TILE_W = 900
LABEL_H = 44
COLS = 2
BG = (18, 20, 26)
FG = (235, 235, 240)


def _font(size: int):
    from PIL import ImageFont

    for name in ("DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _tile(img_path: Path, label: str):
    from PIL import Image, ImageDraw

    im = Image.open(img_path).convert("RGB")
    h = round(im.height * TILE_W / im.width)
    im = im.resize((TILE_W, h))
    tile = Image.new("RGB", (TILE_W, h + LABEL_H), BG)
    tile.paste(im, (0, LABEL_H))
    ImageDraw.Draw(tile).text((12, 8), label, fill=FG, font=_font(26))
    return tile


def _grid(tiles):
    from PIL import Image

    cols = min(COLS, len(tiles))
    rows = [tiles[i : i + cols] for i in range(0, len(tiles), cols)]
    row_h = [max(t.height for t in r) for r in rows]
    sheet = Image.new("RGB", (cols * TILE_W + (cols + 1) * 8, sum(row_h) + (len(rows) + 1) * 8), BG)
    y = 8
    for r, h in zip(rows, row_h):
        x = 8
        for t in r:
            sheet.paste(t, (x, y))
            x += TILE_W + 8
        y += h + 8
    return sheet


def sheet(run_dir: Path, seed: int | None = None) -> Path | None:
    meta = json.loads((run_dir / "meta.json").read_text())
    checked = json.loads((run_dir / "check.json").read_text())
    survivors = [g for g in checked["generators"] if g["survived"]]
    if not survivors:
        print("  no survivors: nothing to tile")
        return None

    rng = random.Random(seed if seed is not None else meta["run"] + "-sheet")
    letters = list(string.ascii_uppercase[: len(survivors)])
    rng.shuffle(letters)
    key, tiles, entries = {}, [], []

    # The references first, as the run rendered them from the brief (run.render_reference):
    # the benchmark, then the look being replaced.
    for ref in sorted((run_dir / "base" / ".swarm" / "out").glob("ref-*.png")):
        tiles.append(_tile(ref, f"REF  {ref.stem[4:]}"))
        entries.append(f"- **REF {ref.stem[4:]}**: `{ref.relative_to(run_dir)}` (a reference, not a candidate)")

    for letter, g in sorted(zip(letters, survivors)):
        wt = run_dir / "gens" / g["gid"]
        renders = [wt / r for r in g["manifest"]["renders"]]
        key[letter] = {"gid": g["gid"], "provider": g["provider"]}
        tiles.append(_tile(renders[0], letter))
        _grid([_tile(r, f"{letter}  {r.name}") for r in renders]).save(run_dir / f"sheet-{letter}.png")
        entries.append(
            f"- **{letter}**: {g['manifest']['intent']} Full renders: `sheet-{letter}.png`; "
            f"rows: `gens/{g['gid']}/.swarm/patch.diff`"
        )

    out = run_dir / "sheet.png"
    _grid(tiles).save(out)
    (run_dir / "key.json").write_text(json.dumps(key, indent=2))

    prompt = Template((config.ROOT / "prompts" / "select.md").read_text())
    (run_dir / "select.md").write_text(
        prompt.substitute(
            skill=meta["skill"], family=meta["family"], run=meta["run"], count=len(survivors),
            candidates="\n".join(entries), pack=f"runs/{meta['run']}/pack.md",
        )
    )
    print(f"  sheet: {out.relative_to(config.ROOT)} ({len(survivors)} candidates)")
    return out
