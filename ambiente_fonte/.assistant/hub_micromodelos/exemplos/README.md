# Exemplos de Micromodelos

O caso original de recência reconcilia sete pessoas: 2 `TRUE`, 1 `FALSE` e 4 `INDETERMINADO`. `migracao_simulada.py` compara saídas sintéticas; não realiza migração institucional.

Casos fictícios para aprender o contrato e conferir resultados sem usar dados corporativos.

## Para que serve e quando usar

Comece pelo caso de recência de contato para ver um `micromodelo.yaml` preenchido, seus dados, as classes `TRUE`, `FALSE` e `INDETERMINADO`, e o cálculo de score. O ensaio de migração demonstra comparação entre saídas legadas sintéticas.

## Como usar

No raiz `.assistant`, com as [dependências de execução](../execucao/README.md#preparação-por-rota) disponíveis, execute `python hub_micromodelos/exemplos/recencia_contato/executar_exemplo.py --conferir` e depois `python hub_micromodelos/exemplos/recencia_contato/conferir_entrega.py`. Os scripts usam somente os arquivos locais da pasta do exemplo e imprimem resultados, sem publicar.

## O que existe aqui

| Item | Uso |
|---|---|
| [recencia_contato/](recencia_contato/README.md) | Micromodelo fictício completo, dataset, resultado esperado e handoff sintético. |
| [catalogo_sintetico.json](catalogo_sintetico.json) | Fixture de metadados usada pelo laboratório de execução. |
| [migracao_simulada.py](migracao_simulada.py) | Comparação local de saídas sintéticas, sem leitura institucional. |

## Limites e armadilhas

Os resultados são ensaios locais com dados fictícios. Reproduzir o resultado esperado confere o cálculo do exemplo; não valida estatisticamente o micromodelo nem aprova seu uso real.

## Onde continuar

Veja o [README de recência](recencia_contato/README.md), a [biblioteca de execução](../execucao/README.md) e o [contrato JSON Schema](../contratos/micromodelo.schema.json).
