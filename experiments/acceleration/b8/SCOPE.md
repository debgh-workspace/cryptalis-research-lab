# B8 inactive payload re-encryption preparation

## Proposed private implementation boundary

One private function, `cryptalis.crypto._payload_rotation.prepare_payload_rotation_batch`,
will accept an immutable tuple of `(record_id, current_frame)` pairs, one trusted
field descriptor and tenant, explicit already-prepared source/target keys, and
row/byte bounds. It returns an immutable tuple of the same identities and newly
sealed CF1 frames only when the complete batch succeeds. It does not publish a
policy, write SQL, call a provider, mutate inputs, or create a new crypto format.

The source must match the explicitly selected active payload/search generations,
even when its reader inventory includes other generations. Domain, tenant,
field/record contexts remain exact. Source and target payload generations and
payload root identities/material must differ; the selected search generation,
root identity/context/material remain exact. CF1 search terms must stay exact.
The source and target prepared-key PID/lease checks remain in effect before,
during, and after preparation. No source lease is renewed or extended here.

Forward and compensating transformations can use the same inactive primitive
with explicit source/target inputs. This is not authority to activate either
generation or accept an old deployment pin. Historical backup frames and readers
remain unchanged. Product runtime admission is untouched.

The explicit limits are at most 5,000 rows and at most 1 GiB logical bytes per
batch. Per-call defaults match maintenance tuning: 1,000 rows and 64 MiB. Reject
duplicates and unbounded iterators. Logical accounting is source frame + target
frame + decoded UTF-8 + 16-byte tenant + 16-byte UUID or 8-byte bigint record per
row. NULL has only identity bytes. Account prospectively before decryption; CF1
source/target representation overhead is unchanged. This is not an RSS, provider,
driver, network, or whole-operation resource guarantee.

## Finite gate

The test file contains 35 cases: eight frozen source/reference target vectors;
eight codec/profile NULL/empty/Unicode and exact-byte-bound cases; nine binding
or late authentication refusals; four PID/mid-batch-expiry cases; five shape,
generation and limit refusals; and one genuine native current-data staging and
transform-back oracle.

The frozen source vectors are checked against the unchanged independent RFC8452
reference implementation before using that implementation to compute expected
target bytes from the observed fresh nonce. The native case independently
decodes all target rows using the existing public-fixture decoder. It separately
maintains plaintext-native reference rows, includes post-protection update,
delete and insert, then transforms a later inactive-target edit back. It proves
current-value transformation, not rollback by an old snapshot.

Native staging/reference tables are test-owned and inactive. Source table,
journal and catalog snapshots must remain unchanged. There is no database
representation switch, new principal, credential, role handoff, external pin,
or live provider. Local deterministic public fixture roots are the only material.
Recorded trigger-catalog facts do not include guard-function body bytes.

Initial RED gate, coordinator only:

```text
-q tests/test_payload_rotation_preparation.py::test_frozen_source_and_independent_target_vector[uuid-equality-unicode] tests/test_payload_rotation_preparation.py::test_native_current_values_inactive_staging_and_transform_back --tb=short -ra
```

At the initial RED boundary the implementation module was intentionally absent.
The coordinator recorded both cases failing with missing
`cryptalis.crypto._payload_rotation`: 2 FAIL in 0.74 seconds under the unchanged
preflight, stable source and successful shutdown. This is a new-feature TDD
baseline, not an existing-runtime defect. Evidence:
`b8-payload-preparation-red-sa21-20261013`.

The small private implementation is now present and statically compiled. The
test file is byte-identical to RED. All 204 inherited files remain unchanged.
GREEN is pending: run the full new test file plus existing CF1/lease/preparation
controls through the unchanged coordinator PostgreSQL preflight. No tests have
run by this worker.

## Integration path and limits

This is a concrete data-transform building block, not the full rotation goal.
Next integration must bind the original operation, exact source/target policies,
source/desired locks and reader inventory; reuse durable maintenance exclusion
and atomic target rows/chunk journal markers; test real interruption/lost replies
and preserved committed bytes; fully verify current native membership/values,
generations, terms, constraints and metadata; then perform the reviewed
database/external-pin cutover and compensating current-data rollback.

Search rotation stays separate: changed search roots require rebuilt terms and
indexes plus newly sealed authenticated headers, exact query/uniqueness parity
and no mixed-generation uniqueness gap. Rewrap remains the third separate action.
The existing host publication/old-worker termination and reconnect-exclusion
procedure must be selected and tested before active publication. No new permanent
token/trigger authority is introduced. Seven production gates remain UNKNOWN.
