# Independent GREEN native and reservation review, r2 v1

2026-10-14. Static source/data-only review. No project imports, collection, tests, database actions, Git, product edits, or test edits. Only this versioned review directory is owned by the reviewer.

## Decision

READY for the coordinator to decide whether to execute the exact pinned eight-case packet in the two serial dependency cells. No blocking oracle or command defect found. This is source readiness, not observed GREEN, release readiness, full compatibility, crash durability, or qualification of any gate. Other independent source/envelope/identity reviews remain required by the coordinator.

The requested prior directory `reviewer-notes/s23-comments-green-independent-20261014` was absent at review start. Its reported v1 blocker was supplied by the parent: the actual-default test could pass even if the product omitted reservation computation. No prior review bytes were invented or replaced.

## Early-refusal discriminator

The eighth test constructs a non-null, storage-only field with no original index/constraint to offset added default metadata. It wraps only `check_schema_budget` to calibrate the in-process cap. It independently encodes the observed raw schema and a deep-copy reserve; it does not call the product reservation helper. Its asserted inequality is raw_size < cap < reserved_size. The original product check is then called with expanded=True.

If the product omits `schema_reservation`, the raw facts fit the cap and `_expand` returns EXPANDED. The required TransitionFailure is absent and the test fails. If the product omits the boundary call entirely, the same expected exception fails (and the visit count cannot be one). A different error cannot satisfy the exact `object_comments_schema_budget_exceeded` code. The test therefore closes the supplied v1 omission gap by inspection. No mutation run is claimed.

The reached-guard count must be one, provider unwrap count zero, native values unchanged, and independent SQL must find no journal, payload columns or defaults. Fault scope ends before the same original plan/pin completes protection, publication, reverse and removal. `_expand` places the check after expanded facts are observed and before the journal INSERT; apply wraps that expansion in the existing transaction. This is a deterministic smaller-cap guard test, not a 4 MiB load or arbitrary schema upper-bound proof.

## Eight cases

- Four native catalog cases retain the v2 assertions unchanged: standalone index, UNIQUE constraint, constraint backing index, and explicit absent comments. Against preserved v2, only the source path, source manifest, internal planner flag and docstring differ. Each has untouched-native and lifecycle paths, quoted/non-ASCII comments, independently sampled catalog shape and constraint/index OID linkage, current-value edits, pending checks and full removal checks. Recreation OID equality is not incorrectly required.
- Partial COMMENT failure injects before the second COMMENT after the first succeeds, requires exact CONSTRAINT/INDEX sequence, compares row/column/journal snapshot and object absence against BACKFILLED, then resumes the exact reverse operation. Pending retry must issue no observed CREATE INDEX, COMMENT or ALTER TABLE. Native values/comments/shape are checked before and after removal. It does not claim lost-COMMIT-reply or process-crash coverage.
- Actual non-null default-dependency case independently encodes the reservation, checks pending and active actual sizes, observes pg_attrdef/default through native SQL, and completes reverse/removal with values preserved. Alone this is not an omission discriminator; it complements the eighth case.
- Tiny budget fault requires exact failure, no unwrap, unchanged comments/shape/values, absent journal/payload, then same-operation PENDING after restoring the cap. It does not claim full removal in this case.
- Eighth calibrated early-refusal case has the discriminator described above.

## Provenance and command readiness

All 214 source hashes match. All 911 INPUTS.sha256 entries match by independent file-only hashlib comparison. Packet conftest equals candidate tests/conftest.py byte-for-byte; candidate scripts/test_postgres.py equals repository runner byte-for-byte. AST reading identifies four parameterized native cases plus four transactional/default tests, matching all eight PLANNED_CELLS IDs. No collection was run. Both proposed evidence directories were absent.

Agent3 corrected stale source-preparation metadata during review; final frozen SOURCE_PREPARATION names r2, eight cases and exact current test/source hashes. Commands select the r2 candidate, explicit pyproject and only the eight-case packet, through the existing wrapper and existing two interpreters. The wrapper preserves lock, preflight, candidate-origin and corpus-capture boundaries. No direct pytest or alternate database command is approved here. Only the coordinator may execute, and only under its existing authorization.

Run file-only pin verification immediately before EACH cell; stop on mismatch. Run the SQLAlchemy 2.1.3 command first. Inspect terminal outcome, exact eight IDs, case outcomes, JUnit, source stability, corpus restoration and server shutdown before deciding the 2.0.51 cell. Preserve failures; no automatic new evidence directory/retry. The exact commands are copied below for review, not executed.

# Coordinator commands: NOT EXECUTED

Run only after independent source review. The coordinator has confirmed that the existing synthetic plaintext-role cutover remains authorized; preparation did not execute it. These commands reuse the existing provisioned database; they do not create a cluster or credential. Do not run the two cells concurrently.

Working directory: `/workspace/scratch/cb28ee9f5f4a`.

## File-only pin check before each cell

```sh
cd /workspace/scratch/cb28ee9f5f4a
sha256sum --check cryptalis-executable/experiments/s23-object-comments-green-r2-20261014/INPUTS.sha256
```

Stop on any mismatch. This command reads files only; it does not import project code or open the database.

## SQLAlchemy 2.1.3: exactly eight tests

```sh
cd /workspace/scratch/cb28ee9f5f4a
cryptalis-executable/repo/.venv/bin/python cryptalis-executable/candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py --candidate-root cryptalis-executable/candidate-s23-object-comments-correction-r2-20261014 --python cryptalis-executable/release-lab/wheel-venv/bin/python --evidence cryptalis-executable/evidence/s23-object-comments-green-r2-sa21-20261014 -- -q -c /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-s23-object-comments-correction-r2-20261014/pyproject.toml /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/s23-object-comments-green-r2-20261014 --tb=short -ra
```

Inspect terminal status, eight exact case IDs, the native-path observations, case receipts, JUnit, source/external-source stability, corpus capture/restoration and database shutdown before deciding whether the second cell remains useful. The historical RED failures remain preserved. No GREEN result is yet observed. A preflight failure or unrelated failure is not permission to continue or substitute a resource.

## SQLAlchemy 2.0.51: exactly eight tests, separate command

```sh
cd /workspace/scratch/cb28ee9f5f4a
cryptalis-executable/repo/.venv/bin/python cryptalis-executable/candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py --candidate-root cryptalis-executable/candidate-s23-object-comments-correction-r2-20261014 --python cryptalis-executable/release-lab/s20-payload-preparation-sa20-20261014/bin/python --evidence cryptalis-executable/evidence/s23-object-comments-green-r2-sa20-20261014 -- -q -c /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-s23-object-comments-correction-r2-20261014/pyproject.toml /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/s23-object-comments-green-r2-20261014 --tb=short -ra
```

Each wrapper invocation acquires the unchanged lab lock, starts the already provisioned server, invokes the byte-identical `scripts/test_postgres.py --preflight-only`, verifies runtime package origin, then invokes that same runner again for pytest. The runner reloads both private URL files and probes both roles on each invocation. The packet conftest requires its in-process attestation. No direct pytest, inherited-credential admission, altered preflight, alternate database, new role or concurrent run is permitted.

The proposed evidence directories must not already exist; the wrapper refuses reuse. Preserve any failed receipts. Do not automatically rerun under a new directory without identifying why another run is justified. The selected interpreter metadata is pinned, but this is not a complete dependency-archive or independent-host qualification.

## Reviewed packet hashes

- `INPUTS.sha256`: `3139aa00e119c999c9b027695cd0c2d089d154ff721b73e38ef4326d832a9b52`
- `CANDIDATE_SOURCE_MANIFEST.json`: `f60c533cd016eee96c2045ddd3efe95633aaf07b2df5761bc2b6bcd695c32741`
- `SOURCE_PREPARATION.json`: `88a630c06cad96d7ecdd96d1087c64c38ce3df94356f73328eb755b33634db9a`
- `PROPOSED_COMMANDS.md`: `e8854547af9db3a4ebde8dcaef8c1565e19adbf3105ee90da49834ae6aa8d033`
- `PLANNED_CELLS.json`: `4d247437c65c221f0c68e67935809d26f6cf5c3ad4712ecd65cabd025c40bb28`
- `SCOPE.md`: `f14392f377ed507d6f989d7c51203461141403a6b7c33710c49d7163e71021fb`
- `conftest.py`: `fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd`
- `test_native_object_comments.py`: `75504f568b92f88042f7916b4c50ca070debe1b2e4342a968d6ca093c172ed51`
- `test_object_comment_transactions.py`: `aac551c552ca2a1a9d1d406500e1d65f8c11a5b24cbaa41c33606e27486b943b`
