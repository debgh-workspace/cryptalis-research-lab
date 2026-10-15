"""Read only the explicitly requested Python-startup environment facts.

Root supplies one of two fixed Popen environment maps. No inherited environment
values may be supplied. No project or installed dependency is imported.
"""

import sys

if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit(2)
if sys.pycache_prefix != "/workspace/scratch/cb28ee9f5f4a/cryptalis-executable/experiments/preview-doctor-dx-slice-20261015/startup-diagnostic-v1/no-bytecode-use":
    raise SystemExit(2)
if len(sys.argv) != 2 or sys.argv[1] not in ("empty", "fixed-locale"):
    raise SystemExit(2)

import json
import os

supplied = {} if sys.argv[1] == "empty" else {"LC_ALL": "C.UTF-8"}
known_augmentation = {**supplied, "LC_CTYPE": "C.UTF-8"}
print(json.dumps({
    "environment_keys": sorted(os.environ),
    "matches_supplied_fixed_map": dict(os.environ) == supplied,
    "matches_known_locale_augmentation": dict(os.environ) == known_augmentation,
}, sort_keys=True, separators=(",", ":")), flush=True)
