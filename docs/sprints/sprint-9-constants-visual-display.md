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

---

## Auditoria da Sprint 9 — 13 achados, todos procedentes

Rodada em sessão sem contexto. O auditor executou os 13, recuperou a saída
célula a célula via `jobs export-run`, e — o que fez a diferença — **imprimiu e
leu o HTML que as funções devolvem** em vez de aceitar a prosa. Foi de onde
saíram os quatro achados mais graves.

Ele também declarou o ponto cego com precisão: 14 saídas do tipo `mimeBundle`
(HTML renderizado e figuras Plotly) não são recuperáveis por job. **Os três
defeitos mais graves passaram por `validate_assistant` APROVADO e por
`publicar_free --verify` APROVADO** — porque nenhum portão olha para dentro do
HTML devolvido.

### Quatro afirmações minhas que o HTML desmentiu

**`display_styled` não faz o que o notebook dizia.** Eu havia escrito que ele
"destaca as duas colunas pedidas" e que "o gradiente faz o resto". O HTML
devolvido tinha **zero células destacadas e nenhum gradiente**: a regra do módulo
é realçar valor **negativo** dentro das colunas declaradas, e a fixture não tinha
nenhum negativo. Três afirmações erradas numa leitura só, e a quarta de brinde —
o `format_dict` com `"{:,.0f}"` produzia `3,375,674`, separador americano, dentro
da sprint que entrega `constants.format_br` para evitar exatamente isso.

Corrigido com uma coluna de negativos na fixture, `fmt_int` no lugar do
`format_dict`, e a prosa descrevendo o que a função faz.

**`section_header` dizia que o estilo vem de `constants.styles`.** Não vem: o CSS
está inline no módulo, e `STYLE_SECTION_HEADER` **não é usado por ninguém**. Quem
fosse trocar a identidade visual editaria aquele arquivo e não veria mudança em
cabeçalho nenhum.

**`badge_score(68)` sai amarelo, não verde.** Os cortes reais são 80 e 50; minha
prosa usava o par 62/68 para explicar a política e errava em 12 pontos — no
parágrafo que existe justamente porque o limiar não está em constante nomeada.

**O bloco do `theme_plotly` mostrava dez cores; a execução imprime oito.** O
`print` corta em 88 caracteres e a lista tem 110. Eu completei a saída para caber
na afirmação "são as dez cores" — que é verdadeira, mas a evidência ao lado dela
foi fabricada. Corrigido com uma célula que imprime `len(colorway)` e a lista
inteira, e o bloco de volta ao literal truncado.

### O inventário de duplicação estava incompleto e invertido

Eu havia registrado **2 de 12** módulos que redeclaram cor de `constants.colors`,
e chamado `visual.theme_plotly` de "contraexemplo positivo" — ele importa a
paleta, e três linhas acima redeclara `#333333`, que é o `CINZA_ESCURO` do mesmo
módulo.

Pior: eu dizia "três definições de verde de selo", sugerindo três valores. São
**três sítios e dois valores** — `constants.styles` e `visual.badge` são cópia
byte a byte um do outro. Isso muda o custo da decisão: juntar os dois é edição
sem efeito visual; alinhá-los ao `VERDE` oficial troca a cor de todos os selos.

E a dívida maior de `constants.styles` não era o hexadecimal copiado: **o módulo
inteiro é um espelho morto**. As oito constantes replicam CSS que vive inline em
cinco outros módulos, e ninguém o importa.

O inventário único, com os doze módulos e a distinção entre cópia idêntica
(onze, higiene) e valor divergente (um, decisão de produto), está em
`PLANO_HUB.md` §12.2.

### Os demais

| # | Achado | Correção |
|---|---|---|
| 5 | a docstring de `format_br` errava `fmt_delta(..., "bps")` por 10× — dentro do módulo cujo notebook auditava essa armadilha | docstring corrigida e `bps` exercitado numa célula |
| 7 | `correlation_matrix` dizia "é `toPandas()` por baixo"; o módulo não chama `toPandas()` | o cálculo é distribuído e o custo cresce com **colunas**, não linhas — amostrar ali perde precisão de graça |
| 8 | o `CATALOGO_HELPERS.md` não marcava nenhuma das duas dependências escondidas, e a tabela de exploração nem tinha a coluna | coluna `Dep.` acrescentada; `dataframe_styled` e `explainability_report` marcados `exec` |
| 9 | seis dos treze blocos eram transcrição editada, não literal | refeitos; onde a saída é longa, o corte está declarado |
| 10 | a docstring do `check_saida_colada` prometia mais rigor do que o código tem | passou a declarar as duas portas, inclusive a de 30 caracteres, por onde passa prosa inventada |
| 11 | "60 objetos" incluía os 2 exemplares de `hub_padroes` | **58 na biblioteca** (51 + 7); 60 é a contagem do validador |
| 12 | dois dos quatro chips semânticos reprovam contraste AA com texto branco, e o notebook não falava de contraste | contraste medido na célula, texto adaptado, e a regra registrada: `COR_ALERTA` e `COR_POSITIVO` são preenchimento, nunca fundo para branco |
| 13 | `display_styled` usa `Styler.applymap`, removido no pandas 3.0 | `getattr(styled, "map", ...)` com fallback; sem mudança de comportamento no 1.5.3 do Free |

### O que a auditoria confirmou intacto

Converter é mover cumprido nos 13, byte a byte — nenhum hexadecimal mudou, que
era a quebra mais silenciosa possível nesta sprint. Os 13 `__init__.py` batem com
a ferramenta, incluindo os 22 nomes de `constants/colors`. Os três valores de
escala do `format_br` conferem, e a varredura AST do ecossistema não achou
ninguém que tenha caído na armadilha. As afirmações visuais **aferíveis no
valor** se sustentam: a hierarquia do `divider` é real nas três dimensões, e a
luminância das paletas sequencial e divergente confirma o que a prosa diz.

### O ponto cego, declarado

Nada do que é pixel foi verificado — nem por mim, nem pelo auditor. O candidato
mais provável a defeito escondido é a **colisão entre o rodapé e a legenda do
`theme_plotly`**: a anotação fica em `y=-0.18` e a legenda em `y=-0.25`, com
`margin.b=60`. A afirmação central daquele notebook ("a diferença que importa é o
rodapé") depende de o rodapé estar legível.

São trinta segundos de trabalho humano com o notebook aberto, e nenhum job
substitui.

**Verificado por inspeção humana em 2026-08-17: está legível.** O rodapé aparece,
não colide com a legenda nem com o eixo, e não é cortado. Os quatro chips
semânticos estão legíveis com a escolha de texto por contraste, a hierarquia dos
quatro separadores se lê sem legenda, e a grade de distribuições mostra os dois
picos da bimodal com os títulos cabendo.

O ponto cego continua existindo como classe — nenhum portão vê pixel —, mas esta
sprint não tem defeito visual conhecido.

### Verificação depois das correções

```text
validate_assistant.py   APROVADO: 0 falha(s), 12 aviso(s)
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
notebooks               13 de 13 SUCCESS
```
