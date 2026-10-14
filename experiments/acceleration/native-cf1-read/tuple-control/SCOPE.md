# T tuple-only control: source preparation, not admission

2026-10-14. No build, candidate import/execution, timing, PG, network, installation,
credential use or Git operation was performed. Original source is read-only.
All proposed tests below remain NOT RUN. Only this directory is written.

## Exact integration boundary

`tuple_read.py` copies S20 `_derive`, `_term`, `_aad`, `open_text` verbatim, with
function globals bound to unchanged S20 crypto objects and a private native tuple
adapter. There is no product monkeypatch. `_context`, `FieldDescriptor._record`,
PreparedKeys and all key admission remain unchanged. The nested int64 record tuple
is still made by Python before the six tuple sites; this explicitly excludes that
context-validation operation from T. Seal/query APIs remain unchanged S20.

Successful storage performs three native assemblies in order: payload info,
payload root salt, AAD. Successful equality then performs search info, search root
salt, equality HMAC message, for six total. The search tuples follow successful
AEAD authentication. NULL makes zero native calls (including int64 NULL context,
which retains its baseline Python validation). Python SHA256, full HKDF,
AESGCMSIV object creation/decryption, HMAC, compare_digest, strict decode, NUL
check and all four/two/one resolution traces retain their original expressions
and try regions. Each value repeats this work; no root/derived key/tuple/result
cache or persistent native secret state is introduced.

P:T includes C call overhead, the Python adapter, argument tuple packing and changed
allocation strategy. It does not isolate a CPU serialization instruction cost.
This is source for one missing original five-arm control, not a selection of MP1,
MP2 or any failure-policy decision and not authority to time it.

## ABI and ownership

`native_tuple.tuple_bytes(*parts)` is private, GIL-held METH_VARARGS, no keywords.
Zero through seven exact immutable bytes parts are admitted. Count and lengths
are explicit unsigned 32-bit big-endian fields. Total encoded size is at most
16 MiB + 512 bytes, comfortably covering every admitted CF1 tuple (including a
16 MiB plaintext equality message). This is deliberately a bounded internal
helper, not a replacement public arbitrary-size tuple API. No fixed UUID/header
length checks belong here: context and frame validation remain Python. C only
serializes bytes; it never selects keys or parses a frame or crypto header.

Each input is borrowed only during the call, with no INCREF, decref, conversion,
callback or GIL release. Every type and arithmetic check precedes output allocation
and memcpy. One PyBytes allocation owns the only result; after allocation all
remaining operations are nonfallible stores/copies, then ownership transfers.
There is no cleanup branch with an owned result, no native plaintext scratch,
EVP object, retained input, buffer view or cached secret. The equality message
contains authenticated plaintext as ordinary immutable Python bytes, just as P;
secure erasure is not claimed for these objects or allocator copies.

Private type/bounds errors use a constant ValueError, mapped by the adapter to
InvalidContext without an explicit cause. CPython argument keyword errors are
TypeError. Allocation failure remains MemoryError at the helper boundary. Existing
S20 try regions still decide public wrapping: AAD and HMAC-message assembly are
inside backend catches; payload/search info and salt assembly are outside their
respective catches. Do not add blanket exception normalization.

Diagnostic-only `tuple_alloc_failure` validates all input then returns MemoryError
before the single output allocation. It has no persistent selector. It tests the
refusal branch, not actual allocator exhaustion. Normal source exports no such
entry when TUPLE_DIAGNOSTIC is undefined. Module-initialization allocation failure
is a separate import failure; no plaintext is accepted or returned there.

## Independent finite byte expectations and reusable evidence

`tuple-oracle.json` has 43 literal byte-for-byte expected encodings: all 36 affected
tuple sites across the eight original public vectors, plus seven delimiter/empty/
all-octet cases. Expected bytes were assembled using standalone standard-library
length framing, without importing S20, C, wrapper or cryptography. All eight AAD
values were also checked against the independently frozen public fixture's exact
AAD field. Root-salt tuple inputs are public identifiers/generations, not roots.
No private material or fixture binaries are copied. Public vector, 89 frame,
case-manifest and source references/hashes are in SOURCE_INDEX.json.

The generation procedure is retained as `prepare_oracle.py` for review only.
Its existing outputs must not be overwritten; new evidence needs new names.
The original 1035-case suite and later 1098-case exact-output suite are references,
not fresh T evidence. Future harness must consume frozen expected outputs directly,
including full strings/types, safe error fields and ordered resolution arguments;
it must not compute expected outputs through T or silently inherit F-only hooks.

## Required qualification before any timing

Freeze and independently review build command/compiler flags, Python executable/
ABI and all dependency/import origins; verify S20 and public-fixture hashes before
import. Use the same pinned cryptography 50.0.2/bundled OpenSSL 4.0.3 as P. T has no
OpenSSL linkage or new provider selection; do not silently accept an alternate
cryptography package. Review the copied function bodies and bounded C arithmetic.
Then separately authorize build and correctness execution. The new direct ABI,
refcount and allocation cases in TEST_MANIFEST.json supplement all applicable
DESIGN A–F full-wrapper cases. F evidence does not qualify this new C helper.

For immediate-after-native expiry, there are three/six helper returns rather than
one fused return. Explicitly test expiry after the last AAD assembly before AEAD
and after equality-message assembly before HMAC; all final resolutions must reject
expired material before public return. Also retain before-first and decode/final
boundary cases and actual-fork rejection with fresh child public-material recovery.
Precise instrumentation/hook sources must be frozen before those executions.

Run ordinary and -O explicit checks, supported ASan/UBSan/leak tooling (otherwise
UNKNOWN), and deliberate one-byte tuple corruption, skipped term comparison,
skipped final resolutions and wrong-text negatives. Fault-only/diagnostic objects
must never be timed. No performance result or ABI, refcount, allocation, leak,
platform, fork, cancellation, production security or product-adoption PASS follows
from source preparation. Full five-arm scheduling and all other controls remain
coordinator-owned, pending their own qualification and protocol selection.
