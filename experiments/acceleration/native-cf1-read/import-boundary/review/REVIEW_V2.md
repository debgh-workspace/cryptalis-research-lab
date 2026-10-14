# Independent static delta review: forward F V2

Decision: bounded static clearance for the exact V2 implementation and freeze identified below, with the provenance erratum in this review. This is permission to attempt the declared finite forward validation, not a claim that it passed. V1 remains rejected and must not be executed.

FREEZE_V2.json SHA-256: 51dfcd754b280c3fe1084d5b54fbb51bd13e17bbb164125483708825cb9d7774.
Reviewed supervisor_v2.py SHA-256: e5e69f622989ba1815ed6e4b2cfd289a577764e8681c2e5aa439f00504849ef6.

## Verified delta

- All 2,217 V2 frozen hashes match current bytes. SOURCE_INVENTORY_V2 has 1,042 entries consistent with the freeze. CACHE_INVENTORY_V2 has 411 entries with matching hashes, lengths and first 16 bytes; its complete content equals the original cache inventory.
- All six current inventory lists exactly match V2, including order. prepare_v2.py uses sorted(paths, key=str), matching both checking implementations. The deterministic V1 ordering blocker is fixed.
- The V1 freeze still hashes to dd7409b3923fa015520c266a96f79204ad7f71a287005e141695e3a6998294c8 and all its 2,208 pinned files still match. V2 also pins the original FREEZE/PREPARATION/PLAN/index files. Original manifest, runner, wrapper, native binary and historical published artifact bytes remain preserved.
- The supervisor independently reviewed here creates a new session, drains nonblocking pipes with a 1 MiB retained-byte limit per stream, imposes a 180-second execution deadline, attempts group TERM/KILL on every outcome, uses bounded leader-reap waits, and records cleanup errors and retained output. It explicitly does not certify absence of all descendants. Deadline plus cleanup grace is the containment bound, not a performance claim.
- Parent final integrity runs in finally for ordinary success, expected negatives, unexpected failures, missing/malformed receipts, supervisor errors, timeouts and output caps. Both complete inventories and all pins are checked with retained errors. A child or validation failure exits the finite plan immediately; the outer finally therefore serves as the final check for that failed child. Successful children also receive an immediate parent integrity check. Child preflight runs before each harness invocation; its finally records separate primary, origin and all-pin/inventory findings.
- Preflight now performs public PathFinder inspection of selected expected package-chain/helper/source/native roots, verifies source/native hashes and loader classes, and verifies any corresponding existing cache hash. It performs no dotted parent import. Explicit alias inputs are inspected at their original source paths. The original run.py still executes through runpy and uses its unchanged ordinary imports/explicit loaders.
- Post-import file-backed origins must exist; bound candidate/dependency files cannot reference an existing unbound cache. Required observed paths are checked. This remains selected-root preflight plus postflight observation, not pre-execution enforcement of every actual import-resolution decision, every dependency, a malicious/custom loader, or the complete native live dependency graph.
- Negative receipts now bind both result and negative modes to the commanded mode. The stderr policy accepts one standard traceback with indented interior lines and the exact terminal mismatch error; unrelated leading/trailing diagnostics and chained tracebacks fail. Exact original observations and mutations remain checked. Positive oracle, ordered coverage, nonce/decode observations and optimization correspondence checks remain intact.

## Provenance erratum: no transferred supervisor approval

PLAN_V2 and FREEZE_V2 describe the supervisor as a verbatim copy of candidate-native-composition-control-20261014/supervisor_v2.py. That is not true of the currently available files. The composition file currently hashes to d7960256071bfe5a8a75f3453df0c3ebf51017a446ec1fd09d235088e9481c7c. The import-boundary copy adds cleanup-error retention, more exception-safe cleanup, and descendants_verified_absent=False. This review does not rely on the claimed copy relationship or transfer any prior approval. Clearance is based on reading the exact pinned import-boundary supervisor implementation itself. Retain this erratum alongside execution evidence; do not modify frozen V2 bytes to repair the description. A later edit would require a newly declared freeze and delta review.

The original top section of PLAN_V2 also retains the V1 launch.py/subprocess.run description; its appended V2 section supersedes that operational instruction. Only launch_v2.py with FREEZE_V2.json is cleared here.

## Clearance boundary

Only the declared ten-child forward matrix, using the pinned interpreter with -I -B and a never-used direct output directory, is covered. Stop on any integrity, supervisor or outcome failure; retain all available receipts. No automatic retry, freeze refresh, fixture regeneration, binary/wrapper changes, cache deletion/rewriting, dependency installation, PostgreSQL, network, Git, compile, benchmark, or expanded qualification is cleared by this review.

No historical source-to-cache correspondence or executed-byte attestation is created. Before/after hashes bind declared on-disk source/cache pairs; they cannot establish cache consumption, semantic source/bytecode equivalence, transient modify-and-restore absence, startup integrity, full stdlib/OS-library provenance, or production readiness.

This delta review itself used only source/data reads, byte comparisons, hashes and inventories. No candidate imports, candidate execution, builds or cache changes occurred. Only the designated review directory was written.
