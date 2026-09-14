# MM00 — Baseline e arquitetura

## Objetivo

Registrar o estado real do repositório e congelar as fronteiras da iniciativa antes de qualquer implementação funcional.

## Baseline

- Branch: `micromodelos/mm00-baseline`.
- Base: `main` em `1b6632194f4b25afc09960c27b069c16df365ee6`.
- Sistema de Temas: V00–V07 integradas no Git; V08 ainda não iniciada neste baseline.

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

## Gate

MM01 permanece bloqueada até testes, auditoria, checkpoint, aceite explícito e merge da MM00.
