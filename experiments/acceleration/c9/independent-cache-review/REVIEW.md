# Native bind required/default cache correctness review

## Finding

Installed SQLAlchemy 2.1.3 and 2.0.51 exhibit the same compiler-only order dependence when structurally identical expanding Text binds differ in required/default state. This is an observed correctness boundary, not an upstream novelty or security claim.

The bounded pure compiler probe imports SQLAlchemy and its PostgreSQL psycopg dialect only. It creates no Engine, connection, database, session, or Cryptalis object. It does not inspect environment variables. Its script and exact stdout for both installed interpreters are adjacent; hashes are in SHA256SUMS.

All structural keys for `missing`, `required-default`, and `default-tuple` compare equal. Actual `_compile_w_cache` calls against an in-memory dict show:

- missing first: cache MISS is stored, then construct_params raises InvalidRequestError/cd3x. Both later cases HIT this same compiler and also raise cd3x, including default-tuple.
- default-tuple first: cache MISS constructs tuple values. Later required-default and missing HIT the compiler; required-default constructs tuple values and missing constructs None, without required-bind errors.
- Explicit supplied values construct successfully for every original/incoming bind combination.

The reverse-order None result is parameter construction only; no assertion is made here about driver execution, database rows, or later expansion.

## Installed source mechanism

Paths below are relative to the task root. SA21 prefix is `repo/.venv/lib/python3.12/site-packages/sqlalchemy`; SA20 prefix is `release-lab/s19-removal-boundary-sa20-20261013/lib/python3.12/site-packages/sqlalchemy`.

1. Bind construction infers required=True when no value/callable is given, and False when a value is given unless required is explicitly provided. SA21 sql/elements.py:2076–2077,2117; SA20:1990–1991,2029.
2. BindParameter._gen_cache_key includes identity token, class, type key, bind key, and literal_execute, but not required or default value. SA21 sql/elements.py:2246–2272; SA20:2160–2184.
3. `_compile_w_cache` combines structural key with dialect, column keys, schema-translation presence and executemany state. It stores a newly compiled object before returning it. SA21 sql/elements.py:711–746; SA20:683–727. Thus later parameter-construction failure does not stop that cache entry from existing.
4. `SQLCompiler.construct_params` resolves incoming extracted bind objects positionally but tests the compiled bind object's required flag before selecting incoming value. SA21 sql/compiler.py:2007–2089, especially 2065 then 2080; SA20:1896–1978, especially 1954 then 1969. This is why refreshing incoming values does not refresh required behavior.
5. Engine execution retrieves engine compiled cache by default, invokes `_compile_w_cache`, then initializes execution context; context calls construct_params. SA21 engine/base.py:1630–1684 and engine/default.py:1660–1678.

## Relation to existing C9 evidence

Existing evidence paths:
- evidence/c9-guard-plans-diagnostic-sa21-20261014/{tests.log,junit.xml}
- evidence/c9-default-tuple-cold-cache-sa21-20261014/{tests.log,junit.xml}

Full-module run: missing and required-default pass expected no-cursor error controls; default-tuple fails at native with StatementError wrapping InvalidRequestError/cd3x and zero cursor observations. Because the assertion occurs inside the variant loop, that failed test never reaches original/candidate. Twenty other cases pass.

Isolated default-tuple run: native/original/candidate all return row IDs 1002,1003,1007; native/original use IN and candidate uses ANY. One test passes.

Current test source and both evidence snapshots have identical SHA256: 8ba279202faaec46ab412327c2733e4bb349c285ed5f13600cf779d39f0f2c4c.

The module-scoped apps fixture (test_c9_postgres_gates.py:58–77) retains one engine per variant across parameterized cases. All first three controls have identical SELECT shape, same `needles` name/type/expanding flag, and empty execution params. Their required/default state differs. Session teardown/rollback does not clear the engine compilation cache. The pure compiler evidence therefore supplies a sufficient mechanism matching the actual order-sensitive failure; no database state contamination is needed.

## Other fixture contamination and oracle limits

- native owns a distinct runtime engine and plain sessionmaker (test_sqlalchemy_search.py:73,176–179); only protected variants attach Cryptalis.
- native runs first in each loop. variant('native') is a no-op. The original implementation monkeypatch uses a context manager and is restored on exit (test_c9_postgres_gates.py:37–55).
- cursor observers remove their listener in finally; first three controls attach no state-mutating listener.
- Native tables/mappings are independently constructed per app, not shared across native/original/candidate.
- Protected query path explicitly sets compiled_cache=None before rewrite (src/cryptalis/sqlalchemy.py:1039–1044), and both generated search TypeDecorators have cache_ok=False (src/cryptalis/_sqlalchemy_search.py:14,31). Rewritten bind preserves required unless a supplied parameter makes it False (line 119). Warm native cache and protected per-operation compilation are different cache regimes.
- These facts support native compilation-cache contamination between test cases, rather than original monkeypatch leakage or persisted SQL state. The full-module evidence did not instrument cache object identity directly; the compiler-only probe independently demonstrates the mechanism.

## Test interpretation

Cold-cache/operation-fresh bind semantics and intentionally warmed native-cache order behavior should be separate, explicitly labeled controls. Do not silently present a cache-normalized native run as default-cache equivalence. Do not reorder tests merely to make default-tuple pass: reverse-order compiler evidence shows that this can instead remove required errors. The existing whole-module test remains failed as recorded; the isolated success does not turn it into a complete gate pass.

No DB/Git/runtime-source edits were performed. No tests.json was read.
