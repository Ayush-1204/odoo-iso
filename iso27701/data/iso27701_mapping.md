# ISO 27701 Control Mapping

This document maps ISO/IEC 27701 privacy controls to features implemented (or planned) in this repository.

| ISO 27701 Control | Description | Repository Feature / Status |
|---|---|---|
| 7.4.1 Logging | Maintain logs of system activities | `auditlog` module — Covered |
| 6.3 Access Control | Restrict access to personal data | `base_user_role` — Covered |
| 6.6 Authentication | Secure user authentication | `password_security` — Covered |
| 7.5 Session Management | Automatic session timeout | `auth_session_timeout` — Covered |
| RoPA / Records of Processing Activities | Document processing activities | `iso27701` module — New (scaffolded) |
| DSAR handling | Data subject request workflow | `iso27701` module — New (scaffolded) |
| Consent Management | Record consents and revocations | `iso27701` module — New (scaffolded) |
| DPIA | Privacy impact assessments | `iso27701` module — New (scaffolded) |
| Breach Notification | Incident recording & notification | `iso27701` module — New (scaffolded) |

## Identified Gaps (next steps)

- Implement retention automation and deletion workflows. (Retention automation scaffolded — daily cron + cleanup method)
- Add consent capture widgets on forms and portal endpoints.
- Add templates and notification logic for breach reporting (72-hour workflows).
- Implement third-party processor agreements and transfers controls.
- Create unit tests and demo data.
