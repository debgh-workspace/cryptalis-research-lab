# Independent terminal audit: internal cleanup transport GREEN SA2.1

Date: 2026-10-15 UTC. Method: static, data-only inspection of the completed cell. This reviewer executed no candidate code, test, database action, or next cell.

## Decision

**ACCEPT_BOUNDED_GREEN_SA21_TRANSPORT.** The exact 17 reviewed cases pass, with all 51 setup/call/teardown reports passing. The test summary is **17 passed in 0.18 seconds**. All eight intended RED effects failures are corrected and reach their subsequent `retryable is False` assertions. All nine preservation/whitelist controls still pass. There is no recorded failure, error, skip, missing phase, collection failure, or timeout.

Tests, wrapper, and outer block each return 0. The explicit shutdown record is separate: `outer.log:288` records `postgres-stop exit 0`; line 290 and the separate `postgres-stop.log` record `server stopped`. All bounded source, packet, command, input, native-source, mailbox, snapshot, and corpus checks pass. No blocker was found in the supplied terminal evidence.

This accepts one trusted-local synthetic serialization cell on the selected SA2.1 dependency cell. It does not execute or authorize the next cell. Coordinator-controlled admission remains separate.

## Evidence and pinned identity

Paths are relative to `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable`.

- Runtime evidence: `evidence/cleanup-transport-metadata-green-sa21-20261014`.
- Captured driver, command, outer capture, and packet: the same path with `-packet` appended.
- Frozen packet: `experiments/cleanup-transport-metadata-20261014`.
- Accepted source/command review: `reviewer-notes/transport-reducer-plan-independent-20261014/review.md`, SHA-256 `e83ecee900c9223103660497ebe49827cf5776cf9b40f65e3c355675cd46809e`.
- PACKET.sha256 anchor: `6a7257031d8e38e7712aa037c14fa704579d6cb994c9be205ba6e8f39c8247d3`.
- Captured and coordinator driver: `877a8691e87ace5771c4e9d3994b645bc62d736de8b265456fc71da107e359ab`.
- Exact GREEN SA2.1 command: `923f8f59009f9d6791833debc73789ab2c3ef24448b2a0da1b02c5860d730d7b`.
- GREEN source listing: `8834d8b6303a349d1508e6c729c77eda6b134298dcdba3bc39ffc25929a06eb1`.
- GREEN reducer file: `ea67be78edbbe7489dd296c57f337fea1dedf84a42e73a6ede2d3aa6d3ab1cae`.
- Unchanged RED/GREEN test file: `49c5ed8e192fdef721d74117ad9bbcd685988519d043a1c1e89100689c5467cc`.

The exact command is byte-identical to an independent extraction of the single GREEN SA2.1 block from the anchored proposed commands. The captured driver matches both the reviewed digest and the coordinator copy. The frozen packet and captured packet each contain exactly the same 30 ordinary files: 29 listed files plus PACKET.sha256. Their complete inventories and bytes agree.

All 9 input pins, 14 explicitly approved installed SQLAlchemy public-source pins, 2 original-mailbox pins, 29 packet pins, and 218 selected source pins match. The outer capture contains exactly the expected ordered 272 successful pin lines before and after execution. Separate driver input/packet checks agree; both packet-copy logs are empty, and their recorded exits are 0. Coordinator status agrees with the command digest, packet anchor, selected phase/cell, and outer/wrapper exits. Driver process success alone was not treated as a test result.

The command selects `release-lab/s25-installed-20261014/sa21/bin/python`. The approved SQLAlchemy source declares version 2.1.3. The allowed outer capture records successful source-origin verification against the GREEN candidate at lines 280-281, and source-root metadata agrees. This audit did not start or hash an interpreter, import a dependency, or qualify an installed wheel.

Both prior RED reviews accept their expected 8-fail/9-pass outcomes. Their ordered nodes and corpus manifests agree with this cell. Their current review hashes are `14d6c82870878d3ef1fb4be100d9f6dfd490fe88644f77d32cfafa50e949f9ba` (SA2.1) and `e4e10a01fd40fa7be99bd3e9c462dbd321435d3fb264150768fc863702f52a17` (SA2.0). The supplied optional integration review accepts its separate bounded 38-case cell and hashes to `41972f42313c765c0a7c927ac8c068ba88559889c744edcbc41be76b65af980d`. Their current modification times precede this GREEN JUnit timestamp, consistent with the coordinator's stated admission sequence. Filesystem chronology is corroboration, not immutable proof of the admission decision; optional integration was not re-audited here.

## Exact outcomes and assertion reach

JUnit records exactly one suite and 17 cases, with 0 failures, 0 errors, 0 skips, and 0.182 seconds. Its timestamp is `2026-10-15T01:01:25.973167+00:00`. The test log rounds the duration to 0.18 seconds; runner elapsed time is approximately 0.437 seconds. These are different measurement scopes.

The independent literal enumeration from the test source, frozen NEW_NODE_IDS list, JUnit cases, progress starts/calls, and runner-receipt selections agree exactly in order. Progress contains 68 events: 17 starts and 51 reports. Every case has exactly one start, setup, call, and teardown in that order. All 17 setup, 17 call, and 17 teardown outcomes are ordinary passes.

| Cases | Count | Confirmed assertion boundary |
|---|---:|---|
| Fresh KeyUnavailable | 1 | Exact safe class diagnostics and identity; effects `none`; retryability singleton True |
| Downgraded key/backend/base | 3 | Exact built-in effects string, literal `unknown`, and subsequent singleton False at lines 71-73 |
| Fresh schema/custody | 2 | Existing literal original/restored class effects and singleton False at lines 89-93 |
| Notes/cause/context/provider_data | 4 | Positive detector controls, private-state exclusions, effects `unknown`, and subsequent singleton False through line 126 |
| Unrelated attached sentinel | 1 | Successful round trip without inspecting attached object; absence of provider_data; effects `unknown`; subsequent singleton False through line 155 |
| Six rejected metadata combinations | 6 | Class-default effects `none` and singleton True through line 183 |

The eight previously failing cases are the three cleanup-downgrade cases, four private-carrier cases, and unrelated-state case. Both RED audits stopped these cases at their effects assertions; retryability assertions were not reached then. This GREEN cell passes the unchanged cases completely, so both effects and the later retryability assertions are now established. The fresh/class-default and six whitelist controls account for the other nine unchanged passes.

Every case invokes `_assert_identity` at lines 26-36. It confirms exact exception class, a distinct restored instance, expected code, original operation ID and args, matching stage/remedy, and absent cause/context/traceback. The preservation claim concerns the safe values constructed in these fixtures. It does not sanitize arbitrary host replacements of code, operation ID, or args.

For each private-carrier case, line 101 proves marker sensitivity in serialized bytes and line 104 proves marker sensitivity in rendered note-bearing output. Line 117 proves the original individual carrier is observable. Lines 121-124 then confirm no marker in the exception payload or restored rendering, and no restored notes/provider_data. These positive controls and negative observations all pass before the final metadata assertions. The separate attached object raises on reduction, equality, truth conversion, and rendering; its round trip and exclusion checks pass. These results cover the synthetic private state used here, not arbitrary provider custody.

## Strict whitelist and narrow source change

The sole RED-to-GREEN source difference is `CryptoFailure.__reduce__`, at `src/cryptalis/crypto/keys.py:38-49`. The exact return class, empty constructor tuple, and original `code`, `operation_id`, and `args` fields remain. The reducer reads effects once, requires an exact built-in `str` equal to `unknown`, and requires retryability to be the singleton False. It writes fixed primitive literals for the two extra fields. It does not serialize the inspected objects or merge an instance dictionary.

The six passing rejection controls cover True, integer zero, a different effects string, a string subclass, an opaque effects object, and an opaque retry object. The subclass raises on equality/reduction, and opaque sentinels raise on inspection. Passing these fixtures agrees with exact-type short-circuiting and identity comparison: subclass/custom equality and retry truth conversion are not needed. No source-mutant sensitivity run was performed, and arbitrary subclass constructors/accessors remain outside this contract.

Notes, causes, contexts, traceback, provider objects, and unrelated attributes are not added to the state. Class defaults remain the restoration behavior for other metadata combinations, including the distinct schema/custody classifications. The implementation and tests do not establish arbitrary host-owned classification transport.

## Source and corpus preservation

Complete live source inventories match their manifests without unexpected ordinary files or symbolic links, apart from the explicitly excluded Python/pytest caches:

- GREEN: 218 files.
- RED: 218 files.
- Inherited candidate: 217 files.

All JSON source maps/counts agree with the SHA listings. RED preserves all inherited files and adds only the test file. GREEN preserves that inventory and changes only the reducer file. Both reducer copies match their frozen packet counterparts; both test copies are identical.

The runtime source-before map and source-stability before/after maps agree for all 157 entries. The live GREEN files and all 157 captured source-repository files hash to that map, and the captured inventory is exact. The runner receipt's 156-entry map agrees with its separate coverage: the 155 Python source/test entries plus the pinned runner. External-source maps are empty and unchanged. The distinct snapshot and receipt scopes were not conflated.

All 26 pre-existing corpus originals and all 26 preserved backups match the strictly path-validated prior-corpus manifest. The current matching corpus inventory is unchanged. The isolation record reports no archived output, deletion, or error, and successful primary-receipt restoration. Candidate-corpus is empty. This focused selection generates no new compatibility-corpus result.

## Terminal boundary and method

The allowed outer log records one successful exit each for start, readiness, package-origin, tests, and stop, followed by the independent-audit stop line at 564. Runner preflight is passed. Explicit stop exit and shutdown text establish the recorded session's terminal shutdown; wrapper exit alone would not. No later live process, socket, or database probe was made, and this audit makes no claim about lab state after that recorded session.

The adjacent `audit-checks.sh` and successful `audit-checks.log` reproduce the bounded verification. The checker was adapted from the prior static audit and its GREEN expectations were inspected against this source and evidence. It uses regular-file/path validation, shell/JQ data processing, byte comparisons, and SHA-256 checks only. Referenced manifest filenames are validated before hashing referenced bytes. No Python process, candidate import, test collection/execution, database/network/Git action, installation, source edit, or next-cell execution occurred. No forbidden raw phase JSON, credentials, environment files, or cache payloads were read, hashed, or copied. All reviewer writes remain within this directory.

This result proves only the named trusted-local protocol-5 synthetic round trips on this cell. It does not prove a real cleanup branch, application retry behavior, physical rollback, pool quarantine, cross-process transport, public IPC, cross-version pickle, arbitrary subclass/accessor behavior, installed artifacts, the full suite, or production readiness. Untrusted pickle remains outside scope. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY, and G-RELEASE remain UNKNOWN. GREEN SA2.0 receives no runtime result from this audit.
