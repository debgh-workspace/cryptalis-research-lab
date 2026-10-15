"""HELD checked source/selection/archive gate. No live cell, corpus, DB or imports.

This helper imports only stdlib when root later executes it. Approval semantics
remain root's responsibility. No source-preparation execution is authorized.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import stat

B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
P = B/'experiments/json-transport-native-probe-v3-cost9-20261015'
M = B/'experiments/integrated221-installed-full-controls-v3-20261015'
SOURCE = B/'candidate-cluster-retained-integrated-v2-20261015'
MEMBERS = {'PROTOCOL.md', 'SELECTION-TEMPLATE.json', 'SOURCE-INPUTS.json',
           'RUNTIME-BINDING.json', 'COMMAND_ARGV.json', 'EXPECTED_CASES.txt',
           'conftest.py', 'test_native_transport.py', 'admit_packet.py', 'run-probe.sh'}
MAIN_NAMES = {'verify_runtime_binding.py', 'launch_cold_wrapper.py',
              'BINDING_SA21.json', 'BINDING_SA20.json', 'CANDIDATE_SOURCE_MANIFEST.json',
              'RUNTIME43_MANIFEST.json', 'INSTALLED_ORDINARY_PINS.json',
              'FULL_NONPRODUCT_PINS.json', 'INSTALLED_NAMESPACE.json', 'CORPUS_BASELINE.json'}
OTHER_INPUTS = {
    'candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py',
    'candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py',
    'toolchain/lab_progress.py', 'toolchain/run_baseline.py', 'repo/scripts/test_postgres.py',
    'reviewer-notes/search-cost-followon-20261015/FINDING.md',
    'reviewer-notes/search-cost-followon-20261015/FINAL_RECEIPT.json',
    'reviewer-notes/search-cost-followon-20261015/independent/REVIEW.md',
    'reviewer-notes/integrated221-installed-focused111-sa20-v2-independent-20261015/REVIEW.md',
    'experiments/json-transport-native-probe-v1-20261015/SHA256SUMS.txt',
    'reviewer-notes/json-transport-native-probe-independent-20261015/V1_HOLD.md',
    'experiments/json-transport-native-probe-v2-20261015/SHA256SUMS.txt',
    'reviewer-notes/json-transport-native-probe-independent-20261015/REVIEW.md',
}
DENIED = {'tests.json', 'readiness.json', 'package-origin.json', 'postgres-start.json',
          'postgres-stop.json', 'uv_cache.json', '__pycache__', '.pytest_cache',
          'home', '.env', 'environment', 'environment.json'}


def need(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def digest(value):
    need(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'UNRESOLVED_DIGEST')
    return value


def regular(path):
    need(path.is_absolute() and '..' not in path.parts and path.is_relative_to(B), 'UNSAFE_PATH')
    need(not any(x in DENIED for x in path.parts), 'PRIVATE_CACHE_OR_PHASE_PATH')
    need(not any(x in str(path).lower() for x in ('password', 'credential', 'secret', '.cryptalis-test')), 'PRIVATE_PATH')
    need(not path.is_relative_to(B/'release-lab') and not path.is_relative_to(B/'evidence'), 'LIVE_INPUT_FORBIDDEN')
    current = Path('/')
    for part in path.parts[1:]:
        current /= part
        mode = current.lstat().st_mode
        need(stat.S_ISREG(mode) if current == path else stat.S_ISDIR(mode), 'TYPE_OR_LINK:' + str(current))
    return path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(name):
    value = PurePosixPath(name)
    need(name and not value.is_absolute() and str(value) == name and '..' not in value.parts, 'UNSAFE_RELATIVE')
    need(not any(x in DENIED for x in value.parts), 'PRIVATE_RELATIVE')
    return value


def inventory(root):
    directories, files = set(), set()
    need(stat.S_ISDIR(root.lstat().st_mode), 'ROOT_TYPE_OR_LINK')
    for directory, dirs, names in os.walk(root, followlinks=False):
        for name in dirs:
            path = Path(directory)/name
            need(stat.S_ISDIR(path.lstat().st_mode), 'DIRECTORY_TYPE_OR_LINK')
            directories.add(str(path.relative_to(root)))
        for name in names:
            path = Path(directory)/name
            need(stat.S_ISREG(path.lstat().st_mode), 'FILE_TYPE_OR_LINK')
            files.add(str(path.relative_to(root)))
    return directories, files


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cell', choices=('sa21',), required=True)
parser.add_argument('--selection-sha256', required=True)
parser.add_argument('--packet-seal-sha256', required=True)
parser.add_argument('--mode', choices=('before', 'archive', 'after'), required=True)
a = parser.parse_args()
need(Path(__file__).absolute() == P/'admit_packet.py', 'WRONG_PACKET')
seal = regular(P/'SHA256SUMS.txt')
need(sha(seal) == digest(a.packet_seal_sha256), 'PACKET_SEAL_ANCHOR')
members = {}
for line in seal.read_text().splitlines():
    match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)', line)
    need(match is not None, 'SEAL_ROW')
    h, name = match.groups()
    need(name not in members, 'DUPLICATE_SEAL_NAME')
    members[name] = h
need(set(members) == MEMBERS, 'EXACT_PACKET_MEMBERS')
for name in members:
    regular(P/name)
for name, h in members.items():
    need(sha(P/name) == h, 'PACKET_BYTES:' + name)
allowed = MEMBERS | {'SHA256SUMS.txt', 'SELECTION_SA21.json', 'run'}
need({p.name for p in P.iterdir()} <= allowed, 'UNADMITTED_PACKET_ADDITION')
if (P/'run').exists() or (P/'run').is_symlink():
    need(stat.S_ISDIR((P/'run').lstat().st_mode), 'RUN_DIRECTORY_LINK')
    need({p.name for p in (P/'run').iterdir()} <= {'sa21'}, 'UNADMITTED_RUN')
    for path in (P/'run').iterdir():
        need(stat.S_ISDIR(path.lstat().st_mode), 'RUN_CELL_LINK')
inputs = json.loads((P/'SOURCE-INPUTS.json').read_text())
need(set(inputs) == {'kind', 'sha256'}, 'SAFE_INPUT_SCHEMA')
targets = inputs['sha256']
need(set(targets) == {str(M/n) for n in MAIN_NAMES} | {str(B/n) for n in OTHER_INPUTS}, 'EXACT_SAFE_INPUT_SET')
for name, h in targets.items():
    regular(Path(name)); digest(h)
for name, h in targets.items():
    need(sha(Path(name)) == h, 'SAFE_SOURCE_BYTES:' + name)
selection_path = regular(P/f'SELECTION_{a.cell.upper()}.json')
need(sha(selection_path) == digest(a.selection_sha256), 'SELECTION_ANCHOR')
selection = json.loads(selection_path.read_text())
need(set(selection) == {'status', 'cell', 'packet_seal_sha256', 'command_sha256',
                       'source_review', 'preceding_terminal_review',
                       'root_current_read_only_authority_confirmed', 'root_exclusive_selection',
                       'no_intervening_lab_stage'}, 'SELECTION_SCHEMA')
need(selection['status'] == 'SELECTED_BY_ROOT_AFTER_INDEPENDENT_ACCEPTANCE' and selection['cell'] == a.cell, 'HELD_OR_WRONG_CELL')
need(selection['packet_seal_sha256'] == a.packet_seal_sha256 and selection['command_sha256'] == members['COMMAND_ARGV.json'], 'SELECTED_PACKET_COMMAND')
need(all(selection[key] is True for key in ('root_current_read_only_authority_confirmed', 'root_exclusive_selection', 'no_intervening_lab_stage')), 'ROOT_AUTHORITY_AND_BOUNDARY_REQUIRED')
reviews = [selection[key] for key in ('source_review', 'preceding_terminal_review')]
for row in reviews:
    need(set(row) == {'path', 'sha256', 'root_semantic_verdict_confirmed'}, 'REVIEW_SCHEMA')
    need(row['root_semantic_verdict_confirmed'] is True, 'REVIEW_SEMANTICS_REQUIRED')
    path = Path(row['path'])
    need(path.is_relative_to(B/'reviewer-notes') and path.suffix == '.md', 'REVIEW_PATH')
    regular(path); digest(row['sha256'])
prior = selection['preceding_terminal_review']
need(prior['path'] == str(B/'reviewer-notes/json-transport-native-probe-terminal-independent-20261015/REVIEW.md'), 'V2_FAILED_RUN_TERMINAL_REQUIRED')
for row in reviews:
    need(sha(Path(row['path'])) == row['sha256'], 'REVIEW_BYTES')
commands = json.loads((P/'COMMAND_ARGV.json').read_text())
need(commands['cwd'] == str(B) and commands['shell'] is False and set(commands['stages']) == {'sa21'}, 'COMMAND_SCHEMA')
need(commands['stages'][a.cell]['expected_cases'] == 9 and commands['stages'][a.cell]['expected_phases'] == 27, 'EXACT_OUTCOME_COUNTS')
need(len((P/'EXPECTED_CASES.txt').read_text().splitlines()) == 9, 'FROZEN_CASE_COUNT')
need(commands['stages'][a.cell]['wrapper_argv'].count(str(P/'test_native_transport.py') + '::test_counterbalanced_native_cost') == 1
     and str(P/'test_native_transport.py') not in commands['stages'][a.cell]['wrapper_argv'], 'COST_ONLY_SELECTION')

if a.mode in {'archive', 'after'}:
    manifest = regular(M/'CANDIDATE_SOURCE_MANIFEST.json')
    need(sha(manifest) == '202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520', 'SOURCE221_MANIFEST')
    source = json.loads(manifest.read_text())['source_sha256']
    need(len(source) == 221, 'SOURCE221_COUNT')
    expected = {}
    for name, h in source.items():
        expected['source221/' + str(relative(name))] = (SOURCE/relative(name), digest(h))
    for name, h in members.items():
        expected['packet/' + name] = (P/name, h)
    expected['packet/SHA256SUMS.txt'] = (seal, a.packet_seal_sha256)
    expected['packet/' + selection_path.name] = (selection_path, a.selection_sha256)
    need(len(expected) == 233, 'ARCHIVE_COUNT')
    # Every expanded path is admitted before opening any expanded source payload.
    for path, h in expected.values():
        regular(path)
    expected_dirs = {str(parent) for name in expected for parent in PurePosixPath(name).parents if str(parent) != '.'}
    archive = P/'run'/a.cell/'frozen-inputs'
    if a.mode == 'archive':
        for path in [archive.parent, *archive.parent.parents]:
            need(stat.S_ISDIR(path.lstat().st_mode), 'ARCHIVE_PARENT_LINK')
        need(not archive.exists() and not archive.is_symlink(), 'EXISTING_ARCHIVE')
        payloads = {}
        for name, (path, h) in expected.items():
            data = path.read_bytes()
            need(hashlib.sha256(data).hexdigest() == h, 'SOURCE_CHANGED:' + name)
            payloads[name] = data
        archive.mkdir(mode=0o700)
        for name, data in payloads.items():
            path = archive/name
            path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(data)
    actual_dirs, actual_files = inventory(archive)
    need(actual_dirs == expected_dirs and actual_files == set(expected), 'EXACT_ARCHIVE_INVENTORY')
    for name, (_, h) in expected.items():
        need(sha(archive/name) == h, 'ARCHIVED_BYTES:' + name)
    if a.mode == 'archive':
        receipt = {'status': 'EXACT_ARCHIVE_VERIFIED', 'source221': 221, 'packet': 12,
                   'total_files': 233, 'directory_count': len(expected_dirs),
                   'packet_seal_sha256': a.packet_seal_sha256,
                   'selection_sha256': a.selection_sha256,
                   'files_sha256': {name: row[1] for name, row in sorted(expected.items())}}
        with (archive.parent/'archive-receipt.json').open('x') as stream:
            stream.write(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
print(json.dumps({'status': 'EXACT_SOURCE_SELECTION_ARCHIVE_GATE', 'cell': a.cell,
                  'mode': a.mode, 'packet_seal_sha256': a.packet_seal_sha256,
                  'selection_sha256': a.selection_sha256, 'safe_inputs': len(targets),
                  'authority': 'Recorded root selection; hashes never create permission.'}, sort_keys=True))
