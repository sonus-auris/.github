# `sonus-auris` repository relationships

Generated from reviewed policy and the current **public** repository inventory.

- Public repositories declared: **4**
- Private repository names withheld: **15**
- Relationship edges: **8**

## Repository roles

| Repository | Role | Lifecycle |
|---|---|---|
| [`.github`](https://github.com/sonus-auris/.github) | `organization_governance` | `active` |
| [`sonus-auris-ui.dart`](https://github.com/sonus-auris/sonus-auris-ui.dart) | `application` | `active` |
| [`sonus-auris-site.web`](https://github.com/sonus-auris/sonus-auris-site.web) | `site` | `active` |
| [`sonus-auris-orm-core`](https://github.com/sonus-auris/sonus-auris-orm-core) | `library` | `active` |

## Declared edges

| From | Relationship | To | Status/basis |
|---|---|---|---|
| `organization://sonus-auris` | `coordinates_via` | `capability://fiducia-cloud/distributed-coordination` | `platform-default` / `explicit-platform-decision`: locks, leases, idempotency, elections, schedules, budgets, and task claims |
| `organization://sonus-auris` | `authenticates_via` | `capability://shared-auth/human-identity` | `platform-default` / `explicit-platform-decision`: platform human identity and session authority |
| `organization://sonus-auris` | `uses_capability` | `organization://3FA-app` | `declared` / `explicit-product-decision`: step-up authentication and trusted-device recovery |
| `organization://sonus-auris` | `deployed_via` | `platform://ORESoftware/k8s-cluster` | `platform-default` / `platform-policy`: immutable artifacts are promoted by digest through GitOps |
| `organization://sonus-auris` | `packaged_via` | `platform://zed-pkg` | `platform-default` / `platform-policy`: Zed resolves artifacts while submodules compose editable source |
| `sonus-auris/.github` | `governs` | `sonus-auris/sonus-auris-orm-core` | `inferred` / `role-convention`: organization defaults, safety, and relationship declarations |
| `sonus-auris/.github` | `governs` | `sonus-auris/sonus-auris-site.web` | `inferred` / `role-convention`: organization defaults, safety, and relationship declarations |
| `sonus-auris/.github` | `governs` | `sonus-auris/sonus-auris-ui.dart` | `inferred` / `role-convention`: organization defaults, safety, and relationship declarations |

## Composition, service, and observability contract

Git submodules compose editable source; Zed packages resolve packages/artifacts; dual-managed commits must match. Production deploys immutable image digests, not runtime source builds. Cross-service access uses APIs/SDKs/events rather than another service database. MCP uses the product API/SDK. Services emit OpenTelemetry traces, bounded metrics, and correlated structured logs.

## Privacy boundary

This public registry deliberately omits private repository names and edges; the count above makes the boundary explicit.
