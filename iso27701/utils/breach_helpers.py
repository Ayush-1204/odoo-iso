from typing import Dict


def severity_level(affected_count: int, sensitive: bool = False) -> str:
    """Determine severity level for a breach."""
    # Sensitive categories (health, biometric, financial, etc.) are treated as
    # high impact even with low volume.
    if sensitive or affected_count >= 1000:
        return 'high'

    # Medium severity band for notable but not massive exposure.
    if affected_count >= 100:
        return 'medium'

    # Default low severity for limited non-sensitive incidents.
    return 'low'


def render_notification(incident: str, affected_data: str, affected_count: int, severity: str) -> Dict:
    """Build a plain-text breach notification payload."""
    # Subject includes incident + severity for rapid triage in inboxes.
    subject = f"Data breach notification: {incident} ({severity})"

    # Keep body line-oriented for readability and easy transport to logs.
    body = f"Incident: {incident}\nAffected data: {affected_data}\nAffected users: {affected_count}\nSeverity: {severity}"
    return {
        'subject': subject,
        'body': body,
    }
