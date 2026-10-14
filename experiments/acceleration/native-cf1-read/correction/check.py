"""Execute only the finite new correction manifest; old suite is not called."""
import copy
import json
import os
from pathlib import Path
import support as s
import native_read as nr

ROOT=Path(__file__).parent
manifest=json.loads((ROOT/'cases.json').read_text())
passed=[];observations=[]

def exact(label,actual,expected):
    if actual!=expected:raise RuntimeError('Mismatch: '+label)

def invoke(case,prepared,*,negative=False):
    spec=manifest['fixtures'][case['fixture']];f,t,r=s.values(spec)
    raw=None if case.get('null_frame') else b'' if case.get('empty_frame') else s.frame(spec)
    original=nr._native_encoded;count=0;decoded=False
    class DecodeBoundary(bytes):
        def decode(self,encoding='utf-8',errors='strict'):
            nonlocal decoded
            if encoding!='utf8' or errors!='strict':raise RuntimeError('Unexpected decoding contract')
            value=super().decode(encoding,errors)
            decoded=True;s.expire(prepared,case['purpose'])
            return value
    def counted(*args):
        nonlocal count
        count+=1;value=original(*args)
        if case['kind']=='post-native-pid':object.__setattr__(prepared,'_pid',os.getpid()+1)
        if case['kind']=='decode-expiry':return DecodeBoundary(value)
        return value
    nr._native_encoded=counted
    try:
        actual=s.observe(nr.open_text_native,(raw,f,t,r,prepared))
    finally:nr._native_encoded=original
    exact(case['id']+'/native-calls',count,case['native_calls'])
    if case['kind']=='decode-expiry':exact(case['id']+'/decoded-before-expiry',decoded,True)
    if negative:
        # Validate actual fresh candidate output first; then corrupt that actual
        # output record at the downstream comparator, not a pair of literals.
        exact(case['id']+'/unmodified',actual,case['original_expected'])
        actual=copy.deepcopy(actual)
        if type(actual.get('value')) is not str:raise RuntimeError('Negative fixture did not produce text')
        actual['value']+='!CORRECTION-NEGATIVE!'
        observations.append({'id':case['id'],'native_calls':count,'original_verified':True,
            'perturbation_applied_to_actual_return':True,'comparison_expected':'reject'})
        exact(case['id'],actual,case['original_expected'])
        raise RuntimeError('Negative comparator accepted changed text')
    exact(case['id'],actual,case['expected'])
    observations.append({'id':case['id'],'actual':actual,'native_calls':count,
        'decode_hook_completed':decoded if case['kind']=='decode-expiry' else None})
    passed.append(case['id'])

def run(negative=False):
    if negative:
        case=dict(manifest['negative'],kind='negative')
        invoke(case,s.keys(manifest['fixtures'][case['fixture']]),negative=True)
        return
    groups={}
    for case in manifest['cases']:
        spec=manifest['fixtures'][case['fixture']]
        if case['kind']=='scope':
            identity=(case['group'],case['fixture'])
            if identity not in groups:groups[identity]=s.keys(spec)
            prepared=groups[identity]
        elif case['kind']=='lifecycle':
            identity=case['group']
            if case['state']=='valid':groups[identity]=s.keys(spec)
            if identity not in groups:raise RuntimeError('Lifecycle prerequisite missing')
            if case['state']=='expire':s.expire(groups[identity])
            if case['state']=='fresh':
                previous=groups[identity];groups[identity]=s.keys(spec)
                if previous is groups[identity]:raise RuntimeError('Fresh material not reconstructed')
            prepared=groups[identity]
        else:prepared=s.keys(spec,policy_domain=case.get('policy_domain'))
        invoke(case,prepared)
    expected=[c['id'] for c in manifest['cases']]
    if passed!=expected or len(set(passed))!=manifest['positive_count']:raise RuntimeError('Case identity mismatch')
