from typing import Dict


def create_dpia(project: str, personal_data: str, mitigations: str, risk_score: int) -> Dict:
    """Create a simple DPIA dict for testing purposes."""
    # Convert numeric score into normalized risk band used by UI/reporting.
    level = assess_risk(risk_score)
    return {
        'project': project,
        'personal_data': personal_data,
        'mitigations': mitigations,
        'risk_score': risk_score,
        'risk_level': level,
    }


def assess_risk(score: int) -> str:
    """Map numeric score to risk level."""
    # Thresholds are intentionally simple and deterministic for testability.
    if score >= 75:
        return 'high'
    if score >= 40:
        return 'medium'
    return 'low'
