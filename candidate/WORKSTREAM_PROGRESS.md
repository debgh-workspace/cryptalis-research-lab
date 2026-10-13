# Lifecycle workstream: root-rewrap successor prerequisite

Updated: 2026-10-13 12:44 UTC. Coordinator owns all PostgreSQL execution and publication.

## Scope and status

Base: verified S14 copy, coordinator revision 2065cb78f3c7126f207fc62c35887ddd204925af.
This directory has no local .git metadata. No commit, reference, upstream, old mailbox,
credential, cluster, or active policy has been changed.

Task: implement one finite prerequisite for CP76 root-rewrap publication. Existing
prepare_rewrap verifies one tenant's candidate roots but does not bind a complete
source artifact, authenticated source pin, tenant inventory, or target policy set.
The first slice adds that binding and repeatable root-equivalence verification.
It MUST NOT make the candidate acceptable to runtime attachment or maintenance.

Canonical owners: docs/security.md (exact root/context/lease/custody contracts),
docs/lifecycle.md (publication, rollback, restore), and CP76 in the research
blueprint (proposed successor state machine, not an approved production contract).

## Finite acceptance gate

1. Exact canonical versioned artifact binds a fresh operation identity, target,
   source artifact/operation/schema-lock digests, complete source/target policy
   inventory, all historical root contexts and unchanged write generations.
2. Source/target maps exactly match all tenants admitted by the source artifact.
   Unknown fields/versions, malformed IDs/digests, noncanonical bytes, changed
   scopes, generations, inventory or source pins reject with typed safe errors.
3. Reverification unwraps through existing bounded Keyring preparation and
   compares every root; all source and target leases remain live at return.
   No stale lease, changed provider/policy or partial candidate succeeds.
4. Existing active-policy/attachment guards continue refusing the candidate.
   Original policies and old CF1/search bytes remain readable and unchanged.
5. Real PostgreSQL evidence is coordinator-run through the unchanged dual-role
   preflight. Pure/static inspection here never starts or connects a database.

## Publication design awaiting integration review

Separate successor identity and artifact; never rewrite a protect artifact or
swap its journal digest. Original artifact and wrappers remain recovery inputs.

- PREPARED/WRAPPED/VERIFIED: no database mutation. Keep source ACTIVE. Persist
  wrapped candidate material only through an authorized external mechanism.
- PENDING database transaction: existing executor lock and table locks; exact
  source ACTIVE pin/journal/target/schema/role checks; complete root revalidation;
  create always-enabled statement write guards; insert successor PENDING;
  mark predecessor REWRAPPING with exact successor identity/digest. Commit all
  together. No application payload, term, index, or root generation changes.
- External ACTIVATING: operator publishes the exact successor pin separately.
  Both source and target runtime admissions remain blocked while stores disagree.
- ACTIVE database transaction: require successor ACTIVATING pin; verify both
  journal records, strict lineage, root policy and guard/schema facts; mark source
  SUPERSEDED and successor ACTIVE. Guard retirement is BLOCKED until a durable
  stale-worker fence is proved; see the source-inspection finding below.
- External ACTIVE: fresh workers admit only exact matching successor artifact,
  pin and database. Old artifacts remain recovery readers, never current authority.

Crash/lost reply: after the original transaction is terminal, read both records
on the trusted current target. Source ACTIVE plus absent successor establishes
no database switch; source REWRAPPING plus exact successor PENDING establishes
pending; source SUPERSEDED plus successor ACTIVE establishes database activation.
Anything one-sided, mismatched, restored behind the independent current pin, or
with unknown transaction termination stays UNKNOWN and fenced. A journal cannot
choose or reconstruct current external authority. No blind COMMIT retry.

Abort requires independently current source authority, pre-activation proof and
an atomic exact-pair reversal. Uncertain host publication blocks abort. After
activation, rollback is a new successor using revalidated retained custody;
republishing an old pin or restoring an old journal is forbidden.

Shared strict artifact resolution must eventually serve runtime, reverse plans,
restore checks, and later rewraps. Deprotection/removal must explicitly inventory
all superseded predecessor rows; existing unknown-journal refusal stays intact.
That integration, stale-worker fencing and actual crash/lost-reply matrix are
NOT IMPLEMENTED by this first prerequisite slice.

## Approvals and remaining objectives

Local synthetic prototype only. Real security-policy publication, persistent
provider access/credentials, key retirement/deletion, deployment or permissions
require the corresponding explicit approval. Production custody, independent
security review and all seven production gates remain UNKNOWN.
Payload-key rotation/re-encryption, search-key reindex/rotation, online capture/
catch-up/fencing, fresh-cluster restore and measured pause budgets remain OPEN.

## Evidence

Initial source inspection only; no tests yet. Test/code hashes and exact commands
will be appended after implementation and coordinator execution.

### B1 RED and first GREEN candidate

Coordinator reports b1-rewrap-successor-red-20261013: selected historical/
multitenant/root-equivalence case 1 FAIL in 0.23 seconds because the proposed
module was absent. Exact source/test snapshots retained; PostgreSQL stopped.
Added private _rewrap_successor.py only. Original runtime, migration,
deprotection, provider, preflight and active guards remain byte-identical.
Static compile passes. GREEN execution is queued with the coordinator.

### B1 first GREEN

Coordinator b1-rewrap-successor-green-20261013: 66 PASS in 0.23 seconds across
new proposal tests and existing preparation/lease controls; unchanged real
owner/runtime preflight. These were crypto/artifact/lease tests, not database
publication tests. Source hashes fixed and PostgreSQL stopped.

Expanded tests now cover genuine PostgreSQL-compiled ACTIVE source, exact
journal/schema/frame preservation, unchanged runtime/reverse policy refusal,
historical-generation frame reads, source-only cross-tenant lease expiry,
intentional warm-lease outage behavior, and target provider identity drift.
Provider identity drift is a suspected gap in the first private verifier;
coordinator RED is requested before that correction.

Authority limit: this prerequisite compares a supplied ACTIVE source pin to its
exact source artifact. It cannot determine independently whether an otherwise
matching old pin is still current. Host authentication/provenance and live
journal/target inspection are mandatory future publication inputs. Generating
an inactive proposal from a retained old source does not reactivate that source.
The tests do not claim restore-resistant publication, stale-worker fencing,
provider custody, durable candidate persistence or full rotation completion.

### B1 expanded RED and identity correction

Coordinator b1-rewrap-successor-expanded-red-20261013: 2 FAIL / 31 PASS in
0.67 seconds. Both expected provider-identity drift cases failed to raise.
Genuine compiled-source/no-publication PostgreSQL control passed. Source fixed
through the run; PostgreSQL stopped. Failure source/receipt are retained there.

Correction checks exact policy-selected provider identities before preparation
and after all callbacks, including warm materials. Final all-material expiry
checks occur after these callbacks. Identity checks are local, not availability
probes: a valid warm same-identity key still works within its original lease
when its provider is offline. No source/target key generation or root changed.


### Publication design blocker found by current-source inspection

sqlalchemy._Attachment.validate calls migration.check_attachment at attachment
startup. Later session creation/operations check static plan/key identity and
mapping fingerprints, not the current journal. A wrapper-only rewrap preserves
row bytes, schema, root contexts and generations. Therefore dropping a temporary
pause guard at successor activation would allow an already-attached old worker
to resume with its old policy. A SUPERSEDED journal marker alone does not fence
that worker. The earlier guard-retirement proposal is insufficient.

Before publication integration, choose and prove a persistent operation-bound
write fence plus admitted transaction binding, or a separately approved distinct
runtime-credential handoff. New credentials/security permissions require their
existing action-time approval. The host still owns current pin authentication,
worker drain and restore quarantine. No unproved instantaneous arbitrary-process
revocation claim is added. The inactive prerequisite is unaffected.

Source locations: sqlalchemy.py lines 331-356 (static policy plus startup
inspection), 1055-1063 (factory checks static key policy), 1066-1120 (attachment),
and migration.py lines 728-735 (existing pause-guard removal during activation).

### B1 corrected final focused gate

Coordinator evidence/b1-rewrap-successor-identity-fixed-sa21-20261013:
72 PASS in 0.57 seconds, with unchanged real owner/runtime role preflight.
Includes actual compiled-source preservation/refusal; it does not include any
publication transition. Source stable; PostgreSQL stopped. Second dependency
cell and full suite NOT RUN for this addition.

Final runtime/test hashes:
- src/cryptalis/_rewrap_successor.py:
  49df6d61abcf7eadf4b2f3cfbb8adec6915319d8e652f3639e4e3772d6e63b77
- tests/test_rewrap_successor.py:
  0e9c23e326604cadfe789c62a5c1d75b77628cf7af1104020c451d841a2cd6e9

Changed files: the two new files above, this progress record, and bounded
candidate-status additions in docs/lifecycle.md and docs/status.md. All other
source, tests, formats, active guards and preflight files remain unchanged.
No packaging, publication or remote action performed by this worker.

Next proposed finite slice (no source/test edits yet): verify the exact reverse
predecessor operation/digest/DEPROTECTING state and source-link metadata on every
active reverse resume, not only initial expansion/abort/removal. Actual-PG RED
must establish the current behavior before deciding whether a correction is
needed. This proposal does not overlap the coordinator's legacy bridge.
