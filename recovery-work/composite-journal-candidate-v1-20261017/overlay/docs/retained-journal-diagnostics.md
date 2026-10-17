# Inspect retained journal projections offline

`cryptalis.doctor.inspect_retained_journal(context, state)` inspects an existing,
already-decoded retained journal observation without opening a database. It gives
one safe report instead of requiring callers to inspect progress, columns, other
schema projections and guards separately. No files, JSON bytes, engines, keys or
provider objects are accepted. Existing `doctor()` modes and CLI are unchanged.

The host supplies ordinary decoded containers, kept stable throughout the call:

```python
from cryptalis.doctor import inspect_retained_journal
report = inspect_retained_journal(retained_context, retained_state)
```

`retained_context` has exactly `format`, `kind`, `operation_id`, `models`.
Kind is `protect`; operation ID is canonical lowercase hyphenated UUID text.
Models is a nonempty list of exact objects with `table_id`, `record_codec`,
`schema`: unique canonical UUID table IDs, schema strings and either `uuid16/v1`
or `int64-be/v1`. These are supplied assertions, not authenticated identities.

Supported format strings are `cryptalis.transition/retained-native-research-v0`,
`cryptalis.transition/retained-native-comments-research-v1`, and
`cryptalis.transition/retained-native-comments-cluster-research-v2`. A supported
label does not prove comments/designation inventories survived or authenticate
the profile. This API never invents absent originals, NULL comments or designation.

The report format is `cryptalis.retained-journal-diagnostic/v1`:
- `SHAPE_INSPECTED`: supplied phase-selected state projections were inspected
- `REJECTED_INPUT`: a fixed `component`/`code` identifies malformed local input
- `UNSUPPORTED_PROFILE`: well-typed format/kind/codec is outside this API's scope

Every report has `effects='NONE'`, `authority='ADVISORY_NOT_AUTHENTICATED'`,
`complete=False`, `ready=False`, and `metadata_validated`, `current_native_verified`,
`successor_authorized`, `text_order_verified` all False. Success includes phase,
verification_present and guard_observation_missing. Refusals leave those three
fields None. Fixed limits accompany every result; no raw identifier/SQL/body is
returned. Returned structures retain no mutable input references.

Missing guard member is malformed progress; present `guard=None` is a missing
historical observation and is distinguishable in a successful shape report.
`state=None` is rejected decoded input, not proof of a missing live journal.
ACTIVE/ABORTED snapshots may retain guards that have already been removed; this
API does not require a live guard or establish cleanup. PENDING/ACTIVE/DEPROTECTING
inspect both retained schema and active_schema. ABORTED never invents its previous
phase or an original schema. Existing `_state` refusal rules are unchanged.

Columns and remaining projections share the exact five-key schema object. Native
uniqueness, DISTINCT, text ordering, relational consistency, ownership/ACL,
current guard state, transaction/snapshot truth, provenance, original comments,
native designation and recovery authority remain unverified. No DB or JSON
transport guarantee is supplied, nor concurrent mutation safety or a new size cap.
Unexpected programmer/runtime exceptions propagate and are not successful reports.

This report is not an admission token and must never be used to resume, abort,
rollback, drop objects, authorize a successor or claim a production gate passed.
Unsupported diagnostics do not declare an older artifact unrecoverable. Preserve
original evidence, ciphertext, access and recovery material for separate review.
