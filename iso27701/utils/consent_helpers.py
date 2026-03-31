from datetime import datetime
from typing import Optional


def create_consent_for_partner(partner_identifier: str, purpose: str, source: Optional[str] = None, now: Optional[datetime] = None) -> dict:
    """Create a pure-Python consent record (dict) for testing without Odoo.

    `partner_identifier` is an arbitrary identifier (name or id) used in tests.
    """
    # Allow deterministic timestamps in tests by accepting `now` override.
    now = now or datetime.utcnow()

    # Keep record schema simple and serializable for logging/fixtures.
    return {
        'subject': partner_identifier,
        'purpose': purpose,
        'consent_date': now.isoformat(sep=' '),
        'status': 'active',
        'source': source,
    }


def revoke_consent(consent: dict, now: Optional[datetime] = None) -> dict:
    """Revoke a consent dict produced by `create_consent_for_partner`.

    Mutates and returns the same dict for convenience.
    """
    # State transition: active -> revoked.
    now = now or datetime.utcnow()
    consent['status'] = 'revoked'

    # Store explicit revocation timestamp for auditability.
    consent['revoked_date'] = now.isoformat(sep=' ')
    return consent
