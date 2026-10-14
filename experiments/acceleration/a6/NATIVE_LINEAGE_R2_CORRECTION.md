# R2: context-local mixed-ID observation

Prepared 2026-10-14. No database tests run by this worker.
Historical R1 evidence is unchanged at evidence/a6-native-uow-lineage-sa21-20261014:
8 PASS, 2 FAIL, 1.62 seconds, as run by root. R1 candidate is also unchanged.

## Exact cause

The mixed-ID test kept only implicit-ID objects in tracking.rows. It emitted
those objects in an earlier native execution, followed by an explicit-ID
execution. At the latter cursor event, earlier implicit IDs were correctly
assigned by native postfetch. The reused A5 observer's blanket assertion that
all tracked implicit IDs remain NO_VALUE was therefore invalid. The explicit
object itself was not included in that tracking list.

R2 changes only the mixed-ID observer. It associates the current cursor context
with exact compiled groups, asserts unassigned identity for that context's
implicit rows, and checks the unchanged explicit identity for its explicit row.
Earlier completed implicit contexts are checked against their exact producer
record and native postfetch result. Every row must appear exactly once in these
bounded small executions. Original producer/compiler/context/postfetch identity
assertions and original eight A5 control bodies remain unchanged. Default
callbacks, evaluation ordering, input dictionaries and state assignment remain
unchanged. This is a test fixture correction, not product compatibility work.

## Source-origin investigation

R1's copied helper pyc contains co_filename pointing to the older A5 candidate.
Its source helper SHA256 is b12997edabab634c01c8b26f8f946392a70503d55389fa6cd826f979b33535e2,
identical to A5. Reading the pyc with marshal, without execution, reproduced
that filename. This explains the traceback filename; the old run did not record
the helper's live __file__, so its actual module origin is not asserted from
that filename alone. Root's existing package-origin check covers Cryptalis,
not these helper modules.

R2 was copied excluding __pycache__ and .pytest_cache. Historical caches were
not removed or altered. The new fixture validates helper __file__ and selected
helper code filenames against its own candidate tests directory, verifies the
A5 and migration helper source hashes, and checks all eight recorded installed
SQLAlchemy source hashes for the exact 2.1.3 or 2.0.51 version before installing
any observer. Unknown version/source or wrong helper origin fails closed.
These are source/version guards for this experiment, not a public runtime API.

## Static cleanup review

- Emitter ContextVar reset remains in finally for success and exceptions.
- Private patches use pytest's function-scoped monkeypatch fixture; pytest
  restores them even after a failed assertion. No on-disk library edits occur.
- The global Engine before_execute observer is removed in fixture finally.
- Mixed-case Session/mapper/engine listeners are removed in context-manager
  finally, including when cursor assertions or flush fail.
- Sessions close and async engines dispose through the inherited cleanup style.
- Traces intentionally retain synthetic evidence until test teardown. They do
  not confer protected authorization or claim production packet cleanup.

R2 selector remains scripts/test_postgres.py -- -q tests/test_sqlalchemy_native_uow_lineage.py
Expected case count remains ten. Root must use unchanged wrapper and existing
pinned interpreters, with fresh role preflight. No test, import, callback, DB or
Git operation was executed by this worker. Python compile() checked syntax only.
