# Certificadores congelados e rotas atuais

Reconciliação documental de 07/10/2026. Baseline examinada:
`2c5975c0718ef9e30ec3fc26998338036262e87c`. Esta página separa o uso histórico
de MM01 v1 e SER pré-promoção das verificações da árvore corrente. Não cria
certificação substituta, não altera policy e não reclassifica FAIL como PASS.

## MM01 v1: plano histórico, diagnóstico atual

O [contrato original](../sprints/micromodelos/MM01/LOCAL_CERTIFICATION_V1.md)
pertence à candidata `micromodelos/mm01-contrato-canonico`. Seus nove pins de
workflow e suas receitas são congelados. A ferramenta
[mm01_local_certify.py](../../tools/mm01_local_certify.py) continua fail-closed;
`--describe` descreve esse plano, não os gates vigentes de `main`.

Linhagem verificada com os blobs Git, sem recalcular pins:

| Marco | SHA | Compatibilidade dos workflows com v1 |
|---|---|---|
| Introdução dos pins, 22/09/2026 | `b9bfec9912ea79781eb6e355c881c2f3185acc4d` | nove identidades correspondentes |
| Última correção histórica do executor, 23/09/2026 | `34681090ae471e0424aeb9a86e3b741e3561dac5` | nove identidades correspondentes |
| Base anterior às três frentes | `2f5a0cb94f82b78324f6a79d70af7d03e7b57040` | um workflow divergente |
| Entrega IA | `126a2e125cca2251527f187a58696243414c6859` | um workflow divergente |
| Baseline desta reconciliação | `2c5975c0718ef9e30ec3fc26998338036262e87c` | nove workflows divergentes |

Compatibilidade de blobs não prova execução nem certificação dos marcos antigos.
A divergência já existia antes da reorganização; não demonstra falha de cálculo
MM01. O self-test original permanece intacto e continua falhando no corpus
incompatível. Nenhuma suíte é apagada ou convertida em skip/expectedFailure.

Da raiz de um checkout completo, o diagnóstico não exige runtime Node/Databricks,
não instala dependências, não executa o plano e não grava bundle:

```sh
python -B tools/mm01_local_certify.py --diagnose
```

A saída JSON registra horário, HEAD/tree, limpeza da worktree, origem dos pins,
blobs observados, snippets ausentes e todos os workflows incompatíveis. Exit 1
com `INCOMPATIBLE_WITH_FROZEN_V1` bloqueia reutilizar v1. Exit 0 com
`FROZEN_INPUTS_MATCH` prova somente os inputs inspecionados: nos dois casos
`certification_status=NOT_RUN`. Os hashes observam os arquivos da worktree; se
ela estiver alterada, não os atribua automaticamente ao blob de HEAD.

Para regressão local da implementação MM01 atual, use as suítes e owners
correntes, com o ambiente já preparado:

```sh
python -B -m unittest tools.tests.test_micromodelo_mm01 tools.tests.test_micromodelo_mm01_r02 tools.tests.test_micromodelo_mm01_r03 -v
python -B tools/validate_assistant.py
python -B tools/ci_workflows.py --check
```

O [agregado e o CI por ambiente](saida-gerada.md#ci-por-ambiente) têm escopo
próprio. Esses comandos não equivalem a MM01 Local Certification v1. Uma futura
certificação da árvore corrente requer versão nova deliberada: comparar cada
gate original com seu sucessor, manter ambientes/dependências/condições/artefatos,
registrar equivalência e divergências, acrescentar negativos e obter revisão e
aceite aplicáveis. Não trocar pins nem reinterpretar a campanha encerrada para
produzir verde. O diagnóstico resolve a escolha de rota; nova certificação da
release não foi executada nem aprovada por esta correção.

## SER: pré-promoção preservada, invariantes atuais separados

O [certifier SER-CERT-1](../../tools/skill_enforcement/ser_certify.py) verifica
pré-promoção L2. A policy observada na baseline já está em L3. O caso original
`SerCertifierTests.test_current_tree_route_is_coherent_pre_promotion` permanece
com resultado **FAIL / PRE_PROMOTION_CURRENT_LEVEL_MUST_BE_L2**, reproduzido
na base IA e na baseline desta reconciliação. Esse fato impede declarar PASS
para descoberta irrestrita, ainda que outros gates passem.

A linhagem está no [registry de cobertura B0](../../tools/skill_enforcement/parallel/coverage_registry.json):
`HISTORICAL_TEMPORAL`, origem `fcec3e34898006081b3e9063c627b5783108687f` e sucessor
`PromotionCertifierTests.test_current_tree_is_promotion_ready`. O sucessor
pertence ao [SER-PROMOTION-CERT-2](../../tools/skill_enforcement/ser_promotion_certify.py),
perfil `ser01-object-validation-post-promotion`, com classificação estreita de
falhas temporais e invariantes L3. Não é permissão para promover outra superfície.

Reprodução separada, preservando o retorno não zero do primeiro comando:

```sh
python -B -m unittest tools.tests.test_ser_certify.SerCertifierTests.test_current_tree_route_is_coherent_pre_promotion -v
python -B -m unittest tools.tests.test_ser_promotion_certify -v
```

Registre cada comando, SHA, versão Python, exit code e diagnóstico. Não ignore
uma falha diferente, erro de infraestrutura ou falha nova chamando-a de
histórica. Os testes do certifier pós-promoção não executam uma nova campanha
FULL e não autenticam aceite humano. O procedimento operacional por superfície
continua no [owner SER](../sprints/skill_enforcement_rollout/README.md).

O [fingerprint B0](fingerprint-core.md#b0-contrato-e-execução-separados) possui
runtime e comandos próprios. Preserve policy, testes temporais, registry e
snapshots originais. Observação local, inventário, certificação de campanha,
CI remoto, autorização de promoção e homologação do destino são provas distintas.
