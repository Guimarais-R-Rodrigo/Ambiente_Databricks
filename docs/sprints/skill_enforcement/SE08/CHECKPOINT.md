# SE08 — checkpoint para certificação local

**Estado:** repo-side consolidado para materialização/certificação; ainda não é RC.

## Autoridade e base

Fonte primária: estado publicado no GitHub e documentação canônica do SEF.
A implementação SE08 foi construída sobre `main@c70f5af9...` e consolidada em
branch própria. Antes de executar qualquer comando local, resolver o HEAD real de
`sef/SE08-operacao`, conferir `origin/main`, merge-base, ahead/behind e worktree.

Se o HEAD divergir deste checkpoint, auditar o delta antes de reutilizar qualquer
evidência.

## Escopo já concluído repo-side

- perfil cumulativo SE08 no certifier;
- subgate SE08 no `ci_local.py`;
- contratos/policy integrados ao validator geral;
- leitura única/fail-closed da policy;
- regressões SE08 e policy I/O;
- documentação operacional de template, skills, policy e Manual;
- gate corporativo e rollback integrados ao runbook/checklist;
- pasta documental mínima da SE08.

As duas skills explicitamente citadas pelo Plano Mestre não receberam alterações
gratuitas: criar-objeto já possui preflight L2 e permanece L2 global; auditoria
já consome policy/Receipt/verifier e permanece na classificação vigente.

## Estado intencional antes do gate local

`ambiente_fonte/` foi atualizado, mas `Novo_Ambiente_Simulado/` não foi
editado manualmente. O primeiro passo local é rodar o renderer canônico,
inspecionar o delta derivado e versioná-lo de forma mecânica.

O snapshot numérico do README raiz também deve ser reconciliado somente a partir
da saída real do validador no checkout completo. Não adivinhar contagens.

## Dívidas carregadas

- SE06 24/25; A1-R4 NOT_RUN; DoD incompleto; FULLY_CERTIFIED=false;
- SE07 com residual aceito; SE07_FULLY_CERTIFIED=false;
- storage cleanup histórico FAIL 8/9;
- WinError32 não reproduzido na recertificação final ≠ corrigido;
- criar-objeto L2 global.

## Critério de parada

A etapa local pode materializar derivado, atualizar snapshot verificável,
investigar/corrigir defeitos repo-side pertencentes à SE08 e executar os gates.
Ela deve parar antes de:

- Free/Genie se o gate local não estiver fechado;
- abertura de PR sem release candidate;
- qualquer promoção ao trabalho;
- mudança de policy/nível que exija decisão humana nova.

O procedimento detalhado está em [RUNBOOK_LOCAL.md](RUNBOOK_LOCAL.md).
