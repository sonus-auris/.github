# Shared ORM Layer — `*-orm-core` / `*-lib-core` Rust adapters

**Status:** Revised 2026-08-29 (aligns with dual-source persistence plan)  
**Extends:** [`SERVICE_AND_DATA_ARCHITECTURE.md`](../SERVICE_AND_DATA_ARCHITECTURE.md) and [`PERSISTENCE_DUAL_SOURCE.md`](PERSISTENCE_AUTHORITY.md).

> **Persistence authority (2026-08-29):** Product SQL and ORM generation are owned in this org’s `*-lib-core` under the dual TypeSpec (P0) + authored JSON Schema (P1) model. Diesel + diesel-async is the primary Rust runtime; SeaORM is secondary. See [`PERSISTENCE_DUAL_SOURCE.md`](PERSISTENCE_AUTHORITY.md). Claims that `ORESoftware/k8s-libs-and-shared-defs` authors this org’s product tables, or that SeaORM is the sole Rust ORM / schema authority, are superseded for product persistence.

## Decision

> **Partial supersession (2026-08-29):** Product schema authority and ORM primacy are redefined in [`PERSISTENCE_AUTHORITY.md`](../PERSISTENCE_AUTHORITY.md) and Linear [general-migration-plan](https://linear.app/denman/document/general-migration-plan-f76fadd4cbb2) revision f. End state: TypeSpec (P0) + authored JSON Schema (P1) in `sonus-auris-lib-core`; Diesel primary / SeaORM secondary; SQL/ORM generation leaves `k8s-libs-and-shared-defs`. This document’s web/API capability split and “migrations are not part of orm-core” rules remain in force.


Because both the web server and the API server read from the database, Rust ORM adapters are shared through the org’s data-plane package rather than duplicated in each service:

- **Canonical home is `sonus-auris/sonus-auris-lib-core`.** A standalone `sonus-auris-orm-core` may remain as a generated compatibility package; it must not author schema or desired.sql.
- **Primary Rust runtime:** [Diesel](https://diesel.rs/) + diesel-async, generated from the reconciled TypeSpec release lineage after dual-source parity.
- **Secondary Rust runtime:** [SeaORM](https://www.sea-ql.org/SeaORM/), generated from scratch databases built from both TypeSpec and JSON Schema candidates, then published from the TypeSpec lineage after compare.
- **Schema authority is in-org:** TypeSpec + authored JSON Schema + extensions SQL inside `sonus-auris-lib-core`. `ORESoftware/k8s-libs-and-shared-defs` keeps platform SQL and the fleet catalog only after cutover—not this org’s product table bodies.

## Boundaries

- **API server** consumes the full read/write surface (Diesel primary; SeaORM secondary where still required).
- **Web server** consumes only the read-only surface: named, policy-aware query functions. No raw Diesel/`DatabaseConnection`, unrestricted query builder, or public entity manager in web request handlers. Web still uses a `SELECT`-only database identity.
- **Migrations are not part of `*-orm-core`.** Desired-state SQL and `dpm` apply live in `*-lib-core` + a migrator Job via [`declarative-migrations`](https://github.com/declarative-migrations). SeaORM/Diesel must not run DDL at process boot.
- **Versioning:** API and web pin the same `sonus-auris-lib-core` digest; schema expand/contract is a lib-core event.

## Rationale

A shared data-plane package fixes entity/mapping drift between the two consumers of the same schema. Dual TypeSpec/JSON Schema authorship catches generator and model defects before `dpm` apply. The build-time coupling trade-off is managed via Zed digests and expand/contract release discipline.
