"""Frozen standalone primitive experiment; no product timing claim."""
from pathlib import Path
import hashlib, importlib.util, json, resource, statistics, sysconfig, time
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV
from cryptography.hazmat.backends.openssl.backend import backend
R=Path(__file__).resolve().parent
binary=R/('native_direction'+sysconfig.get_config_var('EXT_SUFFIX'))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(R/'native_direction.c')=='5933299b46e349cd0e80032fd89beffd797e5ad04230cbfda1d985ef1eca0239'
assert sha(binary)=='393cf26a573870a9e7e1d3b12a3196528f9301f840214dbc05d84e1cb37575ed'
receipt=json.loads((R/'evidence/public-vector-checks-01.json').read_text());assert receipt['status']=='PASS' and receipt['count']==76
spec=importlib.util.spec_from_file_location('native_direction',binary);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
output=R/'evidence/frozen-direction-timing-01.json';assert not output.exists()
fixtures={}
for size in (7,32,128,4096):
 rows=[]; expected=[]
 for i in range(1000):
  seed=f'PUBLIC-C11-{size}-{i}'.encode();key=hashlib.sha256(seed).digest();nonce=hashlib.sha256(b'nonce'+seed).digest()[:12];aad=hashlib.sha256(b'aad'+seed).digest()[:31];plain=(hashlib.sha256(b'plain'+seed).digest()*((size+31)//32))[:size]
  rows.append((key,nonce,AESGCMSIV(key).encrypt(nonce,plain,aad),aad));expected.append(plain)
 fixtures[size]=(rows,expected)
def original(rows):return [AESGCMSIV(k).decrypt(n,c,a) for k,n,c,a in rows]
def candidate(rows):return [m.decrypt_once(k,n,c,a) for k,n,c,a in rows]
def clocks():return {'wall':time.perf_counter_ns(),'process':time.process_time_ns(),'thread':time.thread_time_ns()}
def resources():
 r=resource.getrusage(resource.RUSAGE_SELF);return {'user_s':r.ru_utime,'system_s':r.ru_stime,'voluntary_switches':r.ru_nvcsw,'involuntary_switches':r.ru_nivcsw,'maxrss_kib':r.ru_maxrss}
result={'scope':'Primitive construction-plus-decrypt only, not CF1/product','protocol_sha256':sha(R/'MICRO_PROTOCOL.md'),'harness_sha256':sha(Path(__file__)),'source_sha256':sha(R/'native_direction.c'),'binary_sha256':sha(binary),'native_backend':m.backend_version(),'pyca_backend':backend.openssl_version_text(),'samples':[],'status':'RUNNING'}
try:
 for block in range(7):
  for size,(rows,expected) in fixtures.items():
   for name in (('original','candidate') if block%2==0 else ('candidate','original')):
    fn=original if name=='original' else candidate
    assert fn(rows[:100])==expected[:100]
    r0=resources();c0=clocks();values=fn(rows);c1=clocks();r1=resources()
    assert values==expected;del values
    result['samples'].append({'block':block,'size':size,'variant':name,'operations':1000,'warmups':100,'before':c0,'after':c1,'elapsed_ns':{k:c1[k]-c0[k] for k in c0},'resources_before':r0,'resources_after':r1,'all_outputs_equal':True})
 summary={}
 for size in fixtures:
  pairs={n:[s['elapsed_ns']['wall']/1000 for s in result['samples'] if s['size']==size and s['variant']==n] for n in ['original','candidate']};old=statistics.median(pairs['original']);new=statistics.median(pairs['candidate']);ratio=new/old;favorable=sum(b<a for a,b in zip(pairs['original'],pairs['candidate']));primary=size!=4096
  summary[str(size)]={'original_median_per_item_ns':old,'candidate_median_per_item_ns':new,'ratio':ratio,'favorable_blocks':favorable,'primary':primary,'pass':(ratio<=.8 and favorable>=6) if primary else ratio<=1.05}
 result['summary']=summary;result['mechanism_pass']=all(x['pass'] for x in summary.values());result['status']='COMPLETE';result['operations']=56000;result['product_qualified']=False
finally:
 output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'mechanism_pass':result.get('mechanism_pass'),'summary':result.get('summary')},indent=2))
