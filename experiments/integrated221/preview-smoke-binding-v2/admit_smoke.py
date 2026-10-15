"""Unexecuted finite source/selection admission; never opens installed cells or corpus.

Approval semantics must be independently checked by root. Recorded statements
and hashes cannot create approval. The separate unchanged runtime verifier owns
live namespace/source/dependency/corpus validation after exclusive selection.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import stat

W = Path('/workspace/scratch/cb28ee9f5f4a')
B = W/'cryptalis-executable'
P = B/'experiments/preview-smoke-installed221-binding-v2-20261015'
V5 = B/'experiments/preview-smoke-adapter-v5-installed221-20261015'
MEMBERS = {
    'README.md', 'RUNTIME-BINDING.json', 'COMMAND.json', 'AUTHORITY-PENDING.json',
    'SELECTION-TEMPLATE.json', 'SOURCE-INPUTS.json', 'SOURCE-DELTA.patch',
    'admit_smoke.py', 'archive_smoke.py', 'launch_cold_smoke.py', 'run-smoke.sh',
}
REQUEST = 'Sentinel_d4be0bfc407881d19ce0ef871aa5304d'
DENIED = {'tests.json', 'readiness.json', 'package-origin.json', 'postgres-start.json',
          'postgres-stop.json', 'uv_cache.json', '__pycache__', '.pytest_cache',
          'home', '.env', 'environment', 'environment.json'}

def need(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def regular(path):
    need(path.is_absolute() and '..' not in path.parts and path.is_relative_to(B), 'NONCANONICAL_SAFE_PATH')
    need(not any(x in DENIED for x in path.parts), 'PRIVATE_OR_CACHE_PATH')
    need(not any(x in str(path).lower() for x in ('password', 'credential', 'secret', '.cryptalis-test')), 'PRIVATE_PATH')
    current = Path('/')
    for part in path.parts[1:]:
        current /= part
        mode = current.lstat().st_mode
        need(stat.S_ISREG(mode) if current == path else stat.S_ISDIR(mode), 'PATH_TYPE_OR_LINK:' + str(current))
    return path

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def digest(value):
    need(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'UNRESOLVED_DIGEST')
    return value

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--selection-sha256', required=True)
parser.add_argument('--packet-seal-sha256', required=True)
parser.add_argument('--mode', choices=('before', 'after'), required=True)
a = parser.parse_args()
need(Path(__file__).absolute() == P/'admit_smoke.py', 'WRONG_PACKET')
seal = regular(P/'SHA256SUMS.txt')
need(sha(seal) == digest(a.packet_seal_sha256), 'PACKET_SEAL_ANCHOR')
members = {}
for line in seal.read_text().splitlines():
    match = re.fullmatch(r'([0-9a-f]{64})  ([A-Za-z0-9_.-]+)', line)
    need(match is not None, 'SEAL_ROW')
    h, name = match.groups()
    need(name not in members, 'SEAL_DUPLICATE')
    members[name] = h
need(set(members) == MEMBERS, 'EXACT_PACKET_MEMBERS')
for name in members:
    regular(P/name)
for name, expected in members.items():
    need(sha(P/name) == expected, 'PACKET_MEMBER_CHANGED:' + name)
allowed_additions = {'SELECTION.json', 'selection-support', 'run', 'SHA256SUMS.txt'}
need({p.name for p in P.iterdir()} <= MEMBERS | allowed_additions, 'UNADMITTED_PACKET_ADDITION')
for name in ('selection-support', 'run'):
    path = P/name
    if path.exists() or path.is_symlink():
        need(stat.S_ISDIR(path.lstat().st_mode), 'LINKED_OUTPUT_DIRECTORY')
inputs = json.loads((P/'SOURCE-INPUTS.json').read_text())
need(set(inputs) == {'kind', 'sha256'}, 'INPUT_MAP_SCHEMA')
targets = inputs['sha256']
need(isinstance(targets, dict) and bool(targets), 'EMPTY_INPUTS')
# The external map is immutable under the packet seal. It contains only finite
# source/review/manifest/accepted identity files, never expanded cell or corpus names.
for name, expected in targets.items():
    path = regular(Path(name))
    need(not path.is_relative_to(B/'release-lab'), 'LIVE_CELL_INPUT_FORBIDDEN')
    need(not path.is_relative_to(B/'evidence') or path == B/'evidence/preview-identity-capture-v3-sa21-20261015/safe-identity.json', 'CORPUS_OR_PHASE_INPUT_FORBIDDEN')
    digest(expected)
for name, expected in targets.items():
    need(sha(Path(name)) == expected, 'SAFE_SOURCE_CHANGED:' + name)
need({p.name for p in V5.iterdir()} == {Path(p).name for p in targets if Path(p).parent == V5}, 'EXACT_V5_DIRECTORY')
selection_path = regular(P/'SELECTION.json')
need(sha(selection_path) == digest(a.selection_sha256), 'SELECTION_ANCHOR')
selection = json.loads(selection_path.read_text())
need(set(selection) == {'status', 'packet_seal_sha256', 'command_sha256', 'source_review', 'fixture_acl_approval', 'role_and_helper_provenance', 'preceding_terminal_review', 'root_exclusive_selection'}, 'SELECTION_SCHEMA')
need(selection['status'] == 'SELECTED_BY_ROOT_AFTER_EXPLICIT_APPROVAL', 'NOT_SELECTED')
need(selection['packet_seal_sha256'] == a.packet_seal_sha256, 'WRONG_SELECTED_PACKET')
need(selection['command_sha256'] == members['COMMAND.json'], 'WRONG_SELECTED_COMMAND')
need(selection['root_exclusive_selection'] is True, 'ROOT_SELECTION_REQUIRED')
acl = selection['fixture_acl_approval']
need(set(acl) == {'request_message_id', 'approval_message_id', 'status', 'path', 'sha256', 'root_scope_confirmed'}, 'ACL_SCHEMA')
need(acl['request_message_id'] == REQUEST and acl['status'] == 'EXPLICITLY_APPROVED', 'PENDING_FIXTURE_ACL')
need(isinstance(acl['approval_message_id'], str) and bool(acl['approval_message_id']) and acl['approval_message_id'] != REQUEST, 'ACTUAL_APPROVAL_MESSAGE_REQUIRED')
need(acl['root_scope_confirmed'] is True, 'FIXTURE_SCOPE_NOT_RECONCILED')
need(acl['path'] == str(P/'selection-support/fixture-acl-approval.txt'), 'ACL_EVIDENCE_PATH')
provenance = selection['role_and_helper_provenance']
need(set(provenance) == {'path', 'sha256', 'root_scope_confirmed'}, 'PROVENANCE_SCHEMA')
need(provenance['root_scope_confirmed'] is True and provenance['path'] == str(P/'selection-support/role-and-helper-provenance.txt'), 'ROLE_HELPER_SCOPE_REQUIRED')
for role in ('source_review', 'preceding_terminal_review'):
    record = selection[role]
    need(set(record) == {'path', 'sha256', 'root_semantic_verdict_confirmed'}, 'REVIEW_SCHEMA')
    need(record['root_semantic_verdict_confirmed'] is True, 'REVIEW_NOT_ACCEPTED:' + role)
    path = Path(record['path'])
    need(path.is_relative_to(B/'reviewer-notes') and path.suffix == '.md', 'REVIEW_PATH')
need(selection['preceding_terminal_review']['path'] == str(B/'reviewer-notes/integrated221-installed-focused111-sa20-v2-independent-20261015/REVIEW.md')
     and selection['preceding_terminal_review']['sha256'] == '7318b0b3f7bac950a8e2311dd6d546d6c5f5b376c168d9eec0e0f4c4d97d7678', 'CURRENT_TERMINAL_PREREQUISITE')
records = [selection[x] for x in ('source_review', 'fixture_acl_approval', 'role_and_helper_provenance', 'preceding_terminal_review')]
for record in records:
    regular(Path(record['path']))
    digest(record['sha256'])
for record in records:
    need(sha(Path(record['path'])) == record['sha256'], 'SELECTION_EVIDENCE_CHANGED')
need({p.name for p in (P/'selection-support').iterdir()} == {'fixture-acl-approval.txt', 'role-and-helper-provenance.txt'}, 'SELECTION_SUPPORT_SET')
print(json.dumps({'status': 'SOURCE_AND_RECORDED_SELECTION_BOUND', 'mode': a.mode,
                  'packet_seal_sha256': a.packet_seal_sha256,
                  'selection_sha256': a.selection_sha256, 'safe_input_count': len(targets),
                  'scope': 'Recorded root admission only; no approval semantics, live runtime, database or product result proved.'}, sort_keys=True))
