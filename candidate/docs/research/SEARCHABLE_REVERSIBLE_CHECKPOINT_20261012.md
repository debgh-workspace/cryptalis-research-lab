# Searchable, reversible layout checkpoint, 2026-10-12 09:14 UTC

## Exact candidates

candidate-inplace-search-research-20261012 adds declared equality/unique index handling to the prospective in-place layout. It drops only compiler-admitted native protected-field constraints/indexes, converts the original column from verified CF1 staging, then recreates the existing CF1 check and declared keyed-term index. Reverse removes the CF1 index/check, restores the original type/collation in place, and recreates the exact recorded native index/constraint definitions. Existing row/tenant/field authentication, full cutover verification, writer and snapshot fences remain. Plan formats have explicit inplace-search-research-v0 markers; reverse journal layout is100. Legacy reordered layouts remain refused.

candidate-inplace-search-index-research-20261012 additionally admits ordinary non-unique tenant-field indexes with exact native UUID/text operator classes and C collation. The source compiler and serialized-lock validator both enforce this same shape. Other method, expression, partial, include, uniqueness, and metadata restrictions remain.

## Verified research evidence

- Search-capable parent:14 ordinary lifecycle cases PASS, including restored native uniqueness/NULL behavior and VARCHAR/native column order.
- Native -> encrypted -> native roundtrip: four Text/VARCHAR x unique/non-unique cells exercise seven equality/IN/NULL queries, native uniqueness outcome and exact SELECT * names/order/values. Parent:2 PASS /2 planner failures on non-unique tenant-field indexes. Initial compiler-only correction:2 PASS /2 invalid-lock failures. Aligned compiler and lock validation:4 PASS. Preserve both RED stages.
- Real FastAPI upstream SHA7257e606cb94eada1dca40173e2b7f99dd549bc6: emails protected with declared equality/uniqueness; full_name protected in storage mode. Native baseline58 PASS; protected58 call bodies PASS plus1 protected bulk-delete teardown ERROR. All36 email frames independently decode exactly; five non-null name frames also match. Source unchanged.
- The same searchable real-app profile decrypts both fields back exactly, preserves native schema, publishes to a separate plaintext lab role and passes all58 upstream tests with Cryptalis absent. All58 pass again after metadata removal. Real encrypted pg_dump restoration is independently checked for both emails and names; a restored old encrypted state fails the REMOVED external pin check.
- Final index-admission candidate:119 selected installed tests PASS on each SQLAlchemy version (2.1.3 and2.0.51). The exact final candidate also repeats the complete real-app lifecycle in source-import mode: native58 PASS, protected58 bodies PASS plus1 teardown ERROR, package-free58 PASS before and after removal, exact36-row backup recovery. Evidence:inplace-search-index-real-fastapi-full-removal-20261012-0919.

## Integration and confidentiality costs

The app uses explicit schema qualification and a C-collation email mapping. Eleven external bootstrap lines (including import/setup), four original fixture lines, extra lifecycle/test scaffolding, and an explicit lab-only Item grant are disclosed. Old static six-line harness counters are stale. No upstream business/model/query source was edited. Native test residue is checked for exact values before reset between campaigns. The first two-field oracle incorrectly selected descriptor by position; it now selects by field name, with the failure retained.

This retains exact keyed-term equality/frequency leakage. It is not lower-leakage or fully private search. One synthetic tenant, PostgreSQL16.15, Python3.14.8/SQLAlchemy2.0.51 for the source-import app. The bounded installed-app replay below is verified; full regression and independent security review remain open.

## Remaining blockers

Protected bulk DELETE; generic unqualified-schema and role-handover integration; legacy layouts; second independent app; rewrite latency/WAL/disk bounds; broader SQL and provider qualification. All seven production gates UNKNOWN. No new commits or product promotion. PostgreSQL ALTER TABLE is established prior art, not a novel cryptographic contribution.

## Metadata compatibility checkpoint, 09:34 UTC

Nine installed checks PASS on each SQLAlchemy version: five native public-column metadata cases (comment, default, non-unique index, dependent public-only view, statistics target) plus four VARCHAR lifecycle cells. The native metadata is created before manifest planning. Tests compare native catalog attributes, object identities/definitions, positional order and original values before protection and after decrypt-back. Evidence:inplace-public-metadata-native-20261012-0932 and inplace-public-metadata-native-sa20-20261012-0933.

The initial fixture added these items after protection and expected unconditional removal. It returned six PASS and three active_schema_mismatch failures (default/index/view). This is an incorrect fixture expectation about post-protection schema drift, not evidence to weaken the active-schema guard. The earlier test bytes and failure logs are retained. Candidate runtime code was not changed. Comments/statistics already passed under both fixture timings.

The installed real-app replay completed: native58 PASS, protected58 bodies PASS plus1 teardown ERROR, package-free58 PASS before and after removal; exact backup recovery and old-state refusal also verified. Evidence:inplace-search-index-installed-fastapi-removal-20261012-0934. Its existing pinned dependencies were copied into a separate environment after offline resolution could not find Alembic metadata; Cryptalis itself is installed from the byte-verified candidate wheel. This is not a clean network dependency-resolution claim.
