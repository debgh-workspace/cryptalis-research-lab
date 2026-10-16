# Failed-flush diagnostic continuation: isolated source proposal

Status: IMPLEMENTED IN ISOLATED SOURCE; NOT EXECUTED OR QUALIFIED.

## One defect and existing contract

The selected source is `candidate-doctor-remedy-integrated221-v1-20261015`.
Its `src/cryptalis/sqlalchemy.py:944-960` calls the primary exception's dynamic
`add_note` before native failed-flush cleanup and again after cleanup failure.
An overridden method or an unavailable notes list can replace the primary
exception. The first call can prevent cleanup entirely. In
`src/cryptalis/_sqlalchemy_transactions.py:166-183`, note delivery after failed
invalidation precedes physical-close fallback; another note precedes completion
of the remaining connection loop. The same failure class can interrupt these
steps and replace the rollback exception.

This violates the existing primary-failure preservation rule in
`ENGINEERING_PLAYBOOK.md`, "Fail loudly and explicitly". The approved async
transaction-exit implementation already bypasses a custom note hook and catches
note delivery failure (`sqlalchemy.py`, `_AsyncTransaction.__aexit__`). Apply that
same local pattern only to the two failed-flush helpers. There is no query,
mapping, provider, supported-operation, or refusal-contract change. Failure
remains observable. Lost diagnostic notes do not prove rollback or release.

The original files are preserved. Their SHA256 values are:

- `sqlalchemy.py`: `28cf5c4991aae1cb4f3baf6a5630b30d675cb2308e842ce09fd6a04ddaaf5a88`
- `_sqlalchemy_transactions.py`: `cb128481811576d8f16b233d4a30fca060eb9a1bfc4459d5e7e129434cc522ec`

`source/src/cryptalis/` is a sparse derivative containing only these two copied
and amended files. It is not a complete runnable package or a promoted candidate.

## Why this is new evidence

Existing `tests/test_sqlalchemy_flush_preparation_failure.py` covers ordinary
provider failures, real cancellation and rollback/invalidation faults. It does
not inject note delivery failure in these helpers.
`tests/test_sqlalchemy_async_exit_double_failure.py:293` covers overridden and
unavailable notes, but through `_AsyncTransaction.__aexit__` after a healthy
flush. It does not cover the helper paths amended here.

An ordinary provider Exception is sanitized to a fresh KeyUnavailable by
Keyring; its original identity is not a valid public-path oracle. A cancellation
subclass can pass through the async Keyring boundary because it catches
Exception. The proposed direct-helper tests isolate the diagnostic/cleanup
state machine. They do not claim public-provider-path or real database evidence.

## Focused regression proposal

`regression/test_flush_diagnostic_continuation.py` is a standalone stdlib
unittest file. It imports real Cryptalis modules and real admitted SQLAlchemy;
no function-body extraction, pytest, conftest, fixtures, plugin discovery,
engine creation, provider construction, SQL, connection or DB status is used.
Session, transaction, connection and driver doubles expose only the local
control-flow outcomes. `native_scope` remains the actual imported implementation.

Three test methods contain 15 deterministic subcases:

1. Nine combinations: ordinary/overridden/unavailable notes crossed with
   successful cleanup/rollback failure/incomplete quarantine. Require the same
   primary object, cleared preparation material, exactly one cleanup attempt in
   the primary exception context, no custom output hook, and safe notes when
   their channel is available.
2. Four combinations: overridden/unavailable notes crossed with successful or
   failed first physical close after invalidation failure. Require original
   rollback exception identity, first close attempted, later connection
   invalidated, and exact incomplete-quarantine flag. No physical release claim
   follows from fake driver completion.
3. Two controls: absent/inactive transaction remains a no-op.

Prospective RED: unchanged baseline should fail six first-method subcases and
all four second-method subcases. The three ordinary-note and two no-op controls
should pass. This is a prediction, not a test result. All 15 subcases must pass
against the amended source in each selected dependency cell; source selection,
import origin and unexpected count changes must be independently investigated.

## Explicitly unresolved neighboring faults

This is only the note-dispatch/delivery slice. Independent review identified
additional hooks outside the guarded note call: assigning or reading the
`_cryptalis_quarantine_incomplete` attribute can itself raise, and a failed
transition from False to True can leave stale status. Also,
`type(error).__name__` message construction occurs before entering `note` and
could invoke an exceptional metaclass hook. These paths remain unchanged and
unresolved. No claim that all diagnostic-path failures are corrected is made.
Any change to marker propagation or outcome representation requires its own
minimal design, review and regression slice. The tests here use ordinary marker
attributes and ordinary exception classes, except for the named note hook.

## Remaining gates and reversibility

Root must first admit the exact finite startup/import map and independently
review these files. Then root may select separate baseline and amended no-site
unit runs. Preserve every RED outcome and unexpected error. A subsequent native
integration proposal should add the same two note faults to a cold asynchronous
provider cancellation during a failed flush with real root/SAVEPOINT state
oracles and the established cleanup guards. It requires separate admission;
this proposal does not execute or prepare database actions.

The frozen source, installed cells, prior tests and preview remain unchanged.
Discarding this isolated derivative is the entire rollback. No migration or
authority state changes are involved. There is no deadline-based gate reduction.
