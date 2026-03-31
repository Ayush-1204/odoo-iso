from datetime import datetime, timedelta

from iso27701.utils.consent_helpers import create_consent_for_partner, revoke_consent


def test_create_and_revoke_consent():
    print("\n[CONSENT] Test 1: Create and revoke consent records")
    now = datetime(2026, 3, 12, 12, 0, 0)
    print(f"  INPUT: partner_id='partner-1', purpose='Marketing', source='signup'")
    c = create_consent_for_partner('partner-1', 'Marketing', source='signup', now=now)
    print(f"  ACTION: create_consent_for_partner() [status=active]")
    print(f"  OUTPUT: consent_date={c.get('consent_date')}, purpose={c['purpose']}, status={c['status']}")
    assert c['status'] == 'active'
    assert 'consent_date' in c
    assert c['purpose'] == 'Marketing'
    print(f"  [OK] PASS: Consent created in 'active' state")

    print(f"\n  INPUT: revoke_consent() at time={now + timedelta(days=1)}")
    rc = revoke_consent(c, now=now + timedelta(days=1))
    print(f"  ACTION: transition consent state to 'revoked'")
    print(f"  OUTPUT: status={rc['status']}, revoked_date={rc.get('revoked_date')}")
    assert rc['status'] == 'revoked'
    assert 'revoked_date' in rc
    print(f"  [OK] PASS: Consent successfully revoked with timestamp")
