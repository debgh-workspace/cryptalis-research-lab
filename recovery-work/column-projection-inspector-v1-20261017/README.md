# Isolated column projection inspector and producer recording binding V1

Source-only implementation. No target import, test, native initialization, DB,
SQL execution, build, Git or combined222 source change was performed by worker.
Design review NESTED-METADATA-DESIGN.md SHA256
54e8e7f46f28dccfbe437c0ada55ff0c4e2f90c4801e7189f02b57271f67cf9b
plus PRODUCER_EXPRESSION_ADDENDUM.md SHA256
a035ba0a4c7513ef86333a34e4ad6d2dfc6e3176c08fee545ba8e9b83f7065c4.

## New inspection scope

column_projection.py accepts exactly the14-member columns projection with exact
built-in containers/scalars, increasing positive attnum with gaps, unique names,
lexical canonical signed typmod (no int conversion/cap), nullable scalar domains,
lowercase64-hex default digests and exact producer f-string collation construction.
Individually nullable synthetic schema=None/name='x' therefore matches 'None.x';
this is expression compatibility, not native join consistency. No text sorting,
enum guesses or identifier/byte/digit caps are added.

Frozen/slotted result contains only a constant classification and three constant
False flags: metadata_validated,current_native_verified,successor_authorized.
It retains no column/catalog reference. Errors contain only fixed codes. No
compiler/migration/progress-inspector callsite is changed; no journal or successor
admission is added. Relation/index/constraint/dependency/guard validation, current
catalog/ownership/fence evidence, complete ordering/transaction truth and raw
transport bounds are still separate and unestablished.

##39 proposed independent case outcomes

Seven positive cases: actual producer chain/full literal output; empty columns;
complete literal projection; zero typmod;5000-digit lexical-only typmod;
dotted/non-ASCII collation names; and empty-name producer branch. The actual
producer fixture also covers NULL noncollatable fields, both deterministic bool
values, negative typmod, visible attnum gaps, default digest and 'None.x'.
The long lexical-only string is not a native typmod or large-integer transfer claim.

32 negative mutations cover missing/extra/raw-default fields, invalid/order/duplicate
attnum, duplicate names, noncanonical typmod text, exact scalar/null domains,
digest length/case/type, false collation and dict/list/int/string subclasses.
Every case is reported independently; all39 must pass plus complete closure.

The actual pipeline calls migration._facts -> compiler._schema_facts ->
compiler._read_schema_facts -> compiler._rows, with real SQLAlchemy text conversion
and real canonical digest/column transformations. A recording connection returns
pg_catalog for SHOW search_path and fixed fresh mapping copies for six SELECTs.
It never delegates to a driver. No product producer is substituted or patched.
The runner captures real producer function/alias origins and rechecks identity.

Literal SQL expectations are stored independently from product source at runtime;
comparison normalizes whitespace only and preserves every non-whitespace token,
query order and exact bound parameter dictionary. Full expected stripped output
is separately literal with exact recursive type/value/list-order comparison,
so bool/int alias equality cannot hide a projection change. Three digest hex
oracles pin SHA256 of these explicit canonical JSON bytes:
- "'seed'::text" -> aa805bd3892e01f40d355746bff61d6565c2d46f3be3de9c405a22fb606ec12b
- "UNIQUE (label)" -> 91251caa3d3adf0df8d5b09bcc5c50ae3dd55f9164d03f2116034ae228f1fdcd
- "CREATE INDEX z_idx ON lab.demo ((lower(label)))" -> 27a316aba6adcd2e3832a862b1ed9d926b8b10f43d0a9afbcd284f4d5c7de93d
They are not derived with the product helper at runtime. Raw definition and
_relation_names removal, NULL index slots, NULL dependency columns and supplied
text-list order are producer plumbing controls, not native metadata validation.
Synthetic reversed dependency ordering is intentional preservation evidence,
not proof a native catalog returned that order. Input copies remain unchanged.

Meaningful future selected mutants: removing attnum-order check loses its named
negative oracles; bool truthiness loses nullable_integer/deterministic_integer;
changing product digest to raw SQL bytes loses full_literal_output. No mutant or
prior68-case progress suite is executed/repeated in this packet.

## Import and preservation boundary

Accepted509-dependency map and V9 finite origin/native/proxy policies unchanged.
Actual43 runtime origins remain combined222v2 source selected by manifest
486f900e78cf426f33a5fba71a8d4e992657572c5af10254ec7602c0c707ae5d and root receipt
0c5d736ee47de25f3e97b8665349db39644da5480c6b1e13d2a98b1a0d2976b2.
New local modules are finite admitted controls with before/after origin checks.
560 preserved leaves:509 dependencies+43 runtime files+seven controls+seal.
Existing same-host stdlib/native-loader/native-init trust is explicit; native
OpenSSL initialization occurs at import. No application/key-provider API, native
SQL, network, subprocess or filesystem write is part of this test child. Python-
observable guarding is not native syscall confinement or vendor provenance.

Root alone selects execution after independent review and external host/launch/
timeout/resource/output/aftercheck admission. Exact four-key environment:
LANG=C.UTF-8, LC_ALL=C.UTF-8,TZ=UTC,PSYCOPG_IMPL=binary. Cwd=this packet; existing
admitted Python3.12; -I -S -B -X pycache_prefix=<packet>/bytecode-absent; absolute
runner path, combined, and SOURCE.sha256 digest. Output bound256KiB; cache absent.
