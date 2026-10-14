"""INERT UNTIL COORDINATOR AUTHENTICATES THE EXACT REMOTE READBACK RECEIPT.

Offline standard-library data checker. No network, Git, database, subprocess,
project import, archive-code execution or credential read. Requires independently
supplied immutable commit and SHA-256 of a coordinator-verified per-file receipt.
This checker verifies that attestation and content; it cannot authenticate a
network service. Local staging copies must never be relabeled remote readbacks.
Run only when separately authorized: python -I -S <this script> --expected-remote-commit
<verified 40-hex commit> --authenticated-provenance-sha256 <verified receipt hash>.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import io
import json
import lzma
import os
import re
import stat
import tarfile

P = Path('/workspace/scratch/cb28ee9f5f4a/persistence-recovery-20261013')
PARTS = P / 's24-statistics-continuation-remote-parts'
OUTARCHIVE = P / 's24-statistics-continuation-remote-reconstructed.tar.xz'
OUTROOT = P / 's24-statistics-continuation-remote-fresh-extraction'
OUTREPORT = P / 's24-statistics-continuation-remote-restore-verification.json'
REPOSITORY = 'debgh-workspace/cryptalis-research-lab'
REMOTE_PREFIX = 'recovery/s24-statistics-continuation/parts'
ARCHIVE_NAME = 'CRYPTALIS_S24_STATISTICS_CONTINUATION_RECOVERY_20261014_v1.tar.xz'
ARCHIVE_ROOT = 'CRYPTALIS_S24_STATISTICS_CONTINUATION_RECOVERY_20261014_v1'
ARCHIVE_SHA256 = '666967c6dc20e918de014366a964b8ba4a351e7ea420a9834b1c5b94eafe473a'
ARCHIVE_BYTES = 300660
PART_MANIFEST_SHA256 = 'd8962f9bc453ad2384ae8d2a828be2c85b313879a1db504715b617a2d38edb13'
PART_MANIFEST_BYTES = 1348
PART_MANIFEST_BLOB = '68eb1742b97d1ee697b2b787c084104a3fa09ecc'
PAYLOAD_MANIFEST = 'FROZEN_PAYLOAD_MANIFEST-v1.json'
PAYLOAD_MANIFEST_SHA256 = '74f8721d757a7a6e212450c41a27aa861d2a32e8122570b232ae625f5f06fc2a'
PAYLOAD_MANIFEST_BYTES = 382108
PREPARED_MANIFEST_SHA256 = '1523178b7cf658ab36507db911a64afd681ba38c300737ed0fce831ce9cceb5e'
ALLOWLIST_SHA256 = '8fb94c9fb5b77779afea662426eca8b7f6e5588b1abf78c399b3d0ee6e144431'
BASELINE_MANIFEST_SHA256 = '6c7ca4ecda9e4d0628aa8a8fe4626e36c8708622f020c73c8320210948cd003d'
OBSERVER_SHA256 = '6534250833d3a2362f838a1574a5b0bdd028b8016a8502167539b6a41140f962'
EXPECTED_PARTS = [
 ('part-01.bin',96000,'4da098ade959850276b06e81888b5a2627c07ff5afbe12bcc4962aa8a87f89bf','dba7b72f6b05db4d96037df11a3ffa704c2aff15'),
 ('part-02.bin',96000,'03e00a68d01b6dac6842d04f5a0725053ff7aa683ce2a427edf99487e578054e','1e88dbdbfa8ad14474f751fad7be9d812c662d7e'),
 ('part-03.bin',96000,'ebba2fed2e094bd82d345db3009c8a45cb42e3ad8940b9679620ae667f2e77bd','0fd341d48a55aa66ef3ace5e5d6e769081646738'),
 ('part-04.bin',12660,'59b007b03369a200378f3d0b57d1143d5540ab8e0696c988d62f9369ddd95283','d94e3f0aca39e90ab93d01f514e8ac09acec3cee'),
]
EXPECTED_REMOTE_FILES = [('MANIFEST.json',PART_MANIFEST_BYTES,PART_MANIFEST_SHA256,PART_MANIFEST_BLOB)] + EXPECTED_PARTS
FORBIDDEN_NAMES = {'tests.json','readiness.json','package-origin.json','postgres-start.json','postgres-stop.json'}
FORBIDDEN_PARTS = {'.git','.venv','venv','__pycache__','.pytest_cache','site-packages','node_modules','runtime','source-repository','external-sources','full214source','.ssh','.aws','.codex','credentials','secrets','environment','dependencies','cache','toolchain','pgdata','postgres-data'}
MAX_MEMBER_BYTES = 417054
TOTAL_MEMBER_BYTES = 16535084
TAR_BYTES = 19333120
MEMBERS = 1593
GATES = {'G-ADAPTER','G-CRYPTO','G-QUERY','G-LIFECYCLE','G-PROVIDER','G-POLICY','G-RELEASE'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def hex_digest(value, length=64):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{' + str(length) + '}', value) is not None


def safe_relative(name):
    require(isinstance(name, str) and bool(name), 'Path is not nonempty text')
    require('\\' not in name and all(ord(c) >= 32 and ord(c) != 127 for c in name), 'Forbidden path character')
    require(all(c not in ('', '.', '..') for c in name.split('/')), 'Noncanonical path component')
    q = PurePosixPath(name)
    require(not q.is_absolute() and q.as_posix() == name, 'Noncanonical relative path')
    return q


def allowed_name(name):
    q = safe_relative(name)
    require(q.name not in FORBIDDEN_NAMES and not set(q.parts) & FORBIDDEN_PARTS, 'Forbidden phase/runtime path')
    require(not any(c == '.env' or c.startswith('.env.') for c in q.parts), 'Forbidden environment path')
    require(not q.name.endswith(('.pyc','.pyo','.sqlite','.sqlite3','.db','.tar','.tar.xz','.tar.gz','.tgz','.zip','.bin')), 'Forbidden runtime/nested archive')
    return q


def unique_object(pairs):
    result = {}
    for k,v in pairs:
        require(k not in result, 'Duplicate JSON object key')
        result[k] = v
    return result


def reject_constant(value):
    raise ValueError('Nonfinite JSON value')


def parse_json(data):
    return json.loads(data, object_pairs_hook=unique_object, parse_constant=reject_constant)


def require_directory(path):
    require(stat.S_ISDIR(path.lstat().st_mode), 'Non-directory or symlink ancestor')


def require_directory_chain(path):
    require(path.is_absolute(), 'Directory is not absolute')
    for ancestor in reversed(path.parents):
        require_directory(ancestor)
    require_directory(path)


def read_regular(path, limit):
    require(path.is_relative_to(P), 'Read outside fixed recovery namespace')
    require_directory_chain(path.parent)
    require(stat.S_ISREG(path.lstat().st_mode), 'Input is not regular')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as f:
        info = os.fstat(f.fileno())
        require(stat.S_ISREG(info.st_mode) and 0 <= info.st_size <= limit, 'Input type/size invalid')
        data = f.read(limit + 1)
    require(len(data) == info.st_size and len(data) <= limit, 'Input changed or exceeded bound')
    return data


def absent(path):
    try:
        path.lstat()
    except FileNotFoundError:
        return True
    return False


def write_new(root, relative, data):
    require(root.is_relative_to(P), 'Write outside fixed recovery namespace')
    parts = safe_relative(relative).parts
    parent = root
    require_directory_chain(parent)
    for component in parts[:-1]:
        parent = parent / component
        try:
            parent.mkdir(mode=0o700)
        except FileExistsError:
            require_directory(parent)
    target = parent / parts[-1]
    fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as f:
        require(f.write(data) == len(data), 'Short write')
    require(read_regular(target, len(data)) == data, 'Write readback differs')


def verify_tree(root, expected):
    require_directory_chain(root)
    files, directories = set(), set()
    want_dirs = {p.as_posix() for name in expected for p in safe_relative(name).parents if p.as_posix() != '.'}
    for p in root.rglob('*'):
        name = p.relative_to(root).as_posix()
        safe_relative(name)
        mode = p.lstat().st_mode
        if stat.S_ISDIR(mode):
            directories.add(name)
        else:
            require(stat.S_ISREG(mode) and mode & 0o111 == 0, 'Restored special/link/executable file')
            require(name in expected and read_regular(p, len(expected[name])) == expected[name], 'Restored bytes/name differ')
            files.add(name)
    require(files == set(expected) and directories == want_dirs, 'Fresh tree closure differs')


def main():
    ap = argparse.ArgumentParser(description='Pinned offline data-only checker; coordinator authentication is mandatory')
    ap.add_argument('--expected-remote-commit', required=True)
    ap.add_argument('--authenticated-provenance-sha256', required=True)
    args = ap.parse_args()
    require(hex_digest(args.expected_remote_commit,40), 'Expected immutable commit must be 40 lowercase hex')
    require(hex_digest(args.authenticated_provenance_sha256), 'Expected provenance digest must be 64 lowercase hex')
    require_directory_chain(P)
    require_directory_chain(PARTS)
    for output in (OUTARCHIVE,OUTROOT,OUTREPORT):
        require(absent(output), 'Output already exists; no reuse or overwrite')
    expected_input_names = {r[0] for r in EXPECTED_REMOTE_FILES} | {'REMOTE_PROVENANCE.json'}
    require({p.name for p in PARTS.iterdir()} == expected_input_names, 'Exact remote readback directory differs')
    provenance_bytes = read_regular(PARTS/'REMOTE_PROVENANCE.json',1000000)
    require(sha256(provenance_bytes) == args.authenticated_provenance_sha256, 'Provenance receipt identity differs')
    provenance = parse_json(provenance_bytes)
    require(isinstance(provenance,dict), 'Provenance is not an object')
    require(provenance['authenticated_remote_readbacks_verified'] is True, 'Coordinator authentication absent')
    require(provenance['repository'] == REPOSITORY and provenance['remote_prefix'] == REMOTE_PREFIX, 'Repository/path differs')
    require(provenance['commit_sha'] == args.expected_remote_commit, 'Immutable commit differs')
    require(provenance['authenticated_commit_lookup'] is True and provenance['commit_lookup_sha'] == args.expected_remote_commit, 'Authenticated commit lookup absent')
    require(provenance['archive_sha256'] == ARCHIVE_SHA256 and provenance['part_manifest_sha256'] == PART_MANIFEST_SHA256, 'Capsule identity differs')
    require(provenance['local_readback_directory'] == str(PARTS), 'Readback directory differs')
    require(provenance['source'] == 'authenticated_remote_readback' and provenance['local_staging_used_for_restore'] is False, 'Local staging cannot authenticate remote recovery')
    require(isinstance(provenance['commit_lookup_reference'],str) and 0 < len(provenance['commit_lookup_reference']) <= 4096, 'Commit lookup evidence reference absent')
    remote_rows = provenance['remote_files']
    require(isinstance(remote_rows,list) and len(remote_rows) == 5, 'Expected five individual remote readback receipts')
    inputs = {}
    for row,(name,size,digest,blob) in zip(remote_rows,EXPECTED_REMOTE_FILES):
        require(isinstance(row,dict), 'Remote file receipt is not an object')
        require(row['name'] == name and row['repository'] == REPOSITORY and row['commit_sha'] == args.expected_remote_commit, 'Per-file repository/commit/name differs')
        require(row['remote_path'] == REMOTE_PREFIX+'/'+name and row['authenticated_readback'] is True, 'Per-file remote path/authentication differs')
        require(type(row['bytes']) is int and row['bytes'] == size and row['sha256'] == digest and row['git_blob_sha'] == blob, 'Per-file remote identity differs')
        require(isinstance(row['verification_reference'],str) and 0 < len(row['verification_reference']) <= 4096, 'Per-file evidence reference absent')
        data = read_regular(PARTS/name,size)
        require(len(data) == size and sha256(data) == digest and git_blob(data) == blob, 'Per-file readback bytes differ')
        inputs[name] = data
    manifest_bytes = inputs['MANIFEST.json']
    manifest = parse_json(manifest_bytes)
    require(manifest['format'] == 's24-statistics-continuation-parts-v1' and manifest['archive'] == ARCHIVE_NAME, 'Split format/name differs')
    require(type(manifest['bytes']) is int and manifest['bytes'] == ARCHIVE_BYTES and manifest['archive_sha256'] == ARCHIVE_SHA256, 'Split archive identity differs')
    require(manifest['intended_repository'] == REPOSITORY and manifest['intended_remote_prefix'] == REMOTE_PREFIX, 'Split destination differs')
    require([(r['name'],r['bytes'],r['sha256'],r['git_blob_sha']) for r in manifest['parts']] == EXPECTED_PARTS, 'Split part map/order differs')
    archive_bytes = b''.join(inputs[row[0]] for row in EXPECTED_PARTS)
    require(len(archive_bytes) == ARCHIVE_BYTES and sha256(archive_bytes) == ARCHIVE_SHA256, 'Recombined archive differs')
    decoder = lzma.LZMADecompressor(format=lzma.FORMAT_XZ,memlimit=128000000)
    tar_bytes = decoder.decompress(archive_bytes,max_length=TAR_BYTES+1)
    require(len(tar_bytes) == TAR_BYTES and decoder.eof and not decoder.unused_data, 'XZ bound/trailing stream differs')
    payload,folded = {},set()
    with tarfile.open(fileobj=io.BytesIO(tar_bytes),mode='r:') as tar:
        members = tar.getmembers()
        require(len(members) == MEMBERS, 'Archive member count differs')
        names=set();total=0;last_end=0
        # Validate every path/type/header before reading any member body.
        for m in members:
            allowed_name(m.name)
            require(m.name.startswith(ARCHIVE_ROOT+'/'), 'Archive root prefix differs')
            rel=m.name[len(ARCHIVE_ROOT)+1:];allowed_name(rel)
            require(m.type in (tarfile.REGTYPE,tarfile.AREGTYPE) and not m.sparse and not m.linkname, 'Nonregular/sparse/link member')
            require((m.mode,m.uid,m.gid,m.mtime,m.uname,m.gname)==(0o644,0,0,0,'',''), 'Nondeterministic header')
            require(m.pax_headers in ({},{'path':m.name}), 'Unsupported PAX header')
            require(rel not in names and rel.casefold() not in folded, 'Duplicate/case-colliding member')
            require(type(m.size) is int and 0 <= m.size <= MAX_MEMBER_BYTES, 'Member size bound differs')
            names.add(rel);folded.add(rel.casefold());total+=m.size
            require(total <= TOTAL_MEMBER_BYTES, 'Total member byte bound exceeded')
            last_end=m.offset_data+((m.size+511)//512)*512
        require(total == TOTAL_MEMBER_BYTES, 'Member total differs')
        require(len(tar_bytes)-last_end >= 1024 and not any(tar_bytes[last_end:]), 'Invalid tar end padding')
        for name in names:
            require(all(p.as_posix() not in names for p in safe_relative(name).parents if p.as_posix()!='.'), 'File/directory collision')
        for m in members:
            rel=m.name[len(ARCHIVE_ROOT)+1:]
            with tar.extractfile(m) as stream:
                data=stream.read(m.size+1)
            require(len(data)==m.size, 'Member body length differs')
            payload[rel]=data
    require(PAYLOAD_MANIFEST in payload and len(payload[PAYLOAD_MANIFEST]) == PAYLOAD_MANIFEST_BYTES and sha256(payload[PAYLOAD_MANIFEST]) == PAYLOAD_MANIFEST_SHA256, 'Frozen payload manifest differs')
    document=parse_json(payload[PAYLOAD_MANIFEST]);inventory=document['files']
    require(document['status']=='AUTHORIZED_LOCAL_DATA_FREEZE' and document['archive_root']==ARCHIVE_ROOT and document['self_excluded']==PAYLOAD_MANIFEST, 'Frozen manifest scope differs')
    require(document['allowlist_sha256']==ALLOWLIST_SHA256 and document['prepared_payload_manifest_sha256']==PREPARED_MANIFEST_SHA256, 'Frozen source pins differ')
    require(isinstance(inventory,dict) and len(inventory)==MEMBERS-1 and set(payload)==set(inventory)|{PAYLOAD_MANIFEST}, 'Payload hash map closure differs')
    for name,pin in inventory.items():
        allowed_name(name)
        require(set(pin)=={'size','sha256'} and type(pin['size']) is int and 0 <= pin['size'] <= MAX_MEMBER_BYTES and hex_digest(pin['sha256']), 'Invalid payload hash pin')
        require(len(payload[name])==pin['size'] and sha256(payload[name])==pin['sha256'], 'Payload bytes differ')
    require(sha256(payload['ALLOWLIST.txt'])==ALLOWLIST_SHA256 and sha256(payload['PAYLOAD_MANIFEST-PREPARED.json'])==PREPARED_MANIFEST_SHA256, 'Prepared allowlist/manifest differs')
    allow=payload['ALLOWLIST.txt'].decode('utf-8').splitlines()
    require(allow==sorted(set(allow)) and len(allow)==1550, 'Selected original allowlist differs')
    source=parse_json(payload['SOURCE_INVENTORY_BEFORE.json'])
    require(source==parse_json(payload['SOURCE_INVENTORY_AFTER.json'])==parse_json(payload['PRESERVED_INVENTORY.json']) and set(source)==set(allow), 'Selected inventories differ')
    require({n for n in payload if n.startswith('preserved/')}=={'preserved/'+n for n in allow}, 'Preserved subset closure differs')
    require(sum(r['size'] for r in source.values())==13229599, 'Selected byte count differs')
    for name,pin in source.items():
        allowed_name(name);body=payload['preserved/'+name]
        require(len(body)==pin['size'] and sha256(body)==pin['sha256'], 'Preserved original pin differs')
    source_prefix='preserved/cryptalis-executable/'
    baseline_name=source_prefix+'experiments/s24-statistics-diagnostic-20261014/BASELINE_SOURCE_MANIFEST.json'
    candidate_name=source_prefix+'experiments/s24-statistics-diagnostic-v4-20261014/CANDIDATE_SOURCE_MANIFEST.json'
    overlay_name=source_prefix+'candidate-s24-statistics-diagnostic-v4-20261014/src/cryptalis/_statistics_diagnostic.py'
    require(sha256(payload[baseline_name])==BASELINE_MANIFEST_SHA256 and sha256(payload[overlay_name])==OBSERVER_SHA256, 'Baseline/overlay identity differs')
    baseline=parse_json(payload[baseline_name])['source_sha256'];candidate=parse_json(payload[candidate_name])['source_sha256']
    require(len(baseline)==214 and len(candidate)==215 and dict(baseline,**{'src/cryptalis/_statistics_diagnostic.py':OBSERVER_SHA256})==candidate, 'Manifest-only 214+1 comparison differs')
    summary=parse_json(payload['CELL_SUMMARY.json'])
    require(summary['all_production_gates']=='UNKNOWN' and summary['same_99_case_universe_across_dependency_cells'] is True and summary['groups_disjoint_within_cell'] is True, 'Recorded summary scope differs')
    require(len(summary['cells'])==12, 'Expected twelve recorded selected runs')
    for row in summary['cells']:
        require(set(row['all_seven_gates'])==GATES and set(row['all_seven_gates'].values())=={'UNKNOWN'}, 'A production gate was promoted')
    require(summary['totals_per_dependency_cell']=={'sa21':{'passed':99,'warnings':99},'sa20':{'passed':99,'warnings':99}}, 'Recorded per-cell totals differ')
    # All authenticated/pinned input identities and every archived byte are now
    # checked. Do not follow manifest source paths. Never execute archive code.
    require_directory_chain(P)
    for output in (OUTARCHIVE,OUTROOT,OUTREPORT):require(absent(output),'Output appeared before writing')
    write_new(P,OUTARCHIVE.name,archive_bytes)
    OUTROOT.mkdir(mode=0o700)
    for name,body in payload.items():write_new(OUTROOT,name,body)
    verify_tree(OUTROOT,payload)
    require(read_regular(OUTARCHIVE,ARCHIVE_BYTES)==archive_bytes,'Reconstructed archive readback differs')
    require(read_regular(PARTS/'REMOTE_PROVENANCE.json',1000000)==provenance_bytes,'Provenance changed during restore')
    for name,body in inputs.items():require(read_regular(PARTS/name,len(body))==body,'Remote readback changed during restore')
    require({p.name for p in PARTS.iterdir()}==expected_input_names,'Remote readback directory changed')
    result={
      'status':'PASS_COORDINATOR_AUTHENTICATED_REMOTE_DATA_ONLY_CONTINUATION_RESTORE',
      'repository':REPOSITORY,'remote_commit_sha':args.expected_remote_commit,'remote_prefix':REMOTE_PREFIX,
      'authenticated_provenance_sha256':sha256(provenance_bytes),
      'authentication_scope':'Exact coordinator-authenticated commit and per-file readback receipt; this offline checker does not authenticate a network service.',
      'archive_sha256':ARCHIVE_SHA256,'archive_bytes':ARCHIVE_BYTES,'parts_verified':4,'remote_files_verified':5,
      'part_manifest_sha256':PART_MANIFEST_SHA256,'payload_manifest_sha256':PAYLOAD_MANIFEST_SHA256,
      'archive_members':MEMBERS,'member_bytes':TOTAL_MEMBER_BYTES,'selected_originals':1550,'selected_original_bytes':13229599,
      'fresh_tree_exact':True,'all_remote_readback_inputs_unchanged':True,'regular_nonexecuting_files_only':True,
      'archive_path':str(OUTARCHIVE),'fresh_extraction_path':str(OUTROOT),
      'manifest_source_paths_followed':False,'candidate_or_archived_code_imported_or_executed':False,
      'database_install_network_git_remote_actions_by_checker':False,'full_source_runtime_dependency_database_restore_claim':False,
      'baseline_reconstruction':'214-entry hash reference plus exact one-file private overlay; full baseline bytes external',
      'all_seven_gates':'UNKNOWN','private_observer':'unhooked and not integrated','twelve_mutation_controls':'UNRUN',
      'qualification_limits':'Twelve separate selected runs, 99 cases and retained warnings per cell. Prior V1/V2 HOLD and V3 failure history unchanged. No combined-run, strict xunit2, performance, privileged-removal, package-free, security or release qualification.',
      'publication_authorized_by_checker':False}
    write_new(P,OUTREPORT.name,(json.dumps(result,indent=2,sort_keys=True)+'\n').encode('utf-8'))
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
