# Smallest next slice and future hook obligations

Status: SOURCE-ONLY PLAN. No runnable entry, patch or product admission.

## Immediate concrete step

Complete the independent terminal review of the existing native V2 result.
Do not rerun it to manufacture the review. If accepted, carry forward only the
observed representation/domain facts and the precise evidence boundary.

Then prepare one source-only constructor-equivalence specification for current
forward and reverse emitted pre-switch states. Use the unchanged current
constructors in migration.py:667-672 and deprotection.py:319-323 as the exact
member-set baseline. The deliverable should contain:

- A field-by-field map of every emitted or later-added pre-switch member to its
  exact retained value or maximum-width replacement, both directions.
- Independent complete literal JSON expectations for UUID, signed-int64, N=0,
  mixed models, full forward verification and reverse root fields.
- Exact-N counter reasoning at decimal-width boundaries including beyond 2**53.
- A statement that synthetic schema/guard stress fixtures are not admitted
  native objects. Include a separate actual-catalog-shape fixture specification;
  no invented missing metadata or enlarged product limit.
- A compatibility table: existing v0/v1/v2 read/abort paths unchanged; current
  plan creation still v2; no successor format, lineage member or public API.

Do not wire the constructor into expansion merely because these comparisons
are complete. Root must first choose a new journal policy or identify a current
bounded consumer/producer regression. Until then it is a research prerequisite,
not a product correctness fix. Root's latest direction expressly excludes a
new 16 MiB product-journal ceiling in this slice.

The known recovery outcome remains separate: permit a safely authenticated new
forward plan after a durable abort while retaining the prior journal evidence.
Use the existing successor design to resolve the authority/physical-relation
requirements. Do not replace that work with a broader refusal or delete the
record to make today's plan constructor succeed.

## Exact future expansion-only hook sites

These sites are precise feasibility findings, not approved edits:

1. Forward: after state={'phase':'EXPANDED','models':models} at migration.py:671
   and before the INSERT at :672. Keep check_schema_budget at :669-670 intact.
2. Reverse: after the full reverse state at deprotection.py:321 and before its
   INSERT at :322, thus also before the paired source DEPROTECTING write at
   :323. Keep source validation, locks and paired transaction intact.

All observed schema/guard/scope facts then exist. These hooks occur after
uncommitted additive DDL, so the property is rejection before durable expansion,
not rejection before any SQL effect. Failure must roll back the whole expansion
transaction. A check performed earlier using guessed post-DDL metadata cannot
prove the same property.

Never place the new gate in shared _save, _state, abort, _progress, active
attachment, or removal. Those sites would apply new rules to already committed
historical states and can disable existing recovery. Never replace real observed
facts with the maximum representative. No fake cursor/counter/digest is written.

## Minimum obligations before an implementation can claim a bound

### Contract and compatibility

- Name the actual ceiling and representation it limits. Artifact bytes and
  PostgreSQL jsonb::text transfer bytes are separate contracts. 16 MiB is not
  already a current journal limit.
- Name the newly covered operations/versions and migration behavior for existing
  rows. Same-format rows have no persisted reservation marker today; do not
  infer that every old v2 row passed a new expansion gate.
- Keep historical safe abort available. An old oversized row may require a
  separately reviewed bounded inspection/recovery route; it is not permission
  to truncate/rewrite the row or reject abort after prior commits.
- Keep current API, compiler codecs, and artifact formats unchanged unless a
  separately authorized feature explicitly changes them.

### Size calculation

- Deep-copy the exact expansion state and replace only phase, cursor,
  rows/chunks, and the forward verification-map reservation described in
  FINDING.md. Retain all exact native metadata and reverse root bytes.
- Serialize the complete representative; component sums must include every
  key, comma, colon, escape and root byte. Avoid float conversion of N.
- For a future native limit, prefer an actual same-connection scalar byte-length
  observation of the exact immutable representative. The accepted finite
  spacing experiment is useful supporting evidence, not proof for arbitrary
  catalog data or all future serializers.
- Check canonical parameter size before transferring it. Fetch only the native
  length for admission, not a second full large native text object. Do not claim
  this alone bounds host peak RSS or all database work.
- Add safe typed failure codes with operation context and no metadata echo.
  Distinguish unsupported serialization from a measured over-budget envelope.

### Progress invariant and transaction behavior

- Use exact expansion N. No artifact-counter cap may be silently imported.
- If a pre-SQL guard is selected, validate proposed counters before crypto and
  incrementing SQL: exact nonnegative integers, nonempty returned batch,
  0<=chunks<=rows<=N and proposed_rows<=N. Preserve the previous committed state
  when refused. Cursor identity/order still comes from supported native types
  and ordered queries; lexical comparison of bigint strings is wrong.
- Decide compatibility explicitly before applying a new validator to resumed
  old states. Do not silently reuse a v3-only reference validator on v0/v1/v2.
- Keep data update and marker in one transaction. A refused proposal must leave
  a prior valid committed prefix abortable. Unknown commit outcomes remain
  inspection-required, not claimed rollback.
- Verify native statement/parameter adaptation, lock behavior and rollback in
  a separately admitted controlled fixture. Unit source evidence is not enough.

### Bound scope

The pre-switch representative ends at EXPANDED/BACKFILLED/VERIFIED/ABORTED.
active_schema first enters during switch; PENDING/ACTIVE, reverse
PLAINTEXT_PENDING/PLAINTEXT_ACTIVE, and the source DEPROTECTING row have additional
or different fields. Their existing paths are not silently covered. If a later
bounded journal consumer reads them, it needs a separate exact reservation and
compatibility decision.

A size-only helper does not establish physical PK/column/ACL safety or authenticated
history. Keep those proofs separate. The proposed relation validator's ACL policy
and dependency classification are still explicit design decisions, not assumed
facts about current journals.

## Finite future validation plan after explicit implementation admission

First select a single observable contract. Do not run this list as an automatic
campaign. Prepare one deciding test file and its explicit source identity for
independent review before any execution.

1. Pure constructor equivalence: independent complete literals, both codecs,
   both directions, N=0/1 and decimal-width edges, multiple models, complete
   verification keys, exact metadata preservation, no input mutation.
2. Reservation omission controls: separately remove cursor, counter and forward
   verification reservations; each must reveal an independent underestimate.
3. Boundary classification: exact canonical/native limit-1/limit/limit+1 under
   the chosen future policy. Synthetic wire boundaries remain distinct from
   product-admitted schema fixtures.
4. Expansion integration: actual native metadata, refusal before durable
   journal/staging publication, and reverse source/reverse-row atomic pairing.
5. Partial-prefix integration: one committed chunk, a refused next proposal,
   unchanged prefix and successful existing abort. Preserve ordinary legal
   UUID nil/max and signed-int64 min/max continuation.
6. Legacy compatibility: old artifacts still parse; old valid expanded states
   can continue under their established contract; old safe abort and idempotent
   repeated abort do not encounter any new size/counter/depth gate.
7. Explicit recovery goal: a separately authorized successor slice must prove
   authenticated recovery after a real durable forward abort, preserving old
   history and native metadata. A serializer PASS does not satisfy this case.

No tests, imports, database work, live-cell work, status command, installation,
corpus operation, credential access or Git action is authorized by this file.
