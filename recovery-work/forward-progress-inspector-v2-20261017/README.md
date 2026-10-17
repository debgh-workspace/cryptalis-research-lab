# Forward progress inspector and actual journal-function binding V2

Source-only implementation in this separate packet. No target module import,
test execution, SQL execution, DB access, build, Git or combined-source edit.
Independent source review precedes root execution selection.

Design: phase-journal-contract-20261017/PROPOSAL.md plus both immutable addenda;
independent design review PHASE-JOURNAL-CONTRACT-DESIGN.md SHA256
ede3f5decc6bc33a4f323e7f00293824da491e591c889f5e0725a2400ac53468.

## Actual new code boundary

forward_progress.inspect_forward_progress checks exact built-in context/state
container and scalar domains, the three fixed forward formats/kind protect, two
record codecs, duplicate canonical table IDs, exact phase/model/member sets,
local scope/counter/cursor invariants and verification membership/digests.
Counts are decoded exact ints with relative inequalities, no artifact2**53 cap.
UUID and signed64 cursors require canonical string forms. Output is frozen/slotted
and contains only a fixed phase, Boolean and fixed classification; it retains no
input mapping or catalog object. metadata_validated and successor_authorized
are always False. No truthy result is used by any operational path.

schema/guard/active_schema member presence is checked, but their VALUES are
explicitly opaque and unvalidated. A structural result must not be described as
a validated journal. Cross-table reachability and exact chunk-size history are
not checked either. Current native cleanup, full catalog grammar, raw JSON,
transfer/allocation limits, target/plan authentication, lineage and external
current authority remain separate. No operational _state/_save callsite changes.

## Deciding integration tests, proposed68 cases

recording_cases.run_cases receives the genuine admitted migration module and
inspector. It calls actual _save into an exact SQL/parameter recording connection,
JSON-decodes emitted bytes, and routes allowed phases through actual _state.
The facade is deliberately synthetic and does not authenticate a MigrationPlan
or DeploymentPin, execute SQL, implement JSONB or emulate commit/rollback.

19 positive cases:14 initial/partial/complete/empty/large-int/signed-boundary
roundtrips, one DEPROTECTING serializer-only shape, one UUID cursor roundtrip,
and all three literal forward profiles. Each checks frozen scalar output,
constant false authority flags and input preservation, then mutates separate
input copies to confirm no retained mutable reference.

40 fixed-code mutation refusals include exact built-in type/subclass checks,
counter inequalities, canonical cursor rules, table/context duplication,
phase/member and verification violations. Duplicate plan-context IDs are not
misrepresented as duplicate JSON-object keys after decoding.

Six actual-_state refusal controls: missing successor ID in existing journal,
ABORTED normal read, ABORTED with wrong pin, ACTIVE under stale pin, DEPROTECTING
forward read, and behind-pin state. ABORTED positive read uses allow_aborted=True
and PREPARED; ACTIVE uses ACTIVE; DEPROTECTING positive inspection uses emitted
serialization only and has its separate existing refusal control. No refusal is
caught and converted into operational permission. Cases continue independently;
any unexpected case exception gets only a fixed failure label. Interruptions
propagate and cannot count as success. All68 must pass with full closure.

The above2**53 positive is one exact finite value, not arbitrary JSON integer,
PostgreSQL numeric or transfer support. The metadata fixtures are explicitly
synthetic opaque surrogates; no native metadata/provenance is asserted.

Meaningful source mutants for a future separately selected test boundary:
- Remove the rows==count check inside the phase-completeness branch: the existing
  incomplete_verified and incomplete_aborted_verified mutation cases must fail.
- Replace exact int type checks with isinstance(...,int): bool/int-subclass
  mutation cases must fail where inequalities otherwise permit the input.
- Remove table-not-in-codecs check: duplicate_context_table must fail its oracle.
These are not executed or included as passing evidence. No pure38/ambiguous22
rerun is proposed. This first boundary is actual _save/_state plumbing.

## Genuine import, origins and preservation

run_module_diagnostics.py retains accepted V9 dependency/native/proxy origin
policy and the exact509 dependency map. Product is read directly from actual
combined222v2 source at recovery-work/integrated222-v2-20261017/source. Copied
composition manifest486f900e78cf426f33a5fba71a8d4e992657572c5af10254ec7602c0c707ae5d
and root receipt0c5d736ee47de25f3e97b8665349db39644da5480c6b1e13d2a98b1a0d2976b2
bind the43 runtime origins. No product source is materialized or modified.
The two new modules are admitted local controls with exact module/function
origins and module identities checked before/after cases. Their import does not
permit other local files: existing finite-open/extension checks remain active.

560-preservation set:509 dependencies+43 actual runtime files+seven controls+
SOURCE.sha256. Trusted existing host stdlib/native-loader/native-init boundary
remains explicit; this is not native syscall confinement/vendor provenance.
Native OpenSSL initialization occurs at import. No application/key-provider API
is called. Recording exec_driver_sql methods never reach a driver or network.

Root launch after review: exact four-key environment LANG=C.UTF-8, LC_ALL=C.UTF-8,
TZ=UTC, PSYCOPG_IMPL=binary; cwd=this packet; admitted existing Python3.12 host;
-I -S -B -X pycache_prefix=<packet>/bytecode-absent; absolute runner, combined,
and exact SOURCE.sha256 digest. Root separately admits host/launch controls,
timeout/resource/output limits and external afterchecks. Child bound256KiB.
No baseline repetition; no production authority follows from all68 passing.

V2 preserves V1 unchanged. Profile positives now use the three independent literal
strings and a separate exact-profile-set oracle. Two additional actual _save
controls use rowcount0 and2, require journal_marker_write_failed with the correct
operation and confirm unchanged input plus exact serialized parameters. Total68:
19 positives,40 mutation refusals,six _state refusals,one literal-set check and
two _save refusals. No inspector/product/origin-policy change or execution.
