"""Existing native mapper caches must not survive a storage-type cutover."""
from pathlib import Path
import sys
from uuid import UUID,uuid4
import pytest
from sqlalchemy import select,String,Text
from sqlalchemy.orm import sessionmaker
from test_migration import application,run,publish,keys,TENANT,frames,independent_open
from cryptalis.sqlalchemy import attach
import json

@pytest.mark.parametrize('field_type',[Text(collation='C'),String(24,collation='C')],ids=['text','varchar'])
@pytest.mark.parametrize('count',[1,3])
@pytest.mark.parametrize('action',['insert','update'])
def test_previously_used_mapper_after_attach_matches_native(action,count,field_type):
    with application(rows=count,field_type=field_type) as app:
        if action=='update':
            with sessionmaker(app.runtime)() as s:
                for n in range(count):
                    row=s.get(app.Customer,UUID(int=100+n));row.name=f'warm-{n}'
                s.commit()
        assert run(app).phase=='PENDING';publish(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        with factory(tenant_id=TENANT) as s:
            identities=[]
            for n in range(count):
                if action=='insert':
                    row=app.Customer(id=uuid4(),tenant_id=TENANT,name=f'after-{n}',label='public');s.add(row)
                else:row=s.get(app.Customer,UUID(int=100+n));row.name=f'after-{n}'
                identities.append(row.id)
            s.commit()
            for n,identity in enumerate(identities):assert s.get(app.Customer,identity).name==f'after-{n}'
        descriptor=json.loads(app.plan.lock_bytes)['models'][0]['fields'][0]['descriptor']
        stored=frames(app,True)
        for n,identity in enumerate(identities):
            assert independent_open(stored[identity],descriptor,TENANT,identity)==f'after-{n}'
