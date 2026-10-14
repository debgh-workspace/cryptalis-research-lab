"""Explicitly selected additive sanitizer build/run supervisor. No automatic work."""
import json,os,re,sys
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
from guard_v3 import cache,check,exact,install,interpreter,loaded_origins,save,sha
from supervisor_v2 import bounded
operation,identifier,cache_path=sys.argv[1:]
if operation!='run':raise RuntimeError('D-only v3 has no build operation')
dest=R/(identifier+'-supervisor.json')
if dest.exists():raise RuntimeError('Refuse overwrite')
receipt={'status':'FAIL','operation':operation,'id':identifier,'integrity_errors':[]};f=None;anchor=None
try:
    receipt['cache_before']=cache(cache_path);install();f=check();anchor=f['_anchor'];interpreter(f,0)
    receipt.update(anchor=anchor,argv=list(sys.argv),environment=dict(os.environ),optimize=sys.flags.optimize)
    if dict(os.environ)!=f['compiler_environment']:raise RuntimeError('Controller environment not allowlisted')
    plan=next(x for x in f['runs'] if x['id']==identifier)
    child_cache=Path(plan['cache']);child_cache.mkdir()
    if list(child_cache.iterdir()):raise RuntimeError('New child cache not empty')
    child_path=R/(identifier+'-child.json')
    if child_path.exists():raise RuntimeError('Child receipt exists')
    run=bounded(plan['argv'],plan['environment'],180)
    receipt['child_supervision']=run
    if run['reason'] is not None or not run['leader_reaped'] or run['cleanup_errors'] or run['stdout'] or run['stderr']:raise RuntimeError('Sanitizer child failed containment or emitted diagnostics')
    child=json.loads(child_path.read_text());receipt.update(child_receipt=str(child_path),child_sha256=sha(child_path))
    if child['anchor']!=anchor or child['cache_before']!=[] or child['cache_final']!=[] or child['integrity_errors'] or child['id']!=identifier or list(child_cache.iterdir()):raise RuntimeError('Child guard failed')
    observations=child['observations'];ids=[o['id'] for o in observations];inventory=f['expected_ids'][plan['build']]
    if plan['mode']=='positive':
        if run['exit_code']!=0 or child['status']!='PASS' or ids!=inventory:raise RuntimeError('Positive child not accepted')
    else:
        target=plan['negative_target'];end=inventory.index(target)+1
        if run['exit_code']!=1 or child['status']!='FAIL' or child.get('error_type')!='RuntimeError' or child.get('error')!='Sanitizer subset actual-observation mismatch: '+target or child.get('negative_target')!=target or ids!=inventory[:end]:raise RuntimeError('Wrong negative result')
        record=observations[-1]
        if record.get('original_verified') is not True or record.get('negative_path')!=plan['negative_path']:raise RuntimeError('Unverified negative')
        import copy
        expected=copy.deepcopy(record['original']);node=expected
        for part in plan['negative_path'][:-1]:node=node[part]
        node[plan['negative_path'][-1]]+='00'
        if not exact(expected,record['actual']) or exact(record['original'],record['actual']):raise RuntimeError('Wrong actual perturbation')
    receipt['status']='PASS' if plan['mode']=='positive' else 'EXPECTED_FAIL'
except BaseException as exc:
    receipt.update(error_type=type(exc).__name__,error=str(exc))
finally:
    for name,operation in [('pins',lambda:check(anchor)),('cache',lambda:cache(cache_path)),('origins',lambda:loaded_origins(f) if f else None)]:
        try:
            value=operation()
            if name!='pins':receipt[name+'_final']=value
        except BaseException as exc:receipt['integrity_errors'].append(name+': '+repr(exc))
    if receipt['integrity_errors']:receipt['status']='FAIL_INTEGRITY'
    save(dest,receipt)
sys.exit(0 if receipt['status'] in ('PASS','EXPECTED_FAIL') else 1)
