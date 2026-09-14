# ADR-0014 — Micromodelo é artefato de domínio, não tipo do Hub

Data: 2026-09-14
Status: Aceito pelo usuário em 2026-09-14; integração da MM00 pendente
Autor: ChatGPT

## Contexto

O Hub possui taxonomia fechada de seis tipos de objeto. O micromodelo combina especificação de negócio, evidências, score, estudo, validação e publicação posterior; forçá-lo a essa taxonomia criaria um sétimo tipo e duplicaria padrões transversais já existentes.

## Decisão

Tratar micromodelo como artefato de domínio que consome skills, prompts, notebooks, scripts e outros recursos do Hub. Não criar `hub_padroes/micromodelo` como novo tipo transversal.

Micromodelo também permanece distinto do Produto de Dados: o primeiro representa a definição analítica e sua evidência; o segundo é a materialização governada para consumo.

## Alternativas consideradas

- Criar sétimo tipo do Hub — rejeitada porque quebra a taxonomia vigente e amplia validadores, templates e documentação transversal sem necessidade.
- Tratar cada micromodelo como skill — rejeitada porque o artefato analítico não é mecanismo de roteamento do Genie Code.

## Consequências

- Templates específicos ficam associados à futura skill de micromodelos.
- O Hub permanece menor e coerente.
- Projetos reais podem evoluir sem alterar a taxonomia da biblioteca.

## Referências

- `ambiente_fonte/.assistant/hub_padroes/skill/template.md`
- `ambiente_fonte/.assistant/skills/hub-ml-criar-objeto/SKILL.md`
- `docs/sprints/micromodelos/PLANO_MESTRE.md`

## Ratificação de status — 14/09/2026

O usuário declarou: “D2: Aceito ADR-0014 a ADR-0020 sem ressalvas.” Este ADR fica aceito sem alteração do corpo decisório. O aceite não autoriza iniciar MM01 antes do merge da MM00 e do fechamento documental pós-MM00 previsto pela exceção D1-B.
