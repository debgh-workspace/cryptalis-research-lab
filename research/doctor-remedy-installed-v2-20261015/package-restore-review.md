# Doctor-remedy V2: independent six-file delivery restore

Date: 2026-10-15 UTC.

## Decision

**ACCEPTED_SIX_FILE_PACKAGE_DELIVERY_RESTORE.** The six independently fetched files at exact commit `220d35ce796b913c0cced2bd19b416cf287011c9` directly equal their local publication/accepted-artifact counterparts. Their Git blob identities and SHA256 digests match. The four linked Git trees independently recompute to their reported identities. The downloaded sdist and wheel were restored as inert files, fully admitted, safely extracted into fresh review-owned directories and compared with the already accepted source/package expectations.

This is a six-file package delivery and member-restoration result. It is not whole-source221 recovery, environment restoration, dependency restoration, execution, installation, database qualification or clean-host reproduction. No Git write or new publication occurred.

Repository: `debgh-workspace/cryptalis-research-lab`.

Directory: [preview/artifacts/doctor-remedy-v2-20261015 at the exact commit](https://github.com/debgh-workspace/cryptalis-research-lab/tree/220d35ce796b913c0cced2bd19b416cf287011c9/preview/artifacts/doctor-remedy-v2-20261015).

## Independent remote identity and exact bytes

The reviewer independently fetched the exact-commit API record, the directory at that ref, each of the six files in base64, and the complete four-tree path from the commit root to the delivery directory. No default-branch or moving-ref lookup was substituted. All tree responses were untruncated. The delivery tree contains exactly the six expected ordinary `100644` blobs, without symlink, submodule or extra entry.

The independently recomputed tree chain is:

1. Commit root: `cd827f2df79f8353c0cd73cfa589a8c03489cd96`.
2. preview: `01a3b5570e23d11a6a7ef60ef09644386a1c5ffc`.
3. artifacts: `b35b69f54ce596fc8a9c2e7ed9f23054fcf468ac`.
4. doctor-remedy-v2-20261015: `0c5c3ef37e77af4e3e1736ef792c1a2427ea79d6`.

Each file's locally computed Git blob SHA1 matches the exact-ref contents response and its linked tree entry. Each restored file also directly equals its local counterpart, rather than relying on hash equality alone:

- README.md: 1,241 bytes; SHA256 `44321372e9f052bd8cdf22b0347dd1dcb3c5acbfccfaa73b2fc5389784e766bc`; Git blob `af06f1309113e8be8a04dd25e66cef1f1c10db59`.
- REVIEW.md: 12,514 bytes; SHA256 `20efb7f7e9b43ef78bd8fbb2adae668b1b7697017ecded51178942170a614404`; Git blob `924c0d122974a21c60c7c7fd82a40ffd9ff8da0d`.
- ACTUAL_ARTIFACTS.json: 2,401 bytes; SHA256 `0a8a7d1a996a9cd5f14e03a60edbc09e330bc4746648181ed511220aa9bbd089`; Git blob `2286565384425c7db1d5ec968f839ddd4f7ac921`.
- verification.json: 1,432 bytes; SHA256 `1b64c49c2c81a63d11412049c6ba3c3e18c183585df8bfaf2b5b514b2a450802`; Git blob `9135a3378c58926fedc2f4332c5c0b77a331ebb6`.
- cryptalis-0.1.0-py3-none-any.whl: 140,953 bytes; SHA256 `053f06f9277cc5f15f38887f79a44d91dac98a5b94f2ef2fae5329d0f3086965`; Git blob `22b5929a3ca5db13800af7d7acf80b9547f7de16`.
- cryptalis-0.1.0.tar.gz: 150,427 bytes; SHA256 `2e2a3cfc266602b958e4f4b2206c4d7ccc9e8d1de154ef0412141f529446a330`; Git blob `a4d1aab08b02d194812f8c9f0dc5c5246f84b842`.

The outer README comparison uses the exact root-authored publication note at `persistence-recovery-20261013/doctor-remedy-artifact-publication-2312/README.md`. It is not confused with the README packaged inside the distributions. The other five counterpart files are the accepted independent review/index and actual V2 verifier/direct-wheel/first-sdist outputs.

## Safe archive restoration and source closure

The downloaded archives retain the accepted exact inventories: 49 sdist regular payloads and six directories, and 48 wheel regular payloads and six directories. Their uncompressed payload totals remain 581,851 and 475,528 bytes respectively. Every member name/type/size/link/attribute boundary was admitted before payload extraction. The independent checks include bounded gzip expansion, TAR metadata, ZIP central/local-header agreement, fixed flags/times/modes/compression and bounded nonoverlapping spans. No unexpected, duplicate, absolute, traversing, linked, sparse or special member was admitted.

The six delivery files were written exclusively under `restored/`. The admitted archive members were written exclusively under fresh `sdist-members/` and `wheel-members/`, as nonexecutable ordinary files. Their final namespaces contain exactly the expected 49 and 48 payloads, with every file directly equal to its decoded archive member. None was executed or imported.

All 43 runtime modules in both remote archives directly equal the accepted local source and its complete manifest `40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7`. Source README, license, lock and original/normalized configuration checks pass. PKG-INFO equals METADATA, whose description exactly equals the packaged README. Console entry remains `cryptalis.cli:main`.

The wheel has exactly 48 unique RECORD rows covering all payloads, 47 correct SHA256/size entries and empty self fields. The remote verifier and artifact index are exact copies of the already accepted packaging evidence. Their correct source/artifact identities and UNKNOWN gate boundary were independently checked. Full remote/local archive byte equality preserves the accepted CLI/RECORD-only delta against README-v2 without manufacturing another runtime result.

The remote-member audit re-admitted/rehashed its 158 finite input/restored payloads at the end, with unchanged recorded metadata and identities.

## Scope note and retained optional failure

The outer README correctly keeps fresh installed-successor tests pending, the existing selected installed preview at original Integrated221, all 34 objectives active and all seven gates UNKNOWN. It distinguishes the accepted narrow six-case source regression and same-host packaging equality from full-suite execution, public smoke, clean-host reproduction and production qualification. Its artifact/source/review hashes match the independently restored files.

An optional reviewer attempt to reconstruct canonical raw commit bytes from normalized API author/date/message fields did not reproduce the commit SHA. That overstrong reconstruction assumption is not used as a delivery gate or represented as a repository corruption. The exact-commit API identity and its linked recomputed tree/blob objects are the available evidence. The API reports the commit unsigned, and this review supplies no signature or cryptographic signer-authentication claim.

A subsequent optional `.patch` request returned GitHub error 422 because the connector interpreted the `.patch` suffix as part of the SHA. No alternate route or credential workaround was used. The failed reviewer attempt, its source/stdout/stderr/exit and `COMMIT_OBJECT_LIMIT.json` are preserved. Root explicitly confirmed the scoped exact-commit/tree/blob/SHA256 evidence boundary. Raw commit-object reconstruction remains unclaimed.

The corrected six-file restoration and separate archive/member audit both completed successfully. `FETCH_METADATA.json` retains the exact-ref metadata with tokenized download URLs excluded; `FILE_CHECKS.json` retains Git/file identity results; `RESTORE_CHECKS.json` retains all direct comparisons, member/source checks and read ledger. `EVIDENCE.sha256` seals these records, programs, fetch chunks, restored delivery files and inert extracted members.

All writes were confined to this fresh independent review directory. No accepted source, packet, predecessor, database, installed environment or remote Git state was changed.
