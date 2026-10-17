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


class RecordingConnection:
    def __init__(self):
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
        expected_params = ({'schema':'lab','table':'demo'} if self.position == 0 else
                           {'schema':'lab'} if self.position == 5 else {'oid':1234})
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

def run_cases(migration, inspector):
    records = []
    def check(label, action):
        try: action()
        except Exception: records.append({'id':label,'status':'FAIL','failure':'case_assertion'})
        else: records.append({'id':label,'status':'PASS'})
    def projection():
        return {key:deepcopy(EXPECTED[key]) for key in ('relation','constraints','indexes','dependencies')}
    def inspect(value, code=None):
        before = deepcopy(value)
        try: result = inspector.inspect_remaining_schema_projection(value)
        except inspector.SchemaProjectionError as error:
            assert code is not None and type(error) is inspector.SchemaProjectionError
            assert error.code == code and error.args == (code,)
        else:
            assert code is None and type(result) is inspector.SchemaInspection
            assert result.classification == 'REMAINING_SCHEMA_PROJECTION_SHAPE_ONLY'
            assert all(getattr(result,k) is False for k in ('metadata_validated','current_native_verified','successor_authorized','text_order_verified'))
            assert not hasattr(result,'__dict__')
            try: result.classification = 'changed'
            except FrozenInstanceError: pass
            else: raise AssertionError('mutable_result')
        assert exact(value,before)
    def producer():
        connection = RecordingConnection()
        model = {'schema':'lab','table':'demo'}
        result = migration._facts(connection,model)
        assert exact(result,EXPECTED)
        assert connection.show == 1 and connection.position == 6 and connection.consumed == 6
        assert exact(connection.raw,connection.before)
        assert model == {'schema':'lab','table':'demo'}
        inspect({key:result[key] for key in ('relation','constraints','indexes','dependencies')})
        assert exact(result,EXPECTED)
    check('producer:populated_full_literal_output',producer)
    def canonical():
        compiler = __import__('cryptalis.manifest.compiler',fromlist=['_canonical'])
        definitions = [item['definition'] for item in RAW[2]+RAW[3]]
        assert len(definitions) == len(CANONICAL_BYTES) == len(DIGESTS) == 6
        for definition,raw,digest in zip(definitions,CANONICAL_BYTES,DIGESTS):
            assert compiler._canonical(definition) == raw
            assert hashlib.sha256(raw).hexdigest() == digest
            assert compiler._digest(definition) == digest
    check('producer:independent_canonical_bytes_digests',canonical)
    check('shape:populated',lambda:inspect(projection()))
    def empty():
        value=projection()
        for key in ('constraints','indexes','dependencies'): value[key]=[]
        inspect(value)
    check('shape:empty_inventories',empty)
    def duplicates():
        value=projection()
        for key in ('constraints','indexes','dependencies'): value[key].append(deepcopy(value[key][0]))
        value['constraints'][0]['columns']=['z','z']
        value['indexes'][0]['dependency_columns']=['z','z']
        value['indexes'][0]['opclasses']=['x','x']
        inspect(value)
    check('shape:duplicates_are_unvalidated',duplicates)
    def booleans():
        value=projection()
        for item in [value['relation']]+value['constraints']+value['indexes']:
            for key in item:
                if type(item[key]) is bool: item[key]=not item[key]
        inspect(value)
    check('shape:boolean_complements',booleans)
    def zero_vectors():
        value=projection(); item=value['indexes'][0]
        item['total_columns']=0; item['key_columns']=0
        for key in ('columns','dependency_columns','opclasses','collations'): item[key]=[]
        inspect(value)
    check('shape:zero_counts_empty_vectors',zero_vectors)

    class DictSubclass(dict): pass
    class ListSubclass(list): pass
    class StrSubclass(str): pass
    class IntSubclass(int): pass
    mutations=[]
    def mutation(label, change, code):
        value=projection(); change(value); mutations.append((label,value,code))
    # Literal field profiles independent of implementation constants.
    profiles=(
      ('relation',None,'relkind relpersistence','relrowsecurity relforcerowsecurity relhasrules inherited user_triggers',()),
      ('constraints',2,'name kind schema table','deferrable deferred validated outgoing incoming',('columns','referenced_columns')),
      ('indexes',2,'name method','primary unique exclusion nulls_not_distinct immediate valid ready live replica_identity partial expression',('columns','dependency_columns','opclasses','collations')),
      ('dependencies',2,'kind','',()))
    def item(v,key,index): return v[key] if index is None else v[key][index]
    for key,index,strings,bools,vectors in profiles:
        mutation(key+'_missing',lambda v,k=key,i=index:item(v,k,i).pop(next(iter(item(v,k,i)))),'invalid_members')
        mutation(key+'_extra',lambda v,k=key,i=index:item(v,k,i).__setitem__('unknown','x'),'invalid_members')
        for field in strings.split():
            mutation(key+'_string_'+field,lambda v,k=key,i=index,f=field:item(v,k,i).__setitem__(f,None),'invalid_string')
        for field in bools.split():
            mutation(key+'_bool_'+field,lambda v,k=key,i=index,f=field:item(v,k,i).__setitem__(f,0),'invalid_boolean')
        for field in vectors:
            mutation(key+'_vector_'+field,lambda v,k=key,i=index,f=field:item(v,k,i).__setitem__(f,()),'invalid_vector')
    for key in ('relation','constraints','indexes','dependencies'):
        mutation('top_missing_'+key,lambda v,k=key:v.pop(k),'invalid_members')
    for key in ('columns','_relation_names'):
        mutation('top_extra_'+key,lambda v,k=key:v.__setitem__(k,[]),'invalid_members')
    mutation('relation_oid',lambda v:v['relation'].__setitem__('oid',1234),'invalid_members')
    for key in ('constraints','indexes'):
        mutation(key+'_raw_definition',lambda v,k=key:v[k][2].__setitem__('definition','raw'),'invalid_members')
        for label,bad in (('type',None),('length','a'*63),('case','A'*64),('subclass',StrSubclass('a'*64))):
            mutation(key+'_digest_'+label,lambda v,k=key,b=bad:v[k][2].__setitem__('definition_digest',b),'invalid_digest')
    for key,field in (('constraints','columns'),('constraints','referenced_columns'),('indexes','dependency_columns'),('indexes','opclasses')):
        mutation(key+'_null_'+field,lambda v,k=key,f=field:v[k][2].__setitem__(f,[None]),'invalid_vector')
    for field in ('columns','collations'):
        mutation('indexes_bad_nullable_'+field,lambda v,f=field:v['indexes'][2].__setitem__(f,[1]),'invalid_vector')
    for key,field in (('indexes','constraint_name'),('dependencies','column')):
        mutation(key+'_optional',lambda v,k=key,f=field:v[k][2].__setitem__(f,False),'invalid_optional_string')
    for field in ('total_columns','key_columns'):
        for label,bad in (('bool',True),('negative',-1),('text','1'),('subclass',IntSubclass(1))):
            mutation('count_'+field+'_'+label,lambda v,f=field,b=bad:v['indexes'][2].__setitem__(f,b),'invalid_count')
    mutation('key_exceeds_total',lambda v:v['indexes'][2].__setitem__('key_columns',4),'invalid_count_vector')
    mutation('total_vector_mismatch',lambda v:v['indexes'][2].__setitem__('total_columns',4),'invalid_count_vector')
    for key in ('constraints','indexes','dependencies'):
        mutation(key+'_list_subclass',lambda v,k=key:v.__setitem__(k,ListSubclass(v[k])),'invalid_inventory')
        mutation(key+'_late_dict_subclass',lambda v,k=key:v[k].__setitem__(2,DictSubclass(v[k][2])),'invalid_members')
    mutation('relation_dict_subclass',lambda v:v.__setitem__('relation',DictSubclass(v['relation'])),'invalid_members')
    mutation('string_subclass',lambda v:v['dependencies'][2].__setitem__('kind',StrSubclass('pg_proc')),'invalid_string')
    mutation('vector_subclass',lambda v:v['indexes'][2].__setitem__('opclasses',ListSubclass(['x'])),'invalid_vector')
    mutation('vector_string_subclass',lambda v:v['indexes'][2].__setitem__('opclasses',[StrSubclass('x')]),'invalid_vector')
    for label,value,code in mutations:
        check('reject:'+label,lambda v=value,c=code:inspect(v,c))
    check('reject:top_dict_subclass',lambda:inspect(DictSubclass(projection()),'invalid_members'))
    check('reject:top_none',lambda:inspect(None,'invalid_members'))
    assert len(records)==98 and len({r['id'] for r in records})==98
    return records
