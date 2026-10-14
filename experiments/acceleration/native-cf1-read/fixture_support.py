"""Public synthetic material only. No provider, database, or product mutation."""
import dataclasses
import hashlib
import os
import time
from pathlib import Path
from types import MappingProxyType
from uuid import UUID
from cryptalis.crypto import cf1
from cryptalis.crypto import keys as k

ROOT = Path(__file__).parent
S20 = ROOT.parent / 'candidate-s20-restored-20261014'

class TraceKeys(k.PreparedKeys):
    def _resolve(self, domain, tenant, purpose, generation):
        self.trace.append([str(domain), str(tenant), purpose, generation])
        if len(self.trace) == self.expire_at:
            material = self._materials.get((purpose, generation))
            if material is not None:
                self.mutable_materials[(purpose, generation)] = dataclasses.replace(material, expires=0)
        return super()._resolve(domain, tenant, purpose, generation)

class BytesSubclass(bytes):
    pass

def make_keys(spec, field, tenant, *, expire_at=0, wrong_payload=False, wrong_search=False,
              pid_wrong=False, missing=None, active_new=False, policy_tenant=None):
    mats = {}; wrappers = []
    for purpose in ('payload', 'search'):
        gen = spec[purpose + '_generation']
        if not gen:
            continue
        context = k.KeyContext(field.domain_id, tenant, purpose, UUID(spec[purpose+'_root_id']), gen)
        root = bytes.fromhex(spec[purpose+'_root'])
        if (purpose=='payload' and wrong_payload) or (purpose=='search' and wrong_search):
            root=bytes([root[0]^1])+root[1:]
        wrappers.append(k.WrappedRoot(UUID(int=91), context, b'public-fixture-placeholder'))
        if missing != purpose:
            mats[(purpose,gen)] = k._Material(context, root, time.monotonic()+240)
    pg,sg = spec['payload_generation'], spec['search_generation'] or None
    if active_new:
        for purpose, gen in [('payload', pg), ('search', sg)]:
            if gen is None: continue
            old=mats[(purpose,gen)]; ctx=dataclasses.replace(old.context,generation=gen+1,root_id=UUID(int=100+gen))
            wrappers.append(k.WrappedRoot(UUID(int=91),ctx,b'public-new-placeholder'))
            mats[(purpose,gen+1)]=k._Material(ctx,hashlib.sha256(old.root).digest(),old.expires)
        pg+=1
        if sg is not None: sg+=1
    policy=k.KeyPolicy(field.domain_id,tenant,tuple(wrappers),pg,sg)
    if policy_tenant is not None:
        policy=dataclasses.replace(policy,tenant_id=policy_tenant,
            wrappers=tuple(dataclasses.replace(w,context=dataclasses.replace(w.context,tenant_id=policy_tenant)) for w in wrappers))
    keys=TraceKeys(policy,MappingProxyType(mats),os.getpid()+1 if pid_wrong else os.getpid())
    object.__setattr__(keys,'trace',[]); object.__setattr__(keys,'expire_at',expire_at)
    object.__setattr__(keys,'mutable_materials',mats)
    for m in mats.values():
        if (m.context.domain_id,m.context.tenant_id)!=(field.domain_id,tenant):
            raise RuntimeError('Synthetic material scope mismatch')
    return keys

def fields(spec):
    f=cf1.FieldDescriptor.from_compiled(spec['descriptor'],spec['descriptor_digest'])
    t=UUID(spec['tenant_id'])
    r=UUID(spec['record_id']) if f.record_codec=='uuid16/v1' else spec['record_id']
    return f,t,r

def invocation(case, fixtures):
    spec=fixtures[case['fixture']]; field,tenant,record=fields(spec)
    changes=case.get('field',{})
    changes={key:(UUID(value) if key.endswith('_id') else bytes.fromhex(value) if key=='digest' else value) for key,value in changes.items()}
    if changes: field=dataclasses.replace(field,**changes)
    if 'tenant' in case: tenant=UUID(case['tenant'])
    if 'record' in case: record=UUID(case['record']) if field.record_codec=='uuid16/v1' else case['record']
    if 'record_kind' in case:
        record={'text':str(record),'int':3,'none':None,'bool':True,'low':-(2**63)-1,'high':2**63,'uuid':UUID(int=3)}[case['record_kind']]
    keyopts=case.get('keys',{})
    keyopts={name:(UUID(value) if name=='policy_tenant' else value) for name,value in keyopts.items()}
    keys=make_keys(spec,field,tenant,**keyopts)
    raw=(ROOT/spec['frame_path']).read_bytes()
    operation=case.get('frame_op')
    if operation=='flip':
        pos=case['index']; raw=raw[:pos]+bytes([raw[pos]^1])+raw[pos+1:]
    elif operation=='empty': raw=b''
    elif operation=='short': raw=bytes((74 if field.equality else 42)-1)
    elif operation=='truncate': raw=raw[:-1]
    elif operation=='append': raw+=b'x'
    elif operation=='over': raw=bytes(cf1.MAX_TEXT_BYTES+(74 if field.equality else 42)+1)
    elif operation=='suite': raw=raw[:4]+b'\x02'+raw[5:]
    elif operation=='flags': raw=raw[:5]+bytes([case['flag']])+raw[6:]
    elif operation=='zero_payload': raw=raw[:6]+bytes(4)+raw[10:]
    elif operation=='search_presence': raw=raw[:10]+(bytes(4) if field.equality else b'\0\0\0\1')+raw[14:]
    elif operation=='unadmitted_payload': raw=raw[:6]+(99).to_bytes(4,'big')+raw[10:]
    elif operation=='unadmitted_search': raw=raw[:10]+(99).to_bytes(4,'big')+raw[14:]
    kind=case.get('frame_kind')
    if kind=='null': raw=None
    elif kind=='text': raw=raw.hex()
    elif kind=='bytearray': raw=bytearray(raw)
    elif kind=='memoryview': raw=memoryview(raw)
    elif kind=='subclass': raw=BytesSubclass(raw)
    if case.get('bad_field'): field=object()
    if case.get('bad_keys'): keys=object()
    return raw,field,tenant,record,keys

def observe(fn,args):
    try:
        value=fn(*args)
    except k.CryptoFailure as exc:
        result={'exception':type(exc).__name__,'code':exc.code,'stage':exc.stage,
                'retryable':exc.retryable,'effects':exc.effects,'remedy':exc.remedy,
                'operation_present':bool(exc.operation_id)}
        if not exc.operation_id: raise RuntimeError('Missing operation identifier')
    else:
        if value is not None and type(value) is not str: raise RuntimeError('Non-text output')
        result={'value': None if value is None else {'bytes':len(value.encode('utf8')),
                 'sha256':hashlib.sha256(value.encode('utf8')).hexdigest()}}
    result['trace']=getattr(args[-1],'trace',[])
    return result
