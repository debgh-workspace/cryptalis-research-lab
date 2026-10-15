# Deferred trusted-local RED/GREEN plan

All proposed commands are NOT RUN. This packet grants no execution authority. The coordinator must review the exact command block before running it. Do not start any block while another session owns the lab or while the prior async correction lacks its required terminal audit.

## Frozen sources

- RED: `candidate-cleanup-transport-metadata-red-20261014`, exact inherited 217-file source plus one new focused test.
- GREEN: `candidate-cleanup-transport-metadata-20261014`, the same new test plus only the reducer correction.
- Both source trees are immutable across phases. There is no in-place replacement between RED and GREEN.
- `INHERITED_SOURCE_MANIFEST.json` is an unchanged copy of the parent candidate's full manifest. `INHERITED_SOURCE.sha256` is its original 217-file listing. `RED_SOURCE.sha256` and `GREEN_SOURCE.sha256` each cover 218 files.
- `BASELINE_keys.py`, `GREEN_keys.py` and `SOURCE_DELTA.patch` preserve the exact reducer change. `NEW_NODE_IDS.txt` enumerates all 17 planned nodes without importing or collecting them.

## Proposed sequence

Run exactly one block from `PROPOSED_COMMANDS.txt`, then stop for independent audit: RED SA2.1, RED SA2.0, GREEN SA2.1, GREEN SA2.0. Each block selects only the new focused test module, which has 17 statically planned cases. No full-suite or database-fixture test expansion is authorized by this packet.

The tests themselves use no database fixtures or SQL. However, the inherited conftest requires the real dual-role admission marker. Preserve the unchanged `scripts/test_postgres.py` runner and the exclusive-lock corpus-v2 wrapper. Do not bypass the check, inject an admission marker, run direct pytest, change credentials, or substitute a database. The wrapper starts/stops the existing PostgreSQL lab, runs preflights, establishes package origin, bounds the test process to 600 seconds, preserves exact source snapshots, and captures/restores the original corpus. A failed preflight stops the phase; no automatic retry is proposed.

Each phase uses a fresh evidence directory under `B/evidence`. Those directories are not created during preparation. Existing evidence must never be overwritten. The selected dependency-cell interpreter is explicit; this is source-candidate verification, not installed-wheel qualification.

## Expected RED and GREEN

Source reasoning predicts RED will fail 8 cases and pass 9. The failures are the three cleanup-downgrade cases, four private-attachment cases, and the unrelated-state case, all at literal restored `effects == "unknown"` checks. This is a prediction only. Any other failure, collection problem, origin mismatch, timeout, unexpected node inventory or missing terminal receipt requires diagnosis. Do not relabel it as intended RED.

GREEN is expected to pass all 17 cases, but that status remains NOT RUN. The code/retry/identity/class-effect checks and six type/value controls must still execute. Do not omit controls or weaken assertions to obtain a pass.

## Evidence required after each phase

1. Verify packet, wrapper/runner inputs, original mailbox and selected source manifest before and after the block. Match the actual 17 node IDs and parameter IDs to `NEW_NODE_IDS.txt`.
2. Verify selected interpreter/dependency cell, package origin, source-before/source-after identity, runner and wrapper exit status, readiness probes, pytest outcomes and the final server-stop result. Red failure is expected only at the stated assertions.
3. Independently audit restoration of the original corpus. Even this unit-only selection must not bypass the existing wrapper's custody protocol. Wrapper terminal exit alone does not prove every cleanup/restoration outcome.
4. Verify both source trees remain frozen and their new test copies remain identical. Record unrun checks as NOT RUN; absent observations remain UNKNOWN.
5. Stop and report an unexpected result. Do not change source, retry, repair a failed literal read-only command, terminate backends, rotate credentials, rebuild clusters or advance to the next phase without coordinator review.

## Optional later oracle sensitivity review

No source mutants are created or run here. A separately authorized immutable candidate could omit the effects assignment, omit the retryable assignment, or replace the whitelist with an arbitrary-state merge. The focused tests should fail in each case. For omitted retryability, the KeyUnavailable and CryptoBackendUnavailable controls require literal False despite their True class defaults. For a generic merge, notes/provider markers or the attached reduction sentinel must fail. Removal of exact-type/identity checks is covered by the string-subclass and integer-zero controls. Source-removal evidence is not a prerequisite claim already satisfied by this packet.

The independent auditor decides whether further full-source regression, existing real cleanup tests, packaging or installed qualification is needed. No claimed async integration result or production gate changes here. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE all remain UNKNOWN.
