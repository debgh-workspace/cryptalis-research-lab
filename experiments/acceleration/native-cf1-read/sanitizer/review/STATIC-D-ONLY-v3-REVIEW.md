# Independent source-only review: additive D-only sanitizer v3

2026-10-14. No builds, candidate imports or test execution. File/JSON/hash reads and AST parsing only; only this review note written.

## Disposition

Bounded source clearance for the exact eight D-only v3 runs, subject to separate coordinator execution authorization and first-unexpected-failure stopping. No actionable blocker identified. This does not assert runtime success or convert the failed v2 D launch to an accepted result.

Verified SHA-256 anchors:
- EXECUTION_FREEZE_v3.json: 12fdaed70806d9979a8fe9865b7405d7c55032f045ff6b864222b49aa70e7e99
- CONTROLLER_COMMANDS_v3.json: 2727a6594430ef1b399c422466c4fd40c29314fc2b35e7fbe8a6699526c3f2c0
- Build-origin v2 freeze remains 1a56f94e6f30cf448070038647c092fbaba10071919eca9f22f59f44b9f4f4f1.

## Verified correction and preservation

All 17,202 old pins are retained with identical hashes. All 17,210 v3 pinned file bytes currently match. Cache inventory definitions are unchanged and current inventories match. All 76 pre-existing package artifacts in preserved_v2_artifacts match, including original sources/freeze/commands, six builds/receipts, sixteen accepted T/S test pairs and failed D test pair. guard_v3 verifies this preservation set before work and in finally.

The only additional original-source pin is original ABI runtime.py, hash 7adbbb5de344b956feceb62adb16811ddc7a94081099c892933589e03fa25977. Nine-path D helper inventory covers the adapter, ABI and full-read runtimes, context native_read, original fixture_support and validate, correction support, S20 cf1 and keys. Each current path/hash matches both pins and resolved_pins; entry verifies all nine before native/helper import. No __file__ rewriting, alias deletion to hide origins or broad unknown-origin exception was introduced.

Original D adapter and observation schemas are unchanged. This directly corrects the identified missing manifest pin rather than changing observed behavior or expected results.

## Explicit historical build adoption

v3 definitions are exactly the two D entries from v2. Entry permits only D-normal/D-diagnostic. It requires the adopted receipt's fixed path and SHA-256, the named original v2 freeze hash, matching build-origin anchor, accepted status and cache/integrity fields, exact original compiler command/environment, ELF command/needed set and original v2 controller provenance. It separately checks the adopted binary path/hash and receipt binary hash. The execution anchor remains v3 while build_origin_anchor remains v2; there is no general anchor relaxation.

Adopted D-normal receipt SHA-256: cd9fbda6e3ca651f5f72e7fcf495ce21395cc2dc1dc78dbb469a530ccfbd17ed.
D-normal binary: 9e29741d360ac749cd49d833a5182d199e9ed322d4af8304ee1c3270705de426.
Adopted D-diagnostic receipt SHA-256: 6b9b667103743f36597c00abd8e2fdd45bb3d3da7e485743db95d94308eebdd6.
D-diagnostic binary: 0a9aa5bae2ec92fd87eae0beb06580efa22320981d13bd8f9e990d35c0d53f5a.

No compiler operation is supported by control_v3. Six historical builds are preserved; only D's two are selected. T/S execution is absent.

## Run contracts and guards

Exactly eight commands/runs: D normal and diagnostic, O0/O1, negative/positive. Controller and child argv were reconstructed from the declared interface and match. All sixteen private prefixes and eight child receipt names are fresh at review time. Exclusive creation remains required; no v2 cache/receipt reuse.

Every corresponding v2 D run has identical build selection, mode, optimization, environment, target and mutation path. Positive counts remain 241/374. Negative prefixes remain 101/1 with original verification, exact RuntimeError, exit 1, literal-00 perturbation and independent controller reconstruction. Failed child integrity cannot become EXPECTED_FAIL.

Diff inspection confirms entry's remaining observation/finalization logic is unchanged. Guard changes are limited to v3 namespace and stronger preservation checking. Controller retains original run acceptance/finalization while removing builds. supervisor_v2 is reused unchanged: 180-second child timeout, 2 MiB per stream, pre-reap group signals only and bounded final reap. Module origins, mapped library hashes, sanitizer presence, private cache emptiness and all source/preservation hashes remain checked in finally. Serialization limits and exclusive writes are retained.

The coordinator must externally verify approved anchors and stop on any unexpected failure. Fresh versioning is not permission for an automatic retry. This review supplies no execution authorization itself.

Leak freedom remains UNKNOWN following the historical LSan clean-control fatal exit 23. detect_leaks=0 cannot qualify leaks. No timing, exhaustive allocation/fault coverage, actual-fork, database/product-adoption or full DESIGN closure is implied.
