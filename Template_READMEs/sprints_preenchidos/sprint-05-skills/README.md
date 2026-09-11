![CRM — Missão Modelos Analíticos CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

<a id="agent-skills"></a>

# Agent Skills

> O conjunto metodológico do ecossistema no Databricks Genie Code: diretrizes de engenharia, guardrails e fluxos analíticos passo a passo para orientar trabalhos de Machine Learning.

> **MECANISMO NATIVO, CONTEÚDO CUSTOMIZADO.** Agent Skills são um recurso oficial da Genie Code e seguem o padrão aberto Agent Skills. Os nomes `hub-ml-*`, as metodologias, os templates e os helpers descritos aqui foram criados neste projeto.

> **Rascunho de sprint 5 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/skills/README.md`.


---

<a id="neste-guia"></a>

## 🧭 Neste Guia

**Instrução geral** vale em várias conversas. **Skill** especializa um método. **Template** da skill é gabarito de saída. **Helper** é código Python.

| Para entender... | Vá para... |
|---|---|
| o que uma Agent Skill faz | [O que são Agent Skills](#o-que-são-agent-skills) |
| seleção por relevância ou `@` | [Como as Skills são utilizadas](#como-o-genie-code-e-o-usuário-utilizam-as-skills) |
| relação com código | [Skills, Snippets e Scripts](#relação-entre-skills-hub-snippets-e-hub-scripts) |
| as skills disponíveis | [Catálogo](#catálogo-de-agent-skills) |
| o propósito de cada skill | [Detalhamento](#detalhamento-das-skills) |
| permissões e aprovação | [Aprovações e Revisão](#aprovações-permissões-e-revisão) |

**Primeira utilização:** o que é skill → `@` → caso de EDA → catálogo quando for escolher outra fase.

---

<a id="o-que-são-agent-skills"></a>

## 🧠 O que são Agent Skills?

Imagine entregar a um colega competente um procedimento: por onde começar, o que perguntar, o que não fazer, quais recursos usar, como entregar.

**Uma Agent Skill é esse POP em `SKILL.md` para a Genie Code.** Não é módulo Python.

A skill ensina a:

1. Decompor o problema e declarar premissas.
2. Respeitar guardrails (leakage, `collect` indiscriminado, conclusão sem contexto).
3. Recomendar helpers **sem presumir** que foram importados.
4. Entregar em formato revisável.

Guardrail textual reduz risco; não é barreira absoluta. Permissão, aprovação e teste continuam valendo.

**Demanda genérica:** “analise a campanha.”  
**Demanda contextualizada:** tabela, `event_id`, período, somente leitura, plano primeiro. A skill ajuda no segundo caso; não garante resposta idêntica em todo chat.

---

<a id="como-o-genie-code-e-o-usuário-utilizam-as-skills"></a>

## 🤖 Como o Genie Code e o Usuário utilizam as Skills

![Fluxo de descoberta e seleção de uma Agent Skill](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/skills/png/01_descoberta_e_selecao.png)

*Leitura da figura: há duas vias. A contínua é relevância (`description` × pedido). A explícita é `@nome`. Nenhuma das duas executa Spark.*

<a id="1-pelo-lado-do-genie-code-seleção-por-relevância"></a>

### 1. Pelo lado do Genie Code (Seleção por Relevância)

O frontmatter YAML exige `name` e `description`. A plataforma usa a descrição para decidir se carrega a skill. Recursos em `templates/` entram quando referenciados — não presuma que a pasta inteira cabe no contexto. Teste a seleção; não a trate como certeza.

**Na campanha.** Um pedido “faça EDA desta tabela” *pode* carregar `hub-ml-eda-profissional`. Um pedido de “crie a pasta do helper” não deveria.

<a id="2-pelo-lado-do-usuário-ativação-explícita-com"></a>

### 2. Pelo lado do Usuário (Ativação Explícita com `@`)

```text
@hub-ml-eda-profissional

Quero EDA da tabela anexada catalogo.analytics.customer_events.
Grão: um evento por linha. Chave candidata: event_id.
Temporal: event_timestamp. Período: 2026-01-01 a 2026-06-30.
Somente leitura. Plano antes de consulta ampla. Não invente regra de negócio.
```

`@` reduz ambiguidade; não torna o resultado determinístico. Depois de editar a skill publicada, use **chat novo**; se a versão antiga persistir, atualize a página.

---

<a id="relação-entre-skills-hub-snippets-e-hub-scripts"></a>

## 🔗 Relação entre Skills, Hub Snippets e Hub Scripts

A skill organiza o método. Snippets e scripts são implementações. A execução acontece no runtime; o agente pode operá-lo por ferramentas, conforme contexto e aprovação.

![Relação entre Agent Skill, helpers e runtime](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/skills/png/02_skill_helpers_runtime.png)

*Leitura da figura: a skill recomenda; o notebook importa. A rota ilustrada separa contexto e runtime; ela não exclui ações autorizadas do agente.*

<a id="caso-de-uso-genérico"></a>

### Caso de Uso Genérico

Na campanha, comece pela EDA da fixture. Primeiro selecione a preparação, depois envie o pedido completo da ficha de EDA. Revise o plano antes de permitir chamadas; após executar, confronte o resultado com os 20 eventos e o nulo conhecido. Essa comparação comprova um comportamento do código, não o carregamento da skill.

Uma possível resposta **hipotética** seria: “Vou verificar a chave id_cliente”. Você corrige: “id_cliente identifica a entidade e se repete; use event_id como chave candidata e explique a diferença”. A resposta ajustada deve medir a chave correta e preservar a repetição legítima de clientes. Somente uma conversa realmente realizada e registrada poderá ser chamada de evidência observada.

Ao passar para features, faça handoff: informe o schema verificado, grão, nulos, data de decisão e o que permanece desconhecido. Troque o objetivo e use `@hub-ml-feature-engineering`. Não peça que a nova fase reutilize indiscriminadamente todas as suposições do chat anterior.

**Duas avaliações independentes:** registre na interface ou nos passos das ferramentas a skill efetivamente carregada; depois avalie o conteúdo da resposta contra seu contrato. Faça teste positivo (pedido de EDA), negativo (pedido de criar objeto) e explícito (`@hub-ml-eda-profissional`) em conversas novas. Uma seleção automática não é garantida; a ausência da evidência de carregamento deve ser registrada como não verificada.

---

<a id="o-que-são-os-templates-das-skills"></a>

## 📋 O que são os Templates das Skills?

Gabaritos de especificação e entrega (`templates/` dentro da pasta da skill). Não são executáveis. Só influenciam quando a skill os referencia. Exemplos: `estilo_visual_eda.md`, `checklist-objeto-novo.md`, `notebook_output_stat.md`.

---

<a id="arquitetura-de-skills-no-hub"></a>

## 🏛️ Arquitetura de Skills no Hub

```text
.assistant/skills/hub-ml-feature-engineering/
├── SKILL.md
└── templates/
```

![Três camadas de uma Agent Skill](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/skills/png/03_anatomia_skill.png)

*Leitura da figura: frontmatter sustenta descoberta; o corpo é o método; templates aprofundam sob demanda.*

<a id="requisitos-oficiais-e-seções-estruturais-do-hub"></a>

### Requisitos oficiais e seções estruturais do Hub

Oficial: `name` + `description` válidos. Convenção do Hub (auditada aqui, não exigida pelo padrão aberto): quando se aplica, fluxo, helpers, guardrails, formato de saída.

<a id="onde-as-skills-podem-ficar"></a>

### Onde as skills podem ficar

- Usuário: `/Users/<username>/.assistant/skills/` (caminho de objeto no workspace; ao acessar arquivos pelo Python, a forma usada neste Hub começa com `/Workspace/Users/`)
- Workspace: `Workspace/.assistant/skills/` (escopo e ACL administrativos)

---

<a id="catálogo-de-agent-skills"></a>

## 🗺️ Catálogo de Agent Skills

A etapa organiza o ponto de entrada; você pode combinar skills em fases, com objetivo explícito.

<a id="exploração-diagnóstico"></a>

### 🔍 Exploração & Diagnóstico

| Skill | Objetivo |
|---|---|
| `hub-ml-eda-profissional` | EDA com qualidade e síntese |
| `hub-ml-cross-eda-ml` | cruzamento e prontidão para ML |
| `hub-ml-validacao-estatistica` | testes, efeito, incerteza |

<a id="engenharia-de-dados-risco"></a>

### 🧱 Engenharia de Dados & Risco

| Skill | Objetivo |
|---|---|
| `hub-ml-feature-engineering` | features com instante de decisão |
| `hub-ml-analise-safra` | safras, denominador, MOB |

<a id="modelagem-explicabilidade"></a>

### 📈 Modelagem & Explicabilidade

| Skill | Objetivo |
|---|---|
| `hub-ml-baseline-ml` | baseline por tipo de problema |
| `hub-ml-explainability` | interpretação com limites |

<a id="mlops-produção"></a>

### ⚙️ MLOps & Produção

| Skill | Objetivo |
|---|---|
| `hub-ml-monitoramento-modelo` | drift, performance, decisão de retreino (humana) |
| `hub-ml-pipeline-builder` | Lakeflow, qualidade, automação |

<a id="governança-engenharia"></a>

### 🛡️ Governança & Engenharia

| Skill | Objetivo |
|---|---|
| `hub-ml-comentar-notebook` | narrativa pré/pós código |
| `hub-ml-tutor-databricks` | explicação didática |
| `hub-ml-auditoria-skills` | audita skill ou output |
| `hub-ml-criar-objeto` | cria objeto no padrão Hub |

---

<a id="detalhamento-das-skills"></a>

## 📖 Detalhamento das Skills

As fichas abaixo são pedidos completos de **planejamento**. Selecionar uma célula, arquivo ou modelo na interface é uma ação real: o texto do pedido não a substitui. Quando não houver um recurso, a ficha declara a ausência em vez de fingir uma análise executada. A fixture da campanha é criada no [tutorial de uso](../sprint-02-assistant/README.md#exemplo-conhecer-uma-tabela-nova); selecione essa preparação e seu schema antes de pedir execução sobre a view.

<a id="hub-ml-eda-profissional-exploração-completa-e-visual"></a>

### `hub-ml-eda-profissional` — Exploração Completa e Visual

**Quando escolher e conceito.** Você recebeu uma única base de eventos e ainda não sabe se uma linha representa um envio ou um cliente. EDA é exploração descritiva: organiza qualidade, distribuições e relações antes da modelagem. Use esta skill para a base já consolidada; escolha cross-EDA quando o problema principal envolver cruzar fontes.

**O que fornecer.** Forneça a célula/notebook selecionado que cria a fixture de 20 eventos, seu schema, grão, chave candidata, período e limites de leitura. Na fixture, a entidade se repete legitimamente; a chave candidata é `event_id`, não `id_cliente`.

**Pedido completo — no chat:**

```text
@hub-ml-eda-profissional

Analise a fixture sintética da célula selecionada neste notebook, que cria
vw_campanha_eventos_sintetica na mesma SparkSession. Schema: event_id,
id_cliente, dt_evento, canal, respondeu, valor_gasto. Grão: um evento por linha.
Chave candidata: event_id. Período: 01/06/2026 a 20/06/2026.
Objetivo: verificar a base antes de medir resposta da campanha.
Modo: somente plano neste turno; não execute código nem persista dados.
Proponha consultas de schema, volume, chave e nulos, identificando custo.
Não declare que a view foi anexada como tabela do catálogo.
Critério de aceite: separar fatos a medir de hipóteses; nenhum número sem origem.
```

**Método e entregáveis.** Espere contrato inicial, sequência de inspeção, agregados interpretáveis e recomendações relacionadas ao objetivo. `quick_profile`, `data_quality_check`, `null_summary` e `smart_sample` podem apoiar a implementação. Uma recomendação de helper não prova que houve import ou execução.

**Como revisar.** Após autorizar a execução no notebook, o oráculo da fixture é 20 eventos, 5 clientes, zero duplicatas de event_id e 1/20 de nulos em canal. Confira denominadores e limites da coleta. A ausência de duplicatas não define sozinha o grão de negócio.

**Limites e recuperação.** Não aceite uma conclusão causal sobre efeito da campanha, nem use a aparência do relatório como evidência de carregamento da skill. Para uma hipótese formal sobre resposta, encaminhe à validação estatística.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/templates/roteiro_eda.md).

<a id="hub-ml-cross-eda-ml-cruzamento-de-bases-e-prontidão-para-ml"></a>

### `hub-ml-cross-eda-ml` — Cruzamento de Bases e Prontidão para ML

**Quando escolher e conceito.** Um join pode multiplicar eventos se o cadastro tiver mais de uma linha por cliente. Cobertura é a parcela com correspondência; cardinalidade descreve a relação um-para-um, um-para-muitos ou muitos-para-muitos. Use antes de materializar o cruzamento, não como substituto de EDA de uma única fonte.

**O que fornecer.** Selecione os schemas e as células das duas fontes. Declare a tabela âncora, chaves em cada lado, granularidade esperada, tempo de vigência e o que significa ausência de correspondência. A dimensão didática pode ser criada com cinco clientes únicos a partir da fixture; o exemplo completo está no guia de uso.

**Pedido completo — no chat:**

```text
@hub-ml-cross-eda-ml

Quero avaliar um left join, ainda sem executá-lo. A célula selecionada tem
20 eventos sintéticos e uma dimensão de 5 clientes únicos. Âncora: eventos.
Chave nos dois lados: id_cliente. Grão de saída esperado: um event_id por linha.
Período dos eventos: junho/2026. Vigência histórica do cadastro: NÃO INFORMADO.
Modo: plano somente; não gravar e não presumir que o cadastro atual existia no passado.
Entregue contagens a conferir, duplicidade, cobertura, expansão esperada e
perguntas sobre disponibilidade temporal. Use diagnosticar_join quando adequado.
```

**Método e entregáveis.** Espere inventário das fontes, diagnóstico de chaves, cobertura e expansão, matriz de viabilidade e handoff para features. O helper real é `hub_snippets.spark.join_diagnostics.diagnosticar_join`. `pit_join` é pertinente somente quando o contrato temporal estiver definido.

**Como revisar.** Confira se a expansão foi calculada em relação à âncora, se chaves nulas receberam tratamento explícito e se um cadastro com chaves duplicadas foi identificado antes de juntar. No caso cinco clientes únicos, a relação pretendida é muitos eventos para um cliente.

**Limites e recuperação.** Boa cobertura não prova sinal incremental nem prontidão integral para ML. Falta de vigência é pendência a resolver, não autorização para usar o estado atual como histórico.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/templates/join_feasibility.md).

<a id="hub-ml-validacao-estatistica-rigor-matemático-e-testes-de-hipóteses"></a>

### `hub-ml-validacao-estatistica` — Rigor Matemático e Testes de Hipóteses

**Quando escolher e conceito.** Uma diferença entre taxas observadas pode resultar de acaso ou de composição dos grupos. A skill organiza hipótese, desenho, pressupostos, tamanho do efeito e incerteza; não se resume a pedir um p-valor. Use para inferência; para apenas descrever a distribuição, use EDA.

**O que fornecer.** Informe a unidade experimental, alocação, eventos repetidos por cliente, janela de observação, hipótese, métrica primária e critérios decididos antes de olhar resultados. A fixture de eventos tem clientes repetidos; não estabelece randomização nem independência.

**Pedido completo — no chat:**

```text
@hub-ml-validacao-estatistica

Planeje uma comparação de taxa de resposta entre dois tratamentos.
Tenho apenas a fixture sintética event_id/id_cliente/respondeu; tratamento,
randomização e janela de acompanhamento: NÃO INFORMADO.
Unidade potencial: cliente; eventos do mesmo cliente podem depender entre si.
Modo: explicar e planejar, sem executar testes neste turno.
Liste os dados adicionais necessários, a hipótese, unidade de análise, efeito,
intervalo de confiança e tratamento de múltiplas comparações. Não invente p-valor.
```

**Método e entregáveis.** Espere plano de teste, diagnóstico de pressupostos, definição da estimativa e uma proposta de inferência compatível com a unidade. O template `test_plan.md` organiza decisões; não executa um teste nem substitui o desenho do estudo.

**Como revisar.** Uma resposta adequada recusa inferir efeito causal com a fixture incompleta, identifica dependência por cliente e separa significância estatística de relevância prática. Após dados adequados, revise denominador, intervalo, direção e limites.

**Limites e recuperação.** Não usar o mesmo conjunto para escolher hipóteses e apresentar inferência confirmatória sem ressalva. Caso o objetivo seja monitoramento recorrente de drift, a skill de monitoramento pode ser a entrada correta.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-validacao-estatistica/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-validacao-estatistica/templates/test_plan.md).

<a id="hub-ml-feature-engineering-engenharia-de-atributos-sem-leakage"></a>

### `hub-ml-feature-engineering` — Engenharia de Atributos sem Leakage

**Quando escolher e conceito.** Uma feature só pode usar informação disponível no instante da decisão. Tempo do evento e tempo de publicação podem diferir. Esta skill transforma uma necessidade em especificação de atributos; não é a etapa de avaliar a viabilidade de fontes ainda desconhecidas.

**O que fornecer.** Declare entidade, evento que dispara a previsão, horário de decisão, target e horizonte, atraso de publicação, regras de nulos e fontes autorizadas. A fixture serve ao raciocínio, mas não define um target de retenção real.

**Pedido completo — no chat:**

```text
@hub-ml-feature-engineering

Desenhe features para eventos da campanha sintética com id_cliente e dt_evento.
Decisão didática: início do dia de cada evento. Quero contagem de eventos e
soma de valor_gasto nos 30 dias anteriores, excluindo o evento da decisão.
Target e atraso de publicação reais: NÃO INFORMADO; não materialize nada.
Modo: plano e especificação apenas. Explique cada janela, nulidade, dados tardios,
contrato de entrada/saída e um teste com evento futuro que deve ficar de fora.
Não use respondeu do próprio evento como preditor.
```

**Método e entregáveis.** Espere backlog priorizado, especificações de grão, disponibilidade e janela, plano de implementação e testes de tempo. Helpers possíveis: `pit_join`, `extrair_features_data`, `create_temporal_features`, `rfv_calculator` e `temporal_split`, conforme os tipos de entrada.

**Como revisar.** Revise se o atraso foi tratado como requisito desconhecido, se o evento-alvo foi excluído e se treino/inferência calculam a mesma definição. A saída deve explicar a diferença entre janela de eventos e disponibilidade operacional.

**Limites e recuperação.** Uma junção por data sem considerar disponibilidade não garante ausência de leakage. Não autorize criação de feature table enquanto nome, schema, permissões e semântica estiverem pendentes.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/templates/feature_spec_core.md).

<a id="hub-ml-analise-safra-maturação-e-curvas-de-crédito-vintage"></a>

### `hub-ml-analise-safra` — Maturação e Curvas de Crédito (Vintage)

**Quando escolher e conceito.** Comparar coortes exige medir a mesma idade de acompanhamento. MOB é o número de meses desde a originação; censura ocorre quando ainda não houve tempo para observar um desfecho. Uma safra recente não deve parecer melhor apenas porque está menos madura.

**O que fornecer.** Este é um cenário adicional, não colunas ocultas da campanha. Forneça painel contrato × referência com identificador, data de originação, referência, evento e população elegível. Declare se o target é incidente ou acumulado e qual denominador se usa.

**Pedido completo — no chat:**

```text
@hub-ml-analise-safra

Planeje uma análise de safras; ainda não forneci o painel.
Schema necessário proposto: contrato_id, dt_originacao, dt_referencia, evento.
Grão pretendido: contrato × mês observado. Definição do evento, denominador e
censura: NÃO INFORMADO. Modo: plano somente, sem números ou queries executadas.
Explique como construir MOB, comparar coortes na mesma maturidade e tratar
contratos sem acompanhamento suficiente. Não some taxas acumuladas.
```

**Método e entregáveis.** Espere contrato temporal, tabela de maturação, curvas e uma interpretação que explicite denominadores. `build_vintage_table` e funções de visualização de `vintage_analysis` são implementações possíveis após preparar o painel.

**Como revisar.** Confira se cada contrato entra uma vez por MOB, se o evento acumulado não é contado novamente como incidente e se meses não observados não foram preenchidos como zero de inadimplência.

**Limites e recuperação.** Uma análise de safra não certifica conformidade regulatória. Datas de originação e observação ausentes impedem calcular maturação; peça os dados em vez de reutilizar dt_evento com outro significado.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-analise-safra/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-analise-safra/templates/relatorio_safra.md).

<a id="hub-ml-baseline-ml-benchmark-inicial-e-rastreabilidade"></a>

### `hub-ml-baseline-ml` — Benchmark Inicial e Rastreabilidade

**Quando escolher e conceito.** Baseline é uma régua reproduzível para comparar abordagens, não o modelo automaticamente promovido. A skill escolhe avaliação adequada ao problema: classificação, regressão, série, ranking, sobrevivência, clustering ou anomalia.

**O que fornecer.** Forneça problema, população, target/horizonte, features disponíveis na decisão, estratégia de split, métrica primária, restrições de compute e política de tracking. A fixture de 20 eventos valida mecanismo; não sustenta estimativa confiável de performance real.

**Pedido completo — no chat:**

```text
@hub-ml-baseline-ml

Planeje um baseline para prever respondeu na campanha sintética.
Grão: evento; entidade: id_cliente; tempo: dt_evento. Somente histórico anterior
à decisão pode virar feature; a lista autorizada ainda será revisada.
Os 20 registros são didáticos, não uma amostra de produção.
Modo: plano; sem treino, instalação, MLflow ou persistência neste turno.
Proponha split temporal, baseline de referência, métricas e limites; indique
os dados adicionais necessários para uma avaliação válida.
```

**Método e entregáveis.** Espere suite justificada, split, baseline simples, comparação e plano de rastreabilidade. Helpers de treino, `calculate_binary_metrics`, `temporal_split` e `run_governado` podem ser usados após autorização. Muitos treinadores têm tracking habilitado por padrão: confira `log_mlflow` antes de executar.

**Como revisar.** Confira que o teste não foi usado para escolher hiperparâmetros e que nenhum resultado de treino foi vendido como avaliação fora da amostra. Métricas precisam informar população, corte e unidade.

**Limites e recuperação.** MLflow é recurso de tracking; falha em uma execução específica exige erro, data, versão e configuração, não uma proibição genérica do Free. Para explicar um modelo já treinado, encaminhe à explicabilidade.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-baseline-ml/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-baseline-ml/templates/split_strategy.md).

<a id="hub-ml-explainability-explicabilidade-de-modelos-e-shap"></a>

### `hub-ml-explainability` — Explicabilidade de Modelos e SHAP

**Quando escolher e conceito.** Explicar uma predição é diferente de provar que uma variável causa o resultado. A skill escolhe método compatível com o modelo e público, articulando interpretação global e local.

**O que fornecer.** Selecione modelo real e versão, matriz com as mesmas features/ordem do treino, transformações, saída/classe de interesse, amostra autorizada, população e público. O exemplo abaixo pede o plano porque ainda não há modelo.

**Pedido completo — no chat:**

```text
@hub-ml-explainability

Quero planejar a explicação de um classificador de resposta da campanha.
Modelo treinado e run: NÃO INFORMADO. Público: analista técnico e gestor.
Saída de interesse: probabilidade de respondeu=1; confirme escala do modelo.
Modo: planejar, sem carregar modelo, ler dados ou registrar MLflow.
Liste artefatos necessários, escolha de método global/local, amostragem e
limitações. Não produza valores SHAP, motivos de score ou causalidade fictícios.
```

**Método e entregáveis.** Espere plano de explicação, requisitos de artefatos, método, interpretação técnica e tradução executiva. `compute_shap`, gráficos correspondentes e `explainability_report` ajudam quando houver modelo e dados compatíveis.

**Como revisar.** Confira que classe/escala estão definidas e que importância não foi apresentada como percentual de poder preditivo ou recomendação causal. Features correlacionadas e transformação dos dados exigem ressalvas.

**Limites e recuperação.** Sem modelo e amostra, uma explicação numérica é inventada. A skill não substitui a validação de viés, privacidade ou aprovação do modelo.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-explainability/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-explainability/templates/shap_analysis_technical.md).

<a id="hub-ml-monitoramento-modelo-mlops-e-detecção-de-degradação"></a>

### `hub-ml-monitoramento-modelo` — MLOps e Detecção de Degradação

**Quando escolher e conceito.** Operar um modelo exige separar qualidade, mudança de distribuição, desempenho com rótulos e resposta operacional. Drift pode aparecer antes dos rótulos; não prova sozinho que o modelo piorou.

**O que fornecer.** Forneça versão do modelo, população, referência e atual, janela, disponibilidade dos rótulos, latência, custos, política de limites e responsável por investigar/retreinar. Na fixture de coortes do guia de scripts, ref/igual/mudou são cenários sintéticos, não produção.

**Pedido completo — no chat:**

```text
@hub-ml-monitoramento-modelo

Desenhe monitoramento da campanha usando a fixture de coortes selecionada.
Referência: ref; comparação: mudou; variável: valor_gasto.
Modelo em produção, rótulos e política de limites: NÃO INFORMADO.
Modo: plano somente; não criar jobs, alertas, tabelas ou runs.
Separe drift de performance e proponha investigação, calibração de limites,
responsável e evidência necessária antes de discutir retreino.
```

**Método e entregáveis.** Espere contrato operacional, relatório de drift, métricas com população/janela, política de investigação e decisão humana. Helpers possíveis: PSI/CSI em Spark, `drift_detector`, `PerformanceMonitor` e métricas supervisionadas quando existirem rótulos.

**Como revisar.** Confira faixas comuns entre coortes, cardinalidade, sazonalidade e atraso dos rótulos. Um índice sem limiares calibrados não deve ganhar rótulo crítico por conveniência.

**Limites e recuperação.** Carregar a skill não agenda monitoramento. O agente pode propor ou executar configuração autorizada, mas criar job/alerta é ação separada que deve ser visível e revisada.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-monitoramento-modelo/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-monitoramento-modelo/templates/drift_report.md).

<a id="hub-ml-pipeline-builder-industrialização-e-lakeflow"></a>

### `hub-ml-pipeline-builder` — Industrialização e Lakeflow

**Quando escolher e conceito.** Pipeline transforma etapas em execução repetível com contratos, dependências e recuperação de falhas. A skill é apropriada quando a entrega é infraestrutura, não somente uma análise pontual.

**O que fornecer.** Informe fontes/destinos, incrementalidade, frequência, chaves, dados atrasados, expectativas de qualidade, identidade de execução, ambientes, orçamento e permissões. A view sintética não define um recurso de produção ou SLA.

**Pedido completo — no chat:**

```text
@hub-ml-pipeline-builder

Planeje a industrialização da checagem de qualidade da campanha.
Lógica: ler eventos, verificar event_id e nulos de canal, registrar evidências.
Tabelas de origem/destino, frequência, SLA e identidade: NÃO INFORMADO.
Modo: desenho somente. Não criar Job, pipeline, bundle ou recurso no workspace.
Compare Lakeflow Jobs e Lakeflow Spark Declarative Pipelines conforme necessidade;
explique idempotência, dados tardios, falha, retry, qualidade e rollback.
```

**Método e entregáveis.** Espere especificação por etapa e camada quando pertinente, dependências, política de qualidade, testes e operação. A nomenclatura vigente inclui Lakeflow Spark Declarative Pipelines, Lakeflow Jobs e Declarative Automation Bundles; não implica usar os três em todo projeto.

**Como revisar.** Confira reprocessamento sem duplicação, persistência e modos de falha. Uma expectation configurada para registrar violações não equivale a bloquear dados. A política deve indicar manter, descartar ou falhar conforme o objetivo.

**Limites e recuperação.** Não transforme a view de tutorial em caminho corporativo imaginário. Um bundle proposto não é um deployment executado; registro de API/execução é evidência separada.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-pipeline-builder/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-pipeline-builder/templates/pipeline_spec.md).

<a id="hub-ml-comentar-notebook-documentação-pré-e-pós-código"></a>

### `hub-ml-comentar-notebook` — Documentação Pré e Pós-Código

**Quando escolher e conceito.** Use quando o artefato já existe e precisa explicar objetivo, entrada, raciocínio e resultado antes/depois do código. Para aprender um conceito sem editar o notebook, use tutor.

**O que fornecer.** Selecione o notebook, delimite células e público, preserve resultados existentes e declare se é permitida apenas proposta ou alteração do arquivo. Resultados ausentes devem permanecer ausentes, não simulados como observados.

**Pedido completo — no chat:**

```text
@hub-ml-comentar-notebook

Proponha Markdown para a célula selecionada de data_quality_check da campanha.
Público: analista que lê Python mas não conhece checks/alerts/score.
Não altere código nem execute a célula; entregue apenas o texto proposto.
Antes: objetivo, fixture de 20 linhas, chave e percentuais dos limiares.
Depois: explique os campos e o resultado esperado de 5% de nulos como cálculo,
não execução observada. Preserve o título e use um único cabeçalho CRM.
```

**Método e entregáveis.** Espere células PRÉ/PÓS com explicação proporcional ao código e resultado claramente rotulado. Templates de blocos Markdown e cabeçalho orientam a estrutura; helpers de formatação podem ser recomendados, sem inserção de dependências desnecessárias.

**Como revisar.** Compare o código antes/depois: nenhum filtro, target ou parâmetro deve mudar silenciosamente. Confira se o texto usa os nomes reais do retorno e não chama valor esperado de resultado observado.

**Limites e recuperação.** Não inventar sucesso de execução para preencher a célula PÓS. Sem output, documente o que verificar e a limitação.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-comentar-notebook/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-comentar-notebook/templates/bloco_markdown_pre_codigo.md).

<a id="hub-ml-tutor-databricks-explicação-didática-com-contexto"></a>

### `hub-ml-tutor-databricks` — Explicação Didática com Contexto

**Quando escolher e conceito.** O objetivo é aprender a interpretar código ou erro. A skill organiza explicação progressiva e analogias, mas deve traduzi-las de volta ao comportamento concreto do runtime.

**O que fornecer.** Selecione o trecho, informe o que você sabe, a dúvida, o erro integral e runtime quando pertinente. Evite credenciais no stack trace. O pedido abaixo usa a chamada de qualidade já apresentada.

**Pedido completo — no chat:**

```text
@hub-ml-tutor-databricks

Explique linha a linha a chamada selecionada de data_quality_check.
Sei ler Python, mas quero entender import, SparkSession, view temporária,
checks, alerts e por que 1/20 produz warn com null_warn=5.
Modo: explicar somente; não executar nem alterar o notebook.
Compare importar o módulo, chamar a função e usar raise no consumidor.
Use uma analogia curta, depois relacione cada parte à API real.
```

**Método e entregáveis.** Espere problema em linguagem comum, leitura do trecho, exemplo mínimo, interpretação e um exercício. Catálogo de helpers e templates de explicação podem apoiar a resposta, mas não substituem leitura do código selecionado.

**Como revisar.** Confira se a analogia distingue contexto do agente, interpretador Python e Spark. Uma explicação correta deve dizer que `fail` no dicionário não lança por si só o `raise` do consumidor.

**Limites e recuperação.** Se falta erro ou versão, a resposta deve separar hipóteses diagnósticas de fatos. Para gravar Markdown no notebook, mude explicitamente para a skill de documentação.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-tutor-databricks/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-tutor-databricks/templates/explicacao_bloco_codigo.md).

<a id="hub-ml-auditoria-skills-auditoria-de-implementação-ou-de-output"></a>

### `hub-ml-auditoria-skills` — Auditoria de Implementação ou de Output

**Quando escolher e conceito.** Uma implementação pode cumprir a forma e falhar na prática; uma resposta bonita pode violar o contrato. Declare se quer auditar a pasta da skill ou uma entrega produzida com ela.

**O que fornecer.** Forneça `SKILL.md`, recursos referenciados, pedido original, versão/commit e output com evidência da execução. Não confunda ausência de acesso com ausência do arquivo.

**Pedido completo — no chat:**

```text
@hub-ml-auditoria-skills

Audite o output de EDA selecionado contra o SKILL.md também selecionado.
Pedido: diagnóstico da fixture de 20 eventos, plano antes de executar,
sem persistência, chave event_id e 5% de nulos em canal.
Modo: leitura e relatório; não corrigir arquivos ainda.
Separe erro confirmado, risco, melhoria e item não verificável. Para cada
achado, informe trecho, contrato violado, impacto e teste de aceitação.
Não declare a skill carregada apenas porque o texto seguiu o método.
```

**Método e entregáveis.** Espere matriz pedido→contrato→evidência, achados priorizados e correções testáveis. A rubrica é instrumento de revisão; pontuação não substitui evidência. Helpers só entram quando a auditoria inclui o comportamento de código efetivamente observado.

**Como revisar.** Confira se cada acusação possui fonte e se a conclusão distingue leitura estática, execução e teste conversacional. Links quebrados precisam ser resolvidos no local correto do documento, especialmente em staging.

**Limites e recuperação.** Não usar auditoria como autorização implícita para editar. Um modo de output exige o output; sem ele, só é possível avaliar o contrato fornecido.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-auditoria-skills/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-auditoria-skills/templates/rubrica_universal.md).

<a id="hub-ml-criar-objeto-criação-no-padrão-do-hub"></a>

### `hub-ml-criar-objeto` — Criação no Padrão do Hub

**Quando escolher e conceito.** Use para criar ou converter um objeto com formato consistente. Não use apenas porque a demanda contém a palavra código; escrever lógica analítica avulsa não é necessariamente criar um objeto do Hub.

**O que fornecer.** Informe tipo, público, nome, finalidade, entrada, retorno, efeito permitido e exemplo. Se há um exemplar, selecione-o junto com o template, em vez de pedir que o agente trabalhe de memória.

**Pedido completo — no chat:**

```text
@hub-ml-criar-objeto

Planeje um snippet didático para taxa de resposta por segmento.
Use o template de snippet e o exemplar taxa_resposta_campanha selecionados.
Entrada: Spark DataFrame com uma linha por contato, segmento e respondeu 0/1.
Saída: DataFrame por segmento com contagens, taxa percentual e intervalo Wilson.
Preserve o contrato do exemplar; não substitua por função escalar.
Modo: plano da pasta e revisão do contrato; não criar arquivos antes de aprovação.
Inclua exemplo de 10 contatos/2 respostas e teste de resposta nula rejeitada.
```

**Método e entregáveis.** Espere árvore proposta, função de cada arquivo, assinatura, notebook que exercita o objeto e checklist. A pasta de exemplo em padrões não deve ser copiada para a descoberta de skills como se fosse uma skill ativa adicional.

**Como revisar.** Confira nome do módulo, reexport em `__init__.py`, import público, schema/escala e chamada real. Para o exemplar, dois em dez correspondem a `taxa_pct=20`, não retorno escalar 0,20.

**Limites e recuperação.** Template é padrão de forma, não certificado estatístico. A confirmação de escrita é parte do procedimento solicitado; não é uma limitação técnica absoluta da Genie Code.

[Contrato da skill](../../../ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md) · [Template específico](../../../ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).

<a id="perguntas-frequentes-faq"></a>

## ❓ Perguntas Frequentes (FAQ)

<a id="1-como-a-skill-sabe-quais-colunas-utilizar"></a>

### 1. Como a skill sabe quais colunas utilizar?

Ela não “sabe”. Declare ou marque `NÃO INFORMADO`. Inspecionar schema ≠ inventar regra.

<a id="2-o-que-acontece-se-eu-não-colocar-antes-do-nome-da-skill"></a>

### 2. O que acontece se eu não colocar `@` antes do nome da skill?

Pode haver seleção por relevância. Para método específico, use `@`.

<a id="3-posso-combinar-duas-ou-mais-skills-na-mesma-conversa"></a>

### 3. Posso combinar duas ou mais skills na mesma conversa?

Sim, em fases. Chat novo quando objetivo ou dados mudarem materialmente.

<a id="4-o-que-fazer-se-a-saída-precisar-de-adaptações-do-meu-projeto"></a>

### 4. O que fazer se a saída precisar de adaptações do meu projeto?

Declare a regra e peça alteração. Confira grão, tempo e aceite.

<a id="5-a-equipe-pode-editar-as-instruções-de-uma-skill-existente"></a>

### 5. A equipe pode editar as instruções de uma skill existente?

Sim. Atualize `SKILL.md`, valide frontmatter, rode P/N/`@`. Chat novo.

<a id="6-a-skill-executa-os-helpers-citados-automaticamente"></a>

### 6. A skill executa os helpers citados automaticamente?

O arquivo é instrução, não processo autônomo. A Genie Code pode interpretar a skill e executar helpers por ferramentas autorizadas. Confira as chamadas e aprovações; selecionar a skill não comprova execução.

---

<a id="aprovações-permissões-e-revisão"></a>

## 🔐 Aprovações, Permissões e Revisão

- Skill não amplia Unity Catalog.
- Planejar ≠ gerar ≠ executar ≠ persistir.
- Autoaprovação ≠ segurança.
- Revise `CREATE`/`ALTER`/`DROP`/`DELETE`/`MERGE`, instalação, leitura ampla.
- Sem tokens nem dado desnecessário em skill, template ou prompt.

---

<a id="continue-explorando"></a>

## 🔗 Continue Explorando

- [Skills oficiais](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Hub Prompts](../sprint-06-prompts/README.md)
- [Hub Snippets](../sprint-03-snippets/README.md)
- [Hub Scripts](../sprint-04-scripts/README.md)
- [Catálogo](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md)
