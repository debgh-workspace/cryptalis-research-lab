# Independent source review: native abort-envelope probe V2

## Verdict

**ACCEPTABLE AS SOURCE; NOT ADMITTED OR EXECUTED.** The V2 delta fixes both source-column sort ambiguities without changing any test assertion, test selection, native value, bound or expected observation. The previous V1 review missed these two ambiguous ORDER BY clauses; this review supersedes that portion of its assessment. A passing native result is not established.

Reviewed packet: `experiments/abort-envelope-native-probe-v2-20261015`.

- V2 seal SHA-256: `f8ebb881794328c9b6054129e5966847cd37264dc80e7a21f4b71c4a10b99ff5`.
- V1 seal SHA-256: `0c005d33fd00630e7b3ef986e2bbcae3e4c6cafe65b4b996b52ad514304424e5`.
- Prior source review: `reviewer-notes/abort-envelope-native-probe-source-independent-20261015/REVIEW.md`, SHA-256 `17d39a9c6bb9b3b4ca1c913d64ddfe6e3f9a5043a4461d88e139498309922159`.

Both packet seals match these exact digests, and every one of their seven sealed members verifies. The V2 directory listing consists of those seven regular members plus its seal. The prior source-review digest also verifies. This finite delta review does not freshly verify every inherited SOURCE_INPUTS provenance referent.

## Exact delta and SQL inspection

A complete byte comparison after applying only the following three substitutions to sealed V1 exactly reproduces V2 `test_native_envelope.py`:

1. The evidence destination changes from `abort-envelope-native-probe-v1-sa21-20261015` to `abort-envelope-native-probe-v2-sa21-20261015`.
2. The UUID domain query at lines 252-253 uses `ORDER BY q.v`.
3. The int64 domain query at lines 258-260 uses `ORDER BY q.v`.

No other test-body difference exists. `conftest.py` and `EXPECTED_CASES.txt` are byte-identical to V1. `COMMAND_ARGV.json` differs only in its evidence, selected test and confcutdir paths, each moved to V2; all runner, count, timeout and resource selections remain unchanged.

Both domain queries project `v` and `v::pg_catalog.text`, which can share output name `v`. Qualifying the sort with relation alias `q` explicitly selects the original UUID or int8 input column rather than an ambiguous output name. The projections, reversed typed input parameters, native type/order comparison, canonical text, OIDs, text formats and maximum width assertions are unchanged. The fix does not use a text sort or substitute output order by ordinal.

I inspected all five explicit execute call sites and all fixed SQL text: connection identity (lines 139-141); LENGTH_SQL including both CTE SELECTs and final projection (62-66, executed at 160); TEXT_SQL (67, used at 168 and 320); and both domain branches (252-260, executed at 264). There are exactly two ORDER BY sites, both now qualified. No other sort ambiguity of this form occurs. All execution sites retain `prepare=False`; the body retains its fixed SELECT-only synthetic-parameter scope. No query execution or database-parser check was performed.

## Preserved finite coverage

The exact 31 ordered IDs in EXPECTED_CASES are unchanged: two domain, nineteen family, six full-size boundary, three rejection and one omission-control case. The complete-success expectation remains 93 ordinary setup/call/teardown phases, with no allowed failure, error, skip, xfail or deselection.

The unchanged source independently gives:

- Family state observations: 2 empty families x 7 plus 17 nonempty families x 9 = 167.
- Full-size observations: 6 boundary cases x 2 = 12.
- Omission observations: correct envelope, independent abort and three omissions = 5.
- Total state observations: 167 + 12 + 5 = 184.
- Explicit SELECT executions: 31 connection identities + 184 x 2 measurements + 2 domain sorts + 3 rejections = 404.
- Expected JSONL records: 31 connection + 184 state + 2 domain + 3 rejection + 1 omission = 221.

All six actual 16 MiB constructions and their assertions remain intact. For L = 16,777,216, canonical-basis margins -1/0/+1 retain expected pairs (L-1,L+21), (L,L+22), (L+1,L+23); native-basis margins retain (L-23,L-1), (L-22,L), (L-21,L+1). Each pair is (compact bytes,native bytes). Every associated ABORTED observation must be three bytes smaller in both representations. Both envelope gate classifications remain checked. The diagnostic bounds L+1 and L+32 do not alter the L state ceiling. All twelve full-size native transfers, strict semantic/type/canonical comparisons, three omission-underestimate detections and rejection requirements are preserved.

Records remain observations before assertions, not independent PASS evidence. Complete exact IDs, passed call phases, ledger identities, numeric observations, normal shutdown and source/runtime/corpus closure must still be independently audited after any separately authorized run. The original finite-scope limitations in the prior source review remain applicable; this is not a general serializer proof, admission proof or v3 approval.

## Predecessor and execution hold

Root reports that V1 failed its first UUID case with AmbiguousColumn, with zero prior successful cases, entry exit 1, post-status 3 and all 26 corpus entries equal. Those are parent reports; this source review does not certify run or closure evidence. The separate failure auditor owns those facts. V2 correctly names the actual V1 failed native stage as its pending predecessor and requires CLOSED_FAILURE. An older cost9 success cannot replace that intervening outcome.

PREDECESSOR_BINDING still has null terminal-review fields and false closure/authority/selection fields. COMMAND_ARGV still has null entry, review and selection fields. The source packet is therefore deliberately held. A separate V2 outer companion must bind this exact review, the exact V2 seal, actual independently accepted V1 failed closure, current bounded authority and exclusive selection, unchanged runtime guard/cold launcher, fresh paths, archival identity and closure-aware resource controls. The V1 or transport entry is not authorized for reuse by this review. Source approval supplies neither execution permission nor terminal success.

## Review boundary

Only finite inert V1/V2 packet files and the named prior source review were read, compared or hashed. No target Python was imported, compiled, collected or executed. No tests, database/status commands, live cells, installed payloads, corpus contents, cache, environment/credential values, Git or network operations were inspected or invoked. No V1/V2 source or prior evidence was modified. Only this new reviewer directory was written. Shell text comparison and hashing, plus direct source arithmetic, supplied the checks above.
