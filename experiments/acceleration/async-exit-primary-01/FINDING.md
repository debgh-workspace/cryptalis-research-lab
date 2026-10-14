# ASYNC-EXIT-PRIMARY-01: source-supported correction proposal

Status: source-only, unexecuted. No RED/GREEN, runtime recovery, release or production claim.

## Supported trigger and contract

S25 `_AsyncTransaction.__aexit__` prepares keys after a normal context body. If that preparation fails, it invokes native transaction exit with the primary exception. A secondary native rollback error propagates before the final `raise`, replacing the original provider failure or cancellation. Both pinned native SQLAlchemy sources delegate to synchronous transaction exit and propagate that secondary error.

The independent contract is `ENGINEERING_PLAYBOOK.md`, “Fail loudly and explicitly”: retain the primary when cleanup or error-output handling also fails. `docs/security.md` requires safe diagnostics and explicit uncertainty, without raw secondary text or a false rollback claim. `docs/architecture/README.md` requires failed preparation to be cleared. The existing async cleanup tests cover successful rollback after provider/cancellation faults; their native/data oracles do not cover this double failure.

Canonical baseline: `candidate-s25-async-sqlmodel-integration-20261014`, 216 files; original manifest SHA256 `3fc6eb1e3a70a4401aec1338798463b6d7170992539723b4ed294f247f5fd703`. The authoritative checklist and S24/S25 addendum retain the seven historical failures and all seven UNKNOWN gates. No original assertion, skip, acceptance disposition or objective changes here.

## Exact bounded proposal

One runtime file changes: `src/cryptalis/sqlalchemy.py`, only the adapter-owned failed-preparation branch of `_AsyncTransaction.__aexit__`.

- Clear retained preparation before native cleanup, including when cleanup succeeds.
- On secondary failure, retain the exact sanitized primary object, operation ID, code and stage. Keep actual task cancellation as cancellation.
- Mark a CryptoFailure's local effects UNKNOWN and its retryability false.
- Add fixed cleanup/discard/inspection notes. Bypass exception-subclass output hooks with `BaseException.add_note`; if note delivery itself fails, preserve the primary and continue the cleanup attempt. That exceptional output path makes no delivered-note claim.
- Attempt public `AsyncSession.invalidate()` and report its failure through a second fixed note where note delivery works.
- Re-raise the primary with suppressed display chaining. This does not erase raw exception objects from the trusted process's in-memory graph.

No transaction-state assignment, new private SQLAlchemy hook, connection acquisition, detach, saved-driver close, capability admission, new engine setting or provider change is added. Sync/body-error native exit remains unchanged.

## Important limits

This is a primary-failure/explicit-UNKNOWN correction, not a universal physical-quarantine fix. Native root rollback can close/remove the Connection before raising its saved error. A later public Session.invalidate can then be a no-op for that former physical connection. Never equate no transaction, zero checkouts or a successful invalidate return with physical rollback proof.

Retaining a raw driver and closing it after pool ownership changes is excluded. Upfront detach changes pooling and its composition with native invalidation needs separate evidence. Existing failed-SAVEPOINT invalidation remains byte-identical and is selected for regression.

The new tests use one-shot public callback faults before rollback SQL/driver dispatch. They are not physical transport faults. Independent row-lock/data checks and a later real checkout/commit are required before teardown in ordinary protected arms. Native controls and intentionally failed-invalidation arms have explicit laboratory rescue first; they do not prove pre-rescue native effect equality or successful physical quarantine.

CryptoFailure's existing IPC reducer does not preserve these new per-instance effects/retryability fields or notes. Cross-process diagnostic transport remains unqualified; this slice changes the local exception boundary only.

Independent static contract review: `reviewer-notes/async-cleanup-primary-contract-20261014/contract-review.md`. It supports the narrow boundary and explicitly rejects universal-quarantine claims. A new final source/command review is required for this frozen packet.
