from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

_SECRET_PATTERNS = [
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{16,}", re.I),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
]

def scan_text(text: str) -> list[str]:
    hits = []
    for idx, pattern in enumerate(_SECRET_PATTERNS):
        if pattern.search(text):
            hits.append(f"SECRET_PATTERN_{idx}")
    return hits

def build_manifest(root: Path) -> dict:
    files = []
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.name != "MANIFEST.json"):
        data = path.read_bytes()
        files.append({"path": path.relative_to(root).as_posix(), "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return {"schema_version": "SER-PARALLEL-BUNDLE-1", "files": files}

def write_manifest(root: Path) -> Path:
    manifest = build_manifest(root)
    path = root / "MANIFEST.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return path

def raw_share_binding(raw_summary: bytes, share_summary: bytes) -> dict:
    return {
        "schema_version": "SER-PARALLEL-RAW-SHARE-1",
        "raw_summary_sha256": hashlib.sha256(raw_summary).hexdigest(),
        "share_summary_sha256": hashlib.sha256(share_summary).hexdigest(),
        "identities_are_distinct": raw_summary != share_summary,
    }
