# Standalone leak controls: blocked on first runtime control

2026-10-14. Frozen source and launcher pins verified; no inherited loader/sanitizer override names were present. GCC compilation succeeded with exit 0 and empty stdout/stderr. The binary directly needs the expected ASan/UBSan libraries, recorded in elf.stdout.

The first `clean` process reached normal return from main and printed exactly:

    CONTROL completed mode=clean bytes=0 normal-return

Its LeakSanitizer exit-time check then failed:

    ==12==LeakSanitizer has encountered a fatal error.
    ==12==HINT: For debugging, try setting environment variable LSAN_OPTIONS=verbosity=1:log_threads=1
    ==12==HINT: LeakSanitizer does not work under ptrace (strace, gdb, etc)

The actual exit status was 23, preserved in clean.json; this is a fatal-detector exit, not an intentional-leak success signature. The process was not timed out and its output did not exceed limits. This diagnostic does not prove a debugger was attached or identify the precise failing syscall/security rule. No diagnosis beyond the observed runtime failure is asserted.

The frozen stop rule was followed immediately: free and leak modes were NOT RUN; there was no retry, extra diagnostics launch, install, security change, provider change, native CF1 import/execution or benchmark. STOP.json preserves the supervisor's failed-gate result. The enclosing shell continued to display receipts, so its overall exit code is not the test verdict.

Disposition: installed leak-capable runtime is present, but operational support was NOT ESTABLISHED in this exact permitted configuration. Candidate leak evidence stays UNKNOWN. A clean control's detector fatal error is not a candidate leak and is not evidence of leak freedom. The tool's verbosity suggestion is not authorization to run more processes or relax restrictions.

Pins:
- C source SHA-256: e0ba833a37e8fff514e0f26354f311c6b55517bb85641f141307e08989ec4e81
- Binary SHA-256: 143b41accb66a4e26961843b9a2a28bf4b904b6cfb37ee1146f5bf3c56d41e22
- Launcher SHA-256: c62e2b8a86e2d70bdb6c03abd07026916cf9cf2666de406c4ec45381efa8bc41

All build, preflight, dynamic metadata and clean-control receipts, stdout and stderr remain in this directory. Existing source/evidence trees were not changed.
