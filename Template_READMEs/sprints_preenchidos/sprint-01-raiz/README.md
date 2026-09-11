![CRM — Missão Modelos Analíticos CRM](ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

> Um ambiente integrado de governança, biblioteca algorítmica e inteligência contextual que ajuda a Genie Code e a equipe a trabalhar com métodos, componentes e critérios de revisão consistentes.

> **LEGENDA DE PROCEDÊNCIA.** Agent Skills e instruções são mecanismos reconhecidos pela Genie Code. Pastas com prefixo `hub_` e skills com prefixo `hub-` contêm implementações e convenções deste projeto; não são produtos institucionais da Databricks.

> **Rascunho de sprint 1 — não publicado.** Destino previsto: `README.md` na raiz do repositório.

---

## 🧭 Mapa de Leitura

Este documento apresenta o Hub: o que ele é, quais peças o formam, como o código chega ao workspace e como o projeto é mantido. Ele **não** ensina a importar um helper nem a preencher um briefing — isso fica nos guias de uso.

**O que você conseguirá fazer com este guia.** Ao terminar, você explica a função de cada componente, escolhe o guia certo para a próxima ação e sabe que a cópia editável não é a pasta do workspace.

Há duas rotas. A **primeira leitura** segue as seções na ordem: visão geral → componentes → arquitetura → contexto → manutenção. A **consulta** usa a tabela abaixo e salta para a âncora.

| Se você quer entender... | Continue em... |
|---|---|
| por que o ecossistema existe | [Visão Geral](#-o-que-é-este-ecossistema-e-como-ele-ajuda-no-databricks) |
| quais componentes ele reúne | [Componentes](#-o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho) |
| como repositório, workspace e runtime se relacionam | [Arquitetura](#️-arquitetura-completa-do-ecossistema) |
| como a Genie Code recebe contexto | [Fluxo de Contexto](#-como-o-contexto-chega-ao-genie-code) |
| onde editar e o que não editar | [Manutenção](#-como-o-projeto-é-mantido-sem-criar-duas-verdades) |

Se você já está no Databricks e quer executar a primeira tarefa, abra o [guia do `.assistant`](ambiente_fonte/.assistant/README.md). Este README da raiz é o mapa; aquele é o tutorial de uso.

---

## 🌟 O que é este Ecossistema e como ele ajuda no Databricks?

Uma demanda analítica típica mistura várias coisas ao mesmo tempo: “olhe essa base da campanha e me diga se dá para modelar retenção”. Sem estrutura, o pedido deixa em aberto o grão da linha, a chave, o período, o que pode ser lido e o que não pode ser gravado. A Genie Code preenche lacunas; a equipe depois não consegue revisar o que foi assumido.

**Ecossistema**, neste projeto, é o conjunto organizado de instruções, métodos, briefings e código Python que acompanha esse trabalho no Databricks Genie Code. Ele não substitui permissão, teste nem decisão de negócio.

Três momentos da mesma campanha fictícia:

1. **Pedido incompleto:** “analise a campanha”. Faltam tabela, chave, período e modo de trabalho.
2. **Contexto estruturado:** briefing com recurso, `event_id`, `dt_evento` e leitura apenas.
3. **Resultado revisável:** plano, código e números com origem; a pessoa aceita ou recusa.

O Hub reduz improvisação. Ele não torna a IA infalível.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ROTINA DO TRABALHO ANALÍTICO                      │
│                                                                             │
│   Você descreve objetivo, dados, restrições e entrega                       │
│   A skill organiza método, perguntas e guardrails                           │
│   O notebook importa helpers quando eles forem adequados                    │
│   Você revisa código, execução, resultados e limitações                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧰 O que tem neste ambiente e como ele ajuda na rotina de trabalho?

O ecossistema tem cinco componentes de produto. Não são cinco nomes para a mesma coisa: mudam a entrada, a ação humana e o que acontece no runtime.

![Mapa visual dos cinco componentes do ecossistema .assistant](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/01_mapa_ecossistema.png)

*Leitura da figura: as Agent Skills usam um mecanismo reconhecido pela plataforma; prompts, snippets, scripts e padrões são extensões customizadas do Hub. A via contínua é descoberta nativa; a via tracejada exige ação sua.*

A mesma demanda de campanha atravessa os cinco, com papéis distintos.

### 🧠 1. Agent Skills (`skills/`)

**Necessidade.** Você quer um método (EDA, features, baseline), não só um parágrafo genérico.

**Conceito.** Agent Skill é um pacote de instruções com `SKILL.md`. A Genie Code pode carregá-lo por relevância da `description` ou você seleciona com `@nome-da-skill`.

**O que você faz.** Anexa a tabela da campanha e escreve, por exemplo, `@hub-ml-eda-profissional` pedindo plano somente leitura.

**Saída.** Metodologia, perguntas e, se autorizado, código proposto. A skill **não** importa `hub_snippets` sozinha.

**Diferença.** Perto do prompt: a skill é método carregável; o prompt é o briefing que *você* preenche e cola.

### 📦 2. Hub Snippets (`hub_snippets/`)

**Necessidade.** Você não quer reescrever split temporal, PSI ou formatação brasileira.

**Conceito.** Snippet é módulo Python importável, com pasta de objeto (`__init__.py`, implementação, notebook de exemplo).

**O que você faz.** Coloca a raiz `.assistant` no `sys.path`, importa a função e chama com o DataFrame da campanha.

**Saída.** Objeto Python (DataFrame, número, figura), conforme o contrato.

**Diferença.** Perto do script: o snippet recebe dado já carregado; o script recebe o **endereço** do recurso a inspecionar.

### ⚡ 3. Hub Scripts (`hub_scripts/`)

**Necessidade.** Antes de modelar, você quer um diagnóstico: chave única? nulos? atualidade?

**Conceito.** Script do Hub é utilitário de inspeção. Lê e devolve evidência; não apaga tabela.

**O que você faz.** Importa `data_quality_check` e aponta para o nome da tabela. O notebook decide o que fazer com `pass` / `warn` / `fail`.

**Saída.** Dicionário com status, métricas e alertas.

**Diferença.** Perto do snippet: pergunta sobre um recurso identificado por nome, não transformação de um DataFrame que você já tem na memória.

### 📝 4. Hub Prompts (`hub_prompts/`)

**Necessidade.** O pedido vago gera hipóteses inventadas.

**Conceito.** Prompt do Hub é briefing preenchível. Não é slash command nem pasta descoberta pela plataforma.

**O que você faz.** Abre `eda_rapida.md`, substitui campos (ou `NÃO INFORMADO`) e cola no chat.

**Saída.** O texto do pedido, não um resultado de Spark.

**Diferença.** Perto da skill: o prompt é a ordem de serviço; a skill é o POP que a Genie pode carregar.

### 📐 5. Hub Padrões (`hub_padroes/`)

**Necessidade.** Um objeto novo não deve inventar formato.

**Conceito.** Padrão é molde (template + exemplo). Consulta manual ou skill `@hub-ml-criar-objeto`.

**O que você faz.** Escolhe o tipo, lê o template, preenche contrato e exemplo.

**Saída.** Estrutura; a correção do conteúdo continua humana.

**Diferença.** Não é biblioteca nem skill de análise: é fábrica de forma.

> **INFRAESTRUTURA EDITORIAL DO HUB.** A pasta `hub_readmes_visual_assets/` mantém SVG, PNG e cabeçalhos destes guias. Não é um sexto componente analítico, não é nativa da Databricks e não entra sozinha no contexto da Genie Code.

### A mesma demanda vista por cinco componentes

| Componente | Papel na campanha fictícia |
|---|---|
| Prompt `eda_rapida` | declara tabela, chave e modo leitura |
| Skill `@hub-ml-eda-profissional` | organiza o método da exploração |
| Script `data_quality_check` | mede nulos e unicidade quando você executa |
| Snippet `split_temporal` | parte períodos de calendário se houver modelagem |
| Padrão | só entra se a equipe for **criar** um objeto novo |

---

## 🏛️ Arquitetura Completa do Ecossistema

A fonte versionada, o workspace e o runtime não são a mesma cópia.

![Arquitetura do repositório ao runtime Databricks](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/02_arquitetura_ecossistema.png)

*Leitura da figura: o repositório controla a origem; o workspace disponibiliza o conteúdo; a Genie Code usa as camadas de contexto aplicáveis; o notebook importa e executa no runtime. Revisão humana liga as rotas.*

**Arquitetura**, aqui, é o percurso de um arquivo — não a lista de pastas da seção anterior.

### O que este diagrama deixa explícito

Skills e instruções usam mecanismos de contexto da Genie Code. Prompts e padrões são fornecidos manualmente. Snippets e scripts só entram no Python quando o notebook importa. Estar dentro de `.assistant` **não** coloca o pacote no `sys.path`.

**Aplicação.** Se alguém “corrigir” um helper só no workspace, a próxima publicação da fonte apaga essa correção.

**Consequência.** Edite em `ambiente_fonte/`. O guia de uso no workspace é o README do `.assistant`.

### Ciclo de vida do projeto

![Ciclo de vida de uma mudança no ecossistema](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/03_ciclo_de_vida.png)

*Leitura da figura: editar, validar, renderizar, publicar, verificar e testar são gates complementares — um não substitui o outro.*

Uma correção na frase de um README exige validação de links. Uma mudança em `temporal_split` exige, além disso, testes e, se tocar runtime, smoke. Detalhes de comando estão em `ambiente_fonte/README.md` e no playbook de ciclo de vida.

---

## 🔄 Como o Contexto chega ao Genie Code?

**Contexto** é a informação disponível para a tarefa. Não existe leitura automática de toda a pasta `.assistant`.

**Sem contexto:** “a campanha está boa?” — a Genie precisa inventar tabela, chave e período.

**Com contexto:** tabela anexada, `event_id`, `dt_evento` de janeiro a junho, somente leitura. As ambiguidades de recurso e tempo diminuem; as de negócio (o que é “boa”) continuam suas.

### Explicação Passo a Passo

1. **Gatilho.** No chat da Genie Code, descreva a demanda e o modo (explicar, planejar, gerar, executar).
2. **Diretrizes.** Instruções pessoais ou de workspace, quando existirem, valem nas superfícies suportadas — não em Quick Fix nem Autocomplete.
3. **Skill.** A plataforma pode carregar por relevância; `@hub-ml-*` explicita a escolha.
4. **Plano.** Confira dados, grão, custo e persistência **antes** de autorizar execução.
5. **Runtime.** O notebook configura o caminho, importa o helper e executa. A skill não faz isso sozinha.
6. **Validação.** Separe código sugerido, código executado e resultado aceito.

**Erro comum.** Anexar o arquivo `.py` do helper e achar que ele já está importado. Anexo é contexto de leitura; import é ação no interpretador.

---

## 🧭 Como o Projeto é Mantido sem Criar Duas Verdades

**Fonte canônica** é a cópia que se edita e se versiona: `ambiente_fonte/`. **Derivado** é o espelho gerado (`Novo_Ambiente_Simulado/`). **Cópia operacional** é o workspace.

Se duas pessoas “corrigirem” o mesmo texto, uma no Git e outra só no Databricks, a próxima publicação faz o workspace perder a correção local. Por isso a regra: edite na fonte; gere o derivado; publique; confira.

### Encontrei um problema: como encaminhar uma correção

| Tipo de problema | Onde alterar | O que conferir |
|---|---|---|
| Frase ou link de README | arquivo em `ambiente_fonte/` | validador de links |
| Comportamento de helper | módulo + exemplo + teste | suíte local; smoke se tocar Spark/ML |
| Roteamento de skill | `SKILL.md` (`name`/`description`) | forward tests |

Não edite o simulado à mão. Não grave host, e-mail ou token em arquivo versionado.

### Estado verificável do gate local

O bloco de saídas no final deste README existe para o comando `python tools/validate_assistant.py --conferir-readme` detectar documentação envelhecida. Os números são da última consolidação colada; se divergirem da execução, atualize o bloco com a saída real — não o contrário.

---

## ❓ Perguntas Frequentes (FAQ)

### 1. O que acontece quando eu abro o chat da Genie Code com este ecossistema configurado?

As instruções aplicáveis podem orientar a conversa, e uma skill pode ser carregada por relevância ou por `@`. Extensões `hub_` não entram automaticamente só por existirem na pasta. **Sinal:** a skill aparece como carregada, ou o assistente segue o método sem tê-la selecionado. **Próximo passo:** se quiser um método específico, use `@`.

### 2. Preciso instalar alguma biblioteca ou configurar o Python para usar os snippets?

Depende do snippet. Módulos Python puros tendem a funcionar quando o `sys.path` aponta para a raiz que contém `hub_snippets/`. LightGBM, SHAP, Plotly, MLflow e o próprio Spark precisam existir no compute. Um `ImportError` nomeia o pacote que falta; não instale “tudo” por reflexo. Detalhes: [guia do `.assistant`](ambiente_fonte/.assistant/README.md) e [Hub Snippets](ambiente_fonte/.assistant/hub_snippets/README.md).

### 3. Qual é a diferença prática entre Skill, Prompt, Snippet e Script?

Skill = método para a Genie. Prompt = briefing que você preenche. Snippet = função importável sobre dado já carregado. Script = diagnóstico sobre um recurso endereçado. Na campanha: você preenche `eda_rapida`, menciona `@hub-ml-eda-profissional`, e só executa `data_quality_check` se autorizar código no notebook.

### 4. Como o ecossistema ajuda a mitigar leakage e erros analíticos?

Ele **orienta**: skills e prompts pedem instante de decisão, `pit_join` e `temporal_split` existem para recortes temporais explícitos. Isso não impede leakage se o pedido omitir a data de corte ou se o código for executado sem revisão. Guardrail textual não é barreira de plataforma.

### 5. A equipe pode criar novos snippets, prompts ou skills?

Sim. Use [`hub_padroes/`](ambiente_fonte/.assistant/hub_padroes/README.md) e, se quiser, `@hub-ml-criar-objeto`. Criar arquivo é ação explícita, sujeita a revisão. Objeto novo de skill precisa de testes de roteamento.

### 6. Se o código foi gerado pela Genie Code, posso executá-lo sem revisão?

Não. Planejar, gerar, executar e persistir são ações diferentes. Revise `CREATE`/`DELETE`/`MERGE`, coleta no driver e qualquer escrita. Autoaprovação reduz cliques; não é fronteira de segurança.

### Por onde começo se só quero usar?

[Guia do `.assistant`](ambiente_fonte/.assistant/README.md), seção de ponto de partida.

### Preciso dominar todas as coleções?

Não. Escolha o componente da demanda. Os outros guias existem para quando a pergunta mudar.

### Quem mantém o código?

Quem edita `ambiente_fonte/`, valida, gera o derivado e publica. O workspace não é fonte.

---

## 🔗 Próximos Passos

| Se você... | Abra | O que encontrará |
|---|---|---|
| vai usar o Hub no Databricks | [`.assistant/README.md`](ambiente_fonte/.assistant/README.md) | escolha de componente, contexto, import e revisão |
| vai alterar o pacote | [`ambiente_fonte/README.md`](ambiente_fonte/README.md) | fonte, derivado e comandos de validação |
| precisa de um helper | [Catálogo](ambiente_fonte/.assistant/CATALOGO_HELPERS.md) | demanda → caminho de import |
| precisa de vocabulário | [Glossário](ambiente_fonte/.assistant/GLOSSARIO.md) | termos oficiais e locais |

---

## Saídas de referência conferíveis

Estas linhas permitem que `validate_assistant.py --conferir-readme` detecte documentação envelhecida. Recoloque a saída real ao consolidar a release; não invente o número.

```text
(use a saída atual de python tools/validate_assistant.py)
```
