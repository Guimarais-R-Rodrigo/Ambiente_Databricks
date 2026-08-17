# Sprint 8 — `hub_snippets/ml`, os 14 com dependência opcional

Data: 2026-08-17 · Executor: Claude · Escopo:
`ambiente_fonte/.assistant/hub_snippets/ml/`, os módulos que **não importam** no
runtime do laboratório sem instalação prévia. Com ela, a seção `ml` fica inteira
convertida: 30 objetos.

## O que mudou no desenho da sprint, antes de executá-la

O plano previa 14 notebooks que **documentam sem demonstrar** — bloco canônico de
"não executado" como formato padrão, porque as bibliotecas eram tidas como
ausentes e indisponíveis.

O levantamento feito antes da sprint desfez a premissa. `%pip install` funciona no
serverless, e as 12 bibliotecas envolvidas foram instaladas e **exercitadas com
chamada real**. Os 14 notebooks executam.

O inventário verificado, com a prova de cada uma, está em
`hub_snippets/requirements-optional.txt`. Três exigem pin — `shap==0.44.1`,
`umap-learn==0.5.5` e `pmdarima==2.0.4` (esta com `numpy==1.23.5` na mesma linha)
— e as outras nove resolvem sozinhas.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 12 aviso(s)
                        47 pastas de objeto
                        47 pares de contrato de saída · 47 de contrato de entrada
                        saída colada: 36 notebooks com bloco real, 12 sem
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
smoke test (job real)   116 verificações | 109 PASS | 0 FAIL | 7 opcionais ausentes
notebooks               14 de 14 SUCCESS
```

Os 12 avisos são a dívida herdada das Sprints 1, 4 e 6 — notebooks sem saída
colada. Nenhum é desta sprint.

Os 7 `OPTIONAL_MISSING` do smoke test **continuam corretos e devem continuar**:
ele importa os módulos sem instalar nada, que é o comportamento de quem só faz
`from hub_snippets.ml...` num notebook qualquer. A instalação é escolha de quem
usa o objeto, não estado da biblioteca.

## Duas armadilhas que só a execução encontrou

**O CatBoost escreve na pasta do notebook.** Sem
`params_override={"allow_writing_files": False}`, ele cria `catboost_info/` no
diretório de trabalho — que no Databricks é a pasta do próprio notebook, dentro
de `.assistant`. A primeira execução deixou **dez arquivos de log publicados no
workspace**, num notebook cuja tabela de ambiente declarava "Escrita: nenhuma".

Quem apanhou foi o `--verify` da publicação, listando-os como obsoletos no
remoto. É a mesma guarda criada para detectar sobra de renomeação, funcionando
para um caso que ninguém previu.

**`np.column_stack` promove tudo a float**, e o CatBoost então recusa
`cat_features` com uma mensagem que não sugere a correção: diz que o array é de
ponto flutuante, "o que significa nenhuma feature categórica". A coluna precisa
chegar como inteiro; um array de `dtype=object` preserva os dois tipos.

As duas estão documentadas no notebook de `train_catboost`, que é onde alguém vai
tropeçar nelas.

## Três notebooks escritos contra API imaginada — e o que o portão novo pegou

Escrevi os catorze a partir das assinaturas reais, lidas por AST antes de
escrever. O `check_contrato_de_entrada`, criado na auditoria da Sprint 7, aprovou
os catorze — e **nenhum dos três erros que apareceram na execução era do tipo que
ele cobre**:

| Notebook | O erro | Por que o portão não pega |
|---|---|---|
| `prophet_wrapper` | `modelo, previsao = ...` mas o retorno tem **três** elementos | é aridade de **retorno**; o portão confere a chamada |
| `arima_wrapper` | idem | idem |
| `shap_explainer` | `output_index` omitido; o módulo recusa escolher a classe por conta própria | é regra de **domínio** validada em runtime, não assinatura |

Comparado à Sprint 7 — seis erros em dezesseis, todos de assinatura — a conta
melhorou de 10/16 para 11/14 de acerto na primeira execução, e a classe de erro
mudou. O portão fez o trabalho dele; o que sobrou é o que ele declara não cobrir.

O `shap_explainer` merece nota: a recusa é **boa**. Um classificador binário de
árvore devolve SHAP para as duas classes, e explicar a classe 0 quando se queria
a 1 inverte todo o sinal sem levantar erro. O módulo prefere parar.

## O que os notebooks ensinam, além de como chamar a função

Três valem menção porque o resultado real contrariou o esperado:

**`autoencoder_anomaly` foi mal, e o notebook diz isso.** De 81 marcados, 19 eram
estranhos de verdade; 31 dos 50 plantados passaram. Precisão de 23%, cobertura de
38%. Ficou no notebook com a análise do porquê — anomalia de estrutura, não de
escala, com 25 épocas — e com o ponteiro para `isolation_forest`, que resolve
melhor o mesmo cenário. Notebook didático que só mostra o método brilhando ensina
a confiar nele.

**`prophet_wrapper` ajusta bem e decompõe mal.** MAPE de 1,02% e, na mesma
previsão, um componente `trend` **negativo** (−861) enquanto o `yhat` é 1.626. A
previsão fecha; a decomposição não descreve a série gerada. Registrei como achado
e **não** inventei explicação: com 36 pontos mensais e sazonalidade anual, há
muitas decomposições que ajustam igualmente bem. É o caso mais forte contra
apresentar componentes do Prophet como leitura de negócio.

**`arima_wrapper` escolheu (0, 1, 0)** — passeio aleatório com deriva, sem
estrutura a modelar. Está certo, foi assim que a série foi gerada, e é o
resultado que ninguém escolheria à mão. A previsão sai como uma reta, e a reta é
a resposta honesta.

## Limpeza remota

Como em toda sprint de conversão, `import-dir --overwrite` não apaga. Foram
removidos explicitamente 14 arquivos planos e a pasta `catboost_info/`, antes do
`--verify`, que fechou com 0 obsoletos.

## O que fica para depois

| Item | Por quê |
|---|---|
| Dívida de saída colada: 12 notebooks das Sprints 1, 4 e 6 | passe próprio; a guarda os lista a cada execução |
| Bateria funcional de `ml` no smoke test | fora do escopo do plano (§10) |
| `%pip install` nos notebooks × política do workspace do trabalho | decidido: a linha fica ativa. Se a política de lá exigir outra forma, é ajuste de replicação, não do fonte |
