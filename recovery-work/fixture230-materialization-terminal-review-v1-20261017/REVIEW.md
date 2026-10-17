# Independent actual fixture230 materialization review

Decision: ACCEPTED_SOURCE_COPY_ONLY. The separately selected source-copy operation completed successfully and its actual output passes independent data-only audit. This acceptance supplies the actual-copy prerequisite for a separately root-selected recording run; it does not assert any new runtime, database, package, deployment, or publication result.

## Actual selection and fixed inputs

Capture: persistence-recovery-20261013/fixture230-copy-v1-20261017-1817. Child exit and external aftercheck exit are both 0; stderr is empty. INVOCATION.json records the exact reviewed materializer, ROOT_SELECTS_SOURCE_COPY token, and SOURCE seal c62d8f86bfe6d48a805c290d74b04b8d10cbdd0564a7d4793509eafae0a28fc6. Cwd is the fixed materializer control directory; stdin is DEVNULL. The shell passes through timeout 60 seconds with TERM and 2-second kill-after, then an inner env -i reset with only LANG=C.UTF-8, LC_ALL=C.UTF-8 and TZ=UTC before pinned Python -I -S -B. Recorded limits are CPU 30 seconds, virtual memory 1048576 KiB, core 0 and file size 4096 blocks. These are the reviewed process bounds, not an aggregate storage or OS descendant-absence proof.

The exact integration manifest SHA256 is fa86e1917f631f8d7698faf444b993f412b27bf5ffa39e251392e91d7152c740. Prior source/control acceptance is recovery-work/fixture230-controls-review-v1-20261017/REVIEW.md, 5784 bytes, SHA256 78ec05a7c28150801387e38f4139278c85e74dc1c2862a8ed0196aca1e271b2d. The manifest remains a proposal descriptor with materialized=false; this actual receipt and audit establish materialization separately.

## Independent output and preservation checks

Actual source: recovery-work/fixture230-materialized-v1-20261017/source.

- Exactly 230 regular single-link files, 21 exact expected descendant directories (22 including the source root), and 4,537,908 source bytes; no additional leaves, symlinks, or directory entries.
- Every output size and SHA256 equals its literal manifest entry and the current corresponding donor. The directory set equals precisely the manifest-derived parent-directory set, so there are no extra empty directories or missing parents. All 230 output inodes are unique and collectively disjoint from every donor inode. Reads used nofollow and stable metadata checks; all finite metadata was admitted before body hashing.
- The composition retains 228 unchanged files from actual composite229, replaces the fixture module, and adds the accepted recording test. All 48 product runtime files are unchanged from that base. Existing source-map review retains the byte-identical native-test suffix and unchanged assertions; no test weakening is introduced by copying.
- Receipt output_readback and source_hashes have the exact 230-name set. All readback hash/metadata results PASS. Complete readback, donor preservation, independent copies and complete namespace flags are true; source_files=230 and runtime_python_files=48.
- Receipt preservation has exactly 234 paths: 230 donors plus three controls and their SOURCE seal. Every metadata, hash and final-metadata result is PASS.
- Root before.json contains complete concrete seven-field metadata and SHA256 for exactly 245 paths. after.json contains exactly the same path set with every pass=true. Independent current metadata and hash checks match every original entry, including donor/control/review/tool and original-patch entries admitted in that finite union. Atime is intentionally excluded from stable metadata.

Actual MATERIALIZATION_RECEIPT.json is 100602 bytes, SHA256 e36828e3c95502e26d2cfaf0b45c031c387c2d404719683e39e9e4cebad0cd28. Its status PASS_SOURCE_COPY_PENDING_INDEPENDENT_REVIEW is retained unchanged; this separate review resolves that review gate.

## Evidence and scope

CHECKS.json records exact evidence sizes/hashes; audit.py is the independent data-only audit, not a target program. Before receipt SHA256: 8af4553272c5b71c67fc8ddfb51f66c5da20524fbfe8c665a2dd7ad4eb092006. After receipt SHA256: 259e4609165d6a92e10314f3d72e93e1117797183b9e0170399743db675a35c0. Invocation SHA256: dfda62d64bd721df3c35ea4fc16a00ddfaa834b42cf068503b56032d4a19fe30.

The reviewer performed no target import, syntax compilation, test execution, copy rerun, DB operation, build, install, Git action or publication. Conftest is only an inert admitted source member. No private/cache/credential bodies were enrolled. Earlier failed attempts and accepted historical evidence are preserved. New 19-case runtime acceptance remains pending a separate selection and terminal review; historical public38 evidence requires its explicit unchanged-source transfer review.
