# `scorecard_builder` — converter log-odds em pontos sem confundir escala com probabilidade

<!-- readme-objeto: 1.0.0 -->

Este helper converte coeficientes de um modelo logístico treinado sobre variáveis WOE em uma tabela de pontos por faixa. A escala é definida por `PDO`, score base e odds de referência. Ele torna a contribuição por faixa legível; **não ajusta o modelo, não aplica binning, não pontua linhas novas e não certifica um scorecard para uso regulado**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Conversor de coeficientes logísticos + WOE para tabela de pontos. |
| Para que serve? | Construir a tabela de contribuições de um scorecard. |
| Use quando... | O modelo logístico, a orientação do evento, as tabelas WOE e a escala já estiverem definidos. |
| Evite quando... | Ainda faltar binning, validação, calibração, política de corte ou função de scoring. |
| Precisa de... | NumPy, pandas, coeficientes alinhados e tabelas pandas com `faixa`/`woe`. |
| Entrega... | DataFrame com feature, faixa, WOE, coeficiente e pontos arredondados. |

Consulte a [implementação](scorecard_builder.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_scorecard_builder.py).

## 1. O que é?

Na regressão logística, o preditor linear vive em escala de log-odds. Um scorecard aplica uma transformação linear dessa escala para uma convenção de pontos. `PDO` (*points to double odds*) define quantos pontos correspondem à duplicação das odds favoráveis sob a orientação adotada.

`build_scorecard` distribui o componente de intercepto igualmente entre as features e acrescenta a contribuição `coef × WOE` de cada faixa.

## 2. Que problema este recurso resolve?

Coeficientes e log-odds são pouco operacionais para revisão humana. Uma tabela de pontos permite visualizar quanto cada faixa contribui para o score final e reproduzir manualmente a soma.

Isso não substitui o pipeline que transforma dados brutos em faixas, busca o WOE correto e soma os pontos por cliente.

## 3. Quando faz sentido usar?

Use depois de treinar e validar um modelo logístico sobre features WOE compatíveis com as mesmas tabelas passadas ao helper. A ordem de `feature_names` precisa corresponder exatamente à ordem de `coefs`.

Também faz sentido como artefato de documentação de uma escala já definida, desde que a orientação do evento seja explicitada.

## 4. Quando não usar?

Não use com coeficientes de um modelo que não opera sobre os WOE informados. Não misture tabelas recalculadas depois do treino sem revalidar o modelo.

Não use a tabela retornada como função de scoring. O helper não recebe observações novas nem decide a qual faixa cada valor pertence.

## 5. Como funciona, intuitivamente?

A função calcula `factor = pdo / ln(2)` e `offset = base_score - factor * ln(base_odds)`. Quando `event_is_bad=True`, maior log-odds do evento adverso reduz o score; quando `False`, a direção é invertida.

O termo `(offset + direção × factor × intercept)` é dividido pelo número de features. Para cada faixa, soma-se `direção × factor × coef × woe`. O valor final de cada contribuição é arredondado para zero casas.

## 6. Exemplo de situação

Um modelo de inadimplência usa três features transformadas em WOE e modela `P(mau)`. Com `event_is_bad=True`, `base_score=600`, `base_odds=50` e `pdo=20`, o ponto de referência corresponde a odds favoráveis de 50:1. Vinte pontos adicionais dobram as odds favoráveis nessa convenção.

O score de um cliente seria a soma dos pontos das três faixas que ele ocupa — etapa que este helper não executa automaticamente.

## 7. O que você precisa antes de usar?

`coefs` deve ser finito e ter o mesmo tamanho de `feature_names`. `intercept` precisa ser finito. `pdo` e `base_odds` devem ser positivos.

Cada `woe_tables[feature]` precisa ser um DataFrame pandas com colunas `faixa` e `woe`, com WOE numérico finito. A saída Spark de `woe_iv_calculator.calculate_woe_iv` **não entra diretamente**: é necessário coletar deliberadamente para pandas e renomear a coluna da feature para `faixa`.

## 8. O que este recurso entrega?

O retorno contém `feature`, `faixa`, `woe`, `coef`, `pontos` e `event_is_bad`. WOE e coeficiente são arredondados a quatro casas para apresentação; pontos são arredondados a zero casas.

Esse arredondamento implica que a soma das contribuições discretizadas pode diferir levemente da transformação contínua exata do logit.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.scorecard_builder import build_scorecard

card = build_scorecard(
    coefs=coefs,
    intercept=intercept,
    feature_names=feature_names,
    woe_tables=woe_tables,
    pdo=20,
    base_score=600,
    base_odds=50,
    event_is_bad=True,
)
```

Se as tabelas vierem do helper Spark de WOE, faça a ponte de volume controlado explicitamente antes desta chamada.

## 10. Decisões e configurações que mais importam

`event_is_bad` define a orientação entre logit e pontos. Trocar esse valor inverte o sentido do score. `base_score`, `base_odds` e `pdo` definem a escala e precisam ser tratados como parâmetros de contrato, não como propriedades estimadas pelo helper.

A definição de `base_odds` no código é uma razão favorável:desfavorável coerente com a orientação escolhida. Documente essa convenção junto do score.

## 11. Limitações, riscos e armadilhas

O helper não valida monotonicidade de WOE, qualidade do binning, estabilidade, significância, calibração ou desempenho. Tampouco verifica se categorias/faixas cobrem todos os valores possíveis em produção.

A divisão do intercepto igualmente entre features é uma decomposição de apresentação: a soma preserva o termo total antes do arredondamento, mas a alocação do intercepto por feature não tem interpretação causal.

O notebook histórico diz que pontos tornam a decisão “auditável por quem não lê código”. A tabela ajuda na rastreabilidade, mas auditabilidade real também exige regras de binning, versão, origem dos dados, política, testes e trilha de aprovação.

## 12. Quais são as alternativas?

[woe_iv_calculator](../woe_iv_calculator/README.md) calcula WOE/IV em Spark, mas não cria score. [score_bands](../score_bands/README.md) resume uma distribuição de scores já calculados.

Quando a necessidade principal é probabilidade calibrada e não uma escala de pontos, consumir a probabilidade do modelo validado pode ser mais direto.

## 13. Como saber se o resultado faz sentido?

Escolha combinações de faixas conhecidas e compare a soma dos pontos com a transformação contínua do logit do mesmo caso, aceitando apenas a diferença esperada de arredondamento. Confirme que aumentar o risco move o score na direção prevista.

Valide especialmente a orientação `event_is_bad`, as odds de referência e a ordem dos coeficientes.

## 14. Arquivos relacionados e próximos passos

A [implementação](scorecard_builder.py) constrói a tabela; a [fachada](__init__.py) exporta `build_scorecard`; o [notebook](exemplo_scorecard_builder.py) demonstra a escala de pontos.

O próximo passo operacional é versionar também binning/aplicação de faixas e validar o score completo fora da amostra — funções que não pertencem a este helper.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `289731c79e8ed43d82b39d61cdc41ba2e69ea717`. A transformação usa a relação log-odds da regressão logística e a convenção local de PDO/base score/base odds codificada no helper. Não existe neste README alegação de que essa parametrização seja uma exigência regulatória universal.

Este README não presume homologação do scorecard, publicação no Databricks nem auditoria independente.