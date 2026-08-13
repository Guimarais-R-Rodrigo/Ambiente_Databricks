# Prompt: comparação controlada de tabelas

> **PERSONALIZADO — NÃO AUTO-DESCOBERTO.** Adicione as duas tabelas com **Add context**
> ou `@`. A skill adequada depende de o foco ser qualidade, EDA ou modelagem.

## Antes de usar

Defina se a comparação é de schema, conteúdo, reconciliação, migração, período ou
drift. Sem chaves comparáveis, peça primeiro uma análise de granularidade.

## Prompt pronto para colar

```text
Compare os dois recursos anexados de modo reprodutível e somente leitura.

CONTEXTO
- Recurso A: {{TABELA_A}}
- Recurso B: {{TABELA_B}}
- Objetivo/tipo de comparação: {{TIPO_COMPARACAO}}
- Unidade de análise: {{GRANULARIDADE}}
- Chaves de correspondência: {{CHAVES}}
- Coluna temporal e período: {{COL_DATA_E_PERIODO}}
- Colunas críticas: {{COLUNAS_CRITICAS_OU_TODAS}}
- Tolerâncias: {{TOLERANCIAS_OU_PROPOR}}
- Filtros equivalentes: {{FILTROS}}
- Restrições: {{RESTRICOES}}

FLUXO
1. Verifique que A e B foram anexadas e confirme schemas, tipos e granularidade.
2. Compare cobertura temporal, contagens, chaves, duplicidade, colunas ausentes,
   mudanças de tipo, nulos e estatísticas relevantes.
3. Faça reconciliação por chave com categorias: somente A, somente B, iguais e
   divergentes. Antes, valide que o join não é muitos-para-muitos inesperado.
4. Para números, use tolerâncias absolutas/relativas explícitas; para timestamps,
   declare timezone e precisão; para strings, não normalize silenciosamente.
5. Em alto volume, use Spark SQL/PySpark, pruning e agregações. Não colete registros
   completos ao driver e não exponha valores sensíveis.
6. Não altere tabelas. Qualquer proposta de correção deve ficar separada da análise.

CONTRATO DE SAÍDA
- Veredito resumido: compatível, compatível com ressalvas ou incompatível.
- Matriz de diferenças de schema e scorecard de conteúdo.
- Métricas de reconciliação com numeradores, denominadores e taxas.
- Top diferenças priorizadas, causas prováveis marcadas como hipóteses.
- Código executável e parametrizado para repetir a comparação.
- Limitações e recomendação de aceite/rejeição sem tomar a decisão pelo usuário.

VALIDAÇÃO FINAL
- Confirme filtros idênticos e ausência de multiplicação pelo join.
- Inclua nulos nas comparações e explique tolerâncias.
- Declare contagens antes/depois e o escopo efetivamente lido.
```

## Exemplo mínimo

A = `@main.legacy.clientes`; B = `@main.silver.clientes`; chave = `id_cliente`;
tipo = reconciliação pós-migração; tolerância = 0,01 para saldo.

## Follow-ups úteis

- “Gere um teste automatizado de regressão a partir desta comparação.”
- “Investigue apenas as chaves divergentes, mantendo valores anonimizados.”
- “Proponha uma regra de aceite para a próxima carga.”
