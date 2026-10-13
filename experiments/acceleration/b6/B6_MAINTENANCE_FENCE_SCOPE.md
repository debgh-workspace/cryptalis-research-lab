# B6: warmed-worker maintenance guard

## Contract and finite acceptance gate

This test-only S18 derivative checks an existing database guarantee. A warmed
attachment has already read and authenticated the fixture, retains its mapped
objects and bounded local root cache, ends its database transaction, and queues
an ordinary ORM write. Reverse maintenance then installs its durable guard.
The pending write must receive PostgreSQL SQLSTATE `55000`. It must change no
row bytes, native catalog facts, guard definitions, or journal state. Explicit
rollback and a legitimate pre-switch abort must restore that same attachment's
ordinary write behavior under the unchanged source authority.

The new finite matrix is sync/async × INSERT/UPDATE/DELETE × EXPANDED/VERIFIED:
12 cases. The endpoints cover the first committed pause and last abortable
pause. Existing direct-runtime reconnect controls cover EXPANDED, BACKFILLED,
VERIFIED, and PLAINTEXT_PENDING. Existing publication and abort controls remain
unchanged. Full verification is still performed to reach VERIFIED.

The SQL execution counter stores booleans only. The failure must come from the
real PostgreSQL trigger rather than an unsupported query or missing key. A
counted public-fixture provider proves the retained root lease is warm; no
expiry is extended. Native pre-protection rows and the existing independent
CF1 decoder establish complete value/membership parity. All unaffected
ciphertext must retain its exact bytes. The successful identical DML after
abort is the sensitivity/recovery control.

No database test has been run by this worker. The coordinator must run both
unchanged PostgreSQL-preflight dependency cells before any VERIFIED claim.

## Current authority boundary and unresolved choice

Canonical `docs/lifecycle.md`, Maintenance and ownership, requires the operator
to stop known workers/jobs and exclude unsupported writers. It explicitly says
that an empty connection snapshot does not establish exclusion of reconnecting
writers. It retains one journal, a cooperating advisory lock, and a bounded
maintenance pause; it does not require worker registrations or per-request
mutation ledgers.

The same file, Plan and phases, requires the database and independent deployment
pin to select the same representation. Artifact publication is a separate
effect. Writers stay stopped across the publication gap; missing provenance
keeps service stopped. Supported deployment candidate requires old transactions
to finish, alternate credentials to be unable to restart a writer, exact artifact
publication by the trusted deployment tool, and restarted workers with fresh
target credentials and empty key caches.

Canonical `docs/security.md`, Threat limits, excludes immediate arbitrary-process
revocation and invisible RAM-clone denial. Its key-cache contract permits a warm
admitted key to operate only until its existing deadline. `docs/decisions.md`,
Selected choices and Deleted mechanisms, selects current deployment authority
outside restore and removes the prior distributed fencing/registered-worker
protocol. Approved decision 7 says no production publication/restore procedure
is selected. The 2026-10-09 A4 amendment authorizes isolated rotation work; it
does not select that missing host procedure or authorize new credentials.

Source inspection agrees: `sqlalchemy._Attachment.validate` performs attachment
admission; `_ring` compares against the attachment's supplied plan and pinned
search root. It does not consult a new current host pin on every transaction.
`deprotection._guard` denies non-owner writes during maintenance; abort removes
it after restoring the same source authority. These are not persistent
post-publication old-worker fences. Wrapper-only rewrap keeps the roots and
physical schema unchanged, so schema mismatch cannot establish old-worker
termination. Database write triggers also do not recall cached plaintext/keys.

**Actionable owner decision before active-rotation integration:** identify the
existing trusted release system/operator and select its concrete mechanism to
terminate inventoried old workers and prevent their old workload credentials
from regaining write access across publication and restart. If that mechanism
cannot be evidenced, keep active publication blocked. A permanent operation-token
or database-trigger authority is a separate contract/security decision; this
slice does not implement one. Actual persistent credential/privilege changes
still need their action-time approvals. Retained encrypted backup readers and
their exact prior artifact bytes remain obligations throughout.

## Limits

This controlled negative test intentionally queues an old writer in an owned
fixture. It establishes defense during the durable pause only. It does not
prove deployment-wide worker inventory/termination, authentication turnover,
old-reader revocation, external publication, active rotation, provider custody,
or production qualification. No provider service, role/credential handoff,
cluster, active policy, or runtime source changes are part of this candidate.
The seven historical legacy-profile failures and all seven UNKNOWN production
gates remain unchanged.

## Coordinator-only proposed command

Use the coordinator's unchanged `lab_session.py` wrapper, this candidate as the
source, and its unchanged `scripts/test_postgres.py` with each pinned SA21/SA20
interpreter. The exact pytest arguments are:

```text
-q tests/test_warm_worker_maintenance_fence.py tests/test_deprotection.py::test_runtime_writes_remain_fenced_until_publication tests/test_deprotection.py::test_pending_requires_explicit_external_publication tests/test_deprotection.py::test_abort_before_switch_restores_current_protected_application --tb=short -ra
```

Expected selection: 12 new warmed-attachment cases plus 6 unchanged controls.
Any failure must remain visible and be classified before changing runtime.
