# GitHub Copilot repository instructions

`/agents.md` is the canonical policy for this repository. Read and follow it in full.

- avoid git rebase in favor of git merge.
- Resolve every conflict semantically. Read both sides and surrounding code, docs, tests, schemas, generated artifacts, and contracts; inspect 3–10 relevant prior commits when useful; and review related repositories in **sonus-auris** and relevant external organizations when behavior crosses boundaries.
- Never accept `ours` or `theirs` wholesale, discard unfamiliar work, force-push, rewrite history, use destructive Git/filesystem/data/infrastructure operations, bypass review, or bypass required checks.
- Leave unrelated work untouched. Prefer additive branches, explicit staging, dry runs, backups, reversible roll-forward changes, and normal non-force pushes.
- Never expose secrets or sensitive data. Scan for conflict markers and credential patterns, run relevant validation, and document evidence and tradeoffs.
- Link substantial work to Linear: https://linear.app/denman/project/githubcomsonus-auris-a557165528ef
