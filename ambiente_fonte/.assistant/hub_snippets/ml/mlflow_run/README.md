# `mlflow_run` — registrar um experimento com contexto e limites explícitos

<!-- readme-objeto: 1.0.0 -->

Este snippet envolve um run MLflow em uma convenção local de registro. Pede descrição dos dados, separação de amostras, limitações, parâmetros, métricas e exemplo de entrada do modelo. Ajuda a não esquecer informações; não certifica que sejam verdadeiras ou suficientes para aprovar o modelo.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Contexto `run_governado` com checagem de preenchimento. |
| Para que serve? | Registrar experimentos com uma convenção mínima comum. |
| Use quando... | Há backend MLflow configurado e autorização para gravar seus artefatos. |
| Evite quando... | Já existe run ativo ou o modelo requer outro flavor de registro. |
| Precisa de... | MLflow; para `modelo`, scikit-learn e objeto compatível com seu flavor. |
| Entrega... | Registros no backend e um coletor no bloco `with`; não uma implantação. |

**Há escrita:** o helper e o [notebook de exemplo](exemplo_mlflow_run.py) podem criar runs e gravar parâmetros, métricas, modelo e amostras de entrada no destino MLflow configurado. Confira destino e permissões antes de executar. Veja também a [implementação](mlflow_run.py) e a [fachada](__init__.py).

## 1. O que é?

Um experimento agrupa execuções; cada run reúne informações de uma tentativa. Parâmetros descrevem escolhas, métricas registram resultados e artefatos guardam arquivos ou modelos. Uma assinatura descreve os tipos esperados de entrada e saída de um modelo — não é assinatura digital nem aprovação humana.

`run_governado` é uma convenção do Hub construída sobre MLflow. Não é uma funcionalidade nativa chamada “run governado” na Databricks e não substitui controles de acesso ou aprovação.

## 2. Que problema este recurso resolve?

Ajuda a responder “consigo entender como esta execução foi feita e o que seu resultado não sustenta?”. Sem a origem dos dados, o recorte temporal e as limitações, duas métricas parecidas podem vir de avaliações muito diferentes.

A checagem no encerramento evita esquecimentos de preenchimento. A qualidade das descrições, do split e da avaliação continua dependendo de quem produz e revisa o experimento.

## 3. Quando faz sentido usar?

Use para tentativas que precisam ser comparáveis e recuperáveis: um baseline, um candidato a modelo ou um experimento com escolhas bem definidas. Forneça descrição reconstruível dos dados, incluindo versão ou corte, e diferencie treino, validação e teste.

O flavor fixo é `mlflow.sklearn`. Ele é apropriado para modelos compatíveis com essa interface; o fato de outra biblioteca ser suportada pelo MLflow não significa que este wrapper use o flavor específico dela.

## 4. Quando não usar?

Não abra o contexto dentro de outro run ativo esperando aninhamento automático. Ele chama `mlflow.start_run` sem `nested=True` e não encerra o run anterior. A separação funciona entre blocos sucessivos já fechados, não como limpeza automática da sessão.

Para um modelo Spark, PyTorch ou um Booster que exige tratamento específico, use diretamente o flavor adequado. Não force o registro como sklearn somente para satisfazer a convenção de preenchimento.

## 5. Como funciona, intuitivamente?

Ao entrar no contexto, verifica MLflow disponível, campos textuais não vazios segundo a conversão usada e pelo menos uma limitação. Opcionalmente seleciona um experimento, abre o run e grava tags `dataset`, `split` e `limitacoes`.

Dentro do bloco, o coletor registra parâmetros, métricas, modelo e arquivos. Ao sair normalmente, verifica se recebeu parâmetros, métricas e uma chamada `modelo` com `exemplo_entrada` diferente de `None`. Se houver pendências e `exigir_completo=True`, levanta erro.

Essa falha não desfaz logs já gravados. É um registro incompleto que falhou, não uma transação revertida. Uma exceção no corpo também pode deixar evidências parciais no backend.

## 6. Exemplo de situação

Duas tentativas apresentam AUC semelhante, mas uma usa teste temporal e outra mede o próprio treino. Descrever o split e a limitação permite perceber que os números não sustentam a mesma conclusão.

O exemplo abaixo registra acurácia de treino sobre seis linhas sintéticas para demonstrar a mecânica, não qualidade preditiva. Essa limitação é declarada em vez de esconder a diferença entre registro bem formado e avaliação válida.

## 7. O que você precisa antes de usar?

Confira as URIs de tracking e registry, o experimento permitido, as credenciais e o armazenamento de artefatos. `experimento` muda o experimento ativo da sessão por meio do MLflow; a configuração anterior não é restaurada pelo helper. Ele não configura o backend nem administra suas permissões.

Use strings significativas para `nome`, `dataset` e `split`, e uma lista de strings para `limitacoes`. A implementação aceita valores por conversão textual e não é um validador rígido de tipos: `None` não equivale a descrição útil, e passar uma string em `limitacoes` pode fazê-la ser percorrida caractere a caractere.

`input_example` pode persistir linhas de entrada. Use dados sintéticos ou amostras autorizadas; não envie dados pessoais ou segredos em exemplos, tags, parâmetros ou arquivos.

## 8. O que este recurso entrega?

O `with` fornece um coletor com `parametros`, `metricas`, `modelo`, `artefato` e `pendencias`. Os métodos de registro não retornam o `ModelInfo` do MLflow nem o URI do modelo. Para identificar o run, consulte a API nativa `mlflow.active_run()` dentro do bloco e guarde seu ID.

`pendencias()` lista apenas parâmetros, métricas e a condição local chamada assinatura. `dataset` e `split` são tags textuais, não um snapshot, vínculo automático de linhagem ou divisão efetiva dos dados. `artefato()` é opcional e sua chamada não faz parte da checagem de completude.

## 9. Como usar este recurso no Hub?

**O bloco grava no backend MLflow ativo.** Execute somente depois de escolher um experimento de teste autorizado. Os dados são sintéticos, mas o registro é persistido no destino configurado:

```python
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.linear_model import LogisticRegression
from hub_snippets.ml.mlflow_run import run_governado

X = pd.DataFrame({"valor": [-3., -2., -1., 1., 2., 3.]})
y = [0, 0, 0, 1, 1, 1]
modelo = LogisticRegression().fit(X, y)
with run_governado(
    "demonstracao_registro",
    dataset="sintética: seis linhas declaradas neste exemplo",
    split="sem split: demonstração de registro",
    limitacoes=["sem avaliação fora do treino; não sustenta decisão de negócio"],
) as registro:
    registro.parametros({"algoritmo": "logistic_regression"})
    registro.metricas({"acuracia_treino": float(modelo.score(X, y))})
    registro.modelo(modelo, exemplo_entrada=X.iloc[:2])
    run_id = mlflow.active_run().info.run_id
```

O [notebook](exemplo_mlflow_run.py) inclui tentativas que podem falhar e relatos históricos de runtime. Leia-os como observações datadas, não como garantia de falha no Free ou de sucesso no trabalho. A R09 não executa esse notebook no seu workspace.

## 10. Decisões e configurações que mais importam

`exigir_completo=True` é o padrão. Com `False`, a verificação final não bloqueia parâmetros, métricas ou exemplo ausentes; validações da entrada e erros do backend continuam ocorrendo. Não use essa opção para dar aparência de completude a um registro incompleto.

`modelo(..., nome="model")` tenta `artifact_path` e, diante de `TypeError`, tenta `name`. Esse fallback não garante compatibilidade com toda versão do MLflow e pode também capturar `TypeError` causado por outro motivo.

`metricas` converte valores para `float`, mas não verifica que sejam finitos, estejam em escala correta ou venham de validação independente. Prefira nomes com unidade explícita: `ks_pct=40`, por exemplo, não se confunde com KS na escala 0–1.

## 11. Limitações, riscos e armadilhas

A condição `_tem_assinatura` verifica a presença de exemplo, **não inspeciona a assinatura realmente persistida**. O MLflow pode inferi-la a partir do modelo e do exemplo, mas sua existência e adequação precisam ser conferidas depois. O helper tampouco exige um arquivo adicional de artefato.

Nada impede descrições vagas ou afirmações incorretas sobre dados. O wrapper não testa reconstrução do dataset, vazamento, privacidade, estabilidade ou governança do modelo; não registra automaticamente uma versão no Unity Catalog nem cria endpoint de serving.

O notebook preserva um erro histórico `spark.mlflow.modelRegistryUri`. A documentação oficial atual apresenta MLflow no Free Edition; não é correto generalizar aquele erro para uma proibição permanente. O runtime, as URIs, as permissões e a versão precisam ser verificados no ambiente real. Free Edition é serverless, sem compute clássico; trocar para clássico não é solução disponível dentro dessa edição.

## 12. Quais são as alternativas?

Use diretamente `mlflow.start_run`, `log_params`, `log_metrics` e o flavor apropriado quando precisar de assinatura explícita, aninhamento, controle do retorno ou linhagem de dados. Isso dá flexibilidade, mas exige outra forma de garantir a convenção de registro.

Para só avaliar números sem persistir, [`metrics_report`](../metrics_report/README.md) pode atender. Para comparar deterioração por período, use [`performance_monitor`](../performance_monitor/README.md) junto de uma estratégia externa de armazenamento.

## 13. Como saber se o resultado faz sentido?

Abra o run e confira tags, parâmetros, métricas e arquivos. Inspecione a assinatura armazenada e faça uma previsão de teste com o modelo recarregado usando entradas autorizadas. Um contexto encerrado sem erro não prova que o contrato persistido seja o desejado.

Em experimento isolado, teste um registro completo, um com métrica ausente e uma exceção dentro do bloco. Confirme o estado do run e a existência de logs parciais; não presuma rollback. Verifique também que um run ativo externo não foi encerrado silenciosamente.

## 14. Arquivos relacionados e próximos passos

A [implementação](mlflow_run.py) define o coletor e a checagem; a [fachada](__init__.py) expõe `run_governado`; o [notebook](exemplo_mlflow_run.py) mostra casos de recusa e registro. Consulte o [catálogo](../../README.md) e o [Manual](../../../MANUAL_TECNICO.md) para o fluxo de avaliação e registro.

O próximo passo é revisar a informação persistida e sua procedência. Registro completo não autoriza promover um modelo nem compartilhar dados além das permissões existentes.

## 15. Referências

Fonte do contrato: implementação e fachada locais. Referências primárias consultadas em 13/09/2026: [MLflow `start_run`](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html#mlflow.start_run), [flavor sklearn e inferência de assinatura](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html), [MLflow na Databricks](https://docs.databricks.com/aws/en/mlflow) e [limites do Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).

Autorrevisão R09. Os testes da sprint usam backend local isolado com dados sintéticos; não comprovam acesso, funcionamento ou publicação no Databricks Free ou no trabalho.
