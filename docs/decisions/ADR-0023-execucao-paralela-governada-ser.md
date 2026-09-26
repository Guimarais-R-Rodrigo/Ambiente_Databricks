# ADR-0023 — Execução paralela governada do Skill Enforcement Rollout

Data: 2026-09-24  
Status: Aceito  
Origem: decisão humana explícita após integração da SER01.

## Contexto

A SER01 demonstrou que o custo do rollout não está apenas na execução dos gates: parte relevante veio de handoffs repetidos, infraestrutura certificadora construída durante a própria promoção e defeitos baratos descobertos apenas no laboratório. A matriz de dependências da SER já distinguia ordem de integração de dependência funcional real.

## Decisão

1. Preservar SER02–SER16 e os targets existentes.
2. Substituir a obrigação operacional de executar toda sprint estritamente após a integração da anterior por um DAG explícito: frentes independentes podem ser autoradas, executadas e auditadas em paralelo contra base identificada.
3. Manter dependências próprias L2→L4 e gates humanos de promoção/merge separados.
4. Centralizar implementação, schemas, command registry, casos, oráculos e correções na autoria repo-side. Workers locais executam tarefas fechadas e não alteram critérios/produto.
5. O launcher paralelo B0 é read-only sobre o repositório. Escritas mecânicas compartilhadas, renderer, snapshots, policy, integração e publicação permanecem serializadas em papéis específicos.
6. Separar diagnóstico de certificação; certificação é SHA-bound e single-round, sem retry-until-green.
7. Preservar resultados SEF/SER históricos; assertions temporais ganham sucessores atuais, não são reescritas como PASS.
8. Exigir coverage map por método, metatestes do mecanismo, isolamento e dois pilotos antes de ampliar a concorrência.
9. Evidência RAW e SHARE têm identidades distintas; narrativa de modelo não substitui evento de ferramenta.
10. GitHub Actions permanecem não obrigatórias enquanto indisponíveis por créditos; nenhum required check é removido por esta decisão.

## Consequências

A execução pode avançar em até três frentes de skill após qualificação do mecanismo, sujeita a resource classes e locks. Uma falha de domínio bloqueia sua cadeia; falha do mecanismo/contrato compartilhado bloqueia consumidores afetados. Integração e publicação continuam controladas e não derivam automaticamente de PASS local.

Este ADR complementa o ADR-0022; não altera sua separação entre current/target, prova por superfície, recertificação pós-policy ou autoridade humana.
