# ISO27701 Module — Admin Guide

This document gives a quick overview of the `iso27701` module scaffold included in this repository, how to run the pytest suite that exercises the pure-Python helpers, and suggested next steps for deploying the module in an Odoo environment.

Overview
- RoPA (Records of Processing Activities): `iso.processing.activity`, `iso.pii.type`
- DSAR workflow: `iso.dsr` model with verification token and email helpers
- Consent management: `iso.consent` and convenience helpers
- DPIA & Breach: helper functions and data models scaffolded
- Retention automation: scheduled cron `run_retention_cleanup` on `iso.processing.activity`

Running pytest (no Odoo required)
1. Install pytest: `pip install pytest`
2. Run the iso27701 pytest suite:
```powershell
cd "C:\Users\AYUSH VERMA\odoo-iso"
pytest iso27701/tests_pytest -q
```

What the pytest suite covers
- Pure-Python helper logic: retention math, dsr token/email rendering, consent helpers, DPIA/breach logic, processor helpers, mapping conversion.

Running full Odoo tests (optional)
- The repo contains Odoo `TransactionCase` tests under `iso27701/tests` that require an Odoo runtime and PostgreSQL. Use Docker Compose with an Odoo image to run integration tests.

Suggested next steps
- Flesh out form views, server actions, and access groups for production use.
- Add mail templates and configure outgoing mail in Odoo for DSAR verification emails.
- Implement UI for retention dry-run and manual approval before auto-delete.
- Produce an export endpoint (CSV/Excel) for the ISO mapping document and RoPA.

Contact
- If you want, I can open a PR with this scaffold and a mapping CSV export endpoint implemented in Odoo.
