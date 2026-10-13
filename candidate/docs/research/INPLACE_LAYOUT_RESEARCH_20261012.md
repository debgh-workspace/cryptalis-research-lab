# Prospective in-place layout research, 2026-10-12

## Scope and isolation
This is a separate storage-only prototype. Transition and reverse artifacts use distinct inplace-research-v0 markers. Reverse journal layout is99. It refuses existing searchable/indexed protected fields at plan construction, and refuses already-reordered legacy layouts. It is not a replacement for the99-test temporal candidate and does not reduce the product's searchable-encryption requirement. No commits, product promotion or deployment.

## Mechanism
Retain authenticated staging, full verification under writer exclusion, snapshot fencing, native role handover and exact ordinary-schema comparison. At forward cutover convert the original column to bytea USING verified staging, drop staging, and restore the CF1 frame check on the retained column. At reverse cutover convert the same column to its original text/VARCHAR type and collation USING verified plaintext staging. Public suffix columns are never dropped or reconstructed. Original visible ordinals and table identity remain.

## Evidence available at08:54 UTC
- DDL-only alternatives:2 PASS; naive forward drop/rename cannot recover original positional order by reverse in-place conversion alone. This preliminary fixture used non-cryptographic bytes.
- Integrated actual CF1 storage lifecycle:7 recovery/edit/abort cases PASS. Initial selection of7 searchable fixtures was refused by storage-only scope; no claim those passed. Early constructor guard was added so scope refusal precedes staging.
- Installed exact wheel on SQLAlchemy2.1.3:16 PASS, including provider outage, key expiry, and7 lost-commit-reply points. Cross-version repetition pending.
- FastAPI source unchanged:58 native tests PASS; protected mode58 call bodies PASS with1 protected bulk-delete teardown ERROR. Reverse plan now succeeds, then decrypt-back reaches PLAINTEXT_PENDING with36 values equal to independent decoder and exact source-schema comparison.
- Published plaintext state: fresh Python3.14.8 process proves Cryptalis package absent, checks all36 retained values before test reset, then all58 upstream tests and teardown PASS. Existing plaintext lab role required explicit Item grants as a separate operator step; this is not automatic manifest-only handover.
- First package-free rerun failed one fixed-email insert because protected teardown had left fixture rows. After exact pre-reset value verification, native teardown reset between test campaigns fixes this fixture issue. Initial decrypt-back observation also had a CursorResult-to-dict fixture error, corrected by explicit .all(); preserve both failed logs.

## Limits and next tests
Real-app metadata retirement and encrypted pg_dump restore are running, not yet verified in this note. Installed wheel SHA256 a7edcf6d8f87c7bb73543598935df27570a5312bb5874aefc9eb551da39d2f1d. No full suite, independent review, general legacy conversion or encrypted-search integration. Table rewrite costs, disk/WAL use and old-snapshot risks remain. PostgreSQL's established ALTER TABLE mechanism is not a novelty claim.

Source: https://www.postgresql.org/docs/16/sql-altertable.html . Changing column types commonly rewrites the table/indexes; the operation is not MVCC-safe for older snapshots. Keep existing snapshot fences. Prospective in-place preservation does not repair a column already moved by a legacy installation.


## 08:55 verified result

Real-app metadata retirement and encrypted pg_dump/psql restore now pass. All 58 native tests pass in a Cryptalis-free process both before and after removal. Retained encrypted backup restoration is checked before retirement, and an old encrypted restore after retirement fails the removed-state pin check. Both independent decrypt comparisons match all 36 saved rows. See inplace-real-fastapi-full-removal-20261012-0854 receipts. Extra explicit public Item grants and native test reset remain disclosed lab adaptations.
