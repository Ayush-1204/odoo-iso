from iso27701.utils.breach_helpers import severity_level, render_notification


def test_severity_level_thresholds():
    print("\n[BREACH] Test 1: Classify breach severity levels")
    test_cases = [(10, 'low'), (150, 'medium'), (2000, 'high'), (5, 'high')]
    for (impact_score, expected_level) in test_cases:
        sensitive = (impact_score == 5)  # last case has sensitive=True
        input_str = f"impact_score={impact_score}" + (", sensitive=True" if sensitive else "")
        print(f"  INPUT: {input_str}")
        if sensitive:
            result = severity_level(impact_score, sensitive=True)
        else:
            result = severity_level(impact_score)
        print(f"  ACTION: map score to severity level")
        print(f"  OUTPUT: severity={result} (expected={expected_level})")
        if sensitive:
            assert result == expected_level
        else:
            assert result == expected_level
    print(f"  [OK] PASS: Severity classification correct")


def test_render_notification_content():
    print("\n[BREACH] Test 2: Render breach notification template")
    print(f"  INPUT: incident='DB leak', data_category='emails', affected_records=120, severity='medium'")
    note = render_notification('DB leak', 'emails', 120, 'medium')
    print(f"  ACTION: merge template with incident details")
    print(f"  OUTPUT: subject_contains='DB leak'={('DB leak' in note['subject'])}, body_contains_affected={'Affected data' in note['body']}")
    assert 'DB leak' in note['subject']
    assert 'Affected data' in note['body']
    print(f"  [OK] PASS: Notification template rendered correctly")
