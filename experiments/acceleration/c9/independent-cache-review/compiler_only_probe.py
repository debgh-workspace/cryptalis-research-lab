"""No engine, connection, database, or Cryptalis imports; compiler-only cache probe."""
import json
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.psycopg import PGDialect_psycopg

T = sa.table('customer', sa.column('id', sa.Integer), sa.column('name', sa.Text))
VALUES = ('exact', 'snow')
def statement(case):
    kwargs = {'type_': sa.Text(), 'expanding': True}
    if case != 'missing':
        kwargs['value'] = VALUES
    if case == 'required-default':
        kwargs['required'] = True
    return sa.select(T.c.id).where(T.c.name.in_(sa.bindparam('needles', **kwargs)))

cases = ('missing', 'required-default', 'default-tuple')
statements = {case: statement(case) for case in cases}
keys = {case: stmt._generate_cache_key() for case, stmt in statements.items()}
dialect = PGDialect_psycopg()
result = {'sqlalchemy_version': sa.__version__, 'key_equalities': {}, 'cases': {}}
for a in cases:
    result['cases'][a] = {'required': keys[a].bindparams[0].required,
                          'value': keys[a].bindparams[0].value}
    for b in cases:
        result['key_equalities'][a + ' -> ' + b] = keys[a].key == keys[b].key
result['compiler_matrix'] = []
for original in cases:
    compiled = statements[original].compile(dialect=dialect, cache_key=keys[original])
    for incoming in cases:
        for supplied in (False, True):
            try:
                params = compiled.construct_params(
                    {'needles': VALUES} if supplied else {},
                    extracted_parameters=keys[incoming].bindparams)
                outcome = {'params': params}
            except Exception as exc:
                outcome = {'error_type': type(exc).__name__, 'code': getattr(exc, 'code', None),
                           'message': str(exc)}
            result['compiler_matrix'].append({'compiled_from': original, 'incoming': incoming,
                                              'supplied': supplied, **outcome})
# Exercise the exact in-memory cache lookup/store method, still no Engine or DB.
result['lookup_orders'] = []
for order in (cases, tuple(reversed(cases))):
    cache = {}
    receipts = []
    for case in order:
        parts = statements[case]._compile_w_cache(dialect, compiled_cache=cache, column_keys=[])
        compiled, extracted = parts[:2]
        try:
            params = compiled.construct_params({}, extracted_parameters=extracted)
            outcome = {'params': params}
        except Exception as exc:
            outcome = {'error_type': type(exc).__name__, 'code': getattr(exc, 'code', None)}
        receipts.append({'case': case, 'cache_status': parts[-1].name,
                         'cache_entries': len(cache), **outcome})
    result['lookup_orders'].append(receipts)
print(json.dumps(result, indent=2))
