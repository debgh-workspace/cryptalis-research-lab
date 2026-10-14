"""Research-only return expiry and CPython decode observation. Native bytes unchanged."""
import copy, importlib.util, json, sys
from pathlib import Path
from types import SimpleNamespace
import native_cf1 as native, native_read as nr
from cryptalis.crypto import keys
R=Path(__file__).absolute().parent; B=R.parent
spec=importlib.util.spec_from_file_location('return_expiry_support',B/'candidate-native-cf1-read-correction-20261014/support.py')
support=importlib.util.module_from_spec(spec);spec.loader.exec_module(support)
manifest=json.loads((R/'cases.json').read_text())
observations=[]; negative_record=None

def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def exact(a,b):
    if not same(a,b):raise RuntimeError('Exact return-expiry mismatch')

def invoke(case):
    spec=manifest['fixtures'][case['fixture']]; f,t,r=support.values(spec); prepared=support.keys(spec)
    raw=support.frame(spec); purpose=case['purpose']; identity=(purpose,spec[purpose+'_generation'])
    events=[]; native_calls=0; native_return=None; encoded_object=None
    old_native=nr.native_cf1; old_mapper=nr._native_encoded; old_profile=sys.getprofile()
    if old_profile is not None:raise RuntimeError('Unexpected existing profiler')
    def trace():return copy.deepcopy(prepared.trace)
    def expired():return prepared.mutable_materials[identity].expires==0
    def routed(*args):
        nonlocal native_calls,native_return,encoded_object
        native_calls+=1
        encoded=native.open_encoded(*args)
        # This is the actual successful normal native result, not a fabricated result.
        if type(encoded) is not bytes:raise RuntimeError('Native result type')
        encoded_object=encoded
        native_return={'type':type(encoded).__name__,'hex':encoded.hex()}
        events.append({'event':'native-return','trace':trace()})
        support.expire(prepared,purpose)
        events.append({'event':'expire','purpose':purpose,'generation':identity[1],'expired':expired(),'trace':trace()})
        return encoded  # Exact object, no decode override or replacement.
    def profile(frame,event,arg):
        if event in ('c_call','c_return','c_exception') and getattr(arg,'__name__',None)=='decode' and getattr(arg,'__self__',None) is encoded_object:
            events.append({'event':{'c_call':'decode-call','c_return':'decode-return','c_exception':'decode-error'}[event],
                           'expired':expired(),'trace':trace()})
    nr.native_cf1=SimpleNamespace(open_encoded=routed)
    try:
        sys.setprofile(profile)
        try:value=nr.open_text_native(raw,f,t,r,prepared)
        except keys.CryptoFailure as exc:
            actual={name:getattr(exc,name) for name in ('code','stage','retryable','effects','remedy')}
            safe=(f'{exc.code} during {exc.stage}. {exc.remedy} Operation {exc.operation_id}.',)
            actual.update(exception=type(exc).__name__,operation_present=type(exc.operation_id) is str and bool(exc.operation_id),
                          args_safe=exc.args==safe,cause_none=exc.__cause__ is None,
                          cause_suppressed=exc.__suppress_context__,value_published=False)
        else:actual={'value':value,'value_type':type(value).__name__,'value_published':True}
    finally:
        sys.setprofile(old_profile);nr.native_cf1=old_native
        if nr._native_encoded is not old_mapper:raise RuntimeError('Mapper changed')
    actual.update(trace=trace(),native_calls=native_calls,native_return=native_return,events=events)
    return {'id':case['id'],'actual':actual}

def run(mode):
    global negative_record
    ids=[c['id'] for c in manifest['cases']]
    exact(ids,['after-native-return/storage/payload','after-native-return/equality/search'])
    if mode!='positive':
        control=next(n for n in manifest['negative_controls'] if n['mode']==mode)
        case=next(c for c in manifest['cases'] if c['id']==control['case_id'])
        record=invoke(case);exact(record['actual'],case['expected'])
        changed=copy.deepcopy(record['actual'])
        if mode=='metadata':changed['stage']='deliberately-wrong-stage'
        elif mode=='trace':changed['trace']=changed['trace']+changed['trace'][:1]
        else:raise RuntimeError('Unknown negative')
        negative_record={'mode':mode,'case_id':case['id'],'original_verified':True,'original':record['actual'],'mutated':changed}
        exact(changed,case['expected']);raise RuntimeError('Negative unexpectedly accepted')
    for case in manifest['cases']:
        record=invoke(case);observations.append(record);exact(record['actual'],case['expected'])
    exact([r['id'] for r in observations],ids)
