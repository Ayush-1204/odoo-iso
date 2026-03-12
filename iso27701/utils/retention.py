from datetime import datetime, timedelta
from typing import Optional, Union


def compute_cutoff(retention_days: int, now: Optional[datetime] = None) -> datetime:
    """Return a UTC cutoff datetime: records older than this should be considered for deletion.

    Args:
        retention_days: number of days to retain
        now: reference datetime (UTC). If None, uses datetime.utcnow().
    """
    if retention_days is None:
        raise ValueError('retention_days must be provided')
    now = now or datetime.utcnow()
    return now - timedelta(days=retention_days)


def _parse_datetime(value: Union[str, datetime]) -> datetime:
    if isinstance(value, datetime):
        return value
    # accept common string formats
    formats = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except Exception:
            continue
    raise ValueError('Unsupported datetime format: %r' % (value,))


def should_delete(record_datetime: Union[str, datetime], retention_days: int, now: Optional[datetime] = None) -> bool:
    """Return True if `record_datetime` is older than retention_days relative to `now`.

    `record_datetime` may be a datetime or a string in one of the accepted formats.
    """
    dt = _parse_datetime(record_datetime)
    cutoff = compute_cutoff(retention_days, now=now)
    # Consider records older than or equal to the cutoff as expired.
    return dt <= cutoff
