# Finite deciding matrix: durable inactive preparation

Status: PROPOSED. No test file or runtime code was written and no test was run in this design pass. Freeze exact selectors/parameters after the first RED artifact, before GREEN execution. All database execution belongs to root and uses the unchanged existing-role preflight/wrapper.

## Independent baseline and assertions

Start from a small, already-protected synthetic source with post-protection update, insert and delete before the operation plan. Keep an independently maintained native expected-value map. Freeze current source frames and all relevant source catalog/original journal/pin observations. Preserve a historical pre-edit frame set as a separate control: final inactive results must match current data rather than this old set.

A successful scenario independently reads all staging and journal rows, checks source-to-stage and stage-to-source membership, authenticates/decodes every stage frame through the existing independent reference path, compares values/types/NULLs and unchanged exact equality terms, checks source frames/catalog/original journal unchanged, and confirms the active attachment still uses generation 1. Avoid trusting the prototype's own computed digest or reported count as the oracle.

Every failure checks exact prior stage/journal bytes, no unexpected committed rows, an observable typed failure/pending result, and explicit recoverability or refusal under the same operation. Record module origins, source hashes, versions, preflight outcome, clean database shutdown and limits in each receipt.

## Required bounded scenarios

| ID | Scenario and finite parameters | Deciding observation |
|---|---|---|
| P1 | Four profiles: UUID/storage, UUID/equality, int64/storage, int64/equality; 9 rows, chunks of 2 | Independent full decode/membership parity; five exact markers; repeated completed inspection makes zero seal calls and changes zero bytes. Int64 includes negative, zero and upper/lower boundary values; UUID order is native, not insertion order. |
| P2 | Empty source; all-NULL source with 3 rows, each as one case | Empty operation completes explicitly with zero batches; NULL rows create durable membership/cursors, are not mistaken for missing targets and do not collapse into empty text. |
| P3 | One exact-fit byte boundary and one first-row-over-budget boundary | Exact-fit succeeds. Oversized first row refuses before its frame is transported/crypto invoked; no empty-success marker, skip or truncation. |
| R1 | Real SIGKILL after first chunk committed; fresh exec-based worker resumes | First marker/stage bytes preserved exactly, new PID/provider/keyring preparation observed, no prefix reseal; full final independent parity. |
| R2 | Real SIGKILL during second chunk before marker insertion | First chunk unchanged; second chunk has no committed rows or marker; fresh resume prepares only the second and later chunks. |
| R3 | Real SIGKILL after second marker SQL but before COMMIT | Marker and target rows roll back together. Do not infer atomicity from a single in-memory exception. |
| R4 | Real SIGKILL after full terminal verification but before terminal marker commit | Last committed phase remains PREPARING; fresh process repeats full verification before terminal success. |
| R5 | Real SIGKILL after terminal COMMIT before success output | Fresh inspection returns the identical inactive completion receipt without transformation or active-policy mutation. |
| C1 | Discard actual successful chunk COMMIT reply with the existing local proxy | Original client reports inspection-required; terminal primary inspection finds both marker and rows, and resume preserves them without resealing. Identify the intended commit by an observed SQL/barrier sequence, not an unexplained brittle commit count. |
| C2 | Keep original transaction/session live behind a bounded barrier before its COMMIT | Second executor cannot acquire the same scope lock; absent next marker stays UNKNOWN/PENDING and produces no DML. After original transaction is explicitly allowed to finish, inspect its actual outcome and continue. |
| C3 | Two operation UUIDs against the same one-table scope | The second cannot bypass cooperating scope serialization by using another UUID. No mixed marker/stage ownership or duplicate target rows. |
| S1 | Four source drifts after a committed prefix: changed valid value, valid fresh reseal of same value, delete in completed prefix, insert behind saved cursor | Every case refuses before new target/journal DML; source content/membership proof is stronger than max-key/count. Existing inactive bytes remain intact. |
| S2 | Tenant move and source relation drop/recreate with same name, two cases | Original operation refuses exact scope/OID mismatch; no object adoption or automatic restart. |
| A1 | Four authority/artifact changes: current source pin, target identity, target inactive key-policy fingerprint, selected descriptor/codec | Refuse before target/journal DML. A matching restored journal cannot override the independent artifact/current inputs. |
| A2 | Resume with missing OPERATION entry, unsupported layout, or same operation UUID/different artifact, three cases | No stage adoption, journal repair, table recreation, automatic policy acceptance or downgrade. |
| J1 | Six corruptions after one committed chunk: target missing; orphan target; batch marker missing; skipped/forged cursor; changed NULL marker/member; changed target frame with syntactically valid shape | Independent resume inspection refuses; no overwrite/reseal/repair. Inject each only into its own disposable fixture; save original fault evidence. |
| J2 | Replace committed target by a different authenticated target value, one case | Full source-versus-target value proof rejects even if target AEAD and framing are valid. Update its local target hash in the mutated marker so this test cannot pass by checking that hash alone. This remains a fixture-owner mutation, not an adversarial authenticity claim. |
| L1 | Expire source prepared lease and target prepared lease after B8 returns but before target DML, two cases | Typed key failure, zero target/journal changes. Do not extend deadlines or fall back to old prepared material. |
| L2 | Expire source lease and target lease after target DML but before final precommit binding check, two cases | Actual PostgreSQL rollback removes the complete in-flight chunk and marker while previous bytes remain. A later explicitly prepared fresh same-policy resume succeeds. |
| L3 | PID binding change at the precommit boundary; late authentication failure within a multirow B8 call, two cases | No partial durable chunk. Existing B8 final-return six-case controls remain unchanged and pass separately. |
| D1 | Runtime-role access/control denial against the two new tables and complete source-binding preservation, one scenario | Effective permissions/ownership are unchanged; no new grants; runtime cannot mutate/own/truncate stage or journal. Record actual native denials instead of inferring from ACL text alone. |
| D2 | SQL/driver and safe-diagnostic collectors with positive calibration, one scenario | Collector detects a deliberately exposed unprotected sentinel, then no transition-origin protected plaintext marker, root, term, frame body, credential or raw exception appears in captured output. The preexisting native oracle's synthetic plaintext is explicitly outside the measured transition-bind claim. |
| D3 | Output failure after committed chunk/terminal commit, two cases | Failure remains visible; durable marker/payload inspection finds the real outcome. No success claim based only on output delivery or automatic replay. |

This is 48 primary scenario cells before unchanged B8/crypto/lifecycle companion controls. The experiment supports no arbitrary expansion beyond the stated fixture bounds. Root should preserve failures and distinguish an invalid oracle correction from a product correction.

## Sensitivity controls in separate, never-promoted derivatives

1. Remove only source-content reinspection: S1's valid changed/resealed-source cases must fail their refusal expectation. Pure membership is insufficient.
2. Persist/commit targets separately from their marker: a forced crash boundary must expose the atomicity oracle's failure. This intentionally unsafe mutant stays on public synthetic fixture data only and is never executed by this worker.
3. Skip committed-prefix consistency/value validation: J1/J2 must fail their refusal expectations.
4. Change resume to reseal committed rows: R1/C1 byte-preservation and seal-call observations must fail.
5. Treat an unavailable scope lock/absent marker as rollback: C2 must fail its no-DML/pending assertion.

Keep each mutant isolated; do not relax the production/safe candidate to make a sensitivity run pass. Preserve exact source delta and full failing observation.

## Initial RED and execution order

1. Add only the experimental tests/worker contract in a new root-selected source derivative. Module intentionally absent. Run P1 UUID/equality plus R1 through the existing wrapper and record expected feature-absent RED. Missing-module failure proves only the new-feature baseline.
2. Implement only the test-local prototype after root accepts RED. Run deterministic artifact/cursor/boundary tests, then the finite PostgreSQL matrix, serialized through root.
3. Run unchanged tests/test_payload_rotation_preparation.py, tests/test_cf1.py, tests/test_cf1_backend_failures.py, tests/test_key_lease_renewal.py and relevant existing migration commit/cleanup/runtime-role controls. Select tests by inspected source inventory; do not invent missing files.
4. Repeat the complete finite matrix and affected controls in both SQLAlchemy 2.1.3 and 2.0.51 cells. No expectation changes based solely on which version passes.
5. Run the separate sensitivity derivatives, preserve their intended failures, and reverify the safe source's hashes. Check that all 208 inherited S20 files remain unchanged.
6. Stop at reviewed PREPARED_INACTIVE evidence. Root records exact receipts and recovery artifacts. No active-generation test, policy publication, external KMS operation, package CLI change, new cluster or main promotion follows automatically.
