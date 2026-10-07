"""Empacota fontes E0 sintéticas para transporte concreto ao Databricks Free.

Não conecta, publica nem executa Databricks. Cópias são derivadas de allowlist
fechada e permanecem fora do Git no diretório de saída escolhido.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "tools/free_kit/RUN_FREE.py",
    "tools/free_kit/SETUP_METADATA_FREE.py",
    "docs/sprints/micromodelos/KIT_FREE.md",
    "ambiente_databricks/.assistant_instructions.md",
    "ambiente_databricks/.assistant/hub_padroes/skill_enforcement/policy.json",
)
PRODUCT_FILES = (
    "ambiente_databricks/.assistant/hub_snippets/ml/__init__.py",
    "ambiente_databricks/.assistant/hub_snippets/ml/mlflow_run/__init__.py",
    "ambiente_databricks/.assistant/hub_snippets/ml/mlflow_run/mlflow_run.py",
    "ambiente_databricks/.assistant/hub_snippets/ml/mlflow_run/README.md",
    "ambiente_databricks/.assistant/skills/hub-ml-micromodelos/SKILL.md",
    "ambiente_databricks/.assistant/skills/hub-ml-micromodelos/execution_contract.json",
    "ambiente_databricks/.assistant/hub_prompts/micromodelo_novo/README.md",
    "ambiente_databricks/.assistant/hub_prompts/micromodelo_novo/micromodelo_novo.md",
    "ambiente_databricks/.assistant/hub_prompts/micromodelo_novo/exemplo_micromodelo_novo.py",
    "ambiente_databricks/.assistant/hub_prompts/descobrir_micromodelos/README.md",
    "ambiente_databricks/.assistant/hub_prompts/descobrir_micromodelos/descobrir_micromodelos.md",
    "ambiente_databricks/.assistant/hub_prompts/descobrir_micromodelos/exemplo_descobrir_micromodelos.py",
) + tuple(
    "ambiente_databricks/.assistant/hub_micromodelos/" + path.relative_to(
        ROOT / "ambiente_databricks/.assistant/hub_micromodelos").as_posix()
    for path in sorted((ROOT / "ambiente_databricks/.assistant/hub_micromodelos").rglob("*"))
    if path.is_file() and "__pycache__" not in path.parts
)
DESTINATION = {
    "tools/free_kit/RUN_FREE.py": "RUN_FREE.py",
    "tools/free_kit/SETUP_METADATA_FREE.py": "SETUP_METADATA_FREE.py",
    "docs/sprints/micromodelos/KIT_FREE.md": "README.md",
    "ambiente_databricks/.assistant_instructions.md": "product_overlay/.assistant_instructions.md",
    "ambiente_databricks/.assistant/hub_padroes/skill_enforcement/policy.json":
        "product_overlay/.assistant/hub_padroes/skill_enforcement/policy.json",
}
REQUIREMENTS = "PyYAML>=6.0\nregex>=2024.11.6\njsonschema>=4.23\n"
RESULT_TEMPLATE = """# Resultados do kit Free — cópia sanitizada

- Data/ambiente/runtime: PENDENTE
- Revisão do Git e SHA-256 do manifesto: PENDENTE
- Import e dependências: NOT_RUN
- Código sintético no Free: NOT_RUN
- MLflow sintético no Free (run IDs e mm06.complete): NOT_RUN
- Adapter information_schema: NOT_RUN
- Genie Code/skill: NOT_RUN
- Fingerprint, TRUE/FALSE/INDETERMINADO, total: PENDENTE
- Erros/skips e capacidade ausente: PENDENTE
- Identificadores/outputs privados removidos antes do retorno: PENDENTE
"""


def _safe_source(rel: str) -> Path:
    """Recusa links, quarentena e saída da raiz mesmo em fonte allowlisted."""
    source = ROOT / rel
    root = ROOT.resolve()
    if not source.is_file() or any(part.is_symlink() for part in
                                   (source, *source.parents) if part != root):
        raise FileNotFoundError("KIT_SOURCE_UNSAFE")
    resolved = source.resolve()
    if not resolved.is_relative_to(root) or "Ambiente_Antigo" in resolved.parts:
        raise FileNotFoundError("KIT_SOURCE_UNSAFE")
    return source


def build(output: Path) -> dict[str, str]:
    """Cria diretório e ZIP novos; nunca sobrescreve saída preexistente."""
    output = output.resolve()
    archive = output.with_suffix(".zip")
    if output.exists() or archive.exists():
        raise FileExistsError("OUTPUT_EXISTS")
    missing = [rel for rel in (*FILES, *PRODUCT_FILES) if not (ROOT / rel).is_file()]
    if missing:
        raise FileNotFoundError("KIT_SOURCE_MISSING: " + ", ".join(missing))
    sources = {rel: _safe_source(rel) for rel in (*FILES, *PRODUCT_FILES)}
    output.mkdir(parents=True)
    digests: dict[str, str] = {}
    for rel in FILES:
        packaged = DESTINATION.get(rel, rel)
        dest = output / packaged
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(sources[rel], dest)
        digests[packaged] = hashlib.sha256(dest.read_bytes()).hexdigest()
    for rel in PRODUCT_FILES:
        relative = Path(rel).relative_to("ambiente_databricks")
        packaged = (Path("product_overlay") / relative).as_posix()
        dest = output / packaged
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(sources[rel], dest)
        digests[packaged] = hashlib.sha256(dest.read_bytes()).hexdigest()
    for rel, content in {
        "requirements-free.txt": REQUIREMENTS,
        "RESULTADOS_FREE.md": RESULT_TEMPLATE,
    }.items():
        dest = output / rel
        dest.write_text(content, encoding="utf-8")
        digests[rel] = hashlib.sha256(dest.read_bytes()).hexdigest()
    manifest = {"kind": "E1_PREPARED_SYNTHETIC", "files": digests,
                "e1_execution": "NOT_RUN", "e2_execution": "NOT_RUN"}
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as bundle:
        for file in sorted(output.rglob("*")):
            if file.is_file():
                bundle.write(file, file.relative_to(output).as_posix())
    return {"directory": str(output), "zip": str(archive),
            "zip_sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            "file_count": str(len(digests))}


def main() -> int:
    parser = argparse.ArgumentParser(description="Kit sintético transportável Free")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = build(args.output)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
