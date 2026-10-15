# Current-product abort reservation feasibility

Date: 2026-10-15 UTC
Disposition: SOURCE-ONLY FINDING. No product patch is justified by the examined
size evidence alone. No product or test file was changed. No test was run.

## Decision

The source confirms an absent whole-journal reservation, not a confirmed
current abort-size defect. The current 16 MiB limit belongs to canonical
artifacts. The existing 4 MiB expansion reservation belongs to a future reverse
artifact's active_schemas member. Current journal writers and safe-abort paths
do not impose a 16 MiB limit, and the reviewed current journal consumers do not
use the bounded artifact decoder.

A newly enforced 16 MiB pre-switch journal ceiling would therefore introduce an
admission policy. The native representation experiment does not authorize that
policy or prove that a currently supported abort fails without it. Root agreed
to keep that distinction and explicitly directed no product patch in this slice.

The concrete current recovery gap is different: successful forward abort leaves
its ABORTED journal, and a new forward plan refuses any existing journal. A size
reservation neither removes that refusal nor supplies the missing authenticated
successor/recovery protocol. Recovery should preserve safe abort, current data,
and retained evidence; deleting or relabeling history is not a repair.

## Evidence boundary

Approved source root is candidate-cluster-retained-integrated-v2-20261015.
Line references below are relative to that root and identify the unchanged
source hashed in INPUTS.md. Source-only inspection cannot establish transaction,
driver, native catalog, restore, physical journal, privilege or durable-recovery
behavior. No production qualification follows.

Root reported native V2: 31 PASS in 6.04 seconds, entry exit 0, post-status 3,
and corpus 26 equal. Its independent terminal audit was pending when this task
was assigned. This worker did not inspect runtime receipts or certify those
facts. The native protocol and test body were reviewed only as source.

The native probe isolates JSON representation. It explicitly excludes actual
expansion admission, mutation ordering/rollback, physical journal shape/ACL,
ancestry authenticity, historical abort and durable recovery. Its successful
representation result, once accepted, cannot silently widen those boundaries.

## Current bounds and exact call paths

### 1. Canonical artifact ceiling

- manifest/parser.py:5 sets MAX_DOCUMENT_BYTES to 16 * 1024 * 1024.
- manifest/compiler.py:109-114 canonicalizes with UTF-8, ensure_ascii=False,
  sorted keys, compact separators and allow_nan=False, then rejects above the
  ceiling. This is an artifact encoder, not the journal writer.
- _transition_json.py:23-31 bounds incoming artifact bytes and invokes the
  artifact integer decoder. MigrationPlan and DeprotectionPlan use this path.
- manifest/parser.py:34-43 imposes the artifact counter syntax/range. It does not
  validate scope.count, rows or chunks fetched from a jsonb journal.

### 2. Existing object-comment and reverse-artifact reservations

- _object_comments.py:116-137 constructs a future reverse artifact skeleton.
  It includes the exact source plan, duplicated lock/target/role/schema fields,
  a source pin, fixed estimate member names and bounded variable reservations.
- The variable reservations are 4 MiB active_schemas, 1 MiB retirable_aborted,
  1 MiB cutover_readiness, an escaped role-name allowance and rate-width
  allowances. validate_reverse separately enforces those member budgets at
  :160-192. The skeleton's 2**53-1 estimate maxima are artifact numbers.
- validate_forward rejects an excessive reverse artifact envelope at :156-157.
- schema_reservation at :250-265 deep-copies native schema facts and reserves
  specific later defaults, nullability changes and dependencies. It never
  replaces observed catalog facts with its maximum-width representative.
- check_schema_budget at :268-276 does nothing for legacy v0 and checks only
  the schema mapping for enabled comments-v1/cluster-v2 documents.

This contract does not reserve the entire pre-switch journal, its guards,
progress cursors/counters, verification map or root framing.

### 3. Forward expansion and later progress

- migration.py:627-672 executes expansion under the existing table locks and
  caller transaction. After additive DDL, each model is recorded at :667-668
  with scope, cursor=None, rows=0, chunks=0, exact schema and exact guard.
- :669-670 checks the schema reservation. :671 constructs phase/models.
  :672 inserts state with json.dumps(state), not _canonical(state).
- _scope at :607-616 scans native ordered identities and increments a Python
  integer. It records the exact count and membership digest. It has no
  16-digit or 2**53-1 journal cap.
- _backfill_chunk at :690-712 updates cursor/rows/chunks after a nonempty batch,
  saves the marker in the same transaction, and eventually sets BACKFILLED.
  There is no explicit pre-update rows+batch<=scope.count check here.
- _verify at :715-740 checks fresh membership and rows==scope.count; the
  standalone VERIFIED checkpoint adds the complete per-model digest map at
  :847-848. _switch also uses that complete map at :765-773.
- _save at :490-494 serializes compact JSON through json.dumps and sends jsonb.
  It checks affected-row count, not a canonical/native byte ceiling.

### 4. Reverse expansion and progress

- deprotection.py:296-324 creates the reverse staging metadata and records the
  same six per-model members, plus layout_version=101, source_operation_id and
  source_plan_digest. There is no whole-state expansion size check.
- Its INSERT at :322 and the predecessor update to DEPROTECTING at :323 occur
  in the caller's same transaction. The current code must keep that pairing.
- :349-362 advances rows/chunks/cursor and phase. :365-378 verifies full
  membership and values. Reverse pre-switch verification adds no digest map.
- m._save is shared. No reverse journal-wide byte gate is introduced elsewhere
  in these inspected paths.

### 5. Abort and current consumers

- Forward abort at migration.py:881-901 removes additive objects, checks the
  restored source schema, then changes only phase to ABORTED at :900.
- Reverse abort at deprotection.py:481-507 discards plaintext staging, verifies
  the retained active schema/designation, restores the source marker from
  DEPROTECTING to ACTIVE at :505 and changes its own phase to ABORTED at :506.
  Both writes remain in one transaction.
- Neither abort adds receipt text, a timestamp, lineage, a self-digest or a
  size check. ABORTED has seven characters: one byte shorter than EXPANDED or
  VERIFIED and three bytes shorter than BACKFILLED in the stated JSON domain.
- Current _state readers fetch jsonb directly (migration.py:471-487;
  deprotection.py:220-251). They do not decode through _transition_json.
- Reverse planning fetches current journal rows at deprotection.py:164-170,
  checks phase/source identity, and carries only operation_id/plan_digest into
  retirable_aborted. It does not embed complete abort state in the artifact.
- Final removal reads journal rows directly at deprotection.py:558-569 and
  matches the expected identity/digest set. That read is not a 16 MiB bounded
  journal parser either. It supplies no general hostile-input resource proof.

Therefore no inspected current bounded consumer turns a journal crossing
16 MiB into an abort failure. This is not a proof that all possible journal
sizes, memory usage or PostgreSQL limits are safe; it is the narrower conclusion
that this proposed ceiling is not an existing product contract.

## Why the representation boundary vectors are not a product regression

The native probe test_native_envelope.py:294-310 fills a synthetic
schema={"fill":...} to reach canonical/native +/-1 edges near 16 MiB. It is an
intentional JSON representation fixture, not a compiler-admitted catalog schema.
Current enabled forward expansion reserves a schema map of at most 4 MiB and
requires native schema facts. The native fixture's large schema would fail that
existing forward schema budget; it does not demonstrate a forward expansion
that currently commits and later cannot abort.

The omission controls independently show that omitting verification, cursor or
counter width underestimates the proposed maximum. They do not show that current
code has a whole-state limit it incorrectly checked. No contrary defect was
manufactured by substituting a synthetic schema for observed metadata.

## Supported domains and conditional reservation proof

The current compiler admits UUID and native signed bigint primary keys
(manifest/compiler.py:284-292, :367-376, :531). migration._stream preserves native
ordering with a typed > predicate (:568-570) and native ORDER BY (:593-600).

A future size-only representative can retain every exact expansion member and:

1. Reserve BACKFILLED, the longest legal pre-switch phase at ten ASCII bytes.
2. For each model, use its exact expansion scope.count=N for both rows and
   chunks. Do not substitute estimated_rows, 2**53-1 or an invented maximum.
3. If N=0 reserve cursor=null. Otherwise reserve 36 ASCII characters for UUID
   text or 20 for signed-int64 text, giving 38/22 quoted JSON bytes. UUID nil is
   a valid record value; the nonzero operation/table identity rule is distinct.
4. Include a complete 64-lowercase-hex verification digest for every forward
   model. Do not add this map to reverse state.
5. Retain exact schema, complete guard and scope bytes, and exact reverse root
   fields. Add no lineage or new format member.

Under stopped writers, ordered unique non-null primary-key continuation and
atomic data/marker commits, each nonempty chunk increments rows by at least one
and chunks by one; therefore 0<=chunks<=rows<=N. The current source verifies
membership/completeness later; it does not explicitly enforce this inequality
before each increment. A reservation relying on N must state these assumptions
and decide whether a new pre-SQL invariant guard is required. A helper's size
comparison alone cannot prove runtime membership, exact loader types, physical
uniqueness, writer exclusion, or a restored journal's authority.

The reference's optional artifact counter profile must not be imported into
current journal behavior. A legitimate 17-digit N remains within the proposed
exact-N proof without imposing a new 16-digit cap. Reference parser/depth/type
restrictions also cannot be retrofitted wholesale into old abort.

## Separate confirmed recovery capability gap

Forward migration.plan at :361-362 rejects any existing journal relation with
existing_transition_requires_inspection. Forward abort intentionally retains the
relation and terminal row. Reapplying the original operation reaches
operation_aborted at :479-481. A fresh plan cannot step over the retained row.
The current API has no authenticated aborted-forward successor/replan path.
This is a source-confirmed missing recovery capability, not newly reproduced
runtime evidence, and not evidence of an erroneous safe-abort size gate.

Do not confuse it with reverse retries: deprotection.plan already recognizes
ABORTED reverse attempts bound to its active source and carries their
operation_id/plan_digest entries. This current reverse behavior is not a general
authenticated ancestry protocol and does not accept an aborted-forward root.

The safe target is a reviewed recovery path that retains the old terminal
record and binds a fresh plan to independently authenticated history and current
native metadata. A byte reservation is a prerequisite for some proposed bounded
readers, not a replacement for physical journal validation, ancestry authority,
locking, restore handling, or the missing public recovery API.

## Disposition and next slice

No changed product copy, executable patch, new test or runner was produced.
There is no newly accepted byte limit or format. Native V2 terminal evidence
still requires its independent acceptance. NEXT_SLICE.md identifies exact
future expansion hook sites, required behavior and one finite source-only
preparation step. Any execution remains separately admitted.
