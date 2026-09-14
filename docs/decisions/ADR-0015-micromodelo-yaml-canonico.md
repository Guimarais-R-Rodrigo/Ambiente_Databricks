# ADR-0015 — `micromodelo.yaml` como especificação canônica

Data: 2026-09-14
Status: Proposto
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
