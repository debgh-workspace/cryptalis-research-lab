# Native JSON transport V3: cost9 continuation

Status: PREPARED SOURCE ONLY. Runtime source acceptance, actual root selection and
accepted V2 failed-run terminal review remain required. No product candidate change.

## Preserved failure and narrow correction

V2 is immutable at experiments/json-transport-native-probe-v2-20261015, seal
 d5f457b3968d86adaa2a4f0ecaa70bd7a2a1ab73e6ebaca924de907550716377.
Its source acceptance remains reviewer-notes/json-transport-native-probe-independent-20261015/REVIEW.md,
SHA256 d3d1c24896b6d6e5c1454ba60a21cbaf15ab9e7d50f497707db58b9e1e3e6b58.
Source acceptance did not establish runtime success.

After root confirmed executor completion, the author read only the finite V2
source and safe tests.log. The safe failure log is
 evidence/json-transport-native-probe-v2-sa21-20261015/tests.log,
SHA256 56c734d863f9d54e5ce44af8c512c0c551f3d22b6aec5937ce14865774d8db8d.
It reports 52 passed and 1 failed. The first native cost SELECT exposes both i and
i::bigint with the output name i. Unqualified ORDER BY i therefore raises PostgreSQL
AmbiguousColumn. The failure occurs in the first execute, before any cost sample
is written. The source failure and all completed work are retained.

Root reported executor session 71196 completed at 18:23 UTC: coordinator shell
exit 0, inner entry exit 1, post-status 3 and all 26 corpus identities equal. These
reported closure observations are distinct from independent terminal acceptance,
which was still pending when V3 preparation began. An outer coordinator exit 0 does
not turn the failed inner run into a success. This packet cannot execute until root
binds the actual accepted V2 failed-run terminal review and a fresh exclusive boundary.

The only query correction is ORDER BY g.i, qualified against the generated relation
input alias. All three variants share that same FROM/ORDER BY tail. g.i is the
integer input column used for the leading row counter and the bigint record slot.
Qualifying it therefore specifies the same ascending generated-row order for
native, JSONB and JSON without resolving through possibly duplicate output labels.
No operand, output, cast, format, count, expected value or timing policy is changed.
This is source reasoning; no query, collection or test was executed during preparation.

## Exact selection: nine unfinished cost cases only

The retained harness still contains the completed loader/mutation functions so its
minimal source delta is independently reviewable. The sole selected node in the
exact argv is this packet's
 test_native_transport.py::test_counterbalanced_native_cost.
Only its nine parameter cases run. Neither the 48 loader cases nor the four
actual-observation mutation cases is selected or repeated. Their result must be
established by the preserved V2 terminal audit, never fabricated in V3 receipts.

EXPECTED_CASES.txt freezes nine complete emitted node IDs, in order:
::test_counterbalanced_native_cost[rowsN-bytesN], for rows 1,143,286 and bytes 0,74,1024
in the nested source order. Compare the complete ordered strings directly. No path
stripping, arbitrary suffix matching or post-run normalization is permitted.
COMMAND_ARGV.json binds those IDs to the sole selected function and exact external
source file. The source remains sealed and copied into the checked archive.

Required V3 result: 9 ordinary PASS, 27 passing setup/call/teardown phases, zero
failure/error/skip/xfail/deselection, no extra or duplicate case. There must be exactly
1620 cost observations, including 324 warmups and 1296 measured observations, and no
new transport/isolation/negative observation files. The new body makes 1620 SELECTs
on nine fresh native connections, plus unchanged wrapper/preflight/origin work.
These are expected source counts; no V3 runtime result is claimed.

## Unchanged cost protocol and independent checks

Nine widths are 1/143/286 rows × 0/74/1024 public deterministic opaque bytes. Three
fixed variants return typed native payload/record/tenant, JSONB envelope, or JSON
envelope. Payload bytea and UUID tenant are bound; record is generated i::bigint,
so each envelope depends on the row even at zero payload length. All variants use
identical logical inputs and complete ordered fetch/close. No table or fixture is
created. Opaque bytes are public synthetic values, not valid CF1 frames.

The tuple (native,jsonb,json) supplies all six permutations in fixed itertools
order. Each block performs ten triplets: the first two are warmups, the remaining
eight measured. All 180 samples per width are retained, with order, position,
iteration and warmup label. Nothing is trimmed, reranked, retried or omitted.

Every variant has identical prepare=False, autocommit=True and connect_timeout=5
policies. Each width has one fresh connection, outside the timed interval; all three
variants use it. Default text result format is fixed. Normal GC remains enabled.
Query-string construction and public input creation occur outside timing.

Wall time uses perf_counter_ns. Client process CPU uses process_time_ns; this is
not server CPU. The interval includes cursor creation, execute, complete fetch,
OID/format metadata capture and cursor close. Native has more output columns, whose
overhead is part of this declared diagnostic. Exact order/type/value assertions and
safe JSONL writes follow outside timing. Every native row is checked against the
independent bound bytes, generated integer and UUID. Both decoded arrays are checked
against independently generated hex/int/UUID-string slots. OIDs are observed directly:
native 23/17/20/2950; JSONB 23/3802; JSON 23/114. All formats must be text and each
cursor/connection must close. Global adapter class identities must remain unchanged.

There is no win threshold or product performance PASS. Retain all samples and use
paired per-block descriptive comparisons only. No exclusive server-construction
cost, optimizer plan, authenticated-read gain, index result, wire-byte total,
storage qualification or 3/8 ms application-budget conclusion follows.

## Existing route and held authority

Only installed SA21 is selectable. SA20 is not a stage; a distinct future question
would require another reviewed packet. The current source manifest remains
202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520 and all 221 candidate
files remain unchanged. Current adapter SHA256 is
28cf5c4991aae1cb4f3baf6a5630b30d675cb2308e842ce09fd6a04ddaaf5a88.
The old main43 binding is reused for identity only, not as new execution authority.

Use unchanged main43 verify_runtime_binding.py before/after without its old archive
option, exact installed namespaces, ordinary2506/nonproduct2402 maps, source221,
runtime43, interpreter/harness identities and corpus26. Use the unchanged -B/runpy
cold launcher, guarded corpus wrapper, nonblocking laboratory lock, fresh dual-role
preflight, installed candidate mode and stop/restoration path. The existing wrapper
imports cryptalis only for its established installed-origin/43-byte-match admission.
The selected test body does not import product code or invoke a product fixture.

Root alone may create SELECTION_SA21.json after actual independent V3 source/command
acceptance, actual accepted V2 failed-run terminal review, current read-only authority,
exclusive quiescence and no intervening lab stage. Actual review digests and the
selection digest must be externally recorded; missing or unaccepted review/selection
is a hard hold. The preserved focused111 review is historical context only and does
not replace this required V2 predecessor. No automatic retry or second stage occurs.

Before any live guard/status/database work, the pinned data-only helper admits the
exact ten-member packet, 23 finite safe source/map/review references and actual
selection. It metadata-admits source221, copies source221 plus own ten members,
seal and selection, and verifies exact archive directory/file inventories and all
233 copied byte hashes. No installed cells, corpus, cache, private reader or raw
phase bodies are copied. Any producer/copy/verification failure stops before live
work and retains partial output. The unchanged live guard and pre-status proof follow.

## Safe evidence and stopping conditions

The selected body sends only fixed SELECT over VALUES and generate_series, with
bound synthetic values and fixed SQL casts. No DDL, DML, GRANT, REVOKE, ACL/role,
extension, new cluster, provider, KMS, credential, installation or persistent-setting
action exists. The unchanged wrapper retains its 600-second test bound.

Cost JSONL emits only fixed width/order IDs, OIDs/formats, close/GC flags and timing
numbers. It emits no DSN, full environment, raw credentials or connection diagnostics.
The unchanged conftest retains connection-error redaction. Failures remain failures.

Terminal review must bind exact argv/cwd/fixed environment, actual selection and
accepted failed-run predecessor, all nine IDs/27 phases, exact sample grid and all
warmups/measurements, archived bytes, pre/post identity guards, unchanged source and
corpus identities, wrapper/runner exit 0, stop 0 plus server stopped, independent
pre/post status 3 and corpus26 restoration/generated-receipt accounting. Use safe
logs, runner receipt, JUnit/progress and finite maps only. Never consume raw
 tests.json/readiness.json/package-origin.json/postgres-start.json/postgres-stop.json
bodies or environment/private/cache payloads. Current lab quiescence belongs to root.

Stop on any source, archive, identity, preflight, ordering, value, OID, format,
count, callback-scope, status or closure failure. Preserve the failed evidence.
No previous failure, current scope matrix, CURRENT_CANDIDATE or preview is changed.
The OID/custom-loader hazard, product parser/CF1/key/AAD contracts and broader gates
remain outside this continuation. All seven broad product gates remain UNKNOWN.
