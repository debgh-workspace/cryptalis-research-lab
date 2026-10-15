"""Real native-output corruption after the actual retained product apply.

These bounded synthetic regression injections preserve the real verification,
preflight, locks, final checks and transaction. Each must reach a specific native assertion;
a generic exception, early refusal, or unrelated fixture failure does not pass.
This proves independent-oracle sensitivity to changed real database output. It
does NOT prove product pre-effect detection of mutations introduced after apply.
"""
import pytest
from test_deprotection_ordinals import exercise_retained_metadata
from test_retained_public_metadata import metadata


@pytest.mark.parametrize('attribute',['comment','column_grant','statistics','storage','compression'])
def test_native_metadata_oracle_detects_actual_post_apply_regression(attribute,monkeypatch):
    observed=[]
    def install(d,app):
        original=d.apply
        def applied(*args,**kwargs):
            result=original(*args,**kwargs)
            assert result.phase=='PLAINTEXT_PENDING'
            with app.owner.begin() as c:
                before=metadata(c,app)
                statements={
                    'comment':f'COMMENT ON COLUMN "{app.schema}".customer.label IS NULL',
                    'column_grant':f'REVOKE SELECT(label) ON "{app.schema}".customer FROM "{app.role}"',
                    'statistics':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STATISTICS -1',
                    'storage':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STORAGE EXTENDED',
                    'compression':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET COMPRESSION default',
                }
                c.exec_driver_sql(statements[attribute])
                assert metadata(c,app)!=before, 'mutation did not change native metadata'
                observed.append(attribute)
            return result
        monkeypatch.setattr(d,'apply',applied)
    with pytest.raises(AssertionError,match='native public metadata changed'):
        exercise_retained_metadata(attribute,after_apply=install)
    assert observed==[attribute]


def test_native_current_value_oracle_detects_actual_post_apply_regression(monkeypatch):
    observed=[]
    def install(d,app):
        original=d.apply
        def applied(*args,**kwargs):
            result=original(*args,**kwargs)
            assert result.phase=='PLAINTEXT_PENDING'
            with app.owner.begin() as c:
                count=c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',('obsolete public copy',)).rowcount
                assert count==len(app.source)
                observed.append(count)
            return result
        monkeypatch.setattr(d,'apply',applied)
    with pytest.raises(AssertionError,match='native current values or visible order changed'):
        exercise_retained_metadata('comment',after_apply=install)
    assert observed and len(observed)==1
