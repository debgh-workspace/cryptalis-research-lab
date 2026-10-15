# Minimal Python startup diagnostic

Status: NOT EXECUTED. Preserve proof-v1, its input seal and the failed baseline
receipt. No product or proof-v1 file is changed by this diagnostic proposal.

The retained root launcher explicitly passed `env={}` to `subprocess.Popen`.
Proof-v1 rejected the child's nonempty environment before any case. That is the
established failure; Python locale coercion is only a hypothesis until this
diagnostic runs.

After independent review, root may select exactly two predetermined diagnostic
children, one at a time, with no inherited environment:

- Interpreter: `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python3.12`
- Interpreter SHA-256: `fa67443527ed9647f760d807e2a38f26340757123e643c4639cf273ed15d5ea7`
- Arguments: `-I -B -S -X` followed by
  `pycache_prefix=/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/preview-doctor-dx-slice-20261015/startup-diagnostic-v1/no-bytecode-use`
  and the absolute path to this directory's `startup_probe.py`, followed by
  exactly one mode argument below.
- Working directory: this diagnostic directory.
- First mode `empty`: launch with `subprocess.Popen(..., env={}, ...)`.
- Second mode `fixed-locale`: launch with
  `subprocess.Popen(..., env={"LC_ALL": "C.UTF-8"}, ...)`.
- Do not inherit environment variables, set additional keys, or change values.
- Require the bytecode-prefix path absent before/after. Verify the externally
  handed-off diagnostic source hash before launch.
- Root captures fresh stdout/stderr and the exit status. Use a 5-second wall
  deadline and 16-KiB output limit per child, with no retry or proof variant.

The child emits sorted environment key names and two booleans: exact equality
with the supplied fixed map, and exact equality with that map plus the known
`LC_CTYPE=C.UTF-8` augmentation. It emits no arbitrary environment values,
interpreter configuration dump or project information. Only `sys`, `json` and
`os` are imported. A flag or selector mismatch exits 2 without output.

## Proposed correction, conditional on actual observation

If `empty` reports exactly `["LC_CTYPE"]` with only the known-augmentation
equality true, that establishes the specific startup effect in this invocation.
If `fixed-locale` reports exactly `["LC_ALL"]` with supplied-map equality true
and known-augmentation equality false, prefer a new proof-v2 derivative whose
root launcher explicitly supplies `env={"LC_ALL": "C.UTF-8"}` and whose child
requires exact equality with that same one-key map. Reject every additional key
and every other value. This makes the locale an explicit nonsecret input rather
than accepting an unspecified startup mutation.

Do not implement this conditional correction before both diagnostic results
are independently accepted. If the output differs, HOLD and report it; do not
use a general environment whitelist or silently weaken the original assertion.
No CLI patch, case oracle, source module, variant, dependency boundary or
security contract needs to change for this proposed correction.
