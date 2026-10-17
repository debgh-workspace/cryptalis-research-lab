"""Source-reviewed genuine-module constructor-only experiment; root selects runs."""
import hashlib
import json
import os
import re
from pathlib import Path
import stat
import sys
from types import ModuleType

ROOT = Path('/workspace/scratch/cb28ee9f5f4a/recovery-work/column-projection-inspector-v1-20261017')
STDLIB = Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/python/lib/python3.12')
HOST = '/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12'
PRODUCT = Path('/workspace/scratch/cb28ee9f5f4a/recovery-work/integrated222-v2-20261017/source')
CACHE = ROOT/'bytecode-absent'
CAP = 32 * 1024 * 1024
OWNED_READ_FDS = set()
NATIVE_BINDING_NAMES = ('cython_runtime', '_cython_3_3_0')
CFFI_BINDING_NAMES = ('_openssl', '_openssl.lib')
DEPRECATION_WRAPPERS = {
    'cryptography.hazmat.primitives.ciphers.algorithms': ('cryptography/hazmat/primitives/ciphers/algorithms.py', '2067c2c9c6093a1d53be8237e2b7f0f0a7c9ff19add69fc3a4186dd8582171ea'),
    'cryptography.hazmat.primitives.ciphers.modes': ('cryptography/hazmat/primitives/ciphers/modes.py', '1fb0194a02624930428b482b2fdecdc5a912f79d09c852982ecadaf2d8c73f14'),
    'cryptography.hazmat.primitives.asymmetric.dh': ('cryptography/hazmat/primitives/asymmetric/dh.py', '467b767cb683a501234125fc7cdb659935ce2478e5b7f0ca419d5595f85d8dae'),
    'cryptography.hazmat.primitives.serialization': ('cryptography/hazmat/primitives/serialization/__init__.py', '7d772ee3dba02fdaf1869465ff06639cca84f430a484231cb11c5f8ffa93bde8'),
}
ORIGIN_LABELS = frozenset((
    'native_bootstrap_shape', 'explicit_binary_backend', 'migration_origin',
    'actual_class_binding', 'product_origin', 'product_spec_origin',
    'product_module_set', 'typing_alias_identity', 'unidentified_native_bootstrap',
    'module_file_type', 'loaded_origin_outside_admission', 'dependency_spec_origin',
    'native_openssl_extension_binding', 'native_openssl_owner_shape',
    'native_openssl_lib_shape', 'native_openssl_relations',
    'deprecation_utils_binding', 'deprecation_class_binding',
    'deprecation_wrapper_shape', 'deprecation_raw_origin', 'deprecation_identity',
))
KNOWN_DEPENDENCY_PREFIXES = frozenset((
    '_cffi_backend', 'cffi', 'cryptography', 'greenlet', 'psycopg',
    'psycopg_binary', 'sqlalchemy', 'typing_extensions',
))


def safe_origin_detail(error, stage, module_name):
    # Never stringify arbitrary exception bodies, locals, module objects or paths.
    if (stage != 'IMPORT_REAL_MODULE' or type(error) is not AssertionError
            or len(error.args) != 1 or type(error.args[0]) is not str
            or error.args[0] not in ORIGIN_LABELS):
        return None
    safe_name = None
    if (type(module_name) is str and 1 <= len(module_name) <= 160
            and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', module_name)
            and module_name.split('.')[0] in KNOWN_DEPENDENCY_PREFIXES):
        safe_name = module_name
    detail = {'assertion_label': error.args[0], 'known_dependency_module': safe_name}
    # One rejected sys.modules key only. This reports no attributes, values,
    # paths or admission and leaves the rejection unchanged.
    if error.args[0] == 'unidentified_native_bootstrap':
        identifier = None
        if (type(module_name) is str and 1 <= len(module_name) <= 120
                and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', module_name)):
            identifier = module_name
        detail['rejected_fileless_module_identifier'] = identifier
    return detail

NEW_HASH = '34ef8d914cdaf6f22c2297661fda7c04f16a83b71061be1ac5510a03caa6f33b'



def require(condition, label):
    if not condition:
        raise AssertionError(label)


def stamp(path):
    p=Path(path)
    require(p.is_absolute() and '..' not in p.parts, 'absolute_path')
    for parent in p.parents:
        s=parent.lstat()
        require(stat.S_ISDIR(s.st_mode) and not stat.S_ISLNK(s.st_mode), 'ordinary_ancestor')
    s=p.lstat()
    require(stat.S_ISREG(s.st_mode) and s.st_nlink >= 1 and 0 <= s.st_size <= CAP, 'ordinary_bounded_leaf')
    return (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)


def read(path, expected):
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
    OWNED_READ_FDS.add(fd)
    try:
        with os.fdopen(fd,'rb') as stream:
            s=os.fstat(stream.fileno())
            require((s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)==expected,'fd_identity')
            body=stream.read(CAP+1)
    finally:
        OWNED_READ_FDS.discard(fd)
    require(len(body)<=CAP and stamp(path)==expected,'read_identity')
    return body




def main():
    admitted={}; before={}; final={}; primary=None; records=[]; origins={}; stage='STARTUP'
    wrapper_origins={}; wrapper_bindings={}
    current_origin_module=None; variant=None; guard_active=False; dependency_origins={}; embedded_native_modules=[]; trusted_typing_aliases=[]
    try:
        require(len(sys.argv)==3 and sys.argv[1]=='combined','argv')
        variant,seal=sys.argv[1:]
        require(len(seal)==64 and all(c in '0123456789abcdef' for c in seal),'seal_format')
        require(Path(__file__)==ROOT/'run_module_diagnostics.py' and Path.cwd()==ROOT,'runner_location')
        require(sys.executable==HOST and sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
                and not sys.flags.optimize and sys.pycache_prefix==str(CACHE),'host_flags')
        require(dict(os.environ)=={'LANG':'C.UTF-8','LC_ALL':'C.UTF-8','TZ':'UTC','PSYCOPG_IMPL':'binary'},'clean_environment')
        require(not os.path.lexists(CACHE),'cache_absent')
        require(not any(name in sys.modules for name in ('site','sitecustomize','usercustomize','pytest','conftest','cryptalis','sqlalchemy','psycopg')),'no_preloaded_targets')
        source=ROOT/'SOURCE.sha256'; before[str(source)]=stamp(source)
        raw=read(source,before[str(source)])
        require(hashlib.sha256(raw).hexdigest()==seal,'source_seal')
        admitted[str(source)]=seal
        manifest={}
        for line in raw.decode().splitlines():
            digest,name=line.split('  ',1)
            require(len(digest)==64 and all(c in '0123456789abcdef' for c in digest),'member_digest')
            require(name not in manifest and not Path(name).is_absolute() and '..' not in Path(name).parts,'member_path')
            manifest[name]=digest
        names=('run_module_diagnostics.py','DEPENDENCIES.json','INTEGRATION_MANIFEST.json','README.md','MATERIALIZATION_RECEIPT.json','column_projection.py','projection_cases.py')
        for name in names: before[str(ROOT/name)]=stamp(ROOT/name)
        controls={}
        for name in names:
            body=read(ROOT/name,before[str(ROOT/name)])
            require(hashlib.sha256(body).hexdigest()==manifest[name],'control_hash')
            admitted[str(ROOT/name)]=manifest[name]; controls[name]=body
        deps=json.loads(controls['DEPENDENCIES.json'])
        require(len(deps['files'])==509 and set(manifest)==set(names),'finite_maps')
        require(hashlib.sha256(controls['INTEGRATION_MANIFEST.json']).hexdigest()==
                '486f900e78cf426f33a5fba71a8d4e992657572c5af10254ec7602c0c707ae5d','integration_manifest_binding')
        require(hashlib.sha256(controls['MATERIALIZATION_RECEIPT.json']).hexdigest()==
                '0c5d736ee47de25f3e97b8665349db39644da5480c6b1e13d2a98b1a0d2976b2','materialization_receipt_binding')
        integration=json.loads(controls['INTEGRATION_MANIFEST.json'])
        receipt=json.loads(controls['MATERIALIZATION_RECEIPT.json'])
        source_map={item['path']:item['sha256'] for item in integration['files']}
        require(len(integration['files'])==len(source_map)==222
                and receipt['source_root']==str(PRODUCT)
                and receipt['source_hashes']==source_map,'composition_identity')
        runtime={name:digest for name,digest in source_map.items()
                 if name.startswith('src/cryptalis/') and name.endswith('.py')}
        require(len(runtime)==43,'runtime_count')
        for name,digest in runtime.items():
            path=PRODUCT/name
            require('..' not in Path(name).parts and path.is_relative_to(PRODUCT/'src/cryptalis')
                    and str(path) not in admitted,'runtime_scope')
            admitted[str(path)]=digest
        for path,digest in deps['files'].items():
            require(Path(path).is_relative_to(deps['prefix']) and path not in admitted,'dependency_scope')
            admitted[path]=digest
        require(len(admitted)==560,'exact_admission_count')
        stage='FULL_ADMISSION'
        complete={path:stamp(path) for path in admitted}
        require(all(complete[path]==value for path,value in before.items()),'control_metadata_preserved')
        before=complete
        for path,digest in admitted.items():
            require(hashlib.sha256(read(path,before[path])).hexdigest()==digest,'admitted_hash')
        target=PRODUCT/'src/cryptalis/migration.py'
        require(admitted[str(target)]==NEW_HASH,'combined_migration_hash')
        allowed=set(admitted); trusted=str(STDLIB)+os.sep
        def audit(event,args):
            if event=='import' and len(args)>1 and args[1] is not None:
                origin=os.fsdecode(args[1])
                if origin not in allowed and not (origin.startswith(trusted) and '/site-packages/' not in origin):
                    raise PermissionError('undeclared extension import denied')
            if event=='open':
                path,mode,flags=args
                if (isinstance(mode,str) and any(c in mode for c in 'wax+')) or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):
                    raise PermissionError('writes denied')
                if isinstance(path,int):
                    require(path in OWNED_READ_FDS,'unowned_descriptor_read')
                    return  # Only owned read-only runner fdopen; no native confinement claim.
                path=os.fsdecode(path)
                require(os.path.isabs(path) and os.path.normpath(path)==path,'canonical_open')
                if path.endswith(('.pyc','.pyo')): raise PermissionError('bytecode body denied')
                if path not in allowed and not (path.startswith(trusted) and '/site-packages/' not in path):
                    raise PermissionError('undeclared read denied')
            if event.startswith(('socket.','subprocess.','os.exec','os.spawn')) or event in ('os.system','os.fork','os.forkpty','os.remove','os.rename','os.mkdir','os.rmdir','os.link','os.symlink','os.truncate','os.chmod','os.chown','os.utime','os.chdir'):
                raise PermissionError('external operation denied')
        sys.addaudithook(audit); guard_active=True
        view=PRODUCT/'src'
        sys.path[:]=[str(view),deps['prefix'],str(ROOT),str(STDLIB),str(STDLIB/'lib-dynload')]
        require(all(name not in sys.modules for name in NATIVE_BINDING_NAMES+CFFI_BINDING_NAMES),'native_bootstrap_not_preloaded')
        stage='IMPORT_REAL_MODULE'
        import cryptalis.migration as migration
        import psycopg
        import column_projection
        import projection_cases
        local_modules={'column_projection':column_projection,'projection_cases':projection_cases}
        def check_local_modules():
            for name,module in local_modules.items():
                path=str(ROOT/(name+'.py'))
                require(type(module) is ModuleType and sys.modules.get(name) is module
                        and module.__name__==name and module.__file__==path
                        and module.__spec__ is not None and module.__spec__.origin==path,
                        'inspector_module_origin')
            require(column_projection.inspect_column_projection.__code__.co_filename==str(ROOT/'column_projection.py')
                    and projection_cases.run_cases.__code__.co_filename==str(ROOT/'projection_cases.py'),
                    'inspector_function_origin')
        check_local_modules()
        compiler=sys.modules['cryptalis.manifest.compiler']
        producer_bindings=[(migration,'_facts',migration._facts)]
        producer_bindings += [(compiler,name,getattr(compiler,name)) for name in
                              ('_schema_facts','_read_schema_facts','_rows','_digest','_canonical')]
        def check_producer_bindings():
            require(migration._schema_facts is compiler._schema_facts,'actual_schema_producer_alias')
            for module,name,function in producer_bindings:
                expected_path=(str(PRODUCT/'src/cryptalis/migration.py') if module is migration else
                               str(PRODUCT/'src/cryptalis/manifest/compiler.py'))
                require(getattr(module,name) is function and function.__code__.co_filename==expected_path,
                        'actual_schema_producer_binding')
        check_producer_bindings()
        # Capture only at the end of this reviewed native-import window. This
        # relies on trusted native initialization, not vendor/source provenance.
        native_bindings={}
        for name in NATIVE_BINDING_NAMES:
            native_binding=sys.modules.get(name)
            require(type(native_binding) is ModuleType and native_binding.__name__==name
                    and getattr(native_binding,'__file__',None) is None
                    and getattr(native_binding,'__spec__',None) is None,'native_bootstrap_shape')
            native_bindings[name]=native_binding
        require(psycopg.pq.__impl__=='binary','explicit_binary_backend')
        # Exact CFFI owner relation, not a generic fileless-module allowance.
        rust_name='cryptography.hazmat.bindings._rust'
        rust_owner=sys.modules.get(rust_name)
        cffi_backend=sys.modules.get('_cffi_backend')
        rust_path=deps['prefix']+'/cryptography/hazmat/bindings/_rust.abi3.so'
        backend_path=deps['prefix']+'/_cffi_backend.cpython-312-x86_64-linux-gnu.so'
        def check_extension_owner(module,name,path,digest):
            require(type(module) is ModuleType and module.__name__==name
                    and path in deps['files'] and deps['files'][path]==digest
                    and module.__file__==path and module.__spec__ is not None
                    and module.__spec__.origin==path,'native_openssl_extension_binding')
        check_extension_owner(rust_owner,rust_name,rust_path,
                              '1e5d23fa66915204b9b67202a46993844d81cda56f6ad52cead2def37617ee29')
        check_extension_owner(cffi_backend,'_cffi_backend',backend_path,
                              '9bc1d08072255a5ec2db10fc75df1dd9e73097a75cd9150cfe875ebd6712f17c')
        openssl_owner=getattr(rust_owner,'_openssl',None)
        require(type(openssl_owner) is ModuleType and openssl_owner.__name__=='_openssl'
                and getattr(openssl_owner,'__file__',None) is None
                and getattr(openssl_owner,'__spec__',None) is None,'native_openssl_owner_shape')
        openssl_lib=getattr(openssl_owner,'lib',None)
        openssl_lib_type=type(openssl_lib)
        def check_openssl_bindings():
            require(type(openssl_owner) is ModuleType and openssl_owner.__name__=='_openssl'
                    and getattr(openssl_owner,'__file__',None) is None
                    and getattr(openssl_owner,'__spec__',None) is None,'native_openssl_owner_shape')
            require(type(openssl_lib) is openssl_lib_type and openssl_lib_type is not ModuleType
                    and openssl_lib_type.__module__=='_cffi_backend' and openssl_lib_type.__name__=='Lib'
                    and getattr(openssl_lib,'__name__',None)=='_openssl.lib'
                    and getattr(openssl_lib,'__file__',None) is None
                    and getattr(openssl_lib,'__spec__',None) is None,'native_openssl_lib_shape')
            require(sys.modules.get(rust_name) is rust_owner
                    and sys.modules.get('_cffi_backend') is cffi_backend
                    and getattr(rust_owner,'_openssl',None) is openssl_owner
                    and sys.modules.get('_openssl') is openssl_owner
                    and getattr(openssl_owner,'lib',None) is openssl_lib
                    and sys.modules.get('_openssl.lib') is openssl_lib,'native_openssl_relations')
        check_openssl_bindings()
        cffi_bindings={'_openssl':openssl_owner,'_openssl.lib':openssl_lib}
        # Closed source-backed proxy policy. No imports or registry replacement.
        utils_name='cryptography.utils'
        utils_owner=sys.modules.get(utils_name)
        utils_path=deps['prefix']+'/cryptography/utils.py'
        utils_hash='21aed2d106734b47b3c2920741f63c1b57bea381a3ac78a31175e3c00af58ae2'
        def check_utils_owner():
            require(type(utils_owner) is ModuleType and sys.modules.get(utils_name) is utils_owner
                    and utils_owner.__name__==utils_name and utils_owner.__file__==utils_path
                    and utils_owner.__spec__ is not None and utils_owner.__spec__.name==utils_name
                    and utils_owner.__spec__.origin==utils_path
                    and deps['files'].get(utils_path)==utils_hash,'deprecation_utils_binding')
        check_utils_owner()
        proxy_class=utils_owner._ModuleWithDeprecations
        def check_proxy_class():
            check_utils_owner()
            require(utils_owner._ModuleWithDeprecations is proxy_class and type(proxy_class) is type
                    and proxy_class.__module__==utils_name
                    and proxy_class.__name__=='_ModuleWithDeprecations'
                    and proxy_class.__bases__==(ModuleType,)
                    and proxy_class.__init__.__code__.co_filename==utils_path,'deprecation_class_binding')
        check_proxy_class()
        def check_wrapper(name,wrapper,raw):
            check_proxy_class()
            relative,digest=DEPRECATION_WRAPPERS[name]
            path=deps['prefix']+'/'+relative
            require(type(wrapper) is proxy_class and sys.modules.get(name) is wrapper,
                    'deprecation_identity')
            require(ModuleType.__getattribute__(wrapper,'_module') is raw,
                    'deprecation_identity')
            require(type(raw) is ModuleType and raw.__name__==name and raw.__file__==path
                    and raw.__spec__ is not None and raw.__spec__.name==name
                    and raw.__spec__.origin==path and deps['files'].get(path)==digest,
                    'deprecation_raw_origin')
            require(ModuleType.__getattribute__(wrapper,'__name__')==name
                    and ModuleType.__getattribute__(wrapper,'__spec__') is None
                    and wrapper.__file__==path,'deprecation_wrapper_shape')
            return raw
        for name in DEPRECATION_WRAPPERS:
            if name not in sys.modules: continue
            current_origin_module=name
            wrapper=sys.modules[name]
            require(type(wrapper) is proxy_class,'deprecation_wrapper_shape')
            raw=ModuleType.__getattribute__(wrapper,'_module')
            check_wrapper(name,wrapper,raw)
            wrapper_bindings[name]=(wrapper,raw)
            wrapper_origins[name]={'path':raw.__file__,'sha256':deps['files'][raw.__file__],
                                   'wrapper_spec_is_none':True,'origin_owner':'checked_original_module'}
        current_origin_module=None
        expected=str(view/'cryptalis/migration.py')
        cls=migration.TransitionFailure
        require(migration.__file__==expected and migration.__spec__.origin==expected,'migration_origin')
        require(cls.__module__=='cryptalis.migration' and cls.__init__.__code__.co_filename==expected,'actual_class_binding')
        # Fail if any imported product module escaped the selected exact view.
        for name,module in tuple(sys.modules.items()):
            current_origin_module=name
            if name=='cryptalis' or name.startswith('cryptalis.'):
                path=getattr(module,'__file__',None)
                require(isinstance(path,str) and path in admitted and Path(path).is_relative_to(view),'product_origin')
                require(getattr(module,'__spec__',None) is not None and module.__spec__.origin==path,'product_spec_origin')
                origins[name]={'path':path,'sha256':admitted[path]}
        current_origin_module=None
        require('cryptalis.migration' in origins and len(origins)<=43,'product_module_set')
        for name,module in tuple(sys.modules.items()):
            current_origin_module=name
            if name in wrapper_bindings:
                module=check_wrapper(name,*wrapper_bindings[name])
            path=getattr(module,'__file__',None)
            if path is None:
                if getattr(module,'__spec__',None) is None:
                    if name in ('typing.io','typing.re'):
                        require('typing' in sys.modules and module is getattr(sys.modules['typing'],name.split('.')[1]),'typing_alias_identity')
                        trusted_typing_aliases.append(name)
                    elif name in CFFI_BINDING_NAMES:
                        require(module is cffi_bindings[name],'native_openssl_relations')
                        embedded_native_modules.append(name)
                    else:
                        require(name in NATIVE_BINDING_NAMES and module is native_bindings[name],'unidentified_native_bootstrap')
                        embedded_native_modules.append(name)
                continue
            require(isinstance(path,str),'module_file_type')
            if path.startswith(trusted) and '/site-packages/' not in path: continue
            require(path in admitted,'loaded_origin_outside_admission')
            if path in deps['files']:
                require(module.__spec__ is not None and module.__spec__.origin==path,'dependency_spec_origin')
                dependency_origins[name]={'path':path,'sha256':deps['files'][path]}
        current_origin_module=None
        bound_modules={name:sys.modules[name] for name in tuple(origins)+tuple(dependency_origins)+tuple(trusted_typing_aliases)+tuple(embedded_native_modules)}
        stage='RECORDING_CONNECTION_CASES'
        records=projection_cases.run_cases(migration,column_projection)
        check_local_modules()
        check_producer_bindings()
        require(all(sys.modules.get(name) is module for name,module in bound_modules.items()),'module_identity_after_cases')
        for name,native_binding in native_bindings.items():
            require(sys.modules.get(name) is native_binding,'native_bootstrap_identity_after_cases')
            require(type(native_binding) is ModuleType and native_binding.__name__==name
                    and getattr(native_binding,'__file__',None) is None
                    and getattr(native_binding,'__spec__',None) is None,'native_bootstrap_shape_after_cases')
        check_openssl_bindings()
        check_proxy_class()
        for name,(wrapper,raw) in wrapper_bindings.items():
            check_wrapper(name,wrapper,raw)
        for name,entry in {**origins,**dependency_origins}.items():
            module=(wrapper_bindings[name][1] if name in wrapper_bindings else sys.modules[name])
            require(module.__file__==entry['path'] and module.__spec__.origin==entry['path'],'module_origin_after_cases')
        for name in trusted_typing_aliases:
            require(sys.modules[name] is getattr(sys.modules['typing'],name.split('.')[1]),'typing_alias_after_cases')
        require(not any(name in sys.modules for name in ('pytest','conftest')),'no_test_framework')
    except BaseException as error:
        primary={'type':type(error).__name__,'stage':stage}
        detail=safe_origin_detail(error,stage,current_origin_module)
        if detail is not None: primary['origin_detail']=detail
    finally:
        # Preserve the primary outcome; closure failures are separately recorded.
        stamps={}
        for path in admitted:
            try:
                stamps[path]=stamp(path)
                require(path in before and stamps[path]==before[path],'final_metadata')
                final[path]='METADATA_PASS'
            except BaseException as error: final[path]='METADATA_'+type(error).__name__
        for path,digest in admitted.items():
            if final[path]!='METADATA_PASS': continue
            try:
                require(hashlib.sha256(read(path,stamps[path])).hexdigest()==digest,'final_hash')
                final[path]='PASS'
            except BaseException as error: final[path]='HASH_'+type(error).__name__
        absence=not os.path.lexists(CACHE)
        closure=(primary is None and len(records)==39 and len(admitted)==560
                 and all(value=='PASS' for value in final.values()) and absence and guard_active)
        success=closure and variant=='combined' and all(record['status']=='PASS' for record in records)
        status='PASS_COLUMN_PROJECTION_RECORDING_INTEGRATION' if success else 'HOLD'
        report={'status':status,'variant':variant,
                'integration_manifest_sha256':'486f900e78cf426f33a5fba71a8d4e992657572c5af10254ec7602c0c707ae5d',
                'primary':primary,'case_count':len(records),'cases':records,'product_origins':origins,
                'deprecation_wrapper_origins':wrapper_origins,
                'dependency_origins':dependency_origins,'embedded_native_modules':embedded_native_modules,'trusted_typing_aliases':trusted_typing_aliases,
                'admitted_count':len(admitted),'preservation':final,'cache_absent':absence,
                'scope':'Actual compiler catalog projection and migration._facts with recording connection; isolated column shape only; no SQL execution, native catalog truth, ownership or successor authority',
                'metadata_validated':False,'current_native_verified':False,'successor_authorized':False,'mutants_repeated':False}
        encoded=json.dumps(report,sort_keys=True)
        require(len(encoded.encode())<=256*1024,'result_bound')
        sys.stdout.write('MODULE_DIAGNOSTICS_JSON '+encoded+'\n'); sys.stdout.flush()
    return 0 if success else 1


if __name__=='__main__':
    raise SystemExit(main())
