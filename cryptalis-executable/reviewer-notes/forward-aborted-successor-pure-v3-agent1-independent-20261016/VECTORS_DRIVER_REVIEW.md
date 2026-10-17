# Independent literal-vector, driver and conditional command review

Verdict: **ACCEPTED FOR THE DECLARED FINITE PURE TEST DESIGN**, subject to every
external admission/selection condition in RECIPE.json. No execution occurred.
No current host admission, runtime selection or actual test result is inferred.

Packet: `experiments/forward-aborted-successor-pure-v3-vectors-v1-20261016`.
PACKET.sha256: `cb4a9487895efb4ad4d780b93099c3e91fb813707b8f2122e4459407ff7aeacd`.
Independently hashed all eight named members and matched the packet:

- driver.py `8da63a02ff623a98186a4096038baf3f48b123888c2262982ffbf1cc98549a92`
- RECIPE.json `b5d71e98b3f82109a48c5188ab50c69c8f400b0702bf0bc2f8590f5ffa7973ae`
- EXPECTED_RESULT.json `cdd87f39c6ada08d1c5ef19c0c4298e600476ccfaf778d35d19e100a2fcd2165`
- VECTORS.json `ca2353e9b501cbd2189079f1855be58b9fcfd2017c66fe7f65fc92344aa69e84`
- COMMITMENT_PREIMAGES.json `1796ab05c1954dee5169c7cbdcd583bb18d976a8cc9673fbf3ae510f56a846e8`
- CASE_ORACLES.json `1ca5eac7e10c4bc46418b267ccdd83512625f4d647757fa43c309ae8b4276267`
- README.md `ed0ab7ab9e3f893d3bfe327236fdf2ac6b0c20f64af07467d6884637bb6ea239`
- INPUTS.sha256 `d6e282e2561babfdc08bfde0e8d40db3427b0f6933b8b490564766b34e4cfcd6`

## Independent oracle checks

Extracted all 25 literal canonical strings as data with jq and independently
hashed their exact UTF-8 bytes with sha256sum. Every literal digest matched.
Inspected domain strings, S projection, root references, complete terminal
states, and H1/H2/H3 prior-digest/reference links against the accepted design.
Also independently hashed the literal `{"rows":9007199254740992}`; its digest
matches the separate above-artifact-range integer expectation. No candidate
canonicalizer, hash, constructor, verifier or driver was imported or executed.

Data comparison independently confirms EXPECTED_RESULT's ordered actual values,
IDs, case classes and detachment fields reproduce CASE_ORACLES exactly. The
classification is 38 cases: ten ordinary, 26 exact refusals and two limitations.
The source label examples are intentionally synthetic and not valid historical
producer artifacts. These checks do not establish producer compatibility.

## Driver assessment

- Uses pinned literal vector/oracle files. Its local pin hashing binds artifact
  bytes for test inputs; it does not derive expected commitments through the
  candidate. Candidate calls are limited to the declared finite pure API.
- The 38 generated case IDs are compared in order against the exact oracle, with
  duplicate/count rejection. Static tracing of each mutation reaches the intended
  refusal gate: noncanonical bytes before pin comparison, scope changes before
  policy equality, malformed summary before traversal, prefix mismatch before
  commitment comparison, and ancestor identity during the chain walk.
- Complete return values and refusal codes are compared via canonical data
  encoding, avoiding Python bool/int equality. Unexpected exceptions fail their
  case; they are not accepted as generic refusal evidence.
- Every case snapshots inputs before/after. Returned lineage summaries are
  deliberately mutated after capturing their visible value; aliased inputs make
  the case fail. No xfail, silent dropped case or success from partial iteration
  is present. Completed records survive post-check failure through the bounded
  driver error report.
- The malformed nested-state and conflicting-snapshot examples intentionally
  demonstrate missing premises. Their successful pure result is not native
  admission. All six authority fields remain false in expected successful output.

No correction is required for this finite selection. It does not implement all
questions from the broader TEST_PROPOSAL: size/depth edge campaigns, sensitivity
mutants, genuine historical artifacts, native transfer and complete decoder
coverage remain separate. The README explicitly avoids those claims.

## Conditional command and admission boundary

RECIPE selects the exact pinned Python3.12 host with -I -B -S, no optimization,
one fresh absent pycache prefix, exact driver path, fixed cwd, shell=false and
only HOME/PATH/LANG/TZ. There is no inherited environment merge, package/site
startup, installed-cell dependency path, credential file, database or subprocess
action in the driver. It reads the five explicitly pinned application inputs
and emits stdout; stdlib startup is separately admitted.

The driver is not its own admission framework. Before interpreter startup root
must perform the existing metadata-first canonical regular-file/parent admission
for the host, all 472 stdlib files, final vector packet/seal, original source
packet/seal and reviews. Reject symlink routes, unexpected names and absent-route
collisions; verify exact bytes/hashes before use and again after completion.
The immutable recipe's null admission/selection fields remain truthful. Future
acceptance belongs in a new external receipt, not edits to this sealed packet.

Root must independently enforce the 10-second timeout and 128 KiB combined
stdout/stderr bound. The driver's 64 KiB rendered-report bound is additional,
not a substitute. Preserve partial streams and actual timeout/overflow/exit
status without automatic retry. Whole-report equality, complete ordered cases,
exit0, empty stderr, absent prefix and all external post-admissions are required;
the driver's exit status alone does not prove complete output delivery.

The module-origin inventory checks membership only. Actual stdlib identities
come from external pre/post admission; built-in/frozen code from host identity.
Skipping the two named CPython typing class namespaces is not permission for
other nonmodule aliases. Neither mechanism proves continuous loaded-code
identity, race freedom, native-linker closure or supply-chain provenance.

The prior component review and all native/decoder/authority holds remain in
force. This report establishes static review of exact source/data/recipe only.
No command, import, collection, runtime test, DB/status/ACL, installation, Git or
publication action was performed.
