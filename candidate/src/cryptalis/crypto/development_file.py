"""Restart-safe DEVELOPMENT custody only; the local KEK is plaintext on disk.

This does not provide production custody, authenticated file provenance,
zeroization, protection from the same OS user, or a backup service. Keep the
private file outside databases, repositories, logs and exported evidence.
"""
import hashlib
import os
import stat
import sys
from hmac import compare_digest
from pathlib import Path
from uuid import UUID, uuid4

from .keys import DevelopmentKeyProvider, KeyUnavailable

_MAGIC = b'CDK1'
_SIZE = 84


class FileCustodyUnavailable(KeyUnavailable):
    stage = "development custody file"
    remedy = "Inspect the private development key file and retained recovery copies. Never replace missing or corrupt custody automatically."
    retryable = False
    effects = "A private file may exist after failed creation; inspect before retry."


def _close_descriptors(*descriptors):
    primary = sys.exc_info()[1]
    failed = False
    for descriptor in descriptors:
        if descriptor is not None:
            try: os.close(descriptor)
            except OSError: failed = True
    if failed:
        if primary is not None:
            primary.cleanup_errors = ("descriptor_close_failed",)
        else:
            raise FileCustodyUnavailable() from None


class FileDevelopmentKeyProvider(DevelopmentKeyProvider):
    """Explicit create/open; missing or corrupt custody never regenerates keys."""

    def __init__(self):
        raise FileCustodyUnavailable()

    @staticmethod
    def _parent(path):
        path = Path(path)
        if path.name in ('', '.', '..'):
            raise FileCustodyUnavailable()
        fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
        try:
            info = os.fstat(fd)
            if info.st_uid != os.getuid() or info.st_mode & 0o022:
                raise FileCustodyUnavailable()
            return fd, path.name
        except BaseException:
            _close_descriptors(fd)
            raise

    @classmethod
    def _material(cls, identity, key):
        if identity.int == 0 or len(key) != 32:
            raise FileCustodyUnavailable()
        result = object.__new__(cls)
        result._pid = os.getpid()
        result.provider_id = identity
        result._key = key
        return result

    @classmethod
    def create(cls, path):
        """Create one new private file; never truncate, replace or repair a file."""
        parent = fd = None
        try:
            identity, key = uuid4(), os.urandom(32)
            body = _MAGIC + identity.bytes + key
            blob = body + hashlib.sha256(body).digest()
            parent, name = cls._parent(path)
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                         0o600, dir_fd=parent)
            # A restrictive umask may remove owner bits; never broaden an existing file.
            os.fchmod(fd, 0o600)
            remaining = memoryview(blob)
            while remaining:
                written = os.write(fd, remaining)
                if written <= 0:
                    raise FileCustodyUnavailable()
                remaining = remaining[written:]
            os.fsync(fd)
            os.fsync(parent)
            return cls._material(identity, key)
        except FileCustodyUnavailable:
            raise
        except Exception:
            # A partial file stays unusable; no silent deletion/regeneration.
            raise FileCustodyUnavailable() from None
        finally:
            _close_descriptors(fd, parent)

    @classmethod
    def open(cls, path):
        """Open only an owner-private regular single-link file with exact format."""
        parent = fd = None
        try:
            parent, name = cls._parent(path)
            fd = os.open(name, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent)
            before = os.fstat(fd)
            if (not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid()
                    or stat.S_IMODE(before.st_mode) != 0o600 or before.st_nlink != 1
                    or before.st_size != _SIZE):
                raise FileCustodyUnavailable()
            chunks = []
            total = 0
            while total <= _SIZE:
                chunk = os.read(fd, _SIZE + 1 - total)
                if not chunk: break
                chunks.append(chunk); total += len(chunk)
            blob = b''.join(chunks)
            after = os.fstat(fd)
            fingerprint = lambda info: (info.st_dev, info.st_ino, info.st_uid, info.st_mode,
                                         info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
            if (fingerprint(before) != fingerprint(after) or len(blob) != _SIZE
                    or blob[:4] != _MAGIC or not compare_digest(hashlib.sha256(blob[:52]).digest(), blob[52:])):
                raise FileCustodyUnavailable()
            return cls._material(UUID(bytes=blob[4:20]), blob[20:52])
        except FileCustodyUnavailable:
            raise
        except Exception:
            raise FileCustodyUnavailable() from None
        finally:
            _close_descriptors(fd, parent)
