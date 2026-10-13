"""Approved A6: exact standard VARCHAR mapping and trusted source metadata."""
import json
import pytest
from sqlalchemy import String,text
from test_protection_compiler import app,engine,declaration,inventory,reviews
from cryptalis.manifest.compiler import compile_protection,_previous_lock,PlanningRejected
from cryptalis.manifest.parser import ManifestInvalid

@pytest.mark.parametrize('limit',[None,3])
def test_standard_varchar_plan_and_reload_preserve_native_typmod(app,limit):
    db,mapping,Customer,schema=app
    ddl='varchar' if limit is None else f'varchar({limit})'
    with db.begin() as c:c.execute(text(f'ALTER TABLE "{schema}".customer ALTER COLUMN email TYPE {ddl} COLLATE "C"'))
    Customer.__table__.c.email.type=String(limit,collation='C')
    plan=compile_protection(json.dumps(declaration()).encode(),mapping,db,writers=inventory(),search_reviews=reviews())
    document=json.loads(plan.lock_bytes);model=document['models'][0];field=model['fields'][0]
    source=next(c for c in model['source_schema']['columns'] if c['name']=='email')
    assert (field['source']['type'],source['typmod'])==('varchar',str(-1 if limit is None else limit+4))
    assert _previous_lock(plan.lock_bytes,document,db)==document
    forged=json.loads(plan.lock_bytes);forged['models'][0]['fields'][0]['source']['type']='text'
    with pytest.raises(ManifestInvalid):_previous_lock(json.dumps(forged).encode(),document,db)

@pytest.mark.parametrize('declared',[None,4])
def test_varchar_mapping_length_mismatch_refuses(app,declared):
    db,mapping,Customer,schema=app
    with db.begin() as c:c.execute(text(f'ALTER TABLE "{schema}".customer ALTER COLUMN email TYPE varchar(3) COLLATE "C"'))
    Customer.__table__.c.email.type=String(declared,collation='C')
    with pytest.raises(PlanningRejected) as caught:
        compile_protection(json.dumps(declaration()).encode(),mapping,db,writers=inventory(),search_reviews=reviews())
    assert any(i.code=='unsupported_type' for i in caught.value.issues)
