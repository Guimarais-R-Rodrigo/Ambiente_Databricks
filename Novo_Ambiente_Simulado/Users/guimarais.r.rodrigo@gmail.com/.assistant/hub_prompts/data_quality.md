# Prompt: diagnóstico e contrato de qualidade de dados

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Anexe a tabela/pipeline com **Add context**
> ou `@`. Skill recomendada: `@rodrigo-eda-profissional`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Campos essenciais

Defina recurso, granularidade, chaves, coluna de atualização, uso downstream e
limites de qualidade. Threshold sem justificativa deve ser tratado como hipótese.

## Prompt pronto para colar

```text
Use @rodrigo-eda-profissional para avaliar a qualidade do recurso anexado e propor
um contrato verificável. Não modifique dados nem pipeline nesta etapa.

CONTEXTO
- Tabela/view/DataFrame/pipeline: {{RECURSO}}
- Unidade de análise: {{GRANULARIDADE}}
- Chave(s): {{CHAVES}}
- Coluna de evento/atualização: {{COLUNAS_TEMPO}}
- Partições: {{PARTICOES_OU_NAO_INFORMADO}}
- Uso e consumidores downstream: {{USO_DOWNSTREAM}}
- Regras já acordadas: {{REGRAS_EXISTENTES_OU_NENHUMA}}
- SLOs/thresholds e justificativas: {{THRESHOLDS_OU_PROPOR}}
- Período: {{PERIODO}}
- Restrições: {{RESTRICOES}}

FLUXO
1. Confirme schema, comentários do Unity Catalog, volume e granularidade.
2. Proponha checks de completude, unicidade, validade, consistência, integridade
   referencial, atualidade e volume. Diferencie regra de negócio de regra técnica.
3. Execute somente leituras autorizadas, consolidando agregações para reduzir scans.
4. Para cada falha, mostre numerador, denominador, taxa, período e exemplos somente
   anonimizados/agregados.
5. Se o recurso for Lakeflow Spark Declarative Pipelines, proponha expectations com
   comportamento explícito (monitorar, descartar ou falhar), sem aplicá-las ainda.
6. Priorize regras por impacto downstream e risco de falso positivo.

SEGURANÇA E CUSTO
- Não exponha PII; não liste registros brutos como evidência.
- Não grave quarentena, não altere DDL e não reinicie pipeline sem confirmação.
- Para tabelas grandes, use pruning por partição e agregações; declare o escopo lido.

CONTRATO DE SAÍDA
- Scorecard por dimensão com resultado, limite, evidência e severidade.
- Catálogo de regras: ID, descrição, expressão, nível, ação e proprietário sugerido.
- Código PySpark/Spark SQL ou expectations proposto em bloco separado.
- Riscos, falsos positivos possíveis, lacunas de metadados e plano de implantação.

VALIDAÇÃO FINAL
- Confirme chaves, granularidade, timezone e período de referência.
- Valide que taxas usam denominadores corretos e que nulos não foram omitidos.
- Não declare conformidade quando uma dimensão não foi testada.
```

## Exemplo mínimo

`{{RECURSO}} = @main.silver.transacoes`, `{{CHAVES}} = id_transacao`,
`{{COLUNAS_TEMPO}} = ts_evento, ts_ingestao`, `{{USO_DOWNSTREAM}} = painel diário`.

## Follow-ups úteis

- “Gere testes para as regras críticas e inclua casos de borda.”
- “Converta as regras aprovadas em expectations do pipeline, sem fazer deploy.”
- “Compare o scorecard com a execução anterior e explique regressões.”
