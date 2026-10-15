"""Unexecuted, stdlib-only CLI rendering proof with explicit dynamic stubs.

Run only after independent review and coordinator selection. This is a unit
boundary, not installed-package import, database or provider qualification.
The exact copied product sources execute without body rewriting.
"""

import sys

# Root must launch with -I -B -S and an absent -X pycache_prefix destination.
ROOT = "/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/preview-doctor-dx-slice-20261015/proof-v1"
RUNTIME = "/opt/codex/runtimes/codex-primary-runtime/dependencies/python"
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise RuntimeError("required_isolated_no_site_no_bytecode_flags")
if sys.pycache_prefix != ROOT + "/no-bytecode-use":
    raise RuntimeError("required_fresh_bytecode_prefix")

import argparse
import dataclasses
import errno
import hashlib
import io
import json
import os
from pathlib import Path
import re
import resource
import signal
import stat
import time
import types
import typing
import uuid


BASE = Path(ROOT)
STDLIB = Path(RUNTIME) / "lib/python3.12"
INTERPRETER_SHA = "fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7"
SOURCE_MANIFEST_SHA = "202661a5c2650521bbd4f57164a9e9c2f88803d0eeda3dd8acd88cd9d46a4520"
PATCH_SHA = "31e117393dd77d40a8d10733434defe55c6b590958ec25d73afaaa5821592e10"
BASELINE_CLI_SHA = "0df0b4f0101933b3a069024965b7bc5a3374747aff53d37099d2f22efc105efe"
DERIVATIVE_CLI_SHA = "060cb66057f66c6d22c2b455bfba918545a3fabc251e72a30ab8fbfe61b0f409"
ADDED_LINE = b'            + (f"\\n  remedy: {check[\'remedy\']}" if "remedy" in check else "")\n'
SOURCE_FILES = (
    "src/cryptalis/__init__.py",
    "src/cryptalis/cli.py",
    "src/cryptalis/doctor.py",
    "src/cryptalis/manifest/__init__.py",
    "src/cryptalis/manifest/canonical.py",
    "src/cryptalis/manifest/header.py",
    "src/cryptalis/manifest/parser.py",
    "src/cryptalis/manifest/declaration.py",
)
VARIANTS = {
    "baseline-red": "copied-source/src/cryptalis/cli.py",
    "derivative-green": "variants/derivative.py",
    "omission-mutant": "variants/omission-mutant.py",
    "exact-restored": "variants/exact-restored.py",
}
CASE_IDS = (
    "D01_malformed_text_remedy", "D02_wrong_schema_text_remedy",
    "D03_valid_text_unchanged", "D04_rejected_json_unchanged",
    "D05_valid_json_unchanged", "D06_stdout_write_failure",
    "D07_stdout_short_write", "D08_stdout_flush_failure",
    "D09_stderr_failure_stays_operational",
    "D10_dynamic_sentinels_are_effective",
    "D11_redaction_collector_positive_control",
)
MARKERS = ("PRIVATE_CONTENT_MARKER", "PRIVATE_SCHEMA_MARKER",
           "PRIVATE_PATH_MARKER", "PRIVATE_IO_MARKER")
REMEDY = "Supply a valid bounded cryptalis.protection/v1 declaration."
CHECK_NAMES = ("manifest", "setup", "native_admission", "deployment",
               "compatibility", "roles", "provider", "ciphertext")
DYNAMIC_CALLS = {name: 0 for name in ("compiler", "active", "setup", "ciphertext")}


class ProofRejected(RuntimeError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def require(condition, code):
    if not condition:
        raise ProofRejected(code)


def read_regular(path, limit=64 * 1024 * 1024):
    """Bounded regular-file reads only; reject symlink components."""
    path = Path(path)
    require(path.is_absolute(), "absolute_input_path_required")
    current = Path("/")
    for part in path.parts[1:]:
        current = current / part
        require(not stat.S_ISLNK(current.lstat().st_mode), "symlink_input_refused")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        metadata = os.fstat(descriptor)
        require(stat.S_ISREG(metadata.st_mode), "regular_input_required")
        require(0 <= metadata.st_size <= limit, "input_size_limit")
        chunks = []
        remaining = limit + 1
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        require(len(raw) <= limit, "input_read_limit")
        return raw
    finally:
        os.close(descriptor)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def parse_pins(raw):
    pins = {}
    for line in raw.decode("ascii").splitlines():
        expected, relative = line.split("  ", 1)
        require(re.fullmatch(r"[0-9a-f]{64}", expected) is not None,
                "invalid_pin_digest")
        parts = Path(relative).parts
        require(parts and not Path(relative).is_absolute()
                and ".." not in parts and relative not in pins,
                "invalid_or_duplicate_pin_path")
        require("__pycache__" not in parts and "site-packages" not in parts
                and not relative.endswith(".pyc"), "cache_or_site_input_refused")
        pins[relative] = expected
    return pins


def emit(value):
    sys.stdout.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def preflight(mode, expected_inputs_sha):
    require(not os.environ, "root_must_supply_empty_environment")
    require(sys.version_info[:2] == (3, 12), "python_312_required")
    require(sys.executable == RUNTIME + "/bin/python3.12", "wrong_interpreter_path")
    require(sys.prefix == RUNTIME and sys.base_prefix == RUNTIME, "wrong_runtime_prefix")
    require(not os.path.lexists(ROOT + "/no-bytecode-use"), "bytecode_prefix_must_be_absent")
    allowed_search = {RUNTIME + "/lib/python312.zip", str(STDLIB),
                      str(STDLIB / "lib-dynload")}
    require(set(sys.path) == allowed_search and len(sys.path) == 3,
            "unexpected_stdlib_search_route")
    require(not os.path.lexists(RUNTIME + "/lib/python312.zip"),
            "unadmitted_stdlib_zip")
    require(digest(read_regular(Path(RUNTIME) / "bin/python3.12")) == INTERPRETER_SHA,
            "interpreter_pin_mismatch")
    inputs_raw = read_regular(BASE / "INPUTS.sha256", 256 * 1024)
    require(digest(inputs_raw) == expected_inputs_sha, "input_inventory_anchor_mismatch")
    inputs = parse_pins(inputs_raw)
    required_inputs = {
        "prove_doctor_remedy.py", "EXPECTED_CASE_IDS.json", "STDLIB_PATHS.txt",
        "STDLIB_SHA256.txt", "CANDIDATE_SOURCE_MANIFEST.json",
        "doctor-text-remedy.patch", "RUN_PLAN.md",
        "variants/derivative.py", "variants/omission-mutant.py",
        "variants/exact-restored.py",
        "fixtures/PRIVATE_PATH_MARKER-malformed.json",
        "fixtures/PRIVATE_PATH_MARKER-wrong-schema.json",
        "fixtures/PRIVATE_PATH_MARKER-valid.json",
    } | {"copied-source/" + name for name in SOURCE_FILES}
    require(set(inputs) == required_inputs, "unexpected_proof_input_inventory")
    raw_files = {}
    for relative, expected in inputs.items():
        raw = read_regular(BASE / relative)
        require(digest(raw) == expected, "proof_input_pin_mismatch")
        raw_files[relative] = raw
    require(tuple(json.loads(raw_files["EXPECTED_CASE_IDS.json"])) == CASE_IDS,
            "case_inventory_mismatch")
    manifest_raw = raw_files["CANDIDATE_SOURCE_MANIFEST.json"]
    require(digest(manifest_raw) == SOURCE_MANIFEST_SHA, "source_manifest_anchor_mismatch")
    manifest = json.loads(manifest_raw)
    require(manifest["source_files"] == 221
            and manifest["candidate"] == "candidate-cluster-retained-integrated-v2-20261015",
            "source_manifest_identity_mismatch")
    for relative in SOURCE_FILES:
        require(digest(raw_files["copied-source/" + relative])
                == manifest["source_sha256"][relative], "source_admission_mismatch")
    require(digest(raw_files["doctor-text-remedy.patch"]) == PATCH_SHA,
            "original_patch_changed")
    baseline = raw_files[VARIANTS["baseline-red"]]
    changed = raw_files[VARIANTS["derivative-green"]]
    require(digest(baseline) == BASELINE_CLI_SHA
            and digest(changed) == DERIVATIVE_CLI_SHA, "cli_variant_pin_mismatch")
    require(changed.count(ADDED_LINE) == 1
            and changed.replace(ADDED_LINE, b"", 1) == baseline,
            "delta_is_not_exactly_one_added_line")
    require(raw_files[VARIANTS["omission-mutant"]] == baseline,
            "omission_mutant_not_exact")
    require(raw_files[VARIANTS["exact-restored"]] == changed,
            "restored_variant_not_exact")
    stdlib_pins = parse_pins(raw_files["STDLIB_SHA256.txt"])
    require(len(stdlib_pins) == 472 and
            list(stdlib_pins) == raw_files["STDLIB_PATHS.txt"].decode("ascii").splitlines(),
            "stdlib_inventory_mismatch")
    for relative, expected in stdlib_pins.items():
        require(len(Path(relative).parts) <= 2 and relative.endswith((".py", ".so")),
                "stdlib_route_not_finite")
        require(digest(read_regular(STDLIB / relative)) == expected,
                "stdlib_file_pin_mismatch")
    # Includes stdlib modules already needed during Python startup/preflight.
    for module in tuple(sys.modules.values()):
        location = getattr(module, "__file__", None)
        if location is None:
            continue
        location = Path(location)
        if location == BASE / "prove_doctor_remedy.py":
            continue
        require(location.is_relative_to(STDLIB), "nonstdlib_preloaded_module")
        require(location.relative_to(STDLIB).as_posix() in stdlib_pins,
                "unadmitted_preloaded_stdlib")
    allowed_reads = {str(BASE / name) for name in inputs}
    allowed_reads.add(str(BASE / "INPUTS.sha256"))
    allowed_reads.update(str(STDLIB / name) for name in stdlib_pins)
    allowed_file_identities = set()
    for path in allowed_reads:
        metadata = os.stat(path, follow_symlinks=False)
        require(stat.S_ISREG(metadata.st_mode), "allowed_read_is_not_regular")
        allowed_file_identities.add((metadata.st_dev, metadata.st_ino))

    def audit(event, args):
        if event == "open":
            path, _mode, flags = args
            require(not flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND),
                    "proof_file_write_refused")
            if isinstance(path, int):
                # The unchanged CLI wraps its admitted os.open descriptor with
                # os.fdopen. Admit that second open by fixed file identity.
                metadata = os.fstat(path)
                require(stat.S_ISREG(metadata.st_mode)
                        and (metadata.st_dev, metadata.st_ino) in allowed_file_identities,
                        "unadmitted_runtime_descriptor")
            else:
                require(isinstance(path, (str, bytes, os.PathLike))
                        and os.fsdecode(path) in allowed_reads,
                        "unadmitted_runtime_read")
        if (event.startswith(("socket.", "subprocess.", "ctypes."))
                or event in {"os.system", "os.fork", "os.forkpty", "os.exec",
                             "os.posix_spawn", "os.spawn", "os.putenv", "os.unsetenv",
                             "os.listdir", "os.scandir", "os.mkdir", "os.remove",
                             "os.rename", "os.rmdir", "os.chmod"}):
            raise ProofRejected("external_effect_or_discovery_refused")

    sys.addaudithook(audit)
    return raw_files, inputs, stdlib_pins


def sentinel(name):
    def reject(*_args, **_kwargs):
        DYNAMIC_CALLS[name] += 1
        raise RuntimeError("dynamic_route_entered")
    return reject


def install_product(raw_files, mode):
    require(not any(name == "cryptalis" or name.startswith("cryptalis.")
                    for name in sys.modules), "preexisting_product_import")

    def load(name, relative, package=False):
        module = types.ModuleType(name)
        module.__file__ = str(BASE / relative)
        module.__package__ = name if package else name.rpartition(".")[0]
        if package:
            module.__path__ = []
        sys.modules[name] = module
        exec(compile(raw_files[relative], module.__file__, "exec"), module.__dict__)
        return module

    load("cryptalis", "copied-source/src/cryptalis/__init__.py", True)
    load("cryptalis.manifest", "copied-source/src/cryptalis/manifest/__init__.py", True)
    for leaf in ("parser", "canonical", "header", "declaration"):
        load("cryptalis.manifest." + leaf, "copied-source/src/cryptalis/manifest/" + leaf + ".py")
    compiler = types.ModuleType("cryptalis.manifest.compiler")
    compiler.compile_protection = sentinel("compiler")
    compiler.PlanningRejected = type("PlanningRejected", (Exception,), {})
    compiler.InspectionUnavailable = type("InspectionUnavailable", (Exception,), {})
    sys.modules[compiler.__name__] = compiler
    compatibility = types.ModuleType("cryptalis.manifest.compatibility")
    compatibility.CompatibilityInspectionUnavailable = type("CompatibilityInspectionUnavailable", (Exception,), {})
    sys.modules[compatibility.__name__] = compatibility
    for module_name, attribute, key in (
        ("cryptalis._doctor_setup", "inspect_setup", "setup"),
        ("cryptalis._doctor_ciphertext", "audit_snapshot", "ciphertext"),
    ):
        stub = types.ModuleType(module_name)
        setattr(stub, attribute, sentinel(key))
        sys.modules[module_name] = stub
    doctor_module = load("cryptalis.doctor", "copied-source/src/cryptalis/doctor.py")
    doctor_module._active_report = sentinel("active")
    cli_module = load("cryptalis.cli", VARIANTS[mode])
    return cli_module, doctor_module


def expected_report(valid, raw):
    # Independent expected values, not obtained from doctor or CLI helpers.
    checks = {name: {"status": "NOT_INSPECTED"} for name in CHECK_NAMES}
    if valid:
        checks["manifest"] = {"status": "CHECKED", "scope": "declaration_grammar_only",
                              "sha256": digest(raw), "model_count": 1}
    else:
        checks["manifest"] = {"status": "REJECTED", "code": "invalid_protection_declaration",
                              "remedy": REMEDY}
    return {
        "format": "cryptalis.doctor/v1", "phase": "pre_adoption", "effects": "NONE",
        "authority": "ADVISORY_NOT_AUTHENTICATED", "complete": False, "ready": False,
        "checks": checks,
        "limits": [
            "Native pre-adoption and active deployment metadata use distinct inspection modes.",
            "Writer completeness and value-domain reviews are host assertions, not independent discovery.",
            "Provider custody is not inspected; ciphertext authentication requires explicit active-mode opt-in and bounds.",
            "Read-only database inspection is not a sandbox for trusted host objects or engine callbacks.",
            "All seven production gates and actual query routing require separate qualification.",
        ],
    }


def expected_text(valid):
    manifest_line = "manifest: CHECKED\n" if valid else (
        "manifest: REJECTED (invalid_protection_declaration)\n"
        "  remedy: Supply a valid bounded cryptalis.protection/v1 declaration.\n")
    return ("Doctor: incomplete; no deployment qualification.\n" + manifest_line
            + "".join(name + ": NOT_INSPECTED\n" for name in CHECK_NAMES[1:])
            + "Dynamic inspection requires explicitly supplied host objects through cryptalis.doctor.doctor.\n")


def private_absent(*outputs):
    return all(marker not in output for output in outputs for marker in MARKERS)


class FailedWriter:
    def __init__(self, kind):
        self.kind = kind
        self.attempts = []

    def write(self, value):
        self.attempts.append(value)
        if self.kind == "write":
            raise OSError(errno.EIO, "PRIVATE_IO_MARKER")
        if self.kind == "short":
            return len(value) - 1
        return len(value)

    def flush(self):
        if self.kind == "flush":
            raise OSError(errno.EIO, "PRIVATE_IO_MARKER")

    def getvalue(self):
        return "".join(self.attempts)


def capture(cli, raw_files, fixture, machine_json=False, out_kind=None, err_kind=None):
    relative = "fixtures/PRIVATE_PATH_MARKER-" + fixture + ".json"
    require(read_regular(BASE / relative) == raw_files[relative], "fixture_changed_before_call")
    output = io.StringIO() if out_kind is None else FailedWriter(out_kind)
    errors = io.StringIO() if err_kind is None else FailedWriter(err_kind)
    old_output, old_errors = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = output, errors
        arguments = ["doctor", str(BASE / relative)]
        if machine_json:
            arguments.append("--json")
        code = cli.main(arguments)
    finally:
        sys.stdout, sys.stderr = old_output, old_errors
    require(read_regular(BASE / relative) == raw_files[relative], "fixture_changed_after_call")
    require(not any(DYNAMIC_CALLS.values()), "unexpected_dynamic_call")
    require(not any(name == "sqlalchemy" or name.startswith("sqlalchemy.")
                    or name == "psycopg" or name.startswith("psycopg.")
                    for name in sys.modules), "external_dependency_imported")
    stdout, stderr = output.getvalue(), errors.getvalue()
    require(len(stdout) + len(stderr) <= 16384, "captured_output_limit")
    return {"exit": code, "stdout": stdout, "stderr": stderr,
            "stdout_is_delivery_attempt": out_kind is not None,
            "stderr_is_delivery_attempt": err_kind is not None}


def run_cases(cli, doctor_module, raw_files):
    records = []

    def record(case_id, callback):
        started = time.monotonic()
        try:
            checks, observation = callback()
            passed = all(value is True for value in checks.values())
            result = {"id": case_id, "status": "PASS" if passed else "FAIL",
                      "checks": checks, "observation": observation}
        except Exception as failure:
            result = {"id": case_id, "status": "ERROR", "error_type": type(failure).__name__}
        result["wall_seconds"] = time.monotonic() - started
        records.append(result)
        emit({"event": "case", **result})

    def plain(fixture, valid):
        observed = capture(cli, raw_files, fixture)
        return ({"exit_exact": observed["exit"] == (3 if valid else 2),
                 "stderr_empty": observed["stderr"] == "",
                 "expected_text_exact": observed["stdout"] == expected_text(valid),
                 "redacted": private_absent(observed["stdout"], observed["stderr"])}, observed)

    def machine(fixture, valid):
        observed = capture(cli, raw_files, fixture, machine_json=True)
        expected = expected_report(valid, raw_files["fixtures/PRIVATE_PATH_MARKER-" + fixture + ".json"])
        serialized = json.dumps(expected, sort_keys=True, separators=(",", ":")) + "\n"
        return ({"exit_exact": observed["exit"] == (3 if valid else 2),
                 "stderr_empty": observed["stderr"] == "",
                 "expected_json_bytes_exact": observed["stdout"] == serialized,
                 "expected_json_value_exact": json.loads(observed["stdout"]) == expected,
                 "redacted": private_absent(observed["stdout"], observed["stderr"])}, observed)

    def output_failure(kind, double=False):
        observed = capture(cli, raw_files, "malformed", out_kind=kind,
                           err_kind="write" if double else None)
        checks = {"operational_exit": observed["exit"] == 4,
                  "safe_output_family": "CLI.OutputUnavailable" in observed["stderr"],
                  "no_traceback": "Traceback" not in observed["stderr"],
                  "redacted": private_absent(observed["stdout"], observed["stderr"])}
        if not double:
            checks["stdout_role"] = "output_role=stdout" in observed["stderr"]
            checks["exact_stage"] = ("stage=output_flush" if kind == "flush" else "stage=output_write") in observed["stderr"]
            checks["safe_cause"] = "cause=EIO" in observed["stderr"]
        return checks, observed

    record(CASE_IDS[0], lambda: plain("malformed", False))
    record(CASE_IDS[1], lambda: plain("wrong-schema", False))
    record(CASE_IDS[2], lambda: plain("valid", True))
    record(CASE_IDS[3], lambda: machine("malformed", False))
    record(CASE_IDS[4], lambda: machine("valid", True))
    record(CASE_IDS[5], lambda: output_failure("write"))
    record(CASE_IDS[6], lambda: output_failure("short"))
    record(CASE_IDS[7], lambda: output_failure("flush"))
    record(CASE_IDS[8], lambda: output_failure("write", True))

    def sentinel_control():
        targets = (doctor_module.compile_protection, doctor_module._active_report,
                   sys.modules["cryptalis._doctor_setup"].inspect_setup,
                   sys.modules["cryptalis._doctor_ciphertext"].audit_snapshot)
        caught = 0
        for target in targets:
            try:
                target()
            except RuntimeError:
                caught += 1
        counts = dict(DYNAMIC_CALLS)
        for key in DYNAMIC_CALLS:
            DYNAMIC_CALLS[key] = 0
        return ({"all_sentinels_raise": caught == 4,
                 "each_sentinel_recorded_once": all(value == 1 for value in counts.values())},
                {"caught": caught, "calls": counts})

    def collector_control():
        detected = {marker: not private_absent("known synthetic exposure: " + marker)
                    for marker in MARKERS}
        return ({"detects_each_injected_marker": all(detected.values()),
                 "accepts_safe_remedy": private_absent(REMEDY)},
                {"detected_marker_count": sum(detected.values())})

    record(CASE_IDS[9], sentinel_control)
    record(CASE_IDS[10], collector_control)
    require(tuple(item["id"] for item in records) == CASE_IDS, "executed_case_inventory_mismatch")
    return records


def enforce_limits():
    # No child process, temporary output tree or network is part of this proof.
    for kind, ceiling in ((resource.RLIMIT_CPU, 15),
                          (resource.RLIMIT_AS, 384 * 1024 * 1024),
                          (resource.RLIMIT_FSIZE, 2 * 1024 * 1024),
                          (resource.RLIMIT_NOFILE, 64)):
        old_soft, old_hard = resource.getrlimit(kind)
        hard = ceiling if old_hard == resource.RLIM_INFINITY else min(ceiling, old_hard)
        resource.setrlimit(kind, (hard, hard))

    def expired(_signum, _frame):
        raise ProofRejected("unit_wall_deadline_exceeded")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 20)


def main():
    require(len(sys.argv) == 3 and sys.argv[1] in VARIANTS,
            "explicit_variant_and_input_anchor_required")
    require(re.fullmatch(r"[0-9a-f]{64}", sys.argv[2]) is not None,
            "invalid_external_input_anchor")
    mode = sys.argv[1]
    started = time.monotonic()
    enforce_limits()
    raw_files, inputs, stdlib_pins = preflight(mode, sys.argv[2])
    emit({"event": "selection", "variant": mode, "case_ids": CASE_IDS,
          "source_module_count": len(SOURCE_FILES), "stdlib_file_count": len(stdlib_pins),
          "inputs_sha256": sys.argv[2], "dynamic_dependencies": "explicit_fail_fast_unit_stubs",
          "boundary": "actual_CLI_callable_real_doctor_real_declaration_parser"})
    cli, doctor_module = install_product(raw_files, mode)
    records = run_cases(cli, doctor_module, raw_files)
    # Recheck every proof input after observations; never write original sources.
    for relative, expected in inputs.items():
        require(digest(read_regular(BASE / relative)) == expected, "proof_input_changed_after_run")
    require(not os.path.lexists(ROOT + "/no-bytecode-use"), "unexpected_bytecode_artifact")
    require(not any(DYNAMIC_CALLS.values()), "dynamic_call_count_not_zero")
    failed = [item["id"] for item in records if item["status"] == "FAIL"]
    errors = [item["id"] for item in records if item["status"] == "ERROR"]
    expected_red = list(CASE_IDS[:2]) if mode in ("baseline-red", "omission-mutant") else []
    usage = resource.getrusage(resource.RUSAGE_SELF)
    emit({"event": "terminal", "variant": mode, "executed": len(records),
          "passed": sum(item["status"] == "PASS" for item in records),
          "failed_ids": failed, "error_ids": errors, "expected_red_ids": expected_red,
          "matches_planned_pattern": failed == expected_red and not errors,
          "wall_seconds": time.monotonic() - started, "peak_rss_kib": usage.ru_maxrss,
          "user_cpu_seconds": usage.ru_utime, "system_cpu_seconds": usage.ru_stime,
          "dynamic_calls": DYNAMIC_CALLS, "postrun_inputs_unchanged": True,
          "no_production_or_installed_integration_claim": True})
    signal.setitimer(signal.ITIMER_REAL, 0)
    # Expected RED remains exit 1; it is never relabeled as an ordinary pass.
    return 1 if failed or errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as failure:
        emit({"event": "harness_error", "error_type": type(failure).__name__,
              "failure_code": failure.code if isinstance(failure, ProofRejected) else None,
              "observations_not_accepted": True})
        raise SystemExit(2)
