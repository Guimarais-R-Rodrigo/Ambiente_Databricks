from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_exact(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Trecho esperado ausente em {path}")
    if text.count(old) != 1:
        raise SystemExit(f"Trecho esperado não é único em {path}: {text.count(old)}")
    path.write_text(text.replace(old, new), encoding="utf-8")


checkpoint = ROOT / "docs/sprints/sistema_temas/V03/CHECKPOINT_V03.md"
checkpoint.write_text(
    """# Checkpoint V03 — aceite e integração Git

## Estado vigente — 12/09/2026

Rodrigo concedeu aceite explícito à V03 e autorizou sua integração Git com a instrução
“pode integrar a V03”. O aceite cobre o adaptador Plotly opt-in, sua documentação,
os testes e as garantias de compatibilidade desta sprint. Não autoriza publicação no
Databricks, homologação de Spark/widgets/Apps/AI-BI, migração automática de outros
consumidores nem início da V04.

Para quem nunca entrou no Hub: o merge Git da V03 não exige alterar o uso atual.
Quem já chama `aplicar_tema(fig, ...)` continua usando a mesma API e o mesmo
comportamento legado. A nova rota só é usada quando alguém fornece explicitamente
um `ResolvedTheme` de contexto notebook. Não há seletor de temas nem mudança visual
automática nesta sprint.

## Evidência técnica antes da ratificação documental

A candidata técnica aceita era o head `22392e557557f0faf908acb8f4dd2a9d358d785f`,
árvore `9e92a3073dbbc202afa3db817a6d61e1c050440b`. Nesse estado, os cinco workflows
permanentes concluíram com sucesso: CI geral, V00, V01, V02 e V03. A suíte específica
V03 terminou com 26 testes aprovados. O code review manual do Codex concluiu sobre
essa mesma candidata sem novos achados; os cinco threads P2 anteriores estavam
respondidos e resolvidos.

A ratificação documental deste aceite precisa ser revalidada integralmente antes do
merge. O PR #16 é o registro autoritativo do head final, dos checks e da efetivação
do merge. A presença deste documento em uma branch não prova que a integração ocorreu.

## Garantias preservadas

1. nenhuma chamada legada muda de assinatura;
2. `legado_notebook` mapeia exatamente para `get_tema_eda()`;
3. a nova aplicação é explícita por figura e não altera `pio.templates.default`;
4. registro configurado usa namespace `hub-*` e só ativa globalmente com `ativar=True`;
5. substituir um template já ativo sem `ativar=True` falha antes de trocar o objeto,
   inclusive quando o nome participa de um default composto;
6. dados, eixos e cores explícitas dos traces permanecem intactos;
7. temas não-notebook, modos ainda não suportados e resultados V02 adulterados falham
   sem fallback silencioso;
8. nenhum consumidor existente é migrado implicitamente.

## Limites e gates ainda pendentes

Auditoria independente: PENDENTE. Avaliação com usuário iniciante: PENDENTE.
Homologação visual real no Databricks, Spark, widgets, Apps e AI/BI: NÃO REALIZADA.
Testes Python e GitHub Actions não substituem esses gates. Não houve publicação nem
acesso a dados corporativos.

## Recuperação

Se a integração precisar ser desfeita após o merge, preparar uma reversão em branch
própria, preservando mudanças posteriores e repetindo os gates. Não resetar a `main`,
não fazer force-push e não publicar um pacote antigo no Databricks para desfazer uma
mudança exclusivamente de repositório.

## Próxima etapa

Após a integração e a conferência pós-merge, a próxima sprint planejada é V04. O
aceite da V03 não inicia a V04 automaticamente.
""",
    encoding="utf-8",
)

v03 = ROOT / "docs/sprints/sistema_temas/V03/README.md"
v03.write_text(
    """# V03 — integração explícita do núcleo com Plotly

> **ACEITA POR RODRIGO · INTEGRAÇÃO GIT AUTORIZADA · 12/09/2026.** A V02 está aceita e integrada. A V03 acrescenta uma rota opt-in para Plotly e preserva os gráficos existentes por padrão. O PR #16 registra a efetivação do merge; este texto, isoladamente, não prova integração nem publicação.

## Para quem nunca entrou no Hub

Se você já usa `aplicar_tema(fig, ...)`, continue usando exatamente como hoje. A V03 não exige trocar código antigo nem escolher um novo tema. A nova rota existe para quando você quiser testar conscientemente uma configuração completa validada pelo núcleo V02.

A ordem segura é: obter/resolver uma configuração de notebook → aplicar à figura com a nova função → conferir visualmente → fazer ajustes específicos depois. Não registre template global para experimentar uma única figura.

O aceite desta sprint não publica nada no Databricks. Se a rota V03 vier a ser usada em um ambiente publicado no futuro, Plotly e as dependências de validação declaradas em `hub_snippets/requirements-temas.txt` precisam estar disponíveis; nenhuma função instala pacotes automaticamente.

## Escopo

A V03 conecta `hub_snippets.visual.tema.ResolvedTheme` ao helper `hub_snippets.visual.theme_plotly`. O adaptador consome somente tokens que o contrato 0.1.0 atribui ao Plotly: cor/tamanho de texto, título, paleta categórica, dimensões, margens e estilo do rodapé. Alinhamento de título, legenda e template-base continuam políticas fixas do adaptador porque ainda não são tokens configuráveis.

## Compatibilidade

As APIs legadas `get_tema_eda()`, `aplicar_tema(fig, subtitulo, fonte, n)` e `registrar_template_plotly()` permanecem com as mesmas assinaturas e comportamento observado. O novo caminho é aditivo:

- `get_tema_plotly(theme)` — produz configuração Plotly sem alterar sessão;
- `aplicar_tema_resolvido(fig, theme, ...)` — aplica explicitamente à figura e devolve o mesmo objeto;
- `registrar_template_plotly_resolvido(theme, *, nome, ativar=False, substituir=False)` — registra no namespace `hub-*`; só muda o default da sessão com `ativar=True` e recusa substituir um nome já ativo quando a ativação não é explícita.

## Fail-closed

A V03 aceita somente um `ResolvedTheme` íntegro do contexto `notebook`. Dicionário cru, resultado adulterado, contexto editorial/apresentação e modos `dark`/`high_contrast` são recusados nesta sprint. Os dois últimos continuam válidos no contrato, mas ainda faltam tokens de superfície do gráfico para uma aplicação Plotly completa sem inventar defaults implícitos.

Se um template `hub-*` já participa do default ativo, sozinho ou dentro de uma composição como `plotly+hub-*`, `substituir=True` com `ativar=False` é recusado antes da troca do objeto. Substituir esse nome exige assumir explicitamente o efeito global com `ativar=True`.

## O que não muda

Dados dos traces, títulos/ranges dos eixos e cores explicitamente definidas nos traces não são reescritos pelo adaptador. O simples import não altera `pio.templates.default`. A V03 não migra `correlation_matrix`, `distribution_grid`, curvas de ML ou qualquer consumidor existente; essas migrações precisam de decisão e testes próprios.

## Aceite técnico

Os critérios técnicos da candidata foram satisfeitos antes do aceite de Rodrigo: testes V03 e regressões V00/V01/V02 verdes; fixture `legado_notebook` equivalente ao layout legado; assinaturas antigas preservadas; aplicação nova sem alteração de dados/eixos/cores explícitas; efeitos de sessão opt-in; documentação/espelho sincronizados; CI transversal verde; code review final sem novo achado.

A ratificação do aceite é revalidada novamente antes do merge. O estado efetivo de integração e os SHAs finais pertencem ao PR #16 e à `main`, não a uma afirmação antecipada deste README.

## Limites

Sem publicação Databricks, sem alteração visual automática, sem homologação de Spark/widgets/Apps/AI-BI, sem V04/V05 e sem aprovação de qualquer fixture como tema operacional. Auditoria independente e avaliação com usuário iniciante continuam gates separados.

[Checkpoint](CHECKPOINT_V03.md) · [Testes](TESTES.md) · [V02](../V02/README.md)
""",
    encoding="utf-8",
)

initiative = ROOT / "docs/sprints/sistema_temas/README.md"
replace_exact(
    initiative,
    "## Etapa atual — V03 em desenvolvimento na branch `codex/temas-v03`",
    "## Etapa atual — V03 aceita; integração Git autorizada pelo PR #16",
)
replace_exact(
    initiative,
    "Os quatro checks pós-merge da V02 na `main` passaram. A V03 foi iniciada a partir dessa base verde e acrescenta somente uma rota Plotly opt-in; ainda não foi aceita nem integrada.",
    "Os quatro checks pós-merge da V02 na `main` passaram. A V03 foi iniciada a partir dessa base verde, acrescenta somente uma rota Plotly opt-in e recebeu aceite explícito de Rodrigo em 12/09/2026. A integração Git foi autorizada pelo PR #16; o estado efetivo do merge deve ser verificado na própria PR. Não houve publicação Databricks.",
)
replace_exact(
    initiative,
    "Para quem nunca entrou no Hub: **nada muda na aparência ou na rotina atual por causa\nda V02**. Ela valida uma configuração completa de tema, mas ainda não aplica o tema\na gráficos ou HTML, não cria seletor e não publica nada no Databricks. Comece pelo\n[README da V02](V02/README.md), depois leia o [checkpoint](V02/CHECKPOINT_V02.md) e o\n[guia operacional](../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md).",
    "Para quem nunca entrou no Hub: **nada muda automaticamente na aparência ou na rotina atual por causa\nda V03**. Quem já usa `aplicar_tema` continua no mesmo caminho legado. A V03 só acrescenta\numa rota Plotly opt-in para um `ResolvedTheme` de notebook; não cria seletor e não publica\nnada no Databricks. Comece pelo [README da V03](V03/README.md), depois leia o\n[checkpoint](V03/CHECKPOINT_V03.md) e o\n[guia operacional](../../../ambiente_fonte/.assistant/hub_padroes/identidade_visual/GUIA_OPERACIONAL.md).",
)
replace_exact(
    initiative,
    "A V02 está aceita e integrada no Git. A [V03](V03/README.md) está em desenvolvimento\nna branch `codex/temas-v03`: integra explicitamente o núcleo com Plotly preservando\no comportamento legado por padrão. Ainda não há aceite, merge ou publicação\nDatabricks; V04 e V05 não foram iniciadas.",
    "A V02 está aceita e integrada no Git. A [V03](V03/README.md) recebeu aceite explícito\nde Rodrigo e teve sua integração Git autorizada pelo PR #16: integra explicitamente o\nnúcleo com Plotly preservando o comportamento legado por padrão. O estado efetivo do\nmerge fica registrado na PR; não há publicação Databricks e V04/V05 não foram iniciadas.",
)

sprints = ROOT / "docs/sprints/README.md"
replace_exact(
    sprints,
    "históricas e dos READMEs. V00, [V01](sistema_temas/V01/README.md) e\n[V02](sistema_temas/V02/README.md) estão aceitas e integradas no Git. A V02 entrega\no núcleo de carga, validação e resolução de configurações completas, mas ainda não\naplica tema a Plotly/HTML, não cria seletor e não publica no Databricks.\n\nA [V03](sistema_temas/V03/README.md) está em desenvolvimento em branch separada e acrescenta apenas um adaptador Plotly opt-in; não migra consumidores existentes. A homologação operacional, a auditoria independente e a avaliação com usuário iniciante permanecem pendentes.",
    "históricas e dos READMEs. V00, [V01](sistema_temas/V01/README.md) e\n[V02](sistema_temas/V02/README.md) estão aceitas e integradas no Git. A V02 entrega\no núcleo de carga, validação e resolução de configurações completas.\n\nA [V03](sistema_temas/V03/README.md) recebeu aceite explícito de Rodrigo e teve sua integração Git autorizada pelo PR #16. Ela acrescenta apenas um adaptador Plotly opt-in, preserva o caminho legado por padrão e não migra consumidores existentes. O estado efetivo do merge é registrado na PR. Não houve publicação Databricks; homologação operacional, auditoria independente e avaliação com usuário iniciante permanecem pendentes.",
)

changelog = ROOT / "CHANGELOG.md"
replace_exact(
    changelog,
    "## 2026-09-12 — V03: adaptador Plotly opt-in (Codex)\n\n### Adicionado",
    "## 2026-09-12 — V03: adaptador Plotly opt-in (Codex)\n\n### Aceite e integração\n\n- (Codex) Rodrigo concedeu aceite explícito à V03 com a instrução \"pode integrar a V03\". A integração Git pelo PR #16 fica autorizada após revalidação da árvore exata; o aceite não autoriza publicação Databricks, homologação operacional, migração automática de outros consumidores nem início da V04.\n\n### Adicionado",
)
