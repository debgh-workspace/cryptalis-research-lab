# Independent S23 compatibility add-on publication review

2026-10-14. Agent 2. ACCEPT the exact archive for separately authorized publication. This is a data-only evidence recovery review, not product qualification. No archived code, tests, database, reconciler, Git or network operation was executed.

## Exact archive and fresh restore

CRYPTALIS_S23_CORPUS_EVIDENCE_ADDON_20261014.tar.xz is 194,036 bytes with SHA-256 57172b6a67ffc6dcba6c083d37a45574d2787ecfc246765fe3fbe6b02ef96944. The final whole-file recheck matches.

An independent new extraction contains exactly 263 ordinary, unique, normalized relative files: 249 allowlisted evidence files and 14 metadata files, totaling 5,395,692 uncompressed bytes. No absolute/traversal paths, links, devices or other special members were admitted. Every restored member size/hash matches. All 249 allowlist entries exactly match the archive inventory and current original files. Thirteen preparation metadata files match the archived copies. PAYLOAD_MANIFEST.json correctly pins the other 262 files, excluding its own self-reference; its own bytes are bound by the checked whole-archive hash.

## Complete consumed-input mapping

Independently deriving the union of the two included aggregate hash maps gives exactly 1,549 unique consumed paths. INPUT_REFERENCE_MAP.json has the same complete key set and hashes, with no unresolved or extra paths:

- 152 included at the exact path
- 110 mapped to included byte-identical aliases
- 1,287 mapped to exact members of the frozen S23 source capsule

Every alias hash matches its included bytes. The referenced source capsule matches SHA-256 41c756d905f84f4754208ba4d27bda87621ab88d0bac58fcf421c7bbcbf50870 and 1,750,488 bytes. All 213 referenced source members match the preserved source manifest. No dependency on current live source contents is needed to resolve those references once both capsules are available. The source tree and duplicated archived snapshots are intentionally not physically included in this add-on. This is selected evidence recovery, not an operational lab restore.

## Failure history and composite boundaries

The included S22 failed aggregate remains byte-identical at a08a9f60ce5f2865189b14b4d10f24d96a7544cad6fd7be00b57fc79b2344e86: INCOMPLETE_OR_FAILED, 398 IDENTICAL / 155 REJECTED-LOUD / one TEST_FAILURE. Its separate one-cell additive correction remains intact. The prior S22 evidence add-on reference matches 120,344 bytes and SHA-256 079a8bdf19faddc0ea41a02db04eb3828e444eebd4f8ae5d56e87cd36f733815. Safe JUnit members in that referenced archive still show the original SQLModel eleven passes/one failure and the separate one-pass retest.

The archived v1 synthetic RED result remains 25/41, including all sixteen failed controls; v2 GREEN remains 41/41. Control booleans independently sum to those totals and each target hash matches the included source version. The preparation-stage v1 selection failure is also retained. The baseline eight-case synthetic result stays explicitly coordinator-reported; no raw result was invented.

The archived composite retains SHA-256 84cc859b2bb4cf742f85f68cebb9ce23bb3975a74da86450a2484508d7dfc7e6. An independent set comparison of the included inputs confirms the exact disjoint 554+46 union: 600 keys, 444 IDENTICAL and 156 REJECTED-LOUD. The original 82 missing-combination rows remain unchanged, with separate 36 remaining rows and original reasons. The result combines seven finite source-overlay campaigns. It does not claim one 600-test invocation, full installed behavior or exact whole dependency-environment identity. Async safe identity gaps, pre-run-only baseline identities, source-derived warm-mapper profile correspondence and all seven UNKNOWN gates remain explicit.

## Privacy and publication limits

No forbidden raw tests.json, package-origin.json, readiness/start/stop execution JSON, environment dumps, credential files, private-home material, installed environments, caches or database/runtime contents are present. Every archive member is UTF-8 text. Independent scans of all 263 files, including driver-qualified credential URLs, private-key headers and high-confidence provider/access-token patterns, found no matches. Parsed JSON/JSONL contains no environment objects. These are bounded checks, not universal proof against arbitrary unrecognized secrets.

No archive labels were rewritten. Preparation NOT RUN/pending statements and local-only recovery labels remain historical snapshots beside later explicit results. Root reports that the referenced source capsule is now remotely complete at 1cdc5c79; this reviewer did not use Git/network or independently verify that remote event. The add-on itself remains local at this review. Publication and exact remote-byte verification are separate actions.

FINAL_REVIEW.json and INDEPENDENT_RESTORE_CHECKS.json record the machine-readable findings and hashes. The fresh-extraction directory contains the independently restored data. No source, original receipt, capsule or authoritative ledger was changed.
