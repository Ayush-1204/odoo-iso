from datetime import datetime, timedelta

from iso27701.utils.consent_helpers import create_consent_for_partner, revoke_consent


def test_create_and_revoke_consent():
    now = datetime(2026, 3, 12, 12, 0, 0)
    c = create_consent_for_partner('partner-1', 'Marketing', source='signup', now=now)
    assert c['status'] == 'active'
    assert 'consent_date' in c
    assert c['purpose'] == 'Marketing'

    # revoke
    rc = revoke_consent(c, now=now + timedelta(days=1))
    assert rc['status'] == 'revoked'
    assert 'revoked_date' in rc
