# MM00 — contexto para auditoria independente A1

## Escopo

Auditar a candidata da MM00 do Framework de Micromodelos na branch `micromodelos/mm00-baseline` / PR #43.

A sprint afirma entregar somente arquitetura e documentação: Plano Mestre MM00–MM13, inventário, matrizes, ADRs propostos, testes/checkpoint e reconciliação do contexto canônico. Não deveria existir mudança funcional em `ambiente_fonte/.assistant/`.

## Arquivos que o auditor pode ler

- `CLAUDE.md` e regras relevantes em `.claude/rules/`;
- `docs/decisions/README.md` e ADR-0014 a ADR-0020;
- `docs/sprints/README.md`;
- `docs/sprints/micromodelos/**`;
- implementações/READMEs atuais dos componentes citados pela MM00, somente para verificar afirmações de reuso e fronteira;
- documentos vigentes do Sistema de Temas necessários para verificar o baseline V07.

## Não ler antes de formar os achados

- `CHANGELOG.md`;
- `docs/auditoria/2026-09-14_micromodelos-mm00/` além deste contexto e do prompt;
- comentários/discussão da PR;
- histórico Git (`git log`, `git show`, diffs de commits anteriores).

`git status`, `git ls-files`, leitura da árvore atual e comparação nominal branch/base são permitidos.

## Somente leitura

Não editar, commitar, publicar, executar operações persistentes ou acessar dados externos/corporativos. Experimentos devem usar cópia temporária ou inspeção estática.

## Baseline declarado pela sprint

- base de abertura: `1b6632194f4b25afc09960c27b069c16df365ee6`;
- V00–V07 do Sistema de Temas integradas no Git; V08 ainda não iniciada no baseline;
- nenhum artefato específico de micromodelo existia na `main` segundo a busca realizada;
- ADR-0014 a ADR-0020 permanecem propostos, não aceitos;
- MM01 permanece bloqueada.

O auditor deve verificar essas afirmações e descartar qualquer uma que não possa ser sustentada pela árvore acessível.
