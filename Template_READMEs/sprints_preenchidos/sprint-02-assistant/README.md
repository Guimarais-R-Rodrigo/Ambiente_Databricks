![CRM — Missão Modelos Analíticos CRM](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

<a id="ecossistemahub-assistant-para-databricks-genie-code-voltado-para-machine-learning"></a>

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

> Um ambiente integrado de instruções, habilidades, bibliotecas e briefings que ajuda a transformar a Genie Code em uma parceira contextualizada para a rotina analítica.

> **LEGENDA DE PROCEDÊNCIA.** Agent Skills e instruções são mecanismos nativos suportados pela Genie Code. Os componentes `hub_prompts`, `hub_snippets`, `hub_scripts`, `hub_padroes` e o conteúdo das skills `hub-ml-*` foram criados neste projeto e possuem ativação própria.

> **Rascunho de sprint 2 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/README.md`.

---

<a id="mapa-de-uso"></a>

## 🧭 Mapa de Uso

Este documento acompanha a **utilização no workspace**: escolher o componente, fornecer contexto, revisar a proposta, executar um helper autorizado e ler o resultado. Ele não ensina a publicar o repositório.

**Antes da primeira tarefa.** Você precisa de acesso ao workspace, de um notebook Python e de permissão de leitura sobre os dados que for anexar. Termos que aparecem a seguir:

- **Notebook:** arquivo de células no Databricks.
- **Célula:** bloco de código ou Markdown.
- **DataFrame:** estrutura tabular. Em pandas os dados ficam no processo; em Spark, o objeto representa também um plano de operações distribuídas e pode ainda não ter sido materializado.
- **Helper:** função ou classe dos pacotes `hub_snippets` / `hub_scripts`.
- **Runtime:** o interpretador e o compute onde o código de fato roda.

| Se você quer... | Continue em... |
|---|---|
| conhecer o propósito do Hub | [Visão Geral](#o-que-é-este-ecossistema-e-como-ele-ajuda-no-databricks) |
| escolher entre skill, prompt, snippet e script | [Componentes](#o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho) |
| entender o que é automático ou manual | [Arquitetura](#arquitetura-completa-do-ecossistema) |
| fornecer contexto corretamente | [Fluxo de Contexto](#como-o-contexto-chega-ao-genie-code) |
| iniciar uma tarefa concreta | [Ponto de Partida](#como-escolher-o-ponto-de-partida) |
| conferir runtime, dependências e segurança | [Compute e Segurança](#dependências-compute-e-segurança) |

**Primeira utilização:** leia a visão geral, a bússola de escolha e o exemplo “conhecer uma tabela nova”. **Consulta:** use a tabela. **Problema:** vá ao FAQ e a “Se não funcionou”.

---

<a id="o-que-é-este-ecossistema-e-como-ele-ajuda-no-databricks"></a>

## 🌟 O que é este Ecossistema e como ele ajuda no Databricks?

Você recebeu uma base de campanha e precisa saber se pode usá-la. Há três superfícies diferentes:

1. **Conversa** na Genie Code — pede plano, código, explicação.
2. **Arquivos** em `.assistant/` — skills, briefings, módulos.
3. **Execução** no notebook — ocorre quando código é executado por uma célula, tarefa ou ferramenta autorizada do agente.

O Hub organiza as duas primeiras e oferece código para a terceira. Ele não executa análise só porque a pasta existe.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ROTINA DO CIENTISTA DE DADOS                      │
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

![Mapa visual dos cinco componentes do ecossistema .assistant](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/01_mapa_ecossistema.png)

*Leitura da figura: cada componente tem responsabilidade e forma de ativação. Skills podem ser descobertas; o restante exige anexo, import ou consulta.*

Todos os exemplos abaixo usam a campanha fictícia com `event_id`, `id_cliente` e `dt_evento`.

<a id="1-agent-skills-skills"></a>

### 🧠 1. Agent Skills (`skills/`)

Pacotes `SKILL.md` no padrão Agent Skills. **Quando abrir:** você quer o método de EDA, features, baseline. **O que informar:** tabela, grão, período, modo de trabalho. **O que esperar:** plano e, se autorizado, código. **Não esperar:** import automático de helper.

<a id="2-hub-snippets-hub_snippets"></a>

### 📦 2. Hub Snippets (`hub_snippets/`)

Biblioteca Python. **Quando abrir:** você já tem um DataFrame e quer uma função (split, PSI, formatação). **O que fazer:** `sys.path` + `import` + chamada. **O que esperar:** retorno tipado. Snippet ≠ script: aqui o dado já está carregado.

<a id="3-hub-scripts-hub_scripts"></a>

### ⚡ 3. Hub Scripts (`hub_scripts/`)

Diagnósticos. **Quando abrir:** a pergunta é sobre uma **tabela ou arquivo** identificado por nome. **O que fazer:** importar e passar `table_name`. **O que esperar:** dicionário ou DataFrame de evidência; o notebook decide parar ou seguir.

<a id="4-hub-prompts-hub_prompts"></a>

### 📝 4. Hub Prompts (`hub_prompts/`)

Briefings. **Quando abrir:** o pedido ainda está vago. **O que fazer:** preencher o `.md` e colar no chat. **O que esperar:** melhor especificação, não um job Spark.

<a id="5-hub-padrões-hub_padroes"></a>

### 📐 5. Hub Padrões (`hub_padroes/`)

Moldes. **Quando abrir:** você vai **criar** objeto novo. Não use na exploração da campanha.

> `hub_readmes_visual_assets/` é infraestrutura editorial. Não é componente analítico.

---

<a id="arquitetura-completa-do-ecossistema"></a>

## 🏛️ Arquitetura Completa do Ecossistema

Há duas rotas: **contexto para a conversa** e **código para o runtime**. Uma menção no texto da skill não é um `import`.

![Arquitetura de uso do ecossistema no workspace](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/assistant/png/02_arquitetura_de_uso.png)

*Leitura da figura: instruções, skills e briefing orientam o chat; snippets e scripts entram só na execução do notebook. A revisão humana liga as duas rotas.*

<a id="o-que-acontece-automaticamente-e-o-que-depende-de-você"></a>

### O que acontece automaticamente e o que depende de você

| Componente | Pode chegar ao contexto sozinho? | Exige ação explícita? |
|---|---:|---:|
| instruções pessoais e de workspace | nas superfícies suportadas | configuração |
| `AGENTS.md` / `CLAUDE.md` | hierarquia do arquivo aberto | posicionamento no projeto |
| Agent Skill | por relevância | `@` para seleção explícita |
| Hub Prompt | não | preencher e fornecer |
| Hub Snippet / Script | não | path, import, executar |
| Hub Padrão | não | consultar ou anexar |

Instruções não se aplicam a Quick Fix nem Autocomplete. Autoaprovação reduz confirmações; não amplia ACL.

**Aplicação à campanha.** Anexar `eda_rapida.md` não roda qualidade de dados. Executar `data_quality_check` no notebook, sim.

| Ação | Onde | Resultado observável | O que ainda não aconteceu |
|---|---|---|---|
| `@hub-ml-eda-profissional` | chat | skill carregada | nenhum Spark |
| colar briefing | chat | pedido delimitado | nenhum import |
| `import data_quality_check` | célula | módulo no processo | nenhuma métrica |
| chamar a função | célula | dicionário `status` | política de parar o job |

---

<a id="como-o-contexto-chega-ao-genie-code"></a>

## 🔄 Como o Contexto chega ao Genie Code?

A Genie Code não “lê a pasta inteira”. Você monta o pedido.

![Fluxo do contexto à execução revisada](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/assistant/png/03_contexto_e_execucao.png)

*Leitura da figura: a proposta passa por revisão antes da execução e termina em evidências conferidas.*

<a id="explicação-passo-a-passo"></a>

### Explicação Passo a Passo

1. **Gatilho.** No chat, diga o objetivo e o modo: “somente leitura; mostre o plano antes”.
2. **Contexto.** Use `@` ou Add Context para tabela, notebook ou célula (`@cell` quando a interface oferecer). Prefira `catalog.schema.table`.
3. **Diretrizes e skill.** `@hub-ml-eda-profissional` se quiser o método explícito.
4. **Plano.** Confira filtros, período, `collect` e escrita.
5. **Helpers.** Se o plano citar um módulo, o notebook ainda precisa importá-lo.
6. **Execução.** Permissões do seu usuário continuam valendo.
7. **Validação.** Fato versus hipótese; origem dos números.

**Adaptação.** Se não souber a chave, escreva `NÃO INFORMADO` e peça inspeção do schema — não invente `id_cliente`.

**Erro comum.** Continuar num chat antigo depois de editar a skill. Abra conversa nova; se a descrição antiga persistir, atualize a página.

---

<a id="como-escolher-o-ponto-de-partida"></a>

## 🧭 Como Escolher o Ponto de Partida

![Árvore de escolha do componente mais adequado](../../../ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/assistant/png/01_escolha_ponto_de_partida.png)

*Leitura da figura: o objetivo do momento indica skill, prompt, snippet, script ou padrão — não os cinco ao mesmo tempo.*

<a id="exemplo-conhecer-uma-tabela-nova"></a>

### Exemplo: conhecer uma tabela nova

**Cenário.** Você recebeu eventos de campanha e precisa saber se a base está utilizável.

**Preparar.** Notebook Python no workspace, com a pasta `.assistant` acessível. Não use uma tabela corporativa inexistente neste tutorial: crie 20 linhas sintéticas.

**Dados.** 20 eventos, chave `event_id` única, um nulo em `canal` (coluna não chave). Proporção de nulos em `canal`: 1/20 = 5%.

```python
from pathlib import Path
import sys
from datetime import date, timedelta

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()

linhas = [
    (f"e{i:02d}", f"c{i % 5:02d}", date(2026, 6, 1) + timedelta(days=i),
     None if i == 0 else "email", i % 2, float(i))
    for i in range(20)
]
df = spark.createDataFrame(
    linhas, ["event_id", "id_cliente", "dt_evento", "canal", "respondeu", "valor_gasto"]
)
df.createOrReplaceTempView("vw_campanha_eventos_sintetica")
assert spark.table("vw_campanha_eventos_sintetica").count() == 20
```

Substitua `<username>` pelo diretório do seu usuário no workspace.

**Pedir (chat, ilustração — não é execução certificada):**

```text
@hub-ml-eda-profissional

Quero apenas um plano de diagnóstico da view temporária vw_campanha_eventos_sintetica, criada na sessão Spark deste notebook. Não execute código. Selecionei a célula de preparação e o schema no contexto; se você não os recebeu, peça-os.
Grão esperado: um evento por linha. Chave candidata: event_id.
Coluna temporal: dt_evento. Somente leitura. Mostre o plano antes de qualquer ação Spark ampla.
```

**Revisar.** O plano deve inspecionar schema e unicidade, não gravar tabela.

**Executar** o helper de qualidade, se você autorizar código:

```python
from hub_scripts.data_quality_check import data_quality_check

resultado = data_quality_check(
    table_name="vw_campanha_eventos_sintetica",
    pk_columns=["event_id"],
    date_column=None,  # isola nulidade e chave; não consulta o relógio
    thresholds={"null_warn": 5.0, "null_fail": 20.0},
)
print(resultado["status"])
print(resultado["alerts"])
```

**Resultado esperado por inspeção do contrato, a conferir após executar.** `status="warn"`, `score=95`, vinte linhas, chave única sem nulos e um nulo em `canal`. A taxa é `1 / 20 × 100 = 5%`; o helper compara percentuais com `>=`, portanto alcança o limiar de aviso. `freshness` não integra os checks porque `date_column=None`.

```python
assert resultado["status"] == "warn"
assert resultado["score"] == 95
assert resultado["checks"]["row_count"] == 20
assert resultado["checks"]["nulls"]["canal"]["count"] == 1
assert resultado["checks"]["nulls"]["canal"]["pct"] == 5.0
assert resultado["checks"]["pk_uniqueness"]["duplicate_rows"] == 0
assert "freshness" not in resultado["checks"]
for alerta in resultado["alerts"]:
    print(alerta["check"], alerta.get("column"), alerta["severity"], alerta["message"])
```

O score subtrai 5 por aviso e 25 por falha, com piso zero. É política do helper, não probabilidade de a base estar correta. O nome da coluna fica em `column`; a mensagem de nulidade não precisa repetir esse nome.

**Adaptar sem alterar a regra de negócio em silêncio.** Mantenha `event_id` como chave do evento: `id_cliente` repete porque cada cliente pode receber vários contatos. Para retirar apenas o nulo sintético, gere outra view com `df.na.fill({"canal": "email"})`; ela deve resultar em `pass`. Não aplique essa imputação em dados reais sem investigar o significado do nulo. O [guia de scripts](../sprint-04-scripts/README.md) desenvolve também uma duplicata e um exemplo independente de freshness.

**Contexto da view.** Uma view temporária local existe na SparkSession que a criou, não no catálogo persistente. No chat, selecione a célula que constrói `df`, o schema e a célula que registra a view. Não diga “tabela anexada” antes de efetivamente selecionar um recurso. Se a ferramenta do agente usar outra sessão, peça somente o código e execute-o neste notebook; não crie uma tabela persistente como contorno implícito. Consulte [contexto de células](https://learn.microsoft.com/en-us/azure/databricks/genie-code/tips).

**Recuperação.** Primeiro confira `assistant_root.is_dir()` e a existência de `hub_scripts`. Depois confirme `spark.catalog.tableExists("vw_campanha_eventos_sintetica")`. Só então inspecione nomes de colunas e limiares. `ModuleNotFoundError` de pacote Hub é problema de localização; dependência opcional ausente é outro problema. `columns not found` neste helper gera `ValueError`.

**Exercício.** Na cópia sintética, duplique a primeira linha com `df.unionByName(df.limit(1))`. Antes de executar, preveja: haverá 21 linhas, uma duplicata e status `fail`. Confira `checks.pk_uniqueness` e explique por que um `warn` de nulos não neutraliza a falha da chave.

<a id="exemplo-validar-um-cruzamento"></a>

### Exemplo: validar um cruzamento

**Cenário.** Cadastro e eventos da campanha. Pergunta: o join multiplica linhas?

**Preparar.** Na mesma sessão do exemplo anterior, construa uma dimensão com uma linha por cliente. A origem da dimensão deste teste é a própria fixture, não um cadastro real.

```python
from hub_snippets.spark.join_diagnostics import diagnosticar_join
cadastro = df.select("id_cliente").distinct()
diagnostico_join = diagnosticar_join(df, cadastro, chave="id_cliente")
print(diagnostico_join)
```

A fixture possui cinco clientes na dimensão e vinte eventos; o join interno resulta em vinte linhas. Adicionar uma segunda linha de cadastro para um mesmo cliente pode multiplicar seus eventos. Antes de modelar, examine se esse efeito é esperado pelo grão definido.

**Pedir.** `@hub-ml-cross-eda-ml` com as duas fontes, período e grão esperado.

**Executar quando cabível.** `from hub_snippets.spark.join_diagnostics import diagnosticar_join` — a API pública é `diagnosticar_join`, não um nome em `hub_scripts`.

**Interpretar.** Cobertura, duplicidade e expansão são evidência de join, não prontidão automática para ML.

<a id="exemplo-acompanhar-drift"></a>

### Exemplo: acompanhar drift

**Cenário.** Score ou variável da campanha em dois períodos.

**Pedir.** `@hub-ml-monitoramento-modelo` com referência, atual, métricas e o que você fará com o alerta.

**Executar quando cabível.** `calcular_psi` em `hub_snippets.spark.psi_calculator` (DataFrames Spark já carregados) ou `hub_scripts.drift_detector` (tabela + coluna de coorte). PSI mede mudança de distribuição; não prova sozinho perda de performance.

A skill não agenda monitoramento nem retreina.

---

<a id="dependências-compute-e-segurança"></a>

## ⚙️ Dependências, Compute e Segurança

**Compute** é o recurso que executa o notebook. **Biblioteca** é o pacote Python instalado nele. **Import** é achar o módulo no `sys.path`. **Permissão** é o que o Unity Catalog e o workspace deixam você ler ou gravar. Os quatro falham de formas diferentes.

| Sintoma | Causa provável | Próximo passo seguro |
|---|---|---|
| `ModuleNotFoundError: hub_snippets` | path | inserir a raiz `.assistant`, não a pasta do objeto |
| `ImportError` de lightgbm / shap / plotly | biblioteca opcional | instalar só o pacote exigido, pelo mecanismo permitido |
| `PERMISSION_DENIED` | ACL | não contornar; peça acesso |
| skill “desatualizada” | cache de chat | conversa nova; hard refresh se precisar |

Não prescreva versões de laboratório como universais no trabalho.

Uma skill não amplia permissões. Revise escrita, instalação e `collect` amplo.

---

<a id="perguntas-frequentes-faq"></a>

## ❓ Perguntas Frequentes (FAQ)

<a id="1-o-que-acontece-quando-eu-abro-o-chat-da-genie-code-com-este-ecossistema-configurado"></a>

### 1. O que acontece quando eu abro o chat da Genie Code com este ecossistema configurado?

Instruções aplicáveis e, eventualmente, uma skill por relevância. Pastas `hub_` não são descobertas como skills. Se quiser o método de EDA, use `@hub-ml-eda-profissional`.

<a id="2-preciso-instalar-biblioteca-ou-reiniciar-o-compute-para-usar-snippets"></a>

### 2. Preciso instalar biblioteca ou reiniciar o compute para usar snippets?

Só se o módulo importar uma dependência ausente. Configurar `sys.path` não instala LightGBM. Quando uma instalação exigir recarregar o processo Python, use o procedimento permitido naquele compute; reiniciar todo o compute não é condição universal e não se aplica igualmente ao serverless. Não reinicie a cada import do Hub.

<a id="3-qual-é-a-diferença-prática-entre-skill-prompt-e-snippet"></a>

### 3. Qual é a diferença prática entre Skill, Prompt e Snippet?

Skill = método no chat. Prompt = texto que você preenche. Snippet = função no runtime. O script é o quarto: diagnóstico por nome de recurso.

<a id="4-como-o-ecossistema-contribui-para-mitigar-leakage-e-erros-analíticos"></a>

### 4. Como o ecossistema contribui para mitigar leakage e erros analíticos?

Pedindo instante de decisão e oferecendo helpers temporais. O vazamento continua possível se a data de corte for omitida ou o código for aceito sem leitura.

<a id="5-a-equipe-pode-criar-novos-snippets-prompts-ou-skills"></a>

### 5. A equipe pode criar novos snippets, prompts ou skills?

Sim, com [`hub_padroes`](../sprint-08-padroes/README.md) e revisão. `@hub-ml-criar-objeto` orienta o formato; não grava arquivo sem aprovação.

<a id="6-o-que-fazer-quando-a-skill-ou-o-helper-não-funciona-como-esperado"></a>

### 6. O que fazer quando a skill ou o helper não funciona como esperado?

Isole o defeito: roteamento (chat novo, `@`), import (`sys.path`), biblioteca, permissão ou contrato (assinatura no `.py`). Não “corrija” a `description` antes de saber se o teste é que estava mal formulado.

<a id="anexei-o-arquivo-por-que-ainda-preciso-importar"></a>

### Anexei o arquivo, por que ainda preciso importar?

Anexo alimenta o modelo. O interpretador Python só enxerga o que está em `sys.path` e foi importado.

<a id="como-saber-de-qual-pasta-veio-o-módulo"></a>

### Como saber de qual pasta veio o módulo?

O import `from hub_scripts.data_quality_check import data_quality_check` corresponde a `.assistant/hub_scripts/data_quality_check/`.

---

<a id="continue-explorando"></a>

## 🔗 Continue Explorando

Você já tem um percurso: escolher, contextualizar, revisar, executar, interpretar.

| Objetivo seguinte | Documento |
|---|---|
| Método | [Agent Skills](../sprint-05-skills/README.md) |
| Implementação | [Hub Snippets](../sprint-03-snippets/README.md) |
| Diagnóstico | [Hub Scripts](../sprint-04-scripts/README.md) |
| Briefing | [Hub Prompts](../sprint-06-prompts/README.md) |
| Criar objeto | [Hub Padrões](../sprint-08-padroes/README.md) |
| Vocabulário | [Glossário](../../../ambiente_fonte/.assistant/GLOSSARIO.md) |
| Índice de helpers | [Catálogo](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md) |

<a id="fontes-de-plataforma-e-alcance"></a>

### Fontes de plataforma e alcance

[Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills), [instruções](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions) e [modo agente e aprovações](https://learn.microsoft.com/en-us/azure/databricks/genie-code/agent-mode), consultados em 11/09/2026. As convenções `hub_` e os limiares analíticos são locais. Os exemplos deste guia são sintéticos; uma saída esperada não é homologação do seu workspace.
