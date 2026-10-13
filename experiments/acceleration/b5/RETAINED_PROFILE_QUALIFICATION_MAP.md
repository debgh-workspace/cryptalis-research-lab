# Explicit lifecycle profile-to-test qualification map

Date: 2026-10-13. Scope: the frozen S17 research candidate and a new test-only
copy. This map does not alter test selection, old assertions, a lifecycle
contract, or the meaning of a failing full run. No skip/xfail marker is added.

## Exact profiles and observed result

Legacy exit profile: `cryptalis.transition/v1`, `cryptalis.reverse/v1`, reverse
staging layout 2, protected bytes in the original logical column, and copied
public suffix columns to restore visible order. Complete legacy safety B4 keeps
that profile, its original ten assertions, and the predecessor correction. Its
separate source/reader is required; never overlay it onto retained runtime.

Retained research profile: `cryptalis.transition/retained-native-research-v0`,
`cryptalis.reverse/retained-native-research-v0`, reverse layout 101. The original
native column identity/order stays in place, CF1 occupies a separate physical
slot, and reverse staging exists only for protected fields. Public columns are
not copied or recreated. The profile is explicit; old artifacts are not silently
reinterpreted.

Frozen S17 installed full runs remain:

- SA21: **7 FAIL, 2235 PASS, 18 subtests PASS**, 388.64 s.
- SA20: **7 FAIL, 2189 PASS, 46 SKIP, 18 subtests PASS**, 387.73 s.

These are the pytest console summaries in `s17-installed-full-sa21-20261013`
and `s17-installed-full-sa20-20261013`. The custom runner receipt aggregates
subtest reports differently, so its raw counts are not substituted for these
console counts. Both receipts identify 3 PASS / 7 FAIL in the historical ordinal
module, 11 PASS in retained metadata, 52 PASS in deprotection and 15 PASS in
migration byte bounds. Relevant JUnit cases have no failure/error/skip.

## Seven preserved failures and their safety properties

All names below are in tests/test_deprotection_ordinals.py. Every one remains
an actual failure in both full S17 runs. Independent tests do not turn those
failures into passes or establish full legacy compatibility.

| Historical failing case | Historical safety intent | Retained-profile independent evidence | Remaining distinction/gap |
|---|---|---|---|
| test_reverse_refuses_unhandled_public_suffix_comment_before_staging | Avoid losing a public column comment while reconstructing suffix columns | test_retained_public_metadata.py::test_retained_public_metadata_survives_current_data_reverse[comment] compares native table OID/attnum/type/collation/nullability/storage/compression/statistics/ACL/comment/default and full values; test_native_public_metadata_survives_final_removal[comment] extends through removal | Required refusal belongs to copying profile; preservation in-place is a different mechanism. Both current oracles pass |
| test_reverse_refuses_unhandled_suffix_attributes[column_grant] | Avoid losing a public column grant during reconstruction | test_retained_public_metadata_survives_current_data_reverse[column_grant] compares exact catalog ACL and full values through PLAINTEXT_PENDING | Final-removal attribute matrix omitted column_grant. New B5 case tests exact original SELECT ACL through the existing role handoff/removal, while retaining the old-write denial boundary |
| test_reverse_refuses_unhandled_suffix_attributes[statistics] | Avoid resetting explicit public-column statistics target | Retained current-data reverse[statistics] and final-removal[statistics] native catalog/value comparisons | Refusal is different mechanics; independent preservation oracles pass |
| test_reverse_refuses_unhandled_suffix_attributes[storage] | Avoid losing explicit public-column storage mode | Retained current-data reverse[storage] and final-removal[storage] native catalog/value comparisons | Refusal is different mechanics; independent preservation oracles pass |
| test_reverse_refuses_unhandled_suffix_attributes[compression] | Avoid losing explicit public-column compression mode | Retained current-data reverse[compression] and final-removal[compression] native catalog/value comparisons | Refusal is different mechanics; independent preservation oracles pass |
| test_changed_public_staging_refuses_switch | A copied public value must not replace a current value after staging corruption | test_retained_reverse_preserves_public_edits_without_copy_staging[False/True] proves exact current public values survive without any public copy; test_deprotection.py::test_changed_verified_data_never_switches[staging] corrupts real protected plaintext staging and proves refusal, unchanged VERIFIED phase and retained encrypted storage | Historical test raises NoResultFound because no _copy_ column exists. No public shadow is silently trusted. Protected staging still requires full verification. No new staging mechanism is admitted |
| test_public_copy_participates_in_chunk_byte_bound | Bound bytes that copying brings into a chunk and refuse oversized required values rather than omit them | Retained wide-public edit test completes with chunk_bytes=512 while preserving the full wide public value. test_migration_byte_bounds.py proves forward protected prefix/oversize/no-fetch/full-verify controls | Public bytes are no longer copied. Existing forward tests do not independently exercise reverse protected-byte refusal. New B5 tests cover reverse backfill/verify, exact refusal snapshots, retry recovery, and driver-level exclusion of untouched public values |

The three other historical ordinal cases still pass: public NULL/Unicode/native
order, old-unversioned-stage refusal and pre-switch abort value preservation.
Their result and source remain unchanged.

## Independent coverage versus implementation mechanics

Metadata evidence reads native PostgreSQL catalogs and values, rather than
asserting a generated _copy_ column or using the executor's schema comparator.
The retained tests compare the actual attacl/comment/attstattarget/attstorage/
attcompression. Accepting a public column without copying it is not itself a
proof; the native before/after oracle supplies the bounded evidence.

Staging integrity remains necessary for every value that is actually staged.
The existing protected staging tamper, frame/tag/generation/membership/fence,
expiry and reverse-restore tests retain that check. A removed public-copy path
has no copied value to authenticate; unchanged public data must remain current,
as the independent public-edit tests demonstrate.

The byte budget covers data handled by the transition, not all bytes in a row
that stay in PostgreSQL. It is not a whole-process RSS, Python object-overhead,
WAL or pause-time bound. The new driver projection oracle confirms the untouched
wide public value is not returned by reverse chunk/verification queries. The new
protected-value tests retain no-skip, no oversize payload return and exact
predecessor/journal/schema/value preservation on a refused retry.

## New B5 test-only acceptance gate

Candidate: candidate-accel-retained-profile-oracles-20261013. All 195 inherited
S17 files, including 38 runtime modules and the historical test file, remain
byte-identical. PROFILE_ORACLE_PROVENANCE.json records every inherited hash.

New tests/test_retained_profile_safety_oracles.py contains four cases:

1. Reverse backfill commits only a fitting prefix, refuses the oversized Unicode
   protected successor, leaves its exact catalog unchanged, and on repeated
   refusal preserves all rows/stages/journal/triggers/indexes. It never returns
   the oversized payload, keeps original CF1 bytes, then resumes to exact native
   values with a sufficient explicit bound.
2. Reverse verification refuses its oversized protected value without changing
   the exact BACKFILLED snapshot; a sufficient bound permits full verification
   and exact native restoration.
3. Reverse backfill and verification never return an untouched wide public
   value in their actual driver projection. Full native public values and
   metadata survive under the bounded chunk setting.
4. The existing explicit public SELECT-column grant survives the existing
   plaintext role handoff and final removal. Native values and independently
   decoded retained CF1 frames match. Old runtime table/column write privileges
   remain absent. No new read-denial or read-relaxation policy is introduced.

These are bounded synthetic oracles under the existing maintenance contract.
The fourth test reuses the same existing-role, owned-schema grant fixture as
both preserved historical and retained metadata tests. It creates no account,
credential or broader privilege. It does not promise arbitrary old-process
read revocation; that is outside the selected current contract.

Proposed coordinator-only focused gate:

    -q tests/test_retained_profile_safety_oracles.py \
    tests/test_retained_public_metadata.py tests/test_migration_byte_bounds.py \
    tests/test_deprotection.py::test_changed_verified_data_never_switches \
    --tb=short -ra

Expected count: 4 new + 11 retained metadata + 15 forward byte controls + 5
staging/frame/membership/fence/generation controls = 35. Run both existing
SQLAlchemy cells through unchanged lab_session.py/test_postgres.py preflight.
A separate historical-module run will still contain all seven failures; this
focused gate is not a replacement full-suite result.

At preparation time: syntax compile PASS only; new PostgreSQL results pending.
No database/Git/promotion action by this worker. Main promotion remains subject
to the coordinator's explicit approval boundary. All seven production gates
remain UNKNOWN.
