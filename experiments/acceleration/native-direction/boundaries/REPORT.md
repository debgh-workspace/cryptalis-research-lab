# Supplemental native-direction boundaries

## Results

- `optimize=0`: PASS, 44/44 explicit checks, process exit 0.
- `optimize=1` (`-O`): PASS, the same 44/44 explicit checks, process exit 0.
- Deliberate unequal-output negative control: FAIL as intended under each optimization flag, 0 passed / 1 failed check, process exit 1.
- Each of the four receipts confirms the entire original probe directory's file hashes unchanged before/after. The pinned C and extension hashes were checked before any native module load.
- Exact interpreter invocation: `/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/repo/.venv/bin/python` (symlink not resolved). Cryptography 50.0.2 and pyca OpenSSL `4.0.3 29 Sep 2026` are enforced. The native backend reports OpenSSL 3.5.7.

## New coverage per positive run

1. Ciphertext-body corruption independently of tags: plaintext sizes 1, 17 and 4096 bytes, with each distinct first/middle/last body position flipped. All seven mutations preserve the final 16-byte tag. Pyca refuses all seven as `InvalidTag`; native refuses all seven with `ValueError: Native operation failed`. Original native outputs and immediate valid-call recoveries pass (24 checks).
2. A bytes subclass with otherwise unchanged valid contents is rejected in each of four argument positions with `TypeError: Exact bytes required` (4 checks).
3. Positional arities 0, 1, 2, 3 and 5 are refused as `TypeError`; an ordinary valid call works afterward (6 checks).
4. Six valid length combinations match independent pyca encryption/decryption and expected synthetic plaintext: ciphertext-body lengths 16 MiB - 1 and 16 MiB with 23-byte AAD; AAD lengths 16 MiB - 1 and 16 MiB with 31-byte body; both dimensions together at 16 MiB - 1 and at 16 MiB (6 checks). The sealed length is body length plus the 16-byte tag.
5. Two independently valid pyca fixtures just above the declared bound, body = 16 MiB + 1 with short AAD and AAD = 16 MiB + 1 with short body, receive `ValueError: Invalid bounded input`. An ordinary valid call succeeds after each refusal (4 checks). This tests the wrapper's intentional input bound, rather than a malformed authentication tag.

Public synthetic fixtures use fixed repeated data bytes, a fixed public test key, and distinct incrementing public nonces per positive run. No material is printed. The harness uses explicit exceptions, rejects any Python AST `Assert` node in itself, records the actual optimization flag, and refuses to overwrite an existing receipt. Unexpected failures are retained by type without serializing potentially sensitive exception text. Original tests, audit, source, binary and measurement artifacts were read but never edited or rerun by this harness.

## Hashes

- Base C SHA-256: `5933299b46e349cd0e80032fd89beffd797e5ad04230cbfda1d985ef1eca0239`
- Base binary SHA-256: `393cf26a573870a9e7e1d3b12a3196528f9301f840214dbc05d84e1cb37575ed`
- Supplemental harness SHA-256: `659d731b36de4d0e2a3b5f81f130c3028cfcbfc7c4ab03cc59062a1a2cdf0358`

## Scope and limitations

These are bounded ordinary component tests on the owned experiment using only synthetic public inputs. No benchmark, PostgreSQL, product integration, Git operations, provider corruption, sanitizer, allocator-failure simulation or third-party vulnerability work was performed. Neither hashes nor these runs prove source-to-binary build provenance, complete memory safety, constant-time behavior, all possible inputs, provider isolation or product fitness. They do not reconstruct original assertion-enabled execution or change the frozen performance evidence. Pyca and native use different OpenSSL backend versions.

Full outcomes, individual labels, sizes, environment identity, and all before/after base file hashes are in the four `receipt-o*-*.json` files. Stdout/stderr is preserved in the corresponding `run-o*-*.log` files. `run-outcomes.json` records observed process exits and verifier results.
