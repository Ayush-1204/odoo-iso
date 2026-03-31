# ISO27701 Pytest Trace Summary
## What You See When Running Tests

This document explains what each test prints (input → action → output) to help you understand the contributions.

### How to Run Tests with Trace Output

```powershell
cd "c:\Users\AYUSH VERMA\odoo-iso"
python -m pytest iso27701/tests_pytest -v -s
```

The `-s` flag shows all `print()` statements.

---

## Test Breakdown by Contribution

### 1. RETENTION (Data Lifecycle Enforcement)
**File:** `test_retention_logic.py`  
**What we test:** A record should be deleted if its date is older than the retention days.

#### Test 1: Compute Cutoff Date
```
INPUT:    today=2026-03-12, retention_days=30
ACTION:   calculate cutoff = today - retention_days
OUTPUT:   cutoff=2026-02-10 (30 days ago)
```
**Means:** We correctly calculate when the retention period ends. A 30-day retention period starting March 12 end on Feb 10.

#### Test 2: Delete Decision (Old vs Recent)
```
INPUT:    record_date_old=2026-02-09 12:00:00 (31 days old), retention_days=30
ACTION:   check if record_date <= cutoff
OUTPUT:   True (record is older than retention period)
```
**Means:** A record older than the cutoff is marked for deletion (kept = False).

```
INPUT:    record_date_recent=2026-03-02 12:00:00 (10 days old), retention_days=30
ACTION:   check if record_date <= cutoff
OUTPUT:   False (record is within retention period)
```
**Means:** A record newer than the cutoff should NOT be deleted (kept = True).

#### Test 3: Datetime Object Support
```
INPUT:    record_date=2026-01-31 (datetime object), retention_days=30
ACTION:   parse datetime and compare with cutoff
OUTPUT:   True (record is 40 days old, exceeds 30-day retention)
```
**Means:** Our code handles Python datetime objects, not just strings.

#### Test 4: ISO 8601 String Support
```
INPUT:    record_date=2026-02-10T12:00:00 (ISO string), retention_days=30
ACTION:   parse ISO format and compare with cutoff
OUTPUT:   True (date is exactly 30 days ago, qualifies for deletion)
```
**Means:** We parse industry-standard ISO date strings.

#### Test 5: Error Rejection
```
INPUT:    record_date='not-a-date' (invalid format), retention_days=30
ACTION:   attempt to parse invalid date string
OUTPUT:   ValueError raised (malformed date rejected)
```
**Means:** Invalid dates are caught and rejected, not silently ignored.

---

### 2. DSAR (Data Subject Access Requests)
**File:** `test_dsr_helpers.py`  
**What we test:** Generate verification tokens and render verification emails.

#### Test 1: Generate Unique Tokens
```
ACTION:   generate_token() [call 1]
OUTPUT:   token_1=a9b2b80e... (first 8 chars of 32-char hex string)
ACTION:   generate_token() [call 2]
OUTPUT:   token_2=0e0ffdcf... (different, each call is unique)
```
**Means:** Each DSAR gets a unique, unpredictable 32-char hex token for verification (prevents guessing).

#### Test 2: Render Verification Email
```
INPUT:    name='Alice', email='alice@example.com', token=16ee5a5a...
ACTION:   merge template with name, email, token
OUTPUT:   email_to=alice@example.com, sender=no-reply@example.com
          body contains 'Hi Alice'=True, token=True
```
**Means:** We generate a personalized email with their token embedded, sent from a system address.

---

### 3. CONSENT (Permission & Revocation Audit)
**File:** `test_consent_helpers.py`  
**What we test:** Create consent records and revoke them with timestamps.

#### Test 1: Create & Revoke Consent
```
INPUT:    partner_id='partner-1', purpose='Marketing', source='signup'
ACTION:   create_consent_for_partner() [status=active]
OUTPUT:   consent_date=2026-03-12 12:00:00, purpose=Marketing, status=active
```
**Means:** We record when the partner gave consent, for what purpose, and mark it as active.

```
INPUT:    revoke_consent() at time=2026-03-13 12:00:00
ACTION:   transition consent state to 'revoked'
OUTPUT:   status=revoked, revoked_date=2026-03-13 12:00:00
```
**Means:** When a partner revokes, we record the exact time—not just delete the record (audit trail).

---

### 4. DPIA (Data Protection Impact Assessment)
**File:** `test_dpia_helpers.py`  
**What we test:** Risk scoring for processing activities.

#### Test 1: Risk Level Mapping
```
INPUT:    impact_score=10
ACTION:   map score to risk level
OUTPUT:   risk_level=low

INPUT:    impact_score=50
OUTPUT:   risk_level=medium

INPUT:    impact_score=90
OUTPUT:   risk_level=high
```
**Means:** We consistently classify impact scores into risk buckets (low/medium/high).

#### Test 2: DPIA Record Creation
```
INPUT:    project='ProjectX', data_category='emails', mitigation='anonymize', impact_score=80
ACTION:   create_dpia() -> assess_risk(80) -> 'high'
OUTPUT:   project=ProjectX, risk_level=high, data_category=None
```
**Means:** We create a DPIA record and automatically assign a risk level based on the impact score.

---

### 5. BREACH (Incident Severity Classification)
**File:** `test_breach_helpers.py`  
**What we test:** Classify breach severity and generate notifications.

#### Test 1: Severity Classification
```
INPUT:    impact_score=10
OUTPUT:   severity=low

INPUT:    impact_score=150
OUTPUT:   severity=medium

INPUT:    impact_score=2000
OUTPUT:   severity=high

INPUT:    impact_score=5, sensitive=True
OUTPUT:   severity=high (sensitive data makes it high even at low score)
```
**Means:** We map breach impact to severity, and sensitive data boosts the classification.

#### Test 2: Notification Rendering
```
INPUT:    incident='DB leak', data_category='emails', affected_records=120, severity='medium'
ACTION:   merge template with incident details
OUTPUT:   subject_contains='DB leak'=True, body_contains_affected=True
```
**Means:** We generate a notification email with incident details for responders.

---

### 6. PROCESSOR (Third-Party Oversight)
**File:** `test_processor_helpers.py`  
**What we test:** Registry entries and risk evaluation for processors.

#### Test 1: Create Processor
```
INPUT:    name='Acme', contact='ops@acme.test', contract='CTR-001', country='US', data_types='email'
ACTION:   create_processor() -> instantiate record
OUTPUT:   name=Acme, contact=ops@acme.test, contract_reference=CTR-001
```
**Means:** We record processor details (name, contact, contract, location, data scope).

#### Test 2: Cross-Border Transfer Risk
```
INPUT:    country=US
OUTPUT:   is_high_risk=False (EU/US safe transfer)

INPUT:    country=FR
OUTPUT:   is_high_risk=False (EU country, safe)

INPUT:    country=Wonderland
OUTPUT:   is_high_risk=True (unknown country, needs review)

INPUT:    country=None
OUTPUT:   is_high_risk=True (missing info, flag as risky)
```
**Means:** We automatically flag risky cross-border transfers for review.

#### Test 3: Processor Summary
```
INPUT:    processor name='Acme', country='US', contract_ref='CTR-001'
ACTION:   summarize_processor() -> merge fields into readable text
OUTPUT:   summary_contains_name=True, country=True, contract=True
```
**Means:** We generate human-readable processor summaries from structured data.

---

### 7. MAPPING (ISO Control to Feature Traceability)
**File:** `test_mapping_helpers.py`  
**What we test:** Parse ISO control matrix and export as CSV.

#### Test 1: Parse Markdown Table
```
INPUT:    Markdown table with 2 ISO control rows
ACTION:   parse_mapping_md() -> extract table rows
OUTPUT:   row_count=2, first_row_control=7.4.1
```
**Means:** We can read an ISO control mapping document in human-editable Markdown format.

#### Test 2: Convert to CSV
```
INPUT:    Markdown table with ISO controls
ACTION:   convert_md_to_csv() -> format as RFC 4180 CSV
OUTPUT:   csv_contains_header=True, contains_7.4.1=True, contains_feature=True
```
**Means:** We export the mapping to CSV for audit reports and compliance tools.

---

## Summary: What Each Test Is Proving

| Contribution | Test Count | What's Being Proven |
|---|---|---|
| **Retention** | 5 | Date parsing, cutoff logic, deletion decision accuracy |
| **DSAR** | 2 | Token generation uniqueness, email template rendering |
| **Consent** | 1 | State transitions, audit timestamps |
| **DPIA** | 2 | Risk scoring, record creation |
| **Breach** | 2 | Severity classification, notification generation |
| **Processor** | 3 | Registry creation, risk detection, summary text |
| **Mapping** | 2 | Markdown parsing, CSV export |
| **TOTAL** | **17 tests** | All core logic works, no regressions |

---

## How to Explain This in a Meeting

**"When we run the pytest suite, we see these 17 tests execute. Each one demonstrates that a piece of our privacy management system works correctly:

- **Retention tests** prove we can accurately identify which records to delete based on age.
- **DSAR tests** prove we generate unique tokens and send verified emails.
- **Consent tests** prove we audit who gave/revoked permission and when.
- **DPIA tests** prove we consistently score risk on processing activities.
- **Breach tests** prove we classify incidents and generate notifications.
- **Processor tests** prove we track third parties and flag risky transfers.
- **Mapping tests** prove we can document which ISO controls map to our code.

All tests pass in 0.10 seconds, meaning our privacy logic is fast, reliable, and repeatable. We can run this same test suite every time code changes (CI) to prevent regressions."**

---

## Capturing Test Output for Reports

To save the full trace output to a file for your report:

```powershell
python -m pytest iso27701/tests_pytest -v -s > pytest_full_trace.txt 2>&1
type pytest_full_trace.txt
```

Then include `pytest_full_trace.txt` in your audit/compliance evidence package.
