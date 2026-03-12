import re

from iso27701.utils.dsr_helpers import generate_token, render_verification_email


def test_generate_token_unique():
    t1 = generate_token()
    t2 = generate_token()
    assert t1 != t2
    assert isinstance(t1, str)
    assert re.fullmatch(r'[0-9a-f]{32}', t1)


def test_render_email_contains_token():
    token = generate_token()
    out = render_verification_email('Alice', 'alice@example.com', token, sender='no-reply@example.com')
    assert out['email_to'] == 'alice@example.com'
    assert token in out['body_html']
    assert 'Hi Alice' in out['body_html']
    assert out['email_from'] == 'no-reply@example.com'
