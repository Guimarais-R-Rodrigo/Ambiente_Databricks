from __future__ import annotations

import json
import os
import platform
import subprocess
import sys

def _version(command: list[str]) -> str | None:
    try:
        p = subprocess.run(command, capture_output=True, text=True, timeout=10, shell=False)
    except (OSError, subprocess.SubprocessError):
        return None
    text = (p.stdout or p.stderr or "").strip().splitlines()
    return text[0][:200] if p.returncode == 0 and text else None

def probe() -> dict:
    return {
        "schema_version": "SER-PARALLEL-HOST-1",
        "os": platform.system(),
        "release": platform.release(),
        "python": sys.version.split()[0],
        "git": _version(["git", "--version"]),
        "node": _version(["node", "--version"]),
        "pnpm": _version(["pnpm", "--version"]),
        "filesystem_semantics": "windows" if os.name == "nt" else "posix",
        "sandbox_enforcement": "NOT_PROVEN_BY_HOST_PROBE",
        "credential_material_recorded": False,
    }

def main() -> int:
    print(json.dumps(probe(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
