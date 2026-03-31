import re

from iso27701.utils.dsr_helpers import generate_token, render_verification_email


def test_generate_token_unique():
    print("\n[DSAR] Test 1: Generate unique verification tokens")
    t1 = generate_token()
    print(f"  ACTION: generate_token() [call 1]")
    print(f"  OUTPUT: token_1={t1[:8]}... (first 8 chars)")
    t2 = generate_token()
    print(f"  ACTION: generate_token() [call 2]")
    print(f"  OUTPUT: token_2={t2[:8]}... (first 8 chars)")
    assert t1 != t2
    assert isinstance(t1, str)
    assert re.fullmatch(r'[0-9a-f]{32}', t1)
    print(f"  [OK] PASS: Tokens are unique 32-char hex strings")


def test_render_email_contains_token():
    print("\n[DSAR] Test 2: Render verification email template")
    token = generate_token()
    print(f"  INPUT: name='Alice', email='alice@example.com', token={token[:8]}...")
    out = render_verification_email('Alice', 'alice@example.com', token, sender='no-reply@example.com')
    print(f"  ACTION: merge template with name, email, token")
    print(f"  OUTPUT: email_to={out['email_to']}, sender={out['email_from']}")
    print(f"  OUTPUT: body contains 'Hi Alice'={('Hi Alice' in out['body_html'])}, token={token in out['body_html']}")
    assert out['email_to'] == 'alice@example.com'
    assert token in out['body_html']
    assert 'Hi Alice' in out['body_html']
    assert out['email_from'] == 'no-reply@example.com'
    print(f"  [OK] PASS: Email template rendered with all fields")
