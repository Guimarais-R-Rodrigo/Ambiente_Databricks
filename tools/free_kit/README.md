# Notebooks do laboratório Free de Micromodelos

Esta pasta contém fontes de notebooks usadas pelo kit sintético do Databricks Free.
Não é a biblioteca do produto nem uma tarefa de inicialização do VS Code.

| Arquivo | Finalidade | Efeito |
|---|---|---|
| [RUN_FREE.py](RUN_FREE.py) | Executar o laboratório a partir de `product_overlay/.assistant` importado | Usa o runtime escolhido; registra capacidades e resultados sintéticos |
| [SETUP_METADATA_FREE.py](SETUP_METADATA_FREE.py) | Preparar tabela sintética de metadados | Pode criar schema/tabela quando `RUN_SETUP` for explicitamente ativado; começa desativado |

O [montador do kit](../micromodelo_free_kit.py) define o pacote e as dependências.
Confira `KIT_ROOT`, capacidades e destino antes de executar no Free. O setup
recusa placeholders e não autoriza apagar catálogo/schema ou objetos alheios.
O notebook de execução não instala dependências. Dados reais não entram neste kit.

Manutenção: editar a fonte aqui, conferir os [testes](../tests/README.md) de
Micromodelos/kit e preparar novamente o pacote autorizado. Copiar/importar não
comprova execução nem homologação. [Voltar ao catálogo](../CATALOGO.md).
