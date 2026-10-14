"""Artifact-only post-build verifier. No product imports, extraction, or subprocess."""
import base64
import csv
import hashlib
import io
import json
from pathlib import Path
import tarfile
import zipfile

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OLD = BASE/'release-lab/s20-payload-preparation-20261014/dist-1'
class Invalid(ValueError):
    pass

def need(ok, why):
    if not ok:
        raise Invalid(why)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def source_manifest(root):
    return {str(p.relative_to(root)):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts}

def listed(path):
    result={}
    for line in path.read_text().splitlines():
        digest,name=line.split('  ',1)
        name=name.removeprefix('./')
        need(name not in result,'duplicate_source_entry')
        result[name]=digest
    return result

def tar_files(path):
    with tarfile.open(path,'r:gz') as archive:
        members=archive.getmembers()
        need(len(members)==len({m.name for m in members}),'duplicate_tar_member')
        need(all(m.isfile() or m.isdir() for m in members),'tar_special_file')
        need(all(not m.name.startswith('/') and '..' not in m.name.split('/') for m in members),'tar_path')
        return {m.name:archive.extractfile(m).read() for m in members if m.isfile()}

def lock_check(files,expected):
    path='cryptalis-0.1.0/uv.lock'
    need(path in files,'missing_lock')
    need(files[path]==expected,'altered_lock')

def main():
    plan=json.loads((HERE/'build-plan.json').read_text())
    need(sha(Path(plan['uv']).read_bytes())==plan['uv_sha256'],'builder_identity')
    before=source_manifest(BASE/'candidate-accel-payload-integrated-20261014')
    after=source_manifest(HERE/'source')
    need(before==listed(HERE/'original-source.sha256'),'original_source_integrity')
    need(after==listed(HERE/'derivative-source.sha256'),'derivative_source_integrity')
    need(len(before)==len(after)==208 and set(before)==set(after),'source_inventory')
    need([n for n in before if before[n]!=after[n]]==['pyproject.toml'],'source_delta')
    old_config=(BASE/'candidate-accel-payload-integrated-20261014/pyproject.toml').read_bytes()
    new_config=(HERE/'source/pyproject.toml').read_bytes()
    need(new_config==old_config+b'\n[tool.uv.build-backend]\nsource-include = ["uv.lock"]\n','exact_config_delta')
    oldwheel=OLD/'cryptalis-0.1.0-py3-none-any.whl'
    oldsdist=OLD/'cryptalis-0.1.0.tar.gz'
    need(sha(oldwheel.read_bytes())==plan['original_wheel_sha256'],'old_wheel_hash')
    need(sha(oldsdist.read_bytes())==plan['original_sdist_sha256'],'old_sdist_hash')
    run=HERE/'run'
    archives=[run/f'sdist-{i}/cryptalis-0.1.0.tar.gz' for i in (1,2)]
    need(archives[0].read_bytes()==archives[1].read_bytes(),'sdist_reproducibility')
    files=tar_files(archives[0]); oldfiles=tar_files(oldsdist)
    lock=(HERE/'source/uv.lock').read_bytes()
    need(sha(lock)==plan['lock_sha256'],'source_lock_hash')
    lock_check(files,lock)
    need(set(files)==set(oldfiles)|{'cryptalis-0.1.0/uv.lock'},'sdist_file_set')
    allowed={'cryptalis-0.1.0/pyproject.toml','cryptalis-0.1.0/pyproject.toml.orig'}
    need({n for n in oldfiles if oldfiles[n]!=files[n]}==allowed,'sdist_changed_members')
    need(files['cryptalis-0.1.0/pyproject.toml.orig']==new_config,'sdist_original_config')
    import tomllib
    need(tomllib.loads(files['cryptalis-0.1.0/pyproject.toml'].decode())==tomllib.loads(new_config.decode()),'normalized_config')
    for name in ['direct-wheel','roundtrip-wheel']:
        path=run/name/oldwheel.name
        need(path.read_bytes()==oldwheel.read_bytes(),'wheel_byte_identity:'+name)
    with zipfile.ZipFile(oldwheel) as archive:
        names=archive.namelist()
        need(len(names)==len(set(names)),'duplicate_wheel_member')
        payload={n:archive.read(n) for n in names if not n.endswith('/')}
        modules={str(p.relative_to(HERE/'source/src')):p.read_bytes() for p in (HERE/'source/src').rglob('*.py')}
        need(len(modules)==40 and {n for n in payload if n.endswith('.py')}==set(modules),'runtime_inventory')
        for name,data in modules.items():
            need(payload[name]==data==files['cryptalis-0.1.0/src/'+name],'runtime_bytes')
        record='cryptalis-0.1.0.dist-info/RECORD'
        rows=list(csv.reader(io.StringIO(payload[record].decode())))
        need(all(len(r)==3 for r in rows),'record_shape')
        need(len(rows)==len({r[0] for r in rows}) and {r[0] for r in rows}==set(payload),'record_coverage')
        count=0
        for name,digest,size in rows:
            if name==record:
                need(digest==size=='','record_self');continue
            data=payload[name]
            need(digest=='sha256='+base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b'=').decode() and size==str(len(data)),'record_digest')
            count+=1
        need(count==44,'record_count')
        need(payload['cryptalis-0.1.0.dist-info/licenses/LICENSE']==(HERE/'source/LICENSE').read_bytes(),'license_bytes')
    controls=[]
    for name in plan['negative_controls']:
        mutant=dict(files)
        if name=='missing_lock':
            del mutant['cryptalis-0.1.0/uv.lock']
        else:
            mutant['cryptalis-0.1.0/uv.lock']=b'altered'
        try:lock_check(mutant,lock)
        except Invalid as exc:
            need(str(exc)==name,'negative_reason');controls.append({'id':name,'rejected':True})
        else:raise Invalid('negative_accepted')
    need(source_manifest(BASE/'candidate-accel-payload-integrated-20261014')==before and source_manifest(HERE/'source')==after,'after_source_integrity')
    print(json.dumps({'status':'PASS_SCOPED_PACKAGING','new_sdist_sha256':sha(archives[0].read_bytes()),'wheel_sha256':plan['original_wheel_sha256'],'runtime_modules':40,'record_hashed_entries':44,'source_files':208,'changed_source_files':['pyproject.toml'],'negative_controls':controls,'gates':{g:'UNKNOWN' for g in ['G-ADAPTER','G-CRYPTO','G-QUERY','G-LIFECYCLE','G-PROVIDER','G-POLICY','G-RELEASE']},'limits':['Source-release lock preservation only. No dependency drift resolution, platform qualification, installation or runtime replay.','Same executable/host rebuild equality only. Bundled backend source-to-binary provenance and clean-machine reproducibility unestablished.']},indent=2))

if __name__=='__main__':main()
