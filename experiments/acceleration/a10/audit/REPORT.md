# A10 independent static audit

## Conclusion

No blocking oracle defect found for the narrow expired integer-version ORM slice. The reviewed test and safe receipts support eight native/attached paired cases per cell: sync/async × UPDATE/DELETE × version-only/whole-row expiry. SA21 reports 8 passed in 2.85 seconds; SA20 reports 8 passed in 2.78 seconds. Both JUnit records have zero skipped, failed or errored cases and the expected eight unique parameter combinations.

This audit did not execute tests or independently attest installed package versions. SA21/SA20 are the provided cell labels. Package-origin and tests.json records were deliberately not read.

## Oracle inspection

- Each parameter case executes both native and attached branches in separate randomly named schemas, with a newly mapped application each time. Only the attached branch runs migration and publication. The final assertion compares full collected public-state tuples and final values across both branches.
- The session loads version 1, calls public Session.expire on version_id or the full row, and asserts version_id is expired using inspect without accessing that attribute. No explicit refresh or get intervenes before mutation and flush. DELETE may itself cause a native reload; the claim is public API behavior, not the exact internal reload instruction or timing.
- Both attempts flush. UPDATE requires version 2; DELETE requires the instance deleted state. The first attempt rolls back, records state, verifies the committed snapshot, explicitly refreshes the same object and checks its original name, label, version 1 and persistent state. The second attempt repeats explicit expiry and then commits. A fresh Session independently reads final values or absence.
- Owner-engine snapshots are outside the ORM Sessions. Before commit and after rollback they must exactly equal the baseline tuple, including raw ciphertext bytes for attached storage. Attached snapshots also require the retained name slot to be NULL and independently decode the CF1 frame. The decoder uses a separate HKDF/HMAC/framing path, with the same qualified AEAD primitive and public fixture key provider; it is not an independent cryptographic implementation qualification.
- Sync and async factories are genuinely different. The async factory uses AsyncConnection/create_async_engine and async_sessionmaker or awaited attach. maybe awaits awaitables. Explicit get/delete/flush/rollback/refresh/commit/close calls are awaited where appropriate; expire and inspect are synchronous public APIs. Direct attribute assertions occur after awaited loading/flush/refresh with expire_on_commit=False. This checks async API parity, not event-loop responsiveness: the owner storage check intentionally uses synchronous I/O inside the coroutine.
- No skip, xfail, exception swallowing, early success return, weakened conditional assertion, or native-only exclusion exists in the new test. Its final comparison is unconditional. The reviewed conftest redacts database diagnostic text without changing failure status. The recorded selectors select the whole test file, with no -k/-m or deselection filters. All expected JUnit cases executed successfully.

## Provenance checks

- All 208 inherited candidate files match A10_BASE_RECEIPT hashes. This is verification against the inherited manifest, not a fresh read of the separate base tree.
- All three frozen new-file hashes match A10_FREEZE.
- Each runner receipt has 147 source/test/script hashes; every current candidate hash matches.
- Each source-stability receipt has equal before/after maps of 148 entries; every after hash matches the current candidate.
- Source-root receipts identify this isolated candidate; candidate isolation reports no archived files and primary receipts restored. External-source stability has empty before/after maps, so it proves no independent external-tree coverage.
- The provided execution receipts retain all seven production gates as UNKNOWN. See verification.json for the machine-readable checks and receipt hashes.

## Limits

No concurrent writer is introduced after expiry. The slice cannot prove stale-version conflict behavior against a winner, arbitrary version generators, server-managed versions, implicit async lazy attribute I/O, every transaction schedule, or general ORM compatibility. Whole-row expiry is invoked directly but the test explicitly checks only that version_id is expired; public-state equality compares the resulting full expired-attribute lists. The refresh point checks values/persistent state rather than collecting another full public-state tuple. These are bounded coverage limits, not blockers to the stated parity result.

The audit is static plus standard-library data inspection only. No native/test modules were imported, no PostgreSQL or Git commands ran, and no environment files, tests.json, or package-origin.json were read. Candidate source and existing evidence were not modified. Only this audit directory was created.
