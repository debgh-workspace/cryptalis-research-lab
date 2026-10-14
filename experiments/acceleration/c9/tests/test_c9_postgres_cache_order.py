"""Observe required/default cache order; no cache clearing or runtime changes.

A passing probe establishes protected baseline/candidate parity only. Native
cache-order mismatches remain explicit compatibility defects for review.
"""
import hashlib
import json
from uuid import UUID

import pytest
from sqlalchemy import event
from test_sqlalchemy_search import search_application, TENANT
from test_c9_postgres_gates import variant, rows, error_signature
from test_c9_postgres_guard_plans import statement_for

ORDERS = [('missing', 'default-tuple'), ('required-default', 'default-tuple'),
          ('default-tuple', 'missing'), ('default-tuple', 'required-default')]


def bind_snapshot(bind):
    value = bind.value
    if isinstance(value, UUID):
        value = str(value)
    elif isinstance(value, (tuple, list)):
        value = list(value)
    elif value is not None and not isinstance(value, (str, bool, int)):
        value = {'type': type(value).__name__}
    return {'key': bind.key, 'required': bind.required, 'expanding': bind.expanding,
            'value': value, 'identity': id(bind)}


def cache_snapshot(engine):
    cache = engine._compiled_cache
    if cache is None:
        return {'enabled': False, 'entries': []}
    entries = []
    for key, compiled in list(cache.items()):
        rendered = repr(key)
        binds = {name: bind_snapshot(bind) for name, bind in compiled.binds.items()}
        entries.append({'cache_key_repr': rendered,
            'cache_key_sha256': hashlib.sha256(rendered.encode()).hexdigest(),
            'compiled_identity': id(compiled), 'sql': str(compiled), 'binds': binds})
    return {'enabled': True, 'entries': entries}


@pytest.mark.parametrize('order', ORDERS, ids=['missing-default', 'required-default-default',
    'default-missing', 'default-required-default'])
def test_c9_required_default_cache_order_observations(order, monkeypatch, record_property):
    outcomes, user_keys = {}, {}
    for which in ('native', 'original', 'candidate'):
        with search_application(protected=which != 'native') as app:
            with app.sessions(tenant_id=TENANT) as session:
                session.add_all([app.Customer(id=UUID(int=1002), tenant_id=TENANT, name='exact', rank=2),
                                 app.Customer(id=UUID(int=1003), tenant_id=TENANT, name='雪😀', rank=3)])
                session.commit()
            traces = []
            for case in order:
                trace = {'case': case, 'variant': which, 'cursor': [], 'handle_error': []}
                statement, params = statement_for(app, case)
                key = statement._generate_cache_key()
                rendered = repr(key.key)
                trace['user_cache_key'] = {'identity': id(key.key), 'repr': rendered,
                    'sha256': hashlib.sha256(rendered.encode()).hexdigest(),
                    'binds': [bind_snapshot(bind) for bind in key.bindparams]}
                user_keys.setdefault(which, []).append(key.key)
                trace['cache_before'] = cache_snapshot(app.engine)
                def before(connection, cursor, sql, parameters, context, many):
                    trace['cursor'].append({'sql': sql, 'compiled_identity': id(context.compiled),
                        'cache_hit': getattr(context.cache_hit, 'name', str(context.cache_hit)),
                        'parameter_keys': sorted(parameters) if isinstance(parameters, dict) else None})
                def handle_error(context):
                    execution = context.execution_context
                    trace['handle_error'].append({'original_type': type(context.original_exception).__name__,
                        'sql': context.statement,
                        'cache_hit': getattr(getattr(execution, 'cache_hit', None), 'name', None),
                        'compiled_identity': id(execution.compiled) if execution is not None else None})
                event.listen(app.engine, 'before_cursor_execute', before)
                event.listen(app.engine, 'handle_error', handle_error)
                try:
                    with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session:
                        try:
                            result = rows(session, statement, params)
                            trace['outcome'] = ('rows', result)
                        except Exception as exc:
                            trace['outcome'] = ('error', error_signature(exc))
                        trace['session_state'] = {'active': session.is_active, 'in_transaction': session.in_transaction()}
                        session.rollback()
                finally:
                    event.remove(app.engine, 'before_cursor_execute', before)
                    event.remove(app.engine, 'handle_error', handle_error)
                trace['cache_after'] = cache_snapshot(app.engine)
                traces.append(trace)
            outcomes[which] = traces
            record_property('c9_cache_order_' + which, json.dumps(traces, default=str, sort_keys=True))
    # All variants and both ordered operations are observed before any verdict.
    record_property('c9_user_cache_keys_equal', json.dumps({which: values[0] == values[1]
                                                           for which, values in user_keys.items()}))
    mismatches = []
    for index, case in enumerate(order):
        original = outcomes['original'][index]['outcome']
        candidate = outcomes['candidate'][index]['outcome']
        native = outcomes['native'][index]['outcome']
        assert original == candidate, (case, original, candidate)
        for which in ('original', 'candidate'):
            trace = outcomes[which][index]
            if case == 'default-tuple':
                assert trace['outcome'] == ('rows', [(UUID(int=1002),), (UUID(int=1003),)])
                assert len(trace['cursor']) == 1
                assert ('ANY' in trace['cursor'][0]['sql']) == (which == 'candidate')
            else:
                assert trace['outcome'][0] == 'error'
                assert trace['outcome'][1][:3] == ('StatementError', 'InvalidRequestError', None)
                assert trace['cursor'] == []
        if native != original:
            mismatches.append({'case': case, 'native': native, 'protected': original})
    record_property('c9_open_native_compatibility_mismatches', json.dumps(mismatches, default=str))
    record_property('c9_qualification', 'OBSERVATION ONLY: native cache-order differences remain OPEN; no timing clearance')
