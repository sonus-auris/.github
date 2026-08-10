<!-- ore-org-baseline:begin -->
## Summary

Describe the behavior, intent, affected repositories or contracts, and user or operator impact—not only the files changed.

## Planning and dependencies

- Linear project or issue (required, for example `DEN-123`): [github.com/sonus-auris](https://linear.app/denman/project/githubcomsonus-auris-a557165528ef)
- Related GitHub issues or pull requests:
- Related repositories or external contracts:

## Risk, security, migration, and rollback

- User or operational impact:
- Security/privacy impact and secret-handling review:
- Migration or compatibility considerations:
- Rollback or recovery approach:

## Validation

List exact commands, environments, and results. Include unit, integration, contract, build, and end-to-end evidence as applicable.

## Safe-change checklist

- [ ] Scope, acceptance criteria, dependencies, and validation evidence are synchronized with the canonical Linear issue.
- [ ] The worktree was inspected before mutation and publishing; unfamiliar, uncommitted, and untracked work was preserved.
- [ ] I followed **avoid git rebase in favor of git merge** and did not rewrite shared history.
- [ ] No prohibited destructive Git or filesystem command, force-push, check bypass, or security-control disablement was used.
- [ ] Newly discovered features, fixes, bugs, vulnerabilities, reliability concerns, documentation gaps, and technical debt have linked Linear issues.
- [ ] Remote state was fetched before editing and before pushing.

## Semantic conflict-resolution checklist

Resolve conflicts semantically and with full context; never clear conflict markers by hastily selecting a side.

- [ ] The merge base, both sides, surrounding implementation or documentation, and affected tests and contracts were inspected.
- [ ] When history was available, 3–10 relevant commits from both sides were reviewed with path-scoped history and blame where useful.
- [ ] Related Sonus Auris repositories and relevant external-organization repositories were reviewed for cross-repository APIs, schemas, generated artifacts, infrastructure, or behavior.
- [ ] A conceptual merge preserved compatible intent; neither `ours`/current nor `theirs`/incoming content was accepted wholesale.
- [ ] The complete worktree was scanned for unresolved conflict markers.
- [ ] Affected tests and validation checks were run after resolving conflicts.
- [ ] Non-obvious decisions, incompatible requirements, discarded intent, and operational tradeoffs were documented in GitHub and Linear.
- [ ] No credentials, private data, or customer information were exposed while gathering context.

## Final checklist

- [ ] Focused commits and reviewable diff
- [ ] Documentation and generated artifacts updated from authoritative sources
- [ ] External Actions pinned to full commit SHAs
- [ ] Explicit least-privilege workflow permissions and timeouts
- [ ] No credentials, private data, or sensitive logs included
- [ ] Authoritative remote branch/PR/check evidence verified
<!-- ore-org-baseline:end -->
