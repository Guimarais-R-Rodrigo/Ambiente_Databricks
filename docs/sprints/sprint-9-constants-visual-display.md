# Sprint 9 — `constants`, `visual` e `display`

Data: 2026-08-17 · Executor: Claude · Escopo: os 13 objetos que **não recebem
dados**. Com eles, **a biblioteca inteira está convertida**: 60 pastas de objeto.

Estes usam a segunda variante do template — mostrar o valor, mostrar o efeito
renderizado, explicar a decisão de design. Os movimentos de "erro acontecendo" e
"contrato de fixture" não se aplicam: `constants/colors` tem 22 constantes e zero
funções.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 12 aviso(s)
                        60 pastas de objeto
                        60 pares de contrato de saída · 60 de entrada
                        saída colada: 49 notebooks com bloco real, 12 sem
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
smoke test (job real)   129 verificações | 122 PASS | 0 FAIL | 7 opcionais ausentes
notebooks               13 de 13 SUCCESS
```

Os 12 avisos continuam sendo a dívida nomeada em §12.1 do plano. Nenhum é desta
sprint.

## Duas coisas que não rodam no serverless, por caminhos diferentes

**`display/dataframe_styled` precisa de `jinja2`** — e é o **segundo caso de
dependência escondida** da biblioteca. O módulo não importa `jinja2` em lugar
nenhum; ela entra por `df.style`, que o pandas delega na hora da chamada. O smoke
test importa com `PASS` e o notebook morre.

O primeiro caso foi o `tabulate`, exigido por `DataFrame.to_markdown()` em
`ml.explainability_report`. Dois casos deixam de ser coincidência: **o pandas tem
várias funções que delegam a biblioteca opcional em tempo de chamada**, e nenhuma
análise de import de topo as encontra. As duas estão registradas em
`requirements-optional.txt`.

**`display/correlation_matrix` usa `pyspark.ml` clássico**, que o Spark Connect
não expõe:

```text
Py4JError: An error occurred while calling
None.org.apache.spark.ml.feature.VectorAssembler
```

Aqui não é biblioteca ausente — é API da plataforma que o compute serverless não
oferece. O módulo importa normalmente; falha ao instanciar. É a terceira variação
do mesmo tema desta fase: **importável não é executável**, e as três causas foram
diferentes (biblioteca ausente, dependência delegada, API da plataforma).

Foi para o bloco canônico, com o motivo verificado, e virou linha na matriz de
`free-vs-trabalho`.

## Três duplicações de cor, e uma que faz certo

A conversão expôs um padrão que ninguém tinha olhado de frente:

| Onde | Verde de selo | Importa de `constants.colors`? |
|---|---|---|
| `constants.colors` | `VERDE = #8DC63F` | é a origem |
| `constants.styles` | `STYLE_BADGE_OK` com hex copiado | **não** — o arquivo não tem uma linha de `import` |
| `visual.badge` | `#2E7D32`, cor diferente das outras duas | **não** |
| `visual.theme_plotly` | usa `PALETA_CATEGORICA` | **sim** |

São **três definições de "verde de selo"** convivendo. E `constants.styles`
repete `#005CA9` e `#F8F9FA` em vez de importar `AZUL_CAIXA` e `BG_SECTION` — de
modo que uma mudança de identidade visual feita em `colors.py` não alcançaria os
cabeçalhos.

Cada uma está registrada no notebook do objeto, como o template manda. Unificar
muda o que já está publicado: é etapa 2, e precisa de alguém decidindo qual verde
é o certo.

## O que os notebooks ensinam

**`format_br` tem duas armadilhas de escala, e a segunda é pior.** `fmt_pct(92.8)`
devolve `9280,0%` — absurdo, alguém percebe. `fmt_pct(0.928, input_scale="percent")`
devolve **`0,9%`**, que é plausível, entra no relatório e vira decisão.

E `fmt_delta` tem a mesma pegadinha com um agravante: a unidade "pp" sugere que se
passe pontos percentuais, mas ele espera **razão**. Passar `2.4` pensando em
"2,4 pp" devolve `+240,0 pp`. Descobri isso escrevendo o próprio exemplo — a
primeira versão do notebook passava 2.4.

**`distribution_grid` mostra por que média não basta.** As três variáveis
sintéticas têm médias de 49,8 / 1.984,9 / 45,5, e a tabela não distingue nenhuma
das formas. A bimodal tem média **45,5**, que cai exatamente no vale entre os dois
picos: um valor que quase nenhum cliente tem, descrevendo uma população que não
existe.

**`index_generator` preserva a numeração original ao filtrar.** Pedidas as etapas
1, 3, 4 e 8, o índice mostra 1, 3, 4 e 8 — não 1, 2, 3, 4. Renumerar daria um
índice mais bonito e destruiria a informação: o que falta é tão informativo
quanto o que está lá.

## Limpeza remota

Treze arquivos planos removidos explicitamente antes do `--verify`, que fechou
com 0 obsoletos.

## O que fica para depois

| Item | Por quê |
|---|---|
| As três definições de verde de selo | etapa 2; unificar muda o publicado e precisa de decisão de produto |
| `constants.styles` sem importar `colors` | idem |
| Limiares de `badge_score` sem constante nomeada | são política, e política merece nome — etapa 2 |
| Dívida de saída colada: 12 notebooks | §12.1 do plano |
