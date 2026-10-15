# Independent optional SQLModel38 overlay source and command review

Actual audit date: **2026-10-15 UTC**. The directory suffix `20261014` identifies the experiment generation, as authorized by the coordinator; it is not the audit date.

## Decision and current hold

**ACCEPT_OPTIONAL_SOURCE_COMMAND_WITH_COORDINATOR_GUARD**, restricted to the exact frozen packet and the independently reviewed data-only guard described below. The frozen entry by itself does not establish a complete external-oracle filename boundary; the before guard is mandatory. A terminal-only extra-file check is insufficient.

**Optional runtime remains HELD until both full main SA21 and SA20 terminal audits are independently accepted**, the two focused GREEN audits remain accepted, and genuine coordinator clearance binds those accepted artifacts plus this review. At completion of this review, the coordinator had reported main SA21 terminal execution and corpus restoration, with its full terminal audit still pending; SA20 had not yet been admitted. This source review creates no runtime authorization and writes no CLEARANCE_OPTIONAL38.sha256.

No candidate, original test, fixture, dependency, wrapper, preflight, frozen packet, or product setting was changed by this review. Only this reviewer directory was written.

## Exact identity and independent input verification

- Packet: `experiments/async-cleanup-sqlmodel-overlay-plan-20261014`.
- External PACKET.sha256 anchor: `f3fddd013c20ebe244df3358170a5573c1563abc97dfe05b594750a7696ea096`.
- Exactly 29 sealed members plus PACKET.sha256. No unsealed packet file was present during the completed static audit.
- INPUTS.sha256: `fce3d5e57c62a4d78eb5dee4c73042d0f89aba4422ee3434ed3ccd565b45e490`; exactly 589 unique inputs.
- run-optional38.sh: `bacd19d9ac14f418c5b460937d100320688d9f1ce5bf5e900a50fa7708b0b967`.
- verify_frozen.py: `aab258b380bb5cf3920944719c230d228b03499e66c9d0d87f12fa14b7fed72a`, byte-identical to the main verifier.
- Candidate217 manifest: `4ba41f40c8dc32c80b2f863e5bc60fa7ce8434070c45b8b8f9cfc2a3cb145649`.
- S25 baseline216 manifest: `3fc6eb1e3a70a4401aec1338798463b6d7170992539723b4ed294f247f5fd703`.
- Three-file overlay manifest: `ed7b95572c47f41f454007eaaa84a6207ef4ec064873869cb99a952352c061d9`.
- Independent audit-summary.json: `0c9042349d27b6af8d7ebc6421fdbcdf9473588a63b3d1c262429088f9ba284e`.
- Independent audit_overlay.py: `22dbc3d59208d8bc6cbd8806a73e8c7258a12af623d9731a7ddaa1fc73fd172c`.

All 589 target names and resolved symlink destinations were validated before opening selected payloads for hashing. The bounded classes contain 433 source files, five unchanged harness files, four existing interpreter links, seven focused-ancestry files, 26 original corpus files, 14 main native source files, 28 main metadata files, 13 optional native source files, three optional metadata files, 44 safe S25 evidence files and 12 accepted reference review artifacts. All hashes match after confirmed main SA21 restoration. SAFE_INPUTS equals INPUTS; PACKET_FILES equals PACKET membership.

The optional input closure contains all 566 main input entries with identical digests, plus exactly 23 inputs: one existing optional interpreter, the unchanged 16 optional dependency-source/metadata pins, four safe S25 optional evidence files and two S25 optional review artifacts. The optional16 pin file is byte-identical to the original S25 pin file, digest `9aeff3344a9d236bfaca7aa42f02e90e589e13cf665f5e7ad63171b1acb82c1b`. These are selective source/metadata pins, not full dependency-environment or continuous-import attestation.

The optional interpreter link resolves to the existing laboratory CPython3.14 binary; the other three resolve to the recorded Python3.12 binary. They were hashed, not executed by this reviewer. No version command or dependency import was used to infer the optional environment.

## Exact source and oracle comparison

The complete correction inventory is 217 files and the S25 baseline is 216. The only changed existing file is `src/cryptalis/sqlalchemy.py`; the only added file is `tests/test_sqlalchemy_async_exit_double_failure.py`. Both manifests equal the accepted focused/main manifests. The independently regenerated product/test delta equals both frozen source deltas exactly. Every original optional test/helper, fixture, preflight, configuration, lock and dependency declaration is unchanged. The current source-tree extra filenames are cache-only (146 correction, 170 baseline); their bytes were neither opened nor hashed.

The external oracle contains exactly these three source files:

- `oracle/test_async_sqlmodel_public_hook.py`: `25529e24e5190895f76a19a94520cc15ad03d82ef3f7cc423a3c57226655d49e`.
- `oracle/cleanup_sqlmodel_oracle_support.py`: `f4acfe05fbd16ae254b120de6fa0198d36419375630c7caff932ec30ead33b18`.
- `oracle/conftest.py`: `fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd`.

The entire test module is reproduced by only the stated docstring change and unique support-import rename. All top-level test/helper/fixture/class AST bodies match, including decorators, fault injections, assertions and cleanup. Every byte from `def assert_sanitized_provider_failure` onward is identical. Both patch files were regenerated independently and match exactly.

The entire support module is reproduced by only the declared root/packet/cwd rebinding, insertion of correction/tests for the inherited fixture import, 216-to-217 inventory/receipt changes, and the exact three-file hash check inside the original origin_check function. Every byte from `def enable` onward is identical. No other helper function differs. The support import name is absent from correction/tests, so the new path insertion cannot select the old S25-bound support module. The existing candidate helper remains S25-bound and is not the proposed selection.

Conftest is byte-identical to the original candidate conftest. The preflight-module requirement and connection-failure redaction are intact. No import mode, plugin, test marker, assertion, skip policy, runtime flag default or product admission policy was added or weakened.

## Public routing and origin claims

The unchanged lab wrapper sets source PYTHONPATH to correction/src plus the toolchain, runs from the correction root and separately verifies the Cryptalis package origin. The overlay adds only correction/tests for the existing fixture module. It does not add another product source root or an installed-candidate flag.

The inherited setup/teardown origin check requires the exact correction root/cwd; exact Cryptalis, adapter, SQLModel-support and fixture module paths; all217 candidate hashes; all three overlay hashes; the existing SQLModel interpreter prefix; Python3.14.8; SQLModel0.0.47; SQLAlchemy2.0.51; psycopg3.3.6; and unchanged16 dependency pins. It retains the exact native AsyncSession identity and native `_ensure_sync_result` binding check. Both module-fixture calls remain present. Their inherited receipt status says setup for both; two matching records must be reconciled with successful setup and teardown rather than treated as one call.

Product SQLModel support remains default-off. Guarded async routing still composes the public sync_session_class and public native exec through the existing result boundary; the helper's activation and public-table allowance remain test-only and unchanged. Synthetic post-native-result injection remains inside the existing test oracle. The result-boundary test first completes genuine UPDATE RETURNING and the original native result helper, then injects the test fault. It intentionally requires native-committable versus protected-quarantined outcomes, separately for root and SAVEPOINT. It does not claim natural-driver-fault equivalence.

These are source-overlay checks in an existing installed dependency environment. They do not qualify an installed correction or every loaded dependency/module.

## Same38 semantic identities

Literal AST expansion yields exactly38 unique cases from14 test functions. The ordered suffixes match PLANNED_NODE_SUFFIXES and the38 S25 semantic IDs exactly. They also match the original S25 optional JUnit case names and progress starts. The original control has exactly38 passing setups,38 passing calls and38 passing teardowns, with no duplicate/missing/extra ordinary IDs, failure, error or skip; its runner receipt is0. Its two source/dependency-origin records are identical and identify S25, not this correction.

The new external-path JUnit/progress prefixes have not been collected and must not be guessed. Terminal audit must require one exact external test module and a bijection to these38 suffixes, with no extra helper-imported tests, deselections, xfails or hidden narrowing. It must require114 passing ordinary phase reports, wrapper/runner exit0,12 shape-arm receipts,9 authority/provider/cancellation completion receipts,4 genuine post-native-result UPDATE reaches and4 recovery receipts. Compare paired native/protected observations to the accepted S25 control. The original source38 pass is historical evidence, not a pass for this overlay.

## Frozen command, containment and mandatory external inventory guard

The shell's only runtime invocation is the unchanged corpus-v2 wrapper, with the exact existing SQLModel interpreter, correction root and pyproject.toml, and the single external oracle directory selection. Shell syntax passes. There is no direct pytest invocation, installation, dependency change, network step, hidden filter, selected old candidate optional module, retry or second-cell launch. The selected directory has only one default-discoverable test file.

The shell requires additive clearance and absent evidence/audit destinations, records before-pin status, invokes the wrapper once, captures its actual status immediately, records after-pin status separately, and retains a nonzero wrapper status. At review, the optional evidence path, packet/run, packet/run/optional38 and optional clearance were absent. Recheck them before entry; never reuse or delete them for a retry.

**Inventory finding:** the frozen verifier checks sealed packet members but does not reject an unlisted fourth file in oracle. The helper checks the exact three manifest keys and their hashes but does not enumerate the actual directory. Because the command selects the directory, a new test file could be collected before a terminal audit discovers it. The frozen packet was not edited to address this. Acceptance therefore requires the separately reviewed coordinator guard immediately before and after the runtime entry, with no concurrent oracle writers.

Guard: `reviewer-notes/async-cleanup-optional-plan-independent-20261014/oracle_inventory_guard.py`.

Guard SHA256: **`6b134f1afbdf73ce73c22c5e0bc79e77246b2b247a37c9e5b95f305115f96626`**.

`GUARD_COMMANDS.txt` gives the exact standalone commands. Verify ORACLE_GUARD.sha256 against this review's external guard digest, then run the script using the pinned repository interpreter with `-I -B --phase before`. The before phase requires exactly the three regular source files and no cache or other entry. Both phases pin the supplied packet anchor, exact overlay manifest and source hashes, reject symlinks and reject missing/unlisted source files. After return, run the same script with `--phase after`; only ordinary `__pycache__` .pyc filenames for the three known CPython3.14 modules are allowed additionally. Cache content is never read. No cache cleanup or oracle modification is authorized.

Capture exact guard bytes, commands, outputs, statuses and digest in coordinator evidence. All before statuses must be0 before entry; all after statuses must be0 before acceptance, regardless of wrapper status. A failed guard means STOP and inspection, not repair or retry. This is a controlled single-writer execution boundary, not a filesystem-lock guarantee against arbitrary external writers. The guard-before review run passed with no cache entries. The frozen shell and verifier remain byte-identical.

The wrapper's exclusive nonblocking lab-session lock, fresh readiness and test preflights for both roles, 600-second test and90-second other-phase bounds,180-second faulthandler setting, source archives, finally shutdown and nested-finally26-file corpus restoration remain unchanged. These bounds do not establish termination of every descendant or uncooperative cancellation path. Existing test cleanup assertions retain their original meaning.

Terminal audit must separately require postgres-stop exit0 in safe wrapper output and explicit server-stopped text. The unchanged wrapper does not replace its prior status merely because stop returned nonzero. It must also require successful complete before/after pin logs, identical clearance identity, all original26 corpus archives and restored bytes, exact primary filename set, every generated-artifact archive hash, errors=[], deleted_during_run=[], and primary_receipts_restored=true. An exit0 test result cannot replace those checks.

The verifier archives all29 sealed members plus PACKET.sha256 and clearance, and all217 candidate files. The wrapper must archive exactly the three external source files and stable156 source/config entries; the runner's155 source/test hashes remain a separate inventory. Require the corresponding before/after external maps and archive bytes to equal the exact three-file manifest. Coordinator guard artifacts must also be retained because they live outside the frozen packet.

The clearance parser establishes safe target identity and digest, not verdict semantics or the right prerequisite combination. The coordinator must check real accepted focused reviews, the main source review, both complete main terminal reviews and this conditional optional review, then record and preserve the additive clearance digest. This review does not waive any prerequisite or provide user authorization.

## Review method, retained incidents and limits

Only standard-library source/text/AST/XML/JSON parsing, safe filename/target validation, SHA256 checks and bash -n were performed. No reviewed project/native/wrapper import, compilation, collection, test, database/server action, Git operation, package installation, environment read, credential read, network action or runtime entry occurred. Raw tests.json, readiness.json, package-origin.json, postgres-start.json and postgres-stop.json were not opened, hashed or copied. The interpreter binaries were hash inputs only, apart from the reviewer's normal standard-library execution environment.

REVIEW_METHOD.md records the authorized directory decision, an initial reviewer anchor-parsing error stopped at the first assertion, the authorized constant-only correction, and the later live-corpus mismatch while main SA21 owned the corpus. Both failed observations are retained. After the coordinator confirmed terminal restoration, the authorized unchanged full checker passed every589 input hash and all26 corpus names/hashes. No expected source/test/corpus value was changed to obtain a pass.

Artifacts include audit_overlay.py, audit-summary.json, audit-checks.txt, pin-name-validation.txt, read-paths.txt, audit_static.py, static-summary.json, static-checks.txt, oracle_inventory_guard.py, ORACLE_GUARD.sha256, GUARD_COMMANDS.txt, guard-before-review.json, shell-syntax.txt, REVIEW_METHOD.md and retained earlier attempts.

This accepts only the bounded source/command proposal with its mandatory external guard. It is not optional runtime success, full optional-environment/cross-module coverage, installed-correction qualification, packaging/provenance qualification, independent-host/provider evidence, candidate promotion, release approval or production readiness. S25 remains the highest accepted candidate until the coordinator accepts stronger bounded evidence. Seven historical main failures remain open and all seven production gates remain UNKNOWN.
