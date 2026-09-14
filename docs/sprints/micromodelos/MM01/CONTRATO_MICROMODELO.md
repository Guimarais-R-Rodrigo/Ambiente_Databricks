# Contrato `micromodelo.yaml` — schema 1.0.0

## 1. Papel do arquivo

`micromodelo.yaml` é a especificação estruturada canônica do micromodelo. Ele registra **o que o micromodelo significa e como deve ser avaliado**, não o histórico crescente das execuções. README, notebook, catálogo e handoffs futuros devem ser derivados ou confrontados com esse contrato.

O arquivo real de cada micromodelo pertence ao ambiente corporativo autorizado. Este repositório contém apenas o contrato, o template e fixtures sintéticos.

O carregador da MM01 é fail-closed também na sintaxe: chaves duplicadas em YAML ou JSON são recusadas. Não se aceita o comportamento implícito de parsers que preservam silenciosamente apenas a última ocorrência.

## 2. Grupos obrigatórios

### `schema_version`

Versão do formato estrutural. Na MM01 o único valor aceito é `1.0.0`. Mudança incompatível do contrato exige nova versão do schema; não se altera silenciosamente a interpretação de um arquivo antigo.

### `identidade`

Contém `nome`, `titulo`, `micromodel_version` e `estado`. `micromodel_version` identifica a evolução humana do micromodelo; não substitui o `spec_fingerprint` que será criado na MM02.

`fase_anterior` e `fase_atual` tornam o par declarado localmente verificável, mas o documento corrente não é prova suficiente do próprio histórico. Quando existe uma especificação anterior confiável, o validador pode recebê-la por `--previous`: nesse modo ele confere identidade, versão e transição real entre snapshots, impede regressão de versão e recusa rewind de uma versão já `PUBLICADO`. Isso resolve a auditabilidade da MM01 sem introduzir fingerprint antecipadamente.

### `negocio`

Explicita a característica, o objetivo, a definição operacional, os usos pretendidos e os usos proibidos. A definição deve ser observável e auditável; rótulo de negócio sem critério operacional não é suficiente.

### `entidade`

Declara entidade, chave lógica, granularidade, população elegível e referência temporal. A chave é lógica/informacional; o contrato não concede permissão nem cria constraints no ambiente.

### `fontes`

Cada fonte recebe `id`, `catalogo_ref`, `schema`, `objeto`, tipo, campos, papel e proveniência. A referência permitida na MM01 é `CATALOGO_PRODUTO`, que representa simbolicamente o catálogo oficial configurado no workspace. O validador reprova outra referência.

O nome real do catálogo não é versionado no Git e o contrato não concede acesso à fonte. A CLI da MM01 também não possui argumento para ampliar o conjunto de `catalogo_ref`: ampliar o escopo de fontes é gate humano e deve nascer em mudança explícita posterior, não como override de execução.

### `evidencias` e `contra_evidencias`

Regras favoráveis e desfavoráveis são registradas separadamente. Cada item referencia fontes conhecidas, descreve a regra e carrega proveniência.

Durante as fases iniciais as listas podem permanecer vazias. Ao entrar em `EM_VALIDACAO` ou fase posterior, `fontes`, `evidencias`, `contra_evidencias` e `validacao.criterios` precisam estar não vazios, e as regras de evidência/contra-evidência precisam estar `APROVADO`. Assim, vazio antes do estudo significa “ainda não especificado”; vazio durante validação formal não é aceito como se significasse “provado que não existe”.

### `classificacao`

O tipo inicial é `BOOLEANO_COM_INDETERMINADO`. O contrato exige três definições diferentes:

- `quando_true`: quando há base suficiente para afirmar a característica;
- `quando_false`: quando há base suficiente para negar a característica;
- `quando_indeterminado`: quando a informação não permite concluir nem TRUE nem FALSE.

A distinção é verificada após normalização editorial básica de caixa, acentuação, pontuação e espaços; não basta copiar a mesma definição mudando apenas forma textual. A política de ausência de evidência só aceita `INDETERMINADO` ou `REGRA_EXPLICITA_APROVADA`.

Limiar material pode ser registrado como `PROPOSTO` enquanto o micromodelo ainda está em descoberta/estudo. A partir de `EM_VALIDACAO`, todo limiar existente precisa carregar proveniência `APROVADO`. Dessa forma, a fonte canônica preserva propostas sem permitir que elas atravessem o gate formal como decisões válidas.

### `score`

Score pode ser habilitado ou desabilitado. Quando habilitado, exige:

- `tipo_semantica`: `FORCA_EVIDENCIA`, `PROBABILIDADE_CALIBRADA` ou `OUTRA_APROVADA`;
- descrição da semântica;
- escala 0–100;
- regra de normalização;
- componentes/pesos, quando existirem;
- proveniência da decisão de score.

Assim como limiares, pesos podem permanecer `PROPOSTO` nas fases pré-gate, mas todo peso existente precisa estar `APROVADO` ao entrar em `EM_VALIDACAO` ou fase posterior.

`PROBABILIDADE_CALIBRADA` exige calibração com proveniência `MEDIDO` e referência de execução. Além disso, `calibracao.evidencia_ref` precisa resolver para um `experimentos[].id` existente cujo experimento esteja `EXECUTADO` e com proveniência `MEDIDO`. A referência não é texto decorativo: ela possui integridade referencial dentro da especificação.

Além do enum, o validador barra linguagem probabilística em um score não calibrado; portanto não basta deixar `tipo_semantica=FORCA_EVIDENCIA` e escrever “probabilidade” ou “chance” na descrição.

Quando score está desabilitado, semântica, escala, normalização, componentes, calibração e campo de score na saída devem permanecer vazios/nulos.

### `experimentos`

Registra hipóteses relevantes da especificação. Um experimento `EXECUTADO` exige resultado e proveniência `MEDIDO`. O identificador da execução é referência externa; o YAML não incorpora o histórico das runs.

Experimentos também formam o namespace canônico usado por `score.calibracao.evidencia_ref`: uma calibração probabilística só é aceita se a evidência apontada existir e tiver sido efetivamente executada/medida.

### `validacao`

Separa resultado técnico medido da aprovação humana. `APROVADO` exige ambos:

1. resultado com proveniência `MEDIDO`;
2. `aprovacao_humana.status=APROVADO`, com responsável, timestamp e referência materialmente preenchida.

Fase `VALIDADO` ou posterior não é aceita se esse gate não estiver satisfeito. Strings compostas apenas por whitespace ou caracteres invisíveis não contam como referência auditável; o contrato é fail-closed também para esse tipo de preenchimento aparente.

### `saida`

Possui dois contratos distintos.

`saida.estudo` preserva `TRUE`, `FALSE` e `INDETERMINADO`, além do score quando habilitado.

`saida.publicacao` começa `PENDENTE`. A partir de `CANDIDATO_PRODUTO`, precisa estar `DEFINIDO`, com campo final `BOOLEAN` e uma política aprovada para `INDETERMINADO`: excluir do universo publicado, usar campo de cobertura separado ou outra solução explicitamente aprovada.

A política possui o campo estruturado `indeterminado_vira_false`, fixado em `false`. O validador também recusa descrição que contradiga essa regra estruturada. Assim, nenhum consumidor válido do contrato pode interpretar uma política aceita como autorização implícita para converter `INDETERMINADO` em `FALSE`.

### `tracking`

Na MM01 fixa somente a fronteira: backend `MLFLOW`, política ainda `PENDENTE_MM06` e `armazenar_historico_runs_no_yaml=false`. Tags, métricas e perfis de run pertencem à MM06.

### `governanca`

Reserva campos para classificação de dados, LGPD, gestor da informação e observações. `PENDENTE` é valor explícito aceitável enquanto a decisão humana ainda não ocorreu; o framework não inventa esses valores.

### `publicacao`

Registra apenas o estado de interface com a governança externa: `NAO_INICIADA`, `CANDIDATA`, `EM_VALIDACAO_EXTERNA`, `PUBLICADA` ou `REJEITADA`. Não replica regras institucionais.

O estado de publicação precisa ser coerente com a fase do ciclo: antes de `CANDIDATO_PRODUTO`, permanece `NAO_INICIADA`; em `CANDIDATO_PRODUTO`, é `CANDIDATA` ou `REJEITADA`; `EM_VALIDACAO_GOVERNANCA` exige `EM_VALIDACAO_EXTERNA` e `handoff_ref`; `PUBLICADO` exige `PUBLICADA` e `produto_dados_ref`. As referências de handoff e Produto de Dados precisam conter texto material, não apenas whitespace/invisíveis. A suíte inclui caminhos positivos até publicação para provar que esses gates são satisfazíveis e não apenas negativos.

### `proveniencia`

Registra criação do arquivo e, quando necessário, referências adicionais por alvo. As afirmações materiais também carregam proveniência junto do próprio bloco para permitir validação local.

`APROVADO` exige bloco de aprovação com conteúdo auditável; `MEDIDO` exige medição com referência de execução material. A presença sintática de uma string vazia visualmente não satisfaz esses estados.

## 3. IDs e referências

IDs internos usam `snake_case`, começam por letra e possuem de 3 a 64 caracteres. Referências de evidência para fontes precisam resolver para um `fontes[].id` existente. IDs duplicados são inválidos nas coleções controladas, incluindo fontes, evidências, contra-evidências, limiares, componentes do score e experimentos.

`score.calibracao.evidencia_ref` usa especificamente o namespace de `experimentos[].id` e só aceita experimento executado/medido.

## 4. Valores pendentes

O contrato prefere `PENDENTE`, lista vazia ou `null` explícito a um valor inventado. “Ainda não executado” é estado válido da especificação; transformar lacuna em número, aprovação ou resultado observado é erro de proveniência.

`PROPOSTO` também é estado válido nas fases de construção. O gate transforma a ausência de aprovação em bloqueio apenas quando a fase exige decisão formal; não obriga a fonte canônica a esconder propostas ainda em análise.

## 5. O que não está definido na MM01

A MM01 não define fingerprint, crawler de catálogo, feature engineering, cálculo de score específico, contrato de runs, notebook de estudo, README do micromodelo, handoff de publicação, visual ou migração. Esses temas permanecem nas sprints posteriores do Plano Mestre.
