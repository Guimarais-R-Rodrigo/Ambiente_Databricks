# Resultados — forward tests · rodada <N> · <YYYY-MM-DD>

Executor: <quem rodou> · Workspace: Databricks Free · Réplica publicada em: <data/commit>

Preencha **Observado** com a skill que o Genie Code carregou (ou "nenhuma").
Veredito: PASS/FAIL conforme `.claude/skills/forward-test-skills/SKILL.md`.

| # | Skill | Caso | Esperado | Observado | Veredito | Ação |
|---|---|---|---|---|---|---|
| 1 | rodrigo-eda-profissional | P | carrega | | | |
| 1 | rodrigo-eda-profissional | N | NÃO carrega (ideal: cross-eda-ml) | | | |
| 1 | rodrigo-eda-profissional | @ | carrega | | | |
| 2 | rodrigo-cross-eda-ml | P | carrega | | | |
| 2 | rodrigo-cross-eda-ml | N | NÃO carrega (ideal: eda-profissional) | | | |
| 2 | rodrigo-cross-eda-ml | @ | carrega | | | |
| 3 | rodrigo-feature-engineering | P | carrega | | | |
| 3 | rodrigo-feature-engineering | N | NÃO carrega (ideal: baseline-ml) | | | |
| 3 | rodrigo-feature-engineering | @ | carrega | | | |
| 4 | rodrigo-validacao-estatistica | P | carrega | | | |
| 4 | rodrigo-validacao-estatistica | N | NÃO carrega (ideal: monitoramento) | | | |
| 4 | rodrigo-validacao-estatistica | @ | carrega | | | |
| 5 | rodrigo-baseline-ml | P | carrega | | | |
| 5 | rodrigo-baseline-ml | N | NÃO carrega (ideal: explainability) | | | |
| 5 | rodrigo-baseline-ml | @ | carrega | | | |
| 6 | rodrigo-explainability | P | carrega | | | |
| 6 | rodrigo-explainability | N | NÃO carrega (ideal: monitoramento) | | | |
| 6 | rodrigo-explainability | @ | carrega | | | |
| 7 | rodrigo-monitoramento-modelo | P | carrega | | | |
| 7 | rodrigo-monitoramento-modelo | N | NÃO carrega (ideal: validacao-estatistica) | | | |
| 7 | rodrigo-monitoramento-modelo | @ | carrega | | | |
| 8 | rodrigo-pipeline-builder | P | carrega | | | |
| 8 | rodrigo-pipeline-builder | N | NÃO carrega (ideal: feature-engineering) | | | |
| 8 | rodrigo-pipeline-builder | @ | carrega | | | |
| 9 | rodrigo-analise-safra | P | carrega | | | |
| 9 | rodrigo-analise-safra | N | NÃO carrega (ideal: monitoramento) | | | |
| 9 | rodrigo-analise-safra | @ | carrega | | | |
| 10 | rodrigo-comentar-notebook | P | carrega | | | |
| 10 | rodrigo-comentar-notebook | N | NÃO carrega (ideal: tutor) | | | |
| 10 | rodrigo-comentar-notebook | @ | carrega | | | |
| 11 | rodrigo-tutor-databricks | P | carrega | | | |
| 11 | rodrigo-tutor-databricks | N | NÃO carrega (ideal: comentar-notebook) | | | |
| 11 | rodrigo-tutor-databricks | @ | carrega | | | |
| 12 | rodrigo-auditoria-skills | P | carrega | | | |
| 12 | rodrigo-auditoria-skills | N | NÃO carrega (ideal: eda-profissional) | | | |
| 12 | rodrigo-auditoria-skills | @ | carrega | | | |

## Síntese da rodada

- PASS: __/36 · FAIL: __/36
- Colisões observadas (skill errada carregada em caso negativo): <listar>
- Descriptions a ajustar: <listar skills>
- Observações livres: <UI, cache, comportamento inesperado>
