import json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent;O=B/'candidate-native-cf1-read-20261014'
cases=[]
def add(i,op,expected='ValueError',**kw):
 cases.append(dict(id=i,kind='abi',op=op,expected={'exception':expected,'args':['Invalid private arity' if expected=='TypeError' else 'Python int too large to convert to C long' if expected=='OverflowError' else 'Invalid bounded private input'],'cause_none':True},**kw))
for p in (0,2,3,4,5,6):
 for j in range(3):add(f'abi/type/{p}/{j}','type',pos=p,variant=j)
for p in (2,3,4,5):
 for d in (-1,1):add(f'abi/length/{p}/{d}','length',pos=p,delta=d)
for b in (7,8):
 for p in range(5):
  for j in range(3):add(f'abi/material-type/{b}/{p}/{j}','material-type',bundle=b,pos=p,variant=j)
  for d in (-1,1):add(f'abi/material-length/{b}/{p}/{d}','material-length',bundle=b,pos=p,delta=d)
 for v in ('missing','extra','none','list'):add(f'abi/bundle/{b}/{v}','bundle',bundle=b,variant=v)
for v in ('short','long'):add('abi/arity/'+v,'arity','TypeError',variant=v)
for j,n in enumerate((0,15,17,24,25,26)):add(f'abi/record/{j}','record',length=n)
for j in range(5):add(f'abi/representation/{j}','representation','OverflowError' if j==4 else 'ValueError',variant=j)
for v in ('empty','over'):add('abi/frame/'+v,'frame',variant=v)
add('abi/storage-extra-search','storage-extra-search')
old=json.loads((O/'cases.json').read_text())
exact=json.loads((B/'candidate-native-read-admission-20261014/cases.json').read_text())
for mode in ('000','100'):
 selected=next(c for c in old['cases'] if c['id']==f'grid/grid-{mode}-1')
 success=next(c['expected'] for c in exact['cases'] if c['id']==selected['id'])
 refusal=next(c['expected'] for c in exact['cases'] if c['id']==f'keys/{mode}/pid')
 refusal=dict(refusal);refusal['trace']=success['trace'][:1];refusal['native_calls']=0
 cases.append({'id':'fork/'+mode,'kind':'fork','fixture_case':selected,'expected':{'inherited':refusal,'fresh':success,'child_exit':0}})
for v in ('silent','write-hang','oversize','invalid-json'):
 cases.append({'id':'containment/'+v,'kind':'containment','variant':v,'expected':{'category':'timeout' if v in ('silent','write-hang') else 'protocol','reaped':True,'fds_closed':True}})
if len({c['id'] for c in cases})!=len(cases):raise RuntimeError('Duplicate IDs')
with (R/'cases.json').open('x') as f:json.dump({'cases':cases,'abi_count':sum(c['kind']=='abi' for c in cases)},f,indent=2)
pins=json.loads((B/'candidate-native-read-admission-20261014/PINS.json').read_text())
print(type(pins),list(pins)[:5])
