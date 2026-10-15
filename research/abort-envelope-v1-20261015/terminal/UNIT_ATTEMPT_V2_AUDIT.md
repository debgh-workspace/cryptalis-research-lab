# Independent terminal audit: selected unit attempt v2

## Verdict

INCOMPLETE UNIT ATTEMPT. ONE METHOD COMPLETED; THE BOUNDARY METHOD HAS NO TERMINAL TEST RESULT; SEVENTEEN METHODS DID NOT START.

Do not report 19 passing methods. There is no recorded assertion failure or Python traceback. The process ended by SIGKILL, but the receipt does not establish which mechanism caused that signal. The source/math review remains source-only for the uncompleted methods.

This audit made no launch, retry, reference import, test collection, or test execution. It inspected only the named safe receipt files, the named root selector as data, and finite already-admitted source. No product or database effects occurred in this review.

## Exact evidence

Receipt directory: `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/abort-envelope-unit-v2-root`.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| selection.json | 1,610 | b5d8769c81d84f4f35f21f2d7ce13d34d1101fbc6cd5c951d75505d8835fdd22 |
| RESULT.json | 230 | 3b98eede1f30323effea064c624a4bc8bcf5253dd06ff4d2d8adba2977d3843b |
| stdout.log | 64 | 171eb50fc9892a5c6f5a14d495fcb1de62d02c7908de00c28434972f4047584d |
| stderr.log | 297 | d958399eebedddb65c1947058088a715f9967f9d90823d6fedcfec3a99309c6f |
| /tmp/cryptalis_abort_envelope_unit_root_1757.py | 2,672 | c7ea7a108aaf0755f3f873397c0684e8972220d3adb305a4ae4d8bef43d7002c |

The recorded process command used the selected Python 3.12 binary with `-I -B -S` and the sealed unit runner. The selection set RLIMIT_CPU soft=hard=30 seconds, a 60-second parent wall timeout, and a 2 MiB per-file limit. The helper did not select an address-space/RSS limit and did not record child CPU use or peak RSS.

The parent result reports return code -9, timeout=false, wall_seconds=32.526492753007915, and all five selected source/review pins unchanged. The wall measurement includes small parent work around the child; it is not the child's CPU consumption. This reviewer independently rehashed all five pinned files and confirmed that each still matches its selected hash.

The only stdout line announces an expected count of 19. It is not a completion line. Stderr records:

1. `sealed_abort_envelope_vectors_0.ReferenceVectors.test_cursor_domains_and_exact_widths`: completed `ok`.
2. `sealed_abort_envelope_vectors_0.ReferenceVectors.test_exact_canonical_and_native_candidate_budget_edges`: started, with no following `ok`, failure, error, or suite summary.

No later method is reported as started. The aggregate attempt is incomplete even though the completed cursor method is useful retained evidence.

## What the termination establishes and does not establish

- The exit code establishes SIGKILL termination of the selected child, not the identity of the killer.
- The 30-second CPU hard limit and approximately 32.5-second elapsed observation are consistent with that limit being insufficient. This is a plausible explanation, not a confirmed kernel diagnosis.
- timeout=false means the selector did not enter its subprocess wall-timeout handler. It does not exclude an external supervisor or another resource limit.
- The two tiny log files are far below the selected per-file limit. Their observed sizes give no evidence that output capacity was exhausted.
- Child user CPU, system CPU, peak RSS, and memory-limit events were not captured. They cannot be reconstructed from these receipts alone. No claim of out-of-memory, proven CPU exhaustion, leak, or algorithm failure is justified.
- The source shows substantial deterministic pure counting work. It does not prove how much of that work completed before termination. No individual boundary margin can be marked passed from the method-start line.

## Source-derived work accounting

The interrupted method retains six genuine near-16-MiB boundary values: three native-candidate margins and three canonical margins. Those six values are not six constant-time length operations.

For each native-candidate margin, `sizes(maximum_state(...))` traverses the large filler three times: initial `validate_state` sizing, final sizing within `maximum_state`, and the outer sizing call. `check_expansion_reservation` traverses it three more times by the same constructor-plus-measurement path. This is six full scans per margin, or eighteen across the three margins.

Each of the three canonical-margin cases also performs three full scans. The complete method therefore makes twenty-seven near-16-MiB string scans, approximately 453 million Python character iterations, plus small structural work. Each iteration performs Unicode/type-domain checks, escape classification, and UTF-8 byte counting. The initial empty-filler baseline is additional small work.

The implementation uses deepcopy for containers, but immutable Python strings are shared by deepcopy. That observation does not establish the measured process peak RSS. Replacing a filler can temporarily keep the old and new large strings live, and the interpreter has other allocations. Actual RSS must be measured rather than inferred from byte budgets.

The selected 30-second CPU allowance did not account explicitly for this twenty-seven-scan workload. This is enough reason to reconsider the launch budget before treating termination as a defect in the byte formula. Do not optimize or change the sealed reference merely to obtain a green result, and do not replace the real 16-MiB vectors with smaller limits.

## Minimal continuation for root to select

Preserve the existing receipt, logs, selector, source pins and review. Do not rerun the completed cursor method solely to rebuild an aggregate count.

### Partition A: seventeen unstarted methods

Use the same exact three source files and independent correction. Load the same nineteen source-defined methods, then select exactly the seventeen whose full IDs are neither of the following:

- `sealed_abort_envelope_vectors_0.ReferenceVectors.test_cursor_domains_and_exact_widths`
- `sealed_abort_envelope_vectors_0.ReferenceVectors.test_exact_canonical_and_native_candidate_budget_edges`

Require the selected count to be exactly 17 and record all selected IDs before starting. This includes ten remaining original methods plus all seven correction methods. None of those methods contains the six large filler allocations. Their actual runtime remains to be observed. A fresh receipt and launcher are required; leave the sealed original runner unchanged.

### Partition B: the one incomplete boundary method

Run exactly `sealed_abort_envelope_vectors_0.ReferenceVectors.test_exact_canonical_and_native_candidate_budget_edges` against the unchanged reference and test source. Its earlier partial execution cannot be resumed reliably because no per-margin terminal receipts exist. Repeating this incomplete method is necessary; repeating the already completed cursor method is not.

Root should select a finite budget that acknowledges twenty-seven full scans. One conservative explicit proposal is a 600-second CPU soft limit, 660-second CPU hard limit and 900-second wall limit, retaining the 2 MiB output-file cap. These are proposed stopping limits, not measured requirements or a guarantee of completion. A lower limit should be justified by measured comparable counting work rather than an assumed six cheap operations. A distinct soft/hard CPU limit makes a budget-exhaustion signal more informative than soft=hard, while never removing the terminal hard stop.

Do not add a new unmeasured memory cap just to force another termination. Record actual peak RSS first. If root requires a stricter memory constraint, select and document it explicitly as another proof boundary.

### Resource and result receipts for both partitions

Use a fresh parent process with only the selected proof child, or direct per-child wait4 accounting, so child resource measurements are attributable. Record at minimum:

- exact interpreter/argv, source hashes, selected method IDs and expected count;
- every selected soft/hard CPU, wall, output and any memory limit;
- parent monotonic elapsed time and timeout flag;
- child exit status or signal;
- child user CPU seconds, system CPU seconds and peak RSS, including their units;
- completed method IDs and test outcome, with no promotion of started-only methods;
- before/after source hashes and full bounded stdout/stderr.

A fresh single-child selector may read RUSAGE_CHILDREN before and after its wait: user/system CPU deltas are useful, and the sole child's peak RSS is attributable in that fresh process. Do not subtract peak RSS values across multiple children and call the difference a per-child peak. On Linux, label ru_maxrss as KiB. A direct wait4 result is preferable when available and compatible with the selected timeout handling. Resource accounting must still be written after a signaled exit.

If either partition fails an assertion, preserve that failure and request a fresh authored correction. If it ends by signal or timeout, preserve the partial ledger and use the new measurements to distinguish a selected-budget limit from an actual test result. Do not silently retry or change expectations.

## Aggregate stopping condition

Only after all seventeen newly selected methods and the one boundary method have terminal successful results, with unchanged source hashes, may root report that all nineteen methods have individually completed successfully across preserved attempts. State that this is an aggregate across attempts, not a successful original 19-method invocation. If any result remains incomplete, the unit proof remains open.

Even successful completion does not admit PostgreSQL, real journal data, physical relation/PK/ACL mutations, cutover helpers, product execution, or v3. No such continuation was selected or run by this reviewer.
