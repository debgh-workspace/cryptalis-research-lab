# Native byte comparison and fault questions (NOT RUN)

## Scope and deciding question

Only root's later explicit launch selection may execute this protocol. The
initial scope is parameterized SELECT-only PostgreSQL 16 UTF8 comparison of
synthetic, nonsecret state values, independent of product imports and application
tables. It needs no role, ACL, schema, helper, provider, or credential change.
Do not read a real journal or connect to an assumed endpoint without that launch.

Question: does the exact app-compatible canonical representation round-trip
through the intended driver and PostgreSQL jsonb, with no changed scalar type,
value, Unicode, keys, or number, and do native text lengths of all scoped
pre-switch values remain no larger than native text length of E?

This does not prove actual expansion rollback, complete recovery, transaction
terminal state, hostile catalog safety, or lock behavior. Those need the separate
controlled fixture stage below and separate authorization.

## Exact SELECT-only comparison

Use one intended PostgreSQL connection with the selected native version/encoding
and driver stack recorded. First obtain server_version_num, server_encoding,
client_encoding, current_database(), current_user, and pg_backend_pid() through
read-only catalog/config SELECTs. Values identifying an actual target must be
compared with the launch's approved identity; do not infer a different target.

Bind an exact UTF-8 JSON string generated independently with Python stdlib
json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',',':'),
allow_nan=False). Never interpolate values into SQL. Retain parameter byte
length and SHA-256; receipts need no metadata free text. The comparison statement:

    WITH supplied AS (
        SELECT CAST(%s AS pg_catalog.text) AS wire
    ), parsed AS (
        SELECT wire, CAST(wire AS pg_catalog.jsonb) AS j FROM supplied
    )
    SELECT
        pg_catalog.octet_length(pg_catalog.convert_to(wire, 'UTF8')) AS supplied_bytes,
        pg_catalog.octet_length(pg_catalog.convert_to(j::pg_catalog.text, 'UTF8')) AS native_bytes,
        j::pg_catalog.text AS native_text,
        pg_catalog.jsonb_typeof(j) AS root_type,
        j = CAST(wire AS pg_catalog.jsonb) AS same_jsonb
    FROM parsed

The last equality is only a transport sanity observation; it is not an
independent round-trip oracle. It intentionally does not authenticate state.
Read native_text as text, not as an implicitly configured JSONB Python loader.
Verify its reported wire type/driver behavior separately. Decode it independently
with duplicate-key rejection, exact integer parsing, floats forbidden, strict
Unicode checks and the 32-container bound. Compare recursively with exact types;
Python's True==1 and 1.0==1 must not pass. Re-encode with the independent canonical
encoder and require byte-for-byte equality with the original parameter bytes.
If any key order changes, canonical re-encoding handles it; do not compare raw
jsonb::text to compact canonical bytes.

Require:

1. supplied_bytes equals independently encoded UTF-8 parameter length.
2. native_bytes equals the locally measured UTF-8 length of native_text.
3. canonical bytes from native_text equal the original canonical bytes exactly.
4. reference canonical count equals the independent canonical length.
5. Record whether native_bytes equals canonical bytes plus one byte for each
   colon and comma outside strings. The reference's candidate equality is a
   hypothesis to verify, not the native gate itself.
6. For each legal scoped state s, compare native_bytes(s)<=native_bytes(E) and
   |C(s)|<=|C(E)|. Use actual server observations, not the spacing hypothesis.

Object key reordering does not change length. Literal commas/colons in strings
do not count as separators. Numeric exponent/decimal tokens are outside this
journal grammar; never treat jsonb value equality as preserving their original
numeric lexical form. JSONB may reject U+0000 or malformed surrogate values;
record the exact typed failure rather than dropping/replacing characters.

## Vector matrix and boundaries

- Both directions; UUID and signed-int64; 0, 1, 9, 10, 9999, 10000,
  2**53-1, 2**53 and 10**16 scope counts for sizing comparisons. The latter
  values are synthetic width vectors, not executable table populations.
- All reachable phases; no cursor then max-width cursor; empty and complete
  forward verification maps only as permitted by actual reachability. Reverse
  has no verification map. Include abort from each actual pre-switch phase.
- Immutable schema/guard/proconfig strings containing ASCII, quote, backslash,
  newline, every other allowed control, accented text, CJK, astral characters,
  combining sequences and punctuation that resembles JSON separators.
- Distinct native order of signed bigint keys, especially negative to positive;
  do not substitute lexical string ordering. Include UUID all-zero as a record
  key, while keeping operation/table UUID validators nonzero.
- 32-container acceptance and 33-container refusal before casting; unsupported
  scalar types, bool counters, duplicates, malformed UUID/digest, unknown fields,
  NUL/surrogates, scientific notation and fractional counter rejection.
- Canonical and native +/-1 around 16,777,216 bytes. Tune one allowed ASCII
  metadata filler from the independently computed overhead; report both lengths.
  Native spacing means canonical-at-limit may exceed the native ceiling. Do not
  collapse these two cases or increase the limit to make them fit.
- Omit verification/cursor/counter reservations one at a time and require the
  independent positive state to exceed the faulty envelope. Add an unreserved
  field and require the exact-shape oracle to detect it. An omission control
  failing for an unrelated parser error is not sensitivity evidence.

For boundary-scale payloads, first request only lengths and bounded digests or
identifiers; fetch complete synthetic native_text only within the explicitly
approved transfer/memory budget. No real metadata needs to appear in receipts.
If bytes are truncated by driver/tool/output, mark the comparison incomplete.
Do not hash a truncated display and report it as the parameter's digest.

## Optional controlled-transaction stage: separately selected

Use only an explicitly admitted isolated fixture, exact source pin, bounded
input set, and existing authorized role identities. Do not widen grants or use
the final-removal helper as a convenience. Start with independent native schema,
row, owner, ACL, PK/index, trigger/rule/policy/dependency and journal observations.

Deciding fault questions:

1. If actual maximum canonical/native bytes exceed the ceiling at expansion,
   does the transaction roll back every additive column/index/guard/new row,
   preserving the original native representation and every predecessor row?
2. At each byte boundary, can every committed pre-switch state then ABORT without
   a new size check failing? Does the abort marker retain all fields except phase?
3. If a proposed next chunk violates rows+batch<=N or type/cursor invariants,
   is refusal before SQL, and is the previous committed prefix still safely
   abortable? If failure occurs after SQL but before marker commit, is rollback
   complete? Do not count an abort-blocking limit as a safety success.
4. Does a real native DDL/marker error after partial uncommitted expansion leave
   no externally committed staging? Read the actual terminal transaction state.
5. Does reverse abort restore its source phase in the same transaction, without
   applying the terminal-ABORTED shape/budget to the ACTIVE source row?
6. Can a concurrent sibling insert, shape/PK replacement, changed owner/ACL,
   rule/trigger, RLS or dependency escape the chosen journal lock and late
   validator? Verify lock order and actual grants separately. Administrative
   privilege changes are not assumed to be frozen by a table lock.
7. Are exact old-format abort and idempotent completed-abort contracts unchanged,
   including after a later successor? No generic new envelope gate may block them.
8. On lost COMMIT reply, can the original transaction and intended-primary
   markers/native state establish committed, rolled back, or UNKNOWN? Do not
   automatically retry writes, delete history or claim a rollback from silence.

This document does not authorize mutations, privilege changes, fault injection,
new credentials, connection changes, test collection, or launch. Stop before any
such step unless root supplies the exact independent execution admission.
