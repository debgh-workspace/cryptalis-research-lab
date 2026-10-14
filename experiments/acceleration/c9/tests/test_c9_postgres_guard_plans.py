"""C9 tuple-route guard and plan controls; untimed, coordinator wrapper only."""
from contextlib import contextmanager
from dataclasses import replace
import json
import os
import re
import time
from uuid import UUID

import psycopg
from psycopg import sql
import pytest
from sqlalchemy import Text, bindparam, event, func, select
from sqlalchemy.types import TypeDecorator

import cryptalis.sqlalchemy as integration
from cryptalis.crypto import Keyring
from test_c9_postgres_gates import apps, variant, rows, error_signature, TENANT, OTHER, VALUES

NEEDLES = ('exact', '雪😀') + tuple('absent-%d' % i for i in range(18))


@contextmanager
def cursor_observer(app):
    observations = []
    def before(connection, cursor, statement, parameters, context, many):
        observations.append((statement, parameters))
    event.listen(app.engine, 'before_cursor_execute', before)
    try:
        yield observations
    finally:
        event.remove(app.engine, 'before_cursor_execute', before)


def statement_for(app, case):
    C = app.Customer
    params = {'needles': NEEDLES}
    bind = bindparam('needles', expanding=True, type_=Text())
    predicate = C.name.in_(bind)
    if case == 'missing':
        params = {}
    elif case == 'required-default':
        predicate = C.name.in_(bindparam('needles', value=NEEDLES, required=True,
                                        expanding=True, type_=Text()))
        params = {}
    elif case == 'default-tuple':
        predicate = C.name.in_(bindparam('needles', value=NEEDLES, expanding=True, type_=Text()))
        params = {}
    elif case == 'not-in':
        predicate = C.name.not_in(bind)
    elif case == 'equality':
        predicate = C.name == bindparam('needles', type_=Text())
        params = {'needles': 'exact'}
    elif case == 'unsupported-expression':
        predicate = func.lower(C.name).in_(bind)
    elif case == 'custom-codec':
        class CustomText(TypeDecorator):
            impl = Text
            cache_ok = True
            def process_bind_param(self, value, dialect):
                return None if value is None else value.casefold()
        predicate = C.name.in_(bindparam('needles', expanding=True, type_=CustomText()))
    elif case == 'ambiguous':
        first = bindparam('needles', value=('absent', 'other'), expanding=True, type_=Text())
        second = bindparam('needles', value=NEEDLES, expanding=True, type_=Text())
        predicate = C.name.in_(first) & C.label.in_(second)
        params = {}
    return select(C.id).where(C.tenant_id == TENANT, predicate).order_by(C.id), params


@pytest.mark.parametrize('case', ['missing', 'required-default', 'default-tuple',
    'supplied-tuple', 'not-in', 'equality', 'unsupported-expression', 'custom-codec', 'ambiguous'])
def test_c9_gate4_tuple_admission_and_fallback_controls(apps, monkeypatch, case, record_property):
    outcomes = {}
    for which, app in apps.items():
        with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session, cursor_observer(app) as seen:
            statement, params = statement_for(app, case)
            try:
                outcome = ('rows', rows(session, statement, params))
            except Exception as exc:
                outcome = ('error', error_signature(exc))
            outcomes[which] = (outcome, [item[0] for item in seen])
            record_property('c9_admission_' + which, repr(outcomes[which]))
            session.rollback()
    # Preserve warm-cache outcomes from every variant before asserting any one.
    record_property('c9_admission_outcomes', repr(outcomes))
    assert outcomes['candidate'][0] == outcomes['original'][0]
    for which, (outcome, statements) in outcomes.items():
        if case in ('missing', 'required-default'):
            assert outcome[0] == 'error' and not statements
        elif which != 'native' and case in ('unsupported-expression', 'custom-codec', 'ambiguous'):
            assert outcome[0] == 'error'
            assert outcome[1][0] == 'UnsupportedProtectedOperation' and not statements
        else:
            assert outcome[0] == 'rows' and len(statements) == 1, (which, outcome)
            assert ('ANY' in statements[0]) == (which == 'candidate' and case in ('default-tuple', 'supplied-tuple'))
    if case in ('default-tuple', 'supplied-tuple', 'not-in', 'equality'):
        assert outcomes['candidate'][0] == outcomes['native'][0]


@pytest.mark.parametrize('fault', ['pid', 'tenant', 'lease'])
def test_c9_gate4_tuple_bind_revalidates_prepared_context(apps, monkeypatch, fault, record_property):
    outcomes = {}
    for which in ('original', 'candidate'):
        app = apps[which]
        healthy = app.rings[TENANT]
        if fault == 'lease':
            app.rings[TENANT] = Keyring(healthy.policy, {app.provider.provider_id: app.provider}, max_age=.02)
        rewritten = []
        def inject(connection, statement, multiparams, params, options):
            from sqlalchemy.sql import visitors
            from sqlalchemy.sql.elements import BindParameter
            nodes = [n for n in visitors.iterate(statement)
                     if isinstance(n, BindParameter) and hasattr(n.type, 'binding')]
            assert len(nodes) == 1
            rewritten.append(type(nodes[0].type).__name__)
            if fault == 'pid':
                nodes[0].type.keys = replace(nodes[0].type.keys, _pid=-1)
            elif fault == 'tenant':
                nodes[0].type.tenant = OTHER
            else:
                # Actual short lease, not a fake clock or measured benchmark.
                time.sleep(.04)
            return statement, multiparams, params
        try:
            with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session, cursor_observer(app) as seen:
                event.listen(app.engine, 'before_execute', inject, retval=True)
                try:
                    statement, params = statement_for(app, 'supplied-tuple')
                    with pytest.raises(Exception) as caught:
                        rows(session, statement, params)
                    signature = error_signature(caught.value)
                    assert signature[:3] == ('StatementError', 'KeyUnavailable', None)
                    assert seen == []
                    outcomes[which] = signature
                finally:
                    event.remove(app.engine, 'before_execute', inject)
                    session.rollback()
        finally:
            app.rings[TENANT] = healthy
        assert rewritten == ['_SearchTerms' if which == 'candidate' else '_SearchValue']
        # No poisoned prepared/batch state may survive into the next operation.
        with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session:
            assert rows(session, *statement_for(app, 'supplied-tuple')) == [
                (UUID(int=1002),), (UUID(int=1003),), (UUID(int=1007),)]
    assert outcomes['candidate'] == outcomes['original']
    record_property('c9_prepared_context_outcomes', repr(outcomes))


def test_c9_gate4_final_cursor_policy_check_after_tuple_processing(apps, monkeypatch, record_property):
    outcomes = {}
    for which in ('original', 'candidate'):
        app, before, after = apps[which], [], []
        original_setting = app.engine.hide_parameters
        def late(connection, cursor, statement, parameters, context, many):
            before.append(statement)
            app.engine.hide_parameters = False
        def completed(*args):
            after.append(True)
        with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session:
            event.listen(app.engine, 'before_cursor_execute', late)
            event.listen(app.engine, 'after_cursor_execute', completed)
            try:
                with pytest.raises(Exception) as caught:
                    rows(session, *statement_for(app, 'supplied-tuple'))
                signature = error_signature(caught.value)
                assert signature[0] == 'PolicyMismatch'
                assert len(before) == 1 and after == []
                assert ('ANY' in before[0]) == (which == 'candidate')
                outcomes[which] = signature
            finally:
                app.engine.hide_parameters = original_setting
                event.remove(app.engine, 'before_cursor_execute', late)
                event.remove(app.engine, 'after_cursor_execute', completed)
                session.rollback()
    assert outcomes['candidate'] == outcomes['original']
    record_property('c9_final_cursor_outcomes', repr(outcomes))


def test_c9_gate4_returned_payload_still_resolves_keys_after_tuple_query(apps, monkeypatch, record_property):
    import cryptalis.crypto.keys as keymod
    outcomes = {}
    for which in ('original', 'candidate'):
        app, phase = apps[which], {'returned': False, 'resolves': []}
        resolve = keymod.PreparedKeys._resolve
        def resolved(self, domain, tenant, purpose, generation):
            phase['resolves'].append((phase['returned'], purpose))
            if phase['returned'] and purpose == 'payload':
                from cryptalis.crypto import KeyUnavailable
                raise KeyUnavailable()
            return resolve(self, domain, tenant, purpose, generation)
        def completed(*args):
            phase['returned'] = True
        with monkeypatch.context() as patch:
            patch.setattr(keymod.PreparedKeys, '_resolve', resolved)
            with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session, cursor_observer(app) as seen:
                event.listen(app.engine, 'after_cursor_execute', completed)
                try:
                    C = app.Customer
                    query = select(C.id, C.name).where(C.tenant_id == TENANT,
                        C.name.in_(bindparam('needles', expanding=True, type_=Text()))).order_by(C.id)
                    with pytest.raises(Exception) as caught:
                        rows(session, query, {'needles': NEEDLES})
                    signature = error_signature(caught.value)
                    assert signature[1] == 'KeyUnavailable'
                    assert len(seen) == 1 and ('ANY' in seen[0][0]) == (which == 'candidate')
                    assert (True, 'payload') in phase['resolves']
                    outcomes[which] = signature
                finally:
                    event.remove(app.engine, 'after_cursor_execute', completed)
                    session.rollback()
    assert outcomes['candidate'] == outcomes['original']
    record_property('c9_returned_payload_outcomes', repr(outcomes))


def prepared_sql(statement):
    names = []
    def replace_bind(match):
        name = match.group(1)
        if name not in names:
            names.append(name)
        return '$' + str(names.index(name) + 1)
    return re.sub(r'%\(([^)]+)\)s', replace_bind, statement), names


@pytest.mark.parametrize('mode', ['force_custom_plan', 'force_generic_plan'])
@pytest.mark.parametrize('needles', [NEEDLES, ('exact', None) * 10, (None,) * 20],
                         ids=['hot20', 'mixed-null20', 'all-null20'])
def test_c9_gate5_custom_generic_plans_and_driver_adaptation(apps, monkeypatch, mode, needles, record_property):
    receipts, results = {}, {}
    for which, app in apps.items():
        with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session, cursor_observer(app) as seen:
            query, _ = statement_for(app, 'supplied-tuple')
            results[which] = rows(session, query, {'needles': needles})
        assert len(seen) == 1
        statement, parameters = seen[0]
        assert ('ANY' in statement) == (which == 'candidate')
        prepared, names = prepared_sql(statement)
        assert names and '%' not in prepared
        arguments = [parameters[name] for name in names]
        if which == 'candidate':
            arrays = [value for value in arguments if isinstance(value, list)]
            assert len(arrays) == 1 and len(arrays[0]) == 20
            # ARRAY(LargeBinary) applies the DBAPI Binary adapter to each
            # non-NULL byte string. Keep SQL NULL independent and unchanged.
            assert [value is None for value in arrays[0]] == [value is None for value in needles]
            decoded = []
            for value in arrays[0]:
                if value is None:
                    decoded.append(None)
                else:
                    assert type(value) in (bytes, psycopg.Binary), type(value).__name__
                    body = value.obj if type(value) is psycopg.Binary else value
                    assert type(body) is bytes and len(body) == 32
                    decoded.append(body)
            record_property('c9_array_adaptation', json.dumps({
                'element_types': [type(value).__name__ for value in arrays[0]],
                'null_mask': [value is None for value in arrays[0]]}))
        # Independent runtime-role diagnostic connection. No attached-engine
        # policy mutation or forced index use; EXPLAIN does not execute the query.
        with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as connection:
            if which == 'candidate':
                roundtrip = connection.execute('SELECT %s::bytea[]', (arrays[0],)).fetchone()[0]
                assert roundtrip == decoded
            connection.execute('SET LOCAL plan_cache_mode = ' + mode)
            connection.execute('PREPARE c9_plan AS ' + prepared)
            execute = sql.SQL('EXECUTE c9_plan({})').format(
                sql.SQL(', ').join(sql.Literal(value) for value in arguments))
            plan = connection.execute(sql.SQL('EXPLAIN (FORMAT JSON) ') + execute).fetchone()[0]
            native_rows = connection.execute(execute).fetchall()
            assert native_rows == results[which]
            counters = connection.execute("SELECT generic_plans, custom_plans FROM pg_prepared_statements WHERE name='c9_plan'").fetchone()
            assert counters[0 if mode == 'force_generic_plan' else 1] >= 2
            assert counters[1 if mode == 'force_generic_plan' else 0] == 0
            indexes = connection.execute('SELECT indexname, indexdef FROM pg_indexes WHERE schemaname = %s ORDER BY indexname', (app.schema,)).fetchall()
            if which != 'native':
                expected = [definition for name, definition in indexes if name == app.name_index_name]
                assert len(expected) == 1 and 'substring' in expected[0] and '15, 32' in expected[0]
            receipts[which] = {'mode': mode, 'plan': plan, 'prepared_counts': counters,
                'indexes': indexes, 'parameter_types': [type(value).__name__ for value in arguments],
                'row_ids': [str(row[0]) for row in native_rows]}
    assert results['candidate'] == results['original'] == results['native']
    record_property('c9_plan_receipt', json.dumps(receipts, sort_keys=True))


def test_c9_gate5_native_driver_invalid_text_failure(apps, monkeypatch, record_property):
    outcomes = {}
    with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as connection:
        try:
            connection.execute('SELECT %s::text = ANY(%s::text[])', ('exact', ['exact', '\x00'])).fetchall()
        except Exception as exc:
            outcomes['driver_any'] = (error_signature(exc), int(connection.info.transaction_status))
        else:
            pytest.fail('Native driver unexpectedly accepted NUL text')
    for which in ('native', 'original', 'candidate'):
        app = apps[which]
        with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session, cursor_observer(app) as seen:
            statement, _ = statement_for(app, 'supplied-tuple')
            with pytest.raises(Exception) as caught:
                rows(session, statement, {'needles': ('exact', '\x00')})
            outcomes[which] = (error_signature(caught.value), len(seen))
            if which != 'native':
                assert outcomes[which][0][:3] == ('StatementError', 'InvalidText', None)
                assert seen == []
            session.rollback()
    assert outcomes['candidate'] == outcomes['original']
    record_property('c9_native_failure_observations', repr(outcomes))
