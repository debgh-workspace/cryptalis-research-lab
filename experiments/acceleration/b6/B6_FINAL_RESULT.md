# B6 final bounded result

VERIFIED on the frozen test-only S18 derivative:

- SQLAlchemy 2.1 cell: 18 PASS in 7.63 seconds.
- SQLAlchemy 2.0 cell: 18 PASS in 8.04 seconds.
- Each gate contains 12 new warmed-attachment cases and 6 unchanged lifecycle controls.
- Source imports resolve to the intended isolated candidate. Both unchanged
  dual-role preflights pass, source fingerprints remain stable, and both
  recorded PostgreSQL shutdowns complete successfully.
- All 201 inherited files and 39 runtime modules still match S18 provenance.

Test SHA-256: `7aa02c574306951bfec0932699d1fd27fdd31efe702754cf144b04ae0120a30f`.
Safe combined receipt SHA-256: `8a38e1a1382383248700500d50153bf9f00870250f3235978441a1788fbedba0`.

## Evidence meaning

The test proves that queued ordinary ORM writes issue no SQL before the pause,
then one real DML reaches PostgreSQL and receives `55000`. Native snapshots
preserve catalog facts, all table values, and operation journal rows across
failure and explicit rollback. After legitimate pre-switch abort, the same
attachment performs the identical write successfully. Independent CF1 decoding
verifies complete membership/values; unrelated ciphertext bytes stay unchanged.

The imported catalog observer compares **trigger definitions and enabled flags**.
It does not compare `pg_proc` guard-function body bytes. This narrows the earlier
scope document's phrase “guard definitions” to the facts actually observed.
E's internal read-only review found no blocking oracle issue; this is not
independent human security review.

The frozen scope/progress documents record preparation-time PENDING status.
This final note and the exact receipts supersede that status only for this
18-case gate. These are source-path runs, not installed-wheel or complete-suite
runs. The seven historical legacy-profile failures remain preserved. All seven
production gates remain UNKNOWN.

## Integration and recovery

Coordinator may add the exact new test to its next separately qualified
S18-plus-F4 candidate. No runtime, active policy, artifact format, credential,
role, or cluster change is part of B6. No test was rerun during receipt review.

The publication plan has five files. It is an evidence/test overlay, not a
standalone recovery archive. Restore all 201 S18 base files using the hashes in
B6_PROVENANCE.json before adding the new test. Its helpers, including the
independent catalog and CF1 oracles, remain supplied by that complete base.

The active-rotation blocker remains: select and evidence the existing trusted
host procedure for terminating inventoried old workers and preventing their
old workload credentials from regaining write access across publication and
restart. This maintenance guard evidence does not make that decision or
establish post-publication stale-worker exclusion. Old backup-reader obligations
and action-time permission requirements remain unchanged.
