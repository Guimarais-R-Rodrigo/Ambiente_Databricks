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
    return [f"SECRET_PATTERN_{idx}" for idx, pattern in enumerate(_SECRET_PATTERNS) if pattern.search(text)]


def build_manifest(root: Path) -> dict:
    root_manifest = root / "MANIFEST.json"
    files = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p != root_manifest):
        data = path.read_bytes()
        files.append({"path": path.relative_to(root).as_posix(), "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return {"schema_version": "SER-PARALLEL-BUNDLE-2", "files": files}


def write_manifest(root: Path) -> Path:
    manifest = build_manifest(root)
    path = root / "MANIFEST.json"
    path.write_bytes((json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    return path


def raw_share_binding(raw_manifest: bytes, share_manifest: bytes) -> dict:
    return {
        "schema_version": "SER-PARALLEL-RAW-SHARE-2",
        "raw_manifest_sha256": hashlib.sha256(raw_manifest).hexdigest(),
        "share_manifest_sha256": hashlib.sha256(share_manifest).hexdigest(),
        "identities_are_distinct": raw_manifest != share_manifest,
    }


def build_share(raw_root: Path, share_root: Path, substitutions: dict[str, str], *, binding_path: Path | None = None) -> dict:
    if share_root.exists():
        raise ValueError("SHARE_DIRECTORY_MUST_BE_NEW")
    raw_manifest_path = raw_root / "MANIFEST.json"
    if not raw_manifest_path.is_file():
        write_manifest(raw_root)
    share_root.mkdir(parents=True)
    findings: list[str] = []
    raw_manifest = raw_root / "MANIFEST.json"
    for source in sorted(p for p in raw_root.rglob("*") if p.is_file() and p != raw_manifest):
        rel = source.relative_to(raw_root)
        target = share_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            target.write_bytes(data)
            findings.append(f"{rel.as_posix()}:BINARY_UNEXAMINED")
            continue
        sanitized = text
        for old, new in substitutions.items():
            sanitized = sanitized.replace(old, new)
        findings.extend(f"{rel.as_posix()}:{hit}" for hit in scan_text(sanitized))
        target.write_bytes(data if sanitized == text else sanitized.encode("utf-8"))
    metadata = {
        "schema_version": "SER-PARALLEL-SHARE-METADATA-2",
        "raw_manifest_sha256": hashlib.sha256(raw_manifest_path.read_bytes()).hexdigest(),
        "sanitization_substitution_count": len(substitutions),
    }
    (share_root / "SHARE_METADATA.json").write_bytes(
        (json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    )
    share_manifest_path = write_manifest(share_root)
    binding = raw_share_binding(raw_manifest_path.read_bytes(), share_manifest_path.read_bytes())
    binding["secret_scan"] = {"status": "PASS" if not findings else "FAIL", "findings": findings}
    if binding_path is None:
        binding_path = share_root.parent / f"{share_root.name}.RAW_SHARE_BINDING.json"
    if binding_path.exists():
        raise ValueError("RAW_SHARE_BINDING_MUST_BE_NEW")
    binding_path.write_bytes((json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return binding
