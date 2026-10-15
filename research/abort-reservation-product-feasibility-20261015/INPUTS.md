# Source inputs and preparation record

Date: 2026-10-15 UTC. This is a finite source-only inspection record.

Base: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable
Source: candidate-cluster-retained-integrated-v2-20261015
Output: reviewer-notes/abort-reservation-product-feasibility-20261015

No whole-tree selected manifest was checked. Exact whole-file hashes below
identify finite inputs; they do not mean every line was reviewed. The primary
six product module hashes match the values in the prior envelope INPUTS.md.

## Primary product evidence

| File under source | Bytes | SHA-256 |
|---|---:|---|
| src/cryptalis/migration.py | 54457 | 94344b2f98e0969d9f8b3d41cc9dca6e7d01a5e785a5b3af33431c41e55d2014 |
| src/cryptalis/deprotection.py | 33755 | de1a3dadd276cfce204c18d74aa62dff3828caff2eef7ef8103f316d4880e6d6 |
| src/cryptalis/_object_comments.py | 13637 | 25cf4c00173c6de336382ea7e6f0be26e009a32cd2e3ccbfad37032d3a09a0d8 |
| src/cryptalis/_transition_json.py | 2150 | 2110f79fc1f38500daaaa2da814224afda9a9a92a5e8e776420d9168736d8a19 |
| src/cryptalis/manifest/compiler.py | 51172 | dca174cba23517abfcb03e8a1df7ef12f9f7e1171b765e3c1b2da26edb23951b |
| src/cryptalis/manifest/parser.py | 3380 | 47cd75cc2ca611fe186d36d5d046317b0746714945c11fd2f84917d2f1020448 |

Read focus: artifact constructors and limits; forward/reverse expansion, state
reads/writes, progress/verification, switch, abort, replan and removal; exact
native schema/guard producers; compiler record codecs and canonical encoding;
artifact parsing and counters. Findings cite the unchanged original line numbers.

## Prior proof and native-probe source

| File under base | Bytes | SHA-256 |
|---|---:|---|
| experiments/aborted-successor-envelope-v1-20261015/SPEC.md | 11901 | 5f0b8c49fbcc8a2b34ade55d7ab0d9dc6bf313e982cbbb0a6b10bae294e5a472 |
| experiments/aborted-successor-envelope-v1-20261015/envelope_reference.py | 16279 | 27584299ffaac34c2bb9a0a51671a5873ab76354649052fd8f7725b62f38564c |
| experiments/aborted-successor-envelope-v1-20261015/JOURNAL_VALIDATOR.md | 10506 | 0af03843cabb8fcda93f078c582a4e4c45c48e824875bd3309cbee299b5ac9ea |
| experiments/abort-envelope-native-probe-v2-20261015/PROTOCOL.md | 14214 | 0dffbad803eb6b0e63b28483c198373848d38df82339602b7f177c39e9eacdbc |
| experiments/abort-envelope-native-probe-v2-20261015/test_native_envelope.py | 17866 | 0714ef753d9e86b55e711d09419853f0ec75693c84cb623b9a60c99222b9a2a6 |

Also read the prior envelope INPUTS.md and correction-v2/CORRECTION.md as
source/provenance. Their declarations of preparation status were not reclassified
as current runtime outcomes. Native V2 totals in FINDING.md are attributed to
root and remain unaudited by this worker.

## Supporting finite reads

- Source AGENTS.md (6154 bytes), plus ENGINEERING_PLAYBOOK.md (10762 bytes) in
  finite excerpts. The task's no-Git/no-runtime boundary took precedence over
  generic repository continuation/testing directions.
- Source docs/lifecycle.md (28326 bytes), docs/security.md (31672 bytes), and
  docs/compatibility.md (26001 bytes): focused literal searches and lifecycle
  excerpts only. No product runtime status command was run.
- Source src/cryptalis/cli.py (17882 bytes): bounded reader searches/excerpts;
  doctor.py (11085 bytes): literal symbol search only. Those searches did not
  identify a bounded journal consumer.
- Source tests/test_candidate_envelope.py (7572 bytes) and
  tests/test_maintenance_budget_boundary.py (6567 bytes): read as text only.
  The former concerns ciphertext framing, not the journal reservation.
  No test module was imported, collected or executed.

## Preparation limits and process disclosure

Only shell metadata, finite text reads/searches, sha256sum, and writes within
this new output directory were used. No Python interpreter, product/reference
import, compilation, test collection/run, database/status command, live cell,
corpus, credential, installation, network or Git action was performed. No
existing source, experiment or evidence file was edited or copied for a patch.

The initial bounded max-depth metadata inventory listed filenames and sizes
under tests/__pycache__ before inventory scope was narrowed. No cache file
content was opened, no cache was changed, and no cache supplied evidence.
This metadata-only exposure was reported to root. Later inventories excluded
those paths. Do not inaccurately describe this as zero cache-path metadata access.

A requested cloud software-engineering skill was unavailable. That failure did
not cause runtime work or broaden source authority. Review used the approved
source and task boundaries.

Root's follow-up directed an exact feasibility finding, separation of the
current durable-ABORTED replan gap, future expansion-hook obligations, and no
product patch or further tests. This packet follows that narrower disposition.

Deliverables: FINDING.md, NEXT_SLICE.md, INPUTS.md and their SHA256SUMS.txt.
There is no executable entry point and nothing is promoted.
