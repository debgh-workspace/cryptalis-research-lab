"""Native positional and public-column correctness, not implementation mirrors."""
from dataclasses import replace
import pytest
from test_deprotection import application,prepared,execute
from test_migration import run,publish

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


def _metadata_statement(app,attribute):
 return {
  'comment':f'''COMMENT ON COLUMN "{app.schema}".customer.label IS 'current native metadata 雪' ''',
  'column_grant':f'GRANT SELECT(label) ON "{app.schema}".customer TO "{app.role}"',
  'statistics':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STATISTICS 100',
  'storage':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET STORAGE EXTERNAL',
  'compression':f'ALTER TABLE "{app.schema}".customer ALTER COLUMN label SET COMPRESSION pglz',
 }[attribute]


def _assert_native_public_metadata(actual,expected):
 assert actual==expected, 'native public metadata changed'


def exercise_retained_metadata(attribute,*,after_apply=None):
 # Native PostgreSQL catalog facts and SELECT * are the expectation, never
 # migration._facts, reverse._model, or the executor's equivalence predicate.
 from test_retained_public_metadata import metadata,reverse,complete_removal
 from test_retained_profile_safety_oracles import snapshot,native_values
 with application() as app:
  with app.owner.connect() as c:
   result=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id')
   original=(list(result.keys()),result.all())
  run(app);publish(app)
  value='current post-protection public value 雪'
  with app.owner.begin() as c:
   c.exec_driver_sql(_metadata_statement(app,attribute))
   c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',(value,))
  with app.owner.connect() as c:
   before=metadata(c,app)
   if attribute=='comment':assert before[12]=='current native metadata 雪'
   if attribute=='column_grant':
    assert before[11] is not None
    assert c.exec_driver_sql('SELECT pg_catalog.has_column_privilege(%s,pg_catalog.to_regclass(%s),%s,%s)',(app.role,f'"{app.schema}".customer','label','SELECT')).scalar_one()
   if attribute=='statistics':assert before[10]==100
   if attribute=='storage':assert before[8]=='e'
   if attribute=='compression':assert before[9]=='p'
  expected=(original[0],[tuple(row[:3])+(value,) for row in original[1]])
  protected=snapshot(app)
  d,p,pin,a=reverse(app)
  assert snapshot(app)==protected, 'reverse planning changed native state'
  # A mutation hook is confined to synthetic tests. It runs only after the
  # real product apply; it never replaces verification, authority, or locks.
  if after_apply is not None:after_apply(d,app)
  assert execute(app,d,p,pin,a).phase=='PLAINTEXT_PENDING'
  with app.owner.connect() as c:_assert_native_public_metadata(metadata(c,app),before)
  assert native_values(app)==expected, 'native current values or visible order changed'
  complete_removal(app,d,p,pin,a)
  with app.owner.connect() as c:
   _assert_native_public_metadata(metadata(c,app),before)
   if attribute=='column_grant':
    assert c.exec_driver_sql('SELECT pg_catalog.has_column_privilege(%s,pg_catalog.to_regclass(%s),%s,%s)',(app.role,f'"{app.schema}".customer','label','SELECT')).scalar_one()
    assert not c.exec_driver_sql('SELECT pg_catalog.has_table_privilege(%s,pg_catalog.to_regclass(%s),%s)',(app.role,f'"{app.schema}".customer','INSERT,UPDATE,DELETE,TRUNCATE,REFERENCES,TRIGGER')).scalar_one()
    assert not c.exec_driver_sql('SELECT pg_catalog.has_any_column_privilege(%s,pg_catalog.to_regclass(%s),%s)',(app.role,f'"{app.schema}".customer','INSERT,UPDATE,REFERENCES')).scalar_one()
  assert native_values(app)==expected, 'native current values or visible order changed'


def test_reverse_preserves_current_public_comment_without_planning_effects():
 exercise_retained_metadata('comment')


def test_changed_protected_staging_refuses_without_losing_current_public_edits():
 from test_migration import FIELD_ID
 from test_retained_public_metadata import metadata,complete_removal
 from test_retained_profile_safety_oracles import snapshot,native_values,independent_frames
 with application() as app:
  d,p,pin,a=prepared(app);execute(app,d,p,pin,a,'BACKFILLED')
  backup=independent_frames(app)
  stage='_cryptalis_'+FIELD_ID.hex+'_plain'
  current='current public edit 雪😀'*2048
  with app.owner.begin() as c:
   c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET label=%s',(current,))
   c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{stage}"=%s',('changed protected staging',))
  with app.owner.connect() as c:
   before_metadata=metadata(c,app)
   assert c.exec_driver_sql("SELECT count(*) FROM information_schema.columns WHERE table_schema=%s AND column_name LIKE '%%_copy_%%'",(app.schema,)).scalar_one()==0
  before=snapshot(app)
  for _ in range(2):
   with pytest.raises(app.m.TransitionFailure,match='value_verification_failed'):
    execute(app,d,p,pin,a,chunk_bytes=512)
   assert snapshot(app)==before, 'refused verification changed native state'
   assert independent_frames(app)==backup
  # Repair only the deliberate synthetic stage corruption, from the independent
  # fixture values. Resume the SAME operation, retaining post-backfill edits.
  with app.owner.begin() as c:
   for identity,(_,value) in app.source.items():
    c.exec_driver_sql(f'UPDATE "{app.schema}".customer SET "{stage}"=%s WHERE id=%s',(value,identity))
  assert execute(app,d,p,pin,a,chunk_bytes=512).phase=='PLAINTEXT_PENDING'
  expected=(['id','tenant_id','name','label'],[(k,t,v,current) for k,(t,v) in sorted(app.source.items())])
  assert native_values(app)==expected
  with app.owner.connect() as c:_assert_native_public_metadata(metadata(c,app),before_metadata)
  complete_removal(app,d,p,pin,a)
  assert native_values(app)==expected
  with app.owner.connect() as c:_assert_native_public_metadata(metadata(c,app),before_metadata)


def test_untouched_public_values_stay_outside_actual_bounded_transport():
 # Run the native libpq observer oracle, not an assertion about model internals.
 # The separately collected protected-byte cases are also mandatory acceptance:
 # prefix commit, repeat refusal without effects, no skipped row, same-op resume.
 import test_retained_profile_safety_oracles as native
 native.test_retained_reverse_never_projects_untouched_wide_public_value_into_chunk_transport()


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
def test_reverse_preserves_current_public_attributes_without_planning_effects(attribute):
 exercise_retained_metadata(attribute)
