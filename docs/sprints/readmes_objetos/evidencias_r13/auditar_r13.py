from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ASSIST = ROOT / "ambiente_fonte/.assistant"
DOCS = ROOT / "docs/sprints/readmes_objetos"
OUT = DOCS / "evidencias_r13"
BASE = "ec4b559d098c96dfececbb17e52fbc276cb485c0"

sys.path.insert(0, str(ROOT / "tools"))
import readme_objeto_contract as contract  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail_if(condition: bool, message: str, blockers: list[str]) -> None:
    if condition:
        blockers.append(message)


def direct_object_dirs(root: Path) -> list[Path]:
    return sorted(
        [p for p in root.iterdir() if p.is_dir() and not p.name.startswith("_")],
        key=lambda p: p.name,
    )


def main() -> None:
    blockers: list[str] = []
    observations: list[str] = []

    template_path = ASSIST / "hub_padroes/readme/template_objeto.md"
    checklist_path = ASSIST / "hub_padroes/readme/checklist_objeto.md"
    skill_path = ASSIST / "skills/hub-ml-criar-objeto/SKILL.md"
    manual_path = ASSIST / "MANUAL_TECNICO.md"
    root_manual = ROOT / "MANUAL_TECNICO.md"
    initiative = DOCS / "README.md"
    control_path = DOCS / "CONTROLE_MIGRACAO.json"

    template = template_path.read_text(encoding="utf-8")
    checklist = checklist_path.read_text(encoding="utf-8")
    skill = skill_path.read_text(encoding="utf-8")
    manual = manual_path.read_text(encoding="utf-8")
    initiative_text = initiative.read_text(encoding="utf-8")
    control_text = control_path.read_text(encoding="utf-8")

    try:
        version, headings = contract.template_contract(template)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"template inválido: {exc}")
        version, headings = "ERRO", []

    try:
        control = contract.read_control(control_text)
    except Exception as exc:  # noqa: BLE001
        blockers.append(f"controle inválido: {exc}")
        control = {}

    fail_if(version != "1.0.0", f"versão do template inesperada: {version}", blockers)
    fail_if(len(headings) != 15, f"template não possui 15 seções: {len(headings)}", blockers)
    fail_if(control.get("template_version") != version, "template e controle divergem em versão", blockers)
    fail_if(control.get("phase") != "complete", "controle não está em phase=complete", blockers)
    fail_if(control.get("pending") != {}, "controle ainda possui pendências", blockers)

    for needle in ("template_objeto.md", "checklist_objeto.md", "template vence"):
        fail_if(needle not in skill, f"skill de criação não referencia regra esperada: {needle}", blockers)
    fail_if("seis tipos" not in skill, "skill de criação não declara a lista fechada de seis tipos", blockers)
    for category in contract.CATEGORIES:
        fail_if(category not in skill, f"skill de criação não cita categoria de snippet: {category}", blockers)
    for needle in ("template_objeto.md", "A0_light", "aprovação automática confirma estrutura"):
        fail_if(needle not in checklist, f"checklist editorial perdeu salvaguarda: {needle}", blockers)
    fail_if(contract.TEMPLATE.as_posix() != "hub_padroes/readme/template_objeto.md",
            f"validador aponta para template inesperado: {contract.TEMPLATE}", blockers)
    fail_if(tuple(contract.CATEGORIES) != ("constants", "display", "ml", "spark", "testing", "visual"),
            "categorias do validador divergiram do contrato R12", blockers)
    fail_if("template_contract" not in (ROOT / "tools/readme_objeto_contract.py").read_text(encoding="utf-8"),
            "validador não deriva contrato do template", blockers)
    fail_if("Na migração em andamento" in manual, "Manual mantém linguagem obsoleta de migração em andamento", blockers)
    fail_if("75 objetos" not in manual, "Manual não registra o fechamento dos 75 objetos", blockers)
    fail_if("R13" not in initiative_text, "índice da iniciativa não registra a auditoria R13", blockers)

    problems: list[str] = []
    counts = contract.check_readme_objects(ROOT / "ambiente_fonte", problems, repo=ROOT, previous=set())
    blockers.extend(f"contrato README: {p}" for p in problems)
    expected_counts = {
        "operational": 75,
        "present": 75,
        "exemplar": 3,
        "exemplar_present": 3,
        "pending": 0,
    }
    fail_if(counts != expected_counts, f"contagens de objeto inesperadas: {counts}", blockers)

    specs = contract.discover(ASSIST)
    by_kind = Counter(s.kind for s in specs if not s.exemplar)
    fail_if(dict(by_kind) != {"snippet": 52, "script": 7, "prompt": 16},
            f"composição operacional inesperada: {dict(by_kind)}", blockers)

    inventory = []
    for spec in sorted(specs, key=lambda s: s.path.as_posix()):
        folder = ASSIST / spec.path
        entry = {
            "path": spec.path.as_posix(),
            "kind": spec.kind,
            "exemplar": spec.exemplar,
            "readme_sha256": sha256(folder / "README.md"),
            "main_sha256": sha256(folder / spec.main),
            "example_sha256": sha256(folder / spec.example),
        }
        if spec.kind != "prompt":
            entry["init_sha256"] = sha256(folder / "__init__.py")
        inventory.append(entry)

    category_counts: dict[str, int] = {}
    for category in contract.CATEGORIES:
        root = ASSIST / "hub_snippets" / category
        index = root / "README.md"
        fail_if(not index.is_file(), f"índice de categoria ausente: {category}", blockers)
        children = {p.name for p in direct_object_dirs(root)}
        category_counts[category] = len(children)
        if index.is_file():
            linked = set(re.findall(r"\]\(([A-Za-z0-9_]+)/README\.md\)", index.read_text(encoding="utf-8")))
            fail_if(linked != children,
                    f"índice {category} diverge dos filhos: faltam={sorted(children-linked)} extras={sorted(linked-children)}",
                    blockers)
    fail_if(sum(category_counts.values()) != 52, f"índices cobrem {sum(category_counts.values())} snippets, esperado 52", blockers)
    fail_if((ASSIST / "hub_snippets/tests/README.md").exists(), "tests/ foi promovido indevidamente a categoria funcional", blockers)

    fail_if(manual_path.read_bytes() != root_manual.read_bytes(), "Manual fonte diverge da cópia raiz", blockers)

    # O renderer publica somente .assistant_instructions.md e .assistant/.
    users_root = ROOT / "Novo_Ambiente_Simulado/Users"
    users = sorted(p for p in users_root.iterdir() if p.is_dir()) if users_root.is_dir() else []
    fail_if(len(users) != 1, f"esperado um único usuário simulado, encontrados {len(users)}", blockers)
    if len(users) == 1:
        sim = users[0]
        src_instruction = ROOT / "ambiente_fonte/.assistant_instructions.md"
        dst_instruction = sim / ".assistant_instructions.md"
        fail_if(not dst_instruction.is_file(), "espelho ausente: .assistant_instructions.md", blockers)
        if dst_instruction.is_file():
            fail_if(src_instruction.read_bytes() != dst_instruction.read_bytes(), "espelho divergente: .assistant_instructions.md", blockers)

        ignored = {"__pycache__", ".pytest_cache", ".ruff_cache"}
        for src in sorted(ASSIST.rglob("*")):
            if not src.is_file() or any(part in ignored for part in src.parts) or src.suffix in {".pyc", ".pyo"}:
                continue
            rel = src.relative_to(ASSIST)
            dst = sim / ".assistant" / rel
            fail_if(not dst.is_file(), f"espelho ausente: .assistant/{rel}", blockers)
            if dst.is_file():
                fail_if(src.read_bytes() != dst.read_bytes(), f"espelho divergente: .assistant/{rel}", blockers)

    observations.extend([
        "A auditoria automática certifica estrutura, coerência interna e regressões; não certifica compreensão humana.",
        "A0_light: esta execução não é auditoria independente; o próprio fluxo da iniciativa registra essa limitação.",
        "Databricks Runtime, Spark opcional, publicação no workspace e testes conversacionais Genie Code não são convertidos em homologação por esta R13.",
        "Referências externas são inventariadas pelos READMEs, mas disponibilidade/conteúdo externo não é revalidado por este gate local.",
    ])

    result = {
        "sprint": "R13",
        "base": BASE,
        "status": "PASS" if not blockers else "FAIL",
        "template_version": version,
        "headings": headings,
        "counts": counts,
        "operational_by_kind": dict(sorted(by_kind.items())),
        "category_counts": category_counts,
        "inventory_count": len(inventory),
        "blockers": blockers,
        "observations": observations,
        "scope": {
            "template_checklist": True,
            "skill_criacao": True,
            "validator": True,
            "manual": True,
            "all_readmes": True,
            "category_indexes": True,
            "mirror": True,
            "databricks_homologation": False,
            "independent_audit": False,
        },
    }

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "AUDITORIA_R13.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "INVENTARIO_READMES_R13.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": result["status"],
        "objetos": counts,
        "por_tipo": dict(by_kind),
        "categorias": category_counts,
        "blockers": len(blockers),
    }, ensure_ascii=False))
    if blockers:
        for item in blockers:
            print(f"BLOCKER: {item}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
