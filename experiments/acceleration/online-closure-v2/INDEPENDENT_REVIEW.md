# Final independent acceptance: online-closure V2 source packet

Date: 2026-10-14 UTC. Decision: **CLEAR_SOURCE_ONLY**.

The completed documentary packet is accepted at the exact identity below. The prior missing-packet objection is resolved. The three unsupported inherited ChildFrameLab preparation routes refuse before SQL in the inspected source. This is neither runtime closure verification nor permission to promote, publish, install capture/guards, rotate keys, create credentials/clusters, or contact a live provider. All seven qualification gates remain **UNKNOWN**.

## 1. Frozen identity and preservation

Reviewed packet: `experiments/online-closure-v2-20261014`.

- PACKET_MANIFEST.json SHA256: `33b87cb277e5ab3c20dc05282435465b5acbf4423ed5395f247c4122f1332971`.
- CANDIDATE_MANIFEST.json SHA256: `aecabfaa1ac0413be8fd4b998b91f80d19589bca15b97278acef27adf3b593e2`.
- Packet SOURCE_SHA256SUMS.txt SHA256: `8468baf50bbec2882cfeef8aeef9faa81f6e0c376bf54bf6ca6b4260d24fad86`.
- Standalone source-check SHA256: `f64548836f1534c38bc15e6cf34c761468875d098627a8952fa41ecda45e77e4`.

The packet has exactly 15 regular files and no symlinks or special files. Its manifest identifies exactly the other 14 files; the externally supplied manifest digest closes the deliberate self-hash exclusion. The 11 new documents complete the four-file packet reviewed earlier. All four original files match both the preparation receipt and the earlier independent four-file hash record. All three retained V1 snapshots are byte-identical to their V1 originals.

Data-only checks matched 668 explicit hash comparisons: 201 V2 source entries, 201 V1 entries, 201 D5-base entries, 14 V2 packet members, six V1 packet members, 31 current input entries, ten V1 input entries, and four original V2 files. Every listed byte length also matched. The retained V1/D5/packet/input subset is exactly 418 comparisons. These counts are integrity checks, not tests or independent evidence that historical runtime receipts are true.

V2 contains exactly the same 201 source paths as V1, without symlinks. Its source hashes agree with the earlier independent V2 snapshot. Only `tests/_online_cf1_process_lab.py` differs from V1; 200 files are identical. Relative to the pinned D5 source set, only that file and `tests/_online_cf1_lab.py` differ; 199 files are identical. Product source, capture, independent decoder, inherited tests/manifests and contracts remain unchanged.

SOURCE_DELTA.patch, BASE_TO_V2_SOURCE_DELTA.patch and TEST_DELTA.patch independently reconstruct their named destination bytes exactly when interpreted as data in memory. No patch was applied. An initial comparison to Python difflib's preferred serialization differed because the two source patches use different valid hunk alignment. SOURCE_SHA256SUMS.txt has one harmless final blank line; its 201 nonblank entries exactly match the candidate manifest, without duplicates. `DATA_CHECKS.json` retains those initial strict-text comparison observations; `FORMAT_RECONCILIATION.json` resolves each one. There is no unresolved content mismatch.

## 2. Source correction and all 14 inherited routes

The route inventory accurately covers the complete EnumerationLab method set in the reviewed source:

| Methods | Verified source disposition |
|---|---|
| `seed`, `page` | CF1 and Child explicitly override both. Each opens a transaction and calls shared locked pin/PREPARING admission before inherited production. Base page dispatches seed through `self`. |
| `install` | CF1 performs shared locked admission before dirty-token locking and atomic stage/retirement effects. Child immediately raises its typed unsupported-route exception. |
| `drain`, `finish` | Child immediately refuses. CF1 inherits composition through admitted `self.install` and `self.page`. Initial queue/inventory reads do not authorize writes; historical finish is not durable closure. |
| `connect`, `reconstruct`, `claim`, `oracle`, `snapshot` | Session setup or inspection. `connect` executes session SET/SHOW statements, so “read-only” is not a claim of zero SQL. Reconstruction checks durable identity and pin without admitting writes. Child's inherited plaintext oracle is incompatible with CF1 staged shape and is not the terminal verifier. |
| `__init__`, `close`, `install_capture` | Owner-controlled creation, destruction or initial capture setup, outside concurrent worker admission. Their classification grants no authority to invoke them. |
| `write` | Native/source mutation intentionally remains outside the worker barrier. Unchanged capture is not a durable source-writer guard. |

At `_online_cf1_process_lab.py:36-37`, FixtureRouteUnsupported derives from ValueError. At lines 63-73, each Child install/drain/finish method has one executable statement: a raise of that exception with a fixed message. No SQL, transaction call, inventory read, dirty lock, stage write or retirement occurs first in those method bodies. Ordinary method dispatch reaches these overrides. This resolves the precise earlier source objection.

Successful V1 inherited staging was **never established**. Its inherited plaintext ON CONFLICT SQL refers to `v`, while CF1 setup renames that column to `frame`. The packet correctly retains the original reviewer's correction of a provisional NULL/tombstone-success interpretation. No reproduced V1 write bypass, successful unauthorized transition, or race is claimed.

Child's unchanged `install_presealed` checks operation/frame shape, then takes the aliased locked admission before dirty/stage effects. The unchanged spawned worker invokes it inside the acknowledged outer transaction. The acknowledgement after commit follows that outer transaction's return. CF1's barrier and Child's presealed route are separately inventoried. Explicit base calls, arbitrary owner SQL, monkey-patching and unsupported setup reuse remain outside this cooperative boundary, rather than silently becoming secured routes.

## 3. Pin/phase and closure precision

The common helper selects operation identity, exact pin and phase together. Locked admission uses FOR SHARE and requires PREPARING. The barrier uses FOR NO KEY UPDATE, checks the same pin/PREPARING state and yields inside a transaction. Its lock lifetime follows the enclosing transaction, including an outer transaction. It performs no phase change, source-table exclusion, guard installation or terminal certification.

The retained PostgreSQL reference is commit `d15ab66f500cc70b7dcc9ffdf3843b7013163d37`; its recorded RI-source blob is `6945d99b3d5f2ca7dc4f2e1d6daf745d2585656b`. This review verified retained source-record bytes, not upstream bytes or an installed PostgreSQL binary. The recorded row-lock/FK reasoning remains a hypothesis for native schedule testing, not new runtime evidence.

Full closure remains unimplemented: drain admitted workers; deterministically exclude source writers; establish fresh post-barrier visibility; atomically install/verify the durable native/runtime guard with PAUSED; refuse reconnecting preparation while valid dirty tokens remain; run a distinct byte-bounded paused finisher; fully verify current membership, value, NULL, context and tombstone state; then record PAUSED_VERIFIED while retaining the guard. Failure must remain paused and unpublished. Publication/switch and deployment-wide writer/owner/DDL coverage remain separate obligations. D5 empty snapshots or owner-only fixture connections cannot establish them.

The packet clearly separates current V2 identity from inherited D3/D4/D5 manifests, retained V1 wording and earlier execution receipts. Prior HOLD reports remain preserved. Its assembly-time NOT_YET_OBTAINED/PENDING acceptance fields describe the state before this review; this new review supplies the bounded subsequent decision without rewriting those historical files.

## 4. Standalone source-check execution boundary

The complete standalone check file was read, not executed or AST-parsed by this reviewer. It contains eight unittest test methods. Its only imports are `ast`, `pathlib.Path` and `unittest`. It reads explicit candidate/base source paths, uses AST/string inspection and compares selected bytes. It does not import the fixture, load a provider, invoke subprocesses, contact PostgreSQL or use pytest/conftest collection.

The six original structural checks remain, with two added checks for immediate child refusal and the complete base-method inventory. Those assertions cover selected AST shapes; they do not prove arbitrary dynamic control flow, future subclass APIs, database effects, lock waiting, transaction completion, FK interaction, reconnecting writers, rollback atomicity, key/provider lifetime, deadlock freedom or closure.

The coordinator clarified that the owner already authorized engineering/testing in the existing isolated lab. Packet wording about “permission to execute” means coordinator sequencing/protocol clearance here; it does **not** create a new owner-permission blocker for this bounded standalone source check. This source review clears that boundary. This reviewer has run none of the eight tests and claims no test pass count.

From the `cryptalis-executable` lab root, the exact standalone command is:

```sh
python -I -S -B experiments/online-closure-v2-20261014/test_online_closure_source.py
```

Use the same existing standard-library interpreter already admitted for data-only work. Preserve its exact invocation, first outcome, stdout/stderr and exit status in a fresh evidence directory outside the candidate and packet. Do not substitute pytest or import candidate modules. Stop and preserve any failure; do not retry until it passes.

Before and after that execution, verify all 201 source files and all 15 packet files with the reviewed lists:

```sh
(cd candidate-online-closure-v2-20261014 && sha256sum --check ../reviewer-notes/online-closure-v2-final-independent-20261014/REVIEWED_SOURCE_SHA256SUMS.txt)
(cd experiments/online-closure-v2-20261014 && sha256sum --check ../../reviewer-notes/online-closure-v2-final-independent-20261014/REVIEWED_PACKET_SHA256SUMS.txt)
```

The source-list digest is `2a9d40a6066784b52154677826f78376e30c02daf4c19636de8b80632da4e738`; the packet-list digest is `d26f95849ba8f526e958fbc6ff2bf90692430ef252fc6019a3851f1809cb65ab`. Pin these lists and the packet-manifest/test digests above. A source-check pass, if later observed, is only a structural-check result on those bytes.

## 5. Publication allowlist

PUBLICATION_ALLOWLIST.json contains exactly 23 unique explicit relative regular-file paths: six selected source/contract files, all 15 packet files and the two earlier reviews. Every path is free of glob/traversal syntax and symlink ancestors. Each has an identity binding through the candidate, packet or input manifest, except the packet manifest itself, whose external digest is recorded above.

The allowlist is prospective, explicitly unauthorized and closed. Input references do not expand it. Raw phase/trace JSON, credentials, private URLs, database/queue snapshots, unrestricted logs, caches, archives, Git metadata, symlinks and other unlisted paths are excluded. Documentary JSON is included by exact path only. This is structural acceptance of an eligibility list, not an attestation that every future disclosure is appropriate: recheck bytes, recipient/access scope and required sharing permission before any publication. This new review directory is not automatically added to that allowlist.

## 6. Remaining decisions and permitted continuation

Permissible next work within existing authority is the bounded standalone source check described above, followed by retaining and reviewing its actual result. Source-only design/review may continue within the assigned engineering scope. No fresh owner permission is invented for such static work.

Durable closure remains substantively blocked on missing implementation and the exact capture/handoff, guard/runtime-role and phase/finisher contracts. The packet retains pending capture/handoff request `Sentinel_f9407ee631c081d1a92fb471b6262b6f`. Any new cluster, credentials/access, live-provider action, capture installation/change, guard installation/change or rotation must follow its applicable specific approval boundary. This review cannot resolve those decisions. After their resolution, the coordinator can freeze a separately reviewed implementation/native-evidence packet; it must not infer runtime permission or qualification from this acceptance.

The retained eight future native groups remain planning material: row-lock compatibility; pending native writer; stale normal/presealed workers with valid tokens; already-admitted worker commit/rollback; runtime reconnection; handoff rollback atomicity; paused restart/complete bounded drain; and failure after durable pause. Exact schedules require the actual implementation and applicable authority. Maintenance fallback, full final verification and separate publication remain mandatory.

G-ADAPTER, G-CRYPTO, G-QUERY, G-LIFECYCLE, G-PROVIDER, G-POLICY and G-RELEASE remain UNKNOWN.

## 7. Review procedure

This reviewer used filesystem text reads, file enumeration, standard-library data parsing/hashing and in-memory diff interpretation only. No repository module import, source compilation/AST parse, test, pytest collection, database/role/trigger/provider operation, credential read, network/upstream request, Git command or authoritative-checklist edit occurred. No prohibited raw phase/trace JSON was opened. The isolated candidate lacks Git metadata; the prior authorized filesystem-only review and current assigned source-only scope were used without repeating the known failing Git command. No candidate graph data exists.

Writes are confined to this new reviewer directory. Packet and candidate bytes were preserved. This is independent AI source review, not the separate human cryptographic/security qualification required for release.
