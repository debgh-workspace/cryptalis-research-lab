# SA20 independent RED evidence review

2026-10-14 UTC. Reconciled: exactly 3 FAIL / 1 PASS, zero errors/skips,
2.67 seconds in the terminal. Runner exit 1. The four native/lifecycle case
receipts match SA21 exactly except the reported SQLAlchemy version, 2.0.51.

All native controls passed comment, shape, and current-row comparisons. The same
three commented cases failed only comment preservation at PLAINTEXT_PENDING,
with shape/current rows unchanged and removal NOT_REACHED. The absent-comment
case completed both pending and REMOVED comparisons and both fixture paths.
Four setup and four pytest teardown reports passed; no cleanup failure is
reported. The cleanup/receipt limitations in SA21_RED_REVIEW.md still apply.

All 152 captured source/configuration files and two external files match their
before/after, current, and archived bytes, and match the SA21 input inventories.
All 213 canonical preparation files and runner source hashes remain matched.
The safe origin log identifies the same isolated candidate. All 26 shared corpus
originals still match; no archive changes, deletions, or capture errors occurred.
Fresh preflight and stopped-server logs are present. Numeric stop exit 0 is
coordinator-reported because environment-bearing execution JSON was not opened.

SA20_RED_AUDIT.json records exact outcomes and artifact hashes. This second cell
confirms the bounded metadata nonpreservation finding; it is not a full-suite
run, installed qualification, remedy, or gate promotion. No rerun, test/import,
database, Git, credential, or product action occurred during this data-only
audit. All seven gates remain UNKNOWN.
