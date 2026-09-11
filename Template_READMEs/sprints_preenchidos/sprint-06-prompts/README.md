![CRM — Missão Modelos Analíticos CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

<a id="hub-prompts-briefings-técnicos-estruturados-para-genie-code"></a>

# Hub Prompts — Briefings Técnicos Estruturados para Genie Code

O **Hub Prompts** reúne formulários para traduzir uma demanda analítica em pedido delimitado, rastreável e revisável.

> **CONTEÚDO CUSTOMIZADO PELO HUB · USO MANUAL.** `hub_prompts` não é pasta nativa descoberta ou executada pela Genie Code. Você escolhe o template, preenche e fornece o texto no chat.

> **Rascunho de sprint 6 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/hub_prompts/README.md`.

---

<a id="neste-guia"></a>

## 🧭 Neste Guia

Jornada: escolher → preencher → fornecer contexto → revisar → validar. O catálogo por família é consulta, não substitui essa jornada.

| Para entender... | Vá para... |
|---|---|
| por que usar um briefing estruturado | [O que é um Prompt Estruturado](#o-que-é-um-prompt-estruturado) |
| como a pasta é organizada | [Anatomia da Pasta](#a-anatomia-de-uma-pasta-de-prompt) |
| como preencher sem inventar | [Disciplina dos Parâmetros](#a-disciplina-dos-parâmetros-evitando-alucinações) |
| qual prompt escolher | [Catálogo Detalhado](#catálogo-detalhado-de-prompts) |
| como conduzir a interação | [Passo a Passo Operacional](#passo-a-passo-operacional-do-briefing-ao-resultado) |
| dúvidas e limites | [Perguntas Frequentes](#perguntas-frequentes-faq) |

---

<a id="o-que-é-um-prompt-estruturado"></a>

## 🎯 O que é um Prompt Estruturado?

É uma **ordem de serviço**, não uma fórmula mágica.

**Pedido vago:** “analise a campanha.” Faltam tabela, grão, chave, período, o que pode gravar.

**Pedido melhorado, com motivo de cada acréscimo:**

- recurso anexado → o recurso pretendido fica identificável; a resposta ainda precisa de revisão;
- `event_id` como chave candidata → unicidade pode ser checada;
- `dt_evento` e janela → leakage e filtro ficam explícitos;
- somente leitura + plano primeiro → você controla custo;
- aceite: números com origem → revisão possível.

O briefing **não** garante correção do modelo.

| | Chat ad hoc | Briefing Hub |
|---|---|---|
| Entrada | “analise isto” | objetivo, dados, grão, período, filtros |
| Premissas | lacunas na conversa | `NÃO INFORMADO` visível |
| Custo | implícito | limites declarados |
| Entrega | formato variável | contrato e aceite no texto |

---

<a id="a-anatomia-de-uma-pasta-de-prompt"></a>

## 🏗️ A Anatomia de uma Pasta de Prompt

```text
hub_prompts/eda_rapida/
├── eda_rapida.md              briefing preenchível
└── exemplo_eda_rapida.py      notebook de acompanhamento
```

![Anatomia de um briefing técnico forte](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/prompts/png/03_anatomia_briefing.png)

*Leitura da figura: objetivo e contexto delimitam o problema; restrições controlam a operação; entrega e aceite dizem quando está pronto. O template copiável continua sendo o `.md`.*

<a id="1-o-arquivo-markdown-md"></a>

### 1. O Arquivo Markdown (`<nome>.md`)

Leia para saber quando usar. Copie a seção de prompt preenchida para o chat. Abrir o arquivo **não** envia nada à Genie.

Contém, em geral: quando usar / não usar, guia de cada campo, prompt para preencher, o que conferir na resposta.

<a id="2-o-notebook-de-acompanhamento-exemplo_py"></a>

### 2. O Notebook de Acompanhamento (`exemplo_<nome>.py`)

Três partes: preparo sintético, prompt preenchido, espaço para registrar resposta **real**. Enquanto a parte 3 estiver vazia, o notebook **não** homologa o prompt conversacionalmente. Não execute o `.md` a partir do notebook — não há essa automação.

<a id="3-exemplo-de-briefing-completamente-preenchido"></a>

### 3. Exemplo de briefing completamente preenchido

Cenário: decidir se eventos de campanha (sintéticos ou tabela autorizada) servem a um estudo mensal de retenção.

```text
Quero planejar uma EDA rápida da view local `vw_campanha_eventos_sintetica` criada na célula de preparação selecionada, nesta mesma sessão.

Objetivo:
- conferir o mecanismo de análise de resposta em uma fixture didática de 20 eventos;
- identificar bloqueios de qualidade antes das métricas.

Contexto:
- grão esperado: um evento de cliente por linha;
- chave candidata: event_id;
- entidade: id_cliente;
- coluna temporal: dt_evento;
- período: 2026-06-01 a 2026-06-20;
- filtro: nenhum; não existe event_status nesta fixture;
- regras adicionais: NÃO INFORMADO — pergunte antes de assumir.

Modo de trabalho:
- somente plano neste turno; não execute código;
- plano e consultas pretendidas primeiro;
- não coletar a tabela inteira no driver;
- amostras limitadas e justificadas;
- aprovação antes de persistir ou de leitura ampla.

Entregue:
1. schema, volume e intervalo temporal observado;
2. unicidade da chave e completude;
3. distribuição das variáveis relevantes;
4. anomalias e limitações (fato vs hipótese);
5. código PySpark reproduzível e próximos passos.

Critérios de aceite:
- todo número com origem identificável;
- nenhuma regra de negócio inventada;
- divergência de grão destacada.
```

A preparação completa está no [guia de uso](../sprint-02-assistant/README.md#exemplo-conhecer-uma-tabela-nova). Selecione a célula e seu schema; uma view temporária não passa a ser tabela persistente do catálogo. Ao adaptar, confira também cada coluna e filtro, não somente o nome do recurso. Uma resposta realmente obtida é evidência observada; sua aprovação depende da revisão contra o pedido. Texto hipotético e valores esperados devem manter esses rótulos.

---

<a id="a-disciplina-dos-parâmetros-evitando-alucinações"></a>

## 🧩 A Disciplina dos Parâmetros: Evitando Alucinações

Três convenções (humanas, não travas da plataforma):

| Marca | Significado | Exemplo |
|---|---|---|
| Valor concreto | confirmado | `event_id` |
| `NÃO INFORMADO` | desconhecido agora | peça inspeção ou pergunta |
| `NÃO APLICÁVEL` | avaliado e não cabe | tabela estática sem eixo tempo |

Não envie `{{...}}` vazio.

<a id="o-contexto-mínimo-que-evita-retrabalho"></a>

### O contexto mínimo que evita retrabalho

Objetivo, recursos, grão e chaves, tempo, regras, restrições, entrega, aceite. Faltar um deles é o que costuma gerar hipótese silenciosa.

**Aplicação.** Sem `dt_evento`, a Genie pode misturar eventos futuros à feature. Marque `NÃO INFORMADO` em vez de inventar o nome da coluna.

---

<a id="a-sinergia-triangular-prompts-skills-e-helpers"></a>

## 🔄 A Sinergia Triangular: Prompts, Skills e Helpers

O briefing define o problema; a skill, se carregada, organiza o método; o helper exige uma chamada no runtime; o notebook é a rota usada neste tutorial.

Na campanha: `eda_rapida` + `@hub-ml-eda-profissional` +, se autorizado, `data_quality_check`. Três interfaces, três ações suas.

---

<a id="famílias-funcionais-de-prompts"></a>

## 📂 Famílias Funcionais de Prompts

![Mapa das famílias de briefing](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/prompts/png/01_mapa_familias.png)

*Leitura da figura: quatro famílias conceituais. No disco, os 16 objetos ficam em `hub_prompts/<nome>/`, sem essas pastas extras.*

| Se a pergunta começa com... | Comece por... |
|---|---|
| “O que existe nesta base?” | `eda_rapida`, `eda_completa`, `data_quality` |
| “Como as tabelas se relacionam?” | `cross_eda`, `comparar_tabelas` |
| “Como medir no tempo sem leakage?” | `safra`, `feature_engineering` |
| “Como modelar, explicar, acompanhar?” | `baseline_orchestration`, `explainability`, `monitoramento_modelo` |
| “Como virar processo?” | `pipeline`, `novo_projeto` |
| “Como revisar, ensinar, documentar?” | `auditoria_skills`, `tutor_explicar`, `comentar_notebook` |
| “A evidência sustenta a hipótese?” | `stat_check` |

**Dois briefings próximos.** `eda_rapida` vs `eda_completa`: a primeira decide se a base é usável; a segunda aprofunda distribuições e relações com target. Não preencha os dois no mesmo chat sem fase explícita.

---

<a id="catálogo-detalhado-de-prompts"></a>

## 📖 Catálogo Detalhado de Prompts

Os microbriefings são completamente preenchidos para o **modo plano**; um campo desconhecido continua explicitamente desconhecido. Eles não alegam tabelas, modelos ou resultados reais inexistentes. Primeiro selecione o recurso indicado; depois cole o texto. As instruções completas do formulário e seu notebook específico estão vinculados em cada ficha.

<a id="exploração-perfilamento"></a>

### Exploração & Perfilamento

<a id="eda_rapida-perfil-preliminar-de-dados"></a>

#### `eda_rapida` — Perfil Preliminar de Dados

**Quando usar e quando não usar.** Conhecer uma fonte antes de investir numa análise extensa. Não escolher para cruzar várias fontes ou testar causalidade.

**Campos essenciais.** O foco limita o diagnóstico; chave candidata permite testar unicidade, mas precisa corresponder ao grão. Tempo/custo descrevem autorização de leitura, não prazo prometido pela IA.

**Microbriefing preenchido — chat:**

```text
@hub-ml-eda-profissional

Recurso selecionado: célula que cria vw_campanha_eventos_sintetica e seu schema.
Objetivo: conferir a fixture antes de medir resposta; foco: chave e nulos.
Grão: evento. Chave candidata: event_id. Entidade: id_cliente. Tempo: dt_evento.
Período: 01/06/2026 a 20/06/2026. Filtros: nenhum. Limite: 20 linhas sintéticas.
Modo: plano somente; nenhuma execução ou escrita neste turno.
Entregue consultas propostas, entradas, saídas e como validar os números.
```

**Saída e critérios de aceite.** Após execução autorizada, conferir 20 eventos, cinco clientes, um nulo em canal, 5%. Não aceitar contagem aproximada como exata sem identificação do método. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Aprofunde apenas a nulidade de canal; não proponha imputação sem explicar o efeito sobre o uso.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/eda_rapida/eda_rapida.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/eda_rapida/exemplo_eda_rapida.py).

<a id="eda_completa-análise-exploratória-profunda"></a>

#### `eda_completa` — Análise Exploratória Profunda

**Quando usar e quando não usar.** Investigar distribuições, relações e segmentos de uma fonte já compreendida. Se o objetivo é apenas localizar um bloqueio de qualidade, comece pela rápida.

**Campos essenciais.** Target precisa de definição e disponibilidade temporal. Uma relação bivariada com respondeu não demonstra efeito causal nem validade preditiva.

**Microbriefing preenchido — chat:**

```text
@hub-ml-eda-profissional

Recurso: mesma fixture sintética selecionada; 20 eventos, event_id único.
Entidade: id_cliente; temporal: dt_evento; período: junho/2026; filtros: nenhum.
Target descritivo: respondeu (0/1); valor_gasto é valor por evento sintético em reais.
Foco: distribuição do valor e resposta por cliente; público: analista.
Modo: plano, sem execução ou escrita. Saída: roteiro, gráficos adequados,
agregações, denominadores e limitações da base pequena e artificial.
```

**Saída e critérios de aceite.** Não aceitar performance de modelo ou significância inferencial fictícia. Agregações por cliente mudam o grão e devem ser rotuladas. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Separe análise por evento e por cliente e explique por que seus denominadores diferem.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/eda_completa/eda_completa.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/eda_completa/exemplo_eda_completa.py).

<a id="cross_eda-exploração-cruzada-multi-tabelas"></a>

#### `cross_eda` — Exploração Cruzada Multi-Tabelas

**Quando usar e quando não usar.** Avaliar como fontes se cruzam e se há disponibilidade temporal para ML. Não substitui reconciliação linha a linha entre duas versões equivalentes.

**Campos essenciais.** Âncora é a população que você quer preservar. Definir autoridade de cada atributo impede resolver conflitos por conveniência.

**Microbriefing preenchido — chat:**

```text
@hub-ml-cross-eda-ml

Fontes selecionadas: fixture de eventos e dimensão didática de cinco clientes únicos.
Âncora: eventos; chave de join: id_cliente; saída: uma linha por event_id.
Período: junho/2026. Fontes autoritativas, vigência e instante de publicação: NÃO INFORMADO.
Target/horizonte de modelagem: NÃO INFORMADO. Foco: viabilidade de join, não treino.
Modo: plano apenas; não juntar ou persistir. Entregue duplicidade, cobertura,
expansão esperada, conflitos e perguntas que impedem concluir prontidão.
```

**Saída e critérios de aceite.** Exigir expansão em relação à âncora e bloqueio de inferência temporal enquanto não houver vigência. O helper diagnosticar_join pertence a hub_snippets.spark. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Inclua um teste negativo com cliente duplicado na dimensão antes de propor materialização.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/cross_eda/cross_eda.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/cross_eda/exemplo_cross_eda.py).

<a id="modelagem-safras-estatística"></a>

### Modelagem, Safras & Estatística

<a id="safra-análise-de-coortes-e-maturação-temporal"></a>

#### `safra` — Análise de Coortes e Maturação Temporal

**Quando usar e quando não usar.** Comparar grupos de entrada na mesma idade de observação. Não comparar safras imaturas como se tivessem o mesmo acompanhamento.

**Campos essenciais.** Safra agrupa entrada; MOB mede idade. Denominador, evento e censura determinam a taxa, não são inferidos do nome das colunas.

**Microbriefing preenchido — chat:**

```text
@hub-ml-analise-safra

Dataset: painel adicional ainda NÃO FORNECIDO; não reutilize o schema de campanha como crédito.
Schema pretendido: contrato_id, dt_originacao, dt_referencia, evento.
Entidade/chave: contrato × mês. Safra: mês de dt_originacao; frequência mensal.
Evento, denominador, censura e maturidade: NÃO INFORMADO. Métrica: incidência acumulada proposta.
Segmentos/período: a definir; fonte normativa: NÃO APLICÁVEL ao exemplo sintético.
Modo: planejar sem executar. Entregue contrato, exemplo esquemático e verificações;
não apresente curvas calculadas nem preencha mês não observado com zero.
```

**Saída e critérios de aceite.** Comparação por mesmo MOB, evento incidente versus acumulado explícito, nenhum número tratado como observado sem painel. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Mostre por que duas coortes de idades diferentes não devem ser comparadas pelo último ponto bruto.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/safra/safra.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/safra/exemplo_safra.py).

<a id="stat_check-validação-estatística-de-hipóteses"></a>

#### `stat_check` — Validação Estatística de Hipóteses

**Quando usar e quando não usar.** Planejar inferência e diagnóstico de pressupostos. Para simples completude e duplicatas, data_quality é mais direto.

**Campos essenciais.** Unidade experimental e dependência importam tanto quanto teste. Registros repetidos de cliente não viram indivíduos independentes.

**Microbriefing preenchido — chat:**

```text
@hub-ml-validacao-estatistica

Objetivo: planejar comparação de taxa de resposta entre tratamentos.
Dados selecionados: fixture de eventos; tratamento e alocação aleatória: NÃO INFORMADO.
População: sintética, 20 eventos/5 clientes; chave event_id; grupos ainda não definidos.
Target: respondeu; horizonte, acompanhamento e split: NÃO INFORMADO.
Hipótese: diferença de taxas, a pré-especificar com direção e relevância prática.
Modo: diagnóstico de requisitos e plano; não calcular p-valor ou executar código.
Proponha método, efeito, intervalo, unidade de análise e correção para múltiplos testes.
```

**Saída e critérios de aceite.** Deve detectar contexto insuficiente, dependência por cliente e impossibilidade de alegar causalidade nessa fixture. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Explique o que mudaria se o tratamento fosse sorteado por cliente e não por evento.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/stat_check/stat_check.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/stat_check/exemplo_stat_check.py).

<a id="feature_engineering-engenharia-de-atributos"></a>

#### `feature_engineering` — Engenharia de Atributos

**Quando usar e quando não usar.** Especificar transformações e disponibilidade de atributos. Se a viabilidade das fontes ainda é a pergunta central, use cross_eda.

**Campos essenciais.** Instante de decisão separa passado permitido de futuro; horizonte do alvo não é a janela observada dos atributos.

**Microbriefing preenchido — chat:**

```text
@hub-ml-feature-engineering

Entidade: id_cliente; grão previsto: evento; chave event_id.
Fonte: fixture selecionada com dt_evento e valor_gasto; sem joins adicionais.
Decisão didática: início do dia de cada evento; janela: 30 dias estritamente anteriores.
Target/horizonte reais, features existentes e atraso de publicação: NÃO INFORMADO.
Frequência proposta: por evento. Modo: plano, sem materializar ou executar.
Entregue especificações de contagem/soma, nulos, disponibilidade e testes
para evento futuro. Proíba respondeu do próprio evento como preditor.
```

**Saída e critérios de aceite.** Contrato temporal explícito, grão preservado e teste de não utilização do evento atual/futuro. Atraso desconhecido permanece pendente. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Mostre separadamente data do evento e data em que o dado ficou disponível ao modelo.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/feature_engineering/feature_engineering.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/feature_engineering/exemplo_feature_engineering.py).

<a id="baseline_orchestration-baseline-e-avaliação"></a>

#### `baseline_orchestration` — Baseline e Avaliação

**Quando usar e quando não usar.** Organizar treino e avaliação de uma régua inicial. Não substitui definição do problema ou fornece licença para executar todos os modelos.

**Campos essenciais.** Target, split e métrica devem refletir o uso. Para algumas famílias, ranking e sobrevivência por exemplo, há entradas adicionais obrigatórias.

**Microbriefing preenchido — chat:**

```text
@hub-ml-baseline-ml

Problema: classificação de resposta; dataset: fixture selecionada de 20 eventos.
Target: respondeu; grão/chave: evento/event_id; entidade: id_cliente.
Decisão: início do dia do evento. Horizonte real: NÃO INFORMADO.
Período: junho/2026. Split: proponha temporal e justifique dados adicionais necessários.
Colunas proibidas: respondeu como feature e informação posterior à decisão.
Métrica/custo de erro: propor, sem otimizar na fixture artificial.
Modo: plano; sem treino, instalação, MLflow ou escrita. Entregue plano, baseline,
protocolo de validação, dependências e limites da demonstração.
```

**Saída e critérios de aceite.** Nenhuma métrica inventada; separação entre treino/validação/teste e tracking proposto versus executado. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Explique por que uma divisão temporal de 20 registros não certifica performance de produção.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/baseline_orchestration/baseline_orchestration.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/baseline_orchestration/exemplo_baseline_orchestration.py).

<a id="pipeline-arquitetura-e-operação-de-pipeline"></a>

#### `pipeline` — Arquitetura e Operação de Pipeline

**Quando usar e quando não usar.** Transformar uma rotina validada em processo repetível. Não usar para fingir deployment sem destinos e identidade definidos.

**Campos essenciais.** Idempotência significa que reprocessar não duplica indevidamente o efeito. Incrementalidade exige chave, sequência e tratamento de atrasos.

**Microbriefing preenchido — chat:**

```text
@hub-ml-pipeline-builder

Objetivo: executar checagens recorrentes sobre eventos da campanha.
Origem persistente/destino/consumidores/ambientes: NÃO INFORMADO.
Chave pretendida: event_id; sequência: dt_evento, critério de desempate pendente.
Modo de ingestão: propor batch versus incremental conforme requisitos.
Schema/evolução: apresentar contrato da fixture e perguntas para produção.
Qualidade: chave única/não nula; nulidade de canal com limites a calibrar.
SLO, volume e frequência: NÃO INFORMADO. Modo: arquitetura apenas, sem deploy.
Entregue dependências, replay, qualidade, observabilidade e rollback.
```

**Saída e critérios de aceite.** Proposta deve declarar pendências e efeitos de cada etapa, não criar objetos nem declarar SLAs atendidos. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Diferencie registrar violação, descartar registro e falhar a atualização em cada regra proposta.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/pipeline/pipeline.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/pipeline/exemplo_pipeline.py).

<a id="explainability-explicação-de-modelo"></a>

#### `explainability` — Explicação de Modelo

**Quando usar e quando não usar.** Entender um modelo já existente, globalmente ou em um caso individual. Treinar um modelo novo pertence ao baseline.

**Campos essenciais.** Classe de saída, escala e preprocessamento são parte da explicação. SHAP não é coeficiente causal.

**Microbriefing preenchido — chat:**

```text
@hub-ml-explainability

Modelo/run/versão: NÃO INFORMADO; nenhum modelo foi selecionado ainda.
Objetivo: planejar explicação global/local de probabilidade respondeu=1.
Dataset/split/amostra/segmentos/período: a fornecer após revisão do artefato.
Público: técnico e gestor; método: proponha segundo o modelo, sem presumir árvore.
Modo: plano; não carregar dados, executar explicações ou gravar MLflow.
Entregue lista de artefatos, amostragem, escala, validações e limites;
não invente importância ou razões individuais.
```

**Saída e critérios de aceite.** Deve pedir modelo e dados compatíveis; explicação global não basta para justificar um caso local. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Explique como mudaria a interpretação se a saída estivesse em log-odds e não probabilidade.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/explainability/explainability.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/explainability/exemplo_explainability.py).

<a id="monitoramento_modelo-monitoramento-e-resposta-operacional"></a>

#### `monitoramento_modelo` — Monitoramento e Resposta Operacional

**Quando usar e quando não usar.** Acompanhar distribuição, qualidade, performance e operação. Uma análise de um único período não substitui contrato recorrente.

**Campos essenciais.** Direção da métrica impede alarmar uma melhora. Atraso do rótulo determina quando é possível avaliar performance.

**Microbriefing preenchido — chat:**

```text
@hub-ml-monitoramento-modelo

Modelo/run/versão e caminho de inferência: NÃO INFORMADO; não há produção nesta fixture.
Referência: coorte ref; atual: mudou, da preparação sintética selecionada no guia de scripts.
Variável: valor_gasto. Target e atraso do rótulo: NÃO INFORMADO.
Métrica disponível: PSI; direção/limites de performance: a definir com modelo e rótulos.
Segmentos: nenhum por enquanto. Frequência, owner e SLO: NÃO INFORMADO.
Modo: desenho, sem medir, criar alerta ou retreinar. Entregue contrato de
monitoramento, lacunas, critérios de investigação e responsável a designar.
```

**Saída e critérios de aceite.** Drift não deve virar causa atribuída ou gatilho automático de retreino. Sem limites, pedir calibração em vez de classificar universalmente. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Inclua os cenários sem rótulo, melhora de métrica e população muito pequena.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/monitoramento_modelo/monitoramento_modelo.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/monitoramento_modelo/exemplo_monitoramento_modelo.py).

<a id="qualidade-reconciliação-auditoria"></a>

### Qualidade, Reconciliação & Auditoria

<a id="data_quality-regras-de-qualidade"></a>

#### `data_quality` — Regras de Qualidade

**Quando usar e quando não usar.** Especificar e revisar integridade em uma fonte. Perfilamento explora; este briefing explicita regras e uso downstream.

**Campos essenciais.** Limiar tem unidade e dono. A chave candidata deve ser revisada antes de uma falha interromper um fluxo.

**Microbriefing preenchido — chat:**

```text
@hub-ml-eda-profissional

Recurso: célula da fixture selecionada; view local vw_campanha_eventos_sintetica.
Grão: evento; chave event_id; dt_evento: junho/2026; partições: NÃO APLICÁVEL à view.
Uso: demonstrar checagem antes de análise de resposta.
Regras didáticas: chave não nula/única; nulos warn>=5%, fail>=20%.
Freshness: não medir nesta etapa histórica. Modo: plano, sem executar ou escrever.
Entregue chamada proposta a data_quality_check, campos checks/alerts/score e
oráculos de pass/warn/fail, rotulados como esperados.
```

**Saída e critérios de aceite.** Esperado original warn/95, um nulo em 20. Rejeitar metrics.row_count: retorno usa checks.row_count. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Mostre a política consumidora que interromperia em fail, sem executá-la agora.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/data_quality/data_quality.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/data_quality/exemplo_data_quality.py).

<a id="comparar_tabelas-reconciliação-de-versões"></a>

#### `comparar_tabelas` — Reconciliação de Versões

**Quando usar e quando não usar.** Comparar duas versões que deveriam representar o mesmo universo. Não confundir reconciliação com acrescentar features por join.

**Campos essenciais.** Tolerância monetária, nulidade e duplicidade devem ser decididas antes de comparar valores. Mesma contagem não implica mesmos registros.

**Microbriefing preenchido — chat:**

```text
@hub-ml-cross-eda-ml

Versão A: fixture selecionada. Versão B: ainda NÃO FORNECIDA.
Objetivo: planejar reconciliação por event_id, um evento por linha.
Colunas críticas: id_cliente, dt_evento, respondeu, valor_gasto, canal.
Período: junho/2026; filtros: nenhum. Tolerância de valor: proponha e justifique,
sem converter automaticamente diferença monetária em igualdade.
Modo: plano sem execução/persistência. Entregue faltantes por lado, duplicatas,
diferenças de schema/valor e como tratar nulos; não diga que A e B coincidem.
```

**Saída e critérios de aceite.** Exigir ambas as versões antes do resultado e informar duplicatas antes de presumir correspondência um-para-um. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Inclua um cenário em que as contagens são iguais, mas um event_id foi substituído.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/comparar_tabelas/comparar_tabelas.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/comparar_tabelas/exemplo_comparar_tabelas.py).

<a id="auditoria_skills-revisão-de-contrato-e-evidência"></a>

#### `auditoria_skills` — Revisão de Contrato e Evidência

**Quando usar e quando não usar.** Auditar a implementação de uma skill ou o output produzido contra um contrato. Não confundir com auditoria genérica de dados.

**Campos essenciais.** Modo implementação/output determina as fontes necessárias. Correção de arquivos precisa de autorização diferente da leitura.

**Microbriefing preenchido — chat:**

```text
@hub-ml-auditoria-skills

Modo: auditoria de output; skill alvo: hub-ml-eda-profissional.
Selecione SKILL.md, pedido original e output real; caso não estejam disponíveis,
marque a falta e não conclua sobre eles.
Caso esperado: diagnóstico de 20 eventos, chave event_id e nulidade de canal.
Foco: contrato, números, efeitos e procedência. Dependências: declarações e código selecionados.
Testes: pedido positivo de EDA, negativo de criação de objeto e menção explícita.
Entrega: relatório, sem correções; severidade, evidência e critério de aceite por achado.
```

**Saída e critérios de aceite.** Ausência de acesso não é prova de inexistência. Teste descrito não é teste executado. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Separe quais achados são confirmados por código e quais exigem runtime ou conversa nova.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/auditoria_skills/auditoria_skills.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/auditoria_skills/exemplo_auditoria_skills.py).

<a id="documentação-tutoria-onboarding"></a>

### Documentação, Tutoria & Onboarding

<a id="comentar_notebook-documentação-de-notebook"></a>

#### `comentar_notebook` — Documentação de Notebook

**Quando usar e quando não usar.** Adicionar narrativa ao artefato existente. Para explicar sem propor edição, use tutor_explicar.

**Campos essenciais.** Densidade, público e permissão de alterar código são campos diferentes. Markdown não pode atribuir execução não observada.

**Microbriefing preenchido — chat:**

```text
@hub-ml-comentar-notebook

Objeto: célula selecionada de data_quality_check da fixture.
Objetivo: documentar entradas e interpretação. Público: analista iniciante no Hub.
Densidade: didática. Modo: proposta textual, sem edição/execução.
Pode alterar código: NÃO. Convenções: um banner CRM, títulos em Markdown,
nomes de API preservados, valores esperados separados de observados.
Entregue PRÉ e PÓS; explique 1/20=5%, checks, alerts, score e decisão do consumidor.
```

**Saída e critérios de aceite.** Diff de código vazio, nenhuma saída fabricada, banner não substitui título ou instrução. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Reduza apenas a repetição; preserve entrada, resultado esperado e limites.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/comentar_notebook/comentar_notebook.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/comentar_notebook/exemplo_comentar_notebook.py).

<a id="tutor_explicar-tutoria-e-leitura-de-código"></a>

#### `tutor_explicar` — Tutoria e Leitura de Código

**Quando usar e quando não usar.** Aprender comportamento ou diagnosticar erro com explicação progressiva. Não pedir deployment ou reescrita implícita.

**Campos essenciais.** Nível prévio calibra a explicação; ambiente/erro exato evita prescrever solução incompatível com o runtime.

**Microbriefing preenchido — chat:**

```text
@hub-ml-tutor-databricks

Objeto: chamada de qualidade selecionada. Nível: leio Python, não conheço imports de pacote.
Preciso entender sys.path, SparkSession, temp view e retorno em dicionário.
Contexto: campanha sintética. Ambiente: notebook Databricks; versão exata NÃO INFORMADA.
Modo: linha a linha, explicar apenas; não executar, instalar ou modificar arquivos.
Compare plano da Genie, código proposto e execução. Dê um exercício com chave duplicada.
```

**Saída e critérios de aceite.** Distinguir interpretação Python, execução Spark e contexto do agente; analogia deve voltar à API concreta. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Explique por que colar o arquivo no chat não o importa no interpretador.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/tutor_explicar/tutor_explicar.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/tutor_explicar/exemplo_tutor_explicar.py).

<a id="novo_projeto-planejamento-inicial"></a>

#### `novo_projeto` — Planejamento Inicial

**Quando usar e quando não usar.** Organizar objetivo, responsáveis e entregas quando o projeto ainda está nascendo. Não usar uma estrutura pré-fabricada para evitar esclarecer a decisão.

**Campos essenciais.** Métrica de sucesso não é lista de tecnologias. Donos, restrições e ambientes não devem ser preenchidos com identidades ou caminhos inventados.

**Microbriefing preenchido — chat:**

```text
Nome didático: estudo_resposta_campanha. Objetivo: avaliar dados e planejar análise de resposta.
Recursos: fixture selecionada; fontes reais, repositório e ambientes: NÃO INFORMADO.
Entidade: cliente; grão inicial: evento; target/horizonte de negócio: a definir.
Métricas de sucesso: propor distinguindo qualidade, análise e eventual modelo.
Donos e prazo: NÃO INFORMADO; não inventar responsáveis ou prometer duração.
Entregáveis: escopo, backlog com dependências, critérios de aceite e riscos.
Modo: SOMENTE PLANO; não gerar arquivos, criar recursos, instalar ou publicar.
```

**Saída e critérios de aceite.** Roadmap precisa mostrar decisões bloqueadas por contexto e não declarar projeto implantado. A resposta deve indicar o que foi apenas proposto e o que depende de dados/autorizações. Nenhum pedido acima autoriza execução neste turno.

**Acompanhamento preenchido.** “Separe a primeira entrega de diagnóstico de qualquer compromisso futuro de modelagem.” Reavalie o aceite após a resposta, sem assumir que a segunda tentativa está correta.

[Formulário e guia dos campos](../../../ambiente_fonte/.assistant/hub_prompts/novo_projeto/novo_projeto.md) · [Notebook de acompanhamento](../../../ambiente_fonte/.assistant/hub_prompts/novo_projeto/exemplo_novo_projeto.py).

<a id="passo-a-passo-operacional-do-briefing-ao-resultado"></a>

## 🛠️ Passo a Passo Operacional: Do Briefing ao Resultado

![Fluxo operacional do briefing à entrega](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/prompts/png/02_fluxo_operacional.png)

*Leitura da figura: seleção, preenchimento, contexto, revisão, execução e validação são etapas. A revisão humana é um portão, não o último cartão decorativo.*

1. Escolha o briefing pelo resultado principal. Fases misturadas → contratos separados.
2. Substitua placeholders. Sem segredos.
3. Anexe recursos (`@`, Add Context, `catalog.schema.table`, `@cell` se houver). `/findTables` localiza tabelas; `/eda` **não** é comando do Hub.
4. Revise o plano: `collect`, persistência, custo.
5. Valide contra o aceite. Registre resposta real no exemplo só se obtida e revisada.

**Se não funcionou.** Se a resposta não inspeciona o recurso, confira o contexto selecionado e a autorização. Exemplo: o modo “somente leitura” pode estar conflitando com o pedido de escrita — separe os chats. Skill errada: use `@` da tabela acima.

---

<a id="exemplo-de-interação-revisão-e-encerramento"></a>

### Exemplo de interação, revisão e encerramento

O encadeamento a seguir é **hipotético**: ensina a revisar, não relata conversa executada.

**Pedido inicial:** use o microbriefing de `data_quality` e selecione a preparação da campanha.

**Resposta com defeito:** “Vou testar id_cliente como PK e retornar metrics.row_count”. Isso viola o grão e a API: existem vários eventos por cliente e a chave de saída chama-se `checks`.

**Correção que você envia:** “Use event_id como chave candidata. Confira o módulo selecionado: quero checks.row_count e checks.nulls.canal.pct, não metrics. Reapresente apenas o plano; não execute.”

**Plano corrigido esperado:** chamada com `pk_columns=["event_id"]`, `date_column=None`, limites de 5 e 20; interpretação de um nulo em vinte como aviso, e política consumidora separada.

**Execução, em etapa distinta:** depois de revisar, autorize as células específicas no notebook da fixture. Compare com os asserts do guia de scripts. Só então registre saída real, data, código e recurso utilizados.

**Encerramento:** aceite depende do recurso correto, contrato correto, números conferidos e ausência de efeitos não autorizados. Registrar uma resposta não a torna automaticamente homologada. Quando a entrega muda para features, registre handoff e abra uma fase com novo contrato.

---

<a id="perguntas-frequentes-faq"></a>

## ❓ Perguntas Frequentes (FAQ)

<a id="1-por-que-preencher-um-briefing-estruturado-em-vez-de-apenas-fazer-uma-pergunta-livre"></a>

### 1. Por que preencher um briefing estruturado em vez de apenas fazer uma pergunta livre?

Porque o briefing torna explícitos dados, tempo e aceite. Facilita revisão; não impede erro.

<a id="2-o-que-preencher-quando-eu-não-souber-a-chave-primária-ou-a-granularidade"></a>

### 2. O que preencher quando eu não souber a chave primária ou a granularidade?

`NÃO INFORMADO` + inspeção. Não invente. Não deixe `{{chave}}`.

<a id="3-por-que-o-notebook-exemplo_py-não-executa-o-prompt-automaticamente"></a>

### 3. Por que o notebook `exemplo_*.py` não executa o prompt automaticamente?

Porque o prompt é interface conversacional. O notebook registra evidência.

<a id="4-quando-abrir-uma-conversa-nova"></a>

### 4. Quando abrir uma conversa nova?

Mudança material de objetivo, dados, fase ou skill recém-editada.

<a id="5-minha-equipe-pode-criar-novos-modelos-de-briefing"></a>

### 5. Minha equipe pode criar novos modelos de briefing?

Sim: pasta `<nome>/<nome>.md` + `exemplo_<nome>.py`. `@hub-ml-criar-objeto` orienta forma.

<a id="6-o-prompt-carrega-a-skill-e-os-helpers-automaticamente"></a>

### 6. O prompt carrega a skill e os helpers automaticamente?

O texto não registra uma automação. A skill pode ser selecionada por relevância ou `@`, e o agente pode executar imports/chamadas por ferramentas autorizadas. Contexto, carregamento e execução precisam de evidências distintas.

---

<a id="continue-explorando"></a>

## 🔗 Continue Explorando

- [Agent Skills](../sprint-05-skills/README.md)
- [Hub Snippets](../sprint-03-snippets/README.md)
- [Hub Scripts](../sprint-04-scripts/README.md)
- [Dicas oficiais](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [Funcionalidades da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/features-capabilities)
