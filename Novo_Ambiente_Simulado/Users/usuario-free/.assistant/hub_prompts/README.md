# `hub_prompts` — biblioteca personalizada de prompts para Genie Code

> **EXTENSÃO DO HUB (`hub_`) — NÃO AUTO-DESCOBERTA.** Esta pasta não é uma
> estrutura institucional da Databricks e seu conteúdo não é carregado
> automaticamente pelo Genie Code. O prefixo `hub_` torna essa diferença explícita.

## Para que serve

Estes arquivos são formulários reutilizáveis para preparar pedidos claros e
reprodutíveis. Eles complementam, mas não substituem:

- `.assistant_instructions.md`, usado para preferências globais do usuário;
- `AGENTS.md`, descoberto automaticamente no diretório do projeto e em seus
  diretórios ancestrais;
- `.assistant/skills/<nome>/SKILL.md`, carregado quando relevante ou quando a skill
  é mencionada com `@`.

## Uso recomendado

1. Abra o prompt adequado e substitua cada `{{CAMPO}}`. Use `NÃO INFORMADO` quando
   algo for desconhecido; não deixe placeholders sem intenção.
2. No painel do Genie Code, clique em **Add context** para anexar notebooks, queries,
   pipelines, tabelas ou arquivos. Alternativamente, digite `@<recurso>`.
3. Para uma skill específica, digite `@` e selecione a skill indicada no prompt.
4. Cole apenas o bloco **Prompt pronto para colar** no chat.
5. Revise o plano, os pressupostos e o impacto antes de autorizar execução ou escrita.

### Como preencher sem adivinhar

Cada prompt traz uma tabela `campo → como preencher → por que importa → exemplo`.
Use estes critérios em conjunto:

| Tipo de campo | Regra de preenchimento | Erro que evita |
|---|---|---|
| Recurso | use `@recurso` ou nome `catalog.schema.table`; confirme que foi anexado | analisar outro objeto ou inventar schema |
| Grão, chave e tempo | descreva uma linha, a chave e o instante de observação | duplicidade, leakage e comparação incoerente |
| Target/métrica | defina evento positivo, unidade, direção e horizonte | otimizar a medida errada |
| Restrições | declare PII, permissões, custo, prazo e o que não pode mudar | escrita ou coleta indevida |
| Modo | escolha plano, código, execução ou deploy; execução/escrita exige autorização separada | confundir proposta com ação realizada |

`NÃO INFORMADO` torna uma lacuna visível; não autoriza o assistente a inventar.
`NÃO APLICÁVEL` afirma que o campo foi avaliado e não pertence ao caso. Use-os
deliberadamente.

O contexto selecionado persiste no chat. Para um tema diferente, prefira um novo
chat para evitar que decisões antigas contaminem a resposta.

## Um formulário do início ao fim

O percurso abaixo usa `eda_rapida/eda_rapida.md`. Vale para todos: muda o formulário,
não o método.

**Passo 1 — o modelo, como está no arquivo.** Cada `{{CAMPO}}` é uma decisão que
você toma, não um enfeite. Trecho do bloco a colar:

```text
CONTEXTO
- Tabela/DataFrame: {{TABELA_OU_DF}}
- Objetivo de negócio: {{OBJETIVO}}
- Foco: {{FOCO}}
- Chave esperada: {{PK_OU_NAO_INFORMADO}}
- Coluna temporal: {{COL_DATA_OU_NAO_INFORMADO}}
- Limite de execução: {{TEMPO_CUSTO_OU_NAO_INFORMADO}}
```

**Passo 2 — o mesmo trecho preenchido.** Repare no uso de `NÃO INFORMADO`: ele
comunica "eu não sei", que é diferente de deixar o campo em branco. Campo em
branco o Genie Code tende a preencher sozinha, e passa a trabalhar sobre uma
suposição que você não fez.

```text
CONTEXTO
- Tabela/DataFrame: catalogo.crm.clientes_pf
- Objetivo de negócio: avaliar se a base serve de população para um modelo de propensão a consórcio
- Foco: completude das variáveis de renda e ocupação, e duplicidade de cliente
- Chave esperada: id_cliente
- Coluna temporal: dt_referencia
- Limite de execução: leitura leve, sem varredura completa da tabela
```

**Passo 3 — anexe o recurso.** Antes de colar, adicione a tabela ao chat com
**Add context** ou `@`. O formulário descreve o que fazer; ele não dá acesso ao
dado. Sem o anexo, a resposta vem genérica.

**Passo 4 — o que esperar de volta.** Pelo contrato declarado no próprio
formulário, a resposta deve trazer um plano curto antes de qualquer execução, o
quadro de dimensão/evidência/severidade/ação, e a lista do que ficou pendente.
Se vier código executado sem plano prévio, o contrato não foi respeitado — vale
recusar e pedir de novo apontando a etapa pulada.

> **Retorno real ainda não capturado.** Uma execução verdadeira deste formulário
> no Genie Code, com a resposta colada aqui, fecharia o exemplo. Enquanto não for
> feita, o passo 4 descreve o contrato esperado em vez de mostrar o resultado —
> preferimos assumir a lacuna a inventar uma resposta plausível.

## Cada prompt é uma pasta, com o notebook que o demonstra

```text
hub_prompts/<nome>/
├── <nome>.md                   # o briefing, com os placeholders
└── exemplo_<nome>.py           # o notebook de três partes
```

O notebook **não executa o prompt** — nenhum notebook executa. Ele tem três
partes, e só as duas primeiras rodam:

| Parte | O que é | Roda? |
|---|---|---|
| 1 | preparo: cria a base sintética ou localiza o recurso a que o prompt se refere | **sim** |
| 2 | o prompt preenchido, pronto para copiar | não; é texto |
| 3 | a resposta real do Genie Code, colada de um chat | **exige uma pessoa** |

**A parte 3 está em branco nos dezesseis**, com instrução de como preencher. Não
é esquecimento: prompt produz resposta de assistente, e resposta inventada é pior
que resposta nenhuma — ela ensina que o assistente faz algo que ele não faz.

Quem for preencher: rode a Parte 1, cole a Parte 2 num **chat novo**, e registre
a resposta com a data, **qual skill foi carregada** e o que o assistente deixou
de fora. A segunda metade do comentário é a que ensina.

## Catálogo

| Tema | Pasta | Skill recomendada |
|---|---|---|
| EDA completa | [`eda_completa/`](eda_completa/eda_completa.md) | `@hub-ml-eda-profissional` |
| Perfil rápido | [`eda_rapida/`](eda_rapida/eda_rapida.md) | `@hub-ml-eda-profissional` |
| Qualidade de dados | [`data_quality/`](data_quality/data_quality.md) | `@hub-ml-eda-profissional` |
| Cross-EDA | [`cross_eda/`](cross_eda/cross_eda.md) | `@hub-ml-cross-eda-ml` |
| Feature engineering | [`feature_engineering/`](feature_engineering/feature_engineering.md) | `@hub-ml-feature-engineering` |
| Validação estatística | [`stat_check/`](stat_check/stat_check.md) | `@hub-ml-validacao-estatistica` |
| Baseline de ML | [`baseline_orchestration/`](baseline_orchestration/baseline_orchestration.md) | `@hub-ml-baseline-ml` |
| Explicabilidade | [`explainability/`](explainability/explainability.md) | `@hub-ml-explainability` |
| Monitoramento | [`monitoramento_modelo/`](monitoramento_modelo/monitoramento_modelo.md) | `@hub-ml-monitoramento-modelo` |
| Pipeline de dados | [`pipeline/`](pipeline/pipeline.md) | `@hub-ml-pipeline-builder` |
| Safra/vintage | [`safra/`](safra/safra.md) | `@hub-ml-analise-safra` |
| Auditoria de skills | [`auditoria_skills/`](auditoria_skills/auditoria_skills.md) | `@hub-ml-auditoria-skills` |
| Documentar notebook | [`comentar_notebook/`](comentar_notebook/comentar_notebook.md) | `@hub-ml-comentar-notebook` |
| Explicação/tutoria | [`tutor_explicar/`](tutor_explicar/tutor_explicar.md) | `@hub-ml-tutor-databricks` |
| Comparar tabelas | [`comparar_tabelas/`](comparar_tabelas/comparar_tabelas.md) | conforme o objetivo |
| Iniciar projeto | [`novo_projeto/`](novo_projeto/novo_projeto.md) | conforme o projeto |

## Sobre os atalhos `/...`

Expressões como `/eda`, `/baseline` e `/stat-check` são **convenções pessoais de
texto** mantidas por compatibilidade. Não são comandos registrados do Genie Code.
O comando `/findTables` é uma funcionalidade documentada pela Databricks; os
demais atalhos deste catálogo dependem da interpretação do texto e não devem ser
usados como único mecanismo de roteamento. Para execução determinística, mencione
a skill com `@` e forneça o contexto explicitamente.

## Princípios incorporados

- pedido específico, guia de preenchimento, nível de detalhe e formato de saída explícitos;
- recursos adicionados com **Add context** ou `@`;
- nomes de tabelas em três níveis (`catalog.schema.table`) quando conhecidos;
- pressupostos e campos ausentes sinalizados, nunca inventados;
- separação entre análise, geração de código, execução e mutação;
- amostragem/limites em exploração e processamento distribuído para volume alto;
- proteção de dados sensíveis e nenhuma exposição de valores identificáveis;
- validação técnica antes de recomendar produção.

## Fontes oficiais

- [Tips to improve Genie Code responses](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [Extend Genie Code with agent skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Customize Genie Code with custom instructions](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)

---

Última revisão: 2026-08-13.
