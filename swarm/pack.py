"""Build a job's context pack for one brief from the game repo's current files.

The pack is identical for every generator in a run (so providers cache it); each
generator's direction goes in a separate file. Building fails loudly when a file, row
or marker the job quotes is gone, which is the cue to update the job.
"""

from __future__ import annotations

from pathlib import Path
from string import Template

from . import luarows
from .config import Job

MODES = {
    "owned_row": "only the `{skill}` row may change, or be added if missing",
    "add_rows": "add new rows only; every existing row stays exactly as it is",
}


def _rgb(c) -> str:
    return ",".join(str(int(v)) for v in c)


def _block(lang: str, text: str) -> str:
    return f"```{lang}\n{text.rstrip()}\n```"


def render_commands(brief: dict) -> tuple[str, str]:
    """(reference commands, your-look commands) for the brief's family."""
    skill, color = brief["skill"], _rgb(brief["color"])
    current = brief.get("current_look", "")
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


def build(job: Job, brief: dict, repo: Path) -> str:
    skill = brief["skill"]
    read = lambda rel: (repo / rel).read_text(encoding="utf-8")  # noqa: E731

    files = "\n".join(
        f"   - `{rel}`: {MODES[spec['mode']].format(skill=skill)}" for rel, spec in job.files.items()
    )

    current = []
    for rel, spec in job.files.items():
        src = read(rel)
        names = [skill] if spec["mode"] == "owned_row" else []
        if brief.get("current_look") and spec["mode"] == "add_rows":
            names.append(brief["current_look"])
        for name in names:
            try:
                current.append(f"`{rel}`, row `{name}`:\n\n" + _block("lua", luarows.get(src, name)))
            except KeyError:
                pass  # not every file holds every name; checked below
    if not current:
        raise KeyError(f"none of the job's files has a row for {skill} or its current look")

    examples = []
    for ex in job.data.get("examples", []):
        examples.append(f"`{ex['file']}`, row `{ex['row']}`:\n\n" + _block("lua", luarows.get(read(ex["file"]), ex["row"])))

    kinds_spec = job.data.get("kinds", {}).get(brief["family"])
    if kinds_spec is None:
        raise KeyError(f"job has no kinds for family {brief['family']!r}")
    kinds = _block("lua", luarows.between(read(kinds_spec["file"]), kinds_spec["from"], kinds_spec["to"]))

    rules = []
    for rel in job.data.get("rules", []):
        text = read(rel).strip()
        # Demote the file's headings so they sit under "The rules".
        text = "\n".join(("##" + l) if l.startswith("#") else l for l in text.splitlines())
        rules.append(f"### From `{rel}`\n\n{text}")

    specs = "\n".join(s["cmd"] for s in job.data.get("specs", []))
    ref_cmds, render_cmds = render_commands(brief)

    template = Template((job.dir / job.data.get("template", "pack.md")).read_text(encoding="utf-8"))
    return template.substitute(
        skill=skill,
        family=brief["family"],
        brief=brief["brief"].strip(),
        current_look=brief.get("current_look", "none"),
        color=_rgb(brief["color"]),
        files_section=files,
        current_rows="\n\n".join(current),
        examples="\n\n".join(examples),
        kinds=kinds,
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
