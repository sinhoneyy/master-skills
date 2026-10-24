# v1.0.1 — Security hardening

This patch release delivers the reviewed security fixes to npm, GitHub Packages,
and plugin clients. It preserves all 2,660 skill IDs, the installer interface,
and the HOL Guard and BulkPublish contributions.

- Passes the hosted HOL scanner at **86/100**, up from 67/100. The merged source
  [scan](https://github.com/sinhoneyy/master-skills/actions/runs/40109514249),
  [CI](https://github.com/sinhoneyy/master-skills/actions/runs/40109514384), and
  [Import Validation](https://github.com/sinhoneyy/master-skills/actions/runs/40109514283) passed.
- Hardens screenshot command generation, PowerShell script generation and Unicode
  quoting, temporary passwords, arithmetic examples, and credential handling.
- Adds scoped authorization guidance, pinned Actions, security policies, and
  upstream license notices without removing skills or suppressing scanner rules.
- Adds a GitHub Packages mirror while preserving the existing unscoped npm name
  and CLI commands.

Install the npm release with `npx master-skills@1.0.1 --help`, or update an existing
installation using the same host flag you used before. The GitHub Packages mirror
uses the existing `@sinhoneyy/master-skills` name and GitHub's registry authentication.

Remaining scanner advisories and licensing limitations are documented in
[SECURITY_AUDIT.md](SECURITY_AUDIT.md), [SECURITY_TRIAGE.md](SECURITY_TRIAGE.md), and
[SECURITY_FINDINGS_SUMMARY.md](SECURITY_FINDINGS_SUMMARY.md). A new centralized scan
is still required for the external Awesome AI Plugins listing. No live credential
was confirmed; replace any deployed passwords based on the older weak templates.
