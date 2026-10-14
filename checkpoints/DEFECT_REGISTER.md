# Current Cryptalis defect register

This is a current navigation summary. The authoritative blueprint incorporates the detailed checkpoints. Historical RED receipts remain unchanged. All production gates remain UNKNOWN.

| ID | Severity | Current default product | Original mailbox | Evidence and concrete next step | Owner |
|---|---|---|---|---|---|
| ASYNC-NATIVE-BOUNDARY-01 | HIGH release blocker | OPEN: 20 canonical defect cells across five async methods, two scopes and two versions | Not corrected | CP60 and CP61. Isolated greenlet proposal passes the tested cells. Alternative outside-hook preparation has four unwanted-provider-I/O failures per version. Prototype readiness includes the installed pair. Obtain explicit preparation-contract approval, then implement and run plugin-free product/corpus/installed gates. | dot; owner approves amendment |
| FLUSH-PREFIX-01 | HIGH | Bounded uncommitted correction and removal proofs verified in lab; full product release not qualified | Defect reproduced in installed mailbox wheel | CP52/55. Keep rollback and quarantine mechanisms. Include corrected source only through an explicitly reviewed candidate, with no premature release claim. | dot |
| CORE-AUTOFLUSH-VERSION-01 | HIGH correctness | Version-specific correction and seven removal controls verified in lab | Not included | CP59. Retain Core 2.1 and Session-wide-option tests in both required cells; add future version only through a new native comparison. | dot |
| SNAPSHOT-CUTOVER-01 | HIGH data correctness | Conservative read-only old-snapshot guard verified in bounded lab | Not included | CP43. Retain guard; do not use it to qualify a heap rewrite. Broaden concurrent-reader and online-cutover proof. | dot |
| REVERSE-ORDINAL-01 | HIGH compatibility | Dependency-free text suffix correction only | Reverse lifecycle not included | CP45/46. Generic metadata, non-text suffixes, dependencies and ACL reconstruction remain mandatory. CP62 native ACL prototype is not integrated. | dot; owner approves ACL authority |
| ACL-RECONSTRUCTION-01 | HIGH if generalized without safeguards | Generic reconstruction remains blocked | Not included | CP62. New object defaults can add rights; foreign grantors and owner revocations require precise handling. Complete omission proofs, pre-DDL capability admission and dependency inventory before proposing product replay. | dot |

The CP61 interleaved failures are variants of ASYNC-NATIVE-BOUNDARY-01, not 16 new distinct bugs. The initial CP61 before_flush fixture failure is excluded from product defect counts because the native fault was injected outside native flush rollback handling. The alternative's extra provider calls are a prototype limitation, not evidence of a confidentiality break.

Research-only defect ONLINE-SEED-ABA-01: delayed initial seeding can reuse a retired marker and revalidate an old worker. CP65 shows four real-PostgreSQL data mismatches and a matching finite-model trace. Fresh work identities and separate source-revision comparison each close the executed schedules; complete online migration remains unadmitted. This is not a defect in an existing product online feature. Owner: dot. Next: coverage, visibility and recovery proof before any scan-equivalence decision.

## CP66 cache design boundary (research-only)

Caching a complete admission decision solely from `CacheKey.key` is unsafe: ordinary/callable and expanding/nonexpanding bind forms can share a structural key while requiring different admission decisions. Impact: an unchecked prototype can accept a form the current guard refuses. The current product has no verdict cache. Mitigation: retain invocation-local shape checks and never retain operation context. CP66 tests and removal proofs cover the known variants; custom cache participants and mutable mappings remain explicit review blockers. Root owner: dot; slice: structural admission cache qualification; acceptance: both frozen suites plus independent context/flag controls and a justified measured benefit. No product promotion yet.

## CP67 assignment/search conversion interaction (research-only)

Applying VARCHAR assignment truncation to search binds can silently change equality results. Counting UTF-8 bytes rather than characters rejects native-valid inputs; omitting space-suffix assignment handling stores the wrong value. At CP67 the product refused VARCHAR, so those were prevented-design failures. CP71 now integrates the approved bounded VARCHAR profile with assignment and search conversion kept separate; no arbitrary custom type admission is implied. Three limits and three deliberate broken variants provide native differential evidence. Root owner: dot; slices A6.1–A6.5; next step: retain the integrated conversion/metadata regression controls; complete generic reverse lifecycle, default-collation admission and full application gates, with native failure behavior documented.

## CP79 canonical catalog inspection (confirmed correctness defect)

An unchanged foreign-key schema can be refused as stale when application search_path differs from compiler inspection. Native object identity/deparser control PASS; two product RED failures. Owner: dot. Correction candidate preserves canonical definition hashes, caller transaction/path and fail-closed cleanup;79 focused controls PASS per SQLAlchemy version and3 removal proofs FAIL as expected. Both full source and installed cells now PASS; six removal proofs FAIL as required; exact qualified code is integrated uncommitted into the primary candidate. Acceptance: both full dependency cells, installed exact bytes, genuine-drift detection, transaction/cancellation/fault controls, then real-app migration advances without weakening drift checks.

## CP80 mapper write cache (confirmed defect, bounded correction closed)

A mapper warmed before attachment retains native VARCHAR bind processors independently of the engine cache. Two independent writes failed RED. Clearing the mapper-owned cache on attach fixes eight expanded Text/VARCHAR insert/update variants per version. Removing that correction fails all eight per version. Both full source and installed suites pass (1,659 on 2.1.3; 1,641 plus 18 version-only skips on 2.0.51); 42 primary integration checks pass. Exact qualified runtime/test bytes are integrated uncommitted. This correction is closed unless new evidence reopens it. Owner: dot.

Actual installed FastAPI remains 20 PASS / 38 FAIL / 1 teardown ERROR versus native 58 PASS. All 38 call failures reach current UUID-text record admission; first teardown failure is Core DELETE on unprotected Item. These are current refusal gaps, not 39 newly independent silent defects. UUID-01 remains unapproved; bulk DELETE needs an explicit scoped admission decision and native transaction/identity-map/cascade tests. Do not patch upstream tests to hide either gap. Full app searchable/lifecycle adoption remains open.


## LIFE-OBJECT-COMMENT-01 — 2026-10-14 17:55 UTC, confirmed OPEN

Current bounded S23 source loses comments on admitted standalone indexes, UNIQUE constraints and constraint-backed indexes during protection/decrypt-back. Separate native catalog oracles on SQLAlchemy2.1.3 and2.0.51 each report3FAIL/1PASS (2.70s/2.67s). Native untouched controls preserve comments; lifecycle current values and object definitions pass while comment equality fails at PLAINTEXT_PENDING. The uncommented control proceeds through removal. Commented-case removal is NOT_REACHED. This is a native metadata reversibility defect, not evidence of row-value loss or a confidentiality failure.

Evidence: evidence/s23-object-comments-v2-red-{sa21,sa20}-20261014. Frozen S23 is unchanged; source/external and isolation checks preserved. Independent postrun audit in progress. Next: version-aware inventory/fingerprint and transactional restoration, including backing-index comments, late drift refusal and rollback/resume controls; no interpretation of absent legacy metadata as known NULL. Owner: coordinator with isolated lifecycle implementation and separate review. All seven qualification gates UNKNOWN.

Earlier rows above are chronological evidence. The root CRYPTALIS_BUILD_CHECKLIST.md owns current integrated status; this append does not reopen or erase already-corrected historical defects.
