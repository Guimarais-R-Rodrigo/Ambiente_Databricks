from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from tools.skill_enforcement.parallel.bundle import (
    build_share,
    default_share_substitutions,
    scan_share,
    write_manifest,
)
from tools.skill_enforcement.parallel.process import ROOT
from tools.skill_enforcement.parallel.verifier import verify_bundle, verify_raw_share_binding
from tools.skill_enforcement.real_campaigns.b1.prepare import validate_output_location


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _deterministic_zip(source: Path, target: Path) -> None:
    if target.exists():
        raise RuntimeError("B1_AUDIT_ZIP_MUST_BE_NEW")
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(x for x in source.rglob("*") if x.is_file()):
            rel = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes())


def _copy_public_audit_root(
    *,
    share_root: Path,
    binding_path: Path,
    envelope_path: Path,
    audit_root: Path,
    adapter_result: dict,
) -> dict:
    if audit_root.exists():
        raise RuntimeError("B1_AUDIT_DIRECTORY_MUST_BE_NEW")
    audit_root.mkdir(parents=True)
    shutil.copytree(share_root, audit_root / "SHARE")
    shutil.copy2(binding_path, audit_root / "RAW_SHARE_BINDING.json")
    shutil.copy2(envelope_path, audit_root / "ENVELOPE_VERIFICATION.json")
    context = {
        "schema_version": "SER-B1-P2-AUDIT-CONTEXT-1",
        "campaign_status": adapter_result.get("status"),
        "campaign_id": adapter_result.get("campaign_id"),
        "round_id": adapter_result.get("round_id"),
        "candidate_sha": adapter_result.get("candidate_sha"),
        "candidate_tree_sha": adapter_result.get("candidate_tree_sha"),
        "first_failure": adapter_result.get("first_failure"),
        "raw_manifest_sha256": _sha256(share_root.parent / share_root.name.replace("_SHARE", "") / "MANIFEST.json"),
        "share_manifest_sha256": _sha256(share_root / "MANIFEST.json"),
        "raw_share_binding_sha256": _sha256(binding_path),
        "envelope_verification_sha256": _sha256(envelope_path),
        "raw_included": False,
        "raw_private": True,
        "share_included": True,
        "authority": {
            "promotion_authorized": False,
            "ready_authorized": False,
            "merge_authorized": False,
        },
    }
    (audit_root / "AUDIT_CONTEXT.json").write_text(
        json.dumps(context, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest_path = write_manifest(audit_root)
    scan = scan_share(audit_root)
    verification = verify_bundle(audit_root)
    return {
        "context": context,
        "manifest_sha256": _sha256(manifest_path),
        "scan": scan,
        "verification": verification,
    }


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
    stem = raw_root.name
    share_root = raw_root.parent / (stem + "_SHARE")
    binding_path = raw_root.parent / (stem + "_RAW_SHARE_BINDING.json")
    envelope_path = raw_root.parent / (stem + "_ENVELOPE_VERIFICATION.json")
    audit_root = raw_root.parent / (stem + "_AUDIT")
    audit_zip = raw_root.parent / (stem + "_AUDIT_BUNDLE.zip")
    verdict_path = raw_root.parent / (stem + "_P2_PACKAGE_VERDICT.json")
    for path in (share_root, binding_path, envelope_path, audit_root, audit_zip, verdict_path):
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
    audit = _copy_public_audit_root(
        share_root=share_root,
        binding_path=binding_path,
        envelope_path=envelope_path,
        audit_root=audit_root,
        adapter_result=adapter_result,
    )
    audit_scan = audit["scan"]
    audit_verification = audit["verification"]
    if audit_scan.get("status") != "PASS" or audit_scan.get("findings") != []:
        raise RuntimeError("B1_AUDIT_BUNDLE_SECRET_SCAN_NOT_PASS")
    if audit_verification.get("valid") is not True:
        raise RuntimeError("B1_AUDIT_BUNDLE_MANIFEST_NOT_VALID")
    _deterministic_zip(audit_root, audit_zip)

    package_ok = envelope.get("valid") is True and audit_verification.get("valid") is True
    verdict = {
        "schema_version": "SER-B1-P2-PACKAGE-VERDICT-2",
        "package_status": "PASS" if package_ok else "FAIL",
        "campaign_status": adapter_result.get("status"),
        "candidate_sha": adapter_result.get("candidate_sha"),
        "evidence_envelope_valid": envelope.get("valid") is True,
        "evidence_envelope_issues": envelope.get("issues") or [],
        "raw_manifest_sha256": _sha256(raw_root / "MANIFEST.json"),
        "share_manifest_sha256": _sha256(share_root / "MANIFEST.json"),
        "binding_sha256": _sha256(binding_path),
        "envelope_verification_sha256": _sha256(envelope_path),
        "audit_manifest_sha256": audit["manifest_sha256"],
        "audit_secret_scan": audit_scan,
        "audit_bundle_zip_sha256": _sha256(audit_zip),
        "raw_is_private": True,
        "upload_artifact": str(audit_zip),
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
    parser = argparse.ArgumentParser(description="Build sanitized P2 AUDIT bundle from immutable local B1 output")
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        verdict = package(args.output_dir)
    except Exception as exc:
        verdict = {
            "schema_version": "SER-B1-P2-PACKAGE-VERDICT-2",
            "package_status": "FAIL",
            "issues": [type(exc).__name__ + ":" + str(exc)],
        }
    print(json.dumps(verdict, ensure_ascii=False, sort_keys=True, indent=2))
    return 0 if verdict.get("package_status") == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
