# Pistas de auditoria por skill

> **Recurso customizado:** não é padrão Databricks nem fonte de verdade. Ler o `SKILL.md` atual e auditar o artefato real. Estes checkpoints ajudam a formular testes; não aprovam uma skill por presença de palavras-chave.

## Checkpoints universais

- `SKILL.md` descobrível com frontmatter apenas `name` e `description`.
- Nome igual à pasta; descrição contém função e gatilhos concretos.
- Corpo conciso, imperativo e com recursos carregados sob demanda.
- Links relativos resolvem a partir da raiz da skill.
- Exemplos não contêm path pessoal, segredo, PII ou API inexistente.
- Scripts têm dependências, parâmetros, erros e ao menos teste representativo.
- Heurísticas customizadas estão identificadas; documentação oficial sustenta alegações nativas.
- Handoffs usam nomes reais de skills e não comandos slash não registrados.

## hub-ml-eda-profissional

- Contrato: unidade, chave, período, target e data de corte.
- Qualidade, granularidade, distribuições e relações são verificadas.
- Spark faz agregação; coleta ao driver tem limite e seed.
- Gráficos exibem unidade, denominador, período e top-N/cauda.
- Fatos, hipóteses e recomendações estão separados.

## hub-ml-cross-eda-ml

- Fonte âncora, resolução de entidade e granularidade estão explícitas.
- Join point-in-time respeita disponibilidade real e atraso.
- Coverage, não match, multiplicidade e explosão são medidos.
- Sinal incremental usa comparação justa, preferencialmente OOT.
- Readiness tem evidência e vetos; média não encobre leakage.

## hub-ml-feature-engineering

- Feature spec contém chave, fórmula, janela, event time e disponibilidade.
- Transformações ajustadas no treino não vazam para validação/teste.
- Lags/janelas são particionados por entidade.
- Paridade treino-inferência, determinismo e reprocessamento são testados.
- API de Feature Engineering in Unity Catalog está atual e não mistura legado.

## hub-ml-validacao-estatistica

- Pergunta, estimando, desenho, H0/H1, efeito e multiplicidade são definidos.
- Amostragem preserva a unidade/dependência e registra seed.
- Resultados incluem estimativa, IC, N, efeito e consequência prática.
- P-valor não é interpretado como magnitude/probabilidade de H0.
- Limiares e severidade são calibrados ao risco, não universais.

## hub-ml-baseline-ml

- Suite escolhida explicitamente e comparada a baseline trivial.
- Split respeita tempo, entidade, gap e teste intocado.
- Métricas são válidas para classes/volume e objetivo operacional.
- Séries usam backtesting; ranking valida grupos; survival trata censura.
- MLflow registra pipeline, assinatura, dependências e snapshot sem PII.

## hub-ml-explainability

- Modelo, versão, classe, população e escala explicada estão claros.
- SHAP/importance usa conjunto e preprocessing corretos.
- Retorno multiclasses/versão SHAP é tratado.
- Explicação global/local registra amostra e background.
- Não há linguagem causal, “percentual de acerto” para AUC ou “percentual de decisão” para SHAP.

## hub-ml-monitoramento-modelo

- Contrato contém referência, janela, atraso de label, owner e runbook.
- PSI usa bins de referência e missing/categoria nova explícitos.
- Delta respeita a direção da métrica; melhoria não dispara degradação.
- Serviço, dados, drift, performance, segmentos e negócio são separados.
- Retreino cria challenger e gates; não promove alias automaticamente.

## hub-ml-pipeline-builder

- Nomenclatura atual: Lakeflow Spark Declarative Pipelines, Lakeflow Jobs e Declarative Automation Bundles.
- Contratos de datasets e regras de incrementalidade são explícitos.
- Deduplicação/MERGE são determinísticos; backfill/replay existem.
- Expectations têm ação coerente e API oficial atual.
- Bundle valida targets, secrets, permissões, deploy e smoke test.

## hub-ml-analise-safra

- MOB, data de origem/observação/corte e denominador são definidos.
- Células imaturas permanecem ausentes; comparações usam mesmo MOB.
- Percentuais não são acumulados com `cumsum`.
- Volume/incerteza e decomposição de mix acompanham alertas.
- Referência normativa é precisa e não transforma técnica em obrigação.

## hub-ml-comentar-notebook

- Código e comportamento permanecem inalterados sem autorização.
- Markdown descreve a célula adjacente e usa outputs reais.
- Densidade é proporcional à relevância; sem repetição decorativa.
- Métricas são traduzidas corretamente e PII não é reproduzida.
- Próximo passo e risco remanescente são concretos.

## hub-ml-tutor-databricks

- Explicação começa pela finalidade e pelo fluxo.
- Lazy evaluation, ações, shuffles e driver são diferenciados.
- Erro raiz, hipótese, teste diagnóstico e aceite aparecem.
- Cloud/runtime/compute são confirmados quando a resposta depende deles.
- Analogia é rotulada e não substitui comportamento técnico literal.

## hub-ml-auditoria-skills

- Auditoria separa conformidade, evidência e julgamento.
- Achados trazem arquivo/linha, impacto, correção e aceite.
- Severidade reflete risco; média não compensa crítico.
- Validador, links, scripts e coerência cruzada são efetivamente testados.
- Riscos e testes não executados permanecem visíveis.
