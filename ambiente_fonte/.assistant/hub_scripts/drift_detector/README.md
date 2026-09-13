# `drift_detector` — medir mudança de distribuição sem confundir drift com performance

<!-- readme-objeto: 1.0.0 -->

Duas populações podem ter médias parecidas e distribuições muito diferentes. `drift_detector` compara duas coortes da mesma tabela usando Population Stability Index (PSI), com faixas construídas a partir da população de referência. O índice sinaliza mudança na distribuição; não prova que um modelo piorou.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um script PySpark que calcula PSI para colunas numéricas entre duas coortes. |
| Para que serve? | Localizar mudança de distribuição de entrada entre referência e comparação. |
| Use quando... | Houver duas populações não vazias, comparáveis e uma política de monitoramento coerente. |
| Evite quando... | Precisar medir performance do modelo, variável categórica ou causalidade. |
| Precisa de... | Tabela, coluna de coorte, valores de referência/comparação e colunas numéricas ou seleção automática. |
| Entrega... | PSI por coluna, bins, proporções, tamanhos e classificação opcional. |

Consulte a [implementação](drift_detector.py), a [fachada](__init__.py) e o [exemplo](exemplo_drift_detector.py). O exemplo cria/substitui a view temporária `vw_exemplo_drift`.

## 1. O que é?

PSI compara como a proporção de observações se distribui entre faixas fixas em duas populações. A implementação deste script cria limites por quantis aproximados da referência, aplica os mesmos limites à comparação e soma as contribuições `(p_comp - p_ref) × ln(p_comp / p_ref)` por bucket.

Isso é uma medida de mudança de distribuição. Não é teste de hipótese, não estima impacto no target e não mede diretamente discriminação, calibração ou erro de um modelo.

## 2. Que problema este recurso resolve?

Ele responde: “Esta variável está distribuída de forma diferente na coorte atual em relação à referência?”. A pergunta é relevante porque alterações de mix, faixa, dispersão ou concentração podem passar despercebidas quando olhamos apenas média e desvio.

O resultado apoia investigação de monitoramento. Um PSI alto pede contexto: mudança de produto, sazonalidade, alteração de captura, mudança de população ou outro fenômeno podem explicar o sinal.

## 3. Quando faz sentido usar?

Use quando as duas coortes representam períodos ou grupos que deveriam ser comparáveis e as variáveis são numéricas. É útil em monitoramento de inputs de modelos, features de CRM e variáveis de risco, desde que tamanho amostral e estabilidade dos bins sejam suficientes.

Também faz sentido quando você quer manter a referência fixa: os bins são derivados da coorte de referência e reutilizados, evitando redefinir a escala em cada período.

## 4. Quando não usar?

Não use PSI alto como sinônimo de queda de performance. Um modelo pode receber distribuição diferente e continuar performando; ou pode degradar sem grande PSI nas variáveis monitoradas.

Não passe variável categórica esperando CSI. A implementação chama `approxQuantile` e foi desenhada para colunas numéricas. Para categóricas, use uma rotina apropriada, como a implementação de drift/CSI existente em `hub_snippets/ml/drift_detection`.

## 5. Como funciona, intuitivamente?

A função abre a tabela e filtra duas coortes pela igualdade em `date_col`. Tenta colocar cada recorte em cache; se o ambiente não permitir, continua sem cache. Depois exige que ambos tenham linhas.

Para cada variável, calcula `num_bins - 1` quantis aproximados na referência, remove limites repetidos e cria os buckets comuns. Nulos e `NaN` vão para `missing`. As proporções por bucket alimentam o PSI.

Quando uma proporção é zero, o código usa `epsilon` como piso para evitar `log(0)`. Esse alisamento não renormaliza todas as proporções depois da substituição; ele existe para estabilizar o cálculo, não para produzir uma nova distribuição probabilística exata.

## 6. Exemplo de situação

O [notebook de exemplo](exemplo_drift_detector.py) cria duas safras com média parecida. A referência é concentrada ao redor de um centro; a comparação mistura dois grupos distantes. A média muda pouco, mas o PSI cresce porque os extremos recebem proporções muito diferentes.

Esse cenário ensina por que olhar apenas média pode ser insuficiente. O valor numérico observado no exemplo pertence àquela simulação, não é benchmark universal.

## 7. O que você precisa antes de usar?

`table_name` deve ser legível por `spark.table`. `date_col` deve existir e conter valores que possam ser comparados diretamente com `date_ref` e `date_comp`. As duas coortes resultantes precisam ser não vazias.

`cols`, quando informado, deve conter colunas numéricas existentes. Se omitido, o código seleciona tipos cujo dtype textual contém `tinyint`, `smallint`, `int`, `bigint`, `float`, `double` ou `decimal`, excluindo a coluna de coorte.

`num_bins` deve ficar entre 2 e 100; `relative_error`, entre 0 e 1; `epsilon` precisa ser positivo. Se desejar classificação, forneça **os dois** limiares, obedecendo `0 <= warning_threshold < critical_threshold`.

## 8. O que este recurso entrega?

O retorno é um dicionário por coluna. Cada item contém:

| Campo | Significado |
|---|---|
| `psi` | Soma das contribuições por bucket. Valores maiores indicam maior divergência segundo esse índice. |
| `classification` | `not_classified` sem política completa; caso contrário, `stable`, `attention` ou `critical`. |
| `boundaries` | Limites derivados da referência após remoção de duplicatas. |
| `reference_size`, `comparison_size` | Tamanho das duas coortes. |
| `buckets` | Contagens, proporções alisadas e contribuição ao PSI em cada faixa. |

A classificação não aparece automaticamente em 0,1 ou 0,25. Sem os dois limiares fornecidos pelo consumidor, o código devolve `not_classified`.

## 9. Como usar este recurso no Hub?

```python
from hub_scripts.drift_detector import drift_detector

resultado = drift_detector(
    "catalogo.schema.base_monitoramento",
    date_col="safra",
    date_ref="2026-S1",
    date_comp="2026-S2",
    cols=["score"],
    warning_threshold=0.10,
    critical_threshold=0.25,
)
```

Os números acima são exemplo de política, não recomendação universal. O [notebook](exemplo_drift_detector.py) usa dados sintéticos e mostra como interpretar bins e tamanhos antes do PSI agregado.

## 10. Decisões e configurações que mais importam

A escolha da referência é estrutural: os bins nascem dela. Trocar referência e comparação pode produzir outro conjunto de limites e outro PSI.

`num_bins` aumenta resolução, mas bins pequenos ficam mais sensíveis a ruído. `relative_error` controla a aproximação de `approxQuantile`; zero pede quantis exatos, potencialmente mais caros.

`epsilon` altera a contribuição de buckets ausentes em um dos lados. Não compare execuções com epsilon diferente como se fossem a mesma métrica.

Limiar de classificação deve ser calibrado para variável, amostra, processo e risco. O código se recusa a classificar quando a política está incompleta.

## 11. Limitações, riscos e armadilhas

PSI depende de discretização. Mudanças dentro de um mesmo bucket podem não aparecer; limites repetidos reduzem o número efetivo de faixas.

A seleção automática de colunas depende da representação textual do dtype. Tipos incomuns ou colunas explicitamente incompatíveis podem falhar em runtime. O script não valida significância estatística nem corrige múltiplas comparações.

O cache é oportunista: falhar ao armazenar não interrompe a execução. Isso preserva compatibilidade com compute em que `cache()` é restrito, mas pode aumentar recomputação.

O alisamento por `epsilon` evita infinito em buckets vazios, porém as proporções reportadas após aplicar o piso não são renormalizadas. Leia-as como valores usados no cálculo.

## 12. Quais são as alternativas?

Para PSI/CSI em DataFrames e comparação mais ampla, consulte a implementação de [`hub_snippets.ml.drift_detection`](../../hub_snippets/ml/drift_detection/drift_detection.py). Para um cálculo pontual de PSI/CSI já documentado na camada Spark, consulte [`psi_calculator`](../../hub_snippets/spark/psi_calculator/README.md).

Se a pergunta for performance, use métricas do modelo com target realizado. Se for apenas mudança de média/quantil, uma agregação Spark dirigida pode ser mais transparente e barata.

## 13. Como saber se o resultado faz sentido?

Primeiro confira `reference_size` e `comparison_size`. Depois inspecione `boundaries` e os buckets: proporções muito concentradas ou bins praticamente vazios explicam PSI alto melhor que o número agregado sozinho.

Crie um caso controle em que referência e comparação sejam iguais; o PSI deve ficar próximo de zero. Em outro caso, desloque deliberadamente a distribuição e verifique que o índice cresce.

Compare ainda médias, quantis e histogramas para entender a direção da mudança. PSI sem diagnóstico visual ou estatístico complementar é apenas um alarme.

## 14. Arquivos relacionados e próximos passos

A [implementação](drift_detector.py) contém buckets, PSI e classificação; a [fachada](__init__.py) expõe a função; o [exemplo](exemplo_drift_detector.py) demonstra distribuições de mesma média e forma diferente. O [catálogo](../README.md) separa drift de qualidade, governança e transformação.

Após detectar mudança, identifique origem e impacto. A decisão de reentreinar, bloquear ou ajustar processo pertence a uma política posterior.

## 15. Referências

O comportamento específico foi conferido na implementação e no exemplo locais durante a R04-B em 12/09/2026. O Apache Spark documenta [`DataFrame.approxQuantile`](https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.approxQuantile.html), incluindo o papel do erro relativo; essa API sustenta o cálculo dos limites, não os limiares de PSI.

Os thresholds de monitoramento permanecem política local. A validação da R04-B registra a execução com Spark real após o fechamento técnico. Revisão do próprio autor não é auditoria independente nem homologação Databricks.