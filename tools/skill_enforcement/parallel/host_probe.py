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
    if os.name != "nt":
        return result
    try:
        import ctypes
        from ctypes import wintypes as w
        root = Path.cwd().anchor
        if not root:
            return result
        fs_name = ctypes.create_unicode_buffer(261)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        fn = kernel32.GetVolumeInformationW
        fn.argtypes = [
            w.LPCWSTR, w.LPWSTR, w.DWORD, ctypes.POINTER(w.DWORD),
            ctypes.POINTER(w.DWORD), ctypes.POINTER(w.DWORD), w.LPWSTR, w.DWORD,
        ]
        fn.restype = w.BOOL
        serial = w.DWORD()
        max_component = w.DWORD()
        flags = w.DWORD()
        ok = fn(root, None, 0, ctypes.byref(serial), ctypes.byref(max_component), ctypes.byref(flags), fs_name, len(fs_name))
        if ok and fs_name.value:
            result["type"] = fs_name.value.upper()
            result["observed_by"] = "GetVolumeInformationW"
    except (OSError, AttributeError, ValueError):
        pass
    return result


def probe() -> dict:
    return {
        "schema_version": "SER-PARALLEL-HOST-2",
        "os": platform.system(), "release": platform.release(), "machine": platform.machine(),
        "python": sys.version.split()[0], "git": _version(["git", "--version"]),
        "node": _version(["node", "--version"]), "pnpm": _version(["pnpm", "--version"]),
        "filesystem": _filesystem(),
        "sandbox_enforcement": "PYTHON_AUDIT_SCRATCH_ONLY_TASKS_REQUIRES_NEGATIVE_PROBE",
        "client_model_configuration": "NOT_APPLICABLE_B0_DETERMINISTIC_PYTHON_RUNTIME",
        "credential_material_recorded": False,
    }


def main() -> int:
    print(json.dumps(probe(), ensure_ascii=False, indent=2, sort_keys=True)); return 0

if __name__ == "__main__": raise SystemExit(main())
