# Persistence authority — TypeSpec, JSON Schema, Diesel, SeaORM, and dpm

**Status:** proposed org policy — 2026-09-04 (aligned to fleet revision i)
**Scope:** this GitHub organization and every database-backed product under it

**Organization:** `sonus-auris`
**Contract sources:** [`sonus-auris/sonus-auris-interfaces`](https://github.com/sonus-auris/sonus-auris-interfaces)
**Desired-state release:** [`sonus-auris/sonus-auris-lib-core`](https://github.com/sonus-auris/sonus-auris-lib-core)
**Runtime boundary:** [`sonus-auris/sonus-auris-orm-core`](https://github.com/sonus-auris/sonus-auris-orm-core)
**Migration execution:** [`sonus-auris/sonus-auris-infra`](https://github.com/sonus-auris/sonus-auris-infra)
**Org note:** the current `public` versus `sonus_auris` namespace evidence is unresolved and remains a release gate. Ownership extraction must not silently redesign the namespace.

**Fleet plan:** [general-migration-plan](https://linear.app/denman/document/general-migration-plan-f76fadd4cbb2)
**Execution:** [DEN-3321](https://linear.app/denman/issue/DEN-3321), [ORESoftware/k8s-libs-and-shared-defs#54](https://github.com/ORESoftware/k8s-libs-and-shared-defs/issues/54)

This document supersedes older org text that names `ORESoftware/k8s-libs-and-shared-defs` as the human-authored **product** SQL/ORM generation authority, or that names SeaORM as the sole / primary Rust ORM for new product persistence work.

---

## 1. Decision

Product SQL generation, ORM generation, and dual-source validation move **out of** the shared `ORESoftware/k8s-libs-and-shared-defs` tree and into Sonus Auris repositories. There are four boundaries, not one repository that does everything.

| Tier | Source | Role |
| --- | --- | --- |
| **Peer source A** | Independently authored persistence **TypeSpec** in `sonus-auris-interfaces` | Emits SQL candidate A, Protobuf/gRPC, and TypeSpec-native interfaces/clients |
| **Peer source B** | Independently authored persistence **JSON Schema/OpenAPI** in `sonus-auris-interfaces` | Emits SQL candidate B, validators/types, HTTP interfaces, and write clients |
| **PG capability source** | Authored PostgreSQL **extension SQL** (RLS, grants, triggers, ZD00x guards, partial indexes, CDC hooks) | Shared capability layer applied to both candidates and compared by catalog definition |
| **Release owner** | `sonus-auris-lib-core` | Pins both peer sources; owns candidates, parity evidence, and certified desired state |
| **Runtime owner** | Diesel + diesel-async and SeaORM in `sonus-auris-orm-core` | Diesel is primary; SeaORM is the DB-first runtime/catalog witness |
| **Apply owner** | Reviewed DPM plan in `sonus-auris-infra` | Only production DDL path; runtime services have no migration credential |

`sonus-auris-interfaces` owns both authored contract families. It never depends on lib-core. Lib-core pins exact source revisions/digests and turns their independently generated candidates into one certifiable release.

---

## 2. Why both TypeSpec and JSON Schema/OpenAPI are primary

- They are independent authored sources at the same policy level. Neither is generated from, subordinate to, nor automatically overwritten by the other.
- TypeSpec preserves service/RPC, Protobuf, transport, decorator, and emitter semantics. JSON Schema/OpenAPI preserves JSON validation, examples, compositions, HTTP shapes, and validator/client semantics.
- Each lane independently emits SQL and its native downstream artifacts. Comparing two outputs from one AST would prove deterministic generation, not independent agreement.
- Optional cross-translations may be produced under `generated/witnesses/`, but only as diagnostics. They cannot feed production SQL, Protobuf, OpenAPI, clients, ORM code, or a release.
- A mismatch has no automatic winner. Release blocks while humans classify the difference as a source defect, emitter defect, declared loss boundary, PostgreSQL normalization, or unsupported construct; both sources and fixtures are then reconciled.

---

## 3. Dual pipeline (must converge)

```text
authored TypeSpec ──► SQL A ──► scratch DB A ──► normalized catalog A
        ├───────────► Protobuf / gRPC / wire clients
        └───────────► Diesel/SeaORM candidate metadata A

                    equality + veto gate

authored JSON Schema/OpenAPI ──► SQL B ──► scratch DB B ──► normalized catalog B
              ├───────────────► interfaces / validators / HTTP and write clients
              └───────────────► Diesel/SeaORM candidate metadata B

Required before publish:
  catalog A == catalog B   (server-normalized PostgreSQL)
  constraints, defaults, indexes, grants, RLS, triggers, and ZD00x guards agree
  ORM manifests A == B and both compile against the same release
  transport/interface mapping and negative conformance fixtures agree
  shared PostgreSQL extension definitions are identical after normalization

Then publish a peer-certified release:
  desired.sql + Diesel + SeaORM + IR + digests
        │
        ▼
  dpm plan / verify / apply  (migrator Job only)
```

Text-identical SQL is not required. Equality is semantic: normalized catalogs, ORM manifests, compile success, and shared behavior fixtures.

---

## 4. Repository roles in this org

### `sonus-auris-interfaces` (required)

Owns:

- `contracts/database/typespec/*.tsp` (authored peer A)
- `contracts/database/json-schema/persistence.schema.json` and OpenAPI overlays (authored peer B)
- Protobuf/gRPC, validator, client, and interface mappings specific to each lane

### `sonus-auris-lib-core` (required)

Owns:

- exact Zed source pins and source digests for both peer inputs
- independent SQL/catalog/ORM candidates and scratch-database fixtures
- `contracts/database/extensions/*.sql`
- generators, candidate trees, parity reports, release digests
- opaque named read/write operations
- `.zpkg.toml` / `.zpkg.lock` for schema + rust-orm (or diesel/seaorm) targets

### `sonus-auris-orm-core` (required private runtime boundary)

- Must **not** author a second schema.
- Pins one certified lib-core release and exposes bounded, named persistence operations.
- Uses Diesel + diesel-async as the primary typed runtime and SeaORM as the DB-first entity/catalog and dynamic-query witness.
- May report release compatibility and readiness; cannot select targets, hold migration credentials, or apply DDL.

### `*-api-server.rs` / `*-web-server.rs`

- Pin the same `*-lib-core` Zed digest.
- API: Diesel (primary) and/or SeaORM write profile + `__api_rw`.
- Web: read profile only + `__web_ro` (or API-mediated reads).
- **Never** run DDL, `AUTO_MIGRATE`, SeaORM `sync()`, Diesel migrate, or sqlx migrate at process boot.

### `sonus-auris-infra` migrator Jobs

- Installs the exact `sonus-auris-lib-core` schema release via Zed.
- Owns the non-secret target manifest: environment, database plane, organization namespace, desired-state digest, connection reference, plan/apply role references, lock key, maintenance policy, and receipt sink.
- Exposes `just db-plan ORG=sonus-auris ENV=<env>`, `just db-verify ...`, `just db-apply ...`, and `just db-status ...`.
- Uses a small Rust wrapper with root `.cli-flags.toml` and `flags-2-env`; credentials come only from ores-sops/Fiducia-approved channels and never CLI flags.
- Runs DPM over a direct/unpooled migration connection, acquires a lock scoped to `(organization, database plane, schema)`, verifies live-state and plan digests, applies through the sole DDL role, proves an empty post-apply diff, and writes a receipt.
- Must run a full composed-database plan when DPM cannot prove that schema selection excludes cross-namespace effects.

### `ORESoftware/k8s-libs-and-shared-defs`

Keeps **only**:

- platform / cluster-shared SQL
- org catalog (org → RDS → schema/prefix → Zed package + digest)
- NATS / Redis / non-product shared contracts
- optional verification harnesses that **resolve** org packages (do not re-author product tables)

After cutover, product table bodies and product ORM generation **do not** live here.

---

## 5. Suggested layout inside `*-lib-core`

```text
contracts/database/
  typespec/                 # authored peer A (in sonus-auris-interfaces)
  json-schema/
    persistence.schema.json # authored peer B (in sonus-auris-interfaces)
    persistence.meta.schema.json
  extensions/               # RLS, ZD00x, triggers, grants
  interface-mapping.json
generated/
  candidates/typespec/      # SQL A, ORM A, IR A
  candidates/json-schema/   # SQL B, ORM B, IR B
  witnesses/                # optional lossy projections; never production inputs
  reports/dual-source-parity.json
  release/
    sql/postgres/desired.sql
    diesel/
    sea-orm/
```

Use Zed targets such as `schema`, `rust-diesel`, `rust-seaorm` (names may vary; digests must be explicit).

---

## 6. Diesel vs SeaORM (runtime)

| Concern | Diesel + diesel-async | SeaORM |
| --- | --- | --- |
| Fleet role | **Primary** Rust runtime for new product code | **Secondary** compatibility / dynamic queries |
| Schema authorship | Generated against the peer-certified release; not a third source | Generated from each scratch DB and the certified release; not a second authority |
| Web tier | Read-only compiled surface or named reads only | Default features read-only; no write symbols in web graphs |
| Migrations | Not applied by the app; dpm owns apply | No `SchemaBuilder.sync()` / entity-first apply in prod |

Do **not** adopt Diesel (or SeaORM) as a third independently authored schema source. ORM models are release artifacts, not competing DDL.

---

## 7. Transition from today’s shared-defs pin

Until dual-source generators land in this org:

1. **Freeze** new Sonus product SQL in `k8s-libs-and-shared-defs`.
2. **Extract** it losslessly into lib-core as transitional SQL/extension provenance. Resolve `public` versus `sonus_auris` from live-catalog evidence in a separate change.
3. Independently author TypeSpec and JSON Schema/OpenAPI in interfaces; emit both SQL candidates, load two scratch databases, and turn on fail-closed parity.
4. Generate Diesel and SeaORM against the certified result and prove runtime/catalog parity.
5. Publish immutable Zed source and desired-state releases; move API/web/ORM/infra consumers to exact pins.
6. Rehearse DPM on an isolated clone/Neon branch, require reviewed plan and live-state fingerprints, then apply from infra with the scoped lock and least-privilege role.
7. Remove the central product SQL only after consumers converge and both the organization release and central removal are jointly releasable. Keep its history and any superseded branch reachable; cherry-pick unique work before retirement.

Under DEN-3146, the near-term Supabase deployment uses the shared `oresoftware` Supabase organization with only canonical and auth database planes. Sonus owns an explicit organization schema namespace and never places custom objects in provider-managed `auth`, `storage`, or `realtime` schemas. The later dedicated-project move changes only `RuntimeConfig` / `.cli-flags.toml` target configuration.

Lossless relocation, dual-source conversion, and namespace redesign are **separate** evidence-bearing changes.

---

## 8. Hard refusals

- Product SQL/ORM generation remaining forever in `k8s-libs-and-shared-defs`
- Making either authored source subordinate to the other, or using a cross-translation as a production input
- Releasing when catalogs or ORM manifests disagree
- DDL at API/web boot
- Physical FKs across org packages or across RDS instances (use logical `shared_auth_subject` + realm)
- Git-submodule of product SQL into shared-defs or `k8s-cluster` (use Zed releases)
- Treating SeaORM `sync()` or Diesel CLI migrate as production apply
- Giving `sonus-auris-orm-core`, API servers, or web servers migration credentials
- Closing an outmoded/red PR or deleting its branch before unique work has been inventoried and salvaged

---

## 9. Related org documents

- Supersedes schema-authority sections of `docs/ORM_CORE_LIBRARY.md` and updates `LIB_CORE_AND_SERVICE_BOUNDARIES.md` / `SERVICE_AND_DATA_ARCHITECTURE.md` toward dual-source + Diesel primary.

Update older ORM / service-architecture docs in this `.github` repository to point here when they still say “SeaORM-only” or “schema lives only in shared-defs.” Keep their still-valid web/API capability rules (API writes, web read-only, migrator DDL).
