# Achados R03-B — documentação e comportamento observado

Base: `c60f1e54743dc23ed60b32ad2260b9aa6a77af0a`. Data: 2026-09-12. Autoria e revisão própria: ChatGPT.

As correções desta sprint são documentais. Os testes caracterizam comportamentos existentes, inclusive limitações, sem certificá-los como desejáveis. Os cenários Spark têm execução exigida separadamente; veja o relatório e a evidência do PR.

## B01 — Limiar não destaca células

**Objeto:** `correlation_matrix`.

A explicação prometia realce no mapa. O limiar filtra apenas strong_pairs; escala e células não mudam.

Prosa corrigida; teste compara figuras com cortes diferentes.

## B02 — Custo e ambiente

**Objeto:** `correlation_matrix`.

Texto anterior dizia custo independente das linhas e equivalência entre compute. Correlation calcula sobre linhas/colunas e Spearman ordena valores; APIs devem ser verificadas.

Prosa corrigida; nenhuma garantia generalizada de runtime.

## B03 — Descarte conjunto e escala sequencial

**Objeto:** `correlation_matrix`.

na.drop ocorre depois da seleção, excluindo linhas incompletas conjuntamente. Blues não representa força pelo módulo; correlação negativa forte é clara.

README explicita nulos, NaN, constantes, sinal e matriz quadrática; comportamento não alterado.

## B04 — Comentário numérico antigo

**Objeto:** `correlation_matrix`.

A estimativa ~0,97 está em comentário da célula sintética. Não foi recertificada como coeficiente observado.

Célula e transcrição preservadas; leitura orienta calcular o coeficiente real.

## B05 — HTML não escapado por padrão

**Objeto:** `dataframe_styled`.

A função não ativa escape HTML e pode transportar marcação de células. Destacar negativos não valida segurança.

README alerta conteúdo controlado; teste usa apenas marcação inofensiva.

## B06 — Escopo do realce e efeitos do exemplo

**Objeto:** `dataframe_styled`.

Nome inexistente em highlight_cols é ignorado; strings e tipos fora de int/float não têm o mesmo teste. O notebook instala Jinja2 e reinicia Python.

Explicações e aviso corrigidos sem mudar células executáveis.

## B07 — N e tamanho de amostra

**Objeto:** `distribution_grid`.

sample_n é teto, não quota; o helper usa smart_sample sem estratificação e coleta valores em pandas. N conta linhas coletadas, não válidos de cada coluna.

README descreve população, memória e exposição dos dados incorporados à figura.

## B08 — Histograma e resumos

**Objeto:** `distribution_grid`.

Texto prometia metade exata acima/abaixo da média e invalidava todo resumo. Bins são automáticos; histograma complementa resumos e não elimina escolhas de escala.

Prosa corrigida; número de colunas não é tratado como limite universal de legibilidade.

## B09 — Lista declarada não audita notebook

**Objeto:** `index_generator`.

A omissão de etapa era interpretada como atividade não realizada; a lista não lê células. O helper não cria links, mas isso não nega o sumário nativo.

README, notebook e Manual corrigidos; ordem, repetição e KeyError caracterizados.

## B10 — CSS e preenchimento

**Objeto:** `section_header`.

Explicação dizia STYLE_SECTION_HEADER idêntico e sem uso por ninguém. Esta função monta seu CSS sem consumi-lo; etapa inválida cai em padrão genérico.

Escopo local explicitado; sobrescrita, campos vazios e escape testados.

## B11 — Referência de cores e precedência

**Objeto:** `theme_plotly`.

A cor da fonte usa CINZA_ESCURO importado; texto anterior a descrevia como literal duplicado. A função deve preceder customizações a preservar.

Prosa corrigida; código, cores e CSS intactos.

## B12 — Estado, repetição e procedência

**Objeto:** `theme_plotly`.

Aplicação modifica a figura; rodapé pode duplicar. Registro muda a sessão; paleta retornada é referência compartilhada. A fonte declarada no exemplo diverge da geração NumPy.

README distingue os efeitos e identifica rótulo ilustrativo. Chamada e saída histórica preservadas.

## Limites remanescentes e encaminhamento

Escape de HTML na tabela, validação adicional de entradas, cores divergentes para correlação e tratamento idempotente de rodapés são mudanças funcionais ou visuais. Não foram incluídas nesta migração. Sua priorização deve considerar risco de uso e os planos de centralização visual; qualquer implementação futura precisa de autorização, revisão de consumidores e testes próprios.

Não usar esta lista como declaração de vulnerabilidade explorada: os testes de marcação usam conteúdo sintético inofensivo, sem scripts, rede ou dados reais.
