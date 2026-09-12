# Legal governance and executable contract policy

`sonus-auris/sonus-auris-docs` is the reviewable Sonus legal workspace. `ores-legal` supplies reusable drafting and governance patterns, but no cross-organization template automatically governs Sonus or a recording situation. Product, jurisdiction, participant, customer, and workforce use requires Sonus-specific review.

## Machine-readable contract layer

The standard sources are `contracts/main.tsp`, independently authored `contracts/authored.schema.json`, the `LegalRegistry` corpus, and deterministic generated coverage/runtime manifests in `sonus-auris-docs`. `tjsv` must compare the independent TypeSpec and JSON Schema authorities and validate the corpus. `oresc` is the portfolio governance integration and delegates schema parity to `tjsv`.

Legal states are `approved`, `draft`, `review_required`, and `gap`. Only `approved` end-user-distributed documents can enter the runtime approved manifest; runtime consumers bind to document ID and exact source hash and fail closed for missing, blocked, stale, or mismatched acceptance metadata.

## Recording, consent, and evidence boundary

Operating-system microphone permission is not legal recording consent. Login, account ownership, file access, or device ownership does not automatically establish another participant's consent. Every surface that records, buffers, transcribes, analyzes, embeds, syncs, exports, or remotely processes audio must be mapped to the applicable approved legal/privacy artifact before release.

Changes involving background capture, bystanders, minors, speaker inference, descriptors/embeddings, location/context metadata, research/beta collection, cloud processing, export/sharing, retention/deletion, or consent withdrawal are legal-impact triggers.

Technical provenance or chain-of-custody controls do not let a UI, API, CLI, report, or marketing claim that a recording is lawful, admissible, authentic, complete, tamper-proof, or dispositive of a legal issue.

## Commercial and workforce boundary

SLOs are engineering objectives; SLA commitments and remedies are contractual. SOWs govern engagement-specific scope and acceptance. Employment, contractor, confidentiality/IP, onboarding, offboarding, separation, and termination documents must be jurisdiction-routed. Executed workforce/customer records and signatures stay outside Git.

## Repository privacy boundary

Never commit recordings, transcripts, biometric/voice identifiers, executed agreements, signatures, customer evidence, credentials, privileged communications, personnel files, or matter-specific legal advice. Git may contain blank templates, policy text, non-sensitive routing metadata, approval references, and deterministic hashes.

## Reusable CI

Repositories using the standard legal contract layout can call:

```yaml
jobs:
  legal-contract:
    uses: sonus-auris/.github/.github/workflows/reusable-legal-contract-audit.yml@main
```

Private/release runners should use `require_ores_cli: true` after provisioning `oresc`. CI verifies synchronization and release metadata, not substantive legal sufficiency; qualified counsel and accountable owners remain responsible for approval.
