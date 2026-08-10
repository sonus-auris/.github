# Sonus Auris

Sonus Auris builds privacy-conscious, cross-platform systems for audio capture, indexing, retrieval, transcription, evidence preservation, and recording workflows. The organization covers user-facing applications, service components, synchronization, shared contracts and clients, infrastructure, and end-to-end validation.

This page is the public orientation point for people and authorized AI agents. Repository-specific READMEs and instructions remain authoritative for implementation details.

## Start here

### For people

- Explore the [public application repository](https://github.com/sonus-auris/sonus-auris-ui.dart) and [public website repository](https://github.com/sonus-auris/sonus-auris-site.web).
- Use the [canonical Linear project](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef) for planning, priorities, and delivery context.
- Read the organization [contribution guide](https://github.com/sonus-auris/.github/blob/main/CONTRIBUTING.md), [governance notes](https://github.com/sonus-auris/.github/blob/main/GOVERNANCE.md), [support guide](https://github.com/sonus-auris/.github/blob/main/SUPPORT.md), and [security policy](https://github.com/sonus-auris/.github/security/policy).
- Start in the README and local instructions of the exact repository being changed; this profile is an index, not a substitute for repository documentation.

### For AI agents

1. Read [`project-context.yaml`](https://github.com/sonus-auris/.github/blob/main/project-context.yaml) for the canonical GitHub owner and Linear project identity.
2. Read [`repository-relationships.json`](https://github.com/sonus-auris/.github/blob/main/repository-relationships.json) before inferring repository dependencies, ownership, or routing.
3. Read the organization [`AGENTS.md`](https://github.com/sonus-auris/.github/blob/main/AGENTS.md), [`ORG_CONTEXT.md`](https://github.com/sonus-auris/.github/blob/main/ORG_CONTEXT.md), and every applicable repository-local `AGENTS.md`, `agents.md`, Copilot instruction, and path-specific instruction.
4. Resolve the exact repository explicitly. Sonus Auris has no reviewed default runtime repository, so ambiguous work must stop rather than be guessed.
5. Keep private repository content, recordings, credentials, customer information, incident details, and operational topology out of public outputs.

## Canonical identity and authority

- GitHub organization: [`sonus-auris`](https://github.com/sonus-auris)
- Immutable GitHub owner ID: `292916213`
- Linear project: [`github.com/sonus-auris`](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef)
- Immutable Linear project ID: `40905103-ae88-4186-9cff-858b7b9384d2`
- Linear team: `DEN` (`eb8ab169-5afe-4b6f-9cab-3f2aa3e887dc`)
- Organization defaults and public policies: [`sonus-auris/.github`](https://github.com/sonus-auris/.github)
- Immutable central registry: [`ORESoftware/ai-agent-coordinator.rs/config/org-project-registry.yaml@d3e03ecc`](https://github.com/ORESoftware/ai-agent-coordinator.rs/blob/d3e03ecc2e175a7f6261523d35c73ac775c49942/config/org-project-registry.yaml)

The reviewed central registry is authoritative for GitHub/Linear identity and routing. Repository-local instructions are authoritative for builds, tests, architecture, migrations, and implementation. Missing or contradictory context must be reported and resolved; it must not be invented.

## Operating principles

- Treat consent, privacy, recording integrity, retention, encryption, and evidence provenance as product requirements, not optional polish.
- Preserve recordings, metadata, indexes, keys, and user state non-destructively. Do not use history rewrites, blanket resets, destructive cleanup, or wholesale side selection to make a change appear simple.
- Keep application code and infrastructure repositories separate. An `*-infra` repository does not belong under a monorepo `apps/` directory as a Git submodule.
- Link substantial work to Linear and a GitHub issue or pull request so humans and agents can recover intent.
- Resolve Git conflicts semantically: inspect the merge base, both sides, path-scoped history, and 3–10 relevant commits when available; read linked issues, pull requests, tests, schemas, migrations, architecture decisions, and relevant same-organization or external repositories. Never accept `ours`, `theirs`, current, or incoming wholesale without conceptual review.
- Preserve compatible intent, APIs, schemas, tests, documentation, security controls, and operational safeguards from every relevant side, then scan the complete worktree for unresolved conflict markers and run all affected validation.

## Public context boundary

This profile and the `.github` repository are intentionally public. They may contain public identifiers, links, policies, and operating guidance. They must not contain credentials, private recordings, customer data, legal evidence, private issue content, incident details, security-sensitive topology, or unpublished business information.

<!-- org-project-routing:start -->
## Planning and delivery

- [GitHub Project: sonus-auris-project](https://github.com/orgs/sonus-auris/projects/1)
- [Linear planning project](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef)
- [Detailed project-routing contract](../docs/PROJECTS.md)

GitHub owns code and delivery evidence; Linear owns planning and dependencies. The linked organization Project provides the cross-repository execution view.
<!-- org-project-routing:end -->

<!-- ore-org-baseline:begin -->
## Planning and governance

- Canonical Linear project: https://linear.app/denman/project/githubcomsonus-auris-a557165528ef
- Organization defaults: https://github.com/sonus-auris/.github
- Canonical agent policy: https://github.com/sonus-auris/.github/blob/main/agents.md
- Security policy: https://github.com/sonus-auris/.github/security/policy

Repositories in this organization use semantic conflict resolution with 3–10 relevant prior commits when useful, full cross-repository context, pull-request delivery, and a hard automated-agent denylist for destructive or history-rewriting operations.
<!-- ore-org-baseline:end -->

<!-- BEGIN MANAGED REPOSITORY RELATIONSHIPS v1 -->
## Repository relationship registry

`sonus-auris` declares repository roles, dependency edges, cross-organization capabilities, deployment ownership, and the git-submodule/Zed-package contract:

- [Human-readable map](architecture/REPOSITORY_RELATIONSHIPS.md)
- [Machine-readable manifest](architecture/repository-relationships.json)
- [JSON Schema](architecture/repository-relationships.schema.json)

The public registry withholds private repository names and edges.
<!-- END MANAGED REPOSITORY RELATIONSHIPS v1 -->
