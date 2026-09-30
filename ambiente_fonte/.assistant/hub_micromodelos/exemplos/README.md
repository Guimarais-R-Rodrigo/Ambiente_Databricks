# Exemplos de Micromodelos

Casos fictícios para aprender o contrato e conferir resultados sem usar dados corporativos.

## Para que serve e quando usar

Comece pelo caso de recência de contato para ver um `micromodelo.yaml` preenchido, seus dados, as classes `TRUE`, `FALSE` e `INDETERMINADO`, e o cálculo de score. O ensaio de migração demonstra comparação entre saídas legadas sintéticas.

## Como usar

No diretório do produto, execute `python hub_micromodelos/exemplos/recencia_contato/executar_exemplo.py --conferir`. O script usa somente os arquivos locais da pasta do exemplo.

## O que existe aqui

| Item | Uso |
|---|---|
| [recencia_contato/](recencia_contato/README.md) | Micromodelo fictício completo, dataset e resultado esperado. |
| [catalogo_sintetico.json](catalogo_sintetico.json) | Fixture de metadados usada pelo laboratório de execução. |
| [migracao_simulada.py](migracao_simulada.py) | Comparação local de saídas sintéticas, sem leitura institucional. |

## Limites e armadilhas

Resultados desses arquivos são ensaios E0. A fonte fictícia, a decisão humana, o MLflow e a publicação têm estados separados na especificação. Uma saída comparada ao oráculo local demonstra reprodução do cálculo, não validade estatística ou aceite de governança.

## Onde continuar

Veja o [README de recência](recencia_contato/README.md), a [biblioteca de execução](../execucao/README.md) e o [contrato JSON Schema](../contratos/micromodelo.schema.json).
