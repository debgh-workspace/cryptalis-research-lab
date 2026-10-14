# SA21 independent RED evidence review

2026-10-14 UTC. Reconciled: exactly 3 FAIL / 1 PASS, zero errors/skips.
The terminal reports 2.70 seconds; JUnit records 2.705 seconds. Runner exit 1.
This is a correctness outcome, not a performance observation or full-suite run.

All four independent native controls completed and preserved comments, object
shape, and exact current row tuples. The standalone-index, UNIQUE-constraint,
and constraint-backed-index lifecycle cases then preserved object shape and
current rows but failed only comment equality at PLAINTEXT_PENDING. Their
failure stacks match the intended comment-preservation assertion. Product
removal was NOT_REACHED in those three cases.

The absent-comment control completed PLAINTEXT_PENDING and REMOVED with comments,
shape, and current values all unchanged. Both its fixture paths completed.
The four setup and four pytest teardown reports passed. No cleanup error replaced
the three primary assertions. The pinned fixture finally block runs normal
synthetic-schema cleanup, but there was no separate post-teardown catalog query
in this audit. Lifecycle completed=false in the three RED receipts records the
failed path, not evidence that cleanup failed.

All 152 captured source/configuration hashes match before, after, current files,
and their archived bytes. Both external files match their frozen v2 hashes and
archived bytes. All 213 canonical preparation files and runner source hashes
remain matched. The safe origin log identifies the intended isolated candidate.
All 26 shared corpus originals match their prior hashes; no changed/deleted
corpus files or capture errors are reported. Fresh role preflight is recorded.
The safe shutdown log states server stopped. Numeric stop exit 0 is coordinator-
reported; environment-bearing execution JSON was not opened to confirm it.

The case receipts preserve booleans from exact native comment comparisons, not
the returned comment text/NULL itself. They directly establish nonpreservation.
The source explains comment loss through drop/recreation without restoration;
the serialized receipt alone does not distinguish NULL from different text.

Exact outcomes, source/archive/corpus checks, and safe artifact hashes are in
SA21_RED_AUDIT.json. No rerun, project import, database connection, Git command,
raw environment JSON, credential read, or product edit occurred in this review.
All seven gates remain UNKNOWN. SA20 confirmation requires its own evidence.
