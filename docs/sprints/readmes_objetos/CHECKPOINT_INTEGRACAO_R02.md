# Checkpoint R02-I — preparação da integração

Data: 12/09/2026. Autor: ChatGPT. Estado: composição candidata em branch separada.
A autorização é preparar e verificar a integração; não é aceite editorial,
autorização de merge, publicação no Databricks ou início da R03.

## Bases verificadas

- Main/Concierge: `8744157fe9c3e0603f689fb2bcad52445e96cb41`.
- READMEs R01/R02 revisados: `5996574a337e7c878e19db9d8312c871cb4cd98f`.
- Ancestral comum: `f748c144dbb6909c7437b53498b25dd4f4854ab7`.
- Branch de composição: `codex/readmes-integracao-r02`, baseada na main.

## Entrega

A candidata reúne as duas iniciativas, preserva o conteúdo dos seis pilotos e
dos três exemplares e não aumenta a cobertura operacional. O controle das
68 pendências e o contrato `0.1.0-candidata` permanecem idênticos à R02.
Foram resolvidos quatro conflitos textuais e a colisão de numeração do ADR:
Concierge conserva ADR-0011; a proposta dos READMEs passa a ADR-0012.

A etapa dos READMEs e as três etapas do Concierge convivem com as quatro
comuns no gate. Os comandos de publicação não foram executados. O Manual
foi combinado na fonte e suas cópias sincronizadas; simulado somente por render.

Consulte [registro e evidências](INTEGRACAO_R02.md) e
[matriz nominal](MATRIZ_INTEGRACAO_R02.md). O relatório e os logs devem indicar
separadamente verificações locais e remotas. Presença de workflow não comprova
execução. Os PRs anteriores permanecem disponíveis, sem rebase ou force-push.

## Próxima decisão e cuidados

Revisar a candidata e confirmar aceite editorial do template/pilotos e aceite
da integração. Antes de eventual merge, reconfirmar a main e o estado da CI:
se as bases mudarem, esta evidência não certifica a nova combinação. Não mesclar
simultaneamente os PRs antigos e a candidata acumulada: ambos carregam as
mesmas alterações documentais. Encerrar/substituir PRs e fazer merge exigem
decisão explícita; nenhuma dessas ações foi tomada nesta etapa.

Após o aceite, registrar ratificação editorial e avaliar o congelamento 1.0 de
forma coerente no contrato, controles e exemplares. A R03-A continua aguardando
nova autorização. Auditoria independente e testes no ambiente destino permanecem
pendentes. Não confundir aprovação técnica desta composição com homologação de
roteamento Genie Code, Spark Connect, permissões, custos ou produção.

## Continuidade confirmada em 2026-09-12

A aprovação humana ocorreu nesta conversa; PR nº 7 integrado em `5493f7d`.
A condição “sem merge/aceite pendente” acima descreve a entrega R02-I anterior.
Veja [aceite e estabilização](ACEITE_V1.md) e [lote R03-A](RELATORIO_R03A.md).
