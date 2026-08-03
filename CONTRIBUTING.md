# Contributing

Thank you for contributing to sonus-auris.

## Before starting

1. Read [`AGENTS.md`](AGENTS.md), [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md), and [`SECURITY.md`](SECURITY.md).
2. Find or create the relevant work item in the [sonus-auris Linear project](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef).
3. Confirm the affected repositories, audio/data contracts, generated artifacts, infrastructure, supported platforms, retention behavior, consent requirements, and deployment boundaries.

## Non-destructive workflow

Leave unrelated and uncommitted work untouched. Agents and automated contributors must not use `git stash`, `git reset`, `git clean`, `git filter-repo`, history rewrites, force pushes, recursive deletion, destructive database or infrastructure commands, or equivalent operations. Use additive branches, clean worktrees or clones, explicit staging, normal pushes, dry runs, and reversible roll-forward changes.

Never destroy or rewrite recordings, transcripts, evidence metadata, encryption material, or user data to simplify development or testing. Use synthetic fixtures and isolated test storage.

## Conflicts

Resolve every conflict semantically. Read both sides and the surrounding subsystem; inspect 3–10 relevant prior commits when useful; review related organization and external repositories when contracts cross boundaries; preserve compatible intent; run relevant validation; and explain tradeoffs in the pull request.

## Pull requests

Keep each pull request coherent and reviewable. Include:

- the linked Linear issue or project;
- the problem and intended outcome;
- important implementation and architecture choices;
- compatibility, migration, privacy, consent, security, evidence-integrity, and operational risks;
- tests, checks, and physical-device or end-to-end validation performed;
- conflict-resolution details, when applicable.

Never commit secrets, recordings, transcripts, production data, personal data, generated credentials, or local environment files.
