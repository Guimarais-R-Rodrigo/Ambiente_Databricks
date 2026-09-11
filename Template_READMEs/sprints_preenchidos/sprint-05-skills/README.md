![CRM — Missão Modelos Analíticos CRM](../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Agent Skills

> O conjunto metodológico do ecossistema no Databricks Genie Code: diretrizes de engenharia, guardrails e fluxos analíticos passo a passo para orientar trabalhos de Machine Learning.

> **MECANISMO NATIVO, CONTEÚDO CUSTOMIZADO.** Agent Skills são um recurso oficial da Genie Code e seguem o padrão aberto Agent Skills. Os nomes `hub-ml-*`, as metodologias, os templates e os helpers descritos aqui foram criados neste projeto.

> **Rascunho de sprint 5 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/skills/README.md`.

O título evita a metáfora de “cérebro”: a skill não pensa nem executa sozinha. Ela é um POP para a Genie Code.

---

## 🧭 Neste Guia

**Instrução geral** vale em várias conversas. **Skill** especializa um método. **Template** da skill é gabarito de saída. **Helper** é código Python.

| Para entender... | Vá para... |
|---|---|
| o que uma Agent Skill faz | [O que são Agent Skills](#-o-que-são-agent-skills) |
| seleção por relevância ou `@` | [Como as Skills são utilizadas](#-como-o-genie-code-e-o-usuário-utilizam-as-skills) |
| relação com código | [Skills, Snippets e Scripts](#-relação-entre-skills-hub-snippets-e-hub-scripts) |
| as skills disponíveis | [Catálogo](#️-catálogo-de-agent-skills) |
| o propósito de cada skill | [Detalhamento](#-detalhamento-das-skills) |
| permissões e aprovação | [Aprovações e Revisão](#-aprovações-permissões-e-revisão) |

**Primeira utilização:** o que é skill → `@` → caso de EDA → catálogo quando for escolher outra fase.

---

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

## 🤖 Como o Genie Code e o Usuário utilizam as Skills

![Fluxo de descoberta e seleção de uma Agent Skill](../hub_readmes_visual_assets/readmes/skills/png/01_descoberta_e_selecao.png)

*Leitura da figura: há duas vias. A contínua é relevância (`description` × pedido). A explícita é `@nome`. Nenhuma das duas executa Spark.*

### 1. Pelo lado do Genie Code (Seleção por Relevância)

O frontmatter YAML exige `name` e `description`. A plataforma usa a descrição para decidir se carrega a skill. Recursos em `templates/` entram quando referenciados — não presuma que a pasta inteira cabe no contexto. Teste a seleção; não a trate como certeza.

**Na campanha.** Um pedido “faça EDA desta tabela” *pode* carregar `hub-ml-eda-profissional`. Um pedido de “crie a pasta do helper” não deveria.

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

## 🔗 Relação entre Skills, Hub Snippets e Hub Scripts

A skill organiza o método. Snippets e scripts são implementações. Executar é o notebook.

![Relação entre Agent Skill, helpers e runtime](../hub_readmes_visual_assets/readmes/skills/png/02_skill_helpers_runtime.png)

*Leitura da figura: a skill recomenda; o notebook importa. Três etapas, não um clique.*

### Caso de Uso Genérico

**Sem método.** “Calcule estabilidade da campanha” deixa referência, período, variáveis e bins implícitos.

**Com a skill.** `@hub-ml-monitoramento-modelo` pede esses campos e pode citar `psi_calculator` ou `drift_detector`.

**No runtime.** Você ainda faz:

```python
from hub_snippets.spark.psi_calculator import calcular_psi
```

Ilustração de resposta da Genie (“vou usar PSI com 20 bins”) **não** é execução certificada.

---

## 📋 O que são os Templates das Skills?

Gabaritos de especificação e entrega (`templates/` dentro da pasta da skill). Não são executáveis. Só influenciam quando a skill os referencia. Exemplos: `estilo_visual_eda.md`, `checklist-objeto-novo.md`, `notebook_output_stat.md`.

---

## 🏛️ Arquitetura de Skills no Hub

```text
.assistant/skills/hub-ml-feature-engineering/
├── SKILL.md
└── templates/
```

![Três camadas de uma Agent Skill](../hub_readmes_visual_assets/readmes/skills/png/03_anatomia_skill.png)

*Leitura da figura: frontmatter sustenta descoberta; o corpo é o método; templates aprofundam sob demanda.*

### Requisitos oficiais e seções estruturais do Hub

Oficial: `name` + `description` válidos. Convenção do Hub (auditada aqui, não exigida pelo padrão aberto): quando se aplica, fluxo, helpers, guardrails, formato de saída.

### Onde as skills podem ficar

- Usuário: `/Users/<username>/.assistant/skills/`
- Workspace: `Workspace/.assistant/skills/` (escopo e ACL administrativos)

---

## 🗺️ Catálogo de Agent Skills

A etapa organiza o ponto de entrada; você pode combinar skills em fases, com objetivo explícito.

### Exploração e diagnóstico

| Skill | Objetivo |
|---|---|
| `hub-ml-eda-profissional` | EDA com qualidade e síntese |
| `hub-ml-cross-eda-ml` | cruzamento e prontidão para ML |
| `hub-ml-validacao-estatistica` | testes, efeito, incerteza |

### Engenharia e risco

| Skill | Objetivo |
|---|---|
| `hub-ml-feature-engineering` | features com instante de decisão |
| `hub-ml-analise-safra` | safras, denominador, MOB |

### Modelagem e explicabilidade

| Skill | Objetivo |
|---|---|
| `hub-ml-baseline-ml` | baseline por tipo de problema |
| `hub-ml-explainability` | interpretação com limites |

### MLOps e produção

| Skill | Objetivo |
|---|---|
| `hub-ml-monitoramento-modelo` | drift, performance, decisão de retreino (humana) |
| `hub-ml-pipeline-builder` | Lakeflow, qualidade, automação |

### Governança e engenharia

| Skill | Objetivo |
|---|---|
| `hub-ml-comentar-notebook` | narrativa pré/pós código |
| `hub-ml-tutor-databricks` | explicação didática |
| `hub-ml-auditoria-skills` | audita skill ou output |
| `hub-ml-criar-objeto` | cria objeto no padrão Hub |

---

## 📖 Detalhamento das Skills

Ficha mínima: demanda, quando escolher / não escolher, o que fornecer, pedido-exemplo, helpers, como revisar.

### `hub-ml-eda-profissional`

**Demanda.** Entender uma base nova da campanha.  
**Não escolher** se o problema já é join entre várias fontes (`cross-eda`) ou teste de hipótese (`validacao-estatistica`).  
**Fornecer.** Recurso, grão, chave candidata, tempo, filtros, limite de custo.  
**Pedido.** Ver seção `@` acima.  
**Helpers.** `quick_profile`, `data_quality_check`, `null_summary`, `smart_sample`, `safe_display`, displays e `format_br`.  
**Revisar.** Números com origem; nenhuma regra inventada; amostras limitadas.

### `hub-ml-cross-eda-ml`

Cruzar cadastro e eventos. Helper central: `diagnosticar_join` em **`hub_snippets.spark`**, não em scripts. Também `pit_join`, `psi_calculator`.

### `hub-ml-validacao-estatistica`

A/B ou diferença de taxa: teste, pressuposto, efeito, incerteza. Não substitui desenho amostral.

### `hub-ml-feature-engineering`

Janelas 30/60/90 só com dados ≤ data de decisão. Helpers: `pit_join`, `date_features`, `lgbm_temporal`, `split_temporal`, `woe_iv_calculator`, `rfv_calculator`.

### `hub-ml-analise-safra`

Evento, denominador, coorte, MOB, censura **antes** da curva. `vintage_analysis`.

### `hub-ml-baseline-ml`

População, split, métrica, tracking. Helpers de split, métricas, `mlflow_run` e treinadores. MLflow no Free pode estar bloqueado.

### `hub-ml-explainability`

SHAP/permutação conforme modelo. Contribuição ≠ causalidade.

### `hub-ml-monitoramento-modelo`

Referência vs atual, limiares, decisão humana de retreinar. Não agenda job.

### `hub-ml-pipeline-builder`

Notebook → contrato por camada. Nomenclatura: Lakeflow Spark Declarative Pipelines, Lakeflow Jobs, Declarative Automation Bundles.

### `hub-ml-comentar-notebook`

Markdown antes e depois do código, sem mudar lógica em silêncio.

### `hub-ml-tutor-databricks`

Explica plano Spark, erro, conceito. Analogia não substitui o comportamento real.

### `hub-ml-auditoria-skills`

Dois modos: auditar a skill ou o output. Rubrica nos templates.

### `hub-ml-criar-objeto`

Formato de snippet/script/prompt/README/notebook/skill. Não escreve arquivo até você aprovar. Não altera lógica de domínio.

---

## ❓ Perguntas Frequentes (FAQ)

### 1. Como a skill sabe quais colunas usar?

Ela não “sabe”. Declare ou marque `NÃO INFORMADO`. Inspecionar schema ≠ inventar regra.

### 2. E se eu não puser `@`?

Pode haver seleção por relevância. Para método específico, use `@`.

### 3. Posso combinar skills?

Sim, em fases. Chat novo quando objetivo ou dados mudarem materialmente.

### 4. A saída precisou de adaptação?

Declare a regra e peça alteração. Confira grão, tempo e aceite.

### 5. Podemos editar uma skill?

Sim. Atualize `SKILL.md`, valide frontmatter, rode P/N/`@`. Chat novo.

### 6. A skill executa os helpers?

Não.

---

## 🔐 Aprovações, Permissões e Revisão

- Skill não amplia Unity Catalog.
- Planejar ≠ gerar ≠ executar ≠ persistir.
- Autoaprovação ≠ segurança.
- Revise `CREATE`/`ALTER`/`DROP`/`DELETE`/`MERGE`, instalação, leitura ampla.
- Sem tokens nem dado desnecessário em skill, template ou prompt.

---

## 🔗 Continue Explorando

- [Skills oficiais](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Hub Prompts](../hub_prompts/README.md)
- [Hub Snippets](../hub_snippets/README.md)
- [Hub Scripts](../hub_scripts/README.md)
- [Catálogo](../CATALOGO_HELPERS.md)
