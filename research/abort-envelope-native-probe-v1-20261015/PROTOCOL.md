# Native abort-envelope representation probe v1

Status: HELD_SOURCE_ONLY. No import, collection, test, database/status command,
installed/live/corpus/cache/environment/credential read, network, install or Git
action occurred during preparation. Existing source and failure records remain
unchanged. This packet has no runnable admitted entrypoint yet.

## Primary question and boundary

On the existing root-selected PostgreSQL 16 UTF8 / psycopg 3.3.6 SA21 laboratory
route, do independently encoded synthetic pre-switch journal-state values:

1. preserve exact JSON types, values, Unicode, keys and canonical UTF-8 bytes
   through PostgreSQL jsonb::text;
2. produce native UTF-8 byte lengths equal to compact canonical length plus
   the independently counted structural colon/comma spaces;
3. remain no larger than the source-derived maximum representative E, including
   all legal pre-switch phases and their phase-only ABORTED variants; and
4. correctly distinguish canonical and native +/-1 edges at 16 MiB?

The test imports no product or pure-reference module. It uses an independent
stdlib encoder and an independently written state/envelope family. The accepted
19-method pure-unit evidence supports the earlier reference implementation, not
this new native test. This packet probes the native representation premise; it
does not integrate a product algorithm or enable a v3 format.

This cannot prove universal serializer behavior beyond the selected domain,
actual expansion admission, SQL mutation ordering/rollback, physical journal
shape/PK/ACL safety, ancestry authenticity, safe historical abort, durable
recovery, SQLAlchemy engine behavior, or release qualification. Schema and guard
values are synthetic JSON metadata, not observations of real catalog objects.

## Existing runner; predecessor is deliberately pending

Use only the unchanged underlying installed full-controls cold launcher and
runtime guard whose inert source identities are in SOURCE_INPUTS.json and
COMMAND_ARGV.json. The original external conftest is copied byte-for-byte; it
requires the fresh runner preflight and suppresses connection diagnostics.
The new body obtains only the runner's preflight-attested runtime URL in memory
during a separately authorized future run. It reads no credential file and
never prints, parses, stores or forwards that URL.

Do not invoke the other JSON transport packet's run-probe.sh or admit_packet.py
for this packet. They have a different hardcoded namespace, 61-case grid and
older predecessor. They were read only as inert runner/admission examples.

Root reports that the intervening JSON transport stage ended unsuccessfully and
its independent failure audit is ongoing. This preparation did not inspect its
live outputs or infer successful closure. PREDECESSOR_BINDING.json remains
PENDING with null review path/digest. COMMAND_ARGV.json has entry_argv=null.
No earlier successful stage may be substituted as the latest predecessor.

After independent source review, root must separately bind:

- the actual latest independently closed predecessor, including any preserved
  failed outcome and its verified shutdown/source/corpus accounting;
- current bounded read-only authority, exclusive selection and no intervening
  laboratory stage;
- the exact packet seal, own source-review digest, selected argv and safe fixed
  environment, and fresh output destinations;
- a reviewed outer admission/archival/closure entry that uses the unchanged
  runtime guard and cold launcher. This packet intentionally does not clone
  another elaborate guard or invent successful predecessor facts.

Before launch, archive the exact selected packet and selection plus the existing
selected source221 identity through root's admitted mechanism. Do not expand
installed/corpus referents during source preparation. At runtime retain normal
fresh dual-role preflight, origin checks, exclusive runner lock, stop and corpus
restoration controls. The wrapper's own origin import is unchanged infrastructure;
the new test body itself has no product import or fixture privilege path.

## Frozen case grid and expected identities

EXPECTED_CASES.txt has exactly 31 ordered external-file node IDs, using the
already source-reviewed empty external-file prefix. Compare complete strings
and their one selected test file; never strip arbitrary prefixes or match only
suffixes. Expected ordinary phases: 93 (setup/call/teardown). Unexpected skips,
xfail, failure, error, deselection, duplicate/extra/missing IDs or incomplete
phases prevent acceptance.

- 2 native record-domain cases: UUID (including nil/max) and signed int64
  (including min/max, negative/zero, and values beyond 2**53). Native typed
  ordering and native ::text are checked against independent Python values.
  UUID maximum cursor width is 36 ASCII characters; int64 is 20. These correspond
  to 38/22-byte quoted JSON cursors, not UUID-only admission.
- 19 state families: forward/reverse, zero/one scopes, UUID/int64 and two mixed
  models; Unicode/combining/astral/quote/backslash/punctuation/control strings;
  scope counts 9,10,9999,10000,2**53-1,2**53,10**16. Large scopes are synthetic
  decimal-width inputs, not population/execution/admission claims.
- 6 full-size canonical/native boundary cases, each paired with phase-only abort.
- 3 PostgreSQL rejection cases for escaped NUL and unpaired high/low surrogates.
  They require native DataError with a five-character SQLSTATE class 22 and retain
  the exact actual code. No exact unobserved subclass code is fabricated.
- 1 omission-control case: independently construct a complete ABORTED value,
  then independently observe native underestimates when verification, cursor or
  counter reservations are omitted. All three must be detected.

For each family, E is observed separately from actual shape-family states.
Nonempty families have EXPANDED, partial EXPANDED, BACKFILLED, VERIFIED, and one
ABORTED copy of each; empty families have no partial case. Forward verification
is absent or complete for all model keys. An empty verification map with a
nonempty model set is not a positive case. Reverse has no verification map.
The VERIFIED digest values are synthetic 64-hex strings; no actual value
verification or hash provenance is asserted. Chunks for complete states use
ceil(rows/5000); E reserves chunks=N, achievable via nonempty one-row chunks.

## Exact native observations and independent comparison

Every explicit execute is a fixed SELECT with bound synthetic parameters and
prepare=False. Connections are synchronous, text-format, autocommit with a
five-second connection timeout. There are no custom JSON/text loaders, global
registrations, DDL/DML, roles, grants, tables, functions, extensions, settings,
application queries, or existing-journal reads. SQL control connections and
closing semantics remain the unchanged runner's responsibility.

For every connection, a SELECT records PostgreSQL version, encoding, backend
PID and a digest of database/role identity. It requires version 16 and UTF8.
This digest is consistency evidence, not target authorization; root's fresh
preflight, runtime identity guards and selected boundary remain authoritative.

For each state value:

1. Independently encode canonical JSON with stdlib: ensure_ascii=False, sorted
   keys, compact separators and allow_nan=False. Bound parameter bytes first.
2. Execute the parameterized LENGTH_SQL, obtaining supplied UTF-8 bytes, actual
   jsonb::text UTF-8 bytes and jsonb_typeof. Require the explicit native transfer
   bound before fetching native text.
3. Execute TEXT_SQL for the same immutable parameter and fetch native text.
   Verify OIDs (lengths int4=23, text=25) and actual text result formats=0.
4. Verify reported byte lengths against actual received UTF-8 lengths. Parse
   native text with duplicate-key rejection, exact integer parsing and float/
   nonfinite rejection. Recursively compare exact types, including bool vs int,
   and re-encode to the original canonical bytes exactly.
5. Independently count structural punctuation without scanning string contents.
   Require native_bytes == canonical_bytes + structural separators. Failure
   rejects this premise even if a coarser E still appears large enough.
6. Compare each state's actual canonical/native lengths with E's actual lengths.
   E is size-only and never written as state. Native ordering is not used as
   canonical-byte identity; jsonb text and canonical bytes have separate hashes.

The two SELECTs share only an immutable synthetic parameter. They do not read
mutable tables, so there is no size-preflight/table-row race to claim resolved.
These observations do not substitute for a later same-lock real journal proof.

## Full-size edges and resource plan

All six boundary cases use real strings near 16,777,216 bytes. The simple
one-model forward UUID E has independently accepted 391 compact bytes and 21
separators. Replacing schema={} by schema={"fill":""} adds 9 compact bytes and
one separator: exact base 400 compact / 422 predicted native. Filler length
comes from these constants, not the candidate byte counter. The test verifies
the empty-filler constants with an independent encoder before allocating filler.

Canonical cases target LIMIT-1, LIMIT, LIMIT+1 canonical bytes. Their native
sizes should be 22 bytes larger. Native cases target LIMIT-1, LIMIT, LIMIT+1
native bytes. Phase-only abort is exactly 3 bytes shorter. Out-of-budget E
remains an admission rejection even if its specific abort value happens to fit.

The maximum diagnostic parameter is LIMIT+1 and maximum allowed fetched native
text is LIMIT+32 (the largest selected expected value is LIMIT+23). These small
diagnostic over-limit margins do not change the 16 MiB artifact or proposed
state-admission ceiling; they observe refusal boundaries using raw SELECT values.

Finite expected new-body work, excluding unchanged runner/preflight/origin:

- 31 sequential connections, each with one identity SELECT;
- 184 state observations, each two SELECTs (167 family, 12 boundary, 5 omission);
- 2 domain SELECTs and 3 intentionally rejected conversion SELECTs;
- 404 explicit SELECT statements total;
- 221 bounded JSONL records: 31 connection, 184 state, 2 domain, 3 rejection,
  1 omission summary. Each record is limited to 8 KiB; no raw large metadata.
- Twelve full-size native-text transfers, about 192 MiB aggregate, sequential.
  Length/full-text parameter transmission adds about 384 MiB aggregate input
  at the same boundary sizes. These are logical payload estimates, not measured
  network traffic or server memory. Do not call them a performance benchmark.

Reuse the unchanged wrapper's 600-second tests timeout and existing 180-second
faulthandler diagnostic. Root should select an outer closure-aware watchdog
that leaves room for normal stop/post-gates; no new hard CPU/address-space/RSS
cap is imposed by this packet. Planning envelope is one process, one connection
at a time and up to roughly 1 GiB observed client peak RSS including temporary
copies/driver overhead; this is a resource planning allowance, not a proven
bound. Capture child wall/user/system CPU and lifetime peak RSS externally.
Do not repeat the earlier arbitrary 30-second unit CPU limit. No parallelism,
multi-cell loop, retries, warming campaign or large Python per-character scan
is introduced. If a resource limit interrupts work, preserve the incomplete
attempt and reassess before any new separately admitted run.

## Evidence and stopping conditions

Only bounded IDs, lengths, hashes, native OIDs/formats, public domain strings,
SQLSTATE codes and connection identity digests are appended to
envelope-observations.jsonl. State records say OBSERVED_BEFORE_ASSERTIONS;
presence alone never means PASS. The corresponding successful call phase and
independent terminal audit must establish that all following checks completed.
This preserves a useful actual observation if a later comparator fails.

Stop on the first test failure (-x). Preserve every failure/resource/driver
record. No source repair, loader substitution, rerun, source-format relabeling,
limit increase, hand-edited result, or presumed successful predecessor is allowed.
Root independently reviews exact IDs/93 phases, all observation counts/labels,
the three omission detections, native gate classifications, raw argument/source
identity, and normal stopped-server/source/corpus closure. Until then this is
neither a native result nor a v3 admission. Even full scoped success leaves
physical journal, transactional safety and durable-abort recovery open.
