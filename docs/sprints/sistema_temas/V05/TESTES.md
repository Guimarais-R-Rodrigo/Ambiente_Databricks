# V05 — evidências e limites de teste

## Reconciliação R08 — 13/09/2026

A main `d5945e04328609878f63857cc15cf5e5039b3e75` foi incorporada à branch
V05 pela composição `5cace7f876b2bdb2a1eecaa73e3f7958dfd2764e`.
O conflito consistia nas contagens do README, que foram atualizadas no commit
`57062e86e0741e88fcd0b30c902ff57ece4be1c8` a partir da execução real.
Nenhuma asserção ou implementação foi alterada nesta reconciliação.

| Execução | Composição | Resultado e alcance |
|---|---|---|
| 34761074646 | Head 5cace7f; checkout de teste eacbe44 | 31/31 V05, 345/345 temas e 12/12 legado visual aprovados; FAILURE por 14 divergências de contagem no README. |
| 34761250018 | Head 57062e8 | Workflow V05 completo com success após atualização das contagens. Não é homologação Databricks. |
| 34761250014 / 34761250034 / 34761250027 | Head 57062e8 | Workflows V00, V01 e V02 com success. |
| 34761250016 | Head 57062e8; checkout de teste 1d83a94 | CI geral FAILURE: oito de nove etapas passaram; falta a seção do objeto no inventário do Manual Técnico. Validador estrutural: zero falhas e zero avisos. |

Os 345 casos do primeiro run incluem os 31 originais V05 e as 16 regressões
adicionais, além de V01–V04. Não somar as execuções repetidas. Essa rodada
usou Python 3.12.14, pandas 3.0.5, Plotly 7.0.0 e ipywidgets 8.1.9 no runner.
Os seis casos de UI pulados no CI geral permanecem SKIP nesse run; o workflow
específico instala ipywidgets e executa os testes da interface Python.
Os sete SKIPs do gate de transição dependem de Spark e não são aprovações.

O log do CI após as contagens confirma como única falha
`test_manual_inventory_covers_current_objects`, procurando a seção
`hub_snippets.visual.theme_lab`. Não remover ou enfraquecer essa guarda.
A aprovação estrutural do pacote não substitui a completude do Manual.

A comparação main → composição confirmou somente 16 arquivos acrescentados,
sem alteração de qualquer arquivo anterior da main. A comparação candidata
anterior → composição preservou todos os arquivos próprios V05. A revisão de
README subsequente mudou somente contagens e o newline final; prosa preservada.
As cópias previamente geradas do objeto foram herdadas byte a byte por seus
blobs. Não foi executado um novo render completo, smoke Databricks, benchmark,
publicador ou auditoria independente nesta rodada.

Esta documentação é posterior aos runs acima. Não a apresentar como testada
por eles: o próximo head documental precisa de sua própria execução remota.

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
