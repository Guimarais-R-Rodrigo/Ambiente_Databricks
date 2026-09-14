# ADR-0019 — Micromodelos consomem o Sistema de Temas; não criam tema paralelo

Data: 2026-09-14
Status: Proposto
Autor: ChatGPT

## Contexto

O repositório já possui contrato central de temas e consumidores opt-in. Criar paleta/CSS específicos para micromodelos duplicaria fonte visual e faria a nova iniciativa depender de uma fotografia ainda em evolução.

## Decisão

Manter a semântica de micromodelos independente da implementação visual e realizar a integração definitiva apenas na fase de hardening, consumindo o contrato central do Sistema de Temas vigente naquele momento.

Micromodelo não cria novo contexto visual obrigatório; README e notebook permanecem superfícies existentes com composição de domínio.

## Alternativas consideradas

- Criar tema `micromodelo` — rejeitada por confundir tipo de conteúdo com contexto visual e duplicar fonte de verdade.
- Esperar toda a frente visual antes de iniciar o framework — rejeitada porque bloqueia trabalho semântico sem necessidade.

## Consequências

- MM00–MM10 podem avançar sem fechamento visual completo.
- MM11 reconsulta a `main` antes de integrar.
- Skills/templates não hardcodam cores ou CSS.

## Referências

- `docs/decisions/ADR-0013-sistema-de-temas.md`
- `docs/sprints/sistema_temas/V07/README.md`
- `docs/sprints/micromodelos/PLANO_MESTRE.md`
