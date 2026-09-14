from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def rw(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if text.count(old) != 1:
        raise RuntimeError(f"substituicao nao unica em {path}: {old[:120]!r} -> {text.count(old)}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8").rstrip()
    if marker in text:
        return
    path.write_text(text + "\n\n" + block.rstrip() + "\n", encoding="utf-8")


# Índice de governança: estado vigente do Sistema de Temas.
p = ROOT / "docs/README.md"
rw(
    p,
    "## Sistema de Temas — execução candidata\n\n[Diagnóstico V00 e próximos critérios de aceite](sprints/sistema_temas/README.md). Sem mudança no visual do produto.",
    "## Sistema de Temas — estado vigente no Git\n\n[V00–V04 estão aceitas e integradas no Git](sprints/sistema_temas/README.md). A D05 reconcilia somente documentação viva e não é a sprint funcional V05. Continuam separados: publicação no Databricks, homologação visual/runtime, auditoria independente e avaliação com usuário iniciante.",
)

# Índice de ADRs: status corrente sem reescrever o corpo decisório.
p = ROOT / "docs/decisions/README.md"
rw(
    p,
    "| [0013](ADR-0013-sistema-de-temas.md) | contrato central de temas e aplicação explícita por contexto | aceito para V01; integração Git condicionada aos checks; sem homologação de runtime |",
    "| [0013](ADR-0013-sistema-de-temas.md) | contrato central de temas e aplicação explícita por contexto | aceito; V01–V04 integradas no Git; sem publicação ou homologação visual/runtime |",
)

# ADR: acrescentar registro de implementação; corpo anterior permanece intacto.
p = ROOT / "docs/decisions/ADR-0013-sistema-de-temas.md"
append_once(
    p,
    "## Registro de implementação V02–V04 e reconciliação D05",
    """## Registro de implementação V02–V04 e reconciliação D05 — 2026-09-13

Após a ratificação da V01, a implementação evoluiu de forma aditiva sem alterar a decisão arquitetural: V02 promoveu o schema e integrou o núcleo de carga/validação/resolução; V03 integrou o adaptador Plotly opt-in; V04 integrou rotas opt-in para componentes HTML, estilos compartilhados e tabela pandas, preservando as APIs legadas como default.

Os estados de integração estão registrados nos checkpoints e READMEs próprios da iniciativa. A D05 apenas reconcilia documentos vivos que ainda usavam rótulos pré-merge como “candidata”; não cria a sprint funcional V05, não modifica o contrato visual 0.1.0, não altera APIs e não reclassifica testes Git/locais como publicação ou homologação Databricks.

Permanecem separados: publicação no workspace, homologação visual/runtime, acessibilidade, auditoria independente, avaliação com usuário iniciante e qualquer etapa posterior do plano V00–V14.""",
)

# Índice vivo da iniciativa: D05 documental não é V05 funcional.
p = ROOT / "docs/sprints/sistema_temas/README.md"
rw(
    p,
    "## Etapa concluída — V04 aceita e integrada no Git",
    "## Estado vigente — V04 aceita e integrada no Git; documentação viva reconciliada em D05",
)
rw(
    p,
    "Não houve publicação Databricks, auditoria independente ou homologação visual.\nO aceite e a integração Git da V04 estão concluídos; esses gates operacionais\npermanecem separados. A V05 ainda não foi iniciada por este fechamento.",
    "Não houve publicação Databricks, auditoria independente ou homologação visual.\nO aceite e a integração Git da V04 estão concluídos; esses gates operacionais\npermanecem separados. A [D05 documental](RECONCILIACAO_DOCUMENTAL_D05.md) sincroniza os rótulos vivos pós-merge e **não** inicia a sprint funcional V05 do plano.",
)

# Registro específico D05. Novo documento corrente; nada em V00/..V04/ é reescrito.
p = ROOT / "docs/sprints/sistema_temas/RECONCILIACAO_DOCUMENTAL_D05.md"
if not p.exists():
    p.write_text("""# D05 — reconciliação documental do Sistema de Temas

## Natureza

D05 é uma etapa **documental de manutenção** criada após a reconciliação pós-R13. Ela não é a sprint funcional V05 do plano V00–V14 e não implementa novas capacidades visuais.

## Estado canônico usado

- V01: contrato aceito e integrado no Git;
- V02: núcleo de carga, validação e resolução integrado no Git;
- V03: adaptador Plotly opt-in integrado no Git;
- V04: componentes HTML, estilos compartilhados e tabela pandas por rotas `_resolvido`, aceitos e integrados no Git;
- APIs legadas permanecem o default;
- publicação Databricks, homologação visual/runtime, acessibilidade, auditoria independente e avaliação com usuário iniciante permanecem separadas.

## Derivas corrigidas

D05 reconcilia apenas superfícies vivas que ainda continham rótulos pré-merge: padrão de identidade visual, guia operacional, índices de padrões/snippets, Manual Técnico, índice de governança, índice de ADRs e índice da iniciativa.

O `CHANGELOG.md` ganha uma entrada nova de fechamento em vez de apagar a nota histórica de que V04 era candidata antes do aceite. O ADR-0013 recebe somente um registro datado de implementação; seu corpo decisório e sua ratificação V01 permanecem preservados.

## Preservação

Os diretórios `docs/sprints/sistema_temas/V00*`, `V01/`, `V02/`, `V03/` e `V04/`, seus checkpoints, relatórios e resultados históricos não são reescritos. Implementações, schemas, testes e APIs também ficam congelados nesta etapa.

## Gates

A candidata D05 deve passar renderer, `validate_assistant.py --conferir-readme`, guarda de deriva específica, `ci_local.py`, `git diff --check` e CIs permanentes. Esses gates são locais/Git e não substituem homologação no Databricks.
""", encoding="utf-8")

# Registro pós-R13 agrega D05 sem misturá-la com V05 funcional.
p = ROOT / "docs/sprints/documentacao_pos_r13.md"
append_once(
    p,
    "## D05 — Sistema de Temas",
    """## D05 — Sistema de Temas

D05 reconcilia documentação viva do Sistema de Temas após V04: remove rótulos pré-merge em agregadores e padrões, atualiza o estado corrente do ADR-0013 e preserva integralmente a documentação histórica V00–V04. D05 não é a sprint funcional V05 e não adiciona capacidade de runtime.""",
)

# Changelog: nova entrada de estado; não alterar a nota histórica V04 candidata.
p = ROOT / "CHANGELOG.md"
text = p.read_text(encoding="utf-8")
heading = "## 2026-09-13 — D05: reconciliação documental do Sistema de Temas (ChatGPT)"
if heading not in text:
    anchor = "Template: `.claude/templates/changelog-entry.md`.\n\n"
    entry = (
        heading + "\n\n"
        "- Alinha documentação viva ao estado V00–V04 aceito e integrado no Git.\n"
        "- Preserva notas históricas de candidatura e registra o fechamento por nova entrada, sem reescrever evidência.\n"
        "- D05 é manutenção documental e não inicia a sprint funcional V05.\n"
        "- Sem publicação Databricks, homologação visual/runtime, auditoria independente ou mudança de API.\n\n"
    )
    if anchor not in text:
        raise RuntimeError("ancora do changelog ausente")
    p.write_text(text.replace(anchor, anchor + entry, 1), encoding="utf-8")

print("D05 governanca: estado vivo reconciliado; historicos V00-V04 preservados")
