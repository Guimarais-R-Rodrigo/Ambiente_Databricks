# Framework de Micromodelos — execução por sprints

> Estado: **MM00 encerrada e integrada. MM01 é a próxima sprint e não foi iniciada.**

## Objetivo

Construir uma esteira rastreável e auditável para descobrir, especificar, estudar, validar, publicar e, somente após um piloto novo e o congelamento da V1, migrar micromodelos.

O repositório usa somente fixtures e placeholders. O catálogo real do trabalho é representado aqui por `<CATALOGO_PRODUTO>` e o binding para nomes reais ocorre apenas no workspace autorizado.

## Fases

- MM00–MM06: fundação do framework.
- MM07–MM08: pacote departamental e homologação no trabalho.
- MM09–MM10: primeiro micromodelo novo e prova ponta a ponta.
- MM11: hardening, visual e monitoramento quando disponíveis; freeze V1.
- MM12: migração conservadora dos legados.
- MM13: catálogo, impacto e fechamento.

## Regra de avanço

`implementar → testar → auditar → corrigir → retestar → documentar → checkpoint → aceite → merge`

## Estado da MM00

A MM00 congelou baseline, arquitetura, reuso, riscos, dependências e fronteiras de governança sem alterar funcionalmente o produto `.assistant`.

- auditoria A1 executada: `APTA_COM_CORRECOES`;
- M-01 corrigido;
- D1-B autorizada e posteriormente consumida no fechamento pós-merge;
- ADR-0014 a ADR-0020 aceitos sem ressalvas;
- candidata final aprovada em CI geral, V00, V01 e V02;
- PR #43 integrada em `36e89515a46df24f41deea4791b109f5a1f938f2`;
- Q-01 fechado imediatamente após o merge por entrada estritamente aditiva no `CHANGELOG.md`, preservando o histórico anterior.

A exceção D1-B terminou com o fechamento de Q-01 e não se propaga às próximas sprints.

## Próximo passo

A próxima sprint prevista é **MM01 — contrato canônico `micromodelo.yaml`**.

MM01 não foi iniciada por este fechamento. O início de MM01 deverá partir da `main` já contendo a MM00 e seu fechamento documental, seguindo novamente a regra de branch/PR/testes/auditoria/checkpoint.
