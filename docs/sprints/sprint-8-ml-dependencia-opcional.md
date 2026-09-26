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

**O CatBoost escreve na pasta do notebook.** Por padrão ele cria `catboost_info/`
no diretório de trabalho — que no Databricks é a pasta do próprio notebook, dentro
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
tropeçar nelas. **A correção da primeira ficou inicialmente no lugar errado** —
ver a seção de auditoria no fim deste relatório.

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
escala, com 25 épocas. Notebook didático que só mostra o método brilhando ensina
a confiar nele.

A primeira versão desta seção mandava o leitor para `isolation_forest`, "que
resolve melhor o mesmo cenário". **Estava invertido**, e a auditoria mediu — ver
a seção no fim deste relatório.

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

---

## Auditoria da Sprint 8 — 13 achados, todos procedentes

Rodada em sessão sem contexto. O auditor executou os **14** notebooks em vez dos
5 pedidos — porque mediu o custo real e viu que cabia — e escreveu sondas
próprias para testar afirmações minhas em vez de aceitá-las.

O que ele confirmou intacto: **converter é mover cumprido nos 14** (byte a byte
idênticos), os 14 `__init__.py` batendo com a ferramenta, os pins corretos nos
três lugares certos e só neles, limpeza remota perfeita, e **os números colados
conferindo nos 14** — nenhum inventado, nenhuma saída vazia com prosa em volta.

### O achado que mais ensina: a correção ficou no lugar errado

O efeito colateral do CatBoost — `catboost_info/` publicado dentro de
`.assistant` — eu havia corrigido **no notebook**, passando
`params_override={"allow_writing_files": False}` na chamada.

O notebook parou de escrever, o `--verify` deu limpo, e a narrativa dizia que o
defeito estava resolvido. Não estava: `SKILL.md` recomenda
`hub_snippets.ml.train_catboost` por caminho de import, e o primeiro chamador que
não copiasse aquele parâmetro republicaria os dez arquivos. **Eu documentei o
incidente no passado e deixei a mina armada.**

A correção foi para o módulo (`params.setdefault("allow_writing_files", False)`),
e o notebook voltou à chamada simples — passando a narrar por que a correção mora
lá e não nele.

### Três afirmações minhas que a medição derrubou

Nenhuma era erro de número colado; todas eram prosa confiante sobre coisa não
verificada.

**A comparação com o Isolation Forest estava invertida.** O notebook do
autoencoder mandava o leitor para `isolation_forest`, dizendo que ele "acerta bem
mais". Medido sobre a mesma fixture — e reproduzi a medição antes de aceitar:

```text
                                   marcados  acertos  precisão  cobertura
autoencoder                              81       19     23,5%      38,0%
IsolationForest contamination=0.05       61        7     11,5%      14,0%
IsolationForest contamination=0.10      109       12     11,0%      24,0%
```

O Isolation Forest tem **metade** da precisão aqui. A impressão vinha do
`exemplo_isolation_forest`, cuja fixture é de anomalia grosseira de escala — onde
ele acerta 30 de 30. Dois notebooks, dois cenários, números que não se comparam.
Nenhum portão vê isso: é afirmação sobre um objeto que o notebook não executa.

**`max_samples` não limita o custo do TreeSHAP.** O parâmetro só age no ramo
`model_type="kernel"`, e o notebook chamava com `"tree"` enquanto o texto
ensinava que 800 linhas bastavam. O docstring do módulo estava certo o tempo
todo — foi a prosa que inverteu.

**NDCG@1 não é taxa de acerto.** Eu havia escrito que 0,9548 significa "em 95%
dos grupos o topo estava entre os mais relevantes". É razão de ganho: um ranker
que **nunca** acerta o topo tira 0,4286 nessa escala, e 0,9548 corresponde a
~92% de acerto. Levado a uma reunião, é número inflado que ninguém confere.

### Quatro notebooks explicavam um parâmetro que o módulo não tem

`kaplan_meier`, `optuna_lgbm`, `shap_explainer` e `umap_viz` traziam a seção
"Por que `log_mlflow=False` em tudo" e declaravam "Escrita: nenhuma;
`log_mlflow=False` em todas as chamadas". Nenhum dos quatro módulos importa
mlflow; nenhuma chamada passa o parâmetro. Foi bloco copiado dos dez treinadores
para quatro objetos que não treinam.

A tabela de ambiente é a primeira coisa que alguém lê antes de replicar no
trabalho, e ela justificava a linha mais importante com um fato falso.

### A guarda de saída colada era mais fraca do que anunciava

`check_saida_colada` aceitava bloco vazio e bloco sem conteúdo. Passou a exigir
substância — dígito ou trinta caracteres —, o que preserva o caso legítimo do
`safe_display`, que cola um `RuntimeError` sem um número sequer.

O auditor mostrou também que **seis dos catorze blocos são transcrições
editadas**, não literais: omitem linhas, reordenam, renomeiam colunas. Num deles
— `shap_explainer` — a curadoria removeu justamente as linhas que contradiziam a
prosa. Nenhuma guarda estática distingue bloco editado de bloco inventado. O que
dá para fazer está feito; o resto é disciplina, e fica dito no docstring.

### Os demais

| # | Achado | Correção |
|---|---|---|
| 4 | `AZUL_CAIXA` passa pelo `CORPORATE_RE` enquanto o `CLAUDE.md` chama a regra de inegociável | a decisão já existia em §2.2; passou a ser visível **onde a regra é enunciada** e no código da guarda. Sem renomeação — é decisão sua, de 16/08 |
| 7 | "os valores sobem de @1 para @10" seguido de série que desce | NDCG@k não é monotônico em k, e a não-monotonicidade virou o ponto |
| 8 | "Nenhum destes valores é o padrão do LightGBM" — três dos nove são | seis dos nove; os três mantidos no padrão estão nomeados |
| 10 | o mecanismo do pin do `shap` estava errado, e citava a mensagem do outro caso | mecanismo real (arrasta numpy 2.4.6 sobre o 1.23.5) e a mensagem observada |
| 11 | custo de instalação errado em 11 dos 14 | dois grupos: torch ~5 min, o resto ~1 min. Os 14 juntos são 25 min, não 1 hora |
| 12 | `yhat_lower`/`yhat_upper` do Prophet não são reprodutíveis | ressalva no bloco: o Prophet amostra os intervalos e o wrapper não fixa semente |
| 13 | a dívida dos 12 avisos vivia só na narrativa, e o comentário no código a atribuía só à Sprint 6 | §12.1 do plano, com os 12 caminhos e a sprint de origem de cada |

### Verificação depois das correções

```text
validate_assistant.py   APROVADO: 0 falha(s), 12 aviso(s)
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0
notebooks corrigidos    9 de 9 SUCCESS
```
