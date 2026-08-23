# Security policy

## Reporting a vulnerability

Do not open a public issue for suspected vulnerabilities, and do not disclose vulnerabilities, exploit details, credentials, recordings, transcripts, personal data, biometric data, or production data in a public issue, discussion, pull request, commit, or Linear comment.

Use the affected repository's **Security** tab and private vulnerability-reporting flow when it is available. If private reporting is not enabled, contact the organization maintainers through a verified private channel shown on the organization or maintainer profile. Share only the minimum information needed to establish contact until a private channel is confirmed.

Include the affected repository and version, impact, prerequisites, reproducible steps, and a minimal proof of concept using synthetic data. Do not access data beyond what is necessary to demonstrate the issue, disrupt production, or persist access. Maintainers should acknowledge, create or link a restricted Linear security issue, triage severity and affected versions, remediate, validate, and coordinate disclosure before creating public follow-up work.

## Handling sensitive material

Never commit live credentials, recordings, transcripts, encryption keys, evidence, customer data, or biometric data. Rotate exposed credentials through an approved human-run incident procedure; automated agents must not revoke, delete, or rotate production secrets on their own. Preserve evidence non-destructively and avoid commands that rewrite history or purge data.

<!-- ore-org-baseline:begin -->
## Reporting a vulnerability

Do **not** open a public issue for a suspected vulnerability, exposed credential, authentication bypass, data leak, or sensitive infrastructure weakness.

Use private vulnerability reporting from the **Security** tab of the affected repository when available. Otherwise contact the organization owners through an established private operational channel and identify the affected repository, impact, reproduction conditions, and a safe contact method. Provide only the minimum evidence needed; do not include live credentials, private keys, customer data, or destructive proof-of-concept payloads.

## Handling exposed credentials

Treat any credential pasted into chat, logs, commits, issues, pull requests, build artifacts, screenshots, or test fixtures as compromised. Stop using it, revoke or rotate it, replace dependent configuration, and audit recent use. Removing a secret from the latest file does not invalidate it or erase earlier copies. Repository-history rewriting requires exact authorization and coordinated review.

## Supported versions and response expectations

Each repository documents its own supported versions. No service-level response commitment is implied by this fallback policy. Maintainers should acknowledge valid reports privately, limit access, preserve evidence, coordinate remediation, test the fix, rotate affected secrets, and disclose responsibly when appropriate.

Linear planning context: [github.com/sonus-auris](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef).
<!-- ore-org-baseline:end -->
