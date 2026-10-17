"""Recording-only fixture checks; no database or credential files.

Requires separately selected candidate test_sqlalchemy_search module binding.
"""
from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import patch
import pytest
import test_sqlalchemy_search as fixture


class StopBeforeEngines(Exception):
    pass


@pytest.mark.parametrize('bad_at', [0, 1, 3])
def test_preflight_refusal_precedes_engine_or_mutation(bad_at):
    answers = [(1,), ('160015',), ('existing_runtime',), (True,)]
    answers[bad_at] = [(0,), ('150015',), None, (False,)][bad_at]
    statements = []
    class Connection:
        def execute(self, statement):
            statements.append(statement)
            return SimpleNamespace(fetchone=lambda: answers[len(statements)-1])
    @contextmanager
    def connect(value):
        assert value == 'recording-only'
        yield Connection()
    with patch.dict(fixture.os.environ, {'CRYPTALIS_TEST_DATABASE_URL':'recording-owner',
                                        'CRYPTALIS_TEST_RUNTIME_DATABASE_URL':'recording-only'}), \
         patch.object(fixture.psycopg, 'connect', connect), \
         patch.object(fixture, '_engine', side_effect=AssertionError('engine reached')):
        with pytest.raises(RuntimeError):
            with fixture.search_application():
                pytest.fail('fixture entered')
    assert statements == [
        'select 1', 'show server_version_num', 'select current_user',
        'select not rolsuper and not rolcreatedb and not rolcreaterole and not rolbypassrls from pg_roles where rolname=current_user'
    ][:bad_at+1]


def test_successful_preflight_before_owner_engine():
    seen=[]
    def role(): seen.append('runtime_preflight'); return 'existing_runtime'
    def engine(name):
        seen.append(name)
        raise StopBeforeEngines()
    with patch.dict(fixture.os.environ, {'CRYPTALIS_TEST_DATABASE_URL':'recording-owner',
                                        'CRYPTALIS_TEST_RUNTIME_DATABASE_URL':'recording-only'}), \
         patch.object(fixture, '_fixture_runtime_role', role), patch.object(fixture, '_engine', engine):
        with pytest.raises(StopBeforeEngines):
            with fixture.search_application(): pytest.fail('entered')
    assert seen == ['runtime_preflight', 'CRYPTALIS_TEST_DATABASE_URL']


class RecordingOwner:
    def __init__(self, *, create_error=None, commit_error=None):
        self.events=[]; self.create_error=create_error; self.commit_error=commit_error
    @contextmanager
    def begin(self):
        self.events.append('begin')
        owner=self
        class Connection:
            def execute(self, statement):
                value=str(statement); owner.events.append(value)
                if value.startswith('CREATE ') and owner.create_error:
                    raise owner.create_error
        try:
            yield Connection()
        except BaseException:
            self.events.append('rollback'); raise
        else:
            self.events.append('commit')
            if self.commit_error:
                error=self.commit_error; self.commit_error=None; raise error


@pytest.mark.parametrize('failure', ['create_collision', 'commit_ambiguous'])
def test_unacquired_schema_never_dropped(failure):
    primary=RuntimeError(failure)
    owner=RecordingOwner(**({'create_error':primary} if failure=='create_collision' else {'commit_error':primary}))
    with pytest.raises(RuntimeError) as caught:
        with fixture._owned_fixture_schema(owner, 'cryptalis_search_recording'):
            pytest.fail('unacquired fixture entered')
    assert caught.value is primary
    assert owner.events == ['begin', 'CREATE SCHEMA "cryptalis_search_recording"',
                            'rollback' if failure=='create_collision' else 'commit']


@pytest.mark.parametrize('body_error', [None, RuntimeError('setup failed'), KeyboardInterrupt()])
def test_owned_schema_cleaned_after_body(body_error):
    owner=RecordingOwner(); caught=None
    try:
        with fixture._owned_fixture_schema(owner, 'cryptalis_search_recording'):
            owner.events.append('body')
            if body_error is not None: raise body_error
    except BaseException as exc: caught=exc
    assert caught is body_error
    assert owner.events == ['begin','CREATE SCHEMA "cryptalis_search_recording"','commit','body',
                            'begin','DROP SCHEMA IF EXISTS "cryptalis_search_recording" CASCADE','commit']
