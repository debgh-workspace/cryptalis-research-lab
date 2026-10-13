"""Diagnostic profiles for the measured retained-layout overhead, not timings."""
import cProfile
import json
import os
import pstats
import sys
from pathlib import Path
from uuid import UUID
from sqlalchemy import select
sys.path.insert(0,str(Path(os.environ['GIT_WORK_TREE'])/'tests'))
from single_tenant_public_cascade_fixture import single_tenant_public_cascade_application
from test_migration import run, publish, keys, TABLE_ID
from cryptalis.sqlalchemy import attach


def test_profile_retained_result_paths():
    reports=[]
    with single_tenant_public_cascade_application(rows=1000,unique=False) as app:
        run(app,chunk_size=256);publish(app)
        factory=attach(app.mapping,app.runtime,lock=app.plan.lock_bytes,keys=keys,deployment=(app.plan,app.pin))
        C=app.Customer
        specs=[('point',C.id==UUID(int=600),[(key,value) for key,(_,value) in app.source.items() if key==UUID(int=600)]),
               ('equality',C.name=='exact',[(key,value) for key,(_,value) in app.source.items() if value=='exact']),
               ('in2',C.name.in_(['exact','雪😀']),[(key,value) for key,(_,value) in app.source.items() if value in ['exact','雪😀']])]
        with factory(tenant_id=TABLE_ID) as session:
            for family,predicate,expected in specs:
                expected=sorted(expected);statement=select(C.id,C.name).where(predicate).order_by(C.id)
                for _ in range(5):assert list(session.execute(statement))==expected
                profile=cProfile.Profile()
                for _ in range(40):
                    actual=profile.runcall(lambda:list(session.execute(statement)))
                    assert actual==expected
                stats=pstats.Stats(profile)
                entries=[dict(file=file,line=line,function=fn,primitive_calls=value[0],total_calls=value[1],self_seconds=value[2],cumulative_seconds=value[3]) for (file,line,fn),value in stats.stats.items()]
                reports.append(dict(family=family,rows=len(expected),iterations=40,top_cumulative=sorted(entries,key=lambda x:x['cumulative_seconds'],reverse=True)[:45],top_self=sorted(entries,key=lambda x:x['self_seconds'],reverse=True)[:25]))
    (Path(os.environ['CRYPTALIS_LAB_PROGRESS']).parent/'retained-search-profile.json').write_text(json.dumps(dict(scope='Instrumented diagnostic profiles only; do not compare instrumented seconds to uninstrumented benchmark latency',reports=reports),indent=2)+'\n')
