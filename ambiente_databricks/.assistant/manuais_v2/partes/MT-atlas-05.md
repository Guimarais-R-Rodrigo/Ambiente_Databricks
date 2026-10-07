# MT atlas 05

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0201"></a>
<a id="doc-0201"></a>
### D0201 — Análise técnica SHAP

Este template organiza evidência técnica de SHAP, método que distribui contribuições das variáveis em relação à saída-base do modelo. Seu consumidor é o analista que precisa sustentar uma explicação global e local. O cabeçalho solicita modelo, run quando existente, conjunto explicado, tamanho, método, escala, background, valor-base e tempo de cálculo. As seções pedem, conforme método e perfil, distribuição das contribuições, média do valor absoluto, dependências, casos de alta e baixa previsão, interações, coortes e checagens de consistência. Guardar esses vínculos impede que um gráfico seja separado da versão ou população que o produziu.

Num classificador binário, escolha explicitamente a classe e a escala antes de ler um gráfico local: valores em log-odds, logaritmo da razão entre probabilidades do evento e do não evento, não são pontos de probabilidade. Compare o ranking SHAP com importância nativa como diagnóstico, não como obrigação de concordância. Correlação de Spearman entre rankings, *bootstrap* (reamostragem) para estabilidade e erro de aditividade exigem cálculo e tolerância adequados ao método. Artefatos são condicionais e critérios dependem do contrato; limites fechados do verificador não são recalibrados no relatório. `LINEAR_REGRESSION_SYNTHETIC_V1` verifica contribuições brutas, sem produzir automaticamente plots, interações ou logging. O template documenta a análise; não calcula SHAP, não valida causalidade e não substitui a verificação de desempenho do modelo.

<!-- editorial:exclude:start -->
Fonte: [shap_analysis_technical.md](../../skills/hub-ml-explainability/templates/shap_analysis_technical.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0200](MT-atlas-04.md#doc-0200) · [Próximo: D0202](#doc-0202) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0202"></a>
<a id="doc-0202"></a>
### D0202 — Skill de engenharia de atributos

A skill de *feature engineering* projeta variáveis para treino e inferência, consumida por quem prepara um conjunto modelável ou uma tabela de atributos. Antes de propor cálculo, fixa entidade, chave, alvo, horizonte, instante de decisão, corte, janela, frequência e latência. A regra temporal central é disponibilizar a informação no instante da decisão, incluindo atraso de publicação; um join *point-in-time* seleciona a versão histórica adequada, sem trazer o futuro. As specs ligam fórmula, fonte, granularidade, disponibilidade, responsável e testes.

Por exemplo, “compras nos 30 dias anteriores” deve filtrar por cliente e por instante de referência, excluir eventos posteriores e produzir uma linha por decisão. Imputação, codificação e seleção ajustadas com o alvo ficam apenas no treino; a inferência deve reproduzir o mesmo tratamento para evitar diferença entre treino e produção. A skill recomenda Spark e tabelas governadas quando houver escala, mas materializar exige contrato e autorização próprios. Na policy vigente está em L0, orientação textual, com L4 como alvo para proteção temporal e materialização: lag sintético, vista temporal composta e materialização Delta autorizada têm rotas separadas. A presença desses executores não promove o nível. Sem tempo, fonte e disponibilidade confirmados, o plano permanece exploratório e não demonstra ausência de vazamento.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-feature-engineering/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0201](#doc-0201) · [Próximo: D0203](#doc-0203) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0203"></a>
<a id="doc-0203"></a>
### D0203 — Checklist de validação de atributos

O checklist ajuda o revisor de engenharia de atributos a conferir o plano antes de chamá-lo completo. Ele organiza contexto e alvo, prevenção de vazamento de informação futura (*leakage*), granularidade de joins, codificação de categorias, nulos, estabilidade e implementação. O mecanismo é registrar aplicabilidade e cada item como resolvido, pendente ou NÃO EXECUTADO com justificativa; a seção final conta itens, pendências críticas e decisões necessárias. Essa forma torna visível uma lacuna que seria perdida em um relato genérico de “features validadas”.

Imagine uma média de compras usada para prever abandono. É preciso demonstrar disponibilidade até a decisão, respeitando fronteira LT/LE do contrato, que o join não multiplica clientes e que a transformação de categorias foi ajustada só no treino. WoE, peso da evidência para categorias em alvo binário, e PSI, índice de estabilidade populacional entre distribuições, só entram quando pertinentes e com referência definida. Correlação, cardinalidade e nulos exigem critérios do estudo; o arquivo não impõe corte universal, exclusão automática ou pré-agregação em todo join. Uma caixa marcada sem contagem, distribuição, código ou evidência verificável não prova aceite; um item ainda aberto deve permanecer pendente ou receber decisão explícita.

<!-- editorial:exclude:start -->
Fonte: [checklist_validacao_features.md](../../skills/hub-ml-feature-engineering/templates/checklist_validacao_features.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0202](#doc-0202) · [Próximo: D0204](#doc-0204) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0204"></a>
<a id="doc-0204"></a>
### D0204 — Backlog de atributos por prioridade

O backlog organiza atributos candidatos em tiers A, B e C para sequenciar investigação e implementação. Seu consumidor é a equipe que compara sinal esperado, risco de vazamento de informação futura, custo, dependências e estado de cada proposta. Cada linha mantém o `feature_name` da especificação, motivo de negócio, risco consolidado, fontes dependentes e marcador pendente, em curso, implementado ou bloqueado. Tier A é candidata ao primeiro ciclo, com valor justificado e risco/custo compatíveis. B exige resolver dependências ou incertezas. C requer experimento delimitado, orçamento e critério de parada; nenhum tier autoriza execução.

Por exemplo, a contagem de acessos nos 30 dias anteriores pode ser candidata a A com valor esperado justificado, disponibilidade temporal confirmada e risco/custo compatíveis com os critérios aprovados para o estudo. Se os eventos forem publicados após a previsão, essa classificação deixa de valer, apesar da fórmula simples. Uma razão saldo/renda entre duas fontes pode exigir join histórico e cobertura suficiente, elevando risco e custo. Os exemplos bancários de saldo, comportamento e WoE (peso da evidência para categorias) são ilustrativos; seus rótulos não avaliam a carteira do leitor. “Sinal esperado” é hipótese, não ganho incremental observado. Reclassifique após medir cobertura, custo, estabilidade e validação fora do tempo; dependência ausente deve bloquear ou adiar a proposta.

<!-- editorial:exclude:start -->
Fonte: [feature_backlog_tiers.md](../../skills/hub-ml-feature-engineering/templates/feature_backlog_tiers.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0203](#doc-0203) · [Próximo: D0205](#doc-0205) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0205"></a>
<a id="doc-0205"></a>
### D0205 — Especificação central de atributos

A Feature Spec Core é a tabela compacta que define cada atributo proposto antes da implementação. Seu consumidor é quem transforma uma ideia de variável em cálculo reproduzível. Cada linha registra `feature_name`, definição, tipo, granularidade, janela e origem; o nome em `snake_case` com prefixo `feat_` serve de chave para o documento complementar de risco. Granularidade significa a unidade representada pela linha e deve corresponder à unidade de decisão, evitando que uma contagem de transações seja interpretada como valor por cliente.

Considere `feat_qtd_compras_30d`: a linha deve dizer que conta compras por cliente nos 30 dias anteriores e identificar coluna e tabela de transações. A tabela compacta não basta: vincule por `feature_name` o registro temporal com `event_time`, `available_at`, `cutoff`, fronteiras e desempate. Nulos e testes completam o contexto e a spec de risco. O exemplo de razão entre saldo e limite pede atenção a denominador zero e versão temporal de cada fonte. Tipos como `cat_woe` indicam WoE, peso da evidência para categorias em alvo binário, mas não autorizam ajuste fora do treino. As linhas preenchidas no template são exemplos, não features aprovadas ou dados verificados.

<!-- editorial:exclude:start -->
Fonte: [feature_spec_core.md](../../skills/hub-ml-feature-engineering/templates/feature_spec_core.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0204](#doc-0204) · [Próximo: D0206](#doc-0206) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0206"></a>
<a id="doc-0206"></a>
### D0206 — Especificação de risco e validação de atributos

Esta tabela complementa a Feature Spec Core pelo mesmo `feature_name`, ligando cada atributo a risco de vazamento de informação futura (*leakage*), custo, checagem objetiva, direção esperada do sinal e observações. O consumidor é o revisor que precisa decidir se a definição é testável e se uma dependência torna a proposta inviável. O mecanismo separa forma do atributo de seu risco: uma fórmula simples pode depender de uma fonte tardia ou de uma janela que invade o período do alvo.

Por exemplo, para razão de uso do limite, a validação deve examinar denominador zero, faixas plausíveis e data efetiva do limite; “entre zero e um” pode falhar legitimamente se houver utilização acima do limite. Para recência, dias negativos sinalizam referência ou evento incoerente. A seta de “mais compras, menos abandono” é hipótese sobre o alvo, não direção comprovada. No exemplo WoE, peso da evidência de categorias, o ajuste pertence ao treino e exige convenção de classes; PSI, índice de estabilidade populacional, depende de referência e limite aprovados. Custos BAIXO/MÉDIO/ALTO exigem contexto; risco ausente fica NÃO AVALIADO. O arquivo recusa teto monetário ou cap em percentil automático, exigindo regra e autoridade fundamentadas.

<!-- editorial:exclude:start -->
Fonte: [feature_spec_risco_validacao.md](../../skills/hub-ml-feature-engineering/templates/feature_spec_risco_validacao.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0205](#doc-0205) · [Próximo: D0207](#doc-0207) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0207"></a>
<a id="doc-0207"></a>
### D0207 — Taxonomia de atributos entre fontes

Esta taxonomia recebe candidatas de Cross-EDA verificado ou de fontes com contratos estabelecidos para uma unidade de decisão. Seu consumidor é quem propõe atributos que uma fonte isolada não poderia produzir: razões entre medidas, diferenças, indicadores de presença e combinações temporais. O template registra numerador, denominador, fontes e janela para impedir que um nome sugestivo esconda um join errado. Antes de construir, confirme chave, cardinalidade, cobertura e disponibilidade de ambas as fontes no instante da decisão.

Por exemplo, saldo dividido por renda exige saldo e renda históricos compatíveis, denominador válido e regra explícita para ausência de cadastro. Um indicador “há registro no bureau” pode ser útil, mas a falta de registro também pode refletir cobertura desigual ou informação posterior ao alvo. A checklist anti-*leakage*, vazamento de informação futura, pergunta se alguma fonte contém resultado do evento, se o join multiplica linhas e se a ausência funciona como proxy indevido. Cobertura abaixo de 50% não é veto universal nem taxa geral de nulos. PSI, índice de estabilidade populacional, pede investigação com referência e limite aprovados; sozinho não prova diferença de medição ou ganho preditivo. Sem compatibilidade temporal, a proposta deve ficar bloqueada ou exploratória.

<!-- editorial:exclude:start -->
Fonte: [feature_taxonomy_cross_source.md](../../skills/hub-ml-feature-engineering/templates/feature_taxonomy_cross_source.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0206](#doc-0206) · [Próximo: D0208](#doc-0208) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0208"></a>
<a id="doc-0208"></a>
### D0208 — Mapa dos notebooks-alvo

O mapa é o inventário do corpus de notebooks antes de propor atributos. Seu consumidor é quem precisa localizar a origem de regras, agregações e variáveis finais. Para cada arquivo, registra nome, papel — extração, transformação e carga (ETL), análise exploratória de dados (EDA), regras, modelagem ou agregação —, entradas, saídas, granularidade e observações. A distinção entre ler e escrever uma tabela, produzir uma variável temporária e apenas mostrar um gráfico evita atribuir efeito ao notebook errado.

Num corpus hipotético, um notebook de carteira pode ler clientes e saldos, filtrar ativos e produzir uma linha por cliente; outro pode apenas explorar essa saída, sem gravar tabela. Ao mapear cada um, anote janelas, chaves, filtros, dependências e alertas de qualidade que afetam a futura feature. Um nome de arquivo não prova execução nem ordem real do pipeline: confira código e efeitos observáveis. O exemplo bancário do template, inclusive percentuais de nulos, é ilustração preenchida, não achado deste projeto. O mapa prepara a especificação e a análise temporal; sozinho não autoriza join, materialização ou afirmação de ausência de vazamento de informação futura.

<!-- editorial:exclude:start -->
Fonte: [mapa_notebooks_alvo.md](../../skills/hub-ml-feature-engineering/templates/mapa_notebooks_alvo.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0207](#doc-0207) · [Próximo: D0209](#doc-0209) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0209"></a>
<a id="doc-0209"></a>
### D0209 — Estrutura do notebook de plano de atributos

Este template organiza o notebook de saída de engenharia de atributos em células que tornam o plano revisável. Seu consumidor é quem analisa um corpus de notebooks e precisa passar de contexto de modelagem a inventário, fluxo de dados, evidências, taxonomia, especificações, backlog e validação. Há modos condensado, padrão e expandido: o tamanho deve acompanhar risco e número de fontes, sem encher um notebook pequeno de células vazias. `PENDENTE/DECISAO` preserva incerteza sobre alvo ou horizonte em vez de inventá-los.

Por exemplo, antes de propor compras nos 30 dias anteriores, o autor registra unidade de decisão e data de referência, mapeia o notebook que lê transações e identifica se a agregação ocorre antes do join. A especificação central define fórmula e origem; a de risco pede teste de janela e cardinalidade; o backlog prioriza a hipótese. A célula de código de validação é opcional e aparece comentada: sua presença não prova que schema ou nulos foram medidos. Os exemplos de WoE, peso da evidência para categorias, e PSI, índice de estabilidade populacional, não autorizam cortes universais. O template é plano adaptável, não notebook executado nem feature materializada.

<!-- editorial:exclude:start -->
Fonte: [notebook_output_structure.md](../../skills/hub-ml-feature-engineering/templates/notebook_output_structure.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0208](#doc-0208) · [Próximo: D0210](#doc-0210) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0210"></a>
<a id="doc-0210"></a>
### D0210 — Skill de monitoramento de modelo

A skill organiza o acompanhamento de um modelo em produção ou prestes a entrar nele. Seu consumidor é a equipe que precisa distinguir saúde do serviço, qualidade e volume de dados, mudança de distribuição (*drift*), performance com rótulos disponíveis, segmentos e impacto de negócio. O contrato inicial registra versão ou alias do modelo, população, janela, referência, responsáveis, frequência e atraso dos rótulos. Sem esse atraso, uma queda aparente de performance pode ser apenas ausência temporária de eventos conhecidos.

Por exemplo, uma alteração no perfil dos scores pede comparar distribuições com bins fixados na referência e volume declarado; PSI, índice de estabilidade populacional, é sinal diagnóstico, não prova de erro do modelo. AUC, área sob curva que compara sensibilidade e falsos positivos, só pode ser comparada quando os rótulos amadurecerem na mesma definição de população. A resposta pode ser observar, investigar dados, recalibrar, treinar um desafiante ou propor reversão; promoção e mudança de alias exigem validação e autorização próprias. Na policy vigente, esta skill está em L0, orientação textual, com L4 apenas como alvo em rollout audit. As rotas sintéticas de drift e performance madura têm contratos distintos; a segunda exige finalização e reverificação. Não criam monitor automático nem autorizam retreino.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-monitoramento-modelo/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0209](#doc-0209) · [Próximo: D0211](#doc-0211) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0211"></a>
<a id="doc-0211"></a>
### D0211 — Relatório periódico de mudança de distribuição

O template de *drift*, mudança de distribuição, organiza uma leitura periódica do score e das variáveis de um modelo. Seu consumidor é quem documenta referência, janela atual, volume, métricas por feature, estado e recomendação. PSI, índice de estabilidade populacional, compara proporções em faixas fixas; KS pode indicar distância entre distribuições, mas seu significado depende da forma de cálculo usada. A tabela de performance é condicional: só deve ser preenchida quando rótulos maduros permitem comparar a população atual com a referência.

Imagine que o PSI do score aumenta numa semana com poucos casos. Antes de marcar alerta, confira tamanho da amostra, composição por segmento, categorias ausentes ou novas e variabilidade histórica. Se também houver AUC, área sob curva de discriminação por sensibilidade e falsos positivos, calcule a diferença com direção e janela corretas; uma coluna de delta vazia não significa degradação. Os valores `[X]`, semáforos e ações do arquivo são placeholders, não observações. O template não escolhe limiar universal nem decide retreino: ele registra evidência para investigação, com referência e regra aprovadas pelo caso.

<!-- editorial:exclude:start -->
Fonte: [drift_report.md](../../skills/hub-ml-monitoramento-modelo/templates/drift_report.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0210](#doc-0210) · [Próximo: D0212](#doc-0212) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0212"></a>
<a id="doc-0212"></a>
### D0212 — Registro da decisão de retreino

Este template prepara uma recomendação técnica para a decisão operacional sobre um modelo já monitorado. Registra separadamente responsável, aprovação, execução autorizada e execução observada. Seu consumidor é o responsável por justificar manter, investigar ou treinar um desafiante (*challenger*) frente ao modelo vigente. A tabela pede PSI do score — índice de estabilidade populacional —, mudança de AUC, área sob curva que compara sensibilidade e falsos positivos, número de variáveis em alerta e persistência por janelas. Cada valor precisa de referência, população, volume, rótulos amadurecidos e limiar aprovado; o semáforo sozinho não constitui decisão.

Por exemplo, uma mudança acentuada de distribuição (*drift*) em uma semana pode decorrer de alteração de ingestão: investigar fonte e pipeline antes de usar dados novos para treino. Uma queda de AUC em poucas observações pede incerteza e confirmação em janelas seguintes. Se a opção for treinar, registre período, estratégia e validação fora do tempo do challenger. Isso ainda não promove o novo modelo nem troca alias de produção; a comparação com o vigente e o gate de governança vêm depois. O documento contém campos `[X]` e alternativas para preencher, não medições nem autorização prévia. Retreinar por um único número ou por threshold copiado do template seria extrapolação.

<!-- editorial:exclude:start -->
Fonte: [retreino_decision.md](../../skills/hub-ml-monitoramento-modelo/templates/retreino_decision.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0211](#doc-0211) · [Próximo: D0213](#doc-0213) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0213"></a>
<a id="doc-0213"></a>
### D0213 — Skill de construção de pipelines

A skill orienta infraestrutura de dados e aprendizado de máquina que roda por agenda ou evento. Seu consumidor é quem precisa escolher processamento em lote ou fluxo, contratos de tabelas, qualidade, reprocessamento e implantação por ambiente. A escolha parte de origem, volume, latência, frequência, cloud, permissões e objetivo; camadas bronze, silver e gold só ajudam quando estabelecem fronteiras úteis. A fonte recomenda Lakeflow Spark Declarative Pipelines para fluxos declarativos, Lakeflow Jobs para orquestração e Declarative Automation Bundles para configuração versionada, sempre condicionados à capacidade do ambiente.

Num fluxo de transações, bronze preserva chegada, silver deduplica por chave e tempo, e gold publica grão de consumo definido. Registre *checkpoint* durável — estado e progresso persistidos para retomada —, atraso de chegada, regra de replay (reprocessamento), expectativas de qualidade e ação ao falhar. Idempotência é repetir sem duplicar efeitos; não significa sobrescrever tudo. Esse registro permite retomar ou repetir a janela sem perder a origem do resultado. Um helper de inspeção pode diagnosticar nulos, mas não substitui expectativa monitorada pelo pipeline. Deploy, escrita e execução em ambiente alvo exigem validação, permissões e autorização. A policy mantém L0/audit, com L4 como alvo. Preflight, Spark local e probe Delta autorizado têm contratos separados; esses perfis não comprovam deploy nem promovem a skill.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-pipeline-builder/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0212](#doc-0212) · [Próximo: D0214](#doc-0214) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0214"></a>
<a id="doc-0214"></a>
### D0214 — Especificação editável de pipeline

O template de especificação dá uma visão compacta de um pipeline de dados ou aprendizado de máquina antes da implantação. Seu consumidor coordena datasets, etapas, dependências de dados e compute, qualidade e operação pertinentes. Modelo e scoring são condicionais. O quadro de schedule, quando solicitado, distingue frequência e SLA — meta de nível de serviço — pretendidos da configuração efetivamente observada. Expectations são regras de qualidade com condição, limiar e ação planejada, cuja sintaxe e efeitos precisam ser confirmados na plataforma concreta.

Por exemplo, uma tabela silver pode exigir chave não nula e deduplicação antes de alimentar scoring. O autor registra se a violação deve ser observada, descartada com evidência ou bloquear a etapa, e quem investiga o evento. Preencher “SLA 30 minutos” documenta uma meta, não prova latência medida; marcar uma caixa verde não demonstra que job, alerta ou tabela existem. Modelo, URI e catálogo, quando aplicáveis, precisam ser confirmados. Preflight preserva `effects_authorized=false` e `deployment_status=NOT_RUN` quando retornados; UNKNOWN exige inspeção somente leitura, sem repetir efeitos. O template não cria pipeline, não configura schedule, não escreve tabelas e não autoriza deploy; serve para revisar dependências e lacunas antes desses efeitos.

<!-- editorial:exclude:start -->
Fonte: [pipeline_spec.md](../../skills/hub-ml-pipeline-builder/templates/pipeline_spec.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0213](#doc-0213) · [Próximo: D0215](#doc-0215) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0215"></a>
<a id="doc-0215"></a>
### D0215 — Skill de tutoria Databricks

A skill responde no chat a pedidos de explicação de código, notebook, erro ou conceito. Seu consumidor é quem quer entender o fluxo de dados e os efeitos de uma operação, sem pedir edição do artefato. O método começa pela finalidade e nível de detalhe adequado, situa entradas e saídas, agrupa operações lógicas e distingue transformação Spark avaliada sob demanda de ação que realmente executa. Em um erro, procura a exceção raiz, propõe o menor diagnóstico seguro e define critério para verificar a correção.

Por exemplo, ao explicar `groupBy(...).count()`, mostre o grão antes e depois da agregação, o possível embaralhamento de dados entre partições (*shuffle*) e onde uma ação materializa o plano. Uma analogia bancária pode ajudar após a definição técnica, mas não descreve literalmente a execução distribuída. A existência de uma célula ou de uma saída antiga não prova que o notebook rodou agora. Versão, cloud e compute condicionam APIs, interfaces de programação; confirme quando importarem. Na policy vigente, o tutor está em L0/guidance, orientação textual sem runner obrigatório. Seu destino é a resposta didática; escrever documentação dentro do notebook pertence a outra skill.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-tutor-databricks/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0214](#doc-0214) · [Próximo: D0216](#doc-0216) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0216"></a>
<a id="doc-0216"></a>
### D0216 — Banco de analogias de dados e negócio

O template reúne analogias de banking, gestão de relacionamento com clientes (CRM) e finanças para explicar conceitos de Spark, Delta, MLflow, Unity Catalog e análise. Seu consumidor é o tutor que já apresentou a definição técnica e deseja dar uma imagem familiar: *shuffle* é redistribuição de dados entre partições, como redistribuir carteiras entre gerentes; uma ação Spark aciona o processamento de um plano antes adiado. O paralelo ajuda a recordar custo e sequência, mas não determina algoritmo, tempo ou resultado.

Por exemplo, “time travel é fotografia do cadastro antigo” ajuda a pensar em versões de tabela, mas não promete retenção ilimitada nem restauração de qualquer dado. “Drift é termômetro de perfil” não demonstra perda de desempenho nem ordena retreino. As comparações de catálogo com diretoria e schema com departamento também não substituem permissões e nomes reais. O arquivo orienta escolher uma analogia curta, rotulá-la e dizer onde deixa de funcionar. Se a ressalva ficar maior que a imagem, explique diretamente. Acrescentar nova analogia exige conceito específico e correspondência útil, não uma metáfora genérica aplicável a qualquer tecnologia.

<!-- editorial:exclude:start -->
Fonte: [analogias_banking_crm.md](../../skills/hub-ml-tutor-databricks/templates/analogias_banking_crm.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0215](#doc-0215) · [Próximo: D0217](#doc-0217) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0217"></a>
<a id="doc-0217"></a>
### D0217 — Estrutura para explicar um bloco de código

Este template transforma a leitura de um trecho em explicação didática verificável. Seu consumidor é quem responde a alguém que quer entender o código, não receber uma reescrita automática. A sequência pede visão geral, lugar no pipeline, entradas, saídas, efeitos colaterais, explicação conceitual e técnica, linhas críticas, analogia opcional, exemplo mínimo, riscos e checagens. Preencher “DataFrame de saída” exige conferir o grão e o schema; descrever escrita prevista exige localizar a operação; afirmar “tabela escrita” exige também evidência de execução, não o nome da variável.

Imagine um bloco que lê eventos e agrupa por cliente. A explicação deve dizer quais eventos entram, qual janela é usada, se há filtragem de dados posteriores à decisão e se `groupBy` implica redistribuição de dados entre partições. Em Spark, `groupBy(...).count()` compõe um plano avaliado sob demanda; `DataFrame.count()`, exibição ou escrita acionam execução. Mostre como validar contagens e chaves em amostra segura. O código de exemplo no template é espaço a preencher, não prova de execução; riscos e melhoria devem vir do trecho realmente lido. Uma analogia não substitui revisão de API, interface de programação, custo, permissão ou efeito persistente.

<!-- editorial:exclude:start -->
Fonte: [explicacao_bloco_codigo.md](../../skills/hub-ml-tutor-databricks/templates/explicacao_bloco_codigo.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0216](#doc-0216) · [Próximo: D0218](#doc-0218) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0218"></a>
<a id="doc-0218"></a>
### D0218 — Molde para explicar um notebook inteiro

Este template ajuda o tutor a transformar a leitura de um notebook em explicação de fluxo. Seu consumidor é quem deseja entender objetivo, etapas, entradas, transformações, saídas, pontos críticos e próximos passos, sem pedir que o assistente edite o arquivo. O mapa propõe configuração, leitura, validações, transformação, escrita e métricas; cada etapa só deve aparecer como fato quando o código lido a sustentar. O diagrama com duas tabelas e destino gold é ilustrativo, não descrição de qualquer notebook analisado.

Por exemplo, ao explicar um notebook de carteira, registre parâmetros, tabelas lidas, chave do join, grão antes e depois, filtros e destino que uma operação de escrita realmente aponta. Se há apenas um `display`, não invente persistência. Um status “produção” no cabeçalho exige evidência operacional; o nome do arquivo não basta. Os campos de autor, linguagem e complexidade também podem ficar desconhecidos quando não identificáveis. A seção de melhorias pede motivo e trade-off, como reduzir coleta ao driver em troca de agregação prévia. O template organiza a conversa, mas não executa células nem prova que saídas antigas sejam atuais.

<!-- editorial:exclude:start -->
Fonte: [explicacao_notebook.md](../../skills/hub-ml-tutor-databricks/templates/explicacao_notebook.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0217](#doc-0217) · [Próximo: D0219](#doc-0219) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0219"></a>
<a id="doc-0219"></a>
### D0219 — Skill de validação estatística

A skill planeja e interpreta testes quando uma decisão depende de incerteza, não apenas de descrição da base. Seu consumidor é quem precisa fixar pergunta, população, unidade, desenho, estimando — quantidade que se quer estimar —, efeito mínimo relevante e modo diagnóstico ou inferencial antes de olhar resultados. O fluxo separa plano, preparo de dados, suite pertinente, execução controlada, tamanho de efeito, intervalo de confiança, pressupostos e prescrição. Testes locais em SciPy ou statsmodels pedem amostra limitada; agregações grandes ficam em Spark.

Por exemplo, comparar conversão de dois grupos exige saber se são independentes ou pareados e se as observações da mesma pessoa se repetem. Um p-valor pequeno não mede magnitude; falhar em rejeitar a hipótese nula não prova equivalência. A conclusão deve declarar N, estimativa, incerteza e consequência prática, com correção quando múltiplos testes formam uma família. Na policy vigente, esta skill está em L0, orientação textual, com L3 apenas como alvo em rollout audit; o perfil `TWO_SAMPLE_KS_PILOT_V1` executa comparação única sintética com oráculo externo, sem intervalo de confiança. As demais suites permanecem planejamento; dados reais ficam fora desse piloto. Uma falha de pressuposto pede método ou ressalva proporcionais, não remoção automática de variável ou retreino.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-validacao-estatistica/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0218](#doc-0218) · [Próximo: D0220](#doc-0220) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0220"></a>
<a id="doc-0220"></a>
### D0220 — Tabela de decisão sobre pressupostos

O template relaciona diagnóstico, possível violação e alternativas por família: regressão, séries temporais, aprendizado de máquina tabular, redes neurais e inferência entre grupos. Seu consumidor é o analista que já definiu estimando — quantidade que se quer estimar —, desenho e risco e precisa escolher resposta proporcional ao achado. A tabela liga diagnóstico à evidência e a alternativas que precisam de justificativa; códigos de testes não ampliam a capacidade do piloto KS. Não transforma automaticamente o resultado de um teste em comando para refazer o projeto.

Por exemplo, resíduos heterocedásticos têm variância dos erros não constante, o que pode distorcer os erros padrão usados na inferência; uma alternativa é avaliá-los com método robusto antes de abandonar o modelo. Para dois grupos pareados, usar teste independente ignora a dependência e pede revisão do desenho. VIF, fator de inflação da variância, p-valor e PSI, índice de estabilidade populacional, exigem contexto e critérios aprovados; o arquivo remove cortes universais e remediações automáticas. ADF e KPSS são testes de estacionariedade com hipóteses diferentes; um resultado isolado não certifica previsão. Registre efeito, intervalo, amostra, sensibilidade, mitigação e risco residual. Risco crítico interrompe a etapa dependente; mitigação proposta não equivale a executada, e um reteste não apaga falha anterior ou risco residual.

<!-- editorial:exclude:start -->
Fonte: [decisao_pressupostos.md](../../skills/hub-ml-validacao-estatistica/templates/decisao_pressupostos.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0219](#doc-0219) · [Próximo: D0221](#doc-0221) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0221"></a>
<a id="doc-0221"></a>
### D0221 — Estrutura do notebook StatCheck

O template distribui um diagnóstico estatístico em blocos de notebook `StatCheck_<contexto>`: identificação, imports, inventário, plano, testes gerais, suite específica, consolidação, prescrições e resumo executivo. Seu consumidor é quem monta uma entrega reproduzível sem misturar intenção do teste com resultado observado. Cada teste aplicável e suportado usa uma célula anterior que explica pergunta e configuração, uma célula de código e uma posterior com evidência e interpretação. Se uma condição bloqueante de chave ou unidade falhar, a suite dependente não deve ser apresentada como executada.

Por exemplo, antes de testar resíduos de uma regressão, registre qual modelo e amostra os produziram; se uma rota suportada exigir coleta para SciPy, limite linhas, declare semente e preserve o desenho. A preparação confirma perfil, dependências, alfa, amostra e orçamento, sem defaults silenciosos ou registro global de tema. Imports obrigatórios ausentes bloqueiam; não redefina helpers. O piloto `TWO_SAMPLE_KS_PILOT_V1` exige dados sintéticos, runner e verificador; IC permanece `UNSUPPORTED_IN_PROFILE`. Campos `{{TABELA}}`, contagens e semáforos são placeholders. O notebook só pode anunciar resultados após execução, e seu relatório precisa separar decisão estatística de política de negócio.

<!-- editorial:exclude:start -->
Fonte: [notebook_output_stat.md](../../skills/hub-ml-validacao-estatistica/templates/notebook_output_stat.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0220](#doc-0220) · [Próximo: D0222](#doc-0222) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0222"></a>
<a id="doc-0222"></a>
### D0222 — Relatório diagnóstico consolidado

Este template reúne os testes executados de uma validação estatística em um diagnóstico com decisão e ações. Seu consumidor é quem precisa ver método, modo, quantidade de testes, resultado por código, severidade, condições de avanço e sequência de correção. O quadro distingue OK, atenção, crítico, informativo e pulado; os números devem corresponder aos cards individuais, não a uma lista de testes apenas planejados. GO técnico permite apenas a próxima etapa no escopo e autorização aplicáveis, CONDICIONAL pede mitigação verificável, e NO-GO interrompe a etapa dependente.

Imagine uma chave duplicada que muda a unidade da análise. Resolva essa base antes de interpretar correlações calculadas sobre linhas multiplicadas; por isso a sequência de prescrições tem dependências. No modo inferencial, o template manda NO-GO diante de crítico; essa é regra editorial local que precisa ser lida com o desenho e o risco, não selo regulatório universal. O relatório pede critérios aprovados e direção de cada métrica, justificativa e próximo passo. `{{N_CRITICO}}`, badges e semáforo são espaços a preencher, não resultados. Um teste não aplicável deve aparecer separado, com motivo e fora da contagem executada, e um p-valor sem efeito e incerteza não basta para decisão.

<!-- editorial:exclude:start -->
Fonte: [relatorio_diagnostico.md](../../skills/hub-ml-validacao-estatistica/templates/relatorio_diagnostico.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0221](#doc-0221) · [Próximo: D0223](#doc-0223) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0223"></a>
<a id="doc-0223"></a>
### D0223 — Rubrica de severidade estatística

A rubrica ajuda a classificar achados em OK, informativo, atenção ou crítico conforme impacto na decisão. Seu consumidor é quem consolida testes sem reduzir gravidade a um p-valor. O mecanismo pede identificar pressuposto ou estimando — quantidade que se quer estimar — afetado, magnitude, intervalo de incerteza, unidades atingidas, persistência em análises de sensibilidade, custo do erro e mitigação com critério de aceite. Assim, a mesma estatística pode ter consequência diferente para exploração, inferência ou operação.

Por exemplo, algumas duplicatas explicáveis podem pedir atenção e correção de chave; duplicatas que mudam a unidade de decisão invalidam a análise dependente. Uma mudança de distribuição medida por PSI, índice de estabilidade populacional, só se torna crítica quando população ou contrato mudou de modo material para o uso declarado, considerando desempenho e volume. Vazamento de informação posterior à decisão pode contaminar validação mesmo com métrica alta. O card final liga achado, evidência, severidade, impacto, mitigação, aceite e risco residual. As categorias do template são linguagem customizada, não padrão universal; critérios precisam ser calibrados à população, ao desenho e à política aprovada antes de preencher status.

<!-- editorial:exclude:start -->
Fonte: [severity_rubric.md](../../skills/hub-ml-validacao-estatistica/templates/severity_rubric.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0222](#doc-0222) · [Próximo: D0224](#doc-0224) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0224"></a>
<a id="doc-0224"></a>
### D0224 — Plano anterior aos testes estatísticos

O plano registra a decisão antes de executar testes: conjunto de dados, unidade, alvo, método, modo diagnóstico ou inferencial, suites escolhidas, amostra, prioridade e custo estimado. Seu consumidor é quem precisa evitar escolher o teste depois de ver o p-valor. Para cada teste, a tabela pede código, nome, justificativa, prioridade e tamanho da amostra; a legenda da prioridade orienta parar, mitigar ou documentar conforme o nível. “Core Suite” reúne checagens de qualidade e suficiência; suites específicas dependem do modelo e da pergunta. O template lista sete testes gerais, mas a skill orienta aplicar o que é pertinente, registrando não aplicabilidade quando necessário.

Por exemplo, antes de comparar dois grupos, descreva se as mesmas pessoas aparecem em ambos, qual diferença importa e se há múltiplas comparações. Declarar `toPandas()` no plano é estimar a coleta para biblioteca local, não autorizar trazer dados ilimitados ao driver: fixe tamanho e semente e agregue em Spark antes. MCAR indica ausência completamente aleatória; MAR, ausência explicável por variáveis observadas; MNAR, ausência dependente de informação não observada. Uma taxa de nulos isolada não distingue esses mecanismos. Prioridades e tempo no arquivo são campos planejados, não medições. O plano deve sobreviver ao resultado, permitindo distinguir hipótese prévia de análise exploratória posterior.

<!-- editorial:exclude:start -->
Fonte: [test_plan.md](../../skills/hub-ml-validacao-estatistica/templates/test_plan.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0223](#doc-0223) · [Próximo: D0225](#doc-0225) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0225"></a>
<a id="doc-0225"></a>
### D0225 — Card de resultado de teste

O template separa um card antes da execução de outro depois dela. Seu consumidor é quem explica um teste sem inventar resultado: o pré-card define pergunta, hipótese nula e alternativa quando cabíveis, relevância para o caso, pré-condições, amostra, semente e nível de significância. O pós-card recebe estatística, p-valor ou métrica sem p-valor, faixa de referência, interpretação, severidade e até três ações. Há uma variante para várias variáveis e extensão inferencial com efeito e intervalo de confiança quando calculados e suportados; no piloto KS, IC é `UNSUPPORTED_IN_PROFILE`.

Por exemplo, ao avaliar dispersão por segmento, o pré-card explica por que variâncias diferentes alterariam a inferência. Se o teste não se aplica por pré-condição ausente, registre `SKIPPED`, motivo e alternativa proposta, em vez de preencher a tabela com números fictícios. Um p-valor menor que 0,05 não mede tamanho do efeito nem probabilidade de a hipótese nula ser verdadeira; a conclusão deve relacionar estimativa, incerteza e decisão. O molde mantém quatro casas como formatação, mas exige seed declarada ou não aplicável com motivo e alfa declarado ou pendente, sem preencher ausências por default. O arquivo organiza relato, mas não executa código.

<!-- editorial:exclude:start -->
Fonte: [test_result_card.md](../../skills/hub-ml-validacao-estatistica/templates/test_result_card.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0224](#doc-0224) · [Próximo: D0226](#doc-0226) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0226"></a>
<a id="doc-0226"></a>
### D0226 — Instruções operacionais do assistente no Hub

Este arquivo orienta o Genie Code a escolher recursos do Hub e a separar explicar, planejar, gerar código e executar. Seu consumidor é o assistente ao receber um pedido: confirma a raiz `.assistant`, lê a skill pertinente, consulta policy vigente e usa helpers por importação e chamada reais, sem presumir que uma referência os executou. O mapa de demandas inclui Micromodelos e é roteiro de seleção; Concierge é opcional. O README do objeto pertinente deve ser lido quando existir; sua ausência é lacuna documental, não licença para inventar a interface. A instrução de inicialização não amplia permissões do workspace.

No contrato atual, regras de entrypoint deixam claro: selecionar a skill e pedir para pular runner não autoriza análise manual substituta. `BLOCKED`, `FAIL` ou `INCOMPLETE` interrompem a execução; `PENDING_POSTFLIGHT` permite trabalho necessário ao handoff, entrega final estruturada, e à verificação final, sem declarar conclusão. Para skills com Postflight, a resposta final exige `completion.authorized=true` no payload finalizado; ausência desse gate mantém a tarefa canônica não concluída. Um plano não autoriza escrita, e dados sensíveis, deploy e produção dependem das permissões e decisões aplicáveis. O arquivo orienta comportamento; não prova que o Genie Code remoto carregou ou obedeceu cada regra.

<!-- editorial:exclude:start -->
Fonte: [.assistant_instructions.md](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/ambiente_databricks/.assistant_instructions.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0225](#doc-0225) · [Próximo: D0227](#doc-0227) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0227"></a>
<a id="doc-0227"></a>
### D0227 — README da fonte editável do produto

Este README marca `ambiente_databricks/` como a cópia editável e neutra do conteúdo que seguirá para Databricks. Ele existe porque o mesmo produto aparece em várias camadas: fonte versionada, espelho local de workspace, laboratório Free e destino de trabalho. Sem essa distinção, alguém pode editar o derivado ou tomar um arquivo no Git como prova de publicação. O diagrama e a tabela do documento mostram o papel de cada camada e indicam que o consumidor do ambiente já publicado deve abrir o guia de `.assistant/`.

O mantenedor usa o README para percorrer validação da fonte, renderização do simulado com `--check`, publicação e verificação remota de conteúdo quando autorizado. A árvore distingue `.assistant_instructions.md` e `skills/`, que usam mecanismos nativos, dos componentes `hub_prompts`, `hub_snippets`, `hub_scripts`, `hub_padroes`, `hub_micromodelos` e `hub_readmes_visual_assets`, criados neste projeto. Links levam a playbooks para sequência operacional e a READMEs de coleção para entendimento do produto. O renderer consome a fonte; o workspace recebe uma cópia operacional.

A regra de manutenção é editar `ambiente_databricks/`, nunca `.artifacts/simulado/` à mão. Mesmo depois de um teste no Free, compute, permissões e dados do trabalho exigem conferência própria. O README não contém nem demonstra acesso a um workspace corporativo; seus comandos de publicação são responsabilidade de quem opera a entrega, não requisito de primeiro uso para um analista.

<!-- editorial:exclude:start -->
Fonte: [ambiente_databricks/README.md](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/ambiente_databricks/README.md). Contexto: [MT02](MT-parte-i.md#mt02).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0226](#doc-0226) · [Próximo: D0228](#doc-0228) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0228"></a>
<a id="doc-0228"></a>
### D0228 — Guia de Skill Enforcement

Esta ficha é HISTÓRICA: edição de 01/10/2026, ausente no produto atual. O guia ensina a criar uma skill reconhecível, testar sua seleção e distinguir uso de recursos, qualidade do resultado e prova da execução. Seu consumidor é quem desenha ou revisa skills. Dez histórias do Hub mostram falhas diferentes: pedidos de teste sem artefato, helpers importados sem chamada, bypass, contexto declarado contra dados, auditoria que transmite segurança indevida e certificador que também precisou de testes. O exemplo de vendas é ilustrativo e verificável à mão; seus quatro registros não representam execução de uma skill publicada.

Na edição preservada, L0 é orientação; L1 estrutura contrato; L2 faz preflight, conferência prévia; L3 usa runner e Receipt, comprovante da rota; L4 exige Postflight, conferência final antes de concluir. Escolha o nível pelo risco da etapa, sem tratar `target_level` como nível vigente. Por exemplo, uma skill explicativa pode bastar com orientação, enquanto uma checagem obrigatória de duplicatas pode precisar de prova de chamada e bloqueio se faltar chave. Um Receipt válido não avalia a interpretação de negócio nem autentica, sozinho, quem controlou os registros. O guia preserva caminhos antigos; consulte os responsáveis atuais abaixo. É síntese histórica local; não concede permissão, não altera policy e não demonstra comportamento homologado do Genie Code em outro ambiente.

<!-- editorial:exclude:start -->
Fonte histórica: [guia de 01/10/2026](MT-proveniencia.md#fonte-historica-d0228). Estado e operação atuais: [enforcement](../../hub_padroes/skill_enforcement/README.md), [policy](../../hub_padroes/skill_enforcement/policy.json), [skills](../../skills/README.md) e [rollout SER](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/skill_enforcement_rollout/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0227](#doc-0227) · [Próximo: D0229](#doc-0229) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0229"></a>
<a id="doc-0229"></a>
### D0229 — Por onde começar a estudar um micromodelo?

O README de `hub_micromodelos` apresenta uma característica delimitada por regras, evidências e incerteza, antes de encaminhar ao código. Sua posição na raiz do módulo permite escolher entre contrato, biblioteca, jornada e exemplos. Quem começa pelo resultado pode examinar a recência de contato; quem revisa uma definição segue para o arquivo de especificação `micromodelo.yaml`.

O exemplo introdutório espera sete pessoas fictícias, duas classificadas como `TRUE`, uma como `FALSE` e quatro como `INDETERMINADO`. Os comandos conferem arquivos locais e imprimem resultados; a preparação da entrega continua `DRAFT_NOT_SUBMITTED`, com `published=false`. Esses valores são o resultado esperado documentado, não uma execução feita pela leitura desta ficha.

O índice explica como descoberta, especificação, estudo e governança se conectam. A skill orienta a conversa, enquanto a biblioteca exige chamadas explícitas. A documentação também separa histórico de execuções no MLflow da especificação no YAML. Mantenedores devem reconciliar os links e as receitas quando essas responsabilidades mudarem. Ter código importável não fornece acesso a dados, aprovação humana ou execução protegida da skill: sua policy permanece `L1/audit`, com evolução para L3 apenas como alvo.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_micromodelos/README.md). Detalhe: [MT20](MT-parte-v.md#mt20).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0228](#doc-0228) · [Próximo: D0230](#doc-0230) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0230"></a>
<a id="doc-0230"></a>
### D0230 — O que um YAML válido ainda não comprova?

O guia de contratos ensina a ler `micromodelo.yaml` como uma especificação revisável. Ele aproxima o schema, que define estrutura e condições, do template e do exemplo preenchido. Serve a autores e revisores que precisam distinguir erro de preenchimento de uma decisão ainda pendente, sem transformar um formulário completo em aprovação de negócio.

A sequência proposta carrega documento e schema, obtém os problemas de validação e só então calcula a assinatura material. Essa assinatura é um hash para comparar conteúdo relevante, não a assinatura de um aprovador. Alterar uma regra ou limiar pode modificá-la; ajustar texto editorial pode preservá-la. O mapa de blocos ajuda a localizar entidade, fontes, evidências, saída e proveniência sem supor que todos tenham o mesmo papel.

Por exemplo, a ausência de registros continua `INDETERMINADO` quando falta regra aprovada para interpretá-la. Um score entre zero e cem também não se torna probabilidade sem calibração. Ao manter o guia, confira os nomes e condições no schema e nos invariantes de domínio. Estados `PENDENTE` e referências nulas podem ser honestos; resultados medidos, aceite e publicação precisam de provas próprias.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_micromodelos/contratos/README.md). Detalhe: [MT21](MT-parte-v.md#mt21).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0229](#doc-0229) · [Próximo: D0231](#doc-0231) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0231"></a>
<a id="doc-0231"></a>
### D0231 — Qual chamada corresponde à etapa do estudo?

O README de execução organiza a biblioteca de micromodelos por entradas, resultados e efeitos. Ele atende quem precisa escolher uma função sem presumir que todo arquivo YAML possa ser executado como modelo. A receita local usa uma fixture, entrada sintética preparada, para demonstrar um envelope de metadados sem consultar o Databricks.

O mapa distingue validação da especificação, assinatura material, descoberta, proposta de estudo, laboratório e preparação da entrega. `MetadataCollector` recebe um provedor e um vínculo de catálogo; o adaptador Databricks exige sessão explícita e consulta somente metadados permitidos. Mesmo uma observação marcada `OBSERVED` pode ser parcial. Um `snapshot_id` identifica essa observação local, sem garantir uma fotografia transacional de todas as consultas.

Para entender recência, o leitor segue ao exemplo fechado; para preparar textos, encontra artefatos `NOT_RUN`; para entrega, recebe um rascunho sem publicação. Tracking exige outra rota e autorização para seus efeitos. Mantenedores devem conferir assinaturas e dependências antes de atualizar as receitas. O documento não promete executor universal: o laboratório tem perfil próprio, e negar uma consulta não demonstra que o objeto seja inexistente.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_micromodelos/execucao/README.md). Detalhe: [MT21](MT-parte-v.md#mt21).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0230](#doc-0230) · [Próximo: D0232](#doc-0232) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0232"></a>
<a id="doc-0232"></a>
### D0232 — Qual exemplo permite conferir as classes sem dados reais?

O índice de exemplos reúne casos fictícios para aprender o contrato de micromodelos. Seu papel é encaminhar ao caso de recência, ao catálogo sintético e à comparação simulada de saídas, sem repetir a explicação completa de cada arquivo. Ele atende leitores que querem uma entrada inspecionável antes de discutir adaptação a fontes reais.

A rota recomendada começa na raiz `.assistant`, com as dependências de execução disponíveis. O primeiro comando confere a classificação de sete pessoas contra o resultado esperado; o segundo prepara um rascunho de entrega. Duas classes positivas, uma negativa e quatro indeterminadas formam o total documentado. Os scripts leem os arquivos locais e imprimem resultados, sem publicar um produto de dados.

O ensaio de migração tem outra finalidade: comparar saídas legadas sintéticas. Sua presença não significa migração institucional já realizada. Ao manter este índice, confira destinos, arquivos do exemplo e coerência das contagens com o oráculo preservado. Reproduzir a fixture verifica aquele cálculo didático; desempenho estatístico, representatividade e autorização para uso real exigem avaliação separada. A continuação natural é o README de recência, que explica por que cada classe foi atribuída.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_micromodelos/exemplos/README.md). Detalhe: [MT22](MT-parte-v.md#mt22).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0231](#doc-0231) · [Próximo: D0233](#doc-0233) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0233"></a>
<a id="doc-0233"></a>
### D0233 — Por que falta de contato não basta para classificar como falso?

O guia de recência de contato explica um micromodelo completo com sete pessoas e seis eventos inventados. A pergunta é deliberadamente estreita: existe contato verificável entre zero e sete dias antes da referência de 30/09/2026? O documento combina roteiro de execução, resultado esperado e mapa dos atributos do YAML para quem aprende a relacionar regra, dado e conclusão.

Uma pessoa com contato recente confirmado recebe `TRUE`; uma negativa explícita, com cobertura completa, sustenta `FALSE`. Já contato antigo, cobertura parcial, conflito e simples ausência de evento permanecem `INDETERMINADO`. Assim, as classes somam sete sem ocultar quatro casos incertos. O score mede força de evidência pela regra sintética e não probabilidade.

O roteiro permite explorar outro limiar somente em cópia de trabalho e adverte contra alterar o oráculo para obter aprovação. A preparação da entrega reconcilia classes e scores, mas conserva `DRAFT_NOT_SUBMITTED`; agregados fornecidos continuam `SUPPLIED_UNVERIFIED`. Ao manter o exemplo, confira juntos YAML, dados, fórmula e resultado esperado. Execução didática não altera sozinha validação institucional, aprovação humana ou publicação, e esta leitura não afirma ter executado os comandos.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_micromodelos/exemplos/recencia_contato/README.md). Detalhe: [MT22](MT-parte-v.md#mt22).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0232](#doc-0232) · [Próximo: D0234](#doc-0234) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0234"></a>
<a id="doc-0234"></a>
### D0234 — Como distinguir a próxima etapa da decisão que ainda falta?

O guia de jornada liga briefing, especificação, estudo e entrega sem esconder as decisões entre eles. É útil para quem coordena um caso e precisa saber qual registro produzir, qual função pode ajudar e quem deve decidir depois. A tabela de etapas relaciona entrada, saída verificável e próxima decisão, enquanto o mapa de capacidades delimita o que existe hoje.

Na descoberta, metadados autorizados sustentam hipóteses para escolha humana. Com objetivo conhecido, o YAML recebe regras, fontes e pendências. O estudo pode começar por textos `NOT_RUN` ou por ensaio sintético fechado. Registrar uma execução no MLflow conserva seu histórico; não aprova a característica nem substitui a especificação. A entrega prepara `DRAFT_NOT_SUBMITTED`, com `published=false`, para a governança externa.

Por exemplo, uma coleta parcial deve gerar uma lacuna explícita antes de justificar uma candidata. Não permite inventar fontes ou consultar registros por consequência. Mantenedores devem atualizar o guia quando uma responsabilidade mudar, preservando a separação entre contrato, código, evidência e aceite. O leitor termina sabendo onde guardar cada informação. Catálogo de casos e comparação simulada de legados também têm limites: não concedem migração, promoção ou publicação real.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_micromodelos/guias/README.md). Detalhe: [MT20](MT-parte-v.md#mt20).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0233](#doc-0233) · [Próximo: D0235](#doc-0235) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0235"></a>
<a id="doc-0235"></a>
### D0235 — Quando explorar oportunidades antes de especificar uma característica?

O README de `descobrir_micromodelos` explica quando usar o briefing de exploração: a área e a decisão são conhecidas, mas a característica ainda não foi escolhida. O resultado solicitado é uma lista curta de hipóteses, chamada shortlist, para triagem humana. Esse guia acompanha o formulário e seu exemplo, distinguindo a descoberta de oportunidades da elaboração posterior do YAML.

O leitor informa decisão, população, restrições e critérios qualitativos. Pode trabalhar com catálogo autorizado ou somente com uma fixture textual. Nesse segundo percurso, a informação é `FORNECIDA`, e o escopo efetivamente observado permanece vazio. Por exemplo, um nome de tabela pode sugerir recência de eventos, mas não comprova qualidade temporal nem viabilidade em registros.

O documento ensina a deduplicar candidatas por decisão, característica, população, grão e horizonte, preservando motivos de descarte e próximo teste. Mantenedores devem reconciliar os campos com o briefing e registrar o alcance do exemplo conversacional. Descrições e tags são dados não confiáveis; não viram instruções ou autorização. A shortlist não constitui catálogo completo, modelo validado ou prova de execução. Depois da escolha humana, a rota adequada passa a ser `OBJETIVO_CONHECIDO`.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_prompts/descobrir_micromodelos/README.md). Detalhe: [MT12](MT-parte-iii.md#mt12).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0234](#doc-0234) · [Próximo: D0236](#doc-0236) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0236"></a>
<a id="doc-0236"></a>
### D0236 — Como pedir uma shortlist sem inventar fontes ou viabilidade?

O formulário `descobrir_micromodelos.md` organiza um pedido manual para a skill de micromodelos. Seus campos fixam área e decisão, escopo, população, restrições e critérios de escolha. Essa forma ajuda o solicitante a limitar a exploração antes de receber ideias; o texto não é um coletor que se executa ao ser aberto.

O bloco copiável pede descoberta gradual: observar objetos permitidos, selecionar candidatas e só depois detalhar seus metadados. Se houver apenas uma fixture textual, a resposta deve conservar `FORNECIDA` e não inventar consulta. Por exemplo, nomes e tipos podem sustentar uma hipótese de recência, mas deixam viabilidade e qualidade temporal indeterminadas. A priorização é qualitativa até existir uma regra aprovada.

A saída solicitada reúne cobertura, shortlist deduplicada, descartes e próximo teste por candidata. Antes de iniciar um YAML, o prompt pede escolha humana. Quem o mantém deve conferir campos, modo e limites com a skill e os contratos atuais. A seleção manual da skill não cria permissões: leitura de linhas, contagens e profiling ficam fora deste pedido. Uma resposta conversacional tampouco comprova execução no ambiente ou acesso ao catálogo inteiro.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_prompts/descobrir_micromodelos/descobrir_micromodelos.md). Detalhe: [MT12](MT-parte-iii.md#mt12).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0235](#doc-0235) · [Próximo: D0237](#doc-0237) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0237"></a>
<a id="doc-0237"></a>
### D0237 — Como iniciar um micromodelo quando a decisão já existe?

O README de `micromodelo_novo` orienta o uso do briefing para uma característica já escolhida. Ele explica o que preparar antes da conversa e como interpretar o retorno, enquanto o formulário contém o pedido copiável. Serve a quem conhece a decisão, mas ainda precisa delimitar entidade, grão, tempo, fontes e critérios de estudo.

Um exemplo é estudar interesse recente em canal digital para revisão humana de contatos sintéticos. Se chave, fonte ou responsável forem desconhecidos, o pedido conserva essas lacunas. Com template e schema acessíveis, a skill pode propor o YAML e informar a validação realmente realizada. Sem eles, deve entregar checklist textual, `YAML_NAO_CRIADO` e `MM01_NAO_VALIDADO`, em vez de fabricar uma especificação aparentemente válida.

O guia distingue contexto fornecido de observação, hipótese de medição e ausência de evidência de classe falsa. Também encaminha o estudo de registros a especialistas, sob autorização própria. Mantenedores devem preservar essa distinção ao atualizar exemplos e campos. O relato conversacional datado demonstra apenas seu alcance documentado; não prova o estado atual de outras rotas. Preencher o briefing não executa um micromodelo, promove fase nem aprova publicação.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_prompts/micromodelo_novo/README.md). Detalhe: [MT12](MT-parte-iii.md#mt12).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0236](#doc-0236) · [Próximo: D0238](#doc-0238) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0238"></a>
<a id="doc-0238"></a>
### D0238 — Que campos impedem um objetivo vago de virar uma regra inventada?

O prompt `micromodelo_novo.md` transforma uma decisão conhecida em pedido de especificação progressiva. Ele separa decisão, característica, entidade e grão, população e horizonte, fontes, responsável e uso, restrições e referência do pedido original. Essa organização permite registrar o que falta sem substituir desconhecimento por um valor plausível.

Por exemplo, “interesse recente” precisa de unidade de análise, relógio e evidências antes de receber um limiar. O bloco copiável pede proveniência, hipóteses favoráveis e contrárias, além das condições de `TRUE`, `FALSE` e `INDETERMINADO`. Sem observação e rubrica explícita, conserva `SCORE_INDETERMINADO`; um número entre zero e cem não vira probabilidade por aparência.

O pedido só admite YAML quando template e schema estiverem realmente acessíveis. Caso contrário, solicita checklist com `YAML_NAO_CRIADO` e `MM01_NAO_VALIDADO`. Quem mantém o formulário deve confrontar nomes e condições com o contrato, sem usar um exemplo conversacional antigo como prova atual de execução. O solicitante confere se houve validação real, quais decisões continuam pendentes e qual especialista deve receber a próxima etapa. O texto não concede acesso a registros nem publica artefatos.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../hub_prompts/micromodelo_novo/micromodelo_novo.md). Detalhe: [MT12](MT-parte-iii.md#mt12).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0237](#doc-0237) · [Próximo: D0239](#doc-0239) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0239"></a>
<a id="doc-0239"></a>
### D0239 — Qual receita de baseline calcula localmente e qual altera tracking?

O README dos scripts de baseline distingue duas rotas que têm efeitos diferentes. `run.py` calcula um caso sintético em memória; `run_tracking.py` pode criar experimento, execução e modelo no MLflow, fazer leitura de conferência e realizar exclusão lógica. O leitor deve escolher a rota antes de preparar dependências e autorização.

A receita local exemplifica o perfil `BINARY_TEMPORAL_LOCAL_V1`: separação temporal, ajuste somente no treino e conferência independente das partições e métricas. Request e identificador da tentativa são guardados fora do resultado para que o verificador tenha expectativas confiadas. A presença de Receipt, comprovante estruturado da rota, não aprova o modelo para dados reais.

Na rota de tracking, a autorização fica vinculada ao pedido, usuário, destino e efeito específicos. O texto explica a conferência do modelo enquanto o experimento está ativo e o limite da verificação posterior à exclusão. Mantenedores devem reconciliar a receita com contratos, manifesto de release e verificadores. `BLOCKED` ou `UNKNOWN_RESIDUE` exige examinar a tentativa e seus identificadores antes de qualquer repetição. Exclusão lógica não equivale a apagamento físico, e ler a receita não autoriza executar seus efeitos.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-baseline-ml/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0238](#doc-0238) · [Próximo: D0240](#doc-0240) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0240"></a>
<a id="doc-0240"></a>
### D0240 — O que a receita linear permite conferir sobre SHAP?

O README de explicação sintética apresenta uma rota estreita para atribuições SHAP, valores que repartem a previsão em relação a uma referência. Ele atende quem precisa preparar entradas reais do programa e conferir o resultado com uma conta analítica. O request escrito em JSON não substitui os objetos do modelo, da amostra e do background, a linha de referência.

A receita usa regressão linear escalar e conserva ordem de features, identificadores e formato dos arrays. O runner vincula cópias numéricas de conversão exata ao pedido e à release; o verificador recebe expectativas externas e compara as atribuições com o oráculo linear. Na função ilustrativa com intercepto três, coeficientes dois e menos um, a contribuição de cada variável pode ser conferida diretamente.

Quem mantém a documentação deve verificar dependências, contrato e receita quando o perfil mudar. Nenhum script descrito persiste a saída. O Receipt registra vínculos da execução local, sem autenticar uma pessoa ou promover a skill. Essa explicação não demonstra causalidade e não cobre classificação, árvores, KernelSHAP ou gráficos. Se SHAP estiver indisponível, a execução fica bloqueada; o texto não substitui a chamada por resultado inventado.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-explainability/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0239](#doc-0239) · [Próximo: D0241](#doc-0241) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0241"></a>
<a id="doc-0241"></a>
### D0241 — Por que calcular lag, compor uma vista e materializar exigem rotas distintas?

O README de engenharia de features organiza três percursos com contratos próprios. O primeiro calcula defasagens em memória; o segundo compõe uma vista após verificar a junção temporal upstream; o terceiro pode materializar uma tabela Delta sintética mediante autorização vinculada ao efeito. A tabela inicial evita que o leitor interprete uma receita local como permissão para gravar dados.

No perfil `FIXED_LAG_L1_V1`, lag significa a observação anterior da mesma entidade dentro da janela elegível, não necessariamente o dia anterior. A receita guarda as features esperadas separadamente do resultado. Assim, remover linhas sem histórico suficiente não permite esconder o denominador anterior ao aquecimento.

A vista temporal exige entradas e identificadores externos para verificar a prova upstream e a projeção. Sua existência não implica treino nem nova materialização. Esta última tem pedido, digest, autorização, leitura de conferência, repetição controlada do MERGE e limpeza próprios. Mantenedores devem reconciliar cada receita com seu contrato específico; não existe schema genérico para as três. Um estado `UNKNOWN` requer inspeção, e não repetição automática. Recibos e hashes comprovam vínculos delimitados, sem transformar o ensaio sintético em prontidão de negócio.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-feature-engineering/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0240](#doc-0240) · [Próximo: D0242](#doc-0242) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0242"></a>
<a id="doc-0242"></a>
### D0242 — Onde termina a skill conversacional e começa a biblioteca?

O README da skill de micromodelos apresenta seu contrato conversacional `L1/audit`. Sua função é orientar planejamento e especificação, enquanto a implementação de domínio fica em `hub_micromodelos`. Essa separação ajuda quem encontra a pasta da skill a não presumir que selecionar seu nome executará automaticamente validação, descoberta ou estudo.

O leitor escolhe entre objetivo conhecido e descoberta de oportunidades, informando decisão ou área, ambiente, fonte lógica e permissões. O exemplo pede uma característica de recência a partir de descrição sintética, mantendo chave, instante e disponibilidade como lacunas. O resultado pretendido é um rascunho de requisitos, sem consulta de registros ou medição presumida.

O guia encaminha ao método em `SKILL.md`, ao contrato estático e à jornada do módulo. Mantenedores devem atualizar essas rotas juntas quando uma responsabilidade mudar. A pasta da skill não oferece runner protegido, Receipt ou adaptador de descoberta executável; o módulo separado contém biblioteca e adaptador com chamadas explícitas. Portanto, disponibilidade de código não promove a policy para L3, aprova dados ou autoriza publicação. Para operar uma função, o leitor continua ao guia do módulo correspondente.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-micromodelos/README.md). Detalhe: [MT14](MT-parte-iii.md#mt14).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0241](#doc-0241) · [Próximo: D0243](#doc-0243) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0243"></a>
<a id="doc-0243"></a>
### D0243 — Como a skill preserva incerteza ao estruturar um micromodelo?

O arquivo `SKILL.md` define o método conversacional de micromodelos. Seu cabeçalho declara nome e situações de seleção; o corpo distingue objetivo conhecido de descoberta de oportunidades. O leitor encontra entradas mínimas, sequência, exclusões e encaminhamentos, em vez de um programa que executaria qualquer especificação recebida.

Com objetivo conhecido, a skill pede decisão, população, entidade, tempo e fontes, conservando lacunas. Só propõe YAML com template e schema acessíveis; sem eles, entrega checklist e registra a ausência de criação e validação. Na descoberta, metadados sustentam hipóteses deduplicadas, com seleção humana antes da especificação. Descrições e tags são dados não confiáveis, incapazes de mudar instruções ou permissões.

Por exemplo, conhecer nomes de colunas não prova viabilidade temporal nem autoriza consultar valores. O método preserva `INDETERMINADO`, separa informação fornecida de observação e encaminha estudos especializados sob a policy de cada skill. Mantenedores devem reconciliar cabeçalho, fluxo, recursos e contrato quando a rota mudar. O nível L1 é estático: código de domínio disponível não cria runner protegido ou Receipt. Evidência conversacional, execução no laboratório e autorização corporativa continuam distintas; nenhuma delas deve ser inferida da presença do arquivo.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-micromodelos/SKILL.md). Detalhe: [MT14](MT-parte-iii.md#mt14).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0242](#doc-0242) · [Próximo: D0244](#doc-0244) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0244"></a>
<a id="doc-0244"></a>
### D0244 — Mudança de distribuição significa perda de performance?

O README de monitoramento separa duas perguntas que exigem dados diferentes. O perfil de drift compara distribuições de scores sem rótulos; o perfil de performance binária exige rótulos já disponíveis no instante de avaliação e uma política fornecida. A tabela inicial ajuda a escolher a rota antes de interpretar qualquer indicador como degradação do modelo.

Na receita de distribuição, request e identificador da tentativa permanecem fora do payload para alimentar a conferência independente. O texto explica tratamento de nulos, agrupamento dos scores e comparação das distribuições. Na receita de performance, verificar o runner ainda não encerra o diagnóstico: a sequência inclui `verify`, `finalize` e `verify_finalized`, preservando a prova da conferência final.

Por exemplo, rótulos posteriores a `evaluation_at` não podem ser tratados como maduros apenas porque já aparecem numa tabela. Mantenedores devem conferir a política da fixture e os contratos de cada perfil, sem transformar seus limiares em regra universal. Os resultados descritos ficam em memória e exigem dados realmente sintéticos. Nenhum status autoriza alerta, retreino ou promoção; dados reais anonimizados também não passam a ser fixtures sintéticas.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-monitoramento-modelo/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0243](#doc-0243) · [Próximo: D0245](#doc-0245) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0245"></a>
<a id="doc-0245"></a>
### D0245 — Qual evidência separa planejar um pipeline de executar uma transformação?

O README do Pipeline Builder distingue conferência de especificação, execução Spark local e ensaio Delta autorizado. Quem planeja pode manter permissões desconhecidas; isso não autoriza escrita. O preflight, conferência prévia, valida o pedido e conserva execução de implantação como `NOT_RUN`, sem criar tabelas, jobs ou Receipt de deploy.

A receita local fornece especificação completa e linhas esperadas independentes do resultado. Para a chave repetida, vence o evento mais recente; empate temporal com conteúdo diferente é conflito. O runner cria uma vista temporária, consulta e remove essa vista. Seu comprovante identifica uma transformação delimitada, sem demonstrar implantação de um job.

O ensaio Delta acrescenta efeitos persistentes: criação, MERGE, leitura, repetição para conferir idempotência e remoção da tabela própria. Exige destino novo, autorização vinculada e marcas de propriedade verificadas antes da limpeza. Mantenedores devem reconciliar cada receita com entradas, verificadores e contratos correspondentes. Se uma falha deixar `UNKNOWN`, é preciso inspecionar o recurso da tentativa anterior; repetir escrita para descobrir o estado pode ampliar o problema. O guia não autoriza usar esse ensaio como simples teste de instalação.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-pipeline-builder/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0244](#doc-0244) · [Próximo: D0246](#doc-0246) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0246"></a>
<a id="doc-0246"></a>
### D0246 — Como conferir o resultado de duas amostras sem confiar no próprio payload?

O README da validação estatística explica uma comparação sintética pelo teste de Kolmogorov–Smirnov, abreviado KS. O perfil é bicaudal, com amostras numéricas contínuas, independentes e sem empates. A independência é declaração do estudo; o programa não a deduz dos números. O guia atende quem executa e revisa a receita, incluindo a preservação da evidência.

A sequência passa por preflight, runner e verificador, interrompendo após erro. O runner imprime o resultado; o operador de redirecionamento do shell é quem grava o arquivo e pode sobrescrevê-lo. Por isso cada tentativa precisa de nome e identificador próprios. A conferência exige request, identificador e valores esperados obtidos fora do payload.

Para as amostras originais de um a quatro e de cinco a oito, o documento desenvolve o oráculo: estatística um e valor-p de um trinta e cinco avos. Essa conta pertence à fixture, não a qualquer entrada. Mantenedores devem revisar receita, versão e expectativas quando o caso mudar, sem ajustar o oráculo apenas para obter aprovação. Receipt comprova vínculos delimitados; não fornece intervalo de confiança, equivalência, causalidade ou decisão de negócio.

<!-- editorial:exclude:start -->
Fonte: [documento original](../../skills/hub-ml-validacao-estatistica/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0245](#doc-0245) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
