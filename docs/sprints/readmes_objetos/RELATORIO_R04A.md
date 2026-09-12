# R04-A — seis READMEs de operações Spark

Data: 2026-09-12. Autor e revisor próprio: ChatGPT (A0_light).
Base fixa: `1be947b0a62c3b0b85fa3cd5692f474b9066d85f`, `main` após a integração
coordenada de R03-A/R03-B com V01.
Branch de trabalho: `codex/readmes-r04a`.

## Escopo e autorização

O pedido “Ok, siga” autorizou a próxima leva prevista no plano. Essa autorização
não é aceite editorial antecipado, auditoria independente, autorização automática
de merge ou publicação. A R04-A documenta somente seis snippets Spark:
`date_features`, `join_diagnostics`, `null_summary`, `psi_calculator`,
`safe_display` e `smart_sample`.

O contrato 1.0.0 e os 19 READMEs operacionais + três exemplares já integrados
foram tratados como base. Nenhum algoritmo, fachada pública, dependência ou gate
permanente é alterado para adequar o código ao texto.

## READMEs novos

| Pasta sob `.assistant/hub_snippets/spark/` | Pergunta central |
|---|---|
| `date_features/` | Como derivar calendário sem confundir nove feriados fixos com calendário completo? |
| `join_diagnostics/` | Como estimar cobertura, multiplicidade e expansão antes de um join? |
| `null_summary/` | Como quantificar `NULL` e interpretar limiares sem tratá-los como política validada? |
| `psi_calculator/` | Como medir mudança de distribuição e entender os buckets/limites do helper? |
| `safe_display/` | Como limitar o volume enviado ao renderer sem prometer barateamento do plano upstream? |
| `smart_sample/` | Como amostrar distinguindo teto simples de tamanho exato estratificado condicional? |

Cada pasta recebe `README.md` com as quinze seções do contrato, visão rápida,
cenário sintético, uso mínimo, contraindicações, entradas/saídas, riscos,
verificação e links reais. Nenhum objeto da R04-B é documentado nesta entrega.

## Outras documentações atualizadas

A [matriz nominal](MATRIZ_ALTERACOES_R04A.md) identifica cada caminho efetivamente
alterado no fechamento. As mudanças de autoria incluem:

- seis `exemplo_*.py`: backlink para o README e correções de prosa onde o texto
  anterior extrapolava a implementação; o código executável, magics e saídas
  históricas permanecem preservados;
- `hub_snippets/README.md`: rotas por objeto para os snippets Spark;
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`: rotas locais e correções sobre
  calendário fixo, limiares de nulos e tamanho da amostra; a cópia da raiz é
  sincronizada, não redigida separadamente;
- `CLAUDE.md`, `PLANO_HUB.md`, `docs/sprints/README.md` e índice da iniciativa:
  estado da R04-A e ponto de parada antes da R04-B;
- `CONTROLE_MIGRACAO.json`: retirada apenas das seis dispensas correspondentes;
  candidata com **25/74 operacionais, 3/3 exemplares e 49 pendências**;
- `CHANGELOG.md` e `README.md` da raiz: registro aditivo e contagens produzidas
  pelo validador, sem recertificar publicação histórica;
- simulado: regenerado exclusivamente por `tools/render_simulado.py --write`.

Novos registros desta sprint: este relatório, a matriz, os
[achados](ACHADOS_R04A.md), a [rubrica](RUBRICA_R04A.json) e scripts/logs em
`evidencias_r04a/`. Esses arquivos não contam como READMEs operacionais.

## Verificações e alcance

O fechamento local em Python 3.13.5 passou nas **oito etapas** do gate permanente.
Por execução, os grupos de `unittest` somam **195 casos aprovados e sete opcionais
Spark pulados**: biblioteca 45; ferramentas 39; transição 36 aprovados + sete
pulados; READMEs 49; regressões Concierge 14; integração Concierge 12. A checagem
estrutural do pacote Concierge também passou, mas não é inventada como caso de
`unittest`. Reexecuções não devem ser somadas como testes novos.

As três suítes V00 foram reexecutadas localmente: **27 + 12 + 9 = 48 aprovados**.
As duas suítes V01 também passaram: **114 + 24 = 138 aprovados**. Isso protege o
trabalho visual integrado antes de qualquer submissão desta leva.

O suplemento `evidencias_r04a/verificar_r04a.py` contém **18 casos**: dois
portáteis e 16 que exigem Spark. Localmente, os dois portáteis passaram e os 16
Spark foram corretamente marcados como pulados porque PySpark não está instalado.
A primeira execução remota com PySpark 4.0.1 avançou por 17 casos e revelou uma
expectativa incorreta do próprio teste: `to_date('bad-date')` levantou
`CAST_INVALID_INPUT` com ANSI habilitado. O teste e o README foram corrigidos para
caracterizar esse contrato, sem mudar o helper. O fechamento remoto final deve
executar os 18 com Spark disponível e `--require-spark`, que transforma qualquer
skip em falha. O suplemento inclui a execução do primeiro bloco Python de cada novo
README.

O verificador `evidencias_r04a/verificar_preservacao.py` passou localmente: 205
arquivos Python do produto preservados; seis notebooks com AST, magics, código e
saídas históricas preservados; 22 READMEs anteriores intactos; 332 caminhos
protegidos; 16 formulários; exatamente seis dispensas removidas; 49 pendências;
459 arquivos da fonte espelhados e três cópias do Manual idênticas. Os grupos
podem se sobrepor e não devem ser somados como arquivos únicos.

Criar uma SparkSession local no runner caracteriza o contrato dos helpers; não
homologa Databricks Runtime, serverless, Spark Connect, catálogos, permissões ou
desempenho de produção. Nenhum notebook completo é executado com dados persistentes.
Resultados remotos, versões e árvore exata devem ser anexados ao PR somente depois
da execução efetiva; este relatório não antecipa CI verde.

## Achados e limites

Os [achados](ACHADOS_R04A.md) registram quatorze pontos. Entre eles: calendário
fixo restrito em `date_features`; denominador de cobertura de join; ausência de
validação dos limiares em `null_summary`; construção de buckets/driver collection
no PSI/CSI; necessidade prática de `display_fn` no uso modular de `safe_display`;
e diferença entre teto simples e tamanho estratificado condicional em `smart_sample`.

Esses comportamentos foram explicados ou caracterizados. Nenhum teste de
caracterização transforma limitação em desenho recomendado. Correção funcional,
se desejada, deve ocorrer em tarefa própria.

## Checkpoint e próxima ação

Estado inicial deste relatório: **seis guias escritos e autorrevisados, ainda
pendentes de fechamento técnico, aceite editorial e integração**. A cobertura
25/74 pertence à candidata e não ao workspace enquanto o PR não for integrado.

Pausa antes da R04-B. A próxima leva prevista contém os scripts
`data_quality_check`, `doc_coverage`, `drift_detector`, `naming_checker`,
`rfv_calculator` e `schema_to_yaml`. Não executar essa leva sem nova autorização.
