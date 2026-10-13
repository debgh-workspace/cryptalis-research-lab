"""Same-session paired encoder comparison, with unchanged crypto and SQL paths."""
import json
import os
import statistics
import sys
import time
from pathlib import Path
from uuid import UUID
from sqlalchemy import select
sys.path.insert(0,str(Path(os.environ['GIT_WORK_TREE'])/'tests'))
from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
from test_migration import run,publish,keys,TABLE_ID
from cryptalis.sqlalchemy import attach
import cryptalis.crypto.cf1 as cf1
import cryptalis.crypto.keys as key_module
from cryptalis.crypto.keys import InvalidContext


def original_tuple(*parts):
    # Exact previous encoding/validation body, retained as independent baseline.
    if len(parts) > 0xFFFFFFFF or any(type(p) is not bytes or len(p) > 0xFFFFFFFF for p in parts):
        raise InvalidContext()
    return len(parts).to_bytes(4,'big') + b''.join(len(p).to_bytes(4,'big') + p for p in parts)


def test_same_session_paired_tuple_encoding():
    restored=key_module.tuple_bytes
    assert cf1.tuple_bytes is restored
    records=[]
    with single_tenant_public_cascade_application(rows=1000,unique=False) as app:
        run(app,chunk_size=256);publish(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        C=app.Customer
        specs=[('point',C.id==UUID(int=600),[(key,value) for key,(_,value) in app.source.items() if key==UUID(int=600)]),
               ('equality',C.name=='exact',[(key,value) for key,(_,value) in app.source.items() if value=='exact']),
               ('in2',C.name.in_(['exact','雪😀']),[(key,value) for key,(_,value) in app.source.items() if value in ['exact','雪😀']])]
        queries={family:(select(C.id,C.name).where(predicate).order_by(C.id),sorted(expected)) for family,predicate,expected in specs}
        try:
            with factory(tenant_id=TABLE_ID) as session:
                variants=[('original',original_tuple),('one_pass',restored)]
                for block in range(7):
                    for variant,function in (variants if block%2==0 else list(reversed(variants))):
                        key_module.tuple_bytes=cf1.tuple_bytes=function
                        for family,(statement,expected) in queries.items():
                            samples=[]
                            for iteration in range(50):
                                started=time.perf_counter_ns()
                                actual=list(session.execute(statement))
                                elapsed=(time.perf_counter_ns()-started)/1e6
                                assert actual==expected
                                if iteration>=10:samples.append(elapsed)
                            records.append(dict(block=block,variant=variant,family=family,rows=len(expected),samples_ms=samples,median_ms=statistics.median(samples)))
        finally:
            key_module.tuple_bytes=cf1.tuple_bytes=restored
    aggregate=[]
    for family in queries:
        medians={v:[r['median_ms'] for r in records if r['variant']==v and r['family']==family] for v in ['original','one_pass']}
        delta=[a-b for a,b in zip(medians['original'],medians['one_pass'])]
        aggregate.append(dict(family=family,median_ms={v:statistics.median(a) for v,a in medians.items()},paired_saved_ms=delta,positive_pairs=sum(d>0 for d in delta)))
    report=dict(scope='Synthetic1000-row same-session7 alternating paired blocks;40 samples/cell; only encoder function changes in process and always restores; all query results exact. No production latency or independent security qualification.',aggregate=aggregate,records=records)
    (Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent/'tuple-encoding-paired-performance.json').write_text(json.dumps(report,indent=2)+'\n')
