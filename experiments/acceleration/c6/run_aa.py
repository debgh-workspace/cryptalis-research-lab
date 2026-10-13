"""One unchanged-code A/A diagnostic; no candidate method, engine or database."""
import argparse
import cProfile
import gc
import hashlib
import json
import platform
import pstats
import statistics
import time
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID
import sqlalchemy
from sqlalchemy import Column,Integer,Text,Uuid,select
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base
import cryptalis.sqlalchemy as adapter

BASELINE='fc2f7a7c983370f7c81874b56ec8e511532d226fc962bc0c8939b38d4daadfbe'

def clocks():
    return {'wall_ns':time.perf_counter_ns(),
            'raw_ns':time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW),
            'process_ns':time.process_time_ns(),'thread_ns':time.thread_time_ns()}

def delta(start,end):
    return {k:(end[k]-start[k])/1e6 for k in start}

def main(output):
    assert sqlalchemy.__version__=='2.0.51'
    assert hashlib.sha256(Path(adapter.__file__).read_bytes()).hexdigest()==BASELINE
    Base=declarative_base()
    class Subject(Base):
        __tablename__='subject'
        id=Column(Uuid,primary_key=True)
        tenant_id=Column(Uuid)
        name=Column(Text)
        rank=Column(Integer)
    owner=adapter._Attachment(Base.registry,SimpleNamespace(dialect=postgresql.dialect()),{},None)
    owner.bindings=[SimpleNamespace(column=Subject.__table__.c.name,
                                    descriptor=SimpleNamespace(equality=True))]
    before=dict(owner.__dict__)
    statements={
        'point':select(Subject.id,Subject.name).where(Subject.id==UUID(int=600)).order_by(Subject.id),
        'equality':select(Subject.id,Subject.name).where(Subject.name=='exact').order_by(Subject.id),
        'in2':select(Subject.id,Subject.name).where(Subject.name.in_(['exact','雪😀'])).order_by(Subject.id),
        'public_label':select(Subject.id,Subject.name,Subject.rank.label('chosen')).order_by('chosen')}
    counts={}
    for family,q in statements.items():
        profile=cProfile.Profile()
        for _ in range(100):profile.runcall(owner.admit,q)
        selected={}
        for (_,_,name),v in pstats.Stats(profile).stats.items():
            if name in ('admit','_admit_textual_references','references','protected','search_shape','iterate'):
                selected[name]=selected.get(name,0)+v[1]
        assert selected['admit']==100 and selected['_admit_textual_references']==100
        counts[family]=selected
    events=[];scope={'phase':'idle'}
    def observe_gc(phase,info):
        events.append({'phase':phase,'generation':info['generation'],
                       'collected':info.get('collected',0),'uncollectable':info.get('uncollectable',0),
                       'scope':dict(scope),'clocks':clocks()})
    records=[];failure=None
    settings={'enabled':gc.isenabled(),'thresholds':gc.get_threshold()}
    gc.callbacks.append(observe_gc)
    try:
        for block in range(9):
            for family,q in statements.items():
                for slot in (('A','B') if block%2==0 else ('B','A')):
                    scope.update(phase='warmup',block=block,family=family,slot=slot)
                    for _ in range(30):owner.admit(q)
                    scope['phase']='timed'
                    batches=[];completed=0;start=clocks()
                    for batch in range(10):
                        scope['batch']=batch
                        begin=clocks()
                        for _ in range(50):
                            owner.admit(q);completed+=1
                        end=clocks()
                        batches.append({'batch':batch,'calls':50,'start':begin,'end':end,'elapsed_ms':delta(begin,end)})
                    end=clocks()
                    assert completed==500 and owner.__dict__==before
                    records.append({'block':block,'family':family,'slot':slot,'calls':completed,
                                    'start':start,'end':end,'elapsed_ms':delta(start,end),'batches':batches})
                    scope['phase']='between'
    except BaseException as exc:
        failure=type(exc).__name__
    finally:
        gc.callbacks.remove(observe_gc)
    assert settings=={'enabled':gc.isenabled(),'thresholds':gc.get_threshold()}
    spans=[];pending={}
    for event in events:
        generation=event['generation']
        if event['phase']=='start':pending[generation]=event
        elif generation in pending:
            start=pending.pop(generation)
            spans.append({'generation':generation,'start':start['clocks'],'end':event['clocks'],
                          'elapsed_ms':delta(start['clocks'],event['clocks']),'scope':start['scope'],
                          'collected':event['collected'],'uncollectable':event['uncollectable']})
    for r in records:
        r['gc_overlap_ms']=sum(max(0,min(r['end']['wall_ns'],s['end']['wall_ns'])-
                                  max(r['start']['wall_ns'],s['start']['wall_ns']))/1e6 for s in spans)
        a,b=r['elapsed_ms']['wall_ns'],r['elapsed_ms']['raw_ns']
        r['clock_disagreement']=abs(a-b)>0.05 and abs(a-b)/a>0.01
    pairs=[]
    for family in statements:
        for block in range(9):
            found=[r for r in records if r['family']==family and r['block']==block]
            if len(found)!=2:continue
            a,b=({r['slot']:r for r in found}[slot] for slot in ('A','B'))
            wall=b['elapsed_ms']['wall_ns']-a['elapsed_ms']['wall_ns']
            cpu=b['elapsed_ms']['thread_ns']-a['elapsed_ms']['thread_ns']
            pct=100*wall/a['elapsed_ms']['wall_ns']
            pairs.append({'family':family,'block':block,'order':[r['slot'] for r in found],
                          'B_minus_A_wall_ms':wall,'B_minus_A_thread_ms':cpu,'B_minus_A_percent':pct,
                          'material':abs(pct)>=10,'wall_dominant':abs(wall)>=1 and abs(cpu)<=0.25*abs(wall),
                          'A_gc_ms':a['gc_overlap_ms'],'B_gc_ms':b['gc_overlap_ms']})
    classification=('INVALID' if failure or len(records)!=72 or pending else
                    'MATERIAL_PAIRED_VARIANCE' if any(p['material'] for p in pairs) else 'NOT_DEMONSTRATED')
    result={'question':'identical-code A/A measurement validity; no C5 retest','classification':classification,
            'baseline_sha256':BASELINE,'python':platform.python_version(),'sqlalchemy':sqlalchemy.__version__,
            'failure':failure,'gc_settings_unchanged':settings,
            'clock_info':{k:vars(time.get_clock_info(k)) for k in ('perf_counter','process_time','thread_time')},
            'call_counts_per_100':counts,'records':records,'pairs':pairs,'gc_events':events,'gc_spans':spans,
            'clock_disagreements':sum(r['clock_disagreement'] for r in records),
            'limits':'Telemetry changes workload cost; no outlier removal/noise correction or C5 reclassification.'}
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'classification':classification,'cells':len(records),'pairs':len(pairs),
                      'material_pairs':sum(p['material'] for p in pairs),'wall_dominant_pairs':sum(p['wall_dominant'] for p in pairs),
                      'gc_spans':len(spans),'clock_disagreements':result['clock_disagreements'],'failure':failure},indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
