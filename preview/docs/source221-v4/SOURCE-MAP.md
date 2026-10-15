# Source map and documentation provenance

All source paths below are relative to frozen `candidate-cluster-retained-integrated-v2-20261015`, whose 221-file manifest SHA-256 is `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`. References were statically read, not imported or executed. Public signatures and lifecycle distinctions take precedence over historical API illustrations in the source README.

| Guide claim | Inspected source |
|---|---|
| Dependency declaration, version and build backend | `pyproject.toml` |
| Manifest grammar; unique-implies-equality; routine_allowlist | `src/cryptalis/manifest/declaration.py:113–179` |
| Writer / WriterInventory / SearchReview records | `src/cryptalis/manifest/compiler.py:26–45` |
| Public crypto/provider exports | `src/cryptalis/crypto/__init__.py` |
| KeyContext, WrappedRoot, create_root, KeyPolicy, Keyring | `src/cryptalis/crypto/keys.py:120–175,230–308` |
| Explicit create/open; private-file refusal; no regeneration | `src/cryptalis/crypto/development_file.py:1–145` |
| Advisory doctor/setup and active bounded-audit interface | `src/cryptalis/doctor.py:12–70` |
| DeploymentPin / MaintenanceApproval | `src/cryptalis/migration.py:56–69` |
| Read-only plan, safe default and explicit-false refusal | `src/cryptalis/migration.py:310–383` |
| apply, pre-switch verify, abort | `src/cryptalis/migration.py:825–903` |
| Exact lock-based sync/async attach | `src/cryptalis/sqlalchemy.py:1199–1259` |
| PlaintextApproval / RemovalApproval; reverse plan | `src/cryptalis/deprotection.py:113–180` |
| Cutover, reverse apply/abort, remove and removed-state check | `src/cryptalis/deprotection.py:432–558` |
| Versioned designation capture/check/restore | `src/cryptalis/_cluster_designation.py` |
| Conditional legacy recovery and retained-index reverse abort | `src/cryptalis/_legacy_designation.py` |
| Public synthetic IDs/mapping/manifest and native CRUD example | `tests/test_migration.py:31,88–185` |
| Threat/leakage and authority contracts | `docs/security.md`, `docs/architecture/README.md` |
| Lifecycle/compatibility scope and dated claims | `docs/lifecycle.md`, `docs/compatibility.md`, `docs/status.md` |
| Approved scope and ordered work | `docs/decisions.md`, `docs/build-guide.md` |

The guide adapts exact API shapes into new prose/examples; it does not claim those compositions ran. Current evidence counts and delivery state come from the coordinator and the authoritative checklist front section read on 15 October 2026 after its 14:07 reconciliation. OBJECTIVES.md preserves every one of its 34 objective IDs and full capability descriptions; it is a read-only delivery appendix, not a replacement authority.

The earlier `preview-docs-v2-20261015` is unchanged. This revision replaces stale current-candidate claims in a fresh directory. It adds explicit pending package bindings, the installed/source distinction, corrected legacy/default guidance and an unpromoted README proposal. Source221 and the authoritative checklist were not edited.

The independent packaging review and ACTUAL_ARTIFACTS.json were separately metadata-admitted, read and rehashed. Their exact project-relative paths and digests are in DELIVERY-BINDING.json. The guide inherits the accepted distribution hashes from those records; it did not re-open/re-audit the wheel or sdist.

The documentation checksum file covers only this directory's deliverable text/JSON bytes. It is not a package/source/dependency hash, signature or execution receipt.
