# ADR-0015 — `micromodelo.yaml` como especificação canônica

Data: 2026-09-14
Status: Aceito pelo usuário em 2026-09-14; integração da MM00 pendente
Autor: ChatGPT

## Contexto

O ciclo de um micromodelo precisa manter definição de negócio, entidade, fontes, evidências, classificação, score, experimentos, validação, saída, tracking e proveniência sem depender da memória do chat ou de documentação duplicada.

## Decisão

Adotar `micromodelo.yaml` como fonte estruturada de verdade do micromodelo. A alimentação será progressiva pelas skills e execuções; edição manual permanece possível, mas não é o fluxo primário.

O contrato deverá separar afirmações descobertas, propostas/inferidas, aprovadas e medidas. README, notebook, catálogo e handoffs serão derivados ou verificados contra essa especificação, sem se tornarem fontes paralelas.

## Alternativas consideradas

- README como fonte canônica — rejeitada por ser pouco adequada a validação estrutural e automação.
- Notebook como fonte canônica — rejeitada por misturar execução, narrativa e contrato.
- Banco de metadata próprio desde o início — rejeitada por adicionar infraestrutura antes de provar a necessidade.

## Consequências

- MM01 precisa definir schema e máquina de estados.
- Resultados não executados devem permanecer pendentes.
- O arquivo não armazenará histórico crescente de runs; isso pertence ao backend de tracking.

## Referências

- `ambiente_fonte/.assistant/hub_padroes/output/proveniencia.md`
- `docs/sprints/micromodelos/PLANO_MESTRE.md`

## Ratificação de status — 14/09/2026

O usuário declarou: “D2: Aceito ADR-0014 a ADR-0020 sem ressalvas.” Este ADR fica aceito sem alteração do corpo decisório. O aceite não antecipa o schema detalhado, a máquina de estados ou outras decisões próprias da MM01, e não autoriza iniciar MM01 antes do merge da MM00 e do fechamento documental pós-MM00 previsto pela exceção D1-B.
