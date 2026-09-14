# MM00 — contexto para auditoria independente A1

## Escopo

Auditar a candidata da MM00 do Framework de Micromodelos na branch `micromodelos/mm00-baseline` / PR #43.

A sprint afirma entregar somente arquitetura e documentação: Plano Mestre MM00–MM13, inventário, matrizes, ADRs propostos, testes/checkpoint e reconciliação do contexto canônico. A MM00 não deveria criar alteração funcional própria em `ambiente_fonte/.assistant/`.

## Arquivos que o auditor pode ler

- `CLAUDE.md` e regras relevantes em `.claude/rules/`;
- `docs/decisions/README.md` e ADR-0014 a ADR-0020;
- `docs/sprints/README.md`;
- `docs/sprints/micromodelos/**`;
- implementações/READMEs atuais dos componentes citados pela MM00, somente para verificar afirmações de reuso e fronteira;
- documentos vigentes do Sistema de Temas necessários para verificar o estado V08 reconciliado.

## Não ler antes de formar os achados

- `CHANGELOG.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/` além deste contexto e do prompt;
- comentários/discussão da PR;
- histórico Git (`git log`, `git show`, diffs de commits anteriores).

`git status`, `git ls-files`, leitura da árvore atual e comparação nominal branch/base são permitidos.

## Somente leitura

Não editar, commitar, publicar, executar operações persistentes ou acessar dados externos/corporativos. Experimentos devem usar cópia temporária ou inspeção estática.

## Linha do tempo que o auditor deve verificar

- base de abertura da MM00: `1b6632194f4b25afc09960c27b069c16df365ee6`;
- na abertura, V00–V07 do Sistema de Temas estavam integradas;
- durante a execução, V08 foi integrada na `main` pelo commit `622d2c962a80998cf990b57036f7ae503bfc0458`;
- a branch MM00 foi reconciliada com essa `main` no merge `e322e73fc0dc73c3081c99662ac29cb7721add67`;
- nenhum artefato específico de micromodelo existia na `main` de abertura segundo a busca realizada;
- ADR-0014 a ADR-0020 permanecem propostos, não aceitos;
- MM01 permanece bloqueada.

A presença dos arquivos funcionais V08 na branch reconciliada não deve ser atribuída à MM00 se forem idênticos à `main` vigente. O auditor deve avaliar o diff efetivo da iniciativa contra a `main` atual, não apenas contra a base histórica V07.

O auditor deve verificar todas essas afirmações e descartar qualquer uma que não possa ser sustentada pela árvore acessível.
