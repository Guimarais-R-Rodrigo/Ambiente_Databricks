# `format_br` — apresentar números sem mudar o que eles significam

<!-- readme-objeto: 1.0.0 -->

Este módulo transforma números em textos no padrão brasileiro. Ele ajuda a apresentar valores, taxas e diferenças com a unidade correta, sem alterar a configuração regional do sistema.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Seis funções de formatação para textos de relatório. |
| Para que serve? | Exibir milhares, decimais, moeda, percentuais e variações consistentemente. |
| Use quando... | O cálculo já estiver pronto e você precisar apresentá-lo. |
| Evite quando... | O resultado ainda será somado, comparado numericamente ou usado como identificador. |
| Precisa de... | Um valor numérico e o conhecimento de sua unidade e escala. |
| Entrega... | Uma string; não devolve uma nova medida numérica. |

A [implementação](format_br.py), a [fachada](__init__.py) e o [notebook](exemplo_format_br.py) estão nesta pasta. O helper não escreve dados; o notebook consulta o usuário da sessão para configurar a importação.

## 1. O que é?

Formatar muda a representação, não o fenômeno medido. O número 12345.67 pode ser apresentado como `12.345,67` ou `R$ 12.345,67`. O segundo texto acrescenta uma unidade monetária; a função não verificou se o valor era de fato expresso em reais.

O módulo oferece `fmt_int`, `fmt_pct`, `fmt_brl`, `fmt_dec`, `fmt_delta` e `fmt_n`. Elas produzem texto diretamente, sem instalar ou selecionar um *locale*, configuração regional do sistema. O nome público `Number` também é exportado, mas é um alias de tipos, não uma sétima função de formatação.

## 2. Que problema este recurso resolve?

A pergunta é: “Como mostrar este indicador para que outra pessoa leia a magnitude e a unidade pretendidas?”. Isso evita que uma taxa calculada como fração vire um percentual cem vezes maior, ou que uma diferença entre taxas seja confundida com crescimento relativo. A responsabilidade por calcular corretamente o indicador continua fora do formatador.

## 3. Quando faz sentido usar?

Use na apresentação final de um resumo, legenda, cartão de indicador ou mensagem de notebook. `fmt_n` ajuda quando o espaço é curto e uma aproximação é aceitável; `fmt_int` e `fmt_brl` atendem situações em que o leitor precisa enxergar os dígitos apresentados por inteiro.

Para tabelas pandas já pequenas, a formatação pode ser aplicada à exibição, mantendo os dados originais numéricos. O [componente de tabelas estilizadas](../../display/dataframe_styled/dataframe_styled.py) trata dessa camada de apresentação.

## 4. Quando não usar?

Não substitua uma coluna numérica por strings antes de ordenar, somar ou treinar um modelo. Ordenação textual e numérica são operações diferentes. Um contraexemplo é salvar `"R$ 9,00"` e `"R$ 100,00"` como se fossem valores prontos para comparação de magnitude.

Também não use `fmt_int` ou `fmt_n` para identificadores ou contagens de precisão arbitrária. `fmt_n` converte a entrada para `float`; `fmt_int` usa apresentação `.0f`, que também envolve ponto flutuante. Ambos podem perder dígitos de inteiros muito grandes. Essas funções não são interpretadores de números escritos no padrão brasileiro, como `"1.234,56"`; tratar essa entrada e recuperar um número é outro problema.

## 5. Como funciona, intuitivamente?

Cada função escolhe uma representação. `fmt_int` primeiro aplica `int`, truncando a parte fracionária em direção a zero; depois aplica a apresentação `.0f` e separa milhares; essa etapa pode perder precisão em inteiros muito grandes. `fmt_pct` transforma fração em percentual quando necessário. `fmt_dec` controla as casas decimais. `fmt_delta` converte uma diferença de frações em pontos percentuais ou pontos-base e acrescenta sinal.

`fmt_brl` usa `Decimal(str(v))`, arredondamento `ROUND_HALF_UP` para centavos e montagem do texto com `R$`. Essa regra não é a mesma operação de formatação de ponto flutuante usada em todas as outras funções. A [documentação de Decimal](https://docs.python.org/3/library/decimal.html) explica a aritmética decimal e os modos de arredondamento.

## 6. Exemplo de situação

Uma campanha fictícia passa de 10% para 12% de resposta. A diferença em frações é `0.12 - 0.10 = 0.02`. Sua apresentação por `fmt_delta` é `+2,0 pp`: dois **pontos percentuais**, a diferença direta entre as duas taxas percentuais. Já o crescimento relativo seria 20%, obtido por outro cálculo. A função formata a grandeza recebida; não decide qual comparação você pretendia fazer.

No mesmo relatório, `fmt_pct(0.12)` exibe `12,0%`. Se a origem já traz 12, use `input_scale="percent"`. Passar 12 no padrão de fração produziria `1200,0%`, sem erro de execução.

## 7. O que você precisa antes de usar?

As funções recebem valores escalares, não DataFrames. Confirme antes a escala: fração, percentual, moeda ou diferença entre frações. Para percentual, os valores 0.928 e 92.8 diferem por um fator de **cem**, embora possam representar a mesma taxa sob convenções diferentes.

Não há uma política comum para `None`, NaN, infinito ou strings malformadas. Algumas entradas podem gerar texto inadequado; outras levantam exceção. Trate ausência e inválidos na preparação, sem transformar ausência em zero por conveniência. O módulo usa apenas a biblioteca padrão do Python.

## 8. O que este recurso entrega?

| Chamada | Texto produzido |
|---|---|
| `fmt_int(3375674)` | `3.375.674` |
| `fmt_int(12.9)` | `12` |
| `fmt_pct(0.928)` | `92,8%` |
| `fmt_pct(92.8, input_scale="percent")` | `92,8%` |
| `fmt_brl(1.999)` | `R$ 2,00` |
| `fmt_dec(0.8234)` | `0,8234` |
| `fmt_delta(0.0005, "bps")` | `+5 bps` |
| `fmt_n(3375674)` | `3,4M` |

Esses casos são verificáveis pelo código mínimo e pelos testes locais da R02. São saídas textuais, não valores destinados a nova aritmética. Pontos-base (*basis points*, `bps`) representam centésimos de ponto percentual; um ponto percentual corresponde a 0.01 na escala de fração.

## 9. Como usar este recurso no Hub?

Depois de configurar a importação conforme o [guia da coleção](../../README.md), este bloco usa apenas valores sintéticos:

```python
from hub_snippets.constants.format_br import (
    fmt_int, fmt_pct, fmt_brl, fmt_dec, fmt_delta, fmt_n,
)

assert fmt_int(3375674) == "3.375.674"
assert fmt_int(12.9) == "12"
assert fmt_pct(0.928) == "92,8%"
assert fmt_pct(92.8, input_scale="percent") == "92,8%"
assert fmt_brl(1.999) == "R$ 2,00"
assert fmt_dec(0.8234) == "0,8234"
assert fmt_delta(0.0005, "bps") == "+5 bps"
assert fmt_n(3375674) == "3,4M"
```

O bloco foi executado localmente nesta sprint, com a raiz do Hub adicionada ao caminho Python. O [notebook](exemplo_format_br.py) expande a explicação das escalas; sua execução no Databricks não foi presumida a partir desse teste local. Não é necessário alterar `locale` nem escrever tabela para usar o helper.

## 10. Decisões e configurações que mais importam

`fmt_pct` usa `casas=1` e `input_scale="ratio"` por padrão. Só aceita `"ratio"` e `"percent"` para escala; outros textos geram `ValueError`. `fmt_dec` usa quatro casas por padrão. Escolher menos casas pode ocultar diferenças pequenas e produzir igualdade apenas visual.

`fmt_delta` recebe diferença em frações. Só `unidade="bps"` seleciona pontos-base; qualquer outro texto cai em pontos percentuais, sem validação. Um erro de digitação pode, portanto, mudar a unidade silenciosamente. Use explicitamente `"pp"` ou `"bps"`.

Em `fmt_n`, `sufixo=True` abrevia com `k`, `M` e `B`. Com `False`, remove a abreviação, mas a conversão inicial para `float` permanece. Isso não é uma opção de precisão arbitrária.

## 11. Limitações, riscos e armadilhas

Os formatadores não validam a plausibilidade da métrica. Percentuais acima de 100% podem ser corretos para algumas grandezas e errados para outras; a regra pertence ao indicador. Uma string bem apresentada não resolve unidade incorreta.

Na execução local da R02, `fmt_int(9007199254740993)` produziu `9.007.199.254.740.992`, perdendo uma unidade. `fmt_n` sem sufixo teve o mesmo resultado. Esse limite foi documentado, não corrigido no código nesta sprint. Para precisão integral, preserve o inteiro e use uma representação sem conversão para ponto flutuante. A [especificação de formatação do Python](https://docs.python.org/3/library/string.html#format-specification-mini-language) explica os tipos de apresentação.

Perto das fronteiras de abreviação, o arredondamento pode gerar `1000,0k` em vez de trocar automaticamente para `1,0M`. `fmt_brl` também não implementa uma política contábil completa ou conversão cambial: acrescentar `R$` não muda a moeda de origem. Valores já calculados com erros numéricos não são recuperados pela apresentação decimal.

## 12. Quais são as alternativas?

Formatação nativa de Python pode atender um texto isolado; este módulo facilita consistência entre notebooks. Para um DataFrame pandas pequeno, [dataframe_styled](../../display/dataframe_styled/dataframe_styled.py) organiza a exibição. Para grandes tabelas Spark, mantenha os dados numéricos e escolha uma camada de apresentação apropriada; não colete toda a base apenas para formatar valores.

## 13. Como saber se o resultado faz sentido?

Confira um valor conhecido nas duas escalas percentuais e teste sinais, limites de arredondamento e abreviações próximas de mil, milhão e bilhão. Releia o exemplo de 10% para 12%: a diferença é 2 pp, não 2% de crescimento relativo.

Guarde o valor original ao lado da apresentação quando houver necessidade de auditoria. Para contagens com frações inesperadas, investigue a origem antes de aceitar o truncamento de `fmt_int`.

## 14. Arquivos relacionados e próximos passos

A [implementação](format_br.py) define regras e arredondamento; a [fachada](__init__.py) expõe funções e alias; o [notebook](exemplo_format_br.py) ensina as escalas. O [Manual](../../../MANUAL_TECNICO.md#catalogo-helpers) mantém o catálogo. O próximo passo é identificar a unidade do indicador que será apresentado, não escolher a função apenas pela aparência do texto.

## 15. Referências

Contrato e exemplos conferidos no código da base R01 `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`. A referência externa pertinente é a [documentação oficial de Decimal](https://docs.python.org/3/library/decimal.html), consultada em 12/09/2026, para `quantize` e `ROUND_HALF_UP`. As convenções de saída do Hub são definidas pelo próprio módulo.

Revisão R02 pelo próprio autor, com execução do bloco Python acima e casos de borda em Python 3.13.5. Isso não é uma execução do notebook Databricks. Revisão independente e aceite humano do piloto têm estados próprios no relatório da sprint.
