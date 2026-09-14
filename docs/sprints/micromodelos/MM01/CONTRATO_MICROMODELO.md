# Contrato `micromodelo.yaml` — schema 1.0.0

## 1. Papel do arquivo

`micromodelo.yaml` é a especificação estruturada canônica do micromodelo. Ele registra **o que o micromodelo significa e como deve ser avaliado**, não o histórico crescente das execuções. README, notebook, catálogo e handoffs futuros devem ser derivados ou confrontados com esse contrato.

O arquivo real de cada micromodelo pertence ao ambiente corporativo autorizado. Este repositório contém apenas o contrato, o template e fixtures sintéticos.

## 2. Grupos obrigatórios

### `schema_version`

Versão do formato estrutural. Na MM01 o único valor aceito é `1.0.0`. Mudança incompatível do contrato exige nova versão do schema; não se altera silenciosamente a interpretação de um arquivo antigo.

### `identidade`

Contém `nome`, `titulo`, `micromodel_version` e `estado`. `micromodel_version` identifica a evolução humana do micromodelo; não substitui o `spec_fingerprint` que será criado na MM02.

### `negocio`

Explicita a característica, o objetivo, a definição operacional, os usos pretendidos e os usos proibidos. A definição deve ser observável e auditável; rótulo de negócio sem critério operacional não é suficiente.

### `entidade`

Declara entidade, chave lógica, granularidade, população elegível e referência temporal. A chave é lógica/informacional; o contrato não concede permissão nem cria constraints no ambiente.

### `fontes`

Cada fonte recebe `id`, `catalogo_ref`, `schema`, `objeto`, tipo, campos, papel e proveniência. O binding padrão permitido é `CATALOGO_PRODUTO`, que representa simbolicamente o catálogo oficial configurado no workspace. O validador reprova outra referência por padrão.

O nome real do catálogo não é versionado no Git e o contrato não concede acesso à fonte.

### `evidencias` e `contra_evidencias`

Regras favoráveis e desfavoráveis são registradas separadamente. Cada item referencia fontes conhecidas, descreve a regra e carrega proveniência. Em `EM_VALIDACAO` ou fase posterior, a regra precisa estar `APROVADO`.

Contra-evidência é parte obrigatória do desenho do domínio mesmo quando a lista ainda está vazia durante a ideia inicial. Vazio significa “ainda não especificado”, não “provado que não existe contra-evidência”.

### `classificacao`

O tipo inicial é `BOOLEANO_COM_INDETERMINADO`. O contrato exige três definições diferentes:

- `quando_true`: quando há base suficiente para afirmar a característica;
- `quando_false`: quando há base suficiente para negar a característica;
- `quando_indeterminado`: quando a informação não permite concluir nem TRUE nem FALSE.

A política de ausência de evidência só aceita `INDETERMINADO` ou `REGRA_EXPLICITA_APROVADA`. Limiares materiais têm operador, valor, unidade e proveniência `APROVADO`.

### `score`

Score pode ser habilitado ou desabilitado. Quando habilitado, exige:

- `tipo_semantica`: `FORCA_EVIDENCIA`, `PROBABILIDADE_CALIBRADA` ou `OUTRA_APROVADA`;
- descrição da semântica;
- escala 0–100;
- regra de normalização;
- componentes/pesos, quando existirem;
- proveniência da decisão de score.

Peso material exige `APROVADO`. `PROBABILIDADE_CALIBRADA` exige calibração com proveniência `MEDIDO` e referência de execução. Portanto, “score 80” não pode ser descrito como “80% de probabilidade” apenas por estar na escala 0–100.

Quando score está desabilitado, semântica, escala, normalização, componentes, calibração e campo de score na saída devem permanecer vazios/nulos.

### `experimentos`

Registra hipóteses relevantes da especificação. Um experimento `EXECUTADO` exige resultado e proveniência `MEDIDO`. O identificador da execução é referência externa; o YAML não incorpora o histórico das runs.

### `validacao`

Separa resultado técnico medido da aprovação humana. `APROVADO` exige ambos:

1. resultado com proveniência `MEDIDO`;
2. `aprovacao_humana.status=APROVADO`, com responsável, timestamp e referência.

Fase `VALIDADO` ou posterior não é aceita se esse gate não estiver satisfeito.

### `saida`

Possui dois contratos distintos.

`saida.estudo` preserva `TRUE`, `FALSE` e `INDETERMINADO`, além do score quando habilitado.

`saida.publicacao` começa `PENDENTE`. A partir de `CANDIDATO_PRODUTO`, precisa estar `DEFINIDO`, com campo final `BOOLEAN` e uma política aprovada para `INDETERMINADO`: excluir do universo publicado, usar campo de cobertura separado ou outra solução explicitamente aprovada. O contrato não fornece a opção “mapear indeterminado para FALSE”.

### `tracking`

Na MM01 fixa somente a fronteira: backend `MLFLOW`, política ainda `PENDENTE_MM06` e `armazenar_historico_runs_no_yaml=false`. Tags, métricas e perfis de run pertencem à MM06.

### `governanca`

Reserva campos para classificação de dados, LGPD, gestor da informação e observações. `PENDENTE` é valor explícito aceitável enquanto a decisão humana ainda não ocorreu; o framework não inventa esses valores.

### `publicacao`

Registra apenas o estado de interface com a governança externa: `NAO_INICIADA`, `CANDIDATA`, `EM_VALIDACAO_EXTERNA`, `PUBLICADA` ou `REJEITADA`. Não replica regras institucionais. `EM_VALIDACAO_GOVERNANCA` exige `handoff_ref`; `PUBLICADO` exige confirmação externa e `produto_dados_ref`.

### `proveniencia`

Registra criação do arquivo e, quando necessário, referências adicionais por alvo. As afirmações materiais também carregam proveniência junto do próprio bloco para permitir validação local.

## 3. IDs e referências

IDs internos usam `snake_case`, começam por letra e possuem de 3 a 64 caracteres. Referências de evidência para fontes precisam resolver para um `fontes[].id` existente. IDs duplicados dentro da mesma coleção são inválidos.

## 4. Valores pendentes

O contrato prefere `PENDENTE`, lista vazia ou `null` explícito a um valor inventado. “Ainda não executado” é estado válido da especificação; transformar lacuna em número, aprovação ou resultado observado é erro de proveniência.

## 5. O que não está definido na MM01

A MM01 não define fingerprint, crawler de catálogo, feature engineering, cálculo de score específico, contrato de runs, notebook de estudo, README do micromodelo, handoff de publicação, visual ou migração. Esses temas permanecem nas sprints posteriores do Plano Mestre.
