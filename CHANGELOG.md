# Changelog

Toda mudança relevante deste projeto é registrada aqui, em entradas curtas, sem
expor identificadores corporativos, PII ou segredos. Formato: seções por data,
subseções Adicionado/Atualizado/Corrigido/Removido, cada item com a IA autora
entre parênteses. Template: `.claude/templates/changelog-entry.md`.

## 2026-08-17 — auditoria da Sprint 10: 12 achados, e o defeito que se repetiu

O auditor seguiu o README ao pé da letra — publicou um notebook no Free com os
trechos copiados literalmente e rodou como job. Doze achados, todos procedentes.
Detalhe em `docs/sprints/sprint-10-readmes-de-topo.md`.

### Corrigido

1. (Claude) **As três saídas de comando coladas estavam erradas — pelo arquivo que
   a própria sprint apagou.** Capturei os números e só depois removi o
   `GLOSSARIO.md`; quatro contagens caíram em 1 e uma subiu em 2. Esta sprint
   existia para corrigir saídas desatualizadas e reproduziu o defeito um commit
   adiante. Recapturadas, e a ordem **editar → rodar → colar → commitar** ficou
   escrita no próprio README.
2. (Claude) A seção nova prometia saída real colada em todo notebook, com
   "sempre". Falta em **11 dos 58** — e o exemplo que eu escolhi para ilustrar,
   com "abra este primeiro", era `pit_join`, um dos onze. Trocado por
   `safe_display`, e os onze declarados com ponteiro para §12.1.
3. (Claude) Os "três casos conhecidos" de bloco não-executado erravam nos três:
   `pyspark.ml` não é bloco de não-executado (o notebook executa e cola o
   `Py4JError` real), sobrou uma dependência de pandas e não duas, e havia um
   quarto bloco no template ensinando uma limitação do Prophet que deixou de
   existir.
4. (Claude) `docs/testes/spark/README.md` ainda declarava `prophet_wrapper` não
   verificado — contra o `requirements-optional.txt`, a regra
   `free-vs-trabalho.md` e o próprio README da raiz — e usava caminhos
   `x_snippets/` de antes da Sprint 2.
5. (Claude) "Quatorze objetos de `ml/` instalam sozinhos": são **quinze**, com
   `display/dataframe_styled` estruturalmente idêntico.
6. (Claude) O "Mapa do repositório" omitia o `PLANO_HUB.md`; o
   `CATALOGO_HELPERS.md` não tinha `constants.emojis` nem `constants.styles`; e
   `checklist-replicacao.md` dizia 6 diretórios numa linha e 4 em outra.

### Atualizado

1. (Claude) `check_repo_links` ganhou a guarda de varredura vazia que só
   `check_repo_corporate` tinha. O README prometia que **ambas** reprovassem com
   zero; metade da rede não existia. Preferi consertar o código a enfraquecer a
   frase — provado com sonda que troca `REPO_ROOT` por diretório vazio.

### Notas

- **O que a auditoria confirmou é o que mais importava:** seguir o README
  funciona. Os caminhos existem na caixa exata, os três imports rodam no
  workspace, as saídas de confirmação batem caractere por caractere, e o "engano
  mais comum" documentado reproduz a mensagem prometida.
- O glossário migrou limpo: 65 termos antes, 65 depois, hierarquia correta, onze
  âncoras resolvendo — inclusive as acentuadas.
- **Nenhum portão veria nenhum dos doze.** Eles conferem estrutura, sintaxe, link
  e tipo de objeto; nenhum lê uma frase e pergunta se é verdade. A ironia do
  achado 1 é que o validador imprimia a resposta certa na tela enquanto o README
  exibia a errada. A guarda que fecharia o caso — extrair os blocos de saída,
  reexecutar e falhar na divergência — fica registrada como candidata da
  Sprint 12.

## 2026-08-17 — Sprint 10: os dois READMEs de topo, e o glossário absorvido

`README.md` da raiz e `.assistant/README.md` atualizados na variante longa.
Relatório em `docs/sprints/sprint-10-readmes-de-topo.md`.

### Atualizado

1. (Claude) As três saídas de comando coladas no README da raiz estavam da
   Sprint 2 e erravam por larga margem — 70 arquivos Python contra 193, 176
   arquivos renderizados contra 298, 409 varridos contra 674. Recolhidas de
   execução real, e o bloco do validador passou a mostrar as **quatro guardas
   criadas depois**, com o defeito real de que cada uma nasceu.
2. (Claude) `.assistant/README.md` ganhou tabela de navegação no topo — dez
   perguntas, dez âncoras — e seção nova sobre o notebook por objeto.

### Corrigido

1. (Claude) O quadro de status do README da raiz afirmava que `prophet_wrapper`
   "segue sem combinação funcional". A Sprint 8 mostrou que instala e ajusta um
   modelo completo.

### Removido

1. (Claude) `.assistant/GLOSSARIO.md`, absorvido como seção do
   `.assistant/README.md` conforme §5 do plano. Os cinco links foram reapontados
   para a âncora, e a validação pegou os que eu havia reapontado errado. O
   `--verify` da publicação pegou o que faltava: o arquivo continuava no
   workspace depois de removido da fonte.

### Notas

- **A seção nova sobre os notebooks era o buraco maior.** Nenhum dos dois READMEs
  mencionava que os 58 objetos têm, cada um, um `exemplo_*` na própria pasta —
  que é o que esta fase inteira produziu, e o que um recém-chegado precisa saber
  antes de qualquer outra coisa.
- Contrapartida registrada: o `.assistant/README.md` foi a 494 linhas. Glossário
  é documento de consulta por termo e README é leitura linear; a mesa de
  navegação no topo é o que evita que a fusão piore os dois.

## 2026-08-17 — auditoria da Sprint 9: 13 achados, e o HTML que ninguém lia

Rodada em sessão sem contexto. O auditor **imprimiu e leu o HTML que as funções
devolvem** em vez de aceitar a prosa — foi de onde saíram os quatro achados mais
graves, todos aprovados pelos dois portões. Detalhe em
`docs/sprints/sprint-9-constants-visual-display.md`.

### Corrigido

1. (Claude) `exemplo_dataframe_styled` fazia **três** afirmações erradas sobre a
   função: que ela destaca as colunas pedidas, que há gradiente, e que o realce é
   por coluna. O HTML devolvido tinha zero células destacadas — a regra é realçar
   valor **negativo** dentro das colunas declaradas, e a fixture não tinha
   negativo. Corrigido com coluna de negativos, e o `format_dict` com `"{:,.0f}"`
   (separador americano) trocado por `fmt_int`.
2. (Claude) `exemplo_section_header` dizia que o estilo vem de
   `constants.styles`. O CSS está inline no módulo, e `STYLE_SECTION_HEADER` não
   é usado por ninguém — editá-lo não muda cabeçalho nenhum.
3. (Claude) `exemplo_badge` usava o par 62/68 para explicar a política de corte.
   Os cortes reais são 80 e 50; `badge_score(68)` sai amarelo.
4. (Claude) O bloco de saída do `theme_plotly` mostrava dez cores; a execução
   imprime oito, porque o `print` corta em 88 caracteres. A afirmação era
   verdadeira e a evidência ao lado dela, fabricada. Célula nova imprime
   `len(colorway)` e a lista inteira.
5. (Claude) A docstring de `format_br` errava `fmt_delta(..., "bps")` por um
   fator de dez — dentro do módulo cujo notebook auditava essa exata armadilha.
6. (Claude) `exemplo_correlation_matrix` dizia "é `toPandas()` por baixo"; o
   módulo não chama `toPandas()`. O cálculo é distribuído e o custo cresce com
   colunas, não com linhas — amostrar ali perde precisão de graça.
7. (Claude) `display_styled` usava `Styler.applymap`, removido no pandas 3.0.
   Passou a `getattr(styled, "map", ...)` com fallback, sem mudar comportamento
   no 1.5.3 do Free.
8. (Claude) Seis dos treze blocos de saída eram transcrição editada. Refeitos
   literais; onde a saída é longa, o corte está declarado.

### Adicionado

1. (Claude) `PLANO_HUB.md` §12.2: inventário único da cor redeclarada fora de
   `constants.colors`. Eu havia registrado **2 de 12** módulos e chamado de
   contraexemplo positivo um que também copia. A tabela separa **cópia idêntica**
   (onze — unificar é higiene, sem efeito visual) de **valor divergente** (um,
   `ml/curves_plotly`, que é a única decisão de produto).
2. (Claude) Coluna `Dep.` na tabela de exploração do `CATALOGO_HELPERS.md`, com
   `dataframe_styled` e `explainability_report` marcados `exec`. O catálogo é o
   índice que as skills mandam consultar, e não marcava nenhuma das duas
   dependências escondidas.
3. (Claude) Contraste medido em `exemplo_colors`: **duas das quatro cores
   semânticas reprovam o mínimo AA com texto branco** — `COR_ALERTA` em 1,73:1 e
   `COR_POSITIVO` em 2,04:1. A regra ficou registrada: as duas são cor de
   preenchimento, nunca fundo para texto branco.

### Notas

- **A biblioteca tem 58 objetos** (51 `hub_snippets` + 7 `hub_scripts`). O "60"
  do validador soma os 2 exemplares de `hub_padroes`, que são template.
- `constants/styles` **não é importado por ninguém**, e suas oito constantes são
  cópia byte a byte de CSS que vive inline em cinco outros módulos. O arquivo
  inteiro é um espelho morto.
- **Ponto cego declarado:** nada do que é pixel foi verificado. O candidato mais
  provável a defeito escondido é a colisão entre o rodapé e a legenda do
  `theme_plotly` — anotação em `y=-0.18`, legenda em `y=-0.25`. Precisa de olho
  humano no notebook aberto.

## 2026-08-17 — Sprint 9: a biblioteca inteira convertida

Os 13 objetos de `constants`, `visual` e `display` viraram pasta de objeto, com
notebook que mostra o valor e o efeito renderizado. Com eles, **os 60 objetos da
biblioteca estão convertidos**. Relatório em
`docs/sprints/sprint-9-constants-visual-display.md`.

### Adicionado

1. (Claude) 13 pastas de objeto, com `__init__.py` gerado por
   `tools/api_publica.py` e notebook `exemplo_*`. Os 13 executaram como job:
   13 de 13 SUCCESS.

### Corrigido

1. (Claude) `exemplo_dataframe_styled` passou a instalar `jinja2`. **Segundo caso
   de dependência escondida** da biblioteca: o módulo não a importa, ela entra
   por `DataFrame.style`, que o pandas delega na hora da chamada. O primeiro foi
   o `tabulate`, por `to_markdown()`. Dois casos deixam de ser coincidência, e o
   padrão está registrado em `requirements-optional.txt`.
2. (Claude) `exemplo_correlation_matrix` foi para o bloco canônico: o módulo usa
   a API clássica de `pyspark.ml` (`VectorAssembler`, `Correlation.corr`), que o
   Spark Connect não expõe. Importa normalmente; falha ao instanciar.

### Notas

- **Três definições de "verde de selo" na mesma biblioteca**, expostas pela
  conversão: `constants.colors` (`VERDE = #8DC63F`), `constants.styles`
  (`STYLE_BADGE_OK`, hex copiado) e `visual.badge` (`#2E7D32`, cor diferente das
  outras duas). E `constants.styles` não tem uma linha de `import` — repete
  `#005CA9` e `#F8F9FA` em vez de puxar de `colors`, de modo que uma mudança de
  identidade visual não alcançaria os cabeçalhos. `visual.theme_plotly` é o
  contraexemplo positivo: importa `PALETA_CATEGORICA` de verdade. Cada caso
  registrado no notebook do objeto; unificar é etapa 2.
- `constants.format_br`: `fmt_delta` espera **razão**, não pontos percentuais,
  apesar da unidade "pp". Passar `2.4` pensando em "2,4 pp" devolve `+240,0 pp`.
  Encontrado ao escrever o próprio exemplo, que na primeira versão passava 2.4.
- Terceira variação do mesmo tema nesta fase — **importável não é executável** —,
  agora com três causas distintas: biblioteca ausente (`tabulate`), dependência
  delegada (`jinja2`) e API da plataforma (`pyspark.ml` no Spark Connect).

## 2026-08-17 — auditoria da Sprint 8: 13 achados, e uma correção que estava no lugar errado

Rodada em sessão sem contexto. O auditor executou os 14 notebooks em vez dos 5
pedidos e escreveu sondas próprias para testar as afirmações em vez de aceitá-las.
Treze achados, todos procedentes. Detalhe em
`docs/sprints/sprint-8-ml-dependencia-opcional.md`.

### Corrigido

1. (Claude) `ml/train_catboost` passou a definir `allow_writing_files=False` **no
   módulo**. A correção do efeito colateral estava no notebook, via
   `params_override` — o notebook parou de escrever, o `--verify` deu limpo, e a
   biblioteca continuou com a mina armada para qualquer outro chamador. As skills
   recomendam o módulo por caminho de import.
2. (Claude) `exemplo_autoencoder_anomaly` mandava o leitor para
   `isolation_forest`, "que acerta bem mais". Medido sobre a mesma fixture, o
   Isolation Forest tem **metade** da precisão (11,5% contra 23,5%) e metade da
   cobertura. A impressão vinha do notebook do outro objeto, cuja fixture é de
   anomalia grosseira de escala. A comparação foi substituída pelos números
   medidos, com a explicação de por que os dois cenários não se comparam.
3. (Claude) `exemplo_shap_explainer` ensinava que `max_samples=800` limitava o
   custo. O parâmetro só age em `model_type="kernel"`; o notebook chama com
   `"tree"`, e o TreeSHAP roda sobre a base inteira. O docstring do módulo estava
   certo — a prosa do notebook é que invertia.
4. (Claude) `exemplo_lgbm_ranker` lia NDCG@1 como taxa de acerto do topo. É razão
   de ganho: um ranker que nunca acerta o topo tira 0,4286 nessa escala, e o
   0,9548 obtido corresponde a ~92% de acerto, não 95%.
5. (Claude) Quatro notebooks — `kaplan_meier`, `optuna_lgbm`, `shap_explainer` e
   `umap_viz` — traziam uma seção inteira sobre `log_mlflow=False` e declaravam
   "Escrita: nenhuma" com base nele. Nenhum dos quatro módulos importa mlflow.
   Bloco copiado dos dez treinadores para quatro objetos que não treinam.
6. (Claude) `exemplo_train_lgbm` afirmava que nenhum dos nove parâmetros era o
   padrão do LightGBM; três são. `exemplo_lgbm_ranker` dizia que os NDCG "sobem
   de @1 para @10" citando uma série que desce na primeira transição — a
   não-monotonicidade virou o ponto.
7. (Claude) `requirements-optional.txt`: o mecanismo do pin do `shap` estava
   errado e citava a mensagem de erro do outro caso. O real é que ele arrasta
   numpy 2.4.6 sobre o 1.23.5 do runtime. E o custo de instalação, declarado como
   "~3 min" nos 14, erra por 4 a 6× em 11 deles — são dois grupos, torch (~5 min)
   e o resto (~1 min).

### Atualizado

1. (Claude) `check_saida_colada` passou a exigir substância no bloco — dígito ou
   trinta caracteres. Aceitava bloco vazio. O limite preserva o caso legítimo do
   `safe_display`, que cola um `RuntimeError` sem um número sequer.
2. (Claude) A exceção do `AZUL_CAIXA` passou a ser visível onde a regra é
   enunciada (`CLAUDE.md`) e no código da guarda, apontando para `PLANO_HUB` §2.2.
   Sem renomeação: é decisão registrada em 16/08.
3. (Claude) `PLANO_HUB.md` §12.1, nova: a dívida dos 12 notebooks sem saída
   colada, com caminho e sprint de origem de cada. Vivia só na narrativa, e o
   comentário no código a atribuía inteira à Sprint 6 — são 1, 4 e 6.

### Notas

- **Seis dos catorze blocos de saída são transcrições editadas**, não literais:
  omitem linhas, reordenam, renomeiam colunas. Num deles a curadoria removeu
  justamente as linhas que contradiziam a prosa. Nenhuma guarda estática
  distingue bloco editado de bloco inventado; o limite está dito no docstring.
- O auditor confirmou intacto o que mais custaria: converter é mover cumprido nos
  14, `__init__.py` gerados, pins corretos, limpeza remota, e **os números
  colados conferindo nos 14** — nenhum inventado.

## 2026-08-17 — Sprint 8: `ml` inteira convertida, e os 14 demonstram

Os 14 módulos com dependência opcional viraram pasta de objeto, com notebook
próprio que **instala a biblioteca e executa**. Com isso a seção `ml` fica
completa: 30 objetos. Relatório em
`docs/sprints/sprint-8-ml-dependencia-opcional.md`.

### Adicionado

1. (Claude) 14 pastas de objeto em `hub_snippets/ml/`, com `__init__.py` gerado
   por `tools/api_publica.py` e notebook `exemplo_*` com `%pip install` na
   primeira célula. Os 14 executaram como job: 14 de 14 SUCCESS.

### Corrigido

1. (Claude) `exemplo_train_catboost` passou a exigir
   `params_override={"allow_writing_files": False}`. Sem isso o CatBoost cria
   `catboost_info/` no diretório de trabalho — que no Databricks é a **pasta do
   notebook** —, e a primeira execução deixou dez arquivos de log publicados
   dentro de `.assistant`. Quem apanhou foi o `--verify` da publicação.

### Notas

- **O portão novo funcionou, e os erros mudaram de classe.** O
  `check_contrato_de_entrada`, criado na auditoria da Sprint 7, aprovou os 14, e
  nenhum dos três erros que apareceram na execução era de assinatura: dois eram
  de **aridade de retorno** (`prophet_wrapper` e `arima_wrapper` devolvem três
  elementos, não dois) e um era regra de domínio validada em runtime
  (`shap_explainer` recusa escolher a classe a explicar). Acerto de primeira
  execução subiu de 10/16 na Sprint 7 para 11/14 aqui.
- Três notebooks registram resultado que contraria o esperado, e ficam assim:
  `autoencoder_anomaly` acerta 19 de 81 marcados e o notebook diz que foi mal;
  `prophet_wrapper` ajusta com MAPE de 1,02% e devolve um componente `trend`
  negativo que não descreve a série — registrado como achado, sem explicação
  inventada; `arima_wrapper` escolhe (0,1,0), que é a resposta honesta.
- Os 7 `OPTIONAL_MISSING` do smoke test continuam e devem continuar: ele importa
  sem instalar, que é o comportamento de quem só faz `from hub_snippets.ml...`.

## 2026-08-17 — as 14 dependências opcionais instalam e rodam no Free

Levantamento feito antes da Sprint 8, para saber quantos dos 14 módulos com
dependência opcional conseguiriam demonstrar de verdade. A resposta mudou o
desenho da sprint: **todos**.

### Atualizado

1. (Claude) `hub_snippets/requirements-optional.txt` reescrito com o inventário
   verificado em 2026-08-17. As 12 bibliotecas foram instaladas por `%pip` e
   **exercitadas com chamada real** — ajuste de modelo, projeção, previsão —,
   não apenas importadas. Custo: 200 a 280 segundos de job.
2. (Claude) `.claude/rules/free-vs-trabalho.md`: a linha "bibliotecas ML
   opcionais ausentes" passou a "ausentes do runtime, mas instaláveis na sessão",
   com as três regras que custaram um ambiente quebrado.
3. (Claude) `PLANO_HUB.md`: a Sprint 8 deixa de produzir 14 notebooks que só
   documentam.

### Corrigido

1. (Claude) `prophet` estava registrado como **"sem combinação funcional
   conhecida"** — falhava com `'Prophet' object has no attribute 'stan_backend'`
   — e o plano o listava como fora de escopo, a documentar sem resolver. Em
   17/08 instalou sem pin e ajustou um modelo completo, com previsão de 7 dias.
   O impedimento não existe mais.
2. (Claude) O arquivo mandava fixar `numpy==1.26.4` sempre, por precaução. O
   runtime traz **1.23.5**, e o pin gera conflito em vez de evitar. Também não se
   reproduziu o aviso de que `%pip` antes do primeiro comando Spark abortaria a
   execução.

### Notas

- **Três bibliotecas exigem pin**: `shap==0.44.1` (sem ele, sobe versão que
  espera numpy 2.x e quebra no import), `umap-learn==0.5.5` e `pmdarima==2.0.4`
  (esta com `numpy==1.23.5` na mesma linha). As outras nove resolvem sozinhas.
- **Instale uma por notebook.** As três acima, juntas na mesma sessão, derrubam o
  `import numpy` do próprio notebook: `numpy.dtype size changed, Expected 96 from
  C header, got 88`. Isoladas, funcionam.
- Segunda vez no mesmo dia em que um registro de teste de 14/08 se mostrou
  desatualizado — uma vez para pior (MLflow deixou de abrir run), uma para melhor
  (Prophet passou a funcionar). Reforça a linha da regra: **"foi testado" tem
  data de validade em ambiente gerenciado.**

## 2026-08-17 — auditoria da Sprint 7: 12 achados e duas guardas novas

Rodada em sessão sem contexto, com instrução para executar e com `git show`
liberado para recuperar a versão anterior de cada módulo. Doze achados, todos
procedentes. Relatório completo em `docs/sprints/sprint-7-ml-nucleo.md`.

### Adicionado

1. (Claude) `check_contrato_de_entrada` em `tools/validate_assistant.py`: confere
   por AST o que o notebook **passa** contra a assinatura do módulo — kwarg
   inexistente, posicional a mais, obrigatório omitido. Era a direção sem portão
   nenhum, e por onde entraram seis dos dezesseis defeitos da sprint. Provado com
   os três defeitos reais reinjetados num sandbox; 0 achados no repositório.
2. (Claude) `check_saida_colada` (**aviso**): cobra do notebook um bloco
   ```text com a saída real. Só 6 de 24 tinham; hoje são 22 de 34.
3. (Claude) Seção 4 em `exemplo_drift_detection`, com a política de limiar
   declarada, e o caso de fronteira registrado — `uf` sai 0,250667 contra um
   limiar de 0,25 e dispara alarme por seis milésimos.

### Corrigido

1. (Claude) `exemplo_lgbm_temporal` ensinava a contar nulos por entidade como
   assinatura de lag correto. A função termina com `dropna()` e devolve zero
   nulos sempre; e a chamada do notebook, com a janela móvel no padrão
   `[3,6,12]` sobre 12 meses, devolvia **zero linhas**. O job reportava SUCCESS.
   A demonstração foi refeita sobre contagem de linhas removidas — 9 com
   `entity_cols`, 3 sem — e mostra o lag de B recebendo 898,2, valor de C.
2. (Claude) `exemplo_metrics_report` mandava comparar `accuracy`, que
   `calculate_binary_metrics` não devolve. Leitura reescrita em torno de
   `prevalence`.
3. (Claude) `exemplo_mlflow_run` usava o bloco canônico com motivo que o template
   proíbe ("decisão de escopo, não impedimento técnico"). Ao executar, apareceu
   impedimento real — ver Notas.
4. (Claude) `exemplo_split_temporal`: 60 das 720 linhas somiam sem menção;
   `gap_periods` explicado. `exemplo_score_bands`: pede 5 bandas e recebe 4, por
   colapso de quantis com 26,8% da base empatada no piso. `exemplo_curves_plotly`:
   prevalência 0,0185, não 0,02.
5. (Claude) Título e tabela órfãos em `exemplo_woe_iv_calculator` e
   `exemplo_split_temporal`, resíduo do desmembramento dos notebooks de trânsito.
6. (Claude) `scikit-learn` registrado em `requirements-optional.txt`: entra por
   `mlflow.sklearn`, que `import mlflow` não traz.

### Notas

- **Diferença Free × trabalho nova, e uma lição de método.** Nenhum run do MLflow
  abre no serverless do Free: `mlflow.start_run` instancia um `MlflowClient` que
  lê `spark.mlflow.modelRegistryUri`, e o Spark Connect recusa a config. O mesmo
  caminho foi testado e **passou em 14/08/2026** — `docs/testes/spark/resultados/`
  registra `mlflow_run.completo` como "run completo aceito". Três dias, mesmo tipo
  de compute, resultado oposto. O registro de 14/08 não está errado; o runtime
  mudou. Linha nova na matriz de `.claude/rules/free-vs-trabalho.md`, com a
  conclusão: **"foi testado" tem data de validade em ambiente gerenciado.**
- Dívida declarada: 12 notebooks das Sprints 1, 4 e 6 seguem sem saída colada.
  A guarda os lista a cada execução.

## 2026-08-17 — reestruturação para Hub: Sprints 0 a 7

Execução do `PLANO_HUB.md`, iniciada em 16/08. Esta entrada cobre as oito sprints
concluídas até aqui em bloco, e não uma por uma: o registro detalhado de cada uma
está em `docs/sprints/`, e o estado de cada sprint, com data e auditoria, em
`PLANO_HUB.md` §12. **Foi um lapso de processo não registrar sprint a sprint** —
o CHANGELOG ficou dois dias atrás da execução, contrariando a regra do projeto.

### Adicionado

1. (Claude) `.assistant/hub_padroes/` — seis tipos de template (readme, snippet,
   script, prompt, skill, notebook) com exemplo executável em
   `taxa_resposta_campanha/`. Sprint 1.
2. (Claude) `tools/api_publica.py`: extrai a API pública por AST e gera o
   `__init__.py` da pasta de objeto. A regra é exaustiva, não curada.
3. (Claude) `tools/notebook_marker.py`: detecção canônica de notebook, tolerando
   BOM, linha em branco e comentário de encoding, usada pela publicação e pelo
   smoke test.
4. (Claude) `check_pastas_de_objeto` e `check_contrato_de_dados` em
   `tools/validate_assistant.py`. O segundo compara o que o módulo **produz** com
   o que o notebook **consome**; nasceu de um caso real em que o notebook filtrava
   `status != 'ok'` sobre uma coluna que devolve emoji.
5. (Claude) `docs/decisions/ADR-0006-identidade-hub.md`, com a tabela de
   correspondência `x_*`/`rodrigo-*` → nomes atuais, referenciada pelos dez
   documentos datados que preservam a nomenclatura da época.
6. (Claude) 31 notebooks `exemplo_<objeto>.py`, todos executados como job no
   laboratório: 7 em `hub_scripts` (Sprint 4), 8 em `spark`/`testing` (Sprint 6),
   16 em `ml` (Sprint 7).

### Atualizado

1. (Claude) Prefixo `x_` → `hub_`, e as 12 skills `rodrigo-<tema>` →
   `hub-ml-<tema>`. Regra de nomenclatura: underscore onde o Python importa,
   hífen onde a plataforma nomeia. Sprints 2 e 3.
2. (Claude) `hub_snippets` e `hub_scripts` passaram de arquivo plano a **pasta por
   objeto** (`__init__.py` + módulo + notebook). 31 dos 58 objetos convertidos.
3. (Claude) `tools/publicar_free.py`: detecção de diretório obsoleto,
   `--verify` rápido, e `.assistant/.mcp_servers.json` tratado como arquivo
   gerido pela plataforma.
4. (Claude) `tools/spark_smoke_test.py`: pula notebook no `walk_packages` —
   objetos NOTEBOOK aparecem como `.py` no mount `/Workspace`, o que foi
   verificado com job de sonda — e descobre `hub_scripts` automaticamente.

### Corrigido

1. (Claude) Três notebooks didáticos estavam quebrados desde 14/08: a auditoria da
   biblioteca renomeou chaves de retorno (`cobertura_pct` →
   `cobertura_pct_linhas_validas`, entre outras) e o material didático não
   acompanhou. Encontrado ao executar, não ao ler.
2. (Claude) `hub_scripts/naming_checker` usava `spark` sem importar pyspark — o
   mesmo `NameError` que a documentação declarava eliminado.
3. (Claude) 38 links relativos quebrados pela renomeação, por substituição que
   descartava a profundidade do caminho; refeitos com `os.path.relpath`.

### Removido

1. (Claude) `x_projects/`, `x_docs/` e `x_config/`, com o conteúdo aproveitável
   realocado. Sprint 2.
2. (Claude) `hub_snippets/_notebooks_a_migrar/`, pasta de trânsito criada na
   Sprint 2 para que a renomeação não apagasse o insumo das Sprints 6 e 7. O
   último dos quatro notebooks originais foi desmembrado nesta sprint.

### Notas

- **Dependência escondida.** `ml/explainability_report` está classificado como
  núcleo — não tem `import` de biblioteca opcional e o smoke test o importa com
  `PASS` —, mas não executa no laboratório: usa `DataFrame.to_markdown()`, que o
  pandas delega ao `tabulate`, ausente no runtime. Registrado em
  `hub_snippets/requirements-optional.txt`. A divisão 16/14 entre as Sprints 7 e 8
  é exata sobre importabilidade, não sobre executabilidade.
- Auditorias em sessão sem contexto ao fim das Sprints 1, 2, 4 e 3+6: 21, 13, 9 e
  13 achados, todos procedentes e corrigidos. A da Sprint 7 está pendente.
- `PALETA_CATEGORICA` tem 6 cores em `ml.curves_plotly` e 10 em
  `constants.colors`; duas das três cópias são idênticas à original, o que esconde
  a divergente. Registrado no notebook do objeto; unificar é decisão de produto.

## 2026-08-15 — segunda auditoria da documentação e 25 correções

Rodada independente sobre os **15 READMEs** do repositório, sete deles auditados
pela primeira vez. Ao contrário da rodada anterior, esta pediu que o auditor
**executasse** os procedimentos documentados em vez de apenas lê-los, e que
comparasse cada README com o conteúdo real da pasta que ele descreve. Os dois
achados mais caros vieram exatamente daí. Registro em
`docs/auditoria/2026-08-15_documentacao-rodada2/`.

### Corrigido — proteções que não cobriam o que prometiam

1. (Claude) `check_repo_corporate` varria a partir de `Path(".")`, não da raiz do
   repositório. Rodado de `tools/`, varria 4 arquivos em vez de 409 e devolvia
   `APROVADO: 0 falha(s), 0 aviso(s)` — a proteção do ADR-0003 desligava em
   silêncio conforme o diretório de onde o comando fosse chamado. A raiz passou a
   vir de `Path(__file__).resolve().parents[1]`, e **varredura vazia agora
   reprova**. O padrão foi ampliado de três alternativas para matrícula genérica
   (letra + 6 a 8 dígitos), domínio corporativo e domínio bancário, verificado
   sem falso positivo no repositório atual. O `README.md` deixou de prometer
   cobertura genérica e passou a apontar `CORPORATE_RE` como dona da lista.
2. (Claude) A validação só checava links relativos dentro de `--root`
   (`ambiente_fonte` por padrão), enquanto o `README.md` a apresentava como rede
   que "reprova link quebrado". `README.md`, `docs/` e `.claude/` — 156 links —
   nunca foram verificados. Novo `check_repo_links` cobre o repositório fora da
   raiz analisada; nenhum link quebrado encontrado. O texto passou a dizer que
   não há hook nem CI: a rede só existe quando alguém a aciona.
3. (Claude) `publicar_free.py --verify` filtrava `object_type != "DIRECTORY"`, e
   por isso não enxergava diretório órfão. Havia um caso vivo: `x_projects/archive`,
   vazio, não versionado e publicado no workspace. A conferência passou a comparar
   também os diretórios; `archive/` foi removido da fonte e do workspace.

### Corrigido — procedimento documentado que não executa

1. (Claude) O passo 4 da "Primeira hora" mandava rodar quatro comandos "logo
   abaixo", e o bloco do render aparecia **sem `--write`**. Quem copiasse os
   blocos na ordem publicaria o espelho anterior e receberia `APROVADO` na
   conferência, que compara workspace contra espelho e nunca contra a fonte. Os
   quatro comandos passaram para dentro do passo 4, com `--write` e a explicação
   do porquê a conferência não acusaria o erro.
2. (Claude) `README.md` mandava instalar a CLI com `pip install databricks-cli`,
   que é a CLI legada — parada na 0.18, desaconselhada pela própria Databricks,
   sem `auth login` nem `current-user`, e capaz de sombrear o binário correto no
   PATH em Windows. Substituído por `winget` e pelo instalador oficial, com
   `databricks --version` ≥ 0.200 como pré-requisito conferível.
3. (Claude) O comando de reexecução do smoke test estava marcado como PowerShell
   mas passava JSON entre aspas simples: o shell remove as aspas duplas antes de
   o executável recebê-las. Trocado por here-string.

### Corrigido — código

1. (Claude) `x_scripts/naming_checker.py` referenciava o global de notebook
   `spark` sem importar `pyspark` — o mesmo `NameError` que `docs/testes/spark/`
   declarava eliminado em todos os scripts. Ele nunca esteve no smoke test, então
   nunca foi importado no runtime, e a validação estática não pega porque o
   arquivo é sintaticamente válido. Corrigido; varredura por AST confirmou que
   nenhum outro módulo de `x_snippets` ou `x_scripts` usa o global.

### Corrigido — contradições entre documentos

1. (Claude) `CLAUDE.md` listava o ADR-0002 (engine do Hub) como decisão **ativa**,
   revogada pelo ADR-0005 desde então, e omitia os ADRs 0004 e 0005.
2. (Claude) `.claude/CLAUDE.md` mandava "não invente que já existem" sobre
   `publicar-free`, `forward-test-skills` e `replicar-trabalho` — as três no
   disco, com frontmatter válido e listadas como ativas em `skills/README.md`.
   Como é o primeiro arquivo que toda IA lê, a instrução fazia uma IA nova
   recusar-se a usar ferramenta existente ou reconstruí-la.
3. (Claude) `docs/testes/spark/README.md` afirmava que `requirements-optional.txt`
   traz o conjunto que funciona e, 45 linhas depois, que ele "lista nomes sem
   versão" e não é instalável — resíduo de antes de o arquivo ser pinado.
4. (Claude) `ROADMAP_SKILLS.md` mantinha em aberto dois gates fechados (Spark
   64/71 e forward tests 36/36), e `x_docs/README.md` mandava o leitor lá
   justamente para saber "gates pendentes". Marcados, com o status apontando para
   o README da raiz em vez de duplicá-lo.

### Corrigido — índices que negavam o próprio conteúdo

1. (Claude) `docs/auditoria/README.md` dizia "nenhuma auditoria formal registrada
   ainda" com duas pastas de auditoria ao lado. Tabela preenchida com as três.
2. (Claude) `docs/handoffs/README.md` declarava-se vazio enquanto guardava, dentro
   de um bloco rotulado "exemplo", os dois únicos itens de vigilância abertos do
   projeto — incluindo um que não existe em nenhum outro lugar do repositório.
   Promovido a `2026-08-14_calibracao-descriptions.md` e registrado na tabela; o
   README ficou com esqueleto genérico.
3. (Claude) O mapa do repositório no `README.md` omitia `docs/testes/`, que guarda
   a evidência dos dois gates da fase 3.

### Corrigido — fatos e mecanismos

1. (Claude) `README.md` declarava as dependências opcionais pendentes de fixação
   ("7 módulos ML") quando 13 dos 14 já haviam executado com as versões pinadas;
   só `prophet_wrapper` segue sem combinação funcional.
2. (Claude) `README.md` agrupava `x_projects/` sob "adicionar com `@`/Add context",
   que é falso e é exatamente o engano que `x_projects/README.md` existe para
   desfazer: arquivo que fique nessa pasta nunca é descoberto — é preciso copiar
   o template como `AGENTS.md` na raiz do projeto real.
3. (Claude) `x_scripts/README.md` documentava o contrato anterior à correção
   ("`spark` deve existir no ambiente"), ensinando a aceitar como normal o defeito
   que o projeto eliminou.
4. (Claude) A árvore de `x_projects/README.md` listava 3 das 5 entradas da pasta,
   e o exemplo de `quick_profile` chamava com `sample_fraction=0.05` sobre uma
   saída capturada com fração 1.0.
5. (Claude) O gate do forward test declarava 36/36 sem a ressalva que o próprio
   resultado registra: `11N-r2` passou em sentido fraco.

### Adicionado

1. (Claude) Bifurcação de leitores no `README.md`: usar, contribuir ou assumir o
   projeto. O percurso inteiro era escrito para quem contribui, e o analista que
   só vai usar o ambiente publicado não tinha caminho — o passo 4 o convidava a
   escrever no workspace na primeira hora.
2. (Claude) Diagrama dos três gates (validação estática, Spark, forward test) com
   o que cada um prova e **não** prova, e a fronteira que nenhum deles alcança.
3. (Claude) Sete verbetes no glossário, todos usados sem definição em documentos
   que remetem o leitor a ele: *event log*, *target (de bundle)*, *autologging*,
   *PII*, *LambdaRank/NDCG*, *auditoria do Codex* e `run_governado`. O primeiro
   aparecia em 3 documentos; o penúltimo, em 7.
4. (Claude) Separação entre automático e manual no checklist de pré-publicação de
   `.assistant/README.md`: oito itens viram um comando, e sobram os três que
   exigem uma pessoa.

### Atualizado

1. (Claude) Ordem de `docs/testes/spark/README.md`: a legenda dos três estados
   (`PASS`/`OPTIONAL_MISSING`/`FAIL`) subiu para junto da tabela que os usa, 80
   linhas acima de onde estava.
2. (Claude) A explicação de por que existem duas pastas deixou de ser duplicada
   no `README.md`; `ambiente_fonte/README.md` passou a ser a dona.
3. (Claude) Gênero de "Genie Code" padronizado no masculino em 16 arquivos — a
   forma feminina aparecia em 6 dos 15 READMEs.

### Descoberto durante a correção

1. (Claude) **A plataforma escreve dentro de `.assistant/`.** Abrir o painel de
   MCP em Genie Code → Settings materializa
   `/Users/<username>/.assistant/.mcp_servers.json` com a lista de conectores
   internos (observado em 2026-08-15). Sem tratamento, o `--verify` recém-corrigido
   classificaria um arquivo gerenciado pela plataforma como obsoleto e mandaria
   apagá-lo. Passou a ser reconhecido e reportado à parte. Registrado em
   `.claude/rules/genie-code-oficial.md` com a inversão que importa: o arquivo é
   **saída** da configuração, nunca entrada — criá-lo à mão não configura nada, o
   que preserva a afirmação original da regra.

## 2026-08-14 — auditoria da documentação e 22 correções

Rodada independente sobre os oito READMEs e o glossário, com o auditor tendo
acesso ao sistema de arquivos e à CLI — o que permitiu verificar afirmações
contra o código e contra o workspace, em vez de apenas contra o próprio texto.
Registro em `docs/auditoria/2026-08-14_documentacao/`.

### Corrigido — fatos falsos

1. (Claude) Os blocos de saída do `README.md` estavam desatualizados em três dos
   cinco números, e o texto mandava tratar divergência como diagnóstico. Um
   leitor novo concluiria que seu ambiente está quebrado com o repositório
   aprovado — o inverso do propósito da seção. Números regenerados e a promessa
   trocada: as linhas de contagem são voláteis, o que importa é o `APROVADO`.
2. (Claude) O bloco do `--verify` mostrava 165 arquivos contra 174 reais, e
   omitia a primeira linha da saída — ou seja, havia sido editado à mão logo
   acima da frase que afirmava o contrário. Corrigido e a afirmação ajustada.
3. (Claude) Glossário dizia que **Add context** é a "única forma" de usar
   `x_prompts` e `x_docs`, contradizendo o próprio glossário e outros três
   documentos: `@` também funciona.
4. (Claude) Contagem do smoke test divergia entre documentos (71 e 64). São
   coisas diferentes — 71 verificações, 64 aprovações — e agora está explícito.
5. (Claude) `x_config/README.md` dizia "o único arquivo desta pasta" havendo
   também o próprio README.

### Corrigido — afirmações sobre o próprio sistema

1. (Claude) O `README.md` garantia verificação automática de identificador
   corporativo "inclusive em nome de pasta", mas o validador só cobria
   `ambiente_fonte/` — e o vetor descrito no ADR-0003 se materializa em
   `Novo_Ambiente_Simulado/`, que é versionado. **A guarda foi estendida**:
   `check_repo_corporate` varre o repositório inteiro, conteúdo e caminho,
   buscando apenas padrão corporativo (o username pessoal do laboratório é
   estado aceito). O texto passou a descrever a cobertura real.
2. (Claude) Diagrama e nota de rodapé atribuíam a publicação ao engine do Hub,
   decisão revertida pelo ADR-0005 e contrariada pelo próprio código.
3. (Claude) A camada squad aparecia como "fase 2" no diagrama e "Fase 5" na
   tabela — dois sistemas de numeração sem aviso.

### Adicionado

1. (Claude) Seção **"Antes de começar"** no `README.md`: o percurso mandava
   publicar sem nunca dizer que isso exige CLI instalada e autenticada, e a
   única menção a CLI no arquivo dizia que o workspace do trabalho não tem —
   sugerindo o oposto do pré-requisito. Agora há tabela de pré-requisitos,
   comandos de instalação e como confirmar.
2. (Claude) `x_docs/README.md`, que era a única extensão sem porta de entrada.
   Cinco arquivos dela não eram citados em documento nenhum, incluindo o
   `SKILL_TEMPLATE.md`. Inclui o procedimento de criar uma skill nova, que não
   estava escrito em lugar algum.
3. (Claude) Sete verbetes no glossário para termos usados sem definição:
   driver-side, bronze/silver/gold, expectations, readiness, runbook e AST.

### Atualizado

1. (Claude) FAQ movido para logo após o percurso inicial — respondia as dúvidas
   do primeiro dia e estava atrás de governança e roadmap.
2. (Claude) Os links dos notebooks didáticos quebravam no workspace, que é onde
   o documento é lido: lá os objetos são notebook e não têm extensão.
3. (Claude) O mermaid do guia sugeria que a skill carrega os helpers sozinha —
   exatamente o engano que o prefixo `x_` existe para evitar. Ganhou distinção
   entre automático e manual, com a ressalva explícita.
4. (Claude) Diagrama do `x_projects` mostrava o arquivo em `notebooks/` enquanto
   o texto dizia `modelos/churn/`, ensinando errado o único conceito da seção. O
   nó "fim da busca" afirmava um limite não documentado.
5. (Claude) `x_snippets/README.md` declarava que o catálogo é "a única lista
   mantida" e publicava a segunda lista logo abaixo. Agora a precedência está
   dita.
6. (Claude) A seção de fluxo de engenharia do guia descrevia pipelines que o
   leitor constrói, não a publicação deste pacote — que não usa bundle. Ganhou
   cabeçalho que separa as duas coisas.
7. (Claude) Contagens fixas restantes removidas da prosa.

### Não corrigido

- Números de teste citados na documentação (36/36, 64/71) não puderam ser
  reverificados pelo auditor, que não tinha acesso a `docs/testes/` por
  instrução. Permanecem como estavam, agora com a distinção entre verificações
  e aprovações explicitada.

## 2026-08-14 — auditoria da biblioteca e 13 correções

### Auditoria

1. (Rodrigo + Claude) Rodada de auditoria com Claude em sessão sem contexto,
   registrada em `docs/auditoria/2026-08-14_biblioteca-pit-join/`. Registrada
   como **A1, não A2**: o auditor é do mesmo modelo do implementador, então
   pontos cegos comuns permanecem. O gate para o trabalho segue exigindo uma
   segunda origem.
2. Resultado: 15 achados, **13 procedentes**, todos confirmados por leitura e
   depois reproduzidos em teste.

### Corrigido em `pit_join`

1. (Claude) `atraso_publicacao_dias` passa a ser **obrigatório**. Com o default
   zero e comparação inclusiva, um snapshot diário com data de referência igual
   à data da decisão entrava no resultado — vazamento sem erro, produzido pelo
   helper cuja razão de existir é evitá-lo.
2. (Claude) `janela_maxima_dias` comparava a **disponibilidade** em vez da
   referência, o que tornava a janela efetiva igual a `janela + atraso`. Um
   valor de 8 dias entrava sob janela de 3.
3. (Claude) Diagnóstico separava mal as ausências: chave nula, entidade sem
   histórico e feature indisponível na data caíam num número só, e a leitura
   natural levava a afrouxar o atraso — o movimento que reintroduz o vazamento.
4. (Claude) Empate de instante passa a **interromper por padrão**. O desempate
   anterior era determinístico mas enviesado: escolhia sempre o menor valor, o
   que em crédito é viés conservador sistemático, não escolha neutra.
5. (Claude) Encadear duas chamadas quebrava por colisão da coluna interna de
   disponibilidade, que agora não é devolvida por padrão.
6. (Claude) Contagem de `ts_feature` nulo, tipo do parâmetro validado, nomes de
   coluna protegidos por backticks e fuso da sessão reportado no diagnóstico.

### Corrigido em `join_diagnostics`

1. (Claude) Multiplicidade e relação eram medidas sobre o lado direito inteiro:
   uma chave que só existe à direita inflava a estatística e fazia o helper
   anunciar "1:N duplica" enquanto a expansão calculada dizia 1,0.
2. (Claude) Cobertura usava denominador com chave nula, enquanto os exemplos de
   órfãs as excluíam — a combinação "3 sem match, 0 exemplos" lia como defeito
   da ferramenta. Agora há cobertura sobre chaves válidas e contagem separada.
3. (Claude) Expansão passou a distinguir `left` de `inner`; contagens em passada
   única, para não produzir métricas incoerentes sobre fonte não determinística;
   amostra de órfãs ordenada; base vazia devolve expansão 1,0.

### Notas

- Os módulos haviam passado em 13 verificações de runtime escritas por quem os
  implementou, e **nenhuma delas pegou qualquer um dos treze achados**. As
  categorias que escaparam: ambiguidade semântica de tipo de data, interação
  entre parâmetros nunca combinados no teste, diagnóstico que agrega causas
  distintas, comportamento em escala, encadeamento e política de empate.
- Duas falhas foram introduzidas durante a própria correção e resolvidas:
  `conf.get(chave, default)` valida o default como configuração no Spark Connect
  e derruba a execução; e a fixture sorteava datas que podiam coincidir, criando
  empate acidental — a guarda nova o denunciou.
- Verificação final: **10 testes, um por achado, nenhuma falha**.
- Pendente para o ambiente do trabalho: o achado de escala (A5) recomenda hint
  de range-join, que exige `explain()` sobre volume representativo.

## 2026-08-14 — reformulação das instruções pessoais

### Corrigido

1. (Claude) **Duas instruções orientavam para comportamento que falha.** O
   arquivo pedia para preferir compute serverless e, adiante, para usar cache
   com benefício demonstrável — mas serverless recusa `cache()` e `persist()`,
   como o teste de runtime provou. E mandava instalar bibliotecas "conforme a
   documentação aplicável", quando instalar sem fixar versão derruba o kernel
   por alteração de pacotes core. Ambas substituídas pelo comportamento
   verificado.

### Adicionado

1. (Claude) Seção **Limites inegociáveis**, promovida ao topo, reunindo os vetos
   que estavam dispersos entre preferências de formatação: nada de afirmar
   execução sem evidência, escrita sem declaração prévia, vazamento temporal,
   PII exposta, heurística apresentada como norma, ou falha silenciada.
2. (Claude) Seção **Restrições verificadas do runtime**: serverless sem cache,
   `spark` global inexistente em módulo, autologging do MLflow ligado por
   padrão, necessidade de fixar versão, Python possivelmente anterior ao 3.12 e
   colisão dos wrappers no run ativo.
3. (Claude) Seção **Use a biblioteca antes de escrever**, a lacuna de maior
   custo: skills só valem quando carregadas, e conversas curtas frequentemente
   não carregam nenhuma. Nessas, o único guia ativo é este arquivo, que descrevia
   `x_snippets` como "pacote opcional" sem nunca pedir preferência por ele.
   Reescrever segue permitido — desde que declarado.
4. (Claude) Junção point-in-time e atraso de publicação passam a ser citados no
   anti-leakage, e diagnóstico de junção entra na validação de dados.

### Removido

1. (Claude) Manual dos diretórios `x_` (cerca de 1.400 caracteres): é referência,
   já está no README com mais detalhe, e custava em toda interação.
2. (Claude) Parágrafo esclarecendo que `/eda` e afins não são comandos — o hábito
   acabou junto com o ambiente antigo, apagado nesta mesma série de sessões.
3. (Claude) A contagem "as 12 skills" e demais números que envelhecem sozinhos.
4. (Claude) Procedimento que pertence às skills, onde já está melhor explicado.

### Verificação

Os três critérios de aceite declarados na proposta foram conferidos por script:
nenhuma instrução contradiz fato registrado em `docs/testes/spark/`; nenhuma
contagem, lista de pastas ou alias remanescente; e presença confirmada dos seis
temas que faltavam. Resultado: **7.056 caracteres**, contra 7.371 antes — menos
texto com o conteúdo crítico presente. Instruções não influenciam a seleção de
skill, então a certificação de roteamento 36/36 permanece válida sem reteste.

## 2026-08-14 — material didático, notebooks 03 e 04

### Adicionado

1. (Claude) `03_qualidade_de_juncao.py`: os quatro desfechos de um join —
   preserva, infla, encolhe e perde por chave nula — cada um com os números que
   o denunciam. Explica por que chave nula é contada à parte: em SQL `NULL`
   nunca casa com `NULL`, e a causa costuma ser outra (erro de extração, campo
   opcional) com correção também outra.
2. (Claude) `04_armadilhas_de_credito.py`: demonstra que somar taxas de
   inadimplência por safra exagera o acumulado, porque conta o mesmo contrato
   várias vezes — o erro que a auditoria do Codex corrigiu no ambiente anterior.
   E constrói uma variável deliberadamente vazada para mostrar que IV altíssimo
   é motivo de desconfiança, não de comemoração.
3. (Claude) Seção "Como se localizar" no `x_snippets/README.md`, ligando cada
   tipo de pergunta ao documento que a responde: inventário, catálogo por
   demanda, notebooks, skill do tutor e glossário.

### Notas

- Os quatro notebooks foram executados no Free antes da entrega; os dois novos
  passaram na primeira tentativa.
- O notebook 04 aproveita para reforçar, com exemplo, que faixas de IV e limites
  de PSI são referências e não normas — apresentá-las como exigência regulatória
  sem citar fonte é algo que as instruções do ecossistema proíbem.

## 2026-08-14 — material didático da biblioteca

### Adicionado

1. (Claude) `x_docs/notebooks/01_vazamento_temporal.py`: mostra o join ingênuo
   inflando a base e trazendo dado do futuro, e depois `pit_join` e
   `temporal_split` resolvendo. Executa sobre fixtures sintéticas e imprime a
   prova — zero linhas com score futuro no resultado.
2. (Claude) `x_docs/notebooks/02_drift_e_estabilidade.py`: constrói duas
   populações com **a mesma média** e formas opostas, para mostrar por que
   comparar média e desvio não é PSI. Reproduz o erro que existia no ambiente
   anterior e explica por que a interpretação exige limite calibrado.
3. (Claude) Inventário por módulo no `x_snippets/README.md`: uma linha para cada
   um dos 47 módulos, como visão do que existe. O catálogo continua sendo a
   visão por demanda; os dois papéis são distintos e não se repetem.

### Corrigido

1. (Claude) `tools/publicar_free.py` publicava **todo** `.py` como arquivo, o
   que está certo para a biblioteca e errado para material didático: notebook
   como arquivo não tem células para executar. A ferramenta passou a detectar o
   marcador `# Databricks notebook source` e reenviar esses arquivos como
   notebook; o `verify` confere os dois tipos separadamente.

### Notas

- Ambos os notebooks foram executados no Free antes de serem entregues. As duas
  falhas encontradas eram erros meus de escrita, não defeitos de módulo: import
  faltando e um DataFrame Spark passado a `temporal_split`, que opera em pandas.
- Esse segundo erro virou conteúdo: o notebook agora explica que definir split é
  decisão sobre metadados, não processamento de volume, e que o erro
  `Attribute 'copy' is not supported` não diz nada sobre a causa real.
- Decisão de escopo: notebook apenas onde o erro é caro e a lógica não é óbvia.
  Explicar `fmt_brl` linha a linha criaria manutenção sem ensinar nada. Para
  explicação sob demanda de qualquer módulo, a skill do tutor lê a versão atual
  do arquivo e não fica defasada.

## 2026-08-14 — biblioteca, fecho do sprint 0

### Notas

1. (Claude) **13 dos 14 módulos com dependência opcional verificados em
   runtime**, contra zero no início do dia. O conjunto de versões que funciona
   foi apurado e registrado em `x_snippets/requirements-optional.txt`, que antes
   listava nomes sem versão — e nessa forma não era instalável em serverless.
2. (Claude) `prophet_wrapper` permanece o único não verificado: falha com
   `'Prophet' object has no attribute 'stan_backend'` mesmo com autologging
   desligado e sem registro. O atributo não é usado pelo nosso código; ele deixa
   de existir quando o backend de inferência do Prophet não inicializa, o que
   indica incompatibilidade da biblioteca com o ambiente serverless. Fica
   marcado como não verificado em vez de presumido funcional.

### Corrigido

1. (Claude) `requirements-optional.txt` reescrito: pacotes core fixados no topo
   com a explicação do porquê, conjunto verificado com versões exatas, e o
   Prophet comentado com o motivo. Um inventário sem versões, num ambiente onde
   instalar sem fixar derruba o kernel, era instrução para quebrar o ambiente.

### Aprendizados de ambiente registrados

- O Databricks liga autologging do MLflow por padrão, e ele intercepta o `fit`
  mesmo quando o wrapper não registra nada — foi o que mascarou a falha do
  Prophet na primeira tentativa.
- `mlp_embeddings` espera uma lista de arrays, um por feature categórica, não
  uma matriz. A mensagem de erro do módulo já dizia isso com clareza.
- `tabnet_wrapper` e `arima_wrapper` só falhavam por colisão no run ativo do
  MLflow; isolados, executam normalmente.

## 2026-08-14 — biblioteca, endurecimento do pit_join

### Corrigido

1. (Claude) **Escolha indeterminada em empate de instante.** Duas versões da
   feature publicadas no mesmo momento deixavam o desempate a cargo do plano de
   execução: o mesmo código podia devolver valores diferentes entre execuções, o
   que quebra reprodutibilidade sem emitir erro. Passou a haver desempate
   determinístico, e o diagnóstico reporta `linhas_com_empate_de_instante` —
   empate costuma indicar duplicidade na fonte e não deveria passar silencioso.
2. (Claude) **Identificador sintético de linha eliminado.**
   `monotonically_increasing_id` não tem estabilidade garantida entre
   recomputações, e era usado para particionar a janela. A resolução passou a
   ser por par (chave, instante de decisão) distinto, com junção de volta. O
   desenho novo também corrige o caso de duas decisões da mesma entidade no
   mesmo instante — legítimas, por exemplo para produtos diferentes —, que antes
   disputavam a mesma partição.
3. (Claude) `AMBIGUOUS_COLUMN_REFERENCE` introduzido pela correção anterior: a
   tabela resolvida descende dos fatos, e reaproveitar os nomes das chaves fazia
   o Spark tratar a junção como auto-join. Colunas de junção renomeadas.

### Notas

- Verificação após as correções: **13 aprovações, nenhuma falha**, incluindo dois
  testes novos — escolha estável em três execuções consecutivas sob empate, e
  preservação de decisões duplicadas da mesma entidade.
- As três primeiras perguntas do contexto de auditoria eram fragilidades reais e
  foram resolvidas antes da submissão; o registro delas permanece, porque a
  correção também precisa ser revisada. Cinco perguntas novas ficaram em aberto,
  entre elas se o desempate deveria falhar em vez de escolher, e se o contrato
  de atraso constante por fonte é limitação aceitável.

## 2026-08-14 — biblioteca, sprints 4 a 6

### Adicionado

1. (Claude) `x_snippets/ml/mlflow_run.py`: contexto `run_governado`, que recusa
   abrir sem limitações declaradas e recusa fechar sem parâmetros, métricas e
   assinatura. As instruções pessoais já exigiam esse conjunto; os wrappers
   registravam apenas parâmetros e métricas, e o restante dependia de alguém
   lembrar. As duas recusas foram verificadas em runtime.
2. (Claude) Ponteiro para o catálogo de helpers nos **16 prompts**. Antes, zero
   prompts citavam helpers enquanto 11 das 12 skills os declaravam — quem
   partisse do formulário não recebia a orientação. Optou-se por referência
   única em vez de replicar as listas, para não recriar a divergência já
   corrigida nos dois catálogos e nos dois blocos de comandos.
3. (Claude) `docs/auditoria/2026-08-14_biblioteca-pit-join/01_contexto.md`:
   contexto da auditoria A2, com papéis (Claude implementa e não se autoavalia),
   o que já está verificado e cinco perguntas específicas — entre elas o empate
   de instantes no `pit_join` e a estabilidade de `monotonically_increasing_id`.

### Notas (sprints 4 a 6)

- Sprint 0 avançou de 3 para **8 dos 14** módulos verificados. Restam seis, que
  dependem de PyTorch, TabNet, Prophet e pmdarima — conjunto de versões
  compatível com `pandas 1.5.3`/`numpy 1.26.4` ainda não resolvido.
- Dois comportamentos confirmados em runtime e documentados: os wrappers de
  treino registram no run ativo do MLflow e colidem quando usados em sequência
  na mesma sessão; e `shap_explainer` exige `output_index` em resultado
  multi-output, recusa correta em vez de arbitrar a classe positiva.
- `train_catboost` foi aprovado quando isolado: a falha da rodada 8 era colisão
  de run, não defeito do módulo.

## 2026-08-14 — biblioteca, sprints 0 a 3

### Adicionado

1. (Claude) `x_snippets/spark/pit_join.py`: junção point-in-time com atraso de
   publicação declarado. Devolve o DataFrame e o diagnóstico do que foi
   descartado por indisponibilidade temporal. Preenche exigência textual da
   skill de feature engineering que não tinha implementação.
2. (Claude) `x_snippets/spark/join_diagnostics.py`: cobertura, não-match,
   multiplicidade e fator de expansão medidos **antes** do join, com chaves
   nulas contabilizadas à parte.
3. (Claude) `x_snippets/testing/fixtures.py`: geradores determinísticos
   (tabular, série temporal, fatos/features com vazamento marcado, safras).

### Corrigido

1. (Claude) **Defeito real em `x_snippets/ml/lgbm_ranker.py`**, encontrado ao
   exercitar o módulo pela primeira vez no runtime. Em `evaluate_ranking`, o
   reordenamento `group_labels[ranked_idx]` faz busca **por rótulo** quando `y`
   é uma Series do pandas: funcionava no primeiro grupo, onde rótulo coincide
   com posição, e quebrava do segundo em diante com `KeyError`. Passou a
   converter para array antes de fatiar.
2. (Claude) Defeito na fixture `fatos_e_features`, revelado pelo próprio teste
   anti-vazamento: com clientes repetidos entre decisões, uma feature "futura"
   para uma decisão era legitimamente passada para outra do mesmo cliente, e a
   marca `eh_futura` deixava de valer. Cada decisão passou a ter cliente
   próprio, e o teste ganhou a invariante universal
   (`feature_ts + atraso <= decisão`), que não depende do rótulo.

### Notas

- Verificação no runtime: **11 aprovações, nenhuma falha**, incluindo o teste
  que prova que nenhuma feature publicada após a decisão sobrevive ao
  `pit_join`, e a expansão de join medida contra multiplicidade conhecida
  (1:1 → 1,0; 1:N controlado → 2,0).
- Rodada 7 documentou uma restrição de ambiente não conhecida: instalar as
  bibliotecas de ML sem fixar versão derruba o kernel serverless por alteração
  de pacotes core (`pandas`, `numpy`). Detalhe em `docs/testes/spark/README.md`.
- Sprint 0 permanece **aberto**: apenas 3 dos 14 módulos com dependência
  opcional foram verificados (`train_lgbm`, `survival_cox`, `kaplan_meier`).
  Os demais exigem novo ambiente com versões compatíveis fixadas.

## 2026-08-14 — documentação, sprint 6 de 6

### Atualizado

1. (Claude) `docs/decisions/README.md`: apresenta o que é um ADR e por que a
   imutabilidade importa, usando o par 0002/0005 deste próprio projeto como
   demonstração — a sequência preserva inclusive o erro corrigido.
2. (Claude) `docs/handoffs/README.md`: exemplo curto de handoff. O formato só
   fica claro vendo um pronto; a descrição sozinha não ensinava.
3. (Claude) `docs/auditoria/README.md`: explica por que auditar com mais de um
   modelo — cada um erra de forma diferente, e a divergência entre eles marca
   onde o material é ambíguo. Tabela dos quatro níveis com o gatilho de cada um.
4. (Claude) `docs/testes/forward/README.md`: define roteamento antes de mostrar
   resultado, para quem cai direto na página.
5. (Claude) `docs/testes/spark/README.md`: como ler uma falha, com os três
   padrões observados na prática e a advertência de que passar na máquina local
   não prova nada sobre o runtime.

### Encerramento do plano de documentação

Seis sprints concluídos. Balanço em relação ao diagnóstico: os 14 READMEs
receberam tratamento, mais um glossário novo; as três lacunas sistêmicas
apontadas — ausência de glossário, exemplos sem retorno e falta de percurso
inicial — foram fechadas. Nenhuma `description` de skill foi tocada em nenhum
sprint, e a certificação de roteamento 36/36 permanece válida.

## 2026-08-14 — documentação, sprint 5 de 6

### Adicionado

1. (Claude) `ambiente_fonte/README.md`: diagrama do trajeto fonte → simulado →
   workspaces e a resposta direta a "por que duas pastas com o mesmo conteúdo" —
   a fonte é neutra, o simulado acrescenta a camada `Users/<username>/` que muda
   conforme o destino. Inclui o percurso completo de uma alteração.
2. (Claude) `x_projects/README.md`: diagrama da descoberta hierárquica do
   `AGENTS.md`, com as três consequências práticas — busca de baixo para cima,
   diretórios sem o arquivo são apenas atravessados, e os arquivos encontrados
   somam contexto em vez de se substituírem.
3. (Claude) `x_scripts/README.md`: saída real de `data_quality_check` executada
   em serverless sobre tabela sintética. O exemplo escolhido reprova por prazo de
   atualização com todos os demais checks aprovados, o que evidencia que
   `status: "fail"` reflete a política de limite configurada, não qualidade do
   dado.
4. (Claude) `x_snippets/README.md`: tabela de falhas de import com causa e
   correção, montada a partir de erros reais do runtime, não de suposição.

### Atualizado

1. (Claude) O catálogo por pacote de `x_snippets` passa a apontar para o
   catálogo por demanda, encerrando a duplicação que levaria as duas listas a
   divergir na primeira alteração.

## 2026-08-14 — documentação, sprint 4 de 6

### Atualizado

1. (Claude) `x_config/README.md`: passa a explicar o que é MCP e por que outras
   ferramentas usam arquivo JSON, antes de dizer que aqui isso não vale. Um
   arquivo de configuração que não configura nada, sem mensagem de erro que
   explique, justifica o aviso. Inclui os passos da configuração real e a
   proibição de segredos em pasta versionada.
2. (Claude) `.claude/skills/README.md`: explicita a distinção entre as duas
   famílias de skill do projeto — as daqui constroem o ecossistema, as
   `rodrigo-*` são o ecossistema. Acrescenta como uma skill é acionada e como
   criar outra.
3. (Claude) `x_prompts/README.md`: percurso completo de um formulário, do modelo
   ao preenchido, com a explicação de por que `NÃO INFORMADO` difere de campo
   vazio e de como reconhecer resposta que ignorou o contrato.

### Pendente

- O passo 4 do percurso de `x_prompts` descreve o contrato esperado em vez de
  mostrar retorno real: falta uma execução no Genie Code. Marcado no próprio
  arquivo; resposta plausível não foi inventada para preencher a lacuna.

## 2026-08-14 — documentação, sprint 3 de 6

### Adicionado

1. (Claude) Guia do ecossistema: tabela com o pedido que aciona cada uma das 12
   skills sem precisar de `@`. As frases não foram inventadas — são as que
   passaram nos forward tests. Acompanham as duas lições que os testes deram:
   skill que trabalha sobre artefato não dispara sem o artefato no chat, e
   vocabulário genérico vai para a skill errada.
2. (Claude) Verificação de acesso à biblioteca com saída real, já que o import
   não imprime nada e silêncio pode ser confundido com falha.

### Atualizado

1. (Claude) Tabela de solução de problemas ampliada de 7 para 12 sintomas,
   incorporando o que apareceu durante os gates: `.py` importado como notebook,
   `cache()` recusado em serverless, arquivo obsoleto sobrevivendo à publicação,
   metadata em cache após editar skill, e nenhuma skill carregada por falta do
   artefato citado.

### Corrigido

1. (Claude) `tools/render_simulado.py` copiava a árvore inteira, inclusive
   artefatos de execução local. Rodar um helper dentro de `ambiente_fonte/` — o
   que aconteceu ao capturar as saídas deste sprint — criava `__pycache__`, que
   era renderizado e **publicado no workspace**. O `verify` não acusava, porque
   compara fonte com remoto e o lixo estava nos dois. O render passa a ignorar
   `__pycache__`, `.pyc`, `.pyo` e caches de ferramenta; fonte, simulado e
   workspace foram limpos.

## 2026-08-14 — documentação, sprint 2 de 6

### Adicionado

1. (Claude) `README.md`: percurso de primeira hora em cinco passos, do zero até
   uma alteração publicada e conferida no workspace.
2. (Claude) Seção de comandos com **saída real capturada de execução** — padrão
   que os sprints seguintes replicam. Retorno redigido à mão foi descartado como
   prática: envelhece sem avisar.
3. (Claude) FAQ com oito perguntas, entre elas as três que o diagnóstico
   apontou como não respondidas em lugar nenhum: por que duas pastas com o mesmo
   conteúdo, o que acontece ao editar direto no workspace, e por que a skill
   alterada continua se comportando como antes.

### Corrigido

1. (Claude) O diagrama de ciclo de vida ainda citava publicação pelo engine do
   Hub, decisão supersedida pelo ADR-0005. Passou a refletir os comandos reais,
   incluindo a conferência, que antes não aparecia no fluxo.

## 2026-08-14 — documentação, sprint 1 de 6

### Adicionado

1. (Claude) `x_docs/glossario.md`: 49 verbetes separados por procedência —
   plataforma Databricks, vocabulário de modelagem e convenção deste projeto —
   mais uma seção final sobre capacidades que não existem e induzem a erro
   (slash commands próprios, hooks, memória automática, MCP por arquivo).
   A separação por origem é o ponto: procurar um termo de convenção na
   documentação oficial não devolve nada, e isso não era explicado em lugar
   nenhum.
2. (Claude) Ponteiro para o glossário no `README.md` da raiz e no guia do
   ecossistema. Nenhum outro texto foi alterado neste sprint.

## 2026-08-14

### Adicionado (publicação no Free com verificação)

1. (Claude) `tools/publicar_free.py` e skill `.claude/skills/publicar-free/`:
   plano em dry-run, publicação com gate `--execute` e `verify` read-only que
   confere ausentes, obsoletos, `.py` como `FILE`, 12 skills e 6 diretórios de
   extensão. Ciclo completo executado: 164/164 arquivos, zero pendências.
2. (Claude) ADR-0005, supersedindo o ADR-0002: o engine do Hub não pode ser
   consumido nesta camada. Evidência medida no workspace — `.py` publicado por
   ele vira `NOTEBOOK` (quebraria todos os imports de `x_snippets`), enquanto
   `--format AUTO` produz `FILE`; e o cabeçalho que ele antepõe invalidaria o
   frontmatter YAML das skills. O padrão de três fases foi mantido.

### Corrigido (publicação no Free)

1. (Claude) O `verify` detectou, na primeira execução,
   `.assistant/.mcp_servers.json` remanescente no workspace — arquivo legado
   inerte que a auditoria do Codex removera do pacote e que sobrevivera porque
   `import-dir --overwrite` sobrescreve mas nunca apaga. Removido, e a detecção
   de obsoletos incorporada à ferramenta.

2. (Claude) `tools/publicar_free.py` concatenava stdout e stderr antes de fazer
   parse de JSON. A CLI emite um aviso intermitente em stderr que corrompia a
   saída e derrubava o `verify` com `JSONDecodeError`. Os fluxos passaram a ser
   tratados separadamente, com parse tolerante; verificado em execuções
   repetidas.

### Observação encaminhável (outro repositório)

- O `_fmt_args` do engine do Hub publica `.py` como notebook; o próprio
  `write_evidence.py` da camada global está nessa condição. Correção cabe ao
  dono daquele repositório, com testes próprios.

### Adicionado (fase 4 — replicação no trabalho)

1. (Claude) `docs/playbooks/replicacao-trabalho.md`: runbook completo para o
   workspace corporativo sem CLI — backup obrigatório antes de qualquer
   remoção, três rotas de transporte com o que confirmar em cada uma, limpeza
   do ambiente antigo, verificação de estrutura, testes de aceitação, rollback
   e caminho de escala para squad.
2. (Claude) Skill operacional `.claude/skills/replicar-trabalho/` com os
   pré-requisitos verificáveis e os guardrails da operação.
3. (Claude) `.claude/rules/free-vs-trabalho.md`: nova matriz de diferenças de
   runtime já observadas (cache/persist, config de cluster, bibliotecas ML,
   variável global `spark`).

### Corrigido (fase 4)

1. (Claude) `tools/spark_smoke_test.py` tinha o caminho da biblioteca fixo no
   usuário do laboratório, o que o tornava inútil no trabalho. Passa a resolver
   pelo usuário logado, com widget `assistant_root` para sobrepor. Regressão
   executada no Free: 64 aprovações, nenhuma falha.
2. (Claude) Vetor de vazamento fechado: identificador corporativo em **nome de
   pasta** escapava à validação, que só lia conteúdo. Renderizar o simulado com
   o username do trabalho criaria `Users/<identificador>/` e um `git add`
   publicaria o identificador. Agora `tools/render_simulado.py` recusa username
   com aparência corporativa e `tools/validate_assistant.py` verifica caminhos
   além do conteúdo.

### Adicionado (pacote de helpers — sprints 2 e 3 de 3)

1. (Claude) Seção `## Usar helpers da biblioteca` em 11 `SKILL.md`, cada uma com
   a tabela demanda → módulo do próprio fluxo, link para o catálogo e as
   ressalvas técnicas do domínio (leakage em splits, incidência acumulada em
   safra, thresholds calibrados em drift, escape de HTML em documentação).
2. (Claude) `rodrigo-auditoria-skills` passa a verificar aderência à biblioteca:
   novo passo na auditoria de implementação (conferir seção de helpers contra o
   catálogo), novo passo na auditoria de output (reimplementação silenciosa de
   lógica disponível vira achado) e nova dimensão de avaliação.
3. (Claude) `templates/rubrica_universal.md`: dimensão D10 reescrita com âncoras
   objetivas de aderência à biblioteca.

### Corrigido

1. (Claude) A âncora 9-10 da dimensão D10 da rubrica premiava o uso de "hooks",
   capacidade inexistente na plataforma (`.claude/rules/genie-code-oficial.md`).
   Removida junto com a reescrita da dimensão.

### Notas (pacote de helpers)

- Nenhuma `description` foi alterada nos três sprints: a seleção automática lê
  apenas o frontmatter, e as seções entram no corpo. Verificado por diff — a
  certificação de roteamento 36/36 permanece válida sem reteste.

### Adicionado (pacote de helpers — sprint 1 de 3)

1. (Claude) ADR-0004: helpers passam a ser declarados explicitamente nas skills,
   em vez de descobertos em tempo de chat. Levantamento que motivou a decisão:
   **nenhum dos 12 `SKILL.md` citava um helper** — as 3 referências do pacote
   estavam em templates auxiliares.
2. (Claude) `ambiente_fonte/.assistant/x_docs/catalogo_helpers.md`: catálogo
   demanda → módulo cobrindo os 54 helpers (47 `x_snippets` + 7 `x_scripts`),
   com API pública, marcação de dependência opcional (exigida no import vs. na
   chamada) e as restrições de runtime confirmadas no smoke test.
3. (Claude) Referências cruzadas ao catálogo em `.assistant/README.md`,
   `x_snippets/README.md` e `x_scripts/README.md`. Réplica do Free republicada.

### Adicionado

1. (Claude) `docs/testes/forward/resultados/2026-08-14_rodada1.md`: resultado da
   rodada 1 dos forward tests executada pelo Rodrigo no Genie Code do Free —
   **33 PASS, 2 FAIL, 1 pendente** de 36. Coleta automatizada via arquivos de
   evidência em `x_lab/forward_tests/` lidos por CLI.

2. (Claude) `docs/testes/forward/resultados/2026-08-14_rodada2.md`: rodada 2
   (5 testes com prompts autocontidos, IDs `-r2`) — **5 PASS, 0 FAIL**.
   **Gate de roteamento FECHADO: 36/36 PASS** (positivos 12/12, negativos
   12/12, menções 12/12), sem nenhuma alteração de `description`.

### Notas

- Rodada 2 confirmou a hipótese da rodada 1: `10P` passou com a **mesma**
  `description` e apenas o artefato embutido no prompt — a falha era do
  instrumento de teste. Nenhuma `description` foi alterada em nenhuma rodada.
- Item de vigilância registrado: `comentar-notebook` respondeu ao vocabulário
  "células %md" mas não a "markdown de documentação" no `11N-r2`; sem ação por
  ora, pois no uso real o notebook aberto no editor é sinal mais forte.
- As `description` do pacote auditado pelo Codex se mostraram bem calibradas:
  **12/12 casos negativos corretos**, sem nenhuma das colisões previstas
  (drift, materialização, deterioração, auditoria×execução); em 11 deles o
  Genie ainda escolheu a skill ideal do desvio. Nenhuma description foi
  alterada.
- As 2 falhas (`10P`, `11P`, ambas com resultado "nenhuma") concentraram-se nas
  skills que dependem de artefato no chat: os prompts citavam "este notebook"/
  "este stack trace" sem que existissem — defeito do instrumento, não do
  ambiente. Prompts v2 autocontidos aplicados no roteiro para a rodada 2
  (`07M`, `10P`, `10N`, `11P`, `11N`).
- Confirmado que skills nativas do Databricks (`data-sampling`) coexistem com as
  `rodrigo-*` no mesmo chat, sem conflito de seleção.

## 2026-08-13

### Adicionado

1. (Claude) Bootstrap do repositório: `CLAUDE.md` canônico, adaptadores
   `AGENTS.md`/`GEMINI.md`, `README.md`, este changelog e `.gitignore` com
   quarentena de `Ambiente_Antigo/`.
2. (Claude) Centro de IA `.claude/`: índice operacional, 5 regras
   (fonte de verdade, nomenclatura oficial Genie Code, Free vs. trabalho,
   multi-LLM, padrão de documentação), 3 arquivos de contexto, skills
   `validar-assistant` e `render-simulado`, e 4 templates.
3. (Claude) `ambiente_fonte/` criado como cópia editável do pacote
   `Ajustes_Codex/assistant_optimized_2026-08-13/` (12 skills, instruções,
   extensões `x_`). O pacote original permanece congelado como referência.
4. (Claude) `tools/validate_assistant.py`: recria localmente a bateria de
   validação da auditoria do Codex (frontmatter, links, tamanhos, AST Python,
   cercas Markdown, mojibake, identificadores pessoais).
5. (Claude) `tools/render_simulado.py`: gera `Novo_Ambiente_Simulado/` como
   espelho da árvore do workspace a partir de `ambiente_fonte/`.
6. (Claude) ADRs 0001 (arquitetura multi-IA), 0002 (reuso do engine
   `databricks-genie` do Verg_Alchemy_Hub) e 0003 (quarentena do
   `Ambiente_Antigo/`).

### Adicionado (testes Spark serverless — gate aprovado)

1. (Claude) `tools/spark_smoke_test.py` (notebook) + suíte `docs/testes/spark/`:
   71 checks executados em job serverless one-time no Free (Spark 4.1.0) —
   resultado final **64 PASS / 0 FAIL / 7 opcionais ausentes**.
2. (Claude) O gate revelou e levou à correção de 3 defeitos reais no
   `ambiente_fonte/` invisíveis à validação estática: `spark` como global
   inexistente em 6 módulos; `cache()`/`unpersist()` incompatíveis com
   serverless em `safe_display`, `quick_profile` e `drift_detector`;
   f-string com backslash (PEP 701, Python ≥ 3.12) em `kpi_card.py`.
   Réplica do workspace Free republicada após as correções.

### Adicionado (forward tests)

1. (Claude) Skill `.claude/skills/forward-test-skills/` e suíte em
   `docs/testes/forward/`: roteiro com 36 testes (12 skills × positivo,
   negativo e `@menção`), template de resultados e índice de rodadas. Casos
   negativos desenhados sobre as zonas de colisão entre descriptions
   (drift, WoE/IV, explicar×documentar, materialização, deterioração).

### Atualizado

1. (Claude) Workspace Databricks Free zerado e republicado como réplica deste
   projeto, a pedido do Rodrigo: backup do conteúdo anterior (camada global
   `global-*` do Hub + instruções, 10 arquivos) feito antes da remoção;
   `Novo_Ambiente_Simulado/Users/<username>/` importado via
   `databricks workspace import-dir`. Verificado: 12 skills `rodrigo-*`,
   extensões `x_`, instruções e `.py` como `FILE` (não notebook).
2. (Claude) `.claude/context/ambiente-free.md` atualizado com o novo estado do
   workspace (camada global do Hub removida; republicável pelo Hub).

### Notas

- Análise independente confirmou os achados da auditoria do Codex contra o
  export original (6 skills sem frontmatter, skills de até 2.141 linhas,
  instruções com nome sem ponto, aliases `/eda` e "hooks" não suportados,
  MCP JSON vazio, identificador corporativo em 7+ arquivos).
- Repositório GitHub privado confirmado; `Ambiente_Antigo/` mantido fora do
  git por conter identificador corporativo (ver ADR-0003).
