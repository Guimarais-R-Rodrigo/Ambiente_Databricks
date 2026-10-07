# MT atlas 02

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0051"></a>
<a id="doc-0051"></a>
### D0051 — Formulário de monitoramento de modelo

Este formulário pede modelo, run ou versão, endpoint/job, baseline, janela atual, target e atraso do rótulo, métricas com direção, segmentos, limites, frequência, owners e modo. Esses campos ligam cada alerta a uma população e a uma ação possível. Sem rótulo maduro, um diagnóstico pode tratar serviço e dados, mas não afirmar queda de qualidade preditiva.

O fluxo manda confirmar lineage entre modelo, features, predições e rótulos. Se PR-AUC, resumo da curva de precisão versus recall, melhora e Brier, erro quadrático médio das probabilidades previstas, piora, não se deve aplicar o mesmo sinal às duas métricas: cada uma tem unidade e direção próprias. O formulário pede testar melhora, piora, ausência de rótulo, nulos e baixo volume; recomenda janela, deduplicação, owner e critério de resolução para cada alerta. Drift é observação de mudança, não causa comprovada nem ordem de retreino.

A saída solicitada inclui mapa de observabilidade, catálogo de métricas, diagnóstico, código opcional e runbook. Um pedido em modo desenho não instala monitor, registra webhook, reinicia job ou promove modelo. Execução segue a skill selecionada, sua policy e o perfil suportado; helpers diretos não substituem essa rota. Thresholds de exemplo são ilustrativos e precisam de calibração ao caso e aprovação. O [README](MT-atlas-01.md#doc-0050) explica a escolha inicial.

<!-- editorial:exclude:start -->
Fonte: [monitoramento_modelo/monitoramento_modelo.md](../../hub_prompts/monitoramento_modelo/monitoramento_modelo.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0050](MT-atlas-01.md#doc-0050) · [Próximo: D0052](#doc-0052) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0052"></a>
<a id="doc-0052"></a>
### D0052 — Guia de início de projeto analítico

O README de `novo_projeto` situa o briefing antes de criar pastas, jobs ou tabelas. Seu uso é organizar problema e decisão, donos, métricas, fontes, entregáveis, ambientes e backlog num charter verificável. O guia alerta que escolher arquitetura antes de acordar objetivo e definição de pronto pode cristalizar premissas erradas; um texto gerado não substitui descoberta com negócio e owners reais.

Num projeto de retenção, descreva unidade, evento, horizonte, guardrails e quem aprova antes de pedir árvore de repositório. O guia recomenda `AGENTS.md` apenas no diretório correto, com instruções locais pertinentes, sem duplicar preferências globais ou guardar segredos. Também separa convenções `hub_` do recurso oficial Databricks. Uma proposta de bundle ou alvo dev/stage/prod ainda precisa de revisão e autorização antes de criar recursos.

O notebook de exemplo sobrescreve `workspace.default.hub_exemplo_clientes` como contexto sintético, embora o modo demonstrado seja SOMENTE_PLANO. Portanto, executar o preparo tem efeito próprio; leia o destino antes da célula. Abrir o README ou preencher o charter não cria diretório, não configura memória e não faz deploy. O [formulário](#doc-0053) é o pedido manual.

<!-- editorial:exclude:start -->
Fonte: [novo_projeto/README.md](../../hub_prompts/novo_projeto/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0051](#doc-0051) · [Próximo: D0053](#doc-0053) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0053"></a>
<a id="doc-0053"></a>
### D0053 — Formulário para iniciar projeto

O formulário de `novo_projeto` pede nome estável, problema e decisão, donos, critério de sucesso com guardrails, fontes, entidade e horizonte, entregáveis, ambientes, restrições, repositório e modo. Não há skill analítica única para esta etapa; a skill do trabalho definido pode ser mencionada depois. Campos desconhecidos ficam `NÃO INFORMADO`, especialmente catálogos, permissões e responsáveis.

Num projeto de priorização de contatos, “aumentar conversão” precisa de unidade, prazo e restrições como reclamações ou tratamento de dados sensíveis. O fluxo solicita charter, árvore simples, backlog, testes e contexto local. O `AGENTS.md` proposto deve caber no ancestral certo e conter somente instruções aplicáveis ali; copiar regras globais ou incluir token em arquivo versionado torna a saída inadequada. Um bundle com targets separados é uma proposta quando faz sentido, não deploy realizado.

O modo SOMENTE_PLANO produz desenho para revisão; GERAR_ARQUIVOS depende de escopo e autorização efetivos. O texto do formulário não cria diretórios nem configura instruções hierárquicas automaticamente. Antes de aceitar o material, confirme owners, placeholders, caminhos, ambientes e ações que ainda exigem autorização. O [guia](#doc-0052) ajuda a decidir se já há contexto suficiente.

<!-- editorial:exclude:start -->
Fonte: [novo_projeto/novo_projeto.md](../../hub_prompts/novo_projeto/novo_projeto.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0052](#doc-0052) · [Próximo: D0054](#doc-0054) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0054"></a>
<a id="doc-0054"></a>
### D0054 — Guia de pipeline de dados

O README de `pipeline` ajuda a decidir quando pedir arquitetura de ingestão e transformação. Exige objetivo, fontes e destinos, modo batch, streaming ou CDC (captura de alterações de dados), chaves, schema, qualidade, SLO (objetivo de nível de serviço) e ambientes. Automatizar uma fonte mal entendida apenas repete erros mais depressa; por isso o guia recomenda definir contrato, reprocessamento e idempotência antes de desenhar bundle ou deploy.

Se eventos chegam atrasados, uma chave e sequência devem resolver atualização fora de ordem, enquanto checkpoint e política de late data preservam o estado. Streaming não é escolha automática. Esse SLO expressa latência desejada; não demonstra que o pipeline a cumpre. O README pede testar duplicatas, evolução de schema, falha parcial e parametrização por ambiente. Lakeflow pode ser apropriado, conforme caso e disponibilidade, mas a escolha precisa ser justificada.

O notebook preparatório sobrescreve `workspace.default.hub_exemplo_clientes`; não cria pipeline real. O briefing gera uma solicitação, e eventual YAML (formato estruturado de configuração) ou código produzido ainda é proposta até validação e autorização de deploy. Spec local, runner Spark/Delta e efeitos persistentes são rotas distintas; persistência exige destino, autorização e evidência de execução, readback e limpeza. O [formulário](#doc-0055) detalha contrato e modo.

<!-- editorial:exclude:start -->
Fonte: [pipeline/README.md](../../hub_prompts/pipeline/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0053](#doc-0053) · [Próximo: D0055](#doc-0055) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0055"></a>
<a id="doc-0055"></a>
### D0055 — Formulário de pipeline de dados

O formulário de pipeline pede consumidores, fontes e cadência de chegada, destinos e grão, modo batch/streaming/CDC (captura de alterações de dados), chave e sequência, schema, regras de qualidade, SLO (objetivo de nível de serviço), volume, ambientes, permissões e modo de entrega. Ele serve para transformar uma solicitação vaga em arquitetura testável, sem tratar pedido de código como autorização de escrita ou deploy.

Imagine JSON, formato estruturado de dados, chegando de modo incremental para tabela silver por evento. `id_evento` e `ts_atualizacao` precisam definir deduplicação e desempate; late data, mudança de schema e reprocessamento devem ter tratamento explícito. O fluxo sugere Lakeflow Spark Declarative Pipelines quando adequado, expectations com ação, observabilidade no event log e bundle para targets de ambiente se houver ciclo de implantação. A saída esperada inclui contratos de entrada e saída, testes, plano de rollback e custo, mas não prova que esses recursos existem ou funcionam.

A validação final pede duplicatas, atraso, schema novo, falha parcial e writes idempotentes. Um SLO p95 menor que 15 minutos é meta a verificar com medições, não garantia do formulário. O texto proíbe gravar destino, mudar grants ou iniciar pipeline sem plano, ambiente e autorização. Execução segue a skill selecionada, sua policy e o perfil suportado; helpers diretos não substituem essa rota. O [README](#doc-0054) ajuda na escolha.

<!-- editorial:exclude:start -->
Fonte: [pipeline/pipeline.md](../../hub_prompts/pipeline/pipeline.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0054](#doc-0054) · [Próximo: D0056](#doc-0056) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0056"></a>
<a id="doc-0056"></a>
### D0056 — Guia de análise por safra

O README de `safra` apresenta um briefing para comparar coortes na mesma idade de observação. Safra é o grupo definido pela entrada em um período; idade pode ser mês desde entrada, ou MOB no exemplo. Antes de interpretar uma curva, declare entidade, evento, numerador, denominador, maturação e censura. Uma célula ainda não observável não é taxa zero.

Se a coorte de janeiro tem seis meses e a de maio apenas dois, comparar seus valores cumulativos no mês seis confunde ausência de observação com melhora. O guia orienta montar grade safra por idade, preservar células imaturas e reconciliar entidades, numerador e denominador. Somar taxas cumulativas ou contar o mesmo evento duas vezes distorce a curva. Diferenças entre coortes podem refletir mix ou maturação; o briefing não prova causalidade nem estabelece regra normativa sem fonte.

O notebook associado sobrescreve `workspace.default.hub_exemplo_safras` no preparo sintético; conferir o destino antes de executá-lo. Abrir o README ou preencher o formulário não mede uma safra. O perfil sintético `MONTHLY_BINARY_PILOT_V1` preserva roster fixo: cobertura incompleta não autoriza reduzir denominador. O cálculo reutilizável `vintage_analysis` é alternativa quando a tarefa já exige implementação verificada, enquanto este guia apoia o pedido e a interpretação inicial.

<!-- editorial:exclude:start -->
Fonte: [safra/README.md](../../hub_prompts/safra/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0055](#doc-0055) · [Próximo: D0057](#doc-0057) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0057"></a>
<a id="doc-0057"></a>
### D0057 — Formulário de análise por safra

O formulário de safra organiza o pedido para quem precisa comparar coortes no mesmo estágio de maturação. Informe dataset, entidade e chave, data de entrada, frequência, snapshots, idade, evento, numerador, denominador, métrica, censura, segmentos e período. A referência normativa só entra quando existe fonte aplicável; definição analítica não vira obrigação regulatória por estar no prompt.

Considere contratos originados por mês e primeiro atraso de 30 dias. A idade mensal, ou MOB, mês desde a originação, permite comparar janeiro e fevereiro até uma idade comum. Uma célula que ainda não maturou fica não observável, nunca zero. O fluxo pede grade safra por idade, totais reconciliados, entidades deduplicadas, taxas com denominador explícito e alertas de baixo volume. Taxas cumulativas não devem ser somadas; monotonicidade só é teste válido quando a métrica definida a exige.

O contrato de saída solicita dicionário, matriz, curvas, limitações e código apenas se pedido. O texto não lê a tabela, não calcula curva nem grava resultado. Para executar, siga skill, policy e contrato da rota suportada, sem substituí-los por chamada direta ao helper. Dados incompletos e composição diferente entre safras limitam qualquer interpretação causal; o [guia](#doc-0056) explica quando escolher este briefing.

<!-- editorial:exclude:start -->
Fonte: [safra/safra.md](../../hub_prompts/safra/safra.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0056](#doc-0056) · [Próximo: D0058](#doc-0058) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0058"></a>
<a id="doc-0058"></a>
### D0058 — Guia para checagem estatística

O README de `stat_check` orienta escolher um briefing estatístico antes de modelagem ou inferência. Seu consumidor precisa decidir se a tarefa é previsão, estimativa de um efeito ou experimento, pois essa finalidade muda unidade amostral, método e interpretação. O guia relaciona pergunta e estimando — a quantidade que se quer estimar — com pressupostos, tamanho de efeito e incerteza; um p-valor isolado não responde à decisão.

Imagine comparar conversão entre grupos quando os mesmos clientes aparecem em vários meses. Tratar linhas como observações independentes pode exagerar a evidência; unidade, repetição, tempo e mecanismo de seleção devem ser declarados antes do teste. Muitas comparações até achar significância também exigem cautela com multiplicidade. Um efeito estatisticamente detectável pode ser pequeno para o negócio e não demonstra causalidade sem desenho adequado.

O README remete ao formulário para campos e contrato de saída. Seu notebook ilustrativo usa `mode("overwrite")` para preparar `workspace.default.hub_exemplo_clientes`; executar a Parte 1 pode substituí-la. O perfil `TWO_SAMPLE_KS_PILOT_V1` executa um recorte sintético delimitado, sem representar toda validação estatística. Abrir o guia não calcula estatística nem valida uma hipótese. Confira desenho, população e resultados observados antes de aceitar conclusão.

<!-- editorial:exclude:start -->
Fonte: [stat_check/README.md](../../hub_prompts/stat_check/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0057](#doc-0057) · [Próximo: D0059](#doc-0059) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0059"></a>
<a id="doc-0059"></a>
### D0059 — Formulário de validação estatística

O formulário de `stat_check` transforma uma dúvida estatística em pedido verificável. Anexe dataset e declare grão, chave, grupos repetidos, target, finalidade, método ou pedido de seleção, população, tempo, hipóteses, critérios, volume, restrições e modo. A finalidade — previsão, inferência ou experimento — vem antes da técnica. Um campo essencial ausente deve ficar `NÃO INFORMADO`, sem números inventados.

Num estudo de conversão por canal, a pergunta pode ser diferença de taxas entre grupos; o estimando é essa diferença na população definida. O fluxo pede checar seleção, unidade independente e dependência temporal, mapear método a pressupostos e relatar tamanho de efeito com incerteza. MDE significa efeito mínimo detectável; se usado, precisa de critério e desenho, não limiar universal. Um p-valor baixo em amostra grande não torna o efeito relevante nem estabelece causalidade.

O contrato espera matriz de perguntas, diagnósticos, interpretação e ameaças à validade. Código é opcional; execução exige autorização, dados compatíveis com o perfil e a rota da skill/policy. Helpers diretos não contornam essa rota. Sem leitura do dataset, a resposta honesta é plano ou hipótese, não teste executado. PII, informações pessoais identificáveis, não devem ser expostas; o [README](#doc-0058) ajuda na escolha.

<!-- editorial:exclude:start -->
Fonte: [stat_check/stat_check.md](../../hub_prompts/stat_check/stat_check.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0058](#doc-0058) · [Próximo: D0060](#doc-0060) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0060"></a>
<a id="doc-0060"></a>
### D0060 — Guia de tutoria sobre objetos Databricks

O README de `tutor_explicar` situa um briefing para explicar código, tabela, erro ou pipeline anexado no nível do leitor. Serve quando há objeto real e dúvida concreta: “por que este join embaralha dados?” é mais útil que “explique Spark”. O consumidor informa objetivo prático, profundidade, ambiente e restrições para obter explicação que ajude na próxima tarefa.

O guia recomenda começar por mapa mental e termos definidos antes de detalhes. Uma analogia pode introduzir um conceito, mas deve dizer onde deixa de representar o comportamento real. Em um notebook de join temporal, por exemplo, a resposta deve ligar entradas, saída e custo ao código efetivamente lido; se o arquivo não estiver disponível, deve declarar a limitação em vez de narrar linhas imaginárias. Comportamento de plataforma exige versão ou referência atual, não confiança em uma API (interface de programação) lembrada.

O notebook de exemplo lê `pit_join.py`, mas imprime somente as 20 primeiras linhas; não cria tabela nem comprova contexto integral no chat. O briefing produz pedido, não tutoria executada. A explicação não substitui revisão de correção do código nem autorização para alterá-lo. O [formulário](#doc-0061) define os campos da solicitação.

<!-- editorial:exclude:start -->
Fonte: [tutor_explicar/README.md](../../hub_prompts/tutor_explicar/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0059](#doc-0059) · [Próximo: D0061](#doc-0061) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0061"></a>
<a id="doc-0061"></a>
### D0061 — Formulário de tutoria técnica

O formulário de `tutor_explicar` pede objeto ou pergunta anexada, nível iniciante/intermediário/avançado, profundidade, tarefa futura, ambiente, contexto de negócio e restrições. Essas escolhas permitem calibrar vocabulário e exemplo sem inventar schema ou acesso. Se runtime ou versão forem desconhecidos, use `NÃO INFORMADO` e limite afirmações dependentes de plataforma.

Para entender o shuffle, redistribuição de dados entre partições, de um join, a pessoa pode anexar a célula e pedir explicação passo a passo. O método solicitado começa com resposta direta e mapa mental, depois cobre entradas, saídas, execução lazy (adiada) ou eager (imediata), movimentação de dados, custo, falhas e verificação. Exige distinguir comportamento documentado, boa prática e opinião. O contrato pede exemplo mínimo, armadilhas e perguntas de autoavaliação, cujas respostas ficam em seção separada para permitir estudo.

A resposta deve marcar o que foi lido no objeto, o que foi inferido e o que não pôde ser verificado. Um snippet proposto não é experimento realizado; o texto instrui a não executar nem alterar recursos. Se teste pequeno ajudar, ele fica como sugestão reversível, sujeita à autorização. O [guia](#doc-0060) situa quando tutoria não basta para revisão.

<!-- editorial:exclude:start -->
Fonte: [tutor_explicar/tutor_explicar.md](../../hub_prompts/tutor_explicar/tutor_explicar.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0060](#doc-0060) · [Próximo: D0062](#doc-0062) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0062"></a>
<a id="doc-0062"></a>
### D0062 — Como conferir a mensagem de uma figura sem depender do PNG?

`CONTEUDO_FIGURAS.md` é o índice textual das 21 figuras editoriais distribuídas entre raiz, entrada `.assistant`, snippets, scripts, skills e prompts. Cada bloco nomeia a figura, pergunta que ela responde, alt, caminho do PNG, síntese e rótulos mostrados. Essa estrutura permite ao mantenedor comparar intenção, legenda e palavras da imagem sem usar OCR, e dá ao leitor outra rota para a informação essencial.

As figuras cobrem relações diferentes: mapa de componentes, corte entre contexto e runtime, pista de promoção, anatomia de pasta, fluxo de uso, contratos de retorno e seleção de skill ou briefing. O texto esclarece limites que uma seta isolada poderia esconder: skill orientar não importa helper; script diagnosticar não agenda tarefa; PASS de `data_quality_check` não homologa dados. Os READMEs consumidores continuam donos da explicação e dos exemplos copiáveis.

Na manutenção, atualize esse índice junto com o código de composição, o PNG final e o README que incorpora cada figura. O arquivo não autoriza inferir recurso da plataforma pela cor ou pela ilustração; cabeçalhos decorativos ficam fora das 21 explicações operacionais. A revisão visual e textual precisa conferir a mesma mensagem, sem promover asset apenas porque o índice foi preenchido.

<!-- editorial:exclude:start -->
Fonte: [CONTEUDO_FIGURAS.md](../../hub_readmes_visual_assets/CONTEUDO_FIGURAS.md). Detalhe: [MT25](MT-parte-vi.md#mt25).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0061](#doc-0061) · [Próximo: D0063](#doc-0063) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0063"></a>
<a id="doc-0063"></a>
### D0063 — Como o pacote visual dos READMEs é mantido?

O README de `hub_readmes_visual_assets` apresenta a árvore de imagens, cabeçalhos, especificações, licenças e diagramas por família de README, separada dos insumos e QA de manutenção. Ele distingue o que o consumidor usa do que o autor altera: PNGs em `png/` são saídas referenciadas nos documentos; SVGs em `sources/` são gerados com tipografia em paths; código em `tools/readme_visuals/` compõe diagramas. Cinco assinaturas aprovadas têm SVGs congelados por hash. Os insumos dos cabeçalhos ficam em `tools/readme_visuals/assets/headers/src/`: `copy.json` contém texto editável e a arte-base permanece raster; QA fica em `tools/readme_visuals/qa/`, fora da instalação.

O guia do mantenedor reúne compositor de headers, produção por família, validação, gate do produto e renderer do simulado. `CONTEUDO_FIGURAS.md` guarda equivalentes textuais para a revisão sem OCR. Uma rota V06 parte de tema resolvido e escreve variantes fora do pacote ativo em `.artifacts/`; mudança de bytes pede revisão antes de promoção. Os comandos do renderer antigo são históricos e não regeneram o pacote v2.

Quem usa o Hub referencia os PNGs compartilhados, sem copiar imagens em cada notebook. Na manutenção, preservar hashes congelados, licença e texto circundante. O pacote é conteúdo customizado; a Genie Code não o descobre automaticamente, e gerar uma variante não significa aprovar tema ou publicar no Databricks.

<!-- editorial:exclude:start -->
Fonte: [README dos Visual Assets](../../hub_readmes_visual_assets/README.md). Detalhe: [MT25](MT-parte-vi.md#mt25).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0062](#doc-0062) · [Próximo: D0064](#doc-0064) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0064"></a>
<a id="doc-0064"></a>
### D0064 — Qual cabeçalho escolher para um documento?

O README de `headers/` ajuda a escolher entre dois PNGs compartilhados: CRM para guias e notebooks gerais, Squad para notebook específico da equipe. A regra evita empilhar identidades concorrentes. O documento mostra sintaxe Markdown e `%md` de notebook com caminho relativo; a imagem é embutida, não importada como Python, e precisa viajar com a árvore de assets até o destino.

Os exemplos preservam título e instruções como texto normal abaixo do banner. Um alt descritivo identifica a imagem, ou alt vazio pode marcá-la decorativa quando a mesma identificação já está imediatamente no texto. As conexões luminosas da arte não representam execução ou permissão. A faixa CRM foi composta em 1920 × 480 para caber no topo sem reduzir o texto a ponto de comprometer leitura.

A autoria fica no repositório: `tools/readme_visuals/assets/headers/src/` preserva fundo raster, texto editável e proveniência; `tools/readme_visuals/qa/` reúne verificações. O comando `headers.mjs` recompõe os PNGs finais, que seguem no produto com a licença Inter. Essas fontes de manutenção não integram o pacote instalado. Ao alterar título ou visual, revise caminho, alt, hashes e renderização no documento consumidor.

<!-- editorial:exclude:start -->
Fonte: [README de cabeçalhos](../../hub_readmes_visual_assets/headers/README.md). Detalhe: [MT25](MT-parte-vi.md#mt25).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0063](#doc-0063) · [Próximo: D0065](#doc-0065) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0065"></a>
<a id="doc-0065"></a>
### D0065 — De onde veio o fundo dos cabeçalhos?

`PROMPT_FUNDO.md` registra a proveniência da arte-base criada para os dois banners em 10/09/2026. O bloco de prompt solicita fundo tecnológico ultralargo sem letras, números, logo, gráfico de dados ou setas de fluxo: a área esquerda deveria ficar escura e calma para receber títulos; uma constelação analítica decorativa ocuparia a direita. Essa separação preserva texto exato sob controle do compositor, em vez de pedir à geração raster que desenhe tipografia.

O resultado efetivo teve 1983 × 793 pixels, diferente dos 1920 × 480 pedidos. O documento descreve o tratamento: preservar o original inteiro, encaixá-lo proporcionalmente pela altura no lado direito do canvas final, misturar a borda esquerda ao navy e acrescentar textos Inter convertidos em paths vetoriais. A arte não é redesenhada pelo compositor. Os arquivos `*_tipografia.svg` contêm somente a camada de letras, nunca a ilustração completa.

A fonte foi realocada para ferramentas do mantenedor e não integra mais o produto distribuído. Quem mantém headers usa esse registro para explicar origem e reprodução limitada. Reenviar o mesmo prompt não produz os mesmos bytes; o original raster congelado é a entrada verificável. Qualquer troca exige nova proposta, revisão do aspecto e dos hashes, sem tratar a imagem como diagrama funcional.

<!-- editorial:exclude:start -->
Fonte: [PROMPT_FUNDO.md](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_visuals/assets/headers/src/PROMPT_FUNDO.md). Detalhe: [MT25](MT-parte-vi.md#mt25).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0064](#doc-0064) · [Próximo: D0066](#doc-0066) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0066"></a>
<a id="doc-0066"></a>
### D0066 — Que regras tornam os diagramas legíveis e fiéis?

`guia_visual.md` reúne decisões de composição para as figuras dos READMEs. Seu objetivo é que cada figura esclareça uma pergunta central e também funcione em apresentação. A semântica de cor distingue mecanismo nativo Databricks, conteúdo Hub, decisão humana, evidência e apoio metodológico. Rótulos e legendas acompanham as cores; uma pessoa não precisa deduzir significado pelo matiz.

As regras exigem título que afirme a mensagem, subtítulo que delimite leitura, frases curtas nos cartões e setas somente para dependência ou sequência real. O corpo do README conserva o equivalente textual da informação essencial. Arquétipos como atlas, corte, pista, dossiê e jornada são escolhidos pela relação explicada, evitando a mesma grade de caixas para todo assunto. PNG é a saída publicada; SVG vem do código de composição com Inter em paths. Cabeçalhos seguem outra lógica: raster decorativo com texto preciso, sem legenda operacional.

A receita de geração pertence ao guia externo de autoria do mantenedor; este documento conserva as regras de uso e revisão. Na manutenção, conferir figura e texto juntos, dimensões, contraste e hashes do pacote. O brilho não substitui contraste e a cor nunca cria um contrato analítico ou autorização.

<!-- editorial:exclude:start -->
Fonte: [guia_visual.md](../../hub_readmes_visual_assets/visual_system/guia_visual.md). Detalhe: [MT25](MT-parte-vi.md#mt25).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0065](#doc-0065) · [Próximo: D0067](#doc-0067) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0067"></a>
<a id="doc-0067"></a>
### D0067 — Como atribuir os componentes das figuras?

`licencas.md` separa a proveniência do sistema visual dos READMEs. O arquivo permite ao mantenedor distinguir fonte tipográfica, ícones, código geométrico e arte raster antes de redistribuir uma figura. Inter usa a licença SIL Open Font License; Lucide, a ISC. Os avisos completos acompanham os assets; reconstrução e versões de dependências são administradas pelo mantenedor. Essas licenças não atribuem automaticamente direitos à arte-base raster gerada para cabeçalhos.

Na produção, diagramas partem de código e exportam PNG para o README; SVG intermediário transforma glifos Inter em paths. Um exemplo válido de manutenção é atualizar um ícone Lucide, registrar a versão e reexecutar a composição e a validação visual contra o arquivo gerado. Para um cabeçalho, a arte congelada é entrada do pipeline; repetir o mesmo prompt não garante a mesma imagem. O consumidor desta página é quem recompõe, publica ou audita o pacote visual, não quem interpreta métricas de um notebook.

Ao trocar fonte, ícone ou raster, conferir licença própria, hashes e avisos junto dos artefatos. Uma imagem bonita ou reproduzível a partir do original não comprova permissão sobre outro componente nem substitui o equivalente textual da informação no README.

<!-- editorial:exclude:start -->
Fonte: [licencas.md](../../hub_readmes_visual_assets/visual_system/licencas.md). Detalhe: [MT25](MT-parte-vi.md#mt25).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0066](#doc-0066) · [Próximo: D0068](#doc-0068) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0068"></a>
<a id="doc-0068"></a>
### D0068 — Como escolher um Hub Script?

O README de `hub_scripts` existe para quem precisa executar uma tarefa delimitada sem adotar um fluxo analítico inteiro. Uma árvore com oito pastas não mostra, sozinha, se o próximo passo é descrever uma tabela, calcular RFV ou conferir um contrato de skill. Conceitualmente, o guia apresenta scripts como instrumentos escolhidos pela pergunta. Tecnicamente, reúne o catálogo, as entradas e os tipos distintos de saída: dicionários de diagnóstico, DataFrame Spark, texto serializado, lista de avisos e resultados tipados de preflight, Receipt, Postflight e policy.

O leitor o consulta antes do README de objeto e antes de importar Python. A figura do catálogo retrata os sete utilitários históricos; o texto situa `skill_execution` como oitavo recurso transversal, sem atribuir à imagem uma cobertura que ela não possui. O guia ainda mostra efeitos de execução, como leitura e agregação Spark, e separa diagnóstico de reação do processo consumidor. Na manutenção, conferir links para as pastas, nomes de API, quantidade de objetos e estados de enforcement. Ler o catálogo não executa scripts; rotas instrumentadas seguem a skill e sua policy, sem substituir o contrato específico nem autorizar uso dos dados.

<!-- editorial:exclude:start -->
Fonte: [README de Hub Scripts](../../hub_scripts/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0067](#doc-0067) · [Próximo: D0069](#doc-0069) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0069"></a>
<a id="doc-0069"></a>
### D0069 — Que qualidade o script consegue observar?

Este README orienta quem recebeu uma tabela e quer conferir três propriedades antes de analisá-la: chave candidata, proporção de valores nulos e atualidade opcional. Ele existe porque “qualidade” pode parecer um veredito único, enquanto as falhas têm causas e consequências diferentes. O documento explica quando `data_quality_check` é útil como diagnóstico ad hoc, o que informar em `pk_columns`, `date_column` e `thresholds`, e como ler `checks`, `alerts`, `status` e `score`.

A implementação abre uma tabela nomeada via Spark, agrega nulos e conta combinações distintas da chave. Por isso o leitor deve estabelecer o grão e a cadência esperada antes de chamar a função, além de considerar custo de leitura. Uma tabela mensal testada com frescor de dois dias pode reprovar por política inadequada. O score é uma convenção de penalidades por alerta, sem certificação geral: tabela vazia pode obter `pass`/100 sem freshness e com limiares padrão. Ao manter o README, sincronizar defaults, fórmula do score, nomes dos campos e regras inclusivas de limiar com o código. O consumidor decide se um `warn` ou `fail` bloqueia seu processo; o script não instala uma regra operacional em pipeline.

<!-- editorial:exclude:start -->
Fonte: [README de data_quality_check](../../hub_scripts/data_quality_check/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0068](#doc-0068) · [Próximo: D0070](#doc-0070) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0070"></a>
<a id="doc-0070"></a>
### D0070 — Como localizar código sem explicação próxima?

O README de `doc_coverage` oferece uma triagem para revisores de notebooks exportados. A pergunta é concreta: quais células de código não têm uma célula Markdown imediatamente anterior ou posterior? Essa definição estreita justifica a existência do documento, pois uma porcentagem de “cobertura” poderia ser confundida com avaliação da qualidade de escrita. O guia descreve formatos locais aceitos, saída com índices de células descobertas e leitura do percentual.

Tecnicamente, o script lê JSON de `.ipynb` ou separa fontes Databricks exportadas pelos marcadores de comando e de Markdown. Ele não abre URL do workspace, executa notebook nem interpreta se o texto explica o código certo. Um Markdown contendo apenas um ponto já conta como adjacente; um arquivo sem código retorna 100% por convenção. O leitor deve abrir os índices apontados e julgar o conteúdo. Na manutenção, conferir extensões, marcadores reconhecidos e campos do dicionário com o parser atual. Usar a métrica como meta de equipe incentivaria preencher células vazias; ela serve para priorizar revisão humana, não para conceder aprovação documental automática.

<!-- editorial:exclude:start -->
Fonte: [README de doc_coverage](../../hub_scripts/doc_coverage/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0069](#doc-0069) · [Próximo: D0071](#doc-0071) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0071"></a>
<a id="doc-0071"></a>
### D0071 — Como comparar distribuições numéricas por coorte?

Este README é a entrada do script `drift_detector` para o analista que compara duas coortes da mesma tabela. Ele existe porque médias parecidas podem esconder uma redistribuição importante, mas um índice de mudança não explica sozinho o desempenho de um modelo. O documento apresenta PSI — Índice de Estabilidade da População —, faixas construídas por quantis da referência, proporções das duas coortes e a classificação opcional por limiares locais.

O leitor precisa fornecer tabela, coluna que identifica coorte, dois valores presentes e colunas numéricas; a função exige ambas as populações não vazias. O retorno por coluna traz PSI, tamanhos, limites, buckets e classificação. Se qualquer um dos dois limiares estiver ausente, o estado fica `not_classified`; apenas com ambos a função valida sua ordem e classifica. A implementação utiliza quantis e agregações Spark, com piso `epsilon` para evitar logaritmo de zero. Na manutenção, conferir essa semântica e os nomes de saída contra o código, especialmente o bucket de ausentes. O script não trata variável categórica como CSI, não mede causalidade e não demonstra que o modelo perdeu performance. Sua saída indica onde investigar, sob referência e política declaradas.

<!-- editorial:exclude:start -->
Fonte: [README de drift_detector](../../hub_scripts/drift_detector/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0070](#doc-0070) · [Próximo: D0072](#doc-0072) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0072"></a>
<a id="doc-0072"></a>
### D0072 — De onde vem um aviso de nomenclatura?

O README de `naming_checker` orienta quem revisa nomes antes de compartilhar uma tabela. Ele existe porque convenções como letras minúsculas, limite de comprimento ou prefixo são úteis para manutenção, mas não podem ser apresentadas como proibição universal do Unity Catalog. O documento separa recomendação de contexto, convenção do projeto e política opcional da organização por meio do campo `policy` em cada aviso.

A função abre uma tabela ou view com Spark, lê o schema e devolve uma lista de dicionários, todos com severidade `warning`; não modifica dados nem renomeia objetos. Nome não qualificado, coluna fora da regex local e coluna longa podem gerar avisos. A regra de prefixo só faz sentido com `enforce_prefix=True` e `allowed_table_prefixes` não vazio; sem a lista, a chamada falha. Um elemento `""` passa para qualquer nome: exija prefixos não vazios. Uma view temporária sem três partes pode ser legítima mesmo com aviso. Ao manter o README, conferir regex, limite, condições de prefixo e origem da regra com a implementação. Lista vazia não prova qualidade semântica, compatibilidade de migração nem permissão de publicação; qualquer renomeação exige análise dos consumidores.

<!-- editorial:exclude:start -->
Fonte: [README de naming_checker](../../hub_scripts/naming_checker/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0071](#doc-0071) · [Próximo: D0073](#doc-0073) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0073"></a>
<a id="doc-0073"></a>
### D0073 — Que parte do perfil descreve a tabela inteira?

O README de `quick_profile` serve ao analista que precisa reconhecer uma fonte antes de escolher verificações específicas. Seu motivo principal é impedir que estatísticas de amostra sejam lidas como medidas integrais. A função recebe um nome de tabela, devolve estrutura, volume e nulos sobre todas as linhas, além de cardinalidade aproximada, categorias frequentes, resumos numéricos e intervalos de datas numa amostra declarada.

O documento ensina a conferir `sample_fraction`, `sample_seed` e `sample_rows` e informa que a seleção de colunas para certos resumos é limitada pela ordem do schema. Mesmo uma amostra pequena não evita a contagem integral de linhas e nulos; o script tenta cache e o libera, conforme suporte do ambiente. Valores categóricos podem aparecer na saída sem máscara. Versão da tabela, filtros, horário e ambiente precisam de registro externo ao retorno. Uma cardinalidade amostral aproximada não certifica unicidade de chave, e um perfil não equivale à EDA completa. Ao manter o guia, sincronizar campos, limites por tipo e efeitos Spark com a implementação e revisar o exemplo de view temporária. O leitor deve escolher uma fonte autorizada e registrar o alcance de cada número antes de compartilhá-lo.

<!-- editorial:exclude:start -->
Fonte: [README de quick_profile](../../hub_scripts/quick_profile/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0072](#doc-0072) · [Próximo: D0074](#doc-0074) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0074"></a>
<a id="doc-0074"></a>
### D0074 — Como calcular RFV até uma data comum?

O README de `rfv_calculator` atende quem quer resumir comportamento passado de uma entidade. RFV significa recência, frequência e valor; a data de referência existe para impedir que eventos posteriores entrem na fotografia. O guia apresenta uma API que recebe nome de tabela, colunas de cliente, data e valor, corte inclusivo e períodos positivos, devolvendo DataFrame Spark de medidas brutas. Ele não transforma essas medidas em score, quintis ou segmento. Exija chave não nula: joins de janela podem zerar a entidade nula.

O corte usa a data do evento: datas nulas ou posteriores ficam fora. Para uma janela de 30 dias, entram o dia do corte e os 29 anteriores. `frequencia_total` conta linhas, não pedidos distintos; um item por linha pode inflar a leitura de compras. Clientes sem evento válido até o corte não aparecem, enquanto janelas vazias de clientes com histórico recebem zero nos campos daquela janela. Na manutenção, conferir nomes das colunas geradas, regra de preenchimento e custo de uma agregação/join por período. O helper não conhece atraso de publicação nem decide um instante distinto para cada linha de previsão; nesses casos, a reconstrução point-in-time precisa de outra rota.

<!-- editorial:exclude:start -->
Fonte: [README de rfv_calculator](../../hub_scripts/rfv_calculator/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11), [MU10](MU-parte-iii.md#mu10).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0073](#doc-0073) · [Próximo: D0075](#doc-0075) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0075"></a>
<a id="doc-0075"></a>
### D0075 — Por que registrar um schema em YAML ou JSON?

O README de `schema_to_yaml` explica como transformar a estrutura vista pelo Spark em texto revisável. Ele existe porque uma revisão de mudança precisa comparar nomes, tipos, nulabilidade e comentários disponíveis sem copiar manualmente a interface do catálogo. A API `schema_to_dict` entrega dicionário; `schema_to_yaml` serializa esse retrato em YAML seguro ou, se o import de PyYAML gerar `ImportError`, em JSON compatível com YAML 1.2. O texto é uma fotografia da fonte no momento da chamada, não contrato governado automaticamente.

Sem `include_stats`, o trabalho se concentra no schema. Com ele, a função conta linhas, nulos e cardinalidades aproximadas em uma agregação ampla, o que muda custo e alcance do resultado. A API não oferece filtros ou seleção de colunas; delimitação depende de preparação autorizada. Comentários só aparecem se estiverem no metadata lido pelo helper; a ausência ali não prova inexistência em outras camadas. O guia serve a revisores e mantenedores de objetos, que devem registrar snapshot e comparar mudanças com consumidores reais. Na manutenção, conferir fallback, nomes de campos e custo de estatísticas com a implementação. Não usar `approx_distinct` para certificar unicidade nem supor que gerar arquivo atualiza o Unity Catalog.

<!-- editorial:exclude:start -->
Fonte: [README de schema_to_yaml](../../hub_scripts/schema_to_yaml/README.md). Detalhe: [MT11](MT-parte-ii.md#mt11).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0074](#doc-0074) · [Próximo: D0076](#doc-0076) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0076"></a>
<a id="doc-0076"></a>
### D0076 — Por que preflight, Receipt e Postflight têm resultados separados?

O README de `skill_execution` mapeia preflight, evidência e policy; a EDA (análise exploratória de dados) exemplifica sua rota. Seu primeiro passo, `run_preflight(contract_path, assistant_root=..., context=...)`, lê contrato e contexto e devolve `PreflightResult` com decisões e `PASS` ou `BLOCKED`. *Preflight* é a conferência anterior à lógica protegida: encontrar uma função ou template não prova que foi usado. O core `scripts/run.py::run` registra trace e pode emitir `ExecutionReceiptV1`, comprovante estruturado que vincula resultado, execução e release. A rota `scripts/run_enforced.py::run_enforced` observa imports, chamadas, conclusões e templates carregados. Depois, `scripts/postflight.py::finalize_or_raise` exige evidência aplicável e handoff, o conjunto de informações entregue ao fim.

O README distingue a rota EDA do notebook demonstrativo apenas L2. Sem chave estabelecida, `data_quality_check` é `not_applicable`; não se inventa chamada. No código atual, `run_enforced` pode devolver `PENDING_POSTFLIGHT` após o core, e só Postflight `PASS` com `completion.authorized=true` permite `completion.status="COMPLETED"`. Receipt `VALID` sozinho não satisfaz L4, nível de conclusão por Postflight. Para diagnóstico, compare `resources_resolved`, `resources_called`, `resources_completed`, `templates_loaded` e gaps, sem transformar um desses degraus em outro.

Na manutenção, confira as três implementações vinculadas no README e os scripts da skill antes de atualizar estados ou exemplos. A policy reúne quinze skills; perfis sintéticos não promovem nível nem generalizam L4. O documento explica a separação de responsabilidades; não é trace de uma run nem aprovação universal de conclusão.

<!-- editorial:exclude:start -->
Fonte: [README de skill_execution](../../hub_scripts/skill_execution/README.md). SHA-256 da fonte histórica: `2bc395b5365ba495df782e2cbb209f2d5359fb79ccaa4b62ae1478fdd01b8dd8`. Ponte: [MT17](MT-parte-iv.md#mt17), [MT18](MT-parte-iv.md#mt18), [MT19](MT-parte-iv.md#mt19).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0075](#doc-0075) · [Próximo: D0077](#doc-0077) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0077"></a>
<a id="doc-0077"></a>
### D0077 — Que contexto temporal pode ser resolvido sem fazer join?

O README de `domain_context` apresenta um validador interno para os perfis sintéticos de safra e cross-EDA (análise exploratória de dados entre fontes). A fachada exporta `validate_temporal_context(*, pit, temporal, decision_at, not_applicable_reason=None)`: PIT significa *point in time*, a exigência de respeitar a informação disponível no instante de decisão. O retorno registra intenção, instante normalizado e configuração, sempre com `join_executed=false`. Não lê fonte externa nem seleciona linhas.

Um exemplo estático com `pit="APPLICABLE"` declara relógios de referência e disponibilidade distintos, UTC (tempo universal coordenado), atraso constante, fronteira `LE` (menor ou igual, inclusiva) ou `LT` (menor que, exclusiva) e desempate `REJECT`. Se PIT for `UNKNOWN`, o validador bloqueia; se for `NOT_APPLICABLE`, exige motivo e `temporal=null`. `ContextError` identifica configurações recusadas. A fachada também oferece `loads_strict`, que rejeita chaves JSON (formato textual de dados estruturados) repetidas e números não finitos. Esses limites preservam lacunas temporais explícitas.

Os preflights de [safra](../../skills/hub-ml-analise-safra/scripts/preflight.py) e [cross-EDA](../../skills/hub-ml-cross-eda-ml/scripts/preflight.py) consomem verificações de domínio antes de cálculo ou join. `release.py` confere o fileset protegido da safra; não autentica bibliotecas externas. Na manutenção, confronte o README com a fachada e cada consumidor. Contexto resolvido não demonstra que fonte foi lida, cobertura medida, Spark executado ou prontidão de ML (aprendizado de máquina). O componente integrado não promove policy; consumidores novos exigem integração e testes próprios.

<!-- editorial:exclude:start -->
Fonte: [README de domain_context](../../hub_scripts/skill_execution/domain_context/README.md). SHA-256 da fonte histórica: `88698f04bee8f38b084f9c89bbfbf5d904421bf5a4e5f02215b3fdcb47194af1`. Ponte: [MT17](MT-parte-iv.md#mt17), [MU04](MU-parte-ii.md#mu04).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0076](#doc-0076) · [Próximo: D0078](#doc-0078) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0078"></a>
<a id="doc-0078"></a>
### D0078 — Entrada narrativa da biblioteca de snippets

O README de `hub_snippets/` ajuda o leitor a escolher uma função pela natureza da tarefa antes de procurar um nome de API. Ele apresenta snippets como peças reutilizáveis de cálculo, Spark, apresentação, visualização e dados sintéticos, sem pedir que cada notebook reimplemente a mesma lógica. Tecnicamente, explica a pasta por objeto: README de escolha, fachada pública `__init__.py`, módulo de implementação e notebook didático. A função é importada e chamada pelo código do usuário; a Genie Code não carrega toda a biblioteca automaticamente.

O mapa navega por seis categorias: `ml`, `spark`, `display`, `visual`, `constants` e `testing`. Cada índice local leva aos READMEs dos objetos, onde dependências, efeitos e limites ficam próximos do código. O autor do produto mantém a entrada e os links; analistas a consultam para reduzir candidatos. O catálogo integrado do Manual Técnico vigente continua sendo o índice canônico das APIs; este README oferece leitura narrativa, não uma segunda assinatura oficial para cada helper.

A presença de um nome na lista não prova instalação no workspace, compatibilidade do compute nem adequação do método à base. Os caminhos de tema visual descritos ali são opt-in, sem alterar automaticamente notebooks existentes. Ao manter a página, confira categorias e links contra a árvore atual e diferencie resultados de exemplos históricos de testes no destino do leitor.

<!-- editorial:exclude:start -->
Fonte: [hub_snippets/README.md](../../hub_snippets/README.md). Contexto: [MT05](MT-parte-ii.md#mt05).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0077](#doc-0077) · [Próximo: D0079](#doc-0079) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0079"></a>
<a id="doc-0079"></a>
### D0079 — Onde encontrar constantes reutilizáveis?

O README de `constants` é o índice da categoria de snippets que fornece convenções de apresentação. Ele encaminha o leitor a `colors`, `emojis`, `format_br` e `styles`, permitindo escolher uma dependência pequena antes de importar código. `colors` entrega valores e paletas; `emojis`, rótulos semânticos; `format_br`, textos numéricos; `styles`, CSS de componentes. Um notebook que precisa exibir uma taxa pode ir diretamente a `format_br`, enquanto outro que compõe uma tabela colorida deve examinar também a semântica de `colors`.

Este índice não é o README de contrato de um objeto individual. A assinatura, os parâmetros, a saída e os limites operacionais estão nas páginas dos quatro objetos e em seus módulos. Um uso válido começa pela pergunta de apresentação, abre o README específico, verifica o import e reproduz o exemplo com dado sintético. Importar toda a categoria não demonstra que o tema visual foi aplicado ou que a métrica foi calculada corretamente.

Na manutenção, procurar consumidores dos nomes compartilhados antes de renomear uma constante ou alterar uma escala. Uma mudança local de cor, emoji ou formato pode modificar vários notebooks sem alterar o dado subjacente. O índice deve acompanhar a árvore real, mas sua existência não é homologação de execução.

<!-- editorial:exclude:start -->
Fonte: [README de constants](../../hub_snippets/constants/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0078](#doc-0078) · [Próximo: D0080](#doc-0080) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0080"></a>
<a id="doc-0080"></a>
### D0080 — O que a paleta comunica e o que não calcula?

O README de `colors` documenta constantes hexadecimais e três famílias de paletas para visualizações. A categórica tem dez cores; sequencial e divergente têm cinco cada. As cores de estado, como alerta e positivo, oferecem linguagem visual comum ao Hub, mas não calculam o estado de uma métrica. O consumidor deve decidir a regra analítica antes de mapear seu resultado para uma cor.

Um exemplo válido é copiar `PALETA_CATEGORICA` para uma figura local e declarar qual categoria recebe cada índice. A cópia evita que um ajuste pontual altere a lista compartilhada em memória. Uma escala divergente pede centro e domínio explícitos; a mera escolha da lista não normaliza valores. Para um alerta, escrever também o rótulo textual e o critério que produziu a classe. Assim, cor e legenda continuam compreensíveis sem depender do matiz.

Na manutenção, conferir imports, ordem das paletas e contraste nos fundos reais. O README registra pares de texto branco sobre cores de alerta ou positivo com contraste insuficiente; reutilizar a constante não resolve isso. As listas são mutáveis, portanto efeitos de uma modificação em runtime exigem cuidado. A página é contrato de apresentação, não evidência de qualidade dos dados nem aprovação de acessibilidade do consumidor.

<!-- editorial:exclude:start -->
Fonte: [README de colors](../../hub_snippets/constants/colors/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0079](#doc-0079) · [Próximo: D0081](#doc-0081) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0081"></a>
<a id="doc-0081"></a>
### D0081 — Como usar emojis sem transformá-los em evidência?

`emojis` concentra dois mapas para comunicar o roteiro EDA. `SECOES_EDA` associa as etapas 0 a 8 a símbolos e rótulos; `SEMANTICA` oferece marcas para interpretação e ação. O README ajuda autores de notebooks e componentes visuais a manter um vocabulário reconhecível, sem reescrever esses sinais em cada célula. O mapa serve à leitura humana, enquanto a lógica analítica permanece no código e no texto do diagnóstico.

Um exemplo válido é usar a entrada de atenção para abrir um comentário que também diga “há nulos na coluna” e informe a contagem observada. O emoji sozinho não informa quantidade, severidade nem se o teste foi executado. A chave de etapa precisa existir: buscar etapa fora de 0–8 por indexação direta gera `KeyError`. Se um notebook precisar estender rótulos, deve construir estrutura própria sem alterar o mapa global.

Na manutenção, conferir consumidores e significado de cada chave antes de mudar símbolos. Os dicionários são mutáveis e uma cópia superficial ainda compartilha valores internos mutáveis. O índice gerado para EDA depende de `SECOES_EDA`; mudança de ordem ou rótulo pode aparecer em vários pontos. Acessibilidade exige texto junto ao símbolo, sobretudo para leitores de tela.

<!-- editorial:exclude:start -->
Fonte: [README de emojis](../../hub_snippets/constants/emojis/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0080](#doc-0080) · [Próximo: D0082](#doc-0082) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0082"></a>
<a id="doc-0082"></a>
### D0082 — Como formatar números brasileiros sem mudar sua escala?

O README de `format_br` apresenta seis funções que retornam texto: `fmt_int`, `fmt_pct`, `fmt_brl`, `fmt_dec`, `fmt_delta` e `fmt_n`. Elas aplicam convenções brasileiras de separador e símbolo em pontos de apresentação, sem alterar o locale global do processo. O consumidor típico é um notebook ou cartão que já calculou a medida e precisa exibi-la com unidade e precisão legíveis.

Um exemplo válido é `fmt_pct(0.928)`, que mostra `92,8%` quando a entrada representa uma fração. Passar `92.8` como se fosse fração altera a leitura por fator cem; o contrato da métrica deve declarar a escala antes da chamada. Uma variação de taxa em pontos percentuais também deve ser nomeada como tal, pois não é o mesmo que crescimento relativo. `fmt_delta` sinaliza apresentação da diferença, não escolhe a base comparativa.

Na manutenção, conferir casos de zero, negativos, valores faltantes e unidades de cada consumidor. `fmt_int` trunca parte fracionária e sua formatação pode perder precisão para inteiros muito grandes; não usá-lo como transformação para persistência ou validação. Saída formatada é string e não deve voltar à aritmética. Atualizar o README junto das regras de escala evita dashboards visualmente plausíveis com interpretação errada.

<!-- editorial:exclude:start -->
Fonte: [README de format_br](../../hub_snippets/constants/format_br/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0081](#doc-0081) · [Próximo: D0083](#doc-0083) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0083"></a>
<a id="doc-0083"></a>
### D0083 — Quando os estilos seguem o tema escolhido?

`styles` reúne strings CSS `STYLE_*` legadas e a função V04 `get_styles_resolvidos(theme)`. O README distingue conveniência de import de resolução explícita: as strings legadas são montadas quando o módulo carrega; uma troca posterior de cor não as recalcula. A função recebe um `ResolvedTheme` íntegro e devolve um dicionário de estilos para componentes específicos, sem modificar tema global do notebook.

Um uso válido carrega ou resolve o tema, chama `get_styles_resolvidos(theme)` e aplica a entrada correspondente no HTML do cartão. O notebook que continua usando `STYLE_*` recebe o estilo legado; a coexistência permite migração gradual, mas não transforma todas as telas automaticamente. O documento inclui exemplos de CSS e pares de cor, servindo a quem mantém cartões e badges, não a quem calcula indicadores.

Na manutenção, testar os componentes no renderizador efetivo, verificar contraste e pesquisar imports antes de mudar nomes. O par de aviso documentado fica por volta de 3,99:1, abaixo do patamar usual para texto normal; resolver tema não dispensa a checagem. Uma chamada local não autentica a origem do tema nem valida acessibilidade final. O README deve acompanhar a API e suas variantes resolvidas.

<!-- editorial:exclude:start -->
Fonte: [README de styles](../../hub_snippets/constants/styles/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0082](#doc-0082) · [Próximo: D0084](#doc-0084) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0084"></a>
<a id="doc-0084"></a>
### D0084 — Qual componente de exibição responde à pergunta?

O README de `display` é o índice dos snippets de apresentação analítica. Ele encaminha à matriz de correlação, à tabela pandas estilizada e à grade de distribuições. A escolha começa pela pergunta: relações lineares entre colunas numéricas, inspeção de valores tabulares ou forma univariada. Cada objeto tem README próprio com assinatura, dependências, entrada, retorno e limites; o índice orienta navegação, não substitui esses contratos.

Um uso válido para explorar correlações abre `correlation_matrix`, escolhe poucas colunas numéricas e verifica nulos antes de produzir a matriz. Para conferir destaque visual de valores, `dataframe_styled` requer um pandas DataFrame pequeno e retorna HTML. Para ver caudas e assimetria, `distribution_grid` amostra linhas e devolve figura Plotly. A apresentação não cria garantia estatística: uma tabela colorida não valida dado e um histograma amostral não descreve necessariamente toda a população.

Na manutenção, conferir quantidade de linhas e colunas materializadas no driver e as dependências de cada objeto. Alterações em alias ou tema precisam ser testadas no consumidor concreto. Esta página é README de categoria, portanto não deve prometer limites ou comportamento uniforme para os três módulos, nem declarar runtime homologado apenas por listar exemplos.

<!-- editorial:exclude:start -->
Fonte: [README de display](../../hub_snippets/display/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0083](#doc-0083) · [Próximo: D0085](#doc-0085) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0085"></a>
<a id="doc-0085"></a>
### D0085 — O que a matriz de correlação realmente mede?

O README de `correlation_matrix` descreve `plot_correlation` e seu alias para calcular correlações entre colunas numéricas Spark e apresentar um heatmap. O retorno combina a figura e `strong_pairs`, lista de pares acima do limiar escolhido. O consumidor usa essa triagem para formular perguntas adicionais sobre associação; o desenho não identifica causa. As rotas V07 `_resolvido` recebem tema explícito, mas preservam seleção, cálculo e limiar.

Um uso válido seleciona um conjunto pequeno de colunas, confere tipos e nulos, chama a função e lê os pares fortes junto da matriz. O processo remove linhas com nulo ou NaN nas colunas escolhidas; assim, a população efetivamente comparada pode diminuir muito. Um resultado NaN não equivale a correlação zero. A matriz é coletada para compor a figura no driver e cresce quadraticamente com o número de colunas, mesmo se a tabela original for distribuída.

Na manutenção, registrar colunas, amostra efetiva, método e threshold no relatório que acompanha a figura. Testar casos de coluna constante e ausência de pares fortes antes de interpretar vazios. Mudança de paleta exige revisar contraste e legenda, enquanto mudança de seleção ou limpeza altera o significado estatístico. O README é guia de uso do snippet, não atestado de robustez causal ou de execução em todo volume.

<!-- editorial:exclude:start -->
Fonte: [README de correlation_matrix](../../hub_snippets/display/correlation_matrix/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0084](#doc-0084) · [Próximo: D0086](#doc-0086) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0086"></a>
<a id="doc-0086"></a>
### D0086 — O que a tabela estilizada altera?

`dataframe_styled` oferece `display_styled` e `display_styled_resolvido`, com tema notebook explícito, para converter um pandas DataFrame em HTML com formatação e destaque visual. O README descreve parâmetros de colunas e formatos e explicita que o retorno é uma string HTML: a função não muda os valores da tabela original. O destaque de negativos considera valores Python `int` ou `float` nas colunas indicadas, portanto um número convertido em texto pode escapar da regra.

Um exemplo válido usa uma tabela pandas pequena, escolhe explicitamente uma coluna numérica para destaque e confere o HTML no destino antes de publicar. O formato `"{:.1f}%"` acrescenta o símbolo a um valor já em escala percentual; `"{:.1%}"` multiplica uma fração por cem na apresentação. Se a entrada for 0,25, os dois formatos não dizem a mesma coisa. O consumidor deve declarar unidade e escala no cabeçalho, além de verificar dados nulos e tipos.

Na manutenção, testar o renderizador e escapar adequadamente conteúdo externo das células; produzir HTML sem essa conferência pode inserir marcação indesejada. A cor negativa é pista de leitura, não juízo sobre qualidade ou risco. Mudanças em pandas Styler, CSS ou formato devem ser avaliadas com valores limite, negativos e texto. O README não valida a origem dos dados nem substitui cálculo ou autorização de exibição.

<!-- editorial:exclude:start -->
Fonte: [README de dataframe_styled](../../hub_snippets/display/dataframe_styled/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0085](#doc-0085) · [Próximo: D0087](#doc-0087) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0087"></a>
<a id="doc-0087"></a>
### D0087 — Como ler uma grade de distribuições amostradas?

O README de `distribution_grid` apresenta `plot_distributions` e alias para construir histogramas Plotly de colunas escolhidas. A rota usa `smart_sample`, materializa a amostra em pandas e devolve uma `Figure`; a variante V07 temática muda a aparência por tema resolvido explícito. O objetivo é exploração rápida da forma, das caudas e da dispersão, antes de uma análise mais controlada.

Um uso válido informa as colunas e o tamanho pretendido da amostra, observa o N reportado e verifica separadamente faltantes por coluna. O N no rodapé representa linhas coletadas, não a população nem necessariamente observações válidas em cada painel. Uma amostra não estratificada pode omitir categoria rara ou cauda importante. Perto do limite solicitado, a fração pode ser 1 e `limit` selecionar um prefixo, sem inclusão uniforme garantida. O número de bins e as faixas dos eixos também afetam a leitura; comparar painéis exige olhar essas escolhas.

Na manutenção, medir o volume que vai ao driver e declarar semente ou estratégia de amostragem quando a reprodutibilidade for necessária. Testar colunas vazias, constantes e de tipos inesperados. Trocar tema ou cores não altera amostragem, valores nem bins; uma figura mais clara não corrige viés amostral. O snippet ajuda a formular hipóteses, mas o consumidor deve confirmar conclusões com contagens e recortes calculados sobre a base apropriada.

<!-- editorial:exclude:start -->
Fonte: [README de distribution_grid](../../hub_snippets/display/distribution_grid/README.md). Detalhe: [MT06](MT-parte-ii.md#mt06).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0086](#doc-0086) · [Próximo: D0088](#doc-0088) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0088"></a>
<a id="doc-0088"></a>
### D0088 — Onde começa o catálogo de snippets de ML?

O README da pasta `hub_snippets/ml` é a porta de navegação para os guias de aprendizado de máquina. Ele enumera trinta objetos locais e aproxima tarefas que um projeto costuma encadear: preparação, treino, avaliação, explicação, monitoramento e registro de runs. Seu leitor é quem precisa localizar o guia e o contrato de uma peça antes de copiá-la para um notebook. A página é um mapa editorial, sem assinatura executável própria.

Uma busca por previsão temporal, por exemplo, leva ao guia de ARIMA; uma busca por diagnóstico de desvio leva aos documentos de monitoramento. A escolha seguinte exige ler o README do objeto, a implementação e o exemplo consumidor: a presença no índice não certifica que as duas peças compartilhem escala, métrica ou ambiente. Também não significa que os trinta exemplos tenham sido executados juntos.

Na manutenção do catálogo, verificar se links e nomes apontam para arquivos existentes e se cada descrição continua fiel ao código dono. Alterações de API ou pré-requisito devem ser corrigidas no guia específico e refletidas no índice. Nenhuma linha dessa lista concede permissão para backend, aprova modelo ou comprova resultado em Databricks.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/README.md). SHA-256 da fonte histórica da redação: `324c291e0fc2c5b9df3cb3134dba638600a97f82c220848570323823161af2a3`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0087](#doc-0087) · [Próximo: D0089](#doc-0089) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0089"></a>
<a id="doc-0089"></a>
### D0089 — Como ler o guia do invólucro ARIMA?

O README de `arima_wrapper` apresenta `train_arima(series, m=12, forecast_periods=6, seasonal=True, log_mlflow=True)`, que devolve modelo, previsão pontual e métricas. Destina-se ao autor de notebook com série ordenada e frequência conhecida. O parâmetro `m` representa observações por ciclo: doze serve para sazonalidade anual em dados mensais, mas não transforma qualquer série em mensal.

O código chama `auto_arima` em busca `stepwise`, produz horizonte futuro, obtém AIC e BIC do modelo e calcula RMSE e MAPE a partir dos resíduos de ajuste. Um exemplo responsável separa antes uma janela temporal para verificar previsão fora da amostra e desliga `log_mlflow` quando não houver destino de registro autorizado. As métricas devolvidas pelo helper são de ajuste na amostra, não o erro desse teste; zeros ficam fora do MAPE. O intervalo de confiança calculado internamente não integra o retorno.

Na manutenção, confrontar o texto de seleção de ordens com o código: `random_state` e `n_fits=50` não provam cinquenta tentativas aleatórias quando `stepwise=True`. O import de MLflow é obrigatório no módulo mesmo com logging desligado, e o exemplo histórico de instalação não garante versão atual do ambiente.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/arima_wrapper/README.md). SHA-256 da fonte histórica da redação: `a5a02dfd51b610492391b0a1bdd9abef2588d9b3eb8f7acb90aff21f1791c885`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0088](#doc-0088) · [Próximo: D0090](#doc-0090) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0090"></a>
<a id="doc-0090"></a>
### D0090 — Que anomalia o autoencoder sinaliza?

O guia `autoencoder_anomaly` documenta `train_autoencoder_anomaly`, voltado a quem tem matriz numérica de casos normais para treino e matriz da mesma largura para avaliação. O helper centra e escala pela distribuição do treino normal, ajusta um autoencoder PyTorch por erro quadrático de reconstrução e retorna modelo, limiar e erros de teste. O limiar é um percentil dos erros do próprio treino, escolhido pelo parâmetro `threshold_percentile`.

Com duas colunas finitas, `X_train_normal` de transações aceitas e `X_test` de novas transações, o chamador marca casos por `test_errors > threshold`. Esse booleano é sinal de reconstrução incomum perante a base normal, não probabilidade de fraude, taxa futura de casos nem diagnóstico causal. O notebook sintético padroniza externamente e o helper padroniza outra vez; esse detalhe deve acompanhar qualquer reprodução de valores.

Na manutenção, registrar largura, seleção dos normais e versão de pré-processamento junto do limiar. A parada antecipada observa perda de treino, não validação independente; logo, a qualidade da sinalização precisa ser medida fora desse ajuste. MLflow tem import protegido no carregamento do módulo e é exigido quando `log_mlflow=True`; PyTorch é exigido já no import. Para persistência, guarde também centro, escala, arquitetura e ordem das features: `state_dict()` sozinho perde os atributos NumPy de pré-processamento.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/autoencoder_anomaly/README.md). SHA-256 da fonte histórica da redação: `24170a550fe4ec074fa0cbc7096fa516a66cb3b44e6662b3dbd7f41d145dbd3b`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0089](#doc-0089) · [Próximo: D0091](#doc-0091) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0091"></a>
<a id="doc-0091"></a>
### D0091 — O que o perfil de clusters descreve?

O README de `cluster_profiling` serve a quem já possui rótulos de cluster e quer transformar médias de atributos em uma tabela legível. `profile_clusters(df, feature_cols, cluster_col='cluster_id')` devolve uma linha por cluster e variável; `top_differentiators(profiles_df, cluster_id, top_n=5)` ordena as maiores diferenças absolutas padronizadas. O documento é uma etapa descritiva posterior à atribuição dos grupos. O campo `n` se repete por variável; médias ignoram nulos e têm denominadores próprios.

Se grupos de clientes já foram rotulados e `feature_cols` contém renda e frequência, a tabela compara média do grupo, média geral, razão entre ambas e diferença em desvios globais. Quando a média geral é zero, a razão fica indisponível; quando o desvio não é positivo, o `z_score` vira zero. O ranking não prova que a variável causou a formação do grupo, que a diferença é estatisticamente significativa ou que existe uma persona estável.

Na manutenção, preservar a distinção entre rótulo recebido e modelo de clusterização: este módulo não treina nem prevê novos casos. Conferir tipos dos IDs, pois a iteração usa ordenação, e divulgar composição e período da base antes de nomear segmentos.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/cluster_profiling/README.md). SHA-256 da fonte histórica da redação: `3dc79192dff30d3684180f56e5fec6ef371857f277c389e225c6a6a859aa4693`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0090](#doc-0090) · [Próximo: D0092](#doc-0092) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0092"></a>
<a id="doc-0092"></a>
### D0092 — Como escolher e executar a clusterização local?

O guia `clustering_suite` reúne seleção exploratória de quantidade de grupos e ajuste sobre colunas numéricas. `select_k(X_scaled, k_range, method)` retorna pontuações e `best_k`; `run_clustering_pipeline(df, feature_cols, k=3, algorithm="kmeans", scaler="standard", log_mlflow=False)` retorna rótulos, métricas internas, modelo, scaler e matriz transformada; o argumento intermediário `k_range` fica no default nesta chamada por keywords. O leitor deve reter o scaler junto do modelo para repetir a transformação.

Um fluxo concreto escala duas medidas de clientes, compara `k=2..5` por silhouette e só então ajusta K-Means no conjunto escolhido. Em `method='both'`, a decisão é o maior silhouette, não uma votação com cotovelo. O ramo `elbow` usa a segunda diferença quando há pelo menos três candidatos; sua mensagem impressa ainda diz “Melhor silhouette”, mesmo que essa não tenha sido a regra. DBSCAN usa `eps=0.5` e `min_samples=5` fixos; métricas internas desconsideram ruído `-1`, e essa rota não prevê novos casos. GMM automático escolhe `k` por KMeans/silhouette.

Na manutenção, tratar scores como indícios locais, verificar estabilidade e utilidade em dados separados e revisar o pré-processamento antes de atribuir significado aos grupos. MLflow é importado no topo do módulo inclusive com logging desligado; desligar o efeito não elimina essa dependência.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/clustering_suite/README.md). SHA-256 da fonte histórica da redação: `92e8b76cb5c65ed3cc426a5cf4a1b397b33704d54f143839be33b97545d10017`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0091](#doc-0091) · [Próximo: D0093](#doc-0093) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0093"></a>
<a id="doc-0093"></a>
### D0093 — O que as curvas Plotly permitem verificar?

O README de `curves_plotly` apresenta quatro funções de visualização: ROC, precisão-revocação, lift e KS, além das variantes `*_resolvido` com tema. Cada chamada devolve uma `go.Figure` para inspeção ou exportação posterior. O leitor fornece rótulos binários com as duas classes e probabilidades finitas em `[0,1]`; para lift, `n_bins` precisa caber no número de observações.

Com cem rótulos e cem scores alinhados, `plot_roc_curve` mostra discriminação e AUC; `plot_pr_curve` situa precisão e recall diante da prevalência. `plot_lift_curve` ordena o topo por score; seu primeiro corte usa `ceil(N/n_bins)` linhas, portanto a cobertura real pode exceder a nominal, e `plot_ks_curve` mostra a maior separação `max(tpr-fpr)` como fração. O argumento `n` altera o rodapé mostrado, sem selecionar amostra. Essa unidade de KS não deve ser confundida diretamente com `metrics_report.ks_pct`, cujo cálculo é bilateral e multiplicado por cem.

Na manutenção, validar dados, unidade e contexto antes de publicar uma figura. O tema V07 muda apresentação, não a estatística. Nenhuma das curvas escolhe limiar operacional, demonstra calibração ou homologa por si só uma exportação PNG, PDF ou PPTX.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/curves_plotly/README.md). SHA-256 da fonte histórica da redação: `bfd64914f1375c0a0fc3fdd8cb220bcdfabcdae57728230c86b0c7ef7438770d`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0092](#doc-0092) · [Próximo: D0094](#doc-0094) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0094"></a>
<a id="doc-0094"></a>
### D0094 — Qual mudança de distribuição foi medida?

O README de `drift_detection` orienta quem compara uma população de referência com outra atual em memória pandas. Sua razão de existir é separar medida de mudança de decisão sobre o modelo: PSI e KS para números, CSI para categorias e uma varredura por feature podem apontar onde investigar, mas não demonstram queda de performance. O documento explica bins definidos pela referência, categoria ausente, escolha de tipos e política opcional de alerta.

O leitor deve saber que os dados ficam no driver, exigindo amostra ou agregado controlado quando a origem é Spark. `detect_drift_all_features` reúne índices e status; sem os limiares requeridos, retorna `NOT_CLASSIFIED`, e dados insuficientes têm estado próprio. Na varredura, o CSI categórico ocupa o campo `psi` por compatibilidade de schema: a ficha chama atenção para essa diferença sem fingir que a categoria recebeu PSI numérico. A manutenção deve acompanhar retornos de `calculate_psi`, `calculate_ks`, `calculate_csi` e thresholds com a implementação. Um alerta pede checar população, captura, sazonalidade e resultado do modelo; não ordena retreino nem estabelece causa.

<!-- editorial:exclude:start -->
Fonte: [README de drift_detection](../../hub_snippets/ml/drift_detection/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0093](#doc-0093) · [Próximo: D0095](#doc-0095) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0095"></a>
<a id="doc-0095"></a>
### D0095 — O que compõe o relatório de explicabilidade?

O guia `explainability_report` descreve dois formatadores de texto. `generate_executive_report` recebe importâncias SHAP já calculadas, nomes de negócio, alvo e métrica; `generate_technical_summary` recebe a tabela de importâncias e, opcionalmente, outra importância nativa. Ambos retornam strings Markdown. São consumidores de resultados fornecidos pelo analista, não motores de SHAP nem gravadores de arquivos.

Se a tabela contém importância de renda, frequência e idade, o relatório executivo usa as cinco primeiras linhas na ordem recebida; ordene explicitamente antes da chamada se “principais” significar maior impacto. Os rótulos de impacto acima de 15% e 8%, e a direção indicada pela correlação entre valor e SHAP, são heurísticas locais. Correlação zero cai no ramo textual negativo, sem provar relação inversa ou causalidade. O resumo técnico usa `to_markdown`, que requer `tabulate`; a comparação nativa precisa de colunas `rank` em ambas as tabelas após a junção.

Na manutenção, guardar origem, escala e versão dos valores SHAP e conferir a forma exata das tabelas. Os cortes de Spearman 0,7 e 0,5 organizam a narrativa local, sem virar padrão de aprovação de modelo.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/explainability_report/README.md). SHA-256 da fonte histórica da redação: `8569d6586c27bc3a471da0d7962620d87d4fdce03e5cfae875fed00e5b5abada`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0094](#doc-0094) · [Próximo: D0096](#doc-0096) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0096"></a>
<a id="doc-0096"></a>
### D0096 — Que evidência o Isolation Forest produz?

O guia `isolation_forest` apresenta `train_isolation_forest` para uma base numérica e colunas escolhidas. O retorno inclui scores, rótulos, modelo, estatísticas e scaler. `profile_anomalies` transforma casos sinalizados em tabela de inspeção, embora o notebook exemplo apenas importe essa função e execute o treino. O leitor precisa distinguir score contínuo, rótulo do estimador e resumo de perfil.

Para transações com valor e frequência finitos, `contamination=0.01` orienta o estimador e permite calcular uma estatística de referência: score mais negativo indica maior anomalia. O rótulo `-1` vem de `predict`, pelo corte interno de decisão; `stats.score_threshold` é um percentil local e não necessariamente esse mesmo corte. O perfil escolhe scores menores entre os marcados e aponta variável mais discrepante por z-score global, não por explicação da árvore. Uma atribuição intermediária com `nlargest` é sobrescrita antes do retorno.

Na manutenção, registrar base, escala, contaminação e regra de investigação humana. Nesta implementação, `contamination='auto'` falha no cálculo posterior que multiplica o valor; use número em `(0,0.5]`. MLflow é importado no módulo mesmo com logging desligado. Score anômalo, isoladamente, não comprova fraude.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/isolation_forest/README.md). SHA-256 da fonte histórica da redação: `3713e43687c4f4833839dea78c55da6cb746b53a1ffccc5dd9ad8488c112e011`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0095](#doc-0095) · [Próximo: D0097](#doc-0097) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0097"></a>
<a id="doc-0097"></a>
### D0097 — Como ler uma curva com observações censuradas?

O README de `kaplan_meier` explica um problema que a contagem simples de eventos não resolve: algumas pessoas ou contratos ainda não tiveram tempo suficiente para apresentar o evento. Uma observação censurada contribui para a curva até o fim conhecido de acompanhamento, sem virar “não evento definitivo”. O documento orienta o leitor a fornecer duração, indicador de evento e, se necessário, grupo; `plot_kaplan_meier` produz figura Plotly e `log_rank_test` compara curvas.

Essa ficha é útil a quem estuda churn, inadimplência ou tempo até uma ação. O guia distingue resultado de dois grupos do formato global e pares com correção de Holm quando há mais grupos. Ele também aponta dependência de `lifelines`; o notebook de exemplo instala pacote e reinicia Python, efeitos do exemplo que não pertencem à chamada do helper. Na manutenção, conferir forma dos retornos, legenda, medianas e tratamento de grupos nulos com o código. Censura relacionada ao risco, entrada tardia ou grupos com composição diferente limitam a interpretação; p-valor do log-rank não mede tamanho de efeito nem prova causalidade.

<!-- editorial:exclude:start -->
Fonte: [README de kaplan_meier](../../hub_snippets/ml/kaplan_meier/README.md). Detalhe: [MT08](MT-parte-ii.md#mt08).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0096](#doc-0096) · [Próximo: D0098](#doc-0098) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0098"></a>
<a id="doc-0098"></a>
### D0098 — Como o guia de ranking interpreta grupos?

O README de `lgbm_ranker` documenta `train_lgbm_ranker` e `evaluate_ranking` para ordenar candidatos dentro de consultas ou outros grupos. O consumidor passa matrizes, relevâncias não negativas e vetores `groups_train` e `groups_val` cujos inteiros são tamanhos de blocos contíguos. Eles não são IDs de consulta: a soma precisa igualar o número de linhas e a ordem física deve reunir cada grupo antes da chamada.

Num exemplo com dois grupos de três candidatos, `groups_train=[3,3]` faz o treinamento e a avaliação calcular NDCG@5, @10 e @20, como média por grupo. Passar `[1,1,2,2,3,3]` por imaginar identificadores viola a interface. A função valida soma, positividade e relevância não negativa, mas não reorganiza linhas nem garante compatibilidade dos graus de relevância com `label_gain` do LightGBM. Parâmetros fornecidos substituem o conjunto de defaults, e o import de MLflow é necessário mesmo com registro desligado.

Na manutenção, corrigir a promessa da docstring de `evaluate_ranking`: ela menciona MAP, mas o código só retorna NDCG. Registrar grupos, cortes e ordenação: o avaliador fixa ganho `2**relevancia-1`, que pode divergir de `label_gain` personalizado. Score de ranking não é probabilidade calibrada.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/lgbm_ranker/README.md). SHA-256 da fonte histórica da redação: `6d59304ec5ed824f24cdb623159188fa73177a17057086a4324dbd4231dbcf2b`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0097](#doc-0097) · [Próximo: D0099](#doc-0099) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0099"></a>
<a id="doc-0099"></a>
### D0099 — O que há de temporal no helper LightGBM?

Apesar do nome `lgbm_temporal`, este README descreve um gerador pandas de atributos, não o treino de LightGBM. `create_temporal_features(df, target_col, date_col, lags, rolling_windows, calendar_features, entity_cols, date_format, on_duplicate_dates)` devolve cópia ordenada com defasagens, médias móveis, campos de calendário e tendência. O consumidor pode agrupar por entidade para impedir mistura de históricos.

Para vendas mensais por loja, ordenar por loja e data, criar `lag_1` e janela móvel de três observações faz a linha atual usar apenas valores anteriores no cálculo do rolling, pois há `shift(1)`. Um lag representa uma observação anterior, não necessariamente um mês: meses ausentes não são preenchidos. Datas em formato ano-mês-dia são aceitas; outros textos exigem `date_format`. Datas duplicadas na mesma entidade geram erro por padrão, e `on_duplicate_dates='keep'` conserva a ordem original.

Na manutenção, documentar unidade temporal, chaves, tratamento de duplicatas e disponibilidade real do alvo. O helper remove linhas com nulos nas features de lag/rolling geradas, inclusive propagados de ausências internas do alvo; não limpa nulos em outras colunas nem prova disponibilidade externa na predição. O nome histórico não autoriza descrever um modelo treinado.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/lgbm_temporal/README.md). SHA-256 da fonte histórica da redação: `c4c43776e44afcfb326a4d70c8065cdbe20fcc30fa1a7da074b63feb21474161`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0098](#doc-0098) · [Próximo: D0100](#doc-0100) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0100"></a>
<a id="doc-0100"></a>
### D0100 — Como interpretar o relatório de métricas?

O guia `metrics_report` apresenta `calculate_binary_metrics(y_true, y_prob, threshold=.5)` e `calculate_regression_metrics(y_true, y_pred)`. Cada função devolve um dicionário arredondado, adequado a relatório local, com vetores unidimensionais alinhados. A primeira exige as duas classes 0/1 e probabilidades finitas entre zero e um; a segunda exige valores finitos de alvo e previsão.

Um notebook pode comparar, na mesma base sintética, precisão e recall em limiares de 0,3 e 0,5 sem chamar esse contraste de escolha operacional definitiva. `ks_pct` mede KS bilateral entre distribuições de score de positivos e negativos, multiplicado por cem; a figura de `curves_plotly` usa outra direção e escala. A chave `auc_roc` precisa de tradução antes de alimentar o monitor, que espera `auc`. `auc_pr` representa Average Precision, não integração trapezoidal genérica. Para regressão, MAPE exclui alvos zero e retorna NaN quando todos são zero, incompatível com monitor que exige métricas finitas; o lift top10 binário usa o teto de 10% do tamanho da amostra.

Na manutenção, registrar amostra, limiar, unidade e significado de cada chave. A docstring histórica menciona `format_metrics_table`, ausente da implementação e da fachada pública; tratá-la como função disponível produziria erro de importação.

<!-- editorial:exclude:start -->
Fonte: [README.md](../../hub_snippets/ml/metrics_report/README.md). SHA-256 da fonte: `37e9b5018ca99b449127d71d953bf9650a8dcd9583ab0b85089cc3c5f10b3965`.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0099](#doc-0099) · [Próximo: D0101](MT-atlas-03.md#doc-0101) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
