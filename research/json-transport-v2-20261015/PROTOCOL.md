# Native JSON transport probe V2

Status: PREPARED SOURCE ONLY; all runtime results UNKNOWN. No candidate change.

## Question and hard boundary

Characterize native PostgreSQL 16 and psycopg 3.3.6 result transport for the fixed
three-slot array [hex bytea, record UUID/int64, tenant UUID/text]. Compare
jsonb_build_array (OID 3802) with json_build_array (OID 114) and independent typed
native columns. The current Installed221 product remains unchanged. Its approved
source manifest is 202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520.

The source finding is reviewer-notes/search-cost-followon-20261015/FINDING.md,
SHA256 b8389e83bed200ea5af29d79bd630c54867521377fd6acfdb7a4689a42b88afb.
The selected adapter SHA256 remains
28cf5c4991aae1cb4f3baf6a5630b30d675cb2308e842ce09fd6a04ddaaf5a88.
This is not a new product implementation, C9/C10 repeat, authenticated-read test,
CF1/parser/key/AAD equivalence result, index benchmark, storage measurement, or
application latency claim. All seven broad product gates remain UNKNOWN.

## Exact runtime route and authority

Root alone may select SA21 after actual independent source/command acceptance,
current explicit read-only authority, exclusive lab quiescence and accepted prior
terminal closure. The new selection is distinct from the historical main43
BINDING_SA21/BINDING_SA20. Those unchanged accepted bindings authorize no new action;
they supply only the existing exact source221, installed43, complete installed
namespace, ordinary 2506/nonproduct 2402, interpreter, corpus26 and harness identity
admission. Use unchanged main43 verify_runtime_binding.py before and after, without
its old archive option. No historical full-main test is selected or rerun.

Use the unchanged main43 -B/runpy cold launcher, unchanged guarded corpus wrapper,
nonblocking laboratory lock, private-file fresh dual-role preflight, installed
candidate mode and the original stop/restoration path. The original wrapper's
separate package-origin subprocess imports cryptalis and byte-checks all 43 modules;
this established admission is retained. The new test body does not import any
cryptalis product module or call a product fixture. It uses only the already
preflighted runtime-role URL in runner process memory. It neither reads credential
files nor emits connection values. Existing wrapper/runner source reads, receipt
Git revision metadata and source snapshots remain unchanged runtime behavior.
No such runtime or Git operation was performed during source preparation.

Root must independently verify the meaning of each actual review and permission,
then exclusively create SELECTION_SA21.json from the held
template and supply its externally recorded digest plus the packet seal digest.
Only SA21 is selectable; it requires latest focused111 SA20 terminal hash
7318b0b3f7bac950a8e2311dd6d546d6c5f5b376c168d9eec0e0f4c4d97d7678.
SA20 is not an executable stage. Its native driver version is the same, and this
packet does not use SQLAlchemy engines. A future SA20 run requires a distinct
dependency/integration question and a separately reviewed packet. Any
intervening lab stage invalidates the recorded no-overlap/current-boundary claim;
stop and obtain a newly reviewed binding rather than pretending an old snapshot
remains latest. No second cell, retry, or post-failure repair occurs.

Before any live guard/status/database work, a single checked data-only helper
admits exact own packet/input/selection hashes, metadata-admits all 221 source files,
copies own 10-file packet+seal+current selection and source221 (233 files), and verifies exact archive
file/directory inventories and all copied bytes. It does not copy installed cells,
corpus, caches, private files or arbitrary external payload. Any nonzero producer,
copy or verification blocks runtime; partial output is retained. The checked archive
is followed by the unchanged main43 live guard and stopped-server proof.

## SELECT-only behavior

The new test source sends only fixed SELECT statements over VALUES and
 generate_series. Operands are bound parameters with fixed SQL type casts; no
identifiers or SQL fragments come from user data. Connections are autocommit, use
prepare=False, have connect_timeout=5, and close before a test ends. There is no
DDL, DML, GRANT, REVOKE, fixture, table, schema, role, extension, new cluster, KMS,
provider, credential change, installation or persistent setting. Parent supervision
retains the unchanged 600-second test timeout. Only installed SA21 is selectable;
this does not measure SQLAlchemy engine execution.

## Independent correctness and scoped loader characterization

48 ordinary parameterized cases: sync/async × default text/binary cursor ×
default/shared-connection/per-OID loader × record UUID/bigint × tenant UUID/text.
Binary is a separate explicit control; it is not an application format change.

Per type combination, cases are four payload byte lengths (0,1,74,1024), all eight
NULL masks over the three positions, and finite record/tenant boundary values.
UUID records cover non-nil/nil; bigint records cover -2^63, -2^53-1, -1,0,1,
2^53+1,2^63-1. UUID tenants cover non-nil/nil. Text tenants cover the fixed
single-tenant-shaped UUID text, empty string and one public Unicode string.
The base74-byte all-present mask deliberately overlaps the payload-width control.
Counts are 14/15/19/20 for UUID/UUID, UUID/text, bigint/UUID, bigint/text: 68 shapes
per route/format/loader family, 816 recorded native comparisons per cell.
Opaque bytes are deterministic public values, not valid CF1 frames or ciphertext.

Each SELECT returns typed p/r/t native columns and both builders. The comparator
first checks native values/types against independently configured Python inputs,
then builds expected slots using bytes.hex(), str(UUID), exact Python int and None.
It checks tuple/list types, length3, exact positional NULLs, full strings, exact
integer types/values, OIDs (17,2950-or20,2950-or25,3802,114) and actual cursor formats.
Neither JSON builder, _ReadText nor the proposed product path is the oracle.

Shared set_json_loads registrations always name the connection context. Per-OID
registrations use only connection.adapters and deliberately wrap JSON and JSONB
with different tags. Their required output is INTENTIONAL_PER_OID_DIVERGENCE,
not public compatibility PASS. The callback sequence must match the actual OID
order, including binary-loader behavior; callbacks record only class/length/tag.
Each of 48 cases snapshots all four global adapter classes, verifies untouched
fresh-connection default results before and after, and verifies connection closure
and unchanged global classes. No registration uses the global context.

Four further ordinary controls (sync/async × text/binary) obtain genuine native
observations then separately corrupt NULL placement, list length, integer type,
integer value, slot order, OID, format and native value. All 32 corrupted observations
must fail the same independent comparator. A fabricated expected failure flag is
not an oracle. Each unmodified observed baseline must first pass.

SQLAlchemy engine json_deserializer, ORM sync/async/streaming/alias/outer-join
semantics, _ReadText NULL/context behavior, CF1 authentication, key lifetime,
application errors and one-token derivative compatibility remain UNRUN here.
Observed default equality cannot erase the intentionally demonstrated OID hazard.
A subsequent product candidate requires its own design/admission decision.

## Separately declared native-cost diagnostic

Nine ordinary tests: 1/143/286 rows × 0/74/1024 public opaque bytes. Three fixed SELECT
variants use identical p/r/t input values and generate_series row counts:
typed-native output, JSONB envelope and JSON envelope. Every result includes ordered
i; every fetch is complete and every cursor closes. Text result format is fixed.
The cost record slot is i::bigint, so the envelope depends on each generated row
even when payload length is zero. All variants have the same row-dependent record;
no constant envelope is substituted for per-row construction. Payload and UUID
tenant remain fixed public bound values. No optimizer plan is measured or inferred.
There is no table, planner/index claim, authenticated work or protected denominator.

All six permutations of(native,jsonb,json) are used in their fixed itertools permutation
order of the declared tuple. Each of six blocks performs ten triplets: first two are labeled warmups,
remaining eight measured. All 180 samples per width are retained, including warmups:
1620 total samples, 324 warmups and 1296 measured samples per cell. No exclusions,
reranking, retries or trimming. Normal GC remains enabled. Prepared-statement auto
promotion is explicitly disabled with prepare=False in every statement.

Wall clock is perf_counter_ns; process_time_ns measures CLIENT process CPU only.
The timed interval includes cursor creation, execute, full fetch, actual OID/format
metadata capture and cursor close. Native has more columns; that overhead is part
of this declared diagnostic. Exact row order/type/value checks and JSONL receipt
writes follow outside timing. Connection establishment is outside timing; each
width has its own fresh connection. Input creation is outside timing. No server CPU,
wire-byte total, exclusive server materialization cost or application latency is
inferred. Use paired per-block descriptive comparisons only; retain every sample.
There is no frozen win threshold and no PASS/FAIL product performance claim.

## Exact outcomes, safe projection and stop

Per selected cell: 61 ordinary PASS, 183 passing setup/call/teardown phases, zero skips,
xfails, failures, errors, duplicate cases, extras or deselections. The frozen ordered
EXPECTED_CASES.txt is authoritative.816 transport lines,48 isolation lines,
4 negative lines (each 8 mutations), 1620 cost lines must match their exact grids.
The new body makes 2536 SELECT statements/cell: 816 characterization, 96 untouched
fresh-connection controls, 4 negative baselines and 1620 cost samples.157 native
connections/cell, plus unchanged wrapper/preflight/origin work. These are expected
source counts, not observed runtime results.

Each new JSONL receipt contains only fixed case IDs, public synthetic-value hashes,
lengths/types/null positions, OIDs/formats, safe callback descriptors, comparison
flags and timing numbers. No SQL parameters, raw frames, native credential values,
full environment, DSNs, backend errors or private reader output are emitted.
The unchanged conftest redacts operational/interface/SQLAlchemy DBAPI errors.
Failures are not suppressed, retried or converted into skips.

Terminal review must verify actual launch/cwd/fixed environment, selection and all
source/command hashes; all 61 exact cases and 183 phases; both identity guards;
archived source bytes; unchanged source/external-source/corpus identities; safe
wrapper phase exit lines; runner0; stop0 plus server stopped; independent pre/post
pg_ctl status3 with no server; and corpus26 restoration/generated-receipt accounting.
Use safe logs, runner receipt, JUnit/progress and finite maps. Never read raw
 tests.json/readiness.json/package-origin.json/postgres-start.json/postgres-stop.json
bodies or environment/cache/private-reader payloads. Existing raw files remain
unchanged and may not be treated as safe projection. Root owns current quiescence.

Stop on any comparison, callback, isolation, source identity, preflight, accounting,
archive, status or closure failure. Preserve all failed evidence. Expected custom
OID divergence is a recorded compatibility hazard and no permission for a product
change. Scope matrices, CURRENT_CANDIDATE, previews and closed prior routes remain
unchanged. No deployment, promotion or broad performance conclusion follows.

## Preserved V1 HOLD and exact V2 correction

V1 remains sealed and unexecuted at
experiments/json-transport-native-probe-v1-20261015, seal
8951d143fa8f0216bd72b79976ea52e6844853d5c317cc9697bf9d80176d6be5.
Its independent source HOLD remains
reviewer-notes/json-transport-native-probe-independent-20261015/V1_HOLD.md,
SHA256 617feb1f08a497c225887718a7c5b0109179341497efef52f59a318eff5c0389.
The HOLD found that this external-file route emits an empty module prefix. Root
and the independent reviewer established that from only the first three safe
closed progress records of the accepted focused111 SA20 V2 run; no collection was
needed. The prior accepted terminal review remains bound above.

V2 freezes the 61 exact emitted node IDs as ::function[parameter], in their original
order. Compare the complete ordered strings directly to EXPECTED_CASES.txt. Do not
strip paths, match arbitrary suffixes or invent normalization after execution.
Each function/parameter ID is unique. The COMMAND_ARGV.json emitted_case_identity
record ties these IDs to this packet's sole selected test_native_transport.py file
and its exact wrapper argv; that test source is included in the packet seal and
checked archive. Empty display module names do not broaden the selected source set.

The only intended changes from V1 are this emitted identity correction and explicit
identity contract, successor self/evidence paths and their dependent hashes, plus
binding the preserved V1 seal and HOLD as two additional safe references (21 total).
The ten-member payload and 233-file archive remain unchanged in size. All 61 test
cases, 183 phases, operand grids, expected assertions, scoped adapter controls,
prepare=False policies, sample counts and source/runtime/authority boundaries remain
unchanged. No source import, compilation, collection, test, DB/status, installation
or Git operation was used to prepare V2. No V1 outcome or HOLD was overwritten.
