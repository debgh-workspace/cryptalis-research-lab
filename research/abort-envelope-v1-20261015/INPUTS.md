# Finite inputs and execution boundary

Root directory: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable.
All paths below are relative to that directory. Source was inspected only in
finite requested ranges after metadata checks. Entire-file hashes identify
those input files; they do not claim every line was reviewed or executed.

Selected source prefix: candidate-cluster-retained-integrated-v2-20261015/.
Selected 221-file manifest identity was supplied by root and the design finding:
202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520.
No complete selected-tree manifest verification was performed by this worker.

| File under selected source prefix | Bytes | Observed SHA-256 |
|---|---:|---|
| AGENTS.md | 6154 | 38987c61d5d6f65aa4aeb59148e27c238f37c08e121a5ef5dd8e543736e43c01 |
| src/cryptalis/migration.py | 54457 | 94344b2f98e0969d9f8b3d41cc9dca6e7d01a5e785a5b3af33431c41e55d2014 |
| src/cryptalis/deprotection.py | 33755 | de1a3dadd276cfce204c18d74aa62dff3828caff2eef7ef8103f316d4880e6d6 |
| src/cryptalis/_transition_json.py | 2150 | 2110f79fc1f38500daaaa2da814224afda9a9a92a5e8e776420d9168736d8a19 |
| src/cryptalis/_object_comments.py | 13637 | 25cf4c00173c6de336382ea7e6f0be26e009a32cd2e3ccbfad37032d3a09a0d8 |
| src/cryptalis/manifest/compiler.py | 51172 | dca174cba23517abfcb03e8a1df7ef12f9f7e1171b765e3c1b2da26edb23951b |
| src/cryptalis/manifest/parser.py | 3380 | 47cd75cc2ca611fe186d36d5d046317b0746714945c11fd2f84917d2f1020448 |

| Design input | Bytes | Observed SHA-256 |
|---|---:|---|
| reviewer-notes/aborted-replan-followon-20261015/FINDING.md | 18001 | ddbfd8378f4a4f446070ab01b59654e319bca8f12370a6d8e2ec0908a9c6a178 |
| reviewer-notes/aborted-replan-followon-20261015/INPUTS.json | 6285 | 99390ecd3c5c341ce40ee60df6fdc4a783d8cbd487f1397581d051c1cdc6fc60 |
| reviewer-notes/aborted-successor-design-independent-20261015/REVIEW.md | 23778 | 1cc67af070f5ca7a2a8aa36647f150b62b4da585c2d9ef5875ab6355f5525fc0 |
| reviewer-notes/aborted-successor-design-independent-20261015/ENVELOPE_AND_JOURNAL_PROOF.md | 13770 | bdfe6c9ccd897eb722809fb8e84512378d8b61463597eb95e388e2b4d15f38ef |

Source read focus: migration field construction, permission checks, streaming,
scope, progress, verification, switch and abort; corresponding deprotection
paths; compiler identity codecs, canonical encoder and schema facts; artifact
JSON depth/integer/Unicode limits; existing comment reverse-envelope reservation.
Design REVIEW.md was read in focused excerpts, including exact lines 27–60 for
the proposed summary schemas. ENVELOPE_AND_JOURNAL_PROOF.md and original FINDING
were read as the proof prerequisites. A bounded metadata directory listing
located the source tree; no unrelated file content was consumed.

The design reviewer explicitly confirmed in coordination that exact scope N
with rows/chunks<=N checked before chunk SQL suffices without assuming 16-digit
journal integers. The optional 2**53-1 new-operation profile is distinct from
the artifact history-count grammar. No v3 wire format or execution is enabled.

Only experiments/aborted-successor-envelope-v1-20261015 was written. The permitted
work was static reads, metadata and SHA-256 checks, and new source/text files.
No product/reference import, Python interpreter, compile, test collection/run,
database, runtime status, Git, installation, external network, live cell, corpus,
environment, credential, cache or raw phase inspection occurred. Native driver,
PostgreSQL and controlled-transaction statements are protocol text only.

The existing software-engineering instruction skill was read for task routing;
it is not product evidence. Work remained in the already assigned task and did
not start a new execution environment. No runtime verification claim is made.
