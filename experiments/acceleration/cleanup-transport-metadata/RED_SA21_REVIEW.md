# Independent terminal audit: internal cleanup transport RED SA2.1

Date: 2026-10-14 UTC. Audit mode: read-only evidence and source verification. No phase was executed by this reviewer.

## Decision

Accept this cell as the intended, bounded RED result: **8 expected assertion failures and 9 passes**, with the exact 17 reviewed node IDs and all 51 setup/call/teardown reports. The eight failures all show restored effects `none` where the tests require literal `unknown`. No collection error, unexpected failure, skip, timeout, setup failure or teardown failure appears.

The recorded phase ended normally as a failing RED test selection: tests, wrapper and outer block each returned 1. The independent stop evidence is explicit: `outer.log:354` records `postgres-stop exit 0`; line 356 and the separate `postgres-stop.log` record `server stopped`. Source and corpus preservation checks pass. No blocker was found in the supplied terminal evidence.

This accepts the expected RED evidence, not the implementation, public IPC, async cleanup integration, a full test suite, or any production gate. This review executes and authorizes no next cell. The coordinator retains the one-block-at-a-time admission decision.

## Pinned identity and command custody

All paths below are relative to `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

- Runtime evidence: `evidence/cleanup-transport-metadata-red-sa21-20261014`.
- Captured command and packet: the same path with `-packet` appended.
- Frozen packet: `experiments/cleanup-transport-metadata-20261014`.
- Accepted source/command review: `reviewer-notes/transport-reducer-plan-independent-20261014/review.md`, SHA-256 `e83ecee900c9223103660497ebe49827cf5776cf9b40f65e3c355675cd46809e`.
- Frozen PACKET.sha256 anchor: `6a7257031d8e38e7712aa037c14fa704579d6cb994c9be205ba6e8f39c8247d3`.
- Reviewed and captured driver: `877a8691e87ace5771c4e9d3994b645bc62d736de8b265456fc71da107e359ab`.
- Exact captured RED SA2.1 command: `29d79fcd32073705b71cb8a702bf4c043566e6ea666270d7877375128d6b0325`.

The captured command is byte-identical to the independently extracted single RED SA2.1 block in the frozen command text. The captured driver matches the reviewed driver and the current coordinator copy. The packet has exactly 30 ordinary files: its 29 listed files plus PACKET.sha256. The captured packet matches it exactly.

The command selects the immutable RED candidate and the explicit `release-lab/s25-installed-20261014/sa21/bin/python` dependency-cell interpreter. The approved SQLAlchemy source pin is unchanged and its version declaration is 2.1.3. The safe outer capture records successful package-origin verification against the RED candidate's `src/cryptalis/__init__.py`. This audit did not execute or hash an interpreter, import a dependency, or make an installed-wheel qualification claim.

All 9 INPUTS pins, 14 approved installed SQLAlchemy public-source pins, 2 original-mailbox pins, 29 packet pins and 218 RED source pins currently match. The actual outer log contains the exact ordered 272 successful pin lines both before and after the run. The driver's separate packet/input before/after logs also match their expected successful output, and both packet-copy logs are empty with recorded exit 0. The coordinator status contains outer exit 1 and wrapper exit 1; the separate wrapper-exit file agrees. A driver process exit alone was not used as a result.

## Exact outcomes and reached assertions

JUnit records 17 cases, 8 failures, 0 errors and 0 skips, with 0.225 seconds for its suite. The test log reports `8 failed, 9 passed in 0.22s`; the runner receipt separately records approximately 0.446 seconds. These are different measurement scopes, not conflicting results.

The ordered node list in NEW_NODE_IDS.txt matches JUnit, progress starts, progress calls and runner-receipt selection exactly. Progress has 68 events: 17 starts and 51 reports. Every case has exactly one start, setup, call and teardown in that order. All 17 setup and all 17 teardown outcomes pass; call outcomes are 9 passed and 8 failed. The failure-node list agrees between progress and the test-log summary.

| Cases | Observed call result | Assertion boundary |
|---|---|---|
| Fresh KeyUnavailable | 1 pass | Identity, literal safe class diagnostics, effects `none`, retryable singleton True all reached |
| Downgraded key/backend/base | 3 failures | Identity and exact built-in effects-string check passed; line 72 fails with `none` versus `unknown`; line 73 retryable assertion was not reached |
| Fresh schema/custody | 2 passes | Both literal original/restored class effects and singleton False retryability reached |
| Private notes/cause/context/provider_data | 4 failures | All positive sensitivity controls and private-state exclusions below were reached; line 125 fails on effects; line 126 retryable assertion was not reached |
| Unrelated attached sentinel | 1 failure | Round trip, identity and absence of provider_data passed; line 154 fails on effects; line 155 retryable assertion was not reached |
| Six non-whitelist pairs | 6 passes | Every case reached restored effects `none` and retryable singleton True |

All calls invoke the identity helper before their later effect checks. Its type, distinct instance, code, operation_id, args, stage/remedy equality and absent cause/context/traceback assertions therefore passed in all 17 cases.

For each of the four privacy cases, the following checks precede the failure and therefore actually passed: marker visibility in serialized marker bytes; marker visibility in a note-bearing rendered positive control; visibility of the original individual carrier; absence of marker bytes in the exception payload; absence of the marker from restored rendering; absent restored notes and provider_data. These are exercised exclusions, not inferred solely from a failing case's test name. They establish the checks for these synthetic fixtures only.

The unrelated-state round trip did not trigger the attached sentinel's raising reduction/equality/truth/render methods, and its state-exclusion assertion was reached. The six passing pair controls cover True, integer zero, a different effects string, a str subclass, an opaque effects object and an opaque retry object. Their passing baseline behavior does not demonstrate the proposed GREEN whitelist in this RED run. No source-mutant sensitivity run was performed.

The missing retryability checks in all eight failing cases must not be reported as passed. RED's source reconstruction explains why effects revert to `none`; runtime assertions in this cell do not separately establish the restored retryable value for those eight cases.

## Source and corpus preservation

The full source inventories match the frozen manifests with no unexpected ordinary files or symbolic links, apart from the documented excluded Python/pytest caches:

- RED: all 218 files match.
- Unexecuted GREEN: all 218 files match.
- Inherited parent candidate: all 217 files match.

The RED/GREEN test files are byte-identical. Their key files match the separately frozen baseline and GREEN copies respectively. The runtime source-before map and source-stability before/after maps agree for all 157 recorded files. Both the live RED files and all 157 captured source-repository copies hash to that map, and the captured inventory is exact. The runner receipt's 156-entry map agrees with the same 155 Python source/test entries plus the pinned runner. External-source maps are empty and unchanged. The receipt and snapshot intentionally have different coverage; they were compared according to that coverage.

All 26 pre-existing corpus originals and all 26 preserved backup files match the validated prior-corpus manifest. The current matching corpus inventory is unchanged. The isolation report records no archived outputs, no deletion during the run, no errors and successful primary-receipt restoration. The candidate-corpus directory is empty. These focused tests generated no new compatibility corpus evidence.

## Terminal record and limits

The allowed outer capture records, once each: start exit 0, readiness exit 0, package-origin exit 0, tests exit 1 and stop exit 0, followed by the independent-audit stop line. Runner-receipt preflight is passed. This audit used the explicit final-stop record and shutdown text rather than inferring cleanup success from wrapper exit. It did not make a later live process/socket/database probe, and does not assert the lab's state after the recorded session.

Only existing source/evidence reads, path and regular-file validation, shell/JQ text processing, byte comparison and SHA-256 checks were performed. No Python/candidate import, test collection or test execution, database action, network action, Git command, installation, source edit or next-cell execution occurred. No forbidden raw phase JSON or credential/environment file was read, hashed or copied. Reviewer writes were confined to this directory. `audit-checks.sh` and its final successful log reproduce the bounded verification; it does not invoke the captured command.

The evidence is a trusted-local protocol-5 serialization check on synthetic exceptions. It does not prove a real cleanup path, cross-process transport, public IPC, cross-version pickle, physical rollback, pool quarantine, provider custody, arbitrary host-mutated diagnostics or arbitrary subclass/accessor behavior. Untrusted pickle remains outside scope. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE remain UNKNOWN. Other transport cells and broader inherited regression work receive no result from this audit.
