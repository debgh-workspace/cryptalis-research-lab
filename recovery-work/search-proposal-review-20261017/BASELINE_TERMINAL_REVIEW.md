# Baseline terminal review

Disposition: ACCEPT OBSERVED SAME-HOST SA21 BASELINE CORRECTNESS RESULT, WITH RESOURCE-RECORD LIMITATION. This is not a claim that every proposed resource control was enforced. Candidate execution remains a separate root selection.

Capture: persistence-recovery-20261013/search-new-sa21-baseline-20261017-1317.
Packet: recovery-work/search-next-slice-20261017/runner-v2, seal 4747b053405eafe60a656f95adda95ea483bc3d3cfd676570517206d0e85059c.

## Independently reconciled result

- Child/root exit.txt=0; after-exit.txt=0.
- One terminal CORRECTNESS_JSON: baseline, status PASS, tests_run 25, primary_type and primary_stage null, failures/errors empty, bytecode_absence PASS.
- Parsed closure keys exactly equal VIEWS.baseline's 43 source paths, DEPENDENCIES' 399 paths and six control paths. Exactly 448 distinct entries, each PASS. This checks the exact set, not just a reported count.
- Stderr's 25 successful method names exactly match the 23 catalog-derived names plus test_additional_fallback_and_codecs and test_real_cf1_context_matrix. Final unittest OK is present. The source-bound latter method contains all eight representation/record/tenancy combinations; this capture does not provide a separate per-subtest success ledger.
- Root packet-before.txt and packet-after.txt are identical and contain only successful hash checks. Four control/interpreter before/after metadata records are identical. Current bytecode prefix is also absent.
- stdout 73,034 bytes, SHA256 db1466fd7bb9c189af45c4bdbd3a77d2402bcb50e53c06c7ca95ab9a34eb13e6. stderr 2,742 bytes, SHA256 a437fa03cdbbaf6f89a026c22a22e51cd20f5972d4a3cdf0a3871efee0c4b0f2. Combined observed 75,776 bytes.

## Invocation and resource evidence

The capture includes selection, admission, ulimit readback and exits. Root separately confirmed the actual invocation in a collaboration message at approximately 13:19 UTC; this review records that attestation, not a pre-existing capture argv file:

- cwd: /workspace/scratch/cb28ee9f5f4a/recovery-work/search-next-slice-20261017/runner-v2
- env -i LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC; stdin /dev/null
- /usr/bin/timeout --signal=TERM --kill-after=2s 60s
- /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12 -I -B -S -X pycache_prefix=/workspace/scratch/cb28ee9f5f4a/recovery-work/search-next-slice-20261017/runner-v2/bytecode-absent /workspace/scratch/cb28ee9f5f4a/recovery-work/search-next-slice-20261017/runner-v2/run_correctness.py baseline 4747b053405eafe60a656f95adda95ea483bc3d3cfd676570517206d0e85059c
- Limits read back: CPU 30 seconds, address space 1,048,576 KiB, file 4,096 KiB, core 0. Root confirms these were shell limits around the selected command.

Deviation: no combined-output monitor enforced the proposed 1 MiB combined ceiling. Per-file 4 MiB limits cannot establish that combined bound. The observed 75,776 bytes are below 1 MiB, but that is an observed size, not proof of enforcement. Do not relabel this as an all-controls-pass capture or rerun merely to replace its history. The harness's reported 0.005-second test duration is diagnostic only, not product performance.

## Trust and scope

Existing same-host interpreter, stdlib and native loader are explicitly trusted. The runner's source/dependency hash admission, finite Python reads and final closure checks apply; no independent vendor provenance, hostile-native containment or full dynamic-loader module ledger was collected. Loaded native/runtime behavior is not newly qualified. Direct synthetic PreparedKeys bypass provider preparation and custody. No database or installed-artifact qualification, SA20 result, performance improvement, candidate result or mutant-kill evidence follows.

The observed baseline is sufficient to satisfy the baseline-result prerequisite for considering separately admitted candidate selection under this limited experiment. Future candidate/mutant captures should record exact invocation in-capture and enforce the chosen output policy; root proposed 512 KiB per output file, implying at most 1 MiB across the two captures. That future control is not retroactively attributed to this baseline.

Reviewer performed only source/capture reads, hashes, comparisons and JSON data reconciliation. No target reexecution, import, syntax checking or mutation.
