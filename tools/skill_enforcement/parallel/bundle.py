from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Mapping

SECRET_SCAN_POLICY_VERSION = "SER-PARALLEL-SECRET-SCAN-2"
BUNDLE_SCHEMA_VERSION = "SER-PARALLEL-BUNDLE-3"
RAW_SHARE_SCHEMA_VERSION = "SER-PARALLEL-RAW-SHARE-3"
SHARE_METADATA_SCHEMA_VERSION = "SER-PARALLEL-SHARE-METADATA-3"
_RESERVED_SHARE_ROOT = {"MANIFEST.json", "SHARE_METADATA.json"}
_SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{16,}", re.I),
    re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{16,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
]
_WINDOWS_HOME_RE = re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\/\s\"']+")
_POSIX_HOME_RE = re.compile(r"(?i)(?:^|[\s\"'=:(])/(?:Users|home)/[^/\s\"']+")


def _normalized_for_path_scan(text: str) -> str:
    previous = None
    current = text
    while previous != current:
        previous = current
        current = current.replace("\\\\", "\\")
    return current


def scan_text(text: str) -> list[str]:
    findings = [f"SECRET_PATTERN_{idx}" for idx, pattern in enumerate(_SECRET_PATTERNS) if pattern.search(text)]
    normalized = _normalized_for_path_scan(text)
    if _WINDOWS_HOME_RE.search(normalized):
        findings.append("SENSITIVE_PATH_WINDOWS_HOME")
    if _POSIX_HOME_RE.search(normalized):
        findings.append("SENSITIVE_PATH_POSIX_HOME")
    return findings


def _path_variants(raw: str) -> list[str]:
    if not raw:
        return []
    values = {raw, raw.replace("\\", "/")}
    for value in list(values):
        values.add(value.replace("\\", "\\\\"))
        values.add(json.dumps(value, ensure_ascii=False)[1:-1])
    return sorted((value for value in values if value), key=len, reverse=True)


def default_share_substitutions(repo_root: Path) -> dict[str, str]:
    pairs = [(str(repo_root.resolve()), "<REPO>")]
    try:
        pairs.append((str(Path.home().resolve()), "<HOME>"))
    except OSError:
        pass
    substitutions: dict[str, str] = {}
    for raw, marker in pairs:
        for variant in _path_variants(raw):
            substitutions.setdefault(variant, marker)
    return substitutions


def _safe_files(root: Path) -> list[Path]:
    root = root.resolve()
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError("BUNDLE_SYMLINK_FORBIDDEN:" + path.relative_to(root).as_posix())
        if not path.is_file():
            continue
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            raise ValueError("BUNDLE_PATH_ESCAPE:" + path.relative_to(root).as_posix())
        out.append(path)
    return out


def build_manifest(root: Path) -> dict:
    root = root.resolve()
    root_manifest = root / "MANIFEST.json"
    files = []
    for path in _safe_files(root):
        if path == root_manifest:
            continue
        data = path.read_bytes()
        files.append({"path": path.relative_to(root).as_posix(), "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return {"schema_version": BUNDLE_SCHEMA_VERSION, "files": files}


def write_manifest(root: Path) -> Path:
    manifest = build_manifest(root)
    path = root / "MANIFEST.json"
    path.write_bytes((json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8"))
    return path


def scan_share(root: Path) -> dict:
    findings: list[str] = []
    try:
        files = _safe_files(root)
    except ValueError as exc:
        return {"policy_version": SECRET_SCAN_POLICY_VERSION, "status": "FAIL", "findings": [str(exc)]}
    for path in files:
        rel = path.relative_to(root.resolve()).as_posix()
        for hit in scan_text(rel):
            findings.append(f"{rel}:FILENAME_{hit}")
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(f"{rel}:BINARY_UNEXAMINED")
            continue
        for hit in scan_text(text):
            findings.append(f"{rel}:{hit}")
    return {
        "policy_version": SECRET_SCAN_POLICY_VERSION,
        "status": "PASS" if not findings else "FAIL",
        "findings": sorted(findings),
    }


def raw_share_binding(raw_manifest: bytes, share_manifest: bytes, secret_scan: Mapping[str, object]) -> dict:
    return {
        "schema_version": RAW_SHARE_SCHEMA_VERSION,
        "raw_manifest_sha256": hashlib.sha256(raw_manifest).hexdigest(),
        "share_manifest_sha256": hashlib.sha256(share_manifest).hexdigest(),
        "identities_are_distinct": raw_manifest != share_manifest,
        "secret_scan": dict(secret_scan),
    }


def build_share(raw_root: Path, share_root: Path, substitutions: dict[str, str], *, binding_path: Path | None = None) -> dict:
    raw_root = raw_root.resolve()
    if share_root.exists():
        raise ValueError("SHARE_DIRECTORY_MUST_BE_NEW")
    if any(not isinstance(k, str) or not k or not isinstance(v, str) for k, v in substitutions.items()):
        raise ValueError("SHARE_SUBSTITUTIONS_INVALID")
    raw_manifest_path = raw_root / "MANIFEST.json"
    if not raw_manifest_path.is_file():
        write_manifest(raw_root)
    raw_manifest_bytes = raw_manifest_path.read_bytes()
    share_root.mkdir(parents=True)
    raw_manifest = raw_root / "MANIFEST.json"
    for source in _safe_files(raw_root):
        if source == raw_manifest:
            continue
        rel = source.relative_to(raw_root)
        if len(rel.parts) == 1 and rel.name in _RESERVED_SHARE_ROOT:
            raise ValueError("SHARE_RESERVED_PATH_COLLISION:" + rel.as_posix())
        target = share_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        data = source.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            target.write_bytes(data)
            continue
        sanitized = text
        for old, new in substitutions.items():
            sanitized = sanitized.replace(old, new)
        target.write_bytes(data if sanitized == text else sanitized.encode("utf-8"))
    metadata = {
        "schema_version": SHARE_METADATA_SCHEMA_VERSION,
        "raw_manifest_sha256": hashlib.sha256(raw_manifest_bytes).hexdigest(),
        "secret_scan_policy_version": SECRET_SCAN_POLICY_VERSION,
        "sanitization_substitution_count": len(substitutions),
    }
    (share_root / "SHARE_METADATA.json").write_bytes(
        (json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    )
    share_manifest_path = write_manifest(share_root)
    secret_scan = scan_share(share_root)
    binding = raw_share_binding(raw_manifest_bytes, share_manifest_path.read_bytes(), secret_scan)
    if binding_path is None:
        binding_path = share_root.parent / f"{share_root.name}.RAW_SHARE_BINDING.json"
    if binding_path.exists():
        raise ValueError("RAW_SHARE_BINDING_MUST_BE_NEW")
    binding_path.write_bytes((json.dumps(binding, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return binding
