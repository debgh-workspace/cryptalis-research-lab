"""Real snapshot admission and post-drain recovery, independent native reads."""
import os
from dataclasses import replace
import psycopg,pytest
from test_migration import application,run,publish
from test_deprotection import prepared,execute,ciphertext_column

@pytest.mark.parametrize('isolation',['REPEATABLE READ','SERIALIZABLE'])
@pytest.mark.parametrize('direction',['protect','deprotect'])
def test_old_snapshot_refused_before_switch_and_resume_after_drain(isolation,direction):
 with application() as app:
  if direction=='deprotect':d,p,pin,a=prepared(app)
  with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as old:
   old.execute('BEGIN ISOLATION LEVEL '+isolation)
   old.execute('SELECT txid_current_snapshot()').fetchone()
   with pytest.raises(app.m.TransitionFailure,match='other_database_snapshots_active') as failure:
    run(app) if direction=='protect' else execute(app,d,p,pin,a)
   assert 'Finish or roll back other database transactions' in str(failure.value)
   with app.owner.connect() as c:
    physical='name' if direction=='protect' else ciphertext_column(app)
    observed=c.exec_driver_sql(f'SELECT pg_typeof("{physical}")::text FROM "{app.schema}".customer LIMIT 1').scalar_one()
   assert observed==('text' if direction=='protect' else 'bytea')
   old.rollback()
  result=run(app) if direction=='protect' else execute(app,d,p,pin,a)
  assert result.phase==('PENDING' if direction=='protect' else 'PLAINTEXT_PENDING')


def test_idle_connection_without_snapshot_does_not_block_cutover():
 with application() as app:
  with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as idle:
   assert idle.info.transaction_status==psycopg.pq.TransactionStatus.IDLE
   assert run(app).phase=='PENDING'


def test_snapshot_started_after_guard_sees_committed_staging(monkeypatch):
 with application() as app:
  guard=getattr(app.m,'_require_no_other_snapshots',None)
  assert callable(guard),'Snapshot guard is required'
  old=psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL'])
  def start_after_check(c,p):
   guard(c,p)
   old.execute('BEGIN ISOLATION LEVEL REPEATABLE READ')
   old.execute('SELECT txid_current_snapshot()').fetchone()
  monkeypatch.setattr(app.m,'_require_no_other_snapshots',start_after_check)
  try:
   assert run(app).phase=='PENDING'
   observed=old.execute(f'SELECT id,name FROM "{app.schema}".customer ORDER BY id').fetchall()
   assert [v is None for _,v in observed]==[app.source[k][1] is None for k,_ in observed]
  finally:old.close()


def test_snapshot_started_after_cached_statistics_is_still_refused(monkeypatch):
 with application() as app:
  verify=app.m._verify
  old=psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL'])
  def verify_then_open(c,*args,**kwargs):
   result=verify(c,*args,**kwargs)
   c.exec_driver_sql('SELECT count(*) FROM pg_catalog.pg_stat_activity').scalar_one()
   old.execute('BEGIN ISOLATION LEVEL REPEATABLE READ')
   old.execute('SELECT txid_current_snapshot()').fetchone()
   return result
  monkeypatch.setattr(app.m,'_verify',verify_then_open)
  try:
   with pytest.raises(app.m.TransitionFailure,match='other_database_snapshots_active'):run(app)
  finally:old.close()


def test_read_committed_server_cursor_snapshot_requires_drain():
 with application() as app:
  with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as old:
   with old.cursor(name='snapshot_boundary_cursor') as cursor:
    cursor.execute('SELECT x FROM generate_series(1,100) x')
    assert cursor.fetchone()==(1,)
    with pytest.raises(app.m.TransitionFailure,match='other_database_snapshots_active'):run(app)
   old.rollback()
  assert run(app).phase=='PENDING'


def test_exported_snapshot_requires_drain():
 with application() as app:
  with psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']) as old:
   old.execute('BEGIN ISOLATION LEVEL REPEATABLE READ')
   assert old.execute('SELECT pg_export_snapshot()').fetchone()[0]
   with pytest.raises(app.m.TransitionFailure,match='other_database_snapshots_active'):run(app)
   old.rollback()
  assert run(app).phase=='PENDING'
