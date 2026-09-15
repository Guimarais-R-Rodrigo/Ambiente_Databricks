# Framework de Micromodelos — execução por sprints

> Estado: **MM00 encerrada e integrada. MM01 corrigida após duas auditorias A1 `NAO_APTA`; reteste de construção da segunda correção verde; terceira A1 independente pendente. MM01 ainda não aceita nem integrada.**

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

Uma auditoria que encontra bloqueios não é reclassificada depois da correção. O resultado fica versionado como evidência histórica e a árvore corrigida volta para auditoria independente.

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

A candidata contém exclusivamente o contrato canônico `micromodelo.yaml`: schema, fases/condições, proveniência, validador de referência/CI, fixtures sintéticos, suíte com **26 métodos de teste**, documentação e pacote A1. Não cria skill de micromodelos nem altera `.assistant`.

### Primeira A1

A primeira auditoria independente concluiu `NAO_APTA` com cinco bloqueios. Todos foram confirmados como procedentes e corrigidos: continuidade pós-`PUBLICADO` por snapshot anterior confiável, provas auditáveis materialmente preenchidas, `PROPOSTO` permitido pré-gate, política de `INDETERMINADO` mais forte e integridade referencial de calibração.

### Segunda A1

A reauditoria sobre o head corrigido também concluiu `NAO_APTA`, com três novos bloqueios procedentes:

- marcas Unicode `M*` ainda podiam satisfazer provas auditáveis;
- políticas de ausência/publicação ainda dependiam parcialmente de inferência sobre prosa normativa;
- semântica probabilística podia ser escondida por sinônimos não cobertos por regex.

A segunda correção mudou o desenho para eliminar essas classes de bypass:

- materialidade textual exige positivamente letra/número Unicode após NFKC;
- ausência de evidência e política de publicação de `INDETERMINADO` usam somente campos estruturados para comportamento executável;
- `score.tipo_semantica` é a autoridade exclusiva sobre natureza probabilística; `score.semantica` livre foi removido do schema;
- `score.normalizacao` passou a contrato estruturado com método/referência/proveniência.

O workflow transitório `34912665666` executou **26 métodos com `OK`** e o gate estrutural com zero falhas/avisos antes de publicar o commit permanente `f46b69790fc23ac6c3ebfa633053a3acb6f9ed1a`. Os mecanismos transitórios não permanecem na árvore.

Os resultados das duas A1 estão versionados separadamente e continuam historicamente `NAO_APTA`.

A skill roteável `hub-ml-micromodelos` continua reservada para MM04; fingerprint continua reservado para MM02; descoberta de metadata continua reservada para MM03; tracking definitivo continua reservado para MM06.

## Próximo gate

1. congelar o HEAD documental pós-segunda A1 e obter todos os workflows permanentes verdes;
2. executar uma **terceira A1 independente** sobre esse HEAD, sem usar os relatórios anteriores como prova;
3. confrontar qualquer novo achado e corrigir somente se procedente;
4. sincronizar o bloco MM01 do `CHANGELOG.md` antes do merge, preservando byte a byte o histórico anterior;
5. revalidar a árvore exata após o changelog;
6. solicitar aceite final e integrar a PR #51.

**MM02 permanece bloqueada.**
