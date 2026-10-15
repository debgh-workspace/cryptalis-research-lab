"""Held actual-dependency CLI regression; source only, never run or collected here.

First six nodes use real public CLI.main and real doctor/parser/dependencies.
The seventh additionally checks a real installed python -m cryptalis process.
No dependency stubs, product monkeypatches, database fixture imports or host
objects are used. Run only through a separately accepted guarded stage.
"""

import hashlib
import json
import subprocess
import sys

import pytest


VALID = (
    b'{"schema":"cryptalis.protection/v1","profile":"cf1",'
    b'"domain_id":"10000000-0000-0000-0000-000000000001",'
    b'"models":[{"model":"Synthetic","table_id":'
    b'"20000000-0000-0000-0000-000000000001",'
    b'"tenancy":{"single_tenant":true},"fields":[{"name":"value",'
    b'"field_id":"30000000-0000-0000-0000-000000000001",'
    b'"protect":true,"queries":[],"accept_leakage":[]}]}]}'
)
INVALID = (
    pytest.param(b'{"PRIVATE_MALFORMED":', "PRIVATE_MALFORMED", id="malformed"),
    pytest.param(
        VALID.replace(b"cryptalis.protection/v1", b"PRIVATE_UNSUPPORTED_SCHEMA"),
        "PRIVATE_UNSUPPORTED_SCHEMA",
        id="unsupported-schema",
    ),
)
CHECKS = (
    "manifest", "setup", "native_admission", "deployment", "compatibility",
    "roles", "provider", "ciphertext",
)
REMEDY = "Supply a valid bounded cryptalis.protection/v1 declaration."
BANNER = "Doctor: incomplete; no deployment qualification.\n"
NOTICE = (
    "Dynamic inspection requires explicitly supplied host objects through "
    "cryptalis.doctor.doctor.\n"
)
REJECTED_TEXT = (
    BANNER
    + "manifest: REJECTED (invalid_protection_declaration)\n"
    + "  remedy: " + REMEDY + "\n"
    + "\n".join(name + ": NOT_INSPECTED" for name in CHECKS[1:])
    + "\n" + NOTICE
)
VALID_TEXT = (
    BANNER + "manifest: CHECKED\n"
    + "\n".join(name + ": NOT_INSPECTED" for name in CHECKS[1:])
    + "\n" + NOTICE
)


def expected_report(valid):
    checks = {name: {"status": "NOT_INSPECTED"} for name in CHECKS}
    checks["manifest"] = (
        {
            "status": "CHECKED", "scope": "declaration_grammar_only",
            "sha256": hashlib.sha256(VALID).hexdigest(), "model_count": 1,
        }
        if valid else {
            "status": "REJECTED", "code": "invalid_protection_declaration",
            "remedy": REMEDY,
        }
    )
    return {
        "format": "cryptalis.doctor/v1", "phase": "pre_adoption",
        "effects": "NONE", "authority": "ADVISORY_NOT_AUTHENTICATED",
        "complete": False, "ready": False, "checks": checks,
        "limits": [
            "Native pre-adoption and active deployment metadata use distinct inspection modes.",
            "Writer completeness and value-domain reviews are host assertions, not independent discovery.",
            "Provider custody is not inspected; ciphertext authentication requires explicit active-mode opt-in and bounds.",
            "Read-only database inspection is not a sandbox for trusted host objects or engine callbacks.",
            "All seven production gates and actual query routing require separate qualification.",
        ],
    }


def invoke(tmp_path, capsys, record_property, raw, machine_json=False):
    from cryptalis.cli import main

    # Observe a known exposure in both collectors before testing non-echo.
    marker = "COLLECTOR_PRIVATE_MARKER"
    print(marker)
    print(marker, file=sys.stderr)
    control = capsys.readouterr()
    assert control.out == control.err == marker + "\n"
    path = tmp_path / "PRIVATE_INPUT_FILENAME.json"
    path.write_bytes(raw)
    code = main(["doctor", str(path)] + (["--json"] if machine_json else []))
    captured = capsys.readouterr()
    record_property("doctor_cli_actual", json.dumps({
        "exit_code": code, "stdout": captured.out, "stderr": captured.err,
        "input_sha256_before": hashlib.sha256(raw).hexdigest(),
        "input_sha256_after": hashlib.sha256(path.read_bytes()).hexdigest(),
        "mode": "json" if machine_json else "text",
    }, sort_keys=True))
    assert path.read_bytes() == raw
    assert captured.err == ""
    assert "PRIVATE_INPUT_FILENAME" not in captured.out
    return code, captured.out


@pytest.mark.parametrize(("raw", "private_marker"), INVALID)
def test_rejected_text_has_safe_remedy(tmp_path, capsys, record_property, raw, private_marker):
    code, output = invoke(tmp_path, capsys, record_property, raw)
    assert code == 2
    assert private_marker not in output
    assert output == REJECTED_TEXT
    assert output.count("  remedy: ") == 1


@pytest.mark.parametrize(("raw", "private_marker"), INVALID)
def test_rejected_json_is_unchanged(tmp_path, capsys, record_property, raw, private_marker):
    code, output = invoke(tmp_path, capsys, record_property, raw, machine_json=True)
    expected = expected_report(False)
    assert code == 2
    assert private_marker not in output
    assert json.loads(output) == expected
    assert output == json.dumps(expected, sort_keys=True, separators=(",", ":")) + "\n"


def test_valid_text_is_unchanged(tmp_path, capsys, record_property):
    code, output = invoke(tmp_path, capsys, record_property, VALID)
    assert code == 3
    assert output == VALID_TEXT
    assert "remedy:" not in output


def test_valid_json_is_unchanged(tmp_path, capsys, record_property):
    code, output = invoke(tmp_path, capsys, record_property, VALID, machine_json=True)
    expected = expected_report(True)
    assert code == 3
    assert json.loads(output) == expected
    assert output == json.dumps(expected, sort_keys=True, separators=(",", ":")) + "\n"


def test_installed_module_process_has_safe_remedy(tmp_path, record_property):
    """Installed stage only: isolated interpreter excludes source PYTHONPATH."""
    path = tmp_path / "PRIVATE_INPUT_FILENAME.json"
    raw = b'{"PRIVATE_MALFORMED":'
    path.write_bytes(raw)
    result = subprocess.run(
        [sys.executable, "-I", "-B", "-m", "cryptalis", "doctor", str(path)],
        cwd=tmp_path,
        env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "TZ": "UTC"},
        capture_output=True,
        check=False,
        timeout=10,
    )
    record_property("doctor_cli_actual", json.dumps({
        "exit_code": result.returncode,
        "stdout_hex": result.stdout.hex(), "stderr_hex": result.stderr.hex(),
        "input_sha256_before": hashlib.sha256(raw).hexdigest(),
        "input_sha256_after": hashlib.sha256(path.read_bytes()).hexdigest(),
        "mode": "installed-process-text",
    }, sort_keys=True))
    assert result.returncode == 2
    assert result.stderr == b""
    assert result.stdout == REJECTED_TEXT.encode("utf-8")
    assert b"PRIVATE_MALFORMED" not in result.stdout + result.stderr
    assert b"PRIVATE_INPUT_FILENAME" not in result.stdout + result.stderr
    assert path.read_bytes() == raw
