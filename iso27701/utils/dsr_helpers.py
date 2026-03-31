import uuid


def generate_token() -> str:
    """Generate a random verification token for DSR verification."""
    # UUID4 provides sufficient randomness for a lightweight verification flow.
    # `.hex` avoids dashes and keeps token URL/email friendly.
    return uuid.uuid4().hex


def render_verification_email(requestor_name: str, requestor_email: str, token: str, sender: str = 'no-reply') -> dict:
    """Render a minimal verification email payload.

    Returns a dict with keys: subject, body_html, email_to, email_from
    """
    # Keep subject explicit so recipients can identify the verification action.
    subject = 'Verify your data subject request'

    # Inline token keeps helper independent of website routes for tests.
    body_html = f"<p>Hi {requestor_name},</p><p>Please verify your data subject request by using this token: <strong>{token}</strong></p>"

    # Return a mail-payload-like dictionary so caller can send via Odoo, SMTP,
    # or simply validate content in unit tests.
    return {
        'subject': subject,
        'body_html': body_html,
        'email_to': requestor_email,
        'email_from': sender,
    }
