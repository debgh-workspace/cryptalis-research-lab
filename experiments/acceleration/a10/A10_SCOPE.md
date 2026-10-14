# A10: Expired integer-version ORM writes

## Finding and selection

No new confirmed native-behavior defect was established in this read-only triage.
The known client-default route still needs owner approval for a private-hook encrypted
prototype. Required/default expanding-bind cache order is already characterized in
candidate-notes-native-bind-cache-20261014 and C9; repeating it is not this slice.

The new question is whether the admitted ordinary versioned UPDATE/DELETE path
preserves native reloading of an explicitly expired version column. A3 covers
loaded integer-version stale writes. A4 covers loaded integer-version stale writes
inside SAVEPOINTs. Neither selects explicit version-only or whole-row expiry.
In S20, sqlalchemy.py::_native_delete_rows checks loaded_value and rejects NO_VALUE.
That branch alone is not a defect: SQLAlchemy may reload the version before the
adapter sees the DELETE. The new real-native oracle decides that timing question.

## Scope and oracle

Compatibility.md requires native ORM state and owning-Session behavior. Architecture
requires native refresh and expiry. The existing A3 mapper has an application-assigned
UUID identity, ordinary integer version column and protected text; none changes.

Eight cases cross sync/async, UPDATE/DELETE and version-only/whole-row expiry.
Each native and attached case:

1. Loads version 1, explicitly expires the selected attributes, and proves the
   version is expired without causing a reload.
2. Updates protected text or deletes through ordinary ORM APIs, then flushes.
3. Records public Session and instance state. An independent reader proves that
   the committed row and, when protected, ciphertext bytes are unchanged.
4. Rolls back, compares state, and explicitly refreshes to recover version 1.
5. Repeats the expired write, commits, independently checks current values/version
   or absence, and reads through a fresh Session.

The paired oracle compares exact public state and final values. Independent attached
storage observations reuse A3's CF1 decoder and require retained plaintext NULL.
No implicit async attribute I/O is introduced by the test. Both native and attached
paths must pass; a native failure is a fixture/contract observation, not a product
regression. No newly unsupported grammar, defaults, or bulk DML are admitted.

## Validation and limits

- AST parse passed for the new test.
- All 208 inherited S20 files are byte-identical; receipt records each hash.
- No PostgreSQL execution, credentials, Git operations, installation, shared-tree
  source edits, or new dependencies by the worker.
- Actual PostgreSQL outcomes and any needed correction remain pending. This is
  test-only preparation, not VERIFIED behavior or a confirmed bug fix.
- Root alone runs the unchanged dual-role wrapper and promotes/publishes results.

Coordinator selector from this isolated candidate, once per pinned interpreter:

    <pinned-python> scripts/test_postgres.py -- -q tests/test_sqlalchemy_expired_version.py

The slice does not cover arbitrary version generators, server versions, every
concurrent schedule, deferred mapping admission, provider custody, or the full
qualification gates. Existing seven legacy failures and seven UNKNOWN gates remain.
