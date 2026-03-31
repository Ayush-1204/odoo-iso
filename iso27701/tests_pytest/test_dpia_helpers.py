from iso27701.utils.dpia_helpers import assess_risk, create_dpia


def test_assess_risk_levels():
    print("\n[DPIA] Test 1: Risk level assessment")
    test_cases = [(10, 'low'), (50, 'medium'), (90, 'high')]
    for score, expected_level in test_cases:
        print(f"  INPUT: impact_score={score}")
        result = assess_risk(score)
        print(f"  ACTION: map score to risk level")
        print(f"  OUTPUT: risk_level={result} (expected={expected_level})")
        assert result == expected_level
    print(f"  [OK] PASS: Risk level mapping correct")


def test_create_dpia_contains_level():
    print("\n[DPIA] Test 2: Create DPIA record with risk assessment")
    print(f"  INPUT: project='ProjectX', data_category='emails', mitigation='anonymize', impact_score=80")
    d = create_dpia('ProjectX', 'emails', 'anonymize', 80)
    print(f"  ACTION: create_dpia() -> assess_risk(80) -> 'high'")
    print(f"  OUTPUT: project={d['project']}, risk_level={d['risk_level']}, data_category={d.get('data_category')}")
    assert d['risk_level'] == 'high'
    assert d['project'] == 'ProjectX'
    print(f"  [OK] PASS: DPIA record created with correct risk assignment")
