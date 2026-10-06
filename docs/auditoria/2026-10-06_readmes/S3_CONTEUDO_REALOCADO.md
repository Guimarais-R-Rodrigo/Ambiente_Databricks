# Skills e Micromodelos: trechos anteriores realocados

Baseline `2f5a0cb94f82b78324f6a79d70af7d03e7b57040`. Excertos históricos; contratos operacionais atuais estão nas fontes. Links foram fixados ao snapshot.

## R0067 · ambiente_fonte/.assistant/hub_micromodelos/README.md

## Estado desta entrega

O módulo e o exemplo sintético estão instaláveis no pacote do Hub. A skill permanece `L1/audit`; seu `target_level=L3` é plano, não capacidade presente. O código de laboratório, o ensaio local e o readback de arquivos no Free não homologam comportamento no Genie Code, dados reais, execução do módulo recém-distribuído no Free ou uso corporativo. O [Manual Técnico](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_micromodelos/../MANUAL_TECNICO.md#micromodelos) explica o lugar de Micromodelos no ecossistema; o [guia de jornada](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_micromodelos/guias/README.md) informa a ação e a evidência exigida em cada etapa.

## R0069 · ambiente_fonte/.assistant/hub_micromodelos/execucao/README.md

| conferir o piloto sintético | `execucao.run_greenfield_lab` | Resultado E0 da fixture própria do laboratório. |

## R0069 · ambiente_fonte/.assistant/hub_micromodelos/execucao/README.md

## 15. Referências

O comportamento descrito é o dos módulos desta pasta e do [schema](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/hub_micromodelos/execucao/../contratos/micromodelo.schema.json). As decisões de domínio estão no Manual Técnico do Hub e na documentação arquitetural da frente de Micromodelos.

## R0070 · ambiente_fonte/.assistant/hub_micromodelos/exemplos/README.md

## Limites e armadilhas

Resultados desses arquivos são ensaios E0. A fonte fictícia, a decisão humana, o MLflow e a publicação têm estados separados na especificação. Uma saída comparada ao oráculo local demonstra reprodução do cálculo, não validade estatística ou aceite de governança.

## R0072 · ambiente_fonte/.assistant/hub_micromodelos/guias/README.md

| Capacidade | Onde está | O que está demonstrado | O que continua pendente |
|---|---|---|---|
| Schema, estados, proveniência e assinatura | `contratos/`, `execucao/especificacao.py`, `assinatura.py` | Validação e fingerprint locais, inclusive no caso preenchido. | Decisão humana sobre a adequação semântica de fontes e regras. |
| Descoberta metadata-only e shortlist | `execucao/metadados.py`, `fluxo.py`, `databricks.py` | Fixture E0 e adapter de metadata usado no Free em ensaio anterior. | Binding, escopo e permissões reais no trabalho; metadata não prova viabilidade. |
| Classificação e score | `execucao/execucao.py`; `exemplos/recencia_contato/` | Dois cenários sintéticos reproduzíveis; no caso de recência, `TRUE`, `FALSE` e `INDETERMINADO` reconciliados. | Validação estatística, calibração e dados reais autorizados. |
| Artefatos e tracking | `execucao/artefatos.py`; `hub_snippets/ml/mlflow_run` | Scaffold `NOT_RUN`; runs sintéticas E0/E1 do laboratório anterior documentadas no repositório. | Run do novo caso de recência no Free ou no trabalho; política institucional e aprovação. |
| Handoff e reconciliação | `execucao/entrega.py`; `exemplos/recencia_contato/conferir_entrega.py` | Rascunho local calculado a partir do resultado sintético conferido. | Aceite da autoridade externa, Produto de Dados, reconciliação de publicação real. |
| Catálogo, impacto e comparação legada | `execucao/catalogo.py`; `exemplos/migracao_simulada.py` | Ensaios locais fictícios. | Migração real, monitoramento, tema visual e freeze V1. |

“Implementado” significa que existe código; “demonstrado” identifica um ensaio concreto. O envio e readback de arquivos para o Databricks Free confirma transporte dos bytes, não executa por si os módulos publicados. O guia de implantação e as portas institucionais ficam na documentação de operação do repositório, fora do produto publicado.

## R0083 · ambiente_fonte/.assistant/skills/README.md

Na operação SE08, policy e contratos integram os validadores permanentes do Hub.
Isso ainda não transforma CI local em teste de comportamento do Genie Code:
seleção, uso de recursos e resistência a bypass precisam de evidência própria no
ambiente alvo.

## R0083 · ambiente_fonte/.assistant/skills/README.md

Integrada ao produto; publicação e testes conversacionais no destino pendentes.
É uma entrada opcional, não substitui o especialista explicitamente selecionado.

## R0083 · ambiente_fonte/.assistant/skills/README.md

A candidata de Micromodelos veio da cópia pessoal do Free; sua incorporação ao
catálogo não certifica a sprint MM04 nem a execução de descoberta no Databricks.

## R0086 · ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md

**Estado: integrada ao produto do Hub em 12/09/2026 (versão 0.2.0). Publicação e aceite conversacional no Databricks pendentes.**

## R0091 · ambiente_fonte/.assistant/skills/hub-ml-micromodelos/README.md

A origem desta candidata foi a publicação pessoal no Databricks Free, preservada
por solicitação do usuário e incorporada à fonte em 2026-09-29. Sua presença no
pacote não prova seleção no Genie, execução no Free ou aceite completo de MM04.
O registro de reconciliação do repositório distingue a incorporação da
certificação da sprint.

## R0067 · ambiente_fonte/.assistant/hub_micromodelos/README.md

# Hub Micromodelos

## R0068 · ambiente_fonte/.assistant/hub_micromodelos/contratos/README.md

# Contrato `micromodelo.yaml`

## R0069 · ambiente_fonte/.assistant/hub_micromodelos/execucao/README.md

# Execução de Micromodelos

## R0070 · ambiente_fonte/.assistant/hub_micromodelos/exemplos/README.md

diretório do produto

## R0070 · ambiente_fonte/.assistant/hub_micromodelos/exemplos/README.md

# Exemplos de Micromodelos

## R0071 · ambiente_fonte/.assistant/hub_micromodelos/exemplos/recencia_contato/README.md

há contato recente verificável nos sete dias que terminam em 2026-09-30?

## R0071 · ambiente_fonte/.assistant/hub_micromodelos/exemplos/recencia_contato/README.md

4. Troque `classificacao.limiares[0].valor` de `7` para `2` no YAML e execute sem `--conferir`: `pessoa_f` deixa de ser `TRUE`, pois seu contato tem sete dias. A assinatura material também muda. Restaure `7` para repetir o oráculo.

## R0083 · ambiente_fonte/.assistant/skills/README.md

![CRM — Missão Modelos Analíticos CRM](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Agent Skills

> O cérebro metodológico do ecossistema no Databricks Genie Code: diretrizes de engenharia, guardrails e fluxos analíticos passo a passo para orientar trabalhos de Machine Learning.

> **MECANISMO NATIVO, CONTEÚDO CUSTOMIZADO.** Agent Skills são um recurso oficial da Genie Code e seguem o padrão aberto Agent Skills. Os nomes `hub-ml-*`, as metodologias, os templates e os helpers descritos aqui foram criados neste projeto.

---

## 🧭 Neste Guia

| Para entender... | Vá para... |
|---|---|
| o que uma Agent Skill faz | [O que são Agent Skills](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/README.md#-o-que-são-agent-skills) |
| como ocorre a seleção por relevância ou `@` | [Como as Skills são utilizadas](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/README.md#-como-o-genie-code-e-o-usuário-utilizam-as-skills) |
| a relação entre metodologia e código | [Skills, Snippets e Scripts](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/README.md#-relação-entre-skills-hub-snippets-e-hub-scripts) |
| as skills disponíveis | [Catálogo](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/README.md#️-catálogo-de-agent-skills) |
| o propósito de cada skill | [Detalhamento](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/README.md#-detalhamento-das-skills) |
| permissões e aprovação | [Aprovações e Revisão](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/README.md#-aprovações-permissões-e-revisão) |

---

<a id="-o-que-são-agent-skills"></a>

## 🧠 O que são Agent Skills?

Para entender o que é uma **Agent Skill**, imagine a seguinte situação:

> Você recebe um cientista de dados tecnicamente preparado. Ele conhece teoria e ferramentas, mas ainda não conhece as regras da sua equipe, as bibliotecas internas disponíveis nem as armadilhas recorrentes do seu domínio.
>
> Para orientar o trabalho, você entrega um **Procedimento Operacional Padrão (POP)**: “nesta tarefa, comece por estas perguntas, siga estas etapas, observe estes riscos, utilize estes recursos e entregue o resultado neste formato”.

**Uma Agent Skill funciona como esse POP estruturado para a Genie Code.**

Uma skill **não é código Python para importar**. Ela é um pacote de instruções cujo arquivo principal, `SKILL.md`, ensina o assistente a:

1. **Pensar antes de agir:** decompor o problema e declarar premissas antes de escrever ou executar código.
2. **Respeitar guardrails:** evitar práticas como vazamento temporal, coleta indiscriminada no driver ou conclusão estatística sem contexto.
3. **Recomendar a biblioteca do Hub:** apontar helpers existentes de `hub_snippets` e `hub_scripts` quando eles forem adequados, sem presumir que foram importados.
4. **Entregar de forma consistente:** usar checklists e templates para tornar código, evidências e limitações mais fáceis de revisar.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ANATOMIA DE UMA AGENT SKILL                       │
│                                                                             │
│   🎯 Objetivo & Escopo: quando a habilidade se aplica e onde termina        │
│   🗺️ Metodologia: etapas, decisões e perguntas que orientam o trabalho      │
│   🚫 Guardrails: riscos que precisam ser prevenidos ou aprovados            │
│   📦 Catálogo de Helpers: caminhos reutilizáveis recomendados               │
│   📋 Templates de Saída: estruturas de entrega e critérios de revisão       │
└─────────────────────────────────────────────────────────────────────────────┘
```

Guardrails textuais reduzem risco, mas não são barreiras técnicas absolutas. Permissões, política de aprovação, revisão humana e testes continuam valendo.

---

<a id="-como-o-genie-code-e-o-usuário-utilizam-as-skills"></a>
<a id="como-o-genie-code-e-o-usuario-utilizam-as-skills"></a>

## 🤖 Como o Genie Code e o Usuário utilizam as Skills

O ciclo de vida de uma skill estabelece uma interação colaborativa entre o usuário, o assistente e os recursos do Databricks:

![Duas rotas independentes, relevância e menção com @, convergindo no carregamento de uma Agent Skill.](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_readmes_visual_assets/readmes/skills/png/01_descoberta_e_selecao.png)

*Leitura da figura: a `description` ajuda o roteamento; a menção com `@` torna a escolha explícita.*

**Equivalente textual:** na rota por relevância, a Genie Code compara o pedido com a `description` da skill. Na rota explícita, a pessoa seleciona a skill com `@nome-da-skill`. As duas rotas convergem no carregamento do mesmo pacote de instruções, sem eliminar a necessidade de revisar a entrega.

### 1. Pelo lado do Genie Code (Seleção por Relevância)

Cada skill possui no cabeçalho de `SKILL.md` um frontmatter YAML com `name` e `description`:

- A Genie Code usa a descrição para decidir se a skill é relevante à solicitação.
- Quando o pedido corresponde ao escopo, o assistente pode carregar a skill e seguir suas instruções.
- Recursos adicionais da pasta são utilizados conforme forem referenciados e necessários; não presuma que toda a subpasta `templates/` é carregada integralmente em toda conversa.
- A seleção por relevância depende da qualidade da descrição e do pedido. Ela deve ser testada, não tratada como certeza universal.

### 2. Pelo lado do Usuário (Ativação Explícita com `@`)

Quando você quer indicar uma metodologia específica, mencione a skill com `@`:

```text
@hub-ml-feature-engineering

Desenhe as features para prever o cancelamento de clientes nos próximos 30 dias
utilizando a tabela anexada `catalogo_crm.vendas.historico`.

- Data de referência: dt_venda
- Entidade: id_cliente
- Disponibilidade das fontes: NÃO INFORMADO — pergunte antes de assumir
- Apresente primeiro o plano metodológico e os riscos de leakage.
- Não execute nem persista alterações antes da minha aprovação.
```

A `@menção` é a forma explícita suportada de selecionar uma skill. Ela reduz ambiguidade, mas não transforma o resultado em determinístico nem substitui a revisão do que foi carregado e produzido.

> **Dica:** depois de editar uma skill publicada, teste-a em um chat novo. Se a versão anterior ainda aparecer, faça uma atualização completa da página antes de concluir que a mudança não foi reconhecida.

---

<a id="-relação-entre-skills-hub-snippets-e-hub-scripts"></a>
<a id="relacao-entre-skills-hub-snippets-e-hub-scripts"></a>

## 🔗 Relação entre Skills, Hub Snippets e Hub Scripts

Para que o ecossistema funcione de forma coerente, existe uma divisão de papéis:

> **A Skill é o Maestro: organiza a metodologia.**
> **Os Snippets e Scripts são os Instrumentos: fornecem implementações e diagnósticos reutilizáveis.**

![Dois planos separando método da Agent Skill e execução explícita de helpers no notebook.](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_readmes_visual_assets/readmes/skills/png/02_skill_helpers_runtime.png)

*Leitura da figura: orientação metodológica e código executável são responsabilidades diferentes.*

**Equivalente textual:** no plano de contexto, a skill orienta metodologia e guardrails e pode recomendar um helper quando adequado. No plano de runtime, o notebook precisa importar e chamar esse helper explicitamente; a recomendação não instala, importa nem executa código.

### Caso de Uso Genérico

1. **Sem uma metodologia específica:** ao pedir apenas “calcule estabilidade”, o assistente precisa inferir população de referência, período atual, variáveis, bins, escala e critérios de interpretação.
2. **Com a skill do ecossistema:** a skill orienta essas decisões e recomenda, quando adequado, `hub_snippets.spark.psi_calculator` ou `hub_scripts.drift_detector`.
3. **No runtime:** o notebook ainda precisa tornar `.assistant` visível ao Python, importar o helper e satisfazer suas dependências. A skill não instala, importa ou executa a biblioteca sozinha.

O objetivo é reduzir reinvenção e tornar a solução conferível — não prometer código infalível, execução instantânea ou um threshold universal de PSI.

---

## 🛡️ Skill Enforcement Framework

O Hub usa uma policy transversal para declarar o nível de enforcement realmente
existente em cada skill. Ela não substitui o `SKILL.md`; registra o quanto do
fluxo já saiu de orientação textual e passou a ter gates estruturais
verificáveis.

| Nível | Evidência operacional |
|---|---|
| L0 | orientação textual |
| L1 | contrato estruturado e validável |
| L2 | preflight antes da lógica protegida |
| L3 | execução determinística com evidência/Receipt |
| L4 | Postflight fail-closed antes de conclusão homologada |

`current_level` descreve o que existe agora. `target_level` é roadmap. Por
isso uma skill pode ter target L3/L4 e continuar corretamente em L0/L1/L2 até
que os artefatos correspondentes existam e seus gates passem.

O rollout também é explícito: `guidance`, `audit`, `warn` e `enforce`.
Um modo mais rígido não deve ser inferido do risco da tarefa nem de uma resposta
bem-sucedida. A política é consultável pela API pública de
`hub_scripts.skill_execution`.

A presença de contratos e scripts não comprova que foram usados na conversa. Confira a skill carregada e a evidência da rota executada.

---

## 📋 O que são os Templates das Skills?

Dentro das pastas de algumas skills existe uma subpasta chamada **`templates/`**.

**Templates são gabaritos de especificação, análise e entrega que ajudam a manter uma saída uniforme e revisável.**

Pense neles como formulários técnicos especializados:

- **Gabaritos de Estilo Visual**, como `estilo_visual_eda.md`: orientam composição, hierarquia e leitura; paletas e tokens configuráveis pertencem ao `ResolvedTheme` e ao padrão `hub_padroes/identidade_visual`, não ao template da skill.
- **Checklists de Validação**, como `checklist-objeto-novo.md`: organizam requisitos que devem ser conferidos antes de concluir uma entrega.
- **Formatos de Laudo**, como `notebook_output_stat.md`: estruturam hipótese, teste, efeito, incerteza, limitações e decisão.

Um template não é executável e não é um helper. Ele só influencia a resposta quando a skill o referencia e o assistente o utiliza como contexto.

---

## 🎨 Skills e Sistema de Temas

Skills podem **recomendar** consumidores visuais, mas não são fonte de paleta, token ou aprovação. Quando uma tarefa pedir identidade visual, tema ou consistência entre gráficos:

1. trate `hub_padroes/identidade_visual` e `ResolvedTheme` como fontes canônicas;
2. use a rota `_resolvido` do consumidor quando ela existir;
3. mantenha dados, métricas, thresholds e decisões analíticas independentes da aparência;
4. não presuma publicação ou homologação no Databricks;
5. preserve limites declarados — por exemplo, SHAP/Matplotlib e Kaplan–Meier não possuem theming V07 homologado.

`estilo_visual_eda.md` continua útil para decisões **editoriais da EDA** (estrutura, escolha de gráfico, anotações e leitura), mas não pode redeclarar a paleta do Hub.

<a id="estrutura-de-uma-skill-profissional"></a>

## 🏛️ Arquitetura de Skills no Hub

Cada skill habita em seu próprio diretório em `.assistant/skills/<nome-da-skill>/` e possui um arquivo canônico `SKILL.md`:

```text
.assistant/skills/hub-ml-feature-engineering/
├── SKILL.md                  # metodologia e roteamento da skill
└── templates/                # recursos de apoio, quando necessários
    ├── feature_spec_core.md
    └── checklist_validacao_features.md
```

![Dossiê de uma Agent Skill mostrando frontmatter e instruções dentro de SKILL.md e recursos opcionais ao lado.](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_readmes_visual_assets/readmes/skills/png/03_anatomia_skill.png)

*Leitura da figura: o mecanismo Agent Skills reconhece o pacote; o conteúdo metodológico e seus recursos são mantidos pelo Hub.*

A separação em camadas evita transformar o arquivo principal em um depósito de referências. Metadados ajudam o roteamento; instruções organizam o trabalho; recursos são carregados quando a tarefa realmente os exige.

### Requisitos oficiais e seções estruturais do Hub

No padrão oficial, `SKILL.md` precisa ter frontmatter válido com `name` e `description`. Neste projeto, o contrato editorial acrescenta seções auditadas:

1. **Frontmatter YAML:** identificação e descrição usada no roteamento.
2. **Quando esta skill se aplica:** inclusão, exclusão e fronteiras com outras skills.
3. **Fluxo de execução:** sequência de entendimento, planejamento, código e entrega.
4. **Helpers da biblioteca:** caminhos de `hub_snippets` e `hub_scripts` recomendados, quando existirem.
5. **O que NUNCA fazer (Guardrails):** riscos e operações que exigem prevenção ou aprovação.
6. **Formato de saída:** artefatos e critérios de revisão.

Os itens 2 a 6 são uma convenção de qualidade do Hub, não campos obrigatórios da especificação oficial de Agent Skills.

### Onde as skills podem ficar

- **Skill de usuário:** `/Users/<username>/.assistant/skills/`
- **Skill de workspace:** `Workspace/.assistant/skills/`

O local define o escopo e as permissões. A disponibilidade de uma skill compartilhada depende de como o workspace foi administrado.

---

<a id="️-catálogo-de-agent-skills"></a>

## 🗺️ Catálogo de Agent Skills

As skills cobrem etapas complementares de um ciclo analítico. O catálogo foi
dividido por etapa para permanecer legível em painéis estreitos do workspace.

### 🧭 Descoberta e composição

| Skill | Objetivo principal |
|---|---|
| [hub-ml-concierge](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md) | Localizar e combinar recursos existentes sem exigir que o usuário conheça o catálogo. |
| [hub-ml-micromodelos](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-micromodelos/SKILL.md) | Especificar micromodelo novo ou descobrir oportunidades via metadata, com decisões pendentes explícitas. |

O Concierge é opcional: use-o para escolher recursos. Micromodelos orienta especificação e descoberta; consulte a área de domínio para exemplos e código.

### 🔍 Exploração & Diagnóstico

| Skill | Objetivo principal |
|---|---|
| `hub-ml-eda-profissional` | EDA univariada e bivariada com qualidade e síntese executiva. |
| `hub-ml-cross-eda-ml` | Cruzamento de fontes e avaliação de prontidão para modelagem. |
| `hub-ml-validacao-estatistica` | Hipóteses, pressupostos, efeito e inferência sob incerteza. |

### 🧱 Engenharia de Dados & Risco

| Skill | Objetivo principal |
|---|---|
| `hub-ml-feature-engineering` | Features e joins temporais com instante de decisão explícito. |
| `hub-ml-analise-safra` | Curvas de safra, denominadores e maturação comparável. |

### 📈 Modelagem & Explicabilidade

| Skill | Objetivo principal |
|---|---|
| `hub-ml-baseline-ml` | Baselines por tipo de problema, validação e tracking. |
| `hub-ml-explainability` | Interpretação global/local e comunicação de limitações. |
| `hub-ml-micromodelos` | Especificação e descoberta por metadata, com contrato estático L1 e sem execução protegida. |

A skill Micromodelos mantém especificação e proveniência; a execução requer os recursos, permissões e verificações da etapa escolhida.

### ⚙️ MLOps & Produção

| Skill | Objetivo principal |
|---|---|
| `hub-ml-monitoramento-modelo` | Performance, drift, fairness, custo e decisão de retreino. |
| `hub-ml-pipeline-builder` | Pipelines modulares, qualidade, observabilidade e automação. |

### 🛡️ Governança & Engenharia

| Skill | Objetivo principal |
|---|---|
| `hub-ml-comentar-notebook` | Documentação técnica e executiva de notebooks. |
| `hub-ml-tutor-databricks` | Explicação didática de código, Spark, Databricks e ML. |
| `hub-ml-auditoria-skills` | Auditoria da implementação de skills e das entregas produzidas. |
| `hub-ml-criar-objeto` | Criação orientada de objetos no padrão do Hub. |

> **Como ler o catálogo:** a etapa organiza o ponto de entrada, mas não limita a
> composição. Uma análise pode combinar skills desde que objetivo, ordem e
> responsabilidades permaneçam explícitos.

---

<a id="-detalhamento-das-skills"></a>

## 📖 Detalhamento das Skills

Abaixo você encontra o propósito, o momento de uso, os principais recursos e um exemplo de demanda para cada skill.

### `hub-ml-concierge` — Orientação de uso do Hub

Use ao perguntar o que já existe, por onde começar ou quais peças combinar.
Consulta o inventário do Manual e verifica contratos dos candidatos antes de
recomendar método, briefing, API pública ou composição. A resposta informa
cobertura, evidências, lacunas e próxima ação; não importa helpers nem executa análises.

Exemplo: “O que o Hub tem para conferir nulos e duplicidades antes de modelar?”
Templates de recomendação, handoff e registro de busca ficam no
[pacote da skill](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md).

---

### `hub-ml-eda-profissional` — Exploração Completa e Visual

- **O que faz:** estrutura EDA com volumetria, qualidade, cardinalidade, distribuições, relações e síntese executiva.
- **Templates:** `roteiro_eda.md`, `matriz_graficos_eda.md`, `relatorio_executivo_eda.md` e `estilo_visual_eda.md`.
- **Helpers recomendados:** `hub_scripts.skill_execution`, `hub_scripts.quick_profile`, `hub_scripts.data_quality_check`, `hub_snippets.spark.null_summary`, `hub_snippets.spark.smart_sample`, `hub_snippets.spark.safe_display`, `hub_snippets.display.correlation_matrix`, `hub_snippets.display.distribution_grid`, `hub_snippets.visual.theme_plotly`, `hub_snippets.visual.index_generator` e `hub_snippets.constants.format_br`.
- **Caso de Uso Real:**
  > *“Recebi uma tabela de sinistros com muitas colunas. Preciso entender grão, qualidade, distribuições e relações com o valor pago antes de formular hipóteses.”*

---

### `hub-ml-cross-eda-ml` — Cruzamento de Bases e Prontidão para ML

- **O que faz:** inventaria fontes, avalia cobertura de chaves, cardinalidade, viabilidade temporal do join e prontidão para modelagem.
- **Templates:** `inventario_edas.md`, `coverage_matrix.md`, `join_feasibility.md`, `readiness_scorecard.md`, `notebook_output_cross_eda.md` e `relatorio_executivo_cross_eda.md`.
- **Helpers recomendados:** `hub_snippets.spark.join_diagnostics`, `hub_snippets.spark.pit_join`, `hub_snippets.spark.null_summary`, `hub_snippets.spark.smart_sample`, `hub_snippets.spark.safe_display`, `hub_snippets.spark.psi_calculator`, `hub_scripts.quick_profile` e `hub_scripts.schema_to_yaml`.
- **Caso de Uso Real:**
  > *“Tenho tabelas transacional e cadastral. Quero medir correspondência, multiplicação de linhas, perda de entidades e disponibilidade temporal antes de construir a ABT.”*

> **Nota técnica:** `join_diagnostics` pertence a `hub_snippets.spark`, não a `hub_scripts`.

---

### `hub-ml-validacao-estatistica` — Rigor Matemático e Testes de Hipóteses

- **O que faz:** parte da decisão e do desenho do dado para escolher testes, conferir pressupostos, estimar efeito e comunicar incerteza.
- **Templates:** `test_plan.md`, `decisao_pressupostos.md`, `test_result_card.md`, `notebook_output_stat.md`, `relatorio_diagnostico.md` e `severity_rubric.md`.
- **Helpers recomendados:** `hub_snippets.spark.smart_sample`, `hub_snippets.spark.null_summary`, `hub_snippets.spark.psi_calculator`, `hub_snippets.ml.drift_detection` e `hub_snippets.constants.format_br`.
- **Caso de Uso Real:**
  > *“A taxa de conversão do grupo B foi maior. Quero decidir se a diferença é material, com teste adequado, tamanho de efeito, incerteza e limitações do desenho.”*

---

### `hub-ml-feature-engineering` — Engenharia de Atributos sem Leakage

- **O que faz:** desenha features com entidade, instante de decisão, disponibilidade das fontes, janelas e validações consistentes entre treino e inferência.
- **Templates:** `feature_spec_core.md`, `feature_spec_risco_validacao.md`, `feature_backlog_tiers.md`, `feature_taxonomy_cross_source.md`, `checklist_validacao_features.md`, `mapa_notebooks_alvo.md` e `notebook_output_structure.md`.
- **Helpers recomendados:** `hub_snippets.spark.pit_join`, `hub_snippets.spark.date_features`, `hub_snippets.ml.lgbm_temporal`, `hub_snippets.ml.split_temporal`, `hub_snippets.ml.woe_iv_calculator` e `hub_scripts.rfv_calculator`.
- **Caso de Uso Real:**
  > *“Preciso criar atributos de consumo em 30, 60 e 90 dias usando apenas informações disponíveis antes da data de decisão de cada cliente.”*

---

### `hub-ml-analise-safra` — Maturação e Curvas de Crédito (Vintage)

- **O que faz:** define evento, denominador, coorte, MOB, janela comparável e censura antes de construir curvas de safra.
- **Templates:** `relatorio_safra.md`.
- **Helpers recomendados:** `hub_snippets.ml.vintage_analysis`, `hub_snippets.spark.date_features`, `hub_snippets.constants.format_br` e `hub_snippets.visual.theme_plotly`.
- **Caso de Uso Real:**
  > *“Quero comparar contratos originados em diferentes trimestres após a mesma maturidade, distinguindo safras ainda incompletas.”*

---

### `hub-ml-baseline-ml` — Benchmark Inicial e Rastreabilidade

- **O que faz:** seleciona uma suíte compatível com classificação, regressão, séries, ranking, survival, clustering ou anomalias; define split, métricas, tracking e critério de comparação.
- **Templates:** incluem `suite_selection_guide.md`, `split_strategy.md`, famílias de métricas, `mlflow_checklist.md`, `notebook_output_baseline.md` e `relatorio_executivo_baseline.md`.
- **Helpers recomendados:** `hub_snippets.ml.split_temporal`, `hub_snippets.ml.walk_forward`, `hub_snippets.ml.metrics_report`, `hub_snippets.ml.curves_plotly`, `hub_snippets.ml.mlflow_run` e treinadores adequados ao tipo de problema.
- **Caso de Uso Real:**
  > *“Preciso de um baseline reproduzível para comparar abordagens mais complexas, mantendo população, split, métrica e custo sob o mesmo contrato.”*

---

### `hub-ml-explainability` — Explicabilidade de Modelos e SHAP

- **O que faz:** escolhe abordagem de explicação conforme modelo, público e decisão, separando leitura técnica e comunicação executiva.
- **Templates:** `shap_analysis_technical.md` e `relatorio_executivo_explainability.md`.
- **Helpers recomendados:** `hub_snippets.ml.explainability_report`, `hub_snippets.ml.shap_explainer` e `hub_snippets.ml.curves_plotly`.
- **Caso de Uso Real:**
  > *“Preciso explicar globalmente o comportamento do modelo e revisar uma previsão individual, deixando claro que contribuição não significa causalidade.”*

---

### `hub-ml-monitoramento-modelo` — MLOps e Detecção de Degradação

- **O que faz:** organiza performance, calibração, drift, fairness, latência, custo e critérios de decisão de retreino.
- **Templates:** `drift_report.md` e `retreino_decision.md`.
- **Helpers recomendados:** `hub_snippets.ml.performance_monitor`, `hub_snippets.ml.drift_detection`, `hub_snippets.spark.psi_calculator`, `hub_snippets.ml.metrics_report`, `hub_snippets.ml.curves_plotly` e `hub_scripts.drift_detector`.
- **Caso de Uso Real:**
  > *“Quero comparar população e performance ao longo do tempo e produzir evidências para uma decisão humana de manter, investigar ou retreinar.”*

A skill não agenda o monitoramento, não envia notificações e não retreina automaticamente.

---

### `hub-ml-pipeline-builder` — Industrialização e Lakeflow

- **O que faz:** transforma lógica experimental em contratos por camada, processamento incremental, qualidade, observabilidade e automação.
- **Templates:** `pipeline_spec.md`.
- **Helpers recomendados:** `hub_scripts.data_quality_check`, `hub_scripts.naming_checker`, `hub_scripts.schema_to_yaml` e `hub_snippets.spark.safe_display`.
- **Caso de Uso Real:**
  > *“Quero decompor um notebook em pipeline incremental, definir expectativas, observabilidade e tarefas de Lakeflow Jobs antes de implantar.”*

Use a nomenclatura vigente: **Lakeflow Spark Declarative Pipelines**, **Lakeflow Jobs** e **Declarative Automation Bundles**.

---

### `hub-ml-comentar-notebook` — Documentação Executiva e Técnica

- **O que faz:** cria narrativa antes do código e interpretação depois da execução, sem alterar silenciosamente o comportamento do notebook.
- **Templates:** `cabecalho_notebook.md`, blocos pré e pós-código nas versões completa e compacta.
- **Helpers recomendados:** `hub_scripts.doc_coverage`, componentes de `hub_snippets.visual` e `hub_snippets.constants.format_br`.
- **Caso de Uso Real:**
  > *“Tenho um notebook técnico extenso. Quero documentar objetivo, lógica e resultados para públicos técnico e executivo, preservando o código.”*

---

### `hub-ml-tutor-databricks` — Mentoria Técnica e Didática

- **O que faz:** explica código, notebooks, erros, Spark, Databricks e conceitos de ML no nível adequado ao leitor.
- **Templates:** `explicacao_bloco_codigo.md`, `explicacao_notebook.md` e `analogias_banking_crm.md`.
- **Helpers recomendados:** `hub_snippets.spark.safe_display`, `hub_snippets.spark.smart_sample` e `hub_snippets.constants.format_br`, apenas quando a demonstração prática exigir.
- **Caso de Uso Real:**
  > *“Minha consulta com join está lenta. Quero entender o plano, broadcast, shuffle e skew antes de escolher uma alteração.”*

Analogias facilitam a compreensão, mas não substituem o comportamento técnico real.

---

### `hub-ml-auditoria-skills` — Guardiã da Qualidade das Entregas

- **O que faz:** opera em dois modos: audita a implementação de uma skill ou audita o output que ela produziu.
- **Templates:** `rubrica_universal.md`, `checkpoints_por_skill.md` e `relatorio_auditoria.md`.
- **Helpers recomendados:** `hub_scripts.doc_coverage` e `hub_scripts.naming_checker`; `MANUAL_TECNICO.md#catalogo-helpers` é referência documental, não helper executável.
- **Caso de Uso Real:**
  > *“A Genie Code gerou um notebook. Quero confrontar pedido, metodologia, código, resultados e limitações antes de aceitar a entrega.”*

---

### `hub-ml-criar-objeto` — Fábrica de Expansão do Hub

- **O que faz:** orienta a criação ou alteração de snippet, script, prompt, README, notebook ou skill usando os padrões do Hub.
- **Templates:** `checklist-objeto-novo.md` e os moldes em `hub_padroes/`.
- **Documentação:** snippet, script ou prompt novo deve incluir README local no contrato 1.0.0.
- **Helpers recomendados:** variam conforme o tipo criado; a própria skill lista recursos de estrutura, teste, visual e documentação.
- **Caso de Uso Real:**
  > *“Desenvolvi uma função de LTV útil para a equipe. Quero estruturá-la com API pública, exemplo sintético, testes, documentação e revisão.”*

Gerar ou editar arquivos é uma ação explícita e sujeita à aprovação; a skill não cria artefatos silenciosamente.

---

## ❓ Perguntas Frequentes (FAQ)

### 1. Como a skill sabe quais colunas utilizar?

As skills trabalham em colaboração com você. Declare tabela, grão, chave, target, instante de decisão, período e filtros. Quando um dado estiver ausente, a metodologia pode orientar a inspeção do schema ou perguntas objetivas; isso não autoriza inventar regra de negócio.

### 2. O que acontece se eu não colocar `@` antes do nome da skill?

A Genie Code pode selecionar uma skill pela relevância entre o pedido e sua `description`. Se você quer uma metodologia específica, use `@nome-da-skill`. A `@menção` explicita a escolha, mas a entrega continua sujeita a revisão.

### 3. Posso combinar duas ou mais skills na mesma conversa?

Sim, preferencialmente em etapas: EDA, feature engineering, baseline, explicabilidade ou monitoramento. Reutilize apenas premissas já validadas e abra um chat novo quando objetivo, dados ou fase mudarem materialmente.

### 4. O que fazer se a saída precisar de adaptações do meu projeto?

Declare as regras e peça a alteração. Depois confira se o refinamento preservou grão, temporalidade, segurança e critérios de aceite. Guardrails não tornam toda adaptação automaticamente correta.

### 5. A equipe pode editar as instruções de uma skill existente?

Sim. Atualize `SKILL.md` e os recursos relacionados, valide o frontmatter e execute testes de roteamento positivo, negativo e por `@menção`. Mudanças recém-publicadas devem ser verificadas em uma conversa nova.

### 6. A skill executa os helpers citados automaticamente?

Não. Ela orienta a Genie Code e pode recomendar caminhos. O notebook precisa configurar `sys.path`, importar o módulo e executar a chamada, respeitando dependências, permissões e aprovações.

---

<a id="-aprovações-permissões-e-revisão"></a>

## 🔐 Aprovações, Permissões e Revisão

- Uma skill não amplia permissões no workspace ou no Unity Catalog.
- Planejar, gerar código, editar notebook, executar e persistir são ações diferentes.
- A política de aprovação configurada continua valendo para as ferramentas disponíveis.
- Autoaprovação reduz confirmações; não é uma fronteira de segurança.
- Revise qualquer `CREATE`, `ALTER`, `DROP`, `DELETE`, `MERGE`, instalação, execução ampla ou mudança de configuração.
- Não inclua tokens, senhas, chaves ou dados sensíveis em skills, templates ou prompts.

---

## 🔗 Continue Explorando

- [Documentação oficial de Agent Skills](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções customizadas na Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Hub Prompts](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_prompts/README.md)
- [Hub Snippets](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_snippets/README.md)
- [Hub Scripts](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_scripts/README.md)
- Catálogo de Helpers: `.assistant/MANUAL_TECNICO.md#catalogo-helpers`


## R0083 · ambiente_fonte/.assistant/skills/README.md

![CRM — Missão Modelos Analíticos CRM](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/../hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

## R0239 · ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/arquitetura_e_decisao.md

# Arquitetura do Concierge integrado

**Integração Git autorizada em 12/09/2026, registrada no ADR-0011.** Este guia é distribuído com a skill; o registro decisório vive em `docs/decisions/ADR-0011-concierge-hub.md` no repositório. Integração não é homologação no Databricks.

## Problema e objetivo

O usuário quer melhorar o uso do Hub existente. A pessoa descreve uma necessidade; o Concierge encontra capacidades e recomenda uma composição, inclusive quando nenhuma skill isolada cobre o pedido.

## Desenho escolhido

Pedido -> escopo/versão -> mapa semântico existente -> shortlist -> verificação de contratos -> composição mínima -> recomendação/handoff.

O procedimento é implementado em `SKILL.md`. Referências aprofundam busca e composição; templates padronizam entregas. O assistente utiliza ferramentas de leitura existentes. Não há novo modelo, serviço, indexador, registry autoral, banco vetorial ou dependência de compute nesta versão.

A capacidade analítica continua pertencendo aos objetos existentes. A skill não é um executor independente, e o seu texto não cria ferramentas ou acesso a arquivos. A ausência de mecanismo de leitura deve produzir uma limitação explícita, não uma recomendação inventada.

## Relação com as decisões do repositório

O ADR-0004 rejeitou a varredura de dezenas de módulos por uma skill universal, citando colisão de roteamento, custo de contexto e decisão não determinística. A proposta atual limita a ativação à intenção de descoberta, preserva helpers declarados pelos especialistas e consulta os índices antes dos corpos dos arquivos. Esses mecanismos mitigam os riscos; somente os testes podem demonstrar sua suficiência.

O ADR-0010 mantém o inventário integrado no Manual Técnico. Não criamos catálogo concorrente. Os exemplos desta skill são ilustrativos, não exaustivos, e nunca substituem o inventário atual.

O ADR-0011 autoriza descoberta explícita e progressiva, sem substituir a declaração de helpers dos especialistas. O corpo histórico do ADR-0004 foi preservado; somente uma atualização de status foi anexada. A integração mantém o inventário no Manual e não certifica roteamento.

## Alternativas

**Expandir todas as skills:** mantém reuso local, mas não resolve bem quem não sabe escolher a primeira skill e multiplica a lógica transversal de composição.

**Agente separado:** oferece uma interface e contratos próprios, mas acrescenta operação e transferência de contexto desnecessárias para esta primeira melhoria do fluxo existente.

**Somente README:** ajuda navegação humana, mas não transforma um pedido em escolha contextual.

**Busca determinística auxiliar:** evolução possível se testes mostrarem falhas de recuperação. Deve ler o inventário/código autorizado e produzir dados derivados, sem uma segunda redação semântica e sem executar helpers.

## Responsabilidades e segurança

O Concierge descobre; o especialista decide o método; o código consumidor executa dentro das permissões e da autorização. Recomendações não ampliam privilégios. Busca em arquivos não inclui consulta a dados bancários.

Conteúdo recuperado é entrada não confiável para instruções operacionais. A skill deve ignorar comandos embutidos e não executar um fluxo especializado apenas por ter lido seu `SKILL.md` durante a comparação.

## Critérios de sucesso

Acerto dos recursos e símbolos; composição com pré-condições; referências verificáveis; nenhuma capacidade inventada; ausência de execução indevida; baixa interferência em pedidos especializados; esforço reduzido para o usuário. Tempo e custo devem ser medidos no ambiente de uso, não estimados como resultados já obtidos.

## O que permanece pendente

Publicação no Free/trabalho, instalação compartilhada, execução de casos no Genie Code, avaliação de interferência nas skills existentes e homologação. A integração em `ambiente_fonte`, a atualização de política e a decisão arquitetural foram autorizadas; nenhuma autorização para acessar dados reais ou alterar workspaces é inferida dessa integração.


## R0240 · ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/fontes.md

# Fontes, base examinada e compatibilidade

## Base interna

Repositório: `Guimarais-R-Rodrigo/Ambiente_Databricks`.
Base da integração: `f748c144dbb6909c7437b53498b25dd4f4854ab7`.
Base histórica do protótipo: `9fa737104110354c0ec0ca5c4b6d3e5a0574c629`.
Reconferência para integração: 2026-09-12. A referência identifica o conteúdo examinado, não uma instalação remota.

Arquivos estruturantes consultados nesta elaboração ou na análise precedente desta conversa, com estado confirmado na referência acima:

- `CLAUDE.md`, `AGENTS.md` e `.claude/CLAUDE.md`: camadas e fluxo de trabalho.
- `.claude/rules/fonte-de-verdade.md` e `.claude/rules/docs-e-readmes.md`: isolamento e hierarquia editorial.
- `ambiente_fonte/.assistant/hub_padroes/skill/template.md`: corpo, frontmatter conservador, recursos relativos e testes.
- `docs/decisions/ADR-0004-declaracao-explicita-de-helpers.md`: risco da descoberta universal e declaração de helpers.
- `docs/decisions/ADR-0010-manual-tecnico-unificado.md`: inventário integrado e redação única.
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`, seções `catalogo-helpers` e `metodos`: mapa de recursos.
- READMEs de `.assistant`, `skills`, `hub_scripts`, `hub_snippets` e `hub_micromodelos`: escopos e formas de ativação.
- `tools/project_policy.py`, `tools/validate_assistant.py` e `docs/testes/forward/README.md`: integração futura e distinção dos gates.

Esses caminhos são referências no repositório, não promessas de disponibilidade dentro de um pacote instalado isoladamente. Na operação, o Concierge deve conferir o Hub efetivamente acessível.

## Fontes oficiais

**D1. Databricks — Extend Genie Code with agent skills.** Reconferida em 2026-09-12; documentação em inglês atualizada em 2026-09-11.
https://docs.databricks.com/gcp/en/genie-code/skills

Sustenta o mecanismo de seleção por relevância ou menção, os locais de instalação e o uso de recursos relativos. A documentação admite scripts, mas esta versão usa somente instruções e ferramentas de leitura já disponíveis.

**D2. Agent Skills — Specification.** Reconferida em 2026-09-12.
https://agentskills.io/specification

Sustenta o formato básico e a separação progressiva dos recursos. O padrão admite campos opcionais; o Hub adota um subconjunto conservador de frontmatter, preservado aqui.

## Convenções próprias, não recursos nativos

As rotas `DIRECT_ROUTE`, `HELPER_ROUTE`, `COMPOSITE_ROUTE`, `BRIEFING_FIRST`, `GAP` e `ACCESS_BLOCKED`, a variável conceitual `HUB_ROOT`, os templates, o limite inicial de shortlist e a rubrica de confiança são convenções deste pacote. Não são APIs nem garantias oficiais da Databricks.

## Limites de compatibilidade

O procedimento depende de leitura/pesquisa que o assistente realmente consiga realizar. A skill não cria essa capacidade, não garante acesso recursivo e não invoca outra skill por imprimir seu nome.

O verificador local usa Python 3.10+ e biblioteca padrão. Não exige Spark, MLflow, credenciais ou conectores. Seu sucesso não certifica roteamento, qualidade de recomendações, permissões ou execução Databricks. Não houve homologação dessas superfícies nesta entrega.

Os testes e exemplos não contêm dados reais. Evidências futuras devem preservar essa separação e evitar identidades corporativas, segredos ou payloads de clientes.


## R0241 · ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/instalacao_testes_promocao.md

# Instalação e aceite do Concierge integrado

## Estado e próxima ação

A versão de manutenção é `ambiente_fonte/.assistant/skills/hub-ml-concierge/`.
A integração em Git foi autorizada em 12/09/2026. A cópia em
`novas_funcionalidades/` é histórica; não a instale em paralelo. Não houve
publicação no Free, no trabalho ou em escopo compartilhado nesta integração.

Para conferir o pacote localmente, siga [Testes](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/../tests/README.md).
Para revisar o procedimento, leia [SKILL.md](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/../SKILL.md). A interface e as
condições oficiais estão em [Fontes](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/docs/fontes.md).

## Revisão sem instalação

Fornecer SKILL.md e seus recursos como contexto permite ensaiar o procedimento.
Isso não comprova seleção nativa por relevância nem por menção. Resultados de
simulação devem ser separados dos forward tests observados no Genie Code.

## Instalação pessoal de teste — ação futura autorizada separadamente

Use o fluxo de publicação do repositório, com validação da fonte e conferência
do espelho gerado. Não execute publicação no trabalho a partir deste guia.
A alternativa manual abaixo é somente para teste pessoal controlado:

1. Confirme ambiente, escopo e permissão. Use documentação autorizada e dados
   sintéticos. Preserve versões existentes antes de qualquer substituição.
2. Em Genie Code, use Settings -> Open skills folder quando disponível. O local
   pessoal documentado é `/Users/<username>/.assistant/skills/`; o compartilhado
   é `Workspace/.assistant/skills/`. Não transforme esses endereços em paths
   Python mecanicamente.
3. Copie somente a pasta canônica `hub-ml-concierge/`, preservando os caminhos
   relativos. SKILL.md, references e templates precisam estar disponíveis;
   mantenha o pacote completo para que documentação e testes continuem acessíveis.
4. Confirme também a instalação do Manual e dos componentes do Hub acessíveis ao
   assistente. Uma skill instalada sem arquivos/ferramentas de leitura não conhece
   o repositório por si. Não use o pacote histórico como fonte de helpers.
5. Abra chat novo, teste `@hub-ml-concierge` e depois os casos sem menção. Se a
   interface mantiver metadados antigos, atualize a página e abra novo chat.
6. Registre carregamento observado separadamente da resposta. O nome impresso
   pela IA não comprova ativação. Sem evidência, use NÃO VERIFICADO.

Não é necessário instalar bibliotecas analíticas para executar o procedimento
textual. O acesso de leitura depende das capacidades do assistente e das ACLs.

## Aceite e compartilhamento

O roteiro geral do repositório recebeu os casos 14P, 14N e 14M. A matriz detalhada
em `tests/casos_aceite.json` contém cenários de descoberta, colisão, versão e
segurança; expectativas continuam PENDENTE até execução registrada separadamente.
Reexecute os negativos das skills vizinhas e os testes afetados pelas instruções.
Os resultados antigos de outras skills não homologam o conjunto ampliado.

Antes de compartilhar com a squad, cumpra revisão independente e gates do
repositório. Produção, publicação compartilhada e dados reais continuam sujeitos
à autorização e à avaliação no ambiente de destino.

## Manutenção e rollback

Edite a fonte canônica. Atualizações do inventário pertencem ao Manual; sincronize
sua cópia da raiz quando ele mudar. Valide e regenere o simulado pelo renderer,
nunca editando a árvore derivada à mão. Registre mudanças no changelog canônico.

Para retirar um teste pessoal, remova/desative somente a instalação do Concierge
previamente identificada, com backup, e abra novo chat. Não remova outras skills.
No Git, reverta a integração em commit próprio e ajuste seus consumidores; apagar
um arquivo no Git não o retira automaticamente do workspace.


## R0087 · ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/README.md

# Testes do Concierge

## Duas evidências diferentes

O verificador estático confere a estrutura do pacote. Os casos de `casos_aceite.json` avaliam comportamento humano/conversacional e continuam pendentes até execução registrada. Expectativa escrita não é resultado de teste.

## Executar localmente

Na raiz do checkout, com Python 3.10+ e sem instalar dependências:

```bash
python ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/validar_pacote.py
python -B -m unittest discover -s ambiente_fonte/.assistant/skills/hub-ml-concierge/tests -p "test_*.py" -v
```

`validar_pacote.py` retorna 0 quando não encontra falhas estruturais; retorna 1 quando encontra defeitos. Os testes de regressão usam cópias temporárias do pacote, sem editar o produto. Não precisam de Spark, credenciais, rede ou dados reais.

## O que o verificador confere

Arquivos mínimos, frontmatter conservador, nome/pasta, tamanho da descrição, seções do corpo, limite de linhas, sintaxe Python, links Markdown locais, ausência de links que escapem do pacote e estrutura da matriz de aceite. A verificação de links não testa URLs externas nem âncoras Markdown.

Não confere correção semântica de toda recomendação, existência atual dos helpers no destino, roteamento nativo, ACLs ou execução Databricks. Não substitui `tools/validate_assistant.py`. O CI canônico executa este verificador, suas regressões e os testes de integração em `tools/tests/test_concierge_integracao.py`.

## Roteamento e qualidade

Para positivos, negativos e menções, use chats novos numa instalação pessoal autorizada. Registre skill efetivamente carregada separadamente do texto produzido. Negativo passa somente se Concierge não assumir a tarefa; isso não prova que outro especialista foi corretamente carregado.

Casos `edge` podem ser ensaiados com contexto fornecido ou ferramentas controladas. Não use uma falha real de acesso como justificativa para inventar uma resposta. Para cada caso, salve fora de dados sensíveis: id, commit do pacote e do Hub, superfície, prompt, contexto fornecido, carregamento observado, resposta, recursos/evidências, veredito, motivo e limitações. Use `PASS`, `FAIL`, `BLOQUEADO` ou `NÃO VERIFICADO`.

## Critério para homologação no workspace

Zero recursos/símbolos inventados; zero execução ou escrita indevida; zero interpretação de acesso bloqueado como inexistência; todos os negativos preservam a fronteira do especialista; cada recomendação principal possui evidência de existência e adequação, ou ressalva explícita. Casos compostos precisam demonstrar os contratos ou declarar o plano como conceitual.

Faça pelo menos duas rodadas independentes dos positivos, negativos e menções para observar variação; casos de segurança devem ser repetidos. Avalie utilidade, esforço do usuário e custo/latência no destino. Metas adicionais podem ser pactuadas após baseline, sem atribuir precisão estatística a uma amostra pequena.

## Registro desta entrega

Consulte [RESULTADOS](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/RESULTADOS.md). Não reutilize os resultados históricos das skills canônicas como certificação do Concierge.


## R0248 · ambiente_fonte/.assistant/skills/hub-ml-concierge/tests/RESULTADOS.md

# Resultados — Concierge Hub 0.2.0

Data: 2026-09-12. Base de integração:
`f748c144dbb6909c7437b53498b25dd4f4854ab7`.
Ambiente local: Python 3.13.5, Linux. Sem credenciais ou chamadas Databricks.

## Verificações executadas

Validador estático do pacote:

```text
PASS: estrutura, frontmatter, links locais, sintaxe e matriz de aceite.
NAO VALIDADO: roteamento, recomendacoes reais, Databricks e permissoes.
```

Regressões do verificador: 14 testes, zero falhas, zero skips.
Incluem as 12 regressões do protótipo e dois casos novos: raiz simbólica
recusada antes de resolver o path e divergência entre categoria/ativação da matriz.
A cópia histórica e seus resultados não foram reescritos.

Integração canônica: 12 testes, zero falhas, zero skips, executados pelo arquivo
`tools/tests/test_concierge_integracao.py` no checkout. Conferem política,
frontmatter, rota opcional nas instruções, inventário/cópia do Manual, caminhos
de helpers, símbolos públicos, matriz pendente, fonte/espelho e estágios do CI.
Não importam os helpers nem testam sua execução no workspace.

## Matriz conversacional

26 casos preparados: 7 positivos, 4 negativos, 2 menções e 13 casos de borda.
Todos continuam PENDENTE como expectativas; não são resultados de uso do Genie.
O caso E13 explicita comando de execução embutido em documento recuperado, sem
confundi-lo com uma autorização nova dada pelo usuário.

Os casos básicos 14P/14N/14M foram acrescentados ao roteiro do repositório.
O 39/39 antigo permanece histórico; não representa aprovação da nova skill nem
do conjunto ampliado. Regressões das vizinhas e do mapa de instruções no destino
permanecem pendentes.

## Limites

Integração Git, não instalação ou homologação. Não houve publicação no Free ou
no trabalho, alteração de ACL, consultas, treinamento ou chamadas remotas.
O relatório de integração do repositório registra o CI completo separadamente
em `docs/testes/2026-09-12_concierge-integracao.md`. A presença de um arquivo,
a correção estática e a execução conversacional continuam evidências distintas.


## R0086 · ambiente_fonte/.assistant/skills/hub-ml-concierge/README.md

# Concierge Hub

## R0091 · ambiente_fonte/.assistant/skills/hub-ml-micromodelos/README.md

# Micromodelos — contrato L1

## R0214 · ambiente_fonte/.assistant/skills/hub-ml-baseline-ml/SKILL.md

## Rota executável sintética SER09 (candidata)

## R0214 · ambiente_fonte/.assistant/skills/hub-ml-baseline-ml/SKILL.md

## Tracking sintético pessoal SER10 (candidato)

## R0214 · ambiente_fonte/.assistant/skills/hub-ml-baseline-ml/SKILL.md

no perfil SER09

## R0214 · ambiente_fonte/.assistant/skills/hub-ml-baseline-ml/SKILL.md

autorização. O bloqueio observado no Free em 17/08/2026 é histórico;
  confirme

## R0232 · ambiente_fonte/.assistant/skills/hub-ml-comentar-notebook/SKILL.md

vem da saída real — foi assim que uma tabela rotulada "saída real" nasceu com
  valores extrapolados.

## R0238 · ambiente_fonte/.assistant/skills/hub-ml-concierge/SKILL.md

A cópia histórica em `novas_funcionalidades/` não é a raiz dos helpers nem
a versão de manutenção desta skill.

## R0238 · ambiente_fonte/.assistant/skills/hub-ml-concierge/SKILL.md

componentes V04

## R0238 · ambiente_fonte/.assistant/skills/hub-ml-concierge/SKILL.md

contrato V06

## R0238 · ambiente_fonte/.assistant/skills/hub-ml-concierge/SKILL.md

consumidores V07

## R0249 · ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md

policy e `current_level=L2` continuam inalterados.

## R0249 · ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md

com o
sintoma aparecendo sprints depois da causa.

## R0249 · ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md

sem ler a assinatura. Foi assim
  que nove notebooks desta biblioteca nasceram quebrados.

## R0249 · ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md

A do catálogo é a mais esquecida: dois objetos ficaram fora dele por uma sprint
inteira, indescobríveis pela rota que o próprio README recomenda.

## R0251 · ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/SKILL.md

a rota SER06

## R0258 · ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md

comprovante SE04 íntegro

## R0263 · ambiente_fonte/.assistant/skills/hub-ml-explainability/SKILL.md

## Rota executável candidata

## R0263 · ambiente_fonte/.assistant/skills/hub-ml-explainability/SKILL.md

Sistema de Temas V07

## R0266 · ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/SKILL.md

## Executar o perfil temporal sintético B1

## R0266 · ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/SKILL.md

a rota SER06

## R0274 · ambiente_fonte/.assistant/skills/hub-ml-micromodelos/SKILL.md

Execução de runtime E1 exige pacote e prova separada;
   E2 fica fora da missão.

## R0274 · ambiente_fonte/.assistant/skills/hub-ml-micromodelos/SKILL.md

e, nesta missão, dados
sintéticos. Metadata MM03

## R0274 · ambiente_fonte/.assistant/skills/hub-ml-micromodelos/SKILL.md

`E1_EXECUTADO` conforme o caso real; `E2_NAO_EXECUTADO`.

## R0275 · ambiente_fonte/.assistant/skills/hub-ml-monitoramento-modelo/SKILL.md

## Rota executável sintética SER11 (candidata)

## R0275 · ambiente_fonte/.assistant/skills/hub-ml-monitoramento-modelo/SKILL.md

## Candidato executável SER12 — performance com labels maduras

## R0280 · ambiente_fonte/.assistant/skills/hub-ml-tutor-databricks/SKILL.md

Slash command registrado
  pelo usuário, hook e memória automática **não existem** no Genie Code.

## R0284 · ambiente_fonte/.assistant/skills/hub-ml-validacao-estatistica/SKILL.md

## Execução verificável SER04 (perfil piloto)

## R0243 · ambiente_fonte/.assistant/skills/hub-ml-concierge/references/descoberta.md

# Descoberta progressiva e evidências


## R0249 — complemento de revisão

A lista é **fechada**: seis tipos, e nada fora dela. Escolher errado custa a
reescrita inteira, porque a forma muda.

| O objeto… | é | template |
|---|---|---|
| recebe DataFrame ou valores e devolve resultado | **snippet** | `hub_padroes/snippet/template.md` |
| recebe o **endereço do que vai diagnosticar** e devolve um veredito | **script** | `hub_padroes/script/template.md` |
| é texto que a pessoa preenche e cola no chat | **prompt** | `hub_padroes/prompt/template.md` |
| explica uma pasta para quem chega | **README** | `hub_padroes/readme/template.md`; escala Objeto: `template_objeto.md` na mesma pasta |
| ensina a usar um objeto, executando | **notebook** | `hub_padroes/notebook/template.py` |
| é instrução que o Genie Code carrega sozinho | **skill** | `hub_padroes/skill/template.md` |

A distinção entre snippet e script é a que mais erra, e ela muda a assinatura:
snippet recebe **dado já carregado**; script recebe o **endereço** — nome de
tabela, tipicamente, ou caminho de arquivo, como faz `hub_scripts.doc_coverage`.
Na dúvida, pergunte quem chama: se for um notebook passando um DataFrame que ele
já tem, é snippet.


## R0214 — complemento de revisão

  modelo seguinte vale o custo.
- **Instalar biblioteca opcional sem fixar versão** onde o inventário manda fixar
  — `shap`, `umap-learn` e `pmdarima` exigem pin, e as três juntas quebram o
  `import numpy`.
- **Abrir run de MLflow no serverless** sem conferir runtime, backend e
  autorização. O bloqueio observado no Free em 17/08/2026 é histórico;
  confirme a configuração do perfil executável antes de prometer tracking.
