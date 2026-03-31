from iso27701.utils.mapping_helpers import parse_mapping_md, mapping_rows_to_csv, convert_md_to_csv


SAMPLE_MD = '''
| ISO 27701 Control | Description | Repository Feature / Status |
|---|---|---|
| 7.4.1 Logging | Maintain logs of system activities | auditlog module - Covered |
| 6.3 Access Control | Restrict access to personal data | base_user_role - Covered |
'''


def test_parse_mapping_md():
    print("\n[MAPPING] Test 1: Parse ISO control mapping table from Markdown")
    print(f"  INPUT: Markdown table with 2 ISO control rows")
    rows = parse_mapping_md(SAMPLE_MD)
    print(f"  ACTION: parse_mapping_md() -> extract table rows")
    print(f"  OUTPUT: row_count={len(rows)}, first_row_control={rows[0][0][:6] if len(rows) > 0 else 'N/A'}...")
    assert len(rows) == 2
    assert rows[0][0].startswith('7.4.1')
    print(f"  [OK] PASS: Markdown table parsed correctly")


def test_mapping_to_csv():
    print("\n[MAPPING] Test 2: Convert ISO mapping from Markdown to CSV export")
    print(f"  INPUT: Markdown table with ISO controls")
    csv_text = convert_md_to_csv(SAMPLE_MD)
    print(f"  ACTION: convert_md_to_csv() -> format as RFC 4180 CSV")
    print(f"  OUTPUT: csv_contains_header={'ISO Control' in csv_text}, contains_7.4.1={'7.4.1' in csv_text}, contains_feature={'auditlog' in csv_text}")
    assert 'ISO Control' in csv_text
    assert '7.4.1' in csv_text
    assert 'auditlog' in csv_text
    print(f"  [OK] PASS: CSV export generated correctly")
