"""Untimed C9 DB gates 1–3. Execute only through the authorized PG wrapper.

Original rewrite/term are loaded from frozen source, never installed on disk.
No gate in this file constitutes a timing, full safety, or plan qualification.
"""
import ast
from contextlib import ExitStack, contextmanager
import hashlib
from pathlib import Path
from uuid import UUID

import psycopg
from psycopg import sql
import pytest
from sqlalchemy import Text, bindparam, event, select
from sqlalchemy.orm import aliased
from sqlalchemy.sql import visitors
from sqlalchemy.sql.elements import BindParameter

import cryptalis.crypto.cf1 as cf1
import cryptalis.sqlalchemy as integration
from test_sqlalchemy_search import search_application, TENANT, OTHER

ROOT = Path(__file__).resolve().parents[1]
FROZEN = {
    'src/cryptalis/_sqlalchemy_search.py': '9d3564b80470bb98383af461807969952adc8eb2a82217ec3681c6928d7a1391',
    'src/cryptalis/crypto/cf1.py': '3d34b066e8e2b5983fcc5c1180226e666a7ba0a5fcacb8888ce7adfa66e73ed3',
    'experiments/c9-baseline/_sqlalchemy_search.py': '857bb89d2f0aae0dc8b41f7c14bcc9dcd5285640fbe0969fbd8421ef2059ee63',
    'experiments/c9-baseline/cf1.py': 'd74abd2558023bf5ce1598fba0b61bb27198623dc56fb94ace24753531705278',
}
VALUES = (None, '', 'exact', '雪😀', 'é', 'e\u0301', 'missing', 'exact')
CASES = [(), (None,), (None, None), ('exact', None), ('exact', 'exact'),
         ('雪😀', 'é'), tuple('absent-%d' % i for i in range(20)),
         ('exact', '雪😀') + tuple('absent-%d' % i for i in range(18))]


@contextmanager
def variant(which, monkeypatch):
    if which != 'original':
        yield
        return
    path = ROOT / 'experiments/c9-baseline/cf1.py'
    source = path.read_text()
    node = next(n for n in ast.parse(source).body
                if isinstance(n, ast.FunctionDef) and n.name == 'equality_term')
    space = dict(vars(cf1))
    exec(compile(ast.get_source_segment(source, node), str(path), 'exec'), space)
    path = ROOT / 'experiments/c9-baseline/_sqlalchemy_search.py'
    original = {'__name__': 'cryptalis._c9_db_original', '__package__': 'cryptalis'}
    exec(compile(path.read_text(), str(path), 'exec'), original)
    original['equality_term'] = space['equality_term']
    with monkeypatch.context() as patch:
        patch.setattr(integration, 'rewrite_search', original['rewrite_search'])
        yield


@pytest.fixture(scope='module')
def apps():
    for name, expected in FROZEN.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name
    with ExitStack() as stack:
        result = {name: stack.enter_context(search_application(
            protected=name != 'native', two_fields=True))
            for name in ('native', 'original', 'candidate')}
        for app in result.values():
            for offset, tenant in enumerate((TENANT, OTHER)):
                with app.sessions(tenant_id=tenant) as session:
                    session.add_all([app.Customer(
                        id=UUID(int=1000 + offset * 100 + rank), tenant_id=tenant,
                        name=value, other_name=VALUES[(rank + 2) % len(VALUES)],
                        label=value, rank=rank) for rank, value in enumerate(VALUES)])
                    session.commit()
        yield result


def rows(session, statement, params):
    result = session.execute(statement, params)
    try:
        return [tuple(row) for row in result.all()]
    finally:
        result.close()


def driver_truth(app, tenant, values):
    # Independent psycopg adaptation and PostgreSQL text[] truth oracle.
    # A native fixture connection is used; no attached-engine escape route.
    with app.engine.connect() as connection:
        cursor = connection.connection.driver_connection.cursor()
        try:
            cursor.execute(sql.SQL('SELECT id, name = ANY(%s::text[]), '
                                   'other_name = ANY(%s::text[]), label = ANY(%s::text[]) '
                                   'FROM {}.customer WHERE tenant_id = %s ORDER BY id')
                           .format(sql.Identifier(app.schema)),
                           (list(values), list(values), list(values), tenant))
            return cursor.fetchall()
        finally:
            cursor.close()


@pytest.mark.parametrize('values', CASES, ids=['empty', 'null', 'all-null', 'mixed',
    'duplicates', 'unicode', 'miss20', 'hot20'])
@pytest.mark.parametrize('use_alias', [False, True], ids=['direct', 'alias'])
@pytest.mark.parametrize('tenant', [TENANT, OTHER], ids=['tenant1', 'tenant2'])
def test_c9_gate1_truth_rows_shared_fields_and_pagination(apps, monkeypatch, values, use_alias, tenant):
    oracle = driver_truth(apps['native'], tenant, values)
    outcomes = {}
    for which, app in apps.items():
        with variant(which, monkeypatch), app.sessions(tenant_id=tenant) as session:
            C = aliased(app.Customer) if use_alias else app.Customer
            shared = bindparam('needles', expanding=True, type_=Text())
            p, q, r = C.name.in_(shared), C.other_name.in_(shared), C.label.in_(shared)
            params = {'needles': values}
            projected = rows(session, select(C.id, p, q, r).where(C.tenant_id == tenant).order_by(C.id), params)
            assert projected == oracle
            ids = rows(session, select(C.id).where(C.tenant_id == tenant, p, p).order_by(C.id), params)
            assert ids == [(row[0],) for row in oracle if row[1] is True]
            payload = rows(session, select(C.id, C.name, C.other_name).where(C.tenant_id == tenant, p).order_by(C.id), params)
            result = session.execute(select(C).where(C.tenant_id == tenant, p).order_by(C.id), params)
            try:
                entities = [(row.id, row.name, row.other_name) for row in result.scalars().all()]
            finally:
                result.close()
            assert entities == payload
            page = rows(session, select(C.id).where(C.tenant_id == tenant, p,
                        C.id > UUID(int=1001)).order_by(C.id).limit(2), params)
            assert page == [row for row in ids if row[0] > UUID(int=1001)][:2]
            outcomes[which] = (projected, ids, payload, entities, page)
    assert outcomes['candidate'] == outcomes['original'] == outcomes['native']


@pytest.mark.parametrize('values', [('exact',) * 20, ('exact', None) * 10,
                                  (None,) * 20, ['exact'] * 20],
                         ids=['tuple20', 'mixed20', 'null20', 'list20'])
def test_c9_gate1_actual_cursor_path_and_search_derivations(apps, monkeypatch, values):
    counts, outcomes = {}, {}
    for which in ('original', 'candidate'):
        app, calls, statements = apps[which], [], []
        derive = cf1._derive
        def observed(material, info):
            calls.append(material.context.purpose)
            return derive(material, info)
        def cursor(connection, raw, statement, parameters, context, many):
            statements.append(statement)
        with monkeypatch.context() as patch:
            patch.setattr(cf1, '_derive', observed)
            with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session:
                event.listen(app.engine, 'before_cursor_execute', cursor)
                try:
                    C = app.Customer
                    outcomes[which] = rows(session, select(C.id).where(C.tenant_id == TENANT,
                        C.name.in_(bindparam('needles', expanding=True, type_=Text()))).order_by(C.id),
                        {'needles': values})
                finally:
                    event.remove(app.engine, 'before_cursor_execute', cursor)
        assert len(statements) == 1
        expected_any = which == 'candidate' and type(values) is tuple
        assert ('ANY' in statements[0]) == expected_any
        assert (' IN (' in statements[0]) == (not expected_any)
        assert all(purpose == 'search' for purpose in calls)
        counts[which] = len(calls)
    nonnull = sum(value is not None for value in values)
    assert counts == {'original': nonnull, 'candidate': min(nonnull, 1) if type(values) is tuple else nonnull}
    assert outcomes['candidate'] == outcomes['original']


def error_signature(exc):
    original = getattr(exc, 'orig', exc)
    return (type(exc).__name__, type(original).__name__, getattr(original, 'sqlstate', None),
            tuple(getattr(original, key, None) for key in ('code', 'stage', 'remedy', 'retryable', 'effects')))


def late_outcome(app, which, monkeypatch, factory, *, mutate=False, shared=False):
    observed, connections = [], []
    initial = ['exact'] * 20 if mutate else ('exact',) * 20
    def late(connection, statement, multiparams, params, options):
        connections.append(connection)
        protected = [node for node in visitors.iterate(statement)
                     if isinstance(node, BindParameter) and hasattr(node.type, 'binding')]
        if mutate:
            factory(initial)
        elif which == 'native':
            params = dict(params, needles=factory())
        else:
            assert len(protected) == 1
            protected[0].value = factory()
        return statement, multiparams, params
    def cursor(connection, raw, statement, parameters, context, many):
        observed.append(statement)
    with variant(which, monkeypatch), app.sessions(tenant_id=TENANT) as session:
        event.listen(app.engine, 'before_execute', late, retval=True)
        event.listen(app.engine, 'before_cursor_execute', cursor)
        try:
            C = app.Customer
            bind = bindparam('needles', expanding=True, type_=Text())
            projections = [C.id, C.name.in_(bind)]
            if shared:
                projections += [C.name.in_(bind), C.other_name.in_(bind), C.label.in_(bind)]
            statement = select(*projections).where(C.tenant_id == TENANT).order_by(C.id)
            try:
                outcome = ('rows', rows(session, statement, {'needles': initial}))
            except Exception as exc:
                outcome = ('error', error_signature(exc))
            state = (session.is_active, session.in_transaction(),
                     int(connections[-1].connection.driver_connection.info.transaction_status)
                     if connections else None)
        finally:
            event.remove(app.engine, 'before_execute', late)
            event.remove(app.engine, 'before_cursor_execute', cursor)
            session.rollback()
    return outcome, state, observed


def assert_strict_integer_boundary(outcomes, record_property, *, shared=False):
    """Require the observed native coercion and unchanged strict codec refusal.

    This is an explicit incompatibility control, NOT native equivalence. Keep
    every admitted-input/native comparison in the callers unchanged.
    """
    expected_error = ('error', ('StatementError', 'InvalidText', None,
        ('InvalidText', 'text encoding',
         'Supply strict UTF-8 text without NUL, at most 16 MiB encoded, or SQL NULL.',
         False, 'none')))
    for which in ('original', 'candidate'):
        assert outcomes[which] == (expected_error, (True, True, 0), [])
    def coerced_truth(value):
        return None if value is None else value in ('exact', '7')
    expected = []
    for rank, value in enumerate(VALUES):
        row = (UUID(int=1000 + rank), coerced_truth(value))
        if shared:
            row += (coerced_truth(value),
                    coerced_truth(VALUES[(rank + 2) % len(VALUES)]), coerced_truth(value))
        expected.append(row)
    assert outcomes['native'][0] == ('rows', expected)
    assert outcomes['native'][1] == (True, True, 2)
    assert len(outcomes['native'][2]) == 1
    assert ' IN (' in outcomes['native'][2][0] and 'ANY' not in outcomes['native'][2][0]
    record_property('c9_native_relation',
        'EXPLICIT MISMATCH: native integer-to-text coercion succeeds; '
        'original and candidate identically refuse InvalidText before SQL')


REPLACEMENTS = [lambda: ('雪😀', None), lambda: ['雪😀', None], lambda: (), lambda: [],
                lambda: None, lambda: False, lambda: ('exact', 7),
                lambda: iter(['exact', None]), lambda: ('exact', '\x00')]


@pytest.mark.parametrize('factory, strict_integer',
    [(factory, index == 6) for index, factory in enumerate(REPLACEMENTS)], ids=['tuple', 'list', 'empty-tuple',
    'empty-list', 'none', 'false', 'invalid-int', 'iterator', 'invalid-nul'])
def test_c9_gate2_late_replacement_exact_truth_errors_and_transaction(apps, monkeypatch, factory, strict_integer, record_property):
    outcomes = {which: late_outcome(apps[which], which, monkeypatch, factory)
                for which in ('native', 'original', 'candidate')}
    record_property('c9_outcomes', repr(outcomes))
    # Protected semantic and exception category/SQLSTATE/state must be unchanged.
    assert outcomes['candidate'][:2] == outcomes['original'][:2]
    for which in ('original', 'candidate'):
        for statement in outcomes[which][2]:
            assert ('ANY' in statement) == (which == 'candidate')
    # Native outcomes are retained in failures; invalid text/member rejection is
    # intentionally a product boundary and need not share native exception types.
    if strict_integer:
        assert_strict_integer_boundary(outcomes, record_property)
    elif outcomes['native'][0][0] == 'rows':
        assert outcomes['candidate'][0] == outcomes['native'][0]


@pytest.mark.parametrize('mutation, strict_integer', [(lambda value: value.append('雪😀'), False),
    (lambda value: value.clear(), False), (lambda value: value.append(7), True)],
    ids=['grow21', 'clear', 'invalid'])
@pytest.mark.parametrize('shared', [False, True], ids=['single', 'shared-fields-native'])
def test_c9_gate3_mutable_list_keeps_expanding(apps, monkeypatch, mutation, strict_integer, shared, record_property):
    outcomes = {which: late_outcome(apps[which], which, monkeypatch, mutation, mutate=True, shared=shared)
                for which in ('native', 'original', 'candidate')}
    record_property('c9_outcomes', repr(outcomes))
    assert outcomes['candidate'][:2] == outcomes['original'][:2]
    for which in ('original', 'candidate'):
        for statement in outcomes[which][2]:
            assert 'ANY' not in statement and ' IN (' in statement
    if strict_integer:
        assert_strict_integer_boundary(outcomes, record_property, shared=shared)
    elif outcomes['native'][0][0] == 'rows':
        assert outcomes['candidate'][0] == outcomes['native'][0]
