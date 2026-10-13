# C7: fixed-scope scan as a confidentiality baseline

**RESEARCH PROPOSAL, 2026-10-13.** No product runtime change, new database run,
provider call, API integration or search admission. This card supplies a bounded
comparison for the existing LSDD-PG-v1 research direction. It does not replace
the security contract, qualify CF1, or complete the stronger indexed-search goal.
C1 and C5 remain failed/held; the separate C6 A/A diagnostic changes neither.

## Decision

A trusted client that fetches the same complete authorized scope for every
predicate can avoid disclosing the predicate-dependent row set, result size and
deterministic query token to a passive database observer. That is a useful
stronger **query-transcript baseline**, with linear read/decrypt cost. It is not
automatically stronger snapshot confidentiality. The representation matters:

- Scanning **packed-equality CF1** keeps the snapshot equality classes exposed.
- Scanning **storage-only CF1** has no equality term. It can combine the scan's
  query behavior with the existing randomized payload's declared snapshot
  boundary, which still exposes lengths, NULLs and public linkage.

The current adapter must not silently select either scan as a replacement for a
refused query. Architecture's exact data paths forbid implicit full-table
decryption/filtering. An explicit bounded application workflow is already a
research control in blueprint sections 5–6; a public profile/API would require
new decisions and all applicable admission gates.

## Exact current CF1 evidence

Source scope is the unchanged S17-derived tree. `manifest/declaration.py:169–174`
requires accepted leakage to match declared capabilities and makes `unique`
imply `equality`. `manifest/compiler.py:456` chooses storage-only exactly when
the declared query list is empty. The actual format is in `crypto/cf1.py`.

| Existing metadata | Storage-only, `queries=[]`, `accept_leakage=[]` | Query-enabled packed equality | Consequence |
| --- | --- | --- | --- |
| Magic and suite | Five fixed bytes | Same | Identifies format, not a value equality tag |
| Flags, byte 5 | 0 | 1 | Discloses representation; current implementation rejects companion/other flags |
| Payload generation, bytes 6–9 | Public nonzero generation | Same | Reveals key/rotation cohort, not a direct value term |
| Search generation, bytes 10–13 | Zero | Public nonzero generation | Storage-only has no varying search-generation field |
| Equality term | **Absent** | 32 deterministic bytes at `[14:46]` | Same-value partition within the stable tenant/field/search-key generation; full width does not conceal frequency |
| Nonce | Starts at byte 14 | Starts at byte 46 | Fresh random 12 bytes; bytes 14–45 of a storage frame are not a tag |
| Frame length | UTF-8 bytes + 42 | UTF-8 bytes + 74 | Exact encoded length; zero-length text is identifiable among non-NULL frames |
| SQL NULL | No frame | No frame | Presence/NULL bitmap is exposed and unauthenticated |

All eight frozen public vectors were structurally inspected: four storage vectors
have a 14-byte header and zero term bytes; four equality vectors have a 46-byte
header and 32 term bytes. Receipt: `evidence/c7-cf1-metadata-inspection.json`.
This was fixture parsing/source inspection, not a fresh cryptographic test or
proof. No hidden equality term or new storage-only contract defect was found.

Public row IDs, tenant IDs, table/field identities, row count, public columns,
access/write times and old copies remain additional observations. IDs and the
descriptor digest are expected context/AAD inputs, not extra secret CF1 fields.
Length and NULL information can support inference, and differing lengths prove
inequality. Equal zero lengths identify empty strings. Therefore even storage-only
must not be described as hiding every equality relation or frequency inference.

Dropping the B-tree does not erase the packed term. Truncating it in-place breaks
authentication: both the complete header and representation descriptor are bound
into AAD. Removing this capability needs an approved representation transition,
fresh nonce/reseal, new descriptor/policy binding and full verification. It must
also remove any separate deterministic uniqueness tag. Old packed frames,
indexes, WAL, backups and known row IDs retain previously learned information;
resealing does not make an earlier observer forget it.

## Narrow observer and leakage proposal

For this research control only, fix an authorized public scope, one PostgreSQL
snapshot, a fixed projection and row enumeration, and a valid equality/IN
predicate evaluated only inside the trusted client. The application and its
memory, keys and result recipient are trusted. The database executes honestly
but records its SQL, binds, reads, rows and traffic. This is not a malicious-server
completeness/freshness claim or protection against application compromise.

For any two valid predicates over that same scope, the intended **structural**
database transcript is the same: no protected predicate or list arity in SQL,
no query term, the complete same row set and byte volume, and no match-dependent
fetch/refill, LIMIT, projection or termination. Actual timings must be retained
and reviewed, not silently removed from evidence. The finite experiment cannot
prove timing indistinguishability.

Precisely, this claim covers statements, row sequences and database result counts
for successful fixed-snapshot operations. A database observer with clocks also
sees the recorded timing channel, which remains declared leakage. **No complete
transcript-independence claim is made.** A stronger timed-transcript profile would
need a separately specified scheduler, bounded pacing/buffering, timeout cover
traffic and analysis of the surrounding application, not only a fixed SQL query.

The protocol must finish the full fetch/authentication phase before evaluating
the predicate or publishing a match. It must not use matches to influence cursor
reads, backpressure, fetch cancellation or a database-visible commit. This
requires a bounded trusted buffer for this pilot. Pacing is not implemented or
claimed; another scheduling mechanism would be a separate design. Current
streaming per-value authentication alone supplies no such
whole-result behavior. Buffering is a proposed workflow change, not permission
to cache prepared keys beyond existing leases.

Budget/authentication/provider errors and cancellation are visible aborts, not
covered executions disguised as a full successful scan. Their occurrence and
cut-off point are retained as leakage. No partial success is published and no
automatic retry hides a changed snapshot. Invalid predicates can refuse before
the scan; they are outside the valid-predicate comparison. Later application
queries, actions and response traffic are not paced by this design and can
reveal or correlate the earlier predicate. These exclusions must be accepted
explicitly rather than described as universal query confidentiality.

Declared residual leakage includes scope/table/tenant choice, row count and
length/NULL metadata, query occurrence and arrival time, connection/transaction
behavior, cancellation/failure, update history and later business actions.
Choosing a smaller public partition per secret predicate would defeat the fixed
scope assumption. Client response size, logs or subsequent writes can expose the
result if the observer can see them. No hiding of user-query frequency follows
from making each individual scan structurally identical.

A fresh logical snapshot comparison must condition on the same declared public
metadata. Storage-only removes the *additional deterministic term partition*;
it is not a claim about physical history, old packed snapshots, length hiding,
authenticated NULL, erasure, uniqueness or complete/fresh answers. A hostile
database can still omit/replay rows; scanning all rows it returns does not prove
that it returned all rows that exist.

## Primary-source alternatives and transfer limits

These are mechanism comparisons, not vendor qualification or code adoption.
Sources were read on 2026-10-13; no third-party software was installed or probed.

| Mechanism | Relevant benefit | Remaining cost/leakage and relation to this card |
| --- | --- | --- |
| **L-SDd[1C], USENIX Security 2024** | Dynamic searchable index with forward and BP-II privacy; the paper gives linear encrypted-index storage, logarithmic locality and polylogarithmic overhead, including oblivious merges | Search/access/volume and permitted update history remain. Its costs concern retained update entries, not simply live rows. PG transactions, logs, recovery and uniqueness need an independent composition. Retain LSDD-PG-v1 as the selected scalable indexed target; full scan is a simpler control. [Paper, §§2–4](https://www.usenix.org/system/files/usenixsecurity24-mondal.pdf) |
| **Path ORAM, arXiv v3, 2014 / CCS 2013** | Hides logical block access patterns for equal-length operation sequences | Non-recursive accesses read and rewrite a path, approximately `2 Z log2 N` blocks; position map/stash and recovery matter. At N≈1M, Z=5, 4 KiB blocks, that formula is about 800 KiB per logical access before recursive metadata/protocol overhead. This is a derived illustration, not a PG benchmark. A variable number of accesses/results still requires a query-algorithm and length policy. [Paper, §§2–3](https://arxiv.org/pdf/1202.5150v3) |
| **SealPIR** | Retrieves a selected database element without revealing its index to the server | Requires homomorphic server work and a separate protocol. An index lookup is not arbitrary equality search over an unknown matching set; private address discovery, result multiplicity and updates remain design work. The official repository labels the library research-only and MIT-licensed. No current performance number is transferred. [Official repository](https://github.com/microsoft/SealPIR) |
| **AWS beacons** | Truncated/partitioned HMACs deliberately merge candidate classes, trading disclosure for false positives | Stable bucket/query structure and workload-dependent inference remain. Exact answers require authenticated original-predicate verification; LIMIT/offset cannot precede complete verification. Keeping Cryptalis's full packed term would undo the intended class merging. This is not fixed-scope query hiding. [Official design](https://docs.aws.amazon.com/database-encryption-sdk/latest/devguide/beacons.html), [length/partition costs](https://docs.aws.amazon.com/database-encryption-sdk/latest/devguide/choosing-beacon-length.html) |
| **MongoDB Queryable Encryption** | Stateful encrypted-query design with a stated snapshot-oriented security boundary | Current official limitations exclude persistent access and snapshots plus accompanying query transcripts/logs. This boundary is materially different from a fixed-scan transcript goal, and its database/state machinery is not a drop-in stock-PG index. [Official security limitations](https://www.mongodb.com/docs/manual/core/queryable-encryption/reference/limitations/#security-guarantees) |

Hiding one observation channel does not establish all query privacy. Search
repetition alone can support inference in schemes that otherwise hide access
patterns; see [Oya and Kerschbaum, USENIX Security 2021](https://www.usenix.org/conference/usenixsecurity21/presentation/oya).
The proposed complete fixed-scope transcript must avoid secret-dependent tokens
and per-value caches as well as secret-dependent row selection. No novel scheme
or formal security result is claimed here.

## Unavoidable costs for this scan design

Let N be scope rows, M the non-NULL rows, and L_i each protected UTF-8 length.
Stored CF1 payload bytes are `S = sum(L_i + 42)` over non-NULL rows. Each search
fetches the whole scope and authenticates/decrypts M frames: linear data movement
and crypto work even if the answer is empty. For m matching rows, row-fetch
amplification is N/m when m>0; an empty answer still costs N rows. IN-20 does not
need twenty database scans: the same full fetch can serve the one local IN
predicate. No cross-request plaintext or prepared-key cache is proposed.

Actual current `_Payload.column_expression` uses `encode(frame, 'hex')` inside
`jsonb_build_array`, and `_ReadText` decodes it. Payload text alone therefore
contains **2S bytes**, before JSON punctuation, row/tenant IDs, other projected
columns and protocol overhead. Raw-frame totals below are only a lower baseline,
not a claim that the current adapter has a binary transport optimization.

Illustration: one non-NULL field, exactly 53 UTF-8 bytes in every row. Decimal
MB/GB, no NULLs, no other fields. Transfer floors assume a dedicated 1 Gbit/s
link at ideal line rate; they are arithmetic, not measured latency or a universal
hardware lower bound.

| N | CF1 bytes | Current hex payload bytes | Hex-only transfer floor at 1 Gbit/s |
| ---: | ---: | ---: | ---: |
| 1,000 | 0.095 MB | 0.190 MB | 1.52 ms |
| 10,000 | 0.950 MB | 1.900 MB | 15.2 ms |
| 1,000,000 | 95 MB | 190 MB | 1.52 s |
| 1,000,000,000 | 95 GB | 190 GB | 1,520 s |

At 1M rows even a modeled 10 Gbit/s link needs 152 ms for the hex payload alone.
Trusted buffering needs O(S) logical bytes plus plaintext/Python/driver overhead;
64 MiB of logical data is not a 64 MiB RSS guarantee. Streaming can reduce memory
but needs separate backpressure, cancellation and publication analysis. Long
snapshots also retain database versions. No padding is included: hiding lengths
or cardinality would require additional storage, transport and format decisions.

Existing targets stay added p95 <=3 ms for equality and <=8 ms for IN-20, plus
the specified storage comparison. These calculations suggest a small bounded
workflow, not a claim that scan meets the general target. Any different envelope
requires explicit owner approval; no target is relaxed by this research.

## Minimal finite experiment proposal, NOT RUN

**First decision:** authorize an isolated research workflow only, not an adapter
fallback. Start from storage-only fields, so no capability-removal migration or
new crypto format is needed for the pilot. Keep exact text under qualified C
equality, one field, public UUID ordering, explicit tenant scope and no uniqueness,
joins, protected ordering, range, prefix, aggregate or general Boolean expansion.

Proposed caps are 10,000 rows/scope and 64 MiB logical buffered data. They are
research safety limits, not approved product limits. Exceeding a cap, losing the
snapshot, encountering a bad frame, cancellation or key expiry must return an
explicit failed/incomplete research outcome with no successful partial answer.
Do not extend a lease, prepare keys inside a synchronous result hook, retain keys
past their deadline or retry a changed snapshot as the same answer.

1. **Native oracle and corpus.** At N=1,000 and 10,000, use two synthetic tenants
   with frozen identities, duplicate values, empty strings, NULLs, ASCII, Unicode
   and distinct NFC/NFD strings. Freeze these 16 semantic cases: six equality
   cases (hot, rare, absent, empty, NFC, NFD), equality with a NULL-valued bind,
   five IN cases (empty, NULL-only, value+NULL, duplicates/absent, IN-20), IS NULL,
   IS NOT NULL, and two public-ID ordered LIMIT/OFFSET cases after equality/IN.
   Native direct psycopg SQL is the independent truth/membership/order/type oracle;
   unchanged native SQLAlchemy is a second path. The research evaluator consumes
   a complete admitted storage-only read and compares both projected TRUE/FALSE/
   UNKNOWN and result rows. SQLAlchemy 2.0.51 and 2.1.3 are separate cells: 64
   semantic comparison groups, with all raw outcomes retained.
2. **Transcript control.** On each fixed snapshot, all 16 predicates must produce
   the same admitted storage-read SQL/binds, scope IDs, projection, fetch count
   and transferred row/frame sequence. Record timestamps and byte counts too.
   No predicate evaluation before the full fetch/authentication phase; no native
   semantic oracle may feed the candidate's result. This is structural evidence,
   not a statistical privacy proof. Invalid grammar must still refuse through
   the current adapter; the experiment must not admit SQL over storage-only text.
3. **Snapshot control.** The existing public vectors establish term presence or
   absence, not an empirical equality-partition attack result. A later authorized
   synthetic two-history test must keep row IDs, lengths, NULLs and generations
   equal while changing the plaintext partition. Its packed-CF1 positive control
   must expose the changed partition through term equality within one key/domain;
   the storage-only comparison must have no such field. Label this an engineering
   counterexample check, not proof of computational indistinguishability. Do not
   inject dishonest small-domain search reviews to force a query-enabled manifest
   into this experiment.
4. **Bounded failure and cost observations.** Before timing, check oversize refusal,
   a mutated frame, expired prepared material and mid-fetch cancellation; require
   no successful partial result and normal explicit cleanup. For equality and
   IN-20 only, propose 10 warmups and 30 alternating native/scan samples per size
   per dependency cell. Record every observation, p50/p95, CPU/wall, bytes, rows,
   lease failures and peak memory. No outlier removal or rerun-until-pass. A
   separate plain full-scope read explains scan cost but cannot replace the
   indexed native query as the user-cost denominator.

**Finite go/no-go:** zero semantic differences, cross-tenant releases, unsafe
SQL or successful partial answers; exact structural transcript equality across
the valid corpus; no hidden equality term in the claimed storage representation;
and bounded completion within the declared resource/lease limits. Any failure
is NO-GO for this pilot. A pass allows only further architecture review. Failure
of existing latency targets blocks a claim under that envelope; an owner-approved
small-scope envelope would be a separate decision, not retroactive success.

## Decisions still required before product work

- Name and explicitly opt into the observer, leakage and authorized full-read
  scope. Decide whether bulk plaintext access inside the trusted service is
  acceptable even when the end user is allowed only narrow query results.
- Choose explicit workflow/API/result publication semantics. Preserve native
  equality/IN/NULL/bag/page behavior without presenting arbitrary Python filtering
  as transparent SQLAlchemy compatibility.
- Approve size, memory, timeout and performance budgets; define cancellation,
  buffering/backpressure, key-lease and failure behavior. Decide whether timing,
  response traffic and later actions must also be hidden.
- Keep uniqueness unsupported initially. A hidden full-value uniqueness token
  defeats the snapshot objective; an authorized client uniqueness check would
  require a separate race-safe writer contract and its own leakage review.
- For existing packed fields, approve and qualify representation migration,
  writer fencing, source/target verification, interrupted/unknown-commit recovery,
  stale-reader refusal, external restore pin and retained-reader/key custody.
  No deletion or secure-erasure assumption about historical copies is permitted.
- Retain all applicable G-ADAPTER/G-CRYPTO/G-QUERY/G-LIFECYCLE/G-PROVIDER/G-POLICY
  gates and G-RELEASE. Current full gates remain UNKNOWN. Expert review and a
  formal leakage/composition argument are separate from a finite native test.

Canonical owners: [architecture, exact data paths](../architecture/README.md#exact-data-paths),
[security, format and leakage](../security.md#cryptographic-format),
[compatibility, admission and budgets](../compatibility.md#capability-admission),
[lifecycle, representation changes](../lifecycle.md#changes-and-rotation).
The prior LSDD-PG-v1 card remains in the held C1 workstream and blueprint sections
5–6 / REV-10; this comparison does not reopen C1 or C5 performance gates.
