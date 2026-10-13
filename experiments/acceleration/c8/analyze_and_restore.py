"""Lossless C8 receipt restore and deterministic analysis. No database/imports."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import statistics

PARTS = [
 ('raw-profiles.xz.part-01',700000,'7d0eaf6ed897edb438fdf298a8c1c8d1b0c4d6bc5b3f33f34a45a8a37754051d'),
 ('raw-profiles.xz.part-02',700000,'37bd0e49e98a053319dac77e1c785db7bd00a0a87e368fdbde102c8641285ffc'),
 ('raw-profiles.xz.part-03',700000,'4be8d71a20a76086f09b6140b3701ff1fddcb70ab4ca6066e0d230bcae33f864'),
 ('raw-profiles.xz.part-04',246796,'84f438970361433eb8d2c8c2c5ac25ba6e71a62e11e73a5bb95c6e7b679f5e35'),
]
RAW = [
 ('sa21',1179720,40648581,'73727793b304a39e21c9b927f1d42d443a9f12ca43732850176043004e1c0c9b'),
 ('sa20',1167076,40280593,'a2affd3a0a7fa90df56a304ca10de03a30caa51b3c5adb963455ae37db407e29'),
]
FAMILIES = ('point','eq_miss','eq_hot','in2_miss','in2_hot','in20_miss','in20_hot','in20_duplicate')
ROWS = dict(zip(FAMILIES,(1,0,143,0,286,0,286,286)))
TERMS = dict(zip(FAMILIES,(0,1,1,2,2,20,20,20)))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def restore(parts_dir, output_dir):
    pieces = []
    for name, size, expected in PARTS:
        data = (parts_dir/name).read_bytes()
        assert len(data)==size and sha(data)==expected, name
        pieces.append(data)
    joined=b''.join(pieces); output_dir.mkdir(parents=True,exist_ok=True)
    offset=0; receipt=[]
    for cell,compressed_size,raw_size,expected in RAW:
        data=lzma.decompress(joined[offset:offset+compressed_size]);offset+=compressed_size
        assert len(data)==raw_size and sha(data)==expected,cell
        path=output_dir/f'indexed-cost-profile-{cell}.json'
        with path.open('xb') as stream:stream.write(data)
        receipt.append({'cell':cell,'raw_bytes':raw_size,'sha256':expected})
    assert offset==len(joined)
    return receipt


def median(values):
    return statistics.median(values)


def bucket(filename):
    if '/cryptalis/crypto/cf1.py' in filename:return 'CF1_self'
    if '/cryptalis/crypto/keys.py' in filename:return 'keys_and_tuple_self'
    if '/cryptalis/' in filename:return 'other_cryptalis_self'
    if '/cryptography/' in filename:return 'crypto_backend_python_self'
    if '/sqlalchemy/sql/compiler.py' in filename:return 'SQL_compiler_self'
    if '/sqlalchemy/' in filename:return 'other_SQLAlchemy_self'
    if '/psycopg/' in filename:return 'driver_Python_self'
    return 'builtins_stdlib_other_self'


def profile_fact(row):
    total=search=payload=0.0; counts={}; exclusive={}; top={}
    for phase in row['phases'].values():
        p=phase['profile'];total+=p['total_cpu_s']
        for name,value in p['named'].items():counts[name]=counts.get(name,0)+value['calls']
        for f in p['functions']:
            kind=bucket(f['function'][0]);exclusive[kind]=exclusive.get(kind,0.0)+f['self_cpu_s']
            identifier=':'.join(map(str,f['function']));top[identifier]=top.get(identifier,0.0)+f['self_cpu_s']
            if f['function'][0].endswith('/crypto/cf1.py') and f['function'][2]=='_derive':
                for c in f['callers']:
                    if c['function'][2]=='_term':search+=c['stats'][3]
                    if c['function'][2]=='open_text':payload+=c['stats'][3]
    assert abs(sum(exclusive.values())-total)<1e-8
    return {'pair':row['pair'],'counts':counts,'profiled_thread_cpu_ms':1000*total,
            'search_KDF_caller_cpu_ms':1000*search,'payload_KDF_caller_cpu_ms':1000*payload,
            'search_KDF_share_percent':100*search/total,'payload_KDF_share_percent':100*payload/total,
            'exclusive_cpu_ms':{k:1000*v for k,v in exclusive.items()},
            'largest_exclusive_cpu_ms':sorted(([k,1000*v] for k,v in top.items()),key=lambda x:x[1],reverse=True)[:12]}


def analyze(cell,path):
    data=path.read_bytes();expected=next(r for r in RAW if r[0]==cell)
    assert len(data)==expected[2] and sha(data)==expected[3]
    d=json.loads(data);obs=d['observations']
    assert d['failure'] is None and d['source_unchanged'] and d['source_before']==d['source_after']
    assert d['source_before']['files']==201 and d['source_before']['manifest_sha256']=='aba658622e884084762e09be61aed54c7a1023af37d332af9f5143aa5e358688'
    assert d['gc_settings_unchanged'] and d['all_count_predictions_match'] and d['schedule_complete']
    schedule=[]
    for family in FAMILIES:
        for projection in ('ids','text'):
            for mode,count in (('warmup',3),('timed',10),('profiled',3)):
                for pair in range(count):
                    for which in (('native','protected') if pair%2==0 else ('protected','native')):
                        schedule.append((family,projection,mode,pair,which))
    assert len(obs)==512 and [(r['family'],r['projection'],r['phase'],r['pair'],r['path']) for r in obs]==schedule
    assert all(r['exact_native'] and r['rows']==ROWS[r['family']] and r['terms']==TERMS[r['family']] for r in obs)
    protected_profiles=[r for r in obs if 'prediction' in r];assert len(protected_profiles)==48
    for r in protected_profiles:
        count=ROWS[r['family']] if r['projection']=='text' else 0;terms=TERMS[r['family']]
        expect={'term':terms+count,'derive':terms+2*count,'open_text':count,'resolve':2*terms+4*count}
        observed={name:sum(p['profile']['named'][name]['calls'] for p in r['phases'].values()) for name in expect}
        assert observed==expect==r['prediction']['observed']==r['prediction']['predicted'] and r['prediction']['matches']
    controls=d['native_controls'];assert len(controls)==16 and all(c['exact_native'] for c in controls)
    assert all(c['rows']==(143 if c['family']=='in_hot_null' else 0) for c in controls)
    groups=[]
    for family in FAMILIES:
        for projection in ('ids','text'):
            for which in ('native','protected'):
                rows=[r for r in obs if r['family']==family and r['projection']==projection and r['path']==which]
                timed=[r for r in rows if r['phase']=='timed'];profiles=[r for r in rows if r['phase']=='profiled']
                assert len(timed)==10 and len(profiles)==3
                phase_medians={phase:{name.removesuffix('_ns')+'_ms':median(r['phases'][phase]['elapsed_ms'][name] for r in timed)
                               for name in ('wall_ns','raw_ns','process_ns','thread_ns')} for phase in ('execute','fetch_all')}
                api_sums={name.removesuffix('_ns')+'_ms':median(sum(p['elapsed_ms'][name] for p in r['phases'].values()) for r in timed)
                          for name in ('wall_ns','raw_ns','process_ns','thread_ns')}
                facts=[profile_fact(r) for r in profiles]
                counts={phase:{name:[r['phases'][phase]['profile']['named'][name]['calls'] for r in profiles]
                                    for name in profiles[0]['phases'][phase]['profile']['named']}
                        for phase in ('execute','fetch_all')}
                groups.append({'family':family,'projection':projection,'path':which,'rows':ROWS[family],'terms':TERMS[family],
                    'timed_samples':10,'API_phase_medians_ms':phase_medians,'median_sum_of_API_phases_ms':api_sums,
                    'profiled_samples':3,'profiled_facts':facts,'phase_named_calls':counts,
                    'median_search_KDF_share_percent':median(f['search_KDF_share_percent'] for f in facts)})
    assert len(d['plans'])==32
    return {'cell':cell,'sqlalchemy':d['sqlalchemy'],'raw_bytes':len(data),'raw_sha256':sha(data),
        'source_binding':d['source_before'],'source_unchanged':True,'failure':None,
        'observations':512,'warmup':96,'timed':320,'profiled_queries':96,'profiled_phases':192,
        'protected_count_predictions':48,'all_native_equal':True,'native_controls':controls,
        'exact_schedule_verified':True,'gc_event_count':len(d['gc_events']),
        'process_maxrss_highwater_kib':max(r['maxrss_kib_process_highwater'] for r in d['resources']),
        'plans_with_index_node':sum(p['plan']['index_node_present'] for p in d['plans']),
        'safe_plans':d['plans'],'groups':groups}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parts-dir',type=Path)
    parser.add_argument('--restore-dir',type=Path)
    parser.add_argument('--input-dir',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.parts_dir:
        assert args.restore_dir is not None
        print(json.dumps({'restored':restore(args.parts_dir,args.restore_dir)}))
    if args.input_dir:
        assert args.output is not None
        report={'scope':'C8 unchanged S18 attribution; no optimization or speedup gate',
            'source_commit':'5492cc04ee6c5d6696c9e9fc261f12fa61236043',
            'units':'Raw start/end clock fields are ns. Raw elapsed_ms values are ms despite nested _ns labels. cProfile values are thread CPU seconds.',
            'timing_limits':'Unprofiled API phases still contain clock/GC observation overhead. Their sum excludes harness work between phases; no end-to-end request latency or speedup is inferred.',
            'profile_limits':'Python timer/cProfile overhead materially inflates CPU time. Search/payload KDF caller times are separate; nested inclusive costs are not summed.',
            'parts':[{'name':n,'bytes':b,'sha256':h} for n,b,h in PARTS],
            'cells':[analyze(cell,args.input_dir/f'indexed-cost-profile-{cell}.json') for cell,_,_,_ in RAW]}
        with args.output.open('x') as stream:json.dump(report,stream,separators=(',',':'));stream.write('\n')
        print(json.dumps({'cells':2,'observations':1024,'native_controls':32,'predictions':96,'profiled_phases':384}))
    assert args.parts_dir or args.input_dir

if __name__=='__main__':main()
