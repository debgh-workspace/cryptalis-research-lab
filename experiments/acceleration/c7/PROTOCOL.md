# C7 executable baseline protocol, frozen before database execution

Authorization: isolated synthetic research baseline only. The coordinator runs
PostgreSQL through the unchanged credential/role preflight. The worker prepares
files and performs static checks only. No product source/API change or admission.

Binding: S17's 195-file source manifest, SHA-256
`70a5293e76486f243305968c7a58b8fa8c6be97d5bec5508593529b9eacc49e7`.
The parent assessment is `docs/research/FIXED_SCOPE_SCAN_ASSESSMENT_20261013.md`.
Its source/vector inspection is `evidence/c7-cf1-metadata-inspection.json`.

## Exact executable scope

- A new test-only module, `tests/test_fixed_scope_scan_research.py`; no public API.
- Existing CF1 storage-only (`queries=[]`, `accept_leakage=[]`) and the existing
  public synthetic migration key fixture. No provider integration or new secret.
- Two temporary tables with identical synthetic values/IDs: plaintext native and
  storage-only protected. Empty-table fixture conversion only; no existing
  query-enabled frame is converted. Existing runtime role performs all application
  traffic. Owner role performs only fixture setup, independent inspection and
  cleanup in the newly created experiment schema, using existing fixture grants.
- Text under C equality, two explicit synthetic tenant scopes, N=1,000 and 10,000
  per tenant. Public `(tenant_id,id)` index on both tables; native equality index
  only on the plaintext oracle. Protected field has no equality index or term.
- Fourteen equality/IN cases: six equality values (hot, rare, absent, empty, NFC,
  NFD), equality with a NULL bind, five IN cases (empty, NULL-only, mixed NULL,
  duplicates/absent, IN-20), and two public-ID LIMIT/OFFSET cases. The assessment's
  separate IS NULL/IS NOT NULL cases are omitted to honor the narrower executable
  equality/IN instruction. SQL NULL three-valued truth remains tested.
- 14 cases × 2 tenants × 2 sizes = 56 comparison groups per dependency cell,
  112 across the separately run SQLAlchemy 2.0.51 and 2.1.3 cells.

The scanner accepts no predicate argument. It consumes every row and authenticates
every value through the unchanged adapter before returning a trusted buffer.
Predicate evaluation is a separate test-only function called after the scan and
its database transaction end. There is no successful early exit, match-dependent
refill or changed SQL. No keys or plaintext are cached across scans.

The fixture is unchanged during semantic/cost observations. Each scan has its own
REPEATABLE READ transaction; oracle connections use the identical immutable
logical data. No shared/exported PostgreSQL snapshot or concurrent-update behavior
is claimed. Full buffered values are checked against the frozen fixture on every
semantic scan. This qualification is necessary when comparing sequential traces.

## Observations and limits

Compare direct psycopg native SQL with native SQLAlchemy and the research
evaluator. The direct oracle uses `= ANY(text[])` for IN; SQLAlchemy uses ordinary
expanding IN. Compare complete projected TRUE/FALSE/UNKNOWN vectors and actual
database-filtered ordered/paginated rows. Neither oracle supplies candidate
outputs. Independent CF1 decoding checks the fixture values/format once before
the experiment. Its existing helper independently derives/formats keys but uses
the same AEAD primitive; this is not a new independent cryptographic review.

Structural receipts record candidate SQL/bind hashes, logical fetch partition
sizes and full buffered row/identity/value hashes. They do not expose keys or
credentials. The native plaintext oracle has a separate connection/table and is
outside the candidate privacy trace. SQLAlchemy events do not capture every
network packet or internal driver FETCH. Logical partition equality is not proof
of wire-packet equality. Record per-partition times and total CPU/wall timings;
never infer timing privacy, pacing or packet independence from structural checks.

Budgets: at most 10,000 returned rows and 64 MiB logical frame-plus-identity bytes
per scope. Checks occur during 128-row streaming partitions, so an abort may
already have fetched a partition. These bounds are not pre-transfer byte limits
or RSS guarantees. The fixture independently verifies small bounded frames;
untrusted arbitrary-width transport is outside this pilot. No secret-dependent
predicate is evaluated while fetching. Errors, cancellation and their positions
remain visible leakage; no cover traffic or masking is supplied. Later app
traffic and user response sizes remain outside the claim.

Failure controls cover a small row/byte budget, explicit cooperative cancellation
after a fixed partition, altered tail-frame authentication and expired operation
material. The damaged tail must reject both an early-match page and empty IN,
demonstrating that neither can publish before full authentication. A failure
yields no successful partial result; cleanup precedes a
fresh-session recovery control. Cooperative cancellation is not an async driver
cancellation qualification. No source cache/lease settings are changed.

For the expiry control only, the existing resolver selects a same-policy public
fixture keyring with a 50 ms lease, then pauses after a partition for 75 ms. This
narrows a test lease; it does not alter product defaults, extend issued material
or disable expiry. An early natural expiry is also a valid refusal; no post-first-
partition expiry claim is made unless progress is observed. Restore the ordinary
fixture resolver before the separate fresh-session recovery check.

Cost: equality and IN-20, both sizes, first tenant only. Ten warmups followed by
30 alternating native/scan pairs per workload. All wall/CPU observations retained.
Report empirical p50/p95, result counts and logical bytes. A plain full-scope
native read is a context control, never the denominator for indexed-query cost.
Instrumentation is included in the measured implementation. No outlier removal,
same-gate retry or shared-host noise correction. Existing 3 ms equality / 8 ms
IN-20 added-p95 targets remain unchanged and are reported, not quietly waived.
Process maximum RSS is recorded before/after cost work as a Linux high-water
mark including fixture/driver overhead; it is not isolated scan peak memory.

## Gate and stopping condition

Any semantic difference, cross-tenant release, structural difference among valid
queries over the fixed scope, missing refusal, hidden storage-only term, budget
overrun reported as success or successful partial answer fails the bounded
correctness gate. Preserve the receipt even on failure; do not widen grammar.
Cost is a separate recorded gate against the existing envelope. Failure of that
gate prevents a claim under that envelope and does not erase correctness evidence.
A pass qualifies only this experiment. All product admission/release gates and
independent security review remain required and UNKNOWN.

The coordinator may select the 1,000-row correctness case before the complete
gate. Preserve that selection and its result; do not label it the entire plan.
No worker database execution is authorized by this file.
