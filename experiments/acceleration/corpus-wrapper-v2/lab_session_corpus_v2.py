"""Reuse the provisioned PG16 lab for one guarded, supervised pytest session.

Usage from repo: .venv/bin/python ../toolchain/lab_session.py --evidence ../evidence/NEW_CHECKPOINT -- -q PATH --tb=short
No server rebuild, credential substitution, security relaxation, or runner bypass.
"""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from corpus_artifacts_v2 import snapshot, capture_restore

# Preserve the original toolchain import location for this versioned derivative.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "toolchain"))
from run_baseline import BASE, ENV, PGCTL, REPO, RUNTIME, redact


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--python", type=Path, default=REPO / ".venv/bin/python",
                        help="Selected isolated dependency-cell interpreter; repository runner/preflight unchanged")
    parser.add_argument("--candidate-root", type=Path, help="Separate source candidate under this lab as candidate-*; unchanged preflight required")
    parser.add_argument("--installed-candidate", action="store_true", help="Run candidate tests against a byte-matched installed package in a disposable release-lab interpreter")
    parser.add_argument("pytest_args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    repo = REPO
    if args.candidate_root is not None:
        repo = args.candidate_root.resolve()
        if repo.parent != BASE or not repo.name.startswith("candidate-") or not repo.is_dir():
            parser.error("Candidate must be an existing candidate-* source tree directly inside this lab.")
        if (repo / "scripts/test_postgres.py").read_bytes() != (REPO / "scripts/test_postgres.py").read_bytes():
            parser.error("Candidate must preserve the existing repository runner/preflight exactly.")
    if args.installed_candidate and (args.candidate_root is None or not args.python.absolute().is_relative_to(BASE / "release-lab")):
        parser.error("Installed qualification requires a candidate tree and release-lab interpreter.")
    evidence = args.evidence.resolve()
    if not evidence.is_relative_to(BASE / "evidence"):
        parser.error("Evidence must be in this lab's evidence directory.")
    ENV["PYTHONPATH"] = (str(repo / "src") + os.pathsep if args.candidate_root is not None and not args.installed_candidate else "") + str(BASE / "toolchain")
    if args.candidate_root is not None:
        # The feature tree is a byte-recorded uncommitted derivative of this
        # exact base. Reuse Git's existing object metadata for read-only
        # revision receipts; neither refs nor the original worktree are edited.
        ENV["GIT_DIR"] = str(REPO / ".git")
        ENV["GIT_WORK_TREE"] = str(repo)
    ENV["CRYPTALIS_LAB_PROGRESS"] = str(evidence / "progress.jsonl")
    os.umask(0o077)
    evidence.mkdir(parents=True, exist_ok=False)
    (evidence / "source-root.json").write_text(json.dumps({"source_root": str(repo), "candidate_override": args.candidate_root is not None, "preflight_unchanged": True}, indent=2) + "\n")
    lock = (RUNTIME / "lab-session.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another session owns this PostgreSQL lab; no database action taken.", flush=True)
        return 2

    def interrupted(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupted)
    started_server = False
    prior_corpus = None

    def run(label, command):
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        clock = time.monotonic()
        try:
            result = subprocess.run(command, cwd=repo, env=ENV, capture_output=True, text=True,
                                    timeout=600 if label == "tests" else 90)
        except subprocess.TimeoutExpired as failure:
            from types import SimpleNamespace
            def decode(value):
                return value.decode(errors="replace") if isinstance(value,bytes) else value or ""
            result=SimpleNamespace(returncode=124,stdout=decode(failure.stdout),stderr=decode(failure.stderr)+"\nLAB SESSION TIMEOUT; no final pass claim.\n")
        output = redact(result.stdout + result.stderr)
        (evidence / (label + ".log")).write_text(output)
        (evidence / (label + ".json")).write_text(json.dumps({
            "command": command, "exit_code": result.returncode,
            "started_utc": started, "elapsed_seconds": time.monotonic()-clock,
            "environment": ENV}, indent=2) + "\n")
        print(label, "exit", result.returncode, flush=True)
        print(output[-8000:], flush=True)
        return result.returncode

    try:
        if args.candidate_root is not None:
            prior_corpus = snapshot(BASE / "evidence", evidence)
        code = run("postgres-start", [str(PGCTL), "-D", str(RUNTIME / "data"),
                   "-l", str(RUNTIME / "logs/postgres.log"), "-w", "start"])
        if code:
            return code
        started_server = True
        runner = [str(args.python.absolute()), "scripts/test_postgres.py"]
        code = run("readiness", runner + ["--preflight-only"])
        if code:
            print("Readiness failed; no tests executed. Diagnose before retry.", flush=True)
            return code
        if args.candidate_root is not None:
            origin_code = "import cryptalis,json,sys; from pathlib import Path; p=Path(cryptalis.__file__).resolve(); expected=Path(sys.argv[1]).resolve(); assert p.is_relative_to(expected),str(p); print(json.dumps({'package_origin':str(p),'expected_source':str(expected),'verified':True}))"
            if args.installed_candidate:
                origin_code = "import cryptalis,json,sys; from pathlib import Path; p=Path(cryptalis.__file__).resolve(); source=Path(sys.argv[1]).resolve(); assert p.is_relative_to(Path(sys.prefix).resolve()) and not p.is_relative_to(source),str(p); files=list((source/'cryptalis').rglob('*.py')); assert all((p.parent/f.relative_to(source/'cryptalis')).read_bytes()==f.read_bytes() for f in files); print(json.dumps({'package_origin':str(p),'expected_source':str(source),'installed':True,'byte_matched_modules':len(files),'verified':True}))"
            code = run("package-origin", [str(args.python.absolute()), "-c", origin_code, str(repo / "src")])
            if code:
                return code
        pytest_args = args.pytest_args[1:] if args.pytest_args[:1] == ["--"] else args.pytest_args
        def source_snapshot():
            paths = list((repo / "src").rglob("*.py")) + list((repo / "tests").rglob("*.py")) + [repo / "pyproject.toml", repo / "uv.lock"]
            return {str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
        # Preserve explicitly selected evidence-only tests as well as repo files.
        external_paths = set()
        for argument in pytest_args:
            candidate = (repo / argument.split("::", 1)[0]).resolve()
            if candidate.is_relative_to(BASE / "experiments"):
                if candidate.is_file() and candidate.suffix == ".py":
                    external_paths.add(candidate)
                elif candidate.is_dir():
                    external_paths.update(candidate.rglob("*.py"))
        def external_snapshot():
            return {str(p.relative_to(BASE)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(external_paths)}
        external_before = external_snapshot()
        (evidence / "external-source-before.json").write_text(json.dumps(external_before, indent=2) + "\n")
        for path in sorted(external_paths):
            archived = evidence / "source-external" / path.relative_to(BASE)
            archived.parent.mkdir(parents=True, exist_ok=True)
            archived.write_bytes(path.read_bytes())
        before = source_snapshot()
        (evidence / "source-before.json").write_text(json.dumps(before, indent=2) + "\n")
        for relative, digest in before.items():
            path = repo / relative
            archived = evidence / "source-repository" / relative
            archived.parent.mkdir(parents=True, exist_ok=True)
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != digest:
                raise RuntimeError("Source changed while creating the evidence snapshot")
            archived.write_bytes(data)
        code = run("tests", runner + ["--receipt", str(evidence / "runner-receipt.json"),
                   "--scope", "Isolated authorized research; all production gates UNKNOWN",
                   "--", *pytest_args, "-p", "lab_progress", "-o", "faulthandler_timeout=180", "--junitxml=" + str(evidence / "junit.xml")])
        after = source_snapshot()
        external_after = external_snapshot()
        (evidence / "external-source-stability.json").write_text(json.dumps({
            "before": external_before, "after": external_after,
            "unchanged": external_before == external_after}, indent=2) + "\n")
        (evidence / "source-stability.json").write_text(json.dumps({"before": before, "after": after, "unchanged": before == after}, indent=2) + "\n")
        if before != after or external_before != external_after:
            print("Source changed during run; results retained but not a stable candidate qualification.", flush=True)
            return 3
        return code
    finally:
        try:
            if started_server:
                run("postgres-stop", [str(PGCTL), "-D", str(RUNTIME / "data"), "-m", "fast", "-w", "stop"])
        finally:
            try:
                if prior_corpus is not None:
                    capture_restore(BASE / "evidence", evidence, prior_corpus)
            finally:
                lock.close()



if __name__ == "__main__":
    raise SystemExit(main())
