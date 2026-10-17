# Column projection V1: independent executable source review

Disposition: ACCEPTED SOURCE for separately selected bounded no-DB recording-connection execution. No target code was imported, compiled or run during review; no SQL, DB, installation or product mutation occurred.

Packet recovery-work/column-projection-inspector-v1-20261017.
Seven-member SOURCE.sha256 seal84efbe48cf42f4e0159976feb2059e0c19cf240733e61bfabbcdf4331fbc96b5.
column_projection.py9951eeced91064fb16cf75a476a383573797ab342fc29e5f5bc800c5ce867252.
projection_cases.py0921394c6c2b66ffbbc9ca64905f4c1f6ba161eafefeb8a2d89d4b54c3f451a8.
run_module_diagnostics.pyacfa61d4b29063c8115895e188e668a6c71fb72d2e8045862d5ecaf60320168d.
Seal and all seven member hashes independently verified on stable ordinary files.509 dependency map, integration manifest486f900e78cf426f33a5fba71a8d4e992657572c5af10254ec7602c0c707ae5d and materialization receipt0c5d736ee47de25f3e97b8665349db39644da5480c6b1e13d2a98b1a0d2976b2 are byte-identical to accepted forward-progress V2 controls. Current complete560-file admission remains mandatory at launch.

## Inspector

Exact list/dict/string/int/bool domains and exactly14 column members match accepted design and producer-expression addendum. Attnum must be exact int strictly above previous starting0; gaps allowed. Names are unique exact strings. Typmod is canonical signed ASCII decimal checked lexically, never via int conversion; no digit/numeric cap is introduced. Required and independently nullable optional strings, nullable exact deterministic bool, exact nullable bool and lowercase64-hex optional digest are checked. The f-string collation expression exactly preserves the schema=None/name='x' synthetic 'None.x' branch; empty name produces None. No guessed catalog join consistency, text-sort comparator, enum or native integer range is added.

All outputs are frozen/slotted constant scalar classifications with metadata_validated=false,current_native_verified=false,successor_authorized=false and no references to inputs. Errors contain fixed codes only. The inspector performs no filesystem/native/catalog work, changes no caller input and is not wired into operational product code. Empty columns are structural shape only. All relation/index/constraint/dependency/guard validation and operational recovery gates remain outside this slice.

## Deciding cases and independence

Static count is39 independent outcomes:seven positives and32 fixed-code negative mutations. Positive cases cover actual producer full literal output, empty columns, literal projection, zero typmod,5000-digit lexical typmod, dotted/non-ASCII collation, and empty-name f-string branch. The full producer fixture contains negative/positive typmod, attnum gaps, nullable/nonnullable columns, deterministic None/true/false, exact default digest and synthetic None.x. The5000-digit string is accepted only as lexical shape, with no native typmod or transport claim.

The32 negatives cover missing/extra/raw default members, attnum bool/zero/negative/string/float/duplicate/decreasing order, duplicate name, seven invalid typmods, nullable/deterministic integers, default digest length/case/type, incorrect collation, invalid optional/required strings, four scalar/container subclasses and outer list-subclass/tuple rejection. Each expects exact ColumnProjectionError, fixed code/args and preserved input. Cases continue on ordinary exceptions; BaseException interruption cannot count as success. Source mutants are described only as future work, not executed evidence.

Actual migration._facts calls its real compiler._schema_facts alias, then _read_schema_facts/_rows, using real SQLAlchemy TextClause construction and the real canonical digest/transform helpers. Runner captures and rechecks each producer function's object identity and exact source filename. No helper is replaced or stubbed. SHOW search_path='pg_catalog' intentionally takes the direct catalog branch; savepoint restoration/cleanup is not tested.

Independently compared all six literal SQL expectations against the pinned producer source with the same whitespace-only normalization: relation, columns, constraints, indexes, dependencies and relation-name query all match in order. The recording connection checks TextClause exact type, one SHOW, exactly six selected queries, and exact expected parameter dictionaries. Fresh mapping copies prevent product row-pop transformations from mutating fixture input. No method delegates to a database/driver.

The full five-key stripped expected output is an independent literal, recursively compared with exact types, dictionary members and array order. It requires removal of oid/default_expression/raw definitions/_relation_names and checks transformation output rather than merely calling the inspector. Three hardcoded digest oracles were independently recomputed with inert standard-library JSON/SHA256 analysis: default expression aa805bd3892e01f40d355746bff61d6565c2d46f3be3de9c405a22fb606ec12b; constraint91251caa3d3adf0df8d5b09bcc5c50ae3dd55f9164d03f2116034ae228f1fdcd; index27a316aba6adcd2e3832a862b1ed9d926b8b10f43d0a9afbcd284f4d5c7de93d. All differ from hashes of the raw expression/SQL text. Runtime expected values are never derived from the product helper.

Fixture output preserves NULL expression-index slots and NULL dependency columns. Deliberately non-Python-sorted dependency order proves only preservation of supplied synthetic order, not that PostgreSQL emits that order under any selected collation. The None.x row likewise proves expression compatibility rather than a possible/authentic catalog join. Positive calls assert frozen false-flag results and input preservation before clearing separate input copies to check no retained mutable references.

## Runner/launch scope

Diff from accepted forward-progress V2 changes only packet/local-module bindings, producer identity checks, case dispatch/count and report labels/third false flag. Existing finite audit/origin/V9 closed native/proxy/postcase semantics remain unchanged. Product remains actual combined222v2 runtime43 leaves, dependencies509, controls7+seal, total560. Output remains256KiB, all39 PASS/no primary/full closure/cache absent required.

After external admission, root may select the existing exact Python3.12 with only LANG=C.UTF-8,LC_ALL=C.UTF-8,TZ=UTC,PSYCOPG_IMPL=binary; cwd the absolute V1 packet; -I -S -B -X pycache_prefix=<packet>/bytecode-absent; absolute runner; combined; seal84efbe48cf42f4e0159976feb2059e0c19cf240733e61bfabbcdf4331fbc96b5. Existing60s wall/2s grace,30s CPU,1GiB virtual memory,512KiB file,core0/stdin-dev-null envelope is adequate proposed scope. Root must read back/admit host/limits and preserve packet/host/patch/review before-after evidence even on failure.

Trusted same-host stdlib/native-loader and native OpenSSL initialization remain explicit. Python-observable guards are not a native syscall sandbox. Passing this test cannot establish PostgreSQL semantics, catalog authenticity, owner/ACL/fence/current-native truth, transaction consistency, complete nested-metadata validation, historical reconstruction or destructive/successor authority. Earlier accepted68-case progress evidence is preserved and need not be repeated.
