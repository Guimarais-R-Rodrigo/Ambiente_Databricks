from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / "docs/sprints/readmes_objetos"
BASE = "ec4b559d098c96dfececbb17e52fbc276cb485c0"


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
        raise RuntimeError(f"substituição não única em {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))


def main() -> None:
    index = DOCS / "README.md"
    old = (
        "O contrato vigente é **1.0.0**. A R11 foi aceita e integrada pelo PR nº 31 no commit `d51ca5dd`, encerrando a migração estrutural em **75/75 operacionais e 3/3 exemplares, com 0 pendências**. A R12 integra a navegação por categoria dos snippets e reconcilia essas rotas com o Manual e as entradas gerais.\n\n"
        "Consulte o [relatório R12](RELATORIO_R12.md), a [matriz nominal](MATRIZ_ALTERACOES_R12.md) e os [achados](ACHADOS_R12.md). A R12 é integração documental de navegação; não é homologação Databricks nem publicação no workspace."
    )
    new = (
        "O contrato vigente é **1.0.0**. A R12 foi aceita e integrada pelo PR nº 32 no commit `ec4b559d`, preservando **75/75 operacionais, 3/3 exemplares e 0 pendências** e acrescentando os seis índices funcionais de `hub_snippets`. A R13 é a auditoria final consolidada desta iniciativa.\n\n"
        "Consulte o [relatório R13](RELATORIO_R13.md), a [matriz de auditoria](MATRIZ_AUDITORIA_R13.md), os [achados](ACHADOS_R13.md) e as evidências em `evidencias_r13/`. A R13 verifica coerência, regressões e integridade local; não transforma testes locais em homologação Databricks, publicação no workspace ou auditoria independente."
    )
    replace_once(index, old, new)

    sprints = ROOT / "docs/sprints/README.md"
    marker = "### READMEs R13 — auditoria final consolidada"
    if marker not in read(sprints):
        write(sprints, read(sprints).rstrip() + (
            "\n\n### READMEs R13 — auditoria final consolidada\n"
            "Após a integração da R12 pelo PR #32 (`ec4b559d`), a R13 audita em conjunto contrato, checklist, skill de criação, validador, Manual, 75 READMEs operacionais, três exemplares, seis índices de categoria e espelho derivado. A rodada é local e registra `A0_light`; homologação Databricks/Genie Code e auditoria independente permanecem gates separados.\n"
        ))

    root = ROOT / "README.md"
    old_root = "> **READMEs R12 — candidata:** seis índices de categoria de `hub_snippets` e reconciliação de navegação com as entradas gerais e o Manual Técnico."
    new_root = (
        "> **READMEs R12 — integrada:** seis índices de categoria de `hub_snippets` foram aceitos e integrados pelo PR #32 (`ec4b559d`), preservando 75/75 objetos e zero pendências estruturais.\n"
        ">\n"
        "> **READMEs R13 — auditoria final candidata:** revisão consolidada de contrato, checklist, skill de criação, validador, Manual, READMEs, índices e espelho, com mutantes negativos e regressão local."
    )
    replace_once(root, old_root, new_root)

    report = """# Relatório R13 — auditoria final consolidada\n\n## Objetivo\n\nA R13 encerra a iniciativa de READMEs por objeto com uma auditoria consolidada sobre o estado integrado após a R12. Ela não cria novos READMEs de objeto e não altera algoritmos, notebooks, templates, skill, Manual ou validador para fazer o gate passar.\n\n## Escopo auditado\n\n- contrato `template_objeto.md` e checklist editorial;\n- `hub-ml-criar-objeto`;\n- `tools/readme_objeto_contract.py`;\n- Manual Técnico fonte e cópia raiz;\n- 75 READMEs operacionais e três exemplares;\n- seis índices funcionais de `hub_snippets`;\n- `CONTROLE_MIGRACAO.json`;\n- equivalência `ambiente_fonte/` → `Novo_Ambiente_Simulado/`;\n- regressões permanentes via `ci_local.py`;\n- mutantes negativos do contrato.\n\n## Método\n\nA auditoria executa os gates reais e adiciona verificações de coerência entre as fontes de verdade. Uma suíte de mutantes introduz defeitos sintéticos em cópia temporária para provar que o contrato reprova README ausente, ordem de seções inválida, link quebrado, categoria desconhecida, versão divergente e dispensa reintroduzida.\n\n## Preservação\n\nArquivos de produto ficam congelados na base `ec4b559d098c96dfececbb17e52fbc276cb485c0`. Alterações permitidas na R13 são documentação de fechamento, evidências e o snapshot verificável do README raiz. Qualquer defeito de produto encontrado deve aparecer primeiro em `ACHADOS_R13.md`; não é corrigido silenciosamente.\n\n## Independência e limites\n\nEsta rodada é `A0_light`: o mesmo agente que conduziu a iniciativa executa a auditoria final local. Portanto, ela não é auditoria independente. Também não publica no workspace e não homologa Databricks Runtime, Spark opcional ou comportamento conversacional da Genie Code.\n\n## Resultado\n\nO resultado técnico é preenchido pelas evidências geradas no freeze R13. Aprovação automática significa estrutura/coerência/regressões locais aprovadas; aceite humano continua sendo gate separado.\n"""
    write(DOCS / "RELATORIO_R13.md", report)

    findings = """# Achados R13\n\n## Estado inicial\n\nA auditoria começa sem presumir ausência de defeitos. Achados bloqueadores serão registrados aqui antes de qualquer correção de produto.\n\n## Limitações conhecidas, não tratadas como defeito local\n\n1. A revisão é `A0_light`, não independente.\n2. Não há publicação no workspace nesta sprint.\n3. Databricks Runtime, Spark opcional e testes conversacionais Genie Code permanecem gates próprios.\n4. Referências externas não são reconsultadas integralmente pela auditoria local; o gate confere coerência e links que pertencem ao produto.\n\n## Resultado do freeze\n\nPendente até a execução do workflow R13.\n"""
    write(DOCS / "ACHADOS_R13.md", findings)

    matrix = """# Matriz de auditoria R13\n\n| Dimensão | Fonte de verdade | Verificação |\n|---|---|---|\n| Estrutura do README | `hub_padroes/readme/template_objeto.md` | versão 1.0.0 e 15 seções derivadas do template |\n| Rubrica editorial | `hub_padroes/readme/checklist_objeto.md` | salvaguardas, estados e `A0_light` |\n| Criação futura | `skills/hub-ml-criar-objeto/SKILL.md` | referência ao template/checklist, seis tipos e seis categorias |\n| Gate estrutural | `tools/readme_objeto_contract.py` | descoberta, cobertura, links, artefatos e ratchet |\n| Cobertura | árvore `.assistant` | 75/75 operacionais, 3/3 exemplares, 0 pendentes |\n| Composição | árvore `.assistant` | 52 snippets, 7 scripts, 16 prompts |\n| Navegação | seis índices R12 | filhos diretos = links dos índices |\n| Manual | fonte + raiz | igualdade byte a byte e estado pós-migração |\n| Espelho | `ambiente_fonte/` + simulado | equivalência byte a byte de arquivos publicáveis |\n| Sensibilidade do gate | mutantes R13 | seis defeitos sintéticos devem ser rejeitados |\n| Regressão | `tools/ci_local.py` | todas as etapas locais aprovadas |\n| Homologação Databricks | fora do escopo | não inferida a partir dos testes locais |\n"""
    write(DOCS / "MATRIZ_AUDITORIA_R13.md", matrix)

    rubric = """{
  "sprint": "R13",
  "base": "ec4b559d098c96dfececbb17e52fbc276cb485c0",
  "natureza": "auditoria_final_local",
  "nivel_revisao": "A0_light",
  "produto_congelado": true,
  "criterios": [
    "contrato_e_checklist_coerentes",
    "skill_criacao_coerente",
    "75_de_75_operacionais",
    "3_de_3_exemplares",
    "0_pendencias",
    "seis_indices_exatos",
    "espelho_equivalente",
    "mutantes_rejeitados",
    "ci_local_aprovado"
  ],
  "nao_coberto": [
    "auditoria_independente",
    "publicacao_workspace",
    "databricks_runtime",
    "spark_opcional_integral",
    "genie_code_conversacional",
    "aceite_humano"
  ]
}
"""
    write(DOCS / "RUBRICA_R13.json", rubric)

    freeze = DOCS / "evidencias_r13/FREEZE_R13.txt"
    if not freeze.exists():
        write(freeze, "R13 — placeholder versionado antes do snapshot final. O workflow substitui este conteúdo sem criar novo caminho.\n")

    changelog = ROOT / "CHANGELOG.md"
    heading = "## 2026-09-13 — R13: auditoria final da iniciativa de READMEs (ChatGPT)"
    if heading not in read(changelog):
        anchor = "Template: `.claude/templates/changelog-entry.md`.\n\n"
        entry = (
            heading + "\n\n"
            "- Audita contrato, checklist, skill de criação, validador, Manual, 75 READMEs, três exemplares e seis índices de categoria.\n"
            "- Adiciona inventário por SHA-256 e mutantes negativos para demonstrar sensibilidade do gate.\n"
            "- Congela produto na base pós-R12; correções de produto não são feitas silenciosamente pela auditoria.\n"
            "- Registra revisão `A0_light`: não é auditoria independente nem homologação Databricks/Genie Code.\n"
            "- Sem publicação no workspace, merge antecipado ou início de outra iniciativa.\n\n"
        )
        if anchor not in read(changelog):
            raise RuntimeError("âncora do changelog ausente")
        write(changelog, read(changelog).replace(anchor, anchor + entry, 1))


if __name__ == "__main__":
    main()
