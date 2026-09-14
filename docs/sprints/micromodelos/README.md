# Framework de Micromodelos — execução por sprints

> Estado: **MM00 encerrada e integrada. MM01 materializada na PR #51 e tecnicamente pronta para auditoria A1; ainda não aceita nem integrada.**

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
- PR #43 integrada em `36e89515a46df24f41deea4791b109f5a1f938f2`;
- Q-01 fechado pela PR #49;
- fechamento pós-MM00 integrado em `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5`;
- CI geral e V00–V09 pós-merge concluídos com sucesso.

A exceção D1-B terminou com o fechamento de Q-01 e não se propaga às próximas sprints.

## Estado da MM01

A MM01 foi iniciada a partir de `ec52d379f75dc6906a2d7e8f86fb69608a1c54d5` na branch `micromodelos/mm01-contrato-canonico` e reconciliada com a `main` pós-V10 `a9480391c78e2402986885db0ce08b10e0619a1a`.

A PR #51 contém exclusivamente o contrato canônico `micromodelo.yaml`: schema, fases/condições, proveniência, validador de referência/CI, fixtures sintéticos, suíte com 17 métodos de teste, documentação e pacote A1. A candidata foi endurecida contra chaves duplicadas, IDs duplicados, ambiguidade semântica cosmética, linguagem probabilística sem calibração, coleções materiais vazias em validação, status de publicação incompatível e tentativa de ampliar o catálogo pela CLI.

A skill roteável `hub-ml-micromodelos` continua reservada para MM04; fingerprint continua reservado para MM02; descoberta de metadata continua reservada para MM03.

## Próximo gate

Executar a auditoria A1 da PR #51 em sessão independente, confrontar os achados e só então preparar o aceite final da MM01. **MM02 permanece bloqueada.**
