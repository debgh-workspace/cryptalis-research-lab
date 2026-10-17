# Integrated cleanup-state and operator-docs candidate: independent hash review

Decision: PASS_INERT_STRUCTURE_AND_ACCEPTED_OVERLAY_HASHES_ONLY.
Reviewed 2026-10-17. Target: experiments/candidate-cleanup-docs-integrated-v1-20261017/source221.

Read preparation report, manifest, state V1/V2 acceptance reviews, docs V2 report and root acceptance. Independently admitted all candidate leaves and all 466 recorded input leaves using ancestor/leaf lstat checks before source hashing. No links or nonregular leaves were accepted; leaves are single-link. Hashing was data-only using isolated standard-library Python; product files and conftest were never imported or executed.

Verified exact namespace: 221 files, 21 directories, 4,461,022 bytes. Every candidate leaf hash and recorded metadata tuple matches. Candidate inodes differ from every input inode. All 466 input hashes and metadata tuples still match equal before/after receipts, including CURRENT_CANDIDATE.json, PREVIEW_FREEZE_20261016.json and checklist. No selection, promotion or checklist mutation was performed by this review.

Exactly six changes against frozen doctor manifest:
- docs/doctor.md
- docs/lifecycle.md
- docs/walkthrough-migration.md
- docs/walkthrough-sqlalchemy.md
- src/cryptalis/_sqlalchemy_transactions.py
- src/cryptalis/sqlalchemy.py

The four docs match accepted docs V2 manifest; both product files match accepted state V2 source bytes and accepted review hashes. Remaining 215 files are unchanged. All 116 original test-tree files, including conftest, are unchanged. External regression packets are not inserted into source221. Diff headers name precisely the six expected paths.

Verified evidence identities:
- Candidate manifest SHA256: e8a69b212e8a1759e7641d6bb1227a3aa728e76badd515a54421d98811e5552c
- Exact six-path diff SHA256: 6f6c935428b3c5a12d2eced8770acb4904496f08073f09f8c68f6588f10b94b4
- Frozen doctor manifest SHA256: 40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7
- Accepted docs V2 manifest SHA256: 67ed59efaa74039de964f629fed3c57aac038fdecab1c90b27d28eb4e7ba69dc
- Accepted state V2 SOURCE.sha256: 6cd50a61c811595d6d05df60962c7bd828adafeb7b9f48f4e5fc8693063ec84c

This accepts structural integration and preserved accepted source identities only. It is not a semantic rereview or combined-source execution qualification. Prior direct-helper evidence remains separate. No imports, compilation, tests, build, installation, database/status command, Git, private/credential/pyc reads, publication or promotion occurred. UNKNOWN gates and objective closure remain outside this result.
