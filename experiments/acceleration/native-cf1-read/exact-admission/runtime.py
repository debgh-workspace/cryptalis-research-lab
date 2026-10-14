"""Complete unchanged normal-wrapper admission; research-only observation hooks."""
import asyncio,concurrent.futures,copy,importlib.util,json,os,sys,threading
from pathlib import Path
from types import SimpleNamespace
import native_cf1 as native,native_read as nr,fixture_support as original
from cryptalis.crypto import cf1,keys
R=Path(__file__).absolute().parent; B=R.parent; C=B/'candidate-native-cf1-read-correction-20261014'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module;spec.loader.exec_module(module);return module
correction=load('admission_correction_support',C/'support.py')
# New isolated namespace, exact original bytes; never replace canonical cf1/os.
isolated=load('cryptalis.crypto._admission_baseline',B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py')
manifest=json.loads((R/'cases.json').read_text()); local=threading.local();groups={}
observations=[];negative_record=None

def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def exact(a,b):
    if not same(a,b):raise RuntimeError('Exact admission mismatch')

def routed(*args):
    local.calls+=1
    encoded=native.open_encoded(*args)
    case=local.case;prepared=local.prepared;kind=case.get('source_kind')
    if kind=='post-native-pid':object.__setattr__(prepared,'_pid',os.getpid()+1)
    if kind=='decode-expiry':
        class DecodeBoundary(bytes):
            def decode(self,encoding='utf-8',errors='strict'):
                if (encoding,errors)!=('utf8','strict'):raise RuntimeError('Decode contract changed')
                result=super().decode(encoding,errors)
                local.decoded=True;correction.expire(prepared,case['purpose']);return result
        return DecodeBoundary(encoded)
    return encoded

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
    result.update(trace=copy.deepcopy(getattr(prepared,'trace',[])),native_calls=local.calls)
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
    local.calls=0;local.decoded=False;local.case=case
    if case['kind']=='original':args=original.invocation(case,manifest['original_fixtures']);reader=nr.open_text_native
    elif case['kind'] in ('correction','threads','event-loop'):args=correction_args(case);reader=nr.open_text_native
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
    actual=observe(reader,args)
    if case.get('source_kind')=='decode-expiry' and not local.decoded:raise RuntimeError('Decode hook not reached')
    if case['kind']=='seal' and local.nonce_calls!=1:raise RuntimeError('Nonce stub count mismatch')
    return {'id':case['id'],'actual':actual,'decode_hook_completed':local.decoded,
            'synthetic_nonce_calls':local.nonce_calls if case['kind']=='seal' else 0}

def accept(case,record):
    exact(record['actual'],case['expected']);observations.append(record)

def run(mode):
    global negative_record
    old_module=nr.native_cf1;mapper=nr._native_encoded
    nr.native_cf1=SimpleNamespace(open_encoded=routed)
    try:
        if mode!='positive':
            control=next(n for n in manifest['negative_controls'] if n['mode']==mode)
            case=next(c for c in manifest['cases'] if c['id']==control['case_id'])
            record=invoke(case);exact(record['actual'],case['expected'])
            mutated=copy.deepcopy(record['actual'])
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
        nr.native_cf1=old_module
        if nr._native_encoded is not mapper:raise RuntimeError('Mapper changed')
