# Preparing a PR: iso27701 module

Create a feature branch, commit your changes, and open a PR with the mapping and tests.

Example commands (PowerShell):

```powershell
cd "C:\Users\AYUSH VERMA\odoo-iso"
# create branch
git checkout -b feature/iso27701-pims
# review changes
git add iso27701
git commit -m "feat(iso27701): add PIMS scaffold (RoPA, DSAR, Consent, DPIA, Breach) + pytest helpers"
git push -u origin feature/iso27701-pims

# Open PR on GitHub with title:
# "feat(iso27701): privacy information management scaffold (RoPA, DSAR, Consent, DPIA, Breach)"
```

PR body checklist (suggested):
- Summary of features added (RoPA, ProcessingActivity, DSAR verification email helpers, Consent helpers, DPIA & Breach helpers, retention cron)
- Files added/changed list
- Tests: list of pytest modules under `iso27701/tests_pytest`
- Manual testing steps (how to run pytest, or run Odoo integration tests via Docker)
- Migration/upgrade notes (none for existing models unless you change names)
- Security note: retention auto-delete is opt-in per `iso.processing.activity.allow_auto_delete` — do not enable in production without review.
