"""Independent native oracle for an unqualified public-child mapper.

Only disposable synthetic schemas and already-authorized private profiles.
No production capability admission is implied by this experiment.
"""
import pytest
from sqlalchemy import delete, event, select
from sqlalchemy.orm import sessionmaker
from cryptalis.sqlalchemy import attach
from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
from test_migration import run, publish, keys, TABLE_ID

@pytest.mark.parametrize('qualified', [True, False])
@pytest.mark.parametrize('target', ['child', 'parent_cascade'])
@pytest.mark.parametrize("outcome", ["commit", "rollback", "savepoint"])
@pytest.mark.parametrize("change_path", [False, True])
def test_unqualified_child_delete_matches_native(qualified, target, outcome, change_path):
    with single_tenant_public_cascade_application() as app:
        # Represent an ordinary unqualified application mapper after fixture DDL.
        # The connection's initial search path selects only its owned test schema.
        if not qualified:
            app.public_item.schema = None
        app.runtime.dispose()
        path = ['"'+app.schema+'", pg_catalog']
        def initial_path(connection, record):
            with connection.cursor() as cursor:
                cursor.execute('SELECT pg_catalog.set_config(%s,%s,false)',
                               ('search_path', path[0]))
            connection.commit()
        event.listen(app.runtime, 'connect', initial_path)
        app.runtime.clear_compiled_cache()
        C, P = app.Customer, app.PublicItem
        statement = (delete(P).where(P.label == 'child-1') if target == 'child'
                     else delete(C).where(C.label == 'label-101'))
        with sessionmaker(app.runtime)() as session:
            initial_parent = list(session.execute(select(C.id,C.name,C.label).order_by(C.id)))
            initial_child = list(session.execute(select(P.id,P.label,P.parent_id).order_by(P.id)))
            expected_count = session.execute(statement).rowcount
            expected_parent = list(session.execute(select(C.id,C.name,C.label).order_by(C.id)))
            expected_child = list(session.execute(select(P.id,P.label,P.parent_id).order_by(P.id)))
            session.rollback()
        assert expected_count == 1
        assert len(expected_child) == 6
        run(app); publish(app)
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                         keys=keys, deployment=(app.plan,app.pin))
        factory._owner._experimental_public_delete_tables = (app.table,app.public_item)
        factory._owner._experimental_protected_equality_delete = True
        factory._owner._experimental_public_child_cascade_delete = True
        if change_path:
            path[0] = "pg_catalog"
        with factory(tenant_id=TABLE_ID) as session:
            nested = session.begin_nested() if outcome == "savepoint" else None
            assert session.execute(statement).rowcount == expected_count
            assert list(session.execute(select(C.id,C.name,C.label).order_by(C.id))) == expected_parent
            assert list(session.execute(select(P.id,P.label,P.parent_id).order_by(P.id))) == expected_child
            if outcome == 'commit':
                session.commit()
            elif nested is not None:
                nested.rollback(); session.commit()
            else:
                session.rollback()
            assert list(session.execute(select(C.id,C.name,C.label).order_by(C.id))) == (expected_parent if outcome == 'commit' else initial_parent)
            assert list(session.execute(select(P.id,P.label,P.parent_id).order_by(P.id))) == (expected_child if outcome == 'commit' else initial_child)

@pytest.mark.parametrize('mode', ['no_optin', 'schema_drift', 'name_drift'])
def test_public_schema_binding_does_not_grant_or_retarget_delete(mode):
    from cryptalis.sqlalchemy import PolicyMismatch, UnsupportedProtectedOperation
    with single_tenant_public_cascade_application() as app:
        app.public_item.schema = None
        app.runtime.dispose()
        def initial_path(connection, record):
            with connection.cursor() as cursor:
                cursor.execute('SELECT pg_catalog.set_config(%s,%s,false)',
                               ('search_path', '"'+app.schema+'", pg_catalog'))
            connection.commit()
        event.listen(app.runtime, 'connect', initial_path)
        run(app); publish(app)
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                         keys=keys, deployment=(app.plan,app.pin))
        assert app.public_item.schema == app.schema
        if mode != 'no_optin':
            factory._owner._experimental_public_delete_tables = (app.table,app.public_item)
            if mode == 'schema_drift': app.public_item.schema = None
            else: app.public_item.name = 'customer'
        emitted = []
        def observe(conn, cursor, statement, *rest):
            if statement.lstrip().upper().startswith('DELETE '): emitted.append(statement)
        event.listen(app.runtime, 'before_cursor_execute', observe)
        with factory(tenant_id=TABLE_ID) as session:
            with pytest.raises((UnsupportedProtectedOperation, PolicyMismatch)):
                session.execute(delete(app.PublicItem).where(app.PublicItem.label == 'child-1'))
            session.rollback()
            if mode != "no_optin":
                with pytest.raises(PolicyMismatch):
                    session.execute(select(app.PublicItem.id))
                session.rollback()
        assert emitted == []
        with app.owner.connect() as connection:
            assert connection.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}".public_item').scalar_one() == 7

@pytest.mark.parametrize('target', ['child', 'parent_cascade'])
def test_unqualified_child_does_not_guess_manifest_schema(target):
    from cryptalis.sqlalchemy import UnsupportedProtectedOperation
    with single_tenant_public_cascade_application() as app:
        app.public_item.schema = None
        # Default path has no public_item. A matching manifest schema alone
        # must never be taken as evidence of the application's table choice.
        run(app); publish(app)
        factory = attach(app.mapping, app.runtime, lock=app.plan.lock_bytes,
                         keys=keys, deployment=(app.plan,app.pin))
        assert app.public_item.schema is None
        factory._owner._experimental_public_delete_tables = (app.table,app.public_item)
        factory._owner._experimental_protected_equality_delete = True
        factory._owner._experimental_public_child_cascade_delete = True
        C, P = app.Customer, app.PublicItem
        statement = (delete(P).where(P.label == 'child-1') if target == 'child'
                     else delete(C).where(C.label == 'label-101'))
        emitted = []
        def observe(conn, cursor, statement, *rest):
            if statement.lstrip().upper().startswith('DELETE '): emitted.append(True)
        event.listen(app.runtime, 'before_cursor_execute', observe)
        with factory(tenant_id=TABLE_ID) as session:
            with pytest.raises(UnsupportedProtectedOperation): session.execute(statement)
            session.rollback()
        assert emitted == []
        with app.owner.connect() as connection:
            for name in ['customer','public_item']:
                assert connection.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}"."{name}"').scalar_one() == 7
