# Independent review: static doctor plain-text remedy

Date: 2026-10-15 UTC

State: patch/source and proof-source review complete. No blocking issue found within the stated unit boundary. Coordinator selection is required for execution.

## Result

No blocking defect found in the exact proposed runtime delta. The change makes an existing fixed declaration remedy visible in the plain-text static doctor report. It does not alter the JSON report, native diagnostic API, declaration admission, exit handling or output delivery implementation.

This is a source-level conclusion. No project code, test, proof, import, build, database route or installed package was executed. No runtime PASS, deployment qualification, objective completion or production-readiness claim follows from this review.

## Exact reviewed identity

Proposal: `experiments/preview-doctor-dx-slice-20261015`.

- Patch SHA256: `31e117393dd77d40a8d10733434defe55c6b590958ec25d73afaaa5821592e10`
- Baseline CLI SHA256: `0df0b4f0101933b3a069024965b7bc5a3374747aff53d37099d2f22efc105efe`
- Overlay CLI SHA256: `060cb66057f66c6d22c2b455bfba918545a3fabc251e72a30ab8fbfe61b0f409`
- All 11 entries in `SOURCE_PINS.sha256` matched the selected candidate files.
- All six entries in `ARTIFACT_PINS.sha256` matched the proposal files.
- The selected candidate's `src/cryptalis/cli.py` byte-matched the retained baseline.

The exact baseline/overlay diff contains one added line, within the plain-text branch of `_doctor_command`:

```python
+ (f"\n  remedy: {check['remedy']}" if "remedy" in check else "")
```

No other line differs. The patch has the same hunk as the independently obtained file diff.

## Contract checks

1. **Plain text and approved purpose.** Existing public failure guidance calls for concrete safe remedies. The baseline reports the manifest rejection code while omitting its existing remedy. The added line supplies that remedy immediately below the corresponding check. The change is intentionally additive for rejected plain-text output; exact plain-text rejection byte compatibility is not claimed.

2. **JSON.** The `machine_json` branch still serializes the original `result` with the same `json.dumps` parameters. The added expression is confined to the other branch and does not mutate `result`.

3. **Static/native boundary.** `_doctor_command` still calls `doctor(raw)` without mapping, engine, writers, sources, deployment, keys or audit opt-in. The default phase remains pre-adoption. For valid bytes the doctor returns before compiler/native work because all host inputs are absent. Invalid declarations return earlier. Setup, active and ciphertext paths remain unreachable through this static CLI. Their implementation files are unchanged by the exact delta.

4. **No new dynamic-input disclosure.** The only remedy reachable through this static CLI is the literal `Supply a valid bounded cryptalis.protection/v1 declaration.` assigned when declaration parsing raises `ManifestInvalid`. The renderer does not interpolate the path, declaration bytes, parser exception, model/field names, host object, provider value or raw exception. The conditional also avoids accessing a missing remedy. This conclusion applies to the current static report producer; a future producer of nonconstant remedies would need its own disclosure review.

5. **Exits and incomplete state.** The unchanged final return is 2 for a rejected manifest and 3 otherwise. The incomplete/no-deployment banner, all report authority/ready/complete fields and explicit-host notice remain unchanged. The line adds no exit-0 path or native-admission claim.

6. **Input/file boundary.** The unchanged reader opens input read-only, requires a regular file, and reads at most `MAX_DOCUMENT_BYTES + 1`; the parser enforces its existing size and depth bounds. No write or repair path is introduced.

7. **Output failures and redaction.** The complete rendered string is still passed to the existing `_write_output`. Its short-write, write, flush and cleanup failures retain the sanitized `CLI.OutputUnavailable` handling and exit 4. The new line does not catch errors or create a second output route. Error envelopes and correlation handling are unchanged.

8. **Test-plan scope.** `UNIT_PLAN.md` distinguishes expected baseline failure from executed evidence, selects synthetic local inputs, covers rejection markers, JSON/valid-output compatibility, dynamic-path sentinels and output failures, and requires an independent omission control. It does not authorize database execution or production promotion. The existing static doctor tests inspected in `tests/test_doctor.py` use JSON; they do not directly protect this plain-text behavior.

## Preservation and limits

The 11 pinned selected source/contract files were verified without modification; the selected CLI remains the original baseline. This review made no write to the selected candidate or proposal. Reviewer files are confined to this review directory. The complete 221-file selected inventory, packaging identity and selection metadata have not been independently re-audited here.

An optional read of `cryptalis-executable/CRYPTALIS_BUILD_CHECKLIST.md` found no file at that path. The coordinator subsequently confirmed that the authoritative checklist is one directory above, and that no further checklist read was needed. No alternate location was guessed or retried. This does not affect the directly checked source and security/playbook contract conclusion; this review does not independently corroborate the proposal's root-checklist selection/objective references.

## Independent proof-source review

The author handed off the stable `proof-v1` packet before review. Verified identities:

- `INPUTS.sha256`: `25690581b4618f67c0debfb4e74fc3985c805bcd228e7fa90571ed2045d71c9f`
- `prove_doctor_remedy.py`: `4faeab05a1a44483b6573331e8e7ae24e3dee6013c85d4afde71d08c5a8c6544`
- `RUN_PLAN.md`: `0d1a2e50bd8a84ac422e6e7c753d2a837ab4d5a377676acffb09b1ed1a01230c`
- Copied source manifest: `202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520`

All 21 input pins matched the packet files. The eight copied source hashes match their entries in that pinned candidate manifest. Direct byte comparisons establish baseline equals omission mutant, derivative equals exact-restored variant, and the proof derivative equals the independently reviewed overlay. The 472-entry stdlib path and digest inventories are pinned proof inputs. This review did not read or hash the 472 live runtime files or execute the interpreter; preflight must still establish their runtime match.

The proof source is suitable for the coordinator to select as a finite unit check, with the following verified properties and limits:

1. **Actual changed boundary.** It loads exact copied source bytes for the CLI, doctor, parser, declaration and required local helpers, then calls the actual CLI `main`. It does not manufacture product observations from expected strings. Compiler/compatibility import collaborators and unentered dynamic paths are explicit fail-fast stubs. `_active_report` is replaced by a sentinel. These are disclosed unit boundaries, not installed-import, database, provider or full native-operation evidence.

2. **Meaningful independent oracle.** Expected plain text and complete JSON are written independently in the proof. There are nine actual CLI invocations plus two positive-control cases per variant: two rejected plain outputs, one valid plain output, rejected/valid JSON, write/short-write/flush failures, double-channel failure, dynamic-sentinel controls and redaction-collector controls. The fixtures are bounded synthetic documents; their schema, distinct canonical UUIDs and storage-only field match the inspected declaration grammar.

3. **Real RED and omission evidence.** Baseline and omission mutant use the original CLI bytes. Both are expected to fail exactly the two remedy assertions; their failed cases remain process exit 1. Derivative and exact-restored use identical changed bytes and are expected to pass all cases. The proof does not skip cases or relabel expected failures as ordinary passes. No RED/GREEN result exists from this review.

4. **Captured output and redaction.** Ordinary calls retain stdout/stderr and the actual returned exit. Failing-stream observations are explicitly marked delivery attempts. Private content, schema, path and I/O markers are checked; the collector's positive control verifies that each marker would be detected. JSON and valid-output cases independently check exact output. Dynamic sentinels count entries and receive a positive effectiveness control.

5. **Finite, pinned route.** Preflight requires the handed-off inventory anchor, exact interpreter identity, isolated/no-site/no-bytecode flags, an empty child environment, the declared search path, absent bytecode-prefix and ZIP routes, exact source/variant relations and admitted module origins. It installs a Python audit guard before product source execution and rechecks the pinned input files and fixtures after observations. No external command, network call, package install or result-file writer is present in the proof. These controls are unit assertions, not a hostile-native-code sandbox or a complete interpreter supply-chain claim.

6. **External acceptance remains necessary.** The coordinator must independently select and supervise one serial variant at a time, provide the literal sealed input hash, enforce the external wall/output bounds, and inspect actual receipts before the next variant. Internal resource limits and the alarm do not replace that supervision. Each RED requires only `expected_text_exact` false in D01/D02, every other check/case passing, correct exit 1 and complete terminal evidence. Each GREEN requires all 11 cases passing and exit 0. Any other failure, ERROR, timeout, missing record, unexpected exit or integrity mismatch is HOLD. Compare D03/D04/D05 output and exits across all four receipts as the plan requires.

The original test plan's existing-suite and installed-artifact checks remain outside this proof. Passing these isolated cases would establish the narrow rendering property and its listed controls only. Full selected-inventory preservation must be checked separately during candidate assembly.

## Final review disposition

No revision is requested for the exact one-line patch or sealed proof source. Proceed only through the coordinator-selected finite route, preserving actual baseline, derivative, omission and restored evidence. Selection, promotion, installed compatibility and production gates remain separate decisions. The reviewer performed no code imports, syntax checks, test execution, database activity, environment inspection, live-cell/cache/credential/corpus access or Git operation.
