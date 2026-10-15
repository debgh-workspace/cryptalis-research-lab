# Independent terminal audit: internal cleanup transport RED SA2.0

Date: 2026-10-14 UTC. Mode: static, data-only audit of recorded terminal evidence. This reviewer executed no test, candidate import, database action, or next cell.

## Decision

Accept the supplied SA2.0 cell as the intended bounded RED result: **8 expected assertion failures and 9 passes in 0.18 seconds**, with all 17 reviewed node IDs and all 51 setup/call/teardown reports. All eight failures occur at the intended literal effects assertion: restored `none` versus required `unknown`. There are no collection errors, unexpected failures, skipped cases, setup failures, teardown failures, or recorded timeouts.

Tests, wrapper, and outer block each returned 1. The separate shutdown evidence is explicit: `outer.log:354` records `postgres-stop exit 0`; line 356 and `postgres-stop.log` record `server stopped`. All checked packet, command, input, native-source, candidate-source, snapshot, and corpus preservation records agree. No blocker was found in these supplied terminal records.

This accepts expected RED evidence only. It does not accept the proposed correction or authorize another cell. The coordinator retains one-block-at-a-time admission.

## Evidence and identity

Paths below are relative to `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

- Runtime evidence: `evidence/cleanup-transport-metadata-red-sa20-20261014`.
- Command, driver, outer capture, and captured packet: the same path with `-packet` appended.
- Frozen packet: `experiments/cleanup-transport-metadata-20261014`.
- Source/command review: `reviewer-notes/transport-reducer-plan-independent-20261014/review.md`, SHA-256 `e83ecee900c9223103660497ebe49827cf5776cf9b40f65e3c355675cd46809e`.
- Accepted counterpart: `reviewer-notes/transport-red-sa21-independent-20261014/review.md`, SHA-256 `14d6c82870878d3ef1fb4be100d9f6dfd490fe88644f77d32cfafa50e949f9ba`.
- PACKET.sha256 anchor: `6a7257031d8e38e7712aa037c14fa704579d6cb994c9be205ba6e8f39c8247d3`.
- Reviewed/captured driver: `877a8691e87ace5771c4e9d3994b645bc62d736de8b265456fc71da107e359ab`.
- Exact captured RED SA2.0 command: `81584a394d6f9c9ba32d9905eb942bb4131d222722607ebca215853bf5257a23`.

The captured command is byte-identical to a separate single-block extraction from the anchored command packet. The captured driver matches the reviewed hash and coordinator copy. The packet contains exactly its 29 listed ordinary files plus PACKET.sha256; the captured packet has the same exact inventory and bytes. No captured command or project code was executed during this audit.

The command selects the immutable RED candidate and explicit `release-lab/s25-installed-20261014/sa20/bin/python` dependency cell. The pinned SQLAlchemy source declares version 2.0.51. `outer.log:280-281` records successful package-origin verification against the RED candidate's `src/cryptalis/__init__.py`. This audit did not execute or hash an interpreter, import a dependency, or qualify an installed wheel.

All 9 INPUTS entries, 14 approved native SQLAlchemy source entries, 2 original-mailbox entries, 29 packet entries, and 218 RED source entries currently hash correctly. The outer capture contains exactly the expected ordered 272 successful pin lines before and after the run. Separate driver packet/input checks also match their expected output; packet-copy logs are empty with recorded exit 0. Coordinator status agrees with the command hash, packet anchor, outer exit 1, and wrapper exit 1. The separate wrapper-exit file agrees. Driver process success alone was not treated as test success.

## Exact outcomes and assertion boundaries

JUnit records 17 cases, 8 failures, 0 errors, 0 skips, and a suite duration of 0.186 seconds. The test log reports 0.18 seconds; the runner receipt measures approximately 0.381 seconds. Those measurements cover different scopes.

The ordered NEW_NODE_IDS list matches JUnit, progress starts, progress calls, and runner-receipt selection exactly. Progress contains 68 events: 17 starts and 51 reports. Each node has exactly one start, setup, call, and teardown in that order. All 17 setup and 17 teardown reports passed; calls are 8 failed and 9 passed. The independently enumerated expected failure nodes match JUnit, progress, and the test-log summary.

| Case group | Observed call outcome | Reached assertion boundary |
|---|---:|---|
| Fresh KeyUnavailable | 1 pass | Literal safe identity/diagnostics, effects `none`, retryable singleton True |
| Downgraded key/backend/base | 3 failures | Identity and exact built-in effects-string check pass; line 72 fails on effects |
| Fresh schema/custody | 2 passes | Literal existing original/restored class effects and singleton False retryability |
| Notes/cause/context/provider_data | 4 failures | Sensitivity and private-state exclusions pass; line 125 fails on effects |
| Unrelated attached sentinel | 1 failure | Round trip, identity, and absent provider_data pass; line 154 fails on effects |
| Six non-whitelist combinations | 6 passes | Restored effects `none` and retryable singleton True |

All cases invoke the common identity helper before their effects assertions. Thus exact class, distinct object identity, code, operation ID, args, stage/remedy equality, and absent cause/context/traceback checks are reached and pass in all 17 cases.

In each privacy case, lines 101 and 104 establish marker sensitivity in serialized marker bytes and note-bearing rendered output. Line 117 establishes visibility of the individual original carrier. Lines 121-124 then establish no marker in serialized exception bytes or restored rendering, and no restored notes or provider_data. Every one of these checks precedes the observed line-125 failure and therefore passed for the supplied synthetic fixtures. Their exclusion success is not inferred only from case names.

The unrelated-state round trip completes without triggering the attached sentinel's raising reduction, equality, truth-conversion, or render methods. Its provider_data exclusion is reached before failure. The six passing controls cover True, integer zero, a different effects string, a string subclass, an opaque effects object, and an opaque retry object. Their baseline success does not establish the proposed GREEN admission logic; no source-mutant run occurred.

**All eight failing cases stop before their retryability assertions:** lines 73, 126, and 155 are unreached. They must not be reported as passed. The RED reducer at `src/cryptalis/crypto/keys.py:38-43` serializes only code, operation_id, and args, explaining the restored class-default effects. Source reasoning about retryability remains distinct from runtime assertion evidence in these eight cases.

## Preservation checks

The live frozen inventories and digests agree with their manifests, with no unexpected ordinary files or symbolic links apart from documented excluded Python/pytest caches:

- RED: 218 files.
- Unexecuted GREEN: 218 files.
- Inherited candidate: 217 files.

RED and GREEN test files are identical. Their reducer files match the separately frozen baseline/GREEN copies. Runtime source-before and source-stability before/after maps agree for all 157 recorded files. All 157 live files and captured source-repository copies match that map, with exact captured inventory. The runner receipt's 156-entry map matches its distinct coverage: 155 Python source/test files plus the pinned runner. External-source maps are empty and unchanged.

All 26 pre-existing corpus originals and all 26 preserved backup copies match the path-validated prior-corpus manifest. The current matching corpus inventory is exact. The isolation record reports no archived outputs, no deletions, no errors, and successful primary-receipt restoration. Candidate-corpus is empty. These focused tests produced no new compatibility corpus evidence.

## Comparison with accepted SA2.1 RED

This SA2.0 audit independently reproduces the same 17 ordered nodes, eight expected failure nodes and exact failure boundaries, nine passes, all 51 phase outcomes, source maps, receipt source map, corpus manifest, and terminal phase exit sequence as the accepted SA2.1 audit. Those derived records compare byte-for-byte where applicable. The selected dependency path/version, exact command digest, evidence path, timestamp, and duration differ as intended. SA2.0's 0.18-second test summary and SA2.1's 0.22-second summary are not evidence of a meaningful performance difference.

Both RED cells fail before the same eight retryability oracles. Neither result proves the GREEN correction or broad transport compatibility.

## Terminal and scope limits

The allowed outer capture records once each: start exit 0, readiness exit 0, package-origin exit 0, tests exit 1, and stop exit 0, followed by the independent-audit stop line. The receipt reports passed preflight. Shutdown is accepted from the explicit recorded stop result and shutdown text, not inferred from wrapper status. This reviewer made no later live process, socket, or database probe and makes no claim about the lab after the recorded session.

Only regular-file/path validation, source/evidence reads, shell/JQ text processing, byte comparison, and SHA-256 checks were used. Audit writes remain within this reviewer directory. The adjacent `audit-checks.sh` and successful log reproduce the bounded checks; they do not run the captured command. No Python process, import, test collection/execution, database action, network action, Git command, package installation, source edit, or next-cell execution occurred. Forbidden raw phase JSON and credentials/environment files were not read, hashed, or copied.

This evidence concerns trusted-local protocol-5 round trips of synthetic exceptions. It does not establish a real cleanup branch, application retry behavior, physical rollback, pool quarantine, provider custody, cross-process transport, public IPC, cross-version pickle, arbitrary host-mutated diagnostics, arbitrary subclass/accessor behavior, release artifacts, or production readiness. Untrusted pickle remains outside scope. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY, and G-RELEASE remain UNKNOWN.
