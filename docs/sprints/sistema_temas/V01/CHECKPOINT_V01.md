# Checkpoint V01 — candidata de revisão

## Estado para quem nunca entrou no Hub

O seletor de temas não está instalado. Você pode continuar usando o Hub como antes.
Esta etapa entrega contrato e documentação para revisar antes de construir a interface.
Comece pelo [guia de primeiro uso proposto](GUIA_PRIMEIRO_USO.md).

## Escopo executado

Composição da candidata anterior com main `b88a9cc`, que já integra V00, READMEs e
Concierge. Fonte única candidata em `docs/sprints/sistema_temas/V01/`, ADR-0013
proposto, verificador de manutenção e CI separado. Nenhuma mudança de aparência,
nenhuma publicação Databricks e nenhuma implementação do núcleo V02.

Os resultados pertencem ao [relatório de execução](../../../testes/sistema_temas/V01/RELATORIO_EXECUCAO.md).
O PR registra a branch e o commit efetivamente enviados. Estar nesta pasta não
significa estar na main; validação automatizada não significa aprovação do ADR.

## Pendências e próximos gates

Aceite arquitetural: PENDENTE. Auditoria independente: PENDENTE. Leitura por
usuário iniciante: PENDENTE. Runtime Databricks, Spark, widgets, Apps e AI/BI:
NÃO HOMOLOGADOS nesta sprint. A dívida editorial Node e as pendências V00
permanecem registradas, sem aprovação retroativa.

Antes de V02, revisar o ADR e o roteiro, aceitar a estratégia de configuração
completa e decidir a promoção única do contrato para o padrão do produto.
Medições de prévia e nomes de responsáveis permanecem tarefas dos ambientes
correspondentes, não decisões presumidas desta execução.

## Recuperação

Sem merge, arquivar a proposta. Após eventual merge, preparar PR de reversão
com gates, preservando mudanças posteriores. Não resetar main nem publicar
um pacote antigo para desfazer uma alteração apenas documental.

[Voltar à V01](README.md)
