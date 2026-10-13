# D3 finite captured-text CF1 handoff

Verified 2026-10-13 15:32 UTC against the coordinator's bounded PostgreSQL runs.
This isolated derivative preserves all 190 D2 files byte-for-byte, including its
four publication-ready artifacts. Frozen D1's 186-file inventory is unchanged.
No worker database execution, Git write, credential, role or cluster change.

## Implementation boundary

The new test helper inherits D1's capture, immutable-key enumeration, fresh dirty
tokens, source/native writer twin, cursor transaction, claims and queue drain.
It does not modify D1's helper or tests. One outer fixture transaction installs
the original capture and converts the still-empty stage to bytea. An exact
operation/descriptor/tenant/root-generation/provider/wrapper-digest pin is stored
as fixture metadata and compared with the test's expected pin. It contains no
root or wrapping-key bytes and cannot supply deployment authority.

Only the lab installer is extended: existing key preparation, product CF1
storage-only sealing, frame insertion and exact dirty retirement. Frame and
retirement share one transaction. No key lease is extended. The existing
`test_cf1.setup_keys` fixture supplies fixed public roots through its existing
volatile development provider; no new provider profile is introduced.

The final separate read-only PostgreSQL observer decodes every live frame using
the unchanged D2 independent decoder. It requires complete enumeration, an empty
queue, and exact ordered equality with both current source and native twin,
including empty text, Unicode, SQL NULL and signed bigint extrema. Tombstones
remain distinct from live NULL rows. No product decoder is used as that oracle.

## Fixed 24-case selection

- Five captured mutations between page read and cursor commit: update, delete,
  delete/reinsert, text-to-NULL and NULL-to-text
- The same five mutations after a stale worker claim, with unchanged state after
  refusal and final current-value decoding
- Two page failures, before/after cursor update; new object/connection/key cache
  reconstruction preserves the committed cursor and exact earlier frame bytes
- Two worker failures, after frame insertion/after retirement; both effects roll
  back together and the same operation resumes
- Cold provider failure preserves stage and dirty work; normal recovery follows
- Changed durable pin refuses reconstruction or installation without progress
- A foreign-operation claim with the same key/token refuses without frame writes
- Six independent-observer negatives: valid stale frame, wrong row, changed tag,
  missing NULL row, NULL substitution and a valid but extra frame

Python syntax compilation PASS for both new files. Static AST accounting confirms
24 cases. The unchanged dual-role coordinator runner then recorded:

- SQLAlchemy 2.1.3 cell: 24 PASS in 2.08 seconds, at
  `evidence/d3-online-cf1-handoff-sa21-20261013`
- SQLAlchemy 2.0.51 cell: 24 PASS in 2.65 seconds, at
  `evidence/d3-online-cf1-handoff-sa20-20261013`

Both receipts confirm unchanged source/test bytes, successful dual-role preflights
and server-stop exit 0. These tests directly use psycopg/CF1; running in two
SQLAlchemy environments does not establish new ORM semantics. All 190 inherited
files, D1's original bytes and D2's four publication files remain unchanged.

Coordinator selector through the existing unchanged wrapper:

    --candidate-root candidate-accel-online-cf1-handoff-20261013 \
    --evidence evidence/d3-online-cf1-handoff-initial-20261013 -- \
    -q tests/test_online_cf1_handoff.py --tb=short -ra

The exact source manifest excludes only runtime caches and the manifest itself.
No repeat of the unchanged 23 CP65 controls, D1's 31 cases or D2's pure gate is
needed merely to recount prior evidence.

## Verified frame/retirement atomicity sensitivity

An isolated one-helper omission commits exact dirty retirement before the frame
transaction, then injects the existing after-retirement fault so the frame rolls
back. The unchanged common control reconstructs from the committed cursor and
drains without manual reseeding. The coordinator observed:

- Passing D3 control: 1 PASS in 0.39 seconds,
  `evidence/d3-atomicity-control-20261013`
- Split-retirement mutant: 1 FAIL in 0.40 seconds precisely at the independent
  observer's `assert decoded == native`,
  `evidence/d3-split-retirement-mutant-20261013`

Both runs passed unchanged dual-role preflights, retained source/external-test
bytes and stopped the server with exit 0. No import, setup or timeout error is
counted. The omission retires key 10 before its frame can survive the injected
rollback, which explains the complete-comparison failure. The original worker
transaction preserves the obligation and the healthy control recovers it.
The wrong implementation remains in its separate explicitly named mutant tree.
No passing D3 executable file was changed. This closes only the finite atomicity
sensitivity question; it is not an unbounded crash or online-closure proof.

## Limits

Only synthetic text and one immutable bigint domain, cursor, tenant and
storage-only field are used. Scheduled writers stop before the complete final
comparison; no deployment writer fence is proved. Reconstruction is in the same
process with the same surviving volatile provider. Faults are explicit exceptions,
not SIGKILL, ambiguous COMMIT, failover or fresh-cluster recovery. Actual expiry
during an in-flight transform is not added to this selection. No equality-index,
uniqueness, byte/RSS budget, latency, production key custody or independent human
review claim follows.

There is no product API, lifecycle phase, capture-trigger admission, online
closure or cutover integration. D-REV-04/09/07 decisions remain pending. Full
final verification stays mandatory; no runtime or production gate is promoted.
