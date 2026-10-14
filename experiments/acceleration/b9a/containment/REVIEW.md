# B9A containment R2

Status: staged only, not promoted; no PostgreSQL execution or product imports. Root owns review, promotion, database tests, wrapper/server lifetime, and result interpretation.

Promote only `tests/test_payload_rotation_journal.py` from this directory after review. No extra runtime helper is required. The unchanged frozen source SHA-256 is `5e8db1d91ed20cfd2856d2107d2969eea091f5340e2abc3e897941d8091c322e`; staged R2 is `2cca51e7f8e16a2f420c093c46361a7fb2258557f1170fe68e53d2bc342d8027`. EVIDENCE.json records file/result hashes. R2.diff is the complete change.

## Precise changes

- Linux bootstrap uses the existing C10 PR_SET_PDEATHSIG/SIGKILL pattern, then checks the expected parent before importing the experiment. Every worker/probe starts a fresh session and owned process group. No preexec_fn is used.
- Binary, unbuffered, nonblocking pipes replace text readline and communicate. One monotonic deadline covers each read or completion. Both stdout and stderr are drained; aggregate output is capped at 65,536 bytes for the entire worker, including the barrier. Newline splitting preserves any trailing receipt bytes. Malformed receipts, stderr, and nonzero exits produce fixed diagnostics without exposing child contents.
- Worker groups receive SIGTERM then SIGKILL even when the direct child already exited, with finite direct-child waits and pipe closure on every cleanup path. Completed workers also undergo backend-terminal observation in finally. Child-setup failures clean up the newly launched group.
- Each database worker gets a fresh public `b9a-worker-<uuid>` identity. PGAPPNAME is set for clarity; the actual worker psycopg creator supplies application_name explicitly, so a URL setting cannot override the identity. No credential URL is logged or changed.
- Terminal observation uses an isolated contained child with the existing owner URL and only read-only pg_stat_activity SQL, matching exact backend PID or unique worker application_name. Its connect and statement/lock deadlines are explicit; the parent's bounded raw-pipe reader also covers driver import, connect, query, and shutdown. This is new test code for root to execute; it has not been executed here.
- Root explicitly approved an isolated harness abort on inconclusive backend termination. After finite group cleanup, it emits a fixed sanitized UNKNOWN diagnostic and exits pytest with code 86 before the base application contextmanager can DROP SCHEMA. Normal pytest summary is intentionally lost on that path; schema/failure evidence is retained and the unchanged outer wrapper owns server stop. This is never a cleanup PASS.
- The fixture only adds a worker registry, leaving its existing schema setup/teardown implementation untouched. The busy-worker release becomes one checked nine-byte raw-pipe write. No test selectors or parametrization changed: 12 functions, 16 expanded cases. All substantive feature oracles remain unchanged; no impossible same-term/different-plaintext case was invented.

## Executed controls

`timeout 30s python test_containment_fakechild.py` passed 12 cases using Python stdlib only. The script AST-loads only named containment functions and constants; it never imports the integration module, product, psycopg, or any database fixture. Fake children have CRYPTALIS_* and PG* environment variables stripped. Its controls cover silence, partial line deadline, partial EOF, malformed receipt, completion timeout, stdout limit, stderr drain/limit, withheld stderr diagnostic, coalesced receipts, SIGTERM-ignoring descendant cleanup, direct-child parent death, and the exact exit-86 diagnostic before a simulated teardown finally. See fakechild-results.txt. Staged Python and the isolated probe string were syntax-compiled only.

## Unproved controls and limitations

- Real worker tag visibility, pg_stat_activity permissions/behavior, database backend terminal observations on both successful and failing integration paths, query/network timeout behavior, and the wrapper's actual server-stop behavior after exit 86 remain UNEXECUTED. Root must review then run them.
- The parent-death control proves the direct bootstrap child is killed on coordinator death in this Linux environment. It is not generic descendant parent-death containment. Product workers are not expected to spawn descendants. Group cleanup after an observed failure does signal descendants; fake coverage establishes the demonstrated process shape only.
- SIGKILL/wait is a finite cleanup attempt, not proof that arbitrary uninterruptible native/kernel tasks terminate. Failure cannot produce an integration PASS; the dedicated exit path retains UNKNOWN.
- Existing native_snapshot/source/catalog operations and the base fixture's normal queries are not newly deadline-bounded. This patch addresses worker transport and backend cleanup, not whole-suite boundedness. The external coordinator remains necessary.
- Existing explicit successful SIGKILL test observations by backend PID remain, and finally also checks the unique tag. No unrelated PostgreSQL sessions are terminated; no pg_terminate_backend or pg_cancel_backend is used.
- Other frozen review limitations, including authenticated value-comparison causality, stronger authority drift, no-attempted-DML, aggregate transport budgets, and comprehensive output confidentiality, remain unchanged.

No roles, credentials, clusters, databases, product modules, base fixture files, wrapper files, dependency installs, or Git state were changed. All writes were restricted to this review directory.
