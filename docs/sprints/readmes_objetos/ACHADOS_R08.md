# Achados R08 — clusters, anomalias e explicabilidade

A R08 é documental. Os itens abaixo descrevem o comportamento observado; **não são correções funcionais implementadas nesta sprint**.

1. `autoencoder_anomaly` padroniza internamente treino/teste; o notebook também padroniza antes da chamada, tornando a etapa externa redundante para a API atual.
2. O threshold do autoencoder é percentil do erro do treino, não prevalência nem probabilidade de anomalia.
3. O early stopping do autoencoder observa loss de treino, sem conjunto de validação separado.
4. `cluster_profiling.z_score` é diferença de média dividida pelo desvio global; não é z-test nem significância.
5. `cluster_profiling.index` fica instável/difícil de interpretar com média global perto de zero ou negativa.
6. O output histórico do notebook de profiling é abreviado embora a célula imprima todas as linhas.
7. Em `clustering_suite`, `method="both"` e `method="silhouette"` recomendam o mesmo `best_k`; não há votação entre métricas.
8. O modo `elbow` usa uma segunda diferença de inércia; é heurística e o texto impresso ainda usa o rótulo “Melhor silhouette”.
9. DBSCAN tem `eps=0.5` e `min_samples=5` fixos na implementação e a fachada não os expõe.
10. `clustering_suite` importa `mlflow` no topo, mesmo com `log_mlflow=False`.
11. O bloco histórico do notebook de clustering mostra a tabela de `scores`, mas a célula imprime o dict completo.
12. `generate_executive_report` usa as cinco primeiras linhas recebidas; não ordena `shap_importance`.
13. A direção executiva é sinal de correlação global feature × SHAP; correlação finita exatamente zero cai no texto de associação negativa.
14. O resumo técnico exige `tabulate`; com comparação nativa, também pressupõe coluna `rank` nos dois DataFrames. O notebook atual não fornece esses ranks.
15. Cortes 15/8% e Spearman 0,7/0,5 no relatório são heurísticas locais, não padrões SHAP/estatísticos.
16. Em `shap_explainer`, `max_samples` limita somente KernelSHAP; Tree/Linear usam todo `X` fornecido.
17. KernelSHAP usa as primeiras até 100 linhas da amostra como background e, se amostrar, devolve explicações apenas para a amostra.
18. `get_feature_importance_shap` normaliza antes de aplicar `top_n`; o cumulativo da tabela truncada pode terminar abaixo de 100%.
19. O `base_value` SHAP depende do espaço de output; não é genericamente prevalência/probabilidade.
20. `plot_shap_global` só trata `beeswarm`/`bar` explicitamente; `plot_shap_local` é mais seguro com NumPy porque usa `X[idx]`.
21. `plot_umap_clusters` recomputa UMAP com defaults fixos; não expõe `n_neighbors`, `min_dist` ou `n_components`.
22. `cluster_names` do UMAP presume labels `0..N-1`; labels arbitrários/`-1` podem virar ausentes.
23. O argumento `n` do rodapé UMAP é apenas apresentação e não é validado contra a base.
24. `umap_viz` usa `TEMA_BASE`/constantes legadas e ainda não consome a rota V04 `_resolvido`.
25. A geometria UMAP depende dos hiperparâmetros; o desenho não prova a existência de clusters nem preserva distância global de forma métrica.
