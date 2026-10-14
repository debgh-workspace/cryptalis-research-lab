# Independent capture-wrapper v2 source review

Date: 2026-10-14 15:38 UTC. Reviewer: Agent1. Source-only review; no fixture tests, wrapper main, database operations, Git or network actions executed. No shared source edited.

## Decision

No blocking defect found in the bounded derivative or its 12 proposed filesystem-only controls. Root may decide whether to authorize that exact test file. This review does not itself authorize execution or a new database campaign. Use the pinned source revision and capture the selected helper origin/source hashes with the run receipt. Test success must not be relabelled whole-wrapper or database qualification.

## Pins and unchanged boundaries

All eight entries in candidate-corpus-wrapper-v2-20261014/source-manifest.json match the inspected bytes. STATIC_CHECKS.json records these checks and the 12 test names. The original wrapper hash remains 1138f48a9993c2dded9160e72698aa754c8ec591639bafcb26d35d66e88d5fdf; original role-preflight runner hash remains 118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12.

Static AST comparison confirms the entire run() function is identical, including subprocess arguments, timeout logic, redaction and inherited receipt behavior. Candidate preflight byte comparison, exclusive nonblocking flock, selected runner assignment, readiness preflight call, package-origin check, and test command are unchanged. The change does not weaken role admission or provide a runner bypass.

## Capture and recovery behavior

The snapshot now covers the original compatibility* family and the missed master-s4-compatibility* family, both restricted to corpus-v1-sa*.json. It runs after acquiring the existing lock and before PostgreSQL start. Originals are exclusively copied into prior-corpus with a digest manifest. A snapshot failure prevents starting PostgreSQL; partial backups do not alter shared originals.

On normal capture, new/changed outputs are exclusively archived and checked before their shared paths are removed/restored. Deleted originals are restored. Unchanged files are not relabelled as newly generated evidence. Restoration uses a temporary ordinary file and replacement, with an exact post-write byte check. Final success requires both every prior byte value and the complete original filename set.

Failure semantics are explicit rather than a promise to restore under all I/O failures:
- A failed archive leaves that changed/new source untouched, preserving unarchived output; independent files still receive restoration attempts.
- A failed restoration retains the pre-run backup and archived changed output, records an error and fails the wrapper.
- Enumeration/symlink or final-isolation-report failures cannot produce a successful capture result.
- Nested finally attempts capture even if PostgreSQL stop/reporting raises, and closes the lock even if capture raises.

The inherited treatment of a nonzero postgres-stop subprocess return is unchanged and explicitly excluded from new claims. This is not crash/power-loss atomicity, fsync durability, or protection against filesystem writers ignoring the shared lock.

## Test review

The 12 controls exercise both filename families, successful capture, simulated operation exception, new/deleted/unchanged files, injected archive failure with independent restoration, injected restore failure preserving both versions, snapshot failure, unrelated-file preservation, snapshot symlink refusal, and stop/restore exception cleanup ordering.

The two cleanup tests parse and execute only the wrapper's finalbody with injected names. They do not import run_baseline, call wrapper main, create credentials, run subprocesses, or access a database. They establish cleanup-block ordering only. Helper tests use disposable temporary directories. No malicious archive or external target execution is involved.

## Privacy and provenance limits

The new helper does not read environment, credentials, tests.json or package-origin.json; it only snapshots the two specified corpus filename families. It assumes these are cooperating test-producer artifacts and does not inspect/sanitize arbitrary file contents. The inherited run() still writes environment-bearing JSON; this derivative does not make those files safe for publication or recovery packaging.

Existing shared master-s4 observations remain unattributed. Capturing a current file or adding this correction cannot retroactively bind it to S20/S21/S22. Their historical provenance is being audited separately. Preserve original observations/failures and do not alter earlier receipts.
