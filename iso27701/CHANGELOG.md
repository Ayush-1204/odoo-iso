# Changelog — iso27701 module

## Unreleased

- Scaffolded `iso27701` Odoo addon: manifest, models, views, security entries
- RoPA / PII registry: `iso.pii.type`, `iso.processing.activity` (fields: purpose, lawful_basis, retention_days, controller/processor)
- Retention automation: `target_model`, `date_field`, `allow_auto_delete` on `iso.processing.activity` and daily cron `run_retention_cleanup`
- DSAR workflow: `iso.dsr` model with verification token support, `send_verification_email` fallback, `action_verify`, timestamps and verifier
- Consent management: `iso.consent` model and helper `create_from_partner`, revoke method
- DPIA: `iso.dpia` model scaffold and pure-Python DPIA helpers and tests
- Breach management: `iso.breach` model scaffold and pure-Python breach helpers and tests
- Third-party processor registry: `iso.processor` model and pytest-friendly `processor_helpers`
- Mapping export endpoint: controller at `/iso27701/mapping.csv` (restricted to staff/admin)
- Pytest suite: added `iso27701/tests_pytest` with helpers and tests for retention, dsr, consent, dpia, breach, processor, mapping
- GitHub Actions workflow: `.github/workflows/pytest.yml` runs pytest for the `iso27701` pytest suite
- Admin guide: `iso27701/ADMIN.md` with run instructions and next steps

## Notes

- The module includes both Odoo models/views and pure-Python pytest helpers. Run `pytest iso27701/tests_pytest -q` for quick CI-friendly tests without an Odoo runtime.
- Retention auto-delete is opt-in per activity — review before enabling in production environments.
