# Sonus Auris organization source alignment

This directory defines the machine-readable organization contract used to reconcile Sonus Auris planning, product, delivery, and publication surfaces.

## Authorities and scope

`governance/source-of-truth.toml` in `sonus-auris/.github` is the canonical **organization-direction and resource-mapping** manifest. It does not replace narrower authoritative sources:

- lowercase `agents.md` remains the canonical agent-safety policy, with uppercase/provider files acting as compatibility mirrors;
- `sonus-auris-interfaces` retains the independent TypeSpec and hand-authored JSON Schema product contracts;
- source repositories remain authoritative for runtime behavior, migrations, generated artifacts, and deployment definitions;
- `sonus-auris-docs` remains the long-form documentation and draft legal-template surface;
- Linear and GitHub issues remain planning and delivery records.

The organization manifest names these authorities and makes contradictions observable without absorbing them into one monolithic document.

## Surfaces that must agree

- private canonical `.github` repository;
- private `sonus-auris-docs` repository;
- public Astro `sonus-auris.github.io` marketing/legal/store-review site;
- private `sonus-auris-mcp-server.rs` and `sonus-auris-cli` repositories;
- interfaces, clients, sync, monorepo, infra, Rust/Flutter apps, lambdas, read/write servers, and shared core libraries;
- Linear project and documents;
- primary GitHub Project and tracked issues;
- Supabase organization or approved isolated namespace, Neon organization, Cloudflare domain, GCP project, and Slack channel.

## Append-only reconciliation

Direction changes do not erase history.

1. Add the next `[[supersessions]]` record with the former statement, replacement, reason, evidence, and timestamp.
2. Update current manifest fields in the same reviewed change.
3. Preserve former prose in Git history. When visible marketing copy changes, retain the superseded statement in a non-interactive historical record or linked changelog rather than silently deleting it.
4. Update non-authoritative pointers only after the canonical revision is accepted.
5. Do not add recordings, transcripts, executed contracts, signature images, credentials, keys, connection strings, customer data, or other sensitive material.

## Independent contract authorities

`source-of-truth.tsp` and `source-of-truth.schema.json` are independently authored top-level contracts. TypeSpec may emit JSON Schema B; the hand-authored schema is JSON Schema A. `tjsv` compares normalized declarations and validates generated artifacts without making either authority subordinate.

A governance change is incomplete when only one contract changes. Parity checks, the example TOML instance, and repository-specific fixtures must all pass before merge.

## Status vocabulary

- `verified`: observed through the relevant connected system and consistent with the recorded identifier/state;
- `declared`: selected intentionally but not yet independently observed;
- `drift`: observed and inconsistent with the expected contract;
- `missing`: checked and not present or not visible;
- `blocked`: an administrative, billing, access, dependency, or infrastructure prerequisite prevents completion;
- `unverified`: not checked through an authoritative connector during the recorded review.

A plausible identifier never becomes `verified` by inference.

## Read-only audit and explicit mutation

`ores-cli`/`oresc audit org` is read-only. It inventories repositories, loads this manifest, validates declarations and supersessions, checks live repository visibility/existence, and evaluates mirror pointers. Creation, visibility changes, provider changes, document updates, and other mutations remain separate explicit, reviewable operations.

## Current non-destructive migration rule

Both `sonus-auris-infra` and `sonus-auris.infra` remain recorded until the existing consolidation issue identifies the successor, inventories unique work, and supplies a semantic salvage plan. This manifest does not delete, archive, rename, or silently choose between them.
