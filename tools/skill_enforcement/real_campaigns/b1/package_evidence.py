from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from tools.skill_enforcement.parallel.bundle import (
    build_share,
    default_share_substitutions,
    write_manifest,
)
from tools.skill_enforcement.parallel.process import ROOT
from tools.skill_enforcement.parallel.verifier import verify_raw_share_binding
from tools.skill_enforcement.real_campaigns.b1.prepare import validate_output_location


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _deterministic_zip(source: Path, target: Path) -> None:
    if target.exists():
        raise RuntimeError("B1_SHARE_ZIP_MUST_BE_NEW")
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(x for x in source.rglob("*") if x.is_file()):
            rel = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes())


def package(output_dir: Path) -> dict:
    raw_root = validate_output_location(output_dir)
    if not raw_root.is_dir():
        raise RuntimeError("B1_RAW_OUTPUT_NOT_FOUND")
    required = [
        "ROUND_START.json", "RELEASE_SPEC.json", "CAMPAIGN.json",
        "HANDOFF.json", "CODEX_HANDOFF.md", "ADAPTER_RESULT.json",
    ]
    missing = [name for name in required if not (raw_root / name).is_file()]
    if missing:
        raise RuntimeError("B1_RAW_REQUIRED_MISSING:" + ",".join(missing))
    adapter_result = json.loads((raw_root / "ADAPTER_RESULT.json").read_text(encoding="utf-8"))
    if not isinstance(adapter_result, dict) or not isinstance(adapter_result.get("status"), str):
        raise RuntimeError("B1_ADAPTER_RESULT_INVALID")

    write_manifest(raw_root)
    share_root = raw_root.parent / (raw_root.name + "_SHARE")
    binding_path = raw_root.parent / (raw_root.name + "_RAW_SHARE_BINDING.json")
    envelope_path = raw_root.parent / (raw_root.name + "_ENVELOPE_VERIFICATION.json")
    verdict_path = raw_root.parent / (raw_root.name + "_P2_PACKAGE_VERDICT.json")
    share_zip = raw_root.parent / (raw_root.name + "_SHARE.zip")
    for path in (share_root, binding_path, envelope_path, verdict_path, share_zip):
        if path.exists():
            raise RuntimeError("B1_PACKAGE_SIBLING_MUST_BE_NEW:" + str(path))

    build_share(
        raw_root,
        share_root,
        default_share_substitutions(ROOT),
        binding_path=binding_path,
    )
    envelope = verify_raw_share_binding(raw_root, share_root, binding_path)
    envelope_path.write_text(
        json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    _deterministic_zip(share_root, share_zip)
    verdict = {
        "schema_version": "SER-B1-P2-PACKAGE-VERDICT-1",
        "status": "PASS" if envelope.get("valid") is True else "FAIL",
        "campaign_status": adapter_result.get("status"),
        "candidate_sha": adapter_result.get("candidate_sha"),
        "evidence_envelope_valid": envelope.get("valid") is True,
        "evidence_envelope_issues": envelope.get("issues") or [],
        "raw_manifest_sha256": _sha256(raw_root / "MANIFEST.json"),
        "share_manifest_sha256": _sha256(share_root / "MANIFEST.json"),
        "binding_sha256": _sha256(binding_path),
        "envelope_verification_sha256": _sha256(envelope_path),
        "share_zip_sha256": _sha256(share_zip),
        "raw_is_private": True,
        "upload_artifact": str(share_zip),
        "promotion_authorized": False,
        "ready_authorized": False,
        "merge_authorized": False,
    }
    verdict_path.write_text(
        json.dumps(verdict, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return verdict


def main() -> int:
    parser = argparse.ArgumentParser(description="Build sanitized P2 SHARE evidence from the immutable local B1 output")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        verdict = package(args.output_dir)
    except Exception as exc:
        verdict = {"status": "FAIL", "issues": [type(exc).__name__ + ":" + str(exc)]}
    print(json.dumps(verdict, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if verdict.get("status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
