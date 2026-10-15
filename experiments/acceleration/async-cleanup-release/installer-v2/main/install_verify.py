"""Reviewed offline copy/install verifier. Does not run runtime tests."""
import base64,csv,hashlib,io,json,os,shutil,subprocess,sys,zipfile,stat
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent

ADMISSION_SHA='cbf24f59d1380be9937311d6b05d698574df7535199e736b6dacc905f19d5f2a'
TARGETS_SHA='dae5b3975bc4cdaba158f87123abec30dca162e60cda0ab1e31616e23fd06177'
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

PLAN=json.loads(admission_local_path('plan.json').read_text())
OUT=BASE/'release-lab/async-cleanup-installed-20261015'
SITE=Path('lib/python3.12/site-packages')
DIST='cryptalis-0.1.0.dist-info'
RECORD=DIST+'/RECORD'
def need(ok,why):
    if not ok:raise ValueError(why)
def sha(data):return hashlib.sha256(data).hexdigest()
def inventory(root,installed=False):
    return admitted_inventory(root,installed)

def owned(n):
    return n=='bin/cryptalis' or n.startswith(str(SITE)+'/cryptalis/') or n.startswith(str(SITE)+'/'+DIST+'/')
def dependencies(inv):return {n:v for n,v in inv.items() if not owned(n)}
def rows(data):
    result=list(csv.reader(io.StringIO(data.decode())))
    need(all(len(r)==3 for r in result),'record_shape')
    need(len(result)==len({r[0] for r in result}),'duplicate_record')
    return result
def check_hash(data,digest,size):
    need(digest=='sha256='+base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode() and size==str(len(data)),'record_hash')
def verify(cell,wheel):
    site=cell/SITE
    with zipfile.ZipFile(admission_input_regular(wheel)) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        need(len(names)==len(set(names)),'duplicate_wheel')
        for info in infos:
            n=info.filename
            need(not n.startswith('/') and '..' not in n.split('/'),'wheel_path')
            kind=stat.S_IFMT(info.external_attr >> 16)
            need(kind in ((0,stat.S_IFDIR) if info.is_dir() else (0,stat.S_IFREG)),'wheel_special_member')
        payload={i.filename:z.read(i) for i in infos if not i.is_dir()}
    archive_rows=rows(payload[RECORD]);need({r[0] for r in archive_rows}==set(payload),'wheel_coverage')
    hashed=0
    for n,digest,size in archive_rows:
        if n==RECORD:need(digest==size=='','wheel_self');continue
        check_hash(payload[n],digest,size);need(admission_regular(site/n).read_bytes()==payload[n],'installed_payload:'+n);hashed+=1
    need(hashed==45,'wheel_payload_count')
    modules={str(p.relative_to(site)) for p in (site/'cryptalis').rglob('*.py')}
    need(len(modules)==41 and modules=={n for n in payload if n.endswith('.py')},'module_inventory')
    for n in modules:need(admission_regular(site/n).read_bytes()==admission_input_regular(Path(PLAN['source'])/'src'/n).read_bytes(),'source_module:'+n)
    generated={DIST+'/'+n for n in ['INSTALLER','REQUESTED','direct_url.json','uv_cache.json']}|{'../../../bin/cryptalis'}
    installed_rows=rows(admission_regular(site/RECORD).read_bytes())
    actual={r[0] for r in installed_rows}
    need(actual-set(payload) in (generated, generated-{DIST+'/uv_cache.json'}),'installer_record_additions')
    generated=actual-set(payload)
    need(set(payload)<=actual,'installed_record_coverage')
    for n,digest,size in installed_rows:
        p=(site/n).resolve();need(p.is_relative_to(cell.resolve()),'installed_record_escape')
        if n==RECORD:need(digest==size=='','installed_self');continue
        check_hash(admission_regular(p).read_bytes(),digest,size)
    direct=json.loads(admission_regular(site/DIST/'direct_url.json').read_text())
    need(direct['url']==wheel.as_uri(),'installed_wheel_origin')
    need(admission_regular(site/DIST/'INSTALLER').read_text().strip()=='uv','installer_identity')
    # Accept only an exact fixed uv launcher body and exact fresh interpreter.
    # Long paths can use uv's shell trampoline; arbitrary wrapper code is refused.
    interpreter=str(cell/'bin/python').encode()
    cli_tail=b'# -*- coding: utf-8 -*-\nimport sys\nfrom cryptalis.cli import main\nif __name__ == "__main__":\n    if sys.argv[0].endswith("-script.pyw"):\n        sys.argv[0] = sys.argv[0][:-11]\n    elif sys.argv[0].endswith(".exe"):\n        sys.argv[0] = sys.argv[0][:-4]\n    sys.exit(main())\n'
    direct=b'#!'+interpreter+b'\n'
    trampoline=b"#!/bin/sh\n'''exec' "+interpreter+b" \"$0\" \"$@\"\n' '''\n"
    quoted_trampoline=b"#!/bin/sh\n'''exec' '"+interpreter+b"' \"$0\" \"$@\"\n' '''\n"
    need(admission_regular(cell/'bin/cryptalis').read_bytes() in {prefix+cli_tail for prefix in (direct,trampoline,quoted_trampoline)},'entrypoint_exact_uv_launcher')
    return {'wheel_payload_entries':hashed,'runtime_modules':41,'installer_added_record_entries':sorted(generated),'installed_record_sha256':sha(admission_regular(site/RECORD).read_bytes())}
def main():
    OUT.mkdir(exist_ok=False)
    report={'status':'FAIL','cells':{},'original_cells_unchanged':False}
    originals={name:Path(path) for name,path in PLAN['cells'].items()}
    snapshot_paths={name:admission_local_path(name+'-original.json') for name in originals}
    source_snapshot_path=admission_local_path('source-original.json')
    snapshots={name:json.loads(path.read_text()) for name,path in snapshot_paths.items()}
    wheel=Path(PLAN['wheel'])
    source=Path(PLAN['source'])
    source_snapshot=json.loads(source_snapshot_path.read_text())
    try:
        admission_all_originals()
        need(sha(admission_input_regular(wheel).read_bytes())==PLAN['wheel_sha256'],'wheel_pin')
        need(inventory(source)==source_snapshot and len(source_snapshot)==217,'source_pin')
        need(sha(admission_input_regular(Path(PLAN['uv'])).read_bytes())==PLAN['uv_sha256'],'uv_pin')
        for name,src in originals.items():need(inventory(src)==snapshots[name],'original_changed:'+name)
        original_inodes={(p.stat().st_dev,p.stat().st_ino) for src in originals.values() for p in src.rglob('*') if p.is_file() and not p.is_symlink()}
        new_inodes=set()
        for name,src in originals.items():
            dst=OUT/name
            shutil.copytree(src,dst,symlinks=True,copy_function=shutil.copy2)
            need(inventory(dst)==snapshots[name],'copy_bytes:'+name)
            for n,v in snapshots[name].items():
                if 'sha256' in v:
                    a,b=(src/n).stat(),(dst/n).stat()
                    need((a.st_dev,a.st_ino)!=(b.st_dev,b.st_ino),'copy_hardlink:'+n)
            inode_pairs={}
            for n,v in snapshots[name].items():
                if 'sha256' in v:
                    a,b=(src/n).stat(),(dst/n).stat()
                    inode_pairs[n]={'original':[a.st_dev,a.st_ino],'copy':[b.st_dev,b.st_ino]}
            (OUT/(name+'-copy-inodes.json')).write_text(json.dumps(inode_pairs,sort_keys=True)+'\n')
            # Copied launch scripts keep their old shebangs; use only new bin/python.
            # Ensure the old package uninstall RECORD cannot address dependencies.
            for n,_,_ in rows(admission_regular(dst/SITE/RECORD).read_bytes()):
                p=(dst/SITE/n).resolve()
                need(p.is_relative_to(dst.resolve()) and owned(str(p.relative_to(dst.resolve()))),'old_record_not_owned')
            cmd=[PLAN['uv'],'--no-config','pip','install','--offline','--no-index','--no-deps','--no-cache','--link-mode','copy','--reinstall-package','cryptalis','--python',str(dst/'bin/python'),str(wheel)]
            with (OUT/(name+'-install.stdout')).open('xb') as out,(OUT/(name+'-install.stderr')).open('xb') as err:
                result=subprocess.run(cmd,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ),check=False)
            need(result.returncode==0,'install_exit:'+name+':'+str(result.returncode))
            need(dependencies(inventory(dst,installed=True))==dependencies(snapshots[name]),'dependency_bytes_changed:'+name)
            report['cells'][name]=verify(dst,wheel)
            surviving={}
            current_inodes=set()
            for p in dst.rglob('*'):
                if p.is_file() and not p.is_symlink():
                    b=p.stat();current_inodes.add((b.st_dev,b.st_ino))
                    n=str(p.relative_to(dst))
                    if n in snapshots[name] and 'sha256' in snapshots[name][n]:
                        a=(src/n).stat();surviving[n]={'original':[a.st_dev,a.st_ino],'installed':[b.st_dev,b.st_ino]}
            need(not current_inodes & original_inodes,'installed_original_inode_overlap:'+name)
            need(not current_inodes & new_inodes,'installed_cells_inode_overlap:'+name)
            new_inodes.update(current_inodes)
            (OUT/(name+'-installed-inodes.json')).write_text(json.dumps(surviving,sort_keys=True)+'\n')
            report['cells'][name]['original_and_prior_new_inode_sets_disjoint']=True
            report['cells'][name]['surviving_original_new_pairs']=len(surviving)
            report['cells'][name]['command']=cmd
            report['cells'][name]['dependency_files_unchanged']=len(dependencies(snapshots[name]))
        report['status']='PASS_INSTALLED_PAYLOAD_ONLY'
    finally:
        report['original_cells_unchanged']=all(inventory(src)==snapshots[name] for name,src in originals.items())
        report['source_unchanged']=inventory(source)==source_snapshot
        if not report['original_cells_unchanged'] or not report['source_unchanged']:report['status']='FAIL_ORIGINAL_CHANGED'
        (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    need(report['status']=='PASS_INSTALLED_PAYLOAD_ONLY','failed')
if __name__=='__main__':main()
