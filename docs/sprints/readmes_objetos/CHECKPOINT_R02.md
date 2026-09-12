# Checkpoint R02 — piloto de seis READMEs

Data: 12/09/2026. Autor: ChatGPT. Estado: entrega candidata para revisão.
Autorização recebida: seguir para o piloto proposto após a entrega R01.
Isso autoriza produzir e verificar a R02, não presume aceite editorial final.

## Atualização — revisão de fechamento em 12/09/2026

Os seis textos foram revistos e ajustados sem alterar o contrato candidato.
Consulte [revisão e alterações](REVISAO_FECHAMENTO_R02.md),
[rubrica por objeto](RUBRICA_FECHAMENTO_R02.json) e
[diagnóstico de integração](DIAGNOSTICO_INTEGRACAO_R02.md).
A main recebeu o Concierge em `8744157`; há quatro conflitos textuais com a
R01 e uma colisão de número ADR. Nenhuma integração foi executada. O ADR dos
READMEs citado abaixo é `ADR-0011-readmes-de-objeto.md`, distinto do Concierge.
O aceite humano, a revisão independente e o congelamento 1.0 permanecem pendentes.
As seções seguintes preservam a base e o escopo da entrega original da R02.

## Base e isolamento

Base de conteúdo: `af1efd14f2a688d3d3cc816ef85f5f1755e8afec`, R01.
Árvore da base: `fa56632456b795a1f0ea572274f428b876f713bd`.
Branch R02: `codex/readmes-r02`; depende de `codex/readmes-r01`, ainda em revisão.
A `main`, o PR antigo de R01-A e os arquivos do Concierge não foram promovidos
ou substituídos. Nenhum merge, force-push ou deploy faz parte desta entrega.

O histórico Git completo foi recuperado por bundle gerado em workflow
read-only, com credenciais de checkout desabilitadas. Não foi enfraquecida a
guarda que recusa histórico incompleto. Workflows e partes transitórias usados
na recuperação/integração são removidos da árvore de entrega; commits de
preparação permanecem no histórico com propósito identificado.

## Conteúdo e controle de deriva

Os seis pilotos são `train_xgboost`, `isolation_forest`, `pit_join`, `format_br`,
`quick_profile` e `eda_rapida`. Somente suas seis dispensas foram retiradas do
controle. São seis documentos operacionais e três exemplares já existentes,
não nove novos helpers. Os demais 68 objetos continuam pendentes.

O contrato permanece `0.1.0-candidata`; a decisão de congelá-lo depende da
avaliação dos seis textos. O ADR-0011 continua proposto. O estado histórico da
R01 não foi reescrito. Mudanças de navegação e interpretação estão na matriz;
nenhuma mudança executável foi feita nos helpers ou nos notebooks existentes.

## Evidência e limites de aceite

Consulte [relatório](RELATORIO_R02.md), [matriz](MATRIZ_ALTERACOES_R02.md),
[achados](ACHADOS_R02.md) e [evidências estruturadas](EVIDENCIAS_R02.json).
Os logs identificam ambiente, testes aprovados, testes pulados e limitações.
A conferência dos textos foi feita pelo autor; não há auditoria independente.

Os exemplos originais do Databricks não foram reexecutados como notebooks.
Não houve interação real Genie Code nem escrita da tabela de eda_rapida.
Testes sintéticos portáveis não homologam Databricks, Spark Connect, Unity
Catalog, permissões, custo ou produção. Fontes oficiais não substituem esses
ensaios. Saídas históricas e blocos coláveis foram preservados literalmente.

## Próxima decisão

Parar depois da R02. O usuário avalia linguagem, adequação e utilidade dos
seis READMEs. Ajustes editoriais devem ser reconciliados no piloto e, quando
necessário, no template e nos exemplares, antes de congelar a versão 1.0.
Somente com nova autorização iniciar R03. Não usar aprovação de CI como
aceite humano, autorização de merge ou autorização de publicação.
