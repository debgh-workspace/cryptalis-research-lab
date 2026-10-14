# A9 R2: bounded no-argument default failure/retry proof

Status: PURE FEASIBILITY ONLY. Both pinned releases complete all 12 cases. No real database, network, credentials, cryptography, Cryptalis runtime import, production hook, or admission change.

## Exact executable and scope

Run `experiments/opaque_failure_retry_r2.py` with `-B` using the existing SQLAlchemy 2.1.3 or 2.0.51 interpreter. The script checks all eight exact installed-source hashes in inherited `experiments/opaque_source_hashes.json` before running. It uses DefaultDialect and a local Python fake DBAPI. Results are `experiments/r2-pure-sa21.json` and `experiments/r2-pure-sa20.json`. The R2 receipt records exact executable/result/manifest hashes and preservation of all 228 A9 files.

Historical A9 executable/results remain byte-identical, including their weaker error oracle. R2 is an additional isolated executable. It does not upgrade those earlier results retroactively.

## The 12 cases per version

1–2. Native and routed constructor failure, followed by successful retry.
3–4. Native and routed no-argument default failure, followed by successful retry.
5–6. Native and routed bind-processor failure, followed by successful retry.
7–8. Native and routed fake-driver failure, followed by successful retry.
9–10. Native and routed two-row success, using distinct public logical markers.
11–12. Native and routed context-callback success, retaining the explicit context/list identity counterexample.

Constructor/default/processor faults are exactly `StatementError`; driver faults are exactly `DBAPIError`. Every error must retain the same injected object as `.orig` and `.__cause__`; handle_error must see that same original and the same outer exception later caught by flush. An unrelated error or early assertion cannot satisfy these tests.

The expected first-attempt stage prefix is constructor, default, processor, driver, ending exactly at the injected stage. Callback/driver counts and absence of after_execute on the failed attempt are asserted. A failed session is inactive with an open failed transaction; the row is transient with no assigned ID and unchanged logical marker. Rollback returns an active session with no transaction. Re-adding the same object and flushing must succeed outside the exception catcher, with full stage order and native persistent/identity state. Native and routed results are compared for stage order, callback/driver counts, error types, event sequence and rollback state.

The constructor fault is an injected failure immediately before delegation to the native execution-context constructor. It models native wrapping at that boundary, not all internal constructor failures. Both controls use the same injected boundary. A native pass-through TypeDecorator establishes the processor-failure control instead of pretending native Text can raise this injected processor exception.

## Private-value consumption and row association

The private store now actually supplies the value used to form the synthetic output. An empty Pending object is the exact key. At the native UOW producer, its corresponding record holds the actual InstanceState and parameter dict. At construct_params return, the original input dict is matched by `is` and the actual compiled output retained. Materialization finds that exact compiled dict by `is`, verifies the Pending token is the original producer input, then reads the private store. The owner is matched by actual InstanceState identity, never marker equality, generated-name suffix, or event position.

The two-row controls use distinct markers and native-generated UUIDs. An independent owner-derived expected map is built from the final ORM objects, keyed by their assigned UUIDs. Each fake-driver row is checked against its actual ID and expected marker. This is the final correctness oracle, not the source of routing authority. DefaultDialect emits separate executions for these rows in both pinned releases; this is not an IMV/multirow-driver receipt proof. The native source's per-record branch is ORM persistence.py 1217–1241 (2.1.3), with the corresponding branch in 2.0.51.

Synthetic output is hex-encoded public label data containing native UUID and the captured public marker. Hex is reversible and provides NO confidentiality. These are deliberately public test markers, not secrets, ciphertext, or a safe production representation. Absence of the original literal from repr-based surfaces proves only the bounded routing and collector checks. Actual protected data must never use this encoding.

Before retry, the experiment explicitly clears its private operation store and producer/compiled receipts. Old Pending objects remain strongly referenced for the freshness assertion. The new producer token must be distinct from every old token, belong to the new store, and trace to the same ORM state. Retained exceptions may retain inert old tokens; this does not claim erasure of every Python reference. This manual experiment teardown is not a proof of a production lifecycle implementation.

## Exposure collector calibration

Native before_execute, before_cursor_execute, after_execute, handle_error.parameters and SQLAlchemy exception.params collectors must detect the public logical marker. Routed collectors must not find its plaintext literal in their bounded parameter/context structures; caught exception.params and formatted errors are also checked. The original callback-owned exception object is unchanged.

Every case requires nonempty ordinary SQLAlchemy log capture containing the INSERT and the hide_parameters=True diagnostic, with no logical marker. Separately, a deliberate PUBLIC_LOG_COLLECTOR_CALIBRATION message must be detected by the same handler before the ordinary capture is reset. No parameter-logging security setting is weakened. This distinguishes collector operation from hide_parameters suppression; it does not assert universal logging sanitization.

All injected exception messages are fixed safe strings. Callback-owned exceptions that deliberately include plaintext, arbitrary application diagnostics, stack inspection, recursive user objects, or reentrancy are outside this proof. They must not be confused with adapter-created parameter/context exposure.

## Retained context incompatibility and admission gaps

The native context callback retains the actual ExecutionContext, its current logical dict and the compiled_parameters list. After success, `context.compiled_parameters is retained_list` is True natively and False through the opaque routed view on BOTH releases. Callback-owned logical dictionaries remain intact. Broader native reflection/identity parity is still incompatible with this restoration strategy. No parity concession is approved.

No-argument UUID alone does not define a safe default profile. Another context-aware default in the same execution recreates the problem. The entire execution's callable/default set and relevant processors must be assessed. SQLAlchemy wraps no-argument callables; the apparent stored callable signature alone is insufficient admission evidence. R2 adds no classifier or profile-admission implementation.

No async, PostgreSQL, insertmanyvalues, driver rewrite chain, actual final-driver receipt guard, relationship-assigned tenant, CF1 lease/PID/context checks, protected NULL handling, or runtime error cleanup is qualified here. A7 receipts would still need composition with the actual final parameter guard. No private-hook production architecture decision or real-PG selector follows from these results.

## Preserved harness correction

`experiments/r2_two_row_collector_failure.py.disabled` preserves the draft whose native collector demanded the first row's marker at every event. Both native versions instead execute the second row separately. The corrected collector detects the marker for an actual owner row; expected stage order follows the pinned per-record source path. The draft exits on the unrelated assertion, demonstrating that it no longer false-passes as an injected fault. This was a harness expectation error, not a waived routed/native difference.
