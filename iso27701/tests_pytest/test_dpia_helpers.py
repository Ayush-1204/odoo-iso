from iso27701.utils.dpia_helpers import assess_risk, create_dpia


def test_assess_risk_levels():
    assert assess_risk(10) == 'low'
    assert assess_risk(50) == 'medium'
    assert assess_risk(90) == 'high'


def test_create_dpia_contains_level():
    d = create_dpia('ProjectX', 'emails', 'anonymize', 80)
    assert d['risk_level'] == 'high'
    assert d['project'] == 'ProjectX'
