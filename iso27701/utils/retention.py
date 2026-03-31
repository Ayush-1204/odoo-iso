from datetime import datetime, timedelta
from typing import Optional, Union


def compute_cutoff(retention_days: int, now: Optional[datetime] = None) -> datetime:
    """Return a UTC cutoff datetime: records older than this should be considered for deletion.

    Args:
        retention_days: number of days to retain
        now: reference datetime (UTC). If None, uses datetime.utcnow().
    """
    # Explicit guard: this function must not silently accept missing policy.
    if retention_days is None:
        raise ValueError('retention_days must be provided')

    # Use UTC to avoid timezone drift in server-side cleanup checks.
    now = now or datetime.utcnow()

    # Any record older than this cutoff is considered retention-expired.
    return now - timedelta(days=retention_days)


def _parse_datetime(value: Union[str, datetime]) -> datetime:
    """Normalize incoming datetime values from tests/Odoo-like payloads.

    Accepted inputs:
    - datetime object (returned as-is)
    - common datetime/date string formats
    """
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
            # Try next accepted format.
            continue
    raise ValueError('Unsupported datetime format: %r' % (value,))


def should_delete(record_datetime: Union[str, datetime], retention_days: int, now: Optional[datetime] = None) -> bool:
    """Return True if `record_datetime` is older than retention_days relative to `now`.

    `record_datetime` may be a datetime or a string in one of the accepted formats.
    """
    # Convert string/date-like input into a comparable datetime object.
    dt = _parse_datetime(record_datetime)

    # Calculate policy threshold once per evaluation.
    cutoff = compute_cutoff(retention_days, now=now)

    # Consider records older than or equal to the cutoff as expired.
    return dt <= cutoff
