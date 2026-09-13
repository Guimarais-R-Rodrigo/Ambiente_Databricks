# `drift_detection` — investigar se as distribuições dos dados mudaram

<!-- readme-objeto: 1.0.0 -->

Este snippet compara uma população de referência com outra atual. Produz evidências de mudança de distribuição e, somente com limiares fornecidos, classifica alertas. Não conclui que o modelo piorou nem autoriza retreino.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Diagnóstico de distribuição com PSI, KS e CSI. |
| Para que serve? | Localizar variáveis que merecem investigação entre dois recortes. |
| Use quando... | Referência, população atual e significado das colunas são comparáveis. |
| Evite quando... | Você precisa medir desempenho sem rótulos ou comparar categorias por ordem numérica arbitrária. |
| Precisa de... | NumPy, pandas e SciPy; amostras compatíveis com a memória do driver. |
| Entrega... | Índice escalar, par KS/p-valor ou DataFrame de evidências e status. |

Veja a [implementação](drift_detection.py), a [fachada](__init__.py) e o [notebook](exemplo_drift_detection.py). Os exemplos são sintéticos e não escrevem tabelas.

## 1. O que é?

Drift significa mudança de distribuição: a frequência de determinados valores pode mudar mesmo que a média permaneça parecida. Isso pode refletir comportamento, sazonalidade, composição da população ou um problema no pipeline.

O PSI compara frequências em faixas numéricas; o CSI desta implementação usa a mesma aritmética sobre categorias. O KS compara distribuições acumuladas e retorna a maior distância e um p-valor. São descrições complementares, não três votos automáticos sobre a saúde do modelo.

## 2. Que problema este recurso resolve?

Responde “quais variáveis mudaram entre a referência e o período atual, e por quanto?”. Pode ajudar a priorizar inspeção de uma alteração de origem, de uma nova safra ou do score de um modelo.

É necessário investigar a causa. Uma distribuição diferente pode ser esperada por sazonalidade; uma distribuição parecida não garante que a relação entre features e alvo continue igual.

## 3. Quando faz sentido usar?

Use depois de verificar contrato de dados, unidade e filtros. É útil quando ainda não existem rótulos maduros para medir performance, desde que o resultado seja tratado como alerta sobre dados, não desempenho.

Também ajuda a comparar versões de um pipeline. Fixe a referência e a estratégia de amostragem para distinguir mudança real de troca acidental da população usada na comparação.

## 4. Quando não usar?

Não compare renda em reais com renda em milhares de reais e conclua que o comportamento do cliente mudou. O código pode rodar, mas detectará uma mudança de representação.

Não passe códigos numéricos de categorias a PSI como se a distância entre os códigos tivesse significado. Strings numéricas podem ser convertidas e produzir um resultado inadequado sem erro de tipo. Para categorias, use CSI ou declare `categorical_cols` de forma coerente.

## 5. Como funciona, intuitivamente?

No PSI, o código obtém cortes internos por quantis da **referência**. Une quantis repetidos e acrescenta extremos infinitos; valores atuais além do mínimo ou máximo da referência continuam contados. Os faltantes `NaN` entram em uma faixa adicional.

Para cada faixa ou categoria, soma `(proporção_atual − proporção_referência) × log(proporção_atual / proporção_referência)`. `eps` substitui proporções muito pequenas para evitar logaritmo de zero, sem renormalização posterior. Escolhas de faixas e de `eps` influenciam a magnitude.

O KS usa observações finitas e resume a maior diferença absoluta entre acumuladas. Seu p-valor se refere a hipóteses estatísticas sob premissas de amostragem, não à probabilidade de o modelo estar quebrado.

## 6. Exemplo de situação

Uma referência sintética contém valores concentrados perto de 600. A população atual tem metade perto de 520 e metade perto de 680. As médias podem ficar próximas, mas o formato mudou. PSI e KS permitem enxergar essa mudança que a média isolada esconderia.

O [notebook](exemplo_drift_detection.py) constrói essa situação e também muda a distribuição de UF. Seus resultados são históricos daquela fixture, não limiares recomendados para uma operação real.

## 7. O que você precisa antes de usar?

Para funções numéricas, forneça arrays convertíveis para números. `calculate_psi` rejeita infinitos e exige ao menos um valor finito em cada população; uma população inteiramente faltante não é avaliada. `calculate_ks`, diferentemente, elimina valores não finitos. As funções achatam arrays: valide você mesmo que cada elemento representa uma observação da variável.

Para a varredura, informe DataFrames pandas, `feature_cols` e listas de tipos coerentes. O código verifica a presença de `feature_cols`, mas não garante que listas explícitas de numéricas/categóricas sejam disjuntas e subconjuntos dessa lista. Lista vazia usa inferência por causa do operador `or`; não significa necessariamente “não avaliar esse tipo”.

Alinhe definições e janelas, não as mesmas linhas: são duas distribuições, com tamanhos que podem diferir. Para interpretar p-valores, avalie dependência entre observações, repetições por cliente e valores discretos/empatados; o teste KS clássico pressupõe amostras independentes de distribuições contínuas.

## 8. O que este recurso entrega?

`calculate_psi` e `calculate_csi` devolvem números sem unidade. `calculate_ks` devolve `(estatística, p_valor)`, com estatística entre zero e um. Esse KS compara referência e atual; não o confunda com KS de discriminação entre classes de um modelo.

A varredura retorna colunas `feature`, `type`, `psi`, `ks_statistic`, `ks_pvalue`, `reference_n`, `current_n`, percentuais de faltantes e `status`. Para categóricas, o **CSI aparece na coluna `psi`** e vários outros campos ficam ausentes. A tabela é ordenada por `psi`, com ausentes no fim; não tem arredondamento próprio.

Sem política, o status é `NOT_CLASSIFIED`, não “saudável”. Com dados insuficientes, é `INSUFFICIENT_DATA`. Com limiares, pode ser `OK`, `ALERT` ou `SEVERE`.

## 9. Como usar este recurso no Hub?

Este caso em memória compara populações idênticas sem inventar política:

```python
import pandas as pd
from hub_snippets.ml.drift_detection import detect_drift_all_features

referencia = pd.DataFrame({"valor": list(range(12)), "grupo": ["A", "B"] * 6})
atual = referencia.copy()
relatorio = detect_drift_all_features(
    referencia, atual,
    feature_cols=["valor", "grupo"],
    numeric_cols=["valor"], categorical_cols=["grupo"],
)
print(relatorio[["feature", "psi", "status"]])
```

O [notebook](exemplo_drift_detection.py) acrescenta exemplos com mudança e limiares. A coleta Spark, quando necessária, deve ser limitada e realizada antes: este módulo não a executa.

## 10. Decisões e configurações que mais importam

`calculate_psi` usa `n_bins=10` e `eps=1e-6`; quantis repetidos podem gerar menos faixas. A varredura não expõe esses dois parâmetros e usa os padrões. `min_non_null=10` exige quantidade de valores numéricos finitos; **para categóricas, verifica o total de linhas, não a quantidade não nula**, apesar do nome.

`psi_threshold` e `ks_threshold` devem ser fornecidos juntos ou ambos omitidos. O segundo compara **estatística KS**, não p-valor. Na numérica, basta uma das duas estatísticas atingir o corte; na categórica, CSI usa o corte chamado `psi_threshold`. Os limiares `severe_*` são opcionais.

O código não valida completamente intervalos, finitude e ordem dos limiares de drift. Confira `warning < severe`, escalas e consistência antes da chamada; não presuma que uma política aceita pelo código esteja calibrada.

## 11. Limitações, riscos e armadilhas

Categorias novas ou raras e o valor de `eps` podem dominar o índice. O literal `__MISSING__` representa faltantes: se já for uma categoria legítima, será misturado com eles. Agrupar categorias exige uma regra estável e documentada.

Conversão numérica malsucedida vira `NaN`, mas os percentuais de faltantes da varredura são calculados antes dessa conversão. Por isso os percentuais podem não representar todos os valores descartados. Infinitos podem interromper a varredura inteira quando PSI é calculado; não há captura de erro por feature.

Não há correção de múltiplos testes, diagnóstico causal ou intervalo de confiança para os índices. Mais observações aumentam o poder do KS: p-valor pequeno pode coexistir com efeito pequeno. Não há número de linhas a partir do qual p-valores se tornem universalmente inúteis.

## 12. Quais são as alternativas?

[`performance_monitor`](../performance_monitor/README.md) compara métricas do modelo quando há alvos realizados. [`null_summary`](../../spark/null_summary/README.md) ajuda a avaliar faltantes; o [PSI Spark](../../spark/psi_calculator/README.md) tem outro contrato e deve ser confrontado antes de substituir este cálculo local.

Para distribuições difíceis, examine frequências e histogramas junto dos índices. Não troque uma tabela descritiva transparente por um alerta sem explicar a política.

## 13. Como saber se o resultado faz sentido?

Compare uma base com sua própria cópia: PSI/CSI devem ser zero, salvo efeitos numéricos, e KS também. Injete uma mudança controlada em faltantes ou categorias e confirme sua contabilização. Confira os números finitos usados e os faltantes antes/depois da conversão.

Leia o status junto das evidências e da política. No exemplo histórico, `0,250667 − 0,25 = 0,000667`; estar pouco acima de um corte não transforma automaticamente uma diferença pequena em problema operacional relevante.

## 14. Arquivos relacionados e próximos passos

A [implementação](drift_detection.py) define faixas, categorias e status; a [fachada](__init__.py) expõe quatro funções e a categoria reservada; o [notebook](exemplo_drift_detection.py) mostra a comparação com e sem política. Consulte o [catálogo](../../README.md) e o [Manual](../../../MANUAL_TECNICO.md).

Depois do diagnóstico, investigue qualidade, sazonalidade e composição dos dados; avalie desempenho separadamente quando os rótulos estiverem disponíveis.

## 15. Referências

A implementação/fachada local é a fonte para PSI, CSI, limiares e tratamento de faltantes desta pasta. A [documentação oficial de `ks_2samp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_2samp.html) sustenta a definição bilateral e as premissas do teste. Consultada em 13/09/2026.

Autorrevisão R09 e testes sintéticos registrados separadamente no relatório da sprint. Não há homologação de política, publicação Databricks ou auditoria independente.
