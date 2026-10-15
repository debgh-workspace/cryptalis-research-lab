# Cleanup diagnostic transport: source-only boundary review

Date: 2026-10-14. Scope: S25 and the proposed async cleanup candidate. No candidate changes.

## Decision

Do not make this finding a mandatory blocker for integration of the bounded in-process async cleanup correction. The approved architecture explicitly classifies internal transport and diagnostic helpers as INTERNAL ONLY. No public IPC capability, general exception transport guarantee, untrusted pickle input, or cross-process cleanup qualification is admitted by the inspected contracts.

The existing trusted-local reducer does have a source-visible consistency gap when composed with the new cleanup downgrade. It is justified to prepare a separate, small correction and independent test. Do not describe the current reducer as preserving cleanup effects or retry classification. If integration is intended to make that transport claim, the claim must remain blocked until the separate correction and evidence exist.

This is a predicted loss of safe metadata from exact source, not an executed reproduction, observed host retry, physical cleanup failure, or IPC qualification result.

## Exact contract boundary

All paths below are relative to `candidate-s25-async-sqlmodel-integration-20261014` unless otherwise stated.

- `docs/architecture/README.md:23-29,42`: research is not an alternate specification; implementation details do not establish public support; internal transport and diagnostic helpers are INTERNAL ONLY.
- `docs/decisions.md:7-21,30-43`: the approved stack/capabilities and diagnostics choice contain no public IPC admission. Diagnostics reuse existing checks rather than introduce a separate platform.
- `docs/security.md:266-267`: failures have safe identity, stages, retry indicators, effect states and remedies, without raw provider/crypto exception text.
- `docs/security.md:307-326`: failure diagnostics expose retry class and progress; unknown observations remain unknown; existing effects must be reported when cleanup/output fails.
- `ENGINEERING_PLAYBOOK.md:34-50`: preserve the primary failure, keep safe retry/remedy information, and do not equate ambiguity with rollback.
- `docs/status.md:3-8`: verification is limited to named checks and exact revisions. No runtime/production cell or release is qualified; all seven full gates remain unknown.

The explicit transport promise in executable source is smaller: `src/cryptalis/crypto/keys.py:38-43` says trusted-local IPC only and preserves public diagnostic identity, excluding arbitrary attached attributes and the provider exception. The only located pickle test, `tests/test_retained_schema_errors.py:14-24`, checks code, operation ID and effects for `ProtectedSchemaMismatch`, plus absence of cause/context. This establishes an intended local class-specific round-trip invariant in test source. It does not specify general per-instance cleanup metadata transport, and it is not runtime evidence from this review.

Thus the in-process failure contract remains applicable. INTERNAL ONLY does not justify misleading metadata if an internal consumer uses the helper. It does, however, prevent promotion of this observation into an admitted public IPC defect or a new product feature requirement.

## Source trace

1. `crypto/keys.py:23-35` defines `CryptoFailure.effects = "none"` and `retryable = False`; it constructs an operation ID and safe primary args.
2. `crypto/keys.py:69-78` overrides `retryable = True` for `CryptoBackendUnavailable` and `KeyUnavailable`.
3. `crypto/keys.py:38-43` returns the exception type, empty constructor arguments, and a state dictionary containing only `code`, `operation_id` and `args`.
4. In `candidate-next-unblocked-correctness-20261014/src/cryptalis/sqlalchemy.py:1058-1103`, a secondary native exit failure preserves the primary and sets typed primary instances to `effects = "unknown"`, `retryable = False` at lines 1074-1076. Fixed notes describe discard/inspection and possible quarantine failure.
5. Reconstruction through the unchanged reducer invokes the class constructor and restores only its three listed fields. The instance effect/retry overrides and notes are absent. For `KeyUnavailable`, class lookup therefore predicts `effects == "none"` and `retryable is True` after the round trip.
6. The existing schema-mismatch test cannot detect that loss. `src/cryptalis/sqlalchemy.py:77-80` already defines its expected effect on the class, so reconstruction obtains the same value without transporting any instance effect.
7. The proposed `tests/test_sqlalchemy_async_exit_double_failure.py:193-220` checks the original exception object, its in-process unknown/no-retry metadata and safe formatted output. It does not serialize the exception. This is an intentional evidence separation, not a transport test failure.

No proposed or S25 runtime source caller of pickle was found. The reducer and the single retained-schema test are the located trusted-local transport surface. A downstream application's pickle usage was not inspected.

## Smallest independent source/test proposal

Do not edit the frozen async adapter or its integration tests for this follow-on.

Proposed implementation boundary: only `src/cryptalis/crypto/keys.py::CryptoFailure.__reduce__`.

- Retain the existing type/empty-constructor/code/operation-ID/args behavior.
- Add only the known cleanup downgrade tuple to the transported state: an exact built-in string `"unknown"` for effects together with the singleton Boolean `False` for retryable. Emit these as fixed primitive literals, after exact-type/value checks. No string coercion, repr, arbitrary object serialization, generic `__dict__` merge, or custom output hooks.
- Reconstruct ordinary class defaults as before. This preserves existing `ProtectedSchemaMismatch` and `FileCustodyUnavailable` class-level effects without inventing a new effect vocabulary or converting their diagnostic text into a generic field registry.
- This narrow whitelist promises preservation of the package's known cleanup downgrade, not arbitrary externally mutated effect/retry combinations or arbitrary subclasses with new constructor contracts. Unknown host modifications remain outside the stated boundary.
- Do not copy `__notes__`, `__cause__`, `__context__`, traceback, provider objects, arbitrary attributes, or raw provider/secondary text. Pickle must remain trusted-local only; this change cannot make malicious pickle input safe.

Proposed test boundary: one new focused `tests/test_crypto_failure_transport.py`. It should exercise a deterministic serialization invariant without database fixtures. It must not claim to prove that a real cleanup branch reached the downgrade.

Independent planned cases:

1. A fresh `KeyUnavailable` preserves exact class, code, operation ID, args, stage/remedy and the existing `none`/True defaults.
2. A `KeyUnavailable` carrying the exact unknown/False downgrade round-trips with that pair intact. Compare to literal expected values, not just before/after values obtained from the same helper. This is the decisive RED on the current reducer.
3. `CryptoBackendUnavailable` with the same downgrade exercises the other retryable class. A non-retryable base failure verifies effects preservation independently of an already-False default.
4. A fresh `ProtectedSchemaMismatch` retains its class-level `transaction_requires_rollback` classification. A fresh `FileCustodyUnavailable` retains its existing static class effect text. Neither is rewritten to `none` or a new vocabulary.
5. Attach synthetic private markers separately to notes, cause, context and an unrelated attribute. Verify no marker enters serialized bytes or restored rendering/state; verify cause/context/notes/arbitrary attributes remain absent. First prove that the marker detector sees a known marker-bearing control. Do not place the marker in the existing intentionally transported `args` field and then claim that this narrow change sanitizes arbitrary host mutation of args.
6. With the exact downgrade fields present, use an unrelated attached object that would fail or record an attempted reduction. Successful round-trip without invoking that object protects against a future full-state merge. This is a synthetic local object, never untrusted pickle input.

The literal whitelist test should fail if either added field is omitted, or if an arbitrary-state merge is substituted. These are future controlled source-removal checks, not checks run here.

### Deliberate remaining limits

The proposal does not transport cleanup notes or the full cleanup remedy. Primary args and class remedy remain the original safe primary text. Therefore even a passing follow-on must be described as preserving the safe machine-readable effect/retry downgrade, not complete cleanup-message transport. If a transported human-readable cleanup remedy is later required, separately specify a fixed package-owned message derived from the allowed classification. Do not serialize raw notes to obtain it.

No multiprocessing channel, process start method, cross-version pickle compatibility, host logging policy, arbitrary exception subclass, application retry behavior, database cleanup outcome or connection quarantine guarantee is covered. The actual async cleanup source test continues to own proof that the real branch sets the pair. Any future public transport API needs its own admission.

## Inspection record and fingerprints

Read-only source/document searches, line inspection, file comparison and SHA-256 calculation only. No Python imports, test collection/execution, database access, network access, remote action, secret reads or raw phase JSON reads. A Git status probe at the lab root reported that it is not a repository; no retry, repair or Git change followed. Both inspected candidate directories have no local `.git` metadata. Only this owned review directory was written.

- S25 and proposed `src/cryptalis/crypto/keys.py`: `b76d60f32011705726cc73f6211fa52e5624e475fc63573e578aa9e5078aea56` (byte-identical).
- Proposed `src/cryptalis/sqlalchemy.py`: `6a9b7b5a6bf2f16fe254134f228531188ab02dae16201e87c15a6537d07dfa30`.
- S25 `tests/test_retained_schema_errors.py`: `ba7a4869e0017ca0b812bbe1025d0f325ba578e407f948b0a2803166a31fa215`.
- Proposed `tests/test_sqlalchemy_async_exit_double_failure.py`: `b01604d52da66697da025fe2d752b14700d304a3123408bb19b24c8863cf5978`.

All proposed cases are NOT RUN. The reviewed files can change after these fingerprints; conclusions apply to the exact inspected bytes.
