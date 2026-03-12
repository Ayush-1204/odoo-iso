from datetime import datetime
from typing import Optional


def create_consent_for_partner(partner_identifier: str, purpose: str, source: Optional[str] = None, now: Optional[datetime] = None) -> dict:
    """Create a pure-Python consent record (dict) for testing without Odoo.

    `partner_identifier` is an arbitrary identifier (name or id) used in tests.
    """
    now = now or datetime.utcnow()
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
    now = now or datetime.utcnow()
    consent['status'] = 'revoked'
    consent['revoked_date'] = now.isoformat(sep=' ')
    return consent
