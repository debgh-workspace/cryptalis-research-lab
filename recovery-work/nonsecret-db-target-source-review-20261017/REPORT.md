# Nonsecret existing PostgreSQL target tuple

## Recovered source facts

The existing ordinary setup source cryptalis-executable/toolchain/provision_lab.py is5,983bytes/SHA256f08b2a9d5ba6a6a6ed60717530513009c417604f876cc5e60535185868e28852. It identifies the historical lab target without reading credentials or generated cluster configuration:

- Line14: PORT=55432.
- Lines41–43: generated configuration selects listen_addresses127.0.0.1 and disables Unix sockets with an empty unix_socket_directories. The runtime/socket directory created earlier is therefore not a configured connection target. Line87 explicitly describes loopback TCP only after filesystem socket rejection.
- Lines64–68: both cryptalis_lab and cryptalis_native are created. That alone does not identify which one the preflight uses.
- Lines76–77: .cryptalis-test-url belongs to cryptalis_owner; .cryptalis-test-runtime-url belongs to cryptalis_runtime.
- Line80: generated URL expression fixes host127.0.0.1, PORT and database cryptalis_lab for these role/file pairs. The full credential-bearing expression is intentionally not reproduced. Only whitelisted nonsecret tokens were emitted during inspection.

Thus the source-supported two preflight tuples are:
1. TCP127.0.0.1:55432 / database cryptalis_lab / role cryptalis_owner.
2. TCP127.0.0.1:55432 / database cryptalis_lab / role cryptalis_runtime.

cryptalis_native, lab_admin, cryptalis_writer and cryptalis_unauthorized must not be silently substituted. They appear in provisioning for other purposes.

run_baseline.py (3,905bytes/SHA256a88c24fa1699ce42a091c9d2da1168ba453d4548a811d542316fe95cb833d00f) lines14–21 binds BASE to cryptalis-executable, RUNTIME to BASE/runtime and child HOME to RUNTIME/home. This connects the setup role/file mapping to the unchanged helper's Path.home-based URL loading. It is ordinary source evidence; neither URL body has been inspected.

## Authority and provenance limits

CRYPTALIS_BUILD_CHECKLIST.md lines23 and34 retain mandatory unchanged role preflights and exclusive coordinator serialization for the existing cluster; separate cluster/credential approval remains pending. Its line230 explicitly says never run against another database or bypass the private dual-role preflight. RECOVERY_STATE.json retains fresh_cluster_credential_approval=PENDING and historical stopped/coordinator execution records. These support continuity of the existing-lab route, not a new connection grant from this worker.

The current owner task explicitly authorizes this source-only search and root separately requires a fixed approved local target before any connection. No exact original owner message approving the literal tuple was recovered in this bounded pass: direct owner-message search was not available among the present tools. The tuple is source-supported historical setup intent, not proof of current secret-file contents, current server configuration, effective role privileges, endpoint listener identity or renewed execution approval.

The accepted focused archive RECOVERY_MANIFEST was searched for an exact /toolchain/provision_lab.py mapping and none was found. Therefore this report does not invent archived hash provenance for the surviving setup source. Its fresh stable source hash and finite input metadata are recorded in INPUTS.json; root can decide whether this source plus retained existing-lab instructions supplies the required target contract. A separate proof of actual connection identity remains necessary at any later selected run.

## Effect on the pending preflight design

The missing nonsecret tuple is now concretely recovered. Future admission can require exactly127.0.0.1,55432,cryptalis_lab and the ordered owner/runtime roles above, with no hostname resolution or Unix socket fallback. This does not discharge the remaining parser/default/option, credential-derived-output and private-file-access constraints. A real admission wrapper must reject any mismatch before calling the original connection function, rather than rewrite a different URL into the allowed target. Both genuine helper SELECT1 calls remain required. No start, lock acquisition, network call, source execution, configuration/credential/cache/environment body read or mutation occurred here.
