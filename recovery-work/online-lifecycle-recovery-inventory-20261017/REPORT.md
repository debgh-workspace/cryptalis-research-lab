# Online lifecycle recovery inventory

Immutable source: debgh-workspace/cryptalis-research-lab at
eed4482d824c87004c6df280a038f0b24ac17d8d. Recursive tree returned 2,260 entries,
truncated=false. All reads used that exact ref. No Git writes, DB operation,
model/test execution or change to source restoration elsewhere occurred.

## Result and next action

Both completed synthetic tracks are recoverable. Do not rerun their models.
Keep the accepted 38-case forward-ABORTED result and 22-case ambiguous-COMMIT
result as conditional logic evidence, with every safety/authority flag false.

Smallest useful next engineering action is a source-only integration-premise
document against the separately recovered exact 221-source baseline: specify
(a) closed raw journal/nested-state decoding and exact-N v3 reservation, and
(b) a native observation adapter contract establishing original transaction
identity/terminality and coherent exact-effect reads. Map each requirement to
existing validators and a future deciding observation. Do not implement journal
mutation, flip model assumption flags, repeat source checks, or launch native
fault injection until the corresponding source/contract/target admission is
separately selected. No new model run is needed to recover the current result.

## Exact remote recoverable paths

Every path below is relative to the repository at the immutable ref above.
REMOTE_INVENTORY.json retains exact leaf paths, Git blob IDs and sizes, including
all 41 matching blobs. READBACK_INDEX.json adds the terminal review and adjacent
online-closure source-review paths. The index is an availability inventory, not
a claim that every body was downloaded or revalidated.

Forward component (five files including seal):
cryptalis-executable/experiments/forward-aborted-successor-pure-v3-v1-20261016/
  INPUTS.sha256, PACKET.sha256, README.md, TEST_PROPOSAL.md, successor_contract.py

Forward vectors/driver (nine files including seal):
cryptalis-executable/experiments/forward-aborted-successor-pure-v3-vectors-v1-20261016/
  CASE_ORACLES.json, COMMITMENT_PREIMAGES.json, EXPECTED_RESULT.json,
  INPUTS.sha256, PACKET.sha256, README.md, RECIPE.json, VECTORS.json, driver.py

Forward reviews:
cryptalis-executable/reviewer-notes/forward-aborted-successor-pure-v3-agent1-independent-20261016/VECTORS_DRIVER_REVIEW.md
cryptalis-executable/reviewer-notes/PURE38_V3_TERMINAL_REVIEW_20261017.md

Forward actual capture (nine files):
persistence-recovery-20261013/forward-aborted-successor-pure-v3-vectors-v1-root-20261016/
  admission-after.json, admission-before.json, exit-and-limits.json,
  invocation.json, namespaces-after.json, selection.json, stderr.txt,
  stdout.json, terminal.json

Ambiguous-COMMIT source/results/reviews (nine files):
research/online-ambiguous-commit-model-v1-20261016/
  CASES.json, MANIFEST.json, PROPOSAL.md, SOURCE-REVIEW.md,
  TERMINAL-REVIEW.md, driver.py, model.py, selection.json, stdout.json

Ambiguous actual supporting capture (eight files):
persistence-recovery-20261013/online-ambiguous-commit-model-v1-root-20261016/
  admission-after.txt, admission-before.txt, argv.txt, cwd.txt, exit-code.txt,
  expected.sha256, invocation-transcript-record.json, stderr.txt
The published stdout lives in research/... above, not this capture directory.

Prior online-closure V2 source-check evidence:
experiments/acceleration/online-closure-v2/POSTRUN_REVIEW.md
This accepts eight existing source-structure checks, not native online closure.
The corresponding directory also retains source patches, manifests, source test
and two online fixture helper sources; see READBACK_INDEX.json.

## Checked result identities and qualification

Fifteen selected textual bodies were retained under readback/ using their exact
remote relative paths. All fifteen reconstructed Git blob hashes match the
connector/tree identities (READBACK_BLOB_VERIFICATION.tsv). Snapshot SHA256s are
sealed separately. These are inert readbacks, not a runnable restored packet.

Forward successor_contract.py SHA256:
f1fabd4fd24dbf0532c0bc030f11799f76b9da186ac5c6388c7233352d7817cf
Forward actual stdout SHA256:
93fe65bb2de8bc9b80074b5ce7228d4026300024d48e6507135c0ad3a7c2b88f
Forward terminal SHA256:
664082abfee544fbf8cbc85c466f1d37d88deefa271ae0c2888cc2121987f719
Forward independent terminal review SHA256:
d055805ae6f7496b7a98e10e0e32570423f8e41bd75e7d739ba6f6b12ccc0a1f

Parsing existing JSON as data establishes 38 distinct ordered results, all pass,
10 ordinary/26 refusal/two boundary-limitation cases, no failures, and exact
equality of every fixed pre-execution oracle field. All six authority flags are
literal false. The terminal review independently accepts the bounded synthetic
result and reconciles 495 before/after admissions. The capture's pending-review
status is historical; that later review supplies its scoped acceptance. The
review reconciled host receipts but did not repeat every host body hash.

Ambiguous model.py SHA256:
0e2a079102c496e613ef69ab4473a365e6373ff926c81cdc369be0dd414f5bc0
Ambiguous actual stdout SHA256:
324ca51267c55c0224556cb334fca46854c119e2f8c2aca0df551dd3fdf1ae53
Ambiguous terminal review SHA256:
2b9552397283ad27efc7fec62d2f0fe2b25532fa89fc38e9723041508c7433f6

Existing stdout parses as 22 distinct cases, all pass, no failures, all 66
retry/closure/publication flags false, both counterfeit conclusions rejected.
The terminal review accepts this synthetic result with entry-record limits:
four packet bodies plus interpreter had before/after rows; PROPOSAL had no
separate row; environment/timeout command evidence was a post-run transcription;
per-file ulimit was not a combined-stream monitor; fresh host-stdlib admission
and initial output-absence history were not independently retained. Do not
rewrite these qualifications into stronger execution evidence.

## Remaining integration premises

Forward pure-v3 is only a detached lineage component, not a full artifact/native
constructor. Its source validates top-level forward ABORTED shape and hashes
nested state but deliberately does not validate nested models/schema/guards/
progress. The nested_state_boundary case demonstrates this missing gate. The
unstable_snapshot_boundary case demonstrates that repeated/conflicting UUID
rows can satisfy supplied commitments without a stable native unique-key view.
Before integration, establish:

1. Closed journal decoder grammars for exact historical producers and v3;
   native raw-byte/type admission and complete nested terminal semantics.
2. New-v3-only 16 MiB canonical/native transfer and expansion reservation,
   exact 0 <= chunks <= rows <= N, huge-integer and peak/transfer limits.
   Current post-encoding size checks are not these proofs. Historical oversized
   recovery remains an unresolved broader requirement, not silently discarded.
3. Genuine v0/v1 producer compatibility; complete v3 constructors reusing
   compiler/comments/designation validators and reverse-envelope accounting.
4. Physical journal PK/membership/owner/ACL/dependency admission without repair;
   one stable snapshot with native count/point reads; agreed ordered-table,
   sorted transition-table, then journal SHARE ROW EXCLUSIVE lock ordering,
   insertion exclusion and deadlock evidence.
5. Fresh external PREPARED authority and late role/metadata checks, atomic
   expansion with old-row preservation, repeated abort/resume, reverse-set
   partition, reverse/removal, and independent publication boundary.

Ambiguous-COMMIT model assumes identity_verified,
original_transaction_terminal_verified, coherent_committed_observation and
stage_matches_claim. Its code does not establish any of them. Native integration
must bind exact operation/row/original attempt and current pin/PREPARING state,
resolve original transaction terminality, obtain coherent committed observations
under actual isolation/locks, and verify the complete live/NULL/tombstone/context/
frame effect. A matching effect proves only that observation, not who committed
it, retry safety, no future work, liveness or closure. Empty dirty state and token
ordering remain insufficient. Any later action needs revalidation.

Actual PAUSED closer, durable native/runtime guard and paused finisher remain
unimplemented in the cited proposal. Capture/handoff request and writer/owner/
DDL coverage, runtime-role mapping and PAUSED/finisher contracts are outstanding
premises, not approvals inferred here. Native lock/visibility/rollback/reconnect
observations and applicable exact target/role/operation authorization remain
separate. Retained-native maintenance still requires actual writer exclusion,
byte-bounded atomic work, full current membership/value/type/NULL scan, snapshot
barrier and separate publication. No safety/authority field is widened.

## Recovery limits

These exact referenced paths are absent from the complete remote tree:
- cryptalis-executable/reviewer-notes/forward-aborted-successor-pure-v3-agent1-independent-20261016/REVIEW.md
- cryptalis-executable/experiments/preview-doctor-dx-slice-20261015/proof-v2/STDLIB_SHA256.txt
- persistence-recovery-20261013/pure38-controller-root-20261017

Absence is by exact path at this ref, not proof that no other archive contains
the bytes. The model results and terminal reviews remain recoverable without
inventing a complete current execution admission. All absolute paths in older
INPUTS/receipts describe the former workspace, not today's restored files.
The parent's independent 221-source restoration is outside this inventory's
write scope. Original short publication IDs were not expanded or guessed.
