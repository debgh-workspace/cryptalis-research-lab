"""HELD source-only outer entry. Execute only after root's separate selection.

Imports are stdlib only. Native packet, installed guard and wrapper are unchanged.
No new product algorithm, SQL, role, credential route or cluster is introduced.
"""
from pathlib import Path, PurePosixPath
import argparse
import collections
import hashlib
import json
import os
import re
import stat
import subprocess
import time
import xml.etree.ElementTree as ET

B = Path('/workspace/scratch/cb28ee9f5f4a/cryptalis-executable')
P = B/'experiments/abort-envelope-native-entry-v1-20261015'
N = B/'experiments/abort-envelope-native-probe-v1-20261015'
M = B/'experiments/integrated221-installed-full-controls-v3-20261015'
S = B/'candidate-cluster-retained-integrated-v2-20261015'
A = P/'run/sa21'
E = B/'evidence/abort-envelope-native-probe-v1-sa21-20261015'
COORD = str(B/'repo/.venv/bin/python')
INSTALLED = str(B/'release-lab/integrated221-installed-20261015/sa21/bin/python')
ENV = {'HOME': str(B/'runtime/home'), 'PATH': str(B/'toolchain/pg16/bin')+':/usr/bin:/bin',
       'LANG': 'C.UTF-8', 'TZ': 'UTC'}
NATIVE_SEAL = '0c005d33fd00630e7b3ef986e2bbcae3e4c6cafe65b4b996b52ad514304424e5'
SOURCE_SEAL = '202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520'
BINDING = '669cb3c408144f597cc70de5d8c23295e26ba47f9c68888b1d986e431171cf54'
PREVIOUS = 'experiments/json-transport-native-probe-v3-cost9-20261015'
PREVIOUS_SEAL = 'c78b6d211664a9e451c0b5913cfeb4c53954e9f086943e8758c4d16c32c324ff'
ENTRY_NAMES = {'entry.py', 'run-entry.sh', 'README.md', 'COMMAND_ARGV.json', 'SELECTION-TEMPLATE.json'}
NATIVE_NAMES = {'COMMAND_ARGV.json', 'EXPECTED_CASES.txt', 'PREDECESSOR_BINDING.json',
                'PROTOCOL.md', 'SOURCE_INPUTS.json', 'conftest.py', 'test_native_envelope.py'}
PINS = {
    str(M/'verify_runtime_binding.py'): 'c84e168fd2f9dc5a5e8af943ea52d868f495b542ae00c2e9da47c470d391c861',
    str(M/'launch_cold_wrapper.py'): 'fe7eb1d38cf826c79ecf201a330522f96501d4edc4d40b2f56f779df24f2acbc',
    str(M/'BINDING_SA21.json'): BINDING,
    str(M/'CANDIDATE_SOURCE_MANIFEST.json'): SOURCE_SEAL,
    str(B/'candidate-corpus-wrapper-v2-20261014/lab_session_corpus_v2.py'): 'e5201530c7816a63e606b26352417daff6ca71aedeeccb7b569cea0edb309453',
    str(B/'candidate-corpus-wrapper-v2-20261014/corpus_artifacts_v2.py'): '4c0429a182b5b7a2f7e561892936dba89ed279583bff181b18238f50485de86f',
    str(B/'toolchain/lab_progress.py'): '673e3d41398f6be36876008f80110b313ad86553363052c8f14a25e1c47b93c1',
    str(B/'toolchain/run_baseline.py'): 'a88c24fa1699ce42a091c9d2da1168ba453d4548a811d542316fe95cb833d00f',
    str(B/'repo/scripts/test_postgres.py'): '118952d57d777d692adf1f1447fedbb612030fd3266c9374680d347bb501fd12',
    str(B/PREVIOUS/'SHA256SUMS.txt'): PREVIOUS_SEAL,
}
WRAPPER = [COORD, '-B', str(M/'launch_cold_wrapper.py'), '--candidate-root', str(S),
           '--installed-candidate', '--python', INSTALLED, '--evidence', str(E), '--',
           '-q', '-c', str(S/'pyproject.toml'), str(N/'test_native_envelope.py'),
           '--confcutdir='+str(N), '-p', 'no:cacheprovider', '--tb=short', '-x']
DENIED = {'__pycache__', '.pytest_cache', '.env', 'environment', 'environment.json',
          'tests.json', 'readiness.json', 'package-origin.json', 'postgres-start.json',
          'postgres-stop.json', 'uv_cache.json', 'home'}


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def hexhash(value):
    need(type(value) is str and re.fullmatch('[0-9a-f]{64}', value), 'UNRESOLVED_DIGEST')
    return value


def regular(path, limit=4*1024*1024):
    need(path.is_absolute() and '..' not in path.parts and path.is_relative_to(B), 'PATH_BOUNDARY')
    need(not any(x in DENIED for x in path.parts), 'PRIVATE_OR_PHASE_PATH')
    need(not any(x in str(path).lower() for x in ('password', 'credential', 'secret', '.cryptalis-test')), 'PRIVATE_PATH')
    current = Path('/')
    for part in path.parts[1:]:
        current /= part
        mode = current.lstat().st_mode
        need(stat.S_ISREG(mode) if current == path else stat.S_ISDIR(mode), 'TYPE_OR_SYMLINK')
    need(path.stat().st_size <= limit, 'FINITE_FILE_BOUND')
    return path


def data(path, limit=4*1024*1024):
    regular(path, limit)
    with path.open('rb') as stream:
        value = stream.read(limit+1)
    need(len(value) <= limit, 'FINITE_READ_BOUND')
    return value


def sha(value):
    return hashlib.sha256(value).hexdigest()


def document(path):
    def unique(items):
        result = {}
        for key, value in items:
            need(key not in result, 'DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    return json.loads(data(path), object_pairs_hook=unique)


def sealed(directory, expected, names):
    seal = data(directory/'SHA256SUMS.txt', 8192)
    need(sha(seal) == hexhash(expected), 'SEAL_ANCHOR')
    rows = {}
    for line in seal.decode('ascii').splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)', line)
        need(match is not None, 'SEAL_ROW')
        digest, name = match.groups()
        need(name not in rows, 'DUPLICATE_SEAL_ROW')
        rows[name] = digest
    need(set(rows) == names, 'EXACT_SEAL_MEMBERS')
    for name, digest in rows.items():
        need(sha(data(directory/name)) == digest, 'SEALED_SOURCE_DRIFT:'+name)
    return rows


def save(path, value):
    with path.open('xb') as stream:
        stream.write(value)


def receipt(name, value):
    save(A/name, (json.dumps(value, sort_keys=True, indent=2)+'\n').encode())


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--selection-sha256', required=True)
parser.add_argument('--entry-seal-sha256', required=True)
args = parser.parse_args()
need(Path(__file__).absolute() == P/'entry.py', 'ENTRY_LOCATION')
entry = sealed(P, args.entry_seal_sha256, ENTRY_NAMES)
native = sealed(N, NATIVE_SEAL, NATIVE_NAMES)
need({p.name for p in N.iterdir()} == NATIVE_NAMES | {'SHA256SUMS.txt'}, 'NATIVE_ADDITION')
need({p.name for p in P.iterdir()} == ENTRY_NAMES | {'SHA256SUMS.txt', 'SELECTION_SA21.json'}, 'ENTRY_NOT_FRESH')
selection_bytes = data(P/'SELECTION_SA21.json', 32768)
need(sha(selection_bytes) == hexhash(args.selection_sha256), 'SELECTION_ANCHOR')
selection = document(P/'SELECTION_SA21.json')
need(set(selection) == {'status', 'cell', 'entry_seal_sha256', 'native_seal_sha256',
     'command_sha256', 'native_source_review', 'entry_source_review', 'preceding_terminal_review',
     'root_current_read_only_authority_confirmed', 'root_exclusive_selection', 'no_intervening_lab_stage'}, 'SELECTION_SCHEMA')
need(selection['status'] == 'SELECTED_BY_ROOT_AFTER_INDEPENDENT_ACCEPTANCE' and selection['cell'] == 'sa21', 'HELD_SELECTION')
need(selection['entry_seal_sha256'] == args.entry_seal_sha256 and selection['native_seal_sha256'] == NATIVE_SEAL
     and selection['command_sha256'] == entry['COMMAND_ARGV.json'], 'SELECTED_IDENTITIES')
need(all(selection[k] is True for k in ('root_current_read_only_authority_confirmed', 'root_exclusive_selection', 'no_intervening_lab_stage')), 'ROOT_AUTHORITY_BOUNDARY')
reviews = {}
for key in ('native_source_review', 'entry_source_review', 'preceding_terminal_review'):
    row = selection[key]
    expected_keys = {'path', 'sha256', 'root_semantic_verdict_confirmed'}
    if key == 'preceding_terminal_review':
        expected_keys |= {'source_packet', 'source_packet_seal_sha256', 'closed_outcome'}
    need(set(row) == expected_keys and row['root_semantic_verdict_confirmed'] is True, 'REVIEW_NOT_ACCEPTED')
    path = Path(row['path'])
    need(path.is_relative_to(B/'reviewer-notes') and path.suffix == '.md', 'REVIEW_PATH')
    need(sha(data(path, 128*1024)) == hexhash(row['sha256']), 'REVIEW_DIGEST')
    reviews[key] = (path, row['sha256'])
prior = selection['preceding_terminal_review']
need(prior['source_packet'] == PREVIOUS and prior['source_packet_seal_sha256'] == PREVIOUS_SEAL
     and prior['closed_outcome'] in ('CLOSED_PASS', 'CLOSED_FAILURE'), 'LATEST_COST9_CLOSED_BOUNDARY_REQUIRED')
need(reviews['native_source_review'] == (B/'reviewer-notes/abort-envelope-native-probe-source-independent-20261015/REVIEW.md',
     '17d39a9c6bb9b3b4ca1c913d64ddfe6e3f9a5043a4461d88e139498309922159'), 'ACCEPTED_NATIVE_REVIEW_REQUIRED')
for path, digest in PINS.items():
    need(sha(data(Path(path))) == digest, 'REUSED_SOURCE_DRIFT')
commands = document(P/'COMMAND_ARGV.json')
need(commands['wrapper_argv'] == WRAPPER and commands['environment'] == ENV and commands['cwd'] == str(B)
     and commands['shell'] is False, 'FIXED_COMMAND_REQUIRED')
expected_ids = data(N/'EXPECTED_CASES.txt', 16384).decode('ascii').splitlines()
need(len(expected_ids) == len(set(expected_ids)) == 31 and all(x.startswith('::test_') for x in expected_ids), 'EXACT_IDS')
need(not E.exists() and not E.is_symlink(), 'EVIDENCE_NOT_FRESH')

# Complete finite source archive is checked before any installed/corpus/status/DB work.
source = document(M/'CANDIDATE_SOURCE_MANIFEST.json')['source_sha256']
need(type(source) is dict and len(source) == 221, 'SOURCE221_COUNT')
archive_inputs = {}
for name, digest in source.items():
    relative = PurePosixPath(name)
    need(name and str(relative) == name and not relative.is_absolute() and '..' not in relative.parts, 'SOURCE_RELATIVE_PATH')
    archive_inputs['source221/'+name] = (S/name, hexhash(digest))
for directory, prefix, members, seal in ((P, 'entry', entry, args.entry_seal_sha256), (N, 'native', native, NATIVE_SEAL)):
    for name, digest in members.items():
        archive_inputs[prefix+'/'+name] = (directory/name, digest)
    archive_inputs[prefix+'/SHA256SUMS.txt'] = (directory/'SHA256SUMS.txt', seal)
archive_inputs['entry/SELECTION_SA21.json'] = (P/'SELECTION_SA21.json', args.selection_sha256)
for path, digest in PINS.items():
    archive_inputs['inputs/'+str(Path(path).relative_to(B))] = (Path(path), digest)
for key, (path, digest) in reviews.items():
    archive_inputs['reviews/'+key+'.md'] = (path, digest)
need(len(archive_inputs) == 249, 'ARCHIVE_EXACT_COUNT')
for path, _ in archive_inputs.values():
    regular(path)
payloads = {}
total = 0
for name, (path, digest) in archive_inputs.items():
    value = data(path)
    need(sha(value) == digest, 'ARCHIVE_SOURCE_DRIFT:'+name)
    total += len(value)
    need(total <= 64*1024*1024, 'FINITE_ARCHIVE_TOTAL')
    payloads[name] = value
os.umask(0o077)
(P/'run').mkdir(mode=0o700)
A.mkdir(mode=0o700)
archive = A/'frozen-inputs'
archive.mkdir(mode=0o700)
for name, value in payloads.items():
    target = archive/name
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    save(target, value)
del payloads


def verify_archive():
    files, directories = set(), set()
    for directory, dirs, names in os.walk(archive, followlinks=False):
        for name in dirs:
            path = Path(directory)/name
            need(stat.S_ISDIR(path.lstat().st_mode), 'ARCHIVE_DIRECTORY_LINK')
            directories.add(str(path.relative_to(archive)))
        for name in names:
            path = Path(directory)/name
            regular(path)
            files.add(str(path.relative_to(archive)))
    expected_directories = {str(parent) for name in archive_inputs for parent in PurePosixPath(name).parents if str(parent) != '.'}
    need(files == set(archive_inputs) and directories == expected_directories, 'ARCHIVE_EXACT_INVENTORY')
    for name, (original, digest) in archive_inputs.items():
        need(sha(data(archive/name)) == digest and sha(data(original)) == digest, 'ARCHIVE_OR_SOURCE_DRIFT')


verify_archive()
receipt('archive-receipt.json', {'status': 'EXACT_ARCHIVE_VERIFIED', 'files': 249, 'source221': 221,
    'bytes': total, 'entry_seal_sha256': args.entry_seal_sha256, 'native_seal_sha256': NATIVE_SEAL,
    'selection_sha256': args.selection_sha256, 'files_sha256': {k: v[1] for k, v in sorted(archive_inputs.items())}})


def run(label, argv):
    with (A/(label+'.log')).open('xb') as output:
        result = subprocess.run(argv, cwd=B, env=ENV, stdout=output, stderr=subprocess.STDOUT)
        code = result.returncode
    save(A/(label+'-exit.txt'), (str(code)+'\n').encode())
    return code


def runtime(mode):
    need(sha(data(M/'verify_runtime_binding.py')) == PINS[str(M/'verify_runtime_binding.py')], 'GUARD_DRIFT')
    return run('runtime-'+mode, [COORD, '-I', '-B', str(M/'verify_runtime_binding.py'),
               '--stage', 'sa21', '--binding-sha256', BINDING, '--mode', mode])


STATUS = [str(B/'toolchain/pg16/bin/pg_ctl'), '-D', str(B/'runtime/data'), 'status']
need(runtime('before') == 0, 'RUNTIME_BEFORE_FAILED')
need(run('pre-status', STATUS) == 3, 'PRE_STATUS_NOT_STOPPED')
need(not E.exists() and not E.is_symlink(), 'EVIDENCE_RACE')


def wrapper():
    # Existing tests=600s/control=90s timeouts bound subprocess work. No new
    # parent timer can interrupt the unchanged stop/corpus-restoration finally.
    started = time.monotonic()
    with (A/'wrapper.log').open('xb') as output:
        child = subprocess.Popen(WRAPPER, cwd=B, env=ENV, stdout=output, stderr=subprocess.STDOUT)
        pid, status, usage = os.wait4(child.pid, 0)
        need(pid == child.pid, 'WAITED_CHILD_IDENTITY')
        child.returncode = os.waitstatus_to_exitcode(status)
    code = child.returncode
    save(A/'wrapper-exit.txt', (str(code)+'\n').encode())
    receipt('wrapper-resources.json', {'wall_seconds': time.monotonic()-started,
        'user_cpu_seconds': usage.ru_utime, 'system_cpu_seconds': usage.ru_stime,
        'linux_wait4_peak_rss_kib': usage.ru_maxrss, 'child_exit': child.returncode,
        'entry_wrapper_exit': code, 'inherited_tests_timeout_seconds': 600,
        'inherited_control_phase_timeout_seconds': 90, 'new_parent_deadline': None,
        'measurement_scope': 'wait4 wrapper plus descendants reaped by wrapper; no new CPU/AS/RSS cap'})
    return code


wrapper_code = None
closure = {}
try:
    wrapper_code = wrapper()
finally:
    # Independent post-gates are all attempted even after a failure or timeout.
    for name, action in (('post_status', lambda: run('post-status', STATUS)),
                         ('source_after', verify_archive), ('runtime_after', lambda: runtime('after'))):
        try:
            value = action()
            closure[name] = 0 if value is None else value
        except Exception as error:
            closure[name] = 'FAILED:'+type(error).__name__
    receipt('closure.json', {'wrapper_exit': wrapper_code, **closure,
        'terminal_acceptance': 'PENDING_INDEPENDENT_REVIEW'})
need(wrapper_code == 0 and closure == {'post_status': 3, 'source_after': 0, 'runtime_after': 0}, 'RUN_OR_CLOSURE_FAILED')

# Bounded safe emitted artifacts only. Never open raw phase JSON/environment data.
events = [json.loads(line) for line in data(E/'progress.jsonl', 512*1024).splitlines()]
expected = []
for nodeid in expected_ids:
    expected.append(('start', nodeid, None, None))
    expected.extend(('report', nodeid, when, 'passed') for when in ('setup', 'call', 'teardown'))
observed = [(e.get('event'), e.get('nodeid'), e.get('when'), e.get('outcome')) for e in events]
need(observed == expected, 'EXACT_ORDERED_31_IDS_93_PASSED_PHASES_REQUIRED')
junit = ET.fromstring(data(E/'junit.xml', 512*1024))
suites = list(junit.iter('testsuite'))
need(sum(int(s.get('tests', '0')) for s in suites) == 31
     and all(int(s.get(k, '0')) == 0 for s in suites for k in ('errors', 'failures', 'skipped')),
     'JUNIT_EXACT_COUNTS')
lines = data(E/'envelope-observations.jsonl', 221*8192).splitlines(keepends=True)
need(len(lines) == 221 and all(len(line) <= 8192 and line.endswith(b'\n') for line in lines), 'EXACT_BOUNDED_OBSERVATION_COUNT')
records = [json.loads(line) for line in lines]
need(collections.Counter(r.get('kind') for r in records) == {'connection': 31, 'state': 184, 'domain': 2, 'rejection': 3, 'omission': 1}, 'EXACT_OBSERVATION_KINDS')
need(all(r['status'] == 'OBSERVED_BEFORE_ASSERTIONS' for r in records if r['kind'] == 'state'), 'OBSERVATION_STATUS')
need([r['killed'] for r in records if r['kind'] == 'omission'] == [['verification', 'cursor', 'counters']], 'EXACT_OMISSION_DETECTIONS')
receipt('accounting.json', {'status': 'MECHANICAL_ACCOUNTING_COMPLETE_PENDING_INDEPENDENT_AUDIT',
    'cases': 31, 'passed_phases': 93, 'observation_records': 221, 'state_observations': 184,
    'source_derived_explicit_SELECT_count': 404, 'SELECT_count_is_runtime_trace': False,
    'native_packet_sha256': NATIVE_SEAL, 'expected_ids': expected_ids})
print('Mechanical accounting complete; independent terminal acceptance remains required.')
