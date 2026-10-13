# B5 stronger observer progress

Updated 2026-10-13 15:24 UTC. Separate candidate copied byte-for-byte from B5;
original B5 and receipts are preserved. Coordinator released its stopped runs
before this derivative was created. No shared source edits or DB/Git actions.

Independent reviewer identified alias-sensitive public projection and last-only
rowcount checks. They are observer limitations, not runtime defects. Replaced
those checks with non-consuming native PGresult buffers/provenance, complete
result identity sequences and per-result logical byte bounds. Added native
alias and earlier-oversize/empty-tail negative controls. All S17 inherited source
and historical tests remain identical. New test syntax compiles.

Exact reviewer findings and proposed 37-case gate are documented in
B5_OBSERVER_STRENGTHENING.md. Reviewer notified for source inspection. Frozen
for coordinator review and serialized execution.

2026-10-13 15:29 UTC: coordinator reports prior observer revision 37 PASS per
cell, 10.93/10.19 s, source stable/server stopped. E identified an unobserved
first backfill attempt. Preserved exact prior test bytes/hash under evidence,
then instrumented only that initial backfill branch. Current retry and verify
checks remain intact. Frozen for one affected backfill case per cell; evidence
will be composed rather than claiming a new full run of final test bytes.
