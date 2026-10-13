# Finite independent CF1 decode prerequisite

Verified 2026-10-13 14:25 UTC. This is an offline research derivative of frozen
D1. All 186 inherited files remain byte-identical in both trees. Product source,
crypto/wire format, frozen vectors, provider contracts, D1 tests and its passing
evidence are unchanged. No database or Git action was performed by this worker.

## Existing work reused

`tests/reference_cf1_vectors.py` already supplies an independent RFC8452 reference
using system OpenSSL AES blocks and stdlib HKDF/HMAC. It supports signed bigint
identities. The unchanged eight frozen CF1 vectors include INT64_MIN and -42,
UUIDs, both existing representations and both tenant modes. Published primitive
vectors and locally frozen CF1 vectors are separate kinds of evidence.

The maintenance-test `independent_open` decoder assumes UUID `record.bytes`.
It cannot serve as D1's bigint decoder without an independently checked extension.
It remains unchanged. The new `independent_cf1_decode.py` performs its own strict
signed `!q` identity encoding, tuple writing, framing, stdlib HKDF/HMAC and context
binding. It imports no Cryptalis helper or decoder. Only the library AES-GCM-SIV
primitive is shared with product decoding. All supplied root bytes are the fixed
public fixture roots; no credentials, provider instance or new provider profile
is introduced.

## Executed offline gate

Command, from this candidate:

    ../repo/.venv/bin/python experiments/verify_independent_cf1_decode.py \
      --receipt experiments/cf1-oracle-receipt-20261013.json

Result: 196 explicit checks PASS; one expected record-binding omission is
detected, followed by passing restored refusal. Total verification 1.237 seconds.
These are pure oracle assertions, not 196 PostgreSQL tests or new product cells.

- Existing published primitive/reference checks reproduce all eight frozen CF1
  vectors, including every recorded intermediate byte.
- Eight frames decode exactly and preserve typed identity bytes and SQL NULL.
- Twenty additional reference-generated vectors cover INT64_MIN+1, -1, 0, 1 and
  INT64_MAX across storage/equality and the two existing tenant forms. Together
  with the frozen vectors, these cover both signed extrema and negative values.
- Wrong row/tenant/field/domain/table/digest, payload/search root and generation
  pins, tag/flag/length changes, and implicit/out-of-range identities refuse.
- The negative row-context control fails when expected row binding is omitted
  in memory; the function is restored and the correct refusal passes. No source
  file is mutated for this control.
- Source/reference/frozen bytes remain unchanged; no Cryptalis or database
  module is imported. The receipt records versions, hashes and exact checks.

## Boundary and next prerequisite

The decoder uses a test-supplied exact descriptor, tenant and root/generation
pins. A frame cannot choose a provider, fetch keys, or broaden that pin set.
This is not a supported decoder API, generic untrusted-input parser, key provider,
custody review, lease model or independent human cryptographic review. Shared
AEAD-library failures remain a common dependency. SQL NULL presence, same-context
replay freshness and row-set completeness do not follow from authentication.

No CF1 frames have yet been attached to D1's capture/claim/install paths. A later
separate finite fixture would need exact expected operation/context pins, actual
use-time key expiry and failure atomicity, and this independent full decoding
comparison after scheduled writers stop. Retain the full final comparison.
That work must not rewrite D1 or silently reuse its test count as CF1 evidence.

Product integration remains blocked on D-REV-04's capture/enumeration and phase
contract, D-REV-09's actual host authority/fencing, and D-REV-07's workload/pause
budgets. Proposed FENCED_READY and ACTIVE_VALIDATING states remain proposals.
No runtime capture admission, online migration or production qualification is
claimed by this oracle prerequisite.
