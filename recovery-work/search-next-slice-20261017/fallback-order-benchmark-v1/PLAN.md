# Fallback predicate order: finite steady-state timing proposal V1

SOURCE ONLY; no benchmark has run. This is a new same-host no-DB SA21 experiment. Root must separately admit and select it after independent source review, and pause contending work while the16 invocations run. Existing-host interpreter, stdlib and native loader are explicitly trusted. No vendor/native provenance, installed-artifact, SA20, PostgreSQL/service latency, production qualification or security-gate claim follows. All wider gates remain UNKNOWN.

## Correctness prerequisite and exact reuse

CORRECTNESS_BINDING.json pins the saved independently accepted baseline, candidate and four-mutant terminal reviews of runner-v2 seal4747b053405eafe60a656f95adda95ea483bc3d3cfd676570517206d0e85059c. Both variants passed25 methods; stale/tenant/point/null controls produced5/10/3/21 assertion failures with zero errors and complete448-member closure. The baseline's original output-limit recording exception remains in its review; it is not relabeled an all-controls-pass capture.

Only the exact baseline/candidate43-file source views are copied here. Their bytes match their respective accepted correctness views: baseline runner-v2 and successor candidate fallback-order-runner-v1. The candidate has exactly the separately reviewed one-line predicate-order change described below; the baseline is unchanged. DEPENDENCIES.json is identical to the accepted399-leaf shared-read-only SA21 profile. Six monitored controls plus selected43 source files plus399 dependencies give448 before/after identities. Shared hardlinks remain read-only; no environment activation/install or private/cache/pyc bodies are allowed.

The benchmark reuses runner-v2's metadata-first/O_NOFOLLOW/stable-stamp admission, clean startup, narrow Python audit guard and complete safe-member final checks. Only the measurement body, entry fields, workload control and terminal schema differ. The audit hook is not a hostile-native sandbox: stdlib/native-loader behavior and integer-fd pass-through stay within the explicit trusted-host model. There are no runner subprocesses, provider calls, network, DB or file writes. Root captures stdout/stderr externally.

## What is measured and excluded

Actual _ReadText.process_result_value decrypts actual real-CF1 frames using directly constructed synthetic PreparedKeys/_Material with real policy/context/use checks. No key provider is instantiated. Keys use fixed public synthetic roots and fresh bounded process-local leases; real OS encryption randomness creates the fixtures before measurement. Every output must be the exact literal ASCII plaintext of the declared length.

Construction of _ReadText, cached-string/tuple initialization, policy/key setup, encryption, input-list/hex-string creation, full-source admission, imports, GC collection and output validation are excluded from measured intervals. Therefore this experiment cannot establish a tiny-result-set, one-row query or query end-to-end benefit. It measures warmed repeated result processing only. The timed loop includes Python looping and appending returned strings to a list, intentionally identically in both variants; it is not a pure UUID-parser microbenchmark. Construction cost remains unmeasured and cannot be hidden by a passing screen.

Eight cells: CF1 storage/equality representations × canonical/uppercase tenant text ×16/1,024-byte plaintext. Tenant A contains alphabetic hex digits so uppercase is genuinely noncanonical and follows the fallback. All cells use int64 record7, tenant-column codec, no captured point filters, real authenticated payloads and exact pre-admitted synthetic roots. Previously accepted correctness covers additional codecs, rejection and rebinding; this timing matrix does not rerun or replace that larger finite matrix.

Before timing each cell: explicit gc.collect,128 verified warmup calls, then disable cyclic GC only for that cell's measurement, preserving/restoring its prior state. Exactly4,096 timed calls retain outputs; validate every returned value/type after the interval and release the list. No timing sample or failed cell may be omitted. Fixture setup separately verifies one result per cell. Expiry or any output failure is HOLD, not a shortened or retried measurement.

Measurements bracket only the timed loop: perf_counter_ns wall, process_time_ns CPU, getrusage max-RSS before/after (Linux KiB), voluntary/involuntary context-switch deltas and minor/major fault deltas. max-RSS is a process high-water mark, not instantaneous cell RSS or allocated-byte count; paired cell order controls its interpretation but does not make it per-cell current RSS. Counter collection has small bracketing overhead; CPU includes the two wall-clock reads. No counter is used to claim independent hardware or scheduler isolation.

## Fixed balanced schedule and exact counts

WORKLOAD.json fixes four ABBA cycles: baseline,candidate,candidate,baseline repeated4 times. Exactly16 fresh processes form8 adjacent pairs, alternating AB and BA. Each invocation receives its index0..15 and must match the fixed variant at that index. Both processes of a pair use identical cell order. Pair0 starts at cell0; successive pairs rotate the eight-cell list by pair number, reversing odd pairs. This partially balances cell position without random seed or post-hoc ordering. Rotate-then-reverse gives each cell four positions twice, not all eight positions; it is not a complete Latin square. AB/BA pairs still share the same position sets.

Each process produces8 samples,32,768 timed calls,1,024 warmup calls and8 setup validation calls. Whole schedule:128 samples,524,288 timed calls,16,384 warmup calls and128 setup validation calls. Exactly8 ratios per cell compare candidate with its adjacent baseline. All startup/import/hash work is outside timing. Root must keep the original order, pause contending work throughout and retain an explicit quiet-window attestation. The counters remain evidence of observed contention; the attestation alone does not eliminate noise.

## Entry and bounded root envelope

Root supplies the existing pinned Python executable, -I -B -S -X pycache_prefix=THIS_DIRECTORY/bytecode-absent, absolute benchmark.py, VARIANT, INDEX and exact SOURCE.sha256 seal. Cwd is this directory; stdin /dev/null; clean environment exactly LANG=C.UTF-8, LC_ALL=C.UTF-8, TZ=UTC. The prefix is absent before/after. Proposed per invocation limits: wall60s TERM plus2s hard-kill grace, CPU30s, VM1GiB, core0, each of two root capture files512KiB (thus1MiB combined). Record actual argv/environment/cwd and ulimit readbacks in every capture. Root must confirm process termination and run its external afterchecks even if the child fails. A hard stop or missing child closure remains HOLD; no automatic retry.

Each successful process requires rootexit0, independently accepted root aftercheck, exactly one BENCHMARK_JSON, empty stderr, correct index/variant, statusPASS, no primary failure, eight complete verified samples, exact448 closure keys allPASS and absent bytecode prefix. The child has no mutation authority over source/deps. Measurements alone never override failed admission/closure/output validation.

Suggested root capture namespace (required by reducer): /workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/search-fallback-order-benchmark-20261017. Preparation creates no captures. Each process gets a separate indexed subdirectory; root writes the final manifest only after all16 captures exist and are independently joined. No source change or performance outcome is inferred from directory creation.

## Preset reduction and acceptance screen

reduce.py is a separate read-only tool selected by root after sampling; it imports no product. Args: SOURCE_SEAL, exact CAPTURES/CAPTURE_MANIFEST.json path, manifestSHA256. Root admits the reducer/host independently. Manifest schema:

    {"source_seal":"<seal>","quiet_window":true,
     "sequence":["baseline","candidate","candidate","baseline", ... exactly16],
     "captures":[{"index":0,"variant":"baseline","files":{
       "stdout":{"path":"<absolute capture path>","sha256":"<digest>"},
       "stderr":{"path":"<absolute capture path>","sha256":"<digest>"},
       "exit":{"path":"<absolute capture path>","sha256":"<digest>"},
       "after_exit":{"path":"<absolute capture path>","sha256":"<digest>"}}}, ...]}

Every manifest path must stay beneath the fixed capture namespace; source/control/capture bytes are metadata/hash checked before analysis and again afterward. It requires exact sequence, sample counts, output checks and448 identity sets; root separately verifies invocation/resource records and quiet-window truth. It retains all128 samples in calculations; no trimming, exclusion or automatic rerun.

Noise HOLD if any sample is shorter than50ms, wall-minus-CPU exceeds10% of wall, involuntary switches exceed2, or any major fault occurs; also if median absolute deviation divided by median exceeds10% for either variant's eight wall or CPU samples in any cell. These conservative operational screens are not a confidence interval or proof of absent noise.

Canonical benefit screen: in each of four canonical cells, both median paired wall and CPU ratios must be at most0.98 (at least2% observed reduction), and at least7of8 paired ratios must be strictly below1. Fallback regression screen: in each of four uppercase cells both median ratios must be at most1.03, and at least7of8 ratios must be at most1.10. Median paired maximum-RSS difference must not exceed8,192KiB in any cell. Thresholds are fixed before execution; they are not changed to fit results.

Any failed screen yields HOLD with all ratios/counters and reasons retained. No noisy sample is discarded. A clean screen can support only LOCAL_STEADY_STATE_SCREEN_PASS on this exact host/source/dependency/workload. It is exploratory, not a significance claim, release gate, tiny-result-set benefit or production speedup. Independent review must reconcile raw captures, fixed pairing, counter interpretations, exclusions and source pins before reporting a bounded numerical finding. No benchmark claim has yet been made.


## Preserved predecessor and V2 guard clarification

Benchmark V1 seal7909a745524ce3e96fd43013b8a1d016b4b105136ea5b61aeac16c1691639f5c remains unchanged and unexecuted; benchmark V2 was executed and retains its original HOLD, as detailed below. V2 moves the open-event mode/flags write check before the integer-file-descriptor read allowance. An integer fd is never a write-mode exception. This does not change any completed correctness result or authorize a correctness rerun. The exact source views, dependency map, workloads, pair order, counts and preset thresholds remain unchanged.

Finite source/dependency hashes establish admitted on-disk bytes and preservation, not proof that a native loader selected only those files or vendor-authenticated them. Existing-host stdlib/native-loader trust is an explicit selected assumption. No complete native-origin ledger or hostile-native containment is claimed. Read-only integer fdopen allowance likewise is not a generalized file-descriptor sandbox.

Root applies a240-second whole-schedule deadline in addition to per-process limits. On reaching it, terminate owned work and retain incomplete-experiment HOLD; never reduce counts, discard samples or retry automatically. Reducer afterchecks occur on its normal successful-analysis path; malformed-input exceptions require root's unconditional external afterchecks and missing-output HOLD. No successful reducer aftercheck is inferred from a failure path.


## Successor question, exact changed boundary and preserved HOLD

This is one controlled comparison of the changed predicate against the same unchanged recovered baseline. It is not an unchanged-candidate rerun. The new question is whether skipping the identity expression on exact-string text mismatch reduces observed fallback overhead while preserving canonical processing behavior. It does not directly measure successor-versus-predecessor in one contemporaneous pair; comparing separate experiment medians cannot isolate the code change from time/host variation.

The predecessor benchmark-v2 SOURCE is402f4c7aec63b1aec00840eea25255ec21ca56fdc95a153d814f50ff3e8289c8. All128 original samples, original thresholds and24-flag HOLD remain preserved:16 involuntary-switch flags,3 canonical pair-consistency flags and5 fallback flags. Favorable canonical medians are not accepted speedup. This packet neither changes those gates nor discards/reclassifies samples. No claim follows before the new raw results and independent review.

Candidate sqlalchemy.py is now5ec115163c8c53ba01c34613a9140b4506cd3a38a8280224ea9c21f032743f6a,66312 bytes. Only the text-equality and current-identity conjuncts are swapped, after the unchanged cache-presence/exact-str guards. Source proposal ../fallback-order-v1 seald474745db1af4748204d5640df04b64eaece396c7a412fa95a9694a763e4f753 declares stable/sequential processor semantics. Candidate-only actual correctness was independently accepted:25 methods, zero failures/errors,448 closure PASS, packet763819ac3068ce8fce5a58af757c9c2a0a82c969579da03ceb381c069bee0c1b. CORRECTNESS_BINDING.json binds that saved terminal review. Baseline and four mutant results remain historical evidence, not new successor executions or mutation qualification.

Executable benchmark/reducer differences from benchmark-v2 are only fixed ROOT/capture namespace substitutions; candidate source changes only the reviewed line. VIEWS updates roots and candidate hash; correctness binding and this plan identify the new boundary. WORKLOAD.json and DEPENDENCIES.json remain byte-identical. The same16-process ABBA sequence,128 samples, workload sizes, warmups, iterations, partial position balance, output checks, counters, gate thresholds and resource/deadline limits apply without retuning. Existing flags-first audit check is retained. Root alone may select one quiet-window execution after independent source review and fresh admission; timeout/noise/failure remains HOLD without automatic retry. Construction and end-to-end performance remain unmeasured.
