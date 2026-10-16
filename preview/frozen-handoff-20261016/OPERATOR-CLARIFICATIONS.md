# Frozen preview: current operator clarifications

16 October 2026, 04:12 UTC. External documentation correction for source manifest40c9787c974d38e030ace0b985ffb8a78de76196b28afea071a511eb7bd132e7. Frozen product and historical guides remain unchanged. These clarifications are source-reviewed; they are not new runtime results or permission to perform an operation. Public end-to-end smoke remains unexecuted and all seven qualification gates UNKNOWN.

## 1. Before protection or reversal cutover: drain snapshot holders as well as writers

Alongside actual exclusion of every affected writer, arrange an authorized cutover window in which other account-bearing transactions holding snapshots in this database can finish or roll back. This includes read-only repeatable-read/serializable transactions, exported snapshots, server-side cursors and account-bearing background workers, even when they do not access protected tables. Idle connections without a snapshot need not be disconnected. The library checks this barrier at switch; a planning result or maintenance-approval record does not prove it. If `other_database_snapshots_active` occurs, keep writers stopped, preserve the original operation/artifact and staging, have the responsible operators finish or roll back the relevant transactions, inspect actual progress and current external authority, then resume the same operation only within approval. Do not bypass the guard, delete the journal, terminate sessions without separate authority, or blindly replay business writes.

This is a database-wide snapshot-holder condition, not a requirement to disconnect every open connection. The guard can refuse after earlier staging/backfill transactions have committed. Preserve actual progress; do not assume the operation had no effects. Existing source tests cover this boundary; no tests were rerun for this clarification. This does not establish near-zero-downtime migration or continuous quiescence.

## 2. Prefer the current attach procedure over the older packaged walkthrough

Use [the public quickstart](https://github.com/debgh-workspace/cryptalis-research-lab/blob/d952c505a4666266019e32f27c77f93edd5151ca/preview/docs/source221-v4/QUICKSTART.md), together with these clarifications. The frozen source's docs/walkthrough-sqlalchemy.md contains an older alternate example that omits deployment authority after product protection. Use:

```python
from cryptalis.sqlalchemy import attach

sessions = attach(
    mapping, runtime_engine, lock=p.lock_bytes,
    keys=tenant_keyrings, deployment=(p, active_pin),
)
```

Supply the exact approved plan and its current authoritative ACTIVE pin. Missing or stale authority must remain a refusal; do not fabricate a pin to bypass the check. Await attachment for AsyncEngine. This does not enable default async SQLModel, which retains its documented refusal; the separate optional38 evidence used a private laboratory profile.

## Optional static declaration check after an approved installation

Use the same approved Python interpreter/environment that installed the exact current wheel. The supported module entrypoint is `python -m cryptalis`; the installed console equivalent is `cryptalis`. The static command takes a declaration filename, whereas the Python `doctor(...)` API takes declaration bytes.

Supply an approved local copy of [manifest.example.json](https://github.com/debgh-workspace/cryptalis-research-lab/blob/d952c505a4666266019e32f27c77f93edd5151ca/preview/docs/source221-v4/manifest.example.json), or your separately reviewed declaration. The wheel does not install that example or create `protection.json`. `/APPROVED/manifest.example.json` below is a mandatory local input substitution. Run in an approved output directory; the two report paths are new output files.

This is an unexecuted command template, not installation or smoke authorization:

```sh
if python -m cryptalis doctor /APPROVED/manifest.example.json --json \
    >doctor-report.json 2>doctor-error.json; then
    doctor_status=0
else
    doctor_status=$?
fi
case "$doctor_status" in
    3) printf '%s\n' 'Declaration report produced; qualification remains incomplete.' ;;
    2) printf '%s\n' 'Rejected declaration or invalid input; inspect both output files.'; exit 2 ;;
    4) printf '%s\n' 'I/O or output unavailable; inspect available diagnostics.'; exit 4 ;;
    *) printf '%s\n' 'Unexpected doctor exit for this frozen candidate; stop and investigate.'; exit 1 ;;
esac
```

Exit 3 is the expected result for a valid static declaration: `complete` and `ready` remain false. Do not use `&&` or an unguarded `set -e` invocation to interpret it as exit-0 success, and do not ignore every nonzero result with `|| true`. A readable rejected declaration produces its JSON report on stdout with exit 2. Invalid arguments and file-open/read failures report on stderr; missing/inaccessible input is normally exit 2, while unavailable I/O/output is exit 4. Empty stderr therefore does not prove declaration acceptance.

The static doctor subcommand accepts `doctor PATH [--json]`; setup, database, roles and ciphertext inspection require the separately documented explicit host API and its approved inputs. This command does not establish database readiness, perform migration, or grant any authority.


## Evidence and scope

- Snapshot-holder omission: migration-operator-order-static-20261016/REVIEW.md; independently accepted by SNAPSHOT_DRAIN_OPERATOR_ADDENDUM_REVIEW_20261016.md.
- Alternate attach walkthrough: freeze-orm-attach-handoff-independent-20261016/REVIEW.md.
- CLI onboarding/exit semantics: frozen-cli-dx-independent-20261016/REVIEW.md.

Use the current handoff artifact hashes and installation prerequisites. No software bytes, SQL behavior, security checks or approval requirements were changed by this document. All34 final objectives remain active.
