# Prompt: EDA completa e reprodutível

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Adicione tabelas, notebook e definições
> com **Add context** ou `@`. Skill recomendada: `@rodrigo-eda-profissional`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[CATALOGO_HELPERS.md](../CATALOGO_HELPERS.md).

## Como preencher

Use nomes em três níveis quando possível (`catalog.schema.table`). Marque campo
desconhecido como `NÃO INFORMADO`. Target e período só são obrigatórios quando
existirem no problema.

## Prompt pronto para colar

```text
Use @rodrigo-eda-profissional para construir uma EDA completa, auditável e adequada
ao volume, sem alterar os dados de origem.

BRIEFING
- Recurso principal: {{TABELA_OU_DF}}
- Contexto de negócio/decisão: {{CONTEXTO_NEGOCIO}}
- Unidade de análise: {{GRANULARIDADE}}
- Chave primária/candidata: {{PK_OU_NAO_INFORMADO}}
- Coluna temporal: {{COL_DATA_OU_NAO_INFORMADO}}
- Target e evento positivo: {{TARGET_DEFINICAO_OU_NAO_APLICAVEL}}
- Período e filtros: {{PERIODO_E_FILTROS}}
- Volume estimado: {{VOLUME_OU_NAO_INFORMADO}}
- Foco prioritário: {{FOCO}}
- Restrições de compute, prazo e bibliotecas: {{RESTRICOES}}
- Entregável: {{NOTEBOOK_RELATORIO_OU_CODIGO}}

PRÉ-REQUISITOS
1. Verifique o recurso anexado, schema, comentários do Unity Catalog e permissões.
2. Liste ambiguidades que mudariam a análise; faça perguntas somente sobre bloqueios.
3. Declare plano, número esperado de varreduras e estratégia de amostragem.

ESCOPO MÍNIMO
1. Estrutura: schema, tipos, volume, duplicidade, chaves e granularidade observada.
2. Qualidade: nulos, valores inválidos, cardinalidade, extremos, consistência e
   cobertura temporal. Não confunda ausência permitida com erro.
3. Univariada: estatísticas robustas e distribuições adequadas ao tipo de variável.
4. Bivariada/multivariada: relações relevantes, segmentos, tempo e target, quando
   aplicável; correlação não implica causalidade.
5. Risco de modelagem: leakage temporal/alvo, viés de seleção, drift, desbalanceamento
   e representatividade, se houver finalidade de ML.
6. Visualização: Plotly quando útil; agregue/amostre antes de coletar ao driver.

SEGURANÇA E CUSTO
- Priorize PySpark/Spark SQL. Não faça `toPandas()` ou `collect()` irrestrito.
- Não revele PII, segredos ou valores individuais; use agregação/mascaramento.
- Não escreva tabelas, não sobrescreva notebooks e não instale dependências sem
  apresentar o impacto e obter autorização explícita.

CONTRATO DE SAÍDA
- Resumo executivo orientado à decisão.
- Inventário de qualidade com evidência, severidade, impacto e recomendação.
- Notebook/código organizado por células idempotentes, com parâmetros no início.
- Tabelas e gráficos com títulos, unidade, período, base e observações.
- Conclusões ligadas às evidências, limitações e backlog priorizado.

VALIDAÇÃO FINAL
- Registre recursos, filtros, período, contagens e amostra efetivamente usados.
- Valide que joins não multiplicaram linhas e que denominadores são explícitos.
- Separe achados observados, hipóteses e recomendações.
- Liste o que não foi possível verificar e por quê.
```

## Exemplo mínimo

Recurso = `@main.vendas.pedidos`; granularidade = um pedido; chave = `id_pedido`;
coluna temporal = `data_pedido`; foco = qualidade e sazonalidade.

## Follow-ups úteis

- “Transforme o backlog crítico em regras de qualidade propostas, sem executar.”
- “Crie uma versão executiva com apenas evidências que mudam a decisão.”
- “Prepare o handoff para Cross-EDA ou feature engineering, com riscos de leakage.”
