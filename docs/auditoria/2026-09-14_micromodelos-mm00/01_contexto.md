# MM00 — contexto para auditoria independente A1

## Escopo

Auditar a candidata da MM00 do Framework de Micromodelos na branch `micromodelos/mm00-baseline` / PR #43.

A sprint afirma entregar somente arquitetura e documentação: Plano Mestre MM00–MM13, inventário, matrizes, ADRs propostos, testes/checkpoint e reconciliação do contexto canônico. A MM00 não deveria criar alteração funcional própria em `ambiente_fonte/.assistant/`, `Novo_Ambiente_Simulado/`, `tools/` ou workflows.

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
- o fechamento documental pós-merge da V08 levou a `main` para `55f7006c47d90ae7f760992d252b658f53a59636`;
- a MM00 foi reconciliada novamente sobre essa base no merge `edfcf58e4700ccf5d58d2befddccbd9fe50ac124` e teve seus documentos compartilhados reconciliados sem alterar o produto V08;
- os checks do head `f5e57db5c7fd1fdd21385eaa3f5f6aa07fcaa0a5` concluíram em `success` para CI geral, V00, V01 e V02 após o README raiz ser alinhado aos valores medidos de 1368 arquivos e 1859 links;
- o diff da PR contra a `main` fechada da V08 contém 21 arquivos de contexto, ADRs e documentação MM00/auditoria, sem alteração funcional própria do produto/ferramentas/workflows;
- nenhum artefato específico de micromodelo existia na `main` de abertura segundo a busca realizada;
- ADR-0014 a ADR-0020 permanecem propostos, não aceitos;
- MM01 permanece bloqueada.

## Regra para o alvo auditado

Antes de iniciar a auditoria, consulte a PR #43 e registre o SHA atual de `head` e o SHA atual de `base`. Se a `main` tiver avançado além de `55f7006c47d90ae7f760992d252b658f53a59636`, interrompa a auditoria e reporte `BASE_AVANCOU`; a candidata precisa ser reconciliada antes de o parecer ser válido.

A presença dos arquivos funcionais da V08 na branch não deve ser atribuída à MM00 quando forem herdados da `main`. O auditor deve avaliar o diff efetivo da iniciativa contra a `main` vigente, não apenas contra a base histórica V07.

O auditor deve verificar todas essas afirmações e descartar qualquer uma que não possa ser sustentada pela árvore acessível. A existência de CI verde não substitui os testes semânticos do prompt de auditoria.
