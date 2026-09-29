# `mlflow_run` — contexto governado para registro mínimo obrigatório no MLflow

<!-- readme-objeto: 1.0.0 -->

Este objeto oferece dois contextos MLflow. `run_governado` mantém o contrato de modelo sklearn com assinatura. `run_micromodelo` acrescenta registro E0 rule-based com fingerprint MM02, contrato de saída e métricas agregadas reconciliadas, sem exigir um modelo sklearn. Ambos organizam registro; nenhum substitui aprovação ou validação.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Context managers separados para modelo sklearn e micromodelo rule-based E0. |
| Para que serve? | Evitar experimentos tecnicamente registrados, mas impossíveis de reconstruir ou interpretar depois. |
| Use quando... | MLflow está disponível e o run precisa de convenção mínima auditável. |
| Evite quando... | O runtime não suporta MLflow ou o run já é gerido por outro contexto incompatível. |
| Precisa de... | `mlflow`; `run_governado.modelo()` exige flavor sklearn; `run_micromodelo` exige entradas sintéticas declaradas. |
| Entrega... | Coletor de registro; efeitos persistentes no backend MLflow quando executado. |

Consulte a [implementação](mlflow_run.py), a [fachada](__init__.py) e o [notebook](exemplo_mlflow_run.py).

## 1. O que é?

`run_governado` é o `contextmanager` original: valida metadados, registra tags e oferece parâmetros, métricas, modelo e artefatos. A API aditiva `run_micromodelo` aceita somente `DEVELOPMENT`, `VALIDATION` ou `SCORING` sintéticos; associa o run ao fingerprint da especificação e só recebe configuração e agregados medidos. Não oferece método de modelo ou artefato individual.

## 2. Que problema este recurso resolve?

Um run com AUC e hiperparâmetros pode continuar inútil se não disser qual dataset, corte temporal ou limitação sustentava aquela métrica. Para micromodelos rule-based, o mesmo problema inclui confundir fingerprint de especificação com execução e guardar contagens individuais no tracking. Os dois contextos tornam seus campos mínimos explícitos.

## 3. Quando faz sentido usar?

Use `run_governado` para baselines treináveis que registram modelo sklearn e assinatura. Use `run_micromodelo` no laboratório sintético E0 quando uma regra sem modelo sklearn precisa registrar DEVELOPMENT, VALIDATION ou SCORING, com contagens agregadas e referência de execução. Confira separadamente autorização do experimento MLflow no runtime.

## 4. Quando não usar?

Não use nenhum deles como substituto de Model Registry, aprovação, lineage completo ou governança institucional. `run_micromodelo` não registra resultados por entidade nem serve para dataset real: sua entrada exige o prefixo declarativo `synthetic:`. Não use `run_governado.modelo()` para objeto arbitrário, pois chama `mlflow.sklearn.log_model`.

## 5. Como funciona, intuitivamente?

`run_governado` conserva a checagem original de parâmetros, métricas e assinatura no fechamento completo. `run_micromodelo` verifica tipo, SHA-256 MM02, dataset/split sintéticos, limitações e contrato de saída antes de abrir o run. Seu coletor registra somente parâmetros de configuração da allowlist fechada e agregados: população, contagens TRUE/FALSE/INDETERMINADO e, opcionalmente, mínimo/média/máximo do score 0–100. As contagens devem somar a população; população zero não admite estatísticas de score. No fechamento, falta de parâmetros ou agregados gera `ValueError` e não grava `mm06.complete=true`.

## 6. Exemplo de situação

Um baseline de propensão é registrado com versão do dataset, split temporal, limitações, hiperparâmetros, métricas e exemplo de entrada. No E0, uma regra sintética que classificou quatro entidades pode registrar 1 TRUE, 1 FALSE e 2 INDETERMINADO, além de referência da execução. O teste local usa MLflow simulado: verifica chamadas e falhas, sem provar backend real ou Databricks Free.

## 7. O que você precisa antes de usar?

MLflow precisa estar importável e operacional no runtime. `limitacoes` deve ser iterável de itens; passe uma lista de strings. `modelo(..., exemplo_entrada=...)` é necessário para marcar a assinatura como presente.

Para `run_micromodelo`, informe fingerprint SHA-256 MM02 já validado, `tipo`, `dataset` e `split` iniciados por `synthetic:`, limitações não vazias e `contrato_saida` com `grain`, `classification_field`, os três `classification_values`, `score_field` e `score_semantics`. O prefixo é declaração do caller, não verificação de origem sintética. Dentro do bloco, chame `parametros` com pelo menos uma das chaves de configuração permitidas (`regra`, `versao_regra`, `limiar`, `janela_dias`, `normalizacao`, `politica_indeterminado`, `score_habilitado`) e `agregados_medidos(..., referencia_execucao=...)`. Chaves como `client_id` são rejeitadas antes de enviar parâmetros ao MLflow. Se `experimento` for fornecido, o helper chama `mlflow.set_experiment` antes de abrir o run.

## 8. O que este recurso entrega?

`run_governado` retorna o coletor existente com `parametros`, `metricas`, `modelo`, `artefato` e `pendencias`. `run_micromodelo` retorna coletor com `parametros`, `agregados_medidos` e `pendencias`; tags incluem fingerprint, tipo, dataset/split, limitações, contrato de saída e completude. O efeito externo depende do backend MLflow disponível.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.mlflow_run import run_governado

with run_governado(
    "baseline",
    dataset="catalog.schema.features@2026-08",
    split="temporal: treino <= 2026-06; teste 2026-07",
    limitacoes=["target com maturação parcial"],
) as run:
    run.parametros({"algoritmo": "logistic_regression"})
    run.metricas({"auc_val": 0.78})
    run.modelo(modelo, exemplo_entrada=X_val[:5])
```

O bloco produz efeitos no backend MLflow configurado para a sessão. Antes de executar, confirme o experimento/tracking autorizado e use o flavor adequado ao tipo real do modelo; o atalho `run.modelo()` é sklearn.

Para o caminho rule-based E0, use a mesma fachada pública do snippet:

```python
from hub_snippets.ml.mlflow_run import run_micromodelo

with run_micromodelo(
    "micromodelo_sintetico", tipo="DEVELOPMENT", spec_fingerprint="a" * 64,
    dataset="synthetic:fixture@2026-09", split="synthetic:janela_de_teste",
    limitacoes=["sem dados reais"],
    contrato_saida={"grain": "entidade por data", "classification_field": "classificacao",
                    "classification_values": ["TRUE", "FALSE", "INDETERMINADO"],
                    "score_field": "score", "score_semantics": "FORCA_EVIDENCIA"},
) as run:
    run.parametros({"regra": "sintetica_v1"})
    run.agregados_medidos({"population": 4, "count_true": 1, "count_false": 1,
                           "count_indeterminate": 2},
                          referencia_execucao="exec_sintetica_001")
```

O SHA repetido ilustra a forma do campo, não é fingerprint de uma especificação real. O exemplo acima é ilustrativo; a prova com fingerprint MM02 real e backend MLflow local está em `tools/micromodelo_mm06_e0_tracking.py` e no relatório de entrega do laboratório. A compatibilidade do backend Free permanece sem execução.

## 10. Decisões e configurações que mais importam

`exigir_completo=False` relaxa a verificação de fechamento, mas não torna um run incompleto adequado a decisões. `experimento` muda o destino do registro.

`nome` do artefato do modelo é passado como `artifact_path` em APIs antigas e `name` no fallback para versões que mudaram a assinatura.

Em `run_micromodelo`, não há `exigir_completo=False`: parâmetros e agregados reconciliados são obrigatórios. `score_field=None` exige `score_semantics=None`; caso haja score, a semântica precisa ser declarada. A política não transforma força de evidência em probabilidade.

Os valores dos parâmetros também são limitados: `regra`/`versao_regra` são rótulos curtos, `limiar` fica em 0–100, `janela_dias` em 1–3650, `normalizacao` usa os nomes do contrato MM01, `politica_indeterminado` permanece `INDETERMINADO` e `score_habilitado` é booleano. A allowlist não aceita campos de identificador ou resultado por indivíduo.

## 11. Limitações, riscos e armadilhas

O helper é acoplado ao flavor sklearn em `modelo()`. Para LightGBM, PyTorch ou outro flavor, registre o modelo com a API apropriada ou evolua o helper em sprint funcional separada.

A compatibilidade com MLflow depende do runtime gerenciado. O notebook registra que uma configuração de serverless Free deixou de abrir o run em determinada data; isso é evidência histórica, não regra eterna sobre todo serverless Databricks.

O `yield` ocorre antes da checagem final. Se o corpo do `with` lançar outra exceção, a verificação de completude após o `yield` não é executada; a exceção original se propaga.

`run_micromodelo` não possui API de artifact, linhas ou modelo sklearn. Allowlists fechadas de parâmetros e métricas impedem chaves de identificador e resultados individuais nessas superfícies; rótulos de regra, referências e limitações ainda exigem revisão do caller para evitar PII. `mm06.complete=true` atesta apenas completude estrutural deste wrapper; não atesta qualidade, medição independente, calibração, aprovação ou publicação. A mesma ressalva do `yield` vale para esta API.

## 12. Quais são as alternativas?

Use a API MLflow diretamente quando precisar de flavors específicos, nested runs, datasets estruturados, model registry ou logging avançado. O valor deste wrapper é a convenção mínima fail-closed.

## 13. Como saber se o resultado faz sentido?

Para `run_governado`, confira tags, parâmetros, métricas, artefatos, modelo e input example. Para `run_micromodelo`, confira fingerprint com o YAML MM01, tipo, recorte sintético, contrato de saída, referência de execução, reconciliação de contagens e `mm06.complete=true`. Teste caminho incompleto e MLflow indisponível. Run fechado não é modelo aprovado.

## 14. Arquivos relacionados e próximos passos

A [implementação](mlflow_run.py) contém ambos os contextos e a [fachada](__init__.py) reexporta `run_governado` e `run_micromodelo`. O [notebook](exemplo_mlflow_run.py) demonstra o caminho legado e documenta uma limitação observada de runtime; o teste MM06 novo usa fake MLflow e não substitui exemplo real.

Depois do registro, métricas podem ser produzidas por [`metrics_report`](../metrics_report/README.md) e acompanhadas por [`performance_monitor`](../performance_monitor/README.md).

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da R09. Referência primária: documentação oficial do MLflow para Tracking, `start_run`, logging e model flavors.

Revalide a versão e o comportamento no runtime Databricks de destino antes de transformar observações do notebook em regra operacional.
