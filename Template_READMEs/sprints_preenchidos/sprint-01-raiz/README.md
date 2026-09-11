![CRM — Missão Modelos Analíticos CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

<a id="ecossistemahub-assistant-para-databricks-genie-code-voltado-para-machine-learning"></a>

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

> Um ambiente integrado de governança, biblioteca algorítmica e inteligência contextual que ajuda a Genie Code e a equipe a trabalhar com métodos, componentes e critérios de revisão consistentes.

> **LEGENDA DE PROCEDÊNCIA.** Agent Skills e instruções são mecanismos reconhecidos pela Genie Code. Pastas com prefixo `hub_` e skills com prefixo `hub-` contêm implementações e convenções deste projeto; não são produtos institucionais da Databricks.

> **Rascunho de sprint 1 — não publicado.** Destino previsto: `README.md` na raiz do repositório.

---

<a id="mapa-de-leitura"></a>

## 🧭 Mapa de Leitura

Este documento apresenta o Hub: o que ele é, quais peças o formam, como o código chega ao workspace e como o projeto é mantido. Ele **não** ensina a importar um helper nem a preencher um briefing — isso fica nos guias de uso.

**O que você conseguirá fazer com este guia.** Ao terminar, você explica a função de cada componente, escolhe o guia certo para a próxima ação e sabe que a cópia editável não é a pasta do workspace.

Há duas rotas. A **primeira leitura** segue as seções na ordem: visão geral → componentes → arquitetura → contexto → manutenção. A **consulta** usa a tabela abaixo e salta para a âncora.

| Se você quer entender... | Continue em... |
|---|---|
| por que o ecossistema existe | [Visão Geral](#o-que-é-este-ecossistema-e-como-ele-ajuda-no-databricks) |
| quais componentes ele reúne | [Componentes](#o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho) |
| como repositório, workspace e runtime se relacionam | [Arquitetura](#arquitetura-completa-do-ecossistema) |
| como a Genie Code recebe contexto | [Fluxo de Contexto](#como-o-contexto-chega-ao-genie-code) |
| onde editar e o que não editar | [Manutenção](#como-o-projeto-é-mantido-sem-criar-duas-verdades) |

Se você já está no Databricks e quer executar a primeira tarefa, abra o [guia do `.assistant`](../sprint-02-assistant/README.md). Este README da raiz é o mapa; aquele é o tutorial de uso.

---

<a id="o-que-é-este-ecossistema-e-como-ele-ajuda-no-databricks"></a>

## 🌟 O que é este Ecossistema e como ele ajuda no Databricks?

Uma demanda analítica típica mistura várias coisas ao mesmo tempo: “olhe essa base da campanha e me diga se dá para modelar retenção”. Sem estrutura, o pedido deixa em aberto o grão da linha, a chave, o período, o que pode ser lido e o que não pode ser gravado. A Genie Code pode assumir informações indevidamente quando faltam dados; a equipe depois não consegue revisar o que foi assumido.

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
│   O código consumidor importa helpers quando forem adequados                    │
│   Você revisa código, execução, resultados e limitações                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

<a id="o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho"></a>

## 🧰 O que tem neste ambiente e como ele ajuda na rotina de trabalho?

O ecossistema tem cinco componentes de produto. Não são cinco nomes para a mesma coisa: mudam a entrada, a ação humana e o que acontece no runtime.

![Mapa visual dos cinco componentes do ecossistema .assistant](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/01_mapa_ecossistema.png)

*Leitura da figura: as conexões ao centro representam a organização do Hub, não uma esteira automática. Skills fornecem método, prompts delimitam o pedido e código é importado pelo consumidor. Na campanha, escolher EDA não executa o script de qualidade.*

A mesma demanda de campanha atravessa os cinco, com papéis distintos.

<a id="1-agent-skills-skills"></a>

### 🧠 1. Agent Skills (`skills/`)

**Necessidade.** Você quer um método (EDA, features, baseline), não só um parágrafo genérico.

**Conceito.** Agent Skill é um pacote de instruções com `SKILL.md`. A Genie Code pode carregá-lo por relevância da `description` ou você seleciona com `@nome-da-skill`.

**O que você faz.** Anexa a tabela da campanha e escreve, por exemplo, `@hub-ml-eda-profissional` pedindo plano somente leitura.

**Saída.** Metodologia, perguntas e, se autorizado, código proposto. A seleção da skill não equivale ao import: a chamada precisa acontecer no runtime, manualmente ou por ação autorizada do agente.

**Diferença.** Perto do prompt: a skill é método carregável; o prompt é o briefing que *você* preenche e cola.

<a id="2-hub-snippets-hub_snippets"></a>

### 📦 2. Hub Snippets (`hub_snippets/`)

**Necessidade.** Você não quer reescrever split temporal, PSI ou formatação brasileira.

**Conceito.** Snippet é módulo Python importável, com pasta de objeto (`__init__.py`, implementação, notebook de exemplo).

**O que você faz.** Coloca a raiz `.assistant` no `sys.path`, importa a função e chama com o DataFrame da campanha.

**Saída.** Objeto Python (DataFrame, número, figura), conforme o contrato.

**Diferença.** Perto do script: o snippet recebe dado já carregado; o script recebe o **endereço** do recurso a inspecionar.

<a id="3-hub-scripts-hub_scripts"></a>

### ⚡ 3. Hub Scripts (`hub_scripts/`)

**Necessidade.** Antes de modelar, você quer um diagnóstico: chave única? nulos? atualidade?

**Conceito.** Script do Hub é utilitário de inspeção. Lê e devolve evidência; não apaga tabela.

**O que você faz.** Importa `data_quality_check` e aponta para o nome da tabela. O notebook decide o que fazer com `pass` / `warn` / `fail`.

**Saída.** Dicionário com status, métricas e alertas.

**Diferença.** Perto do snippet: pergunta sobre um recurso identificado por nome, não transformação de um DataFrame que você já tem na memória.

<a id="4-hub-prompts-hub_prompts"></a>

### 📝 4. Hub Prompts (`hub_prompts/`)

**Necessidade.** O pedido vago gera hipóteses inventadas.

**Conceito.** Prompt do Hub é briefing preenchível. Não é slash command nem pasta descoberta pela plataforma.

**O que você faz.** Abre `eda_rapida.md`, substitui campos (ou `NÃO INFORMADO`) e cola no chat.

**Saída.** O texto do pedido, não um resultado de Spark.

**Diferença.** Perto da skill: o prompt é a ordem de serviço; a skill é o POP que a Genie pode carregar.

<a id="5-hub-padrões-hub_padroes"></a>

### 📐 5. Hub Padrões (`hub_padroes/`)

**Necessidade.** Um objeto novo não deve inventar formato.

**Conceito.** Padrão é molde (template + exemplo). Consulta manual ou skill `@hub-ml-criar-objeto`.

**O que você faz.** Escolhe o tipo, lê o template, preenche contrato e exemplo.

**Saída.** Estrutura; a correção do conteúdo continua humana.

**Diferença.** Não é biblioteca nem skill de análise: é fábrica de forma.

> **INFRAESTRUTURA EDITORIAL DO HUB.** A pasta `hub_readmes_visual_assets/` mantém SVG, PNG e cabeçalhos destes guias. Não é um sexto componente analítico, não é nativa da Databricks e não entra sozinha no contexto da Genie Code.

<a id="a-mesma-demanda-vista-por-cinco-componentes"></a>

### A mesma demanda vista por cinco componentes

| Componente | Papel na campanha fictícia |
|---|---|
| Prompt `eda_rapida` | declara tabela, chave e modo leitura |
| Skill `@hub-ml-eda-profissional` | organiza o método da exploração |
| Script `data_quality_check` | mede nulos e unicidade quando você executa |
| Snippet `split_temporal` | parte períodos de calendário se houver modelagem |
| Padrão | só entra se a equipe for **criar** um objeto novo |

---

<a id="arquitetura-completa-do-ecossistema"></a>

## 🏛️ Arquitetura Completa do Ecossistema

A fonte versionada, o workspace e o runtime não são a mesma cópia.

![Arquitetura do repositório ao runtime Databricks](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/02_arquitetura_ecossistema.png)

*Leitura da figura: o repositório controla a origem; o workspace disponibiliza o conteúdo; a Genie Code usa as camadas de contexto aplicáveis; o notebook importa e executa no runtime. Revisão humana liga as rotas.*

**Arquitetura**, aqui, é o percurso de um arquivo — não a lista de pastas da seção anterior.

<a id="o-que-este-diagrama-deixa-explícito"></a>

### O que este diagrama deixa explícito

Skills e instruções usam mecanismos de contexto da Genie Code. Prompts e padrões são fornecidos manualmente. Snippets e scripts só entram no Python quando o notebook importa. Estar dentro de `.assistant` **não** coloca o pacote no `sys.path`.

**Aplicação.** Se alguém “corrigir” um helper só no workspace, a próxima publicação da fonte apaga essa correção.

**Consequência.** Edite em `ambiente_fonte/`. O guia de uso no workspace é o README do `.assistant`.

<a id="ciclo-de-vida-do-projeto"></a>

### Ciclo de vida do projeto

![Ciclo de vida de uma mudança no ecossistema](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/03_ciclo_de_vida.png)

*Leitura da figura: editar, validar, renderizar, publicar, verificar e testar são gates complementares — um não substitui o outro.*

Uma correção em `ambiente_fonte/.assistant/README.md` exige validação de links. O README da raiz e `ambiente_fonte/README.md` permanecem no repositório: não são copiados pelo renderer. Uma mudança em `temporal_split` exige, além disso, testes e, se tocar runtime, smoke. Detalhes de comando estão em `ambiente_fonte/README.md` e no playbook de ciclo de vida.

---

<a id="como-o-contexto-chega-ao-genie-code"></a>

## 🔄 Como o Contexto chega ao Genie Code?

**Contexto** é a informação disponível para a tarefa. Não existe leitura automática de toda a pasta `.assistant`.

**Sem contexto:** “a campanha está boa?” — faltam tabela, chave e período; a resposta correta deve pedir esses dados, não inventá-los.

**Com contexto:** tabela anexada, `event_id`, `dt_evento` de janeiro a junho, somente leitura. As ambiguidades de recurso e tempo diminuem; as de negócio (o que é “boa”) continuam suas.

<a id="explicação-passo-a-passo"></a>

### Explicação Passo a Passo

1. **Gatilho.** No chat da Genie Code, descreva a demanda e o modo (explicar, planejar, gerar, executar).
2. **Diretrizes.** Instruções pessoais ou de workspace, quando existirem, valem nas superfícies suportadas — não em Quick Fix nem Autocomplete.
3. **Skill.** A plataforma pode carregar por relevância; `@hub-ml-*` explicita a escolha.
4. **Plano.** Confira dados, grão, custo e persistência **antes** de autorizar execução.
5. **Runtime.** O notebook configura o caminho, importa o helper e executa. Carregar a skill não realiza essas ações por si só; o agente pode realizá-las conforme as autorizações.
6. **Validação.** Separe código sugerido, código executado e resultado aceito.

**Erro comum.** Anexar o arquivo `.py` do helper e achar que ele já está importado. Anexo é contexto de leitura; import é ação no interpretador.

---

<a id="como-o-projeto-é-mantido-sem-criar-duas-verdades"></a>

## 🧭 Como o Projeto é Mantido sem Criar Duas Verdades

**Fonte canônica** é a cópia que se edita e se versiona: `ambiente_fonte/`. **Derivado** é o espelho gerado (`Novo_Ambiente_Simulado/`). **Cópia operacional** é o workspace.

Se duas pessoas “corrigirem” o mesmo texto, uma no Git e outra só no Databricks, a próxima publicação faz o workspace perder a correção local. Por isso a regra: edite na fonte; gere o derivado; publique; confira.

<a id="encontrei-um-problema-como-encaminhar-uma-correção"></a>

### Encontrei um problema: como encaminhar uma correção

| Tipo de problema | Onde alterar | O que conferir |
|---|---|---|
| Frase ou link de README | arquivo em `ambiente_fonte/` | validador de links |
| Comportamento de helper | módulo + exemplo + teste | suíte local; smoke se tocar Spark/ML |
| Roteamento de skill | `SKILL.md` (`name`/`description`) | forward tests |

Não edite o simulado à mão. Não grave host, e-mail ou token em arquivo versionado.

<a id="estado-verificável-do-gate-local"></a>

### Estado verificável do gate local

A validação local confronta estrutura, contratos e links. Para verificar os rascunhos desta rodada, execute também `python tools/review_readmes.py`. O bloco de referência abaixo recebe somente a saída de execução local registrada; não comprova Spark, chat, publicação ou aprovação editorial.

---

<a id="perguntas-frequentes-faq"></a>

## ❓ Perguntas Frequentes (FAQ)

<a id="1-o-que-acontece-quando-eu-abro-o-chat-da-genie-code-com-este-ecossistema-configurado"></a>

### 1. O que acontece quando eu abro o chat da Genie Code com este ecossistema configurado?

As instruções aplicáveis podem orientar a conversa, e uma skill pode ser carregada por relevância ou por `@`. Extensões `hub_` não entram automaticamente só por existirem na pasta. **Evidência de carregamento:** o registro da interface ou das ferramentas identifica a skill. Uma resposta que segue o método, isoladamente, não comprova carregamento. **Próximo passo:** se quiser um método específico, use `@`.

<a id="2-preciso-instalar-alguma-biblioteca-ou-configurar-o-python-para-usar-os-snippets"></a>

### 2. Preciso instalar alguma biblioteca ou configurar o Python para usar os snippets?

Depende do snippet. Módulos Python puros tendem a funcionar quando o `sys.path` aponta para a raiz que contém `hub_snippets/`. LightGBM, SHAP, Plotly, MLflow e o próprio Spark precisam existir no compute. Um `ImportError` nomeia o pacote que falta; não instale “tudo” por reflexo. Detalhes: [guia do `.assistant`](../sprint-02-assistant/README.md) e [Hub Snippets](../sprint-03-snippets/README.md).

<a id="3-qual-é-a-diferença-prática-entre-skill-prompt-snippet-e-script"></a>

### 3. Qual é a diferença prática entre Skill, Prompt, Snippet e Script?

Skill = método para a Genie. Prompt = briefing que você preenche. Snippet = implementação reutilizável, frequentemente sobre dados fornecidos pelo consumidor. Script = diagnóstico sobre um recurso endereçado. Na campanha: você preenche `eda_rapida`, menciona `@hub-ml-eda-profissional`, e só executa `data_quality_check` se autorizar código no notebook.

<a id="4-como-o-ecossistema-ajuda-a-mitigar-leakage-e-erros-analíticos"></a>

### 4. Como o ecossistema ajuda a mitigar leakage e erros analíticos?

Ele **orienta**: skills e prompts pedem instante de decisão, `pit_join` e `temporal_split` existem para recortes temporais explícitos. Isso não impede leakage se o pedido omitir a data de corte ou se o código for executado sem revisão. Guardrail textual não é barreira de plataforma.

<a id="5-a-equipe-pode-criar-novos-snippets-prompts-ou-skills"></a>

### 5. A equipe pode criar novos snippets, prompts ou skills?

Sim. Use [`hub_padroes/`](../sprint-08-padroes/README.md) e, se quiser, `@hub-ml-criar-objeto`. Criar arquivo é ação explícita, sujeita a revisão. Objeto novo de skill precisa de testes de roteamento.

<a id="6-se-o-código-foi-gerado-pela-genie-code-posso-executá-lo-sem-revisão"></a>

### 6. Se o código foi gerado pela Genie Code, posso executá-lo sem revisão?

Não. Planejar, gerar, executar e persistir são ações diferentes. Revise `CREATE`/`DELETE`/`MERGE`, coleta no driver e qualquer escrita. Autoaprovação reduz cliques; não é fronteira de segurança.

<a id="por-onde-começo-se-só-quero-usar"></a>

### Por onde começo se só quero usar?

[Guia do `.assistant`](../sprint-02-assistant/README.md), seção de ponto de partida.

<a id="preciso-dominar-todas-as-coleções"></a>

### Preciso dominar todas as coleções?

Não. Escolha o componente da demanda. Os outros guias existem para quando a pergunta mudar.

<a id="quem-mantém-o-código"></a>

### Quem mantém o código?

Quem edita `ambiente_fonte/`, valida, gera o derivado e publica. O workspace não é fonte.

---

<a id="próximos-passos"></a>

## 🔗 Próximos Passos

| Se você... | Abra | O que encontrará |
|---|---|---|
| vai usar o Hub no Databricks | [`.assistant/README.md`](../sprint-02-assistant/README.md) | escolha de componente, contexto, import e revisão |
| vai alterar o pacote | [`ambiente_fonte/README.md`](../sprint-07-ambiente-fonte/README.md) | fonte, derivado e comandos de validação |
| precisa de um helper | [Catálogo](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md) | demanda → caminho de import |
| precisa de vocabulário | [Glossário](../../../ambiente_fonte/.assistant/GLOSSARIO.md) | termos oficiais e locais |

---

<a id="saídas-de-referência-conferíveis"></a>

## Saídas de referência conferíveis

Este bloco registra a validação local da árvore candidata. As contagens pertencem ao snapshot indicado no registro da revisão, não a uma execução no workspace. Execute novamente após alterar arquivos; não corrija números para ocultar falhas.

<!-- REVIEW_GATE_START -->
```text
skills             : 13 · 13/13 com as 5 seções estruturais
prompts            : 16 · 161 campos com guia e contrato humano
helpers citados    : 81 caminhos verificados
markdown / links   : 113 arquivos / 210 links relativos
notebooks / links  : 78 notebooks / 17 links relativos
pastas de objeto   : 60 conferidas (nome, arquivos, __init__)
forma da pasta     : 58 conferidas (o módulo tem o nome da pasta)
contrato de dados  : 60 pares (saída: o que o notebook consome)
contrato de entrada: 57 pares (entrada: o que o notebook passa)
saída colada       : 77 notebooks com bloco real, 0 sem
idioma da docstring: 60 módulos, 0 com docstring em inglês
normas do molde    : 70 arquivos, 0 violação(ões)
notebook exercita  : 57 objetos, 0 notebook(s) que só importam
python (AST)       : 209 arquivos
instrucoes         : 8116/20000 caracteres
repo (identidade)  : 888 arquivos varridos no repositório editável/derivado
repo (links)       : 789 links fora da raiz analisada
APROVADO: 0 falha(s), 0 aviso(s)
```
<!-- REVIEW_GATE_END -->

A promoção final exige regenerar essa evidência no checkout que receber os READMEs e executar `python tools/ci_local.py`. A aprovação local não substitui os testes de runtime e de conversa adequados ao impacto.


<a id="fontes-de-plataforma-e-alcance"></a>

### Fontes de plataforma e alcance

[Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills), [instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions) e [modo agente e aprovações](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode), consultados em 11/09/2026. As convenções `hub_` e os limiares analíticos são locais. Os exemplos deste guia são sintéticos; uma saída esperada não é homologação do seu workspace.
