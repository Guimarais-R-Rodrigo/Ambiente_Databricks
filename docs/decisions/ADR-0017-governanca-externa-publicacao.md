# ADR-0017 — Governança externa permanece autoridade de publicação

Data: 2026-09-14
Status: Proposto
Autor: ChatGPT

## Contexto

O ambiente de trabalho possui processo e skills institucionais próprios para gerar, validar e publicar Produtos de Dados. Copiar esse catálogo de regras para o Hub criaria duas fontes de verdade e exigiria sincronização permanente.

## Decisão

Manter o framework de micromodelos fracamente acoplado à governança externa. O Hub prepara um handoff estruturado de um micromodelo validado; geração, validação final e publicação permanecem sob o processo institucional vigente no ambiente autorizado.

Handles, nomes, versões e paths externos não são hardcoded no repositório. São resolvidos/confirmados durante homologação.

## Alternativas consideradas

- Copiar regras externas para a skill — rejeitada por duplicação e risco de desatualização.
- Gerar/publicar diretamente pelo Hub — rejeitada por ampliar autoridade e misturar domínio analítico com governança institucional.

## Consequências

- O contrato `GEGOD_HANDOFF` citado nas conversas será tratado no Git por nome genérico de handoff de governança; binding real fica no ambiente de trabalho.
- Mudança nas regras externas não deve exigir reescrever a metodologia interna, exceto se o contrato de handoff mudar materialmente.

## Referências

- `docs/sprints/micromodelos/PLANO_MESTRE.md`
