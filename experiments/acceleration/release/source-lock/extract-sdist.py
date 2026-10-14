"""Extract only the newly built, path-checked sdist for the authorized roundtrip."""
from pathlib import Path
import tarfile
HERE=Path(__file__).resolve().parent
source=HERE/'run/sdist-1/cryptalis-0.1.0.tar.gz'
target=HERE/'run/extracted'
if not target.is_dir() or any(target.iterdir()):
    raise ValueError('extraction_destination_not_empty')
with tarfile.open(source,'r:gz') as archive:
    members=archive.getmembers()
    if len(members)!=len({m.name for m in members}):
        raise ValueError('duplicate_member')
    for member in members:
        if not (member.isfile() or member.isdir()) or member.name.startswith('/') or '..' in member.name.split('/') or member.name.split('/')[0]!='cryptalis-0.1.0':
            raise ValueError('unsafe_member')
    archive.extractall(target,filter='data')
print('Fresh roundtrip extraction completed; no package import.')
