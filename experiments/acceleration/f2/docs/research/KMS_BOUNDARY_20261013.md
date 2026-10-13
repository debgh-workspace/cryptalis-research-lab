# KMS-BOUNDARY-01: offline request/response experiment

Status: research-only, S14-derived, synthetic fixtures. This is not an AWS
KeyProvider, an approved provider profile, or an approved context format.
G-PROVIDER and all other independent gates remain UNKNOWN.

## Purpose and boundary

The current generic KeyProvider contract identifies a provider by UUID. A future
AWS adapter must bind that identity to a caller-approved KMS key and must not
select authority from ciphertext metadata. This experiment exercises the small
request/response boundary before adding any SDK, transport or custody claim.

`experiments/kms_boundary.py` defines immutable `KmsBinding`, `WrapRequest` and
`UnwrapRequest` values. They produce fresh SDK-shaped argument dictionaries and
validate synthetic response dictionaries. The module is outside the installed
`src/cryptalis` package. All 183 original S14 files, including KeyProvider,
Keyring, provider exports, dependencies and build configuration, remain unchanged.

The experiment constructs no client and calls no service. It performs no
credential discovery, grants, IAM changes, retries, fallback, key generation,
async scheduling, rewrap, caching or external publication. Returned synthetic
roots are ordinary Python bytes; no zeroization claim is made.

## Provisional rules, not product decisions

- Caller authority is one nonzero provider UUID and one full commercial-partition
  ARN with an ordinary UUID key identifier. Alias names, alias ARNs and short key
  IDs reject. Syntax and length checks do not establish account, Region, key
  existence, key origin, standard/custom key store, key state or permissions.
- Both request shapes explicitly contain the pinned `KeyId` and
  `EncryptionAlgorithm=SYMMETRIC_DEFAULT`.
- The provisional plaintext context contains a prototype version plus provider,
  domain, tenant, purpose, root and generation. It is tested only with synthetic
  UUIDs. It is not a confidential encoding. Real tenant UUIDs must not be sent to
  CloudTrail under this prototype without a separate owner-approved context
  policy. The existing development-wrap AAD format is unchanged and not reused.
- Wrap roots must be exactly 32 bytes. Unwrap wrappers must match the expected
  provider UUID and complete KeyContext, with 1..6144 blob bytes.
- Responses must contain ordinary string values for the exact expected key ARN
  and algorithm. Wrap accepts only bounded bytes; unwrap releases only exactly
  32 bytes and rejects recipient-mode responses. Additional SDK metadata is
  ignored, never used as authority. SDK dictionaries with custom comparison
  objects are rejected.
- Failures use a fixed `KmsBoundaryRejected` family with no retry and no external
  effects. They do not echo input values. Request representations omit root and
  ciphertext bodies. Argument dictionaries necessarily contain those bodies
  and must not be logged. Host logging remains outside this local proof.

A frozen object is not an authenticated deployment policy. Another caller can
construct a different binding. No global provider-to-ARN registry, process
isolation or persistent identity mapping is established here. A response-shaped
dictionary can lie about its contents; these validators do not authenticate AWS
or prove that a blob was encrypted at all.

## Executed evidence

Direct command, using each existing environment separately:

```sh
PYTHONPATH=src:. /path/to/existing/python tests/test_kms_boundary_prototype.py
```

Both cells use Python 3.12.14, psycopg 3.3.6 and cryptography 50.0.2, with
SQLAlchemy 2.0.51 or 2.1.3. The final 13 unittest methods PASS in each cell.
These are pure experiments, not PostgreSQL, Boto3 or Botocore executions.

The tests cover exact independently written request shapes, every context field,
provider/context mismatches, immutable values and detached argument dictionaries,
strict response identity/types, boundary lengths, and safe representations and
errors. A logging collector first observes an intentionally emitted synthetic
root marker, then observes no output from the exercised boundary operations.
It does not establish comprehensive application/SDK logging hygiene.

Six single-check omissions fail on both cells:

| Omitted check | Failures per cell |
|---|---:|
| Wrapper provider identity | 1 |
| Wrapper expected context | 5 |
| Returned key ARN | 8 |
| Returned algorithm | 2 |
| Returned root length | 3 |
| Returned blob upper bound | 1 |

Exact source restoration passes all 13 methods in both cells. Logs and hashes
are retained in `evidence/kms-boundary/`. The initial missing-module outcome, a
wrong-length synthetic root fixture, and three later response-shape/ARN-bound
failures are also retained. The fixture was corrected without relaxing the
32-byte rule. The later failures required strict response types and an ARN
length bound. None is evidence of a deployed AWS failure.

## Current official source checks

Checked on 2026-10-13 during the preceding research-only assignment:

- [AWS Encrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Encrypt.html):
  symmetric encryption accepts small roots and returns a bounded blob plus key
  ARN and algorithm.
- [AWS Decrypt](https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html):
  explicitly naming the key prevents selection of another key from symmetric
  ciphertext metadata. The encryption context must match exactly.
- [AWS encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html):
  context is authenticated metadata and appears unencrypted in CloudTrail.
- [Boto3 Encrypt](https://docs.aws.amazon.com/boto3/latest/reference/services/kms/client/encrypt.html)
  and [Boto3 Decrypt](https://docs.aws.amazon.com/boto3/latest/reference/services/kms/client/decrypt.html):
  SDK blobs use bytes, without an extra manual base64 layer.
- [DescribeKey](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html)
  returns key properties, but not the policies/grants needed for custody review.
- [Botocore Stubber](https://docs.aws.amazon.com/botocore/latest/reference/stubber.html)
  can later validate actual SDK-shaped requests without calling an endpoint.
  No SDK is installed or tested by this experiment.

Rolling documentation headers are not an SDK version lock. The old AWS profile,
SDK pin, credential topology and retry numbers in the archived research remain
historical, as specified by the research index.

## Remaining decisions and evidence

Before actual adapter promotion: approve the provider profile and versioned
context/privacy mapping; bind authenticated deployment identity to the key ARN;
approve a locked SDK and artifacts; validate actual SDK requests and errors;
qualify client/credential/endpoint configuration, timeouts, retries, fork behavior
and async cancellation. Rewrap remains a separate lifecycle task.

Live qualification also needs specifically authorized account, Region, key,
workload principals and costs, followed by actual IAM denial, outage/throttling,
revocation, recovery, audit and custody observations. No synthetic validator or
SDK Stubber pass establishes those facts.
