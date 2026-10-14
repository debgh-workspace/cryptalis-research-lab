# Separate V3 DML2 runtime evidence review

Reviewed 2026-10-14 UTC. Evidence:
`evidence/s24-async-sqlmodel-public-v3-dml-20261014`.

## Decision

**Accept the exact two-node DML-result experiment as a bounded synthetic
post-result fault result.** Actual terminal: **2 PASS, 36 deselected, 0.62
seconds**. Root and SAVEPOINT are the exact cleared node IDs. JUnit, progress
and runner receipt agree; all setup/call/teardown phases pass, with no failures,
errors or skips. This reviewer performed no tests or database operations.

This is not natural psycopg-failure equivalence, broad DML permission,
production async SQLModel admission, installed qualification, encrypted-default
integration, or a full adapter/regression gate. All seven broad runner gates
remain UNKNOWN. The default-off product source is unchanged.

## Exact native and protected reach

All four expected arm/unit combinations have genuine post-result reach records:
native/root, protected/root, native/SAVEPOINT and protected/SAVEPOINT. Each
records the completed original native helper, genuine UPDATE and reached
synthetic fault. Native driver cursor type is SQLAlchemy's psycopg async
adapter; protected cursor type is the existing Cryptalis guard cursor. The
pinned test asserts the exact observed completed UPDATE cursor identity and
that the original helper returns the same result with id/label keys before
writing these records. All completed results are CursorResult.

All four combinations also have completed recovery records. Native policy is
`native-committable`; protected policy is `quarantined`. Every record marks the
fault synthetic and recovery successful. Source hash identity plus final JUnit
PASS establish the strict exact injected DBAPIError identity assertion in each
arm; no provider-sanitization relaxation was applied to this later result seam.

## Deliberately different transaction policies

The retained source and passing assertions establish these outcomes before
subsequent recovery:

- Native root and native SAVEPOINT: no Cryptalis failed-unit cleanup, session
  and selected transaction active, successful commit of both the outer update
  and the completed-before-fault update.
- Protected root: exactly one cleanup for the expected synchronous session,
  inactive session/unit, commit rejected, explicit root rollback; the outer
  row returns to NULL and the faulted row remains `old-2`.
- Protected SAVEPOINT: exactly one cleanup, inactive failed nested unit,
  rejected commit until rollback of that SAVEPOINT, then permitted outer commit;
  the outer row remains `outer-valid` while the faulted row remains `old-2`.

Every arm subsequently writes and commits `recovered` successfully. The
protected-table baseline is unchanged; this fixture's baseline is not evidence
for every possible prepopulated protected-data scenario. The test explicitly
checks zero checked-out connections after failure recovery and completes the
normal enclosing session/engine/application cleanup paths.

The original SQLModel helper and cleanup observer identities are restored.
The prior non-None ContextVar marker is restored before its token is reset;
observer removal and token restoration are in finally paths. JUnit PASS also
covers the post-receipt normal context exit, which is essential because the
DML completion record itself is emitted before that final exit. Four receipts
alone would not have sufficed.

The synthetic seam is test-only and occurs after a genuine native result. It
must not be described as a naturally observed database or network fault.

## Integrity and exact execution

The copied coordinator command is byte-identical to the cleared standalone
DML2_ROOT_COMMAND.txt, SHA256:
`16f0cfac76ea8e7db2d0b19b0622a37cd6ef44e898bb79c5a255276c3bdfdcf1`.
It uses the unchanged corpus wrapper, V2 product source, existing dependency
interpreter, fresh evidence path and exact two-node selector.

All **961 current input hashes** match. Coordinator before/after logs each
contain exactly **961 expected OK lines**; wrapper and pin-check exits are 0.
The safe wrapper log records PostgreSQL start, readiness, package-origin, tests
and stop exits as 0. The safe stop log confirms the server stopped. Runner exit
is 0, and the existing role/database preflight passed.

Both runtime origin receipts confirm the exact candidate-local fixture and
Cryptalis origins, Python 3.14.8, SQLAlchemy 2.0.51, SQLModel 0.0.47 and psycopg
3.3.6. Runtime checks cover 214 source files and 16 selected dependency files;
current byte checks independently match those pins. The 153-file product
snapshot and five-file external Python snapshot are unchanged and match their
archives. The V3 test SHA256 is still:
`934e9207486a92e1a7322928e1f896727f1708f2d5fde4cbba5f2df829d697d6`.

All **26 shared corpus files** match their prior snapshots and current bytes,
with unchanged name set, no candidate corpus output/deletion and no restoration
errors. All **24 root-level non-Python V3 packet files** are archived and match
the frozen originals. Those archived plans retain their historical NOT RUN
labels; this separate actual runtime receipt/review records the later execution
without rewriting preparation history.

## Overall finite evidence boundary

The preserved sequence is:

- V2 baseline RED: 6 intended attachment failures / 2 passes after six native
  arm completions.
- V2 core: 33 passes / 3 invalid provider-identity-oracle failures, retained.
- V3 corrected targeted provider selection: 3 passes.
- V3 core: 36 passes.
- Separate V3 synthetic DML-result selection: 2 passes.

Core36 plus DML2 covers the 38 distinct V3 packet nodes. Targeted3 is an
overlapping subset, not three additional unique capabilities or corpus keys.
No historical gap reduction, corpus reconciliation, broader admission,
production provider custody, installed suite or real-application claim follows.

## Reviewer artifacts and actions

`dml2-runtime-checks.json` is the machine-readable audit;
`audit_dml2_data.py` reproduces its safe-data comparisons. All review artifacts
are covered by REVIEWER_OUTPUTS.sha256.

Only safe logs, JUnit, progress, runner/source/origin/corpus receipts, saved
source, and permitted opaque SHA256 inputs were read. No environment values or
raw phase JSON contents were inspected, copied, displayed or retained. No
target import, compilation, collection, tests, DB operation, source modification,
installation, Git/ref write, remote action or feature promotion occurred.
