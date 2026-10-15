# Cluster designation baseline: independent static review

## Decision

The four-case source/oracle design is suitable for one coordinator-selected baseline cell, subject to the launch-freeze and capture conditions below. This is static review only: no collection, test execution, product/test import, database operation, live-environment inspection, corpus access, package installation, network or Git operation was performed. No runtime loss or 2 FAIL / 2 PASS result is established. All full gates remain UNKNOWN.

## Integrity observed

- INPUTS.sha256: 895845c71ad0b613eb6a41e24cb2ea5ab2a4945e240ee95f4af9f22535f8521f.
- All 238 named regular-file pins match current bytes.
- Both manifests contain the same 218 source hashes. Every candidate file matches the transport baseline file byte-for-byte. No extra candidate files or candidate symlinks were found.
- Candidate scripts/test_postgres.py is byte-identical to repo/scripts/test_postgres.py. Packet conftest.py is byte-identical to candidate tests/conftest.py.
- Both proposed evidence destinations are absent, including dangling symlinks, at review time.
- Both selected interpreter links resolve to the recorded Python 3.12 target. No interpreter dependency import or version probe was run.
- The preparation-finalization failure is preserved in the pinned incident files. Historical diagnostic files retain their original bytes; this review changes no historical result.

## Contract and source findings

Reviewed applicable AGENTS, status/evidence limits, lifecycle current-data reversal and removal boundaries, compatibility scope, security/failure requirements, decisions/build slice 6 and engineering evidence policy. The work is a bounded native-metadata preservation baseline, not physical heap ordering, performance, migration online-ness, complete removal or release qualification.

compiler.py inventories index properties without indisclustered, admits the relevant ordinary valid B-tree shapes without rejecting the designation, and retains native definition text but not the designation. migration._switch retires the affected original index or UNIQUE constraint. deprotection._switch recreates those definitions and restores comments without restoring the designation. This supports a suspected omission only; it is not PostgreSQL execution evidence.

## Oracle review

The independent query reads pg_index.indisclustered directly. It also reads the native table/index identities, uniqueness/validity/readiness, pg_get_indexdef, comments and constraint definition/comment/linkage. It uses no product-inspector answer as expected metadata. Constraint conrelid/conindid and index indrelid are checked against the observed table/index identities on each read.

The standalone designated case, UNIQUE-backed designated case, unaffected designated index and undesignated control are distinct. Setup establishes the exact designated set and backing type. Replanning happens after setup and must preserve the entire native observation. Protection retires native_name; unaffected native_label must retain its whole observation while protected. The committed protected edit is read back, and native SQL after reverse must match all original values with only that designated current edit substituted.

At reversal, table identity, full index inventory, native stable definitions/comments/linkage, recreated affected index identity and unaffected identity precede the deciding designation comparison. This localizes the hypothesized omission and does not encode expected failures or xfails. Early errors or different assertions must remain different outcomes. SQL validity and test collection remain unverified.

Only ALTER TABLE ... CLUSTER ON is constructed; no CLUSTER heap-rewrite statement is present. Reversal uses the existing default PLAINTEXT_PENDING route and does not call retire_old_role or plaintext activation/removal. Protection intentionally does call forward.publish to ACTIVE so the committed protected edit is possible. Interpret SCOPE's broad sentence about no activation as no reverse/plaintext activation; the source is authoritative on this distinction.

## Execution-freeze conditions

The packet itself need not change. Add toolchain/lab_progress.py to the coordinator launch freeze: the unchanged wrapper explicitly loads it with -p lab_progress, but INPUTS.sha256 does not include it. Its reviewed implementation writes progress events only; freeze it before and after the run. Freeze the coordinator launcher/capture code too. Recheck all packet pins, types, absent destinations and interpreter targets immediately before invocation. Current absence is not a reservation.

Use exactly one PROPOSED_COMMANDS.json item selected by exact cell equality, retaining its 15-element argv. Pass the JSON list directly to subprocess with shell=False, or an equivalently exact shell array. Do not serialize it through word splitting/eval. No jq expression should consume an argv word beginning with -- as its own option. Record the original selected argv before execution, and preserve complete wrapper stdout/stderr and literal return status even when nonzero. Never use a checked subprocess invocation that skips status/output recording on a normal test failure. Use an exclusive, separate capture destination so the wrapper's required nonexistent evidence destination remains absent until the wrapper creates it.

The wrapper preserves candidate isolation through PYTHONPATH and package-origin checking, requires unchanged preflight, locks the existing lab, snapshots source, starts/stops the existing server, and captures/restores corpus artifacts. Do not manually change lock state or substitute another cluster. Readiness and test execution each go through the fresh dual-role runner. The unchanged runner also uses read-only Git revision lookup for its runtime receipt; no such lookup was executed by this source review.

## Terminal read scope and acceptance

Read only explicit safe receipts/logs needed for readiness, package origin, runner counts, JUnit setup/call/teardown, exact four case IDs, boolean cluster-observations.jsonl, source/external stability, stop status and candidate-corpus-isolation. Do not dump raw phase JSON or environment records. If phase status is needed, extract only explicit exit/status fields with a narrow parser. The wrapper writes internal phase JSON containing ENV: its existence does not authorize broad display.

JUnit owns verdicts; boolean observations are supporting receipts. Require each intended case exactly once and no setup/teardown errors. A 2 FAIL / 2 PASS attribution is justified only if the two affected designated cases reach and fail native_cluster_designation_preserved after every earlier check passes, and the unaffected/undesignated controls pass. Verify postgres-stop success independently because wrapper return status alone is not sufficient proof of clean shutdown. Require unchanged post-run pins and successful corpus restoration. Preserve every nonzero result and inspect it before any later cell, retry or correction. No automatic second-cell run is approved by this review.

## Review process limitations

Commands were source reads and standard-library file hashing/byte comparisons only. No failed shell exit or failed literal assertion occurred in this review. Large read outputs were sometimes display-truncated; the decision rests on the scoped source excerpts and complete packet/test/wrapper reads above, not a claim that every historical status paragraph was re-audited.
