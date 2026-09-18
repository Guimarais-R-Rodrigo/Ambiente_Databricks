---
name: hub-ml-eda-profissional
description: Produz EDA profissional e escalável no Databricks com PySpark/Spark SQL, cobrindo granularidade, chaves, qualidade, distribuições, relações, visualizações agregadas e recomendações. Usar quando pedirem exploração, perfil, diagnóstico de base, qualidade inicial, análise uni/bivariada, notebook de EDA ou relatório executivo de uma fonte de dados.
---

# Produzir EDA profissional

## Quando esta skill se aplica

- Pedem **exploração, perfil, diagnóstico ou qualidade inicial** de uma fonte de
  dados, ou um notebook de EDA.
- A pergunta é sobre **uma** tabela ou uma base já consolidada.

**Não cobre:** cruzar múltiplas fontes (`hub-ml-cross-eda-ml`) nem executar
testes de hipótese com p-valor e effect size (`hub-ml-validacao-estatistica`).

## Definir escopo

Confirmar a pergunta, unidade de análise, data de corte, tabela, filtros, chave candidata e target. Se algo crítico estiver ausente, continuar com hipóteses explícitas e listar o que precisa ser confirmado.

## Executar a rota canônica e finalizar em fail-closed

Para a execução completa L4 desta skill, usar [scripts/run_enforced.py](scripts/run_enforced.py) como orquestrador de enforcement. Ele reutiliza [scripts/run.py](scripts/run.py) para o core L3/Receipt e acrescenta evidência mecânica dos recursos e templates exigidos pelo contrato. Não substituir a rota L4 por Python/PySpark manual, chamada direta aos helpers ou montagem manual de trace/Receipt.

A separação é deliberada:

1. `scripts/run.py::run` continua sendo o **entrypoint canônico do core L3** e emite `ExecutionReceiptV1`;
2. `scripts/run_enforced.py::run_enforced` coleta a evidência adicional necessária ao L4, chamando recursos aplicáveis quando as entradas objetivas existem e registrando gaps quando não existem;
3. [scripts/postflight.py](scripts/postflight.py) confronta Receipt, contrato, evidência observada e handoff;
4. somente `postflight.status="PASS"` autoriza `completion.status="COMPLETED"`.

O runner L3:

1. valida a integridade mínima da release;
2. deriva `numeric_columns` do schema Spark e bloqueia contradição declarada;
3. executa o preflight L2 do `execution_contract.json`;
4. chama a primitive protegida `hub_scripts.quick_profile.quick_profile`;
5. registra em `ExecutionTraceV0` digests, provenance, recursos resolvidos/chamados/concluídos e `fallback_used=false`;
6. quando a execução termina canonicamente, emite `ExecutionReceiptV1` com bindings determinísticos ao trace, input, output e release.

O executor L4 preserva esse core e acrescenta:

- imports/calls/completions observados para recursos required/conditional suportados;
- leitura real dos templates aplicáveis e seus SHA-256;
- `artifacts_digest` para detectar alteração posterior da evidência auxiliar;
- `evidence_gaps` quando faltam entradas, runtime ou conclusão mecânica;
- reemissão do Receipt para vinculá-lo ao trace enriquecido.

Na EDA profissional padrão, **não monte manualmente o contexto condicional**. O executor L4 aplica o perfil canônico de EDA: distribuições e diagnóstico visual ligados, preview/amostra local opt-in e tema desligado até existir `ResolvedTheme`. Chame o entrypoint com o mínimo de parâmetros:

```python
payload = run_enforced_mod.run_enforced(
    TABLE_NAME,
    assistant_root=ASSISTANT_ROOT,
    display_fn=display,
)
```

Só passe overrides quando houver evidência objetiva. Para `data_quality_check`, forneça `pk_columns` apenas quando uma PK/chave candidata tiver sido **explicitamente estabelecida**. Sem PK confirmada, o contrato marca esse helper como `not_applicable`; não invente uma chave para satisfazer o gate. Se `resolved_theme_selected=true`, forneça o `ResolvedTheme` correspondente.

Se `run_enforced` levantar `CanonicalExecutionBlocked`, a execução canônica está encerrada naquele run: **não continue a mesma EDA manualmente e não declare conclusão**. Corrija uma entrada objetiva ausente e reinicie a rota canônica em novo run, ou reporte a etapa como não concluída.

Depois das análises adicionais permitidas, construa o handoff e finalize obrigatoriamente com `scripts/postflight.py::finalize_or_raise`. Somente o retorno bem-sucedido desse método autoriza linguagem de conclusão:

```python
final_payload = postflight_mod.finalize_or_raise(
    payload,
    handoff,
    assistant_root=ASSISTANT_ROOT,
)
```

O arquivo [scripts/preflight.py](scripts/preflight.py) continua disponível para diagnóstico isolado do L2. Ele não substitui o executor L4 quando a EDA for apresentada como concluída com aderência ao contrato.

## Executar em nove etapas

1. **Contextualizar:** registrar objetivo, fontes, snapshot, filtros e limitações.
2. **Inventariar:** obter schema, tipos, estimativa/contagem necessária, partições e período coberto.
3. **Validar granularidade:** medir unicidade, duplicidades, cardinalidade e consistência das chaves.
4. **Medir qualidade:** nulos, vazios, domínios, ranges, datas inválidas e regras de negócio.
5. **Analisar numerais:** percentis robustos, assimetria, zeros, sinal, caudas e outliers contextualizados.
6. **Analisar categorias:** frequência, cobertura acumulada, raridade, valores inesperados e cardinalidade.
7. **Analisar relações:** target, tempo, segmentos e redundância; escolher método compatível com os tipos.
8. **Visualizar:** agregar no Spark, limitar categorias e coletar somente o resultado pequeno para Plotly.
9. **Concluir:** separar fatos, hipóteses, impacto e ações priorizadas.

## Trabalhar de forma escalável

- Preferir agregações PySpark/Spark SQL.
- Evitar `toPandas()` sobre a base completa. Registrar limite, estratégia de amostragem e seed.
- Evitar múltiplos `count()` sem necessidade; persistir apenas quando houver reutilização comprovada e liberar cache.
- Usar `approxQuantile`/`percentile_approx` quando a precisão aproximada for adequada.
- Não exibir todas as categorias ou linhas. Mostrar top-N, cauda e “outros”.
- Mascarar ou agregar PII e dados sensíveis.

## Escolher testes e gráficos pelo dado

Não impor uma matriz fixa. Exemplos:

- numérica: histograma amostrado/agregado, ECDF ou box plot por grupo;
- categórica: barras ordenadas com denominador explícito;
- temporal: série com frequência regular e cobertura;
- target binário: distribuição por classe, AUC apenas se houver score, taxas com volume;
- correlação: Pearson para relação linear, Spearman para monotonicidade, associação apropriada para categóricas.

Rotular unidade, janela e denominador. Não confundir correlação com causalidade.

## Entregar recomendações acionáveis

Para cada achado relevante, informar:

- evidência e população afetada;
- possível impacto em análise/modelo/processo;
- hipótese de causa;
- ação recomendada;
- validação de aceite.

Usar [templates/roteiro_eda.md](templates/roteiro_eda.md) para estruturar o notebook, [templates/matriz_graficos_eda.md](templates/matriz_graficos_eda.md) para selecionar visualizações e [templates/relatorio_executivo_eda.md](templates/relatorio_executivo_eda.md) para o resumo. Consultar [templates/estilo_visual_eda.md](templates/estilo_visual_eda.md) para composição e leitura da EDA. Paleta/tokens configuráveis vêm de `ResolvedTheme` e do padrão `hub_padroes/identidade_visual`; o template não é uma segunda fonte de tema.

## Usar helpers da biblioteca

Importar de `hub_snippets`/`hub_scripts` em vez de reimplementar a lógica. Catálogo completo: [MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

| Demanda | Módulo |
|---|---|
| Core L3 + preflight + Receipt | `skills/hub-ml-eda-profissional/scripts/run.py`, `hub_scripts.skill_execution`, `hub_scripts.skill_execution.receipt` |
| Executor L4 + postflight fail-closed | `skills/hub-ml-eda-profissional/scripts/run_enforced.py`, `skills/hub-ml-eda-profissional/scripts/postflight.py`, `hub_scripts.skill_execution.postflight` |
| Perfil de tabela e checagem de qualidade | `hub_scripts.quick_profile`, `hub_scripts.data_quality_check` |
| Nulos por coluna com semáforo | `hub_snippets.spark.null_summary` |
| Amostra reprodutível e exibição limitada | `hub_snippets.spark.smart_sample`, `hub_snippets.spark.safe_display` |
| Correlação e grid de distribuições | `hub_snippets.display.correlation_matrix`, `hub_snippets.display.distribution_grid` |
| Tema, índice e formatação brasileira | `hub_snippets.visual.theme_plotly`, `hub_snippets.visual.index_generator`, `hub_snippets.constants.format_br` |

Quando um tema notebook validado tiver sido selecionado, mantenha a mesma análise e use as rotas opt-in: `plot_correlation_resolvido`, `plot_distributions_resolvido` e `aplicar_tema_resolvido`/outro consumidor `_resolvido` aplicável. Sem tema selecionado, preserve as APIs legadas. `ResolvedTheme` muda aparência coberta pelo contrato; não muda agregação Spark, amostra, denominador ou interpretação.

`quick_profile` distingue o que é calculado na tabela inteira do que vem da amostra; preservar essa distinção ao relatar números.

## Preparar o handoff obrigatório

Antes do postflight, fornecer objeto estruturado com os campos definidos no contrato:

- `sources_snapshot`;
- `unit_keys_target`;
- `quality_risks`;
- `feature_candidates_leakage`;
- `filters_sample`;
- `open_questions` — pode ser lista vazia quando não houver perguntas pendentes.

Não inventar valores apenas para obter PASS. Se uma informação material não foi estabelecida, registrá-la explicitamente como pendência; o postflight pode devolver `REVIEW` e a skill permanece não concluída.

## Interpretar a evidência de execução

- `ExecutionTraceV0`: registro técnico do que aconteceu durante o run.
- `ExecutionReceiptV1`: comprovante formal que vincula trace e resultado à release/execução canônica esperada.
- `PostflightV1`: valida Receipt, required/conditional aplicáveis, skips, templates, artifacts e handoff.
- `VALID` no Receipt: comprovante SE04 íntegro e compatível; não equivale sozinho a conclusão L4.
- `PASS` no postflight: única condição que autoriza `completion.authorized=true`.
- `PENDING_POSTFLIGHT`: o executor L4 terminou, mas **a skill ainda não terminou**; falta `finalize_or_raise`.
- `FAIL`: evidência material requerida faltou ou não concluiu.
- `BLOCKED`: contrato/Receipt/binding/integridade não são confiáveis o bastante para avaliar.
- `REVIEW`: handoff ou justificativa precisa de revisão antes de concluir.

Se o resultado parecer correto, mas o postflight não estiver `PASS`, não declare “skill concluída com aderência ao contrato”. Task correctness e canonical compliance continuam dimensões diferentes.

## O que nunca fazer

- **Pular `run_enforced.py` ao declarar execução L4 concluída.** `run.py` isolado pode produzir Receipt L3 válido, mas não reúne sozinho toda a evidência de conclusão.
- **Declarar conclusão quando `postflight != PASS`.** Nem resultado correto nem Receipt `VALID` substituem esse gate.
- **Fabricar, copiar ou reaproveitar Receipt/Postflight para legitimar rota manual.** A evidência precisa nascer da execução correspondente.
- **Tratar `resolved` como `called` ou `loaded`.** Disponibilidade estática não prova uso.
- **Fazer fallback manual quando integridade/preflight/primitive falhar ou quando `CanonicalExecutionBlocked` ocorrer.** Bloquear e reportar o gap; não continuar a mesma tarefa por código paralelo.
- **Usar “concluído”, “finalizado”, “sucesso” ou equivalente sem `completion.authorized=true` reverificado.**
- **Inferir chave candidata apenas para satisfazer `data_quality_check`.** Solicitar/usar chave explicitamente estabelecida.
- **Trazer a tabela inteira para o driver.** `toPandas()` sem limite verificável derruba o notebook em base real; passe por amostra declarada.
- **Usar `cache()` sem proteção** — é bloqueado em compute serverless.
- **Afirmar distribuição a partir da média.** Duas bases com a mesma média e desvios diferentes contam histórias opostas.
- **Chamar de qualidade o que é só contagem de nulo.** Nulo tem significado, e tratá-lo como zero enviesa sem deixar rastro.
- **Fechar a EDA sem dizer o que ela não olhou.**

## Handoff

Entregar um contrato com:

- fontes e snapshot;
- unidade, chaves e target;
- principais riscos de qualidade;
- features candidatas e suspeitas de leakage;
- filtros e amostra usados;
- perguntas ainda abertas.

Acionar `hub-ml-cross-eda-ml` para múltiplas fontes, `hub-ml-feature-engineering` para projetar features e `hub-ml-validacao-estatistica` quando a decisão exigir inferência.
