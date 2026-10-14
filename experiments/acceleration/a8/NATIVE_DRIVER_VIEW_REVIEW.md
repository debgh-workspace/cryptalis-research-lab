# A8 prepared synthetic driver-only view

Status: prepared, syntax check only. Root alone executes the unchanged PG wrapper.
Base: candidate-native-slot-probes-20261014 (A7), copied without bytecode caches.
All A7 inherited files remain unchanged. No production source or API change.

## Minimal operation

The new test-only retval listener first validates the exact pending native
statement, parameter container and composed slot provenance with A7's unchanged
SlotProbe.before_cursor. It then allocates a NEW dictionary or tuple. Only label
slots whose actual source bind key is label are changed, using the proven exact
InstanceState, context and logical dictionary for that driver slot. The new
plain TEXT value is:

synthetic-driver-view|<native UUID>|<explicit tenant UUID>|<logical label>

This string is public synthetic test data, not encryption, authentication or a
secure envelope. NULL labels remain NULL so native NOT NULL errors stay real.
No default is evaluated by the listener. It never assigns an ORM ID or tenant.

The original batch parameter object, source driver rows, native compiled
dictionaries and ORM values are retained and repeatedly checked for identity
and unchanged contents. The original A7 source probes and all source/version
hash guards remain intact. A new dependency guard verifies the copied A7 probe
and factory helper bytes and module origins before the test proceeds.

## Actual callback dictionary oracle

A scoped observer calls the original get_current_parameters accessor exactly
once and returns its exact result to the unchanged UUID callback. It retains
that same dictionary by reference. Assertions allow the native ID default to
populate its own ID, but require all non-ID values to remain identical across
view construction, native postfetch, commit, failure and retry. No callback is
wrapped or replaced, no new default is introduced, and no protected wrapper is
made visible to any default.

## Independent observation and database oracle

The transformed listener is followed only by a read-only final collector in
this controlled test chain. It sees the exact newly returned parameter object.
A separate owner connection reads stored ordinary TEXT by actual row ID.
Expected strings are checked independently using that row's native ORM UUID,
explicit known tenant and unchanged logical label; expectations are not derived
from producer receipt order, cursor ordering or the transform function. Three
identical logical labels must still map to their own distinct native UUIDs.

Later MUTATING listeners are deliberately not tested or admitted. A public
cursor event is still after bind processing and cannot bypass the existing
sealed-only payload processor. A8 is not protected implicit-default support,
a post-default/pre-bind public hook, or an authorization-boundary promotion.

## Prepared matrix: 24 cases

16 paired cases: sync/async x named/positional x success, native UUID-callback
failure with retry, native NOT NULL failure with retry, and local view failure
with retry. Each compares an untransformed native-driver control with the
separate-view run. Both halves use A7's already separately validated source
probes. A7 owns original-versus-instrumented native producer parity; A8 does not
relabel its instrumented control as an entirely uninstrumented run.

The local fault is injected for the exact third InstanceState. It occurs after
the first native two-row batch reached the cursor but before the third row's
batch reaches the final collector. Both control and view half receive the same
synthetic local fault. Require native inactive Session, absent object IDs,
transaction rollback, zero committed rows, fresh native callback attempts and
successful retry. No database-driver failure is fabricated for this case.

8 earlier rewrite cases: sync/async x named/positional x equal/reordered copies.
Require exact receipt refusal before a view or final collector sees a batch,
zero committed rows, native failure state and explicit rollback. Value equality
never restores a copied container's authority.

## Cleanup and bounded scope

Source patches and accessor observation use nested monkeypatch contexts.
Listeners are removed and Session/engine resources closed in finally; pending
source receipts clear on unwind through the unchanged A7 scope. Historical trace
references remain only for these tests. No installed files are edited.

The same bounded A7 shapes apply: ordinary mapped TEXT, explicit loaded tenant,
client UUID callbacks, psycopg pyformat/format and native 2+1 IMV pages. Unsupported
positional slices/outside-VALUES binds and native downgrade paths still fail;
no relationship/default-generated tenant, arbitrary dialect or later-listener
security claim is made. No key material or protected route is involved.

## Root-only selector

scripts/test_postgres.py -- -q tests/test_sqlalchemy_native_driver_view.py

Use existing pinned interpreters and unchanged fresh-role preflight. A failed
probe stops the run. This worker performed no imports, callbacks, DB tests or
Git operations. Only Python compile() checked the new test module's syntax.
