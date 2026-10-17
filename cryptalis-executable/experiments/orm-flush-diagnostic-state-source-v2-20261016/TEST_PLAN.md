# Marker/name cleanup successor: isolated implementation and regression plan

Status: SOURCE PREPARED; NO EXECUTION. Separate from frozen preview and note-only
V1/V2. No database, install, Git, live payload or authority operation was made.

## Derivation and exact scope

Base: `orm-flush-diagnostic-continuation-v2-20261016`, seal
`229c4296eabe7174bc32144c1bc05b05fa57d077f177330ce6c801f3e2efebaa`.
The two copied base source hashes are:

- sqlalchemy.py: `5ccac0060cb70dee9be4257289f8d9120e2f09ef88d9528ea139605d670a73fc`
- _sqlalchemy_transactions.py: `2d08b41c96ecabe99d8339fb7778c0b050b5338885d6292841943f3b409a5bc5`

Design: `orm-flush-diagnostic-state-design-v1-20261016`, seal
`68f059de7dc0fd52f78a13d877f5eea29fd1ba9e2acdaccd6fbdf4a8dc215a5f`;
independent design review
`3b7f1b8b7fc09f295044790c115631ff05d56075b06b9244f2f0807ec5cffc23`.
The design inventory's timing phrase is not a prior execution claim.

`NOTE_ONLY_TO_STATE.patch` is the complete product delta from the note-amended
baseline. There are no other source changes. The outer helper's signature and
eight invocation sites remain unchanged. The sole lower-helper caller supplies
an exact local built-in dict initialized to None. Only a completed fallback loop
publishes its monotonic Boolean. The wrapper treats only the exact False object
as a completed bounded observation; everything else is incomplete/unconfirmed.
No exception attribute stores or supplies cleanup outcome. All three secondary
exception-name interpolations are replaced with reviewed fixed safe text.

The lower helper still raises its original rollback exception after the loop.
The outer helper still preserves the original preparation failure for its
caller's re-raise. Unexpected failures before final publication leave None and
cause the unconfirmed warning. Query/refusal rules, public CryptoFailure fields,
native cleanup order and physical-driver ownership remain unchanged.

## Distinct source selections; no signature-error RED

Use the note-only amended source as the new baseline, not frozen selected221.
The new shared `test_flush_cleanup_state_faults.py` calls only the unchanged
outer helper API and the real imported lower helper. Therefore it can run
unchanged on note-only and successor sources without a signature adapter,
AST extraction, simulated product code or an expected TypeError.

Its one test method contains ten subcases:

- ordinary exception control, setter failure, getter failure, stale-False
  setter, and exceptional type-name lookup;
- each crossed with first physical-close success or failure;
- all require second-connection cleanup, original primary identity, cleared
  preparation state, the exact attempted-action sequence, no exception metadata
  hook dispatch, and the correct incomplete warning.

Predicted note-only baseline: eight assertion-failed fault arms and two ordinary
passing controls. The stale-False/successful-close arm specifically fails the
no-marker-hook invariant, even when its old outcome happens to agree. The
failed-close arm also exposes skipped continuation/stale state. Predicted
successor: ten passing arms. These are static predictions, not actual results.
Setup/import errors or signature errors are not acceptable RED evidence.

## Preserve the original fifteen checks

`test_flush_diagnostic_continuation_successor.py` copies all three V2 methods
and all fifteen subcases. `NOTE_TEST_ADAPTATION.patch` shows only explicit private
call/outcome adaptations: required keyword on the stub, direct helper calls with
fresh owned dicts, stub publication of the intended outcome, and exact bool
outcome assertion instead of exception-marker assertion. All primary, context,
capture-flag, note-channel, later-connection, clear-preparation and no-op oracles
remain. These adapted private calls are successor-only; run unchanged original
V2 tests against the note-only baseline to preserve that separate evidence.

`test_flush_cleanup_state_contract.py` is also successor-only:

- one method has four subcases for unpublished None, missing key, integer zero,
  and an object whose truth hook raises; the wrapper must preserve the primary
  and warn, without truth dispatch. It observes the exact initial dict type and
  value outside the caught callback.
- one ordinary test forces an unexpected connection-property interruption
  during the loop. The helper must leave its outcome None, never publish partial
  False. This deliberately does not claim that unrelated hostile connection
  hooks permit remaining cleanup to continue.

Successor total: six unittest methods, 29 subtest arms and one ordinary test.
The runner must report both subtest and ordinary-test results; it must not
silently drop the unparameterized interruption test or count it as a subtest.
Expected successful assertions do not prove physical connection release.

## Admission and limits

Reuse the independently reviewed no-site real-module unit route only after new
source/test/hash/ledger review. The eager fifteen Cryptalis source modules and
external dependency sets from note-only IMPORT_PLAN.md are unchanged. Test-only
imports remain unittest, unittest.mock, types and sys. Use separate fresh
processes and source origins for note-only/successor and SA21/SA20, explicit
test selection, exact closure receipts, clean startup, no pyc and preserved
outputs. This document grants no execution authority or file-read expansion.

Synthetic exception hooks are local robustness fault injection. Ordinary
provider Exceptions remain sanitized; true cancellation and ordinary library
exceptions retain their existing contracts. Arbitrary hostile Python running in
the process is not a security isolation boundary. Host termination, allocation
failure and unrelated connection/driver hooks remain outside this narrow fix.
False is a bounded algorithm observation, never verified rollback/release or
readiness. Native database evidence and any fixture ACL approval remain separate.
