"""Exercise unchanged mapper by routing only its private native module call."""
import ast,copy,hashlib,json,sys,sysconfig
from pathlib import Path
from types import SimpleNamespace
R=Path(__file__).resolve().parent; B=R.parent; O=B/'candidate-native-cf1-read-20261014'
mode=sys.argv[1]; dest=R/sys.argv[2]
if mode not in ('positive','release','transfer') or dest.exists():raise RuntimeError('Invalid launch')
receipt={'status':'FAIL','mode':mode,'optimize':sys.flags.optimize,'observations':[]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def equal(actual,expected):
    if type(actual) is not type(expected):raise RuntimeError('Exact resource mismatch')
    if isinstance(actual,dict):
        if actual.keys()!=expected.keys():raise RuntimeError('Exact resource mismatch')
        for key in actual:equal(actual[key],expected[key])
    elif isinstance(actual,list):
        if len(actual)!=len(expected):raise RuntimeError('Exact resource mismatch')
        for a,e in zip(actual,expected):equal(a,e)
    elif actual!=expected:raise RuntimeError('Exact resource mismatch')
try:
    pins=json.loads((R/'PINS.json').read_text())['pins']
    for n,h in pins.items():
        if sha(Path(n))!=h:raise RuntimeError('Pin mismatch: '+n)
    receipt.update(pins_sha256=sha(R/'PINS.json'),verified_pins=len(pins),cases_sha256=sha(R/'cases.json'))
    for p in R.glob('*.py'):
        if any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))):raise RuntimeError('Assert check')
    if sys.executable!=str(B/'repo/.venv/bin/python') or sys.version_info[:3]!=(3,12,14) or sysconfig.get_config_var('SOABI')!='cpython-312-x86_64-linux-gnu':raise RuntimeError('Wrong interpreter')
    sys.path[:0]=[str(R/'build'),str(O),str(B/'candidate-s20-restored-20261014/src')]
    import native_cf1 as native, native_read as nr, fixture_support as support, cryptography
    from cryptography.hazmat.backends.openssl.backend import backend
    from cryptalis.crypto import keys,cf1
    build=json.loads((R/'build/build.json').read_text())
    if native.__file__!=build['binary'] or native.backend_version()!='OpenSSL 3.5.7 9 Jun 2026':raise RuntimeError('Native origin/backend')
    if cryptography.__file__!=build['cryptography_origin'] or cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Oracle origin/backend')
    for module,path in [(nr,O/'native_read.py'),(support,O/'fixture_support.py'),(cf1,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py'),(keys,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/keys.py')]:
        if Path(module.__file__)!=path:raise RuntimeError('Source origin')
    receipt.update(native_origin=native.__file__,native_backend=native.backend_version(),python=sys.version,python_executable=sys.executable)
    manifest=json.loads((R/'cases.json').read_text()); cache={}; captured={}
    for case in manifest['cases']:
        spec=manifest['fixtures'][case['fixture']]; f,t,r=support.fields(spec)
        group=case['group']
        if group not in cache:cache[group]=support.make_keys(spec,f,t)
        prepared=cache[group];prepared.trace.clear()
        frame=(O/spec['frame_path']).read_bytes()
        if sha(O/spec['frame_path'])!=spec['frame_sha256']:raise RuntimeError('Fixture changed')
        if case['bad_tag']:frame=frame[:-1]+bytes([frame[-1]^1])
        calls=[]
        def routed(*args):
            calls.append({'entry':'open_encoded','selector':case['selector']})
            if 'value' in case['expected']:captured[int(f.equality)]=args
            if case['selector']:return native.open_fault(*args,case['selector'])
            return native.open_encoded(*args)
        original_module=nr.native_cf1; original_mapper=nr._native_encoded
        nr.native_cf1=SimpleNamespace(open_encoded=routed)
        try:
            try:value=nr.open_text_native(frame,f,t,r,prepared)
            except keys.CryptoFailure as exc:
                observed={key:getattr(exc,key) for key in ('code','stage','retryable','effects','remedy')}
                observed.update(exception=type(exc).__name__,operation_present=isinstance(exc.operation_id,str) and bool(exc.operation_id),cause_suppressed=exc.__cause__ is None and exc.__suppress_context__)
                # Public message must be the canonical safe template, no native diagnostics.
                equal(exc.args,(f'{exc.code} during {exc.stage}. {exc.remedy} Operation {exc.operation_id}.',))
            else:observed={'value':value,'value_type':type(value).__name__}
        finally:nr.native_cf1=original_module
        if nr._native_encoded is not original_mapper:raise RuntimeError('Mapper replaced')
        observed.update(trace=copy.deepcopy(prepared.trace),native_calls=len(calls))
        equal(observed,case['expected'])
        balance=json.loads(json.dumps(native.balance_snapshot()))
        equal(balance,case['balance_expected'])
        record={'balance':balance,'id':case['id'],'actual':observed,'native_entry_trace':calls,'same_prepared_group':group}
        if mode!='positive' and 'value' in observed:
            original=copy.deepcopy(balance)
            if mode=='release':balance[0][0][1]-=1
            else:balance[0][9][2]=0
            record.update(original_balance=original,original_verified=True,perturbed_field=mode)
            receipt['observations'].append(record)
            equal(balance,case['balance_expected'])
            raise RuntimeError('Negative unexpectedly accepted')
        receipt['observations'].append(record)
    for case in manifest['direct_cases']:
        rep=case['rep'];args=captured[rep]
        # Last wrapper fixture is same-scope public abcdefg recovery.
        call=native.open_encoded; invocation=args
        if case['phase']=='refusal':
            if case['mutation']=='arity':invocation=args[:-1]
            elif case['mutation']=='selector':call=native.open_fault;invocation=(*args,36)
            else:invocation=(b'',*args[1:])
        try:value=call(*invocation)
        except Exception as exc:observed={'exception':type(exc).__name__}
        else:observed={'value_type':type(value).__name__,'value_hex':value.hex()}
        expected={'exception':case['expected_exception']} if case['expected_exception'] else {'value_type':'bytes','value_hex':b'abcdefg'.hex()}
        equal(observed,expected)
        balance=json.loads(json.dumps(native.balance_snapshot()))
        if case['phase']=='refusal':expected_balance=[[[0,0,0,0,0] for _ in range(10)],0,0]
        else:
            reference=next(c for c in manifest['cases'] if int(bool(manifest['fixtures'][c['fixture']]['search_generation']))==rep and 'value' in c['expected'])
            expected_balance=reference['balance_expected']
        equal(balance,expected_balance)
        receipt['observations'].append({'id':case['id'],'actual':observed,'balance':balance})
    equal([x['id'] for x in receipt['observations']],[x['id'] for x in manifest['cases']+manifest['direct_cases']])
    receipt['status']='PASS'
except BaseException as exc:
    receipt.update(error_type=type(exc).__name__,error=str(exc))
    raise
finally:
    with dest.open('x') as out:json.dump(receipt,out,indent=2);out.write('\n')
