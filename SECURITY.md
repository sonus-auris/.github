# Security policy

## Reporting a vulnerability

Do not disclose vulnerabilities, exploit details, credentials, recordings, transcripts, personal data, biometric data, or production data in a public issue, discussion, pull request, commit, or Linear comment.

Use the affected repository's **Security** tab and private vulnerability-reporting flow when it is available. If private reporting is not enabled, contact the organization maintainers through a verified private channel shown on the organization or maintainer profile. Share only the minimum information needed to establish contact until a private channel is confirmed.

Include the affected repository and version, impact, prerequisites, reproducible steps, and a minimal proof of concept using synthetic data. Maintainers should acknowledge, triage, remediate, validate, and coordinate disclosure before creating public follow-up work.

## Handling sensitive material

Never commit live credentials, recordings, transcripts, encryption keys, evidence, customer data, or biometric data. Rotate exposed credentials through an approved human-run incident procedure; automated agents must not revoke, delete, or rotate production secrets on their own. Preserve evidence non-destructively and avoid commands that rewrite history or purge data.
