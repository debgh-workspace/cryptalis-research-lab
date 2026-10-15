# Identity V3 independent terminal acceptance

2026-10-15. Immutable safe-evidence review only; reviewer performed no DB/status/test/import/key/network/install/Git action.

## Verdict

**ACCEPT one finite identity capture and its closed boundary.** The safe identity receipt may now be pinned as the observed backend/owner/runtime identity for later independently admitted work. This is not authority to run smoke, create a fixture/key, change permissions or activate plaintext. The earlier failed V2 run remains a failure with no accepted identity.

Evidence: `evidence/preview-identity-capture-v3-sa21-20261015`.
Coordinator capture: `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/preview-identity-capture-v3-sa21-coordinator`.

## Exact outcome and closure

- Exactly one case: `test_identity_capture.py::test_capture_existing_lab_identity`.
- Progress: setup PASS, call PASS, teardown PASS. JUnit: 1 test, 0 failures/errors/skips, 0.386s. Safe pytest summary: 1 passed in0.39s.
- Safe wrapper records postgres-start0, readiness0, package-origin0, tests0, postgres-stop0. Wrapper exit0 at13:28:50.756100UTC.
- Completed postgres-stop.log says server stopped; independent post-status3 at13:28:50.926992UTC says no server running. Its argv names the exact existing toolchain pg_ctl and runtime/data directory.
- Before/after2,420-pin receipts are byte-identical; mismatch array empty. Interpreter-link receipts are byte-identical. Before/after26-corpus maps are byte-identical. Supervisor corpus-isolation receipt reports no archived changes and restored=true.
- Candidate source and selected capture source stability both unchanged=true. Boundary errors empty and independently_stopped=true.

The early closure was sent to root before the detailed identity audit, permitting root to select an independently admitted next DB task after its no-overlap check. This report observes the completed run's closure, not a promise that the lab remains idle afterward.

## Strict diagnostic acceptance

All four expected safe diagnostic files exist, one for each owner/runtime × Python/psql route. Values are booleans only. Each reports true for all strict checks: normalized127.0.0.1, exact IPv4/full mask, port55432, configured database/current/session user and numeric-string database OID. Both psql files additionally report subprocess_succeeded=true and same_exact_python_observation=true.

All four report old_literal_address_match=false, old_text_is_exact_host_with_mask=true and old_literal_format_only_difference=true. These support the formatting-only difference for THIS successful observation under all strict checks. They do not reveal or retroactively validate the failed V2 run's suppressed actual values.

The pinned V3 test writes its success receipt only after both role/backend database identities agree. Its source and imported V4 guard/proposal were included in the unchanged full input boundary. Neither DDL/grants/keys/smoke/cutover nor the adapter's security-boundary mutation paths were invoked by this one read-only identity test.

## Accepted non-secret identity receipt

Path: `evidence/preview-identity-capture-v3-sa21-20261015/safe-identity.json`.
SHA256: `089bac088003d7921f755409509afed5544741ebfee8af66faea0776fbfbb92c`.

Exact six leaf fields:

- address: `127.0.0.1`
- port: `55432` (JSON integer)
- database: `cryptalis_lab`
- database_oid: `16388` (JSON string)
- roles.owner: `cryptalis_owner`
- roles.runtime: `cryptalis_runtime`

No extra fields, URL/password/options/environment or credential material appear in this receipt. The actual configured private URL strings were not read by this reviewer. Provenance is the admitted unchanged dual-role runner, exact fixed-ENV launcher and existing supervisor/runtime-data route, corroborated by safe observed Python/psql identity checks and source/input/closure receipts. It is not a universal server attestation against a hostile administrator or a newly provisioned-backend claim. Future use must retain exact receipt bytes/hash and revalidate actual routes under its separately admitted guard.

## Invocation provenance

Actual spawn argv matches the accepted V3 concrete command: existing coordinator interpreter, existing SA21 dependency interpreter, current221 source overlay, explicit current221 pyproject, only identity-captureV3 directory, finite -q/--tb=short/-x and fresh V3 destinations. No --installed-candidate or smoke driver is present. Safe source-root/package-origin records identify candidate-cluster-retained-integrated-v2-20261015 source. This is backend identity evidence only, not installed-product or app acceptance.

## Safe hashes

- boundary-summary.json: `6afb6321e446cee306d0cde3cb20e69a8470b95fd848e478c126e5f0181fead2`
- owner-python and runtime-python diagnostic bytes each: `9ec1190edd3da4e88d59a5a0df14e2fa1b1c2328c0089043b7902c3d8b7eb6fb`
- owner-psql and runtime-psql diagnostic bytes each: `95c0d222f5d3e65a08d579d7f18f93a549f0193b6a6ec31532f07a6b7dee72a5`

## Remaining boundaries

Later smoke needs its own current candidate/runtime/command/authority admission, pinned identity and actual route/schema/permission checks. This observation does not supply plaintext-role/admin identity approval, authorize DDL or key creation, qualify fresh-process recovery, or change any product/release gate. No production or full-application claim follows.

Metadata preceded safe reads. No raw tests/readiness/package-origin/postgres-start/postgres-stop JSON, credential/environment files, cache bodies or key/policy data were read, hashed, copied or archived. Only this additive report was written. Prior failures and all execution evidence remain unchanged.
