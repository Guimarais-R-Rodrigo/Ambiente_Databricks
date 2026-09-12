# Plano de migração — READMEs didáticos por objeto

## 1. Estado desta entrega e decisão de execução

**R00: inventário e plano entregues. R01–R13: planejadas, não executadas.**

Repositório examinado: `Guimarais-R-Rodrigo/Ambiente_Databricks`.
Branch inspecionada: `main`.
Commit de referência: `9fa737104110354c0ec0ca5c4b6d3e5a0574c629`, de 11/09/2026.

Nesta entrega foram lidas árvores Git, regras editoriais, decisões arquiteturais, instruções, ferramentas pertinentes e amostras de implementação. Foi montada a distribuição completa dos objetos entre lotes. Não foi feita auditoria integral dos códigos dos 74 objetos. Nenhum arquivo do repositório foi alterado, nenhum README operacional foi criado no Git, nenhum commit/PR foi aberto, nenhum teste do repositório foi executado e nenhum workspace foi publicado. O teste de integridade incluído no pacote confere somente este planejamento.

A estratégia recomendada combina **aprovação de marcos, lotes pequenos e revisão separada**. Pausar sem salvar decisões não resolve deriva. Paralelizar antes de estabilizar o padrão amplia o custo de corrigir uma interpretação errada. Portanto, há aceite obrigatório do contrato editorial em R01 e do piloto em R02; a partir daí, a produção pode ser distribuída em lotes disjuntos, mantendo o mesmo contrato.

O padrão de continuidade será parar ao final de cada sprint com seu relatório. Uma autorização explícita pode agrupar sprints futuras, mas não suprime o fechamento e a auditoria de cada lote. Não existe execução em segundo plano entre respostas. A próxima unidade de trabalho é **R01**, não a geração indiscriminada de todos os arquivos.

As sprints desta iniciativa usam o prefixo **R** para não sobrescrever as sprints históricas 0–12 já presentes em `docs/sprints/`.

## 2. Objetivo e fronteiras do escopo

Cada pasta de objeto deve permitir que uma pessoa que não conhece o assunto consiga: entender o conceito; reconhecer um problema adequado; rejeitar usos inadequados; compreender entradas e saídas; encontrar o exemplo; e verificar se o resultado sustenta a decisão desejada.

A unidade de documentação é a **pasta de objeto**, não cada `.py`, `__init__.py`, teste ou célula do notebook. O resultado deve complementar o que existe, sem modificar comportamento de helpers nem substituir os READMEs visuais escolhidos pelo usuário.

### Cobertura inicial

| Família | Objetos operacionais |
|---|---:|
| Snippets — `constants` | 4 |
| Snippets — `display` | 3 |
| Snippets — `ml` | 30 |
| Snippets — `spark` | 7 |
| Snippets — `testing` | 1 |
| Snippets — `visual` | 6 |
| **Subtotal snippets** | **51** |
| Scripts | 7 |
| Prompts | 16 |
| **Total operacional** | **74** |

Além desses 74 READMEs de objeto, o plano prevê **três READMEs em exemplares dos padrões** e **seis READMEs de categoria**, estes últimos limitados à navegação. A previsão é de **83 destinos de README de autoria**, sem contar os READMEs agregadores existentes que serão ajustados. As cópias geradas não contam como novos textos independentes.

O total é uma fotografia do commit inspecionado. Antes da execução, reconciliar a árvore real: um objeto criado por outra mudança entra no inventário; um README recém-criado é revisado, não sobrescrito. A guarda de cobertura não deve codificar `74` como verdade eterna.

### Não faz parte desta migração

Não criar README individual para cada teste, `__init__.py`, arquivo de dependências, recurso PNG ou arquivo interno em `tools/`. Não aplicar o template humano de quinze seções aos `SKILL.md`. Não criar um sétimo tipo de objeto. Não renomear APIs, mudar defaults, calibrar thresholds, instalar dependências indiscriminadamente ou corrigir modelos como efeito colateral.

Não reescrever ADRs aceitos nem relatórios históricos. Não substituir imagens, widgets ou o desenho aprovado dos READMEs gerais. Não publicar no Databricks Free ou no trabalho; publicação requer etapa e autorização próprias.

## 3. Arquitetura documental a preservar

A implantação acrescentará a escala **Objeto** ao tipo README. As escalas Curta, Padrão e Longa continuam válidas para entradas agregadoras.

| Documento | Responsabilidade |
|---|---|
| README geral/da coleção | Descoberta, navegação e próximo passo. |
| Manual Técnico | Visão integrada, catálogo central e índice de termos. |
| README do objeto | Conceito aplicado, adequação, limites e caminho de uso daquele objeto. |
| Notebook de exemplo | Demonstração guiada, execução e interpretação com evidência delimitada. |
| Implementação e API pública | Comportamento realmente implementado e nomes expostos. |
| Prompt original | Formulário, instrução colável, placeholders, contrato de saída e limites. |
| Regras/templates | Critérios para produzir e revisar os documentos. |

Uma síntese local do conceito é desejável: o README precisa ser compreensível sozinho. Isso não autoriza copiar capítulos inteiros do Manual nem manter dois catálogos ou glossários concorrentes.

A fonte editável do produto permanece em `ambiente_fonte/`. `Novo_Ambiente_Simulado/` é regenerado pela ferramenta existente. O Manual é escrito em `ambiente_fonte/.assistant/MANUAL_TECNICO.md`; a cópia da raiz deve ser sincronizada, não reescrita de forma independente.

**Navegação do Manual merece um teste próprio.** Como as três cópias têm o mesmo conteúdo, mas ficam em diretórios diferentes, um link relativo novo pode resolver em uma e falhar em outra. Preservar âncoras internas; testar referências nas três posições; usar caminho lógico relativo à raiz do Hub e referência Git explicitamente identificada quando um link local não for portátil. Não presumir que acesso ao GitHub privado existe no workspace corporativo. Uma referência de implementação por commit não é substituída silenciosamente por `main` como evidência histórica.

A figura existente que mostra fachada, implementação e notebook pode continuar representando o núcleo executável. A legenda deve explicar o README adicional como camada humana. Só propor alteração gráfica se houver contradição que texto e legenda não resolvam, como mudança separada.

## 4. Contrato editorial e prevenção de repetição

Em R01, criar `hub_padroes/readme/template_objeto.md`, subordinado ao template geral, e um checklist editorial referenciado. A primeira versão será candidata; o piloto R02 congela a versão 1.0. O mesmo contrato é usado por todos os redatores. Não espalhar versões ligeiramente diferentes do template em skills e prompts.

Preservar as quinze seções da proposta discutida:

| Nº | Seção | Conteúdo exclusivo que deve entregar |
|---|---|---|
| 1 | O que é? | Conceito em linguagem acessível e delimitação do objeto implementado. |
| 2 | Que problema este recurso resolve? | Pergunta concreta e decisão apoiada. |
| 3 | Quando faz sentido usar? | Condições positivas com explicação do porquê. |
| 4 | Quando não usar? | Critérios para rejeitar a escolha antes da execução. |
| 5 | Como funciona, intuitivamente? | Mecanismo, sem começar por sintaxe ou copiar a API. |
| 6 | Exemplo de situação | Um cenário coerente do início ao fim, com dados fictícios identificados. |
| 7 | O que você precisa antes de usar? | Dados, grão, requisitos e condições realmente exigidas. |
| 8 | O que este recurso entrega? | Estrutura e significado das saídas, incluindo limites de interpretação. |
| 9 | Como usar este recurso no Hub? | Rota mínima correta e ligação para a demonstração. |
| 10 | Decisões e configurações que mais importam | Opções que mudam materialmente resultado, custo ou risco. |
| 11 | Limitações, riscos e armadilhas | Cuidados que continuam valendo mesmo quando a escolha foi adequada. |
| 12 | Quais são as alternativas? | Alternativas plausíveis e diferença relevante, sem ranking universal. |
| 13 | Como saber se o resultado faz sentido? | Verificações concretas após a execução. |
| 14 | Arquivos relacionados e próximos passos | Navegação verificada e papel de cada arquivo. |
| 15 | Referências | Fontes que sustentam afirmações, versões e alcance. |

Título, frase de identidade, visão rápida e navegação ficam antes das seções. A abertura deve oferecer acesso direto ao exemplo para quem já conhece o conceito, sem obrigar esse leitor a atravessar toda a introdução.

Os títulos principais são comuns. Subtópicos são condicionais ao objeto. Não exigir “risco estatístico” em um separador visual, “treino” em um prompt ou três concorrentes para uma constante de estilo. Quando um tema realmente não se aplica, explicar sucintamente o motivo pertinente, sem preencher o documento com “N/A”.

Não usar quantidade de palavras como condição de aprovação. Extensão pode gerar alerta de revisão, nunca texto de enchimento. Para modelos complexos, explicar o necessário; para objetos pequenos, responder às mesmas perguntas com menos texto.

### Linguagem e evidência

Usar PT-BR acessível, preservando identificadores e contratos existentes, inclusive identificadores em português. Definir termo técnico no primeiro uso. Evitar frases como “basta”, “obviamente” ou “é trivial” para etapas que podem ser novas para o leitor. Explicar motivos, não apenas dar ordens. Usar exemplos sintéticos coerentes com o contexto de CRM/dados sem expor informação corporativa.

Distinguir sempre: capacidade da técnica/biblioteca; capacidade implementada no helper; premissa escolhida pelo analista; saída observada; saída ilustrativa; recomendação de uso; e regra de plataforma confirmada.

Exemplo concreto do risco: `train_xgboost_baseline` aceita `binary`, `multiclass` e `regression` no código inspecionado. Explicar que a biblioteca XGBoost tem outras aplicações não autoriza declarar que esse helper implementa todas elas. Tampouco o nome do helper demonstra execução distribuída, registro completo de modelo ou deploy. O README deve narrar o que a API efetivamente faz.

O notebook existente é evidência do cenário descrito, não autoridade infalível sobre toda a teoria. Texto, docstring e exemplo precisam ser confrontados com o código e, nas afirmações externas, com documentação primária. Uma execução antiga não comprova compatibilidade atual em outro ambiente.

## 5. Protocolo comum a toda sprint de produção

### Entrada

Confirmar commit de partida, branch de trabalho, alterações simultâneas e versão do template. Abrir o relatório da sprint anterior e o manifesto. Fixar lista de caminhos que o lote pode modificar e caminhos protegidos. Preencher os hashes dos arquivos-fonte pertinentes antes da redação.

Ler a implementação completa, `__init__.py`, notebook de exemplo e testes pertinentes do objeto. Nos prompts, ler o formulário e seu contrato inteiro. Consultar o Manual nas seções relevantes, não usar apenas nomes de pasta ou resumos antigos como base do texto. Verificar fontes externas primárias para afirmações técnicas específicas, sobretudo regras de runtime, dependências e compatibilidade.

### Produção e revisão

Escrever README ancorado no contrato real. Acrescentar ligações de ida e volta sem alterar código executável nem texto colável de prompts. Atualizar rotas de descoberta existentes da família entregue. Não criar links para READMEs de sprints futuras ainda ausentes; apontar temporariamente à pasta/implementação existente ou registrar a ligação pendente para R12.

Revisar coerência entre README, API, notebook e Manual. Um achado funcional vai para o registro de problemas, com severidade e efeito sobre o uso. Não alterar implementação para fazer a documentação parecer correta. Quando a falha impedir um uso seguro ou uma explicação verificável, marcar o objeto bloqueado; não contabilizá-lo como concluído.

Aplicar a rubrica didática, executar verificações estruturais e conferir o diff de arquivos protegidos. Testar exemplos mínimos novos em ambiente seguro quando possível. Caso o ambiente ou a dependência falte, registrar literalmente “não executado” e o motivo; não copiar a marca “executado no laboratório” de outra versão como se fosse evidência desta sprint.

### Saída

Integrar alterações pelo responsável único de documentos compartilhados. Sincronizar o Manual quando necessário. Regenerar derivados a partir da fonte consolidada e verificar o resultado. Registrar testes, falhas preexistentes, regressões, skips e limitações. Encerrar o lote com inventário reconciliado, relatório de alterações e checkpoint de retomada.

Cada sub-lote tem seu gate. Não acumular duas levas grandes para revisar somente no final.

## 6. Roadmap R00–R13

As contagens abaixo são de novos READMEs operacionais previstos. Revisitar um objeto do piloto em uma comparação posterior não o conta duas vezes.

| Sprint | Entrega principal | Operacionais novos | Outros READMEs novos |
|---|---|---:|---:|
| R00 | Inventário, escopo, plano e matriz de impactos | 0 | 0 |
| R01 | Contrato, governança, guardas e exemplares | 0 | 3 exemplares |
| R02 | Piloto representativo e congelamento do padrão | 6 | 0 |
| R03 | Constantes, apresentação e dados sintéticos | 13, em lotes 7 + 6 | 0 |
| R04 | Spark e scripts operacionais restantes | 12, em lotes 6 + 6 | 0 |
| R05 | Modelos tabulares e otimização | 6 | 0 |
| R06 | Temporalidade e séries temporais | 5 | 0 |
| R07 | Score, safras e sobrevivência | 6 | 0 |
| R08 | Agrupamento, anomalias e explicabilidade | 6 | 0 |
| R09 | Métricas, monitoramento e tracking | 5 | 0 |
| R10 | Prompts de investigação e preparação | 6 | 0 |
| R11 | Prompts de modelagem, operação e governança | 9, em lotes 5 + 4 | 0 |
| R12 | Integração, navegação e migração completa | 0 | 6 índices |
| R13 | Auditoria final, regressão e aceite | 0 | 0 |
| **Total** | | **74** | **9** |

### R00 — Levantamento e plano

**Objetivo:** estabelecer o conjunto inicial verificável e retirar ambiguidades de escopo.

**Entregas desta rodada:** plano, manifesto com os 74 objetos alocados uma única vez, matriz de impactos documentais e checkpoint. Conferência local do manifesto: 51 snippets, sete scripts, 16 prompts, 74 atribuições únicas, nenhum objeto omitido e lote máximo de sete.

**Limite:** não equivale à execução de baseline técnico, auditoria integral dos 74 códigos ou validação no Databricks. Essas atividades estão explicitamente pendentes.

**Saída:** autorização para R01 após leitura do plano.

### R01 — Fundação editorial, governança e prevenção de regressão

**Objetivo:** impedir que cada lote invente seu próprio README ou que documentos normativos continuem exigindo a estrutura antiga.

**Trabalho:** executar e registrar o baseline local; estabelecer a branch de trabalho; criar a decisão arquitetural; incorporar a escala Objeto; preparar template/checklist; atualizar templates de snippet, script, prompt e notebook; atualizar a skill de criação; adicionar orientação seletiva nas instruções; preparar ligações nos índices e registro da iniciativa.

O número proposto do ADR é `ADR-0011-readmes-de-objeto.md`, mas precisa ser reconfirmado na árvore antes de escrever. O novo ADR complementa a organização por pasta e a responsabilidade do Manual. Não reescreve os corpos históricos de ADR-0007 e ADR-0010.

**Exemplares a completar:** `hub_padroes/snippet/taxa_resposta_campanha/README.md`, `hub_padroes/script/checar_base_campanha/README.md` e `hub_padroes/prompt/analisar_campanha/README.md`, todos sob a raiz `.assistant/`. São exemplos do padrão; não entram no catálogo operacional como novos helpers.

**Ferramentas:** implementar a guarda de README e seus testes, integrar ao gate existente e documentar seu alcance. Como `ci_local.py` lista explicitamente as etapas/arquivos, um teste recém-criado não pode ser considerado executado por simples presença na pasta.

**Migração gradual:** os objetos legados sem README ficam em lista inicial rastreável, com sprint de entrega. A lista de dispensa temporária só diminui. Objetos novos não ganham dispensa; README entregue não pode ser removido ou voltar a estado incompleto. Em R12, o regime transitório deixa de permitir objetos operacionais sem README.

**Aceite:** regras e templates concordam; exemplares mostram o padrão; testes negativos provam que a guarda detecta defeitos; nenhum comportamento analítico mudou; baseline e falhas preexistentes estão separados; roteiro de leitura é aprovado. Pausa antes do piloto.

### R02 — Piloto de seis objetos diferentes

**Objetos:** `train_xgboost`, `isolation_forest`, `pit_join`, `format_br`, `quick_profile` e `eda_rapida`, nos caminhos completos indicados no manifesto.

O piloto combina modelos, método não supervisionado, transformação Spark temporal, objeto simples de formatação, script de diagnóstico e prompt. Assim, o template é testado em naturezas de recurso realmente distintas.

**Aceite técnico:** parâmetros, entradas, saídas, defaults relevantes, dependências e efeitos correspondem ao código. O guia distingue o método geral da implementação específica. O exemplo mínimo está conferido ou tem status de execução explícito. Nenhuma capacidade ausente foi inventada.

**Aceite didático:** após ler o texto, alguém consegue explicar a finalidade, escolher um uso adequado, rejeitar um uso inadequado, identificar o que fornecer e dizer o que a saída não demonstra. Também deve achar o notebook sem precisar conhecer a estrutura do projeto.

**Decisão de saída:** ajustar o template uma única vez com o aprendizado do piloto, atualizar os três exemplares e os seis pilotos à mesma versão e congelar `1.0`. Solicitar aceite antes de multiplicar o padrão.

### R03 — Constantes, apresentação e fixtures

**Lote A, sete objetos:** `constants/colors`, `constants/emojis`, `constants/styles`, `testing/fixtures`, `visual/badge`, `visual/divider`, `visual/kpi_card`.

**Lote B, seis objetos:** `display/correlation_matrix`, `display/dataframe_styled`, `display/distribution_grid`, `visual/index_generator`, `visual/section_header`, `visual/theme_plotly`.

Todos os caminhos são relativos a `hub_snippets/`. `format_br` já foi entregue no piloto.

**Foco de revisão:** utilidade prática sem artificializar teoria, dependências de apresentação, diferença entre valor numérico e formatação, comportamento de sessão quando existir, finalidade dos dados sintéticos e limites dos gráficos. Não modificar a paleta ou o desenho visual para atender à migração.

**Documentação além dos READMEs:** ligações nos notebooks; entradas pertinentes do Manual e do README da coleção; changelog e fechamento dos dois lotes. Índices de categoria completos são consolidados em R12; navegação inicial não pode ficar esperando até lá.

### R04 — Operações Spark e scripts restantes

**Lote A, seis snippets Spark:** `date_features`, `join_diagnostics`, `null_summary`, `psi_calculator`, `safe_display`, `smart_sample`.

**Lote B, seis scripts:** `data_quality_check`, `doc_coverage`, `drift_detector`, `naming_checker`, `rfv_calculator`, `schema_to_yaml`.

`pit_join` e `quick_profile` já estão no piloto.

**Foco de revisão:** grão, chaves, nomes de recurso, leitura versus escrita, coleta no driver, custo de ações, requisitos de sessão e interpretação de diagnósticos. Verificar exatamente o que significa um status retornado: não o equiparar automaticamente a uma exceção, bloqueio ou correção dos dados.

**Comparações obrigatórias:** `null_summary` versus `quick_profile` versus `data_quality_check`; `drift_detector` versus `psi_calculator`, com cruzamento posterior para `drift_detection`. O plano não presume equivalência entre APIs apenas por nomes parecidos.

**Documentação adicional:** notebooks, Manual, READMEs de snippets/scripts e registros. Alterações de runtime ou restrições de plataforma só entram com fonte e escopo confirmados.

### R05 — Modelos tabulares e otimização

**Seis objetos ML:** `train_lgbm`, `train_catboost`, `lgbm_ranker`, `optuna_lgbm`, `mlp_embeddings`, `tabnet_wrapper`.

**Foco de revisão:** tipo de problema suportado no wrapper, representação das variáveis, conjuntos de treino/validação, objetivo de otimização, dependências, recursos computacionais e artefatos produzidos. Comparar alternativas sem dizer que determinado algoritmo é sempre superior.

Revisitar o README de `train_xgboost` para conferir coerência entre as comparações, sem contá-lo como nova entrega nem reescrever toda a família. Qualquer ajuste no piloto aparece no relatório da sprint.

**Documentação adicional:** notebooks, Manual, rotas de modelagem na coleção e registros. Não modificar hiperparâmetros ou bibliotecas para facilitar exemplos.

### R06 — Temporalidade e séries temporais

**Cinco objetos ML:** `arima_wrapper`, `prophet_wrapper`, `lgbm_temporal`, `split_temporal`, `walk_forward`.

**Foco de revisão:** frequência, horizonte, população, separação temporal e momento de disponibilidade dos dados. Explicar aquilo que o helper realmente controla e as verificações que continuam sendo responsabilidade de quem o usa.

**Coerência transversal:** os critérios de tempo precisam concordar com `pit_join`, já entregue. Não apresentar a existência de um split temporal como prova suficiente de ausência de vazamento.

**Documentação adicional:** notebooks, entradas temporais do Manual, navegação e relatório de achados.

### R07 — Score, safras e sobrevivência

**Seis objetos ML:** `woe_iv_calculator`, `scorecard_builder`, `score_bands`, `vintage_analysis`, `kaplan_meier`, `survival_cox`.

**Foco de revisão:** alvo, evento, classe de referência, unidades, denominadores, transformação em score, tempo de exposição e censura conforme aplicável. Explicar pressupostos e limitações sem atribuir homologação regulatória ou interpretação causal ao cálculo por si só.

**Aceite especial:** um resultado numérico deve ser interpretável a partir do README, incluindo sua população e sua direção. Um limiar contextual não deve ser apresentado como lei universal.

**Documentação adicional:** notebooks, entradas correspondentes do Manual, rotas da coleção e registros de decisão.

### R08 — Agrupamento, anomalias e explicabilidade

**Seis objetos ML:** `autoencoder_anomaly`, `cluster_profiling`, `clustering_suite`, `umap_viz`, `shap_explainer`, `explainability_report`.

**Foco de revisão:** agrupamento versus classificação, detecção de comportamento incomum versus identificação do evento de negócio, projeção visual versus estrutura original, explicação do comportamento do modelo versus causalidade. Cada afirmação deve corresponder ao método e à implementação efetiva.

Revisitar `isolation_forest` na comparação de anomalias e conferir as diferenças entre as duas rotas de explicabilidade. Não transformar uma proibição excessivamente ampla encontrada no notebook em regra de todos os READMEs.

**Documentação adicional:** notebooks, Manual, links recíprocos e relatório de diferenças encontradas.

### R09 — Métricas, monitoramento e tracking

**Cinco objetos ML:** `curves_plotly`, `metrics_report`, `drift_detection`, `mlflow_run`, `performance_monitor`.

**Foco de revisão:** direção e escala de scores/métricas; alvo e classe positiva; limiares; comparação de populações e períodos; o que é registrado; quando há efeito externo; e diferença entre função chamada, agendamento, alerta e retreino.

**Coerência transversal:** comparar `drift_detection`, `drift_detector` e `psi_calculator`; conferir registro MLflow nos wrappers já descritos. Uma biblioteca que calcula diagnóstico não deve ser descrita como serviço que roda continuamente sem infraestrutura adicional.

**Documentação adicional:** notebooks, Manual, navegação e registros; os textos devem separar claramente teste local, execução de exemplo e uso de serviços externos.

### R10 — Prompts de investigação e preparação

**Seis prompts:** `eda_completa`, `cross_eda`, `comparar_tabelas`, `data_quality`, `stat_check`, `feature_engineering`.

**Foco de revisão:** o problema analítico do briefing, informação que o usuário deve fornecer, contexto anexado, limites de uma resposta gerada e sinais para conferir antes de executar código sugerido.

O README de `eda_rapida` serve como referência de formato, não como texto a duplicar trocando o nome. Preservar os placeholders e as orientações de preenchimento que já fazem parte do formulário original.

**Documentação adicional:** backlink fora do prompt colável, Markdown dos notebooks, README da coleção e capítulo de métodos/briefings do Manual quando pertinente.

### R11 — Prompts de modelagem, operação e governança

**Lote A, cinco prompts:** `baseline_orchestration`, `explainability`, `monitoramento_modelo`, `safra`, `pipeline`.

**Lote B, quatro prompts:** `auditoria_skills`, `comentar_notebook`, `novo_projeto`, `tutor_explicar`.

**Foco de revisão:** distinguir um pedido de trabalho de trabalho executado; plano de pipeline de deploy; instrução de monitoramento de agendamento; revisão textual de auditoria independente. Não afirmar ativação automática de uma skill porque seu nome foi escrito na resposta.

**Documentação adicional:** mesmas mudanças limitadas nos formulários/notebooks da R10, navegação da coleção e Manual. Revisar o conjunto dos 16 prompts para manter escopo e vocabulário consistentes.

### R12 — Integração e cobertura completa

**Objetivo:** fechar o sistema documental como um todo, não apenas a soma dos arquivos.

Criar os seis READMEs de categoria em `hub_snippets/{constants,display,ml,spark,testing,visual}/README.md`. Serão entradas concisas: papel da categoria, rota por problema e links para os objetos. Não são um novo catálogo integrado nem recebem as quinze seções de objeto.

Conferir Manual, índices, referências de ida/volta e comparações entre famílias. Resolver ligações pendentes para READMEs que agora existem. Verificar que nenhum objeto está acessível somente por busca de código. Preservar âncoras e atualizar saídas reais de gates afetadas por novas contagens.

Retirar as dispensas transitórias remanescentes somente quando cada item estiver efetivamente atendido. A guarda passa a exigir README em todos os objetos elegíveis encontrados na árvore. Um objeto bloqueado não pode ser escondido do denominador para produzir 100%.

Sincronizar a cópia de leitura do Manual e regenerar derivados. Conferir inclusão dos novos documentos nos pacotes existentes e integridade do manifesto, sem publicar. Não alterar renderer ou empacotador se os mecanismos atuais já atendem; nesse caso, registrar “verificado, sem alteração”.

**Aceite:** cobertura estrutural completa, entregas técnicas/didáticas identificadas por objeto, nenhuma referência interna quebrada, conteúdo protegido preservado e todas as mudanças documentais discriminadas.

### R13 — Auditoria final, regressão e aceite

**Objetivo:** verificar a entrega com perspectiva diferente da autoria e preparar um candidato de documentação à distribuição.

A auditoria final revisa 100% dos caminhos/contratos/documentos previstos; pode organizar a leitura em lotes, não substituir a revisão do conjunto por uma amostra não declarada. Dê profundidade adicional aos objetos analíticos sensíveis, dependências opcionais, efeitos de tracking e restrições de ambiente. Verifique também os documentos gerais: templates, regras, Manual, skill de criação e descrição do gate devem concordar.

Os relatórios identificam autor, revisor, versão dos modelos/ferramentas quando conhecida, commit examinado, fontes e validações realizadas. Revisões sucessivas pela mesma instância não são chamadas de auditoria independente. Quando a separação de revisão não estiver disponível, registrar o limite e manter o aceite independente pendente antes do compartilhamento que o exige.

Executar o gate local e as verificações novas na árvore final; conferir que nenhum arquivo mudou depois da evidência sem nova verificação. Comparar as implementações com o baseline, salvo mudanças externas explicitamente reconciliadas. Conferir links em fonte/derivado e igualdade do Manual.

**Entrega:** relatório de fechamento consolidado, matriz de documentos realmente alterados, achados e resolução, cobertura separada por estado, instrução de manutenção e handoff. Publicação, validação remota e homologação no workspace não são inferidas desse aceite.

## 7. Critérios de qualidade e evidência

### Seis dimensões obrigatórias

| Dimensão | Evidência para satisfazer |
|---|---|
| Compreensão | Conceito explicado sem pressupor domínio prévio; termos definidos; mecanismo inteligível. |
| Escolha | Caso adequado e contraexemplo específico, ambos com motivo. |
| Fidelidade | Escopo, API, entradas/saídas e parâmetros correspondem aos arquivos reais. |
| Uso seguro | Premissas, dependências, contexto de execução e efeitos materiais declarados. |
| Interpretação | O texto explica o resultado, o que não demonstra e como conferi-lo. |
| Navegação/procedência | Arquivos e fontes localizáveis; vínculos corretos; fato observado separado de ilustração. |

Cada dimensão pode ser registrada como 0 (ausente/incorreta), 1 (parcial) ou 2 (satisfatória). Para aceitar, todas as dimensões precisam estar satisfatórias. Não usar média para compensar uma API inventada com boa redação. A rubrica é revisão justificada, não nota automática atribuída por comprimento.

### Gates automáticos

Verificar presença de README nos elegíveis, cabeçalhos/versionamento, campos não preenchidos, cercas de código, links e âncoras suportados, navegação mínima, inventário único, redução monotônica da dívida de migração e ausência de arquivos fora do lote. Testar o próprio detector com exemplos de falha.

Os testes devem incluir: README ausente; objeto novo omitido do manifesto; item entregue apagado; exceção ampliada sem autorização; cabeçalhos só dentro de um bloco de código; link de arquivo válido com âncora inexistente; caminho incorreto por diferença de caixa; exclusão indevida de um objeto do universo; e link novo do Manual inválido em uma das cópias.

Conferir mudanças em implementações e `__init__.py` por diff/hashes. Nas células executáveis dos notebooks, verificar AST ou comparação equivalente, separando comentários Markdown. Nos prompts, comparar o texto dos blocos coláveis e placeholders. Esses controles detectam mudanças; não garantem a verdade científica da explicação.

### Evidência local versus ambiente real

Os comandos existentes de entrada para o gate são:

```bash
python tools/validate_assistant.py
python tools/ci_local.py --verbose
```

Para o renderer, o comando sem `--write` é planejamento; a escrita só acontece após conciliação da árvore:

```bash
python tools/render_simulado.py
python tools/render_simulado.py --write
```

Esses comandos estão documentados como próximos passos; **não foram executados nesta R00**. Novos comandos de teste devem ser confirmados após sua implementação. Não invocar nomes de flags ainda inexistentes como se já funcionassem.

O gate inspecionado verifica saídas e contagens do README raiz; depois de mudanças, recapturar a saída real correspondente e repetir a conferência. Não editar números à mão para obter aprovação. Um teste pulado é `SKIP`, não `PASS`. Uma falha preexistente é registrada separadamente, não escondida nem atribuída automaticamente à migração.

Execução local não confirma Databricks, permissões, recursos remotos ou roteamento conversacional. Uma recomendação de compatibilidade exige fonte oficial e, para afirmar teste no destino, evidência do destino. A etapa de validação remota permanece separada.

### Bloqueadores

Bloqueiam o objeto/lote: capacidade inexistente apresentada como implementada; parâmetro/retorno errado; afirmação material sem apoio; omissão de escrita/efeito material; saída inventada como observada; contradição relevante entre README e exemplo; alterações de código fora do escopo; dados sensíveis; ou falha de navegação essencial.

Uma divergência conceitual exige investigação antes de propagação. Correções de template entram por versão nova, com mapa explícito de quais READMEs já entregues precisam ser revistos.

## 8. Paralelização e auditoria sem deriva

Depois do aceite de R02, um executor com orquestração pode usar até três redatores por sub-lote, cada um responsável por dois ou três objetos. O limite de sete objetos por lote foi escolhido como orçamento inicial de revisão, não como alegação de capacidade universal. Pode ser reduzido em famílias complexas.

O coordenador é o único autor dos documentos compartilhados: templates, regras, Manual, índices gerais, manifestos, changelog consolidado e integração. Redatores só editam as pastas que lhes foram atribuídas. Revisores examinam artefatos e evidências, não mudam silenciosamente o contrato editorial. O integrador resolve divergências em registro próprio.

| Papel | Responsabilidade | Restrição |
|---|---|---|
| Coordenador | Baseline, versão do template, escopo, dependências e integração. | Não declarar auditado aquilo que só foi escrito. |
| Redator | Ler contrato, produzir README e navegação do lote. | Não editar arquivos compartilhados nem alterar o helper. |
| Revisor técnico | Confrontar texto com API, exemplo, fontes e efeitos. | Não validar por plausibilidade do nome do objeto. |
| Revisor didático | Testar compreensão, progressão e adequação dos exemplos. | Não enfraquecer precisão para tornar a prosa agradável. |
| Auditor final | Verificar conjunto e resolução de achados. | Não simular independência da autoria. |

Cada trabalhador recebe o mesmo pacote mínimo: commit, template, exemplar, lista permitida, fontes do objeto, critérios de aceite, formato de relatório e itens proibidos. Fontes externas relevantes entram na evidência com escopo e data. Não enviar toda a biblioteca para cada redator nem fazê-lo depender de memória da conversa.

Se não houver subagentes independentes, usar a sequência leitura → redação → revisão técnica → revisão didática e registrar que as passagens pertencem à mesma autoria. A revisão independente exigida para distribuição deve vir de um revisor realmente distinto; não contar rótulos de papéis como pessoas/modelos independentes.

## 9. Relatório obrigatório de fechamento

O usuário deve receber, em cada fechamento, algo além de “foram feitos seis READMEs”. Usar cinco grupos de mudanças e um grupo de evidências.

**A. READMEs novos/revisados.** Listar cada caminho e se é operacional, exemplar ou índice; informar versão do template, revisão e eventuais ressalvas.

**B. Outras documentações alteradas.** Listar cada caminho concreto, seção alterada, o que mudou, por que era necessário e evidência do diff. Isso inclui regras, templates, skill, instruções, Manual e Markdown de notebooks. Não misturar com o grupo A.

**C. Ferramentas alteradas.** Discriminar mudanças em validador, testes e integração do gate; não chamá-las apenas de “documentação”.

**D. Cópias e derivados.** Informar a sincronização do Manual raiz e a regeneração do simulado, distinguindo autoria de geração. Não inflar a contagem de READMEs com essas cópias.

**E. Revisados sem alteração.** Registrar caminhos relevantes preservados e o motivo. Uma revisão não é uma atualização.

**F. Evidências e continuidade.** Commit/base final, comandos realmente executados, ambiente, retorno, PASS/FAIL/SKIP, revisores reais, achados, bloqueios, divergências, cobertura e próxima sprint. Deixar claro se o lote está aprovado, condicionado ou bloqueado.

Extrair o conjunto efetivo de mudanças de `git diff --name-status` entre pontos identificados. Não compor a lista apenas com memória de quem editou. O relatório deve reconciliar a lista planejada com a lista real e explicar qualquer caminho novo.

### Modelo curto de fechamento

```text
Sprint / lote:
Base examinada e versão final:
Versão do template:
Estado: APROVADO | CONDICIONADO | BLOQUEADO

A. READMEs de objeto entregues:
B. Outras documentações alteradas (caminho + seção + motivo):
C. Ferramentas alteradas:
D. Cópias/derivados regenerados:
E. Arquivos revisados e preservados:

Verificações executadas e resultados:
Verificações não executadas / limites:
Autoria e revisores efetivos:
Achados e providências:
Cobertura: inventariados / escritos / revisados / bloqueados / aceitos
Mudanças concorrentes reconciliadas:
Próxima sprint e ponto de autorização:
```

## 10. Controle de mudanças e retomada

Local proposto da iniciativa no Git: `docs/sprints/readmes_objetos/`. Criar `PLANO.md`, `INVENTARIO.json`, `MATRIZ_IMPACTOS.md` e fechamentos Rxx. Usar `docs/auditoria/<data>_readmes_objetos/` e o padrão existente de handoffs para revisões e transferência de contexto. Esses destinos são propostos; ainda não foram criados no repositório nesta entrega.

Na retomada, ler a entrada canônica do projeto, as regras pertinentes, o changelog recente, o plano vigente, o relatório anterior e o manifesto. Conferir os hashes dos arquivos que o lote vai documentar. Se outra IA mudou um helper, atualizar a análise desse helper antes de escrever o README. Não fazer reset destrutivo nem sobrescrever trabalho concorrente.

Recomenda-se branch dedicada e diffs/commits separáveis por sprint. Evitar misturar correção funcional com migração documental. Nenhum merge na branch principal ou publicação de workspace deve ser tratado como consequência automática do texto deste plano.

Se o template mudar depois de congelado, o coordenador registra o motivo, a versão nova e a lista dos documentos afetados. As sprints seguintes não usam a versão nova enquanto os modelos de referência e a política de revisão não forem reconciliados.

## 11. Mapa completo dos 74 objetos

A tabela a seguir aloca todos os objetos operacionais exatamente uma vez. Em cada pasta o destino é `README.md`. O caminho completo começa com `ambiente_fonte/.assistant/`. O JSON anexo traz também implementação, fachada pública e notebook esperado de cada objeto.

| Sprint/lote | Tipo e categoria | Pasta do objeto, relativa a `.assistant/` |
|---|---|---|
| R02-A | prompt | `hub_prompts/eda_rapida/` |
| R02-A | script | `hub_scripts/quick_profile/` |
| R02-A | snippet / constants | `hub_snippets/constants/format_br/` |
| R02-A | snippet / ml | `hub_snippets/ml/isolation_forest/` |
| R02-A | snippet / ml | `hub_snippets/ml/train_xgboost/` |
| R02-A | snippet / spark | `hub_snippets/spark/pit_join/` |
| R03-A | snippet / constants | `hub_snippets/constants/colors/` |
| R03-A | snippet / constants | `hub_snippets/constants/emojis/` |
| R03-A | snippet / constants | `hub_snippets/constants/styles/` |
| R03-A | snippet / testing | `hub_snippets/testing/fixtures/` |
| R03-A | snippet / visual | `hub_snippets/visual/badge/` |
| R03-A | snippet / visual | `hub_snippets/visual/divider/` |
| R03-A | snippet / visual | `hub_snippets/visual/kpi_card/` |
| R03-B | snippet / display | `hub_snippets/display/correlation_matrix/` |
| R03-B | snippet / display | `hub_snippets/display/dataframe_styled/` |
| R03-B | snippet / display | `hub_snippets/display/distribution_grid/` |
| R03-B | snippet / visual | `hub_snippets/visual/index_generator/` |
| R03-B | snippet / visual | `hub_snippets/visual/section_header/` |
| R03-B | snippet / visual | `hub_snippets/visual/theme_plotly/` |
| R04-A | snippet / spark | `hub_snippets/spark/date_features/` |
| R04-A | snippet / spark | `hub_snippets/spark/join_diagnostics/` |
| R04-A | snippet / spark | `hub_snippets/spark/null_summary/` |
| R04-A | snippet / spark | `hub_snippets/spark/psi_calculator/` |
| R04-A | snippet / spark | `hub_snippets/spark/safe_display/` |
| R04-A | snippet / spark | `hub_snippets/spark/smart_sample/` |
| R04-B | script | `hub_scripts/data_quality_check/` |
| R04-B | script | `hub_scripts/doc_coverage/` |
| R04-B | script | `hub_scripts/drift_detector/` |
| R04-B | script | `hub_scripts/naming_checker/` |
| R04-B | script | `hub_scripts/rfv_calculator/` |
| R04-B | script | `hub_scripts/schema_to_yaml/` |
| R05-A | snippet / ml | `hub_snippets/ml/lgbm_ranker/` |
| R05-A | snippet / ml | `hub_snippets/ml/mlp_embeddings/` |
| R05-A | snippet / ml | `hub_snippets/ml/optuna_lgbm/` |
| R05-A | snippet / ml | `hub_snippets/ml/tabnet_wrapper/` |
| R05-A | snippet / ml | `hub_snippets/ml/train_catboost/` |
| R05-A | snippet / ml | `hub_snippets/ml/train_lgbm/` |
| R06-A | snippet / ml | `hub_snippets/ml/arima_wrapper/` |
| R06-A | snippet / ml | `hub_snippets/ml/lgbm_temporal/` |
| R06-A | snippet / ml | `hub_snippets/ml/prophet_wrapper/` |
| R06-A | snippet / ml | `hub_snippets/ml/split_temporal/` |
| R06-A | snippet / ml | `hub_snippets/ml/walk_forward/` |
| R07-A | snippet / ml | `hub_snippets/ml/kaplan_meier/` |
| R07-A | snippet / ml | `hub_snippets/ml/score_bands/` |
| R07-A | snippet / ml | `hub_snippets/ml/scorecard_builder/` |
| R07-A | snippet / ml | `hub_snippets/ml/survival_cox/` |
| R07-A | snippet / ml | `hub_snippets/ml/vintage_analysis/` |
| R07-A | snippet / ml | `hub_snippets/ml/woe_iv_calculator/` |
| R08-A | snippet / ml | `hub_snippets/ml/autoencoder_anomaly/` |
| R08-A | snippet / ml | `hub_snippets/ml/cluster_profiling/` |
| R08-A | snippet / ml | `hub_snippets/ml/clustering_suite/` |
| R08-A | snippet / ml | `hub_snippets/ml/explainability_report/` |
| R08-A | snippet / ml | `hub_snippets/ml/shap_explainer/` |
| R08-A | snippet / ml | `hub_snippets/ml/umap_viz/` |
| R09-A | snippet / ml | `hub_snippets/ml/curves_plotly/` |
| R09-A | snippet / ml | `hub_snippets/ml/drift_detection/` |
| R09-A | snippet / ml | `hub_snippets/ml/metrics_report/` |
| R09-A | snippet / ml | `hub_snippets/ml/mlflow_run/` |
| R09-A | snippet / ml | `hub_snippets/ml/performance_monitor/` |
| R10-A | prompt | `hub_prompts/comparar_tabelas/` |
| R10-A | prompt | `hub_prompts/cross_eda/` |
| R10-A | prompt | `hub_prompts/data_quality/` |
| R10-A | prompt | `hub_prompts/eda_completa/` |
| R10-A | prompt | `hub_prompts/feature_engineering/` |
| R10-A | prompt | `hub_prompts/stat_check/` |
| R11-A | prompt | `hub_prompts/baseline_orchestration/` |
| R11-A | prompt | `hub_prompts/explainability/` |
| R11-A | prompt | `hub_prompts/monitoramento_modelo/` |
| R11-A | prompt | `hub_prompts/pipeline/` |
| R11-A | prompt | `hub_prompts/safra/` |
| R11-B | prompt | `hub_prompts/auditoria_skills/` |
| R11-B | prompt | `hub_prompts/comentar_notebook/` |
| R11-B | prompt | `hub_prompts/novo_projeto/` |
| R11-B | prompt | `hub_prompts/tutor_explicar/` |

## 12. Fontes internas examinadas e limites de procedência

O inventário foi obtido pelas árvores Git dos hubs no commit de referência. As regras e decisões foram conferidas na mesma base. As leituras de código são pontuais, suficientes para o planejamento, não um laudo de correção de todos os módulos.

Fontes internas principais: `CLAUDE.md`; `.claude/CLAUDE.md`; `.claude/rules/docs-e-readmes.md`; `.claude/rules/multi-llm.md`; `docs/decisions/ADR-0007-catalogo-e-pasta-de-objeto.md`; `docs/decisions/ADR-0010-manual-tecnico-unificado.md`; `ambiente_fonte/.assistant/hub_padroes/readme/template.md`; `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md`; `ambiente_fonte/.assistant_instructions.md`; trechos pertinentes do Manual e de `tools/validate_assistant.py`; `tools/ci_local.py`; `tools/render_simulado.py`; e a implementação de `train_xgboost`.

Os campos metodológicos deste documento são proposta de trabalho. Regras públicas da plataforma, afirmações estatísticas detalhadas e requisitos de bibliotecas precisam ser pesquisados e citados na elaboração de cada README pertinente. Não usar este plano como substituto de referências externas de domínio.

O pacote contém `MATRIZ_IMPACTOS_DOCUMENTAIS.md`, `INVENTARIO_READMES.json`, `IMPACTOS_DOCUMENTAIS.json`, `CHECKPOINT_R00.md` e `VALIDACAO_DO_PLANO.json`. O estado de implementação permanece planejado em todos os objetos.
