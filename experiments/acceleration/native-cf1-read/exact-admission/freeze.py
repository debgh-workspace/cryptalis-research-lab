"""Stdlib-only predeclaration. Never imports product/native crypto."""
import copy,hashlib,json
from pathlib import Path
R=Path(__file__).absolute().parent;B=R.parent
O=B/'candidate-native-cf1-read-20261014';C=B/'candidate-native-cf1-read-correction-20261014'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
old=read(O/'cases.json');correction=read(C/'cases.json')
vectors=read(B/'candidate-s20-restored-20261014/tests/fixtures/cf1_vectors.json')['vectors']
texts=['','abcdefg','x'*32,'x'*128,'x'*4096,'café','cafe\u0301','雪😀\n']
def exact_text(name):
    spec=old['fixtures'][name]
    if 'text' in spec:return spec['text']
    if name.startswith('grid-'):return texts[int(name.rsplit('-',1)[1])]
    if name.startswith('endpoint-'):return 'endpoint'
    if name.startswith('nil-'):return 'nil'
    if name.startswith('max-'):return 'x'*(16*1024*1024)
    raise RuntimeError('No independent exact text: '+name)
def upgrade(expected,name,count):
    result=copy.deepcopy(expected)
    if 'exception' in result:result.update(args_safe=True,cause_none=True)
    else:
        previous=result['value'];value=None if previous is None else exact_text(name)
        if previous is not None:
            encoded=value.encode('utf8')
            if previous!={'bytes':len(encoded),'sha256':hashlib.sha256(encoded).hexdigest()}:
                raise RuntimeError('Independent text disagrees with old digest: '+name)
        result.update(value=value,value_type=type(value).__name__)
    result['native_calls']=count
    return result
cases=[]
for original in old['cases']:
    case=copy.deepcopy(original);e=case['expected'];n=0
    initial=2 if old['fixtures'][case['fixture']]['descriptor']['representation']=='cf1-packed-equality/v1' else 1
    if 'value' in e:n=0 if e['value'] is None else 1
    elif e['exception']=='KeyUnavailable':n=int(len(e['trace'])>initial)
    elif e['exception'] in ('AuthenticationFailed','InvalidText','RepresentationMismatch'):n=int(len(e['trace'])>=initial)
    case['expected']=upgrade(e,case['fixture'],n);case['kind']='original';cases.append(case)
for oldcase in correction['cases']:
    case=copy.deepcopy(oldcase);case['id']='correction/'+case['id'];case['source_kind']=case['kind'];case['kind']='correction'
    case['expected']['native_calls']=case.pop('native_calls')
    if 'exception' in case['expected']:case['expected'].update(args_safe=True,cause_none=True)
    cases.append(case)
for v in vectors:
    eq=bool(v['search_generation']);pre=['payload','search'] if eq else ['payload']
    trace=[[v['domain_id'],v['tenant_id'],p,v[p+'_generation']] for p in pre+pre]
    cases.append({'id':'seal-frozen/'+v['name'],'kind':'seal','vector':v['name'],
        'expected':{'value':v['frame'],'value_type':'bytes','trace':trace,'native_calls':0}})
    if eq:
        trace=[[v['domain_id'],v['tenant_id'],'search',v['search_generation']]]*2
        cases.append({'id':'query-frozen/'+v['name'],'kind':'query','vector':v['name'],
            'expected':{'value':v['term'],'value_type':'bytes','trace':trace,'native_calls':0}})
for concurrency in ('threads','event-loop'):
    for eq in (0,1):
        for scope,name in [('A',f'grid-{eq}00-1'),('B',f'scope-B-{eq}')]:
            source=next(c for c in correction['cases'] if c['kind']=='scope' and c['fixture']==name and not c.get('null_frame'))
            e=copy.deepcopy(source['expected']);e['native_calls']=1
            cases.append({'id':f'{concurrency}/{eq}/{scope}','kind':concurrency,'fixture':name,'group':f'{concurrency}/{eq}','expected':e})
ids=[c['id'] for c in cases]
if len(ids)!=1098 or len(set(ids))!=len(ids):raise RuntimeError('Unexpected ID coverage')
for origin,fixtures in [(O,old['fixtures']),(C,correction['fixtures'])]:
    for spec in fixtures.values():
        base=O if spec.get('frame_origin')=='original' else origin
        if sha(base/spec['frame_path'])!=spec['frame_sha256']:raise RuntimeError('Fixture hash mismatch')
negative=[{'mode':m,'case_id':'keys/100/payload' if m=='stage' else 'grid/grid-100-1','error':'Exact admission mismatch','expected_exit':1} for m in ('text','type','stage','trace')]
manifest={'scope':'NEW finite exact-output wrapper oracle; historical originals unchanged; full DESIGN HOLD',
 'original_manifest_sha256':sha(O/'cases.json'),'original_ids':[c['id'] for c in old['cases']],
 'original_fixtures':old['fixtures'],'correction_fixtures':correction['fixtures'],'vectors':vectors,
 'cases':cases,'negative_controls':negative,'optimization_modes':[0,1],'case_count':len(cases)}
with (R/'cases.json').open('x') as out:json.dump(manifest,out,ensure_ascii=False,indent=2);out.write('\n')
print(json.dumps({'cases':len(cases),'sha256':sha(R/'cases.json'),'crypto_imports':False}))
