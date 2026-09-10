# Hub Prompts — Briefings Técnicos Estruturados para Genie Code

O **Hub Prompts** é a camada de interface e especificação técnica do ecossistema. Ele reúne formulários e briefings padronizados para orientar a interação humana com a **Databricks Genie Code**, ajudando a traduzir demandas analíticas em instruções delimitadas, rastreáveis e reproduzíveis.

> **CONTEÚDO CUSTOMIZADO PELO HUB · USO MANUAL.** `hub_prompts` não é uma pasta nativa descoberta ou executada automaticamente pela Genie Code. Você escolhe o template, preenche os campos e fornece o conteúdo no chat junto aos recursos necessários.

Em vez de depender apenas de comandos improvisados, o Hub Prompts estabelece um contrato claro entre quem solicita a análise e o assistente de IA.

---

## 🧭 Neste Guia

| Para entender... | Vá para... |
|---|---|
| por que usar um briefing estruturado | [O que é um Prompt Estruturado](#-o-que-é-um-prompt-estruturado) |
| como um objeto de prompt é organizado | [Anatomia da Pasta](#️-a-anatomia-de-uma-pasta-de-prompt) |
| como preencher sem inventar informações | [Disciplina dos Parâmetros](#-a-disciplina-dos-parâmetros-evitando-alucinações) |
| qual prompt escolher | [Catálogo Detalhado](#-catálogo-detalhado-de-prompts) |
| como conduzir a interação | [Passo a Passo Operacional](#️-passo-a-passo-operacional-do-briefing-ao-resultado) |
| dúvidas e limites | [Perguntas Frequentes](#-perguntas-frequentes-faq) |

---

<a id="-o-que-é-um-prompt-estruturado"></a>

## 🎯 O que é um Prompt Estruturado?

No ecossistema, um prompt estruturado funciona como uma **Ordem de Serviço (OS) ou Especificação Técnica de Requisitos**.

Imagine solicitar a construção de um pipeline para uma equipe de engenharia de dados:

- Se você disser apenas *“faça um pipeline com os dados de vendas”*, ficarão abertos frequência, grão, chaves, volume, destino e critérios de aceite.
- Se você entregar uma **especificação técnica** com fontes, janela temporal, filtros, restrições, entregáveis e validações, a comunicação fica mais precisa e o resultado mais fácil de revisar.

O Hub Prompts aplica essa disciplina ao desenvolvimento assistido por IA:

| Característica | Chat Informal / Ad hoc | Briefing Estruturado (Hub Prompts) |
| :--- | :--- | :--- |
| **Entrada** | Pedido amplo: “analise esta tabela”. | Objetivo, dados, grão, chaves, período e filtros. |
| **Premissas da IA** | Muitas lacunas precisam ser resolvidas durante a conversa. | Desconhecidos e hipóteses são declarados para inspeção ou aprovação. |
| **Controle de Custo** | Escopo de leitura e execução pode ficar implícito. | Limites e modo de trabalho podem ser definidos antes da execução. |
| **Segurança & Dados** | Operações permitidas podem não estar claras. | Guardrails, aprovações e tratamento de dados são explicitados. |
| **Entregável** | Formato varia conforme a interpretação. | Contrato de saída e critérios de aceite ficam no próprio briefing. |

> **Uso assistido:** o briefing melhora a especificação, mas não garante que a resposta ou o código estejam corretos. Você continua responsável por revisar plano, dados utilizados, código, resultados e operações propostas.

---

<a id="️-a-anatomia-de-uma-pasta-de-prompt"></a>

## 🏗️ A Anatomia de uma Pasta de Prompt

Seguindo o padrão de organização **Pasta de Objeto**, cada demanda do Hub Prompts possui uma pasta autossuficiente com dois arquivos centrais:

```text
hub_prompts/
└── eda_rapida/
    ├── eda_rapida.md             <- briefing técnico preenchível
    └── exemplo_eda_rapida.py     <- notebook didático de acompanhamento
```

### 1. O Arquivo Markdown (`<nome>.md`)

É a fonte do briefing. Em geral, contém:

- **Quando usar e quando não usar:** delimita o propósito e as fronteiras.
- **Guia de preenchimento:** explica o significado, o motivo e um exemplo de cada campo.
- **Prompt pronto para preencher:** reúne contexto, modo de trabalho e contrato de saída.
- **O que conferir na resposta:** checklist para revisar se a entrega cumpriu o pedido.

### 2. O Notebook de Acompanhamento (`exemplo_<nome>.py`)

O notebook documenta o ciclo de uso do briefing em três partes:

1. **Parte 1 — Preparo do Ambiente:** cria dados sintéticos controlados ou aponta recursos de teste.
2. **Parte 2 — Prompt Preenchido:** mostra uma instância completa do briefing, sem placeholders pendentes.
3. **Parte 3 — Registro da Resposta Real:** espaço para registrar a resposta obtida, a skill utilizada, evidências, pontos fortes e lacunas.

> **Atenção:** o notebook é uma demonstração e um recipiente de evidência. Enquanto a Parte 3 não contiver uma resposta realmente produzida e revisada, ele não comprova homologação conversacional do prompt.

### 3. Exemplo de briefing completamente preenchido

```text
Quero realizar uma EDA rápida da tabela anexada `catalogo.analytics.customer_events`.

Objetivo:
- decidir se a base está apta para uma análise mensal de retenção;
- identificar bloqueios de qualidade antes de desenhar as métricas.

Contexto dos dados:
- grão esperado: um evento de cliente por linha;
- chave candidata: event_id;
- entidade: customer_id;
- coluna temporal: event_timestamp;
- período: 2026-01-01 a 2026-06-30;
- filtro: event_status = 'valid';
- regras adicionais: NÃO INFORMADO — pergunte antes de assumir.

Modo de trabalho:
- trabalhe somente em leitura;
- apresente primeiro o plano e as consultas pretendidas;
- não colete a tabela inteira no driver;
- limite amostras e explicite o motivo;
- peça aprovação antes de qualquer operação persistente ou de leitura ampla.

Entregue:
1. schema, volume e intervalo temporal observado;
2. avaliação da unicidade da chave e completude das colunas;
3. distribuição das variáveis relevantes;
4. anomalias e limitações, separando fatos de hipóteses;
5. código PySpark reproduzível e próximos passos priorizados.

Critérios de aceite:
- todos os números devem ter origem identificável;
- nenhuma regra de negócio pode ser inventada;
- divergências entre o grão esperado e o observado devem ser destacadas.
```

Esse exemplo é intencionalmente detalhado: ele mostra ao usuário **o que substituir, por que a informação importa e como conferir a resposta**.

---

<a id="-a-disciplina-dos-parâmetros-evitando-alucinações"></a>

## 🧩 A Disciplina dos Parâmetros: Evitando Alucinações

Um risco recorrente no uso de IA generativa em dados é preencher lacunas com hipóteses não confirmadas: assumir uma chave, inferir uma regra contábil ou escolher granularidade sem validação.

Os templates usam três convenções de preenchimento:

- **Valor concreto:** informação conhecida e confirmada, como `id_cliente` ou `dt_referencia`.
- **`NÃO INFORMADO`:** a informação é desconhecida neste momento. O prompt deve instruir a Genie Code a inspecionar o schema, fazer perguntas ou propor uma hipótese para aprovação antes de usá-la.
- **`NÃO APLICÁVEL`:** o campo foi avaliado e não se aplica ao caso, como uma tabela estática sem eixo temporal.

> **Não envie placeholders vazios (`{{...}}`).** Preencha o valor, use `NÃO INFORMADO` ou declare `NÃO APLICÁVEL`. Essas expressões são convenções do briefing, não travas técnicas da plataforma; a instrução e a revisão humana é que controlam o comportamento esperado.

### O contexto mínimo que evita retrabalho

| Informação | Pergunta respondida |
|---|---|
| **Objetivo** | Qual decisão ou resultado o trabalho deve apoiar? |
| **Recursos** | Quais tabelas, notebooks, células, arquivos ou modelos podem ser usados? |
| **Grão e chaves** | O que representa uma linha e como identificar registros? |
| **Tempo** | Qual período, coluna de data e instante de decisão valem? |
| **Regras e filtros** | O que incluir, excluir ou tratar de modo especial? |
| **Restrições** | Há limite de custo, tempo, memória, coleta ou mutação? |
| **Entrega** | Quais códigos, tabelas, gráficos e explicações são esperados? |
| **Aceite** | O que precisa ser verdadeiro para a resposta ser aprovada? |

---

## 🔄 A Sinergia Triangular: Prompts, Skills e Helpers

O Hub Prompts não opera isoladamente. Ele fornece o contexto do problema; uma skill pode fornecer a metodologia; snippets e scripts podem fornecer implementações reutilizáveis.

```mermaid
flowchart LR
    Briefing["📄 Briefing + recursos<br/>o problema"]
    Skill["🧠 Skill<br/>o método"]
    Genie["💬 Genie Code<br/>plano e código"]
    Helpers["⚡ Snippets + scripts<br/>a implementação"]
    Entrega["📓 Entrega revisável<br/>evidências e limites"]

    Briefing --> Genie
    Skill -. relevância ou @ .-> Genie
    Genie --> Entrega
    Helpers -->|import explícito| Entrega
```

- **O Briefing (Prompt):** fornece objetivo, contexto de negócio, recursos e parâmetros.
- **O Maestro (Skill):** orienta o fluxo metodológico e os guardrails, quando carregada por relevância ou selecionada por `@`.
- **Os Instrumentos (Snippets & Scripts):** oferecem código reutilizável; não são importados nem executados automaticamente pela skill.

---

## 📂 Famílias Funcionais de Prompts

Os briefings podem ser entendidos em quatro famílias do ciclo de dados:

```text
hub_prompts/
├── 🔍 Exploração & Perfilamento
├── 📈 Modelagem, Safras & Estatística
├── 🛡️ Qualidade, Reconciliação & Auditoria
└── 📚 Documentação, Tutoria & Onboarding
```

> **Nota de leitura:** essa árvore é uma organização **conceitual deste README**. Fisicamente, os 16 objetos ficam diretamente em `hub_prompts/<nome>/`.

### Matriz rápida de seleção

| Se a sua pergunta começa com... | Comece por... | Família |
|---|---|---|
| “O que existe e posso confiar nesta base?” | `eda_rapida`, `eda_completa` ou `data_quality` | exploração e qualidade |
| “Como estas tabelas se relacionam?” | `cross_eda` ou `comparar_tabelas` | cruzamento e reconciliação |
| “Como medir no tempo sem leakage?” | `safra` ou `feature_engineering` | temporalidade e risco |
| “Como modelar, explicar ou acompanhar?” | `baseline_orchestration`, `explainability` ou `monitoramento_modelo` | ciclo de ML |
| “Como transformar em processo?” | `pipeline` ou `novo_projeto` | implementação e onboarding |
| “Como revisar, ensinar ou documentar?” | `auditoria_skills`, `tutor_explicar` ou `comentar_notebook` | governança e comunicação |
| “A evidência sustenta a hipótese?” | `stat_check` | validação estatística |

### Legenda dos campos de cada briefing

| Campo | Função na conversa |
|---|---|
| **O que faz** | delimita o problema que o template organiza |
| **Skill recomendada** | sugere método; não significa ativação automática |
| **O usuário precisa informar** | explicita dados que não devem ser inventados |
| **Cenário de uso** | mostra quando o briefing costuma ser útil |
| **Arquivos** | indica os caminhos do template e do exemplo no pacote |

### 1. Exploração & Perfilamento

Diagnostica bases desconhecidas, volume, integridade, distribuições e viabilidade preliminar antes de esforços de desenvolvimento mais caros.

### 2. Modelagem, Safras & Estatística

Orienta coortes históricas, validação de hipóteses, engenharia de atributos, modelos baseline, explicabilidade e acompanhamento de drift.

### 3. Qualidade, Reconciliação & Auditoria

Trata confiabilidade de dados e código: anomalias, reconciliação entre bases e revisão crítica de entregas assistidas por IA.

### 4. Documentação, Tutoria & Onboarding

Transforma código em material compreensível, explica conceitos e estrutura o início de novos projetos.

---

<a id="-catálogo-detalhado-de-prompts"></a>

## 📖 Catálogo Detalhado de Prompts

O catálogo abaixo preserva as famílias e acrescenta links diretos para o briefing e para o notebook didático.

---

### 🔍 Exploração & Perfilamento

#### `eda_rapida` — Perfil Preliminar de Dados

- **O que faz:** organiza um diagnóstico inicial de grão, volume, completude e integridade básica.
- **Skill recomendada:** `@hub-ml-eda-profissional`.
- **O usuário precisa informar:** recurso, objetivo, foco, chave candidata, coluna temporal, filtros e limite de custo/tempo.
- **Cenário de Uso:**
  > *“Recebi acesso a uma tabela nova. Antes de propor uma análise, preciso entender estrutura, qualidade e bloqueios.”*
- **Arquivos:** `hub_prompts/eda_rapida/eda_rapida.md` · `hub_prompts/eda_rapida/exemplo_eda_rapida.py`

#### `eda_completa` — Análise Exploratória Profunda

- **O que faz:** estrutura exploração univariada e bivariada, distribuições, cardinalidade, dispersão e relações com o target quando houver.
- **Skill recomendada:** `@hub-ml-eda-profissional`.
- **O usuário precisa informar:** recurso, target, segmentos, janela, regras e restrições.
- **Cenário de Uso:**
  > *“Vamos construir um modelo de propensão e preciso avaliar as features candidatas antes do pré-processamento.”*
- **Arquivos:** `hub_prompts/eda_completa/eda_completa.md` · `hub_prompts/eda_completa/exemplo_eda_completa.py`

#### `cross_eda` — Exploração Cruzada Multi-Tabelas

- **O que faz:** analisa chaves, cardinalidade, integridade referencial, disponibilidade temporal e risco do join.
- **Skill recomendada:** `@hub-ml-cross-eda-ml`.
- **O usuário precisa informar:** tabelas, chaves, período, grão e resultado esperado do relacionamento.
- **Cenário de Uso:**
  > *“Quero cruzar cadastro e transações e medir correspondência, perda e multiplicação antes da tabela final.”*
- **Arquivos:** `hub_prompts/cross_eda/cross_eda.md` · `hub_prompts/cross_eda/exemplo_cross_eda.py`

---

### 📈 Modelagem, Safras & Estatística

#### `safra` — Análise de Coortes e Maturação Temporal

- **O que faz:** estrutura coortes, MOB, denominadores, eventos, censura e janelas comparáveis.
- **Skill recomendada:** `@hub-ml-analise-safra`.
- **Cenário de Uso:**
  > *“Quero comparar a inadimplência de contratos originados em meses diferentes após maturidade equivalente.”*
- **Arquivos:** `hub_prompts/safra/safra.md` · `hub_prompts/safra/exemplo_safra.py`

#### `stat_check` — Validação Estatística de Hipóteses

- **O que faz:** orienta escolha de teste, pressupostos, tamanho de efeito, incerteza e interpretação.
- **Skill recomendada:** `@hub-ml-validacao-estatistica`.
- **Cenário de Uso:**
  > *“Quero avaliar se a diferença observada em um teste A/B é estatisticamente e materialmente relevante.”*
- **Arquivos:** `hub_prompts/stat_check/stat_check.md` · `hub_prompts/stat_check/exemplo_stat_check.py`

#### `feature_engineering` — Engenharia de Atributos Temporais

- **O que faz:** especifica features, entidades, datas de corte, janelas, fontes e prevenção de leakage.
- **Skill recomendada:** `@hub-ml-feature-engineering`.
- **Cenário de Uso:**
  > *“Quero calcular comportamento em 30, 60 e 90 dias usando apenas dados disponíveis até a decisão.”*
- **Arquivos:** `hub_prompts/feature_engineering/feature_engineering.md` · `hub_prompts/feature_engineering/exemplo_feature_engineering.py`

#### `baseline_orchestration` — Modelo Baseline Ponta a Ponta

- **O que faz:** define problema, população, split, métricas, baseline e tracking antes de comparar soluções mais complexas.
- **Skill recomendada:** `@hub-ml-baseline-ml`.
- **Cenário de Uso:**
  > *“Preciso validar a esteira e estabelecer uma linha de base reproduzível antes de otimizar modelos.”*
- **Arquivos:** `hub_prompts/baseline_orchestration/baseline_orchestration.md` · `hub_prompts/baseline_orchestration/exemplo_baseline_orchestration.py`

#### `pipeline` — Construção de Pipelines Modulares

- **O que faz:** especifica fontes, contratos, etapas, incrementalidade, qualidade, observabilidade e destino.
- **Skill recomendada:** `@hub-ml-pipeline-builder`.
- **Cenário de Uso:**
  > *“Quero decompor um notebook monolítico em etapas testáveis e preparar sua automação.”*
- **Arquivos:** `hub_prompts/pipeline/pipeline.md` · `hub_prompts/pipeline/exemplo_pipeline.py`

#### `explainability` — Explicabilidade de Modelos de ML

- **O que faz:** define modelo, população, método, público e limites de uma explicação global ou local.
- **Skill recomendada:** `@hub-ml-explainability`.
- **Cenário de Uso:**
  > *“Preciso entender quais variáveis influenciaram o comportamento do modelo e comunicar as limitações da análise.”*
- **Arquivos:** `hub_prompts/explainability/explainability.md` · `hub_prompts/explainability/exemplo_explainability.py`

#### `monitoramento_modelo` — Acompanhamento de Performance e Drift

- **O que faz:** delimita referência, período atual, métricas, drift, thresholds e processo decisório.
- **Skill recomendada:** `@hub-ml-monitoramento-modelo`.
- **Cenário de Uso:**
  > *“Quero investigar se a população ou a performance mudou e produzir evidência para decidir o próximo passo.”*
- **Arquivos:** `hub_prompts/monitoramento_modelo/monitoramento_modelo.md` · `hub_prompts/monitoramento_modelo/exemplo_monitoramento_modelo.py`

---

### 🛡️ Qualidade, Reconciliação & Auditoria

#### `data_quality` — Varredura e Regras de Integridade

- **O que faz:** estrutura verificações de schema, nulidade, unicidade, formato e regras específicas.
- **Skill recomendada:** `@hub-ml-eda-profissional`.
- **Cenário de Uso:**
  > *“Antes de disponibilizar uma tabela, quero verificar chaves, nulos, intervalos e regras de domínio.”*
- **Arquivos:** `hub_prompts/data_quality/data_quality.md` · `hub_prompts/data_quality/exemplo_data_quality.py`

#### `comparar_tabelas` — Reconciliação entre Bases de Dados

- **O que faz:** compara schema, contagens, chaves e valores entre duas versões ou implementações.
- **Skill recomendada:** Genie Code ou `@hub-ml-cross-eda-ml`, conforme o foco.
- **Cenário de Uso:**
  > *“Quero reconciliar uma saída legada com a nova implementação e localizar divergências.”*
- **Arquivos:** `hub_prompts/comparar_tabelas/comparar_tabelas.md` · `hub_prompts/comparar_tabelas/exemplo_comparar_tabelas.py`

#### `auditoria_skills` — Auditoria de Código Gerado por IA

- **O que faz:** confronta pedido, skill, código, execução, evidências, helpers e guardrails.
- **Skill recomendada:** `@hub-ml-auditoria-skills`.
- **Cenário de Uso:**
  > *“Antes de aceitar um notebook gerado com IA, quero revisar segurança, temporalidade, custo e aderência ao contrato.”*
- **Arquivos:** `hub_prompts/auditoria_skills/auditoria_skills.md` · `hub_prompts/auditoria_skills/exemplo_auditoria_skills.py`

---

### 📚 Documentação, Tutoria & Onboarding

#### `comentar_notebook` — Refatoração e Documentação Didática

- **O que faz:** orienta cabeçalhos, contexto antes do código, comentários e interpretação depois da execução.
- **Skill recomendada:** `@hub-ml-comentar-notebook`.
- **Cenário de Uso:**
  > *“Quero tornar um notebook denso compreensível para a equipe sem alterar silenciosamente sua lógica.”*
- **Arquivos:** `hub_prompts/comentar_notebook/comentar_notebook.md` · `hub_prompts/comentar_notebook/exemplo_comentar_notebook.py`

#### `tutor_explicar` — Mentoria Técnica e Explicabilidade de Código

- **O que faz:** estrutura uma explicação adequada ao nível do leitor, com conceito, leitura do código, riscos e exercício.
- **Skill recomendada:** `@hub-ml-tutor-databricks`.
- **Cenário de Uso:**
  > *“Quero entender como o plano Spark, o particionamento e o join se relacionam com a lentidão observada.”*
- **Arquivos:** `hub_prompts/tutor_explicar/tutor_explicar.md` · `hub_prompts/tutor_explicar/exemplo_tutor_explicar.py`

#### `novo_projeto` — Kick-off Estruturado de Projetos de Dados

- **O que faz:** conduz descoberta de negócio, fontes, restrições, arquitetura, riscos, entregáveis e critérios de aceite.
- **Skill recomendada:** Genie Code; selecione uma skill especializada depois que a natureza da entrega estiver clara.
- **Cenário de Uso:**
  > *“Vamos iniciar um projeto de precificação e quero organizar perguntas, escopo, dependências e plano antes de criar artefatos.”*
- **Arquivos:** `hub_prompts/novo_projeto/novo_projeto.md` · `hub_prompts/novo_projeto/exemplo_novo_projeto.py`

---

<a id="️-passo-a-passo-operacional-do-briefing-ao-resultado"></a>

## 🛠️ Passo a Passo Operacional: Do Briefing ao Resultado

Seguir o fluxo abaixo favorece respostas mais consistentes, código auditável e menor retrabalho:

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Desenvolvedor
    participant Hub as Hub Prompt (.md)
    participant Chat as Genie Code
    participant Runtime as Databricks

    Dev->>Hub: Seleciona o template adequado
    Dev->>Dev: Preenche campos e critérios de aceite
    Dev->>Chat: Anexa recursos e fornece o briefing
    Chat-->>Dev: Propõe plano, premissas e operações
    Dev->>Chat: Aprova, restringe ou corrige o plano
    Chat->>Runtime: Executa somente o que foi autorizado
    Runtime-->>Chat: Retorna resultados e erros observados
    Chat-->>Dev: Entrega código, evidências e limitações
    Dev->>Dev: Confere a resposta contra o checklist
```

### 1. Selecione o Briefing Adequado

Escolha o prompt pelo resultado principal. Se a demanda mistura EDA, features e baseline, trate cada fase com seu próprio contrato e só transporte premissas já validadas.

### 2. Preencha os Metadados com Rigor

Substitua todos os placeholders. Use identificadores precisos, declare desconhecidos e não envie segredos, tokens, credenciais ou dados desnecessários.

### 3. Anexe os Recursos e Defina o Modo de Trabalho

Na Genie Code:

- use `@` ou **Add Context** para fornecer tabelas, notebooks, arquivos e outros recursos oferecidos pela interface;
- use o identificador completo `catalog.schema.table` quando trabalhar com Unity Catalog;
- quando aplicável, utilize contexto de célula, como `@cell`;
- `/findTables` pode ajudar a localizar tabelas; aliases como `/eda` não são comandos registrados pelo Hub;
- diga se deseja explicação, plano, geração de código ou execução;
- selecione uma skill com `@` quando quiser explicitar a metodologia.

Uma conversa nova é útil quando objetivo, conjunto de dados ou fase mudam materialmente. Para refinamentos do mesmo problema, o histórico validado pode ajudar.

### 4. Revise o Plano antes de Executar

Confirme recursos, filtros, período, operações, coleta no driver, custo e ações persistentes. Um prompt não amplia permissões e não substitui a política de aprovação configurada.

### 5. Valide a Entrega contra o Contrato de Saída

- diferencie código sugerido, código executado e resultado validado;
- confira se fatos e hipóteses estão separados;
- confirme a origem dos números e as limitações;
- revise qualquer `CREATE`, `ALTER`, `DROP`, `DELETE`, `MERGE`, instalação ou mudança de configuração;
- registre a resposta real no notebook de exemplo apenas quando ela tiver sido obtida e revisada.

---

<a id="-perguntas-frequentes-faq"></a>

## ❓ Perguntas Frequentes (FAQ)

### 1. Por que preencher um briefing estruturado em vez de apenas fazer uma pergunta livre?

Porque o briefing torna objetivo, dados, temporalidade, limites e entrega explícitos. Isso reduz ambiguidades e facilita a revisão, mas não impede sozinho erros do modelo ou do usuário.

### 2. O que preencher quando eu não souber a chave primária ou a granularidade?

Use `NÃO INFORMADO` e instrua o assistente a inspecionar ou perguntar antes de assumir. Não invente um nome e não deixe o placeholder vazio.

### 3. Por que o notebook `exemplo_*.py` não executa o prompt automaticamente?

Porque o prompt é uma interface conversacional. O notebook prepara dados, demonstra o preenchimento e registra a resposta real; não existe, neste Hub, uma automação silenciosa que envie o texto ao chat.

### 4. Quando abrir uma conversa nova?

Quando mudar materialmente o objetivo, os dados, a fase ou a skill recém-editada. Para aprofundar a mesma tarefa com premissas já verificadas, continuar a conversa pode preservar contexto útil.

### 5. Minha equipe pode criar novos modelos de briefing?

Sim. Use o padrão `<nome>/<nome>.md` e `<nome>/exemplo_<nome>.py`, explique cada campo e inclua limites, saída e checklist. A skill `@hub-ml-criar-objeto` pode orientar a estrutura, mas criar arquivos continua sendo uma ação explícita.

### 6. O prompt carrega a skill e os helpers automaticamente?

Não. A skill pode ser selecionada por relevância ou `@`. Snippets e scripts precisam ser importados pelo notebook. O prompt apenas fornece contexto e instruções.

---

## 🔗 Continue Explorando

- [Agent Skills](README_skills.md)
- [Hub Snippets](README_snippets.md)
- [Hub Scripts](README_scripts.md)
- [Boas práticas de prompting na Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [Funcionalidades da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/features-capabilities)
