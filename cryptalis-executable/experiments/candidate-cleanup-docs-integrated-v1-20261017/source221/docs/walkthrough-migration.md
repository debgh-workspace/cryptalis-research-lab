# Protect an existing text column

**IMPLEMENTED research prototype.** Production-provider and independent production-security qualification remain incomplete.
All seven gates remain UNKNOWN. Use the authorized disposable PostgreSQL 16 cell.

1. Keep the original application mapping as `Text`. Assign primary keys in the application.
2. Declare tenancy, protected fields, query leakage, writers, and searchable value domains.
3. Use owner maintenance and restricted runtime roles. Approve measured costs and pause.

Before the first `apply`, stop and drain known workers and exclude all alternate writers
with owner or DDL credentials. Follow the snapshot-holder prerequisite below as well.
A maintenance-approval record does not prove either prerequisite.

## Snapshot-holder drain before cutover

Alongside actual exclusion of every affected writer, arrange an authorized cutover window in which other account-bearing transactions holding snapshots in this database can finish or roll back. This includes read-only repeatable-read/serializable transactions, exported snapshots, server-side cursors and account-bearing background workers, even when they do not access protected tables. Idle connections without a snapshot need not be disconnected. The library checks this barrier at switch; a planning result or maintenance-approval record does not prove it. If `other_database_snapshots_active` occurs, keep writers stopped, preserve the original operation/artifact and staging, have the responsible operators finish or roll back the relevant transactions, inspect actual progress and current external authority, then resume the same operation only within approval. Do not bypass the guard, delete the journal, terminate sessions without separate authority, or blindly replay business writes.

This is a database-wide snapshot-holder condition, not a requirement to disconnect every open connection. The guard can refuse after earlier staging/backfill transactions have committed. Preserve actual progress; do not assume the operation had no effects. Existing source tests cover this boundary; no tests were rerun for this clarification. This does not establish near-zero-downtime migration or continuous quiescence.

## Plan and apply under the approved cutover window

```python
from cryptalis.migration import plan, apply, MaintenanceApproval
from cryptalis.sqlalchemy import attach

p = plan(manifest_bytes, Base.registry, owner_engine,
    writers=writer_inventory, search_reviews=domain_reviews,
    keys=tenant_keyrings, runtime_role=runtime_role, target_id=deployment_target_id,
    backfill_rows_per_second=measured_backfill_rate,
    verify_rows_per_second=measured_verify_rate,
    temporary_bytes_per_row=measured_storage_cost, wal_bytes_per_row=measured_wal_cost)
print(p)  # Estimated pause from native row count and the supplied measured rates.
approval = MaintenanceApproval(writer_exclusion_evidence, approved_pause_seconds)
options = dict(keys=tenant_keyrings, pin=prepared_pin, approval=approval)
apply(p, owner_engine, **options)  # Switch database; return PENDING.
```

`plan` changes no schema or data. It rejects incompatible keys, types, tenancy, and search domains.
Save `p.artifact` and the authenticated current pin outside restore; bind target, operation, digest, and phase. The host supplies pin provenance.
Keep the writer exclusion and the approved cutover window in force through publication and activation.
The journal is progress evidence. Never reconstruct current authority from a restored journal.

Expand installs bytea shadows, indexes, and durable per-table maintenance triggers. Tables in one schema share the operation guard function.
Admitted restricted-runtime writes during maintenance fail with SQLSTATE `55000`; roll back and resume only after inspection and matching deployment publication. The host must separately exclude owner/DDL-capable and unsupported writers; the maintenance trigger does not prove their exclusion.
Backfill commits each bounded chunk with its marker. Resume with the same artifact and current pin.
Committed chunks retain their ciphertext. Failed chunks leave neither rows nor markers partially changed.
Verification decrypts every value and checks source equality, types, NULLs, membership, generations, and schema.
Default apply verifies and switches in one transaction. A saved VERIFIED checkpoint is checked again on resume.
Explicit `verify` adds a pass. The pause estimate excludes extra passes, drain, DDL, index build, and publication delay.

Plain reads continue during verification; writes and locking reads wait. DDL can pause reads after its lock is granted.
Strong locks retry three 100 ms attempts with 50 ms gaps; exhaustion reports `table_lock_busy_retry`. Other lock waits retain the 5 s default.
The retained-native protection switch keeps the original column/type slot and clears its values according to the admitted nullability contract; authenticated CF1 remains in the bytea payload column. Original affected indexes/constraints are retired as recorded by the plan. The switch does not drop/rename the original column and does not keep a live plaintext rollback mirror.
**Plaintext-at-rest remains possible:** prior row versions, WAL, snapshots and backups can retain plaintext. Neither updates nor later `DROP COLUMN` operations establish erasure. Retain recovery dependencies until explicit finalization.
Bounded decrypt-back of current edited data and removal are implemented through `cryptalis.deprotection` for admitted profiles. Follow the [recovery/removal guide](https://github.com/debgh-workspace/cryptalis-research-lab/blob/d952c505a4666266019e32f27c77f93edd5151ca/preview/docs/source221-v4/RECOVERY.md) with distinct plaintext-role admission, separate reverse authority, explicit plaintext consent and actual package-free/backup evidence. Public workflow smoke, generic lost-metadata repair and independent fresh-host recovery remain unestablished.

Publish the exact artifact through the trusted host deployment tool while writers stay stopped.
Supply its `ACTIVATING` pin to `apply(..., until="ACTIVE")` to acknowledge publication and remove the fence.
Record the `ACTIVE` pin outside snapshots and restart fresh workers:

```python
sessions = attach(Base.registry, runtime_engine, lock=p.lock_bytes,
    keys=tenant_keyrings, deployment=(p, active_pin))
```

Startup rejects stale pins, schema mismatches, owner credentials, and unplanned tenant key policies.
`apply`, `verify` and `abort` require maintenance approval before connection or locks.
Read-only `plan`, `check_deployment` and supplied-connection `check_attachment` are exempt.
Before switch, `abort` restores native writes and retains the journal; it cannot undo cutover.
Run tests through `scripts/test_postgres.py`; it reloads both private files and probes both roles.
One operation per schema is admitted; later journal reuse is unfinished. [Evidence](status.md) records tests, costs, and limits.
