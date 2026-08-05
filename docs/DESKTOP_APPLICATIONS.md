# Desktop application allocation

Verified **2026-08-05**.

Sonus Auris has a live paired native desktop product plus an additional Flutter device console:

- Rust product app: [`sonus-auris/desktop.app.rs`](https://github.com/sonus-auris/desktop.app.rs) — **live**.
- Flutter product app: [`sonus-auris/sonus-auris-ui.dart`](https://github.com/sonus-auris/sonus-auris-ui.dart) — **live**.
- Additional Flutter device console: [`sonus-auris/sonus-auris-web-desktop.dart`](https://github.com/sonus-auris/sonus-auris-web-desktop.dart) — **live**, related operator surface rather than a replacement for the canonical product pair.

Repository-local contracts were merged through:

- Rust product app [PR #29](https://github.com/sonus-auris/desktop.app.rs/pull/29)
- Flutter product app [PR #66](https://github.com/sonus-auris/sonus-auris-ui.dart/pull/66)
- Additional console [PR #11](https://github.com/sonus-auris/sonus-auris-web-desktop.dart/pull/11)

## Product boundary

The canonical Rust and Flutter apps should maintain semantic parity for recording schedules, microphone and file permissions, capture state, retention, encryption boundaries, playback, search, export, local storage, device/session state, recovery, and notifications. The additional console must be assessed whenever device-control or shared desktop-visible behavior changes.

The Rust and Flutter product apps remain independently buildable, testable, releasable applications. Shared schemas, clients, media/encryption fixtures, device-state models, sample recordings, and conformance tests should be versioned deliberately.

## Feature-delivery rule

Every desktop-facing change must inspect both canonical product apps, define shared acceptance criteria, update both or record an explicit no-change rationale, assess the additional console, and report Rust, Flutter-product, and console status separately.

## Project routing

- GitHub Project: [`sonus-auris-project` — Project 1](https://github.com/orgs/sonus-auris/projects/1)
- Linear project: `github.com/sonus-auris`
- Central registry: [`ORESoftware/project-registry`](https://github.com/ORESoftware/project-registry/blob/main/registry/desktop-applications.json)
- Portfolio rollout: [`DEN-2469`](https://linear.app/denman/issue/DEN-2469/roll-out-paired-rust-flutter-desktop-repositories-across-the-portfolio)

Renames, transfers, archival, platform-status changes, or changes to which Flutter app is canonical must update this document, Linear, the central registry, and all three repositories together.
