# Sonus Auris web/API connection patterns

Status: organization architecture guidance, tracked by [DEN-4259](https://linear.app/denman/issue/DEN-4259/document-sonus-auris-webapi-connection-patterns).

This policy applies to traditional customer web/BFF, API, worker, catalog, device-management, and authorized audio/telemetry services. Repository ADRs may narrow it but may not weaken the security and data boundaries.

## Four supported avenues

| Avenue | Appropriate use | Boundary |
| --- | --- | --- |
| Direct database read | Named, stable, non-sensitive public/read-model projection with a measured need | Never identity, device ownership, private audio/health-adjacent data, billing, or writes; require a distinct `SELECT`-only, `READ ONLY`, non-owner, `NOBYPASSRLS` role |
| Stateless HTTP/JSON | Default for synchronous web-to-API work | Required for customer-private reads, authorization decisions, commands, billing, and all mutations |
| Stateful TCP | Authorized low-latency media or high-frequency telemetry stream after API authorization | Not a persistence, billing, or authorization authority; require ADR, mTLS/delegated identity, bounded frames, deadlines, backpressure, and reconnect rules |
| NATS/message queue | Durable post-commit side effects and fan-out | Never login, interactive authorization, payment approval, or an immediate user response; require an outbox and idempotent consumers |

Stateless HTTP is the default. A direct read, TCP stream, or message flow is a named exception for a specific access pattern, not an interchangeable transport preference.

## Decision and ownership

1. Customer-private data, product authorization, billing, device ownership, and every mutation go through the API over HTTP.
2. An immediate authoritative answer goes through HTTP.
3. A durable post-commit effect goes through a transactional outbox and NATS.
4. A measured media/telemetry stream may use stateful TCP after an ADR and an API-issued authorization decision.
5. Direct database access remains limited to documented public/read projections under a restricted read role.

The web/BFF owns HTML, secure opaque sessions, CSRF, and authorization-code plus PKCE login. The API owns product authorization, writes, commands, and versioned interfaces. A core/data library owns typed queries and mappings. The canonical migration repository owns DDL; application processes verify schema compatibility and never migrate production at startup.

Shared Auth proves identity and assurance, not Sonus Auris product permissions. Validate realm, issuer, audience, tenant, app/client, scopes, session, freshness, and assurance. Protected introspection uses a service credential for the service call and keeps the user's token distinct in the request body. Never log tokens, cookies, codes, PKCE verifiers, audio payloads, or provider secrets.

Pin official Shared Auth clients immutably. Use `opto-sync` only for declared synchronization/outbox workflows, `ores-otel` for bounded/redacted telemetry, and `zed-pkg` for dependency provenance. These tools do not relocate authorization or schema ownership.

## Operational requirements

- Bound HTTP bodies, TCP frames, deadlines, retries, and buffers. Propagate correlation and trace context.
- Require idempotency keys for mutations and idempotent message consumers.
- Fail closed; the BFF must never replace a failed API authorization with a direct query.
- Treat media-stream authorization as short-lived and resource-specific; re-authorize on reconnect or expiry.
- Use a signature-verified, replay-safe webhook—not a browser redirect—as payment-settlement evidence.
- Record an owner and review/expiry date for every direct-read or TCP exception.

Code comments at each call site should name the chosen avenue and the domain reason. This document is the durable organization decision policy.
