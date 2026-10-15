"""Data-only launch admission; not an alternate installer entry."""
import hashlib,json,os
from pathlib import Path
HERE=Path(__file__).resolve().parent

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


def main():
    admission_all_originals()
    data=admission_data()
    for key in ('future_output','future_parent_results','future_run'):
        admission_need(not os.path.lexists(data[key]),'destination_exists:'+data[key])
    for manifest in (HERE/'outer-frozen.sha256',HERE/'frozen-inputs.sha256'):
        parsed=admitted_manifest(manifest,HERE)
        for name,expected in parsed.items():
            admission_need(hashlib.sha256(admission_regular(Path(name)).read_bytes()).hexdigest()==expected,'input_hash:'+name)
    print('PASS_METADATA_FIRST_LAUNCH_ADMISSION; no install or runtime executed by preflight')
if __name__=='__main__':main()
