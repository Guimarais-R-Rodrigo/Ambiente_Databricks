# Framework de Micromodelos — execução por sprints

> Estado: **MM00 encerrada e integrada. MM01 corrigida após a primeira A1, com reteste técnico verde e reauditoria independente pendente; ainda não aceita nem integrada.**

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

A MM01 foi iniciada na branch `micromodelos/mm01-contrato-canonico` e reconciliada de forma fail-closed com as evoluções da `main`, inclusive as bases pós-V10 e pós-V11. A PR #51 permanece aberta, não aceita e não integrada.

A candidata contém exclusivamente o contrato canônico `micromodelo.yaml`: schema, fases/condições, proveniência, validador de referência/CI, fixtures sintéticos, suíte com **24 métodos de teste**, documentação e pacote A1. Não cria skill de micromodelos nem altera `.assistant`.

A primeira A1 independente concluiu `NAO_APTA` com cinco bloqueios. O contraditório confirmou todos como procedentes e a candidata foi corrigida para:

- validar rewind pós-`PUBLICADO` contra especificação anterior confiável por `--previous`, sem antecipar fingerprint;
- rejeitar referências auditáveis compostas apenas por whitespace/caracteres invisíveis;
- permitir limiares/pesos `PROPOSTO` antes do gate e exigir `APROVADO` a partir de `EM_VALIDACAO`;
- impedir contradição entre tratamento estruturado de `INDETERMINADO` e descrição que o converta para `FALSE`;
- exigir que `score.calibracao.evidencia_ref` resolva para experimento existente, executado e medido.

O reteste de construção das correções executou 24 métodos com `OK` e o gate estrutural com zero falhas/avisos antes de publicar os artefatos permanentes. Os mecanismos transitórios usados para aplicar as correções não permanecem na árvore da PR.

A skill roteável `hub-ml-micromodelos` continua reservada para MM04; fingerprint continua reservado para MM02; descoberta de metadata continua reservada para MM03; tracking definitivo continua reservado para MM06.

## Próximo gate

1. concluir os workflows permanentes do HEAD final corrigido;
2. executar a **reauditoria A1** em sessão independente contra esse HEAD;
3. confrontar qualquer novo achado e corrigir somente se procedente;
4. sincronizar o bloco MM01 do `CHANGELOG.md` com a A1/correções antes do merge, preservando byte a byte o histórico anterior;
5. solicitar aceite final e integrar a PR #51.

**MM02 permanece bloqueada.**
