# Harden command generation, skill authorization, and HOL scanner CI

User-controlled screenshot filenames and Microsoft 365 fields could enter shell
commands or generated source. This patch keeps them as structured data, replaces
weak temporary-password generation, and removes unrestricted execution from the
two historical algebra examples. It also requires a runtime Cloud SQL password
and redacts environment-file inspection.

Selected skill instructions now define authorization boundaries for credential
access, account registration, deployment, intrusive testing, and command runners.
All 2,660 skill IDs and bundle memberships remain unchanged; canonical sources
and existing role copies are synchronized. HOL Guard and BulkPublish are intact.
Security detectors, negative fixtures, and defensive education are preserved.

Workflows use verified immutable action references and read-only permissions.
New HOL CI uses the exact centralized scanner action and settings, with a score
gate of 80 and no repository suppressions. Added scoped security/license notices,
restored three upstream license texts, added dependency-free lock metadata and
Actions update automation, and protected private audit artifacts from publishing.

Validation:

- Manifest: 2,660 actual directories and unchanged IDs, 15 categories.
- Bundle consistency: zero differences after refreshing from canonical sources.
- Six Python security regression tests, one Node filename-transport test, and
  53 existing security detector tests pass.
- All 26 changed SKILL.md files pass Skill Lint with zero warnings.
- npm pack inventory and isolated CLI copying pass, including all nine host flags.
- Hostile provisioning/offboarding data produces valid PowerShell syntax and
  no injected command AST nodes; no live tenant operations were executed.
- Scanner 3.0.123 reproduced the original **67/100 and 429 findings** locally.
  The measured patched result and rule deltas are in SECURITY_FINDINGS_SUMMARY.md.

The final immutable hardening commit `3af8068` scored **86/100**, with **346
findings**, exit code 0, and no skipped targets. Audit/attribution documentation
was added afterward without changing executable code.

See SECURITY_AUDIT.md and SECURITY_TRIAGE.md for the 177 canonical finding groups,
technical false-positive explanations, remaining advisories, and evidence hashes.
Raw scanner reports and the ZIP are ignored and excluded from this PR/npm.

No live credential was confirmed. Operators who used old weak credential templates
should replace those deployed passwords. The existing unresolved Composio
redistribution-permission disclosure remains a maintainer licensing action.
The listing maintainer still needs to rescan the eventual published/default-branch
source commit; this PR does not modify external listing PR #970 or its checks.
