# Planning-provider snapshot RED/GREEN evidence review

2026-10-14, approximately 16:17 UTC. Independent saved-evidence audit; no test or database execution by reviewer.

## Result

No blocking discrepancy in the finite evidence. The original redundant host-resolver call and raw-error boundary defect are now demonstrated by RED. GREEN passes the eight new cases and 39 related planning controls in both dependency cells. This supports composing a clean derivative; it does not replace combined integration testing or qualify a release.

| Run | Observed terminal result | JUnit/receipt |
|---|---|---|
| RED | 4 failed, 4 passed in 1.07 seconds | 8 tests, 4 failures, no errors/skips; exit 1 |
| GREEN SA2.1 | 47 passed in 4.84 seconds | 47 tests, no failures/errors/skips; exit 0 |
| GREEN SA2.0 | 47 passed in 4.21 seconds | 47 tests, no failures/errors/skips; exit 0 |

Each GREEN run comprises eight test_plan_provider_snapshot cases, 14 plan-estimate-bound cases, 15 transition-rate-estimate cases and 10 migration-plan-diagnostic cases. Their JUnit identities and receipt/log counts agree. Saved readiness records report both role probes passed; clean stop receipts recorded exit zero. The reviewer did not repeat those operations.

## RED meaning

The three late-resolution variants and multitable case fail exactly as predicted:

- Late callback exception: raw synthetic RuntimeError escapes the public planning call.
- Late invalid ring: raw AttributeError escapes after a None result.
- Late different policy: the plan returns, but the test first fails on the unexpected second resolver invocation.
- Multitable: a third resolution for a previously inspected tenant raises the synthetic RuntimeError outside the sanitizer.

The different-policy RED case stops at its call-count assertion before checking the estimate. Therefore this RED record proves the extra callback, not an independently observed numerical count mismatch. The baseline expression explains the possible mismatch by source inspection. GREEN's independent policy-digest and count assertions directly verify the corrected pairing.

The four unchanged baseline controls pass: initial callback exception, wrong tenant policy, direct keyring, and empty scoped table. Thus this is not merely an all-red missing-API test.

## Source identity

POSTRUN_AUDIT.json records exact file hashes and comparisons.

- All 212 baseline manifest paths still match frozen S22 and RED.
- Exactly migration.py differs among those inherited GREEN paths.
- New test bytes are identical in RED/GREEN, SHA256 58f9f1e5b2226944ba9dc10d23d4b250a9b49a1c49a6f601f86a9d8b3bf54802.
- GREEN migration.py SHA256 remains 76be49957e03f62e32cd0db9155565c1aa8f6f72b822513f17dd73dc27def3c7.
- Each execution's 152-file source/config before/after inventory is identical and matches its present source directory. These are source-byte checks, not historical imported-bytecode or exact dependency-lock attestation.

## Safety observations and limits

The passing tests exercise typed, sanitized initial resolver failures; expected policy fingerprints and wrapper totals; repeated tenants across two models; no sentinel provider unwrap/unwrap_async calls; unchanged named native rows/objects; and no returned-plan keyring retention by weak-reference checks.

These conclusions are bounded by the pinned test assertions. Weak-reference collection does not prove key zeroization. No-unwrap sentinel results do not qualify real provider custody or remote costs. Native snapshots are not an exhaustive catalog/privilege audit. The fix retains only integer counts, leaves subsequent policy checks unchanged, and neither prepares roots nor activates/rotates keys.

Existing per-model last-observed policy behavior remains. This patch does not guarantee a globally atomic host-resolver snapshot or support arbitrary concurrent mutation of trusted host objects. All seven production gates remain UNKNOWN. The seven legacy full-suite failures are outside this focused run and are not waived.
