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

Defina `feature_cols`. Se não passar listas de tipos, a função infere numéricas a partir do DataFrame de referência e trata as demais como categóricas.

Para classificar status, `psi_threshold` e `ks_threshold` devem ser fornecidos juntos. Thresholds severos exigem thresholds de warning. `min_non_null` deve ser positivo.

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

`n_bins` altera a discretização do PSI. `eps` evita log de zero e influencia categorias/bins raros. `min_non_null` controla quando a varredura recusa evidência numérica insuficiente.

A definição da referência é mais importante que o número do threshold: mudar a referência muda a pergunta.

## 11. Limitações, riscos e armadilhas

O código é driver-side. PSI depende dos bins da referência. KS p-value é sensível ao tamanho amostral e requer pressupostos do teste. CSI pode ficar instável em alta cardinalidade/raridade.

Na categórica, a checagem de `min_non_null` usa o comprimento total da série, apesar do nome do parâmetro; portanto ela não conta apenas valores não nulos nesse ramo.

`severe_ks_threshold` sem `severe_psi_threshold` é aceito desde que os thresholds de warning existam; o status severo numérico dispara se qualquer threshold severo configurado for excedido.

## 12. Quais são as alternativas?

Compare quantis, histogramas, Jensen-Shannon/Wasserstein ou testes específicos conforme o tipo de dado. Para acompanhar métricas de modelo realizadas, veja [`performance_monitor`](../performance_monitor/README.md).

## 13. Como saber se o resultado faz sentido?

Inspecione distribuição e missing antes/depois, tamanho amostral, bins/categorias que mais contribuíram e estabilidade histórica do índice. Relacione drift a performance somente quando o target realizado estiver disponível.

## 14. Arquivos relacionados e próximos passos

A [implementação](drift_detection.py) contém PSI/KS/CSI e varredura; a [fachada](__init__.py) define a API pública; o [notebook](exemplo_drift_detection.py) demonstra mudança de forma e política explícita.

Para performance realizada, use [`metrics_report`](../metrics_report/README.md) e [`performance_monitor`](../performance_monitor/README.md).

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da R09. Referência primária para KS: documentação SciPy de `ks_2samp`. PSI/CSI são implementações locais cuja discretização, smoothing e thresholds devem ser tratados como parte do contrato do Hub, não como defaults universais.