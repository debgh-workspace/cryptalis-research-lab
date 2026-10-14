# Native producer in-body slot receipts: prepared research tests

Status: prepared, syntax/AST checks only. Root owns PostgreSQL execution.
Base: candidate-native-uow-lineage-r2-20261014, copied without bytecode caches.
All inherited files are unchanged. Public-cursor blocker, prior failed/successful
evidence and the unrun scalar draft remain unchanged in their own candidates.

## Goal and honest boundary

Observe the actual logical-dictionary to driver-container and driver-bind to
IMV-slot transformations where SQLAlchemy produces them. No value matching,
parsed suffixes or after-the-fact zip of independent arrays establishes origin.
No ciphertext, keys, sealed placeholders, protected route or product admission.
The experiment does not transform stored data. It proves or disproves native
identity receipts and untouched native outcomes in a bounded synthetic mapping.

## Deliberate private fork surface

The new helper parses source for the installed original implementations of
DefaultExecutionContext._init_compiled and
SQLCompiler._deliver_insertmanyvalues_batches. It makes instrumented function
copies in memory and installs them with function-scoped monkeypatch.context.
Installed SQLAlchemy files are never edited. Both exact installed versions and
eight source hashes are checked by the inherited lineage fixture before any
patch. AST insertion counts must exactly match both inspected implementations;
unexpected structures fail instead of silently receiving partial coverage.

This is source-instrumented, version-specific upstream-hook/fork research.
It is more invasive than wrapper observation, adds frames and allocations, and
can affect timing/stack inspection. It is not an existing public API and cannot
be presented as a production integration design. Native differential tests
compare supported outcomes, not every possible Python introspection effect.

## Observation sites

1. Native positional bind list comprehension: an enumerate of the same native
   positiontup supplies the actual construction slot. The key and produced
   scalar pass through a recording call unchanged. This slot is captured during
   actual producer construction, not inferred later from row width or values.
2. Native named bind dictionary comprehensions: a temporary named expression
   retains the actual key expression result, evaluated once. A recording call
   gets exact context, logical dictionary, source bind key, actual driver key
   and produced scalar; it returns the identical scalar.
3. Immediately after each original driver-list append: record the exact logical
   dictionary and the driver container just appended by that same statement.
   No independent list pairing is used.
4. Native named IMV dictionary assembly: record the actual key expression once,
   exact destination dictionary, exact source driver row and source bind key at
   construction. The original dictionary update still performs the write.
5. Native positional IMV chain input: an observing iterator yields each exact
   native driver tuple unchanged to the original chain.from_iterable. Source
   slots are captured while those tuples are consumed, with output positions
   assigned along that actual construction traversal. The tuple must already
   have an exact driver producer receipt. Sliced copies are refused.
6. Every native IMV batch construction: record the original batch object and
   replacement parameters without rewriting them. Actual source driver-row
   references must belong to that exact batch. Integrity checks verify the
   expected produced scalar at its already-established output slot.
7. Public before_cursor_execute: accept only the exact native replacement
   parameter object and statement object for that context's pending receipt.
   Compose the captured output-slot, driver-source and logical-state receipts.
   Values only check integrity after identity provenance exists.

See AST_PROBE_INSERTIONS.md for the small semantic insertion sketch. The helper
never calls a UUID callback itself, replaces a default, changes the original
UOW record, assigns an ORM identity or mutates native compiled parameters.

## Bounded scope and refusals

Synthetic ordinary mapped table only, three client-default UUID rows with equal
ordinary values, explicit loaded tenant, psycopg named pyformat or positional
format. Page size two forces a genuine two-row IMV batch and final single-row
batch for the same native execution context. No guessed event count authorizes
those batches; assertions inspect the actual producer batch metadata.

Positional input must be the actual unsliced native driver tuple. Outside-VALUES
leading/trailing binds, copied slices and native IMV downgrade paths lack the
complete inserted receipt route and fail loudly. The suite does not claim them.
It also does not claim arbitrary dialects, protected payloads, inheritance,
relationship-derived tenants, mixed explicit/default groups or bulk APIs.
Those earlier native cases remain separate R2 evidence.

Equal parameter copies and reordered copies before the checking cursor listener
must lose authority and fail before driver execution. For named parameters,
reversed dictionary order remains semantically equivalent, but it is still a
replacement container and must be refused. Positional reversal additionally
changes slot meaning. No listener is granted a provenance-transfer exemption.
The listener is deliberately last in this controlled test chain. Protection
against later third-party listeners is NOT established and still requires a
future admission/ordering design.

## Prepared tests and independent outcomes

12 paired differential cases: sync/async x named/positional x success/callback
failure with retry/NOT NULL failure with retry. Each case executes once with
original producer functions and once with copied instrumented producers.
Both runs retain the existing R2 observation fixture; no new in-body probes run
in the original half. Compare callback records, generated UUIDs, logical labels,
failed-flush identity/session state, retry outcomes and committed native rows.
Separate owner-connection reads verify actual stored ordinary TEXT. UUIDs are
deterministic only because this pre-existing synthetic callback chooses them.

8 negative rewrite cases: sync/async x named/positional x equal/reordered copy.
Require exact receipt refusal, no successful cursor receipt, absent object IDs,
failed native Session and zero committed rows, followed by explicit rollback.

Expected total: 20 tests. No test was imported or executed by the worker.
Static checks compiled both new Python files and applied the AST rewriter to
both installed source trees, compiled resulting ASTs and verified insertion
counts. This does not execute the copied function bodies or prove DB behavior.

## Cleanup

The new patches restore on success, assertion/default/driver failure and early
return via monkeypatch.context. Finally clears pending batch and temporary slot
receipts. Listener removal and engine/session cleanup occur in finally. Tests
assert both private function identities were restored before closing the test
Session. Evidence traces retain strong references until fixture teardown, which
is intentional test evidence retention rather than production key lifetime.

## Root-only selector

scripts/test_postgres.py -- -q tests/test_sqlalchemy_native_slot_probes.py

Run only from this candidate through unchanged wrapper and existing pinned
interpreters. Do not alter fresh role preflight, credentials, cluster or grants.
On failed readiness, stop. On unsupported-shape or missing-receipt failure,
preserve the result and inspect the exact source branch; never fall back to
value matching, suffix parsing or array pairing to make the test green.
