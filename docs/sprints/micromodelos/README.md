# Framework de Micromodelos — execução por sprints

> Estado: MM00 em fechamento. Esta sprint é apenas documental e arquitetural; não cria skill, helper, micromodelo, tabela, run MLflow ou publicação.

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

Na MM00, D1-B foi autorizada exclusivamente para diferir a entrada do `CHANGELOG.md`, e D2 aceitou sem ressalvas ADR-0014 a ADR-0020. Falta o aceite final da MM00, a revalidação da árvore exata e o merge. Após o merge, o fechamento documental de Q-01 deve ocorrer antes do início efetivo da MM01.
