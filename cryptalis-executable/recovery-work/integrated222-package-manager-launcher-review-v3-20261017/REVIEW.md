# Actual generated-launcher smoke accepted

Decision: ACCEPTED_GENERATED_LAUNCHER_HELP. Independently audited the completed root-selected V3 launcher operation without rerunning any target program.

Packet: recovery-work/integrated222-package-manager-smoke-v3-20261017, seal f72906f313f765c2171576e29eaec114b7fbb2bf8250c5868b4f4d6746c424aa. Root capture: persistence-recovery-20261013/integrated222-launcher-v3-20261017-1553. Actual exit.txt and after-exit.txt both contain 0. The required accepted installer review is 4641 bytes, SHA256 8c375cb6177be671ea8c93abd1d5e3ef32a20bb0f5acfff1c87cc46630d6e735, and was included in the finite runtime admission.

## Actual evidence

Guard status PASS_GUARDED_LAUNCHER_PENDING_TERMINAL_REVIEW and inner status PASS_GENERATED_LAUNCHER_HELP_PENDING_INDEPENDENT_REVIEW are accepted here for this narrow smoke. Child exit 0, reason null, leader reaped, empty stderr, no group signals, no cleanup errors, no received signal. The generated receipt has primary null, case --help, exit_code 0, cache_absent true, dependency_imports 0, and explicit os_shebang_tested/path_discovery_tested false.

The actual uv-generated 355-byte bin/cryptalis remains byte-identical to the precomputed launcher, SHA256 3b5b041d24add9b5942ca18bf162ca74a75e793a3844387580790c04f868ae2b, mode 0755. The admitted runner compiles that exact body under its actual filename and supplies --help under the isolated pinned Python. Its successful control flow requires SystemExit of exact integer type and value zero, empty help stderr, the expected usage prefix, description and help text, and cli.main's code filename at the installed cryptalis/cli.py.

Actual help stdout begins 'usage: cryptalis [-h] {manifest,doctor} ...', describes Protection Manifests, and lists manifest, doctor and help. Exactly six product modules are recorded: cryptalis, cryptalis.cli, cryptalis.manifest, cryptalis.manifest.canonical, cryptalis.manifest.header and cryptalis.manifest.parser. Each receipt path is inside this fresh installed target and its digest independently matches the expected map and current body. The admitted runner additionally requires matching module file/spec origins and rejects any other product module or third-party file origin. Other file-backed imports are confined to the explicitly trusted standard library.

## Preservation and effects boundary

Independent metadata-first enumeration still finds exactly the 50 precomputed target leaves and exact directory closure, all regular single-link files with distinct inode identities. All current hashes match: 47 unchanged wheel payloads, the 4217-byte rewritten RECORD, launcher and empty lock. RECORD independently reconciles all 49 unique rows and 48 digests/sizes, with empty self-entry and no lock row. No unexpected metadata or bytecode leaf exists. No forbidden metadata body was read.

All 50 inner preservation rows report both bytes and metadata equal. All 349 outer inputs (345 static and four dynamic) independently rehash to their pinned digests and retain the recorded before seven-field metadata; all 349 after rows are true. The original patch, 222-source candidate, accepted wheel, V2 failure evidence, V3 installation controls and concrete installer acceptance remain preserved. The cold bytecode prefix is absent.

The pinned runner's audit hook rejects writes, mutation operations, subprocesses, sockets and undeclared path reads during target execution. The receipt and preservation checks support the scoped no-effects outcome; this is not an operating-system sandbox or proof of all possible system effects. descendants_verified_absent remains false. Existing-host interpreter and standard-library trust remains explicit.

## Stable receipts

- guard/launcher/run/terminal.json: 177983 bytes, SHA256 5cab56fc63db87466fd97bad2e6e3247a56d92ad12800da23ed26dfb78466121.
- Child stdout: 13090 bytes, SHA256 32134537d2b826cfda5e1cbfb4cb5fbbb3a7104ae3eb099d8a27f3f34972e0e1. This is one GENERATED_LAUNCHER_JSON receipt.
- Child stderr: zero bytes.

CHECKS.json and the independent data-only audit.py retain reconciliation details. This acceptance establishes actual package-manager-generated launcher behavior under explicit Python invocation. It does not establish OS shebang execution, PATH discovery, portable console installation, dependency-complete runtime, database integration, full-suite correctness, production readiness or publication clearance. No target execution, installation, build, database or Git operation occurred during this review.
