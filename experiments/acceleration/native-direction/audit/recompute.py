"""Read data and source bytes only. Never import or execute candidate code."""
import hashlib,json,statistics
from pathlib import Path
R=Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/candidate-native-direction-probe-20261014')
O=Path(__file__).parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((R/'evidence/frozen-direction-timing-01.json').read_text())
s=f['samples']; checks={}
expected=[(b,n,v) for b in range(7) for n in (7,32,128,4096) for v in (('original','candidate') if b%2==0 else ('candidate','original'))]
checks['schedule_exact']= [(r['block'],r['size'],r['variant']) for r in s]==expected
checks['all_elapsed_match']=all(r['elapsed_ns'][k]==r['after'][k]-r['before'][k]>0 for r in s for k in ('wall','process','thread'))
checks['clock_order']=all(s[i]['after'][k]<s[i+1]['before'][k] for i in range(len(s)-1) for k in ('wall','process','thread'))
checks['counts_and_output_flags']=all(r['operations']==1000 and r['warmups']==100 and r['all_outputs_equal'] is True for r in s)
checks['measured_total']=sum(r['operations'] for r in s)==f['operations']==56000
checks['resources_monotonic']=all(r['resources_after'][k]>=r['resources_before'][k] for r in s for k in r['resources_before'])
summary={}
for n in (7,32,128,4096):
 pairs={v:[next(r for r in s if (r['block'],r['size'],r['variant'])==(b,n,v))['elapsed_ns']['wall']/1000 for b in range(7)] for v in ('original','candidate')}
 a,b=(statistics.median(pairs[v]) for v in ('original','candidate'))
 favorable=sum(y<x for x,y in zip(pairs['original'],pairs['candidate']))
 recomputed={'original_median_per_item_ns':a,'candidate_median_per_item_ns':b,'ratio':b/a,'favorable_blocks':favorable,'primary':n!=4096,'pass':(b/a<=.8 and favorable>=6) if n!=4096 else b/a<=1.05}
 checks[f'summary_{n}_exact']=recomputed==f['summary'][str(n)]
 summary[str(n)]={**recomputed,'reduction_percent':100*(1-b/a),'per_block_wall_ns':pairs,'paired_ratios':[y/x for x,y in zip(pairs['original'],pairs['candidate'])]}
checks['mechanism_pass_exact']=f['mechanism_pass']==all(r['pass'] for r in summary.values())
hashes={str(p.relative_to(R)):sha(p) for p in R.rglob('*') if p.is_file()}
manifest=json.loads((R/'evidence/source-manifest.json').read_text())
checks['manifest_entries_match']=all(hashes[k]==v for k,v in manifest.items())
for key,path in [('protocol','MICRO_PROTOCOL.md'),('harness','measure_direction.py'),('source','native_direction.c'),('binary','native_direction.cpython-312-x86_64-linux-gnu.so')]:
 checks[f'timing_{key}_hash_match']=f[key+'_sha256']==hashes[path]
r=json.loads((R/'evidence/public-vector-checks-01.json').read_text())
fixture=R.parent/'candidate-accel-payload-integrated-20261014/tests/fixtures/cf1_vectors.json'
checks['fixture_hash_match']=sha(fixture)==r['fixture_sha256']
checks['correctness_source_binary_match']=all(r[k+'_sha256']==f[k+'_sha256'] for k in ('source','binary'))
labels=[f'rfc8452-vector-{i}' for i in range(len(json.loads(fixture.read_text())['primitive_vectors']['aes256_gcm_siv']))]
for n in (0,1,7,16,17,31,1024,65536):
 labels += [f'pyca-public-fixture-{n}']+[f'public-fixture-auth-refusal-{n}-{p}' for p in range(4)]+[f'fresh-call-after-refusal-{n}']
labels += [f'exact-type-{p}-{t}' for p in range(4) for t in ('bytearray','memoryview','str','NoneType')]
labels += [f'length-{p}-{n}' for p,n in [(0,0),(0,31),(0,33),(1,11),(1,13),(2,15),(2,16777233),(3,16777217)]]
checks['correctness_labels_exact']=r['passed_checks']==labels and r['count']==len(labels)==76 and r['status']=='PASS'
keys=[];nonces=[]
for n in (7,32,128,4096):
 for i in range(1000):
  seed=f'PUBLIC-C11-{n}-{i}'.encode();keys.append(hashlib.sha256(seed).digest());nonces.append(hashlib.sha256(b'nonce'+seed).digest()[:12])
checks['fixture_keys_unique']=len(set(keys))==4000
checks['fixture_nonces_unique']=len(set(nonces))==4000
result={'method':'Independent standard-library-only data/source-byte inspection; candidate never imported or executed','checks':checks,'all_checks_pass':all(checks.values()),'sample_count':len(s),'measured_operations':sum(r['operations'] for r in s),'declared_warmups':sum(r['warmups'] for r in s),'elapsed_wall_span_ns':s[-1]['after']['wall']-s[0]['before']['wall'],'summary':summary,'observed_sha256':hashes,'manifest_unlisted_files':sorted(set(hashes)-set(manifest))}
(O/'recomputed-evidence.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('summary','observed_sha256')},indent=2));print(json.dumps(summary,indent=2))
