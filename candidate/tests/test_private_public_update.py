"""Native differential oracle for the off-by-default public UPDATE experiment.

The target is a disposable fully public table beside the protected table. This
suite does not admit protected-field bulk UPDATE or a production capability.
"""
from contextlib import contextmanager
from uuid import UUID

import pytest
from sqlalchemy import (Column, Integer, Table, Text, Uuid, bindparam, event,
                        func, inspect, select, update)
from sqlalchemy.orm import sessionmaker

from cryptalis.sqlalchemy import UnsupportedProtectedOperation, attach
from test_migration import application, run, publish, keys, TENANT


@contextmanager
def public_update_application(*, effect=None, mapped_onupdate=False):
    with application() as app:
        table = Table('public_task', app.mapping.metadata,
                      Column('id', Uuid, primary_key=True, autoincrement=False),
                      Column('label', Text, onupdate='implicit' if mapped_onupdate else None),
                      Column('rank', Integer))
        class PublicTask:
            pass
        app.mapping.map_imperatively(PublicTask, table)
        table.create(app.owner)
        with app.owner.begin() as connection:
            q = connection.dialect.identifier_preparer.quote_identifier
            target = q(app.schema) + '.public_task'
            connection.exec_driver_sql('GRANT SELECT, INSERT, UPDATE, DELETE ON ' + target + ' TO ' + q(app.role))
            if effect == 'check':
                connection.exec_driver_sql('ALTER TABLE ' + target + ' ADD CHECK (rank >= 0)')
            elif effect == 'expression_index':
                connection.exec_driver_sql('CREATE INDEX public_task_lower ON ' + target + ' (lower(label))')
            elif effect == 'partial_index':
                connection.exec_driver_sql('CREATE INDEX public_task_partial ON ' + target + ' (rank) WHERE rank > 0')
            elif effect == 'generated':
                connection.exec_driver_sql('ALTER TABLE ' + target + ' ADD COLUMN doubled integer GENERATED ALWAYS AS (rank * 2) STORED')
            elif effect == 'outgoing_fk':
                connection.exec_driver_sql('CREATE TABLE ' + q(app.schema) + '.public_parent (id uuid PRIMARY KEY)')
                connection.exec_driver_sql('ALTER TABLE ' + target + ' ADD COLUMN parent_id uuid REFERENCES ' + q(app.schema) + '.public_parent(id)')
            elif effect == 'incoming_fk':
                connection.exec_driver_sql('CREATE TABLE ' + q(app.schema) + '.public_ref (id uuid REFERENCES ' + target + '(id))')
            elif effect == 'rls':
                connection.exec_driver_sql('ALTER TABLE ' + target + ' ENABLE ROW LEVEL SECURITY')
        with sessionmaker(app.runtime)() as session:
            session.add_all(PublicTask(id=UUID(int=2000+i), label=value, rank=i)
                           for i, value in enumerate([None, '', 'old-2', '雪', 'last']))
            session.commit()
        app.public_table, app.PublicTask = table, PublicTask
        yield app


def protect(app, *, optin=True):
    run(app); publish(app)
    factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                     keys=keys, deployment=(app.plan, app.pin))
    if optin:
        factory._owner._experimental_public_update_tables = (app.public_table,)
    return factory


def values(session, model):
    return [tuple(row) for row in session.execute(select(model.id, model.label, model.rank).order_by(model.id))]


@pytest.mark.parametrize('synchronize', ['auto', 'fetch', 'evaluate', False])
@pytest.mark.parametrize('outcome', ['commit', 'rollback', 'savepoint'])
def test_public_update_matches_native_state_and_transaction(synchronize, outcome):
    with public_update_application() as app:
        P = app.PublicTask
        statement = update(P).where(P.rank.in_([1, 2, 3])).values(label='updated 雪').execution_options(synchronize_session=synchronize)
        with sessionmaker(app.runtime)() as session:
            original = values(session, P)
            loaded = list(session.scalars(select(P).order_by(P.id)))
            expected_count = session.execute(statement).rowcount
            expected_loaded = [(p.id, p.label, inspect(p).expired) for p in loaded]
            expected_rows = values(session, P)
            session.rollback()
        factory = protect(app)
        with factory(tenant_id=TENANT) as session:
            loaded = list(session.scalars(select(P).order_by(P.id)))
            nested = session.begin_nested() if outcome == 'savepoint' else None
            result = session.execute(statement)
            assert result.rowcount == expected_count == 3
            assert [(p.id, p.label, inspect(p).expired) for p in loaded] == expected_loaded
            assert values(session, P) == expected_rows
            if outcome == 'commit':
                session.commit()
            elif nested is not None:
                nested.rollback(); session.commit()
            else:
                session.rollback()
            assert values(session, P) == (expected_rows if outcome == 'commit' else original)
            assert len(list(session.scalars(select(app.Customer)))) == len(app.source)


@pytest.mark.parametrize('returning', ['columns', 'entity'])
@pytest.mark.parametrize('synchronize', ['fetch', 'auto'])
def test_public_update_returning_matches_native(returning, synchronize):
    with public_update_application() as app:
        P = app.PublicTask
        statement = update(P).where(P.rank < 3).values(label=None).execution_options(synchronize_session=synchronize)
        statement = statement.returning(P.id, P.label) if returning == 'columns' else statement.returning(P)
        def consume(session):
            result = session.execute(statement)
            labels = list(result.keys())
            rows = ([tuple(row) for row in result] if returning == 'columns'
                    else [(row.id, row.label, row.rank, inspect(row).persistent) for row in result.scalars()])
            return labels, sorted(rows)
        with sessionmaker(app.runtime)() as session:
            expected = consume(session)
            session.rollback()
        factory = protect(app)
        with factory(tenant_id=TENANT) as session:
            assert consume(session) == expected
            session.rollback()


@pytest.mark.parametrize('core', [False, True])
def test_public_update_repeated_typed_binds_and_empty_set(core):
    with public_update_application() as app:
        P = app.PublicTask
        target = app.public_table if core else P
        statement = update(target).where(app.public_table.c.id == bindparam('chosen', type_=Uuid)).values(label=bindparam('replacement', type_=Text))
        runs = [{'chosen': UUID(int=2001), 'replacement': 'first'},
                {'chosen': UUID(int=2002), 'replacement': 'second'},
                {'chosen': UUID(int=9999), 'replacement': 'absent'}]
        def exercise(session):
            counts = [session.execute(statement, parameters).rowcount for parameters in runs]
            counts.append(session.execute(update(target).where(app.public_table.c.id.in_([])).values(label='none')).rowcount)
            return counts, values(session, P)
        with sessionmaker(app.runtime)() as session:
            expected = exercise(session); session.rollback()
        assert expected[0] == [1, 1, 0, 0]
        factory = protect(app)
        with factory(tenant_id=TENANT) as session:
            assert exercise(session) == expected
            session.rollback()
            assert exercise(session) == expected
            session.rollback()


@pytest.mark.parametrize('shape', ['no_optin', 'protected_table', 'primary_key', 'expression', 'parameters', 'column_named_where_bind', 'executemany'])
def test_public_update_unadmitted_forms_emit_no_update(shape):
    with public_update_application() as app:
        factory = protect(app, optin=shape != 'no_optin')
        P = app.PublicTask
        statement = update(P).where(P.rank == 2).values(label='changed')
        parameters = None
        if shape == 'protected_table':
            factory._owner._experimental_public_update_tables = (app.public_table, app.table)
            statement = update(app.Customer).where(app.Customer.id == UUID(int=102)).values(label='changed')
        elif shape == 'primary_key':
            statement = update(P).where(P.rank == 2).values(id=UUID(int=9999))
        elif shape == 'expression':
            statement = update(P).values(label=func.upper(P.label))
        elif shape == 'parameters':
            parameters = {'rank': 99}
        elif shape == 'column_named_where_bind':
            statement = update(P).where(P.rank == bindparam('rank', type_=Integer)).values(label='changed')
            parameters = {'rank': 2}
        elif shape == 'executemany':
            parameters = [{'id': UUID(int=2002), 'label': 'changed'}]
        emitted = []
        def observe(conn, cursor, sql, *rest):
            if sql.lstrip().upper().startswith('UPDATE '): emitted.append(True)
        event.listen(app.runtime, 'before_cursor_execute', observe)
        with factory(tenant_id=TENANT) as session:
            with pytest.raises(UnsupportedProtectedOperation): session.execute(statement, parameters)
            session.rollback()
        assert emitted == []
        with app.owner.connect() as connection:
            assert connection.exec_driver_sql('SELECT label, rank FROM "' + app.schema + '".public_task WHERE id=%s', (UUID(int=2002),)).one() == ('old-2', 2)


@pytest.mark.parametrize('effect', ['check', 'expression_index', 'partial_index', 'generated', 'outgoing_fk', 'incoming_fk'])
def test_public_update_effect_inventory_refuses_before_update(effect):
    with public_update_application(effect=effect) as app:
        factory = protect(app)
        emitted = []
        def observe(conn, cursor, sql, *rest):
            if sql.lstrip().upper().startswith('UPDATE '): emitted.append(True)
        event.listen(app.runtime, 'before_cursor_execute', observe)
        with factory(tenant_id=TENANT) as session:
            with pytest.raises(UnsupportedProtectedOperation):
                session.execute(update(app.PublicTask).where(app.PublicTask.rank == 2).values(label='changed'))
            session.rollback()
        assert emitted == []


def test_public_update_mapped_onupdate_refuses_before_update():
    with public_update_application(mapped_onupdate=True) as app:
        factory = protect(app)
        with factory(tenant_id=TENANT) as session:
            with pytest.raises(UnsupportedProtectedOperation):
                session.execute(update(app.PublicTask).values(rank=99))
            session.rollback()


@pytest.mark.parametrize('outcome', ['commit', 'rollback', 'savepoint'])
@pytest.mark.parametrize('returning', ['none', 'columns', 'entity'])
def test_async_public_update_matches_native(outcome, returning):
    import asyncio
    import os
    import psycopg
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    with public_update_application() as app:
        P = app.PublicTask
        statement = update(P).where(P.rank < 3).values(label='async 雪').execution_options(synchronize_session='fetch')
        if returning == 'columns': statement = statement.returning(P.id, P.label)
        if returning == 'entity': statement = statement.returning(P)
        async def scenario(protected):
            engine = create_async_engine('postgresql+psycopg://', hide_parameters=True,
                async_creator=lambda: psycopg.AsyncConnection.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
            try:
                if protected:
                    factory = await attach(app.mapping, engine, lock=app.plan.lock_bytes,
                                           keys=keys, deployment=(app.plan, app.pin))
                    factory._owner._experimental_public_update_tables = (app.public_table,)
                    session = factory(tenant_id=TENANT)
                else:
                    session = async_sessionmaker(engine)()
                async with session:
                    original = [tuple(row) for row in await session.execute(select(P.id, P.label, P.rank).order_by(P.id))]
                    loaded = list(await session.scalars(select(P).order_by(P.id)))
                    nested = await session.begin_nested() if protected and outcome == 'savepoint' else None
                    result = await session.execute(statement)
                    observed_result = (result.rowcount if returning == 'none' else
                        sorted(tuple(row) for row in result) if returning == 'columns' else
                        sorted((row.id, row.label, row.rank, inspect(row).persistent) for row in result.scalars()))
                    loaded_values = [(row.id, row.label) for row in loaded]
                    updated = [tuple(row) for row in await session.execute(select(P.id, P.label, P.rank).order_by(P.id))]
                    if not protected or outcome == 'rollback': await session.rollback()
                    elif outcome == 'commit': await session.commit()
                    else: await nested.rollback(); await session.commit()
                    final = [tuple(row) for row in await session.execute(select(P.id, P.label, P.rank).order_by(P.id))]
                    assert final == (updated if protected and outcome == 'commit' else original)
                    return observed_result, loaded_values, updated
            finally:
                await engine.dispose()
        expected = asyncio.run(scenario(False))
        run(app); publish(app)
        assert asyncio.run(scenario(True)) == expected


@pytest.mark.parametrize('drift', ['schema', 'name', 'column_name', 'column_type', 'collation'])
def test_public_update_mapping_drift_refuses_before_update(drift):
    from cryptalis.sqlalchemy import PolicyMismatch
    with public_update_application() as app:
        factory = protect(app)
        table, P = app.public_table, app.PublicTask
        if drift == 'schema': table.schema = None
        elif drift == 'name': table.name = 'other_public_task'
        elif drift == 'column_name': table.c.label.name = 'other_label'
        elif drift == 'column_type': table.c.label.type = Integer()
        else: table.c.label.type.collation = 'C'
        emitted = []
        def observe(conn, cursor, sql, *rest):
            if sql.lstrip().upper().startswith('UPDATE '): emitted.append(True)
        event.listen(app.runtime, 'before_cursor_execute', observe)
        with factory(tenant_id=TENANT) as session:
            with pytest.raises((UnsupportedProtectedOperation, PolicyMismatch)):
                session.execute(update(P).where(P.rank == 2).values(label='changed'))
            session.rollback()
        assert emitted == []


def test_public_update_unqualified_mapping_keeps_native_target():
    with public_update_application() as app:
        app.public_table.schema = None
        path = ['"' + app.schema + '", pg_catalog']
        def initial_path(connection, record):
            with connection.cursor() as cursor:
                cursor.execute('SELECT pg_catalog.set_config(%s,%s,false)', ('search_path', path[0]))
            connection.commit()
        app.runtime.dispose()
        event.listen(app.runtime, 'connect', initial_path)
        P = app.PublicTask
        statement = update(P).where(P.rank == 2).values(label='qualified by native resolution')
        with sessionmaker(app.runtime)() as session:
            assert session.execute(statement).rowcount == 1
            expected = values(session, P)
            session.rollback()
        factory = protect(app)
        assert app.public_table.schema == app.schema
        path[0] = 'pg_catalog'
        with factory(tenant_id=TENANT) as session:
            assert session.execute(statement).rowcount == 1
            assert values(session, P) == expected
            session.rollback()


@pytest.mark.parametrize('effect', ['check', 'expression_index'])
def test_public_update_rechecks_effects_after_prior_success(effect):
    with public_update_application() as app:
        factory = protect(app)
        P = app.PublicTask
        statement = update(P).where(P.rank == 2).values(label=bindparam('replacement', type_=Text))
        with factory(tenant_id=TENANT) as session:
            assert session.execute(statement, {'replacement': 'first success'}).rowcount == 1
            session.commit()
        with app.owner.begin() as connection:
            target = '"' + app.schema + '".public_task'
            if effect == 'check': connection.exec_driver_sql('ALTER TABLE ' + target + ' ADD CHECK (rank >= 0)')
            else: connection.exec_driver_sql('CREATE INDEX public_task_drift ON ' + target + ' (lower(label))')
        with factory(tenant_id=TENANT) as session:
            with pytest.raises(UnsupportedProtectedOperation):
                session.execute(statement, {'replacement': 'must not appear'})
            session.rollback()
        with app.owner.connect() as connection:
            assert connection.exec_driver_sql('SELECT label FROM "' + app.schema + '".public_task WHERE rank=2').scalar_one() == 'first success'


def test_public_update_locks_before_inventory_and_releases_on_rollback():
    from sqlalchemy.exc import DBAPIError
    with public_update_application() as app:
        factory = protect(app)
        probes = []
        target = '"' + app.schema + '".public_task'
        def observe(conn, cursor, sql, *rest):
            if 'SELECT baseline.qualified' not in sql: return
            with app.owner.begin() as independent:
                with pytest.raises(DBAPIError) as caught:
                    independent.exec_driver_sql('LOCK TABLE ' + target + ' IN ACCESS EXCLUSIVE MODE NOWAIT')
                assert caught.value.orig.sqlstate == '55P03'
                probes.append('blocked-before-inventory')
        event.listen(app.runtime, 'before_cursor_execute', observe)
        with factory(tenant_id=TENANT) as session:
            assert session.execute(update(app.PublicTask).where(app.PublicTask.rank == 2).values(label='temporary')).rowcount == 1
            assert probes == ['blocked-before-inventory']
            with app.owner.begin() as independent:
                with pytest.raises(DBAPIError) as caught:
                    independent.exec_driver_sql('LOCK TABLE ' + target + ' IN ROW EXCLUSIVE MODE NOWAIT')
                assert caught.value.orig.sqlstate == '55P03'
            session.rollback()
            with app.owner.begin() as independent:
                independent.exec_driver_sql('LOCK TABLE ' + target + ' IN ACCESS EXCLUSIVE MODE NOWAIT')
                assert independent.exec_driver_sql('SELECT label FROM ' + target + ' WHERE rank=2').scalar_one() == 'old-2'


@pytest.mark.parametrize('core', [False, True])
@pytest.mark.parametrize('autoflush', [False, True])
def test_public_update_autoflush_matches_native(core, autoflush):
    with public_update_application() as app:
        P = app.PublicTask
        target = app.public_table if core else P
        statement = update(target).where(app.public_table.c.rank == 2).values(label='bulk')
        def exercise(session):
            session.autoflush = autoflush
            row = session.get(P, UUID(int=2002))
            row.label = 'pending'
            result = session.execute(statement)
            # Disable subsequent autoflush so the observation does not mask
            # whether the UPDATE itself flushed pending native ORM changes.
            with session.no_autoflush:
                return result.rowcount, row.label, values(session, P), row in session.dirty
        with sessionmaker(app.runtime)() as session:
            expected = exercise(session); session.rollback()
        factory = protect(app)
        with factory(tenant_id=TENANT) as session:
            assert exercise(session) == expected
            session.rollback()


@pytest.mark.parametrize('boundary', ['repeated_before_execute', 'repeated_cursor', 'stale_compiled'])
def test_public_update_permit_state_machine_without_database(boundary):
    """A deterministic one-use protocol oracle; no connection or SQL is used."""
    from types import SimpleNamespace
    from sqlalchemy import MetaData
    from sqlalchemy.orm import registry
    from cryptalis import _experimental_public_update as profile
    mapping = registry(metadata=MetaData(schema='owned'))
    table = Table('public_task', mapping.metadata, Column('id', Uuid, primary_key=True), Column('label', Text))
    Model = type('PublicTask', (), {})
    mapping.map_imperatively(Model, table)
    session, connection = object(), object()
    owner = SimpleNamespace(mapping=mapping, bindings=[], document={'models': [{'schema': 'owned'}]},
        _experimental_public_update_tables=(table,), _control_error=UnsupportedProtectedOperation,
        _check=lambda: SimpleNamespace(session=session, flushing=False))
    profile.freeze_mappings(owner)
    statement = update(Model).values(label='value')
    current, old = statement._annotate({'native': 'current'}), statement._annotate({'native': 'old'})
    permit = profile.UpdatePermit(owner, session, connection, statement, table, {})
    token = profile._permit.set(permit)
    try:
        profile.before_execute(owner, connection, current, [], {})
        context = SimpleNamespace(root_connection=connection, executemany=False,
                                  compiled=SimpleNamespace(statement=old if boundary == 'stale_compiled' else current))
        if boundary == 'repeated_before_execute':
            with pytest.raises(UnsupportedProtectedOperation): profile.before_execute(owner, connection, current, [], {})
        elif boundary == 'stale_compiled':
            with pytest.raises(UnsupportedProtectedOperation): profile.check_cursor(owner, context)
        else:
            profile.check_cursor(owner, context)
            with pytest.raises(UnsupportedProtectedOperation): profile.check_cursor(owner, context)
    finally:
        profile._permit.reset(token)
        mapping.dispose()


@pytest.mark.parametrize("stage", ["initial", "after_attach"])
def test_public_update_pin_skips_ineligible_custom_type_without_database(stage):
    """Opt-out tables must not gain new custom-type accessor calls at attach."""
    from types import SimpleNamespace
    from sqlalchemy import MetaData
    from sqlalchemy.orm import registry
    from sqlalchemy.types import TypeDecorator
    from cryptalis import _experimental_public_update as profile
    class OpaquePublicType(TypeDecorator):
        impl = Text
        cache_ok = True
        @property
        def length(self):
            raise AssertionError('An ineligible public type must not be inspected for UPDATE pins')
    mapping = registry(metadata=MetaData(schema='owned'))
    table = Table('public_task', mapping.metadata, Column('id', Uuid, primary_key=True),
                  Column('label', OpaquePublicType() if stage == 'initial' else Text()))
    Model = type('PublicTask', (), {})
    mapping.map_imperatively(Model, table)
    owner = SimpleNamespace(mapping=mapping, bindings=[], document={'models': [{'schema': 'owned'}]},
                            _experimental_public_update_tables=(table,))
    try:
        profile.freeze_mappings(owner)
        if stage == 'after_attach':
            table.c.label.type = OpaquePublicType()
        assert profile.target(owner, update(Model).values(label='value')) is None
    finally:
        mapping.dispose()
