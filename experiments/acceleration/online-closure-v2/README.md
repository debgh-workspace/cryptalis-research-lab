# Online closure V2: completed source-preparation packet

Date: 2026-10-14 UTC.

Status: **DOCUMENTARY PREPARATION COMPLETE; NOT IMPORTED, NOT COMPILED, NOT RUN.** This handoff identifies the existing V2 bytes and accounts for inherited routes. It does not implement durable online closure, establish a reproduced V1 write bypass, record a passing source test, or authorize execution or publication. Packet promotion remains on HOLD pending coordinator disposition and review of these new packet documents. All seven qualification gates remain UNKNOWN.

## 1. What is complete, and what remains incomplete

Complete in this packet:

- A current 201-file candidate manifest and a SHA256 source list, with exact V1 and D5-base deltas.
- An input manifest for 31 retained documents/receipts, including both independent reviews.
- The complete 14-method inherited API inventory, plus the presealed worker and barrier paths.
- A current disposition, a data-only preparation receipt, an explicit prospective publication allowlist, and a packet manifest.
- The existing eight-method structural check file and three original V1 snapshots remain byte-identical to their starting V2 copies.

Still incomplete: independent acceptance of this newly assembled documentary packet; permission to execute the source checks; the closer, durable native/runtime guard, phase transition, controlled paused finisher, and all runtime evidence. Capture/handoff, guard/runtime-role mapping, rotation/provider and wider qualification approvals remain pending. No runtime or gate status advanced.

The independent V2 review examined the earlier four-file packet and correctly recorded it as incomplete. That review and its RESULT.json are preserved as dated input evidence. This assembly addresses the missing documentation; it does not rewrite the review, convert its HOLD into acceptance, or claim that the reviewer approved these new documents.

## 2. Exact candidate and source ancestry

Current candidate: `candidate-online-closure-v2-20261014`.
Immediate predecessor: `candidate-online-closure-20261014` (V1).
D5 base: `candidate-accel-online-cf1-convergence-20261013`.

Paths in candidate manifests and SOURCE_SHA256SUMS.txt are relative to the named candidate. Paths in INPUTS.json and PUBLICATION_ALLOWLIST.json are relative to the `cryptalis-executable` lab root. Packet-manifest paths are relative to this experiment directory.

The current candidate has exactly the same 201 regular-file paths as V1, with no symlinks. Exactly one candidate file changed from V1; 200 are unchanged. Relative to the D5 base, exactly two helper files changed; 199 are unchanged. No product source, inherited capture, independent decoder, historical source test, source manifest, or contract changed.

- `tests/_online_cf1_process_lab.py`: V1 SHA256 `7da3cb40df90ef12541771c6dc576cb0512f0d88a97e789abb400c0f863c4aee`; V2 SHA256 `2845f4dcc0663b29cf0a502ab687b12fc4ceeca3cffdfbc04b3eb7c236d7ec4c`.
- `tests/_online_cf1_lab.py` is unchanged from V1: `319b16fa2c936f1be85bd8f12466af3212cc36417601cf51b95b712ec597e202`.
- The existing V2 source-check file remains `f64548836f1534c38bc15e6cf34c761468875d098627a8952fa41ecda45e77e4`.

SOURCE_DELTA.patch records V1-to-V2 candidate changes. TEST_DELTA.patch records V1-to-V2 source-check changes. BASE_TO_V2_SOURCE_DELTA.patch records the complete two-helper difference from D5. Their labels distinguish each source; no patch was applied during this assembly.

CANDIDATE_MANIFEST.json is the current candidate identity. Inherited D3/D4/D5 manifests and V1_MANIFEST_SNAPSHOT.json identify earlier source. Their earlier hashes and any historical VERIFIED labels must not be treated as V2 runtime evidence.

## 3. Precise correction and inherited API boundary

V2 adds `FixtureRouteUnsupported(ValueError)` and explicit `ChildFrameLab.install`, `drain`, and `finish` overrides. Source inspection shows that each method's only executable statement raises that exception with a fixed message. The refusal precedes any SQL, transaction call, inventory read, dirty-token lock, staging write or token retirement. This is a source-control-flow observation; it is not an executed refusal result.

The V1 objection concerned ordinary inherited method dispatch, not just an explicit base-class call. Successful V1 inherited staging was never established: its plaintext ON CONFLICT SQL names `v`, while the CF1 fixture uses `frame`. The original reviewer corrected an earlier provisional NULL/tombstone-success interpretation. Preserve that correction; do not describe V2 as repairing a demonstrated successful write bypass or reproduced PostgreSQL race.

V2 does not rename that inherited SQL or admit ordinary workers in PAUSED. The existing `install_presealed` path is unchanged and takes the shared locked pin/phase admission before dirty/stage effects. The spawned worker still calls it inside its acknowledged outer transaction.

INHERITED_ROUTE_INVENTORY.md accounts for all 14 methods defined by EnumerationLab and distinguishes admitted preparation, immediate refusal, inspection/session setup, owner setup/teardown, and native/source writes. Explicit base-class calls, arbitrary owner SQL, monkey-patching and unsupported setup reuse remain outside the cooperative protocol. They are exclusions, not newly secured routes.

## 4. Worker admission and lock reasoning

The inherited V1 correction still selects operation identity, exact pin and phase together. Locked admission uses FOR SHARE and requires PREPARING. The separate preparation_worker_barrier uses FOR NO KEY UPDATE, validates the same pin/PREPARING state, and yields inside a transaction. Its lock lifetime follows the enclosing transaction, including an outer transaction. It writes no phase, locks no source table, installs no persistent guard and returns no closure certificate.

The proposal records PostgreSQL commit `d15ab66f500cc70b7dcc9ffdf3843b7013163d37` and RI-source blob `6945d99b3d5f2ca7dc4f2e1d6daf745d2585656b`. Retained proposal/source-record bytes were hashed here. No upstream fetch or installed-server attestation occurred. SHARE versus NO KEY UPDATE and capture FK KEY SHARE remain the retained source-derived lock argument, not new schedule evidence. Other row, data and table contention remains relevant.

## 5. Mandatory full closure, still approval-blocked

The final objective remains mandatory and unimplemented:

1. Drain admitted preparation workers and deterministically exclude source writers.
2. Establish fresh post-barrier visibility and atomically install/verify the durable native/runtime writer guard with PAUSED.
3. Refuse reconnecting preparation while valid dirty tokens remain.
4. Use a distinct byte-bounded paused finisher and fully compare current membership, value, NULL, context and tombstone state.
5. Record PAUSED_VERIFIED only after full verification, retaining the guard. Failed final work must remain paused and unpublished.

Publication/switch, deployment-wide writer ownership, owner/DDL exclusion, provider lifetime and rotation remain separate obligations. Existing owner-only fixture connections do not prove nonowner runtime reconnection coverage. No credentials, role grants, fresh cluster, trigger authority or provider action is inferred.

Pending capture/handoff request: `Sentinel_f9407ee631c081d1a92fb471b6262b6f`. Its resolution, exact guard reuse/installation boundary, approved source-writer coverage, runtime-role mapping, admitted phase/finisher contract and unchanged full-scan/publication obligations are still required.

The retained proposal's eight future native groups remain: row-lock compatibility; pending native writer; stale normal/presealed workers with valid tokens; already-admitted worker commit/rollback; runtime reconnection; handoff rollback atomicity; paused restart/complete bounded drain; and failure after durable pause. Exact schedules and instances must be frozen only after the missing implementation and authority exist. No rerun of D5 empty snapshots supplies closure evidence.

## 6. Prepared checks and evidence limits

The existing file contains eight structural test methods: the six V1 checks, plus immediate refusal for three child routes and classification of all 14 base APIs. The six admitted producer/installer cases remain enumerated. The new source test also requires five preparation methods to be defined on ChildFrameLab and checks CF1's inherited self-dispatch.

These methods were read as text, not imported, compiled, AST-parsed or executed during this assembly. No pytest collection occurred. Their future string/AST assertions cover selected source shapes; they cannot establish arbitrary dynamic control flow, database effects, phase transitions, lock waits, transaction completion, valid-token refusal, capture/FK interaction, reconnect behavior, rollback atomicity, provider lifetime, deadlock freedom or races. No PASS count is claimed.

No candidate, installed environment, database, role, trigger, provider, Git, remote, checklist or retained evidence was changed. Only new documentary files in this experiment directory were written. The original failures, earlier HOLD decisions and retained receipts remain unchanged.

## 7. Preservation, publication and receipt

PREPARATION_RECEIPT.json records data-only identity checks, scope and the read-only listing incident. All 201 V1 source entries, all 201 D5-base entries, all six V1 packet entries and all ten V1 input entries still match: 418 retained comparisons with zero mismatch. The three retained V1 snapshots match their V1 originals. These are byte-integrity results, not passing source/runtime tests.

PUBLICATION_ALLOWLIST.json is a closed prospective file list for a later separately authorized sharing decision. It grants no publication authority. It excludes secrets, connection URL files, credentials, tokens, raw phase/trace JSON, database snapshots, logs, caches and unlisted paths. Input hash references do not make referenced files publication-eligible. Never publish a directory recursively or infer permission from a manifest.

PACKET_MANIFEST.json hashes every other file in this packet and explicitly excludes itself to avoid a self-hash cycle. Its own digest is returned in the final handoff. A later change requires a new review and refreshed packet identity; do not silently edit the retained snapshots or erase earlier failed evidence.

## 8. Qualification

G-ADAPTER: UNKNOWN. G-CRYPTO: UNKNOWN. G-QUERY: UNKNOWN. G-LIFECYCLE: UNKNOWN. G-PROVIDER: UNKNOWN. G-POLICY: UNKNOWN. G-RELEASE: UNKNOWN.

