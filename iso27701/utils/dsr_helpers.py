import uuid


def generate_token() -> str:
    """Generate a random verification token for DSR verification."""
    return uuid.uuid4().hex


def render_verification_email(requestor_name: str, requestor_email: str, token: str, sender: str = 'no-reply') -> dict:
    """Render a minimal verification email payload.

    Returns a dict with keys: subject, body_html, email_to, email_from
    """
    subject = 'Verify your data subject request'
    body_html = f"<p>Hi {requestor_name},</p><p>Please verify your data subject request by using this token: <strong>{token}</strong></p>"
    return {
        'subject': subject,
        'body_html': body_html,
        'email_to': requestor_email,
        'email_from': sender,
    }
