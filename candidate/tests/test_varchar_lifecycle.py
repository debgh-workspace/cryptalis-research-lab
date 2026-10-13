"""A6 actual protect/edit/decrypt-back with exact native type and order."""
from dataclasses import replace
from uuid import UUID
import pytest
from sqlalchemy import String
from test_migration import application,keys,TENANT
from test_deprotection import prepared,execute
from cryptalis.sqlalchemy import attach

@pytest.mark.parametrize('limit',[None,8])
@pytest.mark.parametrize('public_varchar',[False,True])
def test_varchar_decrypt_back_preserves_types_values_and_order(limit,public_varchar):
    with application(field_type=String(limit,collation='C'),public_type=String(20) if public_varchar else None) as app:
        with app.owner.connect() as c:
            before=c.exec_driver_sql("SELECT a.attname,a.atttypid,a.atttypmod,a.attnotnull,a.attcollation FROM pg_attribute a WHERE a.attrelid=%s::regclass AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum",(f'{app.schema}.customer',)).all()
            oid=c.exec_driver_sql('SELECT %s::regclass::oid',(f'{app.schema}.customer',)).scalar_one()
            expected=dict(c.exec_driver_sql(f'SELECT id,name FROM "{app.schema}".customer').all())
        reverse,plan,pin,consent=prepared(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        with factory(tenant_id=TENANT) as s:
            row=s.get(app.Customer,UUID(int=105));row.name='12345678 ';s.commit()
        expected[UUID(int=105)]='12345678' if limit==8 else '12345678 '
        assert execute(app,reverse,plan,pin,consent).phase=='PLAINTEXT_PENDING'
        assert execute(app,reverse,plan,replace(pin,phase='PLAINTEXT_ACTIVATING'),consent,'PLAINTEXT_ACTIVE').phase=='PLAINTEXT_ACTIVE'
        with app.owner.connect() as c:
            after=c.exec_driver_sql("SELECT a.attname,a.atttypid,a.atttypmod,a.attnotnull,a.attcollation FROM pg_attribute a WHERE a.attrelid=%s::regclass AND a.attnum>0 AND NOT a.attisdropped ORDER BY a.attnum",(f'{app.schema}.customer',)).all()
            assert before==after
            assert c.exec_driver_sql('SELECT %s::regclass::oid',(f'{app.schema}.customer',)).scalar_one()==oid
            rows=c.exec_driver_sql(f'SELECT * FROM "{app.schema}".customer ORDER BY id')
            assert list(rows.keys())==['id','tenant_id','name','label']
            assert {r[0]:r[2] for r in rows}==expected
