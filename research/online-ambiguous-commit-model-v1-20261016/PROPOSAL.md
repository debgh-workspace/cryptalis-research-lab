# Next online-research slice: ambiguous worker-COMMIT observation

Prepared 16 October 2026, 09:57 UTC. **SOURCE-ONLY MODEL AND FINITE TEST PROPOSAL; NOT IMPORTED, COMPILED OR EXECUTED.** Frozen preview, product code, D4/D5 and online-closure V2 are unchanged. This packet is not a usable database reconciler or online capability.

## Why this slice, rather than repeating closure research

D4's acknowledged process-death experiment deliberately distinguishes before-COMMIT from after-COMMIT acknowledgement. `candidate-online-closure-v2-20261014/tests/_online_cf1_process_lab.py:107–129` places its after_commit acknowledgement only after the outer transaction returns. D4_PROCESS_DEATH_PROGRESS.md explicitly excludes a sent-COMMIT/lost-reply outcome. Earlier successful twelve-case results and the corrected minimal IPC packet therefore do not answer this new question.

The accepted D5 counterexample is the failure that must shape the new predicate: a pending writer is invisible to repeated empty/correct committed snapshots, then commits a fresh obligation. Checklist's D5 checkpoint records ten passing counterexample/convergence schedules; D5_CONVERGENCE_PROGRESS.md limits closure to the explicit end of the writer schedule. Thus empty dirty state is never treated as success, writer exclusion or a closure certificate here.

Online-closure V1's inherited-route source HOLD and V2's corrected eight structural checks remain prior evidence, not the question being repeated. A successful V1 write bypass was never established. The actual PAUSED closer, durable runtime/native guard and paused finisher remain unimplemented and subject to capture/handoff and contract decisions. This packet implements none of them.

## Smallest testable question

After a caller loses the acknowledgement for one stage-plus-exact-token-retirement attempt, can a conservative **claim-level observation classifier** distinguish unresolved evidence, an observed matching effect, a still-observed obligation and a different obligation, without authorizing a blind retry or inferring queue/online closure?

The existing fixture installer checks operation/pin/PREPARING, locks the exact dirty token, writes stage data and retires that same token atomically (`tests/_online_cf1_lab.py:160–183`; `_online_cf1_process_lab.py:75–97`). That makes a narrow deterministic predicate possible, but does not supply its future native observation/transaction-resolution adapter.

This is preparatory research for resumable concurrent-write catch-up: distinguish what is known before choosing a future approved same-operation recovery action. It does not solve lost acknowledgements, authenticate observations or enact a retry by itself.

## Proposed mechanism and deliberately missing assumptions

`model.py` consumes only public synthetic observation records. It returns a diagnostic outcome plus three invariant false fields: retry_authorized, closure_established and publication_authorized.

1. Reject malformed evidence. Require modeled verification of exact operation, row key and original-attempt correlation. Attempt strings are test labels, not a proposed product ledger/schema addition.
2. Preserve current expected pin and PREPARING admission; a PAUSED observation blocks this normal-worker path.
3. If the original transaction is not externally verified terminal, return UNKNOWN even if a matching stage or empty queue is visible. “Terminal” does not mean known committed or known rolled back.
4. Require a modeled coherent committed observation; mixed/stale read assumptions remain UNKNOWN.
5. A matching stage token and verified exact intended effect, with that dirty token absent, establishes only **claim effect observed at that observation**. A different dirty obligation remains explicitly pending. This does not identify which worker committed the effect, establish the original attempt's commit outcome, or prove no later writer will create work.
6. The original dirty token still present is only “original obligation observed.” It grants no retry. A different token is only “different obligation observed”; numerical ordering is deliberately not interpreted as chronology or a “newer is safe” certificate.
7. Empty dirty state without a matching exact effect remains UNKNOWN. Same token simultaneously staged and dirty, or wrong effect at the matching token, produces HOLD_CONFLICTING_EVIDENCE. Preserve evidence; do not repair.

The booleans identity_verified, original_transaction_terminal_verified, coherent_committed_observation and stage_matches_claim are explicit **model assumptions**. No code in this packet proves them. A future native adapter must establish original transaction identity/terminality and coherent observations under actual isolation/lock rules, independently verify the full intended live/NULL/tombstone/context/frame effect, and revalidate any later action. They must never be filled with “true” merely because a constructor, network failure, timeout, empty queue or old receipt exists. Until then, actual operational outcome remains UNKNOWN.

## Finite selection proposal: no execution yet

Files:
- model.py: pure dictionary classifier; no imports, database or I/O.
- CASES.json: 22 fixed public synthetic observations, no credentials, URLs or payload secrets.
- driver.py: stdlib-only; reads only these two sibling inputs, executes the new model via runpy, compares exact outcomes, checks all authority fields remain false, rejects two named counterfeit conclusions, rechecks those two input bodies, and prints one JSON result to stdout. It writes no files and launches no subprocess/network/database operation.

The 22 cases cover matching effect; other obligation; original obligation; a lower/different token without ordering inference; empty observations; unverified original transaction with dirty, empty and matching-stage views; unverified/mismatched operation/attempt/key; wrong pin; PAUSED; incoherent observation; contradictory stage/dirty/effect; and malformed values. Two fixed negative-oracle controls reject “empty queue means success” and “visible dirty token means original transaction finished.” These are explicit negative conclusions, not product mutants or newly reproduced database schedules.

Root selection, only after independent source review and entry/input identity admission:

    <already-admitted stdlib Python> -I -S -B <absolute packet path>/driver.py

The interpreter placeholder is not a new interpreter acquisition or execution authorization. Root should pin the reviewed command, cwd and packet hashes, capture stdout/stderr/exit into a fresh separate evidence directory, and retain the first result. A finite 10-second / 128-KiB-output bound is sufficient as a proposed root limit, not a measured performance statement. Expected successful output: 22 matching outcomes, two rejected counterfeit conclusions, all three authority flags false, unchanged two inputs, empty failures, exit 0. Failure must stop and be retained; no automatic retry or source change.

No old D4/D5/native suite, PostgreSQL wrapper, product import, fixture setup, provider or source-check8 rerun is selected. A pass would establish only the model's finite logic on stated assumptions. It would not establish the assumptions, native transaction behavior, liveness, race coverage, provider validity or actual recovery.

## Authority/resources and next gate

**Unblocked now:** isolated model/source/test-plan review. It needs no new cluster, role, credential, dependency install, provider access or change to the current maintenance contract. Root already authorized preparation but has not selected execution.

**After a model result is independently accepted:** design one separately reviewed native observation experiment for the original-transaction resolution boundary. It must use exact existing approved target/roles and coordinator-only wrapper when genuinely authorized, establish fresh identities, preserve original operation and effects, and stop on uncertainty. This packet neither provides a runnable native route nor infers permission for capture/trigger/guard changes or fault injection.

**Still blocked for actual online closure/integration:** pending capture/handoff request `Sentinel_f9407ee631c081d1a92fb471b6262b6f`; exact source-writer/owner/DDL coverage, runtime-role guard mapping and PAUSED/finisher contract; actual native lock/visibility/rollback/reconnect evidence. Any new cluster, credentials, privileges or provider authority requires its separate applicable approval. No approval is invented for those actions.

Selected retained-native maintenance remains normative: original plan/artifact and authenticated current external authority, actual writer exclusion, byte-bounded atomic work, full current membership/value/type/NULL verification, snapshot barrier and separate publication. Empty observations, counters and this classifier cannot replace the final scan or maintenance fallback. No change to all 34 objectives or seven UNKNOWN gates.

## Read-only basis

- `candidate-online-closure-v2-20261014/experiments/D4_PROCESS_DEATH_PROGRESS.md`: `c204f93c5bb29f76bed205bfe737f6208846529f6f7bacd36fb2a068ed53d2e4`.
- `candidate-online-closure-v2-20261014/experiments/D5_CONVERGENCE_PROGRESS.md`: `7b4b1b5bd0e794ffcbd94f69a4900a2334c2f7ff0d7b4e476615f02e810e0b9d`.
- `candidate-online-closure-v2-20261014/tests/_online_cf1_lab.py`: `319b16fa2c936f1be85bd8f12466af3212cc36417601cf51b95b712ec597e202`.
- `candidate-online-closure-v2-20261014/tests/_online_cf1_process_lab.py`: `2845f4dcc0663b29cf0a502ab687b12fc4ceeca3cffdfbc04b3eb7c236d7ec4c`.
- `candidate-online-closure-v2-20261014/tests/_online_enumeration_lab.py`: `a4bd5e3771491bb721b7cbade79180d5423c2076962e80e23350847fe987cc9e`.
- `reviewer-notes/online-closure-v2-final-independent-20261014/REVIEW.md`: `296efee234306dba5c5a492485f762757cc2e6c61e3bd5ff660cd7c88c490eb2`.
- `candidate-doctor-remedy-integrated221-v1-20261015/src/cryptalis/migration.py`: `94344b2f98e0969d9f8b3d41cc9dca6e7d01a5e785a5b3af33431c41e55d2014`.
