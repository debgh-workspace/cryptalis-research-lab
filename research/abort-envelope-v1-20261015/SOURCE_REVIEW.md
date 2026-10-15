# Independent source/math verdict: abort-state envelope

## Verdict

ACCEPT THE SEALED REFERENCE PLUS FRESH V2 DECIDING VECTORS FOR THE NEXT ISOLATED UNIT PROOF.

This accepts the source/math argument and the preparation for a bounded unit run. Nothing was imported, compiled, collected or run. This is not native JSONB conformance, physical-journal validation, transaction/rollback evidence, historical recovery qualification, or permission to enable v3. The selected product remains unchanged; v3 execution remains disabled.

No unsafe claim of established native or runtime behavior was found. The mathematical dominance result is conditional on the explicitly stated new-operation invariants. It must not be turned into a new gate on old-format safe abort.

## Reviewed packet and preserved correction

The base packet is `experiments/aborted-successor-envelope-v1-20261015`. All seven v1 hashes matched on initial inspection and on an independent recheck after the correction. Its seal remains SHA-256 `4273ed617d0fd76d075e62f7648b8c721b705bc7fed059139e0a47deac5b472d`.

The initial review is preserved as `REVIEW_V1.md`, SHA-256 `cc9a89004817e127b17f47dcdb236d1b340d2d618f705979c0f9a04a32e37d9d`. It accepted the source/math direction but held the deciding unit-vector packet for independent complete-wire, multi-model, full-state-depth, and committed-prefix controls. Those were evidence gaps, not an observed byte underestimate or an executed test failure.

The author added a test-only correction under `experiments/aborted-successor-envelope-v1-20261015/correction-v2`, without replacing any v1 file:

| File | Bytes | Verified SHA-256 |
| --- | ---: | --- |
| CORRECTION.md | 4,437 | 53edcb4d141327c3b9b64865c929388919a55938a508e852de8ad7b01cf9043b |
| test_deciding_vectors.py | 12,375 | e631a11f36b346984cee7304d22abefa2099e61c760d08a414af93d32fccf8cc |
| SHASUMS.txt | 171 | 8993259fa728f34a733ca2eb1cc97259ef4f1b1e852ea57b46684c98b7136437 |

The author disclosed a preparation incident: `sha256sum -c ../SHASUMS.txt`, invoked from the correction directory, could not find the parent packet's relative filenames. That was a wrong-working-directory file-not-found result, not a digest mismatch or a test result. This review retains that disclosure. The reviewer's independent explicit-path SHA-256 recheck subsequently confirmed every original v1 file unchanged. It does not erase the failed author check or count it as successful.

## Deciding source/math findings

1. The reference byte equations are correct for the admitted exact plain JSON types. UTF-8 string byte widths include every required escape and quote. NUL and lone surrogates are explicit refusals. Container depth, repeated subtrees, and cycles are handled distinctly. The depth limit is on containers, with the root at depth one.
2. Every exact pre-switch member is retained: complete schema and guard observations, scope, source fields, and explicitly frozen lineage. The longest phase is BACKFILLED. Forward reserves the full per-table 64-hex verification map; reverse does not acquire an invented verification field. No `active_schema` is admitted in terminal-abort state.
3. The per-model constant and counter formula are correct: `147 + 3*d(N) + cursor_width + |C(schema)| + |C(guard)|`. For a new operation, exact nonnegative counters constrained before chunk effects by `chunks <= rows <= N` are bounded by the decimal width of the initial N. UUID and signed-int64 cursor widths are separately correct. N=0 reserves null. The optional 53-bit profile is a new admission choice, not a legacy journal rule.
4. Both successful aborts only shorten their own phase string. Later mutable members cannot add depth. Canonical dominance follows once expansion has reserved all fixed bytes and future scalar widths. Actual native length admission must occur before expansion commits; a later refused proposal must preserve the previously committed abortable state. No new abort-time cap is justified by this proof.
5. Frozen comparisons are exact-type sensitive, so bool/int equality cannot silently change schema, guard, scope or lineage. The reference checks exact model/root sets and canonical UUID/digest/cursor forms. These are shape checks, not catalog validity, provenance, authentication, membership, or ancestry verification.
6. The native candidate adds one space for each structural comma and colon. It is clearly labeled a hypothesis. The protocol requires actual server UTF-8 lengths, independent strict text decoding, exact scalar types and canonical-byte round trips; PostgreSQL JSONB value equality alone is not the oracle.
7. The physical journal proposal is properly separate. It requires actual ordinary relation/column/PK/index structure and native owner/ACL/dependency checks, uses no fabricated historical OID/name, and leaves policy selection and native mutation sensitivity open. Relation locks are not claimed to freeze administrative role/ACL changes.

## Corrected independent vectors

The fresh source adds the missing deciding controls without changing the reference implementation:

- A complete manually written canonical byte literal for the minimal forward UUID maximum, independently compared to stdlib encoding and the candidate constructor. The hand-derived maximum is 391 compact bytes, 21 candidate separator spaces, 412 candidate native bytes; ABORTED is 388/409.
- Explicit expected totals for both codecs and both directions. Signed-int64 forward is 375/396; UUID reverse is 438/462; signed-int64 reverse is 422/446. Zero-scope totals are 357/378 forward and 404/428 reverse, regardless of codec.
- A two-model forward maximum with a complete verification map: 732 compact bytes and 39 candidate separator spaces, or 771 candidate native bytes. Removing either verification entry loses coverage of the independently constructed complete state.
- Full-state guard/proconfig nesting that independently computes depth 32 or 33, including the enclosing root/models/progress/guard containers. The nested config is explicitly a synthetic grammar stress value, not a claim about actual PostgreSQL proconfig shape.
- Independent missing/extra/substituted verification-key and malformed-digest cases, plus rejection of a reverse verification member.
- A valid committed prefix at rows=chunks=1, N=2. The next two-row proposal must fail for the exact counter-growth reason without changing the prefix. An independently built ABORTED copy remains within the envelope and has 265 compact bytes, 18 candidate spaces, or 283 candidate native bytes. A one-row proposal returns (2,2) without mutating the prior state.

The source contains 12 original and 7 added test methods, counted by finite text inspection only. This is not a collected-test count or a PASS total. The existing omission controls independently construct the deciding abort before omitting verification, cursor or counters; the unknown-field control tests exact shape. These controls remain unexecuted.

One clarification applies to the unchanged v1 native matrix: for a nonempty model set, positive forward verification states have the member absent or complete. An empty map is invalid and must be a negative case. The author confirmed this; the phrase “only as permitted” must not be read as admitting an empty reachable map.

## Exact minimum next questions

### 1. Isolated unit proof

May the 19 source-defined stdlib-only methods in the two sealed test files be imported and run against exactly `envelope_reference.py` SHA-256 `27584299ffaac34c2bb9a0a51671a5873ab76354649052fd8f7725b62f38564c`, in an isolated Python invocation with bytecode writes disabled and bounded stdout/stderr retained under a new proof-output directory?

The scope excludes product/helper imports, database connections, network, build/install, selected-source writes, and live-cell/corpus/environment/credential/cache/raw-phase reads. The launch must explicitly make the parent experiment's reference and the correction test module importable; generic recursive discovery must not silently omit the hyphenated correction directory. Preserve every failure and require a fresh authored correction rather than editing expected values in place.

### 2. Native serialization proof, only after the unit result and separate selection

On the explicitly named intended PostgreSQL 16 target and driver/encoding identity, may parameterized SELECT-only calls over synthetic, nonsecret values measure actual `octet_length(convert_to(value::jsonb::text,'UTF8'))`, strictly round-trip the returned text through independent canonical encoding, and compare each scoped pre-switch/ABORTED value with E, including the approved byte/depth boundary and omission vectors?

The launch must name the connection route, identity checks, bounded transfer/memory/output limits, and vector set. It must not read real journal/application data, make DDL or ACL/role changes, call a cutover helper, or enable v3. Returning JSONB directly through an unexamined driver loader is insufficient. Large scalar token limits or numeric normalization must produce an explicit refusal/unknown result, never truncation or coercion.

These are questions for root's execution selection, not permission granted by this review. A unit or scalar SELECT pass would not establish transaction ordering, expansion rollback, committed-prefix native abortability, physical table/PK/ACL safety, role mutation exclusion, lineage traversal, reverse artifact reservation, genuine frozen-producer compatibility, or final removal. Those remain separate controlled-fixture evidence and authorization.

## Scope record

`SOURCE_OBSERVATIONS.md` records the prerequisite hashes and finite independent source anchors. Only this reviewer directory was written. All actions were metadata-first bounded safe-source reads, SHA-256 checks, source/math analysis, and new review text. No product/helper/reference import, compilation, collection, test run, database, runtime status, build, install, Git, network, live-cell/corpus, environment, credential, cache or raw-phase read was performed. This acceptance is source-only.
