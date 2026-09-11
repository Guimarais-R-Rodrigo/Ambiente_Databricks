# Prompt: EDA completa e reprodutível

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Adicione tabelas, notebook e definições
> com **Add context** ou `@`. Skill recomendada: `@hub-ml-eda-profissional`.

Antes de pedir código, veja os helpers que a skill recomendada declara: boa
parte do que este formulário pede já tem implementação verificada, e usá-la
evita que a lógica seja reescrita a cada conversa. Mapa completo em
[MANUAL_TECNICO.md#catalogo-helpers](../../MANUAL_TECNICO.md#catalogo-helpers).

## Como preencher

Use nomes em três níveis quando possível (`catalog.schema.table`). Marque campo
desconhecido como `NÃO INFORMADO`. Target e período só são obrigatórios quando
existirem no problema.

## Como preencher cada campo

| Campo | Como preencher | Por que importa | Exemplo |
|---|---|---|---|
| `{{TABELA_OU_DF}}` | Anexe com `@` ou use nome em três níveis. | Evita inventar origem e schema. | `@main.crm.clientes` |
| `{{CONTEXTO_NEGOCIO}}` | Explique decisão, processo e consumidor. | Dá significado aos achados. | elegibilidade para campanha |
| `{{GRANULARIDADE}}` | Diga o que uma linha representa. | Evita somar entidades incompatíveis. | cliente por mês |
| `{{PK_OU_NAO_INFORMADO}}` | Informe chave simples/composta ou lacuna. | Permite testar unicidade. | `id_cliente, mes_ref` |
| `{{COL_DATA_OU_NAO_INFORMADO}}` | Informe o tempo de observação. | Evita leakage e período ambíguo. | `dt_referencia` |
| `{{TARGET_DEFINICAO_OU_NAO_APLICAVEL}}` | Defina coluna, evento positivo e janela. | Evita interpretar a classe errada. | adesão em 30 dias |
| `{{PERIODO_E_FILTROS}}` | Declare início, fim, população e exclusões. | Torna o universo reproduzível. | 2025-01 a 2026-06; PF ativa |
| `{{VOLUME_OU_NAO_INFORMADO}}` | Informe linhas, partições ou ordem de grandeza. | Orienta estratégia de execução. | cerca de 200 milhões de linhas |
| `{{FOCO}}` | Priorize perguntas e riscos. | Direciona profundidade e gráficos. | qualidade e viés por canal |
| `{{RESTRICOES}}` | Liste compute, prazo, PII e bibliotecas. | Previne custo e exposição indevidos. | serverless; sem valores identificáveis |
| `{{NOTEBOOK_RELATORIO_OU_CODIGO}}` | Escolha o artefato final e formato. | Evita uma entrega inutilizável. | notebook + resumo executivo |

## Prompt pronto para colar

```text
Use @hub-ml-eda-profissional para construir uma EDA completa, auditável e adequada
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

## O que conferir na resposta

- O recurso, o período e o grão usados coincidem com o que foi anexado e preenchido.
- Evidência observada está separada de hipótese, default e recomendação.
- Código, execução e escrita estão rotulados sem apresentar proposta como ação realizada.
- Limitações, validações não executadas e decisões pendentes aparecem explicitamente.

## Limites

- Este formulário não concede acesso, permissão de escrita, execução ou deploy.
- Campo ausente deve permanecer `NÃO INFORMADO`; não invente schema ou regra de negócio.
- Resultado material precisa de validação proporcional ao risco e, quando aplicável,
  revisão humana de negócio, Risco, Compliance ou operação.

## Follow-ups úteis

- “Transforme o backlog crítico em regras de qualidade propostas, sem executar.”
- “Crie uma versão executiva com apenas evidências que mudam a decisão.”
- “Prepare o handoff para Cross-EDA ou feature engineering, com riscos de leakage.”
