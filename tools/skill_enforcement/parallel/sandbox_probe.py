from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
from pathlib import Path


def _blocked(callback) -> bool:
    try:
        callback()
    except PermissionError:
        return True
    return False


def main() -> int:
    scratch = Path(os.environ["TEMP"]).resolve()
    target_raw = os.environ.get("SER_B0_SANDBOX_PROBE_TARGET")
    if not target_raw:
        print(json.dumps({"status": "FAIL", "issues": ["PROBE_TARGET_MISSING"]}, sort_keys=True))
        return 2
    target = Path(target_raw).resolve()

    allowed = scratch / "allowed.txt"
    allowed.write_text("scratch-ok", encoding="utf-8")
    scratch_write_allowed = allowed.read_text(encoding="utf-8") == "scratch-ok"

    outside_write_blocked = _blocked(lambda: target.write_text("mutated", encoding="utf-8"))
    subprocess_blocked = _blocked(
        lambda: subprocess.run([sys.executable, "-c", "print('unexpected')"], check=False)
    )

    def connect():
        sock = socket.socket()
        try:
            sock.settimeout(0.2)
            sock.connect(("127.0.0.1", 9))
        finally:
            sock.close()

    network_blocked = _blocked(connect)
    credential_sentinel_absent = os.environ.get("SER_B0_SECRET_SENTINEL") is None

    checks = {
        "scratch_write_allowed": scratch_write_allowed,
        "outside_write_blocked": outside_write_blocked,
        "subprocess_blocked": subprocess_blocked,
        "network_blocked": network_blocked,
        "credential_sentinel_absent": credential_sentinel_absent,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    print(json.dumps({"schema_version": "SER-B0-SANDBOX-PROBE-1", "status": status, **checks}, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
