# Checkpoint V01 — aceite e integração Git

## Estado vigente — 12/09/2026

Rodrigo deu aceite explícito à V01 e solicitou testar e aplicar. O aceite
cobre o contrato, a arquitetura e a experiência especificada nesta sprint,
bem como sua integração pelo PR #10 após aprovação dos checks. A ratificação
do ADR-0013 não muda seu corpo decisório nem implementa o núcleo V02.

Para quem nunca entrou no Hub: não há nada para instalar, executar ou
reconfigurar no Databricks nesta etapa. Continue usando o Hub como antes.
O seletor de temas ainda não existe; gráficos, imagens, widgets, imports,
cálculos e Manual Técnico permanecem preservados. Os exemplos de tema
continuam sendo entradas de teste, não configurações publicadas.

Integração Git: AUTORIZADA, condicionada à validação da árvore exata. O PR #10
é o registro da efetivação, dos checks e do SHA de merge; a existência deste
documento em uma branch não prova integração. A rodada de aceite identifica
base, candidata, árvore, versões, logs e commit documental em seu artefato.
Nenhum relatório antigo é reaproveitado como aprovação da rodada nova.

Aceite do usuário: CONCEDIDO. Auditoria independente: PENDENTE. Avaliação
com usuário iniciante: PENDENTE. Databricks, Spark, widgets, Apps e AI/BI:
NÃO HOMOLOGADOS. Os casos não executados por ausência de Spark não são PASS.
A dívida editorial Node e os achados V00 não são encerrados por este aceite.
Os testes desta rodada e a conferência pelo mesmo agente não substituem
uma revisão independente. Não houve publicação nem acesso a dados reais.

Após a integração, a próxima sprint é V02; ela não está implementada por
este aceite. Sua execução deve partir da main efetiva, com fonte canônica
única, documentação operacional, regressões e checkpoint próprios.

Para desfazer uma integração, o mantenedor deve identificar o merge do
PR #10 e preparar uma reversão em branch própria, preservando alterações
posteriores e repetindo os gates antes de novo PR. Não resetar main,
fazer force-push ou publicar pacote antigo no Databricks para desfazer
uma mudança exclusivamente de contrato e documentação.

## Registro anterior da candidata — histórico, não estado vigente

O texto abaixo preserva o checkpoint anterior ao aceite. Referências a
aceite pendente ou candidata descrevem aquela rodada, não a decisão acima.

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
