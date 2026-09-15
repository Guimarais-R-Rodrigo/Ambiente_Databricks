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

A distinção é verificada após normalização editorial de caixa, acentuação, pontuação e espaços. Caracteres Unicode default-ignorable (`Cf`) e variation selectors são removidos antes da tokenização, para que inserções invisíveis dentro de palavras não fabriquem uma diferença semântica artificial; não basta copiar a mesma definição mudando apenas forma textual.

A política de ausência de evidência deixou de depender de prosa normativa. `classificacao.ausencia_evidencia` possui comportamento estruturado:

- `tratamento=INDETERMINADO` exige `resultado_sem_evidencia=INDETERMINADO` e `regra_ref=null`;
- `tratamento=REGRA_EXPLICITA_APROVADA` exige proveniência `APROVADO` e `regra_ref` auditável; o resultado aplicável fica declarado em `resultado_sem_evidencia`.

Não existe campo livre capaz de redefinir esse comportamento. Uma propriedade legada como `descricao` nesse bloco é recusada pelo schema fechado. Portanto uma regra que converta ausência em `FALSE` só pode existir de forma explícita, estruturada, referenciada e aprovada.

Limiar material pode ser registrado como `PROPOSTO` enquanto o micromodelo ainda está em descoberta/estudo. A partir de `EM_VALIDACAO`, todo limiar existente precisa carregar proveniência `APROVADO`. `classificacao.limiares[].valor` precisa ser um número finito: NaN e ±Infinity são recusados. Dessa forma, a fonte canônica preserva propostas sem permitir que elas atravessem o gate formal como decisões inválidas.

### `score`

Score pode ser habilitado ou desabilitado. Quando habilitado, a semântica executável é determinada exclusivamente por campos estruturados:

- `tipo_semantica`: `FORCA_EVIDENCIA`, `PROBABILIDADE_CALIBRADA` ou `OUTRA_APROVADA`;
- `semantica_ref`: referência auditável para a decisão/definição de semântica quando o gate formal é atingido; essa referência **não substitui nem sobrescreve** `tipo_semantica`;
- escala exatamente 0–100;
- `normalizacao` estruturada com método, referência quando aplicável e proveniência;
- componentes/pesos, quando existirem;
- proveniência da decisão de score.

A MM01 não usa mais texto livre `score.semantica` para inferir se um score é probabilístico. Esse campo legado é propriedade desconhecida e é rejeitado. Assim, sinônimos como “percentual estimado”, “risco percentual” ou `likelihood` não podem redefinir um `FORCA_EVIDENCIA` por prosa. Se o score representa probabilidade, o único contrato válido é `tipo_semantica=PROBABILIDADE_CALIBRADA`.

`normalizacao` também deixou de ser prosa normativa. Os métodos estruturados são `PENDENTE`, `SOMA_PONDERADA_0_100`, `MIN_MAX_0_100`, `LINEAR_0_100` e `CUSTOM_APROVADO`. Antes do gate formal, `PENDENTE` pode permanecer proposto. A partir de `EM_VALIDACAO`, o método precisa estar definido e aprovado; `CUSTOM_APROVADO` exige referência auditável da regra.

Assim como limiares, pesos podem permanecer `PROPOSTO` nas fases pré-gate, mas todo peso existente precisa estar `APROVADO` ao entrar em `EM_VALIDACAO` ou fase posterior. `score.componentes[].peso` também precisa ser finito; NaN e ±Infinity não são valores materiais válidos.

`PROBABILIDADE_CALIBRADA` exige calibração com proveniência `MEDIDO` e referência de execução. Além disso, `calibracao.evidencia_ref` precisa resolver para um `experimentos[].id` existente cujo experimento esteja `EXECUTADO` e com proveniência `MEDIDO`. Para os demais tipos de semântica, um bloco de calibração probabilística é recusado como inesperado.

Quando score está desabilitado, tipo de semântica, referência de semântica, escala, normalização, componentes, calibração e campo de score na saída devem permanecer vazios/nulos.

### `experimentos`

Registra hipóteses relevantes da especificação. Um experimento `EXECUTADO` exige resultado e proveniência `MEDIDO`. O identificador da execução é referência externa; o YAML não incorpora o histórico das runs.

Experimentos também formam o namespace canônico usado por `score.calibracao.evidencia_ref`: uma calibração probabilística só é aceita se a evidência apontada existir e tiver sido efetivamente executada/medida.

### `validacao`

Separa resultado técnico medido da aprovação humana. `APROVADO` exige ambos:

1. resultado com proveniência `MEDIDO`;
2. `aprovacao_humana.status=APROVADO`, com responsável, timestamp e referência materialmente preenchida.

Fase `VALIDADO` ou posterior não é aceita se esse gate não estiver satisfeito.

A definição de “texto material” é positiva: após normalização NFKC, o validador exige ao menos uma letra ou número Unicode. Espaços, controles, caracteres de formatação, variation selectors e marcas combinantes isoladas não satisfazem uma prova auditável. Isso se aplica a aprovação, medição e referências externas de publicação.

### `saida`

Possui dois contratos distintos.

`saida.estudo` preserva `TRUE`, `FALSE` e `INDETERMINADO`, além do score quando habilitado.

`saida.publicacao` começa `PENDENTE`. A partir de `CANDIDATO_PRODUTO`, precisa estar `DEFINIDO`, com campo final `BOOLEAN` e uma política aprovada para `INDETERMINADO`.

A política de publicação também é exclusivamente estruturada: `indeterminado_vira_false` é fixado em `false`; `tratamento` pode ser `EXCLUIR_DA_PUBLICACAO`, `CAMPO_COBERTURA_SEPARADO` ou `OUTRA_APROVADA`; e `regra_ref` só é usada por `OUTRA_APROVADA`, quando passa a ser obrigatória e auditável. O bloco não possui descrição normativa livre que possa contradizer a estrutura.

### `tracking`

Na MM01 fixa somente a fronteira: backend `MLFLOW`, política ainda `PENDENTE_MM06` e `armazenar_historico_runs_no_yaml=false`. Tags, métricas e perfis de run pertencem à MM06.

### `governanca`

Reserva campos para classificação de dados, LGPD, gestor da informação e observações. `PENDENTE` é valor explícito aceitável enquanto a decisão humana ainda não ocorreu; o framework não inventa esses valores.

### `publicacao`

Registra apenas o estado de interface com a governança externa: `NAO_INICIADA`, `CANDIDATA`, `EM_VALIDACAO_EXTERNA`, `PUBLICADA` ou `REJEITADA`. Não replica regras institucionais.

O estado de publicação precisa ser coerente com a fase do ciclo: antes de `CANDIDATO_PRODUTO`, permanece `NAO_INICIADA`; em `CANDIDATO_PRODUTO`, é `CANDIDATA` ou `REJEITADA`; `EM_VALIDACAO_GOVERNANCA` exige `EM_VALIDACAO_EXTERNA` e `handoff_ref`; `PUBLICADO` exige `PUBLICADA` e `produto_dados_ref`. `handoff_ref` e `produto_dados_ref` precisam conter referência auditável material segundo a mesma regra positiva de letras/números.

### `proveniencia`

Registra criação do arquivo e, quando necessário, referências adicionais por alvo. As afirmações materiais também carregam proveniência junto do próprio bloco para permitir validação local.

`APROVADO` exige bloco de aprovação com conteúdo auditável; `MEDIDO` exige medição com referência de execução material. Presença sintática de caracteres invisíveis não satisfaz esses estados.

## 3. IDs e referências

IDs internos usam `snake_case`, começam por letra e possuem de 3 a 64 caracteres. Referências de evidência para fontes precisam resolver para um `fontes[].id` existente. IDs duplicados são inválidos nas coleções controladas, incluindo fontes, evidências, contra-evidências, limiares, componentes do score e experimentos.

`score.calibracao.evidencia_ref` usa especificamente o namespace de `experimentos[].id` e só aceita experimento executado/medido.

Referências auditáveis externas não são IDs de negócio reais neste repositório: fixtures e template usam somente valores sintéticos. A regra de materialidade impede valores visualmente vazios; ela não concede acesso nem valida existência no ambiente corporativo.

## 4. Valores pendentes

O contrato prefere `PENDENTE`, lista vazia ou `null` explícito a um valor inventado. “Ainda não executado” é estado válido da especificação; transformar lacuna em número, aprovação ou resultado observado é erro de proveniência.

`PROPOSTO` também é estado válido nas fases de construção. O gate transforma a ausência de aprovação em bloqueio apenas quando a fase exige decisão formal; não obriga a fonte canônica a esconder propostas ainda em análise.

## 5. O que não está definido na MM01

A MM01 não define fingerprint, crawler de catálogo, feature engineering específica, contrato de runs, notebook de estudo, README do micromodelo, handoff de publicação real, visual ou migração. Esses temas permanecem nas sprints posteriores do Plano Mestre.

## Autoridade única de materialidade textual Unicode

Campos materiais — referências auditáveis, proveniência material, nomes operacionais, semânticas obrigatórias e critérios — são validados pelo formato customizado `material-text`. O `FormatChecker` do JSON Schema não contém uma segunda heurística: ele delega à mesma `_has_material_text` usada pelos gates semânticos. A regra normaliza por NFKC e exige ao menos um caractere cuja categoria Unicode comece por `L` ou `N`.

Consequentemente, whitespace, NBSP/EM SPACE, `Cf`, zero-width, variation selectors, combining marks isolados, pontuação e símbolos isolados não satisfazem um campo material. CJK, Devanagari, caracteres acentuados, algarismos Unicode e combining marks acompanhados de uma base material continuam válidos. Campos narrativos livres não recebem `material-text` apenas por serem strings.

A mesma autoridade cobre também os campos normativos que satisfazem gates de evidência e validação: `evidencias[].regra`, `contra_evidencias[].regra`, `experimentos[].hipotese`, `experimentos[].resultado`, `validacao.resultado.resumo` e, quando a condição não é `ATIVO`, `identidade.estado.motivo_condicao`. Resultado `EXECUTADO` e motivo operacional não possuem uma heurística paralela por `.strip()`; ambos usam `_has_material_text`.

### Classificação explícita dos textos obrigatórios

A quinta A1 mostrou que a distinção entre texto material e narrativa livre precisava ser explícita. Após a sétima A1, a classificação ficou fail-closed: todo nó que aceite instância `string` (inclusive `type` em array) e use `minLength` deve usar `format: material-text`. Regex não substitui materialidade. `pattern` permanece somente em contratos estritamente estruturais e é congelado por path + expressão exata (`$defs.id`, `identidade.nome` e `micromodel_version`). A autoridade de materialidade é exclusivamente `_has_material_text` após NFKC; não há regex genérica, `.strip()` ou segundo predicado concorrente.

Além dos campos já protegidos anteriormente, usam `material-text`: `identidade.titulo`; todos os valores textuais requeridos de `negocio`; todos os valores textuais requeridos de `entidade`; `fontes[].catalogo_ref`; `evidencias[].descricao`; `contra_evidencias[].descricao`; `classificacao.limiares[].descricao`; `classificacao.limiares[].unidade`; `score.componentes[].descricao`; `score.calibracao.metodo`; `governanca.classificacao_dados`; `governanca.lgpd`; e `governanca.gestor_informacao`.

Identificadores internos, `identidade.nome` e `identidade.micromodel_version` permanecem fechados por `pattern`. `fontes[].catalogo_ref` permanece adicionalmente sujeito ao gate semântico `CATALOGO_PRODUTO`.

`governanca.observacoes[]` é a exceção narrativa explícita: é opcional, não satisfaz gate material e não substitui campo normativo. Por isso não recebe `material-text` apenas por ser string.


### Hardening após a sexta A1

A sexta A1 encontrou três ocorrências residuais de `pattern: ".*\\S.*"` nos campos materiais `proveniencia.origem`, `proveniencia.aprovacao.por` e `validacao.aprovacao_humana.por`, além de um guard que tratava qualquer `pattern` como suficiente. Esses caminhos foram removidos. A regressão permanente agora exige `material-text` para `string + minLength`, rejeita explicitamente um pattern textual genérico sintético e compara todos os patterns existentes com uma allowlist estrutural exata. `governanca.observacoes[]` continua narrativa opcional e sem função de gate.
