"""Verify exact frozen references in Git; never treat them as live local links."""
from __future__ import annotations

import hashlib
import json
import posixpath
import subprocess
from pathlib import Path

from markdown_links import local_destination_path, markdown_destinations

APPROVED_COMMIT = "8dd8da57de89122241890b8b6b059fd2f9be25d0"
MANIFEST = "docs/manutencao/referencias-historicas-faxina.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError("HISTORICAL_GIT_UNAVAILABLE: clone completo/revisão histórica necessária")
    return result.stdout


def frozen(source: str) -> bool:
    return (source.startswith(("docs/auditoria/", "docs/historico/", "docs/decisions/ADR-"))
            or source.startswith("docs/sprints/") and Path(source).name != "README.md")


def load(root: Path) -> set[tuple[str, str]]:
    """Fail closed on any invented, stale, altered or unrecoverable entry."""
    manifest_path = root / MANIFEST
    if not manifest_path.exists():
        return set()  # synthetic fixtures without migrated history have no exceptions
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("source_commit") != APPROVED_COMMIT:
        raise ValueError("HISTORICAL_COMMIT_OR_SCHEMA")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("HISTORICAL_EMPTY")
    accepted: set[tuple[str, str]] = set()
    sources: dict[str, bytes] = {}
    objects: dict[str, tuple[str, bytes]] = {}
    for entry in entries:
        source, href = entry["source"], entry["href"]
        key = source, href
        if key in accepted or not frozen(source) or "\\" in source or posixpath.normpath(source) != source:
            raise ValueError("HISTORICAL_SOURCE_OR_DUPLICATE")
        path = root / source
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            raise ValueError("HISTORICAL_ESCAPE")
        if source not in sources:
            sources[source] = git(root, "show", f"{APPROVED_COMMIT}:{source}")
        original = sources[source]
        if path.read_bytes() != original or digest(original) != entry["source_sha256"]:
            raise ValueError(f"HISTORICAL_SOURCE_CHANGED: {source}")
        if href not in set(markdown_destinations(original.decode("utf-8"))):
            raise ValueError("HISTORICAL_HREF_INVENTED")
        local = local_destination_path(href)
        if local is None or (path.parent / local).exists():
            raise ValueError("HISTORICAL_ENTRY_NOT_NEEDED")
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), local))
        if target != entry["target"] or not (target.startswith(("ambiente_fonte/", "novas_funcionalidades/"))
                                            or target == "MANUAL_TECNICO.md"):
            raise ValueError("HISTORICAL_TARGET_OR_ESCAPE")
        obj = git(root, "rev-parse", f"{APPROVED_COMMIT}:{target}").decode().strip()
        if obj not in objects:
            kind = git(root, "cat-file", "-t", obj).decode().strip()
            if kind not in ("blob", "tree"):
                raise ValueError("HISTORICAL_OBJECT_TYPE")
            objects[obj] = kind, git(root, "cat-file", kind, obj)
        kind, data = objects[obj]
        if (obj != entry["object_id"] or kind != entry["object_type"]
                or digest(data) != entry["target_sha256"]):
            raise ValueError("HISTORICAL_TARGET_CHANGED")
        accepted.add(key)
    return accepted
