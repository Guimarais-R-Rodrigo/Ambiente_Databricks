# ADR-0017 — Governança externa permanece autoridade de publicação

Data: 2026-09-14
Status: Aceito pelo usuário em 2026-09-14; integração da MM00 pendente
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

- O contrato de handoff de governança usa nome genérico no Git; o binding para handles institucionais reais fica no ambiente de trabalho.
- Mudança nas regras externas não deve exigir reescrever a metodologia interna, exceto se o contrato de handoff mudar materialmente.

## Referências

- `docs/sprints/micromodelos/PLANO_MESTRE.md`

## Ratificação de status — 14/09/2026

O usuário declarou: “D2: Aceito ADR-0014 a ADR-0020 sem ressalvas.” Este ADR fica aceito sem alteração do corpo decisório. O aceite não delega ao Hub autoridade de publicação e não antecipa regras institucionais externas; MM01 permanece bloqueada até o merge da MM00 e o fechamento documental pós-MM00 previsto pela exceção D1-B.
