"""Populated synthetic producer observations; no native consistency inference."""
from copy import deepcopy
from types import SimpleNamespace
from dataclasses import FrozenInstanceError
import hashlib

SQL = (
'''SELECT t.oid, t.relkind, t.relpersistence, t.relrowsecurity, t.relforcerowsecurity,
 t.relhasrules,
 EXISTS(SELECT 1 FROM pg_catalog.pg_inherits h WHERE h.inhrelid=t.oid OR h.inhparent=t.oid) AS inherited,
 EXISTS(SELECT 1 FROM pg_catalog.pg_trigger g WHERE g.tgrelid=t.oid AND NOT g.tgisinternal) AS user_triggers
 FROM pg_catalog.pg_class t JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
 WHERE n.nspname=:schema AND t.relname=:table''',
'''SELECT a.attnum, a.attname AS name, ty.typname AS type, ns.nspname AS type_schema,
 a.atttypmod AS typmod, NOT a.attnotnull AS nullable,
 a.attidentity AS identity, a.attgenerated AS generated,
 co.collname AS collation_name, cn.nspname AS collation_schema,
 co.collisdeterministic AS deterministic, co.collprovider AS provider,
 pg_catalog.pg_get_expr(ad.adbin,ad.adrelid) AS default_expression
 FROM pg_catalog.pg_attribute a JOIN pg_catalog.pg_type ty ON ty.oid=a.atttypid
 JOIN pg_catalog.pg_namespace ns ON ns.oid=ty.typnamespace
 LEFT JOIN pg_catalog.pg_collation co ON co.oid=a.attcollation
 LEFT JOIN pg_catalog.pg_namespace cn ON cn.oid=co.collnamespace
 LEFT JOIN pg_catalog.pg_attrdef ad ON ad.adrelid=a.attrelid AND ad.adnum=a.attnum
 WHERE a.attrelid=:oid AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum''',
'''SELECT co.conname AS name, co.contype AS kind, co.condeferrable AS deferrable,
 co.condeferred AS deferred, co.convalidated AS validated,
 co.conrelid=:oid AS outgoing, co.confrelid=:oid AS incoming,
 n.nspname AS schema, t.relname AS "table",
 ARRAY(SELECT a.attname FROM unnest(co.conkey) WITH ORDINALITY k(num,pos)
 JOIN pg_catalog.pg_attribute a ON a.attrelid=co.conrelid AND a.attnum=k.num ORDER BY k.pos) AS columns,
 ARRAY(SELECT a.attname FROM unnest(co.confkey) WITH ORDINALITY k(num,pos)
 JOIN pg_catalog.pg_attribute a ON a.attrelid=co.confrelid AND a.attnum=k.num ORDER BY k.pos) AS referenced_columns,
 pg_catalog.pg_get_constraintdef(co.oid) AS definition
 FROM pg_catalog.pg_constraint co JOIN pg_catalog.pg_class t ON t.oid=co.conrelid
 JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace
 WHERE co.conrelid=:oid OR co.confrelid=:oid ORDER BY n.nspname,t.relname,co.conname''',
'''SELECT t.relname AS name, i.indisprimary AS "primary", i.indisunique AS "unique",
 i.indisexclusion AS exclusion, i.indnullsnotdistinct AS nulls_not_distinct,
 i.indimmediate AS immediate, i.indisvalid AS valid, i.indisready AS ready,
 i.indislive AS live, i.indisreplident AS replica_identity,
 i.indnatts AS total_columns, i.indnkeyatts AS key_columns, am.amname AS method,
 i.indpred IS NOT NULL AS partial, i.indexprs IS NOT NULL AS expression,
 ARRAY(SELECT a.attname FROM unnest(i.indkey) WITH ORDINALITY k(num,pos)
 LEFT JOIN pg_catalog.pg_attribute a ON a.attrelid=i.indrelid AND a.attnum=k.num ORDER BY k.pos) AS columns,
 ARRAY(SELECT DISTINCT a.attname FROM pg_catalog.pg_depend d
 JOIN pg_catalog.pg_attribute a ON a.attrelid=d.refobjid AND a.attnum=d.refobjsubid
 WHERE d.classid='pg_catalog.pg_class'::regclass AND d.objid=i.indexrelid
 AND d.refobjid=i.indrelid ORDER BY a.attname) AS dependency_columns,
 ARRAY(SELECT ns.nspname || '.' || op.opcname FROM unnest(i.indclass)
 WITH ORDINALITY k(num,pos) JOIN pg_catalog.pg_opclass op ON op.oid=k.num
 JOIN pg_catalog.pg_namespace ns ON ns.oid=op.opcnamespace ORDER BY k.pos) AS opclasses,
 ARRAY(SELECT ns.nspname || '.' || co.collname FROM unnest(i.indcollation)
 WITH ORDINALITY k(num,pos) LEFT JOIN pg_catalog.pg_collation co ON co.oid=k.num
 LEFT JOIN pg_catalog.pg_namespace ns ON ns.oid=co.collnamespace ORDER BY k.pos) AS collations,
 co.conname AS constraint_name, pg_catalog.pg_get_indexdef(i.indexrelid) AS definition
 FROM pg_catalog.pg_index i JOIN pg_catalog.pg_class t ON t.oid=i.indexrelid
 JOIN pg_catalog.pg_am am ON am.oid=t.relam
 LEFT JOIN pg_catalog.pg_constraint co ON co.conindid=i.indexrelid AND co.contype IN ('p','u','x')
 WHERE i.indrelid=:oid ORDER BY t.relname''',
'''SELECT DISTINCT a.attname AS "column", d.classid::regclass::text AS kind
 FROM pg_catalog.pg_depend d
 LEFT JOIN pg_catalog.pg_attribute a ON a.attrelid=d.refobjid AND a.attnum=d.refobjsubid
 WHERE d.refclassid='pg_catalog.pg_class'::regclass AND d.refobjid=:oid
 AND d.classid IN ('pg_catalog.pg_rewrite'::regclass, 'pg_catalog.pg_attrdef'::regclass,
 'pg_catalog.pg_proc'::regclass) ORDER BY kind,"column"''',
'''SELECT t.relname AS name FROM pg_catalog.pg_class t
 JOIN pg_catalog.pg_namespace n ON n.oid=t.relnamespace WHERE n.nspname=:schema''',
)


RAW = ([{'relkind': 'r',
   'relpersistence': 'p',
   'relrowsecurity': True,
   'relforcerowsecurity': False,
   'relhasrules': True,
   'inherited': False,
   'user_triggers': True,
   'oid': 1234}],
 [{'attnum': 1,
   'name': 'id',
   'type': 'int8',
   'type_schema': 'pg_catalog',
   'typmod': -1,
   'nullable': False,
   'identity': '',
   'generated': '',
   'collation_name': None,
   'collation_schema': None,
   'deterministic': None,
   'provider': None,
   'default_expression': None}],
 [{'name': 'same',
   'kind': 'f',
   'schema': 'z_schema',
   'table': 'incoming',
   'deferrable': True,
   'deferred': False,
   'validated': True,
   'outgoing': False,
   'incoming': True,
   'columns': ['z', 'a'],
   'referenced_columns': ['b', 'a'],
   'definition': 'FOREIGN KEY (z, a) REFERENCES demo (b, a)'},
  {'name': 'same',
   'kind': 'u',
   'schema': 'lab',
   'table': 'demo',
   'deferrable': False,
   'deferred': True,
   'validated': False,
   'outgoing': True,
   'incoming': False,
   'columns': ['z', 'a'],
   'referenced_columns': [],
   'definition': 'UNIQUE (z, a)'},
  {'name': 'self',
   'kind': 'f',
   'schema': 'lab',
   'table': 'demo',
   'deferrable': False,
   'deferred': False,
   'validated': True,
   'outgoing': True,
   'incoming': True,
   'columns': ['id'],
   'referenced_columns': ['id'],
   'definition': 'FOREIGN KEY (id) REFERENCES demo (id)'}],
 [{'name': 'z_idx',
   'method': 'btree',
   'constraint_name': 'same',
   'primary': False,
   'unique': True,
   'exclusion': False,
   'nulls_not_distinct': True,
   'immediate': True,
   'valid': True,
   'ready': True,
   'live': True,
   'replica_identity': True,
   'partial': False,
   'expression': False,
   'total_columns': 2,
   'key_columns': 2,
   'columns': ['z', 'a'],
   'dependency_columns': ['z', 'a'],
   'opclasses': ['pg_catalog.text_ops', 'custom.é.ops'],
   'collations': [None, 'pg_catalog.C'],
   'definition': 'CREATE UNIQUE INDEX z_idx ON demo (z, a)'},
  {'name': 'expr_idx',
   'method': 'btree',
   'constraint_name': None,
   'primary': False,
   'unique': False,
   'exclusion': True,
   'nulls_not_distinct': False,
   'immediate': False,
   'valid': False,
   'ready': False,
   'live': False,
   'replica_identity': False,
   'partial': True,
   'expression': True,
   'total_columns': 1,
   'key_columns': 1,
   'columns': [None],
   'dependency_columns': ['é'],
   'opclasses': ['custom.é.ops'],
   'collations': [None],
   'definition': 'CHECK ("é" <> \'a\\b\')'},
  {'name': 'include_idx',
   'method': 'btree',
   'constraint_name': '',
   'primary': True,
   'unique': False,
   'exclusion': False,
   'nulls_not_distinct': False,
   'immediate': True,
   'valid': True,
   'ready': True,
   'live': True,
   'replica_identity': False,
   'partial': False,
   'expression': False,
   'total_columns': 3,
   'key_columns': 1,
   'columns': ['id', 'z', 'a'],
   'dependency_columns': ['z', 'id', 'a'],
   'opclasses': ['pg_catalog.int8_ops'],
   'collations': [None],
   'definition': 'CREATE INDEX include_idx ON demo (id) INCLUDE (z, a)'}],
 [{'column': None, 'kind': 'pg_rewrite'},
  {'column': 'é', 'kind': 'pg_proc'},
  {'column': 'é', 'kind': 'pg_attrdef'}],
 [{'name': 'demo'}, {'name': 'z_idx'}])

EXPECTED = {'relation': {'relkind': 'r',
              'relpersistence': 'p',
              'relrowsecurity': True,
              'relforcerowsecurity': False,
              'relhasrules': True,
              'inherited': False,
              'user_triggers': True},
 'columns': [{'attnum': 1,
              'name': 'id',
              'type': 'int8',
              'type_schema': 'pg_catalog',
              'typmod': '-1',
              'nullable': False,
              'identity': '',
              'generated': '',
              'collation_name': None,
              'collation_schema': None,
              'deterministic': None,
              'provider': None,
              'default_digest': None,
              'collation': None}],
 'constraints': [{'name': 'same',
                  'kind': 'f',
                  'schema': 'z_schema',
                  'table': 'incoming',
                  'deferrable': True,
                  'deferred': False,
                  'validated': True,
                  'outgoing': False,
                  'incoming': True,
                  'columns': ['z', 'a'],
                  'referenced_columns': ['b', 'a'],
                  'definition_digest': '4d9ef2b48d2d4130905b1c3bcac192a4e999ed0093f75235d93631f17cd550e8'},
                 {'name': 'same',
                  'kind': 'u',
                  'schema': 'lab',
                  'table': 'demo',
                  'deferrable': False,
                  'deferred': True,
                  'validated': False,
                  'outgoing': True,
                  'incoming': False,
                  'columns': ['z', 'a'],
                  'referenced_columns': [],
                  'definition_digest': '7d98c77f3912a0e9045f5da1ab7c04aa8048c233e049dd9c352835d0fa57ce42'},
                 {'name': 'self',
                  'kind': 'f',
                  'schema': 'lab',
                  'table': 'demo',
                  'deferrable': False,
                  'deferred': False,
                  'validated': True,
                  'outgoing': True,
                  'incoming': True,
                  'columns': ['id'],
                  'referenced_columns': ['id'],
                  'definition_digest': '7daa847dc06d2565bf5d877da82daa18457d1f6a551d4b2e0cea54b26c994bd5'}],
 'indexes': [{'name': 'z_idx',
              'method': 'btree',
              'constraint_name': 'same',
              'definition_digest': 'c1af469a67491cb099069702fa58c0bcf9c82b80fac63b7d4370014c82f299a2',
              'primary': False,
              'unique': True,
              'exclusion': False,
              'nulls_not_distinct': True,
              'immediate': True,
              'valid': True,
              'ready': True,
              'live': True,
              'replica_identity': True,
              'partial': False,
              'expression': False,
              'total_columns': 2,
              'key_columns': 2,
              'columns': ['z', 'a'],
              'dependency_columns': ['z', 'a'],
              'opclasses': ['pg_catalog.text_ops', 'custom.é.ops'],
              'collations': [None, 'pg_catalog.C']},
             {'name': 'expr_idx',
              'method': 'btree',
              'constraint_name': None,
              'definition_digest': '1c62abef2864d113e84a365dab0f448a5a25b51041d80418c1c030cc4fa5cb3e',
              'primary': False,
              'unique': False,
              'exclusion': True,
              'nulls_not_distinct': False,
              'immediate': False,
              'valid': False,
              'ready': False,
              'live': False,
              'replica_identity': False,
              'partial': True,
              'expression': True,
              'total_columns': 1,
              'key_columns': 1,
              'columns': [None],
              'dependency_columns': ['é'],
              'opclasses': ['custom.é.ops'],
              'collations': [None]},
             {'name': 'include_idx',
              'method': 'btree',
              'constraint_name': '',
              'definition_digest': '63425fb578587353483024468670cf6b9add32b4444e6c047b7c8b7b5f0f43f6',
              'primary': True,
              'unique': False,
              'exclusion': False,
              'nulls_not_distinct': False,
              'immediate': True,
              'valid': True,
              'ready': True,
              'live': True,
              'replica_identity': False,
              'partial': False,
              'expression': False,
              'total_columns': 3,
              'key_columns': 1,
              'columns': ['id', 'z', 'a'],
              'dependency_columns': ['z', 'id', 'a'],
              'opclasses': ['pg_catalog.int8_ops'],
              'collations': [None]}],
 'dependencies': [{'column': None, 'kind': 'pg_rewrite'},
                  {'column': 'é', 'kind': 'pg_proc'},
                  {'column': 'é', 'kind': 'pg_attrdef'}]}

CANONICAL_BYTES = [b'"FOREIGN KEY (z, a) REFERENCES demo (b, a)"',
 b'"UNIQUE (z, a)"',
 b'"FOREIGN KEY (id) REFERENCES demo (id)"',
 b'"CREATE UNIQUE INDEX z_idx ON demo (z, a)"',
 b'"CHECK (\\"\xc3\xa9\\" <> \'a\\\\b\')"',
 b'"CREATE INDEX include_idx ON demo (id) INCLUDE (z, a)"']

DIGESTS = ['4d9ef2b48d2d4130905b1c3bcac192a4e999ed0093f75235d93631f17cd550e8',
 '7d98c77f3912a0e9045f5da1ab7c04aa8048c233e049dd9c352835d0fa57ce42',
 '7daa847dc06d2565bf5d877da82daa18457d1f6a551d4b2e0cea54b26c994bd5',
 'c1af469a67491cb099069702fa58c0bcf9c82b80fac63b7d4370014c82f299a2',
 '1c62abef2864d113e84a365dab0f448a5a25b51041d80418c1c030cc4fa5cb3e',
 '63425fb578587353483024468670cf6b9add32b4444e6c047b7c8b7b5f0f43f6']

def exact(actual, expected):
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return (actual.keys() == expected.keys()
                and all(exact(actual[key], value) for key, value in expected.items()))
    if type(expected) in (list, tuple):
        return len(actual) == len(expected) and all(exact(a,b) for a,b in zip(actual,expected))
    return actual == expected


class SchemaConnection:
    def __init__(self, second=False):
        self.second = second
        self.raw = deepcopy(RAW)
        self.before = deepcopy(self.raw)
        self.position = 0
        self.show = 0
        self.consumed = 0

    def exec_driver_sql(self, statement):
        assert statement == 'SHOW search_path' and self.show == 0 and self.position == 0
        self.show += 1
        return SimpleNamespace(scalar_one=lambda: 'pg_catalog')

    def execute(self, statement, params):
        from sqlalchemy.sql.elements import TextClause
        assert type(statement) is TextClause and self.show == 1 and self.position < 6
        assert ' '.join(str(statement).split()) == ' '.join(SQL[self.position].split())
        expected_params = (({'schema':'other','table':'demo2'} if self.second else {'schema':'lab','table':'demo'}) if self.position == 0 else
                           ({'schema':'other'} if self.second else {'schema':'lab'}) if self.position == 5 else {'oid':1234})
        assert exact(params, expected_params)
        rows = deepcopy(self.raw[self.position])
        self.position += 1
        used = False
        def mappings():
            nonlocal used
            assert not used
            used = True
            self.consumed += 1
            return rows
        return SimpleNamespace(mappings=mappings)

from uuid import UUID
from sqlalchemy.dialects.postgresql.base import PGDialect
import json
import unittest
from pathlib import Path

TABLE1='00000000-0000-0000-0000-000000000101'
TABLE2='00000000-0000-0000-0000-000000000102'
OP=UUID('12345678-1234-5678-9abc-123456789abc')
GUARD_SQL=(
'''SELECT g.tgenabled, g.tgtype, g.tgqual IS NULL, g.tgnargs,
 n.nspname, f.proname, f.prosecdef, f.proconfig, f.prosrc, pg_catalog.pg_get_userbyid(f.proowner)
 FROM pg_catalog.pg_trigger g JOIN pg_catalog.pg_proc f ON f.oid=g.tgfoid
 JOIN pg_catalog.pg_namespace n ON n.oid=f.pronamespace
 WHERE g.tgrelid=pg_catalog.to_regclass(%s) AND g.tgname=%s''',
'''SELECT g.tgname, g.tgenabled,
 pg_catalog.pg_get_triggerdef(g.oid), f.prosrc, f.prosecdef, f.proconfig,
 pg_catalog.pg_get_userbyid(f.proowner)
 FROM pg_catalog.pg_trigger g JOIN pg_catalog.pg_proc f ON f.oid=g.tgfoid
 WHERE g.tgrelid=pg_catalog.to_regclass(%s) AND NOT g.tgisinternal
 ORDER BY g.tgname''')
GUARDS={
 'lab':['A',62,True,0,'lab','_cryptalis_12345678123456789abc123456789abc_guard',False,None,'body','owner',[
  ['_cryptalis_12345678123456789abc123456789abc_pause','A','definition','body',False,None,'owner']]],
 'other':['A',62,True,0,'other','_cryptalis_12345678123456789abc123456789abc_guard',False,None,'body','owner',[
  ['_cryptalis_12345678123456789abc123456789abc_pause','A','definition','body',False,None,'owner']]],
}


class GuardConnection:
    def __init__(self, second=False):
        self.dialect=PGDialect(); self.position=0; self.consumed=0
        self.second=second
    def exec_driver_sql(self, sql, params):
        index=self.position
        assert index < 2 and ' '.join(sql.split()) == ' '.join(GUARD_SQL[index].split())
        table='"other"."demo2"' if self.second else '"lab"."demo"'
        assert exact(params, (table,'_cryptalis_12345678123456789abc123456789abc_pause') if index==0 else (table,))
        self.position+=1
        shape=GUARDS['other' if self.second else 'lab']
        used=False
        def consume():
            nonlocal used
            assert not used; used=True; self.consumed+=1
            return tuple(deepcopy(shape[:10])) if index==0 else [tuple(deepcopy(shape[10][0]))]
        return SimpleNamespace(**({'one_or_none':consume} if index==0 else {'all':consume}))


class JournalConnection:
    def __init__(self, state=None, write=False):
        self.dialect=PGDialect(); self.state=state; self.write=write; self.calls=0; self.saved=None
    def exec_driver_sql(self, sql, params):
        self.calls+=1
        if self.write:
            assert self.calls==1
            assert sql=='UPDATE "lab"."_cryptalis_journal" SET state=%s::jsonb WHERE operation_id=%s AND plan_digest=%s'
            assert type(params) is tuple and len(params)==3 and type(params[0]) is str and params[1:]==(OP,'a'*64)
            self.saved=params[0]
            return SimpleNamespace(rowcount=1)
        if self.calls==1:
            assert sql=='SELECT pg_catalog.to_regclass(%s)' and params==('"lab"."_cryptalis_journal"',)
            return SimpleNamespace(scalar_one=lambda:'lab._cryptalis_journal')
        assert self.calls==2
        assert sql=='SELECT plan_digest, state FROM "lab"."_cryptalis_journal" WHERE operation_id=%s' and params==(OP,)
        return SimpleNamespace(one_or_none=lambda:('a'*64,self.state))


def context():
    return {'format':'cryptalis.transition/retained-native-comments-cluster-research-v2',
      'kind':'protect','operation_id':'12345678-1234-5678-9abc-123456789abc',
      'models':[{'table_id':TABLE1,'record_codec':'int64-be/v1','schema':'lab'},
                {'table_id':TABLE2,'record_codec':'uuid16/v1','schema':'other'}]}


def fixture(phase='EXPANDED', verified=False):
    models={}
    for table,schema,cursor in ((TABLE1,'lab','-7'),(TABLE2,'other','00000000-0000-0000-0000-000000000303')):
        item={'scope':{'count':2,'membership':'b'*64},'rows':2,'chunks':1,'cursor':cursor,
              'schema':deepcopy(EXPECTED),'guard':deepcopy(GUARDS[schema])}
        if phase in ('PENDING','ACTIVE','DEPROTECTING'): item['active_schema']=deepcopy(EXPECTED)
        models[table]=item
    state={'phase':phase,'models':models}
    if verified or phase in ('VERIFIED','PENDING','ACTIVE','DEPROTECTING'):
        state['verification']={TABLE1:'c'*64,TABLE2:'d'*64}
    return state


def expected_report(phase=None, verified=None, missing=None, *, code=None, component=None, status='SHAPE_INSPECTED'):
    # Full literal report contract, independent of implementation constants.
    return {'format':'cryptalis.retained-journal-diagnostic/v1','status':status,
      'effects':'NONE','authority':'ADVISORY_NOT_AUTHENTICATED','complete':False,'ready':False,
      'metadata_validated':False,'current_native_verified':False,'successor_authorized':False,
      'text_order_verified':False,'phase':phase,'verification_present':verified,
      'guard_observation_missing':missing,'code':code,'component':component,
      'limits':(
       'State-projection shape coverage only; supplied context is not authenticated.',
       'Original comments, native designation and profile authenticity are not inspected.',
       'No current guard, catalog, ownership, transaction, cleanup or recovery authority is established.',
       'Text ordering, uniqueness, DISTINCT and native relational consistency remain unverified.',
       'Decoded ordinary input must remain stable during this synchronous call; no transport or concurrent snapshot guarantee.')}


def run_composition_cases():
    import cryptalis.doctor as public
    import cryptalis.migration as migration
    from cryptalis import _journal_diagnostics as composite
    import cryptalis.manifest.compiler as compiler
    root=Path(public.__file__).parent
    modules=(public,migration,compiler,composite,composite.progress,composite.columns,composite.guard,composite.remaining)
    bindings=[(public,'inspect_retained_journal',public.inspect_retained_journal),
              (composite,'inspect_retained_journal',composite.inspect_retained_journal),
              (composite.progress,'inspect_forward_progress',composite.progress.inspect_forward_progress),
              (composite.columns,'inspect_column_projection',composite.columns.inspect_column_projection),
              (composite.guard,'inspect_guard_projection',composite.guard.inspect_guard_projection),
              (composite.remaining,'inspect_remaining_schema_projection',composite.remaining.inspect_remaining_schema_projection)]
    bindings += [(migration,name,getattr(migration,name)) for name in ('_facts','_guard_facts','_guard_names','_table','_quote','_save','_state')]
    bindings += [(compiler,name,getattr(compiler,name)) for name in ('_schema_facts','_read_schema_facts','_rows','_canonical','_digest')]
    def binding_check():
        for module in modules:
            expected=root.joinpath(*module.__name__.split('.')[1:]).with_suffix('.py')
            assert Path(module.__file__)==expected and module.__spec__.origin==str(expected)
        for module,name,function in bindings:
            assert getattr(module,name) is function and function.__code__.co_filename==module.__file__
        assert migration._schema_facts is compiler._schema_facts
    binding_check()
    records=[]
    def check(label, action):
        try: action()
        except Exception: records.append({'id':label,'status':'FAIL','failure':'case_assertion'})
        else: records.append({'id':label,'status':'PASS'})
    def inspect(ctx,state,expected):
        before=deepcopy((ctx,state))
        report=public.inspect_retained_journal(ctx,state)
        assert exact(report,expected) and exact((ctx,state),before)
        if type(ctx) is dict: ctx.clear()
        if type(state) is dict: state.clear()
        assert exact(report,expected)
    def joined(phase,verified=False):
        expected_state=fixture(phase,verified)
        state=fixture(phase,verified)
        plan=SimpleNamespace(operation_id=OP,digest='a'*64,document={'journal_schema':'lab'})
        for second,table in ((False,TABLE1),(True,TABLE2)):
            model={'schema':'other','table':'demo2'} if second else {'schema':'lab','table':'demo'}
            schema_connection=SchemaConnection(second)
            produced=migration._facts(schema_connection,model)
            assert exact(produced,EXPECTED)
            assert schema_connection.position==6 and schema_connection.consumed==6 and schema_connection.show==1
            assert exact(schema_connection.raw,schema_connection.before)
            guard_connection=GuardConnection(second)
            observed_guard=migration._guard_facts(guard_connection,plan,model)
            assert exact(observed_guard,GUARDS[model['schema']])
            assert guard_connection.position==2 and guard_connection.consumed==2
            state['models'][table]['schema']=produced
            state['models'][table]['guard']=observed_guard
            if phase in ('PENDING','ACTIVE','DEPROTECTING'):
                active_connection=SchemaConnection(second)
                state['models'][table]['active_schema']=migration._facts(active_connection,model)
                assert active_connection.position==6 and active_connection.consumed==6
        assert exact(state,expected_state)
        writer=JournalConnection(write=True)
        migration._save(writer,plan,state)
        assert writer.calls==1 and exact(state,expected_state)
        decoded=json.loads(writer.saved)
        assert exact(decoded,expected_state)
        reader=JournalConnection(decoded)
        pin=SimpleNamespace(phase='ACTIVE' if phase=='ACTIVE' else 'PREPARED')
        if phase=='DEPROTECTING':
            try: migration._state(reader,plan,pin)
            except migration.TransitionFailure as error:
                assert error.code=='restored_state_behind_external_pin'
            else: raise AssertionError('forward_state_must_refuse')
            observed=decoded
        else:
            observed=migration._state(reader,plan,pin,allow_aborted=phase=='ABORTED')
            assert observed is decoded
        assert reader.calls==2
        inspect(context(),observed,expected_report(phase,'verification' in expected_state,False))
    for phase in ('EXPANDED','BACKFILLED','VERIFIED','PENDING','ACTIVE','DEPROTECTING','ABORTED'):
        check('joined:'+phase,lambda phase=phase:joined(phase))
    check('joined:ABORTED_verified',lambda:joined('ABORTED',True))
    for profile in ('cryptalis.transition/retained-native-research-v0',
                    'cryptalis.transition/retained-native-comments-research-v1',
                    'cryptalis.transition/retained-native-comments-cluster-research-v2'):
        def supported(profile=profile):
            ctx=context();ctx['format']=profile
            inspect(ctx,fixture(),expected_report('EXPANDED',False,False))
        check('profile:'+profile,supported)
    def absent_guard():
        state=fixture('ABORTED');state['models'][TABLE2]['guard']=None
        inspect(context(),state,expected_report('ABORTED',False,True))
    check('coverage:present_none_guard',absent_guard)
    negatives=[]
    def mutation(label,change,component,code,phase='EXPANDED',status='REJECTED_INPUT'):
        ctx=context();state=fixture(phase);change(ctx,state)
        negatives.append((label,ctx,state,expected_report(code=code,component=component,status=status)))
    mutation('missing_guard',lambda c,s:s['models'][TABLE2].pop('guard'),'progress','invalid_model_members')
    mutation('malformed_guard',lambda c,s:s['models'][TABLE2].__setitem__('guard',[]),'guard','invalid_guard_shape')
    mutation('missing_schema',lambda c,s:s['models'][TABLE2].pop('schema'),'progress','invalid_model_members')
    mutation('schema_extra',lambda c,s:s['models'][TABLE2]['schema'].__setitem__('_relation_names',[]),'schema','invalid_schema_members')
    mutation('schema_missing',lambda c,s:s['models'][TABLE2]['schema'].pop('columns'),'schema','invalid_schema_members')
    mutation('late_columns',lambda c,s:s['models'][TABLE2]['schema']['columns'][0].__setitem__('attnum',False),'columns','invalid_column_order')
    mutation('late_remaining',lambda c,s:s['models'][TABLE2]['schema']['indexes'][2].__setitem__('total_columns',4),'remaining','invalid_count_vector')
    mutation('late_progress',lambda c,s:s['models'][TABLE2].__setitem__('rows',3),'progress','invalid_progress_counters')
    mutation('active_columns',lambda c,s:s['models'][TABLE2]['active_schema']['columns'][0].__setitem__('attnum',0),'columns','invalid_column_order','ACTIVE')
    mutation('active_remaining',lambda c,s:s['models'][TABLE2]['active_schema']['dependencies'][2].__setitem__('kind',None),'remaining','invalid_string','PENDING')
    mutation('missing_active',lambda c,s:s['models'][TABLE2].pop('active_schema'),'progress','invalid_model_members','DEPROTECTING')
    mutation('extra_active',lambda c,s:s['models'][TABLE2].__setitem__('active_schema',deepcopy(EXPECTED)),'progress','invalid_model_members','ABORTED')
    mutation('swapped_guards',lambda c,s:s['models'][TABLE2].__setitem__('guard',deepcopy(GUARDS['lab'])),'guard','guard_identity_mismatch')
    mutation('wrong_operation',lambda c,s:c.__setitem__('operation_id','00000000-0000-0000-0000-000000000000'),'guard','guard_identity_mismatch')
    mutation('duplicate_context',lambda c,s:c['models'][1].__setitem__('table_id',TABLE1),'context','duplicate_context_table')
    mutation('context_type',lambda c,s:c.__setitem__('format',None),'context','invalid_context_string')
    mutation('unknown_profile',lambda c,s:c.__setitem__('format','future'),'context','unsupported_diagnostic_profile',status='UNSUPPORTED_PROFILE')
    mutation('reverse_kind',lambda c,s:c.__setitem__('kind','deprotect'),'context','unsupported_diagnostic_profile',status='UNSUPPORTED_PROFILE')
    mutation('unknown_codec',lambda c,s:c['models'][1].__setitem__('record_codec','future'),'context','unsupported_record_codec',status='UNSUPPORTED_PROFILE')
    mutation('codec_type',lambda c,s:c['models'][1].__setitem__('record_codec',None),'context','invalid_context_string')
    mutation('invalid_late_over_unsupported',lambda c,s:(c.__setitem__('format','future'),c['models'][1].__setitem__('schema',None)),'context','invalid_context_string')
    mutation('context_before_none_guard',lambda c,s:(s['models'][TABLE2].__setitem__('guard',None),c.__setitem__('operation_id','bad')),'context','invalid_operation_id')
    mutation('unknown_phase',lambda c,s:s.__setitem__('phase','FUTURE'),'progress','unsupported_producer_phase')
    for label,ctx,state,expected in negatives:
        check('reject:'+label,lambda c=ctx,s=state,e=expected:inspect(c,s,e))
    check('reject:state_none',lambda:inspect(context(),None,expected_report(code='invalid_progress_state',component='progress',status='REJECTED_INPUT')))
    def error_map():
        # Unit boundary only: no real helper is replaced or monkeypatched.
        samples=(('progress',composite.progress.ProgressShapeError,'invalid_scope'),
                 ('columns',composite.columns.ColumnProjectionError,'invalid_column_order'),
                 ('remaining',composite.remaining.SchemaProjectionError,'invalid_vector'),
                 ('guard',composite.guard.GuardProjectionError,'guard_identity_incomplete'))
        for component,error_type,code in samples:
            for source,expected in ((code,code),('unknown secret body','unsupported_diagnostic_reason')):
                def fail(): raise error_type(source)
                try: composite._call(component,fail)
                except composite.JournalDiagnosticError as error:
                    assert error.code==expected and error.component==component and error.status=='REJECTED_INPUT'
                else: raise AssertionError('missing_error')
        def unexpected(): raise RuntimeError('not serialized')
        try: composite._call('progress',unexpected)
        except RuntimeError: pass
        else: raise AssertionError('unexpected_swallowed')
    check('mapping:closed_codes_and_unexpected',error_map)
    check('binding:actual_modules_and_functions',binding_check)
    assert len(records)==38 and len({r['id'] for r in records})==38
    return records


class RetainedJournalDiagnosticsTests(unittest.TestCase):
    def test_public_composition(self):
        for outcome in run_composition_cases():
            with self.subTest(case=outcome['id']):
                self.assertEqual(outcome['status'],'PASS')
