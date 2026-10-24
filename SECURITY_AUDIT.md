# HOL security audit — 2026-10-24

Original centralized score: **67/100**. Final local measurement and rule totals
are recorded in SECURITY_FINDINGS_SUMMARY.md. A passing centralized rescan of
the new commit is still required for listing; this document does not change
the upstream PR or claim that all advisory findings are vulnerabilities.

## Evidence and scope

- Repository: sinhoneyy/master-skills, baseline commit
  `49b924a7ca79f81d5fabe0e66b5e0ac57cf9267e`.
- [Centralized run 40103003701](https://github.com/hashgraph-online/awesome-ai-plugins/actions/runs/40103003701),
  artifact `12563746803`, `scan-findings-pr-970-sinhoneyy-master-skills`.
- Downloaded ZIP SHA-256:
  `ae6e54611db4bd55996965c719f73c9e413d5cc69b449cbd589718d49c38a680`.
  JSON, SARIF, and Markdown agree on 429 findings and the source commit.
  The ZIP and all raw reports remain ignored under audit-input/ and excluded
  from npm distribution.
- Scanner: plugin-scanner **3.0.123**, wheel SHA-256
  `d176d4d35c980e4e66c9e72bd79d0a100efbf40bea9d5f4dae35c8609eb7d04d`.
  Verified against the immutable upstream action's scanner-sha256.txt.
- Read the upstream [SCANNER_GUIDE.md](https://github.com/hashgraph-online/awesome-ai-plugins/blob/main/SCANNER_GUIDE.md)
  and reviewed action
  `hashgraph-online/ai-plugin-scanner-action@caba2e96aa8ad2feb6cf6fca52442b52e22e779f`.
  Source CI uses that exact action and centralized settings: mode scan, default
  profile, minimum 80, advisory severity gate, repository policy untrusted,
  offline, Cisco auto without the optional dependency, no PR comments or SARIF
  upload. No suppression file, rule modification, baseline, or skill exclusion
  was introduced.

## Repository and duplicate mapping

The baseline has 2,660 canonical skill directories, 15 index categories, and 10
role bundles. The npm description's older display count is pre-existing; no
manual count changes were made. skills_index.json and all skill IDs, names,
paths, metadata, and bundle membership are preserved. HOL Guard and BulkPublish
are retained byte-for-byte.

The original 429 scanner occurrences reduce to **177 groups** when keyed by rule,
severity, canonical path, and reported line. Role copies map
`plugins/<bundle>/skills/<id>/...` to `skills/<id>/...`. Repeated marketplace
scans can report one physical path multiple times. These counts are not counts
of independently exploitable vulnerabilities.

The final immutable hardening commit `3af8068` measured **86/100**, with **346
findings**, scanner exit 0, all 17 package surfaces scanned, and zero skipped
targets. The later documentation commit adds audit results and the Apache-2.0
modification notice for webapp-testing; it changes no executable code. This is
a verified local pass; a fresh upstream centralized scan remains required.

[SECURITY_TRIAGE.md](SECURITY_TRIAGE.md) classifies every original group by rule,
severity, canonical location, occurrence count, and technical assessment.

The canonical skills/ tree is maintained source. All 6,557 baseline role-bundle
files matched their corresponding canonical files byte-for-byte. History commit
846009d introduced the role snapshots; no generator was checked in. Added
`.github/scripts/sync_bundles.py` to refresh existing membership from source and
check equality in CI. Bundle copies were refreshed through that script, never
edited as independent implementations. Root and role manifests, installer code,
and CI are maintained directly. The index is an imported catalog snapshot;
validation now also checks for actual skill directories absent from the index.
The two historical benchmark solutions are generated examples; their security
patch is preserved alongside the original purpose and tested arithmetic behavior.

## Confirmed issues and hardening

| Area | Assessment | Remediation |
| --- | --- | --- |
| Screenshot stitching | Confirmed shell and Python-source injection when attacker-controlled filenames are used | Shell-free argument arrays, absolute script paths, JSON data passed through argv, and Python JSON parsing in both stitching modes; sips also uses an argument array |
| Historical algebra examples | Unsafe implementation: caller-controlled operators and operands reached unrestricted execution | Strict integer/operator validation and explicit arithmetic on whitelisted AST nodes; retain operator precedence and exponent associativity |
| Microsoft 365 provisioning | Unsafe password generation: predictable prefix and only about 9,000 numeric choices | Generate 32 cryptographically random bytes for each user at runtime, force a password change, exclude PasswordProfile from CSV export |
| Microsoft 365 script generation | Confirmed script injection through supplied fields, email, and domain | PowerShell literal encoding covers ASCII and all four typographic single-quote forms; remove dynamic comment/here-string interpolation; sanitize the offboarding report filename |
| Cloud SQL deployment example | Unsafe copyable credential default | Require DB_PASSWORD from the runtime environment, with no hardcoded fallback; document Secret Manager injection |
| Cleanup instructions | Unsafe local environment-file disclosure | Display variable names with redacted values rather than dumping .env.local |
| Account, credential, and security operations | Missing or insufficient execution boundaries in selected skills | Add scoped authorization requirements to AgentMail, AppDeploy, CRED-OMEGA, AWS rotation, Vault, privilege escalation, and network lab instructions; retain capabilities and existing user authorization |
| Windows setup instructions | Downloaded response was immediately executed | Download and inspect the complete local installer; separate execution after authorization under the approved host policy |
| Workflows | Mutable action tags; publish checkout persisted credentials | Resolve tags to upstream commit objects, pin each existing action, disable credential persistence in publish, preserve read-only fork PR workflows |
| Security and licensing metadata | Missing policy and notices across installable package surfaces | Root policy, scoped tooling MIT license, role notices, imported upstream license texts, and skill-specific reporting pointers |
| Hygiene | Missing lockfile, update automation, ignored private artifacts, invalid sample frontmatter | Dependency-free npm lockfile; Actions Dependabot; narrow artifact/bytecode ignores; repair the sample skill's frontmatter |

The instruction changes are safeguards for actual consequential operations.
Ordinary HTTP examples and defensive security education were not rewritten
to evade lexical matches. Existing explicit authorization in AgentPhone,
Sendblue, pen-testing skills, and other scoped guides remains intact.

An AST inspection of Python sources also found six intentional shell-enabled
call sites outside the original findings: webapp-testing starts explicitly
supplied server commands; AgentHub and autoresearch execute experiment commands;
Google Workspace selects commands from a static local recipe catalog; TypeScript
diagnostics uses constant command strings. Those are command-runner capabilities,
not demonstrated untrusted-input injection paths. Shell support is preserved.
Added explicit trust/authorization boundaries for experiment configuration and
server commands, and removed webapp-testing's instruction to execute helpers
before allowing source inspection.

## False positives and retained advisory findings

**Dynamic execution:** the eight scanner implementation paths in the baseline
contain detection expressions, diagnostic strings, or remediation prose. They
do not execute the matched text. The security-scorer test file intentionally
writes unsafe sample source as data and tests that the detector rejects it.
Playwright helpers use a fixed DOM extraction callback; its DOM evaluation API
is not unrestricted execution of input as host code. The scanner's lexical
matching also sees prose in comments and strings. All these detectors and
negative fixtures are retained. The two actual arithmetic execution sites were
fixed; no detector patterns or tests were removed to raise the score.

**Risky approval defaults:** all five occurrences map to the single
agentic-actions-auditor skill and its role copy. It lists unsafe sandbox and
approval values as configurations to detect, rate, and remediate. It does not
set those values as defaults or direct an agent to enable them. Retain the
training examples and report this context for scanner-maintainer review.

**Risky instructions:** 76 occurrences map to 72 canonical skills. The rule
matches public HTTP commands, SSH terminology, shell wrappers, and environment
file names without determining data flow, negative examples, or authorization.
For example, Varlock and Linear explicitly prohibit showing secret values and
recommend schema inspection; Vault's SSH CA discussion describes avoiding
per-user authorized-key management; skill auditors describe malicious patterns
to reject. Defensive offensive-security examples already require authorization.
Public lookup and health-check examples do not inherently upload workspace
data. Selected genuine permission and disclosure gaps are hardened above;
remaining lexical matches are not silently suppressed or claimed fixed.

**Credentials:** all 49 canonical reported file/line groups were reviewed with
credential literals redacted from logs. The scanner's 224 occurrences include
synthetic passwords, test configuration, token placeholders, detector regexes,
negative examples, environment lookups, template parameter names, and metadata
strings. No live credential was confirmed; **no specific credential requiring
rotation was identified**. That is not proof that no unreported credential
exists in every historical revision. The weak password generator and Cloud SQL
default were hardened rather than characterized as leaked live credentials.
If actual credentials were deployed using an old weak template, the operator
must replace them and review access; this audit cannot identify those deployments.

**Optional plugin interface assets:** a developer name is added using the
existing author identity. Icons, screenshots, a hosted privacy policy, and
terms URLs are not invented for this local CLI catalog. Their remaining info
findings require a genuine maintainer product decision, not fabricated assets.

## Licensing review

README.md, package.json, and existing plugin manifests explicitly declare MIT
for catalog tooling. The root license implements that existing intent and
explicitly excludes third-party content. Existing nested licenses are untouched.
Each role-bundle notice limits its scope to tooling and points to per-skill
terms and attribution; it is not a new license grant for its contents.
webapp-testing retains its Apache-2.0 license and now carries a prominent dated
notice identifying the locally modified execution guidance.

Restored missing license texts only where existing skill/plugin declarations
and upstream records agree:

| Skill | Upstream evidence | License blob SHA |
| --- | --- | --- |
| aeo | alirezarezvani/claude-skills, MIT; also reproduced in CREDITS.md | c3e30bcc287d6a1ebdb4ab29c10d344fd1053639 |
| youtube-full | Its manifest and source attribution identify ZeroPointRepo/youtube-skills, MIT | b3a72de31eae6d3beecf813bfb8e7e775125fe79 |
| hugging-face-trackio | Its manifest and source identify huggingface/skills, Apache-2.0 | 261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64 |

The existing CREDITS.md disclosure about Composio content lacking redistribution
permission remains unresolved. The original import does not record every upstream
revision. This patch neither removes accepted content nor supplies missing legal
permission; the maintainer must establish redistribution rights with the upstream
owner. A scanner license check is not proof of complete license compliance.

## Validation and reproducibility

Use Python 3.12 and the pinned scanner action in Linux CI for the centralized
runtime. Local validation used Windows, Python 3.15, and Node 24.22.0. Scanner
wheel and policy settings match; local dependency versions/platform differ.

```text
python -B .github/scripts/validate_manifest.py
python -B .github/scripts/sync_bundles.py --check
python -B -m unittest discover -s tests -v
node --test tests/stitch-data.test.mjs
python -B -m unittest discover -s skills/skill-tester/tests -p test_security_scorer.py -v
python -B .github/scripts/smoke_package.py
```

Skill Lint was run against every changed SKILL.md with no blocking errors or
warnings. All 2,660 skill directories match the unchanged manifest. Security
tests cover algebra semantics and hostile values, filename argument transport,
PowerShell field encoding, cryptographic password generation, offboarding, and
secret-free exports. A real PowerShell parser regression verifies that all five
single-quote forms preserve data and produce no injected commands. Windows
PowerShell parsed hostile provisioning and offboarding scripts without errors
or injected command nodes; cloud tenant operations were not executed. The 53 existing
security detector tests pass. Product Design Harness validation is conditional
in existing Import Validation CI and is deferred because that skill is absent
at the baseline. Packaging checks exercise actual copying of all mobile skills,
all nine supported host flags, bytecode exclusion, policy/license inclusion,
and private-artifact exclusion. No browser, cloud, live email, or publishing
operations are needed to validate these patches.

For a private local measurement with the exact scanner wheel installed:

```text
<scanner-python> -B .github/scripts/run_hol_scan.py --revision 49b924a7ca79f81d5fabe0e66b5e0ac57cf9267e --output audit-input/local-before.json
<scanner-python> -B .github/scripts/run_hol_scan.py --output audit-input/local-after.json
```

The helper exports all Git-tracked files plus nonignored new source files to
a fresh directory, so private downloaded reports, environments, and tool binaries
are not part of the scanned source. It records a SHA-256 source inventory. This
is source-export isolation, not a scanner exclusion or rule change. Reports use
the supported stdout transport, captured privately rather than printed; the
scanner's Windows file writer initially failed locking an ancestor directory.
Review SECURITY_FINDINGS_SUMMARY.md for measured results and outstanding actions.

## Files modified

The hardening commits change 84 implementation, metadata, policy, and test files. The four audit/PR documents are committed separately after measurement. The exhaustive list below is derived from the Git diff and the document deliverables.

- `.codex-plugin/plugin.json`
- `.codexignore`
- `.github/dependabot.yml`
- `.github/scripts/run_hol_scan.py`
- `.github/scripts/smoke_package.py`
- `.github/scripts/sync_bundles.py`
- `.github/scripts/validate_manifest.py`
- `.github/workflows/ci.yml`
- `.github/workflows/import-validation.yml`
- `.github/workflows/publish-package.yml`
- `.github/workflows/security-scan.yml`
- `.github/workflows/skill-lint.yml`
- `.gitignore`
- `.npmignore`
- `LICENSE`
- `PR_DESCRIPTION.md`
- `SECURITY.md`
- `SECURITY_AUDIT.md`
- `SECURITY_FINDINGS_SUMMARY.md`
- `SECURITY_TRIAGE.md`
- `package-lock.json`
- `package.json`
- `plugins/master-skills-ai-agent-builder/LICENSE`
- `plugins/master-skills-ai-agent-builder/SECURITY.md`
- `plugins/master-skills-ai-agent-builder/skills/aeo/LICENSE`
- `plugins/master-skills-ai-agent-builder/skills/aeo/SECURITY.md`
- `plugins/master-skills-ai-agent-builder/skills/agenthub/SKILL.md`
- `plugins/master-skills-ai-agent-builder/skills/agentmail/SKILL.md`
- `plugins/master-skills-ai-agent-builder/skills/appdeploy/SKILL.md`
- `plugins/master-skills-ai-agent-builder/skills/autoresearch-agent/SKILL.md`
- `plugins/master-skills-ai-agent-builder/skills/loki-mode/benchmarks/results/2026-01-05-00-49-17/humaneval-solutions/160.py`
- `plugins/master-skills-ai-agent-builder/skills/loki-mode/benchmarks/results/humaneval-loki-solutions/160.py`
- `plugins/master-skills-backend-engineer/LICENSE`
- `plugins/master-skills-backend-engineer/SECURITY.md`
- `plugins/master-skills-backend-engineer/skills/gcp-cloud-run/SKILL.md`
- `plugins/master-skills-backend-engineer/skills/youtube-full/LICENSE`
- `plugins/master-skills-backend-engineer/skills/youtube-full/SECURITY.md`
- `plugins/master-skills-devops-cloud/LICENSE`
- `plugins/master-skills-devops-cloud/SECURITY.md`
- `plugins/master-skills-devops-cloud/skills/ms365-tenant-manager/scripts/user_management.py`
- `plugins/master-skills-devops-cloud/skills/secrets-vault-manager/SKILL.md`
- `plugins/master-skills-frontend-designer/LICENSE`
- `plugins/master-skills-frontend-designer/SECURITY.md`
- `plugins/master-skills-frontend-designer/skills/vibe-code-cleanup/SKILL.md`
- `plugins/master-skills-frontend-designer/skills/webapp-testing/SKILL.md`
- `plugins/master-skills-integrations/LICENSE`
- `plugins/master-skills-integrations/SECURITY.md`
- `plugins/master-skills-marketing-growth/LICENSE`
- `plugins/master-skills-marketing-growth/SECURITY.md`
- `plugins/master-skills-mobile-developer/LICENSE`
- `plugins/master-skills-mobile-developer/SECURITY.md`
- `plugins/master-skills-productivity/LICENSE`
- `plugins/master-skills-productivity/SECURITY.md`
- `plugins/master-skills-qa-testing/LICENSE`
- `plugins/master-skills-qa-testing/SECURITY.md`
- `plugins/master-skills-security-engineer/LICENSE`
- `plugins/master-skills-security-engineer/SECURITY.md`
- `plugins/master-skills-security-engineer/skills/aws-secrets-rotation/SKILL.md`
- `plugins/master-skills-security-engineer/skills/network-101/SKILL.md`
- `plugins/master-skills-security-engineer/skills/privilege-escalation-methods/SKILL.md`
- `plugins/master-skills-security-engineer/skills/skill-tester/assets/sample-skill/SKILL.md`
- `skills/aeo/LICENSE`
- `skills/aeo/SECURITY.md`
- `skills/agenthub/SKILL.md`
- `skills/agentmail/SKILL.md`
- `skills/appdeploy/SKILL.md`
- `skills/autoresearch-agent/SKILL.md`
- `skills/aws-secrets-rotation/SKILL.md`
- `skills/cred-omega/SKILL.md`
- `skills/environment-setup-guide/SKILL.md`
- `skills/full-page-screenshot/scripts/full-page-screenshot.mjs`
- `skills/full-page-screenshot/scripts/stitch-data.mjs`
- `skills/gcp-cloud-run/SKILL.md`
- `skills/hugging-face-trackio/LICENSE`
- `skills/hugging-face-trackio/SECURITY.md`
- `skills/loki-mode/benchmarks/results/2026-01-05-00-49-17/humaneval-solutions/160.py`
- `skills/loki-mode/benchmarks/results/humaneval-loki-solutions/160.py`
- `skills/ms365-tenant-manager/scripts/user_management.py`
- `skills/network-101/SKILL.md`
- `skills/privilege-escalation-methods/SKILL.md`
- `skills/secrets-vault-manager/SKILL.md`
- `skills/skill-tester/assets/sample-skill/SKILL.md`
- `skills/vibe-code-cleanup/SKILL.md`
- `skills/webapp-testing/SKILL.md`
- `skills/youtube-full/LICENSE`
- `skills/youtube-full/SECURITY.md`
- `tests/stitch-data.test.mjs`
- `tests/test_security_hardening.py`
