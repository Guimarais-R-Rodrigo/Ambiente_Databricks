# Observações históricas preservadas em 2026

Este arquivo preserva contexto retirado da carga universal na migração de
2026-10-06. **Não descreve o estado atual da máquina, conta ou produto.** Os
relatos foram lidos na baseline `f2843eafae84d44cd751f307101de84f11981bd7`; resultados
originais continuam nos arquivos/commits citados. Não são novos testes, promessas
de disponibilidade nem autorização para repetir efeitos. Consulte os
[owners vivos](projeto.md#owners-vivos) e [pré-condições](ambientes.md#confirmacao).

## Runtime Free

Origem: [C07 na baseline](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/f2843eafae84d44cd751f307101de84f11981bd7/.claude/rules/free-vs-trabalho.md#L15-L86).
A matriz partiu de Spark 4.1 serverless em 2026-08-13, com acréscimos datados.

| Assunto | Relato preservado | Limite da evidência |
|---|---|---|
| `cache()`/`persist()` | Free recusou com `NOT_SUPPORTED_WITH_SERVERLESS`; helpers foram ajustados para degradar sem cache | compute clássico era citado como alternativa; confirmar hoje |
| `spark.conf.get` de config de cluster | bloqueado no Free | disponibilidade no trabalho não foi demonstrada pela frase “normalmente disponível” |
| `spark` global dentro de módulo importado | descrito como inexistente em ambos os ambientes | passar contexto explicitamente e conferir implementação/teste atual |
| `pyspark.ml` clássico | `VectorAssembler`/`Correlation.corr` bloqueados no caso Spark Connect/JVM | a comparação com compute clássico não homologa destino corporativo |
| pandas | `tabulate` ausente para `to_markdown()` e `jinja2` ausente para `style` | inventário daquela sessão, não garantia sobre imagens futuras |
| MLflow implícito | em 17/08, `MlflowClient` tentou ler `spark.mlflow.modelRegistryUri` e Spark Connect recusou; repetido em 29/09 | caminho implícito específico |
| MLflow explícito | em 29/09, `mlflow.set_registry_uri("databricks")` e nome absoluto de experimento na home permitiram três runs MM06 sintéticas completas | não prova outra versão nem chamada implícita |

O [resultado de 14/08](../../testes/spark/resultados/2026-08-14_catboost_mlflow.json)
registrou `mlflow_run.completo` como “run completo aceito”; a falha em 17/08 não
apaga aquele PASS datado. Em 17/08 `prophet`, antes sem combinação funcional
conhecida por backend de inferência, instalou e ajustou modelo completo. Na mesma
revisão, o aviso anterior sobre instalação sem pin derrubar kernel não se
reproduziu. Esses contrastes motivam reteste antes da replicação, não versões de
história “corrigidas” retroativamente.

## Bibliotecas

Relato de **2026-08-17**: as doze opcionais LightGBM, XGBoost, CatBoost, Optuna,
PyTorch, SHAP, UMAP, lifelines, Prophet, pmdarima, TabNet e tabulate, ausentes da
imagem observada, foram instaladas por `%pip` e exercitadas com chamada real.
O registro dizia `%pip install` na primeira célula seguido de `%restart_python`,
com 200 a 280 segundos de job. Pins históricos: `shap==0.44.1`,
`umap-learn==0.5.5` e `pmdarima==2.0.4` junto de `numpy==1.23.5`; as outras nove
resolveram sem pin naquela rodada. Instalar as três da lista na mesma sessão
quebrou `import numpy`; isoladas funcionaram. A orientação da rodada era uma
biblioteca por notebook.

São dados históricos, não receita atual de instalação nem permissão para
instalar. O [inventário de opcionais](../../../ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt)
e os resultados da sessão nova precisam ser confrontados com runtime e política.

## Quotas e publicacao

- **13/08/2026:** o contexto Free registrou remoção solicitada da camada global
  `global-*` e do ambiente anterior. Backup estava no material da sessão antiga;
  origem da camada global era o repositório do Hub. Referência a republicação
  pelo engine do Hub descrevia aquela camada externa, não o publicador deste
  projeto. Se `global-*` reaparecer, preserve e coordene targets, sem sobrescrever.
- **18/08/2026:** o chat mostrou “Budget reached” e reset em 01/09, descrito como
  quatorze dias bloqueado. A mesma rodada mediu compute com job de RUNNING a
  SUCCESS e workspace com mkdirs/delete/export exit 0. Forward tests por chat
  estavam bloqueados; arquivo/compute continuavam possíveis na conta testada.
  Esses comandos são relato de medição, não instruções para repeti-los.
- **29/08/2026:** o contexto registrou commit `02a5ad3` publicado e conferido:
  315 arquivos, nenhum ausente/obsoleto; smoke pós-correção aprovado em Spark
  4.2.0; chat ainda indicado como bloqueado até 01/09. A própria origem exigia
  revalidar a cota após a janela, sem inferir sucesso pelo calendário.

Fontes: [C10](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/f2843eafae84d44cd751f307101de84f11981bd7/.claude/context/ambiente-free.md#L9-L23)
e [C07](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/f2843eafae84d44cd751f307101de84f11981bd7/.claude/rules/free-vs-trabalho.md#L46-L67).
As negativas gerais de memória/Jobs/serving não são mantidas como estado atual;
veja a [revalidação oficial](../references/databricks-genie-code.md#limites-revalidados).

## Frentes na baseline

Origem: [C02](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/f2843eafae84d44cd751f307101de84f11981bd7/CLAUDE.md#L58-L93).
O antigo bootstrap continha estados de momentos diferentes. Esta seção os
preserva como relato de origem, sem competir com os índices atuais.

- **READMEs R00–R13:** contrato 1.0.0 ratificado em 12/09; migração estrutural
  terminou R11, fechamento após PR #33 (`b0e953cc`) e documental PR #34
  (`99e01012`). Cobertura relatada: 75/75 operacionais, 3/3 exemplares, zero
  pendências; controle `phase=complete`, `pending={}`. Auditoria final A0_light,
  sem publicação/homologação Databricks. [R13](../../sprints/readmes_objetos/RELATORIO_R13.md)
  e [índice](../../sprints/readmes_objetos/README.md) preservam a campanha.
  Objetos posteriores, como `hub_snippets.visual.theme_lab`, entram no mesmo
  contrato; esses números não medem o catálogo atual.
- **Temas:** o bootstrap relatava V00–V09 integradas, V08 alinhando skills,
  padrões, entrada do produto, EDA e Manual às fontes visuais; V09 transportando
  contrato no kit offline com guarda de integridade. PR #45:
  `0f7234c4734f1974ebb1a20123f3c26626c67ef3`; correção Node PR #46:
  `4ae714a35a0aafd930a8cd796d962b0a79449b88`. Isso não descreve o estado mais
  novo do [índice Temas](../../sprints/sistema_temas/README.md), nem prova
  publicação/browser/runtime/acessibilidade/ACL/UAT/promoção visual.
- **Micromodelos MM00:** PR #43 e `36e89515a46df24f41deea4791b109f5a1f938f2`
  integraram ADR-0014–0020. **MM01:** PR #51, head
  `fa1a3653e60472d171307663d1175344bb3f6a8d`, merge
  `73d7659dcf11509a7fba392221c4810d10401c35`; [checkpoint](../../sprints/micromodelos/MM01/POST_MERGE_CHECKPOINT.md).
- **MM02/MM03:** PR #109/#110 (`3214a131`, 23/09) integradas. A FULL R1 MM03
  permaneceu FAIL histórico; FULL R2 e auditoria da candidata corrigida em
  [MM03](../../sprints/micromodelos/MM03/README.md). O núcleo MM03 era
  metadata-only e ainda sem acesso Databricks até aquela candidata.
- **MM04–MM13-LAB:** [relatório E0 sintético](../../sprints/micromodelos/RELATORIO_ENTREGA_LAB.md),
  kit/adapter metadata e MLflow E1 executados no Free via CLI; skill instalada
  na home pessoal; [casos Genie E1 de 29/09](../../sprints/micromodelos/RESULTADOS_GENIE_E1_2026-09-29.md)
  e [briefings P1/P2/P2b/P2c](../../sprints/micromodelos/TESTE_BRIEFINGS_MM04_E1.md)
  com seus vereditos/ressalvas, sem homologação corporativa.

Contexto adicional permanece na [revisão pós-SEF/PSEF/SER](../../sprints/micromodelos/REVISAO_PLANO_POS_SEF_2026-09-23.md),
[retrospectiva MM01](../../sprints/micromodelos/RETROSPECTIVA_MM01.md) e
[protocolo de certificação](../../sprints/micromodelos/PROTOCOLO_CERTIFICACAO_SPRINTS.md).
FAILs antigos e freezes não são apagados quando uma candidata posterior passa.
