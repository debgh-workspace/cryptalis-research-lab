"""Actual retained-layout native/driver/attached comparison; finite local evidence."""
import contextlib
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path
from uuid import UUID
import psycopg
from psycopg import sql
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
sys.path.insert(0, str(Path(os.environ['GIT_WORK_TREE'])/'tests'))
from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
from test_migration import run, publish, keys, TABLE_ID
from cryptalis.sqlalchemy import attach


def test_retained_search_native_baseline():
    results = []
    families = ['point','equality','in2']
    with contextlib.ExitStack() as stack:
        native = stack.enter_context(single_tenant_public_cascade_application(rows=1000,unique=False))
        protected = stack.enter_context(single_tenant_public_cascade_application(rows=1000,unique=False))
        run(protected,chunk_size=256); publish(protected)
        factory = attach(protected.mapping,protected.runtime,lock=protected.plan.lock_bytes,
                         keys=keys,deployment=(protected.plan,protected.pin))
        sessions = {'native':stack.enter_context(sessionmaker(native.runtime)()),
                    'protected':stack.enter_context(factory(tenant_id=TABLE_ID))}
        driver = stack.enter_context(psycopg.connect(os.environ['CRYPTALIS_TEST_RUNTIME_DATABASE_URL']))
        def query(app,family):
            C = app.Customer
            predicate = {'point':C.id == UUID(int=600),'equality':C.name == 'exact',
                         'in2':C.name.in_(['exact','雪😀'])}[family]
            return select(C.id,C.name).where(predicate).order_by(C.id)
        queries={(path,family):query(app,family) for path,app in [('native',native),('protected',protected)] for family in families}
        expected={family:list(sessions['native'].execute(queries['native',family])) for family in families}
        driver_queries={
            'point':(sql.SQL('SELECT id,name FROM {}.customer WHERE id=%s ORDER BY id').format(sql.Identifier(native.schema)),(UUID(int=600),)),
            'equality':(sql.SQL('SELECT id,name FROM {}.customer WHERE name=%s ORDER BY id').format(sql.Identifier(native.schema)),('exact',)),
            'in2':(sql.SQL('SELECT id,name FROM {}.customer WHERE name IN (%s,%s) ORDER BY id').format(sql.Identifier(native.schema)),('exact','雪😀'))}
        # Five alternating blocks; ten warmups and forty observations per cell.
        # Fixed SQL construction isolates query/result processing in this run.
        paths=['native','driver','protected']
        for block in range(5):
            for path in (paths if block%2==0 else list(reversed(paths))):
                for family in families:
                    samples=[]
                    for n in range(50):
                        started=time.perf_counter_ns()
                        if path == 'driver': actual=driver.execute(*driver_queries[family]).fetchall()
                        else: actual=list(sessions[path].execute(queries[path,family]))
                        elapsed=(time.perf_counter_ns()-started)/1e6
                        assert actual == expected[family]
                        if n>=10:samples.append(elapsed)
                    results.append(dict(block=block,path=path,family=family,samples_ms=samples,median_ms=statistics.median(samples),rows_returned=len(expected[family])))
        aggregate=[]
        for family in families:
            medians={path:[r['median_ms'] for r in results if r['family']==family and r['path']==path] for path in paths}
            aggregate.append(dict(family=family,rows_returned=len(expected[family]),median_of_block_medians_ms={path:statistics.median(v) for path,v in medians.items()},paired_protected_minus_native_ms=[a-b for a,b in zip(medians['protected'],medians['native'])]))
        report=dict(scope='1000-row same-host synthetic retained-layout warm sync benchmark; fixed statement objects; five alternating blocks;40 measured samples/cell; no production or p99 qualification',python=platform.python_version(),sqlalchemy=sqlalchemy.__version__,rows_per_fixture=1000,aggregate=aggregate,results=results,exact_results_checked=True,leakage='Declared equality/frequency and observable access/result patterns; no new confidentiality claim')
        (Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent/'retained-native-benchmark.json').write_text(json.dumps(report,indent=2)+'\n')
