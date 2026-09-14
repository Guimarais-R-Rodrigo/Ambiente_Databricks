# MM00 — Baseline e arquitetura

## Objetivo

Registrar o estado real do repositório e congelar as fronteiras da iniciativa antes de qualquer implementação funcional.

## Baseline e reconciliação

- Branch: `micromodelos/mm00-baseline`.
- Base de abertura: `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.
- Na abertura, V00–V07 do Sistema de Temas estavam integradas no Git.
- Durante a execução da MM00, a V08 avançou em paralelo e foi integrada na `main` pelo commit `622d2c962a80998cf990b57036f7ae503bfc0458`.
- A branch MM00 foi reconciliada por merge com essa nova `main` no commit `e322e73fc0dc73c3081c99662ac29cb7721add67`.
- A integração V08 é preservada como fonte vigente do Sistema de Temas; a MM00 não altera seus arquivos funcionais.

## Entregas

- `INVENTARIO.md`
- `MATRIZ_REUSO.md`
- `MATRIZ_RISCOS.md`
- `MATRIZ_DEPENDENCIAS.md`
- `TESTES.md`
- `CHECKPOINT.md`
- ADRs da iniciativa

## Fora do escopo

MM00 não cria skill, prompt funcional, helper, template executável, consulta de dados, run MLflow, Produto de Dados, micromodelo real nem migração de legado.

## Sanitização

Arquivos versionados usam placeholders para nomes do ambiente de trabalho, por exemplo `<CATALOGO_PRODUTO>`. O vínculo com nomes reais ocorre somente no ambiente autorizado.

## Relação com V08

V08 integra o Sistema de Temas transversalmente a skills, padrões e Manual. Isso passa a ser uma dependência vigente para futuras skills do Hub, mas não transforma aparência em regra analítica. O desenho dos micromodelos continua sem tema próprio e a composição visual específica permanece adiada para a fase de hardening, quando será validada contra o contrato vigente.

## Gate

MM01 permanece bloqueada até checks verdes no head final, auditoria independente, checkpoint, aceite explícito e merge da MM00.
