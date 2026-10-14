"""Filesystem-only receipt preservation. Never imports the database runner."""
import hashlib
import json
from pathlib import Path

PATTERNS = ('compatibility*corpus-v1-sa*.json',
            'master-s4-compatibility*corpus-v1-sa*.json')


def matching(root):
    paths = sorted({p for pattern in PATTERNS for p in root.glob(pattern)})
    if any(p.is_symlink() or not p.is_file() for p in paths):
        raise RuntimeError('Corpus artifact must be an ordinary file')
    return paths


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_new(path, data):
    # Exclusive creation prevents overwriting earlier evidence.
    with path.open('xb') as stream:
        stream.write(data)
    if path.read_bytes() != data:
        raise OSError('Corpus evidence verification failed')


def snapshot(root, evidence):
    """Called under the existing lab lock, before starting PostgreSQL."""
    backup = evidence / 'prior-corpus'
    backup.mkdir()
    prior = {}
    for path in matching(root):
        data = path.read_bytes()
        save_new(backup / path.name, data)
        prior[path] = data
    save_new(evidence / 'prior-corpus-manifest.json',
             (json.dumps({p.name: digest(data) for p, data in prior.items()},
                         indent=2) + '\n').encode())
    return prior


def restore_one(path, data):
    temporary = path.with_name(path.name + '.corpus-restore-v2.tmp')
    save_new(temporary, data)
    temporary.replace(path)
    if path.read_bytes() != data:
        raise OSError('Corpus restoration verification failed')


def capture_restore(root, evidence, prior):
    """Archive before restoring; a failed archive retains the changed source.

    Other files still get independent restoration attempts. Durable pre-run
    originals remain available even if archive or restoration fails. Any such
    failure prevents a successful wrapper result.
    """
    dest = evidence / 'candidate-corpus'
    errors, archived, deleted = [], [], []
    try:
        dest.mkdir()
    except OSError as exc:
        errors.append({'stage': 'archive_directory', 'type': type(exc).__name__})
    try:
        current = set(matching(root))
    except (OSError, RuntimeError) as exc:
        current = set()
        errors.append({'stage': 'enumerate', 'type': type(exc).__name__})
    for path in sorted(current | set(prior)):
        try:
            if path.is_symlink():
                raise OSError('Symlink corpus target refused')
            present = path.exists()
            data = path.read_bytes() if present else None
            original = prior.get(path)
            if present and (path not in prior or data != original):
                save_new(dest / path.name, data)
                archived.append({'name': path.name, 'sha256': digest(data)})
            elif not present and path in prior:
                deleted.append(path.name)
            # Never remove or overwrite bytes that failed to archive above.
            if path in prior and data != original:
                restore_one(path, original)
            elif path not in prior and present:
                path.unlink()
        except OSError as exc:
            errors.append({'stage': 'capture_restore', 'name': path.name,
                           'type': type(exc).__name__})
    restored = True
    for path, data in prior.items():
        try:
            restored = (not path.is_symlink() and path.read_bytes() == data) and restored
        except OSError:
            restored = False
    try:
        no_new_files = set(matching(root)) == set(prior)
    except (OSError, RuntimeError):
        no_new_files = False
    report = {'patterns': list(PATTERNS), 'archived': archived,
              'deleted_during_run': deleted,
              'primary_receipts_restored': restored and no_new_files,
              'errors': errors}
    save_new(evidence / 'candidate-corpus-isolation.json',
             (json.dumps(report, indent=2) + '\n').encode())
    if errors or not report['primary_receipts_restored']:
        raise RuntimeError('Corpus preservation failed; inspect isolation report and prior-corpus')
    return report
