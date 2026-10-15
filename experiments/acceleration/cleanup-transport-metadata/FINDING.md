# Trusted-local cleanup metadata: isolated source correction

Date: 2026-10-14. Status: source prepared; all runtime checks NOT RUN.

## Result and boundary

The isolated GREEN candidate changes only `src/cryptalis/crypto/keys.py::CryptoFailure.__reduce__` and adds `tests/test_crypto_failure_transport.py`. It inherits the exact 217 source files from `candidate-next-unblocked-correctness-20261014`. RED retains all inherited bytes and adds the same test. Both trees contain 218 source files.

The internal reducer previously preserved `code`, `operation_id` and `args`. A class constructor recreates class-level defaults. Source inspection therefore predicts loss of the async cleanup branch's instance-level `effects = "unknown"` and `retryable = False` downgrade. In particular, a `KeyUnavailable` would regain its `none`/True defaults. This finding has not been reproduced by this preparation.

The correction keeps the original class, empty constructor arguments and three diagnostic state fields. It examines effects once. Only an exact built-in string equal to `unknown`, together with the singleton Boolean False, adds the two fixed primitive values to the state. It does not serialize the examined objects. Class defaults remain the restoration behavior for other combinations.

This is an internal trusted-local consistency correction. It admits no public IPC capability, general exception transport API, untrusted pickle input, cross-process cleanup qualification, or cross-version guarantee. All seven full gates remain UNKNOWN.

## Contract ownership

Paths below refer to the inherited candidate. Their exact bytes are retained by `INHERITED_SOURCE.sha256` and `INHERITED_SOURCE_MANIFEST.json`.

- `docs/architecture/README.md`, Approved scope: internal transport and diagnostic helpers are INTERNAL ONLY; implementation details do not admit public capabilities.
- `docs/security.md`, Public failure contract and slice-2 failure description: retain safe identity, retry/effects information, and remedies; do not echo raw provider failures; unknown observations stay unknown.
- `ENGINEERING_PLAYBOOK.md`, Fail loudly and explicitly / Test layers: preserve the primary failure and use deterministic independent expectations; prove marker-detector sensitivity before trusting absence.
- `docs/decisions.md`, Approved scope decisions / Selected choices: no public transport platform is selected.
- `docs/status.md`: named revision-bound checks do not promote a runtime cell, production provider, release, or any full gate.
- `INHERITED_REVIEW.md` retains the independent source-only review verbatim. Its proposal is narrower than a complete cleanup-message transport guarantee.

## Independent test expectations

The new focused module contains 17 statically enumerated cases; this is not a collection result.

1. Fresh KeyUnavailable: exact class, code, operation ID, args, stage, remedy and none/True defaults.
2. Three downgraded classes: KeyUnavailable, CryptoBackendUnavailable and nonretryable CryptoFailure must restore literal unknown/False. The base class independently detects lost effects even though its retry default is already False.
3. Two fresh class-specific failures: ProtectedSchemaMismatch retains transaction_requires_rollback; FileCustodyUnavailable retains its complete existing static effect text. No new vocabulary replaces either.
4. Four separate synthetic attachments: notes, cause, context and provider_data. Positive controls prove serialized-byte and rendered-marker sensitivity. Each original attachment is observable, then absent from serialized bytes and restored render/state. Notes, cause, context, traceback and unrelated state remain absent after restore.
5. One attached object raises if reduced or rendered. The exact cleanup pair must survive without touching it. This detects a generic instance-state merge.
6. Six non-whitelist combinations: True, integer zero, a different effect, a string subclass, and opaque effect/retry objects. Restored class defaults remain intact without comparison/coercion/reduction of nonprimitive values.

Tests build their own synthetic exceptions and serialize only locally produced bytes with protocol 5. They do not create an engine, connection, provider, key, database fixture, file custody object, worker process or IPC channel. Importing the existing modules remains a future execution step. The unchanged repository test admission still requires dual-role database probes through the guarded lab wrapper; no direct-pytest bypass is proposed.

## Deliberate remaining limits

- The suite does not exercise a cleanup branch. The inherited async tests own proof that real cleanup code sets the downgrade.
- Cleanup notes and the complete cleanup remedy are deliberately not transported. Original primary args and class remedy remain. A pass supports the machine-readable downgrade only.
- No arbitrary attributes, provider data, notes, causes, contexts or traceback are added to transport state.
- Existing args/code/operation-ID behavior is unchanged. This correction does not sanitize arbitrary host mutations of those intentionally transported fields.
- Other externally mutated effect/retry combinations and arbitrary subclass constructor/accessor contracts remain outside this preservation claim. Existing class-default fallback remains; it does not establish safety of arbitrary host modifications.
- Pickle remains unsafe for untrusted input. This patch does not create an input-validation boundary.
- No application retry behavior, provider custody, physical database outcome, connection quarantine, host logging policy, multiprocessing start method or broad framework qualification follows.
- The async candidate, its packet, the authoritative checklist, the original 15-commit mailbox, credentials, database state, Git objects/refs and remote state were not modified.

## Preparation record

Only shell file reads, source-text inspection, exact copying, source/test editing, SHA-256 calculations and byte comparisons were used. No Python process, package import, test collection, test execution, database access, network action, install, commit, push or graph tool was run. No secret files or raw phase JSON were read. There is no Git metadata in the inherited candidate, so no Git repair or repository-status execution was attempted.

The copied source intentionally excludes `.pytest_cache`, `__pycache__` and `.pyc` runtime artifacts. Every one of the 217 inherited source files matches the inherited manifest. Only the approved runtime reducer differs in GREEN. Both test copies are byte-identical. The original mailbox hashes match the preparation snapshot. `PREPARATION_STATUS.json` states the evidence limits; `PLAN.md` and `PROPOSED_COMMANDS.txt` require coordinator review before execution.
