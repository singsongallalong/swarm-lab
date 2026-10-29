"""Loading the repo's settings: providers, targets, jobs and briefs."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


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

    def directions(self) -> list[str]:
        p = self.dir / self.data.get("directions", "directions.txt")
        if not p.exists():
            return ["No set direction: make the look you think is best."]
        lines = [l.strip() for l in p.read_text().splitlines()]
        return [l for l in lines if l and not l.startswith("#")]

    def brief(self, name: str) -> dict:
        b = load_toml(self.dir / "briefs" / f"{name}.toml")
        b.setdefault("name", name)
        return b


def job(t: Target, name: str) -> Job:
    d = t.dir / name
    return Job(name=name, dir=d, data=load_toml(d / "job.toml"))
