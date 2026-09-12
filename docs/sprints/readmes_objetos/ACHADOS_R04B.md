# Achados da R04-B — Hub Scripts

Data da revisão: 2026-09-12. Escopo: `data_quality_check`, `doc_coverage`, `drift_detector`, `naming_checker`, `rfv_calculator` e `schema_to_yaml`.

Este documento registra limitações e comportamentos observados durante a leitura estática e a preparação dos testes. **Caracterizar um comportamento não significa aprová-lo como desejável.** Nenhuma implementação foi alterada nesta sprint documental.

## A01 — `data_quality_check`: o score é heurística local

O score começa em 100, perde 25 pontos por alerta `fail` e 5 por `warn`, com piso zero. Não existe calibração estatística, ponderação por impacto de negócio ou normalização entre tabelas. O README deve apresentá-lo, no máximo, como sinal de tendência sob a mesma política.

## A02 — `data_quality_check`: atualidade usa o relógio do processo Python

`days_old` compara o maior valor da coluna com `date.today()`. Não há `as_of_date` configurável, calendário útil, timezone de negócio ou tratamento de reprocessamento histórico. Uma política adequada para carga diária pode ser errada para fonte mensal.

## A03 — `data_quality_check`: duplicidade é excesso sobre combinações distintas

`duplicate_rows = total - distinct_pk`. O número quantifica excesso de linhas em relação às combinações distintas da chave; não devolve as chaves duplicadas nem explica a causa. Componentes nulos da chave são medidos separadamente.

## A04 — `doc_coverage`: 100% não é qualidade textual

Uma célula Markdown com apenas `.` cobre estruturalmente a célula de código adjacente. O script deliberadamente não lê a qualidade do texto. Usar a métrica como meta favoreceria gaming.

## A05 — `doc_coverage`: notebook sem código recebe 100%

Quando `total_code_cells == 0`, a fórmula devolve 100%. Isso significa “nenhuma célula de código descoberta” e não “documentação perfeita”.

## A06 — `drift_detector`: PSI é apenas numérico e classificação é opt-in

A implementação chama `approxQuantile` e foi construída para variáveis numéricas. Sem **ambos** `warning_threshold` e `critical_threshold`, o retorno é `not_classified`. O notebook menciona faixas usuais apenas como tradição/heurística; elas não são default do código.

## A07 — `drift_detector`: epsilon evita infinito, mas não renormaliza proporções

Buckets com proporção zero usam `epsilon` como piso antes do log. As proporções exibidas em `buckets` são as usadas no cálculo depois desse piso e não são renormalizadas para somar exatamente 1. Isso deve ser tratado como detalhe numérico do PSI, não como nova distribuição estimada.

## A08 — `naming_checker`: todas as violações são warnings

A implementação não emite severidade `error`. Transformar avisos em bloqueio de CI é decisão do consumidor. O campo `policy` separa recomendação de contexto da Databricks, convenção do projeto e regra opcional da organização.

## A09 — `naming_checker`: a checagem de três partes é textual

O script usa `table_name.split('.')`; não existe parser SQL de identificadores escapados. O próprio `spark.table` continua sendo quem resolve o objeto. Views temporárias legítimas recebem aviso de contexto por não possuírem `catalog.schema.table`.

## A10 — `rfv_calculator`: o corte é global e usa data, não disponibilidade

`dt_referencia` é único para todos os clientes da chamada. Isso não atende naturalmente observações com instante de decisão por linha. Além disso, cortar pela data do evento não impede leakage quando o dado só ficou disponível posteriormente.

## A11 — `rfv_calculator`: frequência conta linhas e duplicidade não é detectada

`frequencia_total` e `frequencia_Nd` usam `count(lit(1))`. Se a origem estiver em grão de item ou contiver duplicatas, a frequência cresce. Valores negativos/nulos também seguem a semântica normal de soma do Spark; não há regra de estorno ou moeda.

## A12 — `rfv_calculator`: janelas repetem agregação e join

Cada período gera filtro, `groupBy` e `left join`. A clareza é boa para poucas janelas, mas dezenas/centenas de períodos podem criar plano caro. A sprint não refatora essa estratégia.

## A13 — `schema_to_yaml`: `approx_distinct` é estimativa

Com `include_stats=True`, a cardinalidade usa `approx_count_distinct` com configuração padrão do Spark. Não deve ser usada para certificar unicidade.

## A14 — `schema_to_yaml`: formato textual depende da presença de PyYAML

Com PyYAML, o retorno é YAML gerado por `safe_dump`; sem a biblioteca, é JSON indentado. JSON é subconjunto oficial de YAML 1.2, mas ferramentas que esperam estilo YAML específico podem reagir de forma diferente. O payload lógico é o contrato mais estável.

## A15 — `schema_to_yaml`: estatísticas mudam o custo da operação

Sem `include_stats`, o helper trabalha com schema/metadata do DataFrame. Com `include_stats=True`, executa uma agregação com contagem total e duas expressões por coluna. Tabelas muito largas/grandes precisam de avaliação de custo.

## A16 — documentação do exemplo RFV contém uma inconsistência histórica de prosa

O bloco de output preservado mostra `valores_distintos_frequencia_total = 9`, enquanto um parágrafo posterior afirma 11 valores distintos e faixa de 6 a 17. Como a R04-B preserva outputs e código executável, a correção permitida é somente na prosa Markdown, alinhando-a ao output registrado ou removendo a afirmação não sustentada. Isso será coberto pela guarda de AST/magics/outputs.

## Tratamento nesta sprint

- Documentar os comportamentos acima nos READMEs.
- Corrigir somente prosa/backlinks dos notebooks quando necessário.
- Não mudar implementações para “fazer a documentação bater”.
- Executar casos controlados, incluindo PySpark 4.0.1 real no runner.
- Manter auditoria independente e homologação Databricks fora do escopo desta autorrevisão.