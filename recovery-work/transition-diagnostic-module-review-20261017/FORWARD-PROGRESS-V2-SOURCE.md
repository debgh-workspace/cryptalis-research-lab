# Forward progress inspector V2: independent source acceptance

Disposition: ACCEPTED for a separately selected bounded no-DB recording-connection run. No target code, import, compile, syntax test, SQL or DB execution occurred during this review. V1 remains preserved with its two test gaps.

Packet: recovery-work/forward-progress-inspector-v2-20261017.
Seven-member SOURCE.sha256: 96e0473ec83634c04402706fbae983dfc937338e1c5b97c0b531c2f4fa093ede.
Inspector: d0c26812e5b6da080ae775042654202a99223e2f6c0a33e414c41c590075d61b.
Cases: 77db56febf3d3665f5a0fc9f10d3f77438e846d95657ab16168215cc7331efa9.
Runner: 35645457ee4390dda73803262fa93b461550cce2009110a24a53b7ead9cf6dd3.
All seven hashes and the seal were independently checked against ordinary stable files. Composition manifest, materialization receipt and 509 dependency map are byte-identical to the accepted combined222 runner. All 43 actual product runtime hashes were independently checked against that manifest during this review. Fresh full admission remains required at execution time.

## Code boundary

Exact built-in containers/scalars, three literal protect formats, two literal codecs, canonical UUID table identifiers with duplicate rejection, exact phase/model/scope/verification key sets, nonnegative exact integer inequalities, canonical signed64 or UUID cursor domains and phase completeness are enforced. Bool/int subclasses are excluded. Zero rows require null cursor and zero chunks; positive rows require a positive chunk count and canonical cursor. BACKFILLED and verified forms require complete local counts. ABORTED can retain optional complete verification and historical metadata; active_schema belongs only to PENDING/ACTIVE/DEPROTECTING. No phase is inferred from schema/guard content.

Output is a frozen/slotted dataclass containing only fixed strings/Booleans, with metadata_validated and successor_authorized permanently initialized false. Inspector writes no input, retains no metadata references and is never connected to operational admission. Opaque schema/guard/active_schema values are deliberately unvalidated. Cross-table reachability, actual scope membership, catalog consistency, authenticated plan/current authority, raw JSON budgets and successor permission remain outside the result.

## Independent oracles

Static enumeration yields 68 distinct outcomes: 19 positive serializer/readback/profile cases, one exact literal profile-set contract, 40 fixed-code negative mutations, six existing _state refusals, and two _save rowcount refusals. Negative cases continue independently and require exact typed refusal codes; unexpected exceptions fail the case. BaseException interruptions escape and prevent success. No source mutants have been executed; the README lists prospective source mutants only.

Actual _save is bound through exact SQL and identity parameters to a recording connection. JSON decode equality and unchanged original inputs are asserted. Rowcount 0 and 2 now require exact journal_marker_write_failed with the original operation identity and preserved state/serialized parameters. These two cases resolve V1's missing mismatch coverage. Profile positives now use three independent literal strings plus an exact set oracle rather than deriving the oracle from inspector.FORMATS, resolving the other V1 gap.

Actual _state routing is phase-sensitive: ABORTED positive uses allow_aborted=True/PREPARED; ACTIVE uses ACTIVE; DEPROTECTING is serializer-only with a separate expected forward read refusal. Other ahead-of-PREPARED states use current semantics. Six refusal controls cover missing operation, ordinary/wrong-pin ABORTED, stale ACTIVE, DEPROTECTING and behind-pin state. No recording connection executes SQL or supplies transaction, native JSONB, catalog, commit or historical provenance evidence.

The finite above2**53 fixture demonstrates only the selected exact integer through Python JSON serialization. It does not establish arbitrary-size transport/PostgreSQL numeric support. UUID and signed64 boundary examples remain local syntax coverage. Input preservation is asserted on positive/negative calls; post-return mutation of copies checks the absence of retained mutable metadata.

## Runner and launch boundary

Diff against accepted combined222 runner preserves finite admission/audit, 509 dependency origins, V9 closed Cython/OpenSSL/typing/deprecation-wrapper bindings and postcase identity checks. Adds only two pinned local modules with exact module/function origins, local path entry and new case dispatch. V2 changes only V1 path/count plus the two oracle fixes. Actual combined222 source remains the product import target, not donor files. Preservation count is 560:509 dependencies+43 runtime leaves+seven controls+seal. Result bound remains256KiB; all68 PASS, no primary, full closure and absent bytecode cache are necessary for success.

Root may separately select the existing pinned Python3.12 under env -i LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC PSYCOPG_IMPL=binary, cwd the exact V2 packet, flags -I -S -B -X pycache_prefix=<absolute V2 packet>/bytecode-absent, absolute run_module_diagnostics.py, then arguments combined and 96e0473ec83634c04402706fbae983dfc937338e1c5b97c0b531c2f4fa093ede. Existing 60s wall/2s grace,30s CPU,1GiB virtual memory,512KiB file,core0 envelope and stdin /dev/null are adequate proposed bounds; root must admit/read back limits and preserve launch/source/host before-after evidence even on failure. No launch was performed here.

Trusted same-host stdlib/native-loader/system initialization remains explicit. Native OpenSSL initialization may occur; no application/key-provider API or real DB connection is called. This is not a race-free native sandbox or vendor-provenance claim. Passing records would qualify this recording-connection/local-inspector slice only; all operational recovery, destructive admissibility and successor authority gates remain unchanged.
