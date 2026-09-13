# V05 — evidências e limites de teste

## Rodadas anteriores

| Execução | Árvore/commit examinado | Resultado |
|---|---|---|
| 34733481224 | 5245c0f | 30 de 31 casos V05 aprovados; falha na frase explícita do README. Rodada reprovada. |
| 34733554922 | a45ebd6 | 31/31 V05, 329/329 temas e 12/12 legado visual aprovados; validador reprovado por links, contrato do exemplo, falta de saída e contagens. Rodada reprovada. |

Os 329 casos incluem os 31 da V05. Não somar reexecuções ou subTest como novos casos.
As bibliotecas ipywidgets foram reais no runner; não houve browser Databricks.

## Retomada em 13/09/2026

A main avançou com R07 para `b73bbb91961f9ba5f9031d648c42ec0891b63347`.
A composição precisa repetir os gates; resultados anteriores não são sua aprovação.
O snapshot auxiliar por workflow foi recusado antes da criação do arquivo.
A branch auxiliar permaneceu sem mudanças. Nenhuma proteção foi relaxada.

## Bateria necessária

Preservar os 31 testes iniciais e acrescentar regressões para arquivo preexistente
após falha, destino inválido, escrita incompleta, erro de renderização, campos ainda
não aplicados, controles sem efeito e comportamento real dos botões Python.
Executar V00, V01–V05, CI geral, conferência de API, fonte/espelho, documentação,
exemplo sintético e preservação dos arquivos da R07 na árvore final.

## Evidência que continua faltando

Runtime e interface Databricks, navegador, teclado/leitor de tela, zoom, contraste
percebido, p95 da prévia, reinício de sessão, autorização do diretório e uso por
iniciante sem ajuda não foram homologados. Nenhum PASS Python substitui esses gates.

[Estado e bloqueios](CHECKPOINT_V05.md)
