# Glossário

> **Documento customizado (`x_docs`), não auto-descoberto pelo Genie Code.**
> Consulte-o quando um termo aparecer sem explicação em qualquer README deste
> ecossistema. Para adicioná-lo ao chat, use `@` ou **Add context**.

Os termos deste projeto vêm de três procedências diferentes, e confundi-las é a
principal fonte de mal-entendido. Um termo de **plataforma** é oficial da
Databricks e você encontra na documentação deles. Um termo de **modelagem** é
vocabulário de estatística e machine learning, independente de ferramenta. Um
termo de **convenção** foi criado aqui e não existe fora deste repositório —
procurar por ele na documentação oficial não devolve nada.

## Plataforma — vocabulário oficial da Databricks

| Termo | O que é | Onde aparece aqui |
|---|---|---|
| **Genie Code** | Assistente de código do Databricks, integrado ao workspace. É ele quem lê as skills e as instruções. | É o destinatário de tudo neste ecossistema |
| **Agent Skills** | Padrão aberto (agentskills.io) para dar a um assistente instruções especializadas em pastas. A Databricks adotou o padrão. | As 12 pastas `rodrigo-*` em `skills/` |
| **`SKILL.md`** | Arquivo obrigatório de cada skill. Contém o cabeçalho de identificação e as instruções do fluxo. | Um por pasta de skill |
| **Frontmatter** | Bloco de metadados no topo do arquivo, delimitado por `---`. Aqui carrega `name` e `description`. Texto antes dele invalida o arquivo. | Primeiras linhas de todo `SKILL.md` |
| **Auto-descoberta** | Capacidade do Genie Code de encontrar e carregar um arquivo sozinho, sem você pedir. Vale para skills, instruções e `AGENTS.md` — e para mais nada. | Motivo do prefixo `x_` (ver convenção) |
| **`description`** | Campo do frontmatter que descreve quando a skill deve ser usada. É o **único** texto que o Genie Code lê para decidir qual skill carregar. | Determina o roteamento; alterá-la exige reteste |
| **`@menção`** | Digitar `@nome-da-skill` no chat força o carregamento daquela skill, sem depender da escolha automática. | Forma determinística de invocar uma skill |
| **Add context** | Botão do painel que anexa um arquivo, tabela ou notebook ao chat. É como conteúdo não auto-descoberto entra no contexto. | Junto com `@`, é o que traz `hub_prompts` e `x_docs` — nunca automático |
| **`/findTables`** | Comando nativo do Genie Code para localizar tabelas cujo nome você não sabe. | Não confundir com `/eda` e similares, que não existem |
| **Instruções pessoais** | Arquivo `.assistant_instructions.md` na sua pasta de usuário, com preferências aplicadas à maioria das interações. Limite de 20.000 caracteres. | Raiz de `ambiente_fonte/` |
| **`AGENTS.md`** | Arquivo de contexto de projeto, descoberto automaticamente ao abrir um arquivo e subir a hierarquia de diretórios. `CLAUDE.md` cumpre o mesmo papel. | Modelo em `x_projects/` |
| **Serverless** | Compute gerenciado pela Databricks, sem cluster para configurar. É o único disponível na Free Edition e tem restrições — não aceita `cache()`, por exemplo. | Onde os helpers foram testados |
| **Unity Catalog** | Camada de governança de dados: catálogos, schemas, tabelas, permissões e linhagem. Origem do padrão `catalog.schema.table`. | Exemplos de acesso a dados |
| **MLflow** | Ferramenta de registro de experimentos: parâmetros, métricas, artefatos e versões de modelo. | Skills de baseline e monitoramento |
| **Lakeflow Spark Declarative Pipelines** | Framework declarativo de pipelines, com expectativas de qualidade e log de eventos. Nome anterior: Delta Live Tables. | Skill de pipeline |
| **Declarative Automation Bundles** | Empacotamento versionável de jobs, pipelines e permissões, com ambientes separados. Nome anterior: Databricks Asset Bundles. | Skill de pipeline |
| **Git folder** | Repositório Git clonado dentro do workspace. Não é onde as skills são descobertas — é só uma cópia do código. | Rota recomendada de replicação |
| **Quick Fix / Autocomplete** | Sugestões pontuais do editor. Exceção oficial: instruções pessoais **não** se aplicam a elas. | Limite documentado das instruções |
| **Driver-side** | Calculado na máquina que coordena o job, não distribuído pelo cluster. Rápido em dado pequeno, e a forma clássica de derrubar um notebook quando o dado é grande. Helpers marcados assim esperam amostra, não a tabela inteira. | `hub_snippets.ml.drift_detection` |
| **Bronze / silver / gold** | Convenção de camadas: bronze recebe o dado bruto, silver limpa e padroniza, gold entrega pronto para consumo. É organização, não exigência da plataforma. | Skill de pipeline |
| **Expectations** | Regras de qualidade declaradas dentro do pipeline Lakeflow, que registram ou barram linhas fora do esperado. Diferente de checagem avulsa em notebook. | Skill de pipeline |
| **Readiness (para ML)** | Avaliação de se os dados sustentam modelagem: cobertura, alinhamento temporal, sinal e qualidade. Responde "dá para modelar?" antes de tentar. | Skill de cross-EDA |
| **Event log** | Tabela que um pipeline Lakeflow escreve sozinho, com um registro por evento de execução: expectations violadas, linhas processadas, falhas. É onde se investiga o que aconteceu numa rodada, sem instrumentar nada. | Fluxo de engenharia; limites de `hub_scripts` |
| **Target (de bundle)** | Ambiente de destino declarado num Declarative Automation Bundle — tipicamente `dev`, `homologação` e `prod`. Cada um aponta para catálogo, schema e permissões próprios, e é o que impede um deploy de desenvolvimento tocar produção. | Diagrama do fluxo de engenharia |
| **Autologging** | Registro automático de parâmetros, métricas e modelo pelo MLflow, ligado por padrão no Databricks. Ele intercepta o `fit` mesmo quando o código não pede nada — e é por isso que aparece como causa de falha com bibliotecas incompatíveis. | `docs/testes/spark/` |
| **PII** | *Personally identifiable information*: dado que identifica uma pessoa (CPF, nome, e-mail, telefone, endereço). Nunca entra neste repositório nem no laboratório Free, em nenhuma hipótese — placeholders sempre. | Regras de edição e checklists |

## Modelagem — vocabulário de estatística e ML

| Termo | O que é | Onde aparece aqui |
|---|---|---|
| **Leakage** | Vazamento de informação do futuro para o treino do modelo. Produz resultado excelente no teste e fracasso em produção. É o erro mais caro da área. | Proibição central das instruções e skills |
| **Split temporal** | Separação de treino e teste por período de calendário, não por sorteio de linhas. É o que impede leakage quando há tempo envolvido. | `hub_snippets.ml.split_temporal` |
| **Walk-forward** | Validação que avança no tempo, retreinando a cada janela, imitando o uso real do modelo. | `hub_snippets.ml.walk_forward` |
| **PSI / CSI** | Índices que medem o quanto uma distribuição mudou entre dois períodos. Não têm faixa universal de corte: o limite é calibrado por modelo e feature. | Monitoramento e comparação de safras |
| **KS** | Teste que mede a maior distância entre duas distribuições acumuladas. Usado tanto em diagnóstico quanto como métrica de separação. | Validação estatística e métricas |
| **Drift** | Mudança no comportamento dos dados ou do modelo ao longo do tempo. Drift de dados não implica queda de performance — são coisas distintas. | Skill de monitoramento |
| **WOE / IV** | Transformação de variável por peso de evidência e medida do seu poder de separação. Herança de crédito, comum em scorecards. | `hub_snippets.ml.woe_iv_calculator` |
| **Safra (vintage)** | Grupo de contratos ou clientes originados no mesmo período. Comparar safras exige alinhá-las pelo tempo de vida, não pelo calendário. | Skill de análise de safra |
| **MOB** | *Months on book*: meses decorridos desde a originação. É o eixo que torna safras comparáveis entre si. | Curvas de maturação |
| **Baseline** | Modelo simples de referência. Serve para saber se o modelo complexo compensa o custo que traz. | Skill de baseline |
| **Scorecard** | Modelo convertido em pontos legíveis por humanos, tradicional em crédito por ser auditável. | `hub_snippets.ml.scorecard_builder` |
| **Banda de score** | Faixas em que o score é agrupado para decisão. Exige declarar qual extremo representa maior risco. | `hub_snippets.ml.score_bands` |
| **SHAP** | Método que atribui a cada variável sua contribuição para uma previsão. Explica o modelo, não a causa do fenômeno. | Skill de explicabilidade |
| **Point-in-time** | Junção que usa apenas informação disponível no instante da decisão. É a forma correta de montar histórico sem leakage. | `hub_snippets.spark.pit_join` |
| **As-of join** | Nome técnico da junção point-in-time: para cada linha, traz a última versão do dado válida naquele momento. | `hub_snippets.spark.pit_join` |
| **Atraso de publicação** | Tempo entre o instante a que um dado se refere e o momento em que ele fica disponível. Um score de bureau com referência 10/01 e atraso de 2 dias só pode entrar em decisões a partir de 12/01; ignorá-lo cria vazamento mesmo com data de referência no passado. | `pit_join(atraso_publicacao_dias=...)` |
| **Fator de expansão** | Quantas vezes um join multiplica as linhas da esquerda. Acima de 1,0 há duplicação, e é como uma base de treino passa a superrepresentar entidades sem ninguém perceber. | `hub_snippets.spark.join_diagnostics` |
| **LambdaRank / NDCG** | Ranking, não classificação: o modelo aprende a **ordenar** os itens de um grupo (LambdaRank) e o NDCG mede se os mais relevantes ficaram no topo. Serve para "quem oferecer primeiro", não para "quem vai contratar". | `hub_snippets.ml.lgbm_ranker` |

## Convenção — criado neste projeto

Nenhum destes termos existe na documentação da Databricks.

| Termo | O que é | Onde aparece aqui |
|---|---|---|
| **Prefixo `hub_` / `hub-`** | Marca de conteúdo do Hub, **não** auto-descoberto. Exige ação manual: `@`, Add context, import ou execução. Underscore onde o Python importa; hífen onde a plataforma nomeia. | `hub_snippets`, `hub_scripts`, `hub_prompts`, `hub_padroes`, `hub-ml-<tema>` |
| **`ambiente_fonte/`** | A única cópia editável do produto. Tudo o mais é derivado ou publicado a partir dela. | Raiz do repositório |
| **Simulado** | Espelho da árvore do workspace, gerado por script a partir do fonte. Nunca editado à mão: o próximo render apaga qualquer alteração manual. | `Novo_Ambiente_Simulado/` |
| **Render** | Ato de gerar o simulado a partir do fonte. Cópia fiel, sem transformação de conteúdo. | `tools/render_simulado.py` |
| **Camada canônica / derivada / operacional** | Canônica é o repositório, única fonte editável; derivada é o simulado; operacional são os workspaces, que são cópias e nunca a verdade. | Divisão que sustenta todo o projeto |
| **Gate** | Verificação que precisa passar antes de avançar de fase. Não é sugestão: enquanto não passa, não se replica. | Testes de runtime e de roteamento |
| **Forward test** | Teste que mede **qual skill o Genie Code carrega** diante de um pedido. Não avalia a qualidade da resposta, só o roteamento. | 36 testes, `docs/testes/forward/` |
| **Smoke test** | Execução dos helpers no runtime real para descobrir o que só quebra fora da máquina local. | Resultados em `docs/testes/spark/` |
| **Caso positivo / negativo** | No forward test, positivo confirma que a skill certa é carregada; negativo confirma que ela **não** é carregada por um pedido parecido de outro domínio. | Método dos forward tests |
| **ADR** | Registro de decisão arquitetural. Imutável depois de aceito: mudar de ideia gera um novo ADR que supersede o anterior, preservando o histórico do raciocínio. | `docs/decisions/` |
| **Handoff** | Documento de passagem de contexto entre sessões ou entre IAs diferentes, escrito para quem chega sem saber de nada. | `docs/handoffs/` |
| **Helper** | Função pronta e auditada da biblioteca (`hub_snippets` ou `hub_scripts`). Existe para que a lógica não seja reescrita a cada conversa. | Catálogo em [catalogo_helpers.md](catalogo_helpers.md) |
| **API pública** | As funções que um módulo oferece para uso externo. As internas começam com `_` e podem mudar sem aviso. | Coluna "API" do catálogo |
| **Runbook** | Procedimento escrito passo a passo, para ser seguido sob pressão sem improviso. Aqui, o da replicação no trabalho. | `docs/playbooks/` |
| **AST** | Representação estruturada do código que permite conferir sintaxe sem executá-lo. A validação usa para garantir que todo `.py` compila. | Saída do validador |
| **Auditoria do Codex** | Revisão independente do ambiente `.assistant` original, feita pelo Codex em 2026-08-13, antes deste repositório existir. Encontrou seis skills sem frontmatter, cálculo de PSI incorreto e identificadores corporativos expostos, e entregou o pacote corrigido que virou o `ambiente_fonte/`. A entrega está congelada em `Ajustes_Codex/`, e os "gates do Codex" são as verificações que ela deixou pendentes. | Origem do produto; `docs/testes/` |
| **`run_governado`** | Gerenciador de contexto que abre um run isolado do MLflow e **recusa fechá-lo** sem parâmetros, métricas, assinatura e limitações declaradas. Existe porque dois wrappers de treino na mesma sessão colidem na chave `algorithm`, que o MLflow trata como imutável. | `hub_snippets.ml.mlflow_run` |

## Termos que descrevem o que **não** existe

Vale registrar, porque aparecem em material antigo e induzem a erro.

| Termo | Situação |
|---|---|
| **Slash commands próprios** (`/eda`, `/baseline`) | Nunca foram funcionalidade. São convenção de escrita entre humanos. O equivalente real é `@nome-da-skill` |
| **Hooks** | Não existem no Genie Code. Nenhuma automação dispara após uma resposta |
| **Memória automática** | Além de instruções, skills e `AGENTS.md`, não há mecanismo de memória |
| **MCP por arquivo JSON** | Configuração de MCP acontece em Genie Code → Settings, não por arquivo no workspace |
