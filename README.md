# sonus-auris organization defaults

This public `.github` repository is the canonical home for **sonus-auris** organization profile content, community-health defaults, contribution guidance, issue and pull-request templates, reusable policy checks, and public agent-safety declarations.

- GitHub organization: https://github.com/sonus-auris
- Linear project: https://linear.app/denman/project/githubcomsonus-auris-a557165528ef
- Organization profile source: [`profile/README.md`](profile/README.md)
- Canonical lowercase agent policy: [`agents.md`](agents.md)
- Compatibility mirror: [`AGENTS.md`](AGENTS.md)
- Copilot instructions: [`.github/copilot-instructions.md`](.github/copilot-instructions.md)
- Portable validator: [`scripts/validate-agent-policy.sh`](scripts/validate-agent-policy.sh)

## Canonical service/data architecture

- [`*-lib-core` data plane and Rust web/API boundary](LIB_CORE_AND_SERVICE_BOUNDARIES.md)
- [Full service and data architecture](SERVICE_AND_DATA_ARCHITECTURE.md)

## Generated organization context bundle

The reviewed central registry identified by the immutable commit in [`project-context.yaml`](project-context.yaml) is the source of truth for the generated, public-safe organization context. These managed artifacts must not be edited independently:

- `project-context.yaml` records the GitHub owner ↔ Linear project mapping and registry provenance.
- `org-context-manifest.json` records deterministic SHA-256 hashes for every other managed file.
- `agents/org-context.agent.md` provides the organization-level GitHub Copilot custom-agent profile.
- `.github/workflows/org-context-integrity.yml` verifies this mirror against the immutable central registry commit.

The generated profile and custom-agent context carry the mandatory semantic Git conflict-resolution policy described below.

## Mandatory operating policy

All contributors and agents must resolve Git conflicts semantically and with full context, normally reviewing 3–10 relevant prior commits when useful and inspecting related repositories across this organization and relevant external organizations. Never hastily choose `ours` or `theirs`; preserve compatible intent and validate the conceptual merge.

**avoid git rebase in favor of git merge.** Agents must operate in deny-by-default non-destructive mode. `git stash`, `git reset`, `git clean`, `git filter-repo`, force pushes, history rewrites, recursive deletion, destructive database or infrastructure operations, release deletion, and equivalent state-destroying actions are prohibited. See [`agents.md`](agents.md) for the complete policy.

## What GitHub inherits

GitHub can use a public organization `.github` repository as the fallback source for supported community-health files and can render `profile/README.md` on the organization page. Issue templates and pull-request templates here provide defaults when an individual repository does not define its own.

`agents.md`, compatibility instruction files, branch protections, repository settings, and workflows are **not automatically inherited merely because they exist here**. Every repository must carry compatible agent instructions, and repositories must explicitly call the reusable policy workflow where enforcement is desired.

Pin reusable workflows to a reviewed immutable 40-character commit SHA:

```yaml
jobs:
  agent-policy:
    uses: sonus-auris/.github/.github/workflows/agent-policy.yml@<reviewed-40-character-commit-sha>
```

Run the local baseline before opening a pull request:

```sh
bash scripts/validate-agent-policy.sh
bash tests/agent-policy-validator.sh
```

Repository-local policy may be stricter—particularly around audio consent, privacy, evidence integrity, encryption, retention, and app-store compliance—but must not weaken the organization baseline.

<!-- ore-org-baseline:begin -->
## Organization-wide defaults

This public repository is the canonical source for GitHub-supported community-health fallbacks, organization profile content, contribution guidance, public security/support policy, issue and pull-request templates, and agent-governance declarations for [`sonus-auris`](https://github.com/sonus-auris).

## Canonical organization links

- GitHub organization: https://github.com/sonus-auris
- Public organization defaults: https://github.com/sonus-auris/.github
- Canonical Linear project: https://linear.app/denman/project/githubcomsonus-auris-a557165528ef
- Fleet tracking issue: https://github.com/ORESoftware/k8s-cluster/issues/1222

## Safety baseline

All Git conflicts must be resolved semantically with full historical, repository-wide, organization-wide, and relevant external-organization context. Automated agents are hard-denied from destructive or history-rewriting operations, including all forms of `git stash`, `git reset`, `git clean`, `git filter-repo`, force pushing, destructive deletion, data or infrastructure teardown, credential revocation, and policy bypass.

## GitHub inheritance boundary

GitHub can use supported community-health files from a public organization `.github` repository as fallbacks and can render `profile/README.md` on the organization page. `agents.md`, `AGENTS.md`, Copilot instructions, workflows, settings, rulesets, branch protections, permissions, and secrets are not automatically inherited merely because they exist here. Each repository must carry or synchronize compatible local policy and explicitly call reusable workflows where enforcement is required.

Generated managed-policy version: `2026-08-08`.
<!-- ore-org-baseline:end -->
<!-- BEGIN MANAGED REPOSITORY RELATIONSHIPS v1 -->
## Repository relationship registry

`sonus-auris` declares repository roles, dependency edges, cross-organization capabilities, deployment ownership, and the git-submodule/Zed-package contract:

- [Human-readable map](architecture/REPOSITORY_RELATIONSHIPS.md)
- [Machine-readable manifest](architecture/repository-relationships.json)
- [JSON Schema](architecture/repository-relationships.schema.json)

The public registry withholds private repository names and edges.
<!-- END MANAGED REPOSITORY RELATIONSHIPS v1 -->
