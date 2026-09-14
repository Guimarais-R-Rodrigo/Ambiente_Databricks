# ADR-0020 — Fontes de micromodelos ficam no catálogo corporativo configurado

Data: 2026-09-14
Status: Proposto
Autor: ChatGPT

## Contexto

A missão de micromodelos quer construir características a partir de Produtos de Dados oficiais, reduzindo dependência de fontes avulsas. O nome real do catálogo não deve ser versionado neste repositório por política de sanitização.

## Decisão

Restringir, por padrão, a descoberta e seleção de fontes ao catálogo de Produtos de Dados configurado no ambiente de trabalho, representado no Git por `<CATALOGO_PRODUTO>`.

A descoberta será metadata-first e declarará o escopo efetivamente visível. Fonte fora desse catálogo exige decisão humana explícita e não será buscada silenciosamente.

## Alternativas consideradas

- Pesquisar todos os catálogos acessíveis — rejeitada porque amplia escopo, risco e inconsistência com a missão.
- Hardcode do nome real no Git — rejeitada pela política de sanitização.

## Consequências

- MM03 deve receber/configurar o binding no ambiente autorizado.
- Fixtures usam nomes sintéticos.
- Ausência por permissão não pode ser tratada como inexistência do objeto.

## Referências

- `CLAUDE.md`
- `docs/sprints/micromodelos/PLANO_MESTRE.md`
