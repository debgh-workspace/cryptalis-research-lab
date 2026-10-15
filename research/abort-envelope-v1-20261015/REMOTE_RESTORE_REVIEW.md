# Independent remote-restoration review: abort-envelope proof packet

## Verdict

**PASS for exact byte restoration and retained evidence integrity.** The 33-file publication under `research/abort-envelope-v1-20261015/` is present as 170,601 restored bytes. Every file independently matches its retained remote response, expected Git blob ID, prior restoration SHA-256/size record, and explicitly mapped local input. There are no missing, duplicate, or extra restored files. All restored files are ordinary, non-symlink files with mode `0600` and no executable bits.

This verdict establishes preservation of the selected proof packet. It does not admit product execution, PostgreSQL/native conformance, journal validity, physical relation/PK/ACL safety, authenticated ancestry, general abort guarantees, or a product v3 implementation.

## Source identity and provenance

- Repository: `debgh-workspace/cryptalis-research-lab` (private).
- Pinned source commit: `711f8a33efc48492953a6d8d3b6a117937a9441b`.
- Remote directory: `research/abort-envelope-v1-20261015/`.
- Tree recorded by the publication record: `dd8cbdb8b2871a928a170b81001570785aab94a0`.
- Root publication record: `persistence-recovery-20261013/abort-envelope-publication-1835.json` relative to the authorized lab; SHA-256 `0c8d76bee84325238e6b487305d06eb3afad1da72ab531380bac009abe53184f`.
- Remote review entrypoint: https://github.com/debgh-workspace/cryptalis-research-lab/tree/711f8a33efc48492953a6d8d3b6a117937a9441b/research/abort-envelope-v1-20261015

The unfinished restoration already retained all 33 connector content responses in `REMOTE_RESPONSES.json`, the inert restored files, and `RESTORE_VERIFICATION.json`. This completion reused those responses rather than making redundant remote requests. Each retained response identifies the same pinned commit in its display URL. Independent decoding and recomputation confirm each `sha1("blob " + decimal_length + NUL + bytes)` against both the retained remote blob ID and root's exact 33-file publication list. SHA-256 independently agrees with the prior restoration records.

The Git commit/tree objects were not independently queried or reconstructed by this completion, and current branch reachability was not rechecked. The recorded tree is therefore provenance from the publication record, not a new tree-object attestation. No remote state was changed.

## Checks completed

1. The publication list, retained remote response list, prior verification list, and restored file set each contain exactly the same 33 unique paths.
2. All retained base64 bodies decode strictly and equal the restored bytes exactly. Every remote URL is pinned to the source commit and expected path.
3. All 33 recomputed Git blob IDs, SHA-256 values, byte counts, and explicit local byte comparisons agree. Total restored content is 170,601 bytes.
4. `RESTORED_FILES.sha256` names exactly those 33 files and every digest matches. The restored tree contains no links, special files, or additional files; all files are mode `0600`.
5. All ten entries across the root, correction-v2, and terminal embedded `SHASUMS.txt` files resolve inside the restored packet and match. None is missing.
6. All seventeen selected input-pin occurrences across the three receipts match their mapped restored files: five original pins and six pins in each split attempt.
7. All twenty-two terminal-audit metadata references match restored byte counts and digests. Historical absolute paths are treated as recorded provenance and resolved through the explicit restoration map.
8. Each retained result's stdout/stderr byte counts match the restored logs, and all six log files are below their selected 2 MiB per-file limit.
9. Static AST enumeration of the two restored test-source files yields the same nineteen source method IDs as the terminal audit. Parsing produced no code object for execution and imported no restored code.
10. Retained stderr outcomes and split JSON event sequences reproduce the terminal audit's exact successful/started method sets, split selection counts, zero failure/error/skip terminal fields, successful split exits, and nineteen-method union. This was a data review, not a rerun.

`RECHECK_VERIFICATION.json` records the independent results and per-file hashes. The original `REMOTE_RESPONSES.json`, `RESTORE_VERIFICATION.json`, `RESTORED_FILES.sha256`, all restored files, and all explicit local comparison inputs were left unchanged.

## Preserved outcome and limits

The original attempt remains incomplete with exit code `-9`: one cursor method completed, the boundary method started without a terminal result, and seventeen methods were unstarted. Its result and both logs remain byte-identical.

The later light partition records seventeen successful methods and exit zero. The later boundary partition records one successful method and exit zero. Together with the original cursor success, the restored evidence contains exactly nineteen distinct successful methods, no duplicate successful completion, and twenty starts because the interrupted boundary method was restarted once. A successful original nineteen-method invocation is not claimed.

The boundary receipt retains 100.687680 user CPU seconds, 0.054236 system CPU seconds, 64,004 KiB child peak RSS, and 100.776303728 parent-wall seconds under the separately selected 240-second CPU and 300-second wall budgets. Those measurements do not prove the original kernel's exact SIGKILL cause. The original attempt did not retain child CPU/RSS or kill-source telemetry.

The retained preparation documents' earlier “not run” labels describe their preparation stage; they were deliberately not rewritten. The later receipts and terminal audit establish the narrow execution history. The term “split v3” identifies the unit-runner revision and supplies no product-v3 admission.

No reference, tests, launcher, or root helper was imported or executed during this completion. No tests were collected or rerun. No database, live environment, corpus, credentials, held archive, or Git write was used. Only isolated standard-library data, hashing, filesystem metadata, JSON, and AST operations were used, with outputs confined to this review directory. Publication remains the root coordinator's responsibility.

## Seal

`SHASUMS.txt` seals this review, the independent recheck, the retained connector-response bundle, the prior verification, and the 33-file restoration manifest. The restoration manifest in turn seals every restored byte. The seal is an integrity manifest, not a digital signature or external timestamp.
