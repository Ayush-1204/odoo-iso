from iso27701.utils.mapping_helpers import parse_mapping_md, mapping_rows_to_csv, convert_md_to_csv


SAMPLE_MD = '''
| ISO 27701 Control | Description | Repository Feature / Status |
|---|---|---|
| 7.4.1 Logging | Maintain logs of system activities | auditlog module — Covered |
| 6.3 Access Control | Restrict access to personal data | base_user_role — Covered |
'''


def test_parse_mapping_md():
    rows = parse_mapping_md(SAMPLE_MD)
    assert len(rows) == 2
    assert rows[0][0].startswith('7.4.1')


def test_mapping_to_csv():
    csv_text = convert_md_to_csv(SAMPLE_MD)
    assert 'ISO Control' in csv_text
    assert '7.4.1' in csv_text
    assert 'auditlog' in csv_text
