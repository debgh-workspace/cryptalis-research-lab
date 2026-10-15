# Independent frozen cleanup recovery capsule review

Date: 2026-10-15 UTC.

Decision: **ACCEPT_FROZEN_DATA_ONLY_RECOVERY_CAPSULE**.

## Exact accepted identity

- Archive: `candidate-async-cleanup-recovery-20261014/CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1.tar.xz`.
- Archive SHA-256: `1c6f9900389f61826d1f1d427a0bfc94e5f3cc20fee0f758281b928a896129af`.
- Compressed bytes: 1,029,680.
- Archive members: 516 regular files, totaling 9,148,868 bytes.
- Canonical uncompressed USTAR stream: 9,543,680 bytes.
- Frozen manifest SHA-256: `e755ba583e885515848bc4334925ba57c11a03f88708f5ad2e44ee5a7792d174`.
- Exact control/member allowlist SHA-256: `8625a305e537c397a65ed75a8f113bf28c6396e6aa7c36a86f93b90907524176`.

## Independent admission and continuity

The supplied accepted input review and freeze handoff were read as review controls. Only pinned controls and archive metadata were inspected before payload admission. Independently validated all archive member names, normalized relative paths, unique sorted order, case and file/directory collision freedom, regular-file-only canonical USTAR headers, complete exact manifest/allowlist closure, complete candidate filesystem closure, parent/leaf types, all sizes, zero padding, and bounded single-stream XZ admission with CRC64 and no trailing stream/data. The 515-entry manifest excludes only its externally pinned own bytes, included as member 516. No archive extraction function was used.

All 516 member bodies match their frozen hashes and current candidate copies. All 482 exact selected originals match the accepted prepared records and their archive copies: 8,166,671 original bytes. Both authored root documents match their accepted hashes; the complete original 484-file prepared candidate remains 8,174,630 bytes. All 25 copied controls match their exact source origins, retained control inventory, and archive copies. Six separately authored controls plus the final manifest complete the 516-member partition. The candidate has only the four explicitly excluded external terminal outputs beyond that closure.

Every selected original filename and filesystem type was validated before original payload reads. The final recheck of all 482 originals, 25 control origins, all candidate members, and external archive/manifest/control pins found zero drift. Preserved scripts were treated as inert data and were never executed. The newly authored `verify_frozen_capsule.py` uses only Python standard-library data handling.

## Full-source and focused-evidence preservation

All 217 source filenames and hashes match both the retained full-source allowlist and GREEN source manifest. A data-only reconstruction using the retained baseline adapter reproduces all 217 RED hashes; removing the added test reproduces the 216-file baseline manifest. The sole RED-to-GREEN source delta remains `src/cryptalis/sqlalchemy.py`.

Safe terminal JUnit and progress records were independently reconciled against the retained ordered-node review for all four focused cells:

- RED SA 2.0: 22 nodes, 13 failures, 9 passes.
- RED SA 2.1: 22 nodes, 13 failures, 9 passes.
- GREEN SA 2.0: 46 nodes, 46 passes.
- GREEN SA 2.1: 46 nodes, 46 passes.

Every selected setup and teardown phase passes. RED node order agrees across versions; GREEN node order agrees across versions and includes the 22 RED nodes plus 24 retained regression nodes. Failure text is preserved byte-for-byte through archive/original equality; no runtime behavior was rerun.

## Deterministic second build and fresh inert restore

This reviewer implemented a new manual USTAR construction without a tar-building library or any preserved builder. It constructs canonical headers, checksums, bodies, file padding, and terminal record padding. Its entire uncompressed stream equals the accepted archive stream byte-for-byte. Independently compressing that stream with XZ preset 6 and CRC64 reproduces the entire accepted compressed archive and SHA-256 exactly.

The new second build is `CRYPTALIS_ASYNC_CLEANUP_RECOVERY_20261014_v1.independent-rebuild.tar.xz` in this review directory. Only after all admission, continuity, and payload hash checks, the new `fresh-inert-restore-v1/` directory was created exclusively. All 516 files were written and read back as regular, nonexecutable mode-0644 data. Exact file and directory closure, every restored byte, and all 217 restored GREEN source hashes pass. This establishes source and evidence byte recovery only.

## Preserved dispositions and qualification boundaries

The two accepted synthetic-fixture dispositions are unchanged at SHA-256 `640f4a4727d588a5f5b03d11941d9e482b2430dfecc12f4252a4850589c3a022`. Their existing paths and line numbers remain `source/tests/test_attachment_engine_preflight.py:24` and `source/tests/test_doctor_setup.py:84`. No matched URL or secret-shaped values are reproduced in this review. The bounded supplemental scan and its zero-unresolved-finding disposition are preserved exactly; this reviewer did not perform a new secret scan or strengthen the prior secret-absence claim.

All seven qualification gates remain UNKNOWN. The seven historical acceptance failures retain their unresolved prior disposition and were not rerun or reclassified. The currently running full-suite work is outside this frozen capsule and this review. Full-matrix and installed qualification remain separate, pending boundaries. This acceptance is not an operational environment restore, security qualification, runtime/dependency/database restore, or release/production decision. It makes no universal physical-quarantine, hostile-driver, transport, or performance claim.

No raw `tests.json`, `rawtests.json`, `readiness.json`, `package-origin.json`, `postgres-start.json`, or `postgres-stop.json` was read or hashed. No environment or credential payload, cache content, installed dependency content, runtime content, or target merely mentioned by a pin record was read. No product imports, tests, database/server operations, network operations, or Git operations occurred. Writes were confined to this new review directory. The frozen candidate, originals, and prior reviews were not changed. No publication was performed.

## Review artifacts

- `verification-summary.json`: machine-readable decision, exact identities, counts, and boundaries.
- `filename-admission.json`: exact admission closure and type/name checks.
- `original-and-control-continuity.json`: verified original and copied-control digests, with zero final drift.
- `focused-node-verification.json`: independent focused JUnit/phase reconciliation.
- `verify_frozen_capsule.py`: this reviewer's data-only implementation.
- `REVIEW_ARTIFACTS.sha256`: exact root review artifact hashes, excluding itself and the restored tree already covered by the verified frozen manifest.
