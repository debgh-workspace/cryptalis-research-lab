# Independent source and command review: internal cleanup metadata transport

Date: 2026-10-14 UTC. Review scope: frozen source, test design, proposed commands, and single-block capture driver. No runtime execution.

## Decision

Accept the frozen reducer/test design and the staged command plan for coordinator-controlled isolated RED/GREEN verification. No source or command blocker was found within this review's scope. This is not permission to execute a phase, integration acceptance, a test result, a production qualification, or independent human security review.

Run only one reviewed block at a time, after the prior session's required terminal audit and with the lab available. Audit that phase before admitting the next. The reviewed single-block driver prevents accidentally running all four proposed blocks. The parent reports both inherited async focused cells as independently accepted at 46 passes each; I did not re-audit those runtime receipts, and the inherited full-suite work remains pending in the supplied context.

All transport runtime outcomes remain NOT RUN in this review. The independently derived expectation is 8 RED failures and 9 RED passes per cell, followed by 17 GREEN passes if execution matches the inspected source.

## Frozen identities and preservation

All paths are relative to `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable` unless otherwise stated.

- Packet: `experiments/cleanup-transport-metadata-20261014`.
- PACKET.sha256 anchor: `6a7257031d8e38e7712aa037c14fa704579d6cb994c9be205ba6e8f39c8247d3`.
- RED source listing: `87fb38d2b7efe6a577ab36fb628a1c57e2317fe49437889f77b90cbf1dc43e11`.
- GREEN source listing: `8834d8b6303a349d1508e6c729c77eda6b134298dcdba3bc39ffc25929a06eb1`.
- New test: `49c5ed8e192fdef721d74117ad9bbcd685988519d043a1c1e89100689c5467cc`.
- RED keys.py: `b76d60f32011705726cc73f6211fa52e5624e475fc63573e578aa9e5078aea56`.
- GREEN keys.py: `ea67be78edbbe7489dd296c57f337fea1dedf84a42e73a6ede2d3aa6d3ab1cae`.
- Proposed command text: `0498464d43dc5c7779fbbb1cb435bac440f701ac1b4c5441e1533de11ade9293`.

Validated manifest paths before reading the referenced bytes: exact permitted roots/classes, relative-path syntax for source lists, no traversal, regular files, resolved paths equal to stated paths, and no duplicate source paths. The JSON source maps and SHA-256 listings agree exactly. Complete ordinary-file inventories, excluding documented Python/pytest cache artifacts, agree with the lists.

The inherited candidate has exactly 217 listed source files. RED contains all 217 unchanged and adds only `tests/test_crypto_failure_transport.py`, for 218. GREEN has the same 218-file inventory and differs from RED only in `src/cryptalis/crypto/keys.py`. The test copies are byte-identical. The real key-file difference is confined to `CryptoFailure.__reduce__`; it matches the packet's preserved before/after source. The inherited review is an exact copy of `reviewer-notes/cleanup-diagnostic-transport-20261014/review.md`.

All 29 packet-listed files match. The complete packet consists of those 29 files plus PACKET.sha256, exactly 30 regular files with no extra files, links, or nested entries. All 9 INPUTS pins, all 14 explicitly approved installed SQLAlchemy public-source pins, and both original-mailbox pins match. The original repository runner and both candidate runners are byte-identical at `118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12`.

## Contract and reducer review

The approved architecture (`docs/architecture/README.md:23-42`) makes internal transport and diagnostic helpers INTERNAL ONLY and does not admit public IPC. `docs/security.md:266-267,307-326` requires safe identity, retry/effect diagnostics, explicit unknown outcomes, and reporting existing effects when cleanup fails. `ENGINEERING_PLAYBOOK.md:34-50,54-81` requires preserving primary failures, meaningful deterministic tests, and positive sensitivity controls for negative privacy observations. `docs/decisions.md:7-21,30-43` admits no public transport platform. `docs/status.md:3-8` keeps all seven full gates UNKNOWN and ties verification to named checks and exact revisions.

In GREEN `src/cryptalis/crypto/keys.py:38-49`, the reducer preserves the existing return class, empty constructor argument tuple, and code/operation_id/args fields. It reads effects once. The conjunction accepts only an exact built-in str equal to the literal `unknown`, together with the singleton False for retryability. It then writes fixed primitive literals, rather than the inspected objects, into the two additional state fields. Exact type checking short-circuits before subclass/custom equality, and identity checking does not invoke retry-object equality or truth conversion.

No instance dictionary merge, coercion, repr, notes, cause, context, traceback, provider object, or arbitrary attribute is added. Other effect/retry combinations retain the original class-default restoration behavior. Fresh ProtectedSchemaMismatch and FileCustodyUnavailable effects are therefore preserved without replacing their class-specific classifications. The inherited async branch still sets the same unknown/False pair (`src/cryptalis/sqlalchemy.py:1074-1076`); its source and tests are unchanged.

The correction intentionally does not sanitize host-mutated code/operation_id/args, promise arbitrary subclass constructors or accessors, preserve arbitrary external classifications, or transport cleanup notes/full cleanup remedy. Reading an attribute on a custom subclass can invoke its accessor; the packet explicitly excludes arbitrary accessor contracts. This is a known narrow boundary, not an omitted general sandbox guarantee. Untrusted pickle remains inadmissible.

## Independent test analysis

The new test's literal expectations support a deterministic serialization property, rather than checking private layout or merely repeating the reducer's own computed result. All 17 cases are statically enumerated; no import or collection was used to count them.

| Cases | Count | Expected RED | Independent purpose |
|---|---:|---|---|
| Fresh KeyUnavailable | 1 | pass | Identity, exact safe class diagnostics and none/True defaults |
| Cleanup downgrade: key, backend, base | 3 | fail at line 72 | Literal unknown effects; key/backend also require False rather than their True class defaults; base isolates lost effects |
| Fresh schema and custody failures | 2 | pass | Preserve existing literal class-level effect classifications |
| Notes, cause, context, provider_data | 4 | fail at line 125 | Separate private carriers absent from bytes/render/state while unknown/False survives |
| Unrelated reduction/render sentinel | 1 | fail at line 154 | Preserve downgrade without touching arbitrary attached state |
| Six non-whitelist combinations | 6 | pass | Retain class defaults for True, integer zero, other effect, str subclass, opaque effect and opaque retry objects |

The privacy cases first establish marker sensitivity in serialized bytes and rendered output (`tests/test_crypto_failure_transport.py:98-104`), then establish that the individual original carrier is observable (line 117). They check no marker enters serialized bytes/restored rendering, no notes or unrelated state survive, and cause/context/traceback are absent. The unrelated sentinel raises on attempted reduction, comparison, truth conversion, or rendering. The str subclass raises on equality or reduction. Those controls would expose a generic state merge or relaxed whitelist.

The expected RED split follows independently from RED retaining only code/operation_id/args: all eight exact-downgrade cases reconstruct KeyUnavailable, CryptoBackendUnavailable, or CryptoFailure with effects `none`. They reach the quoted literal assertion; the private-data exclusion itself already holds in RED. The other nine cases intentionally exercise unchanged behavior. GREEN's two fixed fields should satisfy the eight regressions while leaving all nine controls intact.

Omitting effects should fail the eight regression cases. Omitting retryable should fail the retryable key/backend cases. A generic dictionary merge should fail notes/provider marker or sentinel checks. Removing exact-str/False identity admission should fail subclass/integer-zero controls. These are source-based sensitivity conclusions, not executed mutation results.

The test constructs local synthetic exceptions and protocol-5 byte strings. It does not exercise a real cleanup branch, create an engine or provider, use a database fixture, or prove cross-process transport. Real cleanup-branch evidence remains owned by the inherited async tests. No test-run result follows from this analysis.

## Command and custody review

The four blocks select RED SA2.1, RED SA2.0, GREEN SA2.1, then GREEN SA2.0, using explicit already-selected dependency-cell interpreter paths. Each block has exactly the same ordered 17 node IDs as NEW_NODE_IDS.txt. Static normalization proves that block bodies differ only by the intended candidate, color/source manifest, evidence path, and dependency-cell substitutions.

Each block requires a fresh evidence path; checks INPUTS, native source pins, original mailbox, packet contents, selected source hashes, and selected ordinary-file inventory before the wrapper; records wrapper exit; repeats its checksum checks afterward; then exits and requires independent audit. There is no direct pytest, marker injection, environment/credential substitution, install, retry, database repair, or candidate-source switch in the proposed commands. The original packet file is a collection of four blocks, so it must not be executed wholesale.

The pinned corpus-v2 wrapper is `candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py` at `e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453`:

- Lines 35-40 require the permitted candidate location and exact unchanged repository runner.
- Lines 55-62 create new evidence and take an exclusive, nonblocking lab lock before database action.
- Lines 70-89 impose 600 seconds on the tests and 90 seconds on other subprocess steps; timeout is recorded as 124, not a pass.
- Lines 94-110 start the existing lab, require readiness, and verify package source origin before tests.
- Lines 112-154 retain source snapshots and reject changed source.
- Lines 156-165 attempt final server stop, then corpus capture/restoration, and release the lock.

The unchanged runner reloads both credential files internally, probes both roles, and stops on probe failure (`scripts/test_postgres.py:24-44,71-95`). The test admission marker is generated in-process only after these checks. The unchanged conftest rejects direct pytest without that marker. No credential bytes were inspected by this review.

The pinned corpus helper archives changed artifacts before replacement, preserves originals, checks restoration and inventory, and raises on errors (`corpus_artifacts_v2.py:52-107`). Source inspection does not prove its future restoration outcome.

Mandatory inherited audit limits:

1. A wrapper return status does not incorporate the postgres-stop subprocess result. The separate terminal server-stop audit is essential even if tests and wrapper otherwise succeed.
2. A source-only unit selection still starts the existing lab and invokes its custody protocol. The plan correctly preserves this boundary.
3. The 600-second limit is for the tests subprocess, not a proof of universal descendant termination or total-session deadline. Audit terminal process/server state; do not infer it from a timeout label.
4. Coordinator review still owns actual interpreter/dependency identity and prior-session terminal admission. This review verified approved dependency-source pins but did not start or hash interpreter binaries or inspect runtime secret roots.

## Single-block capture driver

Reviewed `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/run-transport-reviewed-block.py` at `877a8691e87ace5771c4e9d3994b645bc62d736de8b265456fc71da107e359ab`.

The static diff from `run-async-exit-reviewed-block.py` changes only the packet path, phase/cell case, packet anchor, command filename, and evidence prefix. It chooses exactly one complete BEGIN/END block. The truncated END comment suffix is non-executable text only; the closing subshell is retained. It copies the complete frozen packet, exact command and driver, verifies packet copy equality plus packet/input hashes before and after, captures outer output/status, and records the wrapper exit if present. There is no phase loop or automatic advancement.

The driver's exit code alone is not the selected phase's result: the inherited driver records outer_exit/wrapper_exit but does not itself exit with the outer code. A failed assertion can also prevent the final coordinator-status.json from being written. Audit the recorded outcomes and missing records explicitly; never label driver exit zero or missing status a test pass. These are inherited, visible evidence limits and do not require changing the frozen driver for this bounded plan.

## Review method and remaining boundaries

Only source/document reads, metadata/path validation, shell text processing, byte comparison and SHA-256 verification were performed. No Python process, candidate import, test collection, tests, database access, network access, package installation, Git command, commit, or remote action was run. No raw phase JSON, credential files, secret-bearing environment files/variables, or new runtime roots were read, hashed, or copied. Writes were confined to this reviewer-owned directory.

Source-only evidence does not qualify application retry behavior, physical rollback, pool quarantine, provider custody, public IPC, multiprocessing methods, cross-version pickle, installed wheels, release artifacts, or production. G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE remain UNKNOWN.

The adjacent verification logs and empty inventory/map diffs record this review's checks. The review applies only to the pinned bytes; material source or command changes require renewed review.
