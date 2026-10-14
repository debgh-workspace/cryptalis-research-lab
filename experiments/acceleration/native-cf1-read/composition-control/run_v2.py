"""Pre/post pin and cache checks, exact origins, exclusive full observation receipt."""
import importlib,json,sys,sysconfig
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent
sys.path.insert(0,str(R))
from guard_v2 import check,sha
if len(sys.argv)!=5:raise RuntimeError('Expected suite, kind, mode, unique output basename')
suite,kind,mode,name=sys.argv[1:]
if suite not in ('direct','wrapper','corpus') or kind not in ('normal','observed') or Path(name).name!=name or not name.endswith('.json'):raise RuntimeError('Invalid run scope')
if suite=='wrapper' and kind!='observed':raise RuntimeError('Wrapper ownership suite needs observed build')
if suite=='corpus' and kind!='normal':raise RuntimeError('Corpus requires normal build')
dest=R/'runs-v2'/name
if dest.exists():raise RuntimeError('Refuse receipt overwrite')
receipt={'status':'FAIL','suite':suite,'kind':kind,'mode':mode,'optimize':sys.flags.optimize,'observations':[],'negative':None}
runtime=None
try:
    frozen=check()
    if sys.executable!=frozen['python_executable'] or list(sys.version_info[:3])!=frozen['python_version'] or sys.flags.optimize not in (0,1) or not sys.flags.dont_write_bytecode or sysconfig.get_config_var('SOABI')!=frozen['soabi']:raise RuntimeError('Run interpreter mismatch')
    build_dir=R/('build-v2-'+kind);build=json.loads((build_dir/'build.json').read_text())
    if build['status']!='PASS' or build['prebuild_sha256']!=sha(R/'PREBUILD_v2.json') or sha(Path(build['binary']))!=build['binary_sha256']:raise RuntimeError('Unqualified build receipt')
    paths=[build_dir,R,B/'candidate-native-cf1-read-20261014',B/'candidate-s20-restored-20261014/src']
    sys.path[:0]=[str(p) for p in paths]
    import native_primitives,staged_read,fixture_support,cryptography
    from cryptalis.crypto import cf1,keys
    from cryptography.hazmat.backends.openssl.backend import backend
    expected=[(native_primitives,Path(build['binary'])),(staged_read,R/'staged_read.py'),
       (fixture_support,B/'candidate-native-cf1-read-20261014/fixture_support.py'),
       (cf1,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/cf1.py'),
       (keys,B/'candidate-s20-restored-20261014/src/cryptalis/crypto/keys.py')]
    for module,path in expected:
        if Path(module.__file__).absolute()!=path:raise RuntimeError('Unexpected module origin')
    if Path(cryptography.__file__).absolute()!=B/'repo/.venv/lib/python3.12/site-packages/cryptography/__init__.py' or cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Oracle origin/backend mismatch')
    # Verify actual process-mapped system libcrypto bytes, not version strings/-lcrypto alone.
    mapped=set()
    for line in Path('/proc/self/maps').read_text().splitlines():
        parts=line.split()
        if parts and parts[-1].startswith('/') and 'libcrypto.so' in parts[-1]:mapped.add(str(Path(parts[-1]).resolve()))
    expected_lib=str(Path(frozen['F_libcrypto']['path']).resolve())
    if mapped!={expected_lib} or sha(Path(expected_lib))!=frozen['F_libcrypto']['sha256']:raise RuntimeError('Mapped library mismatch')
    runtime=importlib.import_module({'direct':'direct_runtime_v2','wrapper':'wrapper_runtime_v2','corpus':'corpus_runtime_v2'}[suite])
    if Path(runtime.__file__)!=R/(runtime.__name__+'.py'):raise RuntimeError('Runtime origin mismatch')
    check()
    receipt.update(prebuild_sha256=sha(R/'PREBUILD_v2.json'),build_sha256=sha(build_dir/'build.json'),
                   native_origin=native_primitives.__file__,mapped_libcrypto=sorted(mapped),python_executable=sys.executable)
    if suite=='direct':runtime.run(kind,mode)
    else:runtime.run(mode)
    receipt['status']='PASS'
except BaseException as exc:
    receipt.update(error_type=type(exc).__name__,error=str(exc));raise
finally:
    if runtime is not None:
        receipt['observations']=runtime.observations
        receipt['negative']=getattr(runtime,'negative',getattr(runtime,'negative_record',None))
    try:check();receipt['post_pins_and_caches']='PASS'
    except BaseException as exc:receipt['status']='FAIL';receipt['post_pins_and_caches']='FAIL';receipt['post_pin_error']=str(exc)
    with dest.open('x') as f:json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n')
