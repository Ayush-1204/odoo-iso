from iso27701.utils.processor_helpers import create_processor, is_high_risk_transfer, summarize_processor


def test_create_processor_basic():
    print("\n[PROCESSOR] Test 1: Create processor registry entry")
    print(f"  INPUT: name='Acme', contact='ops@acme.test', contract='CTR-001', country='US', data_types='email'")
    p = create_processor('Acme', contact='ops@acme.test', contract_reference='CTR-001', country='US', data_types='email')
    print(f"  ACTION: create_processor() -> instantiate record")
    print(f"  OUTPUT: name={p['name']}, contact={p['contact']}, contract_reference={p.get('contract_reference')}")
    assert p['name'] == 'Acme'
    assert p['contact'] == 'ops@acme.test'
    print(f"  [OK] PASS: Processor record created successfully")


def test_is_high_risk_transfer():
    print("\n[PROCESSOR] Test 2: Evaluate cross-border transfer risk")
    test_cases = [('US', False), ('FR', False), ('Wonderland', True), (None, True)]
    for country, expected_risk in test_cases:
        print(f"  INPUT: country={country}")
        result = is_high_risk_transfer(country)
        print(f"  ACTION: check if country in non-regulated list or missing")
        print(f"  OUTPUT: is_high_risk={result} (expected={expected_risk})")
        assert result is expected_risk
    print(f"  [OK] PASS: Risk assessment logic working")


def test_summarize_processor():
    print("\n[PROCESSOR] Test 3: Generate processor summary text")
    p = create_processor('Acme', country='US', contract_reference='CTR-001')
    print(f"  INPUT: processor name='Acme', country='US', contract_ref='CTR-001'")
    s = summarize_processor(p)
    print(f"  ACTION: summarize_processor() -> merge fields into readable text")
    print(f"  OUTPUT: summary_contains_name={'Acme' in s}, country={'US' in s}, contract={'CTR-001' in s}")
    assert 'Acme' in s
    assert 'US' in s
    assert 'CTR-001' in s
    print(f"  [OK] PASS: Summary text includes all key fields")
