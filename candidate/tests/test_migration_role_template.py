"""Template rendering is side-effect free and bounds/quotes a proposed role."""
import pytest
from sqlalchemy import event
from test_migration import application


def test_plan_role_template_prints_quoted_declared_grants_without_sql(capsys):
    with application(rows=1) as app:
        emitted=[]
        event.listen(app.owner,'before_cursor_execute',lambda *args:emitted.append(1))
        role='review " role'
        print(app.plan.runtime_role_template(role))
        output=capsys.readouterr().out
        assert emitted==[]
        assert 'CREATE ROLE "review "" role" NOLOGIN NOINHERIT NOSUPERUSER' in output
        assert f'GRANT USAGE ON SCHEMA "{app.schema}" TO "review "" role";' in output
        assert f'GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE "{app.schema}"."customer" TO "review "" role";' in output
        assert output.endswith('COMMIT;\n')


@pytest.mark.parametrize('name',['',None,'bad\x00name','x'*64,'é'*32,True,'bad\ud800'])
def test_role_template_rejects_ambiguous_or_truncated_identity(name):
    with application(rows=1) as app:
        with pytest.raises(app.m.TransitionFailure,match='invalid_template_role'):
            app.plan.runtime_role_template(name)
