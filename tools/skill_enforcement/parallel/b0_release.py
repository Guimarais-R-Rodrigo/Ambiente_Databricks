from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .bundle import build_evidence_envelope, verify_evidence_envelope
from .coverage import inventory
from .host_probe import probe
from .pilot_verify import verify as verify_pilot
from .prepare_pilot import prepare

ROOT = Path(__file__).resolve().parents[3]


def _run(argv: list[str]) -> dict:
    p = subprocess.run(argv, cwd=ROOT, capture_output=True)
    return {
        "argv": argv,
        "exit_code": p.returncode,
        "stdout": p.stdout or b"",
        "stderr": p.stderr or b"",
    }


def _write_json(path: Path, payload: dict) -> None:
    path.write_bytes(
        (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    )


def _write_run(raw: Path, stem: str, run: dict) -> None:
    (raw / f"{stem}.stdout.txt").write_bytes(run["stdout"])
    (raw / f"{stem}.stderr.txt").write_bytes(run["stderr"])


def _finalize(output_dir: Path, raw: Path, core: dict) -> dict:
    _write_json(raw / "core_qualification.json", core)
    substitutions = {
        str(ROOT): "<REPO_ROOT>",
        str(Path.home()): "<HOME>",
    }
    try:
        envelope = build_evidence_envelope(output_dir, substitutions)
        verification = verify_evidence_envelope(output_dir)
    except Exception as exc:
        return {
            **core,
            "status": "FAIL",
            "release_status": "NOT_QUALIFIED",
            "first_failure": core.get("first_failure") or "evidence_envelope",
            "evidence_envelope": {
                "valid": False,
                "issues": [f"ENVELOPE_EXCEPTION:{type(exc).__name__}:{exc}"],
            },
        }
    final = {
        **core,
        "evidence_envelope": {
            "valid": verification["valid"],
            "issues": verification["issues"],
            "layout": envelope,
        },
    }
    if not verification["valid"]:
        final["status"] = "FAIL"
        final["release_status"] = "NOT_QUALIFIED"
        final["first_failure"] = core.get("first_failure") or "evidence_envelope"
    return final


def qualify(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=False)
    raw = output_dir / "RAW"
    raw.mkdir()
    checks: list[dict] = []

    meta = _run([sys.executable, "-B", "-m", "unittest", "tools.tests.test_ser_parallel_b0", "-v"])
    checks.append({"name": "metatests", "exit_code": meta["exit_code"]})
    _write_run(raw, "metatests", meta)
    if meta["exit_code"] != 0:
        return _finalize(
            output_dir,
            raw,
            {
                "status": "FAIL",
                "release_status": "NOT_QUALIFIED",
                "first_failure": "metatests",
                "checks": checks,
            },
        )

    cov = inventory()
    _write_json(raw / "coverage.json", cov)
    checks.append({"name": "coverage", "exit_code": 0 if cov["status"] == "PASS" else 1})
    if cov["status"] != "PASS":
        return _finalize(
            output_dir,
            raw,
            {
                "status": "FAIL",
                "release_status": "NOT_QUALIFIED",
                "first_failure": "coverage",
                "checks": checks,
            },
        )

    host = probe()
    _write_json(raw / "host.json", host)
    checks.append({"name": "host_probe", "exit_code": 0})

    for scenario in ("selective", "global"):
        campaign_path = raw / f"pilot_{scenario}.prepared.json"
        try:
            campaign = prepare(campaign_path, scenario)
        except Exception as exc:
            return _finalize(
                output_dir,
                raw,
                {
                    "status": "FAIL",
                    "release_status": "NOT_QUALIFIED",
                    "first_failure": f"pilot_{scenario}_prepare",
                    "checks": checks,
                    "host": host,
                    "prepare_error": f"{type(exc).__name__}:{exc}",
                },
            )

        evidence = raw / f"pilot_{scenario}_evidence"
        launch = _run(
            [
                sys.executable,
                "-B",
                "-m",
                "tools.skill_enforcement.parallel.launcher",
                "--campaign",
                str(campaign_path),
                "--evidence-dir",
                str(evidence),
            ]
        )
        checks.append(
            {
                "name": f"pilot_{scenario}_launcher_expected_exit_1",
                "exit_code": launch["exit_code"],
            }
        )
        _write_run(raw, f"pilot_{scenario}", launch)
        if launch["exit_code"] != 1:
            return _finalize(
                output_dir,
                raw,
                {
                    "status": "FAIL",
                    "release_status": "NOT_QUALIFIED",
                    "first_failure": f"pilot_{scenario}_launcher_exit",
                    "checks": checks,
                    "host": host,
                },
            )

        summary_path = evidence / "summary.json"
        if not summary_path.is_file():
            return _finalize(
                output_dir,
                raw,
                {
                    "status": "FAIL",
                    "release_status": "NOT_QUALIFIED",
                    "first_failure": f"pilot_{scenario}_summary_missing",
                    "checks": checks,
                    "host": host,
                },
            )
        try:
            summary = json.loads(summary_path.read_bytes().decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            return _finalize(
                output_dir,
                raw,
                {
                    "status": "FAIL",
                    "release_status": "NOT_QUALIFIED",
                    "first_failure": f"pilot_{scenario}_summary_invalid",
                    "checks": checks,
                    "host": host,
                    "summary_error": f"{type(exc).__name__}:{exc}",
                },
            )

        pilot = verify_pilot(summary, scenario, campaign=campaign, evidence_root=evidence)
        _write_json(raw / f"pilot_{scenario}_verification.json", pilot)
        checks.append(
            {
                "name": f"pilot_{scenario}_verifier",
                "exit_code": 0 if pilot["valid"] else 1,
            }
        )
        if not pilot["valid"]:
            return _finalize(
                output_dir,
                raw,
                {
                    "status": "FAIL",
                    "release_status": "NOT_QUALIFIED",
                    "first_failure": f"pilot_{scenario}_verifier",
                    "checks": checks,
                    "host": host,
                },
            )

    windows_ntfs = host.get("os") == "Windows" and (host.get("filesystem") or {}).get("type") == "NTFS"
    sandbox_proven = host.get("sandbox_enforcement") != "NOT_PROVEN_BY_HOST_PROBE"
    release = "LOCAL_QUALIFIED" if windows_ntfs and sandbox_proven else "PENDING_HOST_QUALIFICATION"
    core = {
        "status": "PASS",
        "release_status": release,
        "first_failure": None,
        "checks": checks,
        "host": host,
        "release_scope": "MECHANISM_QUALIFICATION_ONLY_NO_SKILL_PROMOTION",
    }
    return _finalize(output_dir, raw, core)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    result = qualify(args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
