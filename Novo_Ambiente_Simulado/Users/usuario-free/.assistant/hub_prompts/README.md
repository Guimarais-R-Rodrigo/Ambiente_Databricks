# `hub_prompts/` — briefings guiados para Genie Code

> **HUB · USO MANUAL.** Esta coleção não é uma estrutura institucional da
> Databricks e não é auto-descoberta. Escolha um arquivo, preencha os campos e
> anexe-o ou copie o bloco final para o chat.

Os prompts transformam um pedido vago em um contrato reproduzível: contexto,
objetivo, dados, modo de trabalho, limites, saída e QA.

## Comece em três passos

1. Escolha a família na [tabela abaixo](#catálogo).
2. Substitua todo `{{CAMPO}}` seguindo o guia do próprio arquivo.
3. Anexe os recursos com `@` e cole **Prompt pronto para colar**.

```text
@hub-ml-eda-profissional

Use o briefing anexado e @catalogo.schema.tabela.
Primeiro apresente o plano. Não execute nem escreva até minha aprovação.
```

Usar `@skill` é recomendado quando você precisa de rota determinística. Sem a
menção, o Genie Code ainda pode escolher uma skill relevante.

## O que existe dentro de cada prompt

| Bloco | Pergunta que resolve |
|---|---|
| Quando usar / não usar | este formulário é o correto? |
| Antes de preencher | que contexto e autorização preciso obter? |
| Guia de campos | o que escrever, por que importa e um exemplo |
| Prompt pronto para colar | qual texto vai ao chat? |
| Contrato de saída | como reconheço uma resposta completa? |
| QA | o que conferir antes de aceitar? |
| Limites | o que o Genie Code não deve inferir ou executar? |

Cada pasta também tem `exemplo_<nome>.py`. O notebook:

1. prepara dado sintético ou localiza o recurso;
2. mostra o prompt preenchido;
3. reserva um bloco para colar a resposta **real** do Genie Code.

O notebook não “executa o prompt”. A terceira parte exige uma pessoa no chat e
deve registrar data, skill carregada e lacunas observadas.

## Como preencher sem inventar

| Campo | Preenchimento útil | Evita |
|---|---|---|
| recurso | `@recurso` ou `catalog.schema.table` confirmado | analisar objeto errado |
| grão | o que uma linha representa | contagem ou join incoerente |
| chave | coluna ou conjunto que identifica o grão | duplicidade silenciosa |
| tempo | instante de decisão e disponibilidade do dado | leakage |
| target/métrica | evento, classe positiva, unidade, direção e horizonte | otimizar medida errada |
| restrições | PII, custo, prazo, ACL e o que não pode mudar | ação indevida |
| modo | explicar, planejar, gerar código, executar ou publicar | confundir proposta com ação |
| saída | artefatos, ordem, evidência e critério de aceitação | resposta plausível mas incompleta |

Use:

- `NÃO INFORMADO` quando a informação está ausente e precisa virar pendência;
- `NÃO APLICÁVEL` quando o campo foi avaliado e não pertence ao caso;
- um valor concreto quando existe evidência.

Não deixe placeholder por descuido. Uma lacuna não marcada pode levar o
assistente a inferir uma premissa que o usuário nunca aprovou.

## Exemplo do início ao fim

Trecho original de `eda_rapida/eda_rapida.md`:

```text
CONTEXTO
- Tabela/DataFrame: {{TABELA_OU_DF}}
- Objetivo de negócio: {{OBJETIVO}}
- Foco: {{FOCO}}
- Chave esperada: {{PK_OU_NAO_INFORMADO}}
- Coluna temporal: {{COL_DATA_OU_NAO_INFORMADO}}
- Limite de execução: {{TEMPO_CUSTO_OU_NAO_INFORMADO}}
```

O mesmo trecho preenchido:

```text
CONTEXTO
- Tabela/DataFrame: @catalogo.crm.clientes_pf
- Objetivo de negócio: avaliar prontidão para um modelo de propensão
- Foco: renda, ocupação e duplicidade por cliente
- Chave esperada: id_cliente
- Coluna temporal: dt_referencia
- Limite de execução: leitura leve; sem varredura completa

MODO
- Primeiro produza plano e pressupostos.
- Não execute nem escreva até aprovação explícita.

SAÍDA
- dimensão, evidência, severidade e ação;
- pendências e limites da conclusão.
```

Depois de anexar a tabela, a resposta deve ser avaliada contra o contrato do
formulário. Se o plano, as premissas ou os limites estiverem ausentes, peça a
correção citando a seção faltante; não aceite apenas porque o texto parece
convincente.

## Catálogo

| Objetivo | Prompt | Skill sugerida |
|---|---|---|
| EDA completa | [`eda_completa`](eda_completa/eda_completa.md) | `@hub-ml-eda-profissional` |
| perfil rápido | [`eda_rapida`](eda_rapida/eda_rapida.md) | `@hub-ml-eda-profissional` |
| qualidade de dados | [`data_quality`](data_quality/data_quality.md) | `@hub-ml-eda-profissional` |
| consolidar EDAs | [`cross_eda`](cross_eda/cross_eda.md) | `@hub-ml-cross-eda-ml` |
| engenharia de features | [`feature_engineering`](feature_engineering/feature_engineering.md) | `@hub-ml-feature-engineering` |
| validação estatística | [`stat_check`](stat_check/stat_check.md) | `@hub-ml-validacao-estatistica` |
| baseline de ML | [`baseline_orchestration`](baseline_orchestration/baseline_orchestration.md) | `@hub-ml-baseline-ml` |
| explicabilidade | [`explainability`](explainability/explainability.md) | `@hub-ml-explainability` |
| monitoramento | [`monitoramento_modelo`](monitoramento_modelo/monitoramento_modelo.md) | `@hub-ml-monitoramento-modelo` |
| pipeline | [`pipeline`](pipeline/pipeline.md) | `@hub-ml-pipeline-builder` |
| safra/vintage | [`safra`](safra/safra.md) | `@hub-ml-analise-safra` |
| auditar saída de skill | [`auditoria_skills`](auditoria_skills/auditoria_skills.md) | `@hub-ml-auditoria-skills` |
| documentar notebook | [`comentar_notebook`](comentar_notebook/comentar_notebook.md) | `@hub-ml-comentar-notebook` |
| explicação/tutoria | [`tutor_explicar`](tutor_explicar/tutor_explicar.md) | `@hub-ml-tutor-databricks` |
| comparar tabelas | [`comparar_tabelas`](comparar_tabelas/comparar_tabelas.md) | depende do objetivo |
| iniciar projeto | [`novo_projeto`](novo_projeto/novo_projeto.md) | depende do projeto |

## Estado de validação

- A estrutura e o contrato humano das 16 famílias são validados
  automaticamente no repositório canônico.
- Campos sem guia, motivo ou exemplo reprovam o gate local.
- Resposta real continua sendo teste conversacional: precisa ser capturada no
  Genie Code e não deve ser simulada na documentação.

## Limites e segurança

- Um prompt não concede acesso: o recurso precisa estar anexado e autorizado.
- “Gerar código” não significa “executar”; “executar” não significa “publicar”.
- Nunca cole PII, token ou segredo no briefing.
- Para dado temporal, declare instante de decisão e atraso de disponibilidade.
- Para volume alto, imponha amostra, limite de linhas ou orçamento de execução.
- Use chat novo quando o tema mudar materialmente, para reduzir interferência de
  decisões anteriores.

## Onde continuar

- [Guia do ecossistema](../README.md)
- [Agent Skills do Hub](../skills/README.md)
- [Template para novo prompt](../hub_padroes/prompt/template.md)
- [Dicas oficiais de prompting](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
