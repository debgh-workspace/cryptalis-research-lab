"""Fixed synthetic rows through actual compiler catalog projection and _facts.

No product-function substitution, SQL execution, DB or native truth assertion.
"""
from copy import deepcopy
from types import SimpleNamespace

# Literal SQL expectations, independent of product source at test runtime.
# Whitespace formatting alone is normalized; all tokens/clauses remain exact.
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

RAW = (
 [{'oid': 1234, 'relkind':'r', 'relpersistence':'p', 'relrowsecurity':False,
   'relforcerowsecurity':False, 'relhasrules':False, 'inherited':False, 'user_triggers':True}],
 [
  {'attnum':1,'name':'id','type':'int8','type_schema':'pg_catalog','typmod':-1,
   'nullable':False,'identity':'','generated':'','collation_name':None,'collation_schema':None,
   'deterministic':None,'provider':None,'default_expression':None},
  {'attnum':3,'name':'label','type':'text','type_schema':'pg_catalog','typmod':-1,
   'nullable':True,'identity':'','generated':'','collation_name':'C','collation_schema':'pg_catalog',
   'deterministic':True,'provider':'c','default_expression':"'seed'::text"},
  {'attnum':5,'name':'é.alias','type':'varchar','type_schema':'pg_catalog','typmod':20,
   'nullable':True,'identity':'','generated':'','collation_name':'x','collation_schema':None,
   'deterministic':False,'provider':'i','default_expression':None},
 ],
 [{'name':'u_label','kind':'u','deferrable':False,'deferred':False,'validated':True,
   'outgoing':True,'incoming':False,'schema':'lab','table':'demo','columns':['label'],
   'referenced_columns':[],'definition':'UNIQUE (label)'}],
 [{'name':'z_idx','primary':False,'unique':False,'exclusion':False,'nulls_not_distinct':False,
   'immediate':True,'valid':True,'ready':True,'live':True,'replica_identity':False,
   'total_columns':1,'key_columns':1,'method':'btree','partial':False,'expression':True,
   'columns':[None],'dependency_columns':['label'],'opclasses':['pg_catalog.text_ops'],
   'collations':[None],'constraint_name':None,'definition':'CREATE INDEX z_idx ON lab.demo ((lower(label)))'}],
 # Deliberately supplied order: this fixture proves preservation, not a native
 # collation result or physical catalog validity.
 [{'column':None,'kind':'pg_rewrite'}, {'column':'label','kind':'pg_attrdef'}],
 [{'name':'demo'}, {'name':'z_idx'}],
)

# Full independent literal stripped output. No call to product digest/transform
# functions constructs this expected object. Hashes are pinned SHA256 of the
# canonical JSON string bytes, not hashes of raw SQL text.
EXPECTED = {
 'relation':{'relkind':'r','relpersistence':'p','relrowsecurity':False,
  'relforcerowsecurity':False,'relhasrules':False,'inherited':False,'user_triggers':True},
 'columns':[
  {'attnum':1,'name':'id','type':'int8','type_schema':'pg_catalog','typmod':'-1',
   'nullable':False,'identity':'','generated':'','collation_name':None,'collation_schema':None,
   'deterministic':None,'provider':None,'default_digest':None,'collation':None},
  {'attnum':3,'name':'label','type':'text','type_schema':'pg_catalog','typmod':'-1',
   'nullable':True,'identity':'','generated':'','collation_name':'C','collation_schema':'pg_catalog',
   'deterministic':True,'provider':'c','default_digest':'aa805bd3892e01f40d355746bff61d6565c2d46f3be3de9c405a22fb606ec12b','collation':'pg_catalog.C'},
  {'attnum':5,'name':'é.alias','type':'varchar','type_schema':'pg_catalog','typmod':'20',
   'nullable':True,'identity':'','generated':'','collation_name':'x','collation_schema':None,
   'deterministic':False,'provider':'i','default_digest':None,'collation':'None.x'},
 ],
 'constraints':[{'name':'u_label','kind':'u','deferrable':False,'deferred':False,'validated':True,
  'outgoing':True,'incoming':False,'schema':'lab','table':'demo','columns':['label'],
  'referenced_columns':[],'definition_digest':'91251caa3d3adf0df8d5b09bcc5c50ae3dd55f9164d03f2116034ae228f1fdcd'}],
 'indexes':[{'name':'z_idx','primary':False,'unique':False,'exclusion':False,'nulls_not_distinct':False,
  'immediate':True,'valid':True,'ready':True,'live':True,'replica_identity':False,
  'total_columns':1,'key_columns':1,'method':'btree','partial':False,'expression':True,
  'columns':[None],'dependency_columns':['label'],'opclasses':['pg_catalog.text_ops'],
  'collations':[None],'constraint_name':None,
  'definition_digest':'27a316aba6adcd2e3832a862b1ed9d926b8b10f43d0a9afbcd284f4d5c7de93d'}],
 'dependencies':[{'column':None,'kind':'pg_rewrite'}, {'column':'label','kind':'pg_attrdef'}],
}


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
        assert params == expected_params
        rows = deepcopy(self.raw[self.position])
        self.position += 1
        return SimpleNamespace(mappings=lambda: rows)


def run_cases(migration, inspector):
    records = []
    def check(label, callback):
        try:
            callback()
        except Exception:
            records.append({'id':label,'status':'FAIL','failure':'case_assertion_or_exception'})
        else:
            records.append({'id':label,'status':'PASS'})

    def positive(columns):
        before = deepcopy(columns)
        result = inspector.inspect_column_projection(columns)
        assert type(result) is inspector.ColumnInspection
        assert result.classification == 'COLUMN_PROJECTION_SHAPE_ONLY'
        assert result.metadata_validated is False and result.current_native_verified is False
        assert result.successor_authorized is False and not hasattr(result,'__dict__')
        try:
            result.metadata_validated = True
        except (AttributeError,TypeError):
            pass
        else:
            raise AssertionError('mutable_result')
        assert exact(columns, before)
        columns.clear()
        assert result.metadata_validated is False and result.current_native_verified is False

    def actual_producer():
        connection = RecordingConnection()
        model = {'schema':'lab','table':'demo'}
        result = migration._facts(connection, model)
        assert exact(result, EXPECTED)
        assert connection.show == 1 and connection.position == 6
        assert exact(connection.raw, connection.before) and model == {'schema':'lab','table':'demo'}
        positive(result['columns'])
    check('actual_producer:full_literal_output', actual_producer)
    check('columns:empty', lambda: positive([]))
    check('columns:literal_projection', lambda: positive(deepcopy(EXPECTED['columns'])))
    def positive_change(key, value):
        columns = deepcopy(EXPECTED['columns'])
        columns[0][key] = value
        positive(columns)
    check('columns:zero_typmod', lambda: positive_change('typmod','0'))
    check('columns:long_lexical_typmod', lambda: positive_change('typmod','1'*5000))
    def dotted():
        columns = deepcopy(EXPECTED['columns'])
        columns[1]['collation_schema'] = 'a.b'
        columns[1]['collation_name'] = 'é.c'
        columns[1]['collation'] = 'a.b.é.c'
        positive(columns)
    check('columns:dotted_nonascii_collation', dotted)
    def empty_collation():
        columns = deepcopy(EXPECTED['columns'])
        columns[1]['collation_name'] = ''
        columns[1]['collation'] = None
        positive(columns)
    check('columns:empty_name_fstring_branch', empty_collation)

    def negative(columns, code):
        before = deepcopy(columns)
        try:
            inspector.inspect_column_projection(columns)
        except inspector.ColumnProjectionError as error:
            assert type(error) is inspector.ColumnProjectionError and error.code == code
            assert error.args == (code,)
        else:
            raise AssertionError('mutation_not_rejected')
        assert exact(columns, before)

    mutations = []
    def mutation(label, change, code):
        columns = deepcopy(EXPECTED['columns'])
        change(columns)
        mutations.append((label, columns, code))
    mutation('missing_member',lambda c:c[0].pop('identity'),'invalid_column_members')
    mutation('unknown_member',lambda c:c[0].__setitem__('owner','claimed'),'invalid_column_members')
    mutation('raw_default_member',lambda c:c[0].__setitem__('default_expression','secret'),'invalid_column_members')
    for label,value in [('bool',True),('zero',0),('negative',-1),('text','1'),('float',1.0)]:
        mutation('attnum_'+label,lambda c,value=value:c[0].__setitem__('attnum',value),'invalid_column_order')
    mutation('duplicate_attnum',lambda c:c[1].__setitem__('attnum',1),'invalid_column_order')
    mutation('decreasing_attnum',lambda c:c.reverse(),'invalid_column_order')
    mutation('duplicate_name',lambda c:c[1].__setitem__('name','id'),'duplicate_column_name')
    for label,value in [('integer',-1),('plus','+1'),('negative_zero','-0'),('leading_zero','01'),('empty',''),('whitespace',' 1'),('unicode','١')]:
        mutation('typmod_'+label,lambda c,value=value:c[0].__setitem__('typmod',value),'invalid_column_typmod')
    mutation('nullable_integer',lambda c:c[0].__setitem__('nullable',1),'invalid_column_nullable')
    mutation('deterministic_integer',lambda c:c[0].__setitem__('deterministic',0),'invalid_column_deterministic')
    mutation('default_short',lambda c:c[1].__setitem__('default_digest','a'*63),'invalid_column_default_digest')
    mutation('default_upper',lambda c:c[1].__setitem__('default_digest','A'*64),'invalid_column_default_digest')
    mutation('default_not_string',lambda c:c[1].__setitem__('default_digest',42),'invalid_column_default_digest')
    mutation('false_collation',lambda c:c[2].__setitem__('collation','x'),'invalid_column_collation')
    mutation('optional_not_string',lambda c:c[0].__setitem__('provider',1),'invalid_column_optional_string')
    mutation('required_null',lambda c:c[0].__setitem__('identity',None),'invalid_column_string')
    class DictSubclass(dict): pass
    class IntSubclass(int): pass
    class StrSubclass(str): pass
    class ListSubclass(list): pass
    mutation('dict_subclass',lambda c:c.__setitem__(0,DictSubclass(c[0])),'invalid_column_members')
    mutation('int_subclass',lambda c:c[0].__setitem__('attnum',IntSubclass(1)),'invalid_column_order')
    mutation('str_subclass',lambda c:c[0].__setitem__('name',StrSubclass('id')),'invalid_column_string')
    mutation('typmod_subclass',lambda c:c[0].__setitem__('typmod',StrSubclass('-1')),'invalid_column_typmod')
    for label,columns,code in mutations:
        check('reject:'+label,lambda columns=columns,code=code:negative(columns,code))
    check('reject:list_subclass',lambda:negative(ListSubclass(deepcopy(EXPECTED['columns'])),'invalid_column_list'))
    check('reject:tuple',lambda:negative(tuple(deepcopy(EXPECTED['columns'])),'invalid_column_list'))
    assert len(records) == 39 and len({r['id'] for r in records}) == 39
    return records
