# Rubrica Universal de Auditoria — Ancoras 0-10

> Cada dimensao e avaliada conforme as ancoras abaixo.
> O auditor deve escolher a ancora mais proxima e justificar.
> Aplicar apenas dimensões pertinentes ao contrato, perfil e risco. Falta de
> evidência é NÃO AVALIADO, não aprovação. Vetos mecânicos, Receipt/Postflight
> e `completion.authorized` prevalecem sobre notas e médias.

---

## Escala Geral (aplica-se a TODAS as dimensoes)

| Nota | Nivel | Descricao generica |
|---|---|---|
| 0 | Ausente | Dimensao completamente ausente no output |
| 1-2 | Vestigial | Tentativa minima, sem substancia. Stub ou placeholder |
| 3-4 | Insuficiente | Presente mas com falhas graves ou lacunas criticas |
| 5-6 | Funcional | Cumpre o basico mas com gaps relevantes ou falta de profundidade |
| 7-8 | Bom | Atende bem ao contrato com gaps menores ou oportunidades de melhoria |
| 9-10 | Exemplar | Excede expectativas. Referencia de qualidade no ecossistema |

---

## Ancoras por Dimensao

### D1 — Completude Estrutural

| Nota | Criterio |
|---|---|
| 0 | Notebook vazio ou com apenas titulo |
| 1-2 | Apenas 1-2 etapas da skill presentes (ex: so imports + 1 calculo) |
| 3-4 | Menos de 50% das etapas obrigatorias presentes |
| 5-6 | 50-70% das etapas presentes, mas falta conclusao ou contexto |
| 7-8 | 70-90% das etapas presentes, com header e conclusao |
| 9-10 | Todos os requisitos aplicáveis demonstrados, com limites e evidência verificáveis; extras não rendem pontos por si só |

### D2 — Reprodutibilidade

| Nota | Criterio |
|---|---|
| 0 | Notebook nao executa (imports faltando, erros de sintaxe) |
| 1-2 | Executa parcialmente mas depende de estado externo nao declarado |
| 3-4 | Executa mas sem seeds, ou com celulas fora de ordem |
| 5-6 | Execução demonstrada, mas dependências ou referência de dados insuficientemente declaradas |
| 7-8 | Reproduzivel: imports, seeds, dados acessiveis, ordem logica |
| 9-10 | Reproduzível, com versões declaradas e bloqueios preservados quando faltam requisitos; try/except não mascara falha |

### D3 — Rigor Metodologico

| Nota | Criterio |
|---|---|
| 0 | Metodologia errada ou ausente (ex: regressao para classificacao) |
| 1-2 | Metodologia presente mas com erro grave (leakage nao tratado, split errado) |
| 3-4 | Metodologia basicamente correta mas parametros duvidosos ou sem validacao |
| 5-6 | Correta com parametros razoaveis mas sem baseline ou sem justificativa de escolhas |
| 7-8 | Correta, com baseline, split adequado, limitacoes declaradas |
| 9-10 | Método rigoroso para o objetivo, pressupostos e limitações demonstrados; baseline, modelo ou comparação estatística somente se exigidos pelo contrato |

### D4 — Documentacao e Narrativa

| Nota | Criterio |
|---|---|
| 0 | Finalidade, entradas e resultados necessários ao leitor não são explicados |
| 1-2 | Texto genérico sem vínculo com o artefato |
| 3-4 | Contexto parcial, sem interpretação dos resultados materiais |
| 5-6 | Contexto útil, mas faltam limites ou interpretação de uma etapa relevante |
| 7-8 | Narrativa coerente e proporcional: objetivo, desenvolvimento, conclusão e evidência |
| 9-10 | Narrativa precisa, didática e suficiente ao público; camadas técnica/executiva e índice somente quando pertinentes, sem prêmio por volume |

### D5 — Rastreabilidade

| Nota | Critério do perfil de rastreabilidade selecionado |
|---|---|
| 0 | Evidência exigida pelo perfil ausente ou incompatível |
| 1-2 | Registro iniciado, sem os bindings/identificadores exigidos |
| 3-4 | Parte dos metadados exigidos presente, com lacunas materiais |
| 5-6 | Registros utilizáveis, mas faltam evidências requeridas ou há inconsistências a resolver |
| 7-8 | Evidências aplicáveis completas, referenciáveis e coerentes; pequenas lacunas explicativas |
| 9-10 | Proveniência e artefatos exigidos conferidos com limites explícitos; modelo, plots, CSVs ou Context Card só quando o contrato os exige |

Perfil sem MLflow usa a rastreabilidade que seu contrato requer (request,
Receipt, links, nomes e versões, conforme aplicável). Não reduzir nota pela
ausência de logging ou artefatos opcionais. Nenhuma nota substitui verificador.

### D6 — Governanca e Compliance

| Nota | Criterio |
|---|---|
| 0 | Nenhuma preocupacao com governanca. Dados expostos sem cuidado |
| 1-2 | Nome da tabela incompleto (sem catalog) ou PII exposta sem aviso |
| 3-4 | Tabela com nome completo mas sem declarar limitacoes ou premissas |
| 5-6 | Nome completo + algumas limitacoes, mas naming inconsistente |
| 7-8 | Naming OK + limitacoes + premissas + periodo declarado |
| 9-10 | Tudo acima + aderencia a norma interna de governanca de dados explicita + PII tratado + lineage documentado |

### D7 — Interpretacao e Acionabilidade

| Nota | Criterio |
|---|---|
| 0 | Nenhuma interpretacao. Apenas numeros/graficos sem explicacao |
| 1-2 | Interpretacao trivial ("media e 42") sem insight de negocio |
| 3-4 | Alguns insights mas genericos. Sem recomendacoes |
| 5-6 | Insights relevantes mas sem priorizacao ou sem proximos passos |
| 7-8 | Insights especificos + recomendacoes concretas + proximos passos |
| 9-10 | Recomendações priorizadas com evidência, incerteza, autoridade e próximos passos; impacto só estimado com fundamento |

### D8 — Qualidade Visual

| Nota | Criterio |
|---|---|
| 0 | Apresentação impede interpretar informação necessária; ausência de gráfico opcional não é defeito |
| 1-2 | Graficos basicos sem titulo/eixos/legenda |
| 3-4 | Graficos com titulo mas sem tema padronizado ou anotacoes |
| 5-6 | Visual pertinente legível, mas contexto, unidade ou limites incompletos |
| 7-8 | Apresentação adequada ao contrato, com títulos, unidades e comparação legível; tema quando aplicável |
| 9-10 | Visual ou tabela adequado ao objetivo, legível e acessível, com unidades, limites e tema aplicável; sem exigir decoração ou biblioteca específica |

### D9 — Robustez e Edge Cases

| Nota | Criterio |
|---|---|
| 0 | Nenhum tratamento defensivo. Quebra com nulos ou dados vazios |
| 1-2 | dropna() generico sem justificativa |
| 3-4 | Tratamento basico de nulos mas sem validacao de volume ou alertas |
| 5-6 | Nulos tratados + sample com seed, mas sem validacao de edge cases do SKILL.md |
| 7-8 | Robusto: nulos, volume, edge cases principais tratados |
| 9-10 | Edge cases do contrato verificados e falhas reportadas; em rota fail-closed, bloqueio preservado sem fallback local |

### D10 — Aderencia ao ecossistema e a biblioteca de helpers

Confrontar o output com [MANUAL_TECNICO_V2.md#catalogo-helpers](../../../MANUAL_TECNICO_V2.md#catalogo-helpers).
Reimplementar logica ja disponivel e o achado tipico desta dimensao: e como
surgem PSI por media/desvio, split temporal por fatia de linhas e incidencia de
safra somada por taxa.

| Nota | Criterio |
|---|---|
| 0 | Output desconectado do ecossistema; reimplementa logica critica da biblioteca de forma incorreta |
| 1-2 | Reimplementa logica disponivel sem justificativa e com divergencia de comportamento |
| 3-4 | Formatacao/convencoes parcialmente aderentes; ignora helpers aplicaveis |
| 5-6 | Segue instrucoes e templates, mas reescreve helper aplicavel sem declarar o motivo |
| 7-8 | Usa os helpers aplicaveis com import correto; desvios justificados explicitamente |
| 9-10 | Usa helpers e templates, declara dependencias opcionais e versoes, e preserva as ressalvas do modulo (direcao de score, threshold calibrado, limite de amostra) |

Reescrever um helper só é aceitável quando a rota permite, o caso exige, a mudança está autorizada e o motivo é declarado. Em rota protegida/fail-closed, justificativa não autoriza bypass.
Reescrita silenciosa, nao. Nao pontuar por recursos inexistentes na plataforma:
nao ha hooks nem slash commands registrados pelo usuario.

---

## Regras de Aplicacao

1. Escolher a ancora mais proxima ao estado real do output
2. Meia-nota permitida (ex: 7.5) quando entre duas ancoras
3. Justificativa DEVE citar evidencia (celula, pattern, contagem)
4. Se uma dimensão não se aplicar (ex.: rastreabilidade de artefato para `@hub-ml-tutor-databricks`): marcar N/A e redistribuir o peso explicitamente.
5. Arredondar score final para 1 casa decimal
