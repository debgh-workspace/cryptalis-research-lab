"""HELD data-only finite archive gate; no installed/corpus/credential reads or imports.

Root must first admit this source, the packet and actual selection. Every producer,
copy and final exact inventory is checked in this one process. Partial output is
retained on failure; zero exit requires the complete byte-verified archive.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import stat

B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
P = B/'experiments/preview-smoke-installed221-binding-v2-20261015'
V5 = B/'experiments/preview-smoke-adapter-v5-installed221-20261015'
SOURCE = B/'candidate-cluster-retained-integrated-v2-20261015'
MANIFEST = B/'experiments/integrated221-installed-full-controls-v3-20261015/CANDIDATE_SOURCE_MANIFEST.json'
ARCHIVE = P/'run/frozen-inputs'
MEMBERS = {'README.md', 'RUNTIME-BINDING.json', 'COMMAND.json', 'AUTHORITY-PENDING.json',
           'SELECTION-TEMPLATE.json', 'SOURCE-INPUTS.json', 'SOURCE-DELTA.patch',
           'admit_smoke.py', 'archive_smoke.py', 'launch_cold_smoke.py', 'run-smoke.sh'}
V5_MEMBERS = {'AUTHORITY-AND-ACTIONS.md', 'CURRENT221-PYTHON.sha256', 'EXECUTION-ADMISSION.md',
              'GENERAL-ENGINEERING-AUTHORIZATION.txt', 'HELD_COMMAND_TEMPLATE.json', 'INPUTS.sha256',
              'METADATA-ADMISSION.json', 'README.md', 'SOURCE-DELTA.patch', 'SOURCE-MAP.md',
              'coordinator_driver.py', 'smoke_proposal.py', 'target_guard.py', 'test_public_preview_smoke.py'}

def need(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def digest(value):
    need(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'INVALID_DIGEST')
    return value

def relative(name):
    path = PurePosixPath(name)
    need(name and not path.is_absolute() and str(path) == name and '..' not in path.parts, 'UNSAFE_RELATIVE_NAME')
    need(not any(part in {'__pycache__', '.pytest_cache', '.env', 'home'} for part in path.parts), 'PRIVATE_OR_CACHE_NAME')
    return path

def regular(path):
    need(path.is_absolute() and '..' not in path.parts, 'UNSAFE_INPUT_PATH')
    need(path == MANIFEST or any(path.is_relative_to(root) for root in (P, V5, SOURCE)), 'OUTSIDE_FINITE_SOURCE_ROOTS')
    current = Path('/')
    for part in path.parts[1:]:
        current /= part
        mode = current.lstat().st_mode
        need(stat.S_ISREG(mode) if current == path else stat.S_ISDIR(mode), 'INPUT_TYPE_OR_LINK:' + str(current))
    return path

def sha(data):
    return hashlib.sha256(data).hexdigest()

def sealed_members(path, expected, names):
    data = regular(path).read_bytes()
    need(sha(data) == digest(expected), 'SEAL_ANCHOR')
    result = {}
    for line in data.decode().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)', line)
        need(match is not None, 'SEAL_ROW')
        h, name = match.groups()
        need(name not in result, 'DUPLICATE_SEAL_NAME')
        result[name] = h
    need(set(result) == names, 'EXACT_SEAL_MEMBERS')
    return result

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--selection-sha256', required=True)
parser.add_argument('--packet-seal-sha256', required=True)
a = parser.parse_args()
need(Path(__file__).absolute() == P/'archive_smoke.py', 'WRONG_PACKET')
packet = sealed_members(P/'SHA256SUMS.txt', a.packet_seal_sha256, MEMBERS)
v5 = sealed_members(V5/'SHA256SUMS.txt', 'b3615d28e04bb6613807050059674eb1a3b0f8aabc51092ac643f54a49b7f79c', V5_MEMBERS)
manifest_data = regular(MANIFEST).read_bytes()
need(sha(manifest_data) == '202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520', 'SOURCE221_MANIFEST_ANCHOR')
source = json.loads(manifest_data)['source_sha256']
need(len(source) == 221, 'SOURCE221_COUNT')
selection_data = regular(P/'SELECTION.json').read_bytes()
need(sha(selection_data) == digest(a.selection_sha256), 'SELECTION_ANCHOR')
selection = json.loads(selection_data)
expected = {}

def add(group, name, path, expected_sha):
    target = group + '/' + str(relative(name))
    need(target not in expected, 'DUPLICATE_ARCHIVE_TARGET')
    expected[target] = (path, digest(expected_sha))

for name, h in source.items():
    add('source221', name, SOURCE/relative(name), h)
for group, root, entries in (('smoke-packet', P, packet), ('v5-packet', V5, v5)):
    for name, h in entries.items():
        add(group, name, root/name, h)
add('smoke-packet', 'SHA256SUMS.txt', P/'SHA256SUMS.txt', a.packet_seal_sha256)
add('smoke-packet', 'SELECTION.json', P/'SELECTION.json', a.selection_sha256)
add('v5-packet', 'SHA256SUMS.txt', V5/'SHA256SUMS.txt', 'b3615d28e04bb6613807050059674eb1a3b0f8aabc51092ac643f54a49b7f79c')
for role, name in (('fixture_acl_approval', 'fixture-acl-approval.txt'), ('role_and_helper_provenance', 'role-and-helper-provenance.txt')):
    record = selection[role]
    path = P/'selection-support'/name
    need(record['path'] == str(path), 'SUPPORT_PATH')
    add('selection-support', name, path, record['sha256'])
counts = {group: sum(name.startswith(group + '/') for name in expected)
          for group in ('source221', 'smoke-packet', 'v5-packet', 'selection-support')}
need(counts == {'source221': 221, 'smoke-packet': len(MEMBERS) + 2, 'v5-packet': 15, 'selection-support': 2}, 'ARCHIVE_SCOPE_COUNTS')
need(len(expected) == 221 + len(MEMBERS) + 2 + 15 + 2, 'ARCHIVE_TOTAL')
# Admit every source path/type before reading any expanded payload. Inputs are
# exact source/selection files, never installed cells, primary corpus or caches.
for path, h in expected.values():
    regular(path)
payloads = {}
for name, (path, h) in expected.items():
    data = path.read_bytes()
    need(sha(data) == h, 'SOURCE_BYTES_CHANGED:' + name)
    payloads[name] = data
for path in [ARCHIVE.parent, *ARCHIVE.parent.parents]:
    need(stat.S_ISDIR(path.lstat().st_mode), 'ARCHIVE_PARENT_TYPE_OR_LINK')
need(not ARCHIVE.exists() and not ARCHIVE.is_symlink(), 'EXISTING_ARCHIVE')
ARCHIVE.mkdir(mode=0o700)
for name, data in payloads.items():
    target = ARCHIVE/name
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(data)
expected_dirs = {str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent) != '.'}
actual_dirs = set()
actual_files = set()
need(stat.S_ISDIR(ARCHIVE.lstat().st_mode), 'ARCHIVE_ROOT_TYPE_OR_LINK')
for directory, dirs, files in os.walk(ARCHIVE, followlinks=False):
    for name in dirs:
        path = Path(directory)/name
        need(stat.S_ISDIR(path.lstat().st_mode), 'ARCHIVE_DIRECTORY_TYPE_OR_LINK')
        actual_dirs.add(str(path.relative_to(ARCHIVE)))
    for name in files:
        path = Path(directory)/name
        need(stat.S_ISREG(path.lstat().st_mode), 'ARCHIVE_FILE_TYPE_OR_LINK')
        actual_files.add(str(path.relative_to(ARCHIVE)))
need(actual_dirs == expected_dirs and actual_files == set(expected), 'EXACT_ARCHIVE_INVENTORY')
for name, (_, h) in expected.items():
    need(sha((ARCHIVE/name).read_bytes()) == h, 'ARCHIVED_BYTES_CHANGED:' + name)
receipt = {'status': 'EXACT_ARCHIVE_VERIFIED', 'counts': counts, 'total_files': len(expected),
           'directory_count': len(expected_dirs), 'packet_seal_sha256': a.packet_seal_sha256,
           'selection_sha256': a.selection_sha256,
           'files_sha256': {name: row[1] for name, row in sorted(expected.items())}}
with (P/'run/archive-receipt.json').open('x', encoding='utf8') as stream:
    stream.write(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
print(json.dumps({key: value for key, value in receipt.items() if key != 'files_sha256'}, sort_keys=True))
