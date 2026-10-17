# Isolated forward-ABORTED v3 pure component, V1

Status: **SOURCE PROTOTYPE ONLY; UNEXECUTED; NOT ADMITTED FOR PRODUCT OR NATIVE USE.** Frozen doctor source, selected artifacts and all old journals are unchanged. No test/import/build/DB command was run. This directory is a separate copy of the new component, not a patched candidate tree.

## Root engineering selection

Root's 2026-10-16 selection, retained verbatim:

> Root selects recommended D1–D3 ONLY for an isolated opt-in experimental v3 source prototype, not public/default promotion: exactpaired predecessor inputs/scopeprojection/commitment from DECISION; newv3-only16MiB canonical+native transfer/reservation with exactN boundedcounters and separately reviewed decodergrammar; strict no-repair physicaljournaladmission and documentedlockorder. Existing v0/v1/v2/abort/read/recovery behavior and alloldrows untouched. Historicaloversize remains typed readonlyrefusal in this prototype, not a discarded finalrequirement. No DB/ACL/grants/newroles or execution authority. Start smallest source slice: pure v3 constructor/scope/ancestry validation + immutable oldformat regressionproposal, separatecopy; do notimplement journalmutation/nativevalidator until purecontract review. No historicalartifact field mutation or generic plannerbypass. Record rootselection and unresolved nativecatalog/locking/completev3endtoend gates. User broadly authorized design/implementation; these were rootengineering choices, not credential/fixtureapproval.

This selects the recommendations in `experiments/forward-aborted-successor-contract-gate-v1-20261016/DECISION.md` (SHA256 `1a3056a45220694ce9c5713e042a7e80868eda856e51b82f684bce9f875a548c`) for isolated engineering. It does not supply host authentication, a current pin, native fixture authority or execution permission.

## Implemented source surface

Only `successor_contract.py` is executable source. It has no entry point, I/O, product import, DB adapter, subprocess, automatic dispatch or authority result.

- `bind_predecessor`: both-or-neither explicit predecessor artifact bytes and pin; exact canonical bytes bind the supplied decoded view; exact PREPARED target/operation/digest equality. It checks equality, not authenticity/currency. The pin is a plain JSON view for this isolated component, not a replacement public DeploymentPin type.
- `scope_bytes` / `require_same_scope`: exact D1 array projection and canonical-byte equality, preserving array order and distinguishing bool/int. Full lock members are closed; only schema/profile/domain/database/declaration/models/required_readers enter S. Tenant universe and fingerprint map compare separately and exactly. Refreshable host observations, derived ddl, costs/scopes/comments/designation and operation ID are not part of S.
- `validate_summary`: exact new forward component member sets, v0/v1/v2 root names, canonical nonzero UUIDs, lowercase digests, count 1..2**53-1 with no smaller attempt limit. Count limits apply only to the artifact lineage count.
- `construct_lineage`: constructs the new **aborted_forward component only**, from a distinct proposed identity and a supplied terminal head. First root has no added lineage field; a v3 predecessor must carry exactly its authenticated artifact prefix. Whole terminal state enters T; domain-separated seed/fold match the selected design. Historical artifact/row objects are never edited. Count exhaustion refuses without pruning.
- `verify_lineage`: checks newest-to-oldest prefix/count/root/reference/commitment consistency, all terminal phases, new identity exclusion, missing/extra supplied rows. It consumes one supplied row at a time, allocates no history-wide ID set/list and makes no full-row query. Returned data is a detached summary, never authority.

Full forward/reverse v3 artifact constructors, comments/designation dispatch and reverse-set construction are intentionally not connected. The exact reverse-v3 format name is reserved in the module; no reverse behavior is implemented.

## Required interpretation of this partial checker

Inputs must be inert decoded values for the pure slice. There is **no journal byte decoder** and no argument that the artifact decoder's 16-digit/<2**53 grammar is suitable for journal counters. Canonical encoding uses existing C options and the 32-container-depth convention. It has no journal integer-range cutoff. Interpreter huge-integer conversion refusal remains typed; arbitrary huge-integer portability is not qualified. Measured floats are admitted only at the two existing artifact estimate-rate paths, never in terminal-state hashing.

The canonical 16 MiB check occurs after encoding already-decoded data. It is not a preallocation, driver-transfer, native jsonb::text, or peak-memory proof. Historical over-budget state gets `successor_canonical_size_exceeded` in this new component only. No existing abort/save/read function gains this condition. New v3 expansion reservation, native size observation and exact `0 <= chunks <= rows <= N` enforcement are not implemented. Those are still prerequisites, not replaced by a per-save size check.

Terminal checking here closes only the forward top-level state keys, requires ABORTED and a nonempty models object, rejects reverse source/layout members, and binds every nested member by the full-state hash. **Nested model/schema/guard/progress semantics are not validated.** Hash agreement cannot establish their validity. No malformed state is thereby admitted for execution.

The iterator must represent one stable unique-key snapshot. Decreasing prefix counts avoid a history-wide visited set only under that premise. A fabricated iterator may supply conflicting versions of the same UUID; this pure checker does not prove PK uniqueness or snapshot stability. Likewise the supplied journal count is only a cross-check, not proof of complete native membership. Physical journal admission, native count and point reads under one approved snapshot/lock must establish those premises before integration. Do not plug a live DB generator into this source packet.

## Still-held engineering gates

1. Independent pure-source review and separately selected finite tests with independent vectors. This packet has no run receipt.
2. Exact closed journal decoder grammar for each admitted producer and v3, native raw-byte/type preflight, complete nested terminal validation, and new-v3-only expansion envelope/reservation with exact N. Historical oversized recovery remains a broader final requirement; this first route refuses read-only.
3. Reuse the existing compiler and comment/designation validators without relabeling an old artifact. Full constructors must inherit all v2 validators and reverse-envelope accounting; no generic parser/planner bypass. Genuine v0/v1 producer compatibility/provenance is not established by synthetic format strings.
4. Strict current physical journal/owner/ACL/dependency admission without repair. Native catalog classification is unimplemented. Proposed mutation lock order remains existing ordered-table advisory identity, sorted transition-table locks, then journal SHARE ROW EXCLUSIVE; consistency, insertion exclusion and deadlock behavior require separate proof. No native validator or journal mutation is present.
5. Fresh external PREPARED authority, late current metadata/current-role checks, atomic expansion and old-row preservation, repeated abort/resume, reverse-set partition and full reverse/removal still require implementation and deciding evidence. No privileges, new credentials/cluster, publication or plaintext switch is selected.

`TEST_PROPOSAL.md` gives the next finite source questions plus immutable-old-format regressions. `INPUTS.sha256` pins the exact finite old sources/design inputs; `PACKET.sha256` seals this packet. Neither map attests live state, a full source tree or supply-chain provenance.
