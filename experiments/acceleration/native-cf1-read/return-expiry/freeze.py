"""Stdlib-only two-case declaration; no candidate/native imports."""
import copy, hashlib, json
from pathlib import Path
R=Path(__file__).absolute().parent; B=R.parent
A=B/'candidate-native-read-admission-20261014'
source=json.loads((A/'cases.json').read_text())
cases=[]; fixtures={}
for eq,purpose,label in [(0,'payload','storage'),(1,'search','equality')]:
    name=f'grid-{eq}00-1'; spec=copy.deepcopy(source['correction_fixtures'][name]); fixtures[name]=spec
    prior=next(c for c in source['cases'] if c['id']==f'correction/decode-expiry/{eq}/{purpose}')
    expected=copy.deepcopy(prior['expected'])
    initial=expected['trace'][:2 if eq else 1]
    expected.update(value_published=False, cause_suppressed=False,
        native_return={'type':'bytes','hex':'61626364656667'},
        events=[{'event':'native-return','trace':initial},
                {'event':'expire','purpose':purpose,'generation':spec[purpose+'_generation'],'expired':True,'trace':initial},
                {'event':'decode-call','expired':True,'trace':initial},
                {'event':'decode-return','expired':True,'trace':initial}])
    if spec['text']!='abcdefg' or spec['encoded_text']!='61626364656667':raise RuntimeError('Precursor fixture drift')
    cases.append({'id':f'after-native-return/{label}/{purpose}','fixture':name,'purpose':purpose,'expected':expected})
ids=[c['id'] for c in cases]
if ids!=['after-native-return/storage/payload','after-native-return/equality/search'] or len(set(ids))!=2:raise RuntimeError('ID coverage')
manifest={'scope':'Two newly frozen immediate-after-native-return expiry cases only; full qualification and timing remain held',
    'source_manifest_sha256':hashlib.sha256((A/'cases.json').read_bytes()).hexdigest(),
    'fixtures':fixtures,'cases':cases,'case_count':2,'optimization_modes':[0,1],
    'negative_controls':[{'mode':mode,'case_id':case['id'],'expected_exit':1,'error':'Exact return-expiry mismatch'} for mode,case in zip(('metadata','trace'),cases)]}
with (R/'cases.json').open('x') as out:json.dump(manifest,out,ensure_ascii=False,indent=2);out.write('\n')
print(json.dumps({'cases':2,'sha256':hashlib.sha256((R/'cases.json').read_bytes()).hexdigest(),'crypto_imports':False}))
