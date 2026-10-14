# D-only additive sanitizer v3, source-only

No v3 execution, candidate import, compilation or installation has occurred. Independent source review and separate coordinator authorization are required before any command in CONTROLLER_COMMANDS_v3.json. Stop at the first unexpected result, without retries, fallback, timeout changes or guard relaxation.

EXECUTION_FREEZE_v3.json SHA256: 12fdaed70806d9979a8fe9865b7405d7c55032f045ff6b864222b49aa70e7e99.

## Exact deltas

- guard_v3.py changes only freeze/cache namespace and additionally checks every previously existing package file against preserved_v2_artifacts before and in finalization. Loaded-origin and mapped-library checks remain exact; no unknown-origin allowlist, module deletion or origin rewriting.
- sanitizer_entry_v3.py uses v3 guard and entry spelling, admits only D-normal/D-diagnostic, and verifies exact adopted v2 receipt and binary hashes plus v2 build-origin freeze hash. Original compiler command/environment, ELF mapping, accepted build status, cache/integrity checks and v2 controller provenance stay intact. The v3 execution anchor and v2 build-origin anchor are recorded separately.
- control_v3.py retains the original run supervision/receipt acceptance branch and removes compilation. Only the eight frozen D run IDs are selectable. The bounded supervisor remains unchanged supervisor_v2.py.
- Missing original candidate-native-abi-fork-20261014/runtime.py is added to pins and resolved_pins with SHA256 7adbbb5de344b956feceb62adb16811ddc7a94081099c892933589e03fa25977. Original helper bytes are unchanged.
- D_HELPER_DEPENDENCIES_v3.json enumerates nine adapter/helper source paths. Every declared helper is checked against both pin maps and current bytes before native/helper import. Related explicit imports inspected: D san_d_abi and san_d_full; san_d_full's admission_correction_support and isolated cf1; ABI helper's native_read, fixture_support, validate and canonical crypto imports. The ABI module is used only through abi(); no fork supervisor is selected. The newly missing ABI helper is the only added original-source pin; all other selected helpers were already pinned.
- Eight new run IDs and eight controller/eight child cache directories use v3 namespaces. No existing v2 receipt/cache is reused or overwritten. No T/S run and no new build command exists.

## Preservation and lineage

Before preparation, all 17,202 old input hashes and shared cache inventories matched. Six accepted build receipts and binary hashes were checked. PRESERVED_V2_ARTIFACTS_v3.json records all 76 pre-existing package files, including original source/freeze/commands, six binaries, six build receipts and seventeen supervisor/child pairs. These hashes are embedded in the v3 freeze and rechecked by guard_v3.check(). All 76 still matched after preparation. BUILD_LINEAGE_v3.json records all six historical builds; only the two D entries are adopted for launching. The old v2 failed D pair remains FAIL/FAIL_INTEGRITY, and its seven unlaunched siblings remain NOT RUN.

The v3 freeze retains every original input pin; its 17,210 pins add the ABI helper and seven new executable/data-interface files. New helper inventory and preservation/lineage records are themselves pinned. This explanatory document is not executable input. Three new Python sources were parsed with ast.parse only, without import or execution.

## Unchanged contracts and limits

D-normal: 100 ABI + 141 full reads = 241 positive observations per optimization mode. D-diagnostic: 374 per mode. Negative targets, paths, exact RuntimeError, prefixes 101/1, original verification and literal-00 mutation are unchanged. Original adapter, candidate C, wrappers, expectations and fixtures are untouched.

Sanitizer environment remains LD_PRELOAD pinned libasan, detect_leaks=0:halt_on_error=1:abort_on_error=1 and UBSAN halt_on_error=1:print_stacktrace=1. Child timeout remains 180 seconds, each stream capped at 2 MiB, final reap 10 seconds, receipt JSON capped at 128 MiB. All cache/startup/source-import/finalization restrictions remain. No execution outcome follows from this source preparation. Leak freedom is UNKNOWN; no exhaustive memory, real allocation-failure, actual-fork, timing, database/product-adoption or complete DESIGN qualification follows.
