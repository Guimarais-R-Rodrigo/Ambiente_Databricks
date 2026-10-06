# `autoencoder_anomaly` — erro de reconstrução para priorizar anomalias, não veredito automático

<!-- readme-objeto: 1.0.0 -->

Este objeto treina um autoencoder PyTorch sobre uma referência que o chamador declara como normal e usa erro de reconstrução para pontuar casos novos. O limiar é um percentil dos erros do próprio treino; ele organiza uma fila de suspeita, mas **não estima probabilidade de fraude nem descobre sozinho a prevalência real de anomalias**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Rede neural que tenta reconstruir a entrada e usa o erro de reconstrução como score de anomalia. |
| Para que serve? | Priorizar casos que se afastam do padrão aprendido na referência normal. |
| Use quando... | Há referência razoavelmente limpa de comportamento normal e relações multivariadas podem importar. |
| Evite quando... | O treino normal está contaminado, há poucos dados para validar ou é preciso uma decisão supervisionada/calibrada. |
| Precisa de... | NumPy, PyTorch; arrays 2D finitos com as mesmas colunas e treino com pelo menos duas linhas. |
| Entrega... | Modelo treinado, limiar escalar e erro de reconstrução por linha de `X_test`. |

Consulte a [implementação](autoencoder_anomaly.py), a [fachada pública](__init__.py) e o [notebook de exemplo](exemplo_autoencoder_anomaly.py).

## 1. O que é?

Um **autoencoder** é uma rede treinada para comprimir e reconstruir a própria entrada. Nesta pasta, a hipótese operacional é que a rede aprende regularidades dos casos apresentados como normais; uma linha mal reconstruída recebe erro maior e pode ser investigada como anomalia.

A implementação é específica: encoder/decoder simétricos, camadas densas com ReLU e `BatchNorm1d`, bottleneck configurável e perda MSE. Ela não é uma biblioteca geral de detecção de fraude.

## 2. Que problema este recurso resolve?

Ele responde: “quais linhas novas são difíceis de reconstruir para um modelo treinado na minha referência normal?”. Isso é útil quando o target de anomalia é ausente, atrasado ou incompleto.

A função não responde “esta linha é fraude?” e não conhece custo de investigação, risco, causalidade ou capacidade operacional.

## 3. Quando faz sentido usar?

Faz sentido quando existe amostra de referência suficientemente representativa do normal, as features são numéricas e relações entre variáveis podem carregar informação além de extremos univariados.

Também pode complementar métodos mais simples: compare ranking, estabilidade e custo com Isolation Forest ou regras antes de escolher.

## 4. Quando não usar?

Evite quando o objetivo é classificação supervisionada com rótulos confiáveis e calibração de probabilidade; nesse caso, um modelo supervisionado responde a outra pergunta.

Evite também tratar uma base histórica contaminada como “normal”. O código não identifica essa contaminação antes do treino: anomalias recorrentes podem ser aprendidas e reconstruídas.

## 5. Como funciona, intuitivamente?

A função converte treino e teste para `float32`, calcula média e desvio por feature **no `X_train_normal` recebido**, padroniza os dois conjuntos e treina o autoencoder em mini-batches.

Depois restaura o melhor estado observado pelo menor loss de treino, calcula o erro MSE de reconstrução de cada linha normal e define `threshold` como `np.percentile(train_errors, threshold_percentile)`. Por fim calcula o mesmo score no teste. Uma linha é considerada acima do limiar quando `test_error > threshold`.

## 6. Exemplo de situação

Uma equipe tem milhares de operações revisadas como rotina normal e quer priorizar novas operações que quebram relações entre variáveis. Ela treina com a referência normal, obtém erros no lote novo e revisa primeiro os maiores.

O [notebook](exemplo_autoencoder_anomaly.py) planta anomalias sintéticas sutis e mostra deliberadamente um caso em que o método erra bastante. Esse resultado é evidência da fixture, não taxa de acerto prometida.

## 7. O que você precisa antes de usar?

O código exige `batch_size > 1`, `epochs > 0`, `patience > 0`, `lr > 0` e `0 < threshold_percentile < 100`. Confirme também tipos/finitude dos parâmetros e capacidade da arquitetura; atender aos limites não torna a referência normal adequada.

`X_train_normal` e `X_test` precisam ser matrizes 2D, finitas e com a mesma quantidade de features. O treino exige ao menos duas linhas; o teste não pode ser vazio.

PyTorch precisa estar instalado. A fachada importa PyTorch ao carregar o módulo. `mlflow` é opcional no import, mas `log_mlflow=True` exige a biblioteca disponível e um ambiente onde registrar métricas faça sentido.

Não é necessário padronizar externamente para satisfazer o helper: ele faz sua própria padronização usando o treino recebido. Se você também padronizar antes, como no notebook histórico, haverá uma segunda transformação interna; documente e versione sua convenção para não treinar e inferir com pipelines diferentes.

## 8. O que este recurso entrega?

`train_autoencoder_anomaly` devolve `(model, threshold, test_errors)`.

O modelo recebe ainda os atributos `input_center_` e `input_scale_` usados internamente. `threshold` está na escala do MSE sobre os dados transformados internamente. `test_errors` possui uma posição por linha de `X_test`.

O retorno não contém rótulo booleano: a comparação `test_errors > threshold` é feita pelo consumidor.

## 9. Como usar este recurso no Hub?

Pontuar outro lote sem ajustar novamente, usando as mesmas features/ordem e todo o pré-processamento externo do treino:

```python
import numpy as np
import torch

X_futuro = np.asarray(X_futuro, dtype=np.float32)
assert X_futuro.ndim == 2 and np.isfinite(X_futuro).all()
assert X_futuro.shape[1] == len(model.input_center_)
Z = (X_futuro - model.input_center_) / model.input_scale_
device = next(model.parameters()).device
model.eval()
with torch.no_grad():
    entrada = torch.as_tensor(Z, dtype=torch.float32, device=device)
    scores_futuros = ((model(entrada) - entrada) ** 2).mean(dim=1).cpu().numpy()
marcados = scores_futuros > threshold
```

Divida em lotes se a matriz não couber na memória do device. O `threshold` continua no espaço padronizado do treino; não o compare a MSE em unidades originais e não ajuste outro scaler no lote futuro. Chamar `train_autoencoder_anomaly` de novo faz um novo treino.

Para persistência autorizada, guarde pesos, arquitetura, ordem das features, `threshold`, `input_center_`, `input_scale_` e qualquer transformação externa. Centro/escala são atributos NumPy comuns, não buffers PyTorch: salvar somente `state_dict()` perde essa parte do contrato. O bloco acima apenas calcula em memória, sem gravar pesos.

```python
from hub_snippets.ml.autoencoder_anomaly import train_autoencoder_anomaly

model, threshold, scores = train_autoencoder_anomaly(
    X_normal,
    X_novo,
    encoding_dim=8,
    threshold_percentile=95,
    log_mlflow=False,
)
suspeitos = scores > threshold
```

Antes de executar o [notebook de exemplo](exemplo_autoencoder_anomaly.py), note que ele instala `torch`, reinicia o Python e trabalha apenas com dados sintéticos em memória.

## 10. Decisões e configurações que mais importam

`threshold_percentile` controla diretamente o ponto de corte na distribuição de erro do treino. Percentil 95 significa que aproximadamente 5% dos **erros do treino** ficam acima desse valor; isso não significa que 5% do mundo real sejam anomalias.

`encoding_dim`, `epochs`, `batch_size`, `lr` e `patience` alteram capacidade, otimização e custo. O early stopping observa somente o loss de treino; não existe conjunto de validação separado nesta função.

O dispositivo é escolhido automaticamente entre CUDA e CPU.

## 11. Limitações, riscos e armadilhas

Treinar apenas no que foi rotulado operacionalmente como normal cria dependência forte da qualidade dessa referência. Concept drift também pode elevar erros sem que haja fraude.

O uso de `BatchNorm1d` faz lotes muito pequenos exigirem cuidado; a função evita um último batch unitário em alguns tamanhos, mas não transforma base minúscula em amostra suficiente.

A semente fixa melhora repetibilidade, mas execução em hardware/bibliotecas diferentes ainda pode variar.

`log_mlflow=True` produz efeito externo de tracking. O helper não abre explicitamente um run; ele registra no contexto MLflow disponível.

## 12. Quais são as alternativas?

[`isolation_forest`](../isolation_forest/README.md) é uma alternativa não supervisionada mais simples e barata de treinar, especialmente como baseline. Regras robustas por domínio podem ser melhores quando os padrões suspeitos já são conhecidos.

Se há rótulo confiável do evento, modelos supervisionados do Hub podem ser mais adequados, mas respondem a um problema diferente.

## 13. Como saber se o resultado faz sentido?

Reserve casos rotulados ou revisados que não participaram do ajuste e avalie precisão, recall/cobertura, carga de investigação e estabilidade do score. Confira a distribuição de erros do treino versus período novo e revise os maiores erros manualmente.

Teste também um baseline simples. Execução sem erro e loss pequeno não demonstram capacidade de detectar o tipo de anomalia relevante.

## 14. Arquivos relacionados e próximos passos

A [implementação](autoencoder_anomaly.py) contém arquitetura e treino; a [fachada](__init__.py) exporta `SEED`, `Autoencoder` e `train_autoencoder_anomaly`; o [notebook](exemplo_autoencoder_anomaly.py) mostra um caso sintético com desempenho imperfeito.

Para caracterizar os casos marcados, combine o score com análise de features e revisão humana; não converta o percentil em política automática sem validação.

## 15. Referências

Consulte a documentação de torch.nn.BatchNorm1d e verifique versões e recursos do ambiente. O detector precisa de validação com casos independentes; a execução do exemplo sintético não comprova eficácia no dado real.

Referências primárias de conceito/API: [Documentação primária de autoencoder_anomaly](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm1d.html).
