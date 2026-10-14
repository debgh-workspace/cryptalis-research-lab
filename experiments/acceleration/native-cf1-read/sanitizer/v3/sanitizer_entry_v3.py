"""New sanitizer binary admission only; does not invoke any old launcher."""
import copy,importlib.util,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;B=R.parent
sys.path.insert(0,str(R))
from guard_v3 import cache,check,exact,install,interpreter,loaded_origins,mapped,save,sha
# Fixed positional interface: run ID, private cache. IDs/argv are independently frozen.
identifier,cache_path=sys.argv[1:];dest=R/(identifier+'-child.json')
receipt={'status':'FAIL','id':identifier,'observations':[],'integrity_errors':[]};anchor=None;binary=None;f=None;build=None
try:
    receipt['cache_before']=cache(cache_path);install();f=check();anchor=f['_anchor']
    plan=next(p for p in f['runs'] if p['id']==identifier)
    if sys.argv!=plan['argv'][plan['argv'].index(str(R/'sanitizer_entry_v3.py')):]:raise RuntimeError('Entry argv mismatch')
    interpreter(f,plan['optimize'])
    import os
    if dict(os.environ)!=plan['environment']:raise RuntimeError('Entry environment mismatch')
    kind=plan['build']
    if kind not in ('D-normal','D-diagnostic'):raise RuntimeError('D-only v3 admission')
    definition=next(b for b in f['builds'] if b['id']==kind)
    adoption=f['adopted_builds'][kind]
    if adoption['build_anchor']!=f['build_origin_anchor']:raise RuntimeError('Build lineage anchor mismatch')
    if sha(f['build_origin_freeze'])!=adoption['build_anchor']:raise RuntimeError('Build-origin freeze mismatch')
    build_path=R/('v2-build-'+kind+'.json');build=json.loads(build_path.read_text())
    if str(build_path)!=adoption['receipt'] or sha(build_path)!=adoption['receipt_sha256']:raise RuntimeError('Adopted build receipt mismatch')
    for key,wanted in {'status':'PASS','id':kind,'anchor':adoption['build_anchor'],'integrity_errors':[],'cache_before':[],'cache_final':[]}.items():
        if not exact(build.get(key),wanted):raise RuntimeError('Unaccepted sanitizer build '+key)
    if build['compiler']['command']!=definition['command'] or build['compiler']['environment']!=f['compiler_environment'] or build['compiler']['exit_code']!=0 or not build['compiler']['leader_reaped'] or build['compiler']['reason'] is not None or build['compiler']['cleanup_errors']:raise RuntimeError('Compiler receipt not accepted')
    if build['elf']['exit_code']!=0 or not build['elf']['leader_reaped'] or build['elf']['reason'] is not None or build['elf']['cleanup_errors']:raise RuntimeError('ELF receipt not accepted')
    if build['elf']['command']!=['/usr/bin/readelf','-d',definition['binary']] or build['needed']!=definition['needed']:raise RuntimeError('Wrong ELF build mapping')
    expected_cache=str(R/('v2-cache-controller-build-'+kind))
    if build['argv']!=[str(R/'control_v2.py'),'build',kind,expected_cache] or build['environment']!=f['compiler_environment'] or build['optimize']!=0:raise RuntimeError('Wrong build controller provenance')
    binary=definition['binary']
    if binary!=adoption['binary'] or sha(binary)!=adoption['binary_sha256'] or build['binary_sha256']!=adoption['binary_sha256']:raise RuntimeError('Adopted binary mismatch')
    for path,digest in f['d_helper_dependencies'].items():
        if f['pins'].get(path)!=digest or f['resolved_pins'].get(str(Path(path).resolve()))!=digest or sha(path)!=digest:raise RuntimeError('D helper dependency mismatch: '+path)
    if build['binary']!=binary or sha(binary)!=build['binary_sha256']:raise RuntimeError('Sanitizer binary mismatch')
    receipt.update(anchor=anchor,build_origin_anchor=adoption['build_anchor'],build_path=str(build_path),build_sha256=sha(build_path),binary=binary,binary_sha256=sha(binary))
    arm,variant=kind.split('-',1);source=f['arm_sources'][arm]
    sys.path[:0]=[str(Path(binary).parent),source,str(B/'candidate-native-cf1-read-20261014'),str(B/'candidate-s20-restored-20261014/src'),f['site_packages']]
    module_name={'T':'native_tuple','S':'native_primitives','D':'native_cf1'}[arm]
    spec=importlib.util.find_spec(module_name)
    if spec is None or spec.origin!=binary:raise RuntimeError('Native pre-import origin mismatch')
    native=importlib.import_module(module_name)
    if native.__file__!=binary:raise RuntimeError('Native loaded origin mismatch')
    if arm=='D' and native.backend_version()!='OpenSSL 3.5.7 9 Jun 2026':raise RuntimeError('Native backend mismatch')
    import cryptography
    from cryptography.hazmat.backends.openssl.backend import backend
    if cryptography.__file__!=f['site_packages']+'/cryptography/__init__.py' or cryptography.__version__!='50.0.2' or backend.openssl_version_text()!='OpenSSL 4.0.3 29 Sep 2026':raise RuntimeError('Python oracle backend mismatch')
    if arm=='D' and variant=='normal' and (hasattr(native,'open_fault') or hasattr(native,'open_observed')):raise RuntimeError('Diagnostic exports in normal D')
    if arm=='D' and variant=='diagnostic' and not hasattr(native,'open_observed'):raise RuntimeError('Missing D observed export')
    receipt['mapped_before']=mapped(f,binary,True);receipt['origins_before']=loaded_origins(f,binary)
    selection=json.loads((R/'CASE_SELECTION.json').read_text());extra=json.loads((R/'ADDITIONAL_EXPECTATIONS.json').read_text())
    emitted=[]
    def emit(identifier,actual,expected):
        if identifier in emitted:raise RuntimeError('Duplicate sanitizer observation')
        if not exact(actual,expected):raise RuntimeError('Unexpected sanitizer oracle mismatch: '+identifier)
        record={'id':identifier,'actual':copy.deepcopy(actual)};emitted.append(identifier)
        if plan['mode']=='negative' and identifier==plan['negative_target']:
            record['original']=copy.deepcopy(actual);record['original_verified']=True
            altered=copy.deepcopy(actual)
            # Adapters use various exact-output schemas; choose only frozen path.
            node=altered
            for part in plan['negative_path'][:-1]:node=node[part]
            key=plan['negative_path'][-1]
            if type(node[key]) is not str:raise RuntimeError('Negative target is not string')
            node[key]+='00';record['actual']=altered;record['negative_path']=plan['negative_path']
            receipt['observations'].append(record)
            if exact(altered,expected):raise RuntimeError('Negative unexpectedly unchanged')
            receipt['negative_target']=identifier
            raise RuntimeError('Sanitizer subset actual-observation mismatch: '+identifier)
        receipt['observations'].append(record)
    adapter_path=R/('adapters_'+arm.lower())/'adapter.py'
    spec=importlib.util.spec_from_file_location('sanitizer_adapter_'+arm,adapter_path)
    if spec is None or spec.origin!=str(adapter_path):raise RuntimeError('Adapter origin')
    adapter=importlib.util.module_from_spec(spec);sys.modules[spec.name]=adapter;spec.loader.exec_module(adapter)
    adapter.run(variant,selection,extra,emit)
    if emitted!=f['expected_ids'][kind]:raise RuntimeError('Sanitizer selected inventory mismatch')
    if plan['mode']!='positive':raise RuntimeError('Negative target not reached')
    receipt['status']='PASS'
except BaseException as exc:
    receipt.update(error_type=type(exc).__name__,error=str(exc))
finally:
    for name,operation in [('pins',lambda:check(anchor)),('cache',lambda:cache(cache_path)),('origins',lambda:loaded_origins(f,binary) if f else None),('mapped',lambda:mapped(f,binary,True) if f and binary else None)]:
        try:
            value=operation()
            if name!='pins':receipt[name+'_final']=value
        except BaseException as exc:receipt['integrity_errors'].append(name+': '+repr(exc))
    if build is not None:
        try:
            if sha(binary)!=build['binary_sha256']:raise RuntimeError('Binary changed')
        except BaseException as exc:receipt['integrity_errors'].append(repr(exc))
    if receipt['integrity_errors']:receipt['status']='FAIL_INTEGRITY'
    save(dest,receipt)
sys.exit(0 if receipt['status']=='PASS' else 1)
