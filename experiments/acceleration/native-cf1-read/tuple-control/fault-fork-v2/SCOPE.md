# T fault / after-tuple expiry / actual-fork supplement V2

SOURCE PREPARATION ONLY. No supplement execution, rebuild or timing has occurred.
Existing T direct/full source, freezes, binaries and receipts are preserved.

## Finite scope and independent expectations

MANIFEST.json freezes 88 observations per Python mode and 44 exact P:T parity
pairs before execution:
- 54 observations: 3 storage / 6 equality sites, each P and T valid/fault/recovery.
- 18 observations: after-last-tuple payload expiry in storage/equality, search
  expiry in equality; each P and T valid/expiry/recovery.
- 16 observations: storage/equality × P/T × parent-before, child inherited-key
  refusal, fresh-child success, parent-after.

Both representations use the already frozen public seven-byte text `abcdefg`,
UUID record mode and existing public frame references. No fixture/root copies
or regenerated crypto outputs. Literal success text and exact resolution traces
are drawn from the independent canonical oracle. Backend error metadata is copied
from unchanged S20 keys.py class definitions; raw MemoryError expectations follow
the exact unchanged try boundaries, not a candidate execution.

Six tuple call sites are named by ordinal and checked tag: payload-info,
payload-salt, AAD, search-info, search-salt, equality-message. Storage reaches the
first three. Initial scope/key admissions happen before any of these calls.

P is a separately loaded byte-identical S20 cf1.py module namespace. Its local
`tuple_bytes` binding is routed only during an observation; canonical P is not
monkeypatched. UUID inputs ensure `_record` does not add an int64 tuple call.
T routes only its local `_native_tuple_bytes` binding. All hooks return the exact
immutable bytes object on success. No subclass, plaintext alias or cache.

At each named fault site P raises MemoryError before its original tuple function;
T calls the already reviewed diagnostic binary's `tuple_alloc_failure`, which
validates arguments and returns MemoryError before PyBytes allocation. Calls
before/after the injected site remain unchanged. Payload/search info and root-salt
errors are expected to escape as raw MemoryError with empty args; AAD and equality
message are expected to retain S20's CryptoBackendUnavailable normalization. This
explicitly records existing raw-error boundaries; it does not repair or broaden
normalization. Native validation preceding injected refusal differs from P's
immediate refusal, but these selected inputs are valid exact bytes in both arms.
This does not establish all-allocation equivalence or real heap-exhaustion safety.

Each valid/fault/recovery invocation prepares fresh public material. Counters
record entered/completed tuple calls and exactly one selected fault/expiry hook.
A failed call returns no value; a separately prepared recovery returns exact text.
After-tuple expiry occurs after the last tuple function returns bytes and before
its Python caller continues. This is before AEAD completion for storage and before
HMAC finalization for equality, not F's after-decrypt encoded-result boundary.
Both arms must continue unchanged work and refuse at the same final resolution.

## Actual fork and containment

Four positive fork groups per mode use os.fork after a successful parent read.
The child first uses inherited PreparedKeys and must fail at the first payload
resolution with zero tuple entries, then prepares fresh public keys in its own PID
and succeeds. The parent reuses its still-valid keys successfully after reaping.
PID evidence requires actual child PID == fork return value, different from parent,
and the child's observed parent PID == parent. These relational predicates are
predeclared; PID integers and operation IDs cannot be frozen literal values.

IPC is an anonymous pipe, capped at 65,536 bytes; no credential/provider/database
connection exists. Child errors exit 97 without transmitting arbitrary exception
text. Parent uses a ten-second selector/reap deadline and kills/reaps a failed
child. No grandchild is created. The top-level launcher starts a new process group,
bounds each child at 180 seconds, and requests group SIGKILL plus bounded reaping
on timeout/interruption. These are containment source provisions, not yet runtime
containment evidence. No concurrent caller or inherited live cipher context is
claimed by this fork test.

## Negatives, provenance and stop rule

Ten top-level subprocesses: raw-boundary, tuple-count, trace and actual fork-PID
negative controls, then positive, in ordinary and -O modes. Each negative first
verifies an unmodified record and then mutates the actual record/receipt; exact
error signature is `RuntimeError: Supplement mismatch`, exit 1, no accepted
observations. Fork-PID negative performs one real fork before mutating its receipt.
Thus the frozen full schedule would include ten actual fork children total.

The existing diagnostic binary is pinned; no build is needed. FREEZE.json extends
prior reviewed source/toolchain/runtime/cache pins and adds all supplement files
and diagnostic build artifacts. Exact cache inventories are checked before/after;
no .pyc is modified or removed. Backend stays Python cryptography 50.0.2 / bundled
OpenSSL 4.0.3. Canonical P function identities and T's original binding are checked
afterward. Sources/bytes checks are integrity evidence, not signed attestation.

Stop on any unexpected failure or mismatch; preserve every output, no automatic
repair/retry. Execution requires separate root clearance after independent source
review. Even PASS would not close sanitizers/leaks, actual allocation exhaustion,
all-fault equivalence, code-removal mutants, distribution, full DESIGN or timing.

## V2 containment delta (V1 remains unexecuted and unchanged)

The launcher now reads nonblocking stdout/stderr through a selector, capped at
65,536 bytes each under the 180-second outer deadline. Cleanup requests process-
group SIGKILL, uses at most ten seconds of nonblocking reap polling, captures
secondary cleanup errors and writes the launch receipt even when containment
cannot be confirmed. UNKNOWN terminal state is an explicit failed outcome, never
a clean-process claim. IPC child cleanup likewise uses at most two seconds of
WNOHANG polling after kill; fork-attempt records preserve failures and reaping
limits. The launcher requests group cleanup even after the main child exits to
terminate unexpected residual descendants; no descendant memory state is attested.

Each real fork child performs source/cache pin and canonical/isolated/T binding
checks before its observations and after their hooks restore state, before sending
success IPC and calling os._exit. Parent validates literal PASS guard fields and
PID relations; these are child-reported checks, not independent memory attestation.
No observation/expected-value, error normalization, failure site, schedule or crypto
primitive changed. Equality payload expiry after tuple 3 is NOT covered by this
after-last-tuple slice and remains separate if selected.
