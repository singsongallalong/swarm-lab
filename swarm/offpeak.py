"""DeepSeek's time-of-day pricing: when a run is cheap.

Since 2026-08-17 (00:00 UTC+8) DeepSeek bills V4 models at full price only in its weekday
peak, 09:00-12:00 and 14:00-18:00 Beijing time (01:00-04:00 and 06:00-10:00 UTC), and at
half price the rest of the time; from 2026-08-23 Beijing's Saturday and Sunday are off-peak
all day. (Third-party write-ups, 2026-10-30: docs.apiyi.com, deepakness.com; DeepSeek's own
pricing page didn't render. Check against the balance after a run.) The windows live in
providers.toml ([<provider>.peak]) so a change is a data edit.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from . import config

BEIJING = timezone(timedelta(hours=8))


def windows(p: config.Provider) -> tuple[list[tuple[int, int]], bool] | None:
    """The provider's peak windows as (start, end) minutes of the Beijing day, and whether
    weekends are off-peak; None when it has no time-of-day pricing."""
    peak = getattr(p, "peak", None)
    if not peak:
        return None
    spans = []
    for span in peak["beijing"]:
        a, b = span.split("-")
        h0, m0 = map(int, a.split(":"))
        h1, m1 = map(int, b.split(":"))
        spans.append((h0 * 60 + m0, h1 * 60 + m1))
    return spans, bool(peak.get("weekends_off", True))


def is_peak(p: config.Provider, at: datetime) -> bool:
    w = windows(p)
    if not w:
        return False
    spans, weekends_off = w
    bj = at.astimezone(BEIJING)
    if weekends_off and bj.weekday() >= 5:
        return False
    minute = bj.hour * 60 + bj.minute
    return any(a <= minute < b for a, b in spans)


def next_change(p: config.Provider, at: datetime) -> datetime:
    """The next minute at which peak turns to off-peak or back (searched minute by minute,
    at most a week ahead)."""
    now = is_peak(p, at)
    t = at.replace(second=0, microsecond=0)
    for _ in range(7 * 24 * 60):
        t += timedelta(minutes=1)
        if is_peak(p, t) != now:
            return t
    return t


def clear_for(p: config.Provider, at: datetime, minutes: int) -> bool:
    """Whether a run of `minutes` starting `at` stays off-peak the whole time."""
    return not is_peak(p, at) and next_change(p, at) >= at + timedelta(minutes=minutes)


def next_clear(p: config.Provider, at: datetime, minutes: int) -> datetime:
    """The first start time from `at` (to the minute) at which a run of `minutes` stays
    off-peak throughout."""
    t = at.replace(second=0, microsecond=0)
    for _ in range(7 * 24 * 60):
        if clear_for(p, t, minutes):
            return t
        t = next_change(p, t) if is_peak(p, t) else t + timedelta(minutes=15)
    return t


def describe(p: config.Provider, at: datetime, minutes: int, local: timezone | None = None) -> str:
    tz = local or datetime.now().astimezone().tzinfo
    fmt = lambda d: d.astimezone(tz).strftime("%a %H:%M %Z")  # noqa: E731
    if not windows(p):
        return f"{p.name} has no time-of-day pricing: any time is the same price."
    lines = []
    if is_peak(p, at):
        lines.append(f"{p.name} is at PEAK price now (full rate) until {fmt(next_change(p, at))}.")
    else:
        lines.append(f"{p.name} is OFF-PEAK now (half price) until {fmt(next_change(p, at))}.")
    start = next_clear(p, at, minutes)
    if start == at.replace(second=0, microsecond=0):
        lines.append(f"A {minutes}-minute run started now stays off-peak.")
    else:
        lines.append(f"The next start where a {minutes}-minute run stays off-peak: {fmt(start)}.")
    return " ".join(lines)
