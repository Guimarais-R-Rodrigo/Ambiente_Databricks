# `mlflow_run` — contexto governado para registro mínimo obrigatório no MLflow

<!-- readme-objeto: 1.0.0 -->

Este objeto oferece dois contextos MLflow. `run_governado` exige o registro de modelo sklearn com exemplo de entrada. `run_micromodelo` acrescenta registro E0 rule-based com fingerprint MM02, contrato de saída e métricas agregadas reconciliadas, sem exigir um modelo sklearn. Ambos organizam registro; nenhum substitui aprovação ou validação.

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

Use `run_governado` para baselines treináveis que registram modelo sklearn e um exemplo de entrada, verificando separadamente a assinatura efetivamente persistida. Use `run_micromodelo` no laboratório sintético E0 quando uma regra sem modelo sklearn precisa registrar DEVELOPMENT, VALIDATION ou SCORING, com contagens agregadas e referência de execução. Confira separadamente autorização do experimento MLflow no runtime.

## 4. Quando não usar?

Não use nenhum deles como substituto de Model Registry, aprovação, lineage completo ou governança institucional. `run_micromodelo` não registra resultados por entidade nem serve para dataset real: sua entrada exige o prefixo declarativo `synthetic:`. Não use `run_governado.modelo()` para objeto arbitrário, pois chama `mlflow.sklearn.log_model`.

## 5. Como funciona, intuitivamente?

`run_governado` exige parâmetros, métricas e uma chamada `modelo(..., exemplo_entrada=...)` no fechamento completo; sua flag interna de assinatura verifica apenas se o exemplo não é `None`. `run_micromodelo` verifica tipo, SHA-256 MM02, dataset/split sintéticos, limitações e contrato de saída antes de abrir o run. Seu coletor registra somente parâmetros de configuração da allowlist fechada e agregados: população, contagens TRUE/FALSE/INDETERMINADO e, opcionalmente, mínimo/média/máximo do score 0–100. As contagens devem somar a população; população zero não admite estatísticas de score. No fechamento, falta de parâmetros ou agregados gera `ValueError` e não grava `mm06.complete=true`.

## 6. Exemplo de situação

Um baseline pode registrar dataset, split, limitações, hiperparâmetros, métricas e exemplo de entrada. Um micromodelo sintético pode registrar população 4 com 1 TRUE, 1 FALSE e 2 INDETERMINADO, junto da referência de execução; as contagens devem reconciliar.

## 7. O que você precisa antes de usar?

MLflow precisa estar importável e operacional no runtime. `limitacoes` deve ser iterável de itens; passe uma lista de strings. `modelo(..., exemplo_entrada=...)` é necessário para marcar a flag local de assinatura como presente; não verifica o schema gravado pelo backend.

Para `run_micromodelo`, informe fingerprint SHA-256 MM02 já validado, `tipo`, `dataset` e `split` iniciados por `synthetic:`, limitações não vazias e `contrato_saida` com `grain`, `classification_field`, os três `classification_values`, `score_field` e `score_semantics`. O prefixo é declaração do caller, não verificação de origem sintética. Dentro do bloco, chame `parametros` com pelo menos uma das chaves de configuração permitidas (`regra`, `versao_regra`, `limiar`, `janela_dias`, `normalizacao`, `politica_indeterminado`, `score_habilitado`) e `agregados_medidos(..., referencia_execucao=...)`. Chaves como `client_id` são rejeitadas antes de enviar parâmetros ao MLflow. Se `experimento` for fornecido, o helper chama `mlflow.set_experiment` antes de abrir o run.

## 8. O que este recurso entrega?

`input_example` não é prova de assinatura completa. O coletor marca `_tem_assinatura` somente pela presença de `exemplo_entrada`, sem reler o artefato MLflow. Quando executar o registro autorizado, confira a assinatura efetiva no artefato do modelo (tipos, nomes e formas de entrada/saída) antes de afirmar completude de schema. Não infira esse resultado apenas de `pendencias() == []`.

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

O fingerprint repetido no exemplo mostra apenas o formato de 64 caracteres hexadecimais. Em uso, obtenha o fingerprint da especificação validada e confirme o experimento/tracking autorizado. Consulte o exemplo MM06 e seu relatório de evidência para os ambientes já exercitados.

## 10. Decisões e configurações que mais importam

No coletor de `run_micromodelo`, `agregados_medidos` aceita uma única chamada bem-sucedida por contexto; nova chamada é recusada. Prepare e reconcilie o agregado antes de registrar. Ao sair do `with`, inclusive por exceção, o coletor é invalidado e não pode ser reutilizado. Se houver `score_field`, o valor exato permitido para `score_semantics` é `"FORCA_EVIDENCIA"`; sem campo de score, ambos são `None`.

`exigir_completo=False` relaxa a verificação de fechamento, mas não torna um run incompleto adequado a decisões. `experimento` muda o destino do registro.

`nome` do artefato do modelo é passado como `artifact_path` em APIs antigas e `name` no fallback para versões que mudaram a assinatura.

Em `run_micromodelo`, não há `exigir_completo=False`: parâmetros e agregados reconciliados são obrigatórios. `score_field=None` exige `score_semantics=None`; caso haja score, a semântica precisa ser declarada. A política não transforma força de evidência em probabilidade. Com estatísticas `score_min`, `score_mean` e `score_max`, informe também `score_count`: a média cobre somente os scores emitidos, que podem ser menos que a população. Sem scores, `score_count=0` pode ser registrado sem o trio; `score_habilitado=False` recusa estatísticas de score.

Os valores dos parâmetros também são limitados: `regra`/`versao_regra` são rótulos curtos, `limiar` fica em 0–100, `janela_dias` em 1–3650, `normalizacao` usa os nomes do contrato MM01, `politica_indeterminado` permanece `INDETERMINADO` e `score_habilitado` é booleano. A allowlist não aceita campos de identificador ou resultado por indivíduo.

## 11. Limitações, riscos e armadilhas

Não há transação nem rollback de logging. Tags, parâmetros, métricas ou modelos já enviados podem permanecer no backend se uma chamada ou o fechamento falhar. Uma exceção no corpo do `with` também pode impedir a verificação final de completude. Antes de repetir, inspecione o run e os artefatos parciais; não trate exceção como garantia de que nada foi escrito nem apague recursos automaticamente.

O helper é acoplado ao flavor sklearn em `modelo()`. Para LightGBM, PyTorch ou outro flavor, registre o modelo com a API apropriada ou evolua o helper em uma mudança funcional separada.

A compatibilidade com MLflow depende do runtime gerenciado. O notebook registra que uma configuração de serverless Free deixou de abrir o run em determinada data; isso é evidência histórica, não regra eterna sobre todo serverless Databricks.

O `yield` ocorre antes da checagem final. Se o corpo do `with` lançar outra exceção, a verificação de completude após o `yield` não é executada; a exceção original se propaga.

`run_micromodelo` não possui API de artifact, linhas ou modelo sklearn. Allowlists fechadas de parâmetros e métricas impedem chaves de identificador e resultados individuais nessas superfícies; rótulos de regra, referências e limitações ainda exigem revisão do caller para evitar PII. `mm06.complete=true` atesta apenas completude estrutural deste wrapper; não atesta qualidade, medição independente, calibração, aprovação ou publicação. A mesma ressalva do `yield` vale para esta API.

## 12. Quais são as alternativas?

Use a API MLflow diretamente quando precisar de flavors específicos, nested runs, datasets estruturados, model registry ou logging avançado. O valor deste wrapper é a convenção mínima fail-closed.

## 13. Como saber se o resultado faz sentido?

Para `run_governado`, confira tags, parâmetros, métricas, artefatos, modelo e input example. Para `run_micromodelo`, confira fingerprint com o YAML MM01, tipo, recorte sintético, contrato de saída, referência de execução, reconciliação de contagens e `mm06.complete=true`. Teste caminho incompleto e MLflow indisponível. Run fechado não é modelo aprovado.

## 14. Arquivos relacionados e próximos passos

A implementação e a fachada expõem run_governado e run_micromodelo. O notebook demonstra o contexto de modelo sklearn. Para o contexto rule-based E0, consulte o exemplo MM06; verificar imports não substitui confirmar que o backend recebe e devolve o registro.

Depois do registro, métricas podem ser produzidas por [`metrics_report`](../metrics_report/README.md) e acompanhadas por [`performance_monitor`](../performance_monitor/README.md).

## 15. Referências

Evidências de manutenção, com escopos separados:

- [Testes locais com backend simulado](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/tools/tests/test_micromodelo_mm06_tracking.py): verificam chamadas/recusas do wrapper; não provam persistência real.
- [Exemplo de tracking E0](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/tools/micromodelo_mm06_e0_tracking.py) e [relatório datado de 29/09/2026](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/micromodelos/RELATORIO_ENTREGA_LAB.md): registram backend local real com MLflow 3.16.1 e leitura das runs.
- O mesmo relatório, seção “MLflow Free e instalação da skill”, delimita três runs sintéticas completas no Databricks Free, com configuração explícita de registry URI e experimento absoluto. As etapas usam a mesma fixture, sem holdout independente; não homologam o ambiente corporativo nem outra configuração.

Os scripts externos não são pré-requisitos ocultos do pacote e não devem ser executados apenas para ler este guia. Um ensaio de registro exige autorização de destino e efeitos próprios.

Consulte a documentação da versão MLflow usada para Tracking, start_run, logging e flavors. Antes de registrar, confirme tracking, experimento e permissões; falhas observadas em outra configuração de runtime não determinam o comportamento do seu ambiente.
