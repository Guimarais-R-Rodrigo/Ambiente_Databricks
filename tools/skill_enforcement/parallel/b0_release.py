from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .bundle import build_share, write_manifest
from .coverage import inventory
from .host_probe import probe
from .pilot_verify import verify as verify_pilot
from .prepare_pilot import prepare
from .verifier import verify_raw_share_binding

ROOT = Path(__file__).resolve().parents[3]


def _decode(data: bytes) -> str:
    return data.decode("utf-8", errors="replace")


def _run(argv: list[str]) -> dict:
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=1800)
    return {"argv": argv, "exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def _write_run(output_dir: Path, stem: str, run: dict) -> None:
    (output_dir / f"{stem}.stdout.txt").write_bytes(run["stdout"])
    (output_dir / f"{stem}.stderr.txt").write_bytes(run["stderr"])


def _finish(output_dir: Path, result: dict) -> dict:
    mechanism_path = output_dir / "MECHANISM_RESULT.json"
    mechanism_path.write_bytes((json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    write_manifest(output_dir)

    share_root = output_dir.parent / f"{output_dir.name}_SHARE"
    binding_path = output_dir.parent / f"{output_dir.name}_RAW_SHARE_BINDING.json"
    envelope_path = output_dir.parent / f"{output_dir.name}_ENVELOPE_VERIFICATION.json"
    try:
        build_share(output_dir, share_root, {}, binding_path=binding_path)
        envelope = verify_raw_share_binding(output_dir, share_root, binding_path)
    except Exception as exc:
        envelope = {"valid": False, "issues": [f"EVIDENCE_ENVELOPE_EXCEPTION:{type(exc).__name__}:{exc}"]}
    envelope_path.write_bytes((json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))

    final = dict(result)
    final["evidence_envelope"] = {
        "raw_root": str(output_dir),
        "share_root": str(share_root),
        "binding_path": str(binding_path),
        "verification_path": str(envelope_path),
        "valid": envelope.get("valid") is True,
        "issues": envelope.get("issues") or [],
    }
    if envelope.get("valid") is not True:
        final["status"] = "FAIL"
        final["release_status"] = "NOT_QUALIFIED"
        final["first_failure"] = final.get("first_failure") or "evidence_envelope"
    return final


def qualify(output_dir: Path) -> dict:
    share_root = output_dir.parent / f"{output_dir.name}_SHARE"
    binding_path = output_dir.parent / f"{output_dir.name}_RAW_SHARE_BINDING.json"
    envelope_path = output_dir.parent / f"{output_dir.name}_ENVELOPE_VERIFICATION.json"
    if output_dir.exists() or share_root.exists() or binding_path.exists() or envelope_path.exists():
        return {
            "status": "FAIL", "release_status": "NOT_QUALIFIED",
            "first_failure": "evidence_destination_not_new", "checks": [],
        }

    output_dir.mkdir(parents=True, exist_ok=False)
    checks = []

    meta = _run([sys.executable, "-B", "-m", "unittest", "tools.tests.test_ser_parallel_b0", "-v"])
    checks.append({"name": "metatests", "exit_code": meta["exit_code"]})
    _write_run(output_dir, "metatests", meta)
    if meta["exit_code"] != 0:
        return _finish(output_dir, {"status": "FAIL", "release_status": "NOT_QUALIFIED", "first_failure": "metatests", "checks": checks})

    cov = inventory()
    (output_dir / "coverage.json").write_bytes((json.dumps(cov, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    checks.append({"name": "coverage", "exit_code": 0 if cov["status"] == "PASS" else 1})
    if cov["status"] != "PASS":
        return _finish(output_dir, {"status": "FAIL", "release_status": "NOT_QUALIFIED", "first_failure": "coverage", "checks": checks})

    host = probe()
    (output_dir / "host.json").write_bytes((json.dumps(host, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    checks.append({"name": "host_probe", "exit_code": 0})

    for scenario in ("selective", "global"):
        campaign_path = output_dir / f"pilot_{scenario}.prepared.json"
        prepare(campaign_path, scenario)
        evidence = output_dir / f"pilot_{scenario}_evidence"
        launch = _run([
            sys.executable, "-B", "-m", "tools.skill_enforcement.parallel.launcher",
            "--campaign", str(campaign_path), "--evidence-dir", str(evidence),
        ])
        checks.append({"name": f"pilot_{scenario}_launcher_expected_1", "exit_code": launch["exit_code"]})
        _write_run(output_dir, f"pilot_{scenario}", launch)
        if launch["exit_code"] != 1:
            return _finish(output_dir, {
                "status": "FAIL", "release_status": "NOT_QUALIFIED",
                "first_failure": f"pilot_{scenario}_launcher_exit", "checks": checks, "host": host,
            })

        summary_path = evidence / "summary.json"
        if not summary_path.is_file():
            return _finish(output_dir, {
                "status": "FAIL", "release_status": "NOT_QUALIFIED",
                "first_failure": f"pilot_{scenario}_summary_missing", "checks": checks, "host": host,
            })
        pilot = verify_pilot(json.loads(summary_path.read_text(encoding="utf-8")), scenario)
        (output_dir / f"pilot_{scenario}_verification.json").write_bytes(
            (json.dumps(pilot, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
        )
        checks.append({"name": f"pilot_{scenario}_verifier", "exit_code": 0 if pilot["valid"] else 1})
        if not pilot["valid"]:
            return _finish(output_dir, {
                "status": "FAIL", "release_status": "NOT_QUALIFIED",
                "first_failure": f"pilot_{scenario}_verifier", "checks": checks, "host": host,
            })

    sandbox_pending = host["sandbox_enforcement"] == "NOT_PROVEN_BY_HOST_PROBE"
    fs_pending = host["os"] == "Windows" and host["filesystem"]["type"] != "NTFS"
    release = "PENDING_HOST_QUALIFICATION" if sandbox_pending or fs_pending else "LOCAL_QUALIFIED"
    return _finish(output_dir, {
        "status": "PASS",
        "release_status": release,
        "first_failure": None,
        "checks": checks,
        "host": host,
        "release_scope": "MECHANISM_QUALIFICATION_ONLY_NO_SKILL_PROMOTION",
    })


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", required=True, type=Path)
    a = p.parse_args()
    result = qualify(a.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
