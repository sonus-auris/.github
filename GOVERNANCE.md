# Governance

<!-- ore-org-baseline:begin -->
This public `.github` repository defines the minimum organization-wide community, contribution, automation, and agent-safety defaults for Sonus Auris. Repository-local policy may be stricter, but it must not weaken this baseline.

## Sources of truth

- GitHub is authoritative for source, policy, architecture records, public organization context, reviewed implementation, and immutable commit history.
- [github.com/sonus-auris](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef) is the planning and delivery ledger.
- Repository-local documentation is authoritative for repository-specific behavior and may strengthen this baseline.
- `repository-relationships.manual.json` is authoritative for reviewed public relationship declarations; the generated JSON graph is a deterministic projection.
- The approved private project registry is authoritative for private repository inventory and private-only edges.
- Private member context belongs in an approved private system, such as `.github-private`, never in this public repository.

## Change control

Material policy and architecture changes use issues or pull requests, focused commits, reviewable diffs, tests, and linked planning context. Existing content must be preserved unless a change explicitly supersedes it. Generated and mirrored artifacts must be updated from their authoritative source. Inferred relationship edges remain advisory until reviewed and declared.

Conflicts are resolved semantically with full history and cross-repository context. Destructive operations, history rewrites, force pushes, bypasses, and deletion of shared resources are default-deny and require exact authorization.

## Decision authority and required change record

- Normal changes are proposed through reviewable pull requests; direct default-branch edits are reserved for a documented, human-authorized exceptional process.
- Routine wording and template maintenance requires maintainer review and passing policy validation.
- Security, privacy, identity, workflow, governance, or reusable-automation changes require an explicit maintainer decision and relevant domain-owner review when they affect recording consent, audio privacy, evidence integrity, retention, encryption, or application-store compliance.
- Weakening semantic conflict resolution, the destructive-operation denylist, secret handling, immutable Action pinning, or required validation requires explicit organization-owner approval and a documented rationale.

Substantial changes must include the linked Linear work item, affected repositories and contracts, risks, compatibility or migration effects, exact validation evidence, and a statement describing conflicts and their semantic resolution.

## Automation and releases

- Workflows use least-privilege permissions, explicit timeouts, concurrency controls where appropriate, checkout without persisted credentials, and immutable full-commit Action pins.
- Reusable workflow consumers pin a reviewed 40-character commit SHA rather than a mutable branch or tag.
- Dependency updates remain reviewable and do not bypass required checks or human review.
- Branch protections, rulesets, organization settings, secret scanning, and private vulnerability reporting must be configured in GitHub settings because files in this repository do not enable those controls automatically.

## Security and review cadence

Report vulnerabilities privately according to `SECURITY.md`. Never place credentials, recordings, transcripts, biometric data, personal data, production data, or other sensitive material in public issues, pull requests, logs, examples, or fixtures.

Review this baseline after material GitHub platform changes, security incidents, organization-wide tooling changes, or at least quarterly. Track identified drift in Linear and remediate it through reviewable changes.

## Precedence

A repository may impose stricter requirements. It must not weaken secret handling, non-destructive collaboration, semantic conflict resolution, evidence-backed completion, or required review and checks.
<!-- ore-org-baseline:end -->
