# Achados R07 — score, vintage e sobrevivência

**Base:** `289731c79e8ed43d82b39d61cdc41ba2e69ea717`
**Escopo:** seis objetos R07; sem alteração de implementação/fachada.

Os itens abaixo são achados de documentação/caracterização. Registrar um comportamento não significa aprová-lo como desenho desejável.

## 1. `kaplan_meier`

1. A figura Plotly usa a censura no ajuste do `KaplanMeierFitter`, mas **não desenha marcadores de censura**. O notebook histórico afirma que as marcas aparecem; essa frase precisa ser corrigida em Markdown.
2. A legenda inclui a mediana. No `lifelines`, a mediana pode ser infinita quando a curva não cruza 0,5 no horizonte observado.
3. Com dois grupos, `log_rank_test` retorna apenas estatística e p-valor; com mais de dois, o formato muda para teste global + pares com Holm.
4. O helper não valida explicitamente duração positiva, binariedade, missingness ou grupos nulos antes de delegar ao `lifelines`.
5. O log-rank padrão deve ser lido com cautela quando curvas cruzam; p-valor não mede magnitude nem causalidade.

## 2. `score_bands`

1. `higher_score_is_better` **tem default `True`**. O notebook diz que a direção “não tem padrão silencioso de propósito”; isso é falso no contrato atual e será corrigido apenas na prosa.
2. `aprovacao_acum` é, tecnicamente, a cobertura cumulativa da base percorrida da melhor para a pior banda. Não é aprovação efetiva sem cutoff/política.
3. `taxa_default` assume semanticamente `y_true=1` como evento adverso/default, embora a API aceite qualquer target binário.
4. `qcut(..., duplicates="drop")` pode devolver menos bandas que `n_bands`; rótulos precisam ter tamanho igual às bandas efetivas.
5. Os cortes são recalculados em cada base. As bandas não são automaticamente comparáveis entre períodos ou modelos.

## 3. `scorecard_builder`

1. O helper cria **tabela de pontos**, não função completa de scoring: não aplica binning/faixas a novas observações.
2. A saída de `woe_iv_calculator` é Spark e usa a coluna original da feature; é necessário `toPandas()` controlado + rename para `faixa` antes da entrada no builder.
3. Os pontos são arredondados individualmente para zero casas; a soma discretizada pode divergir levemente da transformação contínua do logit.
4. O intercepto é dividido igualmente entre features por convenção de apresentação; essa alocação não tem interpretação causal.
5. `event_is_bad` altera a direção do score. `base_score`, `base_odds` e `pdo` são parâmetros de escala, não valores estimados pelo helper.
6. O bloco histórico de output do notebook omite as linhas de `tempo_woe` embora o código imprima toda a tabela; o output será preservado como evidência histórica, e a prosa passará a identificá-lo como trecho abreviado.

## 4. `survival_cox`

1. `c_index`, log-likelihood e `AIC_partial_` são lidos do **modelo ajustado na própria amostra**; não constituem validação externa.
2. O campo chamado `aic` no dicionário é especificamente `model.AIC_partial_`.
3. A implementação remove complete cases com `dropna()`; `n_observations` pode ser menor que a base de entrada.
4. O stdout chama de “significativas” features com `p<0,05` sem correção por multiplicidade.
5. `validate_proportionality` com p≥0,05 significa “não rejeitou” naquele diagnóstico, não prova de proporcionalidade.
6. Hazard ratio é associação de hazard condicionada às covariáveis do modelo; não é diferença de probabilidade acumulada nem causalidade automática.
7. Se MLflow estiver ausente e `log_mlflow=True`, o erro ocorre depois do ajuste.

## 5. `vintage_analysis`

1. O helper não preenche snapshots ausentes: `taxa_acumulada` só é publicada quando todos os contratos da safra considerada estão observados naquele MOB.
2. Duplicidades contrato×MOB são colapsadas pelo máximo do evento.
3. Com `target_is_cumulative=False`, a implementação usa `cummax`; com `True`, exige que o target acumulado não diminua.
4. `dt_originacao` e `dt_referencia` continuam obrigatórios mesmo quando `mob_col` já existe.
5. A coorte base é formada pelos contratos que restam após filtros de MOB válido; não há base-mestra externa para recuperar contrato totalmente ausente dos snapshots válidos.
6. `compare_safras` calcula diferença para a média disponível por checkpoint; isso não ajusta composição e não é benchmark causal.
7. O notebook usa `mob * 30 dias` para fabricar `dt_ref`, mas o cálculo de MOB usa a coluna `mob` fornecida nessa chamada. Essa construção de data não deve ser copiada como equivalência geral entre mês e 30 dias.

## 6. `woe_iv_calculator`

1. O helper **não faz binning**. Feature contínua crua vira grupos por valores distintos, o que não é um processo de discretização apropriado por si só.
2. O cálculo realiza ações Spark: agregação+`collect`, `grouped.count()` e `collect` do IV total. “Sem `toPandas`” não significa “sem coleta”.
3. Target inválido/nulo é rejeitado e ambas as classes 0/1 são exigidas.
4. `smoothing` afeta WOE/IV, sobretudo em bins pequenos.
5. `classify_iv` codifica uma régua heurística local. Ela não é norma regulatória universal.
6. IV alto pode ocorrer por leakage, proxy do target, concentração ou bins superajustados; não deve ser celebrado automaticamente.
7. O notebook afirma que IV >0,5 torna leakage a hipótese “mais provável”; essa generalização será suavizada em Markdown.

## Decisão da R07

Nenhum achado acima será corrigido por mudança algorítmica nesta sprint. A R07 é documental: os guias descrevem o contrato real, notebooks recebem apenas correções editoriais/backlinks e uma suíte de caracterização prova os comportamentos observados.
