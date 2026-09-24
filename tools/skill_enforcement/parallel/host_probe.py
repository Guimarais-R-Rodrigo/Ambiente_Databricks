from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def _version(command: list[str]) -> str | None:
    try: p = subprocess.run(command, capture_output=True, text=True, timeout=10, shell=False)
    except (OSError, subprocess.SubprocessError): return None
    lines = (p.stdout or p.stderr or "").strip().splitlines()
    return lines[0][:200] if p.returncode == 0 and lines else None


def _filesystem() -> dict:
    result = {"family": "windows" if os.name == "nt" else "posix", "type": "NOT_OBSERVED"}
    if os.name != "nt": return result
    drive = Path.cwd().drive or str(Path.cwd().anchor).rstrip("\\")
    if not drive: return result
    try:
        p = subprocess.run(["fsutil", "fsinfo", "volumeinfo", drive], capture_output=True, text=True, timeout=10, shell=False)
    except (OSError, subprocess.SubprocessError): return result
    if p.returncode == 0:
        upper = (p.stdout or "").upper()
        for kind in ("NTFS", "REFS", "FAT32", "EXFAT"):
            if kind in upper: result["type"] = kind; break
    return result


def probe() -> dict:
    return {
        "schema_version": "SER-PARALLEL-HOST-2",
        "os": platform.system(), "release": platform.release(), "machine": platform.machine(),
        "python": sys.version.split()[0], "git": _version(["git", "--version"]),
        "node": _version(["node", "--version"]), "pnpm": _version(["pnpm", "--version"]),
        "filesystem": _filesystem(),
        "sandbox_enforcement": "NOT_PROVEN_BY_HOST_PROBE",
        "client_model_configuration": "NOT_OBSERVED_BY_HOST_PROBE",
        "credential_material_recorded": False,
    }


def main() -> int:
    print(json.dumps(probe(), ensure_ascii=False, indent=2, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
