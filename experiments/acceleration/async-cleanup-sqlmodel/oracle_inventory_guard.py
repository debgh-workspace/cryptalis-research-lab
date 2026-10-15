"""Data-only coordinator guard. Does not import or execute reviewed project/oracle code."""
from pathlib import Path
import argparse
import hashlib
import json
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--phase', choices=('before', 'after'), required=True)
args = parser.parse_args()
B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
P = B / 'experiments/async-cleanup-sqlmodel-overlay-plan-20261014'
O = P / 'oracle'
ANCHOR = 'f3fddd013c20ebe244df3358170a5573c1563abc97dfe05b594750a7696ea096'
OVERLAY_MANIFEST_SHA256 = 'ed7b95572c47f41f454007eaaa84a6207ef4ec064873869cb99a952352c061d9'
EXPECTED = {
    'oracle/cleanup_sqlmodel_oracle_support.py': 'f4acfe05fbd16ae254b120de6fa0198d36419375630c7caff932ec30ead33b18',
    'oracle/conftest.py': 'fa521d4bec6b84320304ad59d22e7551c342d7e60f2c254c8b6495b07bdf06dd',
    'oracle/test_async_sqlmodel_public_hook.py': '25529e24e5190895f76a19a94520cc15ad03d82ef3f7cc423a3c57226655d49e',
}
assert P.is_dir() and P.resolve(strict=True) == P and not P.is_symlink()
assert O.is_dir() and O.resolve(strict=True) == O and not O.is_symlink()

def read_regular(path):
    assert path.is_file() and not path.is_symlink() and path.resolve(strict=True) == path, path
    return path.read_bytes()

def digest(path):
    return hashlib.sha256(read_regular(path)).hexdigest()

assert digest(P / 'PACKET.sha256') == ANCHOR, 'Frozen packet anchor changed'
assert digest(P / 'OVERLAY_SOURCE_MANIFEST.json') == OVERLAY_MANIFEST_SHA256, 'Overlay manifest changed'
assert json.loads(read_regular(P / 'OVERLAY_SOURCE_MANIFEST.json')) == EXPECTED
members = list(O.rglob('*'))
source_paths = set()
cache_names = []
for path in members:
    assert not path.is_symlink() and path.resolve(strict=True) == path, path
    relative = path.relative_to(O)
    if path.is_dir():
        assert args.phase == 'after' and relative == Path('__pycache__'), path
        continue
    assert path.is_file(), path
    if str(path.relative_to(P)) in EXPECTED:
        source_paths.add(str(path.relative_to(P)))
        continue
    assert args.phase == 'after' and relative.parent == Path('__pycache__'), path
    assert re.fullmatch(r'(?:cleanup_sqlmodel_oracle_support|conftest|test_async_sqlmodel_public_hook)\.cpython-314(?:-pytest-[A-Za-z0-9_.+-]+)?\.pyc', relative.name), path
    cache_names.append(str(relative))
assert source_paths == set(EXPECTED), source_paths
assert all(digest(P / relative) == expected for relative, expected in EXPECTED.items()), 'Oracle source hash changed'
print(json.dumps({'phase': args.phase, 'status': 'EXACT_THREE_SOURCE_FILES_VERIFIED',
                  'packet_sha256': ANCHOR, 'source_sha256': EXPECTED,
                  'cache_filenames_only_not_read': sorted(cache_names)}, sort_keys=True))
