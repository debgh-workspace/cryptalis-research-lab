"""Freeze unchanged S20 oracle outcomes BEFORE native candidate execution."""
import copy
import hashlib
import json
import sys
from pathlib import Path
from uuid import UUID
ROOT=Path(__file__).parent
sys.path.insert(0,str(ROOT.parent/'candidate-s20-restored-20261014'/'src'))
import fixture_support as s
from cryptalis.crypto import cf1
from cryptalis.crypto.keys import tuple_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCMSIV

fixtures={}; cases=[]

def add_fixture(name,spec,frame):
    spec=copy.deepcopy(spec); spec.pop('frame',None)
    path=ROOT/'fixtures'/f'{name}.bin'
    with path.open('xb') as out: out.write(frame)
    spec['frame_path']=str(path.relative_to(ROOT)); spec['frame_sha256']=hashlib.sha256(frame).hexdigest()
    fixtures[name]=spec

def case(name,fixture,**kwargs):
    cases.append({'id':name,'fixture':fixture,**kwargs})

def descriptor(eq,big,single):
    d={'schema':'cryptalis.context/v1','domain_id':str(UUID(int=1)),'table_id':str(UUID(int=2)),
       'field_id':str(UUID(int=3)),'text_codec':'utf8-exact/v1','normalizer':'identity/v1',
       'null_policy':'sql-null/v1','record_codec':'int64-be/v1' if big else 'uuid16/v1',
       'tenant_codec':'single-tenant-uuid/v1' if single else 'uuid16/v1',
       'representation':'cf1-packed-equality/v1' if eq else 'cf1-storage/v1'}
    digest=hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'descriptor':d,'descriptor_digest':digest,'tenant_id':str(UUID(int=2 if single else 4)),
        'record_id':5 if big else str(UUID(int=5)),'payload_generation':7,'search_generation':9 if eq else 0,
        'payload_root_id':str(UUID(int=6)),'search_root_id':str(UUID(int=7)),
        'payload_root':bytes(range(32)).hex(),'search_root':bytes(range(32,64)).hex()}

def seal_raw(spec,encoded,wrong_term=False):
    f,t,r=s.fields(spec); keys=s.make_keys(spec,f,t); typed=f._record(t,r)
    payload=keys._materials[('payload',spec['payload_generation'])]
    term=b''
    if f.equality:
        term=cf1._term(encoded,f,keys._materials[('search',spec['search_generation'])])
        if wrong_term: term=bytes([term[0]^1])+term[1:]
    header=cf1._MAGIC+bytes([int(f.equality)])+spec['payload_generation'].to_bytes(4,'big')+spec['search_generation'].to_bytes(4,'big')+term
    key=cf1._derive(payload,tuple_bytes(b'CF1/payload-key',f.field_id.bytes,typed))
    nonce=bytes(range(12))
    return header+nonce+AESGCMSIV(key).encrypt(nonce,encoded,cf1._aad(f,t,typed,header))

(ROOT/'fixtures').mkdir()
vectors=json.loads((s.S20/'tests/fixtures/cf1_vectors.json').read_text())['vectors']
for v in vectors:
    name=v['name']; raw=bytes.fromhex(v['frame']); add_fixture(name,v,raw)
    case('frozen/'+name,name)
    for i in range(len(raw)): case(f'flip/{name}/{i}',name,frame_op='flip',index=i)
    for op in ('empty','short','truncate','append','suite','zero_payload','search_presence','unadmitted_payload'):
        case(f'frame/{name}/{op}',name,frame_op=op)
    for flag in (2,4,255): case(f'frame/{name}/flag{flag}',name,frame_op='flags',flag=flag)

texts=['','abcdefg','x'*32,'x'*128,'x'*4096,'café','cafe\u0301','雪😀\n']
for eq in (False,True):
 for big in (False,True):
  for single in (False,True):
    stem=f'{int(eq)}{int(big)}{int(single)}'; spec=descriptor(eq,big,single)
    for i,value in enumerate(texts):
        name=f'grid-{stem}-{i}'; f,t,r=s.fields(spec); keys=s.make_keys(spec,f,t)
        # Unchanged product sealing supplies independent fixtures; no nonce patch.
        raw=cf1.seal_text(value,f,t,r,keys)
        if cf1.open_text(raw,f,t,r,s.make_keys(spec,f,t))!=value: raise RuntimeError('Oracle sealing mismatch')
        add_fixture(name,spec,raw); case('grid/'+name,name)
    base=f'grid-{stem}-1'
    case('null/'+stem,base,frame_kind='null')
    for kind in ('text','bytearray','memoryview','subclass'): case(f'type/{stem}/{kind}',base,frame_kind=kind)
    for kind in (('bool','low','high','uuid') if big else ('text','int','none')): case(f'record/{stem}/{kind}',base,record_kind=kind)
    case('type/'+stem+'/field',base,bad_field=True);case('type/'+stem+'/keys',base,bad_keys=True)
    case('context/'+stem+'/field',base,field={'field_id':str(UUID(int=101))})
    case('context/'+stem+'/digest',base,field={'digest':bytes(32).hex()})
    case('context/'+stem+'/domain',base,field={'domain_id':str(UUID(int=102))})
    case('context/'+stem+'/record',base,record=123 if big else str(UUID(int=123)))
    case('context/'+stem+'/tenant',base,tenant=str(UUID(int=124)))
    case('context/'+stem+'/policy-tenant',base,keys={'policy_tenant':str(UUID(int=124))})
    case('keys/'+stem+'/payload',base,keys={'wrong_payload':True})
    case('keys/'+stem+'/missing-payload',base,keys={'missing':'payload'})
    case('keys/'+stem+'/older-admitted',base,keys={'active_new':True})
    case('keys/'+stem+'/pid',base,keys={'pid_wrong':True})
    for at in range(1,5 if eq else 3): case(f'expiry/{stem}/{at}',base,keys={'expire_at':at})
    case('null-expiry/'+stem,base,frame_kind='null',keys={'expire_at':1})
    if eq:
        case('keys/'+stem+'/search',base,keys={'wrong_search':True})
        case('keys/'+stem+'/missing-search',base,keys={'missing':'search'})
        case('frame/'+stem+'/unadmitted-search',base,frame_op='unadmitted_search')
    case('precedence/'+stem+'/context-before-frame',base,record_kind='bool' if big else 'none',frame_op='empty')
    case('precedence/'+stem+'/policy-before-frame',base,keys={'policy_tenant':str(UUID(int=124))},frame_op='empty')
    case('precedence/'+stem+'/frame-before-expiry',base,frame_op='empty',keys={'expire_at':1})
    case('precedence/'+stem+'/admission-before-tag',base,frame_op='flip',index=-1 if False else 45,keys={'missing':'payload'})
    if eq: case('precedence/'+stem+'/tag-before-search',base,frame_op='flip',index=74,keys={'wrong_search':True})
for eq in (False,True):
    for number in (-(2**63),0,2**63-1):
        name=f'endpoint-{int(eq)}-{number}';spec=descriptor(eq,True,False);spec['record_id']=number
        add_fixture(name,spec,seal_raw(spec,b'endpoint'));case(name,name)
    name=f'nil-{int(eq)}';spec=descriptor(eq,False,False);spec['record_id']=str(UUID(int=0));spec['tenant_id']=str(UUID(int=0))
    add_fixture(name,spec,seal_raw(spec,b'nil'));case(name,name)
    spec=descriptor(eq,False,False);name=f'max-{int(eq)}'
    add_fixture(name,spec,seal_raw(spec,b'x'*cf1.MAX_TEXT_BYTES));case(name,name);case('over/'+name,name,frame_op='over')
    for label,encoded in [('utf8',b'\xff'),('nul',b'x\0y')]:
        name=f'content-{int(eq)}-{label}'
        add_fixture(name,spec,seal_raw(spec,encoded));case(name,name)
        case('precedence/text-before-expiry/'+name,name,keys={'expire_at':3 if eq else 2})
        if eq:
            name+='-wrong-term';add_fixture(name,spec,seal_raw(spec,encoded,True));case(name,name)
    if eq:
        name='valid-aead-wrong-term';add_fixture(name,spec,seal_raw(spec,b'abcdefg',True));case(name,name)
# Shape-valid opposite representation of adequate size.
case('shape/storage-frame-for-equality','grid-000-4',field={'representation':'cf1-packed-equality/v1'})
case('shape/equality-frame-for-storage','grid-100-4',field={'representation':'cf1-storage/v1'})
ids=[c['id'] for c in cases]
if len(ids)!=len(set(ids)): raise RuntimeError('Duplicate case IDs')
for c in cases:
    c['expected']=s.observe(cf1.open_text,s.invocation(c,fixtures))
manifest={'scope':'Public fixtures; baseline outcomes frozen before native import','fixtures':fixtures,'cases':cases}
with (ROOT/'cases.json').open('x') as out: json.dump(manifest,out,indent=2);out.write('\n')
print(json.dumps({'cases':len(cases),'fixtures':len(fixtures),'status':'FROZEN'}))
