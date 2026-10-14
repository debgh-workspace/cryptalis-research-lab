# Original five-arm S control: source proposal

2026-10-14. SOURCE ONLY, NOT BUILT, NOT IMPORTED, NOT TESTED. No timing admission.

## Exact question and boundary

S retains Python CF1 composition, tuple_bytes, compare_digest, frame validation,
context/policy admission, pre-use resolutions, strict UTF-8/NUL checks and final
resolutions. Four private stateless native operations replace the Python primitive
calls: SHA256, full HKDF-SHA256, AES-256-GCM-SIV decrypt, HMAC-SHA256. No product
file is modified or monkeypatched. Entry point: staged_read.open_text_staged.
Existing seal_text and equality_term remain unchanged and outside this module.

Successful native entry order is sha256, hkdf_sha256, decrypt for storage, followed
by sha256, hkdf_sha256, hmac_sha256 for equality. Each repeated input performs the
same calls anew. NULL performs zero native calls and one active-payload resolve.
Resolution order is payload/search/payload/search for equality and payload/payload
for storage. Search derivation follows successful payload authentication. Term
comparison precedes text decoding; text validation precedes final key resolutions.
The wrapper body is copied from pinned S20 open_text, with only primitive routing
and safe data-stage exception translation changed. Python still builds all six
CF1 tuple values in equality mode (two salt tuples, payload info, AAD, search info,
and equality message). Material context, root identity and generation supply salt,
including older admitted generations; header IDs do not select custody.

Complete-result measurement, if later authorized, must begin before _context and
end after final resolutions and the returned string; result-list allocation belongs
inside the timed batch. Every call has fresh keyed native contexts. No batch API,
cache, keyed capsule, reusable plaintext buffer, retries, fallback, provider load,
provider configuration change, alternate cipher or plaintext-return-on-failure.

S:F measures composition/serialization/FFI packaging as a bundle. S uses the same
explicit provider=default requests, default libctx, and fresh decrypt-only cipher
strategy as pinned F build-03-normal. It does not reproduce pyca's unused encryption
base or copy/reinit path. P:S does not isolate backend. Matched backend attribution
remains UNKNOWN. DECISION-v2 is a proposal, not a selected failure/timing policy.

## Private ABI, fixed before any build

All are METH_VARARGS positional calls, GIL-held, exact bytes only, no user buffer
callbacks. Arity checked before indexing; types checked before sizes/pointers.

- sha256(data): data 0..1024 bytes; returns exact immutable bytes32.
- hkdf_sha256(ikm, salt, info, length): ikm 1..1024; salt/info 0..1024;
  exact int length 1..64 (bool/subclasses rejected); returns exact bytes(length).
  The wrapper always passes length32. Wider private shape admits the independent
  RFC5869 length42 vector without changing CF1 keys.
- decrypt(key, nonce, sealed, aad): exact bytes32, bytes12, bytes16..16MiB+16,
  bytes0..256. Sealed includes tag16. Returns bytes of len(sealed)-16 only after
  authenticated final success and checked returned sizes.
- hmac_sha256(key, message): key1..1024, message0..16MiB+20; returns bytes32.

Out-of-shape private inputs -> ValueError('Invalid bounded private input'); wrong
arity -> TypeError('Invalid private arity'). Diagnostic builds alone export each
name suffixed _fault with one appended exact int selector. Wrong selector type ->
TypeError; unrepresentable/out-of-range selector -> ValueError, both safe constant
messages. Selector0 is no injection. The production research entry points contain
no selectable faults; FAIL expands to zero without S_DIAGNOSTIC. No counters.

## Ownership and release

Arguments are borrowed under the GIL, kept live by CPython's argument tuple. No
input ref is retained. Each primitive allocates a private result, builds fresh EVP
objects and frees them on every exit. Successful result ownership transfers once;
failed result is cleansed then decref'd. Cipher scratch is clear-freed on every
exit; it is copied to the private result only after authentication and size guards.
All outputs are Python-owned immutable bytes. This intentionally introduces
Python-resident salt, derived keys and authenticated encoded plaintext between
calls, as staged Python composition requires. The encoded bytes are internal to
the wrapper until term/text/final-lease checks pass. The private primitive API is
not the application read API. No native function or wrapper publishes a partial
value on failure. Python immutable intermediates, reference cycles in exception
frames, allocator copies, provider internals and registers are NOT claimed erased.
No extra Python del statement could establish that guarantee.

The owned-reference manifest specifies acquisition/finalization obligations, not
measured frees/leaks. Reused F resource observations cannot qualify this changed
allocation order or these four result transfers. A future untimed instrumented
build must observe S-specific ownership; ordinary output tests cannot prove it.

## Observable failure mapping and explicit non-equivalences

All setup, digest, derive, MAC and result-reservation failures -> private backend
-> existing CryptoBackendUnavailable. AEAD AAD/setup failures likewise backend;
returned data/update/final failures and size-guard failures -> data-processing ->
AuthenticationFailed. This is the existing F/S20 observable stage policy, not a
causal discriminator. Invalid term -> RepresentationMismatch; authenticated bad
UTF-8/NUL -> InvalidText; lease/PID faults remain existing KeyUnavailable. Existing
safe class/code/stage/remedy/retryable/effects/operation-ID contract is retained,
with unsafe explicit exception chaining suppressed. No provider error strings or
input bytes enter diagnostic messages.

Native SHA failures are normalized, whereas S20 hashlib salt hashing is outside
its HKDF try; allocation schedule and primitive FFI boundaries differ. Tuple
allocation remains in the same Python catch regions as S20. There is no blanket
API catch. Full allocation/fault equivalence and a stronger causal failure policy
remain HOLD; this source does not select FP1 or override DECISION-v2.

Each native call independently uses F's ERR_set_mark/pop-to-mark pattern for a
preexisting queue and clears only its own initially empty queue on completion.
No blanket entry clear. ERR_set_mark refusal returns backend without starting the
queue scope; pop return is not checked, matching F. No claim of full preservation,
marked-state fidelity, queue-capacity behavior or provider isolation follows.
S invokes this boundary three/six times, not once; independent observation remains
required. Pinned newer F diagnostic supplements are references, not S execution.

## Frozen oracle material and boundaries

ORACLES.json contains literal expected bytes from the unchanged published fixture,
plus literal SHA256 empty/abc standard answers. It never obtains expectations from
S. Eight complete CF1 vectors and six primitive vectors are copied without changing
labels/bytes in reused-fixtures.json. Intermediate calls are explicitly tied to
those vectors, with Python-independent recipe serialization in prepare_source.py.
That preparation script imports only stdlib JSON/hash/path/UUID, never candidate,
cryptography, tests, compiler or subprocess. It is source/oracle preparation only.

S_BOUNDARIES.json freezes direct ABI refusal cases, every one of the 25 declared
primitive fault selectors in valid/fault/recovery triplets, expected private result
and stage, and ownership obligations per stage. These are independent of invoking
S. New-boundary expectations are not inherited from F. The manifest also freezes
complete-read primitive order, public resolutions, safe failures, final-return
expiry hooks and actual-observation negative controls. Baseline direct ABI refusals
are not public API error oracles. New full-wrapper fault/ownership harnesses and
normal/-O executions remain to be written and independently reviewed; these source
files alone are not an executable qualification suite or full DESIGN completion.

Existing full-read admission manifest is pinned only as an applicable public-input
and expected-result corpus. Reusing it requires a new S adapter and independent
review that exact fields, ordered resolutions, full strings/types, no-return and
normal/-O negatives are preserved. No success count from F transfers to S.

## Build/run hold and smallest next step

No build or launcher is supplied to imply permission. Before any execution root
must select scope, independently review these sources/oracles and freeze a direct
ABI harness with provenance checks, actual-output mutation negatives and bounded
process cleanup. Then separately qualify wrapper behavior, ABI/fork containment,
fault/resource ownership, provider/property/queue correspondence and current leak
limitations. Timing additionally requires the original five-arm controls, protocol,
failure-policy disposition and all accepted admission gates. No product adoption,
DB qualification, security review or end-to-end latency claim.

SOURCE_INDEX.json pins the basis and linked-libcrypto hash recorded in F's build
receipt; it does not inspect a freshly built S library (none exists). A future S
build must use the exact F compiler/ABI/flags/header/library pins and verify actual
resolved library bytes, top-level provider identities/properties, and normal vs
diagnostic deltas. Merely matching version text or -lcrypto is insufficient.
