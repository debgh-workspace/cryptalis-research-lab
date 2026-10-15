# Independent terminal audit: internal cleanup transport GREEN SA2.0

Date: 2026-10-15 UTC. Method: static, data-only review of the completed cell. No candidate runtime, import, test, or database action was executed by this reviewer.

## Decision

**ACCEPT_BOUNDED_GREEN_SA20_TRANSPORT.** The exact 17 reviewed cases and all 51 setup/call/teardown reports pass. The recorded test summary is **17 passed in 0.18 seconds**. All eight intended RED effects failures are corrected and reach their subsequent `retryable is False` assertions. All nine preservation/whitelist controls still pass. No failure, error, skip, collection failure, missing phase, or timeout is recorded.

Tests, wrapper, and outer block each return 0. Separately, `outer.log:288` records `postgres-stop exit 0`; line 290 and `postgres-stop.log` record `server stopped`. The source, packet, command, input, native-source, snapshot, and corpus preservation checks pass. No blocker was found within the supplied terminal evidence.

This accepts the named trusted-local synthetic serialization cell on the selected SA2.0 dependency cell. It neither executes nor authorizes further runtime work, integration, packaging, or release.

## Evidence and command identity

Paths below are relative to `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

- Evidence: `evidence/cleanup-transport-metadata-green-sa20-20261014`; captured command, driver, packet, outer log, and coordinator status are in the adjacent `-packet` directory.
- Frozen packet: `experiments/cleanup-transport-metadata-20261014`.
- PACKET.sha256 anchor: `6a7257031d8e38e7712aa037c14fa704579d6cb994c9be205ba6e8f39c8247d3`.
- Exact captured command: `741ed2716c773a5d94e42ed9c441a8665c189fa4aa2f4b0ec8692d110e616070`.
- Captured and coordinator driver: `877a8691e87ace5771c4e9d3994b645bc62d736de8b265456fc71da107e359ab`.
- GREEN source listing: `8834d8b6303a349d1508e6c729c77eda6b134298dcdba3bc39ffc25929a06eb1`.
- GREEN reducer: `ea67be78edbbe7489dd296c57f337fea1dedf84a42e73a6ede2d3aa6d3ab1cae`.
- Unchanged RED/GREEN test: `49c5ed8e192fdef721d74117ad9bbcd685988519d043a1c1e89100689c5467cc`.

The captured command is byte-identical to the independently extracted single GREEN SA2.0 block from the anchored command text. The captured driver matches the reviewed hash and current coordinator copy. The packet and captured packet have identical complete inventories and bytes: 29 listed ordinary files plus PACKET.sha256, exactly 30 files.

All 9 INPUTS entries, 14 approved installed SQLAlchemy public-source entries, 2 original-mailbox entries, 29 packet entries, and 218 selected GREEN source entries currently match their pins. The actual outer capture has exactly the expected 272 successful pin lines in order both before and after execution. Separate packet/input verification outputs also agree; packet-copy logs are empty and the recorded exits are 0. Coordinator status and the separate wrapper-exit file agree with the command digest, anchor, selected phase/cell, outer 0, and wrapper 0. The driver process exit alone was not used as a test outcome.

The selected command names `release-lab/s25-installed-20261014/sa20/bin/python`. The pinned public SQLAlchemy source declares version 2.0.51. The successful package-origin record at outer-log lines 280-281 identifies the GREEN candidate's `src/cryptalis/__init__.py`, and source-root metadata agrees. No interpreter was executed or hashed, dependency imported, or installed wheel qualified by this audit.

## Prior reviews and counterpart comparison

All four required reviews were read and their hashes verified:

- Source/command review: `reviewer-notes/transport-reducer-plan-independent-20261014/review.md`, `e83ecee900c9223103660497ebe49827cf5776cf9b40f65e3c355675cd46809e`.
- RED SA2.1: `reviewer-notes/transport-red-sa21-independent-20261014/review.md`, `14d6c82870878d3ef1fb4be100d9f6dfd490fe88644f77d32cfafa50e949f9ba`.
- RED SA2.0: `reviewer-notes/transport-red-sa20-independent-20261014/review.md`, `e4e10a01fd40fa7be99bd3e9c462dbd321435d3fb264150768fc863702f52a17`.
- Accepted GREEN SA2.1: `reviewer-notes/transport-green-sa21-independent-20261015/review.md`, `773923ddee6e3e5d7a26be697b23c8a4716200748698758e2ef27b13cde1cea5`.

Both RED progress records independently identify the same eight failed nodes and nine passing controls. All 17 now pass in SA2.0 GREEN. Node lists and corpus manifests agree with both RED reviews. Against actual GREEN SA2.1 evidence, normalized start/setup/call/teardown events, source-before maps, receipt source maps, and prior-corpus manifests compare byte-for-byte. The selected dependency path/version, command digest, evidence path, timestamp, and durations differ as intended. No performance conclusion is drawn from these short runs.

## Outcomes and assertion reach

JUnit contains exactly one suite and 17 cases, with 0 failures, 0 errors, 0 skips, and a duration of 0.179 seconds. Its timestamp is `2026-10-15T01:07:52.828292+00:00`. The test summary rounds to 0.18 seconds; the runner measures approximately 0.469 seconds. These cover different measurement scopes.

Literal enumeration from the unchanged test source, NEW_NODE_IDS, JUnit, progress starts/calls, and runner selection agree exactly in order. Progress contains 68 events: 17 starts and 51 reports. Every node has one start, setup, call, and teardown in that order. All 17 setup, 17 call, and 17 teardown reports pass.

| Group | Cases | Reached and passed assertion boundary |
|---|---:|---|
| Fresh KeyUnavailable | 1 | Exact safe class diagnostics and identity, effects `none`, retryability singleton True |
| Downgraded key/backend/base | 3 | Exact built-in effects string, literal `unknown`, subsequent singleton False through lines 71-73 |
| Existing schema/custody effects | 2 | Literal original/restored class effects and singleton False through lines 89-93 |
| Notes/cause/context/provider_data | 4 | Positive sensitivity controls, private-state exclusions, `unknown`, subsequent singleton False through line 126 |
| Unrelated attached sentinel | 1 | Round trip and absent provider_data, `unknown`, subsequent singleton False through line 155 |
| Non-whitelist pairs | 6 | Restored class-default effects `none` and singleton True through line 183 |

The eight RED regressions are the three downgrade cases, four private-carrier cases, and unrelated-state case. Both RED cells stopped at their effects assertions; their later retryability assertions were unreached. Here the unchanged cases pass completely, establishing both fields. The other nine controls retain their passing outcomes.

All cases invoke the common identity helper at lines 26-36: exact exception class, distinct restored instance, expected code, original operation ID and args, matching stage/remedy, and absent cause/context/traceback. These are the safe values constructed by the fixtures, not a guarantee about arbitrary host-mutated diagnostics.

Every private-carrier case passes marker sensitivity in serialized bytes (line 101), rendered note-bearing output (line 104), and the original individual carrier (line 117). Lines 121-124 then establish marker absence from the exception payload and restored rendering, plus absent notes/provider_data. All pass before the final metadata assertions. The unrelated object raises on attempted reduction, equality, truth conversion, and rendering; its round trip and exclusion pass. These positive controls support the observed negative results for the named synthetic fixtures.

## Source boundary and preservation

The sole RED-to-GREEN source change is `CryptoFailure.__reduce__`, at `src/cryptalis/crypto/keys.py:38-49`. It preserves the return class, empty constructor tuple, and existing code/operation_id/args state. It reads effects once, accepts only an exact built-in string equal to `unknown` paired with the singleton False, and writes fixed primitive literals. It adds no instance-dictionary merge, notes, cause, context, traceback, provider object, or arbitrary attached attribute.

The six passing rejection controls cover True, integer zero, another effects string, a string subclass, an opaque effects object, and an opaque retry object. The subclass raises on equality/reduction and opaque objects raise on inspection. These results agree with exact-type short-circuiting and identity checks. Other metadata combinations retain class defaults, including the separate schema/custody classifications. No source-mutant run was performed. Arbitrary subclass constructors/accessors and arbitrary host-owned classifications remain outside scope.

Complete source inventories and JSON/SHA maps agree: GREEN 218 files, RED 218, inherited candidate 217. There are no unexpected ordinary files or symbolic links apart from documented excluded Python/pytest caches. RED adds only the test to the unchanged inherited source; GREEN changes only the reducer. Test copies are identical and reducer files match their frozen packet copies.

The runtime source-before map and source-stability before/after maps agree for all 157 entries. All live and captured source files match, with exact captured inventory. The receipt's 156 entries agree with its different scope: 155 Python source/test files plus the pinned runner. External-source maps are empty and unchanged.

All 26 pre-existing corpus originals and all 26 preserved backups match the path-validated prior-corpus manifest. Original and backup inventories are exact. The isolation record reports no archived output, deletion, or error, and successful primary-receipt restoration. Candidate-corpus is empty. This focused selection produced no new compatibility-corpus result.

## Terminal record, method, and limits

The outer capture contains exactly five phase statuses, each once and each 0: start, readiness, package-origin, tests, and stop. It contains one explicit `server stopped` line and ends with the independent-audit stop record at line 564. Runner preflight is passed. Explicit final-stop evidence is required because wrapper success alone does not establish shutdown. No later live process, socket, or database probe was made; this accepts the recorded session shutdown, not an assertion about subsequent lab state.

`audit-checks.sh` and `counterpart-checks.sh`, with their separate attempt-1 logs and exit records, reproduce the data-only checks. Both attempts returned 0. The main checker was adapted from the accepted SA2.1 checker; its adaptation diff is retained, and source assertions and GREEN expectations were inspected independently. Referenced manifest paths were validated before referenced byte hashing. Checks used shell/JQ processing, regular-file/path validation, byte comparison, and SHA-256 only. No Python process, candidate import, test collection/execution, database/network/Git action, installation, source/evidence edit, or next-cell execution occurred. Forbidden raw phase JSON, credentials/environment dumps, and cache payloads were not read, hashed, or copied. Reviewer writes are confined to this new directory; no failed reviewer attempt was discarded.

The evidence establishes the named trusted-local protocol-5 synthetic round trips. It does not prove a real cleanup branch, application retry behavior, physical rollback, pool quarantine, provider custody, public IPC, cross-process or cross-version transport, arbitrary host-mutated diagnostics, arbitrary subclass/accessor behavior, installed artifacts, full-suite status, or production readiness. Untrusted pickle remains outside scope. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY, and G-RELEASE remain UNKNOWN.
