# MT atlas 04

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0151"></a>
<a id="doc-0151"></a>
### D0151 — Template de métricas de classificação

O template reúne métricas de classificação para quem compara baseline e candidato em população definida. Pede período, número de eventos, prevalência, custo dos erros, referência trivial, métrica primária, limiar e critério de aceite. Separa discriminação, calibração, operação no limiar e robustez por período ou segmento. OOT significa teste fora do tempo; sua coluna não deve receber resultado de um split aleatório apresentado como temporal.

AUC-ROC, área sob a curva de sensibilidade versus taxa de falsos positivos, mede discriminação por ordenação de positivos e negativos, não percentual de acertos. AUC-PR, área sob a curva de precisão e recall, resume essas duas medidas e deve ser lida com a prevalência em evento raro. Brier mede erro quadrático médio das probabilidades previstas; métricas de limiar, como precision e recall, dependem da regra operacional escolhida. Por exemplo, uma melhora na AUC pode coexistir com calibração ruim ou volume sinalizado acima da capacidade da equipe.

O cabeçalho avisa que não há faixas universais de “bom” para essas métricas; benchmark e política devem ser específicos. Valores `[X]` são espaços a preencher após medição, não evidência de performance. A skill de baseline permanece L0, orientação textual, na policy, e o template não executa avaliação nem autoriza produção.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/metricas_classificacao.md](../../skills/hub-ml-baseline-ml/templates/metricas_classificacao.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0150](MT-atlas-03.md#doc-0150) · [Próximo: D0152](#doc-0152) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0152"></a>
<a id="doc-0152"></a>
### D0152 — Template de métricas de ranking

O template de ranking ajuda a comparar modelos que ordenam itens dentro de grupos de consulta. NDCG é ganho cumulativo descontado normalizado: valoriza relevância e posição. MAP é a média entre consultas da precisão média (AP) calculada nas posições dos itens relevantes de cada consulta; MRR é média do inverso da posição do primeiro item relevante. Essas métricas não são intercambiáveis e exigem rótulos e grupos válidos. O arquivo reserva resultados em k, baseline aleatório, comparação de abordagens e análise por grupo.

Imagine ordenar ofertas para clientes. Compare o ranker com uma regra simples nos mesmos grupos e no mesmo período; conte consultas sem itens relevantes e escolha k conforme a decisão. O critério depende do estudo, benchmark e responsável, sem faixas universais. NDCG@k descreve ordenação ponderada e normalizada, não percentual de acertos; hit rate ou Precision@k devem ser relatados separadamente, com seus denominadores.

O limite k é o número de posições avaliadas. Todos os valores `[X]` são placeholders, não resultados de avaliação. Importância de feature não prova causa da ordenação. A skill de baseline permanece L0, orientação textual, na policy; este modelo de relatório não treina ranker nem valida grupos.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/metricas_ranking.md](../../skills/hub-ml-baseline-ml/templates/metricas_ranking.md).
Definição de MAP: [Stanford IR Book, avaliação de rankings](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0151](#doc-0151) · [Próximo: D0153](#doc-0153) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0153"></a>
<a id="doc-0153"></a>
### D0153 — Métricas de regressão

Este template orienta a leitura de erros de regressão, isto é, previsões de valor numérico. RMSE é a raiz do erro quadrático médio e pesa mais desvios grandes; MAE é o erro absoluto médio, na unidade do alvo. R², coeficiente de determinação, compara a qualidade do ajuste com uma referência constante, e MAPE mede erro percentual absoluto médio, mas falha quando o valor real é zero ou quase zero. O consumidor deve escolher a métrica conforme custo e escala do erro, não por faixa universal.

Se o alvo é custo em reais, MAE de R$ 200 significa erro absoluto médio de R$ 200 no recorte avaliado; RMSE de R$ 600 sugere erros grandes que merecem inspeção. Dividir RMSE pela média do alvo só ajuda quando essa média é materialmente diferente de zero e a razão faz sentido no domínio. R² negativo pode simplesmente indicar desempenho pior que a média de referência no conjunto avaliado, sem provar bug.

O arquivo rejeita faixas universais de MAPE e R² e exige critério do caso, baseline e incerteza. O texto executivo contém placeholders, não medições. Compare sempre baseline trivial, período e distribuição dos resíduos antes de recomendar uso.

<!-- editorial:exclude:start -->
Fonte: [metricas_regressao.md](../../skills/hub-ml-baseline-ml/templates/metricas_regressao.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0152](#doc-0152) · [Próximo: D0154](#doc-0154) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0154"></a>
<a id="doc-0154"></a>
### D0154 — Relatório comparativo de métricas

O template reúne uma camada executiva e outra técnica para comparar baseline e modelo no mesmo problema. Em classificação binária, reserva AUC, área sob curva de discriminação, KS, distância máxima entre distribuições acumuladas de score, lift, calibração e métricas por treino, validação e teste. Em regressão, lista RMSE, raiz do erro quadrático médio, MAPE, erro percentual absoluto médio, e R². O consumidor preenche população, denominadores, unidades e referência antes de atribuir qualidade.

AUC resume ordenação de um par positivo-negativo; não é percentual de casos corretos. Brier mede erro quadrático médio das probabilidades, não produz sozinho rótulo “confiável”. RMSE está na unidade do alvo e não deve ser traduzido como erro médio simples para cima ou para baixo. Um intervalo de confiança só aparece após estimação apropriada; a coluna `IC 95%`, intervalo de confiança de 95%, vazia não o calcula. Delta relativo precisa de denominador e sinal definidos.

O próprio bloco de aceite pede benchmark histórico, custo dos erros e política aprovada: faixas universais para AUC, KS ou R² não são válidas. Células `[X]` e semáforos são exemplos. Ler o arquivo não executa treino, calcula métrica ou aprova modelo.

<!-- editorial:exclude:start -->
Fonte: [metricas_report.md](../../skills/hub-ml-baseline-ml/templates/metricas_report.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0153](#doc-0153) · [Próximo: D0155](#doc-0155) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0155"></a>
<a id="doc-0155"></a>
### D0155 — Métricas de previsão temporal

Este template compara erros de previsão de séries ao longo do tempo. MAPE é erro percentual absoluto médio e fica indefinido quando o valor real é zero; sMAPE é uma versão simétrica que também exige cuidado com valores muito pequenos. MASE é erro absoluto médio escalado: abaixo de um, o erro absoluto médio avaliado é menor que o denominador ingênuo calculado no treino; isso não prova superar a previsão ingênua nos mesmos períodos de teste. RMSE, raiz do erro quadrático médio, conserva a unidade do alvo. Coverage é a fração observada coberta por intervalos preditivos.

Imagine vendas mensais com sazonalidade. Compare modelo e previsão ingênua sazonal nos mesmos períodos de teste, por fold, uma rodada ou janela de avaliação, com horizonte fixo. Se MASE é 1,1, o modelo teve erro escalado maior nessa avaliação; isso não prova inutilidade universal. Coverage de 95% exige comparar proporção empírica, incerteza amostral e largura dos intervalos; faixa muito larga cobre mais sem ser útil.

O template exige critérios do estudo e resultados observados; métricas ausentes ficam NÃO CALCULADO. A frase executiva não autoriza produção nem substitui backtesting, validação histórica em janelas sucessivas, análise de custo e incerteza. Nenhuma previsão foi gerada por ler o arquivo.

<!-- editorial:exclude:start -->
Fonte: [metricas_series_temporais.md](../../skills/hub-ml-baseline-ml/templates/metricas_series_temporais.md).
Referência metodológica: [Forecasting: Principles and Practice, §5.8, Scaled errors](https://otexts.com/fpp3/accuracy.html), consultada em 2026-10-05; leitura estática, sem execução.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0154](#doc-0154) · [Próximo: D0156](#doc-0156) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0156"></a>
<a id="doc-0156"></a>
### D0156 — Checklist de tracking no MLflow

O checklist serve ao mantenedor de um baseline que precisa registrar o que foi realmente treinado. MLflow é a ferramenta de tracking de runs, parâmetros, métricas e artefatos. Quando aplicável e autorizado, o arquivo lista experimento, run, tags exigidas pelo perfil, modelo, assinatura, input e artefatos observados; isso facilita reproduzir comparação e encontrar limitações. O consumidor precisa confirmar API, interface de programação, versão, compute e permissões do ambiente antes de preencher cada item.

Num treino de classificação, registre métricas por split sem misturar teste com validação; um `run_id` só existe se a chamada de logging ocorreu. A lista separa registro no Unity Catalog de métricas: exige rota compatível, destino, governança e autorização próprios. Um checklist marcado não prova que o registro remoto foi persistido ou que o modelo foi promovido. Evite PII, informações pessoais identificáveis, em amostras e artefatos.

`BINARY_TEMPORAL_LOCAL_V1` não grava MLflow; tracking fica NÃO APLICÁVEL nessa rota. O adapter separado exige `SER10-AUTH-1`, verificação e cleanup, mantendo Registry fora do escopo. Se tracking exigido não estiver acessível, registre a lacuna; UNKNOWN não autoriza repetir efeitos. A policy da skill de baseline está em L0, orientação textual.

<!-- editorial:exclude:start -->
Fonte: [mlflow_checklist.md](../../skills/hub-ml-baseline-ml/templates/mlflow_checklist.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0155](#doc-0155) · [Próximo: D0157](#doc-0157) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0157"></a>
<a id="doc-0157"></a>
### D0157 — Estrutura do notebook de baseline

O template organiza um notebook de baseline em configuração, carga, divisão dos dados, referência trivial, modelo candidato, avaliação, diagnóstico e handoff. O cabeçalho pede suite B1–B7, dataset, target quando houver, split, data e autor. B4, agrupamento, e B7, anomalias, podem não ter target confiável; preencher um por conveniência mudaria a tarefa. A sequência ajuda o consumidor a localizar onde cada decisão e evidência deveria aparecer.

Num caso de cancelamento, a referência trivial e o modelo devem usar a mesma população e métrica, com transformações ajustadas no treino. A tabela executiva resume decisão, enquanto a técnica guarda métricas por treino, validação e teste e incerteza quando estimada. A seção de importância usa somente método suportado, com conjunto, escala e normalização declarados. SHAP, atribuição de contribuição ao modelo, não representa percentual de decisões. Seções fora do perfil ficam não aplicáveis, com motivo.

O template contém placeholders e ordem sugerida, não código executado. Run de MLflow, ferramenta de tracking, só existe após registro observado; o Context Card é proposta de repasse, não publicação. A policy do baseline continua L0, orientação textual.

<!-- editorial:exclude:start -->
Fonte: [notebook_output_baseline.md](../../skills/hub-ml-baseline-ml/templates/notebook_output_baseline.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0156](#doc-0156) · [Próximo: D0158](#doc-0158) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0158"></a>
<a id="doc-0158"></a>
### D0158 — Relatório executivo de baseline

Este template prepara uma síntese de baseline para quem decide se vale avançar na modelagem. Pede tipo de problema, população, período, métrica principal, comparação com referência trivial, semáforo, atributos importantes, limitações e próximos passos. Seu propósito é conectar o resultado observado à decisão, não trocar evidência por adjetivos como “bom” ou “pronto”.

Imagine um modelo que melhora a métrica no teste, mas varia muito entre meses. O quadro deve registrar ganho com unidade, tamanho do grupo, split, incerteza e estabilidade antes de sugerir explicabilidade ou mais features. O gap treino–teste pode sinalizar sobreajuste, mas precisa de métrica, direção e recorte comparáveis. Os percentuais de “importância” das top features exigem método e normalização declarados; não são parcelas causais das decisões. Um semáforo só tem sentido com critério aprovado e responsável.

Frases executivas e features listadas são placeholders; a seção de importância só se preenche quando calculada, na escala declarada. O template não mede performance nem promove modelo. Se não houve treino, a saída deve permanecer plano ou rascunho, sem preencher números plausíveis. A skill de baseline está em L0, orientação textual, na policy atual.

<!-- editorial:exclude:start -->
Fonte: [relatorio_executivo_baseline.md](../../skills/hub-ml-baseline-ml/templates/relatorio_executivo_baseline.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0157](#doc-0157) · [Próximo: D0159](#doc-0159) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0159"></a>
<a id="doc-0159"></a>
### D0159 — Tabela de faixas de score

O template organiza uma população por faixas de score para examinar volume, taxa de evento e efeito de um ponto de corte. Cada linha pede limites do score, número de observações, bons, maus, taxa de default e volume acumulado. “Bom” e “mau” dependem da definição explícita do evento; a taxa usa maus divididos pelo total elegível da faixa. A ordenação A “melhor” até E “pior” ordena risco, não determina a orientação numérica: declare se score alto representa risco maior ou menor. Limites mínimo e máximo são placeholders a preencher conforme escala observada.

Se uma política cogita aprovar até a faixa C, calcule a parcela da população incluída e a taxa de evento nesse conjunto com denominador agregado; não some taxas das faixas. Compare com a política atual no mesmo período e população. KS, distância máxima entre distribuições acumuladas de score, e Gini, medida de discriminação derivada da curva de ordenação, não escolhem sozinhos o corte. Capacidade operacional e custo de erro importam.

O arquivo pede volume mínimo, monotonicidade, estabilidade e taxas relativas justificados pelo estudo; sem política, o estado é NÃO CLASSIFICADO. Score bands não são probabilidades calibradas por definição. Placeholders e cores não provam risco observado nem autorizam decisão de crédito.

<!-- editorial:exclude:start -->
Fonte: [score_bands_table.md](../../skills/hub-ml-baseline-ml/templates/score_bands_table.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0158](#doc-0158) · [Próximo: D0160](#doc-0160) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0160"></a>
<a id="doc-0160"></a>
### D0160 — Relatório de scorecard de crédito

O template estrutura o relatório de um scorecard: objetivo e horizonte, amostra de desenvolvimento, evento “mau”, seleção de variáveis, faixas, regressão logística, pontos, performance, bandas e estabilidade. IV, valor de informação, resume separação descritiva de uma variável; WoE, peso de evidência, expressa uma razão logarítmica entre distribuições de bons e maus, cujo sinal depende da convenção adotada. Esses campos ajudam o revisor a rastrear de onde veio cada ponto do score.

Num produto de crédito, a definição de inadimplência e a data de observação vêm antes do binning, divisão de uma variável em faixas. A parametrização PDO, pontos para dobrar as odds, precisa definir o evento cuja probabilidade é p: odds são p/(1−p), razão entre probabilidades de evento e não evento. Inverter o evento altera a orientação e a leitura do score. PSI, índice de estabilidade populacional, compara distribuições entre referências e janelas, mas seu valor isolado não diagnostica causa. KS, distância máxima entre distribuições acumuladas, e Gini são medidas de discriminação, não provas de calibração.

A interpretação do IV e a seleção exigem contexto e ganho incremental; somar IVs não mede informação conjunta. Aprovação humana é decisão separada. O texto executivo e valores `[X]` exigem medições e política aplicável; nenhum scorecard foi treinado por abrir o arquivo. A skill de baseline permanece L0, orientação textual, na policy.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/scorecard_report.md](../../skills/hub-ml-baseline-ml/templates/scorecard_report.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0159](#doc-0159) · [Próximo: D0161](#doc-0161) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0161"></a>
<a id="doc-0161"></a>
### D0161 — Estratégia de divisão dos dados

O guia ajuda a escolher treino, validação e teste de acordo com o uso futuro, repetição da entidade e prevalência do target. Split é a divisão dos exemplos; leakage é informação indisponível na decisão que contamina a avaliação. Para previsão futura, separe por datas e preserve ordem; se o mesmo cliente gera várias linhas, defina se as entidades devem ser disjuntas; histórico da mesma entidade pode ser legítimo em painéis. Estratificação só é segura depois de afastar risco temporal ou por entidade.

Imagine prever cancelamento mensal. Uma linha por cliente-mês pode cruzar treino e teste se dividir aleatoriamente, tornando a métrica otimista. O guia encaminha a `temporal_split`, que divide períodos observados inteiros. O gap precisa refletir maturação do rótulo e atraso real; pular um bucket observado não garante duração fixa se faltam períodos. Use limites por calendário e verifique sobreposição de entidades, features futuras e preprocessing ajustado fora do treino.

Os defaults da API não são critérios universais; no perfil `BINARY_TEMPORAL_LOCAL_V1`, prevalecem valores fixos do perfil e seu runner. O checklist é uma proposta de verificação, não teste executado. A escolha do split só fica defensável com data, chave, horizonte e população do caso.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/split_strategy.md](../../skills/hub-ml-baseline-ml/templates/split_strategy.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0160](#doc-0160) · [Próximo: D0162](#doc-0162) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0162"></a>
<a id="doc-0162"></a>
### D0162 — Guia de escolha da suite de baseline

Este guia mapeia a pergunta do projeto para uma suite da skill de baseline. B1 cobre classificação, regressão e scorecard; B2, previsão temporal; B3, aprendizado profundo comparado a B1; B4, agrupamento; B5, ordenação; B6, tempo até evento com censura, quando o evento não foi observado até o fim do acompanhamento; B7, detecção de anomalia. O consumidor deve declarar o objetivo antes do algoritmo, porque cada família exige referência, split e métrica próprios.

Se a pergunta é “quando um contrato entra em atraso?”, B6 só faz sentido quando tempo de observação, evento e censura estão definidos. Se é “quais clientes são parecidos?”, B4 pode não ter target supervisionado. O texto traz perguntas sobre target, tempo e rótulos confiáveis para diferenciar esses casos. As frases de trigger com `@hub-ml-baseline-ml` ajudam a pedir uma rota, mas não provam que ela foi selecionada ou executada.

O próximo passo é planejar a suite escolhida e confirmar a rota executável. B1–B7 são categorias metodológicas, não promessa de execução de todas as suites. Volume, disponibilidade temporal, custo do erro e restrições do ambiente ainda precisam ser confirmados. O guia não cria dataset nem escolhe suite por leitura; a policy da skill segue L0, orientação textual.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/suite_selection_guide.md](../../skills/hub-ml-baseline-ml/templates/suite_selection_guide.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0161](#doc-0161) · [Próximo: D0163](#doc-0163) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0163"></a>
<a id="doc-0163"></a>
### D0163 — Interpretação de análise de sobrevivência

O template de survival, análise do tempo até um evento, registra número de eventos e censuras, horizonte, curvas Kaplan–Meier, grupos, razões de risco e validação. Censura significa que o evento não foi observado até o fim do acompanhamento; não equivale a ausência definitiva de evento. S(t) representa a probabilidade estimada de permanecer sem evento além do tempo t, sob pressupostos de censura. A mediana pode não ser estimável se a curva não cair a 50%.

Em comparação de dois grupos, HR, razão de riscos instantâneos do modelo de Cox, compara taxas instantâneas condicionais ao modelo: HR=2 não significa “duas vezes mais chance de evento em doze meses”. É preciso conferir intervalo de confiança, proporcionalidade dos riscos e confusão antes de interpretar a associação. O C-index mede concordância de ordenação de tempos/risco, não probabilidade individual calibrada. O IBS, erro de Brier integrado no tempo, exige definição do horizonte e tratamento da censura.

O arquivo exige benchmark e critérios do estudo, descreve associação com hazard e subordina intervenções a política e aprovação próprias; não oferece cortes universais nem inferência causal. Sem dados e validação, nenhuma curva, mediana ou vantagem foi demonstrada. A skill de baseline permanece L0, orientação textual, na policy.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/survival_interpretation.md](../../skills/hub-ml-baseline-ml/templates/survival_interpretation.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0162](#doc-0162) · [Próximo: D0164](#doc-0164) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0164"></a>
<a id="doc-0164"></a>
### D0164 — Guia de validação walk-forward

O guia apresenta walk-forward, validação que treina em passado e testa em janelas futuras sucessivas. Na janela expansiva, o treino cresce a cada fold, ou rodada; na deslizante, mantém tamanho fixo e descarta passado antigo, mas essa opção não existe no helper canônico. O mecanismo aproxima a previsão operacional e expõe variação de desempenho ao longo do tempo. Faz sentido quando a decisão usa dados futuros em relação ao treino, não como regra cega para qualquer problema.

Considere previsão mensal com doze meses iniciais de treino e dois de teste. A rodada seguinte avança o corte sem permitir que dados posteriores entrem no ajuste anterior. `gap` conta períodos observados entre treino e teste; lacunas no calendário exigem conferir a duração real conforme horizonte, atraso do rótulo e disponibilidade das features. Relate métrica por rodada, média, dispersão e pior período; uma média boa pode esconder falha recente.

A API `walk_forward_cv` chama `model_fn` em cada fold e retorna métricas e metadados em dicionários; o callback ajusta somente no treino. Pouco histórico pode produzir lista vazia. Os números de folds e janelas são exemplos. Ler o pseudocódigo no template não executa backtesting nem demonstra estabilidade do modelo.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-baseline-ml/templates/walk_forward_guide.md](../../skills/hub-ml-baseline-ml/templates/walk_forward_guide.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0163](#doc-0163) · [Próximo: D0165](#doc-0165) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0165"></a>
<a id="doc-0165"></a>
### D0165 — Skill para comentar notebook

A skill `hub-ml-comentar-notebook` atende quem quer tornar legível um notebook existente sem mudar seu comportamento. Ela pede o notebook anexado, lê objetivo, entradas, saídas e dependências entre células e decide onde cabem explicações antes e depois de trechos críticos. Sua entrega é o mesmo notebook com células Markdown adicionadas; código, ordem, parâmetros e resultados existentes devem ser preservados byte a byte salvo pedido explícito de mudança.

Antes de uma transformação, a célula PRÉ explica objetivo, grão e saída esperada. Depois, a PÓS interpreta contagem ou métrica realmente observada, risco e próximo passo. Se o notebook não foi executado, deixe número pendente. Não transforme AUC, área sob curva de discriminação, em percentual de acerto nem SHAP, contribuição atribuída ao modelo, em efeito causal. PII, informações pessoais identificáveis, e segredos não devem ser reproduzidos na documentação.

A skill recomenda templates conforme densidade e `hub_scripts.doc_coverage` para medir cobertura quando útil; importar helper não comprova aplicação. A policy atual marca L1, contrato estático, e rollout audit, que mede desvios sem veto automático por si; isso não elimina bloqueios de outros validadores. Não há runner que garanta invariância de cada notebook editado. A revisão precisa comparar diff do código e outputs reais.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-comentar-notebook/SKILL.md](../../skills/hub-ml-comentar-notebook/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0164](#doc-0164) · [Próximo: D0166](#doc-0166) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0166"></a>
<a id="doc-0166"></a>
### D0166 — Template pós-código completo

Este template é para a célula Markdown após um bloco crítico de notebook, como validação de qualidade, granularidade ou resultado material. Pede, quando pertinente, indicador-chave de desempenho, ou KPI, tabela de resultados, interpretação técnica e de negócio, checks, riscos e próximo passo. O consumidor deve escolher apenas seções que ajudam a entender a decisão; uma célula longa pode ser dividida entre parte factual e interpretativa.

Imagine uma verificação de duplicatas. A tabela só pode dizer “54 duplicatas” ou `STATUS: OK` se o output realmente observou 54 no recorte e se há critério para chamar isso de aceitável. O template começa com NÃO EXECUTADO, NÃO INFORMADO e campos sem números; valores e checks só devem ser preenchidos após verificação. Indique chave, filtros e denominador antes de concluir taxa. O bloco PÓS deve estar junto da célula correta; se não houve execução, marque resultado pendente e descreva o teste necessário.

O teto de quatro ou cinco KPIs e orientações de apresentação não impõem quota mínima de linhas nem qualidade analítica automática. O arquivo não executa código nem valida notebook. A skill de comentário exige preservar as células existentes, e a policy atual é L1, contrato estático, com rollout audit que mede desvios sem veto automático por si; outros validadores podem bloquear, e isso não garante o diff.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-comentar-notebook/templates/bloco_markdown_pos_codigo.md](../../skills/hub-ml-comentar-notebook/templates/bloco_markdown_pos_codigo.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0165](#doc-0165) · [Próximo: D0167](#doc-0167) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0167"></a>
<a id="doc-0167"></a>
### D0167 — Bloco pós-código compacto

Este template orienta uma célula Markdown curta depois de uma célula cujo resultado já é simples e verificável. O consumidor é quem comenta um notebook existente: deve mostrar até três indicadores-chave de desempenho (KPIs), o achado principal, seu impacto imediato e o próximo passo. A síntese curta serve à legibilidade, sem quota rígida de linhas; não dispensa evidência nem transforma resultado em aprovação.

Numa checagem de constantes, o exemplo fictício mostra zeros, sem demonstrar valor preditivo ou ausência de redundância. Ao aplicar o molde, leia primeiro a saída da célula, confirme população e critérios, e só então escreva a contagem realmente observada. Se a célula não foi executada ou a saída não está disponível, deixe o valor pendente. Um `printSchema` sem surpresa pode receber nota breve; uma divergência de chave, duplicatas materiais ou risco de negócio exige o template pós-código completo e interpretação específica.

O exemplo está explicitamente rotulado como fictício e não deve ser copiado como resultado observado. A skill de comentário preserva código e resultados existentes; o template não executa validação. Sua policy atual é L1, contrato estático; audit é o modo de rollout que mede desvios sem substituir verificações.

<!-- editorial:exclude:start -->
Fonte: [bloco_markdown_pos_compacto.md](../../skills/hub-ml-comentar-notebook/templates/bloco_markdown_pos_compacto.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0166](#doc-0166) · [Próximo: D0168](#doc-0168) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0168"></a>
<a id="doc-0168"></a>
### D0168 — Bloco pré-código completo

Este molde produz a célula Markdown anterior a um bloco de notebook que merece contexto técnico. Quem documenta preenche objetivo, papel no fluxo, entradas, parâmetros, lógica, funções ou interfaces de programação (APIs), resultado esperado e pontos de atenção. A posição antes do código ajuda o leitor a entender a intenção e a reconhecer quando a implementação ou a saída não corresponde ao plano.

Imagine uma junção entre pedidos e clientes. A célula pré deve dizer quais chaves entram, qual cardinalidade se espera, quais filtros atuam antes da junção e qual grão da saída se pretende obter. Se o bloco escreve uma tabela, informe destino e efeito persistente previsto; não use a forma compacta para esconder essa mutação. Uma previsão de volume exige fundamento identificado, sem ser apresentada como contagem observada. A contagem real pertence à célula pós e só pode aparecer após ler o resultado da execução.

O template é uma estrutura para adaptar ao código existente, não uma prova de que filtros ou verificações foram implementados. A skill de comentário não altera código sem pedido explícito; mantenha premissas e riscos visíveis quando ainda dependem de validação. Policy L1 significa contrato estático, não execução garantida.

<!-- editorial:exclude:start -->
Fonte: [bloco_markdown_pre_codigo.md](../../skills/hub-ml-comentar-notebook/templates/bloco_markdown_pre_codigo.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0167](#doc-0167) · [Próximo: D0169](#doc-0169) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0169"></a>
<a id="doc-0169"></a>
### D0169 — Bloco pré-código compacto

Este template serve a um trecho simples de notebook que precisa de orientação, mas não de análise extensa: configuração, imports agrupados, função auxiliar curta ou leitura direta. A célula Markdown pré-código usa objetivo, entradas e saída numa introdução curta quando a intenção não for óbvia. Não comente imports triviais ou código autoexplicativo. Quem comenta deve ligar cada campo à célula adjacente e explicar por que aquela preparação é necessária ao restante do fluxo.

Antes de `spark.read.table(...)`, por exemplo, informe qual tabela autorizada é lida, qual DataFrame se espera e onde ele será usado. A leitura direta não comprova esquema nem contagem; só descreva valores observados se houver saída real. Para um bloco que grava Delta, modifica configuração compartilhada, agrega com regra de negócio ou gera métrica, prefira o pré-código completo: explicite destino, transformação, premissas e risco. Quando houver resultado material, acrescente também uma célula pós adequada.

A forma curta reduz ruído, não autoriza omitir efeito persistente ou inventar diagnóstico. O exemplo de imports do arquivo é ilustração de formato. A skill exige preservar comportamento do notebook; sua policy atual L1 sustenta contrato textual e estático; audit mede desvios no rollout, sem garantir que um notebook comentado passou por verificação automática.

<!-- editorial:exclude:start -->
Fonte: [bloco_markdown_pre_compacto.md](../../skills/hub-ml-comentar-notebook/templates/bloco_markdown_pre_compacto.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0168](#doc-0168) · [Próximo: D0170](#doc-0170) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0170"></a>
<a id="doc-0170"></a>
### D0170 — Cabeçalho de notebook documentado

Este template coloca no início do notebook uma ficha de leitura: título, responsável, versão, datas, projeto, catálogo, esquema, status, objetivo, público, posição no fluxo, entradas, saídas, premissas, limites, riscos e instruções de execução. Seu consumidor é tanto quem mantém o notebook quanto quem precisa executá-lo ou revisar seus efeitos. O cabeçalho fornece contexto para a interpretação das células, sem substituir a inspeção do código.

Num pipeline que escreve uma tabela, registre o nome da entrada e da saída apenas se forem conhecidos e autorizados, a chave e a data de referência que determinam o recorte, e os pré-requisitos que a execução exige. Diferencie saída prevista de tabela efetivamente persistida. Os passos “executar em ordem” e “conferir resumo” são orientações a adaptar ao fluxo real; não provam que o notebook já rodou.

O arquivo pede autor/equipe informados, versão observada e estado comprovado, mantendo catálogos como placeholders. Reutilizá-los literalmente pode atribuir responsabilidade, ambiente ou status falsos. Preencha somente fatos fornecidos ou verificados e marque o restante como pendente. A skill de comentário mantém código e outputs existentes; policy L1 sustenta contrato estático e audit mede desvios no rollout; nenhum deles certifica a atualidade do cabeçalho.

<!-- editorial:exclude:start -->
Fonte: [cabecalho_notebook.md](../../skills/hub-ml-comentar-notebook/templates/cabecalho_notebook.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0169](#doc-0169) · [Próximo: D0171](#doc-0171) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0171"></a>
<a id="doc-0171"></a>
### D0171 — README do Concierge Hub

O README apresenta o Concierge a quem sabe sua necessidade, mas não conhece a taxonomia do Hub. Ele aponta o contrato em `SKILL.md`, as decisões, o procedimento de instalação, os exemplos e os testes. A promessa é uma recomendação verificável de método, briefing, helper e ordem de uso; o Concierge não é executor universal. O Manual Técnico permanece dono do inventário semântico, sem catálogo paralelo mantido pela skill.

O contrato estático atual é L1/audit. Estrutura do pacote, transporte da release e comportamento conversacional são provas distintas. Encontrar a pasta no repositório não demonstra que ela está instalada ou ativa num workspace. Para uma simulação, anexe a skill e os recursos necessários; isso permite avaliar a resposta no contexto recebido, mas não comprova descoberta nativa por relevância ou menção `@`.

O exemplo sobre nulos e duplicidades pede recomendação sem consulta nem escrita; a resposta deve respeitar esse modo e distinguir checagem pontual de análise exploratória de dados (EDA) completa. Arquivos de teste e exemplos mostram critérios e casos, não homologação remota por si. Consulte o resultado observado da instalação pretendida antes de afirmar disponibilidade.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-concierge/README.md](../../skills/hub-ml-concierge/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0170](#doc-0170) · [Próximo: D0172](#doc-0172) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0172"></a>
<a id="doc-0172"></a>
### D0172 — Contrato da skill Concierge

A skill Concierge é acionável para descobrir ou compor recursos do Hub quando a pessoa pede orientação de escolha. Ela começa pelo objetivo e pela raiz autorizada confirmada, consulta o Manual Técnico, as cinco famílias gerais e o domínio pertinente, reduz candidatos e verifica contratos dos finalistas antes de recomendar a menor rota suficiente. O leitor deve distinguir descoberta de execução: ler um módulo não importa Python, consulta tabelas ou ativa outra skill.

Se alguém pergunta como checar nulos numa tabela, a rota pode ser `HELPER_ROUTE` após conferir entrada, assinatura e efeitos de um helper público. Se faltam chave e grão para escolher entre checagem pontual e método amplo, `BRIEFING_FIRST` registra a ambiguidade que muda a escolha. Já um pedido explícito à skill de análise exploratória de dados (EDA) não deve ser interceptado pelo Concierge. A rota escolhida e a cobertura (`TOTAL_PARA_ESCOPO`, `PARCIAL` ou `NAO_DETERMINADA`) são campos independentes.

A resposta cita arquivos e seções realmente lidos, base e versão, limites e próxima ação. Sem acesso, use `ACCESS_BLOCKED`, não infira lacuna global. Um `@` no texto é repasse, não chamada automática. Policy atual L1: contrato estático, sem execução de candidatos; audit mede desvios no rollout.

<!-- editorial:exclude:start -->
Fonte: [hub-ml-concierge/SKILL.md](../../skills/hub-ml-concierge/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0171](#doc-0171) · [Próximo: D0173](#doc-0173) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0173"></a>
<a id="doc-0173"></a>
### D0173 — Arquitetura e decisão do Concierge

Este documento delimita a descoberta progressiva e a composição no assistente existente. O fluxo vai do pedido à definição de escopo e versão, índices, lista curta, verificação de contratos, composição mínima e recomendação ou repasse. `SKILL.md` contém o procedimento; referências detalham busca e composição; templates ajudam a redigir a entrega. Quem mantém o Hub usa esta separação para revisar cada mudança no lugar certo.

A arquitetura evita transformar uma consulta de catálogo em execução de todos os módulos. Por exemplo, para uma pergunta sobre junção temporal, o Concierge pode comparar método, helper de junção pontual e diagnóstico de cardinalidade; só uma etapa especializada e autorizada executaria código. O documento atribui capacidade analítica aos objetos existentes e conserva o Manual Técnico como inventário, em vez de criar outro registro manual.

O guia distingue recomendação de pipeline testado e encaminha a história ao registro de manutenção externo ao pacote. Integração no Git não demonstra publicação, casos conversacionais ou homologação no workspace. Testes locais podem verificar arquivos e contratos; não demonstram disponibilidade remota. Conteúdo recuperado é evidência para comparação, não ordem para ampliar acesso ou alterar recursos. A policy atual marca Concierge L1, contrato estático, e audit como modo de rollout que mede desvios.

<!-- editorial:exclude:start -->
Fonte: [arquitetura_e_decisao.md](../../skills/hub-ml-concierge/docs/arquitetura_e_decisao.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0172](#doc-0172) · [Próximo: D0174](#doc-0174) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0174"></a>
<a id="doc-0174"></a>
### D0174 — Fontes e compatibilidade do Concierge

Este documento orienta a compatibilidade na instalação autorizada e distingue fontes oficiais de convenções do Concierge. A base histórica e as referências internas de elaboração ficam no registro externo de manutenção. O consumidor é quem revisa uma recomendação ou adapta o procedimento a outra instalação; precisa reconfirmar os contratos na raiz realmente acessível, não supor que o snapshot histórico está publicado.

Por exemplo, a documentação oficial pode sustentar seleção de uma skill por relevância ou menção após instalação compatível. Já `HUB_ROOT`, nome conceitual da raiz consultada, e rotas como `HELPER_ROUTE` são categorias autorais do Concierge, não interfaces nativas da Databricks. Um hash de commit identifica código no Git; não prova que o assistente no workspace consegue lê-lo. Um teste local com Python também não comprova roteamento ou permissões remotas.

A lista de fontes serve à rastreabilidade, não à execução de todos os caminhos citados. Antes de indicar um helper, confira símbolo público, entrada, saída e versão atual. Se a fonte existe apenas como documentação, marque contrato ou disponibilidade como não verificado. Nenhuma consulta a dados reais é inferida deste registro.

<!-- editorial:exclude:start -->
Fonte: [fontes.md](../../skills/hub-ml-concierge/docs/fontes.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0173](#doc-0173) · [Próximo: D0175](#doc-0175) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0175"></a>
<a id="doc-0175"></a>
### D0175 — Instalação, testes e promoção do Concierge

Este guia organiza o primeiro uso em uma instalação autorizada do Concierge. A fonte de manutenção é a pasta canônica em `ambiente_fonte`; a cópia histórica não deve ser instalada em paralelo. O usuário confirma disponibilidade, seleciona `@hub-ml-concierge`, descreve objetivo, recursos e restrições e fornece contexto ou leitura autorizada. Sem acesso, a resposta deve preservar `ACCESS_BLOCKED`, sem inventar recursos.

Instalação, publicação, rollback e validação de manutenção pertencem ao responsável pelo Hub, com escopo e permissões próprios; o guia não manda instalar uma cópia nem misturar versões. Registre separadamente carregamento observado e qualidade da resposta: o assistente imprimir `@hub-ml-concierge` não prova ativação. Também é necessário que Manual e recursos do Hub sejam acessíveis; a skill sozinha não materializa os arquivos que recomenda.

Estrutura, transporte dos bytes e comportamento conversacional são provas diferentes; resultado antigo não homologa a instalação atual. Confira recurso, API, adequação, limites e próxima decisão; a recomendação não executa análise. O roteiro anterior foi encaminhado à manutenção. Apagar no Git não retira automaticamente uma skill já instalada no workspace.

<!-- editorial:exclude:start -->
Fonte: [instalacao_testes_promocao.md](../../skills/hub-ml-concierge/docs/instalacao_testes_promocao.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0174](#doc-0174) · [Próximo: D0176](#doc-0176) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0176"></a>
<a id="doc-0176"></a>
### D0176 — Regras de composição mínima

Esta referência explica como combinar objetos de naturezas diferentes sem lhes atribuir poderes novos. Helper resolve uma operação pontual; skill orienta método; briefing estrutura dados e decisões do caso; padrão orienta criação. O Concierge escolhe entre componente direto, interface de programação (API) pontual, composição complementar ou esclarecimento prévio. A rota `COMPOSITE_ROUTE` só se justifica quando cada peça entrega algo necessário à etapa seguinte.

Para unir um diagnóstico de chaves e uma junção histórica, confira antes tipo do DataFrame, estrutura tabular de linhas e colunas, grão, instante de decisão, nomes de campos, retorno e efeitos persistentes. Em Spark, transformações desse DataFrame distribuído são avaliadas sob demanda. Ele não entra automaticamente em função pandas; converter com `toPandas()` pode estourar memória ou perder contrato. Se falta código de ligação entre partes, apresente a sequência como plano, não pipeline pronto. Uma métrica em razão também não deve ser repassada como percentual sem conversão explícita.

A prioridade de reuso é símbolo público, método público, template metodológico e, por último, adaptação revisada. Não trate função privada ou célula dependente de estado como API estável. O handoff leva decisão, evidências, restrições e lacunas; a menção `@skill` não executa a etapa seguinte nem amplia autorização. A policy do Concierge é L1, contrato estático; audit mede desvios no rollout.

<!-- editorial:exclude:start -->
Fonte: [composicao.md](../../skills/hub-ml-concierge/references/composicao.md).
Referência técnica: [PySpark Quickstart: DataFrame](https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_df.html), consultada em 2026-10-05; leitura estática, sem execução.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0175](#doc-0175) · [Próximo: D0177](#doc-0177) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0177"></a>
<a id="doc-0177"></a>
### D0177 — Descoberta progressiva e evidências

Esta referência define a busca que sustenta uma recomendação do Concierge. `HUB_ROOT` nomeia a raiz efetivamente acessível: fonte do checkout, instalação autorizada ou apenas os anexos recebidos. Manual Técnico e índices apontam candidatos; README, contrato, fachada `__init__.py`, implementação e exemplos esclarecem papéis diferentes. No trabalho, pesquise somente a instalação autorizada; checkout é manutenção separada. Registre a busca e distinga existência, adequação, disponibilidade e execução.

Se a pessoa quer identificar um helper para uma tabela, a busca separa capacidades, consulta as cinco famílias gerais e a área de domínio pertinente, forma lista curta e lê entrada, retorno, dependências e efeitos dos finalistas. Um nome no catálogo não prova tipo de DataFrame, estrutura tabular de linhas e colunas; uma anotação pode se referir a pandas local ou Spark distribuído, cujas transformações são avaliadas sob demanda. Verificação estática lê código, mas não importa módulo ou executa notebook. Se o candidato só aparece em anexo, conclua sobre o anexo, não sobre todo o Hub.

`GAP` significa cobertura inadequada no escopo pesquisado; `ACCESS_BLOCKED`, falta de acesso para verificar. Cobertura `PARCIAL` pode coexistir com uma rota útil. Confiança alta, média ou baixa descreve qualidade da evidência, não probabilidade calculada. A referência não certifica nenhum helper específico sem sua leitura atual.

<!-- editorial:exclude:start -->
Fonte: [descoberta.md](../../skills/hub-ml-concierge/references/descoberta.md).
Referência técnica: [PySpark Quickstart: DataFrame](https://spark.apache.org/docs/latest/api/python/getting_started/quickstart_df.html), consultada em 2026-10-05; leitura estática, sem execução.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0176](#doc-0176) · [Próximo: D0178](#doc-0178) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0178"></a>
<a id="doc-0178"></a>
### D0178 — Exemplos ilustrativos do Concierge

Este arquivo calibra o tamanho e o tipo de resposta do Concierge com sete cenários: qualidade pontual, junção temporal, formatação, drift (mudança de distribuição), ausência de acesso, lacuna de implementação e especialista explícito. São modelos editoriais, não transcrições de atendimentos ou testes atuais. O consumidor usa a estrutura da escolha e revalida cada caminho e assinatura no Hub efetivamente consultado.

Na checagem de nulos de uma tabela, o exemplo aponta um script como candidato pontual e uma skill de análise exploratória de dados (EDA) se a pergunta for ampla. Já na mudança de distribuição sem rótulos, o cenário separa drift de desempenho supervisionado: uma alteração estatística não prova que o modelo piorou. Para junção histórica, a data de disponibilidade do dado, a chave e a cardinalidade são pré-condições antes de propor um helper pontual. Esses exemplos ajudam a formular perguntas, não autorizam consulta ou treino.

A classificação `ACCESS_BLOCKED` do caso sem arquivos preserva a incerteza; não conclui inexistência do recurso. Quando o usuário já escolheu um especialista, o Concierge não deve interceptar o trabalho. Nomes de helpers no arquivo precisam ser reconfirmados, e nenhum deles foi chamado por esta leitura.

<!-- editorial:exclude:start -->
Fonte: [exemplos.md](../../skills/hub-ml-concierge/references/exemplos.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0177](#doc-0177) · [Próximo: D0179](#doc-0179) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0179"></a>
<a id="doc-0179"></a>
### D0179 — Template de handoff do Concierge

Este template transporta para a etapa especializada apenas o contexto que já foi confirmado. Campos de destino, objetivo, decisão esperada, modo autorizado e proibições preservadas mantêm a autorização original visível. Base consultada, recursos e evidências mostram o que foi de fato lido; entradas disponíveis, ausentes, adaptações e lacunas impedem que uma hipótese seja transferida como dado.

Imagine que o Concierge recomendou um helper de junção temporal, mas não recebeu a chave de entidade. O repasse deve listar o símbolo verificado e o instante de decisão, escrever `NÃO INFORMADO` para a chave, definir validação de cardinalidade como critério e registrar qualquer código de ligação ainda não implementado. A ordem pré-condição → etapa → saída não significa execução já realizada. O campo final deixa explícito que há somente uma recomendação.

Um `@` dentro do texto não é chamada de ferramenta nem ativação de outra skill. O handoff evita repetir a descoberta resolvida e só retorna ao Concierge se surgir lacuna nova. Não inclua credenciais, dados pessoais ou números não observados. Este molde não salva arquivo, cria sessão ou amplia permissões por si.

<!-- editorial:exclude:start -->
Fonte: [handoff.md](../../skills/hub-ml-concierge/templates/handoff.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0178](#doc-0178) · [Próximo: D0180](#doc-0180) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0180"></a>
<a id="doc-0180"></a>
### D0180 — Template de recomendação do Concierge

Este é o molde da resposta principal do Concierge. O consumidor preenche objetivo compreendido, rota, cobertura, componente escolhido, evidências, ordem, condições, limites, base consultada, alcance, confiança e próxima ação. Em pedido simples, a própria fonte recomenda prosa curta em vez de expor campos vazios. A tabela de papéis existe para composição que realmente exige vários recursos.

Se uma função pública basta para formatar valores, a rota pode ser `HELPER_ROUTE` e a cobertura total para aquele escopo. A recomendação deve nomear símbolo e fonte verificados, explicar entrada e saída e indicar como continuar. Se a pergunta inclui capacidade ainda não coberta, marque cobertura parcial sem alterar artificialmente a rota. `BRIEFING_FIRST` cabe quando uma informação ausente muda a escolha; `ACCESS_BLOCKED` cabe quando não há fonte acessível para verificá-la.

O campo de confiança alta, média ou baixa se refere à adequação sustentada pelas fontes, não a porcentagem estatística. Base no Git e disponibilidade no workspace são evidências separadas. O template manda declarar ausência de execução analítica e não salvar arquivo automaticamente; menção `@skill` numa próxima ação não aciona a skill. Nenhuma recomendação nasce pronta de placeholders.

<!-- editorial:exclude:start -->
Fonte: [recomendacao.md](../../skills/hub-ml-concierge/templates/recomendacao.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0179](#doc-0179) · [Próximo: D0181](#doc-0181) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0181"></a>
<a id="doc-0181"></a>
### D0181 — Registro da busca do Concierge

O modelo de registro permite ao Concierge deixar uma trilha verificável de como encontrou uma opção no catálogo do Hub. Seu consumidor é a pessoa que pediu uma recomendação ou a equipe que precisa conferir o alcance daquela busca. O formulário pede raiz consultada, versão, superfície, famílias consideradas, consultas realizadas e candidatos inspecionados, incluindo áreas de domínio quando pertinentes. Assim, uma recomendação pode ser reproduzida a partir dos nomes e caminhos observados, sem expor raciocínio privado do assistente.

Por exemplo, numa busca por análise exploratória de dados, o registro pode listar os termos usados, a skill escolhida, alternativas descartadas e o motivo observável do descarte. Também anota conflitos, limitações de acesso, cobertura por família e ações que não foram executadas. Se a pesquisa examinou só os primeiros resultados, o texto deve delimitar esse recorte; não pode afirmar varredura completa. A persistência do registro depende de pedido ou fluxo autorizado, e registrar uma busca não certifica a adequação técnica da skill nem prova que ela executou alguma análise.

<!-- editorial:exclude:start -->
Fonte: [registro_busca.md](../../skills/hub-ml-concierge/templates/registro_busca.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0180](#doc-0180) · [Próximo: D0182](#doc-0182) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0182"></a>
<a id="doc-0182"></a>
### D0182 — Plano de testes do Concierge

O README direciona mantenedores aos instrumentos de teste e usuários ao guia da skill. A matriz contém expectativas, não resultados; o roteiro histórico separa dois tipos de evidência. O validador estático verifica arquivos, metadados, rotas, links, sintaxe e a matriz de casos; isso detecta defeitos estruturais sem iniciar Spark nem acessar dados. Já os casos conversacionais examinam o comportamento do assistente diante de pedidos reais formulados em chats novos. Um pacote íntegro pode, portanto, falhar na escolha da skill certa, e o teste estrutural sozinho não resolve essa dúvida.

A matriz prevê casos positivos, negativos, menções incidentais e situações de borda. Num negativo, por exemplo, um pedido que já pertence claramente a uma skill especialista não deve ser capturado pelo Concierge. Para testar encaminhamento, o avaliador observa separadamente se a skill de destino foi carregada e o que a resposta afirmou; uma frase dizendo que houve encaminhamento não é prova de carregamento. Os comandos do runbook pertencem à raiz do checkout de autoria; `tools/tests` não é ferramenta distribuída do produto. O documento não oferece homologação, nem valida permissões, execução em Databricks ou resultado analítico: esses efeitos exigem verificações próprias.

<!-- editorial:exclude:start -->
Fonte: [tests/README.md](../../skills/hub-ml-concierge/tests/README.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0181](#doc-0181) · [Próximo: D0183](#doc-0183) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0183"></a>
<a id="doc-0183"></a>
### D0183 — Resultados locais dos testes do Concierge

O arquivo de resultados encaminha à fotografia de 12/09/2026 da verificação local do Concierge, útil para quem audita uma alteração e precisa saber exatamente qual base foi testada. O registro histórico preserva o commit, o ambiente Python e os resultados do validador estático, da regressão e da integração canônica. Na execução histórica ali descrita, esses grupos passaram sem falhas ou testes ignorados; a afirmação vale para aquela base e aquele ambiente, não para uma versão posterior automaticamente.

O mesmo registro identifica 26 expectativas conversacionais então pendentes. Elas incluem pedidos positivos, negativos, menções e bordas, cuja avaliação exige conversas novas e observação do carregamento efetivo das skills. Por exemplo, um teste local de link e metadado pode passar enquanto o assistente ainda escolhe um especialista inadequado diante de uma pergunta ambígua. A utilidade do arquivo é mostrar o que já foi medido e a lacuna restante, sem converter contagens históricas de outras skills em certificado do Concierge. Não houve nessa evidência publicação, chamadas Databricks, uso de credenciais ou validação de workspace.

<!-- editorial:exclude:start -->
Fonte: [tests/RESULTADOS.md](../../skills/hub-ml-concierge/tests/RESULTADOS.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0182](#doc-0182) · [Próximo: D0184](#doc-0184) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0184"></a>
<a id="doc-0184"></a>
### D0184 — Contrato da skill de criar objeto

A skill orienta a criação ou conversão de snippet, script, prompt, README, notebook e skill no repositório. Seu consumidor é o autor que precisa escolher tipo, template e destino antes de escrever. O preflight, verificação prévia sem escrita, exige campos e caminhos fechados. Para criação de objetos cobertos, a validação de nível L3 produz Receipt, um comprovante verificável; o nível L2 do preflight trata somente da checagem anterior. A policy vigente põe a skill em L3 com rollout audit, isto é, medição sem veto automático do rollout, embora um validador possa bloquear sua própria operação.

O piloto de escrita é mais estreito que a lista de tipos: o runner canônico gera bytes em memória e só aplica create/readme/agregador, mediante confirmação externa exata, diretório de evidências separado e destino novo em diretório real existente. Ele rejeita sobrescrita, conversão e atalhos de sistema de arquivos; uma falha após escrita parcial não autoriza repetir automaticamente. O SKILL agora registra L3/audit de forma coerente com a policy; o preflight L2 permanece uma etapa distinta e não amplia a superfície de escrita. Exemplo: criar um README agregador novo exige preflight, validação e confirmação, sem supor autorização para editar notebook existente.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-criar-objeto/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0183](#doc-0183) · [Próximo: D0185](#doc-0185) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0185"></a>
<a id="doc-0185"></a>
### D0185 — Checklist de objeto novo

O checklist ajuda o autor e o revisor a distinguir provas que outra pessoa consegue repetir de decisões que dependem de julgamento. Nas pré-condições e nos artefatos verificáveis, enumera estrutura do arquivo, caminhos, links, metadados, validação e, quando couber, saídas de notebook e testes de encaminhamento. Cada item deve apontar para um artefato ou comando verificável. Na seção de juízo, o autor fundamenta decisões, limites calibráveis e literalidade do conteúdo; sua declaração orienta a revisão, mas não substitui prova independente.

Imagine um novo prompt: o revisor pode conferir localização, formato e referências; ainda precisa avaliar se o pedido descrito produz o comportamento esperado. Para um notebook, uma checagem de estrutura não prova que as células executam com dados reais nem que o encaminhamento conversacional funciona. Os caminhos de ferramenta citados pertencem ao repositório, não ao workspace de dados. Portanto, o checklist organiza a entrega e revela pendências, mas marcar suas caixas não concede aprovação de produto, permissão de escrita ou execução em ambiente corporativo.

<!-- editorial:exclude:start -->
Fonte: [checklist-objeto-novo.md](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0184](#doc-0184) · [Próximo: D0186](#doc-0186) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0186"></a>
<a id="doc-0186"></a>
### D0186 — Contrato de análise exploratória entre fontes

A skill cross-EDA organiza a análise exploratória de dados de várias fontes antes de propor integração para aprendizado de máquina. Seu consumidor é quem decide se tabelas e achados anteriores podem sustentar uma mesma unidade analítica. Ela exige fonte âncora, entidade, instante de observação, alvo, horizonte, chaves, cardinalidade das junções e cobertura; depois compara sinal incremental, qualidade e restrições de uso. Uma tabela com muitas colunas interessantes pode ser inviável se não representar a mesma entidade no mesmo tempo.

Por exemplo, ao juntar clientes e eventos, o autor deve mostrar se havia uma linha por cliente no instante permitido, quantos clientes receberam eventos válidos e se alguma informação surgiu após o desfecho. Usar dado futuro seria vazamento de informação e veta a prontidão, mesmo com boa pontuação média. O índice de estabilidade populacional, se calculado, compara distribuições em faixas fixas de referência; não identifica sozinho a causa da mudança. O scorecard propõe GO (prosseguir), COND (prosseguir sob condições) ou NO-GO (não prosseguir), com evidências e vetos. A policy mantém L0/audit. Existem rotas distintas de contexto, diagnóstico Spark e junção temporal sintética com conferência final. Ler recomendações não as executa nem promove autorização; consulte seus contratos antes de escolher.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-cross-eda-ml/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0185](#doc-0185) · [Próximo: D0187](#doc-0187) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0187"></a>
<a id="doc-0187"></a>
### D0187 — Contexto, diagnóstico e junção temporal da cross-EDA

O README dos scripts distingue três rotas para a análise exploratória entre fontes. Seu consumidor é quem prepara contexto, mede cobertura ou precisa selecionar a versão temporal adequada. O preflight, conferência prévia, recebe uma entrada fechada e verifica declarações; sozinho não usa Spark nem comprova cobertura. O diagnóstico seguinte executa o helper em duas fontes sintéticas estáticas, sem produzir a junção de negócio.

A receita fornece três entidades na âncora e duas correspondências esperadas, guardadas fora do resultado. O verificador compara pedido, dados, identificador da tentativa e diagnóstico com esse oráculo independente. O resultado não prova prontidão para aprendizado de máquina. O schema de contexto também não vale como contrato universal das outras rotas.

A junção temporal sintética tem perfil próprio: sessão Spark em UTC, disponibilidade conferida, fronteira inclusiva e janela positiva. Atraso variável e bitemporalidade ficam fora. Depois de executar, é necessário finalizar e reverificar com entradas externas preservadas; ausência dessa etapa mantém a conclusão pendente. Mantenedores devem atualizar receitas e contratos juntos. Esses componentes não promovem a policy da skill, que permanece L0/audit, e não autorizam publicar ou tratar o ensaio como homologação do ambiente.

<!-- editorial:exclude:start -->
Fonte: [scripts/README.md](../../skills/hub-ml-cross-eda-ml/scripts/README.md). Detalhe: [MT18](MT-parte-iv.md#mt18).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0186](#doc-0186) · [Próximo: D0188](#doc-0188) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0188"></a>
<a id="doc-0188"></a>
### D0188 — Matriz de cobertura entre fontes

A matriz registra que fração das entidades da fonte âncora aparece em cada fonte secundária e em suas combinações. Seu consumidor é quem avalia o alcance de uma junção antes de interpretar novos atributos. O template pede denominador explícito, perfis de cobertos e não cobertos, chaves e estratégia de junção. Assim, “80% de cobertura” significa 80% da população âncora definida, não 80% de todos os registros disponíveis.

Num exemplo ilustrativo com clientes como âncora, a matriz separaria clientes presentes somente na fonte A, somente na B, em ambas ou em nenhuma. Ela também compararia diferenças de qualidade e período para revelar se os ausentes formam grupo relevante. O plano de validação é pseudocódigo, sem execução como célula. Use a rota canônica aplicável; cache é opcional, condicionado ao ambiente, custo e liberação prevista. A presença da chave não assegura que a linha secundária respeite o mesmo grão e tempo, nem que exista sinal incremental para o modelo. Padrões de ausência podem ser descritos; o mecanismo causal da ausência não decorre apenas dessa contagem.

<!-- editorial:exclude:start -->
Fonte: [coverage_matrix.md](../../skills/hub-ml-cross-eda-ml/templates/coverage_matrix.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0187](#doc-0187) · [Próximo: D0189](#doc-0189) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0189"></a>
<a id="doc-0189"></a>
### D0189 — Inventário das análises exploratórias

O inventário reúne o que cada análise exploratória de dados, ou EDA, já sabe sobre uma fonte antes de misturar tabelas. Seu consumidor é o analista que precisa comparar evidências de notebooks e bases produzidos em momentos diferentes. O template organiza nome da tabela e do notebook, grão da linha, volume, período, chave, qualidade, achados, limitações e relevância esperada. Grão significa o que uma linha representa: cliente, transação ou dia, por exemplo.

Imagine três EDAs: clientes com uma linha por pessoa, compras com várias linhas por pessoa e atendimento com uma linha por chamado. O inventário torna visível que uma junção direta pode multiplicar linhas, mesmo que todas usem a mesma chave de cliente. O autor registra também se a data e o filtro de cada análise são comparáveis, e quais achados continuam hipóteses. O quadro do template tem colunas A, B e C, mas pode ser adaptado verticalmente para mais fontes. Preencher o inventário não confirma compatibilidade temporal, segurança de junção nem benefício preditivo; ele prepara as perguntas que as próximas verificações devem responder.

<!-- editorial:exclude:start -->
Fonte: [inventario_edas.md](../../skills/hub-ml-cross-eda-ml/templates/inventario_edas.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0188](#doc-0188) · [Próximo: D0190](#doc-0190) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0190"></a>
<a id="doc-0190"></a>
### D0190 — Viabilidade da junção

O formulário de viabilidade de join, a junção entre tabelas por chaves, orienta quem pretende combinar fontes sem mudar inadvertidamente a unidade de análise. Ele compara formato e nulidade das chaves, cardinalidade, sobreposição, registros órfãos, risco de multiplicação e checagens após a junção. Cardinalidade 1:N indica várias linhas secundárias para uma entidade âncora; M:N indica multiplicidade nos dois lados. Se a pergunta pede uma linha por cliente, agregar compras por cliente pode ser adequado, desde que a agregação respeite tempo e significado.

O índice de Jaccard mede tamanho da interseção das chaves dividido pelo tamanho da união; um valor baixo sinaliza pouco encontro, mas valor alto não garante join seguro. Num exemplo ilustrativo, duas tabelas podem compartilhar quase todos os clientes e ainda duplicar cada cliente por dez eventos. Por isso, o analista deve comparar contagem antes e depois, órfãos, chaves repetidas e período válido. Os critérios dependem do estudo; igualdade de contagens pode esconder perdas e duplicações, e `1 − coverage` não mede toda nulidade de atributos. Uma junção tecnicamente executável também pode ser inadequada se usar dado futuro ou autorização ausente.

<!-- editorial:exclude:start -->
Fonte: [join_feasibility.md](../../skills/hub-ml-cross-eda-ml/templates/join_feasibility.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0189](#doc-0189) · [Próximo: D0191](#doc-0191) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0191"></a>
<a id="doc-0191"></a>
### D0191 — Estrutura do notebook cross-EDA

O template de notebook organiza a análise exploratória de dados entre fontes em uma sequência auditável de células. Seu consumidor é quem constrói ou revisa a investigação: primeiro inventário e entidade, depois tempo, chaves, junção, cobertura, qualidade, sinal e decisão. As variantes compacta, padrão e expandida ajustam a extensão ao número de fontes e à profundidade do problema; os trechos de código são moldes com campos a preencher, não resultados executados.

Num estudo ilustrativo com clientes e compras, uma célula descreveria a linha âncora e o instante de observação, outra testaria multiplicidade da chave, e outra compararia cobertura por grupo. O resumo final precisaria relacionar evidência a riscos e encaminhamento, inclusive pontos abertos. O radar opcional usa as sete dimensões do scorecard, escala de zero a quatro e vetos explícitos. Contexto L2 não prova leitura ou prontidão; perfis diagnósticos/PIT exigem Receipt, Postflight e oráculos independentes. Construir as células não torna a junção correta nem prova ganho para aprendizado de máquina. A execução, os filtros e as conclusões dependem dos dados reais e das permissões vigentes.

<!-- editorial:exclude:start -->
Fonte: [notebook_output_cross_eda.md](../../skills/hub-ml-cross-eda-ml/templates/notebook_output_cross_eda.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0190](#doc-0190) · [Próximo: D0192](#doc-0192) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0192"></a>
<a id="doc-0192"></a>
### D0192 — Scorecard de prontidão

O scorecard é um quadro de decisão para quem avalia se a integração de fontes pode avançar ao aprendizado de máquina. O template usa sete dimensões, notas de zero a quatro, pesos, evidência, bloqueador, responsável, ação e critério de aceite. A nota ajuda a localizar trabalho pendente; sua média não decide sozinha. Uma chave inválida, informação posterior ao instante de previsão, alvo ambíguo, população inadequada, uso não autorizado ou junção que altere o grão podem vetar a prontidão.

Por exemplo, boa cobertura e qualidade não compensam um atributo calculado depois do desfecho. O avaliador deve registrar o veto, indicar dono para corrigir a fonte temporal e dizer qual teste demonstrará a correção. GO significa prosseguir sob evidência suficiente; CONDICIONAL, prosseguir somente após condições explícitas; NO-GO, interromper até resolver impedimentos. Esses rótulos dependem de julgamento fundamentado e dos critérios aprovados para o caso, não de um limiar universal de média. Preencher placeholders sem medições não constitui score observado nem autorização operacional.

<!-- editorial:exclude:start -->
Fonte: [readiness_scorecard.md](../../skills/hub-ml-cross-eda-ml/templates/readiness_scorecard.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0191](#doc-0191) · [Próximo: D0193](#doc-0193) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0193"></a>
<a id="doc-0193"></a>
### D0193 — Relatório executivo cross-EDA

O relatório executivo traduz a análise exploratória entre fontes em uma decisão que gestores e equipes de engenharia possam verificar. Ele pede fonte âncora, entidade, alvo e horizonte, cobertura, sobreposição de chaves, viabilidade da junção, oportunidades, riscos e próximos passos. O objetivo não é empilhar números: cada recomendação deve apontar para uma medição e para o limite que ela não resolve. Um alvo ou horizonte ainda indefinido precisa aparecer como pendência, nunca como prontidão presumida.

Num exemplo ilustrativo, o texto poderia informar que a fonte de atendimento cobre parte da base de clientes e propor medir se o grupo descoberto altera a avaliação fora do período de desenvolvimento. Antes disso, não se afirma ganho preditivo. O relatório deriva do scorecard vigente: sete dimensões de zero a quatro, pesos e evidências iguais, com vetos acima da média. Sem dados ou execução suficientes, registra NÃO AVALIADO; GO técnico não autoriza treino, promoção ou execução do handoff. Jaccard, interseção dividida pela união das chaves, cobertura e conclusão de negócio também não substituem teste de temporalidade, autorização e efeito após junção.

<!-- editorial:exclude:start -->
Fonte: [relatorio_executivo_cross_eda.md](../../skills/hub-ml-cross-eda-ml/templates/relatorio_executivo_cross_eda.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0192](#doc-0192) · [Próximo: D0194](#doc-0194) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0194"></a>
<a id="doc-0194"></a>
### D0194 — Skill de análise exploratória profissional

A skill de análise exploratória de dados, ou EDA, orienta a investigação de uma fonte única, com perguntas, qualidade, distribuições, relações, riscos e entrega para a etapa seguinte. Seu consumidor é o analista que precisa produzir achados reproduzíveis sem confundir um notebook gerado com uma análise concluída. Na policy vigente, esta skill está em L4 enforce: a rota canônica passa por `run_enforced.py`, que chama o runner L3 e emite Receipt, um comprovante de execução. Depois, o postflight verifica evidências; só um PASS permite registrar `COMPLETED`.

Um exemplo ilustrativo seria analisar uma tabela de clientes: registrar origem, unidade da linha e filtros; medir ausência e perfis; e entregar achados, riscos de interpretação e perguntas abertas. Em Spark, processamento tabular distribuído e avaliado sob demanda, agregações limitadas evitam trazer todas as linhas ao computador local; cache precisa ser avaliado conforme o ambiente. Se a execução canônica for bloqueada, não há atalho manual para declarar conclusão. O texto da skill descreve método e exigências, mas esta ficha não executou EDA nem apresenta achados sobre dados reais.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-eda-profissional/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0193](#doc-0193) · [Próximo: D0195](#doc-0195) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0195"></a>
<a id="doc-0195"></a>
### D0195 — Estilo visual da análise exploratória

Este template orienta a apresentação da análise exploratória de dados (EDA) no notebook. Seu consumidor é quem organiza gráficos, tabelas e interpretação pós-código para que o leitor encontre escopo, evidência e próximo passo. Ele propõe hierarquia de títulos, índice, anotações de fonte e denominador, cartões com poucos indicadores e separação entre resultado observado, interpretação técnica e implicação de negócio. O tema visual é recebido como `ResolvedTheme`, configuração já resolvida pelo sistema compartilhado; o template não define uma paleta própria.

Por exemplo, ao mostrar nulos por coluna, o autor pode exibir contagem e percentual observados, identificar o recorte e só então discutir o impacto para modelagem. Se não houver tema selecionado, usa a API legada, isto é, a interface de programação existente; com tema válido, usa a rota `_resolvido` documentada pelo componente. A troca de tipografia ou cor não altera filtro, amostra, intervalos de agrupamento, métrica ou conclusão. Gráficos SHAP, explicações por contribuição de variáveis, produzidos por Matplotlib não herdam automaticamente o tema. Indicadores e emojis do modelo são convenções de apresentação, nunca valores inventados ou aprovação analítica.

<!-- editorial:exclude:start -->
Fonte: [estilo_visual_eda.md](../../skills/hub-ml-eda-profissional/templates/estilo_visual_eda.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0194](#doc-0194) · [Próximo: D0196](#doc-0196) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0196"></a>
<a id="doc-0196"></a>
### D0196 — Matriz de gráficos da análise exploratória

A matriz ajuda o analista a escolher visualizações de análise exploratória de dados (EDA) pela pergunta, pelo tipo das variáveis e pelo volume. Seu mecanismo associa, por exemplo, distribuição numérica a histograma ou percentis; categorias a frequências e barras; tempo a linhas com janela explícita; e relações entre duas variáveis a dispersão, tabela cruzada ou agregados. O consumidor deve preservar unidade, denominador e tamanho da amostra para que uma figura não esconda mudança de população.

Imagine milhões de transações por dia. Primeiro agregue em Spark por mês e segmento; depois envie apenas o resultado limitado ao gráfico. Para uma inspeção rápida, visualização nativa pode bastar; para um relatório interativo, Plotly pode servir. Se a amostra for necessária, registre semente e regra de seleção. Top N categorias requer uma cauda “outros” identificada, e um gráfico de correlação mostra associação, não causa. A matriz é um guia de seleção, não prova que a biblioteca esteja instalada no runtime, que o gráfico foi produzido ou que o achado seja válido. Verifique disponibilidade e custo no ambiente concreto.

<!-- editorial:exclude:start -->
Fonte: [matriz_graficos_eda.md](../../skills/hub-ml-eda-profissional/templates/matriz_graficos_eda.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0195](#doc-0195) · [Próximo: D0197](#doc-0197) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0197"></a>
<a id="doc-0197"></a>
### D0197 — Relatório executivo da análise exploratória

Este template transforma uma análise exploratória de dados (EDA) documentada em relatório legível para decisão. O consumidor é o responsável por apresentar escopo, qualidade, grão, padrões, anomalias e implicações a alguém que talvez não abra o notebook. A abertura exige tabela, período, volume, data, notebook fonte e granularidade, isto é, o que representa uma linha. Depois separa achados de recomendações, com anexo técnico para estatísticas e gráficos detalhados. Essa estrutura permite rastrear uma afirmação executiva até o recorte que a sustenta.

Em uma tabela de clientes, por exemplo, “renda ausente” deve vir acompanhado de contagem ou percentual, período e regra de seleção antes de virar recomendação de tratamento. A seção de modelagem pode registrar variáveis candidatas, riscos de vazamento de informação do futuro (*leakage*) e desbalanceamento, sem aprovar automaticamente uma feature. Os campos de qualidade exigem critérios e medições; sem eles, o resultado permanece não classificado. O relatório não substitui Receipt, Postflight ou conclusão autorizada reverificada. O relatório não substitui verificação de chave, fonte, filtro ou código; uma anomalia observada tampouco autoriza atribuir causa sem investigação adicional.

<!-- editorial:exclude:start -->
Fonte: [relatorio_executivo_eda.md](../../skills/hub-ml-eda-profissional/templates/relatorio_executivo_eda.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0196](#doc-0196) · [Próximo: D0198](#doc-0198) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0198"></a>
<a id="doc-0198"></a>
### D0198 — Roteiro por aplicabilidade da análise exploratória

O roteiro é um checklist por aplicabilidade para análise exploratória de dados (EDA), consumido por quem constrói ou revisa o notebook. Começa com objetivo, fonte, unidade da linha, período, premissas e governança; segue por inventário de schema e volume, chaves, duplicidades, nulos, distribuições, relações e visualizações; termina com recomendações técnicas e relatório executivo. A ordem importa: interpretar uma taxa por cliente antes de confirmar se há uma linha por cliente pode transformar duplicidade de join em conclusão de negócio.

Num pedido sobre transações, o autor primeiro define se a unidade é transação ou cliente, mede volume e possíveis chaves, e só então compara distribuição de valores e segmentos. Para gráficos de grande volume, o checklist pede agregação em Spark antes de trazer dados ao processo local. Reaproveite evidência da mesma execução e recorte; não repita contagens por ritual. Resumos adicionais dependem de necessidade, suporte, custo e autorização. Marcar uma caixa não torna resultado correto: cada medida precisa de saída observada, recorte e interpretação. A conclusão depende da rota de execução e do postflight, a verificação final, vigentes da skill, não apenas do preenchimento deste roteiro.

<!-- editorial:exclude:start -->
Fonte: [roteiro_eda.md](../../skills/hub-ml-eda-profissional/templates/roteiro_eda.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0197](#doc-0197) · [Próximo: D0199](#doc-0199) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0199"></a>
<a id="doc-0199"></a>
### D0199 — Skill de explicabilidade de modelos

A skill orienta explicar um modelo já treinado, globalmente ou para casos individuais. Seu consumidor é quem precisa relatar quais variáveis influenciaram previsões sem chamar influência de causa. Antes de calcular, fixa versão do modelo, classe, população, período, pré-processamento e escala da saída: probabilidade, margem, log-odds (logaritmo da razão entre probabilidades do evento e do não evento) ou valor previsto. SHAP, método que atribui contribuições de variáveis em relação a um valor base, é uma opção; importância por permutação, coeficientes e curvas de efeito têm pressupostos diferentes.

Por exemplo, para explicar risco de abandono, use amostra de validação ou teste representativa, registre *background* de referência, método e semente, e compare explicações globais com casos locais típicos, fronteiriços e errados. Uma contribuição SHAP em log-odds não vira contribuição aditiva em pontos de probabilidade após conversão. O relatório executivo deve proteger dados pessoais e declarar limites. Na policy vigente a skill está em L0, orientação textual, com L3 apenas como alvo; o perfil `LINEAR_REGRESSION_SYNTHETIC_V1` executa regressão linear sintética com referência de uma linha e oráculo externo. Seu comprovante não promove a policy nem substitui verificação dos valores. A explicação descreve comportamento do modelo, não efeito causal nem validade do próprio modelo.

<!-- editorial:exclude:start -->
Fonte: [SKILL.md](../../skills/hub-ml-explainability/SKILL.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0198](#doc-0198) · [Próximo: D0200](#doc-0200) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mt-mod-d0200"></a>
<a id="doc-0200"></a>
### D0200 — Relatório executivo de explicabilidade

O template executivo traduz uma análise de explicabilidade para gestores em linguagem executiva. Seu consumidor precisa identificar modelo, população, período, métrica de desempenho, fatores principais, exemplos locais, limitações e ações de investigação. A tabela de drivers pede direção e significado de negócio, enquanto a seção de confiança delimita onde a leitura se aplica. Esses campos só devem ser preenchidos depois de conferir a análise técnica e o mesmo conjunto em que o modelo foi avaliado.

Por exemplo, se um fator aparece no topo de uma ordenação SHAP — método que atribui contribuições relativas à saída do modelo — informe como o ranking foi calculado. Uma “importância de X%” só faz sentido se o denominador e a normalização forem definidos; a contribuição SHAP bruta não é percentual de decisão. AUC, área sob a curva ROC, que compara sensibilidade e taxa de falsos positivos, tampouco é porcentagem de casos acertados. O texto atual separa influência sobre a previsão de determinação do alvo real; hipóteses de intervenção exigem investigação causal, sem recomendação automática ou autorização para agir. Todos os números e perfis do arquivo são placeholders, não resultados medidos; casos individuais exigem cuidado com dados pessoais.

<!-- editorial:exclude:start -->
Fonte: [relatorio_executivo_explainability.md](../../skills/hub-ml-explainability/templates/relatorio_executivo_explainability.md).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: D0199](#doc-0199) · [Próximo: D0201](MT-atlas-05.md#doc-0201) · [Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
