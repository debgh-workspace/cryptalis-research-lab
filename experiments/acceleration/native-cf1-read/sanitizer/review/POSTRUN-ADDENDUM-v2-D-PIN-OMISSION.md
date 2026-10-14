# v2 post-run addendum: D ABI helper omission

2026-10-14. Read-only source and JSON/hash audit; no imports, reruns, builds or changes to accepted files. This additive report preserves STATIC-SCOPE-REVIEW-v2.md and corrects its missed dependency.

## Disposition and correction to static review

The first D-normal negative launch is NOT accepted. Its controller status is FAIL and child status FAIL_INTEGRITY. The initial static review missed an explicit adapter dependency absent from the execution freeze. Its bounded clearance was therefore incomplete for D. The origin guard correctly detected and rejected the omission; no guard relaxation or retrospective PASS is justified.

Six build receipts are PASS, with current binary hashes and required ELF dependency sets matching their receipts. The first sixteen T/S launches have the expected outcomes: eight positive PASS and eight EXPECTED_FAIL. Remaining seven v2 D launches have no supervisor receipts and remain NOT RUN. The failed seventeenth launch is retained as failure.

## Exact cause

adapters_d/adapter.py calls load('san_d_abi', B/'candidate-native-abi-fork-20261014/runtime.py'). This original source file is intentionally loaded via spec_from_file_location; there is no incorrectly copied helper __file__ or forged loader origin. Its absolute path is absent from EXECUTION_FREEZE_v2.json pins. Its cases.json IS pinned.

The current original runtime.py SHA-256 is:
7adbbb5de344b956feceb62adb16811ddc7a94081099c892933589e03fa25977

This matches the historical ABI PINS.json and context-control FREEZE-v5.json, FREEZE-v6.json and FREEZE-v7.json. The historical ABI RESULTS.md describes accepted finite ABI/fork evidence with unchanged runtime; the later context freezes independently retain the same hash. There is no evidence that this source changed to cause the failure.

v2-D-normal-negative-o0-01-child.json contains 101 observations and the intended exact RuntimeError at frozen/uuid-storage-unicode. Its final origin check adds:
origins: RuntimeError('Unpinned loaded module: san_d_abi /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-native-abi-fork-20261014/runtime.py')

The controller reports Child guard failed. The correct negative text and mutation do not override failed integrity.

## Completed receipt audit

For all seventeen existing supervisor/child pairs, independently checked freeze anchors, child receipt SHA-256 bindings, clean captured streams, null supervision reason, confirmed leader reaping, empty cleanup errors, controller integrity and empty before/final private caches. The D child alone has the specified integrity failure. All existing positive ordered IDs match their frozen inventory. All negative prefixes, RuntimeError text/type, exit 1, original_verified markers, mutation paths and independently reconstructed literal-00 mutations match their intended negative contracts.

T/S positive counts are T-normal 234, T-diagnostic 168, S-normal 275 and S-observed 417 under each optimization mode. Full observation records are exactly identical between O0 and O1 for each T/S build. All 17,202 frozen input hashes and all shared cache inventories still match at this audit. These are bounded receipt/source checks; the experiment still does not qualify leaks or instrumentation of uninstrumented CPython/provider internals.

## Related explicit paths checked

All other adapter-selected original source paths are present in v2 pins:
- T tuple_read.py, full_runtime.py, fault-fork-v2/runtime.py and original fixture_support.py; local direct.py is also frozen.
- S staged_read.py, direct_runtime_v2.py, wrapper_runtime_v2.py and corpus_runtime_v2.py, original fixture_support.py, admission-correction support.py and isolated S20 cf1.py.
- D read-admission/runtime.py, context-control/native_read.py, original fixture_support.py, original validate.py, admission-correction support.py, S20 cf1.py and keys.py.
- ABI cases.json and the data dependencies used by original validate.py are already in the broad frozen input set.

D normal's second explicit helper, san_d_full, is pinned at read-admission/runtime.py. The D diagnostic adapter does not use san_d_abi; it uses its selected frozen manifest, original fixture helper and context wrapper. No second missing explicit adapter-load path was found. This is not a proof about all possible dynamic imports outside the selected finite branches.

## Minimal additive D-only v3 recommendation

1. Preserve all v2 source, freeze, commands, binaries, build receipts, sixteen accepted T/S test pairs, failed D pair and stop evidence byte-for-byte. Do not rerun T/S or rebuild unchanged binaries merely to obtain a new anchor.
2. Create a distinct v3 guard/entry/controller and freeze/command namespace, restricted to the two D build IDs and eight D test launches (negative/positive for normal/diagnostic under O0/O1), with entirely new exclusive receipt/cache names. The failed D-normal negative is a newly authorized replacement launch, not continuation of or overwrite of the failed receipt.
3. Add the exact original ABI runtime path/hash above to the v3 input pins and resolved pin map; review a declared D helper dependency inventory before importing helpers. Do not remove san_d_abi from sys.modules to evade the guard, alter __file__, broaden path allowlists or accept unknown origins.
4. Reuse the six accepted build artifacts as historical provenance without new builds. Only the two D binaries need be admitted by the D-only launcher. Explicitly bind each adopted build receipt and binary hash to the approved v2 freeze anchor, exact compiler command/environment, source/include/tool/runtime pins, ELF receipt and accepted build guards. Keep the v3 execution anchor separate from the v2 build-origin anchor. A blanket relaxation of build anchor equality is insufficient; cross-version adoption must name exact receipts and expected hashes.
5. Apart from this missing helper dependency, versioned entry plumbing and explicit build-adoption lineage, keep candidate C sources, existing wrapper/helpers, oracles, IDs/counts, negative paths, sanitizer environment, origin/cache guards, limits and stop rules unchanged. Verify all old pins and six binary/receipt hashes again before freezing the adopted lineage.
6. Obtain independent source review and separate execution authorization for the v3 freeze. Stop on the first unexpected failure with no automatic retry. No v3 execution is authorized by this recommendation.

LSan remains blocked after the preserved clean-control detector fatal exit 23. detect_leaks=0 is not leak qualification; leak freedom remains UNKNOWN.
