# D4 bounded transaction-worker process death

Verified 2026-10-13 against the coordinator's corrected-source PostgreSQL runs:
twelve cases pass in each environment (SQLAlchemy 2.1.3: 7.04 seconds;
2.0.51: 6.89 seconds). The narrow review correction removes unused synthetic
plaintext from child IPC. Both runs passed unchanged dual-role preflights, source
and external stability checks, and server-stop exit 0. Static compilation passed.
This direct-child candidate preserves all 194 D3
files, including its source manifest and the four frozen D2 publication files.
Only the two new test files, this progress document and D4's manifest are added.

## Question and process boundary

Can the fixture recover after the actual death of an owned transaction worker
at either side of an acknowledged frame/dirty-retirement commit boundary?

The existing DevelopmentKeyProvider, Keyring and PreparedKeys deliberately reject
cross-process use. Their checks are unchanged. The surviving pytest supervisor
uses the existing D3 fixture provider and product CF1 encoder to seal a synthetic
claim. A fresh `multiprocessing` spawn child receives a value-free claim packet
(operation, key, token and live/tombstone bit), the expected operation/context pin
and sealed bytes over local IPC. The live bit is necessary to distinguish a live
SQL NULL frame from a deleted-row tombstone. No claimed plaintext, provider,
keyring, prepared key, root or wrapping-key object crosses IPC. The child inherits
only the already-preflighted test environment for its new database connections;
there is no new credential, role, provider profile or cluster.

This is transaction-process loss. It does not test the death or recovery of the
process that owns encryption keys. The parent retains the original volatile
provider. The child installs already sealed work through a new research helper
that preserves D3's transaction boundary and SQL checks; D3's original installer
is not modified. Transported bytes confer no authority: the child checks the
expected operation, full durable pin under a share lock, and exact current dirty
token under a row lock. Frame insertion and exact retirement share the outer
transaction. Final independent decoding detects context/value/membership errors.

## Fixed twelve-case schedule

Six work states each run at the two barriers: initial partial inventory, captured
update, captured delete, captured delete/reinsert, text-to-NULL and NULL-to-text.
The inherited fixture includes int64 extrema, negative keys, empty text, Unicode
and a live SQL NULL row. Writers finish and all supervisor database connections
close before the child starts. There is one owned child at a time.

1. The child connects and reconstructs the same durable operation. It installs
   the presealed claim in a nested transaction under an explicit outer transaction.
   It checks its own staged tuple and pending-token removal before reporting the
   `before_commit` barrier over the private pipe. It then waits for permission.
2. For the before-commit case, the supervisor sends no commit permission and kills
   only that child through its owned Process object. For the after-commit case,
   the supervisor sends `commit`, waits for `after_commit` acknowledgement sent
   after psycopg's outer COMMIT returns, then kills only that same child.
3. The supervisor joins and requires the exact SIGKILL exit status. A missing
   acknowledgement, early exit, setup/connection error or deadline fails the test;
   none can stand in for a successful injected process death. Each acknowledgement
   has a ten-second limit, child commands a twenty-second limit and reaping a
   five-second limit. These are test fail-fast bounds, not workload SLOs.
4. A new connection locks the pending row to wait for disconnected-transaction
   cleanup. Before-commit death must preserve the exact complete prior snapshot.
   After-commit death must preserve source/native/pin/cursor and all unrelated
   rows, remove exactly the claimed obligation and retain the exact sealed tuple.
5. D3 reconstruction opens new connections and a fresh key cache with the surviving
   provider. Before-commit work must install successfully. After-commit replay must
   refuse without changing any state or frame bytes. The remaining inventory and
   queue drain without reseeding already completed ranges.
6. The unchanged D3 observer opens a separate read-only repeatable-read snapshot,
   requires complete inventory and an empty queue, independently decodes every
   live frame with D2, and compares complete source/native membership and values.

The tests never signal a PostgreSQL backend, server, service or process group.
They do not restart the server or introduce independent concurrent lab sessions.
The existing coordinator session lock and unchanged role preflights remain the
only database-run entry point. Worker preparation executed no database command.

Coordinator selection, from the existing lab root:

    --candidate-root candidate-accel-online-cf1-process-death-20261013 \
    --evidence evidence/d4-minimized-ipc-sa21-20261013 -- \
    -q tests/test_online_cf1_process_death.py --tb=short -ra

No D1/D3 or old 23-case CP65 rerun is requested merely to recount prior evidence.
The complete D4 manifest records all inherited files and new source hashes. The
standard wrapper records source/tests but not the imported D2 experiment decoder;
its unchanged hash is additionally pinned in D4's full manifest for a post-run
comparison. Corrected-source results are recorded at
`evidence/d4-minimized-ipc-sa21-20261013` and
`evidence/d4-minimized-ipc-sa20-20261013`. These tests directly use psycopg/CF1;
two SQLAlchemy dependency environments do not establish new ORM semantics or
installed-wheel qualification. No additional test is needed for this same finite
acknowledged-commit question.

## Review correction and preserved evidence

The first two successful coordinator gates used the D1 Claim object, which also
carried its unused public synthetic text value into the child. That value was not
required by frame installation. The review correction introduces a value-free
FrameCommitClaim packet and changes only the Process argument to use it. Claim
freshness, operation/pin checks, the live/tombstone bit and transaction SQL stay
unchanged. This is fixture data minimization, not a runtime/product defect.

The original four-file D4 overlay and both original run receipts are preserved
under the recovery checkpoint. The original results were 12 PASS in 7.34 seconds
(2.1.3) and 12 PASS in 6.38 seconds (2.0.51). The same twelve-case selector passed
again after the correction, with the final helper source hash recorded in each
receipt. No pre-change pass is counted as proof of the corrected source.

The publication plan uses ten files: the four-file final overlay, checkpoint,
exact D3-based recovery map, both corrected-run logs, the preserved original
helper and the pre-minimization checkpoint. The local four-file original overlay
also retains its original progress and manifest. Recovery starts with the exact
194-file D3 base and adds only the four D4 files. A separate local byte restore
verifies the complete 198-file final inventory; it does not run a database or
establish fresh-machine/cluster recovery.

## Precise missing claims

- No ambiguous COMMIT: both sides are deliberately distinguished by explicit
  acknowledgements. The window after a COMMIT request is sent but before its
  success acknowledgement is lost or observed is not exercised. No claim covers
  a network partition, server-side committed/client-unknown outcome or an
  idempotency/reconciliation protocol for that outcome.
- No provider recovery: the encryption/provider owner survives. This does not
  recover the volatile provider after restart, transport live prepared keys,
  validate a custody restore or change cross-process provider guards.
- No encryption-worker death during preparation/sealing, cache invalidation on
  process transfer, time-of-use expiry in that worker, or provider service outage.
- No PostgreSQL process/server crash, restart, WAL crash recovery, power loss,
  failover, fresh-cluster restore or deployment disaster proof.
- No product lifecycle/online closure/cutover admission, external authority,
  stale-process fencing, multi-worker range scheduling, equality indexes,
  production key custody, installed-artifact or new ORM qualification.

D-REV-04/09/07 owner decisions remain pending. The full final independent scan is
mandatory. These twelve prepared cases do not promote a runtime capability.
