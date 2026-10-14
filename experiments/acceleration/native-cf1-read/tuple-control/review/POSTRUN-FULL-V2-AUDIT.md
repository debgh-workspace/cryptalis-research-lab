# Independent full-wrapper V2 postrun data audit

2026-10-14. Data/source audit of `candidate-native-tuple-control-20261014/full-evidence-v2-01`. This reviewer did not execute/import/build/rerun the candidate or harness. Only this review note was written.

## Verified result

Both ordinary Python and -O receipts contain exactly the canonical 1098 IDs in order, without omissions/duplicates/extras: 2196 positive case instances total. Every actual record was independently compared recursively with exact JSON types against the canonical literal record after removing only F's native_calls and adding the frozen T tuple_entries. All full strings/bytes encodings, value_type, exception class/code/stage/retryable/effects/remedy, operation-ID presence, safe-args/cause flags and ordered resolution arguments match. No expected outcome was computed through T.

Per mode:

- 628 cases enter3 tuple calls;394 enter0;76 enter6.
- Every tuple_sites sequence equals the declared ordered prefix for that count.
- All3 decode-expiry cases report completed hooks; no other case does.
- Both post-native PID cases report exactly1 hook; every other case reports0.
- Each of8 sealing cases reports1 synthetic nonce call; other cases report0.
- Positive receipt status PASS, child exit0, empty stdout/stderr, no negative record.

All12 expected negative runs were independently checked, six per optimization mode. Their original observations equal their selected frozen expected records. Their actual mutations are exactly the declared text suffix, wrong type label, wrong stage, appended trace, incremented tuple count, or suppressed decode hook. The hook negative changes the frozen KeyUnavailable result to exact string `abcdefg`, with the expected two-payload-resolution trace and3 tuple entries. Each mutated record differs from its original. Every negative has exit1, FAIL, RuntimeError with exact `Exact admission mismatch`, expected traceback suffix, no positive observations and original_verified=true.

## Receipt and provenance consistency

The directory contains exactly43 artifacts:14 child result receipts,14 cache receipts,14 individual launch records, and the aggregate launch list. Aggregate and individual launch records are identical and ordered as the frozen14-child plan. Every result/cache SHA matches its launch record. Ordinary/-O flags, mode labels, source freeze hashes and hook hashes agree.

Each child records verification of the original4387pins. Each additive cache receipt reports before/after PASS against V2 SHA256 `5baccd54e797c542faa240d24ec6d8e27aea8bbae01dcf3cd952770d7b4e9e01`. All4459 V2 pins independently match current bytes, and all five cache inventories match. Crypto receipts identify the pinned cryptography origin and `OpenSSL 4.0.3 29 Sep 2026`. Normal T binary and build receipt were already pinned/reviewed; no diagnostic export is admitted by the runner.

Direct evidence remains preserved: both direct binary hashes match their build receipts; all eight direct child receipts match their original launch hashes; positive direct build hashes still match their original build records. Existing reviewed source pins remain unchanged.

## Interpretation and limits

Unlike the direct ABI receipts, these full-wrapper receipts retain actual output/error/trace records, so their exact equality could be independently rechecked from saved data. They remain ordinary self-produced execution records, not signed machine attestation. Matching current pins plus before/after receipts supports bounded provenance and source stability; it does not prove absence of every unrecorded action or transient mutation.

This supplies finite exact full-wrapper equivalence evidence for the1098-case T adaptation in ordinary/-O on the pinned local runtime, including declared PID/decode hooks, sealing/query parity and caller-isolation cases. Synthetic public-material tests exercise consumption boundaries, not production key-provider custody.

It does not close the complete original DESIGN: actual fork/fresh-child recovery, six full-wrapper allocation-site fault tests, genuine skipped-term/skipped-final code mutants, required after-helper lease-expiry cases beyond current PID hooks, actual allocator-exhaustion behavior, sanitizer/leak support, and full requirement mapping remain separate gates. Five post-observation mutation controls are harness sensitivity checks; suppressed decode hook is a genuine hook-removal control, but neither substitutes for skipped authentication/final-check source mutants. GIL-held thread/event-loop cases are not async cancellation qualification.

No timing, backend attribution, full five-arm protocol selection, production adoption, independent security qualification, or C9/C10 admission follows. Full DESIGN/timing HOLD remains; this audit finds no data inconsistency in the bounded completed run.
