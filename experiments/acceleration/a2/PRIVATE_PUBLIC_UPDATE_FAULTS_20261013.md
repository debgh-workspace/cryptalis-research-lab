# Private public UPDATE fault boundary: A2

Research-only correction in an isolated derivative of frozen A1. No protected-table bulk UPDATE is admitted. The feature stays private and off by default. All seven production gates remain UNKNOWN.

## Confirmed defect and correction

A real PostgreSQL int4 overflow (SQLSTATE 22003) through an admitted public UPDATE left native SQLAlchemy Session and transaction `is_active` flags true. The attached path instead converted that statement failure into failed-ORM-flush state. Four native differential cases demonstrated the difference: synchronous/asynchronous, each at the root transaction and a SAVEPOINT.

The correction imports SQLAlchemy DBAPIError and exempts it only inside the native statement-invocation catch. Native SQLAlchemy owns driver-error state and actual ORM autoflush failures. PostgreSQL still requires recovery from its aborted transaction or SAVEPOINT; an active Session flag is not permission to keep issuing SQL without rollback.

Provider preparation, authentication, cancellation and the outer asynchronous post-result cleanup remain unchanged. In particular, the outer result boundary does not exempt DBAPIError. The inner invocation has already marked its own failures handled; an exception after successful result production is a different boundary.

## Final executed controls

The final 20 cases pass on both SQLAlchemy 2.1.3 (8.15 s) and 2.0.51 (7.90 s), under the coordinator's unchanged two-role preflight and serialized existing PostgreSQL 16 lab:

- Four real 22003 errors: exact native transaction state before explicit rollback, outer-work scope and same-session recovery.
- Four real 23505 errors during pending protected/native INSERT autoflush: preserve failed-flush state and no unintended public UPDATE.
- Eight provider controls: cold unavailability or expired-lease renewal, sync/async and root/SAVEPOINT. Public Keyring construction and a key-module-only test clock are used; no private cache changes.
- Two real async task cancellations during preparation: native before_flush control versus awaited provider. Independent lock and connection-pool observations precede Session.close.
- Two explicitly synthetic post-native-result failures: a genuine Core UPDATE RETURNING completes through SQLAlchemy's actual `_ensure_sync_result`, then the test raises DBAPIError. Native committability and attached quarantine are independently observed. This is not a reproduced natural psycopg cursor failure.

Every case checks exact protected-table storage and recovery on the same Session. The existing 35 private DELETE controls passed in the earlier SA2.1 combined run against the final runtime bytes. Its three A2 harness failures are retained; this is not a claim that that combined run passed as a whole.

## Sensitivity and failed harnesses

The original A1 runtime failed all four overflow controls. Adding only an outer async DBAPIError exemption to the final candidate makes both synthetic post-result cases fail at the quarantine assertion (1.23 s). The exact unmodified final candidate passes those cases and both complete 20-case cells.

Initial cancellation injection inside a native cursor event invalidated the connection, which was a different boundary from provider preparation. Moving the native injection to before_flush preserved the expected outer transaction and lock oracle.

Initial cursor-finalization hooks did not affect the attached guarded cursor: the recorded wrapper and delegated raw cursor had different identities. A subsequent optional private cursor attribute probe correctly raised UnsupportedProtectedOperation. The final test neither bypasses nor unwraps the guard; it records permitted result/cursor types, context identity, successful native completion and synthetic injection reach. Every failed fixture and source version remains in the coordinator's immutable evidence snapshots.

## Exact artifacts

- Runtime `src/cryptalis/sqlalchemy.py`: ef764a712b60c6c33e694937ed23ce56f21b8374f081d276b0f076310a9d3b89
- Tests `tests/test_private_public_update_faults.py`: b02b835db801c7b0bc735323ea91e058ed8d2bc1e3408b39604ea1aa280281e6
- `A2_FAULT_VERIFICATION_RECEIPT.json`: source hashes, all nine coordinator cells, exact counts, per-module results and stable-source/server-stop checks.
- `A2_BASE_RECEIPT.json`: the 187-file frozen A1 derivation inventory.
- Separate outer-exemption mutant: candidate-accel-orm-faults-20261013-outer-exemption; only sqlalchemy.py differs, with hash f69b486d0d96429422bedb1c04731a1a30d5903e8aa5eb5efed6db19ee1d7719.

Full installed S17 integration is coordinator-owned and was still running at this checkpoint. This slice does not qualify broad bulk DML, production provider custody, independent security review or fresh-cluster recovery.
