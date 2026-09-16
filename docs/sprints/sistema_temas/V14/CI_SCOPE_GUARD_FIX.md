# Correção do guard de escopo — V14 S1

Data: 2026-09-16

## Problema observado

Após a integração da V14 S1, o teste `test_ci_diff_stays_inside_s1_allowlist` passou a ser executado por suítes agregadas em pull requests de outras frentes, porque vários workflows usam descoberta global `test_temas*.py`.

Como o teste verificava apenas `GITHUB_ACTIONS=true` e excluía `push` da `main`, ele aplicava a allowlist específica da S1 também a PRs que não eram da V14 S1. Isso produziu falsos failures em frentes independentes, incluindo a SE01 do Skill Enforcement Framework.

## Correção

O guard agora segue o padrão já adotado pela V14 S0:

- continua inativo fora do GitHub Actions;
- continua inativo em `push` da `main` já integrada;
- resolve a branch ativa por `GITHUB_HEAD_REF` ou `GITHUB_REF_NAME`;
- aplica a allowlist somente quando a branch ativa começa por `codex/temas-v14-s1`;
- em qualquer outra branch, o teste é `skipped`, não `PASS` forçado.

Foi acrescentado um teste unitário de escopo que verifica explicitamente:

- branch V14 S1 → guard ativo;
- branch SE01 → guard inativo;
- branch V13 → guard inativo;
- branch da própria correção → guard inativo;
- `push` da `main` → guard inativo.

## Limites

Esta correção não altera:

- matriz de ownership;
- modelo operacional;
- política de autorização;
- estado A11-01;
- issue #57;
- qualquer comportamento Databricks;
- V14 S2;
- código ou contrato da SE01.

O objetivo é exclusivamente restaurar o isolamento correto da guarda de escopo da S1, preservando seu fail-closed na branch à qual ela pertence.
