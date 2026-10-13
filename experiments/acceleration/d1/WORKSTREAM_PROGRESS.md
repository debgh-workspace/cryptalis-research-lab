# Online enumeration coordination prerequisite

Updated 2026-10-13 13:54 UTC. Coordinator alone executes PostgreSQL and publishes.

## Authority and base

Parent approved this finite synthetic experiment after the read-only proposal.
All 183 files copied from candidate-ciphertext-doctor-20261013 are byte-identical.
Sorted `relative_path:sha256\n` base manifest SHA256:
0dced382416e084ddd5ee9e145981cd29eabb77e0f3d55db4ae0890e7e0b8695.
No product runtime, API, phase, compiler trigger admission, role or credential
changes. B1 and B2 candidates remain frozen and unchanged. No database was
started or contacted by this worker. All seven production gates remain UNKNOWN.

## CP65 provenance and reuse

The following current archived files exactly match both before/after hashes in
`../evidence/cp65-restored-all-sa20/external-source-stability.json`; its unchanged
receipt records 23 PASS in 3.17 seconds. These files remain unchanged; the
coordinator can select them once as a baseline if needed. No historical file is
rewritten and the new slice does not require repetition of that known result.

- test_online_retirement_protocol.py:
  e108aea9bc18dd7448edcd9f17491d9b42b56ffa352158a9a759d9683a008b1d
- test_online_initial_inventory.py:
  7280f0df41114bd48048359017b8ce1d6807a4c446ac122aefef95a83ddff0a7
- test_online_inventory_version_alternative.py:
  2da9e453f6a75725a3bedd49cbf96952bc7606887683f7e41a90f184be93d63d

`../checkpoints/CP65-online-initial-inventory.md` explicitly leaves concurrent
initial enumeration coverage and operation identity unresolved. Its fixture
inserts source rows after capture installation and seeds one chosen identity.
This slice starts with native rows before capture and runs actual bounded
keyset pages, rather than repeating only the delayed-seed schedule.

## Owned experiment and fixed acceptance matrix

New files: tests/_online_enumeration_lab.py (owned disposable-schema harness)
and tests/test_online_enumeration_handoff.py (31 scheduled cases after review).

- Seven writes after a page read, before seed/cursor commit: insert behind,
  between selected keys, ahead; update to/from NULL; delete; delete/reinsert.
- Six inserts after empty-page observation: behind/ahead of a completed
  cursor, and into an initially empty table; each before and after durable
  completion commits.
- Two page failures before/after cursor update: work and cursor roll back
  together; a reconstructed object and fresh connection repeat the original
  page and complete from durable state.
- Empty-page completion rollback does not report durable completion.
- Reconstruction after a failed later page preserves the committed cursor and
  previously staged prefix. A wrong expected operation refuses without effects.
- A claim from another operation with the exact same key and numeric token
  refuses with no source, native, stage, cursor or work mutation.
- A page seed delayed until newer work is retired cannot revive an old claim.
- Worker stage/retirement failure and writer rollback each preserve atomicity.
- An empty queue with incomplete inventory cannot pass the oracle.
- Four full-comparison negative controls: missing/stale/NULL-substituted/extra
  stage rows all fail, despite complete inventory and empty dirty membership.
- Identity movement refuses before source or coordination effects.
- Capture installation waits for an earlier writer; known lock-timeout rollback
  leaves no operation metadata. Later retry inventories its committed value.
- A READ COMMITTED transaction started before installation captures its later
  source write through the installed trigger.
- A controlled before/after-trigger pause exercises token allocation order
  differing from commit order. Capture must replace the obligation, even when
  its allocated token is numerically older than an intervening inventory token.
  Only inventory publication uses GREATEST, matching CP65. Sequence magnitude
  is not source freshness. No executed failure is claimed before coordinator run.

One immutable bigint key domain and one durable cursor; fresh operation-scoped,
noncycling sequence tokens; exact operation/key/token claims; atomic synthetic
stage and work retirement. The capture-install lock is a fixture metadata
boundary, not a downtime measurement. The scheduling trigger in one test is a
controlled pause only, not admission of user triggers.

After scheduled writers stop, require durable inventory completion, an empty
queue, and complete ordered equality of native twin, current source and live
stage rows including NULL. A separate PostgreSQL backend uses a read-only
repeatable-read transaction for this final comparison. No hash/count/sample
replaces that final comparison.
Synthetic side-table values are not CF1 frames or the proposed same-row VDRC
product representation. This is neither a complete online engine nor proof of
arbitrary schedules, tenant semantics, failover/restore, lost replies, runtime
permissions, external publication or retained-reader custody.

## Static evidence and coordinator gate

Python syntax compilation PASS for both new files. Static AST accounting finds
31 cases. A corrected absolute-path comparison confirms all 183 S14 files remain
byte-identical, and all three CP65 source hashes still match the values above.
The first comparison script used a relative parent incorrectly; its path lookup
failed after syntax/count output and established no baseline comparison.
No pytest/DB run performed by either worker. Original source/preflight bytes
remain unchanged.

Proposed unchanged-wrapper selection (coordinator only):

    python toolchain/lab_session.py \
      --candidate-root candidate-accel-online-enumeration-20261013 \
      --evidence evidence/b3-online-enumeration-initial-20261013 -- \
      -q tests/test_online_enumeration_handoff.py --tb=short -ra

Expected static count: 31 new cases. If one combined provenance baseline is
needed, append the three unchanged `../experiments/test_online_*.py` files named
above: retirement_protocol, initial_inventory, and inventory_version_alternative.
That explicit combined selection contains 54 cases; do not use a wildcard that
also selects unrelated online experiments.
The coordinator supplies the existing admitted interpreter path and serial lab
ownership. A failing probe stops the run; no substitute database or test route.

High-value omission candidates after the first correct run: discard capture for
an insert behind the cursor; split page work from cursor transaction; omit the
operation binding; preserve a higher inventory token instead of replacing it on
source capture. These require separate frozen copies and explicit coordinator
scheduling; none was executed or applied to the main candidate here.

## Worker D review and freeze

The coordinator transferred exclusive ownership from B to D at 13:51 UTC.
D reviewed the capture ordering, cursor transaction, claim namespace and full
comparison. The review retained capture's unconditional EXCLUDED.token update;
only initial inventory uses GREATEST. It added actual reconstruction from the
expected durable operation, preservation of a committed prefix across later
page rollback, post-completion-commit inserts, and an independent observer.
There are no product changes, Git writes, role changes or worker DB runs.
One cursor covers the entire fixed immutable bigint identity domain; multiple
parallel ranges remain outside this finite fixture. Writers stop by completion
of the explicit test schedule, not an independently qualified deployment fence.
Reconstruction is a new object/connection in the same test process, not SIGKILL,
lost COMMIT reply, fresh-cluster recovery or failover qualification.

## Approved contract versus pending decisions

Current `docs/decisions.md`, approved scope decision 6: added read p95 <=3 ms
point/equality, <=8 ms IN-20, and protected-column/equality-index storage <=2x;
write throughput and pause budgets remain D. Decision 7: no designated
production key provider or independent review; no production publication/restore
procedure selected. Selected Lifecycle choice: "One PG journal, cooperating
advisory lock, writer pause, full verify, separate artifact publication."

Current `docs/lifecycle.md` Maintenance and ownership: "Use a bounded maintenance
write pause for affected tables." Unknown writer coverage blocks apply; an empty
connection snapshot does not prove excluded writers cannot reconnect. Current
Plan and phases require full verification under writer exclusion, separate
external publication, and stopped writers between database and publication.
Its final online paragraph retains the full final scan until independent review.

Archive `docs/research/CRYPTALIS_FINAL_REVAMP_BLUEPRINT.md`:

- D-REV-04 (line 6254): expressly a proposed replacement of maintenance/full
  verification, compiler user-trigger refusal and slice 5. Initial protection
  first; other online transitions qualify separately. Operation-owned capture,
  immutable ranges, exact obligations, atomic verified target writes and exact
  closure accounting are proposed. Replacing the final O(N) scan requires the
  invariant, privilege boundary and certificate to pass independent review and
  fault-injected tests. Durable FENCED_READY, optional ACTIVE_VALIDATING, host
  fenced publication and no silent downgrade are proposed, not approved product
  phases. Approvers: database/protocol reviewer, operations owner, product owner.
  If rejected, full verification remains normative and no near-zero claim.
- D-REV-07 (line 6284): proposed workload manifest must set sustained-write floor,
  p99, total writer exclusion through drain/publication/restart, reader delay,
  provider policy, memory/WAL/disk/replication and RTO/RPO. The <=5 s / 1M-row and
  10M challenge are illustrative, neither approved SLAs nor achievements.
  Approvers: product/application/operations owners. Missing budgets never PASS.
- D-REV-09 (line 6304): proposed existing authenticated host authority binds exact
  target, operation/epoch, predecessor, locks, phase, key/wrapper generations and
  runtime identity. "A database lease/lock alone does not fence an in-flight
  external publish." Writes remain fenced until exact successor authority and
  fresh-worker admission. Actual host publication delay/reorder/lost-reply/
  old-operator and backup-quarantine evidence is required. Approvers: deployment
  and security owners. If unresolved, G-POLICY and online cutover stay blocked.

One bounded owner decision for a later integration proposal: approve or decline
an INITIAL-PROTECTION-ONLY experimental contract exception for operation-owned
capture and durable enumeration, while retaining current maintenance final
verification and separate publication. Require database/protocol and operations
review before admission. Do not bundle final-scan removal, a pause SLA, rotation,
new credentials or old-attachment acceptance into that decision. Actual online
cutover additionally remains blocked on D-REV-09 authority/fencing and D-REV-07
workload budgets. The broad deadline supplies none of those decisions.

## Exact pending proposed clauses

These are verbatim research proposals, not owner approval or admitted contracts.

### D-REV-04 Near-online admission and bounded closure
**Exact proposed replacement:** “Retain full writer-fenced verification for maintenance transitions. Admit initial online protection first, then separately qualify online current-data removal, payload-root rotation and search-root rotation with their operation-specific byte/semantic/recovery oracles. The first protocol applies to the qualified stock PostgreSQL 16 table/writer cell through operation-owned source invalidation/capture, immutable baseline ranges, exact dirty obligations, atomic verified target writes and fixed-size transactional closure accounting. A source mutation creates an obligation in the same transaction; a worker cannot clear a newer obligation. Final closure may replace an O(N) writer-stopped scan only when the named inductive invariant, privilege boundary and fixed-size certificate pass independent database review and fault-injected native tests. No active mixed search generation or hidden weakened uniqueness is permitted. Permit operation-scoped database range claims, worker epochs, dirty identities and exact fixed membership counters solely for this transition; this does not reinstate a general distributed worker registry or business mutation ledger. For non-null fields, separately admit ACTIVE_VALIDATING with enforced CHECK (column IS NOT NULL) NOT VALID, followed by online validation and native NOT NULL restoration; changed catalog/reflection/SQLSTATE behavior must be qualified or that application must use maintenance. Stop and drain writers/workers, commit a durable FENCED_READY fence in its own transaction, reacquire and verify locks/epoch, close all obligations, atomically switch, publish through externally fenced compare-and-set authority, verify fresh workers and resume. Measure total exclusion through publication/restart and reader blocking. On failed proof, excessive backlog, unsupported identity/tenant move, schema/capture drift or absent publication fencing, refuse before effects or use the explicitly planned maintenance route. Never downgrade silently mid-transition.”
**Alternatives:** correctly bridged logical decoding remains a researched alternative; application dual-write requires every host writer to change; scanning all live markers at cutover defeats R04. **Acceptance:** REV-09A/B/C invariant and initial protection; REV-09D/E/F separately qualified online removal/payload/search rotation; REV-09G individual difficult-cell admission; adversarial schedule suite, counter contention/maintenance bounds, crash/failover/publication tests and proposed 1M/10M envelope. **Approver:** database/protocol reviewer, operations owner and product owner. **If rejected:** full final verification stays normative; no near-zero-downtime claim.

### D-REV-07 Workload-specific numerical budgets
**Exact proposed addition:** “Retain added p95 ≤3 ms point/equality, ≤8 ms IN-20 and ≤2× isolated protected-column-plus-index storage against a matched native baseline. Before qualification, approve the exact runtime/workload, sustained write-throughput floor, p99 envelope, total writer exclusion including drain/publication/restart, reader delay, provider cold/outage/revocation policy, memory/WAL/disk/replication bounds and restore RTO/RPO. Evaluate the illustrative Section 8 envelope, including ≤5 s total writer exclusion on a controlled 1M-row online workload and a matched 10M challenge. These proposed values are not approved SLAs or measured achievements. Approve integration edit/time targets after the first native baseline and report all excluded workflows.”
**Alternatives:** declare generic zero downtime/near-zero edits, which is unsupported; leave budgets indefinite, which prevents release decisions. **Acceptance:** owner-signed workload/threshold manifest, at least five paired runs where feasible, uncertainty and failed outcomes included. **Approver:** product, application and operations owners. **If unresolved:** no missing budget is PASS.

### D-REV-09 Current authority and stale actor fencing
**Exact proposed replacement:** “Use the existing authenticated host deployment system as current authority outside database restore. Bind exact target, operation/epoch, predecessor artifact, source/target lock, phase, wrapper/root generations and runtime identity. A publisher must reject an obsolete operation through authenticated compare-and-set or an equivalent host-enforced fencing mechanism. A database lease/lock alone does not fence an in-flight external publish. Keep writes fenced after switch until the exact successor authority is confirmed and fresh workers pass admission. Quarantine restores and failovers until database lineage, journal/capture continuity, retained readers/keys and current authority agree. No mandatory new authority service is introduced.”
**Alternatives:** database-only authority replays with backups; an unbounded/reorderable external publisher breaks near-online and stale-worker guarantees. **Acceptance:** publish-delay/reorder/lost-reply/old-operator tests and old-backup quarantine under the actual deployment system. **Approver:** deployment/security owners. **If unresolved:** G-POLICY and online cutover stay blocked.
