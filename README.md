![CRM — Missão Modelos Analíticos CRM](ambiente_fonte/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Ecossistema/Hub `.assistant` para Databricks Genie Code voltado para Machine Learning

> Um ambiente integrado de governança, biblioteca algorítmica e inteligência contextual que ajuda a Genie Code e a equipe a trabalhar com métodos, componentes e critérios de revisão consistentes.

> **LEGENDA DE PROCEDÊNCIA.** Agent Skills e instruções são mecanismos reconhecidos pela Genie Code. Pastas com prefixo `hub_` e skills com prefixo `hub-` contêm implementações e convenções deste projeto; não são produtos institucionais da Databricks.


**Manual Técnico:** [entenda APIs, Python, Spark, helpers e o funcionamento do Hub](MANUAL_TECNICO.md).

---

## 🧭 Mapa de Leitura

> **Este documento apresenta a visão do ecossistema:** finalidade, componentes, arquitetura, circulação de contexto e manutenção do projeto.

| Se você quer entender... | Continue em... |
|---|---|
| por que o ecossistema existe | [Visão Geral](#-o-que-é-este-ecossistema-e-como-ele-ajuda-no-databricks) |
| quais componentes ele reúne | [Componentes](#-o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho) |
| como repositório, workspace e runtime se relacionam | [Arquitetura](#️-arquitetura-completa-do-ecossistema) |
| como a Genie Code recebe contexto | [Fluxo de Contexto](#-como-o-contexto-chega-ao-genie-code) |
| como o projeto evita cópias concorrentes | [Manutenção](#-como-o-projeto-é-mantido-sem-criar-duas-verdades) |

---

<a id="-o-que-é-este-ecossistema-e-como-ele-ajuda-no-databricks"></a>

## 🌟 O que é este Ecossistema e como ele ajuda no Databricks?

Desenvolver projetos de Machine Learning em ambientes de Big Data envolve desafios recorrentes: escrever engenharia de atributos, recalcular métricas de risco e drift, padronizar análises exploratórias e mitigar vazamento temporal (*data leakage*).

Quando usamos um assistente sem o contexto do projeto, ele pode propor fórmulas novas, escolher bibliotecas diferentes das adotadas pela equipe ou deixar premissas de dados implícitas.

**O ecossistema `.assistant` ajuda a transformar esse cenário em um fluxo contextualizado e revisável.**

Ele reúne Agent Skills, instruções, bibliotecas Python, diagnósticos e briefings. Assim, a Genie Code pode receber metodologia e contexto, enquanto o notebook reutiliza implementações do Hub de forma explícita.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ROTINA DO CIENTISTA DE DADOS                      │
│                                                                             │
│   ❌ Sem contexto: premissas implícitas, lógica repetida e revisão difícil  │
│   ✅ Com o Hub: método explícito, helpers reutilizáveis e saída conferível   │
└─────────────────────────────────────────────────────────────────────────────┘
```

O Hub não substitui julgamento técnico, permissões ou testes. Ele organiza o trabalho para que as decisões sejam mais claras e as entregas mais fáceis de auditar.

---

<a id="-o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho"></a>
<a id="o-que-tem-neste-ambiente-e-como-ele-ajuda-na-rotina-de-trabalho"></a>

## 🧰 O que tem neste ambiente e como ele ajuda na rotina de trabalho?

O ecossistema é dividido em cinco componentes modulares que cobrem diferentes responsabilidades do ciclo analítico:

![Mapa do ecossistema .assistant separado entre contexto e método, código e diagnóstico, com cinco componentes e suas formas de uso.](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/01_mapa_ecossistema.png)

*Leitura da figura: as ligações pontilhadas mostram organização, não execução. Agent Skills usam um mecanismo nativo com conteúdo do Hub; cada componente tem sua própria forma de uso.*

### 🧠 1. Agent Skills (`skills/`)

- **O que são:** habilidades modulares no padrão de Agent Skills que orientam a Genie Code em tarefas analíticas completas.
- **Como ajudam:** fornecem escopo, fluxo metodológico, guardrails, helpers recomendados e formatos de saída.
- **Como usar:** a Genie Code pode carregá-las por relevância da `description`, ou você pode selecioná-las explicitamente com `@hub-ml-*`.

### 📦 2. Hub Snippets (`hub_snippets/`)

- **O que são:** uma biblioteca Python customizada com funções e classes organizadas por pasta de objeto.
- **Como ajudam:** evitam reimplementar operações como split temporal, PSI, safras, métricas, formatação e diagnósticos Spark.
- **Como usar:** configurar a raiz que contém `hub_snippets/` no `sys.path` ou no ambiente Python adotado e importar o módulo explicitamente.

### ⚡ 3. Hub Scripts (`hub_scripts/`)

- **O que são:** utilitários importáveis de inspeção, transformação analítica e governança técnica.
- **Como ajudam:** respondem a perguntas operacionais sobre qualidade, perfil, drift, RFV, schema, nomenclatura e documentação.
- **Como usar:** configurar o caminho Python, importar a função e executar explicitamente. Cada utilitário tem seu contrato de retorno: diagnóstico, DataFrame, texto ou lista de violações. Quando houver uma decisão operacional, o notebook ou a tarefa define se deve alertar, interromper ou prosseguir.

### 📝 4. Hub Prompts (`hub_prompts/`)

- **O que são:** briefings estruturados para preencher.
- **Como ajudam:** orientam o usuário a declarar contexto, grão, período, regras, limites, entrega e critérios de aceite.
- **Como usar:** abrir o template, substituir todos os campos, anexar os recursos e fornecer o texto à Genie Code. Eles não são slash commands nem são descobertos automaticamente.

### 📐 5. Hub Padrões (`hub_padroes/`)

- **O que são:** moldes arquiteturais e editoriais do ecossistema.
- **Como ajudam:** mantêm novos objetos coerentes em estrutura, documentação, testes e exemplo.
- **Como usar:** consultar manualmente ou fornecer como contexto ao criar conteúdo. A skill `@hub-ml-criar-objeto` pode orientar a aplicação desses moldes.

> **INFRAESTRUTURA EDITORIAL DO HUB.** A pasta
> `hub_readmes_visual_assets/` mantém os diagramas e os cabeçalhos compartilhados
> de CRM e Squad, com fontes de composição e PNGs. Ela
> não é um sexto componente funcional, não é nativa da Databricks e não fornece
> contexto automaticamente à Genie Code.

Os diagramas ficam em `readmes/<familia>/`; os cabeçalhos, em `headers/`.
O PNG de CRM serve aos READMEs e aos notebooks gerais; o da Squad identifica
notebooks específicos, sem empilhar os dois banners. A origem raster, a camada
tipográfica e os caminhos de uso estão no [guia de assets](ambiente_fonte/.assistant/hub_readmes_visual_assets/README.md).

---

<a id="️-arquitetura-completa-do-ecossistema"></a>
<a id="arquitetura-completa-do-ecossistema"></a>

## 🏛️ Arquitetura Completa do Ecossistema

O diagrama abaixo mostra como o repositório, o workspace e o runtime se relacionam sem confundir contexto da IA com importação de código:

![Corte arquitetural entre fonte versionada, workspace, contexto da Genie Code, notebook e runtime.](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/02_arquitetura_ecossistema.png)

*Leitura da figura: a publicação torna os arquivos disponíveis no workspace. O plano de contexto e o plano de execução são distintos: helpers podem ser usados diretamente pelo notebook, sem passar pela conversa.*

> **Leitura do fluxo:** o repositório controla a origem; o workspace disponibiliza
> o conteúdo; a Genie Code usa apenas as camadas de contexto aplicáveis; o
> notebook importa e executa código no runtime.

### O que este diagrama deixa explícito

- Agent Skills e instruções usam mecanismos de contexto reconhecidos pela Genie Code.
- `hub_prompts` e `hub_padroes` são fornecidos manualmente quando necessários.
- `hub_snippets` e `hub_scripts` pertencem ao runtime Python; estar dentro de `.assistant` não os coloca automaticamente no `sys.path`.
- Evidência local, conteúdo promovido e execução no runtime são gates diferentes.

<a id="ciclo-de-vida-do-projeto"></a>

### Ciclo de vida do projeto

![Pista de promoção com sete gates e retornos de correção para a etapa de edição.](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/raiz/png/03_ciclo_de_vida.png)

*Leitura da figura: editar, validar, renderizar, publicar e verificar, testar, registrar e promover são sete gates. Publicação e conferência pertencem ao mesmo gate; qualquer falha exige correção na fonte antes de prosseguir.*

O registro associa a mudança às evidências e à versão correspondente. A promoção
ao destino autorizado é uma ação controlada, não uma continuação automática de
uma execução que terminou sem erro.

`ambiente_fonte/` é a fonte editável. `Novo_Ambiente_Simulado/` é derivado por ferramenta e não deve ser alterado manualmente. Auditorias, testes e orientações operacionais ficam na documentação interna do projeto.

---

<a id="-como-o-contexto-chega-ao-genie-code"></a>
<a id="como-o-contexto-chega-ao-genie-code"></a>

## 🔄 Como o Contexto chega ao Genie Code?

Uma pergunta importante é: *“Como a Genie Code sabe que essas orientações e bibliotecas existem?”*

A resposta depende da camada. **Não existe uma única leitura automática de toda a pasta `.assistant`.**

![Confluência de fontes de contexto suportadas para a Genie Code e suas saídas possíveis.](ambiente_fonte/.assistant/hub_readmes_visual_assets/readmes/assistant/png/03_contexto_e_execucao.png)

*Leitura da figura: código e histórico, metadados permitidos, instruções aplicáveis e recursos fornecidos à tarefa convergem para a Genie Code. As ações respeitam o escopo e a política de aprovação configurada; aceitar o resultado continua exigindo revisão técnica.*

### Explicação Passo a Passo

1. **Gatilho e intenção:** você descreve uma demanda em linguagem natural, anexa tabelas, notebooks ou células e pode selecionar uma skill com `@`.
2. **Diretrizes aplicáveis:** instruções pessoais, instruções de workspace quando configuradas e arquivos hierárquicos de projeto orientam as superfícies suportadas.
3. **Ativação da skill:** a Genie Code pode carregar uma Agent Skill por relevância da `description`, ou você pode selecioná-la explicitamente.
4. **Plano e geração:** a skill orienta método, riscos, recursos e formato. Ela pode recomendar um helper, mas não o importa automaticamente.
5. **Execução no runtime:** o notebook configura o caminho que contém os pacotes, importa a função e executa conforme dependências e permissões.
6. **Revisão:** a pessoa verifica código, dados, custo, resultado e qualquer ação persistente antes de aceitar a entrega.

Esses itens explicam responsabilidades, não uma ordem rígida de carregamento.
Para uma resposta sem execução, declare isso no pedido. A aprovação de ferramentas
pode ser individual ou previamente configurada; ela não substitui controles de
acesso nem comprova a correção analítica. Veja a [documentação do modo agente](https://docs.databricks.com/aws/en/genie-code/agent-mode).

> **Dica:** após editar uma skill, teste em uma nova conversa. Se a versão anterior continuar aparecendo, faça uma atualização completa da página.

---

<a id="-como-o-projeto-é-mantido-sem-criar-duas-verdades"></a>

## 🧭 Como o Projeto é Mantido sem Criar Duas Verdades

| Camada | Papel | Regra principal |
|---|---|---|
| `ambiente_fonte/` | fonte do produto | editar aqui |
| `Novo_Ambiente_Simulado/` | representação derivada | gerar com `tools/render_simulado.py` |
| `tools/` | gates e automação | executar antes de promover |
| `docs/` | decisões e evidências | registrar data, escopo e limitações |
| workspace | cópia operacional | verificar inventário, conteúdo e runtime |

O gate local verifica estrutura e contratos; a comparação de conteúdo verifica equivalência; o smoke verifica execução; os forward tests verificam roteamento de skills. Nenhum deles substitui os demais.

### Concierge integrado, publicação pendente

O [Concierge Hub](ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md)
ajuda a descobrir e combinar recursos existentes sem substituir especialistas.
A integração inclui templates e testes locais; o aceite conversacional e a
publicação no Databricks permanecem separados. Consulte os
[forward tests](docs/testes/forward/README.md) antes de compartilhar a instalação.

### Estado verificável do gate local

O bloco abaixo é a saída do validador no estado versionado. Ele não é uma
declaração decorativa: `python tools/validate_assistant.py --conferir-readme`
reexecuta o gate e reprova se qualquer contagem ficar desatualizada.

```text
skills             : 14 · 14/14 com as 5 seções estruturais
prompts            : 16 · 161 campos com guia e contrato humano
helpers citados    : 88 caminhos verificados
markdown / links   : 154 arquivos / 609 links relativos
notebooks / links  : 79 notebooks / 43 links relativos
readmes de objeto  : 20/75 operacionais; 3/3 exemplares; 55 pendentes (estrutura, não aceite editorial)
pastas de objeto   : 61 conferidas (nome, arquivos, __init__)
forma da pasta     : 59 conferidas (o módulo tem o nome da pasta)
contrato de dados  : 61 pares (saída: o que o notebook consome)
contrato de entrada: 58 pares (entrada: o que o notebook passa)
saída colada       : 78 notebooks com bloco real, 0 sem
idioma da docstring: 61 módulos, 0 com docstring em inglês
normas do molde    : 71 arquivos, 0 violação(ões)
notebook exercita  : 58 objetos, 0 notebook(s) que só importam
python (AST)       : 214 arquivos
instrucoes         : 9043/20000 caracteres
repo (identidade)  : 1100 arquivos varridos no repositório editável/derivado
repo (links)       : 1032 links fora da raiz analisada

APROVADO: 0 falha(s), 0 aviso(s)
```

---

## ❓ Perguntas Frequentes (FAQ)

### 1. O que acontece quando eu abro o chat da Genie Code com este ecossistema configurado?

As instruções aplicáveis podem orientar a conversa, e uma Agent Skill pode ser carregada quando sua `description` for relevante ou quando você a selecionar com `@`. As extensões `hub_prompts`, `hub_snippets`, `hub_scripts` e `hub_padroes` não entram automaticamente apenas por existirem na pasta.

### 2. Preciso instalar alguma biblioteca ou configurar o Python para usar os snippets?

Você precisa garantir que a raiz que contém `hub_snippets/` esteja disponível ao Python. Uma forma direta no workspace é:

```python
from pathlib import Path
import sys

assistant_root = Path("/Workspace/Users/<username>/.assistant")
if str(assistant_root) not in sys.path:
    sys.path.insert(0, str(assistant_root))

from hub_snippets.ml.split_temporal import temporal_split
```

Alguns helpers possuem dependências opcionais. Em compute serverless, elas podem ser declaradas pelo **Environment** ou pelo ambiente do Git folder, conforme o fluxo suportado. Confirme pacote, versão e compatibilidade antes de executar.

### 3. Qual é a diferença prática entre Skill, Prompt, Snippet e Script?

- **Skill:** metodologia usada pela Genie Code; mecanismo nativo com conteúdo `hub-ml-*` do projeto.
- **Prompt:** briefing que você preenche e fornece manualmente.
- **Snippet:** função ou classe importável para compor seu código.
- **Script:** utilitário autocontido chamado explicitamente, com contrato próprio de saída.

### 4. Como o ecossistema ajuda a mitigar leakage e erros analíticos?

Skills e helpers tornam entidade, instante de decisão, janela temporal, disponibilidade e validações mais explícitos. Isso reduz riscos conhecidos, mas não garante ausência de leakage. A pessoa precisa confirmar o contrato temporal, revisar o código e testar o caso real.

### 5. A equipe pode criar novos snippets, prompts ou skills?

Sim. Use `hub_padroes/` e a skill `@hub-ml-criar-objeto`, mantendo API pública, documentação, exemplo e testes. Mudanças no produto nascem em `ambiente_fonte/`, passam pelos gates e são registradas no changelog.

### 6. Se o código foi gerado pela Genie Code, posso executá-lo sem revisão?

Não é recomendado. Confira recursos, filtros, plano, coletas, dependências, permissões e operações persistentes. Gerar código, executar e aprovar um resultado são decisões diferentes.

---

## 🔗 Próximos Passos

- [Guia do ecossistema para usuários](ambiente_fonte/.assistant/README.md)
- [Hub Snippets](ambiente_fonte/.assistant/hub_snippets/README.md)
- [Hub Scripts](ambiente_fonte/.assistant/hub_scripts/README.md)
- [Agent Skills](ambiente_fonte/.assistant/skills/README.md)
- [Hub Prompts](ambiente_fonte/.assistant/hub_prompts/README.md)
- [Recursos da Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/features-capabilities)
- [Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)

Para a instalação pessoal no trabalho, siga o [guia de transição com kit e notebook de aceite](docs/playbooks/replicacao-trabalho.md).

## Migração documental por objeto

A [iniciativa R00–R13](docs/sprints/readmes_objetos/README.md) acrescenta guias
de conceito, adequação e uso seguro. Consulte o checkpoint antes de iniciar um
lote. R01 é fundação editorial, não geração dos READMEs operacionais nem
publicação no Databricks.

### Integração READMEs + Concierge e continuidade

A [R02-I](docs/sprints/readmes_objetos/INTEGRACAO_R02.md) foi integrada pelo
PR nº 7 após aprovação de Rodrigo em 2026-09-12 (`5493f7d`). As oito etapas
preservam as verificações das duas frentes. O [aceite e versão estável](docs/sprints/readmes_objetos/ACEITE_V1.md)
registra o contrato 1.0.0; o [lote R03-A](docs/sprints/readmes_objetos/RELATORIO_R03A.md)
acrescenta sete guias em branch própria para revisão. A integração Git não
publica o Hub no Databricks nem substitui homologação no workspace.

### Continuidade R03-B

O [lote R03-B](docs/sprints/readmes_objetos/RELATORIO_R03B.md) documenta seis
objetos de apresentação e navegação, em branch dependente da R03-A ainda em
revisão. O contrato permanece 1.0.0; não há alteração visual, novo merge ou
publicação. A matriz da sprint identifica também as demais documentações atualizadas.