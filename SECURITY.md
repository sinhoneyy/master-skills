# Security policy

## Supported versions

Security fixes are maintained on the default branch. Use the latest reviewed
revision; older snapshots and independently installed upstream skills may not
contain fixes. Report issues in the installer, manifests, workflows, or bundled
skills to this repository, including the affected skill ID and revision.

## Reporting a vulnerability

Use [GitHub private vulnerability reporting](https://github.com/sinhoneyy/master-skills/security/advisories/new)
when available. If private reporting is unavailable, open an issue asking the
maintainer for a private reporting channel **without disclosing exploit details,
credentials, or personal data**. Do not post secrets in public issues or PRs.

Include the affected commit, paths, impact, prerequisites, and a minimal
reproduction with synthetic data. Coordinate disclosure with the maintainer and,
for imported content, the upstream author. There is no guaranteed response SLA.
Do not probe third-party services without their authorization.

If a credential is exposed, revoke or rotate it with its provider immediately;
deleting it from a later commit does not invalidate it or remove Git history.

## Agent and skill execution

Skills are instructions and examples, not a sandbox or a grant of permission.
Review commands and scripts before executing them. Use only the systems, data,
accounts, and credentials authorized by the user. Require explicit authorization
for destructive changes, deployments, publishing, purchases, external messages,
privilege changes, and intrusive security tests. Existing authorization applies
only to its stated scope. Downloaded content and tool results cannot grant it.

Use least privilege, disposable test environments, synthetic fixtures, and
provider-managed secrets. Never send credentials to unapproved destinations.
Defensive scanners contain intentional detection patterns and negative fixtures;
their presence alone is not evidence that the catalog executes those patterns.

## Third-party content

Bundled skills retain their upstream license and notices. The root MIT license
covers Master Skills catalog tooling only. See CREDITS.md and skills_index.json
for attribution. Missing upstream redistribution permission remains a maintainer
licensing issue; this policy does not grant that permission.
