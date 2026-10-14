"""Data-only artifact/receipt consistency check. Never imports candidate code."""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).parent.absolute();OLD=ROOT.parent/'candidate-native-cf1-read-20261014'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
pins=json.loads((ROOT/'PINS.json').read_text())['pins']
for path,pin in pins.items():
    if sha(path)!=pin:raise RuntimeError('Pinned artifact changed: '+path)
old=json.loads((OLD/'ARTIFACTS.json').read_text())['files']
for name,pin in old.items():
    if sha(OLD/name)!=pin:raise RuntimeError('Original artifact changed: '+name)
manifest=json.loads((ROOT/'cases.json').read_text());ids=[c['id'] for c in manifest['cases']]
if len(ids)!=43 or len(set(ids))!=43:raise RuntimeError('Manifest identity mismatch')
for spec in manifest['fixtures'].values():
    if spec['text'].encode('utf8').hex()!=spec['encoded_text']:raise RuntimeError('Exact text mismatch')
    encoded=json.dumps(spec['descriptor'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    if hashlib.sha256(encoded).hexdigest()!=spec['descriptor_digest']:raise RuntimeError('Descriptor hash mismatch')
    base=OLD if spec['frame_origin']=='original' else ROOT
    if sha(base/spec['frame_path'])!=spec['frame_sha256']:raise RuntimeError('Frame hash mismatch')
positives=[];negatives=[]
for optimize in (0,1):
    positive=json.loads((ROOT/'evidence'/f'positive-o{optimize}-01.json').read_text())
    negative=json.loads((ROOT/'evidence'/f'negative-o{optimize}-01.json').read_text())
    launch=json.loads((ROOT/'evidence'/f'launch-negative-o{optimize}-01.json').read_text())
    if positive['optimize']!=optimize or positive['status']!='PASS' or positive['passed']!=ids:raise RuntimeError('Positive receipt mismatch')
    if len(positive['observations'])!=43:raise RuntimeError('Observation count mismatch')
    for actual,case in zip(positive['observations'],manifest['cases']):
        if actual['id']!=case['id'] or actual['actual']!=case['expected'] or actual['native_calls']!=case['native_calls']:
            raise RuntimeError('Exact observation mismatch')
    if (negative['optimize']!=optimize or launch['exit']!=1 or negative['status']!='FAIL' or negative['passed'] or
        negative.get('error_type')!='RuntimeError' or negative.get('error')!='Mismatch: actual-output-perturbation' or
        negative['observations']!=[{'id':'actual-output-perturbation','native_calls':1,'original_verified':True,
            'perturbation_applied_to_actual_return':True,'comparison_expected':'reject'}]):raise RuntimeError('Negative receipt mismatch')
    positives.append(positive);negatives.append(negative)
if positives[0]['observations']!=positives[1]['observations'] or negatives[0]['observations']!=negatives[1]['observations']:
    raise RuntimeError('Optimization-mode observations differ')
receipt={'status':'PASS','scope':'Data-only self-check; not independent execution attestation',
 'verified_pins':len(pins),'unchanged_original_artifacts':len(old),'positive_ids':ids,
 'positive_observations_equal_across_optimization':True,'negative_observations_equal_across_optimization':True,
 'manifest_sha256':sha(ROOT/'cases.json'),'pins_sha256':sha(ROOT/'PINS.json'),
 'original_inventory_sha256':sha(OLD/'ARTIFACTS.json')}
with (ROOT/'evidence/integrity-01.json').open('x') as out:json.dump(receipt,out,indent=2);out.write('\n')
print(json.dumps({'status':'PASS','verified_pins':len(pins),'unchanged_original_artifacts':len(old)}))
