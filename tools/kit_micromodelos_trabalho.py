"""Empacota o runtime técnico de Micromodelos para aceite sintético no destino.

O ZIP é complementar ao Hub. Não instala a skill, acessa Databricks nem executa
consultas. O manifesto confere integridade, não autentica a origem do arquivo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
KIND = "MM_E2_PREPARED_SYNTHETIC"
VERSION = 1
MANIFEST = "manifest.json"

# Uma lista fechada evita transportar o checkout, dados ou ferramentas locais.
RUNTIME_FILES = (
    "tools/micromodelo_mm01_contract.py",
    "tools/micromodelo_mm02_fingerprint.py",
    "tools/micromodelo_mm03_metadata.py",
    "tools/micromodelo_mm04_flow.py",
    "tools/micromodelo_mm06_artifacts.py",
    "tools/micromodelo_mm07_databricks.py",
    "tools/micromodelo_mm09_lab.py",
    "tools/micromodelo_mm10_handoff.py",
    "tools/micromodelo_mm12_migration_lab.py",
    "tools/micromodelo_mm13_catalog.py",
    "tools/kit_micromodelos_trabalho.py",
    "tools/aceite_micromodelos_trabalho.py",
    "tools/tests/fixtures/micromodelos_mm03/catalogo_sintetico.json",
    "docs/sprints/micromodelos/MM01/micromodelo.schema.json",
    "docs/sprints/micromodelos/MM01/micromodelo.template.yaml",
    "docs/playbooks/aceite-micromodelos-trabalho.md",
)
OPTIONAL_TRACKING = (
    "ambiente_fonte/.assistant/hub_snippets/__init__.py",
    "ambiente_fonte/.assistant/hub_snippets/ml/__init__.py",
    "ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/__init__.py",
    "ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/mlflow_run.py",
)
MINIMUM_REQUIREMENTS = "PyYAML>=6.0,<7\nregex>=2024.11.6\njsonschema>=4.23,<5\n"
GENERATED_FILES = ("requirements-micromodelos.txt",)


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _is_link(path: Path) -> bool:
    return path.is_symlink() or getattr(path, "is_junction", lambda: False)()


def _source_path(root: Path, rel: str) -> Path:
    source = root / rel
    try:
        resolved_root = root.resolve(strict=True)
        resolved = source.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise FileNotFoundError("KIT_SOURCE_MISSING") from exc
    if (not source.is_file() or not resolved.is_relative_to(resolved_root)
            or any(_is_link(part) for part in (source, *source.parents)
                   if part != resolved_root)
            or "Ambiente_Antigo" in resolved.parts):
        raise ValueError("KIT_SOURCE_UNSAFE")
    return source


def _identity(root: Path) -> str:
    def git(*args: str) -> str:
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()
    commit = git("rev-parse", "HEAD")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("KIT_COMMIT_INVALID")
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("KIT_CHECKOUT_DIRTY")
    return commit


def _entries(root: Path) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    for rel in RUNTIME_FILES:
        entries[rel] = _source_path(root, rel).read_bytes()
    for rel in OPTIONAL_TRACKING:
        packaged = "runtime/" + rel.removeprefix("ambiente_fonte/.assistant/")
        entries[packaged] = _source_path(root, rel).read_bytes()
    entries[GENERATED_FILES[0]] = MINIMUM_REQUIREMENTS.encode("utf-8")
    if len(entries) != len(RUNTIME_FILES) + len(OPTIONAL_TRACKING) + len(GENERATED_FILES):
        raise ValueError("KIT_DUPLICATE_PATH")
    return entries


def _assert_commit_sources(root: Path, commit: str, entries: dict[str, bytes]) -> None:
    """O SHA declarado deve identificar os bytes efetivamente empacotados."""
    for rel in (*RUNTIME_FILES, *OPTIONAL_TRACKING):
        packaged = (rel if rel in RUNTIME_FILES else
                    "runtime/" + rel.removeprefix("ambiente_fonte/.assistant/"))
        try:
            committed = subprocess.check_output(
                ["git", "show", f"{commit}:{rel}"], cwd=root)
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ValueError("KIT_SOURCE_NOT_IN_COMMIT") from exc
        if entries[packaged] != committed:
            raise ValueError("KIT_SOURCE_COMMIT_MISMATCH")


def build(archive: Path) -> dict[str, Any]:
    """Cria um ZIP novo de checkout limpo; nunca substitui uma saída existente."""
    archive = archive.resolve()
    if archive.exists():
        raise FileExistsError("KIT_OUTPUT_EXISTS")
    if archive.suffix.lower() != ".zip":
        raise ValueError("KIT_OUTPUT_EXTENSION")
    if archive.is_relative_to(ROOT.resolve()) and not archive.is_relative_to((ROOT / ".artifacts").resolve()):
        raise ValueError("KIT_OUTPUT_LOCATION")
    commit = _identity(ROOT)
    entries = _entries(ROOT)
    _assert_commit_sources(ROOT, commit, entries)
    manifest = {
        "kind": KIND,
        "version": VERSION,
        "source_commit": commit,
        "files": {rel: {"sha256": _sha(raw), "size": len(raw)}
                  for rel, raw in sorted(entries.items())},
        "e2_execution": "NOT_RUN",
    }
    raw_manifest = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True)
                    + "\n").encode("utf-8")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with archive.open("xb") as handle:
        try:
            with zipfile.ZipFile(handle, "w", zipfile.ZIP_DEFLATED) as bundle:
                for rel, raw in sorted(entries.items()):
                    bundle.writestr(rel, raw)
                bundle.writestr(MANIFEST, raw_manifest)
        except BaseException:
            handle.close()
            archive.unlink(missing_ok=True)
            raise
    return {"zip": str(archive), "zip_sha256": _sha(archive.read_bytes()),
            "source_commit": commit, "manifest_sha256": _sha(raw_manifest),
            "file_count": len(entries)}


def _safe_relative(path: str) -> bool:
    parsed = PurePosixPath(path)
    return (bool(path) and "\\" not in path and ":" not in path
            and not parsed.is_absolute() and path == parsed.as_posix()
            and all(part not in ("", ".", "..") for part in parsed.parts)
            and path != MANIFEST)


def verify(package_root: Path, manifest_path: Path | None = None) -> dict[str, Any]:
    """Confere identidade estrutural e bytes antes de importar código do pacote."""
    root = package_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("KIT_ROOT_INVALID")
    location = root / MANIFEST if manifest_path is None else Path(manifest_path)
    try:
        if (_is_link(location)
                or location.resolve(strict=True) != (root / MANIFEST).resolve(strict=True)):
            raise ValueError("KIT_MANIFEST_LOCATION")
    except OSError as exc:
        raise ValueError("KIT_MANIFEST_MISSING") from exc
    try:
        manifest = json.loads(location.read_bytes())
    except (OSError, ValueError) as exc:
        raise ValueError("KIT_MANIFEST_INVALID") from exc
    if (not isinstance(manifest, dict) or manifest.get("kind") != KIND
            or manifest.get("version") != VERSION
            or not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("source_commit", "")))
            or manifest.get("e2_execution") != "NOT_RUN"
            or not isinstance(manifest.get("files"), dict)):
        raise ValueError("KIT_MANIFEST_INVALID")
    files = manifest["files"]
    expected = set(RUNTIME_FILES) | {
        "runtime/" + rel.removeprefix("ambiente_fonte/.assistant/")
        for rel in OPTIONAL_TRACKING
    } | set(GENERATED_FILES)
    if set(files) != expected:
        raise ValueError("KIT_MANIFEST_FILESET")
    for rel, entry in files.items():
        if (not _safe_relative(rel) or not isinstance(entry, dict)
                or set(entry) != {"sha256", "size"}
                or not re.fullmatch(r"[0-9a-f]{64}", str(entry["sha256"]))
                or type(entry["size"]) is not int or entry["size"] < 0):
            raise ValueError("KIT_MANIFEST_INVALID")
        path = root / rel
        if not path.is_file() or _is_link(path) or not path.resolve().is_relative_to(root):
            raise ValueError("KIT_FILE_MISSING_OR_UNSAFE")
        raw = path.read_bytes()
        if len(raw) != entry["size"] or _sha(raw) != entry["sha256"]:
            raise ValueError("KIT_FILE_HASH_MISMATCH")
    actual = set()
    for path in root.rglob("*"):
        if _is_link(path):
            raise ValueError("KIT_EXTRA_UNSAFE")
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            if "__pycache__" in path.relative_to(root).parts and path.suffix == ".pyc":
                continue
            actual.add(rel)
    if actual != expected | {MANIFEST}:
        raise ValueError("KIT_EXTRA_OR_MISSING")
    return {"status": "PASS", "source_commit": manifest["source_commit"],
            "manifest_sha256": _sha(location.read_bytes()), "file_count": len(files)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Kit técnico Micromodelos para trabalho")
    parser.add_argument("--output", type=Path, required=True, help="novo caminho ZIP")
    args = parser.parse_args()
    print(json.dumps(build(args.output), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
