"""Monta/verifica o bundle local do Databricks App de gestão visual V10.

Não usa Databricks CLI, token, rede ou workspace. O artefato é derivado do produto
canônico e deve ser implantado somente por procedimento autorizado separado.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PRODUCT = REPO_ROOT / "ambiente_fonte" / ".assistant"
APP_SOURCE = PRODUCT / "hub_padroes" / "identidade_visual" / "databricks_app"
APP_FILES = ("app.py", "app_service.py", "app.yaml", "requirements.txt", "README.md", "GUIA_PRIMEIRO_USO.md", "DEPLOY_ROLLBACK.md")
MANIFEST = "V10_APP_MANIFEST.json"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _copy_tree(source: Path, target: Path, *, ignore_name: str | None = None) -> None:
    if not source.is_dir() or source.is_symlink():
        raise ValueError(f"fonte inválida: {source}")
    target.mkdir(parents=True, exist_ok=False)
    for item in sorted(source.rglob("*")):
        relative = item.relative_to(source)
        if ignore_name and relative.parts and relative.parts[0] == ignore_name:
            continue
        if item.is_symlink():
            raise ValueError(f"symlink recusado: {item}")
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)


def _commit() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, capture_output=True, text=True, timeout=20
    )
    if completed.returncode != 0:
        raise ValueError("não foi possível resolver o commit Git")
    return completed.stdout.strip()


def _entries(root: Path) -> list[dict[str, str | int]]:
    result = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlink recusado no bundle: {path}")
        if path.is_file() and path.name != MANIFEST:
            result.append({
                "path": path.relative_to(root).as_posix(),
                "sha256": _sha(path),
                "bytes": path.stat().st_size,
            })
    return result


def _validate_app_config(root: Path) -> None:
    config = (root / "app.yaml").read_text(encoding="utf-8")
    required = (
        "streamlit", "app.py", "HUB_THEME_VOLUME", "valueFrom: theme_storage",
        "HUB_THEME_APP_MODE", "authoring_only", "STREAMLIT_GATHER_USAGE_STATS",
    )
    for text in required:
        if text not in config:
            raise ValueError(f"app.yaml sem contrato obrigatório: {text}")
    forbidden = ("/Volumes/", "DATABRICKS_TOKEN", "PAT", "http://", "https://")
    for text in forbidden:
        if text in config:
            raise ValueError(f"app.yaml contém valor proibido/hardcoded: {text}")


def build(output: Path) -> Path:
    output = output.resolve()
    if output.exists():
        raise ValueError("destino já existe; não sobrescreva bundle V10")
    if not APP_SOURCE.is_dir():
        raise ValueError("fonte do App V10 ausente")
    output.mkdir(parents=True)
    try:
        for name in APP_FILES:
            source = APP_SOURCE / name
            if not source.is_file() or source.is_symlink():
                raise ValueError(f"arquivo obrigatório ausente/inválido: {name}")
            shutil.copy2(source, output / name)
        _copy_tree(PRODUCT / "hub_snippets", output / "hub_snippets")
        identity_target = output / "hub_padroes" / "identidade_visual"
        identity_target.parent.mkdir(parents=True, exist_ok=True)
        _copy_tree(PRODUCT / "hub_padroes" / "identidade_visual", identity_target, ignore_name="databricks_app")
        _validate_app_config(output)
        manifest = {
            "schema_version": 1,
            "source_commit": _commit(),
            "surface": "databricks_app_theme_manager_v10",
            "app_mode": "authoring_only",
            "persistence": "unity_catalog_volume_resource",
            "resource_key": "theme_storage",
            "publication": "not_implemented",
            "files": _entries(output),
        }
        (output / MANIFEST).write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except Exception:
        shutil.rmtree(output, ignore_errors=True)
        raise
    verify(output)
    return output


def verify(root: Path) -> None:
    root = root.resolve()
    manifest_path = root / MANIFEST
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ValueError("manifesto V10 ausente")
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("manifesto V10 inválido") from exc
    required_keys = {"schema_version", "source_commit", "surface", "app_mode", "persistence", "resource_key", "publication", "files"}
    if type(data) is not dict or set(data) != required_keys:
        raise ValueError("shape do manifesto V10 divergente")
    if data["schema_version"] != 1 or data["app_mode"] != "authoring_only":
        raise ValueError("versão/modo V10 divergente")
    if data["persistence"] != "unity_catalog_volume_resource" or data["resource_key"] != "theme_storage":
        raise ValueError("contrato de persistência V10 divergente")
    if data["publication"] != "not_implemented":
        raise ValueError("bundle V10 não pode declarar publicação")
    expected = {item["path"]: item for item in data["files"]}
    observed = {item["path"]: item for item in _entries(root)}
    if set(expected) != set(observed):
        raise ValueError("inventário do bundle V10 divergente")
    for path, item in expected.items():
        if item.get("sha256") != observed[path]["sha256"] or item.get("bytes") != observed[path]["bytes"]:
            raise ValueError(f"hash/tamanho divergente no bundle V10: {path}")
    for name in APP_FILES:
        if name not in expected:
            raise ValueError(f"arquivo do App ausente do manifesto: {name}")
    if not any(path.startswith("hub_snippets/visual/theme_lab/") for path in expected):
        raise ValueError("Visual Lab V05 não foi transportado ao bundle")
    if not any(path == "hub_padroes/identidade_visual/theme.schema.json" for path in expected):
        raise ValueError("schema canônico não foi transportado ao bundle")
    _validate_app_config(root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--output", type=Path)
    group.add_argument("--verify", type=Path)
    args = parser.parse_args()
    try:
        if args.output is not None:
            result = build(args.output)
            print(f"OK bundle V10 criado: {result} ({len(_entries(result))} arquivos + {MANIFEST})")
        else:
            verify(args.verify)
            print(f"OK bundle V10 verificado: {args.verify}")
        return 0
    except ValueError as exc:
        print(f"FAIL V10: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
