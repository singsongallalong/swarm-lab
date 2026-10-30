from datetime import datetime, timedelta, timezone

from swarm import config, offpeak

NY = timezone(timedelta(hours=-4))


def deepseek():
    return config.Provider(name="deepseek", runtime="claude-code", model="m",
                           peak={"beijing": ["09:00-12:00", "14:00-18:00"], "weekends_off": True})


def test_peak_windows_in_beijing_weekdays():
    p = deepseek()
    # Wednesday 2026-10-28 in New York: 21:00-24:00 and 02:00-06:00 are Beijing's peak.
    assert offpeak.is_peak(p, datetime(2026, 10, 28, 22, 0, tzinfo=NY))
    assert offpeak.is_peak(p, datetime(2026, 10, 28, 3, 0, tzinfo=NY))
    assert not offpeak.is_peak(p, datetime(2026, 10, 28, 1, 0, tzinfo=NY))  # Beijing's lunch
    assert not offpeak.is_peak(p, datetime(2026, 10, 28, 14, 0, tzinfo=NY))


def test_beijing_weekend_is_off_peak():
    p = deepseek()
    # Friday 22:00 New York is Saturday 10:00 Beijing.
    assert not offpeak.is_peak(p, datetime(2026, 10, 30, 22, 0, tzinfo=NY))


def test_next_clear_skips_a_window_too_short():
    p = deepseek()
    # Wednesday 19:00 New York: off-peak until 21:00, too short for a 3-hour run, so the
    # next clear start is after the 21:00-24:00 window and before 02:00 is too short too,
    # so it lands at 06:00.
    start = offpeak.next_clear(p, datetime(2026, 10, 28, 19, 0, tzinfo=NY), 180)
    assert start.astimezone(NY).hour == 6


def test_no_peak_table_means_any_time():
    p = config.Provider(name="x", runtime="exec", model="m")
    assert not offpeak.is_peak(p, datetime(2026, 10, 28, 22, 0, tzinfo=NY))
