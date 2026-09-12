# `psi_calculator` — medir mudança de distribuição com referência fixa

<!-- readme-objeto: 1.0.0 -->

PSI e CSI resumem quanto a distribuição de uma variável mudou entre uma população de referência e outra população. Este módulo implementa o cálculo em PySpark, mantendo as faixas numéricas derivadas somente da referência e exigindo política explícita para classificar o valor.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Cálculo Spark de PSI numérico, CSI por feature e interpretação opcional por limiares. |
| Para que serve? | Sinalizar mudança de distribuição entre duas populações. |
| Use quando... | Referência e comparação representam populações comparáveis e a variável tem significado estável. |
| Evite quando... | Você quer medir performance do modelo, causalidade ou decidir retreino automaticamente. |
| Precisa de... | Dois DataFrames Spark, coluna(s), bins e política própria se quiser classificação. |
| Entrega... | Float de PSI, dicionário de CSI ou texto de interpretação conforme a função usada. |

Leia a [implementação](psi_calculator.py), a [fachada](__init__.py) e o [notebook](exemplo_psi_calculator.py). Não há escrita persistente; existem agregações, quantis aproximados e coletas agregadas para o driver.

## 1. O que é?

O *Population Stability Index* (PSI) compara proporções em faixas comuns. A ideia é fixar a régua na referência e observar como a população atual se redistribui. O módulo usa quantis aproximados da referência para construir os cortes de variáveis numéricas.

`calcular_psi` trabalha com uma coluna numérica. `calcular_csi` percorre uma lista de features: tipos numéricos usam o mesmo PSI; os demais são tratados como categorias e comparados por frequência. `interpretar_psi` apenas converte um valor em mensagem; sem dois limiares explícitos, não classifica.

## 2. Que problema este recurso resolve?

A pergunta é: “A distribuição desta feature mudou em relação à população de referência?”. Isso é útil em monitoramento de dados, comparação de safras e investigação de mudança populacional.

A função não responde “o modelo piorou?”. Performance preditiva exige métricas e, em geral, o alvo realizado. Drift de entrada e degradação de performance são fenômenos relacionados, mas distintos.

## 3. Quando faz sentido usar?

Use quando há uma referência defensável — por exemplo, população de desenvolvimento, período aprovado ou coorte estável — e uma população atual comparável. Os significados, unidades e tratamentos da feature precisam permanecer consistentes.

`calcular_csi` é útil quando você quer varrer várias features e ordená-las pelo índice. Para categóricas de baixa cardinalidade, ele preserva a categoria ausente separadamente e protege a coleta com `max_categorias`.

## 4. Quando não usar?

Não use PSI como gatilho universal de retreino. Um índice alto pede investigação; a decisão de retreinar depende de performance, causa da mudança, custo e governança.

Não use `calcular_psi` em categorias textuais; nesse caso use `calcular_csi`. Evite CSI categórico em identificadores ou cardinalidade muito alta sem agregação prévia.

Contraexemplo: a feature mudou de escala de reais para milhares de reais entre períodos. O PSI sinaliza forte mudança, mas o problema é quebra de contrato da variável, não necessariamente mudança da população.

## 5. Como funciona, intuitivamente?

Para variável numérica, a referência fornece os quantis internos de `n_bins`. Cortes repetidos são deduplicados. Valores ausentes/NaN entram no bucket 0; valores válidos são distribuídos nos buckets definidos pelos cortes.

As duas populações são agregadas pelos mesmos buckets. Para cada bucket, o cálculo usa `(p_atual - p_base) * ln(p_atual / p_base)` e soma as contribuições. `epsilon=1e-6` é interno para evitar proporção zero no log.

Para categorias, cada combinação `(is_missing, category)` é uma classe. A distribuição agregada de cada população é coletada depois da guarda de cardinalidade.

## 6. Exemplo de situação

Uma referência sintética tem renda concentrada perto de 10 mil. A população atual mantém média semelhante, mas se divide em dois grupos perto de 4 mil e 16 mil. Comparar só a média quase não vê a mudança; faixas de PSI capturam a redistribuição.

O notebook registra esse cenário e mostra que `interpretar_psi(psi)` sem política devolve apenas o valor e a instrução de comparar com uma política calibrada.

## 7. O que você precisa antes de usar?

Os dois DataFrames devem conter a coluna analisada. `n_bins` precisa estar entre 2 e 100. As populações não podem ser vazias no momento do cálculo do índice.

Para `calcular_csi`, `feature_cols` não pode ser vazio e todas as colunas devem existir nos dois lados. O tipo usado para decidir “numérico ou categórico” vem de `df_base.dtypes`; confirme que a coluna atual possui semântica e tipo compatíveis.

`max_categorias` deve ser inteiro positivo — booleano é recusado — e limita a quantidade de categorias agregadas **por população** antes da coleta. Ele não limita bytes totais nem elimina o custo do `groupBy`.

## 8. O que este recurso entrega?

`calcular_psi` devolve um `float` arredondado a seis casas. `calcular_csi` devolve `{feature: valor}`, ordenado do maior índice para o menor. O retorno não inclui os breakpoints nem contribuições por bucket.

`interpretar_psi` devolve texto. Se `warning_threshold` ou `critical_threshold` estiver ausente, a função retorna mensagem genérica; informar somente um deles também não classifica. Com ambos, exige `0 <= warning < critical` e usa 🟢/🟡/🔴 conforme os cortes.

O valor não tem unidade e não informa por si só a causa da mudança.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.spark.psi_calculator import calcular_psi, interpretar_psi

psi = calcular_psi(referencia, atual, "renda", n_bins=10)
print(interpretar_psi(psi))
```

O [notebook](exemplo_psi_calculator.py) demonstra mudança de forma com média parecida, classificação somente com limiares explícitos e varredura por `calcular_csi`. Não persiste tabelas.

## 10. Decisões e configurações que mais importam

A primeira decisão é a população de referência. Mudar a referência muda a régua. `n_bins` controla a granularidade desejada, mas quantis repetidos podem reduzir a quantidade efetiva de faixas.

Os quantis numéricos usam `approxQuantile(..., relativeError=0.01)` fixo nesta implementação. Esse erro relativo não é parâmetro público de `calcular_psi`.

`max_categorias=1000` é uma guarda local, não um limite universal. `warning_threshold` e `critical_threshold` são política do consumidor; os números 0,10 e 0,25 citados no notebook são exemplos de uma régua tradicional, não defaults da função nem norma.

## 11. Limitações, riscos e armadilhas

A implementação numérica coleta apenas agregados por bucket, mas ainda executa quantis e `groupBy` distribuídos. A categórica faz contagem de categorias em cada população e depois coleta distribuições completas até o limite configurado.

A guarda é por número de categorias, não por tamanho textual ou memória real. Tipos são classificados a partir da referência; alteração de tipo entre períodos não recebe uma validação explícita de igualdade.

O retorno do PSI não expõe os cortes; para auditoria detalhada por bucket, [`drift_detector`](../../../hub_scripts/drift_detector/drift_detector.py) possui contrato diferente e devolve boundaries e contribuições para coortes de uma tabela nomeada.

## 12. Quais são as alternativas?

[`drift_detector`](../../../hub_scripts/drift_detector/drift_detector.py) compara duas coortes selecionadas por uma coluna de data em uma tabela e devolve detalhe por bucket para variáveis numéricas. Ele não é substituto exato: recebe `table_name`, só implementa PSI numérico e possui parâmetros de erro relativo e suavização.

`psi_calculator` é mais direto quando você já tem dois DataFrames e também precisa de CSI categórico. Métodos como KS, Jensen-Shannon ou testes de hipótese respondem a contratos diferentes e não estão implementados aqui.

## 13. Como saber se o resultado faz sentido?

Primeiro compare uma população com ela mesma ou com cópia equivalente: o índice deve ser zero ou muito próximo, sujeito às operações usadas. Depois crie uma mudança sintética forte e confira que o índice aumenta.

Verifique também nulos, unidades, faixas, quantidade de categorias e tamanho das duas populações. Um valor inesperado deve levar à inspeção da distribuição e do pipeline, não diretamente a uma ação operacional.

## 14. Arquivos relacionados e próximos passos

- [Implementação](psi_calculator.py): bins, estabilidade e guardas.
- [Fachada](__init__.py): exporta limite e três funções públicas.
- [Notebook](exemplo_psi_calculator.py): cenário sintético e interpretação.
- [`drift_detector`](../../../hub_scripts/drift_detector/drift_detector.py): comparação de coortes de uma tabela com detalhe numérico por bucket.
- [Coleção](../../README.md): demais snippets Spark.

## 15. Referências

O comportamento e as comparações foram conferidos em `psi_calculator.py`, `__init__.py`, `exemplo_psi_calculator.py` e na implementação local de `drift_detector`. O notebook documenta a distinção conceitual entre drift de entrada e performance.

Os índices e limiares apresentados são mecanismos de monitoramento, não padrões Databricks. A R04-A registra execução sintética Spark em evidência própria; sem publicação, dados reais ou auditoria independente.
