# B5 observer-strengthening boundary

Date: 2026-10-13. This separate derivative preserves the original B5 source and
35-case results: SA21 35 PASS / 11.85 s; SA20 35 PASS / 11.21 s. Those results
retain the limitations identified by independent review. No runtime defect was
established by that review, and no runtime correction is made here.

## Exact previous limitations

The public-transport observer checked cursor output names only. A selected
public column under another output alias could escape that assertion. The
oversize observer collected every relevant CTE rowcount but required only the
last one to be zero; an earlier unwanted payload could therefore escape it.
These are test-evidence weaknesses, not proof that either behavior occurred.

## Stronger finite evidence

The observer now reads libpq PGresult metadata and result buffers through
ntuples, nfields, ftable, ftablecol, ftype, fformat and get_value. It never advances
the cursor. Native result OID/attribute-number provenance is checked independently
of output aliases. The installed psycopg PGresult API was inspected locally;
no database was connected by this worker.

For each reverse byte-refusal retry, require the complete expected result
sequence: an empty result for backfill after the committed prefix; only the
fitting identity followed by an empty result for verification. Every result
must have the exact expected native projection and identities, must exclude the
oversized identity, and must fit the logical fetched-value byte budget.

For wide public preservation, every observed backfill/verification result must
have one of the two exact expected native projections, exclude the actual
public-column provenance and wide UTF-8 marker, and fit the logical fetched
value budget. The complete returned identity sequence must cover each fixture
row once in backfill and once in verification. Unknown expressions/provenance
and added aliased public columns fail those expectations.

Two new actual native-query negative controls make the observers sensitive:

- A SELECT returns label under an innocuous alias. Both its native provenance
  and its buffered wide marker are independently detected. The ordinary caller
  still receives its unconsumed result after observation.
- A native SELECT returns the oversized identity/value, followed by an empty
  SELECT. The old final-rowcount-only condition would pass. Complete identity
  sequence and per-result byte-bound checks each detect the unwanted earlier
  result.

This remains a bounded observer of buffered result sets from the selected
_cryptalis_candidates SQL family, plus the explicit native control queries.
It is not a general SQL/network capture, streaming-cursor proof, whole-process
RSS/object-overhead bound, or pause/WAL qualification. Logical value sizes count
UUIDs as 16 bytes, decoded bytea length, and text UTF-8 bytes, not PostgreSQL
text-protocol formatting overhead. Native catalog/value and exact journal
snapshots remain independent of the executor's own schema comparator.

## Preservation and proposed gate

OBSERVER_PROVENANCE.json binds all 199 files of the original B5 copy. Only its
new test file is strengthened in this derivative; original B5 is unchanged.
All 195 S17 inherited files, including 38 runtime modules and every historical
assertion, remain byte-identical. Historical seven failures remain failures;
no skip, xfail, contract change, old-worker read change or main promotion occurs.

The test-only gate now has 37 cases: six strengthened/new observer/metadata
cases plus eleven existing retained metadata cases, fifteen existing byte-bound
cases and five staged-integrity cases.

    -q tests/test_retained_profile_safety_oracles.py \
    tests/test_retained_public_metadata.py tests/test_migration_byte_bounds.py \
    tests/test_deprotection.py::test_changed_verified_data_never_switches \
    --tb=short -ra

Static syntax compilation PASS. Native execution is pending the coordinator's
unchanged dual-role preflight and serialized PG16 queue for both cells. No DB
or Git action was performed here. All seven production gates remain UNKNOWN.

## First-attempt correction and composed evidence boundary

The preceding observer revision, test SHA256
523b51634bca445617d34de06c6aeb6fa89de9b0d3fea936063d2d070d5b1c7e,
passed 37 cases on SA21 (10.93 s) and SA20 (10.19 s), per coordinator. Those
stable stopped-run receipts apply to that exact revision. Review then identified
that its first bounded backfill attempt was not observed; only its retry was.
The prior test bytes and their SHA record are retained under
evidence/observer-before-first-attempt/ without default test collection.

Only the backfill parameter branch is now strengthened: install the same
non-consuming observer before the initial bounded attempt, require exactly the
fitting UUID(100) result followed by an empty result, and enforce exact native
provenance plus the byte bound for both. The separate retry still requires only
an empty result. The verification branch and the other five cases are unchanged.

Coordinator-requested final selector, one affected case per existing cell:

    -q 'tests/test_retained_profile_safety_oracles.py::test_retained_reverse_protected_byte_refusal_preserves_exact_state_and_recovers[backfill]' --tb=short -ra

After those checks, the evidence is a composition of the two prior 37-case
receipts and the exact final affected-case receipts. It must not be presented as
a new full 37-case run of the final test file or a green S17 full suite. At this
edit boundary, only static compilation has been performed; final DB checks are
pending. Original seven historical failures and every runtime byte are unchanged.
