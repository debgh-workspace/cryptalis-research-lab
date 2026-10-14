"""Explicit correctness validation. Invoke through launch.py pin enforcement."""
import asyncio
import concurrent.futures
import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from cryptalis.crypto import cf1
from cryptalis.crypto import keys as k
import fixture_support as s
import native_read as nr
import native_cf1

ROOT=Path(__file__).parent
manifest=json.loads((ROOT/'cases.json').read_text()); fixtures=manifest['fixtures']
passed=[]; planned=[]

def equal(label,actual,expected):
    if actual!=expected:
        raise RuntimeError('Mismatch: '+label)
    passed.append(label)

def refuse(label,fn,exception):
    try: fn()
    except exception: passed.append(label)
    else: raise RuntimeError('Missing refusal: '+label)

def native_args(case):
    frame,f,t,r,keys=s.invocation(case,fixtures)
    typed=cf1._context(f,t,r,keys)
    p=keys._resolve(f.domain_id,t,'payload',int.from_bytes(frame[6:10],'big'))
    search=keys._resolve(f.domain_id,t,'search',int.from_bytes(frame[10:14],'big')) if f.equality else None
    return (frame,int(f.equality),f.domain_id.bytes,t.bytes,f.field_id.bytes,f.digest,typed,nr._bundle(p),None if search is None else nr._bundle(search))

def run():
    if '--negative-output' in sys.argv: equal('negative-output','wrong','expected')
    original=nr._native_encoded
    if '--skip-final' in sys.argv:
        # Disposable separately named function, compiled from candidate source only.
        source=(ROOT/'native_read.py').read_text()
        tail="    keys._resolve(field.domain_id, tenant, 'payload', payload_generation)\n    if field.equality:\n        keys._resolve(field.domain_id, tenant, 'search', search_generation)\n    return value"
        if source.count(tail)!=1: raise RuntimeError('Mutation anchor changed')
        source=source.replace(tail,'    return value')
        namespace={};exec(compile(source,'<disposable-skip-final>','exec'),namespace)
        reader=namespace['open_text_native']
        selected=next(c for c in manifest['cases'] if c['id']=='expiry/100/3')
        equal('mutant-skip-final',s.observe(reader,s.invocation(selected,fixtures)),selected['expected'])
        return
    if '--skip-term' in sys.argv:
        selected=next(c for c in manifest['cases'] if c['id']=='valid-aead-wrong-term')
        equal('mutant-skip-term',s.observe(nr.open_text_native,s.invocation(selected,fixtures)),selected['expected'])
        return
    for c in manifest['cases']:
        equal(c['id'],s.observe(nr.open_text_native,s.invocation(c,fixtures)),c['expected'])
    # Two independent callers; isolation evidence only, GIL remains held.
    selected=[next(c for c in manifest['cases'] if c['id']==name) for name in ('grid/grid-000-1','grid/grid-100-1')]
    def work(c): return s.observe(nr.open_text_native,s.invocation(c,fixtures))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        for i,(actual,c) in enumerate(zip(pool.map(work,selected),selected)):
            equal('threads/'+str(i),actual,c['expected'])
    async def async_work(c):
        await asyncio.sleep(0)
        return work(c)
    async def both(): return await asyncio.gather(*(async_work(c) for c in selected))
    for i,(actual,c) in enumerate(zip(asyncio.run(both()),selected)):
        equal('event-loop/'+str(i),actual,c['expected'])
    for i,c in enumerate([selected[0],selected[1],selected[0]]): equal('interleave/'+str(i),work(c),c['expected'])
    bad=next(c for c in manifest['cases'] if c['id']=='keys/100/payload')
    for i,c in enumerate([selected[1],bad,selected[1]]): equal('valid-invalid-valid/'+str(i),work(c),c['expected'])
    # Actual isolated fork: inherited PreparedKeys must fail, then freshly
    # constructed child public material succeeds. No provider/DB is inherited.
    inherited=s.invocation(selected[1],fixtures)
    rfd,wfd=os.pipe();pid=os.fork()
    if pid==0:
        os.close(rfd)
        try:
            old=s.observe(nr.open_text_native,inherited)
            fresh=s.observe(nr.open_text_native,s.invocation(selected[1],fixtures))
            data=json.dumps({'inherited':old.get('exception'),'fresh':fresh}).encode()
            os.write(wfd,data);os.close(wfd);os._exit(0)
        except BaseException: os._exit(2)
    os.close(wfd)
    # Bounded parent readiness wait, kill on timeout, then reap.
    import select,signal
    ready,_,_=select.select([rfd],[],[],10)
    if not ready:
        os.kill(pid,signal.SIGKILL);os.waitpid(pid,0);os.close(rfd)
        raise RuntimeError('Fork control timed out')
    data=os.read(rfd,65536);os.close(rfd);_,status=os.waitpid(pid,0)
    equal('fork/exit',status,0);received=json.loads(data)
    equal('fork/inherited',received['inherited'],'KeyUnavailable')
    equal('fork/fresh',received['fresh'],selected[1]['expected'])
    # Expiry caused immediately after native return, before decoding.
    for c in selected:
        args=s.invocation(c,fixtures);ks=args[-1]
        def expire_return(*a):
            value=original(*a)
            for identity,m in list(ks.mutable_materials.items()):
                ks.mutable_materials[identity]=s.dataclasses.replace(m,expires=0)
            return value
        nr._native_encoded=expire_return
        try: actual=s.observe(nr.open_text_native,args)
        finally: nr._native_encoded=original
        equal('after-native/'+c['id'],actual.get('exception'),'KeyUnavailable')
    # Private ABI refuses all malformed exact-type and length forms before EVP.
    valid=native_args(selected[1])
    for pos in (0,2,3,4,5,6):
        for j,value in enumerate((None,bytearray(valid[pos]),s.BytesSubclass(valid[pos]))):
            args=list(valid);args[pos]=value
            refuse(f'abi/type/{pos}/{j}',lambda a=args:native_cf1.open_encoded(*a),(TypeError,ValueError))
    for pos in (2,3,4,5):
        for delta in (-1,1):
            args=list(valid);args[pos]=bytes(len(valid[pos])+delta)
            refuse(f'abi/length/{pos}/{delta}',lambda a=args:native_cf1.open_encoded(*a),ValueError)
    for bundlepos in (7,8):
        for pos in range(5):
            for j,value in enumerate((None,bytearray(valid[bundlepos][pos]),s.BytesSubclass(valid[bundlepos][pos]))):
                args=list(valid);bundle=list(args[bundlepos]);bundle[pos]=value;args[bundlepos]=tuple(bundle)
                refuse(f'abi/material-type/{bundlepos}/{pos}/{j}',lambda a=args:native_cf1.open_encoded(*a),ValueError)
            for delta in (-1,1):
                args=list(valid);bundle=list(args[bundlepos]);bundle[pos]=bytes(len(bundle[pos])+delta);args[bundlepos]=tuple(bundle)
                refuse(f'abi/material-length/{bundlepos}/{pos}/{delta}',lambda a=args:native_cf1.open_encoded(*a),ValueError)
        for label,value in [('missing',valid[bundlepos][:-1]),('extra',valid[bundlepos]+(b'',)),('none',None),('list',list(valid[bundlepos]))]:
            args=list(valid);args[bundlepos]=value
            refuse(f'abi/bundle/{bundlepos}/{label}',lambda a=args:native_cf1.open_encoded(*a),ValueError)
    for label,args in [('short',valid[:-1]),('long',valid+(None,))]:
        refuse('abi/arity/'+label,lambda a=args:native_cf1.open_encoded(*a),TypeError)
    for j,value in enumerate((b'',bytes(15),bytes(17),bytes(24),bytes(25),bytes(26))):
        args=list(valid);args[6]=value
        refuse('abi/record/'+str(j),lambda a=args:native_cf1.open_encoded(*a),ValueError)
    for j,value in enumerate((None,True,-1,2,2**100)):
        args=list(valid);args[1]=value
        refuse('abi/representation/'+str(j),lambda a=args:native_cf1.open_encoded(*a),(ValueError,OverflowError))
    for label,value in [('empty',b''),('over',bytes(cf1.MAX_TEXT_BYTES+75))]:
        args=list(valid);args[0]=value
        refuse('abi/frame/'+label,lambda a=args:native_cf1.open_encoded(*a),ValueError)
    storage=list(native_args(selected[0]));storage[-1]=valid[-1]
    refuse('abi/storage-extra-search',lambda:native_cf1.open_encoded(*storage),ValueError)
    # Unchanged product equality_term remains the independent query oracle.
    for name,spec in fixtures.items():
        if not name.startswith('grid-1'): continue
        f,t,r=s.fields(spec);ks=s.make_keys(spec,f,t);raw=(ROOT/spec['frame_path']).read_bytes()
        text=cf1.open_text(raw,f,t,r,ks)
        equal('query-term/'+name,cf1.equality_term(text,f,t,s.make_keys(spec,f,t)),raw[14:46])
    if hasattr(native_cf1,'open_fault'):
        sites=json.loads((ROOT/'fault-sites.json').read_text())
        valid=native_args(selected[1])
        for number,label in sites.items():
            number=int(number)
            expected='AuthenticationFailed' if number in (17,18) else 'CryptoBackendUnavailable'
            def inject(*args):
                # Only research module name is replaced, never product crypto.
                frame,f,t,typed,payload,search=args
                try:
                    return native_cf1.open_fault(frame,int(f.equality),f.domain_id.bytes,t.bytes,
                        f.field_id.bytes,f.digest,typed,nr._bundle(payload),nr._bundle(search),number)
                except RuntimeError as exc:
                    if exc.args==('data-processing',): raise k.AuthenticationFailed() from None
                    if exc.args==('term',): raise k.RepresentationMismatch() from None
                    raise k.CryptoBackendUnavailable() from None
            nr._native_encoded=inject
            try: actual=s.observe(nr.open_text_native,s.invocation(selected[1],fixtures))
            finally: nr._native_encoded=original
            equal('fault/'+label,actual.get('exception'),expected)
            equal('fault-recovery/'+label,work(selected[1]),selected[1]['expected'])
        # Injected result reservation beats bad-tag data processing, and a bad
        # tag beats a search-stage fault which is not reached.
        corrupted=copy.deepcopy(selected[1]);corrupted.update(frame_op='flip',index=74)
        args=native_args(corrupted)
        for number,category in [(13,'backend'),(21,'data-processing')]:
            try: native_cf1.open_fault(*args,number)
            except RuntimeError as exc: equal('fault-precedence/'+str(number),exc.args,(category,))
            else: raise RuntimeError('Fault precedence unexpectedly returned')
    planned=[c['id'] for c in manifest['cases']]
    planned += ['threads/'+str(i) for i in range(2)] + ['event-loop/'+str(i) for i in range(2)]
    planned += ['interleave/'+str(i) for i in range(3)] + ['valid-invalid-valid/'+str(i) for i in range(3)]
    planned += ['fork/exit','fork/inherited','fork/fresh']
    planned += ['after-native/grid/grid-000-1','after-native/grid/grid-100-1']
    planned += [f'abi/type/{p}/{j}' for p in (0,2,3,4,5,6) for j in range(3)]
    planned += [f'abi/length/{p}/{d}' for p in (2,3,4,5) for d in (-1,1)]
    for b in (7,8):
        for p in range(5):
            planned += [f'abi/material-type/{b}/{p}/{j}' for j in range(3)]
            planned += [f'abi/material-length/{b}/{p}/{d}' for d in (-1,1)]
        planned += [f'abi/bundle/{b}/{label}' for label in ('missing','extra','none','list')]
    planned += ['abi/arity/short','abi/arity/long']
    planned += ['abi/record/'+str(i) for i in range(6)] + ['abi/representation/'+str(i) for i in range(5)]
    planned += ['abi/frame/empty','abi/frame/over','abi/storage-extra-search']
    planned += ['query-term/'+name for name in fixtures if name.startswith('grid-1')]
    if hasattr(native_cf1,'open_fault'):
        for label in json.loads((ROOT/'fault-sites.json').read_text()).values():
            planned += ['fault/'+label,'fault-recovery/'+label]
        planned += ['fault-precedence/13','fault-precedence/21']
    if passed != planned or len(passed)!=len(set(passed)):
        raise RuntimeError('Missing, extra, duplicate, or reordered executed IDs')

if __name__=='__main__':
    run()
    print(json.dumps({'status':'PASS','passed':len(passed),'ids':passed}))
