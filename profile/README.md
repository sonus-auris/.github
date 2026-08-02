# sonus-auris

This organization is mapped to the Linear project [github.com/sonus-auris](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef).

## AI agent context

- GitHub owner ID: `292916213`
- Linear project ID: `40905103-ae88-4186-9cff-858b7b9384d2`
- Linear team: `DEN` (`eb8ab169-5afe-4b6f-9cab-3f2aa3e887dc`)
- Machine-readable context: [`project-context.yaml`](https://github.com/sonus-auris/.github/blob/main/project-context.yaml)
- Canonical registry: [`ORESoftware/ai-agent-coordinator.rs/config/org-project-registry.yaml`](https://github.com/ORESoftware/ai-agent-coordinator.rs/blob/7929612d92e6aa37f966326cc1a50b4dcd150f3a/config/org-project-registry.yaml)

No default repository is declared; agents must resolve the exact repository and fail closed on ambiguity.

Repository-local `AGENTS.md`, `agents.md`, and tool instructions remain authoritative for build, test, and implementation details. The central registry remains authoritative for GitHub/Linear identity and routing. Unmapped or ambiguous work must be rejected rather than guessed.

## Semantic Git conflict resolution

> resolve any and all git conflicts semantically, will full context, even looking back 3-10 commits in git log history for more context - never hastily pick sides in a conflict but merge things conceptually, using max context and complete conceptual awareness for a given github organization's repos and external org repos too

Before resolving a conflict, inspect the merge base and 3–10 relevant commits from both sides when available, including path-scoped history for every conflicted file. Read repository-local instructions, linked Linear issues, pull requests, architecture decisions, tests, migrations, schemas, and documentation. When a contract crosses repository boundaries, inspect relevant repositories in the same GitHub organization and relevant repositories in external GitHub organizations too.

Never resolve by blindly or wholesale selecting `ours`, `theirs`, current, or incoming. Produce a conceptual merge that preserves compatible intent, invariants, APIs, schemas, migrations, tests, documentation, security controls, and operational safeguards from all relevant sides. Document non-obvious decisions, scan the whole worktree for conflict markers, and run every affected validation contract. “Max context” means all relevant authorized context; it never authorizes exposing credentials, private data, or hidden reasoning.

This public repository contains identifiers, links, and public operating guidance only. Do not place credentials, private customer data, or private operational details here.
