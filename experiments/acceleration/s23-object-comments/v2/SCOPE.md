# S23 native object-comment round-trip oracle, v2

Status: SOURCE PREPARED; NOT IMPORTED, COLLECTED OR RUN.

V1 remains unchanged at `experiments/s23-object-comments-20261014`. V2 changes only the independent native observation: it directly resolves the table and named index OIDs, compares the constraint backing-index/table OIDs with those observations within each sample, and excludes those OIDs from cross-phase shape equality. No product or expected outcome changes.

## One question

Does unchanged S23 preserve native comments on its admitted protected-field indexes, UNIQUE constraints and constraint-backed indexes through protection, current-data reverse and removal?

The source review identifies missing inventory/restoration paths. Actual PostgreSQL loss remains **source-inferred** until this native oracle runs. This packet changes no product source, metadata contract, parser, admission policy, assertion from an older test, dependency, credential or role setup. It does not make object comments a newly qualified feature.

## Isolated inputs

- Frozen canonical input: `candidate-s23-planning-20261014`, 213 source files.
- Separate byte-identical execution copy: `candidate-s23-object-comments-oracle-20261014`, also 213 files. No test was added inside it and no runtime file differs.
- Packet test: `test_native_object_comments.py`.
- Packet `conftest.py` is copied byte-for-byte from canonical S23. Its fresh-wrapper attestation and database-error redaction remain unchanged.
- `BASELINE_S23_MANIFEST.json` is the prior 213-file S23 preparation manifest, copied unchanged. Its old preparation-status prose is historical; this packet uses its verified source hash inventory, not that status as a new result.
- `SOURCE_PREPARATION.json` pins the copy, canonical source, unchanged helpers, runner/preflight, wrapper and selected dependency metadata. `INPUTS.sha256` supports a file-only coordinator check before each run.

The test checks all isolated source hashes and exact runtime/helper import locations before creating a database fixture. The wrapper separately verifies runtime package origin and captures candidate/external test bytes before/after execution. Select the packet directory, not only its test file, so the unchanged packet conftest is included in the wrapper's external-source inventory.

## Fixed four-case matrix

Each case first runs an independent native application fixture, then a separate protected fixture with the same synthetic values. The native fixture receives only ordinary current-value DML after setup. No protect/deprotect/remove call runs in that native path.

1. `standalone_index`: a non-unique, tenant/field equality index with a synthetic comment.
2. `unique_constraint`: an immediate, non-deferrable tenant/field UNIQUE constraint with a synthetic comment; its backing index has no comment.
3. `constraint_backing_index`: the same UNIQUE shape, with a comment only on the backing index.
4. `absent_comments`: the same UNIQUE shape with both comments absent.

Comment content is public synthetic text containing an ASCII apostrophe, double quotes, Unicode and an emoji. COMMENT statements use fixed templates with psycopg `Identifier` and `Literal`. No hostile payload, security probe or real application value is involved.

For UNIQUE cases, the fixture converts its existing native unique index to a UNIQUE constraint with the same name and scope. These shapes are already admitted by the S23 compiler. The test obtains a **fresh public protection plan after this setup** and replaces its local test pin before applying. It does not edit a plan artifact or bypass native admission.

## Independent deciding observations

The oracle reads exact schema/table/index/constraint catalog identities, `obj_description`, native definitions, uniqueness, validity/readiness, immediate/distinct-NULL behavior and the constraint/backing-index relationship. It never calls product `_facts`, reverse `_model`, or the product schema comparator to construct expected results. Exact object OIDs need not survive deliberate drop/recreation.

The native path proves that ordinary DML preserves the initial object comments and definitions. In both paths, row 105 is updated through the actual ORM to the same current synthetic value. The protected path uses ordinary attachment and current-row decryption before reverse. All seven current native rows must match after reverse, including NULL and Unicode values.

The lifecycle path compares comments, object shape and current values at PLAINTEXT_PENDING. A mismatch fails immediately and product removal is NOT_REACHED. The owned synthetic schema still receives normal fixture teardown; this is not an in-database forensic-retention experiment.

Only a successful pending-state comparison proceeds through the existing plaintext cutover/removal helper and repeats the native observations at REMOVED. The original helper uses the **already provisioned** distinct plaintext role and existing reviewed test-administrator procedure, with `create_role=False`; it does not create roles or credentials. Its existing workload/backup attestation strings are fixture-level state-machine inputs. This new test does not qualify a real package-free application, encrypted-backup recovery or provider custody. Do not execute if that existing cutover authorization or resource is unavailable.

## Fixed evaluation budget and disposition

- Four tests on SQLAlchemy 2.1.3 and four on 2.0.51, serially through the existing lab lock and unchanged fresh owner/runtime preflights.
- One run per version after independent static review; do not repeat an unchanged failure to obtain a different outcome.
- Baseline prediction only: three comment-preservation failures, one uncommented passing control. Any fixture-admission, native-control, data-value, definition or cleanup failure must be reported separately; it does not confirm comment loss.
- No skips, xfails, automatic expected-failure conversion, or accepted refusal substitutes are present.
- Existing seven legacy deprotection assertion failures remain untouched. This focused run is not a full-suite run and cannot erase those failures.
- A failed preflight, wrong package/source pin, wrong dependency version or unexplained native-control failure stops dependent work. Do not substitute a database, repair credentials or broaden permissions.
- After actual results, KEEP only the useful oracle/evidence. Product correction requires a separate reviewed derivative. All qualification gates remain UNKNOWN.

## Safe case receipts

The existing wrapper sets `CRYPTALIS_LAB_PROGRESS`. Each attempted case appends one record to that run's `object-comment-outcomes.jsonl`. The record has the static case ID/version, path completion, observation stages and booleans, removal state and classification. It contains no connection strings, SQL, exception messages, key material or data values. Successful fixture teardown is required before marking a path complete; both paths are required for IDENTICAL. A missing receipt after interruption is incomplete evidence. Reconcile all four IDs with JUnit and progress outcomes. This packet does not rewrite historical receipts or the compatibility corpus.

## Authorization and exclusions

Authorized here: source/test preparation and static validation only. No project import, pytest collection, test, database connection, new cluster, new credential, publication or product modification has occurred. `PROPOSED_COMMANDS.md` is for the coordinator after review; it is not an execution receipt. Existing active rotation/private-hook decisions remain pending and unrelated.
