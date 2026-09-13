from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
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
        raise RuntimeError(f"substituicao nao unica em {path}: {old[:100]!r}")
    write(path, text.replace(old, new, 1))


def main() -> None:
    index = DOCS / "README.md"
    old = "O contrato vigente é **1.0.0**. A R10 foi aceita e integrada pelo PR nº 30 no commit `7ba5d386`. A R11 documenta os nove Hub Prompts restantes em lotes A/B. A candidata busca fechar a migração estrutural em **75/75 operacionais e 3/3 exemplares, com 0 pendências**, sujeita ao validador real.\n\nConsulte o [relatório R11](RELATORIO_R11.md), a [matriz nominal](MATRIZ_ALTERACOES_R11.md) e os [achados](ACHADOS_R11.md). Fechar `pending` encerra a migração estrutural de READMEs, não homologação Databricks nem etapas posteriores da iniciativa."
    new = "O contrato vigente é **1.0.0**. A R11 foi aceita e integrada pelo PR nº 31 no commit `d51ca5dd`, encerrando a migração estrutural em **75/75 operacionais e 3/3 exemplares, com 0 pendências**. A R12 integra a navegação por categoria dos snippets e reconcilia essas rotas com o Manual e as entradas gerais.\n\nConsulte o [relatório R12](RELATORIO_R12.md), a [matriz nominal](MATRIZ_ALTERACOES_R12.md) e os [achados](ACHADOS_R12.md). A R12 é integração documental de navegação; não é homologação Databricks nem publicação no workspace."
    replace_once(index, old, new)

    sprints = ROOT / "docs/sprints/README.md"
    if "### READMEs R12 — integração de navegação" not in read(sprints):
        write(sprints, read(sprints).rstrip() + "\n\n### READMEs R12 — integração de navegação\nApós a R11 fechar 75/75 objetos, a R12 cria os seis índices de categoria de `hub_snippets` e reconcilia a navegação com o catálogo, a entrada `.assistant` e o Manual Técnico. Não altera implementação nem reabre a migração de objetos.\n")

    root = ROOT / "README.md"
    replace_once(root,
        "> **READMEs R11 — candidata:** nove guias finais de Hub Prompts; cobertura alvo 75/75 e zero pendências estruturais, sujeita ao freeze e aceite editorial.",
        "> **READMEs R11 — integrada:** nove guias finais de Hub Prompts foram aceitos e integrados pelo PR #31 (`d51ca5dd`), fechando 75/75 e zero pendências estruturais.\n>\n> **READMEs R12 — candidata:** seis índices de categoria de `hub_snippets` e reconciliação de navegação com as entradas gerais e o Manual Técnico."
    )

    write(DOCS / "RELATORIO_R12.md", "# Relatório R12 — integração de navegação por categoria\n\nR12 cria seis índices locais em `hub_snippets`: `constants`, `display`, `ml`, `spark`, `testing` e `visual`, e reconcilia o catálogo geral, a entrada `.assistant` e o Manual Técnico. Não cria objetos nem altera os 75 READMEs operacionais. `hub_snippets/tests/` permanece infraestrutura interna. O freeze exige cobertura exata, links válidos, equivalência fonte/simulado, snapshot real e `ci_local`. Não cobre publicação, Databricks Runtime, Genie Code ou auditoria independente.\n")

    write(DOCS / "MATRIZ_ALTERACOES_R12.md", "# Matriz de alterações R12\n\n| Caminho | Alteração |\n|---|---|\n| `hub_snippets/{constants,display,ml,spark,testing,visual}/README.md` | seis novos índices de categoria |\n| `hub_snippets/README.md` | categorias passam a apontar para os índices |\n| `.assistant/README.md` | rota direta para as seis categorias |\n| `MANUAL_TECNICO.md` fonte + cópia raiz | migração concluída + rotas por categoria |\n| documentação da iniciativa | estado R12, evidências e changelog |\n")

    write(DOCS / "ACHADOS_R12.md", "# Achados R12\n\n1. As seis categorias funcionais existiam, mas não possuíam `README.md` no nível da categoria.\n2. `hub_snippets/tests/` é regressão interna, não uma sétima categoria funcional.\n3. O Manual ainda dizia “migração em andamento” após a R11 encerrar 75/75.\n4. O catálogo geral já descrevia as categorias; R12 deve ligar a navegação existente, não reescrevê-la.\n")

    write(DOCS / "RUBRICA_R12.json", '{\n  "sprint": "R12",\n  "escopo": "navegacao_categoria",\n  "indices": 6,\n  "objetos_alterados": 0,\n  "gates": ["cobertura_indices", "links", "preservacao", "renderer", "ci_local"]\n}\n')

    changelog = ROOT / "CHANGELOG.md"
    heading = "## 2026-09-13 — R12: índices de categoria e navegação (ChatGPT)"
    if heading not in read(changelog):
        anchor = "Template: `.claude/templates/changelog-entry.md`.\n\n"
        entry = heading + "\n\n- Cria índices para as seis categorias funcionais de `hub_snippets`.\n- Liga catálogo geral, entrada `.assistant` e Manual aos índices sem alterar objetos.\n- Registra que a migração estrutural terminou na R11.\n- Mantém `hub_snippets/tests/` como infraestrutura interna.\n- Sem publicação, homologação runtime, auditoria independente, merge ou início da R13.\n\n"
        if anchor not in read(changelog):
            raise RuntimeError("ancora do changelog ausente")
        write(changelog, read(changelog).replace(anchor, anchor + entry, 1))


if __name__ == "__main__":
    main()
