# Independent startup-diagnostic acceptance

Date: 2026-10-15 UTC

Accepted: both retained diagnostic observations exactly match the preselected patterns. This permits preparation of the narrow fixed-locale proof successor for separate review. It does not authorize execution of that successor or convert proof-v1's startup HOLD into a product RED.

Receipt directory: `/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013/doctor-startup-diagnostic-v1`.

## Observations and launch verification

The inspected root launcher explicitly selects the pinned interpreter with `-I -B -S`, the diagnostic's fresh bytecode-prefix path, exact working directory and two fixed child environment maps. It does not inherit environment values for either child. It applies a five-second wait/kill boundary and a 16-KiB regular-output-file limit.

- **Empty map:** selected `env={}`. Actual keys are exactly `["LC_CTYPE"]`; known `LC_CTYPE=C.UTF-8` augmentation equality is true; supplied-map equality is false. Exit is 0, timeout false, stderr empty, prefix absent.
- **Fixed locale:** selected `env={"LC_ALL":"C.UTF-8"}`. Actual keys are exactly `["LC_ALL"]`; supplied-map equality is true; known-augmentation equality is false. Exit is 0, timeout false, stderr empty, prefix absent.

The two stdout files are 110 and 108 bytes. They contain only the planned key names and booleans. No arbitrary environment value is emitted. Both root results report the three diagnostic/review pins unchanged; this reviewer independently rehashed those same three files and confirmed the expected values.

Within these exact invocations, the evidence establishes that empty-map startup adds the known locale entry and that the explicit one-key LC_ALL mapping remains exact. It does not establish general startup behavior on other runtimes or configurations.

## Admitted preparation boundary

Prepare a separate proof-v2 with an explicit fixed `LC_ALL=C.UTF-8` launch input and child exact equality against the same one-key map. Reject all other keys and values. Keep proof-v1, its original empty-environment assertion, its seal and failed receipt unchanged. Keep the product patch, source modules, fixtures, oracles, case inventory, variant relations and dependency boundary unchanged except for the new packet's path and fixed-locale launch/preflight contract. Seal and independently review the successor before any new proof execution.

## Receipt hashes

- Root launcher `/tmp/cryptalis_startup_diagnostic_root_2156.py`: `28e1f0fa1b23a2ffa1ac3a066669348488401c2f2bdc0b17e24b9d538d546726`
- `empty.stdout`: `501b979e1150937a9c67aa565df06034f89a1ea97bb961f74fe7c8a0e0355e5f`
- `empty.stderr`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `empty-RESULT.json`: `c77512ac3b8fdbc8daa9bb10c32ffb594ce4624944fea2f70f6130253be9f628`
- `empty-selection.json`: `cb0f69e7dca804abbd915c674fb5642c504b38685ae5aa05c854911970eafabd`
- `fixed-locale.stdout`: `69b0b7ae024cfd88b7f9b8737e65df1c8d36d9a8a1f8292cf62f983fe71fc294`
- `fixed-locale.stderr`: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `fixed-locale-RESULT.json`: `c77512ac3b8fdbc8daa9bb10c32ffb594ce4624944fea2f70f6130253be9f628`
- `fixed-locale-selection.json`: `c19dcbbf7c25ea84880fdde17f7f238c847091362d3ca65a1c32a39e43e21c34`

The reviewer read source and retained safe receipts only, hashed the listed artifacts, and did not rerun any diagnostic, import project code or inspect an existing environment.
