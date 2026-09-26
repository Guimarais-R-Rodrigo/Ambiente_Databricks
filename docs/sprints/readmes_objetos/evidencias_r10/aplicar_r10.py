from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = "d412acb750ce0f4011f97416c74fe7a685863772"
NAMES = (
    "comparar_tabelas",
    "cross_eda",
    "data_quality",
    "eda_completa",
    "feature_engineering",
    "stat_check",
)
PROMPTS = ROOT / "ambiente_fonte/.assistant/hub_prompts"
DOCS = ROOT / "docs/sprints/readmes_objetos"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = read(path)
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError(f"substituicao nao unica em {path}: {old[:80]!r}")
    write(path, text.replace(old, new, 1))


def edit_notebooks() -> None:
    for name in NAMES:
        path = PROMPTS / name / f"exemplo_{name}.py"
        text = read(path)
        backlink = "# MAGIC 📘 Guia local: [`README.md`](./README.md)"
        if backlink not in text:
            title = f"# MAGIC # `{name}`"
            pos = text.find(title)
            if pos < 0:
                raise RuntimeError(f"titulo nao encontrado: {path}")
            end = text.find("\n", pos)
            if end < 0:
                raise RuntimeError(f"fim de titulo nao encontrado: {path}")
            text = text[: end + 1] + "# MAGIC\n" + backlink + "\n" + text[end + 1 :]
        write(path, text)

    fixes = {
        "comparar_tabelas": (
            "| Escrita | **sim** — cria a tabela `workspace.default.hub_exemplo_clientes_v1` para o chat poder consultá-la |",
            "| Escrita | **sim** — cria/sobrescreve as tabelas `workspace.default.hub_exemplo_clientes_v1` e `workspace.default.hub_exemplo_clientes_v2` para o chat poder consultá-las |",
        ),
        "cross_eda": (
            "| Escrita | **sim** — cria a tabela `workspace.default.hub_exemplo_fatos` para o chat poder consultá-la |",
            "| Escrita | **sim** — cria/sobrescreve as tabelas `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features` para o chat poder consultá-las |",
        ),
        "feature_engineering": (
            "| Escrita | **sim** — cria a tabela `workspace.default.hub_exemplo_fatos` para o chat poder consultá-la |",
            "| Escrita | **sim** — cria/sobrescreve as tabelas `workspace.default.hub_exemplo_fatos` e `workspace.default.hub_exemplo_features` para o chat poder consultá-las |",
        ),
    }
    for name, (old, new) in fixes.items():
        replace_once(PROMPTS / name / f"exemplo_{name}.py", old, new)


def edit_control() -> None:
    path = DOCS / "CONTROLE_MIGRACAO.json"
    lines = read(path).splitlines()
    removed = []
    out = []
    for line in lines:
        matched = next((name for name in NAMES if f'"hub_prompts/{name}"' in line), None)
        if matched:
            removed.append(matched)
            continue
        out.append(line)
    if set(removed) not in (set(), set(NAMES)):
        raise RuntimeError(f"controle parcialmente alterado: {removed}")
    write(path, "\n".join(out) + "\n")


def edit_catalog() -> None:
    path = PROMPTS / "README.md"
    text = read(path)
    for name in NAMES:
        old = f"- **Arquivos:** `hub_prompts/{name}/{name}.md` · `hub_prompts/{name}/exemplo_{name}.py`"
        new = old + f" · [README local]({name}/README.md)"
        if new in text:
            continue
        if text.count(old) != 1:
            raise RuntimeError(f"entrada de catalogo nao unica: {name}")
        text = text.replace(old, new, 1)
    write(path, text)


def edit_indexes() -> None:
    initiative = DOCS / "README.md"
    old = (
        "O contrato vigente é **1.0.0**. A R08 foi aceita e integrada pelo PR nº 27 no commit `d5945e0`. A R09 documenta `curves_plotly`, `drift_detection`, `metrics_report`, `mlflow_run` e `performance_monitor`, preservando implementações/fachadas. A cobertura candidata é **60/75 operacionais e 3/3 exemplares, com 15 pendências**; o validador da árvore fechada é fonte de verdade.\n\n"
        "Consulte o [relatório R09](RELATORIO_R09.md), a [matriz nominal](MATRIZ_ALTERACOES_R09.md), os [achados](ACHADOS_R09.md) e o [registro de recuperação](RECUPERACAO_R09.md). A próxima parada é freeze técnico e revisão antes da R10."
    )
    new = (
        "O contrato vigente é **1.0.0**. A R09 foi aceita e integrada pelo PR nº 29 no commit `d412acb`. A R10 documenta seis Hub Prompts: `comparar_tabelas`, `cross_eda`, `data_quality`, `eda_completa`, `feature_engineering` e `stat_check`. A cobertura candidata é **66/75 operacionais e 3/3 exemplares, com 9 pendências**; o validador da árvore fechada é fonte de verdade.\n\n"
        "Consulte o [relatório R10](RELATORIO_R10.md), a [matriz nominal](MATRIZ_ALTERACOES_R10.md) e os [achados](ACHADOS_R10.md). A próxima parada é freeze técnico e revisão antes da R11."
    )
    replace_once(initiative, old, new)

    sprints = ROOT / "docs/sprints/README.md"
    marker = "### READMEs R10\n"
    if marker not in read(sprints):
        text = read(sprints).rstrip() + (
            "\n\n### READMEs R10\n"
            "Após a integração da R09 pelo PR #29 (`d412acb`), a R10 cobre seis Hub Prompts de exploração, qualidade, reconciliação, feature engineering e validação estatística. A cobertura alvo é 66/75 operacionais + 3/3 exemplares, sujeita ao validador e ao aceite editorial.\n"
        )
        write(sprints, text)

    root = ROOT / "README.md"
    old_root = "> **READMEs R09 — candidata:** cinco guias de avaliação, drift e MLOps; cobertura alvo 60/75, sujeita ao freeze e aceite."
    new_root = (
        "> **READMEs R09 — integrada:** cinco guias de avaliação, drift e MLOps foram aceitos e integrados pelo PR #29 (`d412acb`).\n"
        ">\n"
        "> **READMEs R10 — candidata:** seis guias de Hub Prompts; cobertura alvo 66/75, sujeita ao freeze e aceite editorial."
    )
    replace_once(root, old_root, new_root)


def write_docs() -> None:
    report = f"""# Relatório R10 — Hub Prompts\n\n## Escopo\n\nDocumentar seis prompts do lote R10-A: `comparar_tabelas`, `cross_eda`, `data_quality`, `eda_completa`, `feature_engineering` e `stat_check`. Os briefings `.md` permanecem byte a byte iguais à base `{BASE}`.\n\n## Meta\n\nBase integrada: 60/75 operacionais, 15 pendências. Meta candidata: **66/75 operacionais, 3/3 exemplares e 9 pendências**, sujeita ao validador real.\n\n## Alterações editoriais\n\nOs seis notebooks recebem backlink para o README. `comparar_tabelas`, `cross_eda` e `feature_engineering` corrigem somente a descrição Markdown da escrita persistente: o código já criava duas tabelas, embora a tabela de pré-requisitos citasse apenas uma. Nenhuma célula executável ou saída histórica é alterada.\n\n## Validação\n\nO freeze exige contrato 1.0.0, gate permanente, preservação byte a byte dos seis briefings, equivalência dos notebooks após reversão apenas das edições declaradas, renderer do simulado e conferência do snapshot do README raiz. Interação Genie Code e homologação Databricks permanecem gates separados.\n\n## Estado\n\nCandidata R10 em construção; nenhum aceite editorial ou merge é presumido.\n"""
    write(DOCS / "RELATORIO_R10.md", report)

    matrix = "# Matriz de alterações R10\n\n| Objeto | README | Briefing `.md` | Notebook |\n|---|---|---|---|\n" + "\n".join(
        f"| `{n}` | novo, contrato 1.0.0 | preservado byte a byte | backlink Markdown" + (" + errata de escrita" if n in {"comparar_tabelas", "cross_eda", "feature_engineering"} else "") + " |"
        for n in NAMES
    ) + "\n\nOutras alterações: catálogo de Hub Prompts, controle de migração, índices/checkpoints, README raiz, changelog, simulado e evidências da R10.\n"
    write(DOCS / "MATRIZ_ALTERACOES_R10.md", matrix)

    findings = """# Achados R10\n\n1. Todos os seis objetos são prompts: o arquivo principal é briefing textual e não execução automática.\n2. Todos os notebooks de exemplo possuem preparo com escrita persistente via `overwrite`; o README precisa separar o efeito do exemplo do efeito do prompt.\n3. `comparar_tabelas`, `cross_eda` e `feature_engineering` descreviam uma única tabela na linha de pré-requisitos, mas o código cria duas; a candidata corrige apenas essa prosa.\n4. Respostas reais do Genie Code continuam marcadas como dependentes de interação humana; a sprint não fabrica evidência conversacional.\n"""
    write(DOCS / "ACHADOS_R10.md", findings)

    rubric = """{\n  \"sprint\": \"R10\",\n  \"contrato\": \"1.0.0\",\n  \"objetos\": 6,\n  \"revisao\": \"A0_light\",\n  \"gates\": [\"estrutura\", \"preservacao\", \"ci_local\", \"renderer\"],\n  \"nao_coberto\": [\"interacao_genie_code\", \"runtime_databricks\", \"publicacao_workspace\", \"auditoria_independente\", \"aceite_editorial\"]\n}\n"""
    write(DOCS / "RUBRICA_R10.json", rubric)

    evidence = DOCS / "evidencias_r10/FREEZE_R10.txt"
    if not evidence.exists():
        write(evidence, f"R10 freeze placeholder\nbase={BASE}\n")

    changelog = ROOT / "CHANGELOG.md"
    text = read(changelog)
    heading = "## 2026-09-13 — R10: READMEs de Hub Prompts (ChatGPT)"
    if heading not in text:
        anchor = "Template: `.claude/templates/changelog-entry.md`.\n\n"
        entry = (
            heading + "\n\n"
            "- Documenta seis prompts no contrato 1.0.0: `comparar_tabelas`, `cross_eda`, `data_quality`, `eda_completa`, `feature_engineering` e `stat_check`.\n"
            "- Preserva os seis briefings `.md`; notebooks recebem somente backlinks e três erratas Markdown sobre tabelas sintéticas já gravadas pelo código.\n"
            "- Retira exatamente seis dispensas R10 do controle de migração; cobertura alvo 66/75, sujeita ao validador.\n"
            "- Sem publicação Databricks, resposta Genie Code fabricada, auditoria independente, aceite editorial, merge ou início da R11.\n\n"
        )
        if anchor not in text:
            raise RuntimeError("ancora do changelog ausente")
        write(changelog, text.replace(anchor, anchor + entry, 1))


def update_snapshot(output_path: Path) -> None:
    output = read(output_path).strip()
    if "APROVADO: 0 falha(s), 0 aviso(s)" not in output:
        raise RuntimeError("validador inicial nao aprovado")
    path = ROOT / "README.md"
    text = read(path)
    heading = "### Estado verificável do gate local"
    start = text.find(heading)
    if start < 0:
        raise RuntimeError("secao de snapshot ausente")
    fence = text.find("```text\n", start)
    end = text.find("\n```", fence)
    if fence < 0 or end < 0:
        raise RuntimeError("bloco de snapshot ausente")
    prefix = text[: fence + len("```text\n")]
    suffix = text[end:]
    write(path, prefix + output + suffix)


def apply() -> None:
    edit_notebooks()
    edit_control()
    edit_catalog()
    edit_indexes()
    write_docs()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", type=Path)
    args = parser.parse_args()
    if args.snapshot:
        update_snapshot(args.snapshot)
    else:
        apply()


if __name__ == "__main__":
    main()
