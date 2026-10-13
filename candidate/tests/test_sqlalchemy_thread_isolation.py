"""Concurrent real PostgreSQL Sessions use independent authenticated tenant scopes."""
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from test_sqlalchemy_search import search_application, _row, OTHER

@pytest.mark.parametrize('protected',[False,True],ids=['native','attached'])
@pytest.mark.parametrize('workers',[2,8])
def test_threaded_sessions_preserve_tenant_values_and_rollback(protected,workers):
    with search_application(protected) as app:
        barrier=Barrier(workers,timeout=15)
        def work(number):
            tenant=app.tenant if number%2==0 else OTHER
            barrier.wait()
            for iteration in range(10):
                rank=number*100+iteration
                value=f'worker-{number}-row-{iteration}-雪'
                with app.sessions(tenant_id=tenant) as session:
                    row=_row(app,value,rank,tenant)
                    session.add(row)
                    session.flush()
                    assert session.scalar(select(app.Customer.name).where(app.Customer.id==row.id))==value
                    if iteration%3==0:
                        session.rollback()
                    else:
                        session.commit()
                with app.sessions(tenant_id=tenant) as session:
                    found=list(session.scalars(select(app.Customer.rank).where(app.Customer.tenant_id==tenant,app.Customer.name==value)))
                    assert found==([] if iteration%3==0 else [rank])
            return number
        with ThreadPoolExecutor(max_workers=workers) as pool:
            assert sorted(pool.map(work,range(workers)))==list(range(workers))
        with app.owner_engine.connect() as c:
            actual=c.exec_driver_sql(f'SELECT rank FROM "{app.schema}".customer ORDER BY rank').scalars().all()
        assert actual==[n*100+i for n in range(workers) for i in range(10) if i%3]
        assert app.engine.pool.checkedout()==0

@pytest.mark.parametrize('protected',[False,True],ids=['native','attached'])
def test_concurrent_tenant_unique_conflict_has_one_winner_per_tenant(protected):
    with search_application(protected,unique=True) as app:
        barrier=Barrier(4,timeout=15)
        def work(number):
            tenant=app.tenant if number<2 else OTHER
            barrier.wait()
            with app.sessions(tenant_id=tenant) as session:
                session.add(_row(app,'shared unique value',number,tenant))
                try:
                    session.commit()
                    return tenant,'commit'
                except IntegrityError as err:
                    assert err.orig.sqlstate=='23505'
                    session.rollback()
                    return tenant,'conflict'
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(work,range(4)))
        for tenant in (app.tenant,OTHER):
            assert sorted(result for scope,result in results if scope==tenant)==['commit','conflict']
            with app.sessions(tenant_id=tenant) as session:
                assert list(session.scalars(select(app.Customer.name).where(app.Customer.tenant_id==tenant,app.Customer.name=='shared unique value')))==['shared unique value']
        assert app.engine.pool.checkedout()==0
