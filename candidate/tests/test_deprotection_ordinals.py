"""Native positional and public-column correctness, not implementation mirrors."""
from dataclasses import replace
import pytest
from test_deprotection import application,prepared,execute,plaintext_role
from test_migration import run,publish,keys

def test_reverse_preserves_public_null_unicode_and_native_order():
 with application() as app:
  with app.owner.begin() as c:
   c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=CASE WHEN name IS NULL THEN NULL ELSE name END')
  with app.owner.connect() as c:
   result=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id');before=(list(result.keys()),result.all())
  d,p,pin,a=prepared(app);execute(app,d,p,pin,a)
  execute(app,d,p,replace(pin,phase='PLAINTEXT_ACTIVATING'),a,'PLAINTEXT_ACTIVE')
  with app.owner.connect() as c:
   result=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id');after=(list(result.keys()),result.all())
  assert after==before


def test_reverse_refuses_unhandled_public_suffix_comment_before_staging():
 with application() as app:
  run(app);publish(app)
  with app.owner.begin() as c:c.exec_driver_sql(f"COMMENT ON COLUMN \"{app.schema}\".customer.label IS 'retained application metadata'")
  from cryptalis import deprotection as d
  with pytest.raises(app.m.TransitionFailure,match='unsupported_reverse_suffix_metadata'):
   d.plan(app.plan,app.owner,source_pin=app.pin,keys=keys,plaintext_runtime_role=plaintext_role(),backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
  with app.owner.connect() as c:
   assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}"._cryptalis_journal').scalar_one()==1
   assert c.exec_driver_sql("SELECT count(*) FROM information_schema.columns WHERE table_schema=%s AND column_name LIKE '%%_plain'",(app.schema,)).scalar_one()==0


def test_changed_public_staging_refuses_switch():
 with application() as app:
  d,p,pin,a=prepared(app);execute(app,d,p,pin,a,'BACKFILLED')
  with app.owner.begin() as c:
   name=c.exec_driver_sql("SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND column_name LIKE '%%_copy_%%'",(app.schema,)).scalar_one()
   c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{name}"=%s',('tampered public copy',))
  with pytest.raises(app.m.TransitionFailure,match='public_copy_verification_failed'):execute(app,d,p,pin,a)
  with app.owner.connect() as c:
   assert c.exec_driver_sql(f'SELECT pg_typeof(name)::text FROM "{app.schema}".customer LIMIT 1').scalar_one()=='bytea'


def test_public_copy_participates_in_chunk_byte_bound():
 with application() as app:
  with app.owner.begin() as c:c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',('wide public suffix'*2048,))
  d,p,pin,a=prepared(app)
  with pytest.raises(app.m.TransitionFailure,match='row_exceeds_chunk_byte_limit'):
   execute(app,d,p,pin,a,'BACKFILLED',chunk_bytes=512)
  with app.owner.connect() as c:
   state=c.exec_driver_sql(f'SELECT state FROM "{app.schema}"._cryptalis_journal WHERE operation_id=%s',(p.operation_id,)).scalar_one()
   assert all(progress['rows']==0 for progress in state['models'].values())
  assert execute(app,d,p,pin,a,'BACKFILLED',chunk_bytes=1024*1024).phase=='BACKFILLED'


def test_old_unversioned_staging_requires_inspection():
 with application() as app:
  d,p,pin,a=prepared(app);execute(app,d,p,pin,a,'EXPANDED')
  with app.owner.begin() as c:
   c.exec_driver_sql(f'UPDATE "{app.schema}"._cryptalis_journal SET state=state-\'layout_version\' WHERE operation_id=%s',(p.operation_id,))
  with pytest.raises(app.m.TransitionFailure,match='reverse_staging_layout_requires_inspection'):
   execute(app,d,p,pin,a)


def test_abort_removes_every_ordered_stage_and_preserves_protected_values():
 with application() as app:
  d,p,pin,a=prepared(app)
  with app.owner.connect() as c:
   result=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id');before=(list(result.keys()),result.all())
  execute(app,d,p,pin,a,'BACKFILLED')
  assert d.abort(p,app.owner,pin=pin,approval=app.approval,plaintext_approval=a).phase=='ABORTED'
  with app.owner.connect() as c:
   result=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id');after=(list(result.keys()),result.all())
  assert after==before


@pytest.mark.parametrize('attribute',['column_grant','statistics','storage','compression'])
def test_reverse_refuses_unhandled_suffix_attributes(attribute):
 with application() as app:
  run(app);publish(app)
  statements={
   'column_grant':f'GRANT SELECT(label) ON "{app.schema}".customer TO "{app.role}"',
   'statistics':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STATISTICS 100',
   'storage':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STORAGE EXTERNAL',
   'compression':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET COMPRESSION pglz',
  }
  with app.owner.begin() as c:c.exec_driver_sql(statements[attribute])
  from cryptalis import deprotection as d
  with pytest.raises(app.m.TransitionFailure,match='unsupported_reverse_suffix_metadata') as failure:
   d.plan(app.plan,app.owner,source_pin=app.pin,keys=keys,plaintext_runtime_role=plaintext_role(),backfill_rows_per_second=1000,verify_rows_per_second=1000,temporary_bytes_per_row=700,wal_bytes_per_row=2000)
  assert 'Keep protection enabled' in str(failure.value)
  with app.owner.connect() as c:
   assert c.exec_driver_sql(f'SELECT count(*) FROM "{app.schema}"._cryptalis_journal').scalar_one()==1

