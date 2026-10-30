"""Loading the repo's settings: providers, targets, jobs and briefs."""

from __future__ import annotations

import os

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 (Ubuntu 22.04's): pip install tomli
    import tomli as tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_dotenv(path: Path | None = None) -> None:
    """Read KEY=value lines from swarm-lab's .env into the environment. A variable
    already set in the shell wins, so a one-off override still works. Blank lines and
    # comments are skipped; quotes around a value are stripped."""
    path = path or ROOT / ".env"
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.removeprefix("export ").strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        if key and value and key not in os.environ:
            os.environ[key] = value


load_dotenv()


def load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


@dataclass
class Provider:
    name: str
    runtime: str
    model: str
    key_env: str = ""
    base_url: str = ""
    small_model: str = ""
    price_in: float = 0.0
    price_cached: float = 0.0
    price_out: float = 0.0
    max_turns: int = 40
    timeout_s: int = 1500
    budget_tokens: int = 0
    command: list[str] = field(default_factory=list)  # runtime "exec": argv, for tests
    env: dict[str, str] = field(default_factory=dict)  # extra variables for the runtime
    peak: dict = field(default_factory=dict)  # time-of-day pricing windows (swarm/offpeak.py)

    def key(self) -> str:
        return os.environ.get(self.key_env, "") if self.key_env else ""

    def cost(self, usage: dict) -> float:
        fresh = usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
        cached = usage.get("cache_read_input_tokens", 0)
        out = usage.get("output_tokens", 0)
        return (fresh * self.price_in + cached * self.price_cached + out * self.price_out) / 1e6


def providers(path: Path | None = None) -> dict[str, Provider]:
    # SWARM_PROVIDERS points the tests (or a private setup) at another providers file.
    data = load_toml(path or Path(os.environ.get("SWARM_PROVIDERS", ROOT / "providers.toml")))
    return {name: Provider(name=name, **row) for name, row in data.items()}


@dataclass
class Target:
    name: str
    dir: Path
    repo: str
    ref: str
    setup: str = ""
    path: list[str] = field(default_factory=list)
    share: list[str] = field(default_factory=list)
    hide: list[str] = field(default_factory=list)

    def repo_path(self) -> Path | None:
        """The repo as a local path (relative paths are from swarm-lab's root), or None
        when it's a URL."""
        if "://" in self.repo or self.repo.startswith("git@"):
            return None
        p = Path(os.path.expanduser(self.repo))
        return p if p.is_absolute() else (ROOT / p).resolve()

    def env(self) -> dict[str, str]:
        env = dict(os.environ)
        extra = [os.path.expanduser(p) for p in self.path]
        if extra:
            env["PATH"] = os.pathsep.join(extra + [env.get("PATH", "")])
        return env


def target(name: str) -> Target:
    d = ROOT / "targets" / name
    data = load_toml(d / "target.toml")
    return Target(name=name, dir=d, **data)


@dataclass
class Job:
    name: str
    dir: Path
    data: dict

    @property
    def files(self) -> dict[str, dict]:
        return self.data.get("files", {})

    def rule(self, path: str, skill: str) -> dict | None:
        """The file rule a changed path falls under: an exact key, or a glob key (which
        may name the skill as {skill}), as in job.toml's [files]."""
        import fnmatch

        if path in self.files:
            return self.files[path]
        for key, spec in self.files.items():
            pat = key.replace("{skill_lower}", skill.lower()).replace("{skill}", skill)
            if path == pat or (any(c in key for c in "*?[") and fnmatch.fnmatchcase(path, pat)):
                return spec
        return None

    def directions(self, brief: dict | None = None) -> list[str]:
        # A brief may bring its own directions file (in the job's folder).
        name = (brief or {}).get("directions") or self.data.get("directions", "directions.txt")
        p = self.dir / name
        if not p.exists():
            return ["No set direction: make the look you think is best."]
        lines = [l.strip() for l in p.read_text().splitlines()]
        return [l for l in lines if l and not l.startswith("#")]

    def brief(self, name: str) -> dict:
        # Jobs may share another job's briefs (`briefs = "../effects/briefs"`).
        b = load_toml(self.dir / self.data.get("briefs", "briefs") / f"{name}.toml")
        b.setdefault("name", name)
        return b


def job(t: Target, name: str) -> Job:
    d = t.dir / name
    return Job(name=name, dir=d, data=load_toml(d / "job.toml"))


# Where a figure's files go in each worktree, relative to its root.
FIGURE_DIR = ".swarm/figure"


@dataclass
class Figure:
    """Who wears a set: guidance added to the pack after the brief, files copied into
    each worktree, and checks the filter runs after the job's specs
    (targets/<target>/figures/<name>/figure.toml)."""

    name: str
    dir: Path
    data: dict

    @property
    def values(self) -> dict:
        return self.data.get("values", {})

    def wt_dir(self) -> str:
        return f"{FIGURE_DIR}/{self.name}"

    def checks(self, skill: str) -> list[dict]:
        """The figure's checks as specs ({name, cmd}), their commands filled in."""
        fill = {**{k: str(v) for k, v in self.values.items()}, "skill": skill, "dir": self.wt_dir()}
        return [{"name": f"{self.name}:{c['name']}", "cmd": c["cmd"].format(**fill)} for c in self.data.get("checks", [])]

    def guide(self, skill: str) -> str:
        from string import Template

        checks = self.checks(skill)
        text = (self.dir / self.data.get("guide", "guide.md")).read_text(encoding="utf-8")
        return Template(text).substitute(**self.values, figure_cmd=checks[0]["cmd"] if checks else "")


def figure(t: Target, name: str) -> Figure:
    d = t.dir / "figures" / name
    if not (d / "figure.toml").exists():
        known = sorted(p.name for p in (t.dir / "figures").glob("*") if (p / "figure.toml").exists())
        raise KeyError(f"no figure {name!r} in {t.name}; known: {', '.join(known) or 'none'}")
    return Figure(name=name, dir=d, data=load_toml(d / "figure.toml"))


def figures(t: Target, j: Job, brief: dict, override: str | None = None) -> list[Figure]:
    """The figures a run uses: the command line's, else the brief's, else the job's. Each
    may be one name, a comma list or a list; "none" means no figure."""
    for spec in (override, brief.get("figure"), j.data.get("figure")):
        if spec is None:
            continue
        names = [n.strip() for n in (spec.split(",") if isinstance(spec, str) else spec) if n.strip()]
        if names == ["none"]:
            return []
        out = [figure(t, n) for n in names]
        for f in out:
            fams = f.data.get("families")
            if fams and brief.get("family") not in fams:
                raise ValueError(f"figure {f.name!r} is for {', '.join(fams)} briefs, not {brief.get('family')!r}")
        return out
    return []
