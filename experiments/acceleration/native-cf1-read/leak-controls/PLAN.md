# Frozen leak-detector controls: source-only preparation

2026-10-14. Status: NOT COMPILED / NOT EXECUTED. Independent source review and root authorization are prerequisites. This control does not import or execute any CF1 candidate. Existing evidence is unchanged.

## Question and bounds

Can the installed GCC ASan/LSan runtime detect a real unreachable heap allocation in this exact sandbox, with no install, security or provider changes? Three processes use the same small executable: clean, free, leak. The latter two malloc and touch exactly 131071 bytes; free releases it, leak returns without freeing it. The pointer does not escape the helper, so the intended leak is not deliberately retained as a reachable global root. Ordinary return from main allows exit-time scanning; no fork, _exit, os._exit, quick_exit or signal shortcut is used.

Each mode executes once, in order clean/free/leak. A failed clean/free control stops dependent runs. Compilation and each process have a 30-second timeout, and combined preparation/execution has a 150-second cap. Capture stdout/stderr to exclusive-create files with a 1 MiB per-stream cap; exceeding a cap fails the run and terminates/reaps its process group. An authorized launcher must enforce those bounds, preserve compiler/launch exit or signal, and never label killed processes clean. No performance measurements. No RLIMIT_AS limit that interferes with ASan shadow reservations.

## Exact build argv (after approval only)

Working directory: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-native-leak-controls-20261014

/usr/bin/gcc -std=c11 -O1 -g -Wall -Wextra -Werror -fno-omit-frame-pointer -fno-optimize-sibling-calls -fsanitize=address,undefined leak_control.c -o leak_control

Before compiling, verify frozen source/tool/runtime hashes in FREEZE.json; reject an existing output binary or receipt. Record compiler stdout/stderr/exit. After success, record binary SHA-256 and readelf dynamic dependencies before running. Do not use this standalone control to claim that the Python extension's preload/import configuration is qualified.

## Exact launch argv and environment additions

Only these subprocess-local environment additions/replacements are authorized by this proposal:

ASAN_OPTIONS=detect_leaks=1:leak_check_at_exit=1:halt_on_error=1:abort_on_error=0
LSAN_OPTIONS=exitcode=23:report_objects=1
UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1

The GCC-built executable links the sanitizer runtime directly, so no LD_PRELOAD is added. Before launch, inspect only the names/presence and relevant values of sanitizer/loader variables. If an inherited LD_PRELOAD, LD_AUDIT, LSAN_OPTIONS, ASAN_OPTIONS, UBSAN_OPTIONS or sanitizer log/suppression override would conflict with this frozen configuration, stop and report it rather than silently running or changing global settings. Do not dump the entire environment or secrets. Record the effective specified flags. No suppressions, disabled regions, ignored objects, alternate root scanning, debugger or ptrace wrapper.

Within the reviewed working directory, execute these exact argv arrays using the above environment overlay and bounded supervisor (not an unbounded shell):

1. ["./leak_control", "clean"]
2. ["./leak_control", "free"]
3. ["./leak_control", "leak"]

Equivalent human-readable commands, with the same mandatory supervisor bounds:

env ASAN_OPTIONS=detect_leaks=1:leak_check_at_exit=1:halt_on_error=1:abort_on_error=0 LSAN_OPTIONS=exitcode=23:report_objects=1 UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 ./leak_control clean
env ASAN_OPTIONS=detect_leaks=1:leak_check_at_exit=1:halt_on_error=1:abort_on_error=0 LSAN_OPTIONS=exitcode=23:report_objects=1 UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 ./leak_control free
env ASAN_OPTIONS=detect_leaks=1:leak_check_at_exit=1:halt_on_error=1:abort_on_error=0 LSAN_OPTIONS=exitcode=23:report_objects=1 UBSAN_OPTIONS=halt_on_error=1:print_stacktrace=1 ./leak_control leak

## Frozen acceptance signatures

- clean: exit 0, stdout exactly `CONTROL completed mode=clean bytes=0 normal-return\n`, empty stderr.
- free: exit 0, stdout exactly `CONTROL completed mode=free bytes=131071 normal-return\n`, empty stderr.
- leak: exit 23, stdout exactly `CONTROL completed mode=leak bytes=131071 normal-return\n`; stderr contains `LeakSanitizer: detected memory leaks`, `Direct leak of 131071 byte(s) in 1 object(s)`, and `131071 byte(s) leaked in 1 allocation(s)` with allocation provenance attributable to allocation_control/leak_control.c, or, if symbolization is absent, an independently resolved address inside that pinned executable's allocation path. Raw reports must be retained. Addresses/PIDs are not exact-string oracles.

A zero leak-mode exit, missing intentional allocation, fatal thread-scanning error, sanitizer startup failure, timeout, extra/unattributed leaks, missing provenance or unexpected diagnostic is not a pass. Preserve the failure and stop, without installations, security changes or repeated attempts to obtain a desired result. Conservative stale stack pointers can hide an intentional leak; a miss is inconclusive regarding operational support, not proof that the detector is unavailable. A revised control would need independent review and a newly frozen protocol.

## Meaning of a pass

All three observed signatures establish bounded detector sensitivity for this standalone executable/configuration. They do not establish Python preload operation, CF1 leak absence, provider-internal allocator behavior, reachable retention correctness, zeroization, fork behavior, product security, performance or full DESIGN admission. Before CF1 leak checks, a separately frozen Python/extension launch must repeat suitable positive/negative controls in its own launch configuration. Do not import native candidates as part of this control stage.

## Review handoff

Review actual malloc/free visibility under flags, pointer reachability at exit, exact signatures and bounds, compiler/runtime pins, subprocess-only environment scope, and absence of provider/security/network/candidate operations. Root should authorize compilation and bounded execution only after that review. No runnable launcher has been executed or supplied as evidence of a pass.
