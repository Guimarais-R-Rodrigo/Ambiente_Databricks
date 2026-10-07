from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from . import loads_strict


def load_sibling(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("SIBLING_IMPORT_UNAVAILABLE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def release_integrity(skill_dir: Path, required_paths: set[str]) -> dict:
    root = skill_dir.parents[1]
    manifest_path = skill_dir / "release_manifest.json"
    raw = loads_strict(manifest_path.read_text(encoding="utf-8"))
    if (set(raw) != {"manifest_version", "skill", "algorithm", "artifacts"}
            or raw["manifest_version"] != "0.1" or raw["skill"] != skill_dir.name
            or raw["algorithm"] != "git_blob_sha1" or not isinstance(raw["artifacts"], list)):
        raise ValueError("RELEASE_MANIFEST_INVALID")
    observed = {}
    for row in raw["artifacts"]:
        if not isinstance(row, dict) or set(row) != {"path", "git_blob_sha1"}:
            raise ValueError("RELEASE_ARTIFACT_INVALID")
        rel, expected = row["path"], row["git_blob_sha1"]
        if (not isinstance(rel, str) or not rel or "\\" in rel or ":" in rel
                or rel.startswith("/") or any(x in ("", ".", "..") for x in rel.split("/"))
                or rel in observed):
            raise ValueError("RELEASE_PATH_INVALID")
        path = root / rel
        if any(part.is_symlink() for part in (path, *path.parents)):
            raise ValueError("RELEASE_SYMLINK_NOT_ALLOWED")
        path.resolve().relative_to(root.resolve())
        if (not isinstance(expected, str) or len(expected) != 40
                or any(c not in "0123456789abcdef" for c in expected)
                or blob(path) != expected):
            raise ValueError("RELEASE_INTEGRITY_MISMATCH:" + rel)
        observed[rel] = expected
    if set(observed) != required_paths:
        raise ValueError("RELEASE_FILESET_MISMATCH")
    return {"manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            "artifacts": observed}
