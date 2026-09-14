"""Contrato V09 do Sistema de Temas para o kit de transição.

Este módulo é deliberadamente offline: valida inventários e manifesta o conjunto
mínimo que precisa viajar no pacote. Não publica, ativa ou promove temas.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from collections.abc import Iterable, Mapping
from pathlib import Path

THEME_CONTRACT_VERSION = 1
THEME_REQUIRED_PATHS = (
    ".assistant/hub_padroes/identidade_visual/theme.schema.json",
    ".assistant/hub_padroes/identidade_visual/TOKENS.md",
    ".assistant/hub_padroes/identidade_visual/assets.json",
    ".assistant/hub_padroes/identidade_visual/README.md",
    ".assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md",
    ".assistant/hub_snippets/visual/tema/__init__.py",
    ".assistant/hub_snippets/visual/tema/tema.py",
    ".assistant/hub_snippets/visual/theme_plotly/__init__.py",
    ".assistant/hub_snippets/visual/theme_plotly/theme_plotly.py",
)


def _paths(entries: Iterable[Mapping[str, object]]) -> set[str]:
    result: set[str] = set()
    for entry in entries:
        path = entry.get("path")
        if isinstance(path, str):
            result.add(path)
    return result


def validate_theme_inventory(entries: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Falha se o bundle perder qualquer peça mínima do contrato temático V09."""
    present = _paths(entries)
    missing = [path for path in THEME_REQUIRED_PATHS if path not in present]
    if missing:
        raise ValueError("Sistema de Temas incompleto no bundle: " + ", ".join(missing))
    return {
        "contract_version": THEME_CONTRACT_VERSION,
        "required_paths": list(THEME_REQUIRED_PATHS),
        "transport": "required_and_hashed",
        "activation": "manual_opt_in",
        "publication": "not_performed",
    }


def validate_theme_contract(manifest: Mapping[str, object]) -> dict[str, object]:
    """Confere que manifesto e inventário contam a mesma história sobre temas."""
    files = manifest.get("files")
    if not isinstance(files, list):
        raise ValueError("Manifesto sem lista de arquivos para validar temas.")
    expected = validate_theme_inventory(files)
    contract = manifest.get("theme_contract")
    if contract != expected:
        raise ValueError("Contrato de temas ausente ou divergente no manifesto.")
    return expected


def validate_theme_zip(package: Path) -> dict[str, object]:
    """Confere contrato, presença e SHA256 das peças temáticas dentro do ZIP final."""
    package = Path(package)
    if not package.is_file():
        raise ValueError("ZIP do Hub ausente para validação do Sistema de Temas.")
    with zipfile.ZipFile(package) as archive:
        try:
            manifest = json.loads(archive.read("MANIFEST.json"))
        except KeyError as exc:
            raise ValueError("ZIP do Hub sem MANIFEST.json.") from exc
        contract = validate_theme_contract(manifest)
        entries = {entry["path"]: entry for entry in manifest["files"] if isinstance(entry, dict) and isinstance(entry.get("path"), str)}
        names = archive.namelist()
        for path in contract["required_paths"]:
            if names.count(path) != 1:
                raise ValueError("Arquivo temático ausente ou duplicado no ZIP: " + path)
            entry = entries[path]
            raw = archive.read(path)
            if len(raw) != entry.get("bytes") or hashlib.sha256(raw).hexdigest() != entry.get("sha256"):
                raise ValueError("Hash do arquivo temático diverge dentro do ZIP: " + path)
    return contract


def validate_kit_directory(directory: Path) -> dict[str, object]:
    """Localiza exatamente um ZIP 01 no diretório do kit e valida seu contrato temático."""
    directory = Path(directory)
    packages = sorted(directory.glob("01_IMPORTAR_HUB_*.zip")) if directory.is_dir() else []
    if len(packages) != 1:
        raise ValueError(f"Esperado exatamente 1 ZIP 01 do Hub; encontrados {len(packages)}.")
    return validate_theme_zip(packages[0])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kit-dir", type=Path, required=True, help="diretório gerado por kit_transicao_trabalho.py")
    args = parser.parse_args()
    try:
        contract = validate_kit_directory(args.kit_dir)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print("FAIL:", str(exc))
        return 1
    print(
        f"OK theme_contract v{contract['contract_version']}: "
        f"{len(contract['required_paths'])} caminhos obrigatórios presentes e com SHA256 válido; "
        "ativação manual_opt_in; publicação not_performed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
