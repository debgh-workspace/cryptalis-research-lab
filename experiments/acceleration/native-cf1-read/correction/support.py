"""Public fixture setup and exact-observation helpers; no candidate imports."""
import copy
import dataclasses
import hashlib
import json
import os
import time
from pathlib import Path
from types import MappingProxyType
from uuid import UUID
from cryptalis.crypto import cf1
from cryptalis.crypto import keys as k

ROOT=Path(__file__).parent
ORIGINAL=ROOT.parent/'candidate-native-cf1-read-20261014'

class TracedKeys(k.PreparedKeys):
    def _resolve(self,domain,tenant,purpose,generation):
        self.trace.append([str(domain),str(tenant),purpose,generation])
        return super()._resolve(domain,tenant,purpose,generation)

def descriptor(spec):
    d=spec['descriptor']
    digest=hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if spec.get('descriptor_digest')!=digest:raise RuntimeError('Frozen descriptor digest mismatch')
    return cf1.FieldDescriptor.from_compiled(d,digest)

def values(spec):
    f=descriptor(spec);t=UUID(spec['tenant_id'])
    r=UUID(spec['record_id']) if f.record_codec=='uuid16/v1' else spec['record_id']
    return f,t,r

def keys(spec, *, policy_domain=None):
    f,t,_=values(spec);domain=f.domain_id if policy_domain is None else UUID(policy_domain)
    wrappers=[];materials={}
    for purpose in ('payload','search'):
        generation=spec[purpose+'_generation']
        if not generation:continue
        c=k.KeyContext(domain,t,purpose,UUID(spec[purpose+'_root_id']),generation)
        wrappers.append(k.WrappedRoot(UUID(int=91),c,b'public-correction-placeholder'))
        materials[(purpose,generation)]=k._Material(c,bytes.fromhex(spec[purpose+'_root']),time.monotonic()+240)
    policy=k.KeyPolicy(domain,t,tuple(wrappers),spec['payload_generation'],spec['search_generation'] or None)
    result=TracedKeys(policy,MappingProxyType(materials),os.getpid())
    object.__setattr__(result,'trace',[]);object.__setattr__(result,'mutable_materials',materials)
    return result

def expire(prepared,purpose=None):
    for identity,m in list(prepared.mutable_materials.items()):
        if purpose is None or identity[0]==purpose:
            prepared.mutable_materials[identity]=dataclasses.replace(m,expires=0)

def frame(spec):
    base=ORIGINAL if spec['frame_origin']=='original' else ROOT
    raw=(base/spec['frame_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=spec['frame_sha256']:raise RuntimeError('Fixture mismatch')
    return raw

def error_record(cls):
    exc=cls()
    return {'exception':cls.__name__,'code':exc.code,'stage':exc.stage,'retryable':exc.retryable,
            'effects':exc.effects,'remedy':exc.remedy,'operation_present':bool(exc.operation_id)}

def observe(reader,args):
    prepared=args[-1];prepared.trace.clear()
    try:value=reader(*args)
    except k.CryptoFailure as exc:
        result={'exception':type(exc).__name__,'code':exc.code,'stage':exc.stage,'retryable':exc.retryable,
                'effects':exc.effects,'remedy':exc.remedy,'operation_present':bool(exc.operation_id)}
        if not exc.operation_id:raise RuntimeError('Missing operation ID')
    else:
        if value is not None and type(value) is not str:raise RuntimeError('Wrong native result type')
        result={'value':value,'value_type':'NoneType' if value is None else 'str'}
    result['trace']=copy.deepcopy(prepared.trace)
    return result

def trace(spec,purposes):
    f,t,_=values(spec)
    return [[str(f.domain_id),str(t),p,spec[p+'_generation']] for p in purposes]

def expected_success(spec,value):
    f,_,_=values(spec)
    purposes=['payload'] if value is None else (['payload','search','payload','search'] if f.equality else ['payload','payload'])
    return {'value':value,'value_type':'NoneType' if value is None else 'str','trace':trace(spec,purposes)}

def expected_failure(spec,cls,purposes):
    result=error_record(cls);result['trace']=trace(spec,purposes);return result
