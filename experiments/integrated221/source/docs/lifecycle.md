# One transition engine

**SPECIFIED:** lifecycle contract. **IMPLEMENTED:** bounded product protection transition with plan/apply/verify and pre-switch abort.
Decrypt-back, removal and rotation remain unimplemented product slices. [Status](status.md) states the evidence limits.
The protection engine verifies and switches in one transaction; saved verification checkpoints require a fresh pass on resume.
Plain reads continue during verification. Writes and locking reads wait; schema DDL can pause all access.
VERIFIED paragraphs below describe recorded receipts, not current product qualification. All other requirements remain SPECIFIED.
Every protection change uses expand → backfill → verify → switch → contract.
Rollback, deprotect, search changes, and key transformations reuse this path.

**VERIFIED, recorded earlier lab:** the service lab passes 27 listed checks over 1,000 synthetic rows. It observes a blocked concurrent writer,
a process exit after a committed chunk, inspected idempotent resume, full verification mutants, CF1 companion transport,
payload/search rotation, and current-data decrypt-back. An isolated ordinary application then reads and updates the recovered data with Cryptalis/lab-reader imports blocked.
This is not the original application's complete retrofit/removal test. Post-commit process exit is not a transport-level lost COMMIT-reply test.
Live provider custody, authenticated deployment publication, retained-backup readers and full writer ownership remain unqualified.

## Integrated lifecycle checkpoint: 2026-10-07

The preceding 27-check lab is historical. The new [23-check receipt](../spikes/revamp/results/gate-lifecycle.json)
uses the original three-model application's actual CF1 data and one transition executor for protect, rotate and deprotect.
Chunk members and transformed rows commit together. Resume inspects the original digest/membership and preserves committed ciphertext.
**VERIFIED, recorded spike:** streaming verification checks membership, native values/types/NULLs, and generations before the transactional switch.
It compares inspected source index names/definitions and their validity/readiness flags. Target unique-index construction exercises the fixture's scoped uniqueness.
Generic CHECK/FK/default/collation and dependency preservation remain UNKNOWN. Source-index observations do not prove them.
A competing executor is denied; an actual concurrent writer is observably blocked while the maintenance lock is held.
That observation does not prove deployment-wide writer exclusion between chunks.

The lost-reply test shuts down the receive side of the original connected socket before COMMIT completes.
It observes EOF and an initially absent marker, then independently observes the original transaction terminal and a matching committed marker.
It never consumes the COMMIT reply through libpq. Resume preserves the committed bytes.
The separate [fault receipt](../spikes/revamp/results/gate-faults.json) proves that real SQL errors and injected local-provider failures
roll back both staged chunk data and its marker. Actual disk/WAL exhaustion remains pending.

Payload rotation, search rotation and local rewrap are separate tested actions. Current post-cutover application edits survive rollback,
reprotection and deprotect with all original columns and types compared. Eligible shadows, indexes, trigger and journal are removed.
A fresh process blocks Cryptalis/crypto readers, verifies all current data, commits an ordinary edit, then runs the untouched 29-assertion original oracle.
Only its owned synthetic rows are cleared between the current-data proof and the oracle's empty-database fixture.

The database phase remains `SWITCHED_DATABASE_POLICY_PENDING`. Authenticated host publication/startup, restored-old-policy denial,
stale-worker termination, durable independent-process readers/keys, format/codec upgrade and native provider deletion remain UNKNOWN.
The local backup decode and fork-inherited interruption test do not qualify retained-backup custody or a fresh independent provider restart.
The [million-row protection receipt](../spikes/revamp/results/gate-performance.json) measures initial protection; it does not qualify
million-row rotation/deprotect, a production pause ceiling or a storage-exhaustion response.
These pending requirements keep the complete lifecycle gate UNKNOWN.

## Maintenance and ownership

Use a bounded maintenance write pause for affected tables.
The deployment operator stops known workers/jobs and excludes unsupported writers before transformation.
The runtime principal cannot change schema, operation metadata, or lifecycle privileges.
Unknown writer coverage blocks apply. An empty connection snapshot alone does not prove that excluded writers cannot reconnect.

One PostgreSQL journal stores the immutable operation ID/plan digest, target binding, source/desired lock, phase, and chunk outcomes.
Chunk data and its completion marker commit in one transaction.
A session advisory lock serializes cooperating executors. It is not external writer exclusion or fencing of provider calls.
Hold table locks where required. Reinspect durable operation state after a crash or lost connection.
A second executor must acquire the lock and reconcile the original operation before it resumes work.

No operation leases, distributed worker registrations, receipt dispatcher, or per-request mutation ledger are required.
The deployment stop, database transaction, and provider native outcome define the SPECIFIED boundary.
Unresolved in-flight work remains pending. A timeout does not establish worker termination or external effect completion.

## Plan and phases

The plan binds its exact target, original/desired lock digests, schema facts, data scopes, writer inventory, readers/keys, approvals, and estimates.
`plan` creates no data or schema effects. It shows changed query semantics, leakage, and plaintext exposure before approval.
A changed manifest is a request, not authorization to weaken the active representation.

| Phase | Required evidence |
|---|---|
| Expand | Inspected additive shadows/indexes and durable operation identity. Old representation remains authoritative |
| Backfill | Bounded chunks authenticate source where protected and write complete target payload/companions plus marker atomically |
| Verify | Full required row membership, decoded value/type/NULL equivalence, companion recomputation, and valid constraints/indexes under writer exclusion |
| Switch | Verification still matches the stopped source. Database schema/state and the independently controlled deployment pin select the same representation |
| Contract | Package/reader/key/backup dependencies permit exact approved retirement. Actual effects and retained obligations remain observable |

Schema/data switch can be transactional within PostgreSQL.
Updating an external deployment artifact is a separate effect, not a cross-service atomic commit.
Writers remain stopped between those effects. Startup denies either mismatch until inspection finishes the switch.
Use the existing deployment tool to publish the exact planned policy artifact.
Do not write a new distributed CAS or automatic policy service merely to hide maintenance downtime.

Default chunk size is a measured tuning parameter, not a security guarantee.
The executor resumes committed chunks without regenerating their ciphertext.
Counters/cursors alone do not prove membership coverage. Full terminal verification is mandatory.
Verification mutants must include wrong payload, missing row, stale companion, duplicate normalization, and invalid index.
Disk/WAL/provider exhaustion stops progress and retains completed chunks. It never produces a partial-success switch.

For a lost COMMIT response, do not automatically retry business writes or assert rollback.
For transition chunks, inspect the original operation/chunk marker on the trusted current primary after the original transaction is terminal.
A matching marker and transformed rows establish the committed chunk within PostgreSQL's durability assumptions.
An absent marker while the original transaction can still commit is UNKNOWN.
Privileged corruption, failover data loss, or wrong-target inspection also prevents a confident classification.
No global exactly-once guarantee follows from a marker.

## Rollback

The default is decrypt-back or transform-back from **current** active data.
It is the same verified engine used for deprotect. A static pre-switch snapshot is not a lossless rollback after post-switch writes.

Before switch, `apply --abort OPERATION` can remove operation-owned shadows and retain the unchanged source.
After switch, rollback pauses writers, reads current values, transforms the previous representation, verifies, and performs a new switch.
It requires compatible readers/keys and a lossless prior type/constraint contract.
If current values cannot fit that contract, report the exact conflict class and keep the active representation.
Do not discard new values or restore an old data snapshot silently.

Rollback/removal remains available through decrypt-back until explicit user finalization retires its required recovery dependencies.
Finalization uses the existing lifecycle and adds no command or mode.
The selected default retains no live plaintext rollback mirror and no timer that forces finalization.
Plaintext needed for rollback appears only in the explicitly approved reverse transition.
Rollback can be slower. Status shows estimated pause and actual progress.
A required old key/reader cannot be retired while it remains the only approved reverse or backup recovery route.

The earlier local experiment changed a value after cutover, then recovered that current value through decrypt-back.
The integrated checkpoint records the original application's narrow rollback/removal evidence. Neither qualifies the full lifecycle gate.

## Changes and rotation

| Change | Engine action |
|---|---|
| Protect or stop protection | Transform payload, create/drop declared search representations, verify, switch, contract |
| Add/remove a query capability | Derive/retire companions and indexes. Reseal payload when authenticated search metadata changes. Verify source/target and queries |
| Normalizer/search-domain change | Full reindex and duplicate/constraint review. New identity, no in-place reinterpretation |
| Payload key generation | Re-encrypt payloads and authenticated companion metadata. Search roots can remain stable |
| Search key generation | Rebuild terms/arrays and indexes. Reseal authenticated payload headers with fresh nonces. Keep writers stopped |
| Provider/KEK change | Rewrap exact roots and verify unwrap/context under the new provider. Payload/search bytes stay unchanged |
| Format/codec upgrade | Deploy required readers first, transform, verify, then switch writers. Retire old readers only after dependency review |

Keep exactly one active application writer representation during maintenance cutover.
No partial-generation OR query or cross-generation uniqueness gap is silently admitted.
Native KMS KEK material rotation is different from root rewrap, payload rotation, or search reindex.
Rewrap alone does not cure a leaked payload/search root.
No normal rotation automatically deletes historical keys or makes copied old ciphertext safe after compromise.

## Restore and authority loss

These are deployment requirements. Only a local policy model ran; no authenticated restore test passed.
A restore starts in quarantine with production writers stopped.
The operator inspects trusted schema, target identity, current deployment policy, key wrappers, formats, and backup lineage.
A restored operation journal is progress evidence, not current authority.
Old consistent metadata cannot select an older active policy or revive externally revoked access.

Compare the database representation to the current policy artifact outside the restore.
If it is older, plan a verified transformation to current policy before admission.
If required readers/keys no longer exist, identify irrecoverable scopes and refuse silent incomplete recovery.
If current policy provenance is unavailable, keep service stopped. A restored database pin cannot replace it.

The host's existing current authorization must enforce subject denial independently when that denial must survive restore.
Putting the only deny record inside PostgreSQL cannot supply that property.
Deployment policy can reject retired generations. It does not prove every row is fresh within an admitted generation.
No policy counter detects arbitrary same-context row replay or an invisible old application/RAM clone by itself.
Workers must restart under current policy and target credentials after restore.
Managed-provider target identity and failover behavior remain external compatibility tests.

KMS/provider loss and policy loss differ. Intact keys with unprovable current policy deny service.
Permanent loss of every recovery key/wrapper can make ciphertext permanently unreadable.
The operator retains a tested recovery inventory and reader artifact. There is no Cryptalis key-hostage service.

## Revocation and destruction

Subject revocation means host-authorized managed denial and row cleanup, not cryptographic erasure.
Default tenant roots remain able to decrypt a subject's old encrypted backup when the required authority survives.
Shared search roots can retain subject linkage. Deleting a current row or wrapper does not destroy backed-up copies.

Domain/tenant key destruction is a separate provider-admin operation after inventory and explicit approval.
Tenant-level destruction requires a provider KEK dedicated to that tenant, or another independently proved root-destruction route.
Deleting a tenant wrapper cannot erase its backed-up copies under a surviving shared KEK.
Report requested deletion, provider pending state, observed native deletion, remaining cached/copied keys, and physical backup expiry separately.
Do not call recoverable values shredded, erased forever, or cryptographically destroyed.
A provider deletion request is not proof of completed deletion or loss of every descendant key.
No per-subject KMS key, puncturable encryption, tombstone service, or instantaneous revocation protocol is selected by default.

## Deprotect and remove

Approve plaintext exposure before the first plaintext staging write.
The approval names scope, target, resulting WAL/backups, and retained recovery ownership.
Authenticate current ciphertext, reconstruct original ordinary SQL types, recompute/verify exact values, and switch while writers remain stopped.

Removal completes only after:

1. The ordinary-schema application passes real read/write/query tests without Cryptalis attachment or import.
2. Search companions/indexes, ciphertext columns, and eligible internal metadata are retired after dependency review.
3. Every retained encrypted backup has a tested reader/key route or an explicit approved loss disposition.
4. Old workers/jobs no longer require Cryptalis readers or write protected representations.
5. Package removal occurs last. Status names ongoing external key/backup obligations.

Rollback during deprotect/removal uses the same transform-back path. It is not a second mirror protocol.
The earlier package-free SQL read does not satisfy application removal. The integrated checkpoint records a narrow original-application child test.
Durable retained-backup recovery and the full removal gate remain UNKNOWN.
Dropping columns does not erase dead tuples, WAL, backups, or host exports.

### Safe-default remembered-index designation research profile

SOURCE-ONLY FOLLOW-ON, NOT VERIFIED: new `migration.plan(...)` calls default to
`preserve_cluster_designation=True` and explicitly select
`cryptalis.transition/retained-native-comments-cluster-research-v2`. Its reverse
artifact uses `cryptalis.reverse/retained-native-comments-cluster-research-v2`.
The separate `cryptalis.cluster-designation/research-v1` inventory records every
original native index name, constraint link and explicit clustered boolean for
each protected table. It binds these facts to the unchanged compiler lock/v1.
OIDs are not durable artifact identities; this adds no physical-instance-only
restore restriction. Existing schema checks still bind definitions and native
table/constraint linkage. At most one index per table may be designated.

The candidate checks designation before expansion and during paused and active
phase checks. Before each switch it rechecks under the existing transition table
lock. During protection, a retired affected index has no live designation. An
unaffected designated index keeps its designation. Reverse recreates admitted
native indexes, restores affected designation with `ALTER TABLE ... CLUSTER ON`,
restores comments and verifies ordinary schema in one transaction. Unexpected
designation, incomplete inventory or changed linkage refuses the operation;
it does not silently clear or replace another designation. This operation does
not run `CLUSTER`, rewrite the heap or promise physical row order.

The omitted option selects the new v2 profile. Explicit false refuses with
`legacy_profile_creation_disabled` before planning effects. This is an announced
default change; no existing artifact is rewritten or relabeled.
Comments-v1 and retained-native-v0 artifacts remain parseable. Their designation
status stays `NOT_INVENTORIED`, not false or verified absent. Their prior loss
cannot be reconstructed from the active catalog after an affected index is
dropped. The conditional recovery rules below change admission of destructive
legacy operations without changing old bytes or inventing historical metadata.
Do not use historical artifacts as evidence of exact designation recovery.

All existing comment inventory, size reservations, current-value verification,
writer fencing, external pin and plaintext approval requirements still apply.
The new inventory and longer format names are included in the existing forward
artifact/reverse-envelope budget. A failed reverse transaction must retain the
previous durable phase; inspect it before resuming the same operation. The new
tests are prepared only. No expanded lifecycle or production qualification follows.
PostgreSQL can also retain dropped-column bytes in existing heap tuples: `DROP COLUMN` hides the column from SQL,
but does not immediately remove its stored data ([PostgreSQL 16 ALTER TABLE](https://www.postgresql.org/docs/16/sql-altertable.html)).
Protection switch retires the original SQL column after verification. It does not establish plaintext erasure.
Historical plaintext and encrypted-reader obligations remain explicit after application exit.

## Recovery behavior

`status` reports the original operation, last durable phase, attempted effect, pending work, and remedy.
`apply --resume` reinspects that operation and actual state before another effect.
An expired initial plan cannot authorize changed effects. It can identify an already approved operation for current reinspection.
Unknown provider effect requires native inspection before retry. Advisory locks do not fence an already dispatched KMS request.
No separate reconcile, break-glass, receipt repair, or restore-admission language is required for the normal product.
If an essential outcome cannot be established, remain PENDING/UNKNOWN and state the specific required observation.

## Supported deployment candidate

The selected candidate uses one application deployment, one current PostgreSQL primary, and an existing trusted release operator.
The operator controls worker termination, database credentials, deployment artifacts, and restore quarantine.
No profile qualifies yet. Multi-deployment writer coordination is unavailable until that exact host procedure passes its tests.

1. Stop affected writers and wait for their transactions to finish. Confirm that alternate credentials cannot restart a writer.
2. Run the database transition and full verification under the maintenance principal. Record the exact pending policy artifact digest.
3. Switch the database representation. Leave writers stopped. `status` names the operator and the required artifact publication.
4. Publish the exact artifact through the trusted deployment tool. Restart workers with fresh target credentials and empty key caches.
5. Admit traffic only after startup compares the current artifact, target, schema, and active representation.

Interruptions between steps 3 and 4 retain `writers: STOPPED` and a named pending effect.
Neither the restored journal nor a stale worker can approve publication. Missing provenance keeps service stopped.
This procedure needs real tests for both switch boundaries, stale policy, old workers, and unavailable host denial authority.

`plan` must estimate temporary storage, WAL, provider calls, verification duration, and total writer pause.
Pause budgets remain undecided (D). The operator must approve the concrete measured/estimated pause before an actual transition.
No production pause ceiling is approved.
The admitted text/equality plan enforces encoded-text and bind limits before SQL.
Range tree depth/cover and prefix term bounds are INTERNAL ONLY until capability admission.
Resource bounds prevent uncontrolled expansion. They do not establish an approved write-throughput budget.
Advanced capability/normalizer/search-domain changes are UNSUPPORTED BY DESIGN until [admission](compatibility.md#capability-admission).
The selected lifecycle scope uses text, application-generated primary keys, and explicit tenancy.

## Isolated lifecycle work authorized: 2026-10-09

Slices 6/7 remain incomplete. The owner authorized their implementation after corrective and app-baseline work; no lifecycle completion is implied.
Chunk-boundary lease renewal must re-prepare through the provider with bounded total age, fail closed on expiry/outage, and emit no SQL after failed preparation. No TTL extension is authorized.
Online proposals retain the maintenance fallback and full final scan until independent review permits a stronger verification argument.

## Chunk key-lease scheduling margin

Maintenance backfill and verification request at least min(1 second, half the configured lease) of remaining prepared-key lifetime per tenant/chunk. Keyring.prepare and prepare_async accept keyword-only minimum_validity; default0 preserves ordinary cache behavior. Too-short leases cause exact provider-backed preparation, not expiry extension. Provider latency consumes the original max_age budget (at most300seconds). Failed preparation does not fall back to stale material; every actual crypto use still checks expiry. Issued snapshots retain their original deadline. Mid-chunk expiry aborts that chunk; earlier commits remain resumable after explicit inspection.

This margin is not a guarantee that arbitrary batches finish in time. It does not automatically retry application transactions, cap whole-job wall time, or detect a provider outage/revocation before the next provider contact. Byte bounds and application-level chunk sizing remain separate qualification requirements. Tests: test_key_lease_renewal.py and test_migration_key_leases.py.

## Byte-bounded maintenance chunks

apply and verify accept chunk_bytes: a positive integer up to1GiB, default64MiB, alongside the existing row-count bound. PostgreSQL selects an ordered identity/size prefix before returning payloads to the client. Backfill accounting includes source UTF8 plus prospective CF1 frame bytes and identity bytes; verification includes source UTF8, actual frame bytes and decoded UTF8. Null frames contribute no payload bytes. Python object, key-policy, driver and server overhead are outside this logical data budget; it is not a process-RSS guarantee.

row_exceeds_chunk_byte_limit means the first remaining row cannot fit. Keep writers paused, inspect its aggregate protected-field size and raise the explicit budget within the limit if the host has capacity, then resume the same operation. Earlier committed chunks remain unchanged. Never skip or truncate that row. A row exceeding the maximum requires a reviewed per-field/streaming transport; that capability is not implemented. Full verification obeys the bound too and remains mandatory. Tests include Unicode, storage-only/equality fields, exact byte boundaries, oversized payload not returned to client, prefix recovery, and real transport/lock faults.

### Print-only runtime role setup template

**IMPLEMENTED:** after read-only planning, print
`plan.runtime_role_template("cryptalis_runtime_new")` with a fresh role name.
The method returns a ready-to-run SQL transaction for administrator review. It creates
nothing. The template specifies a NOLOGIN/NOINHERIT role with all administrative flags
disabled, USAGE on declared schemas, and SELECT/INSERT/UPDATE/DELETE on declared tables.
It grants no schema CREATE, ownership, TRUNCATE, routine EXECUTE or grant option.
Login authentication and assigning the role to a workload are separate explicit actions.
The role name must not already exist; names over 63 UTF-8 bytes reject instead of truncating.
An existing role, PUBLIC rights, default privileges and membership paths require their
own inspection. Printing the template is not an admission verdict or permission repair.


### Conditional legacy designation recovery

Historical v0/v1 artifacts remain NOT_INVENTORIED. Existing trusted source locks,
external pins and journal checks remain mandatory. For an unstarted operation,
replace the old plan with a fresh v2 plan while the original native catalog still
exists. Use a fresh external deployment pin. For a staged pre-switch operation,
the existing abort path retains original indexes and values. Its durable ABORTED
journal is retained; automatic journal deletion or replan is not supplied here.

A legacy source that retired no original index has a bounded recovery path.
Validate all surviving original index names, definitions and constraint links;
observe current native designation under transition locks; preserve that complete
survivor map across reverse switching and verify it again before commit. Never
infer historical absence. A designated disposable transition index requires
explicit review and refuses before its removal. Current native metadata is the
authority only for indexes that the authenticated transition did not retire.

If the authenticated source permits original index retirement, this follow-on
refuses a new destructive switch, reverse plan/apply, activation of incomplete
plaintext recovery, or removal when essential designation cannot be established.
It leaves protected application attachment, existing active checks, status,
read access, ciphertext, keys, manifests, journal and backups available. The
classification NATIVE_REPLAN_OR_EXTERNAL_METADATA_REQUIRED describes the artifact,
not proof that a particular database has already lost metadata.

After retirement, recovery needs independently authenticated pre-transition
metadata bound to the correct target and exact source artifact: complete original
table/index identities, index definitions, constraint links and explicit true/false
designation, with provenance and a verified timeline. A trusted historical export
or an independently checked pre-transition backup may provide this evidence.
Current missing flags, the old lock alone, comments alone and arbitrary JSON do
not. An evidence importer and a post-loss upgrade/recovery protocol are not
implemented or verified in this follow-on. Those cases remain blocked for a
separately reviewed procedure; this is not a complete backward-compatibility or
removal qualification. Do not discard recovery material or abandon those cases.


The path-aware legacy reverse abort observes every currently retained native index
under the existing transition locks, after full staged-schema and fence checks.
Abort removes plaintext staging columns only. It preserves a designated ciphertext
companion, verifies the complete native map after cleanup, then restores source
ACTIVE in that same transaction. Destructive deprotection still refuses to discard
a designated companion. This safe abort does not recover missing historical flags
or authorize a subsequent destructive switch.
