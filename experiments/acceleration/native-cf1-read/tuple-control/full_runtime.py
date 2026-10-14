"""T-specific full-wrapper oracle runner. SOURCE PREPARATION, not yet executed."""
import asyncio,concurrent.futures,copy,importlib.util,json,os,sys,threading
from pathlib import Path
from types import SimpleNamespace
import native_tuple as native,tuple_read as nr,fixture_support as original
from cryptalis.crypto import cf1,keys
R=Path(__file__).absolute().parent; B=R.parent; C=B/'candidate-native-cf1-read-correction-20261014'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module;spec.loader.exec_module(module);return module
correction=load('admission_correction_support',C/'support.py')
# New isolated namespace, exact original bytes; never replace canonical cf1/os.
isolated=load('cryptalis.crypto._admission_baseline',B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py')
manifest=json.loads((B/'candidate-native-read-admission-20261014/cases.json').read_text())
counts=json.loads((R/'FULL_EXPECTATIONS.json').read_text())['cases']
for case, count in zip(manifest['cases'], counts):
    if case['id'] != count['id']: raise RuntimeError('Count index mismatch')
    case['expected'].pop('native_calls')
    case['expected']['tuple_entries']=count['tuple_entries']
if len(counts)!=1098 or len(manifest['cases'])!=1098: raise RuntimeError('Coverage mismatch')
local=threading.local();groups={}
observations=[];negative_record=None

def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def exact(a,b):
    if not same(a,b):raise RuntimeError('Exact admission mismatch')

SITES=('payload-info','payload-salt','aad','search-info','search-salt','equality-message')
DECODE_LINE=None

def routed(*args):
    local.calls+=1
    ordinal=local.calls
    if not 1<=ordinal<=6:raise RuntimeError('Unexpected tuple count')
    site=SITES[ordinal-1]
    expected_tags=(b'CF1/payload-key',b'CF1/root',b'CF1/payload',b'CF1/search-key',b'CF1/root',b'equality')
    if not args or type(args[0]) is not bytes or args[0]!=expected_tags[ordinal-1]:
        raise RuntimeError('Tuple site order mismatch')
    result=native.tuple_bytes(*args)
    if type(result) is not bytes:raise RuntimeError('Tuple did not return exact bytes')
    local.sites.append(site)
    if local.case.get('source_kind')=='post-native-pid' and ordinal==local.last_tuple:
        object.__setattr__(local.prepared,'_pid',os.getpid()+1)
        local.pid_hook+=1
    return result

def trace_decode(frame,event,arg):
    if frame.f_code is nr.open_text.__code__ and event=='line' and frame.f_lineno==DECODE_LINE:
        if local.decoded:raise RuntimeError('Decode hook repeated')
        if type(frame.f_locals.get('encoded')) is not bytes or type(frame.f_locals.get('value')) is not str:
            raise RuntimeError('Decode boundary type mismatch')
        local.decoded=True
        correction.expire(local.prepared,local.case['purpose'])
    return trace_decode

def observe(fn,args):
    prepared=args[-1]
    if hasattr(prepared,'trace'):prepared.trace.clear()
    try:value=fn(*args)
    except keys.CryptoFailure as exc:
        result={name:getattr(exc,name) for name in ('code','stage','retryable','effects','remedy')}
        safe=(f'{exc.code} during {exc.stage}. {exc.remedy} Operation {exc.operation_id}.',)
        result.update(exception=type(exc).__name__,operation_present=type(exc.operation_id) is str and bool(exc.operation_id),
            args_safe=exc.args==safe,cause_none=exc.__cause__ is None)
    else:
        if type(value) not in (str,bytes,type(None)):raise RuntimeError('Unexpected result type')
        result={'value':value.hex() if type(value) is bytes else value,'value_type':type(value).__name__}
    result.update(trace=copy.deepcopy(getattr(prepared,'trace',[])),tuple_entries=local.calls)
    return result

def correction_args(case):
    spec=manifest['correction_fixtures'][case['fixture']];f,t,r=correction.values(spec)
    kind=case.get('source_kind')
    if kind=='scope':
        identity=(case['group'],case['fixture'])
        if identity not in groups:groups[identity]=correction.keys(spec)
        prepared=groups[identity]
    elif kind=='lifecycle':
        identity=case['group'];state=case['state']
        if state=='valid':groups[identity]=correction.keys(spec)
        if identity not in groups:raise RuntimeError('Missing lifecycle predecessor')
        if state=='expire':correction.expire(groups[identity])
        if state=='fresh':
            previous=groups[identity];groups[identity]=correction.keys(spec)
            if previous is groups[identity]:raise RuntimeError('Not fresh public material')
        prepared=groups[identity]
    else:prepared=correction.keys(spec,policy_domain=case.get('policy_domain'))
    raw=None if case.get('null_frame') else b'' if case.get('empty_frame') else correction.frame(spec)
    return raw,f,t,r,prepared

def invoke(case):
    local.calls=0;local.decoded=False;local.case=case;local.sites=[];local.pid_hook=0
    if case['kind']=='original':args=original.invocation(case,manifest['original_fixtures']);reader=nr.open_text
    elif case['kind'] in ('correction','threads','event-loop'):args=correction_args(case);reader=nr.open_text
    elif case['kind'] in ('seal','query'):
        spec=next(v for v in manifest['vectors'] if v['name']==case['vector'])
        f,t,r=original.fields(spec);prepared=original.make_keys(spec,f,t)
        if case['kind']=='seal':
            f=isolated.FieldDescriptor.from_compiled(spec['descriptor'],spec['descriptor_digest'])
            nonce=bytes.fromhex(spec['nonce'])
            def public_nonce(n):
                if n!=12:raise RuntimeError('Unexpected nonce size')
                local.nonce_calls+=1;return nonce
            local.nonce_calls=0;isolated.os=SimpleNamespace(urandom=public_nonce)
            reader=isolated.seal_text;args=(spec['text'],f,t,r,prepared)
        else:reader=cf1.equality_term;args=(spec['text'],f,t,prepared)
    else:raise RuntimeError('Unknown predeclared case')
    local.prepared=args[-1]
    local.last_tuple=6 if case.get('source_kind')=='post-native-pid' and args[1].equality else 3
    old_trace=sys.gettrace()
    hook=case.get('source_kind')=='decode-expiry' and not getattr(local,'suppress_hook',False)
    if hook and old_trace is not None:raise RuntimeError('Unexpected existing tracer')
    try:
        if hook:sys.settrace(trace_decode)
        actual=observe(reader,args)
    finally:
        if hook:sys.settrace(old_trace)
    if case.get('source_kind')=='decode-expiry' and not getattr(local,'suppress_hook',False) and not local.decoded:raise RuntimeError('Decode hook not reached')
    if case['kind']=='seal' and local.nonce_calls!=1:raise RuntimeError('Nonce stub count mismatch')
    return {'id':case['id'],'actual':actual,'decode_hook_completed':local.decoded,
            'synthetic_nonce_calls':local.nonce_calls if case['kind']=='seal' else 0,
            'tuple_sites':list(local.sites),'pid_hook_count':local.pid_hook}

def accept(case,record):
    exact(record['actual'],case['expected'])
    exact(record['tuple_sites'],list(SITES[:case['expected']['tuple_entries']]))
    exact(record['pid_hook_count'],1 if case.get('source_kind')=='post-native-pid' else 0)
    observations.append(record)

def run(mode):
    global negative_record
    global DECODE_LINE
    hook_plan=json.loads((R/'FULL_HOOKS.json').read_text())
    DECODE_LINE=hook_plan['decode_line']
    old_tuple=nr._native_tuple_bytes
    nr._native_tuple_bytes=routed
    try:
        if mode!='positive':
            control=next(n for n in json.loads((R/'FULL_HOOKS.json').read_text())['negatives'] if n['mode']==mode)
            case=next(c for c in manifest['cases'] if c['id']==control['case_id'])
            record=invoke(case);exact(record['actual'],case['expected'])
            mutated=copy.deepcopy(record['actual'])
            if mode=='hook':
                local.suppress_hook=True
                try:mutated=invoke(case)['actual']
                finally:local.suppress_hook=False
            elif mode=='count':mutated['tuple_entries']+=1
            if mode=='text':mutated['value']+='!ADMISSION-NEGATIVE!'
            elif mode=='type':mutated['value_type']='bytes'
            elif mode=='stage':mutated['stage']='deliberately-wrong-stage'
            elif mode=='trace':mutated['trace']=mutated['trace']+mutated['trace'][:1]
            negative_record={'mode':mode,'case_id':case['id'],'original_verified':True,'original':record['actual'],'mutated':mutated}
            exact(mutated,case['expected']);raise RuntimeError('Negative unexpectedly accepted')
        pending=[]
        for case in manifest['cases']:
            if case['kind'] in ('threads','event-loop'):pending.append(case)
            else:accept(case,invoke(case))
        for kind in ('threads','event-loop'):
            for eq in (0,1):
                selected=[c for c in pending if c['group']==f'{kind}/{eq}']
                if len(selected)!=2:raise RuntimeError('Concurrent scope count')
                if kind=='threads':
                    barrier=threading.Barrier(2)
                    def caller(c):barrier.wait(timeout=10);return invoke(c)
                    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                        records=list(pool.map(caller,selected))
                else:
                    async def caller(c):await asyncio.sleep(0);return invoke(c)
                    async def both():return await asyncio.gather(*(caller(c) for c in selected))
                    records=asyncio.run(both())
                for c,record in zip(selected,records):accept(c,record)
        exact([r['id'] for r in observations],[c['id'] for c in manifest['cases']])
    finally:
        nr._native_tuple_bytes=old_tuple
