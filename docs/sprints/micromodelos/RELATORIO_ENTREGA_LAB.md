# Entrega da candidata de laboratório de micromodelos

**Data:** 2026-09-29. **Base:** `origin/main@4ba7f551767d847381df1556ed937116258fa77d`; MM03/PR #110 já integrada. **Branch:** `micromodelos/autonomia-local-v2`. **Classificação:** `E0_VALIDADO` para o fluxo sintético e as interfaces testadas; `E1_PREPARADO`, `E1_NOT_RUN`; `E2_NAO_EXECUTADO`. A candidata não é `FRAMEWORK_MICROMODELOS_V1` corporativa.

## Entregas por sprint original

| Sprint | Capacidade nesta candidata | E0 | E1 | E2 |
|---|---|---|---|---|
| MM00–MM03 | Contratos MM01, fingerprint MM02 e metadata-only MM03 reutilizados; status vivo de MM03 corrigido. | PASS regressão | NOT_RUN | NOT_RUN |
| MM04–MM05 | Skill `hub-ml-micromodelos` L1, dois briefings, objetivo conhecido e shortlist de oportunidades, spec progressiva MM01, incerteza explícita. | PASS código e contrato | Código/Genie NOT_RUN | NOT_RUN |
| MM06 | Notebook/README de estudo ligados ao fingerprint e helper rule-based com runs DEVELOPMENT/VALIDATION/SCORING. | PASS artefato e MLflow local real | MLflow Free NOT_RUN | NOT_RUN |
| MM07–MM08-LAB | Adapter `information_schema` com capability/status explícitos; kit portátil, setup sintético opcional e roteiro Free. | PASS fake Spark/empacotamento isolado | PREPARADO; adapter real NOT_RUN | NOT_RUN |
| MM09–MM10-LAB | Piloto novo, seis entidades fictícias, evidência, contra-evidência, indeterminado, scoring heurístico e handoff de governança como rascunho. | PASS | Código/Genie NOT_RUN | NOT_RUN |
| MM11-LAB | Integração de temas/monitoramento: não aplicável ao scoring sem interface visual; ponto de integração documentado no plano. | NOT_APPLICABLE | NOT_RUN | NOT_RUN |
| MM12-LAB | Equivalência conservadora com legado fictício, skill de migração não roteável. | PASS ensaio | NOT_RUN | NOT_RUN |
| MM13-LAB | Catálogo derivado do YAML e impacto por fonte declarada. | PASS | NOT_RUN | NOT_RUN |

O piloto E0 encontrou `TRUE=1`, `FALSE=2`, `INDETERMINADO=3`, total `6`; o SHA-256 material MM02 foi `85af625b7ea71babeb00051da089dfc63d4faab2e1f995c4f7a191a2aee79e88`. O score 0–100 expressa força heurística de evidência, não probabilidade ou risco aprovado. As três runs MLflow usam a **mesma fixture**, sem holdout independente; os nomes dos tipos registram etapas operacionais e não demonstram validação estatística.

## Provas reproduzíveis

Ambiente de execução: Windows, Python 3.12.10. A bateria integrada abaixo passou com **186 testes**:

```text
python -B -m unittest tools.tests.test_micromodelo_mm01 tools.tests.test_micromodelo_mm01_r02 tools.tests.test_micromodelo_mm01_r03 tools.tests.test_micromodelo_mm02_fingerprint tools.tests.test_micromodelo_mm03_metadata tools.tests.test_micromodelo_mm04_flow tools.tests.test_micromodelo_mm06_artifacts tools.tests.test_micromodelo_mm06_tracking tools.tests.test_micromodelo_mm07_databricks tools.tests.test_micromodelo_mm09_lab tools.tests.test_micromodelo_mm10_handoff tools.tests.test_micromodelo_mm12_migration_lab tools.tests.test_micromodelo_mm13_catalog tools.tests.test_micromodelo_free_kit -q
```

Regressão policy/entrypoint: `python -B -m unittest tools.tests.test_skill_enforcement_policy_io tools.tests.test_skill_enforcement_se07 tools.tests.test_concierge_integracao tools.tests.test_tool_guards -q`: **111 testes, 1 skip**. `python -B tools/validate_assistant.py --root ambiente_fonte`: **APROVADO, 0 falhas, 1 aviso** para `__pycache__` local. `python -B tools/render_simulado.py --write`: **583 arquivos renderizados** pelo gerador canônico. O primeiro comando integrado tinha um nome de módulo MM01 inexistente e falhou na coleta; foi corrigido para os três módulos MM01 reais e a bateria passou. Nenhuma assertion foi removida.

MLflow 3.16.1 em virtualenv local: `python -B tools/micromodelo_mm06_e0_tracking.py` passou contra backend de arquivos local ignorado pelo Git, com opt-in exigido pela versão instalada. O script consulta as runs gravadas e confere `mm06.complete=true`, fingerprint e agregados. Run IDs da prova: DEVELOPMENT `d23e9b83391244acab257126121cc054`, VALIDATION `19d1f5b84d48463ea64402398b4aabc9`, SCORING `ab5a531213b94d81b97466c9f28cf145`. Esses IDs só têm significado na base E0 local. Testes com fake exercem negativos do wrapper, mas não substituem essa prova real. O pacote transportado foi executado em subprocesso isolado local nos testes; isso não é execução Free.

## Revisão e correções

Implementações principais foram revisadas por agente diferente do autor, com escopo focal MM04, MM06, MM07, MM09, MM10, política e tracking. Correções relevantes: guard de fingerprint/perfil no piloto, precedência de contra-evidência e IDs de evento únicos; reconciliação do score; chaves fechadas de parâmetros MLflow e população zero sem estatísticas de score; adapter com `UNAVAILABLE` honesto; allowlist rígida no kit; handoff com agregado recebido marcado `SUPPLIED_UNVERIFIED` e contrato de saída copiado, sem alias mutável. Isto é revisão cruzada da equipe de implementação, não auditoria externa.

## Transporte e próxima ação

`KIT_FREE.md` descreve importação, setup sintético opcional, execução offline, teste metadata, MLflow opcional, Genie Code e formato de retorno sanitizado. O builder é `python -B tools/micromodelo_free_kit.py --output <diretorio-novo>`. O pacote local gerado é `.artifacts/mm-free-kit-lab-v2-20260929.zip`, com 32 arquivos no manifesto e SHA-256 `23e9f75622f862ff239c60b350c5a3fd5eba4783b0d76602eeec280632765a51`. `RUN_FREE.py` foi executado dentro da cópia do pacote no Python local: contagens e fingerprint passaram; capability local: `spark=false`, `mlflow=false`. O manifesto e o ZIP ficam fora do Git. O kit não deve conter dados de `Ambiente_Antigo/`, arquivos `.env` ou objetos corporativos. Preencha `RESULTADOS_FREE.md` **somente após** execução do usuário no Free. Até lá, código Databricks/Genie permanece `NOT_RUN`.

Decisões E2 pendentes: dono e gestor, permissões/catálogo, população e grão, limiares, retenção dos resultados individuais, LGPD, auditoria/custo e autoridade de publicação. O handoff MM10 é `DRAFT_NOT_SUBMITTED`, seu agregado é `SUPPLIED_UNVERIFIED`, e `published=false`. Ensaio E2 e rollback estão em `KIT_FREE.md`; nenhum acesso corporativo foi realizado.
