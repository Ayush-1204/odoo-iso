from iso27701.utils.breach_helpers import severity_level, render_notification


def test_severity_level_thresholds():
    assert severity_level(10) == 'low'
    assert severity_level(150) == 'medium'
    assert severity_level(2000) == 'high'
    assert severity_level(5, sensitive=True) == 'high'


def test_render_notification_content():
    note = render_notification('DB leak', 'emails', 120, 'medium')
    assert 'DB leak' in note['subject']
    assert 'Affected data' in note['body']
