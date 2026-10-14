# Independent read-only native-direction audit

## Verdict

Frozen numerical evidence is internally consistent and passes its stated experiment-selection arithmetic. No obvious source-level bounds, ownership, cleanup, or premature-plaintext-release defect was found in this small wrapper under the intended trusted OpenSSL provider contract and conventional CPython/Linux integer widths. This is not full memory-safety qualification, independent execution of correctness tests, product admission, or evidence that the measured improvement is caused solely by avoiding a second context.

The frozen correctness and warmup claims remain conditional on assertions having been enabled during the original runs. Neither receipt records the interpreter optimization flag. Preserve the original evidence and its limitations; do not replace it or imply that later validation retroactively proves the original run configuration.

## Method and scope

Read candidate source, protocol, harness, frozen JSON, correctness/build receipts, manifest and fixture bytes. Executed only the attached independent standard-library data-recomputation script. Never imported the native module, ran candidate tests or timing, started PostgreSQL, edited candidate inputs, or performed product integration. Wrote only into this audit directory. The script and `recomputed-evidence.json` provide reproducible arithmetic and observed hashes. A git status attempt established that the current workspace directory is not itself a Git repository; no Git provenance claim is made.

## Independent numerical results

| Plaintext bytes | Original median ns/item | Native median ns/item | Ratio | Reduction | Favorable blocks |
|---|---:|---:|---:|---:|---:|
| 7 | 3143.005 | 1736.967 | 0.552645319 | 44.735% | 7/7 |
| 32 | 3294.138 | 1825.596 | 0.554195362 | 44.580% | 7/7 |
| 128 | 3478.078 | 2210.293 | 0.635492649 | 36.451% | 7/7 |
| 4096 control | 16837.747 | 15380.041 | 0.913426303 | 8.657% | 5/7 |

All 21 independent checks passed. These cover exact seven-block/four-size/two-variant order, expected alternation by block, 56 samples, 56,000 measured operations, 5,600 declared warmups, all 168 elapsed-clock subtractions, sequential nonoverlapping clock intervals, nondecreasing resource counters, all reported medians/ratios/favorable counts/acceptance decisions, listed manifest entries, timing source/binary/protocol/harness hashes, correctness source/binary and fixture hashes, exact 76 correctness labels, and 4,000 distinct deterministic keys and nonces. Timing span from first before to last after is 381,986,702 ns. No samples were excluded by this audit. The control's two unfavorable blocks are preserved and do not violate the stated median-based control rule.

The statistic is a ratio of separate seven-block medians, not a median paired ratio or individual-call latency distribution. Each interval times a 1,000-result list including fresh Python object construction or native calls; fixture encryption, validation, and list destruction occur outside the measured body. Clock bookkeeping gives slightly different endpoints to wall/process/thread counters. One short serial run is not a confidence interval, independent-process replication, concurrency benchmark, tail-latency result or production workload.

## C source review

- Lines 18–27 require exactly four positional objects and exact immutable bytes before accessing bytes internals. Key/nonce lengths are 32/12; sealed must contain a 16-byte tag; ciphertext and AAD are bounded to 16 MiB. Subtracting 16 from nonnegative bytes length cannot underflow Py_ssize_t here. Bounds precede casts to int.
- Lines 29–31 allocate ciphertext length plus EVP_MAX_BLOCK_LENGTH, including a nonzero buffer for empty input. On the intended platform these sizes and all later length sums fit their types.
- Lines 32–45 fetch the named default-provider cipher per call, allocate fresh context, verify key/IV lengths, initialize decryption, install the final 16-byte tag before AAD/data, and perform exactly one non-NULL-output update. Input and output buffers are disjoint.
- Lines 46–50 check update/final results and output lengths, and only create a Python plaintext object after successful authentication. The generic operation-failure path returns NULL with an exception. A failed Python bytes allocation retains its allocation exception through cleanup.
- Lines 55–58 release context/cipher and clear/free the allocated output on every path after allocation. An early output-allocation failure owns no further native resources. Borrowed input references remain owned by the call tuple; no GIL release or persistent key state appears in this module.
- The wrapper's order agrees with the documented SIV interface: set a 16-byte tag before data, use a single data update, and do not release unauthenticated output. The buffer sizing follows the documented EVP bounds. See [OpenSSL 3.5 EVP documentation](https://docs.openssl.org/3.5/man3/EVP_EncryptInit/).

Limits: returned immutable Python bytes and input key objects are not zeroized; the explicit output clear does not prove all provider/allocator/process copies are erased. The global default library context is not a private provider isolation boundary. The module holds the GIL and clears the current thread's entire OpenSSL error queue, potentially discarding earlier unrelated errors. Post-call length checks assume a conforming provider and are not a sandbox against provider memory corruption. No sanitizer, fault-injection, concurrency/cancellation, ABI-distribution, constant-time, or provider implementation audit was performed.

## Evidence and test gaps

1. Both harnesses use assert for essential checks. In optimized Python, equality checks disappear; timing warmups at measure_direction.py:32 disappear entirely while the receipt still records 100 warmups and true output flags. Hash guards and the no-overwrite assertion also disappear. Current interpreter state, if separately checked, is only corroboration and cannot reconstruct original flags.
2. measure_direction.py:11 only checks correctness receipt status/count, not its source/binary/fixture binding or label identity. Independent audit confirms those bindings for the supplied files, but the harness itself does not enforce them.
3. The test's sealed-value mutation flips only the last byte, therefore tests tag corruption rather than a separate ciphertext-body change. Key, nonce and AAD changes are covered. Four published-fixture entries include empty plaintext/AAD coverage. Exact bytes subclasses, arity, valid 16-MiB boundaries, allocation/provider failures and exhaustive malformed-length cases are not covered by these 76 checks.
4. Source and binary hashes identify current bytes and agree across receipts; they do not prove that the binary was built from that source, that the run actually executed every reported check, or that protocol text was frozen before measurement. No signed/externally anchored chronology is present. Source manifest predates timing files; timing receipt binds protocol/harness itself. A separate post-measurement receipt repeats matching source/protocol/harness/binary hashes but does not resolve original-run provenance.
5. Native backend is recorded as OpenSSL 3.5.7, pyca backend as OpenSSL 4.0.3; cryptography package is 50.0.2. These are distinct package/backend identities. Backend version/build/provider behavior and wrapper/language boundaries confound attribution. No same-backend counterfactual or context-construction instrumentation is established here.

## Disposition

Retain this as a promising, narrowly scoped direction-specific primitive experiment with independently checked arithmetic. A separately named explicit-check validation harness and run-configuration receipt could strengthen future component evidence without rewriting the frozen measurement. None of these results qualify CF1 framing/HKDF/HMAC, key lifecycle, SQLAlchemy/PostgreSQL behavior, or C9/C10/product performance budgets.
