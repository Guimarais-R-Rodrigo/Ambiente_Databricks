![CRM — Missão Modelos Analíticos CRM](../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Hub Prompts — Briefings Técnicos Estruturados para Genie Code

O **Hub Prompts** reúne formulários para traduzir uma demanda analítica em pedido delimitado, rastreável e revisável.

> **CONTEÚDO CUSTOMIZADO PELO HUB · USO MANUAL.** `hub_prompts` não é pasta nativa descoberta ou executada pela Genie Code. Você escolhe o template, preenche e fornece o texto no chat.

> **Rascunho de sprint 6 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/hub_prompts/README.md`.

---

## 🧭 Neste Guia

Jornada: escolher → preencher → fornecer contexto → revisar → validar. O catálogo por família é consulta, não substitui essa jornada.

| Para entender... | Vá para... |
|---|---|
| por que usar um briefing estruturado | [O que é um Prompt Estruturado](#-o-que-é-um-prompt-estruturado) |
| como a pasta é organizada | [Anatomia da Pasta](#️-a-anatomia-de-uma-pasta-de-prompt) |
| como preencher sem inventar | [Disciplina dos Parâmetros](#-a-disciplina-dos-parâmetros-evitando-alucinações) |
| qual prompt escolher | [Catálogo Detalhado](#-catálogo-detalhado-de-prompts) |
| como conduzir a interação | [Passo a Passo Operacional](#️-passo-a-passo-operacional-do-briefing-ao-resultado) |
| dúvidas e limites | [Perguntas Frequentes](#-perguntas-frequentes-faq) |

---

## 🎯 O que é um Prompt Estruturado?

É uma **ordem de serviço**, não uma fórmula mágica.

**Pedido vago:** “analise a campanha.” Faltam tabela, grão, chave, período, o que pode gravar.

**Pedido melhorado, com motivo de cada acréscimo:**

- recurso anexado → a Genie não inventa a tabela;
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

## 🏗️ A Anatomia de uma Pasta de Prompt

```text
hub_prompts/eda_rapida/
├── eda_rapida.md              briefing preenchível
└── exemplo_eda_rapida.py      notebook de acompanhamento
```

![Anatomia de um briefing técnico forte](../hub_readmes_visual_assets/readmes/prompts/png/03_anatomia_briefing.png)

*Leitura da figura: objetivo e contexto delimitam o problema; restrições controlam a operação; entrega e aceite dizem quando está pronto. O template copiável continua sendo o `.md`.*

### 1. O Arquivo Markdown (`<nome>.md`)

Leia para saber quando usar. Copie a seção de prompt preenchida para o chat. Abrir o arquivo **não** envia nada à Genie.

Contém, em geral: quando usar / não usar, guia de cada campo, prompt para preencher, o que conferir na resposta.

### 2. O Notebook de Acompanhamento (`exemplo_<nome>.py`)

Três partes: preparo sintético, prompt preenchido, espaço para registrar resposta **real**. Enquanto a parte 3 estiver vazia, o notebook **não** homologa o prompt conversacionalmente. Não execute o `.md` a partir do notebook — não há essa automação.

### 3. Exemplo de briefing completamente preenchido

Cenário: decidir se eventos de campanha (sintéticos ou tabela autorizada) servem a um estudo mensal de retenção.

```text
Quero realizar uma EDA rápida da tabela anexada `catalogo.analytics.customer_events`.

Objetivo:
- decidir se a base está apta para análise mensal de retenção;
- identificar bloqueios de qualidade antes das métricas.

Contexto:
- grão esperado: um evento de cliente por linha;
- chave candidata: event_id;
- entidade: customer_id;
- coluna temporal: event_timestamp;
- período: 2026-01-01 a 2026-06-30;
- filtro: event_status = 'valid';
- regras adicionais: NÃO INFORMADO — pergunte antes de assumir.

Modo de trabalho:
- somente leitura;
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

Substitua o identificador da tabela pelo recurso que você **anexou**. A resposta da Genie a este texto é ilustração até você colá-la na parte 3 do exemplo e revisar.

---

## 🧩 A Disciplina dos Parâmetros: Evitando Alucinações

Três convenções (humanas, não travas da plataforma):

| Marca | Significado | Exemplo |
|---|---|---|
| Valor concreto | confirmado | `event_id` |
| `NÃO INFORMADO` | desconhecido agora | peça inspeção ou pergunta |
| `NÃO APLICÁVEL` | avaliado e não cabe | tabela estática sem eixo tempo |

Não envie `{{...}}` vazio.

### O contexto mínimo que evita retrabalho

Objetivo, recursos, grão e chaves, tempo, regras, restrições, entrega, aceite. Faltar um deles é o que costuma gerar hipótese silenciosa.

**Aplicação.** Sem `dt_evento`, a Genie pode misturar eventos futuros à feature. Marque `NÃO INFORMADO` em vez de inventar o nome da coluna.

---

## 🔄 A Sinergia Triangular: Prompts, Skills e Helpers

O briefing define o problema; a skill, se carregada, organiza o método; o helper executa só no notebook.

Na campanha: `eda_rapida` + `@hub-ml-eda-profissional` +, se autorizado, `data_quality_check`. Três interfaces, três ações suas.

---

## 📂 Famílias Funcionais de Prompts

![Mapa das famílias de briefing](../hub_readmes_visual_assets/readmes/prompts/png/01_mapa_familias.png)

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

## 📖 Catálogo Detalhado de Prompts

Cada item: o que faz, skill recomendada (não automática), o que informar, cenário, arquivos.

### Exploração

**`eda_rapida`** — perfil preliminar. `@hub-ml-eda-profissional`. Informar recurso, objetivo, chave, tempo, filtros, limite. `hub_prompts/eda_rapida/`.

**`eda_completa`** — univariada/bivariada. Mesma skill. Informar target e segmentos se houver.

**`cross_eda`** — chaves e join. `@hub-ml-cross-eda-ml`.

### Modelagem, safras e estatística

**`safra`** — `@hub-ml-analise-safra`. Coorte, MOB, denominador, censura.

**`stat_check`** — `@hub-ml-validacao-estatistica`. Hipótese, teste, efeito.

**`feature_engineering`** — `@hub-ml-feature-engineering`. Data de decisão, janelas.

**`baseline_orchestration`** — `@hub-ml-baseline-ml`. População, split, métrica.

**`pipeline`** — `@hub-ml-pipeline-builder`. Camadas, incrementalidade.

**`explainability`** — `@hub-ml-explainability`. Público e limite da explicação.

**`monitoramento_modelo`** — `@hub-ml-monitoramento-modelo`. Referência, atual, o que fazer com o alerta.

### Qualidade e auditoria

**`data_quality`** — regras de integridade. Frequentemente `@hub-ml-eda-profissional`.

**`comparar_tabelas`** — reconciliação. Genie ou `@hub-ml-cross-eda-ml`.

**`auditoria_skills`** — `@hub-ml-auditoria-skills`. Confronta pedido, código e evidência.

### Documentação e onboarding

**`comentar_notebook`** — `@hub-ml-comentar-notebook`.

**`tutor_explicar`** — `@hub-ml-tutor-databricks`.

**`novo_projeto`** — kick-off; skill especializada só depois da natureza da entrega.

---

## 🛠️ Passo a Passo Operacional: Do Briefing ao Resultado

![Fluxo operacional do briefing à entrega](../hub_readmes_visual_assets/readmes/prompts/png/02_fluxo_operacional.png)

*Leitura da figura: seleção, preenchimento, contexto, revisão, execução e validação são etapas. A revisão humana é um portão, não o último cartão decorativo.*

1. Escolha o briefing pelo resultado principal. Fases misturadas → contratos separados.
2. Substitua placeholders. Sem segredos.
3. Anexe recursos (`@`, Add Context, `catalog.schema.table`, `@cell` se houver). `/findTables` localiza tabelas; `/eda` **não** é comando do Hub.
4. Revise o plano: `collect`, persistência, custo.
5. Valide contra o aceite. Registre resposta real no exemplo só se obtida e revisada.

**Se não funcionou.** Prompt recusou-se a inspecionar: o modo “somente leitura” pode estar conflitando com o pedido de escrita — separe os chats. Skill errada: use `@` da tabela acima.

---

## ❓ Perguntas Frequentes (FAQ)

### 1. Por que não só uma pergunta livre?

Porque o briefing torna explícitos dados, tempo e aceite. Facilita revisão; não impede erro.

### 2. Não sei a chave?

`NÃO INFORMADO` + inspeção. Não invente. Não deixe `{{chave}}`.

### 3. Por que o `exemplo_*.py` não dispara o chat?

Porque o prompt é interface conversacional. O notebook registra evidência.

### 4. Quando abrir conversa nova?

Mudança material de objetivo, dados, fase ou skill recém-editada.

### 5. Podemos criar briefing novo?

Sim: pasta `<nome>/<nome>.md` + `exemplo_<nome>.py`. `@hub-ml-criar-objeto` orienta forma.

### 6. O prompt carrega skill e helpers?

Não. Skill por relevância ou `@`. Helper por import.

---

## 🔗 Continue Explorando

- [Agent Skills](../skills/README.md)
- [Hub Snippets](../hub_snippets/README.md)
- [Hub Scripts](../hub_scripts/README.md)
- [Dicas oficiais](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips)
- [Funcionalidades da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/features-capabilities)
