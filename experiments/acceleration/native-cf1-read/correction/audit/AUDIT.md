# Independent native CF1 correction evidence audit

2026-10-14. Verdict: the bounded correction evidence is internally consistent and closes the named gaps at the scope described below. Full DESIGN correctness admission, timing and product/backend admission remain HOLD. No certain blocking defect was found in this correction's implementation or receipt correspondence. This is a static/data audit, not an independent execution attestation or complete security review.

## Scope and method

Compared candidate-native-cf1-read-correction-20261014 against the original candidate-native-cf1-read-20261014/evidence-audit/AUDIT.md. Read correction source, manifest, receipts, static review and relevant unchanged wrapper/key source. Independently calculated JSON correspondence, canonical descriptor SHA-256, UTF-8, fixture/pin/inventory hashes and AST assert absence. Ran only the new stdlib-only verify_data.py in this audit directory. No native/product imports, crypto, old or new test reruns, builds, benchmarks, DB, Git or input changes. verification.json is the data result; verify_data.py makes its checks reproducible without candidate execution.

## Verified results

- Exactly 43 unique predeclared ordered observation IDs: eight table-derived context relocations, sixteen domain-policy mismatches (valid/malformed frame in eight modes), six A/B/A reads, two NULL, six lifecycle, three decode-expiry and two post-native PID. There are 12 text/NULL outcomes and 31 refusals. All 18 fixture descriptors, text/UTF-8 pairs and referenced frame hashes match.
- Both positive launch receipts have exit 0, empty stderr, PASS, and exactly the manifest's ordered 43 IDs. Each actual record equals its frozen expectation, including exact text/type or safe failure fields and full ordered resolution arguments, plus helper-call count. O0/O1 observation arrays are identical. All three decode-expiry records have decode_hook_completed=true.
- Failure observations compare class, code, stage, retryable, effects, remedy, operation-ID presence and trace. They do not compare literal operation IDs or exception args/message/cause; the current exception args include the changing operation ID. Thus “full safe fields” is accurate for the stated schema, not an unrestricted assertion that every exception property is compared.
- All 628 listed pins currently match; all 130 original inventory files currently match. Launch receipts refer to the current PINS digest and count; launch receipt hashes match each positive/negative result. Freeze receipt's manifest digest matches cases.json. All seven correction Python files are AST-assert-free.
- cases.json SHA-256: 25e1252cbee9bd2e350aca536e8f0622049050610462c022e00edf5c9547afdb
- PINS.json SHA-256: 4211076650a56db951155113e7b4dfa94d6dcc84d602fa0ba126065d530daed8
- Original ARTIFACTS.json SHA-256: bd6fba6d773ca746ae8ac0bc4ecc0f539f95fcf244b488b3bd6bc9e191ea81a8

## Source-to-evidence interpretation

### Context gaps

The table cases alter table_id, recompute canonical descriptor digest and rebuild the descriptor. All eight representation/record/tenant modes are represented. In single-tenant modes the expected tenant changes with table ID and policy/material match, avoiding early single-tenant-context rejection. These are combined table/tenant relocation tests in those modes, not independently isolated table-only perturbations. All table cases reach one helper call and AuthenticationFailed.

All sixteen policy-domain cases retain the original descriptor but construct a different policy domain with internally matching material. Valid and malformed empty frames both produce KeyUnavailable, empty resolution trace and zero helper calls. This addresses the original explicit domain-policy/precedence gap.

### True two-scope sequence and lifecycle

A uses tenant UUID integer 4 and record UUID integer 5; B uses 444 and 555, respectively. B text is exactly “scope-B-雪”; A is “abcdefg”. Storage and equality each perform A/B/A, and the per-group/per-fixture cache in check.run reuses the first A PreparedKeys for the second A. Every successful non-NULL read has one helper call; the following A/NULL read has zero helper calls and one active-payload resolution. NULL follows the sequence rather than interleaving it. This is sequential isolation evidence, not concurrent thread/event-loop isolation.

Lifecycle valid and expired reads share the same PreparedKeys reference and unchanged frame. expire replaces material entries in the same dictionary exposed through MappingProxyType, so the already-used object's next resolution sees expired material. The expired call refuses at its first payload resolution, before native entry. The fresh step reconstructs PreparedKeys and checks object distinction before success. This closes the same-object controlled-state gap; it does not demonstrate natural time passage, provider refresh or provider custody.

### Late checks

DecodeBoundary.decode first performs strict built-in UTF-8 decoding, then expires selected material before returning text to the wrapper. The three payload/search paths stop at their expected final resolution: storage payload; equality payload; equality search after final payload succeeded. The C result is wrapped in a research bytes subclass only at the separately named wrapper helper boundary. This tests a deliberate decode-to-final-check boundary, not a natural concurrent expiry event.

PID cases mutate prepared._pid immediately after the original helper returns successfully; final payload resolution rejects in both representations. These are simulated stored-PID mismatch tests, not actual fork or OS PID change tests. The old actual fork evidence is preserved rather than rerun. The hook is restored in finally.

Counts surround _native_encoded; static inspection shows that unchanged helper invokes native_cf1.open_encoded once. They support the stated call-count claims, but are not an independent C-internal execution counter.

### Actual returned-text negative

This is materially stronger than the original wrong-literal comparator. invoke calls the real wrapper, obtains its observed returned value, verifies the entire unmodified record against the frozen original_expected, deep-copies that actual record, appends !CORRECTION-NEGATIVE! to actual['value'], and compares it with the same strict comparator. The altered data is derived from actual candidate output; no successful literal-versus-literal check is counted as an end-to-end oracle.

Both negative launches exit exactly 1 with FAIL, zero passed checks, error_type RuntimeError and exact error “Mismatch: actual-output-perturbation”. Both observations have native_calls=1, original_verified=true, perturbation_applied_to_actual_return=true and comparison_expected=reject. Stderr terminates with that same exception. Thus neither an unrelated import failure nor a different candidate failure is being accepted as the intended negative result.

Important bound: this is a downstream actual-return observation perturbation. It is not a mutation inside the C helper, decoded wrapper return channel or product source. The receipt stores flags/count rather than the full original/mutated record; source inspection supplies the dataflow evidence. Do not call it a native-return-channel mutant.

## Predeclaration and provenance limits

The generator freezes all 43 outcomes and the negative expectation into cases.json without importing the native candidate. prepare checks old pins, invokes that generator and includes generated manifest/fixtures in PINS. launch checks pins and environment/origins before native imports. Unlike the old supplements, these IDs and expected records exist in a required JSON manifest before candidate import. This mechanism and matching receipts are useful provenance, not authenticated chronology or proof that a historical process executed exactly as reported. Current hashes cannot independently prove every intermediate historical state was immutable.

## What remains HOLD

This slice closes the eight table/domain-policy omissions and adds bounded true-scope sequencing, reused-key lifecycle, late decode/PID checks, exact observations and a real downstream output-derived negative. It does not retroactively change original evidence:

- Original frozen/grid read assertions still use length/hash; exact text expectations here cover selected A/B fixtures, not every old case or all eight frozen vectors. Frozen seal/equality parity gap remains.
- Complete original supplementary IDs/outcomes were not pre-frozen; class-only old after-native/fork/fault checks remain class-only. Full injected native fault-mapper diagnostics are not repaired.
- Six primitive oracle entries and frozen intermediate-value diagnostics are still absent.
- No measured allocator/context balance, leak qualification, comprehensive allocation/provider-failure branch evidence or complete fault equivalence is added. Recovery does not prove cleanup.
- Cross-thread/event-loop distinct-context isolation, real provider custody, async cancellation and memory erasure are not established by these synthetic sequential tests.
- Observable stage/cause ambiguity remains: data/final failures mapped to authentication need not have an authentication root cause. Omitted pyca unused-encrypt/copy paths, differing allocation order and differing native backend remain limits.
- Packaging, platform/provider qualification, full DESIGN admission, performance and product/backend approval are not supplied by a 43-case correction PASS.

No additional execution is implied or requested by this audit.
