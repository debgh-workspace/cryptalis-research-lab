# Accepted independent terminal audit: doctor-remedy source RED

Date: 2026-10-15 UTC

## Verdict

**ACCEPTED as the intended source regression RED.** The real-dependency run produced exactly two missing-remedy text-output assertion failures and four passing controls, with no errors or skips. All six actual CLI outputs, identity/restoration checks and stopped-database receipts satisfy the reviewed terminal gates.

This accepts only baseline source RED. It supports preparation of a separately reviewed, freshly bound GREEN stage; it does not select or execute GREEN, package new artifacts, qualify an installed successor or change any production-gate status. The three earlier stubbed proof attempts remain HOLD, and the V1 coordinator size-cap failure remains a separate failed startup.

## Selected route and immutable identities

- Capture: `persistence-recovery-20261013/doctor-real-red-v2-root`.
- Wrapper evidence: `cryptalis-executable/evidence/doctor-remedy-real-source-red-sa21-v1-20261015`.
- Exact V2 helper: `2f03c34a9565365dd3e6efda216dbb491f4688d595567c9d8a2859e13b1359d3`.
- V2 source review: `cdb1023ca73c60a5eed2e4e77e90d65019ab3504f9023a0b998f95434a9e8014`.
- Selected RED binding: `2a26848e44f0986ff0fd5ba34c5fc5e56b4b839fab23b4ee7332103773e02705`.
- Complete new union receipt: `07d7721242822e5d3663542b3d2dcfb1017d3922df0ca6d14c0e8056e7b400b0`.
- Fresh before-guard receipt: `c22a42909ef5c7a477fbad4c3d7d17d4b68982ca4129415d135a5a850b6ed155`.
- Baseline source manifest: `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`.
- External regression test: `adc17effc9821befc46ba79c76f5923d86c542579ac7995520cf3d041b64a9fe`.

The actual `entry-argv.json` exactly matches `BOOTSTRAP_ROUTE.json`. It selects the pinned host isolated/no-site cold launcher with the separate absent prefix, baseline source candidate221, admitted SA21 child interpreter and precisely the six reviewed source nodes. There is no installed-process node, `--installed-candidate` or `-x`; xunit1, no pytest cache and the external-test confcutdir are retained. Selection and binding hashes match their actual bytes and referenced admission receipts. The prepared repository-venv shell entry was not selected.

## Actual failures and all six output captures

JUnit reports six tests, two failures, zero errors and zero skips. Both failures are specifically `test_rejected_text_has_safe_remedy`, parameterized as `malformed` and `unsupported-schema`, at the intended line 114 assertion `output == REJECTED_TEXT`. The safe test log reports `2 failed, 4 passed in 0.72s`. It contains no unexpected collector/import/preflight error. Wrapper and test exit are 1; no failure was converted to a skip or xfail.

Progress independently records six starts and 18 reports: all six setup and all six teardown phases pass; the call phase has exactly the two intended failures and four passes. Reaching the decisive output assertions also confirms the positive collector controls and earlier input-preservation/redaction assertions passed.

`ACTUAL_OUTPUTS.json` is a lossless extraction of the six actual JUnit properties. Independent explicit text/JSON comparisons, rather than only the pytest summary, establish:

- Both rejected-text outputs equal the complete prior baseline text, with CLI exit 2 and exactly the expected constant remedy line absent. No other text difference is present.
- Both rejected-JSON outputs exactly equal the canonical rejection report, including the existing constant remedy, all seven NOT_INSPECTED checks and unchanged advisory/qualification limits. CLI exit is 2.
- Valid text exactly equals its unchanged oracle with no remedy and CLI exit 3.
- Valid JSON exactly equals its canonical grammar-only report with one model, the correct declaration digest, unchanged limits and CLI exit 3.
- All six stderr values are empty. No private input marker, collector marker or filename appears in any actual CLI output.
- All six before/after synthetic-input hashes agree. The fixture bytes were independently reconstructed from the pinned source and hashed: malformed `1074a01ae26372d67c0f47188f908e2107618fe81e819f17926d8b8a940ed365`, unsupported schema `2b5743c0d1d92149850c4884ff3defc7e607a73829f0ca524e173b115cc57b4f`, valid `09ab01bcfd546d42f5eba2bdedf8e7a9e6307de21389fadd42381e803aa4b492`.

## Identity and source preservation

Both unchanged main43 guard runs exit 0 and report VERIFIED with exactly 3,025 target rows. Their complete target maps and packet maps compare equal. The root's source-before and source-after maps each match all 221 baseline manifest paths and hashes. The completed helper's exact candidate/packet namespace assertions reject extra files, directories, conftests or bytecode.

The new map has 3,266 rows and equals the exact union of the preserved 3,025-row map and the 242 separately admitted source/packet/helper/review/receipt rows, with one overlapping row of identical digest. No original row is replaced. The 15 packet rows include all 13 sealed members, the seal itself and its separately pinned inert listing. All 13 sealed member hashes were independently rechecked, and their after-map entries match. The selected binding is additive and checked separately.

The unchanged wrapper additionally records 160 source-snapshot rows unchanged and the external test's exact before/after identity unchanged. This partial wrapper snapshot is not substituted for the coordinator's complete source221 map. Safe package-origin output names the exact baseline candidate's `src/cryptalis/__init__.py`, with the expected source directory and verified flag.

## Corpus and lifecycle closure

- Before and after independent status commands both return 3 and say `pg_ctl: no server running`.
- Safe wrapper output records start 0, readiness 0, source origin 0, tests 1, then explicit `postgres-stop exit 0` and `server stopped`. Wrapper stderr is empty.
- Binding-after is independently recorded as 0; the selected binding digest remains unchanged.
- Bootstrap, guard and wrapper bytecode-prefix paths remain absent by terminal metadata inspection.
- All five complete 26-row corpus maps agree: coordinator before/after, guard before/after and wrapper prior-corpus manifest. No corpus payload was read by this reviewer.
- Corpus isolation reports `primary_receipts_restored: true`, no errors, no archived generated corpus files and no deletions during this run.

Every acceptance-relevant RESULT field is supported by underlying safe captures/maps, not accepted merely because its summary boolean is true. The result's original PENDING_INDEPENDENT_REVIEW label is preserved; this separate sealed review supplies the acceptance.

## Evidence and limits

`REVIEWED_EVIDENCE.sha256` seals the exact safe terminal inputs used. `ANCHORS.sha256`, `MAP_COMPARISON.json`, `PACKET_COMPARISON.json`, `OUTPUT_COMPARISON.json`, `PHASE_COMPARISON.json` and `INDEPENDENT_FIXTURE_HASHES.txt` retain the independent calculations; `DERIVED.sha256` seals those derived records. Actual captures were never rewritten.

One read-only comparison launch initially failed because the exec-server transport disconnected before process creation; the same receipt-only command subsequently completed. It did not rerun the product or touch database state.

The audit began only after root reported terminal. It read safe captures, source, manifests and recorded identity maps, used data-only text/JSON comparisons and hashes, and inspected the three absent prefix paths. It did not run product code, imports, tests, helpers, database/status commands or Git, and did not inspect live installed payloads, corpus/cache payloads, credentials, existing environment values or raw environment-bearing phase JSON. This is narrow regression and file-identity evidence, not universal imported-code provenance or a new deployment/native/output-failure qualification.
