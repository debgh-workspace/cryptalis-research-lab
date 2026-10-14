# Generated-setup acceptance: independent post-run audit

Date: 2026-10-14 UTC. Both coordinator-run cells are terminal. Reviewer performed no test, database, project-import, Git, credential, or runtime action.

## Result

The focused V2 acceptance packet passed both planned dependency cells:

| Planned cell | Actual named pytest cases | Result | JUnit time | Console time |
| --- | --- | --- | --- | --- |
| SA21 | sync and async | 2 PASS, 0 failure/error/skip | 0.826 s | 0.82 s |
| SA20 | sync and async | 2 PASS, 0 failure/error/skip | 0.739 s | 0.74 s |

Each runner receipt independently reports exit 0 and exactly two passes in `tests/test_manifest_setup_integration.py`. The JUnit case-name set is exact, with no failure or skip children. Both logs show successful dual-role preflight and server stop. Source-origin logs identify the intended candidate source overlay, not an installed Cryptalis package. Coordinator separately reported wrapper exit 0 and stop exit 0; the audit's safe log observation confirms `server stopped`.

## Exact accepted scope

Each passing case executes all five reviewed shapes natively, performs the unchanged fixture maintenance/publication sequence, executes the exact emitted public setup template, rebuilds all five shapes, and compares the attached results against both native observations and literal UUID/string expectations. Thus each cell contains two modes × five shapes: ten native query observations and ten protected query observations. Across both cells, there are four pytest cases and forty query-result observations. These are not forty independent pytest cases or a count of all underlying driver statements.

The source-bound completed assertions establish, for each mode:

- Two public connection acquisitions emit two checkout events and two engine-connect events, with the same transient DBAPI identity. This is the corrected pooled-connection collector control.
- The separate setup window emits no observed connection or SQL event and leaves mapped table/type identities unchanged.
- The native query-bind observer detects a known string-valued synthetic marker, while the attached query path emits real driver calls without detecting those exact string markers.
- Typed-bound equality, composed/decomposed Unicode equality, expanding IN containing NULL/empty/decomposed values, and empty IN produce the exact expected ordered UUID/string rows.

These statements are inferred from completion of the pinned deterministic assertions in the two named passing cases. The packet does not emit separate per-query or per-event trace receipts. The marker collector does not prove absence of byte-encoded plaintext, arbitrary secrets, or all write-route exposures. Synthetic publication remains host-attested fixture authority.

## Identity and preservation checks

The executed added test is bound in each runner map, wrapper before/after maps, archived source snapshot, and current candidate to SHA-256:

`b851385a2f663e4faff36890efe8420b2b4416f0a0b68aa555f20210cc967b00`

All 213 inherited S23 files still match the authoritative preparation hashes in both the source and derivative candidate. This repeats the pre-run review's equality check. Exactly one additional non-cache candidate file exists: the new integration test. Test execution generated ordinary cache files; those are not source additions or qualification artifacts.

For each cell, the wrapper's 153-entry source/config before and after maps are equal. All archived bytes and current candidate bytes match those entries. All 152 runner-recorded source/test/script hashes also match. The external-source map is empty and stable. These are the wrapper's actual scopes; do not describe its in-run snapshot as an inventory of all 213 inherited documentation/source files.

Each isolation receipt reports no archived output changes, deletions, or errors and successful prior-receipt restoration. All 26 prior corpus files were independently hash-checked in that run's archive and at their current primary paths. No historical corpus outcome was rewritten by this test.

`POSTRUN.json` binds 631 consumed safe files, including source snapshots, runner/JUnit/log evidence, prior corpus archives and both dependency-identity observations. Raw `tests.json`, raw `package-origin.json`, and credential files were not read.

## Dependency-identity limitation

The safe identity files record Python 3.12.14 and SQLAlchemy 2.1.3 / 2.0.51 using the exact planned interpreter paths. Their observations were made at 17:39:28 UTC, before these 17:50 runs, and copied unchanged into the two evidence directories. This audit hash-binds those records. They are pre-run identity observations only; they do not provide during-run import attestation, unchanged dependency-byte proof, or complete installed-environment identity.

## Disposition

The generated-template/native-query composition gap is verified within this focused source-overlay fixture scope. The initial V1 observer HOLD and the V2 correction remain preserved; no earlier execution was reclassified. No full source-suite, installed-package, unrelated application, performance, provider custody, active rotation, online closure, or production qualification claim follows. The seven retained legacy failures and all seven full qualification gates are unaffected.

Coordinator alone decides integration, authoritative ledger changes, and publication.
