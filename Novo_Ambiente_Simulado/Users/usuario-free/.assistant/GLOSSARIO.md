# Glossário — plataforma, modelagem e convenções do Hub

Use a procedência antes da definição. Um termo de **plataforma** vem da
Databricks; um termo de **modelagem** independe de ferramenta; uma
**convenção do Hub** só existe neste pacote.

[Voltar ao guia do ecossistema](README.md)

## Plataforma Databricks

| Termo | Significado neste guia |
|---|---|
| **Genie Code** | Assistente de código e dados do Databricks para pessoas técnicas. Pode planejar, buscar contexto, gerar e executar código conforme permissões e aprovações. |
| **Genie One** | Experiência conversacional voltada a usuários de negócio. Não é o destinatário deste pacote. |
| **Genie Agent** | Ambiente de dados e semântica configurado para perguntas de negócio. Não é sinônimo de Genie Code. |
| **Agent Skill** | Pasta no padrão aberto Agent Skills, com `SKILL.md` obrigatório e recursos opcionais, carregada quando relevante ou por `@menção`. |
| **`SKILL.md`** | Arquivo que declara `name`, `description` e instruções da skill. Pode referenciar outros arquivos relativos à raiz da skill. |
| **Frontmatter** | Metadados YAML entre delimitadores `---` no início do `SKILL.md`. |
| **`description`** | Campo que descreve o que a skill faz e quando usá-la; participa da decisão de relevância. Descrição alterada exige novo teste de roteamento. |
| **Skill de usuário** | Skill em `/Users/<username>/.assistant/skills/`, disponível apenas para a pessoa. |
| **Skill de workspace** | Skill em `Workspace/.assistant/skills/`, compartilhada conforme permissões administradas. |
| **Instruções pessoais** | `.assistant_instructions.md` no diretório do usuário; preferências persistentes aplicadas às interações suportadas. |
| **Instruções de workspace** | `Workspace/.assistant_workspace_instructions.md`, administrado para orientar o workspace e geralmente priorizado sobre instruções pessoais quando houver sobreposição. |
| **`AGENTS.md` / `CLAUDE.md`** | Contexto de projeto descoberto na árvore do arquivo aberto. A localização define o escopo. |
| **`@menção`** | Referência explícita no prompt a skill, arquivo, tabela ou outro recurso oferecido pela interface. |
| **Quick Fix / Autocomplete** | Superfícies às quais as instruções pessoais e de workspace não se aplicam, segundo a documentação oficial atual. |
| **Inline suggestions / Suggest Fix** | Superfícies às quais as instruções se aplicam, além do chat. Não confundir Suggest Fix com Quick Fix. |
| **Agent mode** | Modo em que o Genie Code conduz tarefas em múltiplas etapas e pode usar ferramentas ou executar código, sujeito a permissões e configuração de aprovação. |
| **Unity Catalog** | Camada de governança de catálogos, schemas, tabelas, permissões e linhagem. Origina o nome de três níveis `catalog.schema.table`. |
| **Serverless** | Compute gerenciado. Suporte de API e bibliotecas depende do runtime e deve ser verificado no destino. |
| **Spark Connect** | Arquitetura cliente-servidor usada em runtimes gerenciados; algumas APIs clássicas do driver/JVM podem não estar expostas. |
| **MLflow** | Ecossistema de tracking, avaliação e ciclo de vida de modelos e aplicações de IA. |
| **Lakeflow Spark Declarative Pipelines** | Framework declarativo para pipelines, qualidade e observabilidade. Nome anterior: Delta Live Tables. |
| **Declarative Automation Bundles** | Definição versionável de recursos e destinos de implantação. Nome anterior: Databricks Asset Bundles. |
| **Git folder** | Repositório Git no workspace; é controle de versão, não diretório nativo de descoberta de skills. |
| **MCP** | Protocolo para conectar ferramentas e fontes externas. No Genie Code, a configuração é feita em Settings; nunca versione tokens. |

## Estatística e machine learning

| Termo | Significado prático |
|---|---|
| **Grão** | O que uma linha representa. Toda análise deve declará-lo antes de contar ou juntar. |
| **Target** | Evento ou valor que o modelo tenta prever, com classe positiva e horizonte explícitos. |
| **Leakage** | Informação indisponível no instante de decisão entrando no treino ou na validação. |
| **Split temporal** | Separação de treino e teste por tempo, em vez de sorteio de linhas. |
| **Walk-forward** | Validação que avança por janelas temporais e imita retreino e uso futuro. |
| **Point-in-time / as-of join** | Junção que considera apenas informação já disponível no instante da decisão. |
| **Atraso de publicação** | Intervalo entre a referência do dado e sua disponibilidade real; ignorá-lo cria leakage. |
| **Fator de expansão** | Razão entre linhas após e antes de um join; acima de 1 indica multiplicação da esquerda. |
| **Baseline** | Modelo de referência simples contra o qual uma solução mais complexa deve justificar custo. |
| **Drift** | Mudança na distribuição de dados, previsões ou relação com o target. Não implica sozinho queda de performance. |
| **PSI / CSI** | Índices de mudança de distribuição. Limiares são heurísticas que precisam de calibração. |
| **KS** | Maior distância entre distribuições acumuladas; pode ser diagnóstico ou métrica de separação, conforme o contexto. |
| **WOE / IV** | Transformação por peso de evidência e medida de poder de separação, comuns em scorecards. |
| **SHAP** | Método de atribuição de contribuição às previsões. Explica comportamento do modelo, não causalidade. |
| **Safra / vintage** | Grupo originado no mesmo período, comparado por tempo de maturação equivalente. |
| **MOB** | `Months on book`: tempo desde a originação, usado para alinhar safras. |
| **LambdaRank / NDCG** | Objetivo e métrica de ranking; tratam ordem dentro de grupos, não probabilidade de classe. |
| **Driver-side** | Cálculo na máquina coordenadora. Requer limite ou amostra para não concentrar dado excessivo. |

## Convenções deste projeto

Estes termos não são interfaces institucionais da Databricks.

| Termo | Significado |
|---|---|
| **`hub_` / `hub-`** | Prefixo de conteúdo criado neste projeto. Underscore em pacotes Python; hífen em nomes de skills. |
| **`ambiente_fonte/`** | Única cópia editável do produto. |
| **Simulado** | Árvore de workspace derivada da fonte por script. Nunca é editada à mão. |
| **Render** | Geração determinística do simulado a partir da fonte. |
| **Camada canônica** | Repositório e `ambiente_fonte/`, onde a mudança nasce e é versionada. |
| **Camada derivada** | `Novo_Ambiente_Simulado/`, recriado pelo render. |
| **Camada operacional** | Workspaces Free e de trabalho, que recebem cópias verificadas. |
| **Helper** | Função reutilizável em `hub_snippets` ou `hub_scripts`. |
| **Pasta de objeto** | Diretório com implementação, `__init__.py` e notebook de exemplo do mesmo objeto. |
| **Gate** | Evidência que precisa passar antes de avançar; cada gate prova uma propriedade delimitada. |
| **Forward test** | Teste conversacional de qual skill é carregada para pedido positivo, negativo e `@menção`. |
| **Smoke test** | Execução no runtime real para detectar falhas que análise local não revela. |
| **ADR** | Registro imutável de uma decisão arquitetural aceita; outra decisão o supersede sem apagá-lo. |
| **Handoff** | Passagem explícita de estado, bloqueio e próximo passo entre sessões ou agentes. |
| **Runbook** | Procedimento operacional copiável com pré-condições e critério de sucesso. |
| **`run_governado`** | Helper local para exigir metadados mínimos e isolar um run do MLflow. |

## Nomes que não devem virar promessa

| Expressão | Interpretação correta |
|---|---|
| `/eda`, `/baseline` e outros slash aliases locais | convenções de texto; não são comandos registrados |
| “memória do Hub” | não existe mecanismo próprio; há instruções, skills e contexto de projeto |
| “`hub_prompts` é auto-descoberto” | falso; o prompt precisa ser anexado ou copiado |
| “skill importa helper automaticamente” | falso para este pacote; o Python precisa importar a biblioteca |
| “passou no Free, então passa no trabalho” | falso; runtime, bibliotecas, ACLs e políticas precisam de nova evidência |

## Fontes oficiais

- [Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/)
- [Agent Skills no Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/skills)
- [Instruções customizadas](https://learn.microsoft.com/en-us/azure/databricks/genie-code/instructions)
- [Uso do Genie Code](https://learn.microsoft.com/en-us/azure/databricks/genie-code/use-genie-code)
- [Especificação Agent Skills](https://agentskills.io/specification)
