"""Admission oracles use constant-return functions and no-op procedures only."""
import json
import pytest
from cryptalis.manifest.compiler import Writer, WriterInventory, SearchReview
from test_migration import application, keys, TABLE_ID, FIELD_ID, run


def replan(app, allow=None):
    declaration = app.plan.document['lock']['declaration']
    if allow is not None:
        declaration['routine_allowlist'] = allow
    return app.m.plan(json.dumps(declaration).encode(), app.mapping,
        app.owner.execution_options(postgresql_readonly=True),
        writers=WriterInventory(True, (Writer(TABLE_ID, 'app', 'sqlalchemy', evidence='harmless fixture'),)),
        search_reviews=(SearchReview(FIELD_ID, False, 'synthetic names'),), keys=keys,
        runtime_role=app.role, target_id=app.plan.target_id,
        backfill_rows_per_second=1000, verify_rows_per_second=1000,
        temporary_bytes_per_row=700, wal_bytes_per_row=2000)


def create(app, kind, definer, grant):
    with app.owner.begin() as c:
        name=f'"{app.schema}".harmless'
        body="RETURNS integer LANGUAGE sql AS 'SELECT 1'" if kind=='FUNCTION' else "LANGUAGE plpgsql AS 'BEGIN NULL; END'"
        c.exec_driver_sql(f'CREATE {kind} {name}() {body} SECURITY {"DEFINER" if definer else "INVOKER"} SET search_path=pg_catalog')
        if grant!='PUBLIC':
            c.exec_driver_sql(f'REVOKE EXECUTE ON {kind} {name}() FROM PUBLIC')
        if grant=='direct':
            role=c.dialect.identifier_preparer.quote_identifier(app.role)
            c.exec_driver_sql(f'GRANT EXECUTE ON {kind} {name}() TO {role}')


@pytest.mark.parametrize('kind', ['FUNCTION', 'PROCEDURE'])
@pytest.mark.parametrize('definer', [False, True])
@pytest.mark.parametrize('grant', ['PUBLIC', 'direct', 'none'])
def test_readonly_admission_requires_explicit_routine_review(kind, definer, grant):
    with application(rows=1) as app:
        create(app, kind, definer, grant)
        unsafe=definer and grant!='none'
        if unsafe:
            with pytest.raises(app.m.TransitionFailure) as error:
                replan(app)
            assert error.value.code=='unreviewed_runtime_routine'
        else:
            assert replan(app).document['kind']=='protect'
        # The planner must not change grants, invoke routines, or create a journal.
        with app.owner.connect() as c:
            assert c.exec_driver_sql('SELECT to_regclass(%s)',
                (f'"{app.schema}"._cryptalis_journal',)).scalar_one() is None


@pytest.mark.parametrize('kind', ['FUNCTION', 'PROCEDURE'])
def test_routine_added_after_plan_is_rejected_before_effects(kind):
    with application(rows=1) as app:
        create(app, kind, True, 'PUBLIC')
        with pytest.raises(app.m.TransitionFailure) as error:
            run(app, 'EXPANDED')
        assert error.value.code=='unreviewed_runtime_routine'
        with app.owner.connect() as c:
            assert c.exec_driver_sql('SELECT to_regclass(%s)',
                (f'"{app.schema}"._cryptalis_journal',)).scalar_one() is None


def inventory(app):
    from cryptalis.manifest.routines import routine_inventory
    with app.owner.execution_options(postgresql_readonly=True).connect() as c:
        return [r for r in routine_inventory(c, app.role) if r['schema']==app.schema]


@pytest.mark.parametrize('kind', ['FUNCTION', 'PROCEDURE'])
@pytest.mark.parametrize('grant', ['PUBLIC', 'direct', 'none'])
def test_inventory_and_explicit_review_acceptance(kind, grant):
    with application(rows=1) as app:
        create(app, kind, True, grant)
        rows=inventory(app)
        assert len(rows)==1
        row=rows[0]
        assert row['security_definer'] and row['kind']==('f' if kind=='FUNCTION' else 'p')
        assert row['search_path']==['search_path=pg_catalog']
        assert row['review_required']==(grant!='none')
        if grant!='none':
            expected='PUBLIC' if grant=='PUBLIC' else app.role
            assert any(g['grantee']==expected for g in row['execute_grants'])
            assert app.role in row['executable_as']
        assert 'catalog_definition' not in row
        proposal=replan(app, [row['review_digest']])
        assert proposal.document['lock']['declaration']['routine_allowlist']==[row['review_digest']]
        # The same review remains valid through actual migration admission.
        app.plan=proposal
        app.pin=app.m.DeploymentPin(proposal.target_id, proposal.operation_id, proposal.digest, 'PREPARED')
        assert run(app, 'EXPANDED').phase=='EXPANDED'


@pytest.mark.parametrize('change', ['body', 'search_path', 'wrong_digest', 'missing_second_routine'])
def test_review_is_exact_and_cannot_hide_unreviewed_routines(change):
    with application(rows=1) as app:
        create(app, 'FUNCTION', True, 'PUBLIC')
        digest=inventory(app)[0]['review_digest']
        with app.owner.begin() as c:
            if change=='body':
                c.exec_driver_sql(f'''CREATE OR REPLACE FUNCTION "{app.schema}".harmless() RETURNS integer
                    LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS 'SELECT 2' ''')
            elif change=='search_path':
                c.exec_driver_sql(f'ALTER FUNCTION "{app.schema}".harmless() SET search_path=pg_catalog,pg_temp')
            elif change=='missing_second_routine':
                c.exec_driver_sql(f'''CREATE FUNCTION "{app.schema}".other() RETURNS integer
                    LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS 'SELECT 1' ''')
        with pytest.raises(app.m.TransitionFailure) as error:
            replan(app, ['0'*64 if change=='wrong_digest' else digest])
        assert error.value.code=='unreviewed_runtime_routine'


@pytest.mark.parametrize('value', [None, '', ['*'], ['A'*64], ['0'*64, '0'*64], [1]])
def test_invalid_review_declarations_are_rejected(value):
    from cryptalis.manifest.declaration import parse_protection_declaration
    from cryptalis.manifest.parser import ManifestInvalid
    with application(rows=1) as app:
        declaration=app.plan.document['lock']['declaration']
        declaration['routine_allowlist']=value
        with pytest.raises(ManifestInvalid, match='Routine allow-list'):
            parse_protection_declaration(json.dumps(declaration).encode())


def test_plan_error_is_exact_and_contains_no_routine_source():
    with application(rows=1) as app:
        create(app, 'FUNCTION', True, 'PUBLIC')
        with pytest.raises(app.m.TransitionFailure) as error:
            replan(app)
        assert str(error.value)==('unreviewed_runtime_routine; operation=unstarted; SQLSTATE=UNKNOWN. '
            'Keep writers stopped. Inspect this operation and the external current policy before resume.')


@pytest.mark.parametrize('boundary', ['resume', 'attach'])
def test_new_routine_blocks_resume_and_attachment(boundary):
    from cryptalis.sqlalchemy import attach, PolicyMismatch
    from test_migration import publish
    with application(rows=1) as app:
        run(app, 'EXPANDED' if boundary=='resume' else 'PENDING')
        if boundary=='attach':
            publish(app)
        create(app, 'FUNCTION', True, 'PUBLIC')
        with pytest.raises((app.m.TransitionFailure, PolicyMismatch)):
            if boundary=='resume':
                run(app, 'BACKFILLED')
            else:
                attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,
                       deployment=(app.plan,app.pin))


def test_attachment_without_migration_journal_still_checks_routines():
    from test_sqlalchemy_search import search_application
    from cryptalis.sqlalchemy import attach, PolicyMismatch
    from cryptalis.migration import TransitionFailure
    with search_application(attach_now=False) as app:
        with app.owner_engine.begin() as c:
            c.exec_driver_sql(f'''CREATE FUNCTION "{app.schema}".harmless() RETURNS integer
                LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS 'SELECT 1' ''')
        with pytest.raises((TransitionFailure,PolicyMismatch)):
            attach(app.mapping,app.engine,lock=app.plan.lock_bytes,keys=app.keys)


def test_journalless_attachment_accepts_explicit_review():
    from test_sqlalchemy_search import search_application
    from cryptalis.sqlalchemy import attach
    from cryptalis.manifest.routines import routine_inventory
    with search_application(attach_now=False) as app:
        with app.owner_engine.begin() as c:
            c.exec_driver_sql(f'''CREATE FUNCTION "{app.schema}".harmless() RETURNS integer
                LANGUAGE sql SECURITY DEFINER SET search_path=pg_catalog AS 'SELECT 1' ''')
        with app.engine.connect() as c:
            role=c.exec_driver_sql('SELECT current_user').scalar_one()
            row=next(r for r in routine_inventory(c,role) if r['schema']==app.schema)
        lock=json.loads(app.plan.lock_bytes)
        lock['declaration']['routine_allowlist']=[row['review_digest']]
        attach(app.mapping,app.engine,lock=json.dumps(lock,sort_keys=True,separators=(',', ':')).encode(),keys=app.keys)
