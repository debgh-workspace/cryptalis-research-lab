# Addendum: explicit validation evidence

## Verdict

The separate explicit-check harness removes the observed assertion-optimization defect for the retained component tests. Source/AST inspection and the four supplied execution receipts are mutually consistent: 76 checks pass with optimization flags 0 and 1, and both deliberate wrong-output controls fail with `AssertionError: Output mismatch` before recording a passed check. This is evidence about these separate component-validation runs, not a repair of the original timing provenance.

Important environment distinction: every new receipt records **cryptography 50.0.0 / pyca OpenSSL 4.0.1**, whereas the original correctness evidence records **cryptography 50.0.2 / pyca OpenSSL 4.0.3**. Native OpenSSL remains 3.5.7 and native source/binary hashes match. Do not describe the new validation as using the original pinned Python package/backend environment. The launch path is the resolved runtime interpreter, not proof of a newly qualified virtual environment.

## Read-only checks

The independent `inspect-explicit.py` script performed 33 passing checks, retained in `explicit-addendum-checks.json`. It parsed source as data, calculated hashes and inspected JSON. It did not import or execute the candidate, tests, generated harnesses or launcher.

- `validate_direction_explicit.py` and all four `generated_explicit-o*.py` files have no AST Assert nodes.
- Each generated `main()` is AST-identical to the original `main()`: all original test cases are retained.
- Every generated file equals the original test source with only the intended replacements: explicit exception-based output/refusal checks, the wrong-output control branch, optimization/style receipt fields and separate evidence destination.
- O0/O1 positive receipts contain precisely the original 76 check labels in order, PASS status and matching flag values.
- O0/O1 negative receipts contain FAIL status, zero checks and precisely the expected AssertionError type/message.
- All four execution records have the expected exit codes; command combinations cover normal/-O with and without the negative-control argument.
- Receipt source/binary/fixture hashes match current bytes. All files observed by the original audit remain byte-identical.

## Pin enforcement and limits

Manual launcher control-flow review confirms that fixed native source, native binary and original test-source SHA-256 values are checked with explicit if/raise statements before `runpy.run_path` can execute the generated file and import the native extension. Existing output receipts and generated files are rejected explicitly rather than via assert. The AST guard rejects remaining Assert nodes before generating/running the replacement file.

Those pre-import pins belong to the launcher. The generated files themselves retain the original direct native import and do not independently enforce the source/binary pins if invoked directly. The supplied launch records point to the launcher, so this is a direct-invocation limitation rather than a discrepancy in the recorded path. The launcher does not pin the pyca package/backend or fixture bytes before execution; the receipts identify those afterward. Hash checks do not provide atomic protection against concurrent file replacement, reproducible-build proof or signed execution attestation.

Negative controls demonstrate that an explicitly incorrect comparison is caught even under -O. They are not ciphertext-corruption tests or proof that every test failure path was independently exercised. Original coverage gaps, provider assumptions and source-only memory-safety limits remain.

## Unchanged disposition

The original AUDIT.md and frozen measurement remain unchanged. The numerical audit still supports only internal arithmetic/schedule/hash consistency and satisfaction of the recorded experiment-selection rule. The original run's missing optimization provenance is still missing. There was no timing rerun, no benchmark-environment qualification and no CF1/product admission. Any future same-environment validation should be separately labeled and preserve both prior evidence sets.

## Subsequent separately preserved pinned-environment validation

The later `validate_direction_explicit_pinned.py`, four `generated_explicit-pinned-o*.py` files and corresponding receipts were also inspected without execution. `inspect-explicit-pinned.py` reports 34 passing source/AST/hash/receipt consistency checks in `explicit-pinned-addendum-checks.json`.

This second launcher adds an explicit cryptography 50.0.2 / OpenSSL 4.0.3 version check before native import and retains the source/binary/original-test pins. All four receipts report those expected oracle versions, native OpenSSL 3.5.7, Python 3.12.14, correct optimization flags and matching fixture/source/binary hashes. The original 76 test cases remain AST-identical in the generated `main()` functions. Normal and -O positives report 76 PASS; both wrong-output controls report exactly zero passed checks and the expected AssertionError. Recorded commands use the virtual-environment interpreter path without resolving it to the underlying runtime executable.

This establishes separately recorded, assertion-independent component-validation evidence in the expected package/backend version environment. Version strings alone do not qualify the whole environment or prove reproducible builds. Generated direct-invocation pin limitations and all original coverage limits still apply. The earlier 50.0.0/4.0.1 results remain preserved as distinct evidence, not relabeled. Neither new series supplies missing optimization metadata for the original frozen timing or changes its arithmetic-only review verdict.
