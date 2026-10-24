# Before/after findings summary

Original centralized score: **67/100**, with **429 findings**, at
`49b924a7ca79f81d5fabe0e66b5e0ac57cf9267e`.

Verified local score: **86/100**, with **346 findings**, at
`3af80680c550872b3dd924a4efcc74184e2acc75`. The scanner completed successfully with exit code 0.
All 17 package surfaces were scanned; zero targets were skipped.

Scanner **3.0.123**, the default profile, offline mode, untrusted repository
policy, Cisco auto without its optional dependency, minimum score 80, and
advisory severity settings match the centralized action. The local baseline
reproduces every original rule, severity, location, and line, as well as the
67 score and 429 total. The final source export is the immutable hardening
commit above, including the Unicode quote correction. The subsequent documentation
commit adds the four audit/PR documents and an Apache-2.0 modification notice in
the webapp-testing source and its role copy; executable code is unchanged.

The local platform is Windows/Python 3.15; upstream uses Linux/Python 3.12.
Runtime dependency versions differ, while the scanner wheel and settings
match. This is a measured local pass, not a new centralized listing verdict.
The pinned source CI can reproduce the upstream runtime after publication.

Counts below are raw scanner occurrences, including duplicate copies and
marketplace package scans. They are not counts of distinct vulnerabilities.
Retained false positives remain visible to the scanner and are not suppressed.

| Rule | Before | Verified after | Removed occurrences |
| --- | ---: | ---: | ---: |
| CLAUDE_SKILL_FRONTMATTER_INVALID | 2 | 0 | 2 |
| CODEXIGNORE_MISSING | 1 | 0 | 1 |
| DANGEROUS_DYNAMIC_EXECUTION | 57 | 47 | 10 |
| DEPENDABOT_MISSING | 2 | 0 | 2 |
| DEPENDENCY_LOCKFILE_MISSING | 2 | 0 | 2 |
| GITHUB_ACTION_UNPINNED | 18 | 0 | 18 |
| HARDCODED_SECRET | 224 | 214 | 10 |
| LICENSE_MISSING | 17 | 0 | 17 |
| PLUGIN_JSON_INTERFACE_ASSET_COMPOSERICON | 1 | 1 | 0 |
| PLUGIN_JSON_INTERFACE_ASSET_LOGO | 1 | 1 | 0 |
| PLUGIN_JSON_INTERFACE_ASSET_PRIVACYPOLICYURL | 1 | 1 | 0 |
| PLUGIN_JSON_INTERFACE_ASSET_SCREENSHOTS | 1 | 1 | 0 |
| PLUGIN_JSON_INTERFACE_ASSET_TERMSOFSERVICEURL | 1 | 1 | 0 |
| PLUGIN_JSON_INTERFACE_DEVELOPERNAME | 1 | 0 | 1 |
| RISKY_APPROVAL_DEFAULT | 5 | 5 | 0 |
| RISKY_SKILL_INSTRUCTION | 76 | 75 | 1 |
| SECURITY_MD_MISSING | 17 | 0 | 17 |
| SHELL_INJECTION_PATTERN | 2 | 0 | 2 |
| **Total** | **429** | **346** | **83** |

## Remaining findings and maintainer actions

- **214 credential matches:** reviewed synthetic fixtures,
  placeholders, negative examples, detector patterns, and metadata. The weak
  password generator and copyable Cloud SQL credential default were hardened.
- **47 execution matches:** detector strings,
  test data, and a fixed Playwright DOM callback. The two actual unrestricted
  arithmetic execution sites were removed without weakening any detector.
- **75 instruction matches:** network examples and
  scoped defensive education. Actual permission/disclosure gaps were hardened;
  capabilities and safe examples remain available.
- **5 approval matches:** descriptions of unsafe
  settings that the auditor is instructed to flag, not enabled defaults.
- **Five optional interface asset notices:** genuine maintainer-owned icons,
  screenshots, privacy policy, and terms URLs remain a product decision.

No live credential was confirmed; no specific live key requiring rotation
was identified. Operators who used old weak templates must replace those
deployed passwords and review access. Existing missing redistribution
permission for Composio content remains a maintainer licensing action.

Publish or submit the hardening branch through the normal review process,
then have the listing maintainer run a fresh centralized scan against the
eventual default-branch commit. External PR #970 and its checks were not
modified. No force push, merge, npm release, or external messaging was done.

See SECURITY_AUDIT.md and SECURITY_TRIAGE.md for technical justifications,
all 177 original canonical finding groups, changed paths, and validation.

## Private local evidence

Raw reports and source inventories stay untracked under audit-input/ and
out of npm. Only metrics and maintainer assessments are committed.

| Evidence | SHA-256 |
| --- | --- |
| pr-970-sanitized-scan.zip | `ae6e54611db4bd55996965c719f73c9e413d5cc69b449cbd589718d49c38a680` |
| local-before.json | `67378d0b6be4e69e0702bf11e724ffb45d742ceedc23bd661e64040b8168a29c` |
| local-before.inventory.json | `344ac6149667b38b1f73a52376a0bef1523fa28e4b1e8adaab3e72393777a43b` |
| verified-after.json | `1b10a334309f3f559b72c29633fe642307db112c82dd48cb80b226bf79870e72` |
| verified-after.inventory.json | `06796b046150aaa0c6cd76d76a8cef70b16ad06db82581dfdea09a91b50bde32` |
