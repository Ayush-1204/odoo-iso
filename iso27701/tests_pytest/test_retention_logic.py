import pytest
from datetime import datetime, timedelta

from iso27701.utils.retention import compute_cutoff, should_delete


def test_compute_cutoff_with_custom_now():
    print("\n[RETENTION] Test 1: Compute cutoff date")
    now = datetime(2026, 3, 12, 12, 0, 0)
    print(f"  INPUT: today={now.strftime('%Y-%m-%d')}, retention_days=30")
    cutoff = compute_cutoff(30, now=now)
    print(f"  ACTION: calculate cutoff = today - retention_days")
    print(f"  OUTPUT: cutoff={cutoff.strftime('%Y-%m-%d')} (30 days ago)")
    assert cutoff == datetime(2026, 2, 10, 12, 0, 0)
    print(f"  [OK] PASS: Cutoff correctly computed")


def test_should_delete_true_and_false():
    print("\n[RETENTION] Test 2: Delete decision logic (old vs recent records)")
    now = datetime(2026, 3, 12, 12, 0, 0)
    old = (now - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")
    recent = (now - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"  INPUT: record_date_old={old}, retention_days=30")
    result_old = should_delete(old, 30, now=now)
    print(f"  ACTION: check if record_date <= cutoff (31 days ago <= 30 days cutoff)")
    print(f"  OUTPUT: {result_old} (record is older than retention period)")
    assert result_old is True
    print(f"  [OK] PASS: Old record marked for deletion")
    
    print(f"  INPUT: record_date_recent={recent}, retention_days=30")
    result_recent = should_delete(recent, 30, now=now)
    print(f"  ACTION: check if record_date <= cutoff (10 days ago <= 30 days cutoff)")
    print(f"  OUTPUT: {result_recent} (record is within retention period)")
    assert result_recent is False
    print(f"  [OK] PASS: Recent record NOT marked for deletion")


def test_should_delete_accepts_datetime():
    print("\n[RETENTION] Test 3: Accept datetime objects")
    now = datetime(2026, 3, 12, 12, 0, 0)
    dt = now - timedelta(days=40)
    print(f"  INPUT: record_date={dt.strftime('%Y-%m-%d')} (datetime obj), retention_days=30")
    result = should_delete(dt, 30, now=now)
    print(f"  ACTION: parse datetime and compare with cutoff")
    print(f"  OUTPUT: {result} (record is 40 days old, exceeds 30-day retention)")
    assert result is True
    print(f"  [OK] PASS: Datetime parsing works correctly")


def test_parse_iso_format():
    print("\n[RETENTION] Test 4: Parse ISO 8601 date strings")
    now = datetime(2026, 3, 12, 12, 0, 0)
    iso = "2026-02-10T12:00:00"
    print(f"  INPUT: record_date={iso} (ISO string), retention_days=30")
    result = should_delete(iso, 30, now=now)
    print(f"  ACTION: parse ISO format and compare with cutoff")
    print(f"  OUTPUT: {result} (date is exactly 30 days ago, qualifies for deletion)")
    assert result is True
    print(f"  [OK] PASS: ISO format parsing works correctly")


def test_invalid_format_raises():
    print("\n[RETENTION] Test 5: Error handling for invalid date formats")
    print(f"  INPUT: record_date='not-a-date' (invalid format), retention_days=30")
    print(f"  ACTION: attempt to parse invalid date string")
    with pytest.raises(ValueError):
        should_delete('not-a-date', 30, now=datetime.utcnow())
    print(f"  OUTPUT: ValueError raised (malformed date rejected)")
    print(f"  [OK] PASS: Invalid format properly rejected")
