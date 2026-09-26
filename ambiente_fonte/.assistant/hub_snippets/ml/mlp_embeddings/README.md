# `mlp_embeddings` — MLP binária com representações aprendidas para categorias indexadas

<!-- readme-objeto: 1.0.0 -->

Uma *embedding* é uma tabela aprendida que transforma cada índice categórico em um vetor denso. Este módulo combina embeddings para categorias com features numéricas e uma rede MLP (*multilayer perceptron*). A classe pública também consegue construir saída de regressão, mas o treinador `train_embedding_mlp` desta versão implementa **apenas classificação binária**.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Uma classe PyTorch `EmbeddingMLP` e um treinador binário com early stopping por AUC. |
| Para que serve? | Testar representação densa aprendida para categóricas já indexadas, junto com variáveis numéricas. |
| Use quando... | Houver categorias com cardinalidade suficiente, volume para aprender embeddings e baseline de comparação. |
| Evite quando... | Quiser solução tabular simples, houver nível novo não tratado ou o problema não for binário no treinador pronto. |
| Precisa de... | PyTorch, NumPy, scikit-learn e MLflow se o logging for habilitado. |
| Entrega... | `EmbeddingMLP` treinada e `auc_val`, `gini_val`, `epochs_trained`. |

Consulte a [implementação](mlp_embeddings.py), a [fachada](__init__.py) e o [notebook](exemplo_mlp_embeddings.py). O exemplo instala `torch` sem versão fixada, reinicia o Python e desliga o logging do helper.

## 1. O que é?

`torch.nn.Embedding` funciona como uma tabela de consulta treinável: cada categoria é representada por um índice inteiro entre zero e a cardinalidade menos um, e esse índice recupera um vetor. Durante o treinamento, esses vetores são ajustados junto com os demais pesos para ajudar na tarefa.

`EmbeddingMLP` concatena as embeddings com as features numéricas e passa o resultado por camadas densas com BatchNorm, ReLU e Dropout. No modo binário, termina com um neurônio e Sigmoid; no modo de regressão da **classe**, termina com um neurônio linear.

`train_embedding_mlp`, porém, sempre instancia a classe no default `task="binary"`, usa `BCELoss` e AUC. Portanto o treinador pronto não é um treinador de regressão.

## 2. Que problema este recurso resolve?

A pergunta é: “Uma representação aprendida das categorias melhora a previsão binária em relação a representações mais simples?”. Embeddings podem compartilhar estrutura entre níveis por meio de vetores próximos, em vez de representar cada nível apenas como uma coluna independente.

Isso não significa que one-hot ou árvores “não conseguem” o problema. O ganho depende dos dados, da arquitetura, do volume por categoria e do baseline. O helper serve para testar a hipótese sob comparação controlada.

## 3. Quando faz sentido usar?

Use quando as categorias já foram mapeadas para índices estáveis, existem observações suficientes por nível e há razão para esperar estrutura compartilhável entre categorias. Compare com pelo menos um baseline de árvore ou modelo mais simples usando os mesmos splits.

Também pode ser útil quando a representação aprendida será reutilizada em uma arquitetura maior. Este wrapper específico, entretanto, só retorna o modelo completo; não fornece API separada de extração/exportação de embeddings.

## 4. Quando não usar?

Não use diretamente quando produção pode receber categorias inéditas e você não definiu uma política de “unknown”. `nn.Embedding` espera índices dentro do intervalo configurado; o treinador rejeita índices negativos ou `>= cat_dims[i]` e não cria bucket desconhecido.

Não use `train_embedding_mlp` para regressão apenas porque a classe `EmbeddingMLP(task="regression")` existe. O loop pronto continua binário: labels, loss e métrica são específicos desse caso.

## 5. Como funciona, intuitivamente?

Cada categórica recebe uma embedding. Se `cat_dims=[150,40]`, existem duas tabelas de vetores. Quando `emb_dims` não é informado na classe, cada dimensão vira `min(50,(cardinalidade+1)//2)`.

Os vetores das categorias de cada linha são concatenados às features numéricas. A sequência de camadas padrão é 256 → 128 → 64, cada uma com normalização, ReLU e dropout 0,3. No treinamento binário, Adam minimiza binary cross-entropy; gradientes são limitados por norma 1,0.

A cada época, o helper mede AUC na validação. Se melhora, salva uma cópia de `state_dict`; caso contrário incrementa a paciência. Ao final, restaura o melhor estado observado e devolve AUC/Gini do melhor checkpoint.

## 6. Exemplo de situação

Imagine categorias fictícias de agência e produto, cada uma codificada por índices inteiros, junto com renda e tempo de relacionamento. Há milhares de observações e você suspeita que certos níveis compartilham comportamento.

Depois de fixar treino/validação, você treina a MLP e compara AUC com um LightGBM sob os mesmos dados. Se a rede melhora de forma estável em validações pertinentes, a representação merece investigação. Um único resultado sintético não estabelece superioridade da família.

## 7. O que você precisa antes de usar?

`X_num_train`/`X_num_val` devem ser matrizes 2-D com o mesmo número de colunas e somente valores finitos. `y_train` e `y_val` são convertidos para `float32` e achatados.

`X_cat_train` e `X_cat_val` são listas: uma array por feature categórica. O tamanho das duas listas deve igualar `len(cat_dims)`, e cada array deve alinhar com seu split. Os valores são convertidos para `int64`; códigos precisam estar em `[0, cardinalidade)`.

O treino exige labels 0/1 e ambas as classes no **treino**. A validação é checada como 0/1, mas o código não exige localmente que ela contenha as duas classes; `roc_auc_score` falhará se houver só uma.

PyTorch, NumPy e scikit-learn são obrigatórios. MLflow é opcional com `log_mlflow=False` porque a importação é protegida.

## 8. O que este recurso entrega?

O treinador retorna `(model, metrics)`.

| Campo | Significado |
|---|---|
| `auc_val` | Melhor AUC observado durante as épocas de validação. |
| `gini_val` | `2*auc_val-1`. |
| `epochs_trained` | Número de épocas realmente percorridas no loop, não a época do melhor checkpoint necessariamente. |

O modelo é restaurado para `best_state`, mas `epochs_trained` registra `epoch+1` quando o loop terminou. Portanto “modelo da época N” e “quantidade de épocas percorridas” são conceitos diferentes.

A classe pública `EmbeddingMLP` também pode ser instanciada manualmente com `task="regression"`; isso não muda o escopo do treinador pronto.

## 9. Como usar este recurso no Hub?

```python
from hub_snippets.ml.mlp_embeddings import train_embedding_mlp

model, metrics = train_embedding_mlp(
    X_num_train,
    [agencia_train, produto_train],
    y_train,
    X_num_val,
    [agencia_val, produto_val],
    y_val,
    cat_dims=[150, 40],
    log_mlflow=False,
)
```

O [notebook](exemplo_mlp_embeddings.py) instala PyTorch e reinicia a sessão. A prosa histórica será ajustada nesta R05 para não dizer que one-hot “não expressa” relações ou que árvores necessariamente deixam de aprendê-las; o ponto correto é que embeddings oferecem uma representação densa compartilhável que deve ser comparada empiricamente.

## 10. Decisões e configurações que mais importam

`cat_dims` define os intervalos válidos dos códigos. Esse mapeamento é parte do contrato de inferência: a mesma categoria precisa receber o mesmo índice no futuro. O wrapper não serializa encoders nem dicionários de mapeamento.

Na classe, `emb_dims`, `hidden_layers`, `dropout` e `task` controlam arquitetura. O treinador não expõe esses argumentos: usa os defaults de `EmbeddingMLP`. Para alterar arquitetura via API atual, seria necessário instanciar/treinar manualmente ou evoluir o wrapper.

`epochs`, `batch_size`, `lr` e `patience` controlam o loop. O tamanho efetivo do batch é limitado pelo número de linhas; quando o resto da divisão seria exatamente 1, `drop_last=True` evita BatchNorm com batch unitário.

## 11. Limitações, riscos e armadilhas

A classe aceita `emb_dims` opcional, mas não valida que seu comprimento seja igual ao de `cat_dims`; ela cria embeddings com `zip(cat_dims, emb_dims)`. Uma lista curta pode criar menos embeddings do que categorias declaradas. O treinador não expõe `emb_dims`, então usa o caminho default seguro, mas consumidores diretos da classe devem conferir isso.

Não há normalização automática das numéricas, tratamento de missing, encoder de categorias, pesos de classe, calibração, seed de todos os backends CUDA, exportação do pré-processamento ou suporte a múltiplas GPUs.

O device é escolhido automaticamente entre CUDA e CPU. Semente 42 melhora repetibilidade, mas kernels/hardware podem introduzir diferenças. A presença de GPU altera custo e eventualmente determinismo.

## 12. Quais são as alternativas?

[train_lgbm](../train_lgbm/README.md) e [train_catboost](../train_catboost/README.md) são baselines naturais para dados tabulares. One-hot + modelo linear pode ser mais simples quando cardinalidade e volume permitem. Target/frequency encoding podem ser úteis se construídos sem leakage e avaliados corretamente.

A escolha deve vir da mesma validação, não da complexidade do algoritmo. Embedding é uma hipótese de representação, não uma melhora garantida.

## 13. Como saber se o resultado faz sentido?

Valide os dicionários de índices: mínimo, máximo, cardinalidade observada e categorias desconhecidas. Confira que nenhuma numérica possui NaN ou infinito. Garanta ambas as classes na validação antes de calcular AUC.

Compare com baseline sob a mesma população e repita em outra semente/janela quando estabilidade importar. Para investigar as embeddings, extraia os pesos de `model.embeddings[i].weight` e analise distâncias apenas como estrutura aprendida, não como causalidade.

## 14. Arquivos relacionados e próximos passos

A [implementação](mlp_embeddings.py) contém a classe e o treinador; a [fachada](__init__.py) exporta `SEED`, `EmbeddingMLP` e `train_embedding_mlp`; o [notebook](exemplo_mlp_embeddings.py) demonstra duas categóricas. O [guia da coleção](../../README.md) e o [Manual Técnico](../../../MANUAL_TECNICO.md#catalogo-helpers) mantêm as rotas.

Antes de produção, empacote também os mapeamentos categóricos e todo o pré-processamento — o modelo sozinho não basta.

## 15. Referências

Contrato local conferido na implementação, fachada e notebook da base `d9da056c95bf5c4209b2f208de1c9a987580efe7`. A documentação oficial de [`torch.nn.Embedding`](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding) descreve a camada como tabela de lookup de tamanho e dimensão fixos, indexada por inteiros.

A evidência de runtime desta R05 será registrada no relatório. Este README não afirma publicação no Databricks, superioridade sobre árvores nem auditoria independente.