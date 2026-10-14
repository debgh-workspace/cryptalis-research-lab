# A5: Native client UUID default timing

Status: source investigation and prepared native oracles. No database tests ran.
All 204 inherited S19 files remain unchanged. No runtime change is proposed as
qualified, and no new protected operation is admitted by this candidate.

## Classification

Polar's `Feedback` inherits `RecordModel` (`server/polar/models/feedback.py:27`).
`IDModel.id` is `mapped_column(Uuid, primary_key=True, default=generate_uuid)`
(`server/polar/kit/db/models/base.py:70–73`). `generate_uuid` calls `uuid.uuid4()`
(`server/polar/kit/utils.py:9–10`). This is application/client generation,
not SERIAL, IDENTITY, a PostgreSQL expression or another server default.

The canonical design selects application-generated UUIDs and forbids
server-generated identities. It does not independently qualify every client
default timing. The implemented walkthrough is explicit:

- `docs/walkthrough-sqlalchemy.md:18`: assign row/tenant identities before flush;
  a Python default does not replace assignment.
- `tests/test_sqlalchemy_adapter.py:854–864`: a callable-default mapping is
  covered only when the application explicitly supplies the UUID.
- `manifest/compiler.py:296–301,377–378`: callable/scalar Python defaults are
  not classified as server generation. Such a mapping can be used with explicit
  IDs, so accepting its schema does not establish implicit-default execution.

Therefore the observed Polar route is a documented, unqualified timing gap.
It is not a regression in a previously admitted implicit-default operation and
must not be described as server-generated-key refusal. The blueprint already
tracks this distinction in ORM-ID-01 / B-ORM-05. Its proposed work is evidence
planning, not permission to bypass the canonical boundary.

## Exact current refusal and native sequence

S19 `sqlalchemy.py:782–819` prepares pending rows in `before_flush`. At 793 it
reads the loaded record attribute; 801–802 refuses `NO_VALUE` or NULL. The call
is at 931–940, before native default execution. Separately, 846–862 expects a
known record parameter and an already-sealed payload at `before_execute`.
`_Payload.process_bind_param` at 193–199 requires a current operation-bound
`_Sealed` object; ordinary protected plaintext cannot reach a driver bind.

The installed SQLAlchemy sources establish this sequence:

| Stage | SQLAlchemy 2.1.3 source | SQLAlchemy 2.0.51 source |
|---|---|---|
| Native `before_flush` | `orm/session.py:4572` | `orm/session.py:4381` |
| Execute native flush unit | `orm/session.py:4636–4640` | `orm/session.py:4445–4449` |
| Before-execute events then execution-context construction | `engine/base.py:1630–1670` | `engine/base.py:1605–1645` |
| Construct each compiled parameter group | `engine/default.py:1660–1678` | `engine/default.py:1408–1424` |
| Process native defaults | `engine/default.py:1694–1695` | `engine/default.py:1440–1441` |
| Invoke callable once per native parameter group | `engine/default.py:2614–2634` | `engine/default.py:2369–2389` |
| Apply bind processors after defaults | `engine/default.py:1697,1771–1789` | `engine/default.py:1443,1517–1535` |
| Assign generated identity after successful execution | `orm/persistence.py:1194–1200,1253–1261` | `orm/persistence.py:1191–1197,1250–1258` |
| Native failed-flush rollback | `orm/session.py:4678–4680` | `orm/session.py:4487–4489` |

The source inference is that default evaluation is late, but still before the
database INSERT. A callback can return a UUID while the ORM object's `id`
remains absent until execution succeeds. The prepared tests establish this at
the real PostgreSQL boundary; source reading alone is not execution evidence.

## Mechanisms considered

### Reject eager identity assignment

Calling a default in the constructor, `before_flush`, `before_insert`, or
`before_execute` changes native ordering. It can also change callback context,
call counts, dependency/default ordering, error wrapping and whether a generated
ID survives a failed flush. Calling arbitrary callbacks twice or manually
assigning the returned identity is not an acceptable compatibility correction.
The test's separate explicit-ID suppression control is a native behavior check,
not an app adaptation or substitute for its missing-ID path.

### Do not defer plaintext to a cursor rewrite

`before_cursor_execute` occurs after bind processing. Keeping the current
sealed-only `_Payload` guard means an ordinary unsealed value fails before that
event. Relaxing the guard to emit placeholder bytes or passing plaintext through
it would create a new security boundary and difficult insertmanyvalues/batch
reassociation. This investigation does not implement that route.

### Candidate investigation: after native defaults, before bind processing

The most direct source-level experiment would retain native default evaluation
and native postfetch identity assignment. Only after *all* defaults for a native
execution context finish, each compiled parameter group has its generated UUID,
explicit tenant and ordinary field values together. At that point local sealing
could occur before the existing sealed-only payload bind processor.

This is an unimplemented direction, not an approved or proven design. The
installed engine offers the private `_process_execute_defaults` implementation
at that boundary. No sufficient public event at this exact point was identified
in the inspected native path. An owner-scoped execution-context customization
there needs explicit review because the architecture calls for public hooks.
It also needs proof that the insertion originates from the exact native UOW
invocation. A flag, caller execution option, row index, or value-only match is
not adequate insertion authority.

Required properties before even a bounded correction can be considered:

1. SQLAlchemy invokes the original callback at its native phase, once per row
   per attempt. Do not wrap, replace, evaluate or reorder arbitrary defaults.
2. Preserve ordinary original values for every context-sensitive default until
   all defaults complete. A protected-value wrapper visible to a later callback
   is a semantic change, even if it compares equal to a string.
3. Seal each parameter group's own returned exact UUID, explicitly supplied
   tenant and protected values. Do not associate rows by an unqualified batch
   order, callback index, global last-row state or identity assigned to objects.
4. Bind authorization to the actual native UOW/statement/execution context and
   current operation. Clear it on success, failure, cancellation and rollback.
   Raw/Core paths and absent or mismatched context remain refused.
5. Leave `_Payload` sealed-only. Omitting the new boundary must fail closed
   before the raw cursor; it must never yield plaintext or usable placeholders.
6. Keep provider work in the existing async preparation boundary. S19
   `_Session._keys` at 896–900 awaits before native flush; sealing must use only
   those admitted local keys. No await/provider/network work in bind processors.
7. Preserve native failed-flush state, callback side effects and retry behavior.
   Let native postfetch assign IDs after successful execution; do not repair
   object IDs or transaction flags manually after a failure.
8. Keep missing/default-generated tenant identity, SQL-expression defaults,
   server-generated IDs, mutable IDs and unsupported protected defaults refused.

No source change to any of these security-sensitive boundaries has been made.
Root approval is required before creating a runtime prototype of this direction.
If approval or exact association proof is unavailable, retain the documented
refusal and count the actual Polar adoption gap honestly.

## Prepared minimum independent oracles

`tests/test_sqlalchemy_client_default_boundary.py` contains ten planned cases:

- Four native cases: sync/async × zero-argument/context-aware UUID callbacks.
  Omitted IDs remain absent through construction, before-insert, callback and
  cursor events, then appear through native postfetch. A two-row batch calls
  each default once; context-aware defaults see original strings. A separate
  explicit-ID insert suppresses the callback. Independent owner reads verify
  committed row identity/value correspondence. The cursor collector must see
  known plaintext in this native control, establishing collector sensitivity.
- Four native cases: sync/async × callback failure/public NOT NULL failure.
  Require exact callback cause or PostgreSQL SQLSTATE 23502, native inactive
  failed Session, no assigned IDs or committed rows, explicit rollback, and a
  successful retry with exactly one new callback invocation per row.
- Two current attached cases: sync/async omitted-ID writes after a real empty
  protection transition. Planning admits the mapping, then flush raises the
  current typed refusal with zero default invocations and zero INSERT cursor
  events. These are refusal evidence, not compatibility passes.

No database tests ran during preparation. All syntax checks are static only.
Coordinator-only commands, using existing pinned interpreters and unchanged
preflight in this candidate:

`scripts/test_postgres.py -- -q tests/test_sqlalchemy_client_default_boundary.py -k native`

`scripts/test_postgres.py -- -q tests/test_sqlalchemy_client_default_boundary.py -k current_attached`

The first selects eight native controls; the second selects two current refusal
controls. Do not relabel them as a corrected protected implementation.

## Further deciding tests for an approved implementation

The eight native controls must become native/attached differential tests while
keeping their callbacks and observed states unchanged. The two current-refusal
controls remain historical evidence until explicitly superseded. Then add:

- Cold async provider failure/cancellation before defaults: zero callback and
  INSERT calls, native-like failed-unit cleanup, pool reuse after rollback.
- Local sealing failure after successful default evaluation: callback count is
  retained, no identity prematurely assigned, no INSERT, correct retry count.
- Interleaved Session/connection operations and mixed explicit/implicit IDs,
  repeated/default-equal values and duplicate returned UUID constraints.
- Context-sensitive public defaults reading protected plaintext and generated
  ID after the original callback. Missing tenant stays refused, and attempted
  context substitution cannot select another row or tenant.
- Real prepared-value/cursor collector calibration, exact independent CF1
  decoding, wrong-context rejection, omitted-boundary failure, and stale token
  reuse refusal. Do not reuse parent row order as the expected decoder context.
- Native SAVEPOINT failures, mapper events that alter pending data, callback
  exception before later callbacks, mapper cache reuse and actual unchanged
  Polar Feedback creation. F's real native app baseline remains indispensable.

This fixture does not reproduce Polar relationships, JSONB defaults, timestamp
defaults, services or route authorization. It qualifies none of them. All seven
production gates remain UNKNOWN and S19 remains the prior bounded runtime.
