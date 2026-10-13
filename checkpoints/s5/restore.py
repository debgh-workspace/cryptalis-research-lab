from pathlib import Path
import hashlib,json,tarfile,sys
root=Path(__file__).resolve().parents[2]
manifest=json.loads((root/'checkpoints/s5/manifest.json').read_text())
out=Path(sys.argv[1]).resolve()
if out.exists(): raise SystemExit('Choose a new nonexistent restore directory')
parts=[]
for p in manifest['parts']:
 data=(root/p['path']).read_bytes()
 assert len(data)==p['bytes'] and hashlib.sha256(data).hexdigest()==p['sha256'],p['path']
 parts.append(data)
data=b''.join(parts)
assert len(data)==manifest['archive_bytes']
assert hashlib.sha256(data).hexdigest()==manifest['archive_sha256']
out.mkdir(parents=True)
archive=out/'checkpoint.tar.xz';archive.write_bytes(data)
target=out/'restored';target.mkdir()
with tarfile.open(archive) as t:t.extractall(target,filter='data')
count=0
for line in (target/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split(maxsplit=1);f=(target/name.lstrip('*')).resolve()
 assert f.is_relative_to(target.resolve())
 assert hashlib.sha256(f.read_bytes()).hexdigest()==digest,name
 count+=1
assert count==manifest['manifest_entries']
print(f'PASS: {count} restored files verified; runtime replay still required')
