# Independent static review: native-controls sanitizer v2

2026-10-14. Source-only audit; no compiler, candidate import, candidate execution, sanitizer launch, installation, security/provider change or Git operation. Inspection used file reads and standard-library JSON/hash checks. Writes are confined to this review directory.

## Disposition

Bounded static clearance for the exact six separately admitted builds and 24 test launches in CONTROLLER_COMMANDS_v2.json, subject to separate coordinator execution authorization, checking this external freeze anchor before execution, and stopping at the first unexpected result. This is not runtime qualification or evidence that a compiler/test will succeed. No actionable source-level blocker was found in the reviewed scope.

EXECUTION_FREEZE_v2.json SHA-256: 1a56f94e6f30cf448070038647c092fbaba10071919eca9f22f59f44b9f4f4f1.

All 17,202 input hashes matched current bytes. Shared cache inventories matched. Six output directories did not yet exist at audit time. There are 30 distinct controller cache prefixes and 24 distinct child prefixes. Existing proposal BUILD_COMMANDS/LAUNCH_COMMANDS are not the executable v2 interface.

## Source/build admission

- T-normal: tuple-control/native_tuple.c; T-diagnostic: same source plus TUPLE_DIAGNOSTIC.
- S-normal: composition-control/native_primitives.c; S-observed: native_primitives_observed_v2.c plus S_DIAGNOSTIC.
- D-normal: context-control/native_cf1.c plus CF1_CONTEXT_CONTROL; D-diagnostic: same plus CF1_DIAGNOSTIC.
- Each has an exclusive v2-native-* output directory. All use -shared -fPIC -O1 -g -Wall -Wextra -Werror -std=c11, -fsanitize=address,undefined, -fno-omit-frame-pointer and -fno-sanitize-recover=all.
- T expected ELF NEEDED: libasan.so.8, libubsan.so.1, libc.so.6. S/D additionally link and require libcrypto.so.3. These are declared sets consistent with source/link commands; actual emitted metadata must pass the bounded readelf gate after compilation.
- Child admission verifies separate successful build receipt, command/environment, controller provenance, ELF command/needed set, binary path/hash, freeze anchor and cache/integrity fields. Native origin is checked before import and after loading. D normal excludes diagnostic exports; D diagnostic requires observed export. S checks the exact export inventory.

## Independent finite oracles and count reconstruction

Historical manifests were read independently and compared to every selected copied row: full_read, T annotations/direct IDs/fault rows, S normal/observed direct and wrapper rows, D diagnostic manifest and D rows all match. ADDITIONAL_EXPECTATIONS T_tuple_oracles matches tuple-oracle.json exactly; D_normal_abi matches the original ABI-kind rows exactly. These comparisons did not invoke preparation scripts.

Positive inventory counts per optimization mode:
- T-normal = 93 direct + 141 full reads = 234.
- T-diagnostic = 96 direct + 72 fault/expiry = 168.
- S-normal = 134 direct + 141 full reads = 275.
- S-observed = 242 direct + 175 wrapper = 417.
- D-normal = 100 ABI + 141 full reads = 241.
- D-diagnostic = 8 vectors + 8 observation ABI + 179 direct + 179 wrapper = 374.

Each build has a negative and positive launch under optimize 0 and 1, giving 24 test children. Positive acceptance requires ordered exact inventory, exit zero, PASS, clean streams, bounded supervision and all final checks.

T direct oracles are frozen byte records or independently encoded literal boundary/refcount contracts, not candidate-derived expected results. Full-read expectations come from the historical independently frozen corpus; T tuple/decode/PID and S primitive-order adapters retain additional observations. D diagnostic wrapper records include both public results and exact nested native observations. T fault/expiry uses fresh prepared keys per observation, so it is paired before/fault/recovery rather than same-instance recovery. S/D grouped paths retain grouped key instances. No actual fork is selected; D calls only abi(), not the imported module's fork supervisor.

## Exact negative signatures

The emit function verifies the unmodified actual against the frozen expected value before mutation, deep-copies it, appends literal 00 only at the frozen string path, stores original_verified and raises the exact RuntimeError. The supervisor independently reconstructs the mutation and rejects alternative exception text/type, exit status, inventory prefix, mutation path or content.

Required negative prefixes/targets (identical under both optimization modes):
- T-normal and T-diagnostic: prefix 1, oracle/uuid-storage-unicode/payload-info, case/value/hex.
- S-normal: prefix 2, normal/sha256/abc, result/hex.
- S-observed: prefix 2, q0/sha256/abc, result/hex.
- D-normal: prefix 101, frozen/uuid-storage-unicode, value.
- D-diagnostic: prefix 1, vector/frozen/uuid-storage-unicode, value_hex.

Expected child exit is 1 and child status FAIL; only the outer controller records EXPECTED_FAIL. The exact message is `Sanitizer subset actual-observation mismatch: ` plus the target. Other failures cannot substitute.

## Runtime origin, cache and finalization controls

Compiler/controller environment is the minimal PATH/LANG/LC_ALL map. Child environment adds only the frozen preload and sanitizer/cache settings. LD_PRELOAD points to the existing pinned /lib/x86_64-linux-gnu/libasan.so.8. ASAN_OPTIONS is detect_leaks=0:halt_on_error=1:abort_on_error=1; UBSAN_OPTIONS is halt_on_error=1:print_stacktrace=1. Mapped resolved shared-library paths/hashes are checked before observations and in finalization, and both sanitizer libraries must be present. No inherited loader override or suppression is admitted.

-E -S -B and an exclusive empty -X pycache_prefix are present before controller/entry imports. SourceFinder refuses sourceless and .pyc origins. All loaded module paths must be in frozen pins (or be the separately admitted binary); private prefixes must remain empty; shared cache inventory and input hashes are rechecked in finally. Adapter imports are source based. T/S restore their temporary aliases/hooks; D restores native wrapper binding and checks its mapper. Receipt finalization is attempted on positive, negative and exception paths. Uncatchable process termination cannot promise a receipt and is not accepted as PASS.

## Supervision and stopping

Compiler timeout 60 seconds; readelf 10 seconds; test 180 seconds. Both captured streams are independently capped at 2 MiB. The supervisor uses nonblocking selector reads and observes leader exit through waitid(WNOWAIT), retaining the PID identity until its final signal opportunity. Timeout, overflow and caught interruption signal the process group before proc.wait. No poll/wait precedes group signaling and no numeric process-group signal follows reaping. Final wait is bounded at 10 seconds. Uncertain reap and cleanup errors fail acceptance. Descendant absence is explicitly not claimed, including escaped descendants or a successful leader whose descendants close inherited pipes.

Receipts use exclusive creation and a 128 MiB encoded JSON cap. Partial/overflowed receipts are not acceptable. Controller selects only one explicit operation and does not automatically continue. Coordinator must stop on the first unexpected failure, preserve evidence, and perform no retries/timeout changes/fallbacks. The initial guard anchors to the freeze it reads; comparison to the externally approved hash is therefore a coordinator precondition, not an embedded immutable constant.

## Limits retained

The existing LSan clean control reached normal main return then suffered a detector fatal error and exit 23. Free/leak controls were not run. Leak freedom remains UNKNOWN. detect_leaks=0 supports only the declared finite address/undefined-behavior experiment and cannot qualify leaks. Installed CPython and provider libraries are not thereby instrumented. Static review does not demonstrate supervisor stress behavior, sanitizer operational success, exhaustive memory/fault coverage, actual-fork coverage, timing equivalence, backend/product adoption or full DESIGN closure.
