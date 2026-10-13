# Search and performance workstream

## Scope and finite gate

Assigned isolated 183-file S14 snapshot, base `2065cb78f3c7126f207fc62c35887ddd204925af`.
Only the coordinator publishes or promotes changes. No database commands run here.
The snapshot intentionally has no Git metadata. After the initial `git status`
failed, the coordinator explicitly authorized direct edits and pure checks.

Candidate: reuse deterministic public CF1 metadata on immutable objects.
The HKDF salt depends only on public domain, tenant, root identity and generation.
The search info tuple depends only on immutable field identity and fixed codec,
normalizer and capability. Never cache raw roots, derived keys, result plaintext,
operation state or SQLAlchemy result processors. Preserve all existing key
resolution, expiry, fork, context and authentication checks and exact CF1 bytes.

Finite pure performance gate, declared before the experiment: at least 10% lower
median in repeated short equality-frame opening and query-term generation, with
at least 7 of 9 alternating pairs favorable. No tested repeated CF1 workload may
regress more than 5%. The experiment is a local microbenchmark, not a deployment
performance claim. Frozen independent CF1 vectors, independent metadata encoding,
replacement/serialization and expiry/fork controls must pass. A PostgreSQL paired
native-result comparison and unchanged full test suites remain coordinator-run
requirements before promotion.

## Progress

- Read repository instructions and canonical security, lifecycle, compatibility,
  implementation and engineering contracts; current root checklist and existing
  S9 profile/S10 allocation evidence. All seven qualification gates remain UNKNOWN.
- Existing S10 tuple allocation correction is retained without duplication.
- No database access, provider credentials, external systems or source publication.

## Evidence and blockers

### First finite result: 2026-10-13

The implementation adds `cached_property` for the public root salt on
`KeyContext` and public search-info tuple on `FieldDescriptor`. It substitutes
these bytes at their existing use sites. HKDF and HMAC still run on each use.
The properties add no dataclass fields, change no serialized context members,
and have no global cache or reference to secret material. Retention is bounded
by the lifetimes of existing immutable context/descriptor objects. Replacing
an object constructs fresh derived metadata. Python's trusted-process object
mutability remains outside the existing threat claim.

Prototype with an explicit dictionary lookup failed the declared speed gate:
storage opening 11.6%, equality opening 9.1%, term creation 22.0% lower medians.
Its failure is retained in `evidence/public-metadata-prototype.json`.
The implemented descriptor lookup passed the unchanged gate in nine alternating
pairs (`evidence/public-metadata-implemented.json`):

| Repeated CF1 operation | Baseline median | Candidate median | Reduction | Favorable pairs |
| --- | ---: | ---: | ---: | ---: |
| Storage-frame open | 13.335 us | 12.048 us | 9.6% | 8/9 |
| Equality-frame open | 23.154 us | 18.855 us | 18.6% | 9/9 |
| Equality query term | 10.331 us | 6.887 us | 33.3% | 9/9 |

These are warm, short-value, synthetic, same-process observations with 4,000
calls per cell, not native SQL or production latency. Raw monotonic and process
CPU clocks are retained separately. Longer text, concurrent load, cold process
cost and lifecycle-wide impact are not qualified by this experiment.

Six pure independent control groups pass (0.069 s, then 0.064 s restoration):
320 exact generated transcripts; eight frozen independent vectors used cold and
warm; UUID/bigint and single/multi-tenant boundaries; exact Unicode; dataclass
serialization and replacements; changed roots under identical public metadata;
expired and post-crypto-expired leases; fork-inherited-key rejection. The
reference encoder uses `struct`, standard-library HMAC and the RFC 5869 single
block construction rather than production helpers. AES-GCM-SIV remains the
native library primitive; this is not independent cryptographic review.
In-memory mutations that omit salt context or field identity each fail the
independent transcript control. Restoration passes all six groups. No runtime
source file was modified by mutation execution.

Files/hashes are in `evidence/candidate-source-hashes.json`; exact S14 runtime
diff is in `evidence/runtime-delta.patch`. Runtime hashes:

- `src/cryptalis/crypto/cf1.py`: `fa7131cb263640eccb420cd77bb4b56ad0775f9be992e1721ba0b48ca66c727a`
- `src/cryptalis/crypto/keys.py`: `e9913d47b101c91b4bd08831e9ac365f72e9403198f8db7155a6eee62afffc0b`

### Queued coordinator checks

Runtime/test files are frozen pending these runs:

1. `tests/test_cf1_public_metadata.py`, `tests/test_cf1.py`,
   `tests/test_cf1_backend_failures.py`, `tests/test_file_development_provider.py`,
   `tests/test_file_provider_postgres.py`, `tests/test_key_lease_renewal.py`,
   `tests/test_sqlalchemy_adapter.py`, `tests/test_sqlalchemy_search.py`,
   `tests/test_sqlalchemy_thread_isolation.py`.
2. `experiments/test_public_metadata_paired.py`: one before/after retained-layout
   PostgreSQL question with native result control, 1,000 synthetic rows, seven
   alternating blocks and 40 measured queries per cell. Declared DB speed gate:
   equality and IN each improve at least 5%, with at least 6/7 favorable pairs;
   point must not regress more than 10%. Emit receipt even if this gate fails.

Only the coordinator runs these through unchanged dual-role PostgreSQL
preflights. No database command has run in this workstream. Full installed
compatibility suites and packaging checks remain requirements before promotion.
The initial missing Git metadata and later guessed runner path failures were
reported, and the coordinator explicitly authorized snapshot-only continuation.
No infrastructure repair or access workaround was attempted.

All seven full qualification gates remain UNKNOWN.

### Coordinator evidence received at 13:00 UTC

The coordinator reports the selected SQLAlchemy 2.1.3 security/native suite:
260 passed in 19.43 s, three fork warnings, unchanged source and stopped server.
The single paired PostgreSQL question passes its declared gate. Reported
median-of-block-medians: equality 9.123451 to 6.995368 ms (23.325%, 6/7 favorable),
IN2 14.784648 to 11.9245555 ms (19.345%, 7/7), point 1.995375 to 1.9053835 ms
(4.51%, 4/7). Corresponding native medians are 0.4087815, 0.638264 and
0.20407 ms. Every exact native result check passes. Point variability remains;
these are bounded warm synthetic observations, not production qualification.
SQLAlchemy 2.0.51 and installed build/full-suite boundaries are pending with
the coordinator. Runtime, test and benchmark source remain frozen.

Additional pure lifetime/serialization review:

- The installed Python 3.12 `cached_property` reads/writes the instance dictionary
  without a lock. Concurrent first use can duplicate deterministic public-byte
  computation; it does not reuse or share a root/derived key.
- Eight threads completed 128 independent exact CF1 transcript/read/query checks
  using two different root sets that share the exact same public KeyContext and
  FieldDescriptor instances. All passed.
- Warmed objects retain equal `asdict` output and stable dataclass equality/hash.
  Shallow/deep copy, trusted local pickle roundtrip, and `dataclasses.replace`
  preserve matching public metadata. This does not authorize untrusted pickle.
- Cached payload size is 32 bytes per used KeyContext and 86 bytes per used
  equality descriptor, plus ordinary Python byte-object/dictionary overhead.
  No global retention or larger secret-key lifetime is introduced. Cold first
  use can pay the property/dictionary setup cost; it is not claimed faster.

Receipt: `evidence/public-metadata-thread-serialization.json`. All frozen source
hashes were rechecked and still match. No further timing campaign was run.
