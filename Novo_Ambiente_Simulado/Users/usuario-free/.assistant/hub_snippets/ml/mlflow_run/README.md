# `mlflow_run` — contexto governado para registro mínimo obrigatório no MLflow

<!-- readme-objeto: 1.0.0 -->

Este objeto cria um contexto de run MLflow que exige dataset, split, limitações e, no fechamento completo, parâmetros, métricas e assinatura de entrada. Seu objetivo é **consistência de registro**; ele não substitui governança de modelo, aprovação ou validação.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Context manager que abre um run MLflow e verifica campos mínimos. |
| Para que serve? | Evitar experimentos tecnicamente registrados, mas impossíveis de reconstruir ou interpretar depois. |
| Use quando... | MLflow está disponível e o run precisa de convenção mínima auditável. |
| Evite quando... | O runtime não suporta MLflow, já existe outro run incompatível ou o flavor do modelo não é sklearn. |
| Precisa de... | `mlflow`; para `modelo()`, flavor sklearn e dependências correspondentes. |
| Entrega... | Contexto `_RunGovernado`; efeitos persistentes no backend MLflow. |

Consulte a [implementação](mlflow_run.py), a [fachada](__init__.py) e o [notebook](exemplo_mlflow_run.py).

## 1. O que é?

`run_governado` é um `contextmanager`. Ele valida metadados antes de abrir o run, registra tags e devolve um coletor com métodos para parâmetros, métricas, modelo e artefatos.

## 2. Que problema este recurso resolve?

Um run com AUC e hiperparâmetros pode continuar inútil se não disser qual dataset, corte temporal ou limitação sustentava aquela métrica. O helper transforma esses campos em parte explícita do contrato.

## 3. Quando faz sentido usar?

Use para baselines, comparações champion-challenger e experimentos que precisam ser revisitados. É especialmente útil quando múltiplos autores usam o mesmo workspace e precisam registrar informação mínima de forma consistente.

## 4. Quando não usar?

Não use como substituto de Model Registry, aprovação, lineage completo ou governança institucional. Não use `modelo()` para qualquer objeto arbitrário: a implementação chama `mlflow.sklearn.log_model`.

## 5. Como funciona, intuitivamente?

Antes do run, valida `nome`, `dataset`, `split` e pelo menos uma limitação. Dentro do contexto, `parametros`, `metricas` e `modelo` marcam o que foi registrado. Ao sair, se `exigir_completo=True`, qualquer ausência entre parâmetros, métricas e assinatura gera `ValueError`.

## 6. Exemplo de situação

Um baseline de propensão é registrado com versão do dataset, split temporal, limitações, hiperparâmetros, métricas e exemplo de entrada. Meses depois, o registro contém contexto suficiente para reconstruir o que foi avaliado.

## 7. O que você precisa antes de usar?

MLflow precisa estar importável e operacional no runtime. `limitacoes` deve ser iterável de itens; passe uma lista de strings. `modelo(..., exemplo_entrada=...)` é necessário para marcar a assinatura como presente.

Se `experimento` for fornecido, o helper chama `mlflow.set_experiment` antes de abrir o run.

## 8. O que este recurso entrega?

O retorno do contexto é um coletor com `parametros`, `metricas`, `modelo`, `artefato` e `pendencias`. O principal efeito é externo: criação e preenchimento do run no backend MLflow.

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

## 10. Decisões e configurações que mais importam

`exigir_completo=False` relaxa a verificação de fechamento, mas não torna um run incompleto adequado a decisões. `experimento` muda o destino do registro.

`nome` do artefato do modelo é passado como `artifact_path` em APIs antigas e `name` no fallback para versões que mudaram a assinatura.

## 11. Limitações, riscos e armadilhas

O helper é acoplado ao flavor sklearn em `modelo()`. Para LightGBM, PyTorch ou outro flavor, registre o modelo com a API apropriada ou evolua o helper em sprint funcional separada.

A compatibilidade com MLflow depende do runtime gerenciado. O notebook registra que uma configuração de serverless Free deixou de abrir o run em determinada data; isso é evidência histórica, não regra eterna sobre todo serverless Databricks.

O `yield` ocorre antes da checagem final. Se o corpo do `with` lançar outra exceção, a verificação de completude após o `yield` não é executada; a exceção original se propaga.

## 12. Quais são as alternativas?

Use a API MLflow diretamente quando precisar de flavors específicos, nested runs, datasets estruturados, model registry ou logging avançado. O valor deste wrapper é a convenção mínima fail-closed.

## 13. Como saber se o resultado faz sentido?

Abra o run no MLflow e confirme tags, parâmetros, métricas, artefatos, modelo e input example. Teste explicitamente o caminho incompleto e a indisponibilidade do runtime. Não confunda “run fechado” com “modelo aprovado”.

## 14. Arquivos relacionados e próximos passos

A [implementação](mlflow_run.py) contém o contexto e coletor; a [fachada](__init__.py) expõe apenas `run_governado`; o [notebook](exemplo_mlflow_run.py) documenta inclusive uma limitação observada de runtime.

Depois do registro, métricas podem ser produzidas por [`metrics_report`](../metrics_report/README.md) e acompanhadas por [`performance_monitor`](../performance_monitor/README.md).

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da R09. Referência primária: documentação oficial do MLflow para Tracking, `start_run`, logging e model flavors.

Revalide a versão e o comportamento no runtime Databricks de destino antes de transformar observações do notebook em regra operacional.