# Additive V11 runtime supervisor derivative

SOURCE ONLY. No execution, syntax checking, target imports, DB operation, Git,
installation or materialization was performed in preparing this derivative.
The sealed V11 packet and all actual output files remain unchanged. The original
packet supervisor is watched as an original input but is not selected to run.

## Fixed binding and selection boundary

- P: /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/tenant-fastpath-no-db-packet-v11-20261017
- Packet SHA256: 7af82fd53dda6564f6d2a670cee43d0dc255ac4798dda1e32d817cfff2938426
- Actual PREPARED SHA256: 0ee0e251481d6bd01e5eda6dbf67e3e568c25ed643570c565c635ae3fdc2f7a2
- Actual ALLOW SHA256: 17413de2a8f341f221355e288b1fef3d0e8f759912d5dfbd0366be93d18cbb17
- Host: /opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12
- D: this exact reviewer-notes/tenant-fastpath-v11-runtime-supervisor-v1-20261017 directory.
- R: D/attempt-001, required absent and exclusively created on a selected run.

PREPARED and ALLOW hashes above were verified from the actual approved controls;
the ALLOW binding is also read from PREPARED. No new output inventory is invented.

Separate fresh external source/tool/bootstrap admission must bind this external
source manifest and supervisor, the exact V11 io_guard, host and 488 stdlib map,
current originals and materialized copies before explicit runtime selection.
Source acceptance is not that admission and does not itself select execution.
The V11 trusted_startup entry list is unchanged: the external derivative uses
the existing module_origins checker with an explicit external-entry exception,
exact P/io_guard, and the fixed-pinned 488 host paths. Native loader and trusted
controller startup remain the same stated boundary, not a sandbox claim.

Exact proposed child-of-root argv is HOST, -I, -S, -B, -X,
pycache_prefix=P/bytecode-absent, D/supervisor.py, the PREPARED digest above,
and the independently admitted SHA256 of D/SOURCE.sha256. Cwd is exactly D;
stdin is /dev/null; environment exactly LANG=C.UTF-8, LC_ALL=C.UTF-8, TZ=UTC.
There is deliberately no runnable placeholder command here. Root must supply
the actual accepted source seal. The source-only launch.sh imposes checked limits
and records outer stdout/stderr/exit in exclusive D/outer-001. It uses a
600-second TERM deadline plus 30-second hard-kill grace, 480 CPU seconds per
process, 1 GiB address space per process, and 8 MiB per-file write limit. The two
outer diagnostic streams together have a 16 MiB ceiling; child streams retain
the tighter combined 2 MiB bound. Outer resource setup must pass explicit
readback before env/timeout/Python launches. Hard-stop evidence is retained.
The shell, env, timeout and mkdir tools must be freshly admitted externally;
their native-loader trust is not established by a successful script receipt.

## Ownership and signal changes

TERM, INT and HUP handlers only record the first signal. They never throw or
interrupt assignment of a newly returned Popen handle. Explicit cancellation
points precede spawn, follow handle acquisition, and run throughout capture and
waiting, before another child, and around final result/terminal evidence writes.

Each child still starts a new session/process group. Its leader is observed
using waitid(P_PID, owned_pid, WEXITED|WNOHANG|WNOWAIT), without reaping. There
is no poll() or wait() before group cleanup. The group is killed/cleaned while
its leader PID is still reserved, then one bounded wait(timeout=10) reaps it.
A previously exited successful leader keeps its original exit status. This
also prevents a live descendant from being left behind when its leader exits.
If waitid reports lost ownership (ECHILD), HOLD and do not target a potentially
reused PGID. Other observation/cleanup/reap failures are retained and fail closed.
SIGCHLD must have default disposition; no competing reaper is selected.

Wall deadline remains 60 seconds per child, with up to 10 seconds for cleanup
reaping; combined stdout/stderr remains at most 2 MiB per child. CPU/address and
regular-file write limits are provided by the separately admitted outer launcher.
No runtime test or failed setup is retried. SIGKILL can prevent final evidence;
missing final evidence or unconfirmed owned-child termination means HOLD.

## Preserved tests, writes and closure

Run order is unchanged: SA20 baseline, SA20 candidate, SA20 reducer, then SA21
baseline, SA21 candidate, SA21 reducer. Exactly four correctness children must
each collect 468 unique cases. Existing DIFFERENTIAL_JSON checks, exact reducer
inputs, unchanged runner/oracle code, hashes, namespaces, and final original/
copied/host checks are preserved. No timing or product-performance claim is added.

Only a future selected run may add the existing results subtree beneath output.
PREPARED, ALLOW, all materialized inputs and sealed packet members are watched,
never modified. This derivative's SOURCE.sha256, supervisor.py, launch.sh and PLAN.md join
the finite monitored map. Initial control stamps precede control parses and
must match the later full metadata-first admission pass. Final observation
attempts each finite metadata entry first, then hashes only entries still safely
admitted with unchanged metadata; namespace and absence categories are attempted
independently. Failure before full admission is marked HOLD/NOT_ADMITTED.

External exclusive BEFORE, INVOCATION, AFTER, CLOSURE_FINAL and TERMINAL receipts
are retained in R, each capped at 8 MiB. Output child receipts retain process
status, cancellation, cleanup ordering and failure classes; their in-memory
ledger is created before output acquisition and updated before output contexts
close. Open/flush/close failures are retained without replacing an existing
primary; final external closure evidence retains the ledger even if a child
receipt write/hash fails. Output/results/CLOSURE_FINAL remains for compatibility.

The final RESULT and TERMINAL claims require successful original/copied/control
closure, all six children/reducers, and no recorded signal. Cancellation is
checked after evidence writes as well as before. A retained success-looking
file never overrides a nonzero exit, recorded signal, missing closure or hard
stop: independent root review must require all matching evidence and exit zero.

## Review and preservation

Review this additive source, SOURCE manifest and exact launch separately before
use. It does not modify V11 admission policy or replace PREPARED/ALLOW. The finite
module inventory still deliberately rejects undeclared namespace/spec-less or
extension-package forms. Encountering one requires review, never guard widening.
Once independently accepted and sealed, preserve this proposal; any corrections
must be a distinct successor. There is no chmod or filesystem immutable flag.
