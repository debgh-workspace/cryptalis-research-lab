# Historical import provenance: bounded addendum

2026-10-14. Read-only evidence/source inspection; no candidate imports, test reruns, builds, database/network/Git/settings actions, or cache edits. Only this new notes directory was written. Paths below are relative to `cryptalis-executable/`. Existing outcomes and evidence are preserved.

## Finding and material consequence

Source hashes plus Python module `__file__` checks do not uniquely bind executed Python bytecode. `-B` and `PYTHONDONTWRITEBYTECODE=1` prevent writing caches, not reading existing valid caches. None of the five historical native slices inspected below pins any `.pyc` in its launch/build pin dictionaries. This is a missing execution-provenance guarantee, not evidence that any cache was stale, incorrect or malicious, or that any recorded functional outcome was false. No present cache inventory/hash can retroactively attest past execution bytes.

Original F normal, correction and full admission therefore retain their recorded finite results, source/binary pin consistency and limitations, but do not establish that every imported Python dependency executed the pinned source rather than an associated cache. Do not describe their Python import provenance as fully frozen or source-only. The gap includes oracle construction where that construction imported Python crypto; it does not make committed expectations cease to exist or prove their values wrong. A new forward freeze/run cannot repair historical chronology.

## Scope-specific evidence

### Original F normal (and shared launcher)

`candidate-native-cf1-read-20261014/build.py:35-41` selects research files, S20 `*.py`, cryptography `*.py`/`*.so`, fixtures, interpreter/compiler/headers; `:47-56` adds binary/dynamic dependencies and checks stability. `build-03-normal/build.json` has 585 pins and zero `.pyc` pins. `evidence/normal-o0-01.json` and `normal-o1-01.json` each preserve 1,182 PASS checks and those same 585 pins, with zero cache pins.

`launch.py:19-37` checks those files and origins, then normally imports cryptography/backend, S20 cf1/keys, native extension and `validate`; `validate.py:10-14` normally imports fixtures/wrapper. No source-only loader or isolated empty cache-prefix policy is enforced. `evidence/final-integrity-01.json` rechecks the recorded pins, not unrecorded execution caches. The same launcher structure applies to its diagnostic/sanitizer/mutant evidence; native ELF pins are a separate provenance layer unaffected by the Python-cache distinction.

Narrow exception: `validate.py:41-46` explicitly reads and compiles modified wrapper source for the disposable skip-final function. That one dynamically compiled function bypasses a wrapper `.pyc`; it does not bypass ordinary imports of its harness/dependencies or make the normal wrapper source-only.

### Correction

`candidate-native-cf1-read-correction-20261014/PINS.json` contains 628 pins and zero `.pyc`. `prepare.py:14-19,30-36` inherits original artifacts/build pins and adds correction files; `:21-25` imports cryptography and launches the baseline freeze. `freeze.py:10-12` imports support and S20 cf1/keys. `launch.py:15-38` checks pins/origins and ordinarily imports cryptography, original wrapper, S20 and the correction checker. `run_new.py:15-18` uses `-B` and the no-write environment flag, with no cache-read exclusion. The original ARTIFACTS inventory (130 entries) and correction ARTIFACTS inventory (25 entries) also contain zero caches.

### Full read admission

`candidate-native-read-admission-20261014/PINS.json` has 650 pins and zero `.pyc`; its ARTIFACTS inventory has 33 entries and zero caches. `prepare.py:7-11,25-27` inherits prior manifests and adds its own files. `run.py:10-27` checks pins, ABI, origins and normally imports the baseline/wrapper/helpers/runtime. `launch_all.py:10-11` uses only the no-write cache controls.

`runtime.py:8-12` uses `spec_from_file_location(...).loader.exec_module(...)` for correction support and isolated baseline cf1. An isolated module namespace is not a source-only execution mechanism: the ordinary source loader can consult associated bytecode caches. Thus the RESULTS statement about executing unchanged S20 source needs this provenance qualification, including sealing/query observations.

Important unaffected distinction: `freeze.py` is stdlib-only and constructs the newly predeclared exact-output data without importing product/native crypto. This avoids the product/cryptography cache-loading path during that freeze, but inherited failure/correction expectations keep their historical provenance. It is not a claim of a fully attested stdlib/startup environment.

### Provider/backend and mark observations

`candidate-native-backend-observation-20261014/PINS.json` has 371 entries; `build/build.json` has 376. Mark equivalents have 373 and 378. All have zero cache pins. However, each `run.py:1-15` is a directly executed script whose imports are stdlib plus the native extension from its own build directory. Neither imports S20, cryptography, the F Python wrapper, nor fixture helper modules; fixture data is read as JSON/binary. The extension and dependencies are hashed and checked before import, with backend/origin checks and binary hashes in results.

Consequently the specific unpinned S20/cryptography/wrapper `.pyc` gap does not transfer to these direct C observation paths. Keep the bounded provider/unmarked-queue findings and the 60-case-per-mode mark findings, along with their existing caveats and provider ERRATUM. They are diagnostic-build observations, not evidence that normal F has a cache-proof Python wrapper or a complete execution attestation. Stdlib/startup import provenance remains outside these manifests; direct-script execution itself does not eliminate that broader limitation.

### S20 wrapper source-stability

`toolchain/lab_session.py:96-103` checks package location and, for installed mode, byte-compares installed `*.py` modules against the candidate. This runs after importing `cryptalis` and does not check cached execution bytes. `:106-108` snapshots candidate `src/**/*.py`, `tests/**/*.py`, `pyproject.toml` and `uv.lock`; `:110-120` separately selects explicit experiment Python files. `:127-145` archives the source and compares before/after hashes.

The four inspected receipts (`evidence/s20-installed-full-sa20-20261014`, `s20-installed-full-sa21-20261014`, `s20-restored-smoke-sa20-20261014`, `s20-remote-restored-smoke-sa20-20261014`, each `source-stability.json`) all record 147 source/config entries, zero `.pyc`, and `unchanged: true`. These accurately support their named source/config stability scope. They do not cover installed dependency/cache inventories or prove the Python bytes executed. Installed full sa20's `package-origin.json` records source-byte matching, not cache validation. The runner `candidate-s20-restored-20261014/scripts/test_postgres.py:96-116` imports pytest and later hashes source/tests/scripts; its receipt likewise is not a cache-read exclusion mechanism. No wider S20 acceptance reversal follows from this narrower scope clarification.

## Smallest forward correction

Preserve every existing manifest/receipt and attach this qualification. For the next authorized Python-dependent admission or timing run, add a separately reviewed launcher/freeze version that either (a) pins and enforces the exact allowed cache inventory in all scoped import roots, including optimization variants, or (b) enforces source loading via a fresh empty per-process cache prefix set before startup/imports, with no-write behavior and controlled startup/path overrides. Record/enforce the selected mechanism; an origin string, namespace change or `-B` alone is insufficient. Retain pre/post integrity outcomes even on intended negative/error exits. Keep stdlib/startup coverage explicit rather than silently claiming whole-interpreter attestation.

Only new authorized execution under that policy can establish the stronger forward provenance claim. There is no need to rerun direct provider/mark diagnostics solely to fix a Python dependency path they do not use. Any new tests, cache additions or cache strategy implementation remain separate authorization/work; none was performed here.
