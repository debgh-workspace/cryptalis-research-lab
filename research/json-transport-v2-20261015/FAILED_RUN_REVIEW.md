# Native JSON transport V2 SA21 failed-run terminal review

Verdict: ACCEPT_SCOPED_JSON_TRANSPORT_NATIVE_V2_SA21_FAILED_RUN_CLOSURE.

The exact V2 run failed its declared 61-case goal. Its completed 52-case transport/loader/mutation prefix and its stopped, restored terminal boundary are independently verified. This verdict accepts the accounting and closure of a failed run, not a complete probe PASS. No cost observation, performance conclusion, product admission, repeat run or next database stage is authorized by it.

## First failed gate and retained outcome

The first cost case, ::test_counterbalanced_native_cost[rows1-bytes0], failed at test_native_transport.py:319 during cursor.execute with psycopg.errors.AmbiguousColumn: ORDER BY "i" is ambiguous. The pinned source's first variant is native. It projects both i and i::bigint under the same output name i, then uses unqualified ORDER BY i. This is a cost-harness SQL name-resolution defect, not a failed JSON-versus-JSONB equality comparison. The accepted source review did not catch this defect; its original bytes remain preserved.

Actual ordered outcome:

- 48 loader/transport cases PASS.
- Four observed-comparator negative cases PASS.
- First cost case FAIL during its first native warmup execute.
- Remaining eight cost cases UNRUN because the frozen command uses -x.
- Exactly 53 start events and 159 setup/call/teardown reports: 158 passing phases and one failed call phase. Setup and teardown of the failed case passed.
- JUnit has the same exact ordered 53 identities, 52 passing cases, one failure, zero errors and zero skips. The runner records passed=52, failed=1 and exit_code=1.
- All 61 required outcomes / 183 passing phases were not achieved. The eight unrun cases are not skips or passes.
- cost-observations.jsonl is absent. Zero warmups and zero measurements were recorded; the planned 324 warmups plus 1,296 measurements cannot be inferred from source expectations.

Root entry exit and wrapper exit are both 1. The coordinator shell's successful completion is not a probe PASS. No failure, assertion, command or evidence was repaired; no test or database command was rerun by this reviewer.

## Independently verified completed prefix

All 816 transport records exactly match the complete declared ordered grid, without duplicate or missing route/input identities. The reviewer independently reconstructed fixed opaque bytes, UUIDs, bigint boundaries, NULL masks and tenant variants using standard-library data logic, then checked recorded input IDs, native/decoded types, NULL positions, lengths, expected-value hashes, actual OIDs/formats, callback records and outcome tags.

- Default decoding: 272 exact native matches.
- Connection-local shared decoding: 272 exact native matches.
- Deliberately distinct per-OID decoding: 272 INTENTIONAL_PER_OID_DIVERGENCE observations.
- All 48 isolation records correspond exactly to completed loader cases and record connection closure, unchanged global loader classes and untouched fresh-default checks before/after.
- All four negative records match sync/async × text/binary and contain the exact eight rejected actual-observation mutations: format, integer type, integer value, length, native value, NULL slot, OID and slot order. All 32 controls completed after an unmodified genuine baseline passed.

The passing source-bound tests and complete safe records support this narrow native PostgreSQL/psycopg transport characterization. Intentional custom-loader divergence is a compatibility hazard, not public-equivalence qualification. SQLAlchemy engine json_deserializer, ORM/streaming/outer-join behavior, _ReadText context semantics, crypto/key lifecycle and any product derivative remain untested here.

## Exact selected invocation and provenance

- Packet: experiments/json-transport-native-probe-v2-20261015.
- Packet seal: d5f457b3968d86adaa2a4f0ecaa70bd7a2a1ab73e6ebaca924de907550716377.
- Source review: reviewer-notes/json-transport-native-probe-independent-20261015/REVIEW.md, SHA256 d3d1c24896b6d6e5c1454ba60a21cbaf15ab9e7d50f497707db58b9e1e3e6b58.
- Actual selection SHA256: 1d99e6f8a7370222cfe0263e7f53c72fad0c6a6501bcd6f73a747620b4843176.
- Exact predecessor terminal review: reviewer-notes/integrated221-installed-focused111-sa20-v2-independent-20261015/REVIEW.md, SHA256 7318b0b3f7bac950a8e2311dd6d546d6c5f5b376c168d9eec0e0f4c4d97d7678.
- Actual root capture: /workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/json-transport-native-probe-v2-sa21-root.
- Evidence: evidence/json-transport-native-probe-v2-sa21-20261015.

Actual root argv is the exact /bin/bash V2 entry, sa21, selection digest and packet seal, with laboratory cwd, shell=false and the frozen four-key non-secret environment. The runner's complete pytest arguments match the frozen single external file selection plus the unchanged wrapper's progress, faulthandler and JUnit additions. The actual empty-prefix node IDs match the exact frozen strings; no suffix normalization was used. V1's original identity HOLD remains unchanged.

Current selection, ten packet members, seal and all 21 finite source/map/review references match their pinned bytes. Both selected reviews and root semantic/authority/exclusive-boundary declarations are present. Actual root receipts support the selected action; file hashes alone are not treated as authority.

## Archive, source and complete cold installed closure

The archive producer exited0 before the live main43 guard and wrapper, as required by the pinned entry. The archive receipt and independent inventory agree on exactly 233 ordinary files and 23 directories: source221 plus ten packet members, seal and actual selection. Every archived digest agrees with its admitted original. No installed dependency, cache, corpus or credential payload was placed in this archive.

Both original and clean source221 trees have the exact admitted ordinary name/type set under the inherited source-cache exclusions, and all source hashes match. The wrapper's separate source-repository and sole external-test snapshots/copies are also exact and unchanged. The source test file remains SHA256 8f848a77c42067c79f9070cfc7ce2c8c2cd1c6eff64a08cc6e33e938b4f00faa.

The unchanged main43 pre/post guards both exit0 and report the same exact 3,025-target manifest union. This is 3,024 INPUTS targets plus the distinct clearance review; the union, not a guessed count, was independently reconstructed from the four bound manifests. Every current target hash matches the accepted bindings and both receipts after complete metadata admission.

Independent current cold namespace counts are:

- SA21: 111 directories, 1,255 regular files, four aliases.
- SA20: 113 directories, 1,253 regular files, four aliases.

All 2,506 ordinary installed files and all 2,402 nonproduct files agree with their exact maps. Both opaque uv_cache.json installer markers were lstat-only and match their complete recorded metadata; neither body was read or hashed. No new cache/bytecode namespace was admitted. Interpreter chains, link texts and endpoints match the exact allowed set.

All 43 current installed product modules in each cell were independently joined to the source43 map, yielding 86 matches. The actual safe origin log records the selected installed SA21 package and 43 byte-matched modules. These are bounded source/installation identity snapshots, not continuous imported-code attestation or new dependency provenance.

## Stopped and restored boundary

Root explicitly reported session71196 terminal before this reviewer inspected runtime evidence or current boundary files, and confirmed the laboratory would remain quiescent with no next database stage during the audit.

Safe wrapper phase lines record start0, readiness0, origin0, tests1 and stop0. Fresh dual-role readiness and the runner's own preflight are recorded. The stop log ends with server stopped. Both independently captured root pg_ctl status commands use the exact frozen command/cwd/environment and return3 with no server running and empty stderr. The packet's separate pre/post status receipts agree. The reviewer issued no status or database command.

All 26 corpus names/hashes agree across root before/after snapshots, accepted corpus baseline, both main43 guards, wrapper prior-corpus manifest, retained originals and independent current hashing. The generated-corpus directory is empty. Isolation reports primary_receipts_restored=true, archived=[], deleted_during_run=[] and errors=[].

The separate source/archive post-gate and main43 post-gate both exit0. No unchanged-source, installed, corpus, stop or restoration failure is hidden behind the test failure. This is an accepted dated closed boundary for the failed run, not a standing assertion after subsequent activity.

## Audit record, limits and next-stage boundary

- OBSERVATION_CHECKS.json: 1,777 passing accounting comparisons; the record explicitly preserves the failed full-probe goal.
- CLOSURE_CHECKS.json: 531 passing identity/archive/corpus comparisons and the full finite current-target hash set.
- RUNTIME_MODULE_JOIN.json: 86 installed-to-source module joins.
- Each bounded standard-library audit has its original script, exit0, stdout and empty stderr. Audit success means the failed-run evidence was accounted for; it does not turn the failed test run green.

An initial metadata lookup interpreted the supplied relative root capture under the laboratory base and found it absent. Root supplied the exact sibling-directory absolute path; only that confirmed path was then inspected. This navigation correction did not alter or retry any experiment.

The reviewer read no raw tests/readiness/package-origin/postgres-start/postgres-stop JSON body, environment dump, credential, private-reader output, cache or bytecode payload. No project/dependency/helper import or execution, compilation, collection, tests, database/status command, installation, Git/network action or evidence mutation occurred. Only read-only finite metadata/hash/data checks and new reviewer-owned artifacts were used.

No native cost conclusion can be drawn. Any correction belongs in a separately sealed and independently reviewed source successor with new selection and this actual failed-run closure bound as its predecessor. The completed 52 cases are retained evidence and are not a reason to rerun them. No subsequent stage is selected by this review. All seven broad product gates remain UNKNOWN.
