# Ordinary ORM optimistic versioning: A3 bounded evidence

**VERIFIED only in the named local cells.** No runtime correction was needed. All seven production gates remain UNKNOWN.

## Result

The test-only S17 derivative passed four native-differential cases on SQLAlchemy 2.1.3 (1.78 s) and the same four on 2.0.51 (1.47 s). Both runs used the coordinator's unchanged PostgreSQL 16 dual-role preflight. Each run stopped cleanly and retained matching source snapshots.

The eight-cell [corpus supplement](A3_OPTIMISTIC_VERSIONING_CORPUS_20261013.json) records exact source and test hashes. It does not relabel or requalify the inherited 554-cell historical corpus.

## Exact scenario

The original mapper has a non-null public `Integer` version column with SQLAlchemy's default version generator. One ordinary table has an application-assigned UUID record ID, UUID tenant ID, one storage-only protected `Text` field, and a public label. The mapper exists before schema creation, planning, migration, and attachment.

Each case creates independent native and attached schemas. Two Sessions load version 1 with `expire_on_commit=False`. The winner commits a protected-field edit at version 2. The stale Session then issues an ordinary ORM UPDATE or DELETE in a root transaction.

Both paths raise the exact native `StaleDataError`. They have equal failed-transaction and identity-map state. An independent owner connection confirms that the failed flush did not change the winner's physical storage. The existing independent CF1 decoder confirms its plaintext and context. Explicit rollback recovers the same stale Session: a fresh UPDATE commits version 3, or a fresh DELETE removes the row.

## Contract boundary

The ordinary ORM contract requires native behavior for admitted operations. Manifest mapper compilation has no integer-version exclusion, and native DELETE admission explicitly preserves the version bind. The separate private public-table bulk UPDATE helper refuses versioned mappings; that restriction remains unchanged.

This closes only the four deterministic schedules in this test. Generic version counters, server/custom generators, detached merge, nested transactions, locking schedules, multi-row races, and stress qualification remain untested here. The broader blueprint B-ORM-17 campaign remains open. Optimistic concurrency is not proof of freshness against a hostile database that replays old data and counters.

## Provenance and execution

- Candidate: `candidate-accel-orm-versioning-20261013`, derived from frozen S17 `candidate-accel-integrated-r2-20261013`.
- All 195 inherited files remain byte-identical; `A3_BASE_RECEIPT.json` holds their hashes.
- Test: `tests/test_sqlalchemy_optimistic_versioning.py`.
- Coordinator arguments: `tests/test_sqlalchemy_optimistic_versioning.py -q --tb=short`.
- Receipts: `a3-optimistic-versioning-sa21-20261013` and `a3-optimistic-versioning-sa20-20261013`.
- Test-only addition. No runtime source, bulk authority, credential, role, or cluster changes.
- The unchanged seven legacy-profile assertions remain full-suite failures. These focused passes do not make the current full suite green.
