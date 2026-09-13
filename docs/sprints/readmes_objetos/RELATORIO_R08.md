# Relatório R08 — clusters, anomalias e explicabilidade

## 1. Objetivo

Entregar os seis READMEs R08 no contrato 1.0.0, corrigir divergências didáticas já existentes e provar que a documentação não alterou as APIs.

## 2. Objetos

`autoencoder_anomaly`, `cluster_profiling`, `clustering_suite`, `explainability_report`, `shap_explainer` e `umap_viz`.

## 3. Cobertura esperada

Após retirar exatamente as seis dispensas R08: **55/75 objetos operacionais + 3/3 exemplares; 20 pendências**. A contagem efetiva vem do validador da árvore fechada.

## 4. Alterações fora dos READMEs

A lista nominal está em `MATRIZ_ALTERACOES_R08.md`. Ela inclui os seis notebooks, Manual canônico/cópia, catálogo, índices, controle de migração, CHANGELOG, CLAUDE, PLANO_HUB e evidências. O simulado é derivado pelo renderer.

## 5. Testes exigidos

- contrato 1.0.0 e ordem das 15 seções;
- validador estrutural e `--conferir-readme`;
- gate geral e regressões V00–V04;
- preservação byte a byte das implementações/fachadas;
- preservação do código executável dos seis notebooks;
- runtime separado para core/scikit-learn, PyTorch, SHAP e UMAP;
- verificação de dependências ocultas/contratos documentados;
- cobertura 55/75 e retirada monotônica de seis dispensas.

## 6. Limites

A R08 não corrige APIs, não migra UMAP para V04, não publica no Databricks, não homologa modelo/segmentação/explicabilidade e não constitui auditoria independente.

## 7. Gate editorial

STATUS_R08: PASS técnico — 10/10 casos do suplemento aprovados (4 estruturais e 6 de runtime), sem skips, no run 34756829497; aguarda aceite editorial humano.

## 8. Fechamento de compatibilidade e evidencias — 2026-09-13

O run anterior 34753403221 passou em core, PyTorch e SHAP, mas falhou no UMAP: a versao 0.5.5 chamou `check_array(force_all_finite=...)` contra scikit-learn sem esse parametro. Este freeze fixa somente no ambiente isolado UMAP `numpy==1.26.4`, `umap-learn==0.5.5` e `scikit-learn==1.4.2`, verifica a assinatura e executa `pip check`. As versoes completas estao nos quatro arquivos `*-pacotes.txt` do artefato do run. Essa combinacao nao e uma homologacao do Databricks nem recomendacao universal de versao.

A coleta agora inclui stdout e stderr e reconhece os resumos singulares e plurais do unittest. A identidade do commit automatizado e explicita. O gate e a preservacao sao repetidos depois de registrar os resultados. As alteracoes desta retomada ficam no workflow temporario, neste relatorio, na rubrica, no changelog e na matriz; implementacoes e dependencias permanentes nao mudam.

Referencia de compatibilidade: https://scikit-learn.org/1.4/modules/generated/sklearn.utils.check_array.html
