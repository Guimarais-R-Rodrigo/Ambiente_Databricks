# Resultados — forward tests · rodada <N> · <YYYY-MM-DD>

Executor: <quem rodou> · Workspace: Databricks Free · Réplica publicada em: <data/commit>

Preencha **Observado** com a skill que o Genie Code carregou (ou "nenhuma").
Veredito: PASS/FAIL conforme `.claude/skills/forward-test-skills/SKILL.md`.

| # | Skill | Caso | Esperado | Observado | Veredito | Ação |
|---|---|---|---|---|---|---|
| 1 | hub-ml-eda-profissional | P | carrega | | | |
| 1 | hub-ml-eda-profissional | N | NÃO carrega (ideal: cross-eda-ml) | | | |
| 1 | hub-ml-eda-profissional | @ | carrega | | | |
| 2 | hub-ml-cross-eda-ml | P | carrega | | | |
| 2 | hub-ml-cross-eda-ml | N | NÃO carrega (ideal: eda-profissional) | | | |
| 2 | hub-ml-cross-eda-ml | @ | carrega | | | |
| 3 | hub-ml-feature-engineering | P | carrega | | | |
| 3 | hub-ml-feature-engineering | N | NÃO carrega (ideal: baseline-ml) | | | |
| 3 | hub-ml-feature-engineering | @ | carrega | | | |
| 4 | hub-ml-validacao-estatistica | P | carrega | | | |
| 4 | hub-ml-validacao-estatistica | N | NÃO carrega (ideal: monitoramento) | | | |
| 4 | hub-ml-validacao-estatistica | @ | carrega | | | |
| 5 | hub-ml-baseline-ml | P | carrega | | | |
| 5 | hub-ml-baseline-ml | N | NÃO carrega (ideal: explainability) | | | |
| 5 | hub-ml-baseline-ml | @ | carrega | | | |
| 6 | hub-ml-explainability | P | carrega | | | |
| 6 | hub-ml-explainability | N | NÃO carrega (ideal: monitoramento) | | | |
| 6 | hub-ml-explainability | @ | carrega | | | |
| 7 | hub-ml-monitoramento-modelo | P | carrega | | | |
| 7 | hub-ml-monitoramento-modelo | N | NÃO carrega (ideal: validacao-estatistica) | | | |
| 7 | hub-ml-monitoramento-modelo | @ | carrega | | | |
| 8 | hub-ml-pipeline-builder | P | carrega | | | |
| 8 | hub-ml-pipeline-builder | N | NÃO carrega (ideal: feature-engineering) | | | |
| 8 | hub-ml-pipeline-builder | @ | carrega | | | |
| 9 | hub-ml-analise-safra | P | carrega | | | |
| 9 | hub-ml-analise-safra | N | NÃO carrega (ideal: monitoramento) | | | |
| 9 | hub-ml-analise-safra | @ | carrega | | | |
| 10 | hub-ml-comentar-notebook | P | carrega | | | |
| 10 | hub-ml-comentar-notebook | N | NÃO carrega (ideal: tutor) | | | |
| 10 | hub-ml-comentar-notebook | @ | carrega | | | |
| 11 | hub-ml-tutor-databricks | P | carrega | | | |
| 11 | hub-ml-tutor-databricks | N | NÃO carrega (ideal: comentar-notebook) | | | |
| 11 | hub-ml-tutor-databricks | @ | carrega | | | |
| 12 | hub-ml-auditoria-skills | P | carrega | | | |
| 12 | hub-ml-auditoria-skills | N | NÃO carrega (ideal: eda-profissional) | | | |
| 12 | hub-ml-auditoria-skills | @ | carrega | | | |
| 13 | hub-ml-criar-objeto | P | carrega | | | |
| 13 | hub-ml-criar-objeto | N | NÃO carrega | | | |
| 13 | hub-ml-criar-objeto | @ | carrega | | | |

| 14 | hub-ml-concierge | P | carrega | | | |
| 14 | hub-ml-concierge | N | NÃO carrega (ideal: tutor) | | | |
| 14 | hub-ml-concierge | @ | carrega | | | |

## Síntese da rodada

- Casos executados: __/42 · PASS: __ · FAIL: __ · BLOQUEADO: __ · NÃO VERIFICADO: __
- Registro de carregamento na interface: <evidência; autorrelato não basta>
- Não copiar PASS de uma rodada anterior como resultado desta rodada.
- Colisões observadas (skill errada carregada em caso negativo): <listar>
- Descriptions a ajustar: <listar skills>
- Observações livres: <UI, cache, comportamento inesperado>
