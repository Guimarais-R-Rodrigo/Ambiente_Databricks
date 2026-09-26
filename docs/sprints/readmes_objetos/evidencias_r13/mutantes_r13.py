from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/sprints/readmes_objetos/evidencias_r13"
sys.path.insert(0, str(ROOT / "tools"))
import readme_objeto_contract as contract  # noqa: E402


def validate(product_root: Path) -> list[str]:
    problems: list[str] = []
    contract.check_readme_objects(product_root, problems, repo=ROOT, previous=set())
    return problems


def expect_failure(name: str, problems: list[str], evidence: dict[str, object]) -> None:
    if not problems:
        raise AssertionError(f"mutante {name} foi aceito")
    evidence[name] = {"status": "REJEITADO_COMO_ESPERADO", "amostra": problems[:5]}


def main() -> None:
    evidence: dict[str, object] = {}

    with tempfile.TemporaryDirectory(prefix="r13-mutantes-") as temp_dir:
        product = Path(temp_dir) / "ambiente_fonte"
        shutil.copytree(ROOT / "ambiente_fonte", product)

        baseline = validate(product)
        if baseline:
            raise AssertionError(f"baseline do contrato falhou: {baseline[:5]}")
        evidence["baseline"] = "PASS"

        specs = [s for s in contract.discover(product / ".assistant") if not s.exemplar]
        target = sorted(specs, key=lambda s: s.path.as_posix())[0]
        readme = product / ".assistant" / target.path / "README.md"
        original = readme.read_text(encoding="utf-8")

        readme.unlink()
        expect_failure("readme_ausente", validate(product), evidence)
        readme.write_text(original, encoding="utf-8")

        h1 = "## 1. O que é?"
        h2 = "## 2. Que problema este recurso resolve?"
        assert h1 in original and h2 in original
        mutated = original.replace(h1, "## 99. TEMP", 1).replace(h2, h1, 1).replace("## 99. TEMP", h2, 1)
        readme.write_text(mutated, encoding="utf-8")
        expect_failure("secoes_fora_de_ordem", validate(product), evidence)
        readme.write_text(original, encoding="utf-8")

        readme.write_text(original + "\n[link mutante](arquivo_que_nao_existe.xyz)\n", encoding="utf-8")
        expect_failure("link_quebrado", validate(product), evidence)
        readme.write_text(original, encoding="utf-8")

        unknown = product / ".assistant/hub_snippets/categoria_mutante"
        unknown.mkdir()
        expect_failure("categoria_desconhecida", validate(product), evidence)
        unknown.rmdir()

        template = product / ".assistant/hub_padroes/readme/template_objeto.md"
        original_template = template.read_text(encoding="utf-8")
        template.write_text(original_template.replace("<!-- readme-objeto: 1.0.0 -->", "<!-- readme-objeto: 9.9.9 -->", 1), encoding="utf-8")
        expect_failure("versao_template_divergente", validate(product), evidence)
        template.write_text(original_template, encoding="utf-8")

        ratchet = contract.check_ratchet({"hub_snippets/ml/objeto_mutante"}, set())
        if not ratchet:
            raise AssertionError("ratchet aceitou nova dispensa")
        evidence["dispensa_reintroduzida"] = {"status": "REJEITADO_COMO_ESPERADO", "amostra": ratchet}

        final = validate(product)
        if final:
            raise AssertionError(f"baseline final contaminado: {final[:5]}")
        evidence["baseline_final"] = "PASS"

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "MUTANTES_R13.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS R13 mutantes: {len(evidence)-2} defeitos sintéticos rejeitados; baseline inicial/final aprovados.")


if __name__ == "__main__":
    main()
