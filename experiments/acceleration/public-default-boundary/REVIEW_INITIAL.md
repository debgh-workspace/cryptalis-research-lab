# Public default-completion boundary: no qualifying alternative established

2026-10-14. Source research and public-event/type fake-DBAPI diagnostics only.
No Cryptalis runtime import, cryptography, database connection, PostgreSQL, dependency
installation, Git action, private hook override, product change, or admission change.
The isolated directory contains new diagnostic files only; inherited candidates were
read, not edited. No claim of independently audited evidence.

## Decision

Do not queue an encrypted implementation or PG run from this result. The inspected
public interfaces do not establish a route satisfying all current invariants. This
is a bounded negative finding, not a mathematical impossibility theorem about all
possible SQLAlchemy extensions. A9R2's native true/routed false retained
compiled_parameters list identity difference remains unresolved; nothing here
repairs its routing architecture or qualifies ordinary omitted UUID defaults.

## Evidence

The standalone public_boundary_probe.py uses the native unchanged DefaultDialect,
Engine, Session, ordinary TypeDecorator.process_bind_param, and public events. It
never subclasses ExecutionContext, patches native methods, or intercepts compiler
or UOW producers. A local fake DBAPI receives PUBLIC diagnostic markers only.
It validates the eight inherited A9 source pins before running for each exact
installed release, 2.1.3 and 2.0.51. Six cases per version complete with explicit
assertions and observations in sa21.json and sa20.json.

1. Native callback retains context, compiled_parameters list and current dict.
   Ordinary execution preserves list identity and logical marker.
2. A synthetic sealed-only rejection at the bind processor prevents the cursor
   event from running. This is a stage-placement diagnostic, not execution of
   Cryptalis's actual sealed guard.
3. A bind-processor Fault is wrapped as StatementError with the exact original
   object, and handle_error observes it on both versions.
4. Moving the same fault to before_cursor_execute yields the exact raw Fault,
   not StatementError, on both. In 2.1.3 handle_error runs; in 2.0.51 it does not.
   All three failure cases show inactive Session with failed transaction, absent
   ID and zero fake-driver calls. Explicit rollback and re-add of the same object
   succeed with a second callback invocation and native persistent state. No
   manual private-store teardown or object-ID repair occurs in this harness.
5. Replacing only the returned driver parameter dict preserves retained list and
   logical dictionary identity/content but leaves plaintext in compiled_parameters.
6. Mutating compiled dicts in place preserves list identity but changes the
   callback-retained logical dictionary; it also leaves the already-processed
   driver parameters unchanged. This mutation is a deliberately failing semantic
   alternative in an isolated diagnostic, not a proposed supported API mechanism.

The first draft incorrectly expected the 2.0 handle_error result on both versions;
2.1.3 failed that assertion. initial_probe.py.disabled preserves that exact draft.
The corrected probe explicitly asserts both version-specific outcomes. The original
failure was a harness assumption; it is not a product defect or waived parity check.

## Source constraints and inference

S20 src/cryptalis/sqlalchemy.py::_Payload.process_bind_param requires an exact
operation-bound _Sealed value before returning its body. Delaying ordinary plaintext
until a cursor callback therefore requires weakening or replacing that security
boundary. Existing S20 docs/decisions.md selects public hooks and native state;
no permission for such a weakening follows from this investigation.

Pinned 2.1.3 engine/default.py constructs compiled_parameters at 1661/1669,
executes defaults at 1695 and bind processors at 1775/1784. engine/base.py places
before_cursor_execute inside its exception handler at 1864-1874; the corresponding
2.0.51 callback is outside that try block. Native get_current_parameters provides
context-aware defaults their current logical inputs. TypeDecorator's public bind
method receives value and dialect, not execution context or exact owning UOW row.
These interfaces alone do not provide the A6/A7 exact producer-to-compiled-to-driver
receipt association. No positional, UUID-value, same-text or generated-name match
is substituted here. No IMV, executemany, async or relationship lineage claim.

Public documentation corroborates interface contracts (online docs are newer than
our installed pins, so exact execution claims come from the pinned local sources):
- https://docs.sqlalchemy.org/en/20/core/events.html#sqlalchemy.events.ConnectionEvents.before_cursor_execute
- https://docs.sqlalchemy.org/en/20/core/custom_types.html#sqlalchemy.types.TypeDecorator.process_bind_param
- https://docs.sqlalchemy.org/en/20/core/defaults.html#context-sensitive-default-functions

Early eager UUID evaluation changes call timing/error/postfetch behavior. Opaque
pending values inserted before defaults change what arbitrary context-aware
callbacks see. Leaving original values untouched preserves callback semantics but
also preserves plaintext in the public execution context. Replacing the list after
callbacks recreates A9R2's identity divergence; editing its dictionaries mutates
callback-retained native values. A cursor fault's wrapping differs from a bind
fault even when both native transactions roll back. These separate concerns cannot
be solved by a passing list-identity assertion alone.

## Next decision

No minimal viable actual-encrypted public-route RED slice is proposed because the
prerequisite mechanism is unestablished. An unchanged S20 refusal test could record
the adoption gap again, but would not advance it or justify DB use. Keep the private-
hook encrypted prototype approval pending and distinct. If a new public mechanism
is proposed, require an exact hook contract supplying post-default row/producer
association before sealed bind, retained-context identity AND logical-content
parity, native callback/error/retry behavior, and unchanged confidentiality and
final-driver guard; then review a real-CF1 test-only RED plan before any DB run.
All full qualification gates and existing legacy failures remain unchanged.
