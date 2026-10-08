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


def load_faxina(root: Path) -> set[tuple[str, str]]:
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


PLAN_MANIFEST = "docs/manutencao/referencias-historicas-plano-hub.json"
PLAN_SOURCE_COMMIT = "6ac0060dfcd09134634abe204474debb5757e231"
PLAN_TARGET_COMMIT = "09ecdc1eaf9ed7cd8acf7a4db3a6443eb47337fd"
PLAN_TARGET_HASH = "4307e9c3dd6301b7b04733f6ebaebaa8d6ab41215550e6817bb0b68b39ac125f"
PLAN_PAIRS = {
    ("docs/handoffs/2026-09-09_plano-consolidado.md", "../../PLANO_HUB.md"),
    ("docs/manutencao/organizacao-tools-raiz-workflows-2026-10-07.md", "../../PLANO_HUB.md"),
}


def load_plan(root: Path) -> set[tuple[str, str]]:
    """Recover only two approved historical hrefs; no directory-wide exemption."""
    path = root / PLAN_MANIFEST
    if not path.exists():
        return set()  # Fixtures without the new ledger have no new exceptions.
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if (manifest.get("schema_version") != 1
            or manifest.get("source_commit") != PLAN_SOURCE_COMMIT
            or manifest.get("target_commit") != PLAN_TARGET_COMMIT
            or manifest.get("target") != "PLANO_HUB.md"
            or manifest.get("target_sha256") != PLAN_TARGET_HASH):
        raise ValueError("PLAN_HISTORY_SCHEMA_OR_REVISION")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or len(entries) != 2:
        raise ValueError("PLAN_HISTORY_COUNT")
    pairs = [(e["source"], e["href"]) for e in entries]
    if len(set(pairs)) != 2 or set(pairs) != PLAN_PAIRS:
        raise ValueError("PLAN_HISTORY_SOURCE_OR_HREF")
    target = root / "PLANO_HUB.md"
    if target.exists() or target.is_symlink():
        raise ValueError("PLAN_HISTORY_ENTRY_NOT_NEEDED")
    obj = git(root, "rev-parse", f"{PLAN_TARGET_COMMIT}:PLANO_HUB.md").decode().strip()
    if obj != manifest.get("object_id") or git(root, "cat-file", "-t", obj).strip() != b"blob":
        raise ValueError("PLAN_HISTORY_TARGET_OBJECT")
    if digest(git(root, "cat-file", "blob", obj)) != PLAN_TARGET_HASH:
        raise ValueError("PLAN_HISTORY_TARGET_CHANGED")
    for entry in entries:
        source = root / entry["source"]
        if not source.resolve().is_relative_to(root.resolve()) or source.is_symlink():
            raise ValueError("PLAN_HISTORY_ESCAPE")
        original = git(root, "show", f"{PLAN_SOURCE_COMMIT}:{entry['source']}")
        if source.read_bytes() != original or digest(original) != entry["source_sha256"]:
            raise ValueError("PLAN_HISTORY_SOURCE_CHANGED")
        if entry["href"] not in set(markdown_destinations(original.decode("utf-8"))):
            raise ValueError("PLAN_HISTORY_HREF_INVENTED")
        local = local_destination_path(entry["href"])
        if local is None or posixpath.normpath(posixpath.join(posixpath.dirname(entry["source"]), local)) != "PLANO_HUB.md":
            raise ValueError("PLAN_HISTORY_TARGET_OR_ESCAPE")
    return set(pairs)


def load(root: Path) -> set[tuple[str, str]]:
    """Combine independent strict ledgers without widening the faxina contract."""
    return load_faxina(root) | load_plan(root)
