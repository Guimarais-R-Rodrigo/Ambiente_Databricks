from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

_SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{16,}", re.I),
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{16,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]


def scan_text(text: str) -> list[str]:
    return [
        f"SECRET_PATTERN_{idx}"
        for idx, pattern in enumerate(_SECRET_PATTERNS)
        if pattern.search(text)
    ]


def _payload_files(root: Path) -> list[Path]:
    manifest = root / "MANIFEST.json"
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path == manifest:
            continue
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise ValueError("BUNDLE_SYMLINK_FORBIDDEN:" + rel)
        if path.is_file():
            files.append(path)
    return files


def build_manifest(root: Path) -> dict:
    files = []
    for path in _payload_files(root):
        data = path.read_bytes()
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return {"schema_version": "SER-PARALLEL-BUNDLE-3", "files": files}


def write_manifest(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    manifest = build_manifest(root)
    path = root / "MANIFEST.json"
    path.write_bytes(
        (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    )
    return path


def raw_share_binding(raw_manifest: bytes, share_manifest: bytes, secret_scan: dict) -> dict:
    raw_hash = hashlib.sha256(raw_manifest).hexdigest()
    share_hash = hashlib.sha256(share_manifest).hexdigest()
    return {
        "schema_version": "SER-PARALLEL-RAW-SHARE-3",
        "identity_scope": {
            "raw": "RAW/MANIFEST.json",
            "share": "SHARE/MANIFEST.json",
        },
        "raw_manifest_sha256": raw_hash,
        "share_manifest_sha256": share_hash,
        "manifest_hashes_are_distinct": raw_hash != share_hash,
        "secret_scan": secret_scan,
    }


def build_share(raw_root: Path, share_root: Path, substitutions: dict[str, str]) -> dict:
    if share_root.exists():
        raise ValueError("SHARE_DIRECTORY_MUST_BE_NEW")
    if not raw_root.is_dir():
        raise ValueError("RAW_DIRECTORY_MISSING")
    raw_manifest = raw_root / "MANIFEST.json"
    if not raw_manifest.is_file():
        write_manifest(raw_root)

    share_root.mkdir(parents=True)
    findings: list[str] = []
    examined = 0
    unscannable = 0
    for source in _payload_files(raw_root):
        rel = source.relative_to(raw_root)
        target = share_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            # Preserve bytes for audit, but fail closed: unexamined content can
            # never be counted as a successful complete SHARE scan.
            target.write_bytes(data)
            unscannable += 1
            latin = data.decode("latin-1")
            findings.append(f"{rel.as_posix()}:UNSCANNABLE_BINARY")
            findings.extend(f"{rel.as_posix()}:{hit}" for hit in scan_text(latin))
            continue

        for old, new in substitutions.items():
            text = text.replace(old, new)
        examined += 1
        findings.extend(f"{rel.as_posix()}:{hit}" for hit in scan_text(text))
        # write_bytes preserves the decoded newline sequence exactly; write_text
        # would translate newlines on Windows.
        target.write_bytes(text.encode("utf-8"))

    share_manifest_path = write_manifest(share_root)
    secret_scan = {
        "status": "PASS" if not findings and unscannable == 0 else "FAIL",
        "findings": sorted(findings),
        "text_files_examined": examined,
        "unscannable_files": unscannable,
    }
    return {
        "schema_version": "SER-PARALLEL-SHARE-BUILD-3",
        "share_manifest": str(share_manifest_path),
        "secret_scan": secret_scan,
    }


def build_evidence_envelope(envelope_root: Path, substitutions: dict[str, str]) -> dict:
    raw_root = envelope_root / "RAW"
    share_root = envelope_root / "SHARE"
    binding_path = envelope_root / "RAW_SHARE_BINDING.json"
    if not raw_root.is_dir():
        raise ValueError("RAW_DIRECTORY_MISSING")
    if share_root.exists() or binding_path.exists() or (envelope_root / "MANIFEST.json").exists():
        raise ValueError("EVIDENCE_ENVELOPE_NOT_FRESH")

    raw_manifest_path = write_manifest(raw_root)
    share = build_share(raw_root, share_root, substitutions)
    share_manifest_path = share_root / "MANIFEST.json"
    binding = raw_share_binding(
        raw_manifest_path.read_bytes(),
        share_manifest_path.read_bytes(),
        share["secret_scan"],
    )
    binding_path.write_bytes(
        (json.dumps(binding, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    )
    envelope_manifest_path = write_manifest(envelope_root)
    return {
        "schema_version": "SER-PARALLEL-EVIDENCE-ENVELOPE-3",
        "raw_manifest": str(raw_manifest_path),
        "share_manifest": str(share_manifest_path),
        "binding": str(binding_path),
        "envelope_manifest": str(envelope_manifest_path),
        "secret_scan": share["secret_scan"],
    }


def verify_evidence_envelope(envelope_root: Path) -> dict:
    # Local import avoids coupling the bundle builder to the campaign verifier
    # at module import time.
    from .verifier import verify_bundle

    issues: list[str] = []
    raw_root = envelope_root / "RAW"
    share_root = envelope_root / "SHARE"
    binding_path = envelope_root / "RAW_SHARE_BINDING.json"

    for label, root in (("RAW", raw_root), ("SHARE", share_root), ("ENVELOPE", envelope_root)):
        result = verify_bundle(root)
        if not result["valid"]:
            issues.extend(f"{label}:{issue}" for issue in result["issues"])

    if not binding_path.is_file() or binding_path.is_symlink():
        issues.append("BINDING_MISSING_OR_INVALID")
        return {"valid": False, "issues": sorted(set(issues))}
    try:
        binding = json.loads(binding_path.read_bytes().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, OSError):
        issues.append("BINDING_UNREADABLE")
        return {"valid": False, "issues": sorted(set(issues))}

    if binding.get("schema_version") != "SER-PARALLEL-RAW-SHARE-3":
        issues.append("BINDING_SCHEMA_INVALID")
    if binding.get("identity_scope") != {
        "raw": "RAW/MANIFEST.json",
        "share": "SHARE/MANIFEST.json",
    }:
        issues.append("BINDING_SCOPE_INVALID")

    raw_manifest = raw_root / "MANIFEST.json"
    share_manifest = share_root / "MANIFEST.json"
    if raw_manifest.is_file() and share_manifest.is_file():
        raw_hash = hashlib.sha256(raw_manifest.read_bytes()).hexdigest()
        share_hash = hashlib.sha256(share_manifest.read_bytes()).hexdigest()
        if binding.get("raw_manifest_sha256") != raw_hash:
            issues.append("RAW_MANIFEST_BINDING_MISMATCH")
        if binding.get("share_manifest_sha256") != share_hash:
            issues.append("SHARE_MANIFEST_BINDING_MISMATCH")
        if binding.get("manifest_hashes_are_distinct") != (raw_hash != share_hash):
            issues.append("MANIFEST_DISTINCTNESS_FLAG_MISMATCH")

    scan = binding.get("secret_scan")
    if not isinstance(scan, dict) or scan.get("status") != "PASS" or scan.get("findings") != []:
        issues.append("SHARE_SECRET_SCAN_NOT_PASS")
    return {"valid": not issues, "issues": sorted(set(issues))}
