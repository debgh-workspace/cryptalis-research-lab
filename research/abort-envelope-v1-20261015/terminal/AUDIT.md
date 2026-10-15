# Independent terminal audit: abort-envelope pure-reference unit attempts

## Verdict

**ACCEPTED, narrowly: all nineteen source-defined methods individually completed successfully across three preserved attempts.** This is not a successful original nineteen-method invocation. The original invocation remains an incomplete SIGKILL result.

The successful coverage is exactly one original cursor method, seventeen previously unstarted light methods, and the one previously incomplete boundary method. There are nineteen unique successful methods, no duplicate successful completion, and no missing source-defined method. There were twenty method starts in total because the incomplete boundary method was necessarily restarted once.

The selected unit question is closed. These results do not establish PostgreSQL conformance, native representation equality, product behavior, journal validity, SQL ordering/rollback, physical relation/PK/ACL safety, authenticated ancestry, a v3 implementation, or a general abort guarantee. Any separately selected database probe is outside this audit.

## Review procedure and scope

I inspected metadata before bounded source/receipt contents and read only the named, finite evidence for this task. I checked the source as text and with Python AST parsing; I did not import the reference, test modules, launchers, or root helpers; collect tests; execute or rerun tests; access a database; inspect live execution cells; or use Git. I did not inspect corpus, environment, credentials, caches, or raw phase data. The boundary receipt was opened only after root explicitly reported it terminal.

The independently owned output is this directory. All existing source, review, launch, and receipt files were read-only inputs. The machine-readable `RECEIPT_VERIFICATION.json` contains exact source method IDs, per-attempt successful/started IDs, all resource result fields, finite input sizes/hashes, and assertion-backed merge checks. `SHASUMS.txt` records digests of this audit packet's current bytes.

## Actual terminal outcomes and selected bounds

| Attempt | Completed methods | Child exit | Parent wall s | Child user CPU s | Child system CPU s | Child peak RSS KiB | Selected CPU soft/hard s | Wall limit s |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: |
| original v2 | 1; boundary incomplete; 17 unstarted | -9, SIGKILL | 32.526492753 | not retained | not retained | not retained | 30 / 30 | 60 |
| split v3 light17 | 17 PASS | 0 | 0.152876270 | 0.104869 | 0.012009 | 14,976 | 30 / 30 | 60 |
| split v3 boundary1 | 1 PASS | 0 | 100.776303728 | 100.687680 | 0.054236 | 64,004 | 240 / 240 | 300 |

Every attempt selected a 2,097,152-byte (2 MiB) per-file limit. All retained stdout/stderr files are below it. Both split results record no signal and no wall timeout. No new address-space or RSS cap was selected by either helper; this does not inventory inherited environment constraints.

The light unittest summary is `Ran 17 tests in 0.044s`, `OK`. The boundary summary is `Ran 1 test in 100.683s`, `OK`. Parent wall duration includes launch/wait polling and post-child pin verification; it is not the unittest duration or CPU time.

The split helper reaps the exact launched PID through `os.wait4`, obtains user/system seconds and the child's lifetime peak RSS, and retains accounting even for a signaled exit. It assigns the already-reaped status to the subprocess object. This avoids attributing a cumulative collection of unrelated children to the proof child. The recorded Linux `ru_maxrss` unit is KiB, not bytes. Per-method RSS records are process-lifetime peaks at method return, not isolated per-method allocation or RSS deltas; they must not be summed or subtracted to infer memory consumption.

Boundary total child CPU is 100.741916 seconds. The measured complete work exceeds the original thirty-second CPU budget, making insufficient budget a concrete explanation for why that original attempt could not finish equivalent work. It still does not establish the original kernel's exact SIGKILL cause. Original child CPU/RSS and kill-source telemetry were not retained, and cannot be reconstructed from these receipts. There was no recorded assertion failure or traceback in that attempt.

## Method partition and result integrity

The unchanged original source defines twelve `ReferenceVectors` methods. The unchanged correction defines seven `DecidingVectors` methods. Static AST enumeration gives nineteen distinct IDs and matches the actual split selection list exactly.

The original first two methods, in the loader's alphabetical order, are:

1. `sealed_abort_envelope_vectors_0.ReferenceVectors.test_cursor_domains_and_exact_widths`: has a terminal `ok` in original stderr.
2. `sealed_abort_envelope_vectors_0.ReferenceVectors.test_exact_canonical_and_native_candidate_budget_edges`: started in original stderr but has no terminal outcome there.

The split launcher loads all nineteen before selecting, checks total and unique counts and the two partition members, and excludes the already successful cursor in both modes. `light17` selects precisely the remaining ten original methods plus all seven correction methods. `boundary1` selects precisely the incomplete boundary method.

For each split, I independently verified:

- Selection IDs exactly equal the intended source-derived partition, with no extras, duplicates or omissions.
- Every selected method has exactly one ordered `method_started`, `method_ok`, and `method_returned` sequence, and a matching stderr `... ok`.
- The terminal JSON has the exact selected/executed count, `successful: true`, and zero failures, errors and skips.
- Unittest ends with the matching `Ran N test(s)` and `OK` summary; child exit is zero.
- The sealed launcher additionally excludes expected failures and unexpected successes from partition success, even though those counts are not separately emitted in terminal JSON.
- The merge of successful IDs across all attempts is exactly the nineteen source-defined IDs. Only the interrupted method is started twice, and its successful completion is counted once.

These counts are unittest methods, not individual assertions, loop iterations, vectors or subtests. Three source `subTest` call sites are present; no separate subtest ledger was retained. The six genuine near-16-MiB boundary cases run in ordinary loops, with margins -1, 0 and +1 for the native-spacing candidate and the canonical count. A successful method with the unchanged straight-line loop source supports completion of its assertions, but does not yield six independent terminal resource/receipt records.

The unchanged boundary source still uses `DOCUMENT_LIMIT = 16 * 1024 * 1024` and actual large filler strings. It has not replaced vectors with smaller data or altered expected results. Static source confirms the repeated sizing paths behind the earlier estimate of twenty-seven near-16-MiB scans. This audit did not rerun or optimize that work.

## Exact source and launcher pins

The original helper and original receipt pin five files. Each split receipt pins the same six files, substituting the split launcher and adding its preparation note. All current digests match their recorded values. The three reference/test source pins are identical across all attempts.

| Pinned file | SHA-256 |
| --- | --- |
| envelope_reference.py | 27584299ffaac34c2bb9a0a51671a5873ab76354649052fd8f7725b62f38564c |
| test_envelope_reference.py | 152f8c605be07d5a63877f09942f66c3f89045457dad051cd8b85a780aa60d6c |
| correction-v2/test_deciding_vectors.py | e631a11f36b346984cee7304d22abefa2099e61c760d08a414af93d32fccf8cc |
| prior REVIEW.md | a15a3cc81b5ad65734a22d9691538ad94cd26b28e7c52961586a9ac2eb77c021 |
| original UNIT_RUNNER.py | 665cfa4894726559623e7d56511c76890f18e8a40f617460f9f68712503d63e9 |
| UNIT_RUNNER_SPLIT_V3.py | f9b36facdb5d208fd217f243152ac79642aa5bd5fb4b80fb33d63b1d1bd1e546 |
| SPLIT_V3_PREPARATION.md | 081720008501e6d728a5a0eae16cbd080830a0f04203836c60c0aee57afe7dc2 |
| retained UNIT_ATTEMPT_V2_AUDIT.md | fe3e942d2610220b6c4f3fec0058bb0de6dc3b2f411a613b451a73d63bf1f455 |

Source roots are `cryptalis-executable/experiments/aborted-successor-envelope-v1-20261015` and `cryptalis-executable/reviewer-notes/aborted-successor-envelope-independent-20261015`, relative to `/workspace/scratch/cb28ee9f5f4a`.

The exact root selector source hashes are:

- `/tmp/cryptalis_abort_envelope_unit_root_1757.py`: c7ea7a108aaf0755f3f873397c0684e8972220d3adb305a4ae4d8bef43d7002c
- `/tmp/cryptalis_abort_envelope_split_root_1810.py`: c8bd81c9b330f2c6a8f3b902d1a4cd67950029014105ebfbbfea9dd32d1f2c34

Both helper sources check the selected Python 3.12 binary against `fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7` and launch with `-I -B -S`. This reviewer read those checks as source but did not independently hash or execute the interpreter. The interpreter digest and root helper hash are not fields in selection JSON; their provenance is the retained helper source and this audit, not a separate binary-attestation receipt.

The helpers verify source pins before launching and after the child exits, and both split result files state that pins are unchanged. This reviewer independently rehashed them. The source's retained “unexecuted” preparation comments are left byte-identical; terminal receipts, rather than those historical comments, establish which methods have since executed.

## Preservation of the initial incomplete attempt

Original directory: `persistence-recovery-20261013/abort-envelope-unit-v2-root`.

| File | Bytes | Preserved SHA-256 |
| --- | ---: | --- |
| selection.json | 1,610 | b5d8769c81d84f4f35f21f2d7ce13d34d1101fbc6cd5c951d75505d8835fdd22 |
| RESULT.json | 230 | 3b98eede1f30323effea064c624a4bc8bcf5253dd06ff4d2d8adba2977d3843b |
| stdout.log | 64 | 171eb50fc9892a5c6f5a14d495fcb1de62d02c7908de00c28434972f4047584d |
| stderr.log | 297 | d958399eebedddb65c1947058088a715f9967f9d90823d6fedcfec3a99309c6f |

These match the earlier independent terminal audit exactly. The SIGKILL and partial progress remain in the evidence; no green result overwrote or reclassified them.

Fresh split directories are `persistence-recovery-20261013/abort-envelope-unit-v3-light17-root` and `persistence-recovery-20261013/abort-envelope-unit-v3-boundary1-root`. Their four files each are hashed with sizes in the machine-readable verification. No original or split receipt was edited by this audit.

## Closing statement

The defensible result is: **nineteen individually successful pure-reference unit methods across preserved attempts, including the full-size boundary method under a separately selected larger finite budget.** The original attempt remains incomplete, and the initial SIGKILL cause remains unproven. Unit success neither selects nor authorizes further execution and does not remove any native, product, authority, lifecycle, or historical-abort proof obligation.
