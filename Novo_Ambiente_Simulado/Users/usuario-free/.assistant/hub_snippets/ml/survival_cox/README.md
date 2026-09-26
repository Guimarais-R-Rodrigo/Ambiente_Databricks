# `survival_cox` — associações de risco relativo sob o pressuposto de riscos proporcionais

<!-- readme-objeto: 1.0.0 -->

O modelo de Cox relaciona covariáveis ao risco instantâneo de um evento sem exigir uma forma paramétrica para o risco basal. Este helper ajusta `CoxPHFitter`, resume métricas in-sample e oferece um teste de proporcionalidade. Ele ajuda a estimar **associações condicionais de hazard**; não transforma coeficientes em efeitos causais nem garante previsão individual.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Wrapper local do modelo de riscos proporcionais de Cox do `lifelines`. |
| Para que serve? | Relacionar covariáveis ao tempo até evento com censura e testar proporcionalidade. |
| Use quando... | Duração/evento estiverem bem definidos e riscos proporcionais forem plausíveis/avaliados. |
| Evite quando... | Covariáveis variam no tempo sem modelagem apropriada, PH é inadequado ou a pergunta é causal sem desenho causal. |
| Precisa de... | pandas, NumPy, `lifelines`; MLflow se `log_mlflow=True`. |
| Entrega... | `CoxPHFitter`, métricas in-sample e, separadamente, DataFrame do teste PH. |

Consulte a [implementação](survival_cox.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_survival_cox.py). O notebook instala `lifelines` e usa `log_mlflow=False`.

## 1. O que é?

No Cox PH, o hazard de um indivíduo é o hazard basal multiplicado por `exp(xβ)`. Para uma covariável, `exp(coef)` é o hazard ratio associado a uma unidade adicional, mantendo as demais covariáveis do modelo fixas.

`train_cox_ph` usa `CoxPHFitter` com penalização configurável. `validate_proportionality` aplica `proportional_hazard_test(..., time_transform="rank")` às mesmas covariáveis ajustadas.

## 2. Que problema este recurso resolve?

Regressão comum não representa adequadamente observações censuradas. O Cox permite estudar tempo até evento e covariáveis sem descartar quem ainda não apresentou o evento ao fim da observação.

O helper também torna explícito um pressuposto central: o efeito relativo das covariáveis é tratado como proporcional ao longo do tempo no modelo ajustado.

## 3. Quando faz sentido usar?

Use quando houver tempo até evento/censura, indicador binário de evento e covariáveis medidas de forma compatível com o início/seguimento do estudo. É especialmente útil para associações ajustadas em churn, sobrevivência de contratos e outros eventos com censura.

A penalização pode ajudar estabilidade com covariáveis correlacionadas ou muitas variáveis, mas não corrige desenho ruim ou leakage.

## 4. Quando não usar?

Não use hazard ratio como “percentual de mudança na probabilidade final”. Hazard é taxa instantânea condicional, e sua relação com risco acumulado depende do tempo e do hazard basal.

Não use coeficientes como efeitos causais apenas porque outras variáveis estão no modelo. Confundimento residual, seleção e temporalidade continuam relevantes.

## 5. Como funciona, intuitivamente?

A função seleciona duração, evento e features, remove linhas com qualquer nulo e ajusta `CoxPHFitter(penalizer=..., l1_ratio=...)`. Depois lê C-index, log-likelihood, AIC parcial, número de observações e eventos.

O diagnóstico PH usa a matriz completa das mesmas colunas após `dropna()` e devolve a tabela do teste com uma coluna local `violates_at_0_05`.

## 6. Exemplo de situação

Você acompanha contratos até cancelamento ou censura e quer saber se uso do limite e renda estão associados ao hazard de cancelamento. O Cox estima razões de hazard condicionais.

Se `exp(coef)=1,5`, a interpretação local é hazard estimado 1,5 vez maior por unidade da covariável, dadas as demais variáveis — não “50% mais clientes cancelarão”.

## 7. O que você precisa antes de usar?

`feature_cols` deve ser lista não vazia sem duplicatas. Duração, evento e features precisam existir. Após remoção complete-case, deve restar ao menos uma linha; durações precisam ser positivas e o evento deve ser binário com pelo menos um evento observado.

O helper **remove silenciosamente linhas com nulos** nas colunas usadas. Compare `n_observations` com a base original e avalie se complete-case é aceitável.

## 8. O que este recurso entrega?

`train_cox_ph` retorna `(model, metrics)`. `metrics` contém `c_index`, `log_likelihood`, `aic` (na realidade `AIC_partial_` do lifelines), `n_observations` e `n_events`.

Essas métricas vêm do modelo ajustado na própria amostra; o C-index retornado não é validação externa. `validate_proportionality` devolve DataFrame com estatística, p-valor e flag `violates_at_0_05` por feature.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.survival_cox import train_cox_ph, validate_proportionality

model, metrics = train_cox_ph(
    df,
    duration_col="duracao",
    event_col="evento",
    feature_cols=features,
    log_mlflow=False,
)
ph = validate_proportionality(model, df, "duracao", "evento")
```

O teste PH é uma chamada separada; treinar o modelo não o executa automaticamente.

## 10. Decisões e configurações que mais importam

`penalizer` controla força de regularização; `l1_ratio=0` corresponde ao componente L2 no contrato do lifelines, enquanto valores maiores introduzem L1. Alterar penalização muda coeficientes e inferência.

A unidade de cada covariável muda a leitura do hazard ratio. Uma variável padronizada tem interpretação por desvio-padrão; uma variável em reais ou anos tem outra escala.

## 11. Limitações, riscos e armadilhas

A implementação imprime como “significativas” as features com `p<0,05` **sem correção por multiplicidade**. Isso é uma convenção de exibição local, não prova substantiva nem regra universal.

`violates_at_0_05=False` significa que o teste não rejeitou PH naquele diagnóstico; não prova que a proporcionalidade seja verdadeira. Avaliação gráfica e conhecimento do processo podem continuar necessários.

O logging MLflow, quando solicitado, acontece depois do ajuste; se MLflow não estiver disponível, o helper pode gastar o custo de treino antes de lançar `ImportError`.

O AIC retornado é `AIC_partial_`, não um AIC genérico comparável indiscriminadamente a modelos de likelihood diferente.

## 12. Quais são as alternativas?

[kaplan_meier](../kaplan_meier/README.md) descreve curvas não ajustadas e compara grupos. Modelos com covariáveis dependentes do tempo, AFT ou modelos flexíveis de sobrevivência podem ser necessários quando o contrato do Cox PH é inadequado.

Para previsão individual, valide discriminação/calibração temporal fora da amostra; o wrapper atual não implementa esse pipeline.

## 13. Como saber se o resultado faz sentido?

Compare eventos e observações efetivamente usadas; examine hazard ratios, intervalos e sinais; execute o teste PH e inspecione padrões ao longo do tempo. Faça validação temporal ou cross-validation apropriada se a meta for previsão.

Confirme que covariáveis estavam disponíveis no instante correto e não foram medidas após o começo do acompanhamento de forma incompatível com um Cox de covariáveis fixas.

## 14. Arquivos relacionados e próximos passos

A [implementação](survival_cox.py) define treino e teste PH; a [fachada](__init__.py) exporta `SEED`, `train_cox_ph` e `validate_proportionality`; o [notebook](exemplo_survival_cox.py) usa uma base sintética com efeitos constantes.

Depois do ajuste, se a pergunta for preditiva, crie avaliação fora da amostra; se for explicativa/causal, explicite o desenho e as hipóteses adicionais.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. Fontes primárias consultadas em 12/09/2026: documentação `lifelines.CoxPHFitter` e `lifelines.statistics.proportional_hazard_test`, incluindo a forma `h(t|x)=h0(t)exp((x-x̄)'β)`, penalização e o teste com transformação temporal.

Este README não presume causalidade, homologação de modelo, publicação no Databricks nem auditoria independente.