import pytest
from datetime import datetime, timedelta

from iso27701.utils.retention import compute_cutoff, should_delete


def test_compute_cutoff_with_custom_now():
    now = datetime(2026, 3, 12, 12, 0, 0)
    cutoff = compute_cutoff(30, now=now)
    assert cutoff == datetime(2026, 2, 10, 12, 0, 0)


def test_should_delete_true_and_false():
    now = datetime(2026, 3, 12, 12, 0, 0)
    old = (now - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")
    recent = (now - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")

    assert should_delete(old, 30, now=now) is True
    assert should_delete(recent, 30, now=now) is False


def test_should_delete_accepts_datetime():
    now = datetime(2026, 3, 12, 12, 0, 0)
    dt = now - timedelta(days=40)
    assert should_delete(dt, 30, now=now) is True


def test_parse_iso_format():
    now = datetime(2026, 3, 12, 12, 0, 0)
    iso = "2026-02-10T12:00:00"
    assert should_delete(iso, 30, now=now) is True


def test_invalid_format_raises():
    with pytest.raises(ValueError):
        should_delete('not-a-date', 30, now=datetime.utcnow())
