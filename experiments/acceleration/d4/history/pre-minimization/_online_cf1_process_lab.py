"""D4 owned-process transaction experiment; no provider guard is bypassed.

The surviving supervisor seals public fixture values using the existing D3
provider. A spawn child receives only synthetic claim metadata and CF1 bytes,
opens its own connection, and installs frame plus dirty retirement atomically.
Neither a provider, keyring, prepared key nor database connection crosses IPC.
"""
from dataclasses import dataclass
import multiprocessing
import os
import signal

from _online_enumeration_lab import EnumerationLab
from _online_cf1_lab import CF1EnumerationLab


ACK_SECONDS = 10
CHILD_WAIT_SECONDS = 20
JOIN_SECONDS = 5


class ChildFrameLab(EnumerationLab):
    # Reuse the exact D3 operation/context-pin check, without a crypto object.
    _require_pin = CF1EnumerationLab._require_pin

    @classmethod
    def reconstruct(cls, schema, operation, expected_pin):
        lab = super().reconstruct(schema, operation)
        lab.expected_pin = expected_pin
        with lab.connect() as c:
            lab._require_pin(c)
        return lab

    def install_presealed(self, c, claimed, frame):
        """The D3 frame/retirement SQL boundary, with sealing already complete.

        This is a research-only trusted packet, not a new product admission API.
        Operation, exact token and full expected pin are still checked here.
        """
        if claimed.operation != self.operation:
            return False
        if frame is not None and type(frame) is not bytes:
            raise TypeError("sealed fixture bytes required")
        with c.transaction():
            self._require_pin(c, lock=True)
            current = c.execute("SELECT token FROM dirty WHERE operation=%s AND id=%s FOR UPDATE",
                                (self.operation, claimed.key)).fetchone()
            if current != (claimed.token,):
                return False
            c.execute("INSERT INTO staged(operation,id,frame,live,token) VALUES(%s,%s,%s,%s,%s) "
                      "ON CONFLICT(operation,id) DO UPDATE SET frame=EXCLUDED.frame,live=EXCLUDED.live,token=EXCLUDED.token",
                      (self.operation, claimed.key, frame, claimed.live, claimed.token))
            retired = c.execute("DELETE FROM dirty WHERE operation=%s AND id=%s AND token=%s",
                                (self.operation, claimed.key, claimed.token))
            assert retired.rowcount == 1
            return True


def _command(pipe, expected):
    if not pipe.poll(CHILD_WAIT_SECONDS):
        raise TimeoutError("D4 supervisor command deadline")
    if pipe.recv() != expected:
        raise ValueError("unexpected D4 supervisor command")


def _child_worker(pipe, schema, operation, expected_pin, claimed, frame):
    """Only the supervisor's newly spawned process runs this entry point."""
    try:
        lab = ChildFrameLab.reconstruct(schema, operation, expected_pin)
        with lab.connect() as c:
            # install_presealed's transaction is a nested savepoint. The outer
            # transaction makes the real COMMIT boundary explicit to the pipe.
            with c.transaction():
                assert lab.install_presealed(c, claimed, frame)
                assert c.execute("SELECT token FROM dirty WHERE operation=%s AND id=%s",
                                 (operation, claimed.key)).fetchone() is None
                assert c.execute("SELECT frame,live,token FROM staged WHERE operation=%s AND id=%s",
                                 (operation, claimed.key)).fetchone() == (frame, claimed.live, claimed.token)
                pipe.send(("before_commit", os.getpid()))
                _command(pipe, "commit")
            # This acknowledgement is sent only after psycopg's outer COMMIT
            # returns. It intentionally excludes the ambiguous-COMMIT window.
            pipe.send(("after_commit", os.getpid()))
            _command(pipe, "finish")
    except BaseException as exc:
        # Do not let a child traceback print connection strings or provider data.
        # Failure remains explicit and cannot be counted as an injected death.
        try:
            pipe.send(("worker_error", type(exc).__name__))
        except (BrokenPipeError, EOFError, OSError):
            pass
        raise SystemExit(2) from None
    finally:
        pipe.close()


def _ack(pipe, child, expected):
    if not pipe.poll(ACK_SECONDS):
        raise TimeoutError("D4 worker acknowledgement deadline")
    try:
        message = pipe.recv()
    except EOFError:
        raise RuntimeError("D4 worker ended before acknowledgement") from None
    if message[0] == "worker_error":
        raise RuntimeError("D4 child failed: " + message[1])
    assert message == (expected, child.pid)
    assert child.is_alive(), "D4 worker must remain alive at its barrier"
    return expected


@dataclass(frozen=True)
class KilledWorker:
    barrier: str
    acknowledgements: tuple[str, ...]
    exitcode: int


def kill_owned_worker(lab, claimed, frame, *, barrier):
    """Kill and reap only this function's child, at one acknowledged boundary.

    Call with every supervisor database connection closed. The approved wrapper
    has already supplied the existing test role in the child's inherited env.
    No DSN, keys, provider, or connection are sent through this private pipe.
    """
    if os.name != "posix" or not hasattr(signal, "SIGKILL"):
        raise RuntimeError("D4 requires the authorized POSIX process environment")
    if barrier not in ("before_commit", "after_commit"):
        raise ValueError("unknown D4 commit barrier")
    context = multiprocessing.get_context("spawn")
    parent_pipe, child_pipe = context.Pipe(duplex=True)
    child = context.Process(target=_child_worker,
                            args=(child_pipe, lab.schema, lab.operation, lab.expected_pin, claimed, frame),
                            name="cryptalis-d4-owned-frame-worker", daemon=True)
    started = False
    try:
        child.start()
        started = True
        child_pipe.close()
        assert child.pid is not None and child.pid != os.getpid()
        acks = [_ack(parent_pipe, child, "before_commit")]
        if barrier == "after_commit":
            parent_pipe.send("commit")
            acks.append(_ack(parent_pipe, child, "after_commit"))
        # Process.kill targets only the child object created above. No process
        # search, PostgreSQL backend signal, service operation or group kill.
        child.kill()
        child.join(JOIN_SECONDS)
        assert not child.is_alive(), "D4 owned child did not reap by deadline"
        assert child.exitcode == -signal.SIGKILL
        return KilledWorker(barrier, tuple(acks), child.exitcode)
    finally:
        parent_pipe.close()
        child_pipe.close()
        if started:
            if child.is_alive():
                child.kill()
                child.join(JOIN_SECONDS)
            if child.is_alive():
                raise RuntimeError("D4 owned child cleanup deadline")
            child.close()
