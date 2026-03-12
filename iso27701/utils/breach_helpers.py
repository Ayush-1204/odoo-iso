from typing import Dict


def severity_level(affected_count: int, sensitive: bool = False) -> str:
    """Determine severity level for a breach."""
    if sensitive or affected_count >= 1000:
        return 'high'
    if affected_count >= 100:
        return 'medium'
    return 'low'


def render_notification(incident: str, affected_data: str, affected_count: int, severity: str) -> Dict:
    subject = f"Data breach notification: {incident} ({severity})"
    body = f"Incident: {incident}\nAffected data: {affected_data}\nAffected users: {affected_count}\nSeverity: {severity}"
    return {
        'subject': subject,
        'body': body,
    }
