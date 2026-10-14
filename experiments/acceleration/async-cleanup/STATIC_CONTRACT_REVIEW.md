# Async transaction preparation cleanup: independent contract review

Date: 2026-10-14. Classification: static source review only, not reproduction or runtime verification.

## Finding and bounded recommendation

The S25 `_AsyncTransaction.__aexit__` preparation-failure handler awaits native transaction exit before its bare re-raise. If native rollback also raises, that second failure replaces the preparation failure. This follows from the inspected control flow and both pinned native sources. It has not been executed by this reviewer.

A narrow correction can preserve the same already-sanitized preparation exception or cancellation object, clear prepared material, report cleanup ambiguity safely, and attempt public Session invalidation without claiming physical quarantine succeeded. Keep ordinary body-failure exits and unrelated native commit paths outside this slice. Do not describe the resulting change as complete transaction-quarantine qualification.

A public Session invalidation attempt after native exit is not proof of physical connection closure: root native rollback can close and remove the Session's connection before re-raising the recorded rollback error. An independent database observation is required for any stronger claim.

## Source roots and constraints

Reviewed snapshot:
`/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-s25-async-sqlmodel-integration-20261014`

Pinned native source roots:
`/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/release-lab/s25-installed-20261014/sa20/lib/python3.12/site-packages/sqlalchemy` (source reports 2.0.51)
`/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/release-lab/s25-installed-20261014/sa21/lib/python3.12/site-packages/sqlalchemy` (source reports 2.1.3)

No tests, imports, database calls, network access, remote operations, installs, credential reads, raw phase JSON reads, or author-candidate edits were performed. Only this review directory is written.

Navigation incidents: the snapshot has no Git repository metadata; `git status` reported that fact. The parent explicitly authorized continuing source review without repairing the snapshot. Initial guessed crypto module paths `errors.py`/`keyring.py` were absent; file discovery located the existing `crypto/keys.py`. These were ordinary missing-path diagnostics, not access denials. No repository or permission repair occurred.

## Exact contract owners

- `ENGINEERING_PLAYBOOK.md:32-47`: important failures cannot be silent; diagnostics need a safe cause, retry class and remedy; line 41 explicitly preserves the primary failure when cleanup also fails. An ambiguous commit is not proof of rollback.
- `docs/security.md:158-159`: cancellation discards late material and reports transaction ambiguity instead of assuming rollback.
- `docs/security.md:261-267`: material publishes only after all roots pass; cancellation rejects late material; raw provider/crypto exception text must not enter diagnostics.
- `docs/security.md:307-326`: operation/stage/code/retry/progress/remedy, no plaintext, key bytes, ciphertext, terms, SQL binds or raw provider text; unknown observations remain UNKNOWN; existing effects must be reported when cleanup fails.
- `docs/security.md:335-341` and `docs/compatibility.md:17-21`: failed native SAVEPOINT control invalidates the physical connection and deliberately forbids continuation of the outer unit. Repeated cancellation during cleanup and arbitrary host event extensions remain unqualified.
- `docs/architecture/README.md:90-104`: retain native ORM state and public integration boundaries; failed flush/rollback clears preparation.
- `docs/build-guide.md:41-50`: real PostgreSQL native-versus-attached state, rollback, failure cleanup and async cancellation evidence is required.
- `docs/status.md:3-8`: exact named revision/cell bounds every VERIFIED claim; no runtime/production cell or independent review is qualified and all seven full gates remain UNKNOWN.

Existing diagnostic shape: `crypto/keys.py:23-43,75-78`. `CryptoFailure` owns a stable operation ID, code and stage; `effects` defaults to `none`; `KeyUnavailable.retryable` defaults to True. On a secondary cleanup failure, an instance-level `effects='unknown'` avoids a misleading no-effects result. A corresponding no-retry-before-inspection classification/remedy should be explicit. Preserve the primary object's ID/code/stage rather than reconstructing it. Its existing trusted-local IPC reducer does not preserve arbitrary new attributes or notes; cross-process cleanup-diagnostic transport is not established by this slice.

## Current adapter and related paths

- `sqlalchemy.py:1058-1069`: the selected async context-exit boundary prepares only on normal body exit; it supplies an ensuing preparation failure to the native rollback context and re-raises only after that native call completes.
- `sqlalchemy.py:1088-1090`: failed await assignment leaves any earlier `_prepared` reference unchanged. Clear it on every failed preparation exit, including successful cleanup; root `after_end` does not clear it.
- `sqlalchemy.py:944-960`: the existing failed-flush helper already preserves the primary and adds safe secondary notes; it restores exception context for native rollback capture. This is a related pattern, not a reason to route context exit through failed-flush state or redesign native transaction internals.
- `sqlalchemy.py:1071-1079,1099-1116,1125-1138`: transaction commit, async commit preparation and result-boundary cleanup have distinct failed-flush semantics. Do not conflate these paths with the targeted context-exit change.
- `_sqlalchemy_transactions.py:65-83`: public Session events track live connections; root `after_end` clears the tracking set.
- `_sqlalchemy_transactions.py:129-145`: failed SAVEPOINT control invalidates its owning connection before propagation. Preserve this stronger existing behavior.
- `_sqlalchemy_transactions.py:148-183`: early failed-flush cleanup snapshots connection/driver state before rollback. That narrower existing implementation is not evidence that retaining a raw driver after normal root context exit is ownership-safe.
- `_sqlmodel_support.py:48-69`: guarded async SQLModel inherits the adapter transaction methods; its separate `exec` result boundary is not the transaction-exit correction. SQLModel remains an exact gated 2.0.51 profile.

## Pinned native source observations

Both versions have the same relevant structure:

- `ext/asyncio/session.py`: 2.0.51 lines 1885-1888, 2.1.3 lines 2205-2208 simply run sync transaction `__exit__` in a greenlet. They do not catch secondary rollback failure.
- `engine/util.py`: 2.0.51 lines 155-167, 2.1.3 lines 152-164 call rollback for exceptional exit, then restore context fields in finally. Rollback exceptions propagate.
- `orm/session.py`: 2.0.51 lines 1359-1398, 2.1.3 lines 1373-1412 capture rollback failure, restore snapshot, close the SessionTransaction, then re-raise the captured failure.
- Root `SessionTransaction.close`: 2.0.51 lines 1414-1437, 2.1.3 lines 1428-1451 remove the Session root transaction and close owned connections before the transaction-end event.
- Public `Session.invalidate`: 2.0.51 lines 2556-2598, 2.1.3 lines 2669-2711 closes/invalidates only connections still owned by current Session transactions. A successful return after root exit can therefore be a no-op for the former physical connection.

Thus `in_transaction() == False`, zero pool checkouts, or a successful `invalidate()` return cannot on their own establish rollback or physical quarantine.

## Minimal meaningful RED and native comparison

Prefer an integration test through the attached public session factory and a real cold keyring preparation failure, with already-flushed work. Use a one-shot public rollback/rollback-savepoint callback or a narrowly qualified dialect fault to trigger the secondary failure. State which boundary the synthetic failure bypasses. Do not inject through a new product-private hook solely to make the test pass.

Required assertions:

1. Preparation really failed after earlier writes/row locks existed; the secondary rollback fault was reached exactly as intended.
2. The caught attached exception is the exact sanitized primary from `Keyring.prepare_async`, with the same operation ID, code and stage. The raw provider exception need not be identical: `Keyring.prepare_async` intentionally normalizes ordinary provider errors to a new `KeyUnavailable`.
3. An injected primary `CancelledError` remains that object; a separate real suspended-provider task cancellation keeps `task.cancelled()` true. An injected cancellation alone is not real-task cancellation evidence.
4. Human-visible formatted traceback and notes retain safe primary diagnostics plus fixed cleanup-stage/UNKNOWN/discard/inspect instructions, with no raw secondary or invalidation sentinel. `raise primary from None` suppresses display chaining; it does not assert raw causes are erased from all in-memory object graphs.
5. Primary preservation still holds when the best-effort invalidation also raises. Do not report successful physical quarantine for that path.
6. Inspect transaction activity and independent PostgreSQL row values plus bounded NOWAIT/lock-timeout locking before any fixture `Session.close`, explicit rescue rollback or engine disposal. Old committed values alone are weak because MVCC can hide still-open uncommitted work.
7. After the fault is removed, a new pool checkout/ordinary commit must not publish the failed unit's writes. For failed SAVEPOINT control, verify the original outer unit cannot continue and accidentally commit inner or outer prefix work. Keep normal successful SAVEPOINT rollback outer-preservation controls distinct.
8. Include primary preparation failure with successful cleanup, no-connection/pending-only context, and native/body exit controls to show the narrow fix does not create database work or modify unrelated paths.

For the native oracle, record what native exit actually emits under the same local cleanup fault. Do not demand primary-identity equality with native where native intentionally emits the secondary exception. The attached primary-preservation policy is an explicit diagnostic difference justified by Cryptalis's failure contract. Native behavior is the baseline for transaction/database effects, not an authority to discard Cryptalis's primary-error rule.

Existing `tests/test_sqlalchemy_async_cleanup.py:13-159` supplies useful row-lock/state-before-close and real task cancellation controls but never combines primary prep failure with secondary rollback failure. `tests/test_sqlalchemy_flush_preparation_failure.py:72-103,199-227` covers failed-flush rollback/invalidation faults at a different boundary. `tests/test_sqlalchemy_savepoints.py:166-189` protects whole-unit nonpublication after native SAVEPOINT control failure.

## Detach alternative: not recommended in this slice

`await session.connection()` followed by `AsyncConnection.run_sync(Connection.detach)` is technically reachable through public APIs but is not a pure lookup of an already-owned connection.

In 2.0.51, `ext/asyncio/session.py:929-937` delegates to sync Session.connection. `orm/session.py:2054-2113,1158-1206` shows that absent connection ownership can cause a pool checkout/root transaction and that a lazy nested transaction can create a SAVEPOINT. `in_transaction()` alone does not prove a connection already exists. Obtaining one only for cleanup therefore adds database work after preparation has already failed.

`engine/base.py:752-786` (2.1.3:768-802) says detach leaves the Connection usable and makes normal later close physically close instead of return the DBAPI connection to the pool. In nested use it detaches the root socket, including still-valid outer work. It does not itself roll back or release locks. This changes pooling and normal cleanup lifetime even if nested rollback succeeds.

There is also a source-only composition concern: `_ConnectionFairy.detach` clears `_connection_record`; `_ConnectionFairy.invalidate` invokes record invalidation only when that record exists, then clears its DBAPI reference. See 2.0.51 `pool/base.py:1476-1514` and 2.1.3 `pool/base.py:1506-1550`. No explicit detached-driver close is visible on that invalidation branch. Current protected SAVEPOINT failure calls Connection.invalidate, so combining detach with that mechanism needs an independent native/real-PostgreSQL experiment. This is not a reproduced leak claim.

Public detach is consequently not a drop-in guarantee, and saving a raw driver to close after root exit can target a socket whose pool ownership has changed. Defer either design. A narrow primary-preserving UNKNOWN correction can be reviewed independently without asserting full quarantine closure.

## Draft source review, 22:27 UTC

Reviewed the author's separate `candidate-next-unblocked-correctness-20261014/src/cryptalis/sqlalchemy.py:1058-1091` and complete `tests/test_sqlalchemy_async_exit_double_failure.py` read-only. No static blocker was found for the bounded primary/UNKNOWN scope. The implementation clears preparation before cleanup, preserves the original exception, sets typed failure effects to unknown and retryable to False, uses fixed diagnostic notes and suppresses secondary traceback display, then attempts only public Session invalidation. No detach or saved-driver closure was introduced.

The new source defines 16 parameterized planned cases, including native/protected ordinary/injected-cancellation comparisons, additional invalidation failure, real task cancellation and sync-body preservation. No cases were collected or executed. The native and deliberately failed-invalidation arms perform explicit cleanup before their database observation, so they do not establish pre-cleanup native-effects equivalence. The new nested setup has no preflushed outer prefix; whole-outer-prefix discard remains dependent on existing SAVEPOINT regressions. These are evidence limits, not static failure findings.
