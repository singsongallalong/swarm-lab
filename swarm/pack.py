"""Build a job's context pack for one brief from the game repo's current files.

The pack is identical for every generator in a run (so providers cache it); each
generator's direction goes in a separate file. Building fails loudly when a file, row
or marker the job quotes is gone, which is the cue to update the job.
"""

from __future__ import annotations

import re
from pathlib import Path
from string import Template

from . import luarows
from .config import Figure, Job

MODES = {
    "owned_row": "only the `{skill}` row may change, or be added if missing",
    "add_rows": "add new rows only, each named starting with `{prefix}`; every existing row stays exactly as it is",
    "new_file": "a new file of your own (its name must match this pattern); never an existing one",
    "add_lines": "add lines only, each one an entry for your own module; change nothing else",
}


def _rgb(c) -> str:
    return ",".join(str(int(v)) for v in c)


def _block(lang: str, text: str) -> str:
    return f"```{lang}\n{text.rstrip()}\n```"


def _fill(template: str, skill: str) -> str:
    return template.replace("{skill_lower}", skill.lower()).replace("{skill}", skill)


# Placeholders a family's render commands may use, each filled from the manifest's
# field of that name (<YourLook> from `look`, as ever).
PLACEHOLDERS = {"<YourLook>": "look", "<Tileset>": "tileset", "<SetPiece>": "setpiece", "<Sculpts>": "sculpts"}


def fill_placeholders(cmd: str, manifest: dict) -> str:
    for ph, key in PLACEHOLDERS.items():
        if ph in cmd:
            val = manifest.get(key)
            if isinstance(val, list):
                val = ",".join(val)
            cmd = cmd.replace(ph, str(val or ""))
    return cmd


def render_commands(brief: dict) -> tuple[str, str]:
    """(reference commands, your-look commands) for the brief's family."""
    skill, color = brief["skill"], _rgb(brief.get("color", (0, 0, 0)))
    current = brief.get("current_look", "")
    if brief["family"] == "armour":
        # A whole set worn at once, as armourpreview draws a comma list: the set's
        # looks replace <YourLook>, in slot order. The reference is every family's set.
        ref = ["lune run scripts/armourpreview sets .swarm/out/ref-sets.png"]
        mine = [
            "lune run scripts/armourpreview <YourLook> .swarm/out/armour-set-r1.png",
            "lune run scripts/armourpreview <YourLook> .swarm/out/armour-set-close-r1.png close",
            "lune run scripts/armourpreview <YourLook> .swarm/out/armour-set-fit-r1.png fit",
        ]
        return "\n".join(ref), "\n".join(mine)
    if brief["family"] == "map":
        # A drafted map's layout, dressed in its own tileset: the whole map over three
        # seeds, and its first landmark up close. The reference is the moor's own layout
        # in the same look, the map a draft must not merely repaint.
        ref = ["lune run scripts/dresspreview whole .swarm/out/ref-whole-moor-moonwell.png 2 1 tileset=moonwell"]
        mine = [
            "lune run scripts/dresspreview whole .swarm/out/map-whole-r1.png 3 1 layout=<YourLook>",
            "lune run scripts/dresspreview landmark .swarm/out/map-landmark-r1.png 2 1 layout=<YourLook>",
        ]
        return "\n".join(ref), "\n".join(mine)
    if brief["family"] == "zone":
        # A whole area's look: its tileset dressing the moor's layouts (dresspreview's
        # tileset=), its pieces, its props and its set piece. The reference is the
        # Ashfields, the newest area, in the same views.
        ref = [
            "lune run scripts/dresspreview whole .swarm/out/ref-whole-field2.png 1 1 tileset=field2",
            "lune run scripts/dresspreview pool .swarm/out/ref-pool-field2.png 2 1 tileset=field2",
        ]
        mine = [
            "lune run scripts/dresspreview whole .swarm/out/zone-whole-r1.png 1 1 tileset=<Tileset>",
            "lune run scripts/dresspreview pool .swarm/out/zone-pool-r1.png 2 1 tileset=<Tileset>",
            "lune run scripts/dresspreview ruin .swarm/out/zone-ruin-r1.png 2 1 tileset=<Tileset>",
            "lune run scripts/tilesetpreview <Tileset> .swarm/out/zone-tileset-r1.png",
            "lune run scripts/tilesetpreview <Tileset> .swarm/out/zone-tileset-eye-r1.png eye",
            "lune run scripts/sculptpreview <Sculpts> .swarm/out/zone-sculpts-r1.png 3",
            "lune run scripts/setpiecepreview <SetPiece> .swarm/out/zone-setpiece-r1.png",
        ]
        return "\n".join(ref), "\n".join(mine)
    if brief["family"] == "area":
        shape = f"angle={brief['angle']} radius={brief['radius']}"
        ref = [
            f"lune run scripts/areapreview HeavedRocks .swarm/out/ref-HeavedRocks.png powers=0,4,8 color=255,220,120 {shape}",
        ]
        if current:
            ref.append(
                f"lune run scripts/areapreview {current} .swarm/out/ref-{current}-as-{skill}.png powers=0,4,8 color={color} {shape}"
            )
        mine = [
            f"lune run scripts/areapreview <YourLook> .swarm/out/area-<YourLook>-r1.png powers=0,4,8 color={color} {shape}",
        ]
    elif brief["family"] == "flight":
        volley = f" {brief['volley']}" if brief.get("volley") else ""
        ref = []
        if current:
            ref.append(
                f"lune run scripts/flightpreview {current} .swarm/out/ref-{current}-as-{skill}.png powers=0,4,8 color={color}{volley}"
            )
        ref.append("lune run scripts/flightpreview SparkBolt .swarm/out/ref-SparkBolt.png powers=0,4,8 color=150,190,255")
        mine = [
            f"lune run scripts/flightpreview <YourLook> .swarm/out/flight-<YourLook>-r1.png powers=0,4,8 color={color}{volley}",
        ]
    else:
        raise ValueError(f"unknown family {brief['family']!r}")
    note = "\n# If you change the colour in your SkillVisuals row, pass the new one in color=."
    return "\n".join(ref), "\n".join(mine) + note


def particles_render(job: Job, repo: Path) -> bool:
    spec = job.data.get("particles", {})
    f = repo / spec.get("render_check_file", "")
    return bool(spec.get("render_check")) and f.is_file() and re.search(spec["render_check"], f.read_text(encoding="utf-8")) is not None


def burst_scales(bursts_src: str) -> dict[str, float]:
    block = bursts_src.split("SCALE = {", 1)[1].split("}", 1)[0]
    return {k: float(v) for k, v in re.findall(r"(\w+)\s*=\s*([\d.]+)", block)}


def end_size(row_text: str) -> float:
    """The last point of an Emitters row's size curve: its size at the end of a life."""
    m = re.search(r"\bsize\s*=\s*\{(.*?)\}\s*,\s*\n", row_text, re.S)
    points = re.findall(r"\{\s*[\d.]+\s*,\s*([\d.]+)\s*\}", m.group(1)) if m else []
    if not points:
        raise ValueError("no size curve")
    return float(points[-1])


def bursts_rule(spec: dict, bursts_src: str, emitters_src: str) -> str:
    """The game's own burst rule, quoted, with a worked size example computed from the
    current rows so it stays true when the game changes."""
    start = bursts_src.find(spec["bursts_from"])
    fn = bursts_src.find(spec["bursts_fn"], start)
    end = bursts_src.find("\nend\n", fn)
    if start < 0 or fn < 0 or end < 0:
        raise KeyError("the burst rule's markers aren't in " + spec["bursts_file"])
    quoted = bursts_src[bursts_src.rfind("\n", 0, start) + 1 : end + 5]
    text = (
        "### The game's burst rule, quoted\n\n"
        f"From `{spec['bursts_file']}`, which both the game and the preview read, so a burst "
        "the preview shows is the burst the game fires. `scale` multiplies the row's sizes "
        "and speeds.\n\n" + _block("lua", quoted)
    )
    row, kind = spec.get("worked_row"), spec.get("worked_kind")
    if row and kind:
        scale = burst_scales(bursts_src).get(kind)
        size = end_size(luarows.get(emitters_src, row))
        if scale is not None:
            text += (
                f"\n\n**Worked example:** `{row}`'s puffs end at {size:g} studs. In a {kind} look "
                f"they fire at scale {scale:g}, so they end at {size * scale:g} studs on screen: "
                f"{'specks' if size * scale < 2 else 'readable'} by the measurements above. "
                f"To end at about 2.5 studs in a {kind}, a row's last size point needs about "
                f"{2.5 / scale:g}."
            )
    return text


def particles_section(job: Job, repo: Path, skill: str) -> str:
    spec = job.data.get("particles")
    if not spec:
        return "Particles aren't part of this job."
    read = lambda rel: (repo / rel).read_text(encoding="utf-8")  # noqa: E731
    out = []
    if particles_render(job, repo):
        out.append(
            "**Renders draw particle bursts** as soft sprites, simulated from the row. Judge "
            "their timing, reach and spread from the render; the texture itself is only "
            "approximated (a procedural sprite), so pick it by its description below."
        )
    else:
        out.append(
            "**Renders don't draw particles yet:** a burst shows only as thin rings on the "
            "ground marking where and how wide it goes. You can still use particles, but "
            "you'll be judging them from those rings and the row's numbers alone."
        )
    out.append(
        "An area look fires particles only through its own `emitter` field (and a Rocks "
        "look's `burst`), which names an Emitters row. Give your look its own row (named "
        "`{skill}...`) rather than reusing `SlamDust`, so its colour, size and timing are "
        "this skill's."
    )
    if spec.get("guide"):
        out.append((job.dir / spec["guide"]).read_text(encoding="utf-8").strip())
    src = read(spec["file"])
    if spec.get("bursts_file"):
        out.append(bursts_rule(spec, read(spec["bursts_file"]), src))
    fmt = luarows.between(src, spec["from"], spec["to"])
    if fmt.count("{") > fmt.count("}"):  # the end marker sits on the type's last field
        fmt = fmt.rstrip() + "\n}"
    out.append("The row format:\n\n" + _block("lua", fmt))

    textures = sorted(set(re.findall(r'texture\s*=\s*"([^"]+)"', src)))
    lines = [f"- `{t}` (Roblox built-in, already used by a skill effect)" for t in textures]
    if spec.get("painted") and (repo / spec["painted"]).is_file():
        painted = read(spec["painted"])
        for name, about, image in re.findall(
            r'^\t(\w+)\s*=\s*\{\s*\n\s*about\s*=\s*"([^"]+)".*?image\s*=\s*"([^"]+)"', painted, flags=re.M | re.S
        ):
            lines.append(f"- `{image}`: {name}, our own painting: {about}")
    out.append(
        "Textures you may use (pick one of these, never a new id). The art direction prefers "
        "our painted ones over Roblox defaults (SE11), and every one is greyscale, tinted by "
        "the row's `color`:\n\n" + "\n".join(lines)
        + "\n\nIf the look truly needs a texture that doesn't exist yet (a frost crystal, "
        "say), use the closest one here and describe the one you'd want in the manifest's "
        "`requests`."
    )
    ex = [f"Row `{n}`:\n\n" + _block("lua", luarows.get(src, n)) for n in spec.get("examples", []) if n in luarows.top_rows(src)]
    out.append("Examples, chosen to differ:\n\n" + "\n\n".join(ex))
    return "\n\n".join(out).replace("{skill}", skill)


def api(src: str, prefix: str) -> str:
    """Every `function <prefix>...` signature in a module, with the comment lines
    directly above it: a module's API without its bodies."""
    lines = src.splitlines()
    out = []
    for i, line in enumerate(lines):
        if line.startswith(f"function {prefix}"):
            k = i
            while k > 0 and lines[k - 1].startswith("--"):
                k -= 1
            out.extend(lines[k : i + 1])
            out.append("")
    if not out:
        raise KeyError(f"no functions starting {prefix}")
    return "\n".join(out).rstrip()


def quote(spec: dict, read) -> str:
    """One [quotes.<name>] entry of job.toml: a whole file, a span between markers,
    one row, or a module's API."""
    src = read(spec["file"])
    if "row" in spec:
        text = luarows.get(src, spec["row"])
    elif "api" in spec:
        text = api(src, spec["api"])
    elif "from" in spec:
        text = luarows.between(src, spec["from"], spec["to"])
    else:
        text = src
    head = f"From `{spec['file']}`" + (f", {spec['note']}" if spec.get("note") else "") + ":\n\n"
    return head + _block("lua", text)


def build(job: Job, brief: dict, repo: Path, figures: list[Figure] | tuple = ()) -> str:
    skill = brief["skill"]
    read = lambda rel: (repo / rel).read_text(encoding="utf-8")  # noqa: E731

    files = "\n".join(
        f"   - `{_fill(rel, skill)}`: {MODES[spec['mode']].format(skill=skill, prefix=_fill(spec.get('prefix', '{skill}'), skill))}"
        for rel, spec in job.files.items()
    )

    current = []
    for rel, spec in job.files.items():
        if spec["mode"] not in ("owned_row", "add_rows"):
            continue  # new files and registries have no current rows to show
        src = read(rel)
        names = [skill] if spec["mode"] == "owned_row" else []
        if brief.get("current_look") and spec["mode"] == "add_rows":
            names.append(brief["current_look"])
        for name in names:
            try:
                current.append(f"`{rel}`, row `{name}`:\n\n" + _block("lua", luarows.get(src, name)))
            except KeyError:
                pass  # not every file holds every name; checked below
    # A row to show is expected when the job owns one, or the brief names a current look;
    # a job that only adds new rows (zones) has none.
    wants = any(spec["mode"] == "owned_row" for spec in job.files.values()) or (
        brief.get("current_look") and any(spec["mode"] == "add_rows" for spec in job.files.values()))
    if not current and wants:
        raise KeyError(f"none of the job's files has a row for {skill} or its current look")

    examples = []
    for ex in job.data.get("examples", []):
        examples.append(f"`{ex['file']}`, row `{ex['row']}`:\n\n" + _block("lua", luarows.get(read(ex["file"]), ex["row"])))

    kinds_spec = job.data.get("kinds", {}).get(brief["family"])
    if kinds_spec is None and "kinds" in job.data:
        raise KeyError(f"job has no kinds for family {brief['family']!r}")
    kinds = _block("lua", luarows.between(read(kinds_spec["file"]), kinds_spec["from"], kinds_spec["to"])) if kinds_spec else ""

    rules = []
    for rel in job.data.get("rules", []):
        text = read(rel).strip()
        # Demote the file's headings so they sit under "The rules".
        text = "\n".join(("##" + l) if l.startswith("#") else l for l in text.splitlines())
        rules.append(f"### From `{rel}`\n\n{text}")

    specs = "\n".join(s["cmd"] for s in job.data.get("specs", []))
    # A figure's guidance follows the brief, and its checks run with the job's.
    figure_checks = [c["cmd"] for f in figures for c in f.checks(skill)]
    if figure_checks:
        specs += "\n" + "\n".join(figure_checks)
    brief_text = brief["brief"].strip()
    for f in figures:
        # Demoted a level, so its headings sit under "The brief".
        guide = f.guide(skill).strip().splitlines()
        brief_text += "\n\n" + "\n".join(("#" + l) if l.startswith("#") else l for l in guide)
    ref_cmds, render_cmds = render_commands(brief)

    quotes = {name: quote(spec, read) for name, spec in job.data.get("quotes", {}).items()}

    template = Template((job.dir / job.data.get("template", "pack.md")).read_text(encoding="utf-8"))
    return template.substitute(
        **quotes,
        skill=skill,
        skill_lower=skill.lower(),
        family=brief["family"],
        brief=brief_text,
        current_look=brief.get("current_look", "none"),
        color=_rgb(brief.get("color", (0, 0, 0))),
        files_section=files,
        current_rows="\n\n".join(current),
        examples="\n\n".join(examples),
        kinds=kinds,
        particles=particles_section(job, repo, skill) if brief["family"] == "area" else
        "Flight looks don't fire particles; this section is for area looks only.",
        rules="\n\n".join(rules),
        ref_cmds=ref_cmds,
        render_cmds=render_cmds,
        spec_cmds=specs,
    )


def direction_file(direction: str) -> str:
    return (
        "# Your direction\n\n"
        f"{direction}\n\n"
        "This is where you start, not a rule: the pack's rules still win, and if the "
        "direction can't make a good look for this skill, bend it.\n"
    )
