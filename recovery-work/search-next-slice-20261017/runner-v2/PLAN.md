# New search correctness runner V2

SOURCE ONLY. Root selects any later execution after independent source review and fresh admission. This is a new same-host SQLAlchemy 2.1.3 experiment using the recovered combined221 source and the newly reviewed canonical tenant candidate. It does not restore the lost V2 implementation or run the old 468-case harness. It does not qualify installed artifacts, SA20, PostgreSQL, production custody, independent-host provenance or performance. All broader gates remain UNKNOWN.

## Exact source and dependency scope

The unchanged parent proposal seal is ec7298aa79b41c53326e2aea616bd8e300a138a830da6eaefb98de3640d0d45e. Its independent source review is recovery-work/search-proposal-review-20261017/REVIEW.md. The recovered source's AGENTS.md, playbook, README, architecture, status, security, lifecycle, compatibility, approved decisions and build slices were consulted. Security owns tenant/point verification and no stale cached context; this bounded experiment is not a substitute for prescribed database integration qualification.

Six separate complete 43-file runtime source views are present: baseline, candidate and four deliberate mutants. Each was copied from the exact restored manifest and all donor sizes/hashes checked; only sqlalchemy.py differs by the declared candidate/mutant edits. No tests/conftest or package installation is copied. VIEWS.json lists all exact bytes, sizes and paths. No source view is imported during preparation.

DEPENDENCIES.json binds exactly399 leaves beneath /workspace/scratch/cb28ee9f5f4a/cryptalis-executable/release-lab/cp84-adoption/wheel-venv/lib/python3.12/site-packages. They comprise sqlalchemy266/cryptography79/greenlet32/cffi20/typing_extensions1/_cffi_backend1. The independently compared finite reference inventory SHA256 is004fe92e31130b56e965da4d28d1c608c8905f3227edf41a36e2f17e61b31093. Shared hardlinks with nlink>=1 are accepted only read-only. No package activation, installation, cache body, private credential file or extra dependency is admitted.

The selected trust model is the existing same-host interpreter, stdlib and native loader. Root freshly pins the exact Python executable and source packet before selection. This runner does not regenerate a whole-stdlib map or claim independent vendor/native provenance. Its post-admission Python audit hook limits source/dependency reads to the finite map, permits the explicitly trusted stdlib tree outside site-packages, rejects bytecode bodies and denies file-write, network, process-spawn and common mutating filesystem events. Python audit hooks do not sandbox trusted native extensions or their loader dependencies. Only reviewed known code is selected; no hostile native-code containment claim is made.

## Entry and expected outcomes

One process selects exactly one variant. No runner subprocesses or automatic retries exist. Root supplies absolute HOST executable, -I -B -S -X pycache_prefix=THIS_DIRECTORY/bytecode-absent, absolute run_correctness.py, one exact variant name and the freshly admitted SOURCE.sha256 digest. Cwd is this exact directory, stdin /dev/null and environment exactly LANG=C.UTF-8, LC_ALL=C.UTF-8, TZ=UTC. The bytecode prefix must be absent before and after. No shell script is supplied or implicitly selected. Root must capture stdout/stderr and exit externally with bounded time/memory/file output; proposed per invocation wall60s, CPU45s, VM1GiB and combined capture1MiB. Timeout, signal death, missing terminal JSON or partial closure means HOLD. Root owns termination evidence; this single-process runner has no child ownership to manage.

Order proposed for separate root selection: baseline, candidate, mutant-stale, mutant-tenant, mutant-point, mutant-null. Baseline and candidate require exit0, statusPASS,25 unittest methods, no failures/errors, all448 monitored identities PASS and absent bytecode prefix. They must each satisfy literal expected outcomes, not merely match one another. No sequence is authorized by preparation or source acceptance alone.

The23 original literal oracle rows are copied byte-for-byte from the sealed parent. The new runner concretizes every setup; the Q(B) row also checks the full P(A),Q(B),P(A) sequence. One additional unittest method covers incoming UUID/bytes/object rejection, benign str subclass, captured UUID subclass, bool/float/string versus int record handling, UUID record valid/malformed/wrong-point cases, and both NULL tenancy branches. A second method runs eight real-CF1 combinations: two representations, two record codecs and two tenancy codecs. Each combination requires literal alpha/beta success, cross-tenant rejection, wrong-record rejection, altered-tag rejection, realNULL success, expired/missing/wrong-process material rejection, wrong-policy NULL rejection and independent P/Q/P plaintext results. Method count25 is not represented as25 total assertions or old468-case coverage.

PreparedKeys and _Material are constructed directly from declared synthetic32-byte roots, immutable policy wrappers and bounded process-local leases. WrappedRoot sealed bytes are explicitly synthetic placeholders; no provider is instantiated or called. The test exercises actual CF1 encryption/decryption/context/key-use code with actual native crypto, but bypasses provider preparation and custody. Fixture ciphertext is generated by the admitted sealer; expected text/context/error outcomes are literal, not inferred from generated results. OS randomness for encryption remains the real host operation, not a provider or network call.

## Deliberate mutant interpretation

Mutants are separate frozen source views. They must terminate nonzero with complete closure and the expected specific test failure. Setup/import/guard errors or missing closure are not successful mutant kills.

- mutant-stale removes the identity gate and substitutes rebound self.tenant when old cached text matches. Required failed method: test_literal_rebind_tenant_reject_old. This is the meaningful stale-text bug; deleting identity gate alone while retaining cached[0] would not establish a changed outcome.
- mutant-tenant removes tenant equality while retaining point checks. Required failed method: test_literal_wrong_tenant.
- mutant-point removes point validation while retaining tenant equality. Required failed method: test_literal_wrong_point.
- mutant-null returns None before open_text for realNULL. Required failed method: test_real_cf1_context_matrix, including KeyUnavailable expectations on unusable material. Other observer cases also detect the missing call.

All test failures remain recorded. A mutant's required method may be among multiple failures, but no test errors or bootstrap primary failure may be treated as a valid kill. Real baseline/candidate failures stop dependent correctness acceptance and any benchmark proposal. No timing comparison is performed.

## Admission and final checks

The source seal is verified before parsing. Five controls have a complete metadata pass before their hashes/parses. The selected43 source files,399 dependency leaves and6 controls (SOURCE plus five members) form448 distinct identities. The runner completes full finite metadata admission before expanded body hashing, preserving initial control stamps. Each body uses O_NOFOLLOW and pre/post stable dev/ino/mode/nlink/size/mtime/ctime; ordinary cap16MiB. The host interpreter's larger exact size is admitted by root outside this map.

Finally, every admitted identity receives an independent metadata check, followed by hashing each safely unchanged member; one failed member does not suppress safe later checks. Even an initial import failure records primary stage/type and attempts final admitted closure. The unittest log is capped262,144 characters; terminal JSON contains only fixed scope, method identities and finite closure statuses. Flush or output failures remain nonzero/missing-evidence HOLD. No result file is created. Root must independently join the current file map, complete terminal record, root exit and bounded captures before claiming this limited local correctness result.

Preparation consisted only of literal source edits, inert copying, metadata and hash checks and JSON/text generation. No target import, syntax compilation, test, DB access, provider call, benchmark or source promotion occurred.


## Preserved V1 hold and narrow V2 correction

V1 source16f923ac295fbffcbb7da579ccfd61b73c41b931d347d0865fec1fa8441a116f remains unchanged. Independent source review found that intended mutants can raise a different crypto exception, which assertRaises classifies as a unittest error, conflicting with the no-errors mutation acceptance rule. V2 uses expect_error only around the specific operation being tested. It demands the exact literal exception class; a different Exception or missing exception becomes an assertion failure. Fixture/setup/import exceptions outside that helper remain errors or primary failure. BaseException is not caught by the helper. No expected exception was broadened and no mutation kill is inferred from a setup failure. All other runner logic and view bytes remain unchanged apart from this directory binding.
