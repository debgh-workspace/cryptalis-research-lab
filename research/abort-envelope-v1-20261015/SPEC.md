# Pre-switch abort envelope: source-only prerequisite

Status: PREPARATION ONLY. The reference and vectors have not been imported,
compiled, collected, or executed. No product code, original document, checklist,
or selected Integrated221 file was changed. No database, live cell, corpus,
environment, credential, cache, raw phase receipt, install, Git, or network was
used. This is neither an accepted algorithm nor v3 feature/execution admission.

Review entrypoint: this file, then envelope_reference.py,
test_envelope_reference.py, NATIVE_PROTOCOL.md, and JOURNAL_VALIDATOR.md.
INPUTS.md records finite source inputs. SHASUMS.txt seals the deliverables.

## Source-confirmed facts

Selected source is candidate-cluster-retained-integrated-v2-20261015, accepted
221-file manifest identity supplied by root:
202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520.
Only the named inputs were read/hashed. This is not a whole-manifest recheck.

- migration.py:667–672 creates each model's scope, cursor, rows, chunks,
  schema and guard, then the root phase/models object.
- migration.py:707 changes cursor/rows/chunks; :712 changes phase;
  :715–740 and :847–848 add the complete forward verification map.
- migration.py:881–900 safe abort changes only phase to ABORTED.
- deprotection.py:319–323 creates the same model fields, plus layout_version
  101, source_operation_id and source_plan_digest. :349–378 and :469–470
  do not add a verification map. :481–506 abort changes only its phase, and
  separately restores the source row from DEPROTECTING to ACTIVE atomically.
- active_schema first enters at migration.py:792 or deprotection.py:419.
  It is outside the pre-switch ABORTED envelope. The active source row's own
  schema and size requirements are not replaced by this proof.
- compiler.py:284–292 and :367–376 admit UUID and native signed bigint primary
  keys, not UUID alone. migration.py:569 decodes by record codec, and :707
  serializes the last native key with str(). UUID text is 36 ASCII characters;
  signed int64 text is at most 20, including its minus sign. Their JSON strings
  occupy at most 38 and 22 UTF-8 bytes. NULL occupies 4.
- _scope (migration.py:607–617) increments a Python integer. Existing journal
  rows/chunks have no 16-digit validator. The artifact decoder's integer rule
  (manifest/parser.py:34–43) is a different boundary.
- A backfill chunk is nonempty and the API admits chunk_size 1..5000. A cursor
  orders a single non-null primary key. The stopped-writer contract, exact native
  result types, monotonic continuation, and atomic marker/data transaction still
  need runtime proof. They are not supplied by a byte counter.

## Exact field envelope

Let Q(s) be the exact byte width of a UTF-8 JSON string, with ensure_ascii=False.
Let C(x) be compact canonical bytes, sorted object keys, separators comma/colon
without whitespace, allow_nan=False. Sorting affects identity, not length.

For an object with k members:

    |C(object)| = 2 + max(k-1,0) + sum(Q(key) + 1 + |C(value)|)

For an array with k members:

    |C(array)| = 2 + max(k-1,0) + sum(|C(value)|)

The reference uses these equations and exact string escaping. It does not use a
character count or an average bytes-per-character multiplier. Unicode scalar
values, quoted strings, backslashes, and short/control escapes are counted.

Freeze the exact native expansion observations in each model. For table t,
let N_t be its immutable expansion scope.count and d_t the decimal width of
N_t (d_t = 1 when N_t = 0). Reserve these field values:

| Field | Expansion value | Maximum before switch/abort |
|---|---|---|
| phase | EXPANDED | BACKFILLED, 10 unescaped ASCII characters |
| models keys | exact admitted table UUIDs | unchanged |
| scope.count | exact nonnegative integer N_t | unchanged; d_t bytes |
| scope.membership | exact 64 lower-case hex digest | unchanged; 66 bytes with quotes |
| cursor | null | null if N_t=0; otherwise UUID string width 38 or int64 string width 22 |
| rows | 0 | exact integer N_t, d_t bytes |
| chunks | 0 | exact integer N_t, d_t bytes |
| schema | actual full expansion facts | exact unchanged bytes |
| guard | actual full guard/inventory array | exact unchanged bytes |
| forward verification | absent | every exact table key maps to 64 lower-case hex; all entries reserved |
| reverse layout_version | 101 | exact integer 101, 3 bytes |
| reverse source_operation_id | canonical nonzero UUID | unchanged, 38 bytes with quotes |
| reverse source_plan_digest | 64 lower-case hex | unchanged, 66 bytes with quotes |
| proposed forward aborted_forward | approved exact summary | unchanged, entire encoded subtree included |

The proposed aborted_forward shape is the design review's exact schema/root/
predecessor/count/digest object. Its root format is one of the exact admitted
v0/v1/v2 forward names. History count is a positive artifact integer <=2**53-1.
It is independent of per-table N_t. The reference supplies a shape validator;
it cannot authenticate or verify ancestry. No old row is amended. No new reverse
journal field is required. The proposed reverse artifact's
retirable_aborted_reverse summary is not silently inserted into reverse state.
If a later design adds any immutable field, that exact field must be included
at expansion and separately reviewed before execution is enabled.

For one model with six exact fields, the compact maximum is:

    147 + 3*d_t + cursor_width_t + |C(schema_t)| + |C(guard_t)|

The 147 includes model member names/punctuation and the scope skeleton plus
its quoted 64-hex membership digest. When N_t=0 use cursor_width_t=4; otherwise
use 38 for UUID or 22 for int64. The implementation derives this structurally,
not from the constant. The complete model mapping, root fields, optional frozen
lineage, and complete verification mapping are then counted with the object
equation. No independently summed component silently omits a comma or key.

The maximum representative intentionally combines BACKFILLED with a verification
map. It need not be reachable. It is a size-only value, never a journal update,
observed state, inferred fact, or authority. Exact schema and guard bytes are not
assumed small; the existing 4 MiB schema reservation is not a whole-state bound.

## Required new-operation invariant; no retroactive abort refusal

For a newly selected format, require exact integer rows/chunks (bool and float
are excluded), 0 <= chunks <= rows <= N_t, cursor NULL exactly at zero progress,
and nonzero chunks exactly when rows is nonzero. Validate the proposed updated
counters and canonical cursor after selecting a nonempty bounded batch and
before its incrementing SQL. Check cursor progress against native ordering, not
string lexicographic order for bigint. Freeze every other member. Each commit
must pair data and its marker atomically.

This makes d(N_t) sufficient without a manufactured maximum. The reviewer's
optional <=2**53-1 profile can separately align new journal counters with the
artifact grammar. The reference exposes that option explicitly; it is not the
default and is not an existing journal rule. Independently, native single-PK
domains contain no more than 2**128 UUID or 2**64 signed-int64 distinct values.
That mathematical observation does not prove runtime membership, concurrency,
or parser compatibility, and is not used to silently accept arbitrary counts.

Compute E after all exact expansion metadata exists, but before that expansion
transaction commits. If either |C(E)| or the server's actual UTF-8
octet_length(convert_to(E::jsonb::text,'UTF8')) exceeds 16 MiB, roll the entire
expansion back. Keep the existing 16 MiB artifact limit unchanged. The native
transfer ceiling here is a proposed prerequisite, not an existing product rule.

Any subsequent failed proposed chunk must leave the prior committed state
untouched. Rejecting a new proposal must not disable its prior safe-abort path.
Do not add a new size/canonicalization/counter cap at abort and discover an
unreserved field after committing expansion. In particular, do not retrofit
the reference validator or optional counter profile into old v0/v1/v2 abort.
Oversized historical terminal state may be a read-only successor-scope refusal;
it is never permission to rewrite/truncate that state or to block old abort.

Within the stated invariant, ABORTED changes only phase from EXPANDED or VERIFIED
(8 characters) or BACKFILLED (10) to 7. It shrinks by 1 or 3 bytes. Any forward
verification map already present remains; no receipt, timestamp, error text,
terminal self-digest, or lineage update is added. Therefore an admitted E
dominates every legal resulting abort state. This is conditional source/math
reasoning, not a demonstrated runtime property.

## Reference scope and explicit omissions

envelope_reference.py has no product imports or I/O. Its byte counter admits
only exact dict/list/str/int/bool/None objects, ASCII property names, valid
Unicode, and at most 32 nested containers. It rejects floats, NaN, infinity,
Decimal, UUID objects, tuples/subclasses, cycles, NUL, and lone surrogates.
Duplicate members must be rejected before dict construction; a supplied dict
cannot prove duplicates were absent in its input. Its separate object-pairs
hook demonstrates that boundary. Raw wire decoding/materialization limits
remain a required outer boundary; this code is not a complete hostile-input
parser or streaming JSON decoder.

schema and guard have type checks, exact frozen-byte semantics, and full size
accounting here, but not their product/native semantic validators. Synthetic
vectors use explicit placeholders. Passing them admits no catalog or journal.
No source pin, target, external approval, lineage hash chain, role graph,
physical relation, artifact dispatch, database type loader, transaction, or
result-row authenticity is proved by this module. It is not a feature patch.

The integer counter avoids Python's int-to-str digit ceiling while counting.
Actual JSON serialization of enormous/corrupt integers can still fail under
interpreter or PostgreSQL numeric limits. Those cases remain explicit refusal
or unknown preparation outcomes, not assumed round-trips. A decimal token
parser, memory preflight, driver loader behavior, native Unicode escaping,
jsonb numeric normalization, and canonical re-encoding require the protocol.
There is no truncation, modulo conversion, numeric coercion, or skipped row.

test_envelope_reference.py contains unexecuted vectors for primitives, byte
escapes, negative bigint cursors, UUID zero record values, duplicate keys,
bool/int aliases, 32/33-container depth, repeated subtrees, exact N digit
boundaries including 17 digits, optional cap rejection, both directions,
ABORTED shrinkage, frozen metadata changes, exact budget +/-1 edges, and
omission controls for verification/cursor/counter reservations and extra fields.
No PASS total is claimed. Native bytes and physical relation validation still
require independently admitted SELECT-only or controlled-transaction evidence.

## Decisions and stop conditions

1. Root reviews this packet and independent math/source review before execution.
2. Native serialization and constructor comparisons may be selected separately.
   Their exact limited question is in NATIVE_PROTOCOL.md.
3. Root must choose the ACL policy and counter admission profile before any
   implementation. JOURNAL_VALIDATOR.md specifies the narrow candidate.
4. Stop on an unproved serialization/type/overflow/truncation/locking case;
   report its exact boundary. Do not call it a safe pass or broaden authority.
5. The full v3 reverse-artifact envelope, ancestry protocol, genuine producer
   recovery campaign, controlled faults, cutover helper authority, final
   removal, and durable-recovery qualification remain open. This prerequisite
   does not close them.
