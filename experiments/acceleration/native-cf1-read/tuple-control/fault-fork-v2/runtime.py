"""Finite P:T fault/expiry/fork comparison. Public fixtures only; untimed."""
import copy
import dataclasses
import importlib.util
import json
import os
from pathlib import Path
import selectors
import signal
import sys
import time
from uuid import UUID
import native_tuple
import tuple_read
import fixture_support
from cryptalis.crypto import cf1,keys
R=Path(__file__).parent;T=R.parent;B=T.parent
manifest=json.loads((R/'MANIFEST.json').read_text())
fixtures=json.loads((B/'candidate-native-cf1-read-20261014/cases.json').read_text())['fixtures']
spec=importlib.util.spec_from_file_location('cryptalis.crypto._tuple_fault_baseline',B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py')
pbaseline=importlib.util.module_from_spec(spec);sys.modules[spec.name]=pbaseline;spec.loader.exec_module(pbaseline)
observations=[];fork_receipts=[];fork_attempts=[];negative_record=None
original_p_tuple=pbaseline.tuple_bytes
child_check=None
TAGS=(b'CF1/payload-key',b'CF1/root',b'CF1/payload',b'CF1/search-key',b'CF1/root',b'equality')

def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b

def exact(a,b):
    if not same(a,b):raise RuntimeError('Supplement mismatch')

def prepare(arm,fixture):
    s=fixtures[fixture]
    mod=pbaseline if arm=='P' else cf1
    f=mod.FieldDescriptor.from_compiled(s['descriptor'],s['descriptor_digest'])
    tenant=UUID(s['tenant_id']);record=UUID(s['record_id'])
    prepared=fixture_support.make_keys(s,f,tenant)
    raw=(B/'candidate-native-cf1-read-20261014'/s['frame_path']).read_bytes()
    return raw,f,tenant,record,prepared

def observe(case,args):
    arm=case['arm'];mod=pbaseline if arm=='P' else tuple_read
    binding='tuple_bytes' if arm=='P' else '_native_tuple_bytes'
    saved=getattr(mod,binding);prepared=args[-1];prepared.trace.clear()
    entries=completed=fault_fired=expiry_fired=0
    def route(*parts):
        nonlocal entries,completed,fault_fired,expiry_fired
        entries+=1
        if not 1<=entries<=6 or not parts or parts[0]!=TAGS[entries-1]:raise RuntimeError('Tuple route mismatch')
        if entries==case.get('fault_at'):
            fault_fired+=1
            if arm=='P':raise MemoryError()
            return native_tuple.tuple_alloc_failure(*parts)
        result=saved(*parts)
        if type(result) is not bytes:raise RuntimeError('Non-exact tuple bytes')
        completed+=1
        if entries==case.get('expire_after'):
            expiry_fired+=1
            purpose=case['expire_purpose']
            for identity,material in list(prepared.mutable_materials.items()):
                if identity[0]==purpose:prepared.mutable_materials[identity]=dataclasses.replace(material,expires=0)
        return result
    setattr(mod,binding,route)
    try:
        try:value=mod.open_text(*args)
        except keys.CryptoFailure as exc:
            result={name:getattr(exc,name) for name in ('code','stage','retryable','effects','remedy')}
            safe=(f'{exc.code} during {exc.stage}. {exc.remedy} Operation {exc.operation_id}.',)
            result.update(exception=type(exc).__name__,operation_present=type(exc.operation_id) is str and bool(exc.operation_id),args_safe=exc.args==safe,cause_none=exc.__cause__ is None,published=False)
        except MemoryError as exc:
            result={'exception':'MemoryError','args':list(exc.args),'cause_none':exc.__cause__ is None,'published':False}
        else:
            result={'value':value,'value_type':type(value).__name__,'published':True}
    finally:
        setattr(mod,binding,saved)
    result.update(trace=copy.deepcopy(prepared.trace),tuple_entries=entries,tuple_completed=completed,fault_fired=fault_fired,expiry_fired=expiry_fired)
    return {'id':case['id'],'actual':result}

def accept(case,record):
    exact(record['actual'],case['expected']);observations.append(record)

def fork_group(group):
    cases=[c for c in manifest['cases'] if c.get('fork_group')==group]
    before,inherited,fresh,after=cases
    args=prepare(before['arm'],before['fixture'])
    first=observe(before,args);exact(first['actual'],before['expected'])
    parent_pid=os.getpid();read_fd,write_fd=os.pipe()
    try:pid=os.fork()
    except BaseException:
        os.close(read_fd);os.close(write_fd);raise
    if pid==0:
        os.close(read_fd)
        try:
            if child_check is None:raise RuntimeError('Child guard unavailable')
            before_guard=child_check()
            result={'child_pid':os.getpid(),'observed_parent_pid':os.getppid(),
                'records':[observe(inherited,args),observe(fresh,prepare(fresh['arm'],fresh['fixture']))],
                'guard_before':before_guard,'guard_after':child_check()}
            raw=json.dumps(result).encode('utf8')
            if len(raw)>65536:raise RuntimeError('IPC oversized')
            while raw:
                n=os.write(write_fd,raw)
                if n<=0:raise RuntimeError('IPC write failure')
                raw=raw[n:]
            os.close(write_fd);os._exit(0)
        except BaseException:
            try:os.close(write_fd)
            finally:os._exit(97)
    os.close(write_fd);deadline=time.monotonic()+10;chunks=[];size=0;reaped=False
    attempt={'group':group,'parent_pid':parent_pid,'child_pid':pid,'deadline_seconds':10,'cleanup_reap_seconds':2,'status':'RUNNING','reaped':False}
    fork_attempts.append(attempt)
    selector=None
    try:
        selector=selectors.DefaultSelector();selector.register(read_fd,selectors.EVENT_READ)
        while True:
            left=deadline-time.monotonic()
            if left<=0:raise RuntimeError('Fork child timeout')
            if not selector.select(left):raise RuntimeError('Fork IPC timeout')
            block=os.read(read_fd,4096)
            if not block:break
            size+=len(block)
            if size>65536:raise RuntimeError('IPC oversized')
            chunks.append(block)
        while True:
            ended,status=os.waitpid(pid,os.WNOHANG)
            if ended:
                reaped=True
                if not os.WIFEXITED(status) or os.WEXITSTATUS(status)!=0:raise RuntimeError('Fork child failed')
                break
            if time.monotonic()>=deadline:raise RuntimeError('Fork reap timeout')
            time.sleep(0.01)
        child=json.loads(b''.join(chunks))
        if child['child_pid']!=pid or child['child_pid']==parent_pid or child['observed_parent_pid']!=parent_pid:raise RuntimeError('Fork PID mismatch')
        if len(child['records'])!=2:raise RuntimeError('Fork record count')
        exact(child['guard_before'],{'source_cache':'PASS','bindings':'PASS'})
        exact(child['guard_after'],{'source_cache':'PASS','bindings':'PASS'})
        last=observe(after,args)
        records=[first,*child['records'],last]
        for case,record in zip(cases,records):
            exact(record['id'],case['id']);exact(record['actual'],case['expected'])
        attempt.update(status='PASS',reaped=True)
        return records,{'group':group,'parent_pid':parent_pid,'fork_return_pid':pid,'child_pid':child['child_pid'],'observed_parent_pid':child['observed_parent_pid'],'exit_code':0,'reaped':True,'ipc_bytes':size,'guard_before':child['guard_before'],'guard_after':child['guard_after']}
    except BaseException as exc:
        attempt.update(status='FAIL',error_type=type(exc).__name__,error=str(exc),reaped=reaped)
        raise
    finally:
        if selector is not None:selector.close()
        os.close(read_fd)
        if not reaped:
            try:os.kill(pid,signal.SIGKILL)
            except ProcessLookupError:pass
            reap_deadline=time.monotonic()+2
            while True:
                ended,_=os.waitpid(pid,os.WNOHANG)
                if ended:
                    attempt['reaped']=True;break
                if time.monotonic()>=reap_deadline:
                    attempt.update(status='FAIL',terminal_state='UNKNOWN',reaped=False)
                    raise RuntimeError('Fork cleanup reaping unconfirmed')
                time.sleep(0.01)

def run(mode):
    global negative_record
    if mode!='positive':
        control=next(c for c in manifest['negatives'] if c['mode']==mode)
        if mode=='fork-pid':
            records,receipt=fork_group(control['group']);mutated=copy.deepcopy(receipt);mutated['child_pid']=mutated['parent_pid']
            negative_record={'mode':mode,'original_verified':True,'original':receipt,'mutated':mutated}
            if mutated['child_pid']!=mutated['fork_return_pid'] or mutated['child_pid']==mutated['parent_pid']:raise RuntimeError('Supplement mismatch')
        else:
            case=next(c for c in manifest['cases'] if c['id']==control['case_id'])
            record=observe(case,prepare(case['arm'],case['fixture']));exact(record['actual'],case['expected'])
            mutated=copy.deepcopy(record['actual'])
            if mode=='raw-boundary':mutated['exception']='CryptoBackendUnavailable'
            elif mode=='count':mutated['tuple_entries']+=1
            elif mode=='trace':mutated['trace']+=mutated['trace'][:1]
            negative_record={'mode':mode,'case_id':case['id'],'original_verified':True,'original':record['actual'],'mutated':mutated}
            exact(mutated,case['expected'])
        raise RuntimeError('Negative unexpectedly accepted')
    for case in manifest['cases']:
        if 'fork_group' not in case:accept(case,observe(case,prepare(case['arm'],case['fixture'])))
    for group in manifest['fork_groups']:
        records,receipt=fork_group(group)
        for record in records:
            case=next(c for c in manifest['cases'] if c['id']==record['id']);accept(case,record)
        fork_receipts.append(receipt)
    exact([r['id'] for r in observations],[c['id'] for c in manifest['cases']])
    byid={r['id']:r['actual'] for r in observations}
    for pair in manifest['parity_pairs']:exact(byid[pair[0]],byid[pair[1]])
