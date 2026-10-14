# S24 pre-correction recovery: independent data-only audit

VERIFIED for the local data-only archive. Combined R2 remains RED; promotion HOLD and all seven qualification gates UNKNOWN.

Archive: CRYPTALIS_S24_PRECORRECTION_EVIDENCE_ADDON_20261014_v2.tar.xz
Bytes: 1,061,420
SHA256: d2402a5055be7cb2e56c169be771e10d3f26f90ac2ebd0a8efdc511d2c9af5b8

## Independently checked

- All 1,030 members are unique regular files with canonical relative paths, no parent traversal, absolute paths, backslashes, links or special files.
- All 1,029 payload-manifest entries match exact bytes and hashes. The sole non-manifested member is the payload manifest itself, covered by the archive hash. The inventory and allowlist agree on all 1,022 captured inputs. Freeze inventory hash matches.
- Raw tests/package-origin/readiness/start/stop JSON and associated private logs, credentials paths, Git/cache/virtualenv internals and S24 R3 correction packets are absent. Twenty legacy producer artifacts are JUnits only; producer request/ready/release/cleanup payloads are not archived.
- A separate scan across all 1,030 members checked private-key headers, credential-bearing service URLs, GitHub tokens, AWS access IDs and OpenAI key shapes. No unresolved match. Reviewed matches are exact synthetic fixture URLs at invalid.example in test source and the archival builder's literal allowlist. This is a bounded pattern review, not a universal secret-free guarantee.
- Independently materialized all four historical source variants in this review directory, strictly as data. All 856 files match their four 214-entry manifests and expected manifest hashes. No archived script, product module or test was loaded or executed.
- Reverified the existing 214-file S23 R3 source base and compared every reconstructed source entry with that base. Default-planner variant changes migration and two fixture files; safe-display variant changes migration/deprotection; history variant changes deprotection; combined R2 changes migration/deprotection and two fixture files. No base source path is missing. Detailed per-file deltas are in AUDIT_v1.json.
- All five prior checkpoint pointer hashes reverify against local archive/receipt bytes. This establishes local continuity, not independent authentication of any remote Git state.

## Failed-run preservation

The archive contains the completed combined-R2 SA21 aggregate JUnit: 2,638 ordinary testcase elements, 33 failures, no errors/skips. Thus 2,605 ordinary cases pass. The suite reports 2,694 total events, consistent with the captured additional 56 passing subtests. Captured result metadata keeps seven baseline failures, 26 pass-to-fail changes, SA20 aggregate NOT_RUN_WITHHELD, and later test-oracle/product fixes EXCLUDED. No later correction is substituted for the failed source/evidence boundary.

V1 inventory documents remain historical preparation records and can say not yet frozen; v2 freeze/inventory and this exact archive are the new snapshot. Retaining those earlier records is deliberate provenance, not a claim that their contemporaneous status is current.

## Limits

This verifies local recoverability of selected historical source/evidence bytes. It does not restore dependencies, credentials, provider or database state, installed distributions, or a working environment. It does not make failed tests pass or qualify any product behavior. The embedded remote readback receipt is preserved, not independently authenticated by this audit. No DB, test, restored-code, Git or publication action was performed.

AUDIT_v1.json contains exact counts, source reconstruction hashes/deltas, checkpoint continuity and captured result metadata. PATTERN_SCAN_v1.json records safe match classifications without exposing credentials.
