# `drift_detection` — PSI, KS e CSI com política de classificação explícita

<!-- readme-objeto: 1.0.0 -->

Este objeto diagnostica mudanças entre uma população de referência e uma população atual. Ele calcula evidências de drift, mas **não conclui sozinho que a performance do modelo piorou** e não aplica limiares universais quando nenhuma política é fornecida.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Helper pandas/NumPy/SciPy para PSI, KS, CSI e varredura de features. |
| Para que serve? | Investigar mudança de distribuição entre referência e período atual. |
| Use quando... | Referência, janela atual, tipo das features e política de alerta estão definidos. |
| Evite quando... | Você quer provar degradação de performance ou processar grandes tabelas Spark sem amostragem. |
| Precisa de... | NumPy, pandas e SciPy; dados no driver. |
| Entrega... | Índices escalares ou DataFrame de diagnóstico por feature. |

Consulte a [implementação](drift_detection.py), a [fachada](__init__.py) e o [notebook](exemplo_drift_detection.py).

## 1. O que é?

`calculate_psi` mede mudança numérica usando bins definidos pela referência e bucket explícito de missing. `calculate_ks` executa KS de duas amostras sobre valores finitos. `calculate_csi` aplica a aritmética de estabilidade a categorias. `detect_drift_all_features` organiza essas evidências por coluna.

## 2. Que problema este recurso resolve?

Responde “a distribuição mudou?” com medidas apropriadas a numéricas e categóricas e separa **medição** de **política**. Sem thresholds fornecidos, o status permanece `NOT_CLASSIFIED`.

## 3. Quando faz sentido usar?

Use em monitoramento de features, comparação de safra/janela, diagnóstico de mudança de mix e investigação de incidentes. A referência deve representar o estado contra o qual a mudança é relevante.

## 4. Quando não usar?

Não use drift de entrada como sinônimo de queda de AUC, perda financeira ou necessidade de retreino. Não use p-valor isoladamente como magnitude de drift. Não aplique limiares copiados de outro contexto como se fossem padrão regulatório.

## 5. Como funciona, intuitivamente?

PSI divide a referência por quantis, compara proporções referência×atual e soma termos logarítmicos. KS mede a maior distância entre distribuições acumuladas. CSI compara proporções de categorias, incluindo `__MISSING__`.

Na varredura, numéricas recebem PSI + KS; categóricas recebem CSI armazenado na coluna `psi` por compatibilidade de schema.

## 6. Exemplo de situação

Duas populações têm média quase igual, mas uma ficou bimodal. PSI e KS detectam a mudança de forma. Uma feature categórica cuja distribuição de UFs se tornou uniforme é avaliada por CSI.

## 7. O que você precisa antes de usar?

`__MISSING__` é categoria reservada do CSI. Uma categoria real com esse texto se funde a ausências, podendo ocultar drift. Recuse-a ou remapeie-a com uma convenção sem colisões **igual nas duas bases**, antes de chamar:

```python
for frame in [ref, atual]:
    assert not frame["uf"].dropna().eq("__MISSING__").any()
```

As listas de tipos não são validadas pelo helper como partição do universo: rejeite duplicatas, sobreposição, colunas extras e falta de cobertura. `numeric_cols=[]`/`categorical_cols=[]` acionam inferência por `or`, assim como `None`; não significam “desabilite este ramo”.

Defina `feature_cols`. Se não passar listas de tipos, a função infere numéricas a partir do DataFrame de referência e trata as demais como categóricas.

Para classificar status, `psi_threshold` e `ks_threshold` devem ser fornecidos juntos. Recomenda-se sempre associar severidade a uma política de warning. O código só rejeita `severe_psi_threshold` sem warning; `severe_ks_threshold` isolado é aceito mas ignorado na classificação, ficando `NOT_CLASSIFIED` se houver dados suficientes. `min_non_null` deve ser positivo.

## 8. O que este recurso entrega?

A varredura devolve `feature`, `type`, `psi`, `ks_statistic`, `ks_pvalue`, contagens, missing percentuais e `status`.

Status possíveis incluem `NOT_CLASSIFIED`, `INSUFFICIENT_DATA`, `OK`, `ALERT` e `SEVERE`, conforme dados e política fornecida.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.drift_detection import detect_drift_all_features

relatorio = detect_drift_all_features(
    ref,
    atual,
    feature_cols=["score", "renda", "uf"],
    psi_threshold=0.25,
    ks_threshold=0.10,
)
```

Os valores acima são apenas exemplo de chamada; calibre a política no seu processo.

## 10. Decisões e configurações que mais importam

| Função | Parâmetros de configuração expostos |
|---|---|
| `calculate_psi(reference, current, n_bins=10, eps=1e-6)` | `n_bins >= 2`, `eps > 0` |
| `calculate_ks(reference, current)` | Sem bins, smoothing ou thresholds |
| `calculate_csi(reference, current, eps=1e-6)` | `eps > 0`; categorias, incluindo ausências |
| `detect_drift_all_features(...)` | `feature_cols`, `numeric_cols`, `categorical_cols`, warning PSI/KS, severidade PSI/KS e `min_non_null=10`; não recebe `n_bins`/`eps` |

Pré-validação ilustrativa para listas explícitas:

```python
features = ["score", "renda", "uf"]
numericas, categoricas = ["score", "renda"], ["uf"]
assert len(set(features)) == len(features)
assert len(set(numericas)) == len(numericas) and len(set(categoricas)) == len(categoricas)
assert set(numericas).isdisjoint(categoricas)
assert set(numericas) | set(categoricas) == set(features)
assert set(features) <= set(ref.columns) and set(features) <= set(atual.columns)
```

Se usar inferência, derive e confira as listas efetivas sob os dtypes da referência antes de interpretar o relatório.

`n_bins` altera a discretização do PSI. `eps` evita log de zero e influencia categorias/bins raros. `min_non_null` controla quando a varredura recusa evidência numérica insuficiente.

A definição da referência é mais importante que o número do threshold: mudar a referência muda a pergunta.

## 11. Limitações, riscos e armadilhas

O código é driver-side. PSI depende dos bins da referência. KS p-value é sensível ao tamanho amostral e requer pressupostos do teste. CSI pode ficar instável em alta cardinalidade/raridade.

Na categórica, a checagem de `min_non_null` usa o comprimento total da série, apesar do nome do parâmetro; portanto ela não conta apenas valores não nulos nesse ramo.

Com os dois thresholds de warning presentes, `severe_ks_threshold` pode ser usado sem `severe_psi_threshold`; severidade numérica dispara por qualquer limiar severo configurado atingido (`>=`). Sem warning, KS severo isolado não classifica. Os limiares devem ser coerentes e finitos por política do chamador; o wrapper não valida todos esses limites.

## 12. Quais são as alternativas?

Compare quantis, histogramas, Jensen-Shannon/Wasserstein ou testes específicos conforme o tipo de dado. Para acompanhar métricas de modelo realizadas, veja [`performance_monitor`](../performance_monitor/README.md).

## 13. Como saber se o resultado faz sentido?

Inspecione distribuição e missing antes/depois, tamanho amostral, bins/categorias que mais contribuíram e estabilidade histórica do índice. Relacione drift a performance somente quando o target realizado estiver disponível.

## 14. Arquivos relacionados e próximos passos

A [implementação](drift_detection.py) contém PSI/KS/CSI e varredura; a [fachada](__init__.py) define a API pública; o [notebook](exemplo_drift_detection.py) demonstra mudança de forma e política explícita.

Para performance realizada, use [`metrics_report`](../metrics_report/README.md) e [`performance_monitor`](../performance_monitor/README.md).

## 15. Referências

Consulte scipy.stats.ks_2samp para a definição do teste KS. PSI/CSI usam a discretização e o smoothing descritos neste guia; seus thresholds são política do consumidor, não limites universais.