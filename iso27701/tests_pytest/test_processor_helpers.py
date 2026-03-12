from iso27701.utils.processor_helpers import create_processor, is_high_risk_transfer, summarize_processor


def test_create_processor_basic():
    p = create_processor('Acme', contact='ops@acme.test', contract_reference='CTR-001', country='US', data_types='email')
    assert p['name'] == 'Acme'
    assert p['contact'] == 'ops@acme.test'


def test_is_high_risk_transfer():
    assert is_high_risk_transfer('US') is False
    assert is_high_risk_transfer('FR') is False
    assert is_high_risk_transfer('Wonderland') is True
    assert is_high_risk_transfer(None) is True


def test_summarize_processor():
    p = create_processor('Acme', country='US', contract_reference='CTR-001')
    s = summarize_processor(p)
    assert 'Acme' in s
    assert 'US' in s
    assert 'CTR-001' in s
