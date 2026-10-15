"""Additive bounded launcher. V1 sources stay frozen and are never rewritten."""
import hashlib
import json
from pathlib import Path
import resource
import os

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
RECEIPTS=HERE/'parent-results'
SUPERVISOR_SHA='b5cc92887125d1b923cb49f9d673a922a75d55f31f19efb4934992c02a1f0065'

def digest(data):return hashlib.sha256(data).hexdigest()

ADMISSION_SHA='90b1fbc4805e5499bc30a19554652ee64f7f01534173e41147cea33789dee346'
TARGETS_SHA='dd0498d2183a341e8e9357638e30b93b642dab1ecc01b5e20f3377af71cdd300'
LOCAL_JSON_NAMES=frozenset(('plan.json', 'source-original.json', 'sa21-original.json', 'sa20-original.json'))

# Every independently reached local metadata read is name/type-admitted here.
def admission_local_path(name):
    admission_need(name in LOCAL_JSON_NAMES,'unadmitted_local_json:'+str(name))
    return admission_regular(HERE/name)

def admission_input_regular(path):
    path=Path(path)
    allowed=admission_json('FROZEN_TARGETS.json',TARGETS_SHA)
    admission_need(str(path) in allowed,'unadmitted_input_path:'+str(path))
    return admission_regular(path)
# Metadata-first admission; this helper never follows arbitrary manifest paths.
import re, stat

def admission_need(ok, why):
    if not ok: raise ValueError(why)

def admission_regular(path):
    path=Path(path)
    admission_need(path.is_absolute() and '..' not in path.parts,'absolute_regular_required:'+str(path))
    for parent in path.parents:
        admission_need(stat.S_ISDIR(parent.lstat().st_mode),'redirected_parent:'+str(parent))
    admission_need(stat.S_ISREG(path.lstat().st_mode),'not_regular:'+str(path))
    return path

def admission_json(name, expected_hash):
    path=admission_regular(HERE/name)
    payload=path.read_bytes()
    admission_need(hashlib.sha256(payload).hexdigest()==expected_hash,'admission_identity:'+name)
    return json.loads(payload)

def admission_data():
    return admission_json('PATH_ADMISSION.json',ADMISSION_SHA)

def admission_scan(root, installed=False):
    data=admission_data();root=Path(root)
    key=str(root)
    admission_need(key in data['roots'],'undeclared_inventory_root:'+key)
    policy=data['roots'][key]
    schema=policy['installed' if installed else 'original']
    for p in [root,*root.parents]:
        admission_need(stat.S_ISDIR(p.lstat().st_mode),'redirected_root:'+str(p))
    observed={};observed_dirs=set()
    allowed_dirs=set(schema['directories'])
    allowed_files=set(schema['regular'])
    links=schema['links']
    def walk(directory):
        for item in sorted(os.scandir(directory),key=lambda x:x.name):
            path=Path(item.path);name=str(path.relative_to(root))
            st=item.stat(follow_symlinks=False)
            if stat.S_ISDIR(st.st_mode):
                admission_need(name in allowed_dirs,'unexpected_directory:'+name)
                observed_dirs.add(name)
                walk(path)
            elif stat.S_ISREG(st.st_mode):
                admission_need(name in allowed_files,'unexpected_regular:'+name)
                observed[name]={'sha256':None}
            elif stat.S_ISLNK(st.st_mode):
                target=os.readlink(path)
                admission_need(links.get(name)==target,'unexpected_link:'+name)
                observed[name]={'link':target}
            else:raise ValueError('unexpected_special:'+name)
    walk(root)
    if not installed:admission_need(observed_dirs==allowed_dirs,'directory_membership:'+key)
    names=set(observed);required=set(schema['required'])
    admission_need(required<=names and names<=allowed_files|set(links),'inventory_membership:'+key)
    admission_need({n:v['link'] for n,v in observed.items() if 'link' in v}==links,'inventory_links:'+key)
    # Every path/type/link is admitted before this function returns to a hasher.
    return observed

def admitted_inventory(root, installed=False):
    observed=admission_scan(root,installed)
    for name,value in observed.items():
        if 'sha256' in value:
            p=admission_regular(Path(root)/name)
            value['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    return observed

def admitted_manifest(manifest, root):
    manifest=admission_regular(manifest)
    if manifest==HERE/'outer-frozen.sha256':
        allowed={str(HERE/n) for n in ('outer.py','supervisor_v2.py','frozen-inputs.sha256')}
    elif manifest==HERE/'frozen-inputs.sha256':
        allowed=set(admission_json('FROZEN_TARGETS.json',TARGETS_SHA))
    else:raise ValueError('undeclared_manifest:'+str(manifest))
    parsed={}
    for line in manifest.read_text().splitlines():
        expected,name=line.split('  ',1)
        admission_need(re.fullmatch('[0-9a-f]{64}',expected) is not None,'bad_manifest_digest')
        path=Path(name) if name.startswith('/') else root/name
        admission_need(str(path) in allowed and str(path) not in parsed,'unadmitted_manifest_target:'+str(path))
        parsed[str(path)]=expected
    admission_need(set(parsed)==allowed,'incomplete_manifest_target_set')
    # Validate all targets before any expanded target payload read.
    for name in parsed:admission_regular(Path(name))
    return parsed

def admission_external_tools():
    data=admission_data()
    for name in data['external_regular']:admission_regular(Path(name))
    for name,target in data['external_aliases'].items():
        p=Path(name)
        for parent in p.parents:admission_need(stat.S_ISDIR(parent.lstat().st_mode),'redirected_tool_parent')
        admission_need(stat.S_ISLNK(p.lstat().st_mode),'tool_alias_type')
        admission_need(str(p.resolve(strict=True))==target,'tool_alias_target')

def admission_all_originals():
    data=admission_data()
    admission_external_tools()
    for name,policy in data['roots'].items():
        if not policy.get('future_copy',False):admission_scan(Path(name))


def verify_manifest(manifest,root):
    errors=[];count=0
    try:
        admission_all_originals()
        parsed=admitted_manifest(manifest,root)
        for name,expected in parsed.items():
            actual=digest(admission_regular(Path(name)).read_bytes());count+=1
            if actual!=expected:errors.append({'path':name,'error':'digest_mismatch','expected':expected,'actual':actual})
    except BaseException as exc:errors.append({'manifest':str(manifest),'error':repr(exc)})
    return {'manifest':str(manifest),'checked':count,'pass':not errors,'errors':errors}

def original_inventory(name):
    errors=[];count=0
    try:
        # Both local paths are admitted before either payload is read, even
        # when this group follows an earlier frozen-manifest failure.
        plan_path=admission_local_path('plan.json')
        snapshot_path=admission_local_path(name+'-original.json')
        plan=json.loads(plan_path.read_text())
        root=Path(plan['source'] if name=='source' else plan['cells'][name])
        expected=json.loads(snapshot_path.read_text())
        actual=admitted_inventory(root)
        count=len(actual)
        if actual!=expected:
            errors.append({'error':'original_inventory_mismatch','missing':sorted(expected.keys()-actual.keys()),'added':sorted(actual.keys()-expected.keys()),'changed':sorted(n for n in expected.keys()&actual.keys() if expected[n]!=actual[n])})
    except BaseException as exc:errors.append({'error':repr(exc)})
    return {'original_cell':name,'checked':count,'pass':not errors,'errors':errors}

def integrity():
    # Each original path set, symlink target and regular file is checked even
    # when the installer child was killed before its own finally block.
    return [verify_manifest(HERE/'outer-frozen.sha256',HERE),
            verify_manifest(HERE/'frozen-inputs.sha256',HERE),
            original_inventory('sa21'),original_inventory('sa20'),original_inventory('source')]

def main():
    # Exclusive parent evidence, distinct from V1's exclusive run/ output.
    RECEIPTS.mkdir(exist_ok=False)
    original_limits=None
    report={'status':'NOT_STARTED','wall_seconds':120,'captured_stream_cap_each':2097152,
            'child_regular_file_limit_bytes':67108864,'before':None,'after':None,
            'child':None,'errors':[], 'prior_artifacts_preserved':True}
    env={'PATH':'/usr/bin:/bin','HOME':str(RECEIPTS/'home'),'TMPDIR':str(RECEIPTS/'tmp'),
         'LC_ALL':'C.UTF-8','LANG':'C.UTF-8','TZ':'UTC','SOURCE_DATE_EPOCH':'0',
         'UV_OFFLINE':'1','UV_CACHE_DIR':str(RECEIPTS/'cache'),'PYTHONDONTWRITEBYTECODE':'1'}
    try:
        for name in ['home','tmp','cache']:(RECEIPTS/name).mkdir(exist_ok=False)
        report['before']=integrity()
        if not all(x['pass'] for x in report['before']):raise ValueError('preflight_integrity')
        if os.path.lexists(BASE/'release-lab/cleanup-transport-installed-20261015'):raise ValueError('install_output_exists')
        source=admission_regular(HERE/'supervisor_v2.py').read_bytes()
        if digest(source)!=SUPERVISOR_SHA:raise ValueError('supervisor_identity')
        namespace={'__name__':'pinned_bounded_supervisor','__file__':str(HERE/'supervisor_v2.py')}
        exec(compile(source,str(HERE/'supervisor_v2.py'),'exec'),namespace)
        # Bound redirected per-step logs as well as supervisor-captured streams.
        # This limit is inherited by bash and its build/helper children.
        original_limits=resource.getrlimit(resource.RLIMIT_FSIZE)
        soft,hard=original_limits
        limit=67108864 if soft==resource.RLIM_INFINITY else min(67108864,soft)
        resource.setrlimit(resource.RLIMIT_FSIZE,(limit,hard))
        report['child_regular_file_limit_bytes']=limit
        report['parent_original_fsize_limits']=list(original_limits)
        report['child']=namespace['bounded'](['/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3','-I','-B',str(HERE/'install_verify.py')],env,120,2097152)
        child=report['child']
        if child['reason'] is not None or child['exit_code']!=0 or child['cleanup_errors'] or not child['leader_reaped']:
            raise ValueError('child_failed_or_cleanup_incomplete')
        report['status']='PASS_BOUNDED_INSTALLATION'
    except BaseException as exc:
        report['status']='FAIL'
        report['errors'].append(repr(exc))
    finally:
        # Child cleanup is complete before restoring the parent's original soft
        # limit. The hard limit was never lowered; restoration needs no privilege.
        if original_limits is not None:
            try:
                resource.setrlimit(resource.RLIMIT_FSIZE,original_limits)
                report['parent_fsize_limits_restored']=True
            except BaseException as exc:
                report['status']='FAIL'
                report['parent_fsize_limits_restored']=False
                report['errors'].append('restore_parent_fsize: '+repr(exc))
        # Always attempt each frozen-input/source integrity group, even on set-e
        # failure, supervisor timeout/cap, launch exception, or Python interruption.
        report['after']=integrity()
        if not all(x['pass'] for x in report['after']):report['status']='FAIL_INTEGRITY'
        report['outer_environment']=env
        report['inner_environment_note']='Installer inherits only this exact allowlisted environment; no source or database test execution.'
        with (RECEIPTS/'parent-receipt.json').open('x') as stream:
            json.dump(report,stream,indent=2,sort_keys=True);stream.write('\n')
    return 0 if report['status']=='PASS_BOUNDED_INSTALLATION' else 1

if __name__=='__main__':raise SystemExit(main())
