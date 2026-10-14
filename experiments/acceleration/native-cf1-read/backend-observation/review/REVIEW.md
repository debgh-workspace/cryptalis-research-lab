# Static backend observation review

Static review: no blocker found for the bounded diagnostic build and 36-case O0/O1 plan. No build, import, native execution, tests, or Git operations performed.

Verified:
- Instrumentation is additive relative to the original C source. Fetch requests, property guards, private refusal labels, term check, cleanup, and queue policy remain unchanged.
- Six observation slots use public method/provider getters after successful fetches, while handles are alive. Strings are copied into call-local buffers; no retained handles or new global observation state.
- Queue fixture installs only 0/1/2 benign ERR_LIB_USER entries without marks. Runner checks exact ordered code/file/line/function/data/flags before versus complete post-call drain, rejects extras, and requires exact bytes or RuntimeError arguments.
- Frozen fetch-stage subsets match the source branches for the 36 declared cases.
- Queue-entry removal and provider-name corruption are downstream comparator controls and must both reject before a success receipt.
- All entries in PINS.json currently match their files, verified through jq and sha256sum. Build is diagnostic-only, has an exclusive build directory, and records command/compiler/linkage/binary pins; result files use exclusive creation.

Nonblocking limits:
- Observation and queue methods are unconditionally exported in this copied source. Isolation therefore depends on the separate diagnostic directory/build plan; this source must not be adopted as a normal binary.
- Provider and method names are truncated to 63 bytes without a truncation marker. Adequate for the expected default-provider names, not arbitrary future provider identities.
- Oldest/newest peeks establish the full pre-call sequence only for the known 0/1/2 fixture. No arbitrary-queue, preexisting-mark, allocation-failure, concurrency, or untested-path claim follows.
- O0/O1 means Python optimization modes; both use the same C -O2 diagnostic binary.
- prepare.py is a source-generation utility, not an immutable replay validator: its assert disappears under Python optimization and its outputs overwrite files. Do not rerun it during the approved build/run.
- Provenance is extensive but not hermetic: compiler/linker environment, transitive tool dependencies, standard-library modules and every system header are not exhaustively pinned. ldd records resolved binary dependencies; it does not itself establish runtime mapping identity under arbitrary loader environment changes.
- No runtime behavior or OpenSSL mark-semantics claim has been independently established by this static review.

SHA256:
- native_cf1.c: 277ce47a7507a53b6aaf9286de2459a6201ea5c2e885f12f4a6e6321ad24d75a
- Original native_cf1.c: 2926d61e43b3dc53a5fff56ab5367982c89b92b146ef9cbc47fbd2b71e5a9469
- run.py: 9fa3e9d3e7a31518bcb4e7e7fe9af7dd91d4694bb1c8d303f38b36d9e00ebd30
- build.py: b74913df0042321c7761aeeaa7d4eac2672fa58c88414d50b1bca41b913fb9ad
- prepare.py: 7035232dc79f72b833704995d791f09c52b821f272630ceb38ef952471157664
- cases.json: 7e47e7128c9eedc4c9bc1595bb8ea71bd1676ca20c2faf5ae26aa58db3e02ea1
- PINS.json: 5fdcbf3b640342adc15fd160e7706e9c455abae084b0ac2c2d3fe3f57df91a83
- SCOPE.md: 30fc7f088bd032a2aa26fc117a57eb5980583804e6219c149f4a45892e3ffbec
