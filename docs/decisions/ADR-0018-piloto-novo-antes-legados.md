# ADR-0018 — Provar a esteira com caso novo antes de migrar legados

Data: 2026-09-14
Status: Proposto
Autor: ChatGPT

## Contexto

Usar micromodelos legados como primeiros consumidores poderia fazer a nova arquitetura herdar acidentalmente convenções antigas e levar a migração em massa antes de saber se YAML, skill, tracking, handoff e documentação funcionam bem em um caso criado do zero.

## Decisão

Exigir um piloto greenfield ponta a ponta antes da migração. A migração dos legados só começa após homologação técnica, criação/validação/publicação autorizada de um micromodelo novo, hardening do framework e congelamento da V1.

## Alternativas consideradas

- Migrar um legado como piloto — rejeitada porque mistura validação da nova esteira com compatibilidade histórica.
- Migrar todos em paralelo ao desenvolvimento — rejeitada por ampliar retrabalho caso o framework mude.

## Consequências

- `hub-ml-padronizar-micromodelo` e seu prompt são adiados até MM12.
- O piloto novo deve medir também experiência do cientista e lacunas do framework.
- Migração conservadora e modernização funcional serão fases separadas.

## Referências

- `docs/sprints/micromodelos/PLANO_MESTRE.md`
