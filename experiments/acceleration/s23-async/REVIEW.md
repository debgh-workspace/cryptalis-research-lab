# S23 async extension source review R2

Date: 2026-10-14. Reviewer: Agent 1. Source and saved-data review only. No tests, test collection, database, Git, credentials or raw environment-bearing receipts were accessed. Canonical source and authoritative checklist were not edited.

## Decision

No blocking code defect found for the bounded native differential campaign. Execution is not authorized by this review. Root must accept the review and retain the canonical S23 candidate routing below. The UUID SCOPE.md sentence directing runtime source to its nested source directory is not a valid wrapper instruction and must not be followed. The wrapper and admission rules must remain unchanged.

## Exact scope and source identity

- All 213 frozen manifest files match both candidate-s23-planning-20261014 and the UUID source copy. Every UUID packet pin and all nine warm-mapper preparation pins match.
- The original S5 ledger SHA-256 is 9df455d63a89a0cb1cc4e6ee22bfdd0e3b50c2899187265bf3a8081bccebe971. The S23 target missing inventory exactly matches it.
- The UUID plan is exactly its missing 30 keys: uuid-text/{get,equality,in}/{canonical,upper,hex,braces,four_groups}, mode async, SQLAlchemy 2.0.51 and 2.1.3.
- The warm plan is exactly its missing 16 keys: warm-mapper/warm_mapper_{insert,update}_{1,3}_{text,varchar}, mode async, the same two versions.
- These are additive cells. The historical 159 IDs/554 executed cells and 82 missing combinations remain historical facts. If all 46 new keys later verify, 36 other historical gaps still lack new evidence. STATIC_AUDIT.json enumerates every exact key.

## Oracle assessment

UUID: real native and protected async engines run sequentially with the same fixed UUID and value. A fresh query session prevents get() from succeeding by identity-map reuse. Each branch asserts exact UUID/str types, canonical identity and plaintext. The public before_cursor_execute event checks that the caller's original spelling reaches the driver. Exceptions and refusals cannot count as IDENTICAL. The receipt remains DEFECT until both engines and fixture contexts close. This is strong bounded value/type/bind evidence. It does not independently decode stored frames, measure leakage, or prove general authentication/security properties; canonical-row authentication here is exercised through the existing protected read path.

Warm mapper: native/protected arms share input IDs, tenant, C collation, seed rows and values. The actual async INSERT path is warmed with flush/rollback; UPDATE is warmed with commit. Attachment retains the used registry and engine, with no private cache manipulation. No application session spans maintenance. The awaited post-commit SELECT compares every returned row, and a separate CF1 decoder checks each protected changed row with its exact tenant/record context. Refusal, mismatch or exception fails. The warm receipt is emitted only on success; absence must be treated as missing/failed, never inherited success. ID/tenant values are string-normalized, so this harness does not independently establish exact Python UUID types or full ORM-state parity. This matches its finite historical row-value scope.

Both harnesses use public application/runtime APIs. Names _row and _async_factory are frozen local test helpers, not private SQLAlchemy hooks. Their inspected implementations use public async_sessionmaker/create_async_engine/attach. The warm maintenance helpers use the existing public migration and attachment operations. Sync schema fixtures and independent sync verification are explicit; the compared application operations are async. There is no concurrency, SQLModel, implicit-default, async-DDL, cancellation, performance or production qualification claim.

## Preserved admission and privacy boundaries

The canonical, copied and original scripts/test_postgres.py files are byte-identical (SHA-256 118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12). Both external conftests match the canonical/original preflight-attestation and failure-redaction conftest (fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd). Async engines disable echo and hide parameters. Static comparison confirms the wrapper's entire subprocess run() function equals the original. Existing exclusive lock, dual fresh-role probes, package-origin guard, candidate-root admission, start/stop and capture/restore remain in force.

Do not read, publish or package tests.json/package-origin.json: the inherited wrapper can include environment data there. The unchanged runner performs its usual read-only revision receipt step during an authorized run; this review itself performed no Git operation. Preflight or lock failure stops the campaign. Never substitute credentials, roots, interpreters, preflight attestations or databases to force a run.

## Routing resolution and evidence requirements

Use candidate-s23-planning-20261014 as --candidate-root for every cell. Do not pass experiments/.../source, make a candidate alias, alter the wrapper, or override PYTHONPATH. Omitting --installed-candidate intentionally selects source-overlay qualification.

Select each experiment directory. For UUID, explicitly ignore its nested source directory; this excludes the copied full suite. The ordinary test naming rules select only the 15-case async module; SYNC_ORACLE_REFERENCE.py is not a test filename. The warm directory contains only its 8-case async module. Passing the directory lets the existing wrapper archive/hash external conftest.py and the UUID fixture sources as well as the test module. An explicit canonical pyproject.toml makes the pytest configuration unambiguous. No collection was executed in this review.

PROPOSED_COMMANDS.md contains four exact serialized commands. Interpreters exist and installed METADATA identifies 2.1.3 and 2.0.51; this is a static check, not a fresh runtime identity claim. Each evidence directory was absent during review. Run one command, inspect safe receipts and stop/isolation status, and only then consider the next. Never reuse an evidence directory or run xdist/background jobs.

Before crediting results, bind all 213 source pins and external manifests; require 15 or 8 expected testcase outcomes per version, no failures/errors/skips, exact unique receipt keys, successful fresh-role probes, package-origin verification through approved safe extraction, source stability, PostgreSQL stop and corpus restoration. Preserve any failure and incomplete receipt set. The historical reconciler does not ingest these two new filenames/formats; keep them additive and require a separately reviewed result reconciliation rather than modifying the 554-key baseline. All seven production gates remain UNKNOWN.
