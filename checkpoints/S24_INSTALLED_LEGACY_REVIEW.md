# Installed S24 consumes genuine S23 committed phases: V2 independent acceptance

## Decision and actual results

**PASS for both exact ten-case installed legacy handoff cells. No remaining failure, integrity, origin, cleanup, retention, corpus-restoration or shutdown blocker was found in their evidence.**

| Cell | Parent cases | Child producer cases | Terminal result | Parent JUnit duration |
|---|---:|---:|---|---:|
| SQLAlchemy 2.1.3 | 10 passed | 10 passed | 10 passed, 1 warning in 14.18 s | 14.144 s |
| SQLAlchemy 2.0.51 | 10 passed | 10 passed | 10 passed, 1 warning in 15.41 s | 15.360 s |

These are the same **ten distinct lifecycle scenarios exercised separately in two dependency cells**, not twenty different scenarios or a full installed suite. Each cell's ten producer children are setup/ownership evidence for its ten parent cases; they are not ten extra recovery scenarios.

`audit_installed_handoff.py` passed **137/137 checks independently for each cell**, rehashing 1,516 safe inputs per audit. `audit_both_cells.py` then passed **10/10 cross-cell checks** and rehashed the union of **1,806 safe inputs unchanged after both runs**. The two cell JSON audits and combined JSON audit preserve exact case identities, origins, artifact/retained-file hashes and input hashes. Only standard-library data-reading reviewer code was executed. No product, test, helper, runner or wrapper import/execution, database, install, build, process probe or remote action occurred. Only this reviewer directory was written. The five environment-bearing wrapper phase JSON types were never read, including for hashing.

## Exact phase and child identity

Both parent JUnits have exactly the expected `test_legacy_recovery` classname and each planned case once: forward EXPANDED, BACKFILLED, VERIFIED, PENDING and ACTIVE; reverse EXPANDED, BACKFILLED, VERIFIED, PLAINTEXT_PENDING and PLAINTEXT_ACTIVE. There are no skips, errors, failures, extra or missing cases. Each cell's progress has ten exact starts and all thirty setup/call/teardown reports passed. Runner selectors, counts, module identity, exit status and UNKNOWN gates reconcile exactly.

Each unique phase directory retains exactly one passing child named `test_frozen_producer_checkpoint`. **Child classnames are empty in both cells.** They remain unchanged in the evidence and are explicitly recorded in the audits. Their identity proof is the exact producer name, unique phase directory and matching request/ready data, plus unchanged byte-pinned producer/consumer command and selected-file provenance. This is not literal `producer_case` classname equality or an independent module-path trace. No unverified causal explanation for the empty metadata is asserted. Parent classnames match without this variance.

Each terminal warning is the single known `PytestAssertRewriteWarning` for `installed_origin` already being imported. Origin checks completed and final reports were emitted. No warning-free claim follows.

## Genuine old artifacts and ownership

- The immutable genuine S23 producer matches the accepted V4 source byte-for-byte, SHA-256 `7359ecc2533b648be67054b0f4195b91c3b2c2d2e36bbe3f3973fcbf5b233ecf`. Its source/helper pins, old origins and fresh child preflight are guarded by the reviewed passing producer. The installed consumer preserves the exact reviewed handoff/lifecycle body.
- Each newly retained forward artifact decodes to canonical old v0 bytes with the recorded SHA-256, same journal/model schema and operation identity. All ten reverse artifacts across both cells independently verify their own old v0 bytes/hash, source pin and exact embedded forward bytes/digest/operation/target identity. Historical digests were not substituted for newly generated artifacts.
- There are twenty unique schema/forward-operation pairs across the two cells; within each cell all fifteen forward/reverse operation IDs are distinct. The protected current-value edit in reverse cases is preserved; terminal native rows match exactly.
- All nine ownership/result booleans are true in all twenty handoff records, with no failure codes. Each producer record shows fresh preflight/old-source attestation, zero checkouts and a nonempty unique backend-ID set. Successful consumer assertions establish producer PID absence and the same journal phase before consumer lifecycle work.
- All **100 retained child file hashes** verify, with exactly five allowlisted bounded regular files per case. Each release is the exact consumer-finished/engines-closed record; each cleanup record is true and every child JUnit is one pass. No producer-error file is present. Endpoint/current-value and applicable ciphertext-frame assertions passed.

These observations are interpreted with the preserved source: producer pools close before ready, producer waits without DB work, consumer closes both engines/mapping before release, and uncertain closure never authorizes cleanup. Passing recorded checks are not a new live database probe or universal concurrency/hostile-owner proof.

## Installed consumer and integrity

Each cell's single final `INSTALLED_ORIGIN_CURRENT` identifies its exact new-cell executable/prefix, the 214-file R3 manifest and pinned wheel. All **23 loaded Cryptalis origins** are in the selected installed cell, including migration, deprotection, SQLAlchemy adapter and object-comment code. SQLAlchemy's origin and static metadata match the selected 2.1.3 / 2.0.51 cell; the unchanged runtime checker also enforces its version.

The manifest remains `6c7ca4ecda9e4d0628aa8a8fe4626e36c8708622f020c73c8320210948cd003d` and the wheel remains `4a83731a84dec485fbe0cecf7563a530c64464ec82064b2d61416d5e1109d279`. All **41 installed runtime modules per cell** match wheel and clean source. All 214 candidate hashes and the exact clean inventory verify. These establish current payload/origins, not historical imports or bytecode execution identity.

Both commands have exit 0 and after-pin statuses `0 0`. Every before/after ENTRY log contains exactly one successful entry; every INPUTS log contains exactly **1,198** successful entries. Live pins and preserved V1 files still verify. Each command captured all **34 packet files** under `.txt` names. Each wrapper archived exactly **four external Python files** and **153 R3 source files**, all unchanged. Each runner records exactly **152 source/test/script hashes** and a matching recomputed revision. Full 214-file identity is not described as a 214-file wrapper capture. The first cell's text-suffixed archives did not expand the second cell's Python selection/capture.

## Startup, shutdown and corpus restoration

Safe logs record all five wrapper stages with exit 0 in the expected order: start, readiness, installed-origin precheck, tests and stop. Environment-free runner preflight records agree with separate readiness logs on successful fresh dual-role probes. Separate stop logs say `server stopped` in both cells; shutdown was not inferred from outer exit status.

Both runs preserve the same **26-file prior corpus**, with exact archived/current hashes, restoration true, no archived/deleted changes, no errors and an empty candidate-corpus directory. Final cross-cell rehashing found no source, packet, prior-evidence or audited result drift.

## Incident and acceptance boundary

The complete V1 packet and both failed entry-prefix logs remain preserved. Its earlier no-entry-execution claims are withdrawn by V2's explicit incident note. Independent source/log review placed those failures at the missing-ENTRY guard before wrapper, preflight or DB work. They are preparation failures, not test results, and were not erased by these later successes.

This acceptance covers planned, transaction-free recovery from genuine frozen S23 committed phases into the pinned installed S24 consumer. It does **not** establish crash recovery, lost COMMIT/ACK behavior, timeout/signal injection, corrupt-storage recovery, hostile-owner fencing, arbitrary historical upgrades, a full installed-suite pass, release readiness or production safety. The four optional design-matrix extensions remain unrun. Dependency provenance/drift limits, seven historical full-suite failures and **all seven UNKNOWN qualification gates** remain unchanged.

## Evidence and reviewer artifacts

- SA21 evidence: `evidence/s24-installed-legacy-handoff-v2-sa21-20261014`
- SA20 evidence: `evidence/s24-installed-legacy-handoff-v2-sa20-20261014`
- Command/capture receipts: `experiments/s24-installed-legacy-handoff-v2-20261014/run/sa21` and `run/sa20`
- Detailed cell audits: `SA21_POSTRUN_AUDIT.json`, `SA20_POSTRUN_AUDIT.json`
- Final cross-cell audit: `BOTH_CELLS_POSTRUN_AUDIT.json`
- Original hold: `ORIGINAL_HOLD.md`; source clearance: `V2_SOURCE_COMMAND_REVIEW.md`
- Prior SA21 gate decision: `SA21_POSTRUN_REVIEW.md`
