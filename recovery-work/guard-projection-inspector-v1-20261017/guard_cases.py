"""Literal synthetic observations through genuine migration guard producer."""
from copy import deepcopy
from dataclasses import FrozenInstanceError
from types import SimpleNamespace
from uuid import UUID
from sqlalchemy.dialects.postgresql.base import PGDialect

SQL = (
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
CONTEXT = {'operation_id': '12345678-1234-5678-9abc-123456789abc', 'schema': 'lab'}
ROW = ('A', 62, True, 0, 'lab', '_cryptalis_12345678123456789abc123456789abc_guard',
       False, None, 'synthetic outer body', 'synthetic_owner')
INVENTORY = (
    ('z_callback', 'O', 'synthetic definition', 'callback body', True, [], 'other_owner'),
    ('_cryptalis_12345678123456789abc123456789abc_pause', 'A', 'guard definition',
     'synthetic outer body', False, None, 'synthetic_owner'))
EXPECTED = ['A', 62, True, 0, 'lab', '_cryptalis_12345678123456789abc123456789abc_guard',
 False, None, 'synthetic outer body', 'synthetic_owner', [
 ['z_callback', 'O', 'synthetic definition', 'callback body', True, [], 'other_owner'],
 ['_cryptalis_12345678123456789abc123456789abc_pause', 'A', 'guard definition',
  'synthetic outer body', False, None, 'synthetic_owner']]]


def exact(a, b):
    if type(a) is not type(b): return False
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(exact(x, y) for x, y in zip(a, b))
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(exact(a[k], b[k]) for k in a)
    return a == b


class Result:
    def __init__(self, row, inventory, stage):
        self.row, self.inventory, self.stage = row, inventory, stage
        self.consumed = False
    def one_or_none(self):
        assert self.stage == 0 and not self.consumed
        self.consumed = True
        return deepcopy(self.row)
    def all(self):
        assert self.stage == 1 and not self.consumed
        self.consumed = True
        return list(deepcopy(self.inventory))


class RecordingConnection:
    def __init__(self, row, inventory, table):
        self.dialect = PGDialect()
        self.row, self.inventory, self.table = deepcopy(row), deepcopy(inventory), table
        self.position, self.results = 0, []
    def exec_driver_sql(self, query, params):
        position = self.position
        assert position < 2 and type(query) is str
        assert ' '.join(query.split()) == ' '.join(SQL[position].split())
        expected = ((self.table, '_cryptalis_12345678123456789abc123456789abc_pause')
                    if position == 0 else (self.table,))
        assert exact(params, expected)
        result = Result(self.row, self.inventory, position)
        self.results.append(result)
        self.position += 1
        return result


def run_cases(migration, inspector):
    records = []
    def check(label, action):
        try:
            action()
        except Exception:
            records.append({'id': label, 'status': 'FAIL', 'failure': 'case_assertion'})
        else:
            records.append({'id': label, 'status': 'PASS'})
    def inspect(value, context, code=None):
        before, before_context = deepcopy(value), deepcopy(context)
        try:
            result = inspector.inspect_guard_projection(value, context)
        except inspector.GuardProjectionError as error:
            assert code is not None and type(error) is inspector.GuardProjectionError
            assert error.code == code and error.args == (code,)
        else:
            assert code is None and type(result) is inspector.GuardInspection
            expected = ('MISSING_GUARD_OBSERVATION' if value is None else
                        'GUARD_PROJECTION_SHAPE_AND_DECLARED_IDENTITY')
            assert result.classification == expected
            for field in ('metadata_validated','current_native_verified','successor_authorized','text_order_verified'):
                assert getattr(result, field) is False
            assert not hasattr(result, '__dict__')
            try:
                result.classification = 'changed'
            except FrozenInstanceError:
                pass
            else:
                raise AssertionError('mutable_result')
        assert exact(value, before) and exact(context, before_context)
    def producer(row, inventory, expected, code=None, model=None, context=None, table='"lab"."demo"'):
        model = {'schema': 'lab', 'table': 'demo'} if model is None else model
        context = deepcopy(CONTEXT) if context is None else context
        plan = SimpleNamespace(operation_id=UUID('12345678-1234-5678-9abc-123456789abc'))
        before = deepcopy((row, inventory, model, context))
        connection = RecordingConnection(row, inventory, table)
        result = migration._guard_facts(connection, plan, model)
        assert exact(result, expected)
        assert connection.position == (1 if row is None else 2)
        assert all(item.consumed for item in connection.results)
        assert exact((row, inventory, model, context), before)
        assert exact(connection.row, row) and exact(connection.inventory, inventory)
        inspect(result, context, code)
    check('producer:absent', lambda: producer(None, INVENTORY, None))
    check('producer:literal_full_order', lambda: producer(ROW, INVENTORY, EXPECTED))
    check('producer:empty_inventory', lambda: producer(ROW, (),
          ['A',62,True,0,'lab','_cryptalis_12345678123456789abc123456789abc_guard',False,None,
           'synthetic outer body','synthetic_owner',[]], 'guard_identity_incomplete'))
    check('producer:missing_named_inventory', lambda: producer(ROW, (INVENTORY[0],),
          ['A',62,True,0,'lab','_cryptalis_12345678123456789abc123456789abc_guard',False,None,
           'synthetic outer body','synthetic_owner',[
           ['z_callback','O','synthetic definition','callback body',True,[],'other_owner']]],
          'guard_identity_incomplete'))
    def quoted():
        row = ('A',62,True,0,'a."é','_cryptalis_12345678123456789abc123456789abc_guard',
               False,None,'synthetic outer body','synthetic_owner')
        expected = ['A',62,True,0,'a."é','_cryptalis_12345678123456789abc123456789abc_guard',
          False,None,'synthetic outer body','synthetic_owner',[
          ['z_callback','O','synthetic definition','callback body',True,[],'other_owner'],
          ['_cryptalis_12345678123456789abc123456789abc_pause','A','guard definition',
           'synthetic outer body',False,None,'synthetic_owner']]]
        producer(row, INVENTORY, expected, model={'schema':'a."é','table':'t."x'},
                 context={'operation_id':'12345678-1234-5678-9abc-123456789abc','schema':'a."é'},
                 table='"a.""é"."t.""x"')
    check('producer:literal_quoted_identifiers', quoted)
    def disagreement():
        inventory = (('z_callback','O','synthetic definition','callback body',True,[],'other_owner'),
          ('_cryptalis_12345678123456789abc123456789abc_pause','D','different definition',
           'different body',True,['b=2','a=1'],'different_owner'))
        expected = ['A',62,True,0,'lab','_cryptalis_12345678123456789abc123456789abc_guard',False,None,
          'synthetic outer body','synthetic_owner',[
          ['z_callback','O','synthetic definition','callback body',True,[],'other_owner'],
          ['_cryptalis_12345678123456789abc123456789abc_pause','D','different definition',
           'different body',True,['b=2','a=1'],'different_owner']]]
        producer(ROW, inventory, expected)
    check('producer:shared_fields_disagree', disagreement)
    def scalar_domains():
        value = deepcopy(EXPECTED)
        value[1] = 2**80
        value[3] = 2**80
        value[7] = []
        value[10][0][5] = ['z=1','a=2','z=1']
        inspect(value, CONTEXT)
    check('shape:uncapped_integer_config_order', scalar_domains)

    class ListSubclass(list): pass
    class DictSubclass(dict): pass
    class StrSubclass(str): pass
    class IntSubclass(int): pass
    mutations = []
    def mutation(label, change, code):
        value = deepcopy(EXPECTED)
        change(value)
        mutations.append((label, value, code))
    mutation('outer_missing', lambda v:v.pop(), 'invalid_guard_shape')
    mutation('outer_extra', lambda v:v.append('unknown'), 'invalid_guard_shape')
    mutation('trigger_missing', lambda v:v[10][0].pop(), 'invalid_trigger_shape')
    mutation('trigger_extra', lambda v:v[10][0].append('unknown'), 'invalid_trigger_shape')
    for i in (0,4,5,8,9):
        mutation('outer_string_'+str(i), lambda v,i=i:v.__setitem__(i,None), 'invalid_guard_string')
    for i in (1,3):
        for label, bad in (('bool',True),('negative',-1),('string','0'),('subclass',IntSubclass(0))):
            mutation('outer_int_'+str(i)+'_'+label, lambda v,i=i,bad=bad:v.__setitem__(i,bad), 'invalid_guard_integer')
    for i in (2,6):
        mutation('outer_bool_'+str(i), lambda v,i=i:v.__setitem__(i,0), 'invalid_guard_boolean')
    for i in (0,1,2,3,6):
        mutation('inner_string_'+str(i), lambda v,i=i:v[10][0].__setitem__(i,None), 'invalid_trigger_string')
    mutation('inner_bool', lambda v:v[10][0].__setitem__(4,1), 'invalid_trigger_boolean')
    for label,bad in (('tuple',()),('scalar','a=b'),('mixed',['a=b',None]),('subclass',ListSubclass()),('str_subclass',[StrSubclass('a=b')])):
        mutation('outer_config_'+label, lambda v,bad=bad:v.__setitem__(7,bad), 'invalid_guard_config')
        mutation('inner_config_'+label, lambda v,bad=bad:v[10][0].__setitem__(5,bad), 'invalid_trigger_config')
    mutation('inventory_tuple', lambda v:v.__setitem__(10,tuple(v[10])), 'invalid_inventory')
    mutation('inventory_subclass', lambda v:v.__setitem__(10,ListSubclass(v[10])), 'invalid_inventory')
    mutation('trigger_tuple', lambda v:v[10].__setitem__(0,tuple(v[10][0])), 'invalid_trigger_shape')
    mutation('trigger_subclass', lambda v:v[10].__setitem__(0,ListSubclass(v[10][0])), 'invalid_trigger_shape')
    mutation('outer_str_subclass', lambda v:v.__setitem__(0,StrSubclass('A')), 'invalid_guard_string')
    mutation('inner_str_subclass', lambda v:v[10][0].__setitem__(0,StrSubclass('z_callback')), 'invalid_trigger_string')
    mutation('duplicate_unrelated', lambda v:v[10].append(deepcopy(v[10][0])), 'duplicate_trigger_identity')
    mutation('duplicate_named', lambda v:v[10].append(deepcopy(v[10][1])), 'duplicate_trigger_identity')
    mutation('wrong_schema', lambda v:v.__setitem__(4,'other'), 'guard_identity_mismatch')
    mutation('wrong_function', lambda v:v.__setitem__(5,'other'), 'guard_identity_mismatch')
    mutation('other_operation_trigger', lambda v:v[10][1].__setitem__(0,'_cryptalis_00000000000000000000000000000000_pause'), 'guard_identity_incomplete')
    mutation('late_invalid_entry', lambda v:v[10].append(['later','A','d','b',False,42,'o']), 'invalid_trigger_config')
    for label,value,code in mutations:
        check('reject:'+label, lambda value=value,code=code:inspect(value, CONTEXT, code))
    check('reject:outer_tuple', lambda:inspect(tuple(deepcopy(EXPECTED)),CONTEXT,'invalid_guard_shape'))
    check('reject:outer_subclass', lambda:inspect(ListSubclass(deepcopy(EXPECTED)),CONTEXT,'invalid_guard_shape'))
    contexts = [
      ('missing', {'schema':'lab'}, 'invalid_context_members'),
      ('extra', dict(CONTEXT, owner='untrusted'), 'invalid_context_members'),
      ('subclass', DictSubclass(CONTEXT), 'invalid_context_members'),
      ('nonstring_schema', dict(CONTEXT,schema=None), 'invalid_context_string'),
      ('nonstring_operation', dict(CONTEXT,operation_id=123), 'invalid_context_string'),
      ('str_subclass',dict(CONTEXT,schema=StrSubclass('lab')),'invalid_context_string'),
      ('bad_uuid',dict(CONTEXT,operation_id='invalid'),'invalid_operation_id'),
      ('compact_uuid',dict(CONTEXT,operation_id='12345678123456789abc123456789abc'),'invalid_operation_id'),
      ('uppercase_uuid',dict(CONTEXT,operation_id='12345678-1234-5678-9ABC-123456789ABC'),'invalid_operation_id')]
    for label,context,code in contexts:
        for suffix,value in (('present',deepcopy(EXPECTED)),('absent',None)):
            check('reject:context_'+label+'_'+suffix, lambda value=value,context=context,code=code:inspect(value,context,code))
    assert len(records) == 74 and len({r['id'] for r in records}) == 74
    return records
