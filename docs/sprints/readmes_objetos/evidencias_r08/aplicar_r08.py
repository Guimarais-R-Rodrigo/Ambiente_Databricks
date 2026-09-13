"""Aplica a integração editorial/transversal da R08.

Não altera implementações nem fachadas. Todas as mutações dependem de âncora única.
O simulado é gerado depois, exclusivamente por tools/render_simulado.py.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OBJECTS = [
    "autoencoder_anomaly",
    "cluster_profiling",
    "clustering_suite",
    "explainability_report",
    "shap_explainer",
    "umap_viz",
]


def replace_once(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    assert count == 1, (path, count, old[:180])
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before_once(path: str, marker: str, block: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    assert text.count(marker) == 1, (path, text.count(marker), marker[:180])
    p.write_text(text.replace(marker, block.rstrip() + "\n\n" + marker, 1), encoding="utf-8")


def append_once(path: str, heading: str, block: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    assert heading not in text, (path, heading)
    p.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def add_backlinks() -> None:
    for obj in OBJECTS:
        path = f"ambiente_fonte/.assistant/hub_snippets/ml/{obj}/exemplo_{obj}.py"
        p = ROOT / path
        text = p.read_text(encoding="utf-8")
        marker = "\n# COMMAND ----------"
        assert marker in text and "Guia local completo:" not in text, obj
        intro = "\n# MAGIC\n# MAGIC **Guia local completo:** [README deste objeto](README.md)."
        p.write_text(text.replace(marker, intro + marker, 1), encoding="utf-8")


def edit_notebooks() -> None:
    path = "ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/exemplo_autoencoder_anomaly.py"
    replace_once(
        path,
        '# MAGIC **E repare no limiar:** `threshold_percentile=95` marca 5% do *treino* por\n# MAGIC construção, e no teste marcou 8,1%. O número de marcados é decidido pelo\n# MAGIC percentil que você escolheu, **não** pela quantidade de anomalias que\n# MAGIC existe. Aumentar para 99 marcaria menos e acharia menos; o método não sabe\n# MAGIC quantas anomalias há.',
        '# MAGIC **E repare no limiar:** `threshold_percentile=95` deixa aproximadamente 5% dos\n# MAGIC **erros do treino** acima do corte por construção, e no teste marcou 8,1%.\n# MAGIC Isso não estima a prevalência real de anomalias. Mudar o percentil muda o\n# MAGIC ponto de operação e precisa ser validado contra custo, cobertura e revisão.',
    )
    replace_once(
        path,
        '# MAGIC - **Sem padronizar.** O erro fica dominado pela variável de maior escala, e a anomalia vira "quem tem valor alto".\n# MAGIC - **Em base pequena.** Rede neural com poucos milhares de linhas decora; Isolation Forest resolve melhor e mais barato.',
        '# MAGIC - **Sem uma convenção consistente de escala.** Este notebook padroniza externamente, mas o helper também padroniza internamente a partir do treino recebido. A etapa externa é redundante para esta API; em produção, versione o pipeline para treino e inferência usarem a mesma convenção.\n# MAGIC - **Em base pequena sem validação suficiente.** Uma rede pode sobreajustar e custar mais; compare com métodos mais simples, como Isolation Forest, em vez de presumir superioridade de qualquer um.',
    )

    path = "ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/exemplo_cluster_profiling.py"
    replace_once(
        path,
        "# MAGIC Executado no laboratório, o resultado é:",
        "# MAGIC O bloco histórico abaixo é **abreviado**: a célula imprime todas as combinações cluster × feature, mas aqui foram preservadas apenas seis linhas como amostra visual:",
    )
    replace_once(
        path,
        '# MAGIC **Como ler.** Os clusters 0 e 2 foram construídos **quase idênticos** — de\n# MAGIC propósito. O perfil mostra isso: renda, idade e número de produtos ficam\n# MAGIC próximos entre os dois, e distantes do cluster 1.',
        '# MAGIC **Como ler.** Os clusters 0 e 2 foram construídos **quase idênticos** — de\n# MAGIC propósito. O perfil mostra isso: renda, idade e número de produtos ficam\n# MAGIC próximos entre os dois, e distantes do cluster 1.\n# MAGIC\n# MAGIC O campo `z_score` deste helper é apenas `(média_cluster - média_global) /\n# MAGIC desvio_global`. Ele expressa diferença de média em desvios globais; **não é\n# MAGIC z-test, p-value nem significância estatística**.',
    )
    replace_once(
        path,
        '# MAGIC três variáveis. Para 0 e 2, o "top diferenciador" existe — a função sempre\n# MAGIC devolve um — mas a magnitude é pequena.',
        '# MAGIC três variáveis. Para 0 e 2, ainda existe um ranking entre as features\n# MAGIC disponíveis, mas a magnitude é pequena.',
    )

    path = "ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/exemplo_clustering_suite.py"
    replace_once(
        path,
        '# MAGIC **O problema.** A pergunta "quantos clusters?" não tem resposta no dado. Cotovelo e silhueta são heurísticas que discordam entre si com frequência, e o gráfico do cotovelo quase sempre tem mais de um joelho plausível. Apresentar o k como descoberta esconde que foi escolha.',
        '# MAGIC **O problema.** A pergunta "quantos clusters?" não tem resposta única garantida por uma única métrica. Cotovelo e silhueta são heurísticas e podem apontar escolhas diferentes. Apresentar o `k` recomendado como descoberta automática esconde os critérios usados.',
    )
    replace_once(
        path,
        "# MAGIC Executado no laboratório, o resultado é:",
        '# MAGIC A tabela histórica abaixo corresponde a `resultado_k["scores"]`, com `best_k` mostrado separadamente. A chamada `select_k` devolve um **dict**, portanto o `print(resultado_k)` literal da célula tem outra representação textual:',
    )
    replace_once(
        path,
        '# MAGIC **Como ler.** A padronização não é detalhe: k-means mede distância\n# MAGIC euclidiana, e uma variável em reais domina outra em anos por três ordens de\n# MAGIC grandeza. Sem escalonar, o "cluster" acaba sendo a variável de maior\n# MAGIC amplitude, e nada no resultado avisa.',
        '# MAGIC **Como ler.** A escala é parte do problema: K-Means usa distância euclidiana.\n# MAGIC O `run_clustering_pipeline` aplica `standard` ou `robust` internamente; já\n# MAGIC `select_k` isolado pressupõe `X_scaled` na assinatura. Se você o chamar\n# MAGIC diretamente, é sua responsabilidade preparar uma escala coerente.',
    )

    path = "ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/exemplo_explainability_report.py"
    replace_once(
        path,
        '# MAGIC O que falta   : instalar `tabulate` na sessão (%pip install tabulate),\n# MAGIC                 ou trocar `to_markdown()` por formatação própria —\n# MAGIC                 etapa 2, porque muda a saída.',
        '# MAGIC Primeiro bloqueio: instalar `tabulate` na sessão (%pip install tabulate).\n# MAGIC Segundo bloqueio: a comparação nativa atual também espera uma coluna `rank`\n# MAGIC em **ambos** os DataFrames; esta fixture não a fornece. Instalar `tabulate`\n# MAGIC sozinho, portanto, não faz a célula concluir.',
    )
    replace_once(
        path,
        '# MAGIC defeito — as duas medem coisas diferentes. Importância nativa de árvore\n# MAGIC conta quantas vezes a variável foi usada para dividir; SHAP mede\n# MAGIC contribuição para a previsão de cada linha.',
        '# MAGIC defeito — as duas podem medir quantidades diferentes. A definição de\n# MAGIC importância nativa depende do estimador/configuração (por exemplo, ganho,\n# MAGIC redução de impureza ou contagem de splits); SHAP atribui contribuição no\n# MAGIC espaço de saída explicado pelo modelo.',
    )
    replace_once(
        path,
        '# MAGIC O que a discordância indica é **correlação entre features**: quando duas\n# MAGIC variáveis carregam a mesma informação, cada método distribui o crédito de\n# MAGIC um jeito. É sinal para investigar, não para escolher a ordenação que\n# MAGIC agrada.',
        '# MAGIC Correlação entre features **pode** contribuir para a discordância, mas não\n# MAGIC é a única causa: definições de importância, amostra e propriedades do modelo\n# MAGIC também importam. Discordância é sinal para investigar, não para escolher a\n# MAGIC ordenação que agrada.',
    )

    path = "ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/exemplo_shap_explainer.py"
    replace_once(
        path,
        '# MAGIC **O problema.** Importância de variável de árvore responde "quantas vezes o modelo usou isso", que não é o que o negócio pergunta. E não responde de jeito nenhum a pergunta que chega do atendimento: *por que este cliente foi recusado?*',
        '# MAGIC **O problema.** Importância nativa de árvore resume o modelo por uma definição que varia com o estimador/configuração e não substitui uma atribuição por observação. Já uma pergunta individual como *por que esta previsão mudou?* exige declarar também qual output/classe está sendo explicado.',
    )
    replace_once(
        path,
        '# MAGIC explicação recuperou o que plantamos, o que é a única forma de verificar\n# MAGIC um método de explicabilidade.',
        '# MAGIC ordenação ficou coerente com o sinal plantado nesta fixture. Isso é um\n# MAGIC **sanity check**, não prova geral de correção ou estabilidade do método.',
    )
    replace_once(
        path,
        '# MAGIC A leitura prática: **importância pequena e não nula é a assinatura de\n# MAGIC "não tem sinal"**, e a linha de corte é sua, não do método. Quem ordena a\n# MAGIC tabela e pega o top-10 sempre acha dez variáveis importantes, inclusive\n# MAGIC numa base de puro ruído.',
        '# MAGIC A leitura prática é mais cautelosa: importância pequena e não nula pode\n# MAGIC surgir por ajuste amostral, dependência entre features ou uso residual pelo\n# MAGIC modelo. Não existe neste helper um cutoff universal que transforme valor\n# MAGIC pequeno em "sem sinal".',
    )
    replace_once(
        path,
        '# MAGIC O `valor base` de **0,3168** é a previsão média — igual à prevalência,\n# MAGIC como se espera. Todo valor SHAP é uma partida desse ponto.',
        '# MAGIC Nesta fixture o `valor base` de **0,3168** ficou próximo da prevalência.\n# MAGIC Em geral ele é o valor esperado do **output explicado** pelo explainer, cuja\n# MAGIC escala depende do modelo/configuração e não deve ser chamada genericamente\n# MAGIC de probabilidade ou prevalência.',
    )

    path = "ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/exemplo_umap_viz.py"
    replace_once(
        path,
        '# MAGIC **O problema.** Cluster em espaço de 30 variáveis não se enxerga, e PCA achata a estrutura local: dois grupos vizinhos mas separados viram uma mancha só. Sem ver, a discussão sobre segmentação vira opinião.',
        '# MAGIC **O problema.** Cluster em espaço de muitas variáveis não se enxerga diretamente. PCA oferece uma projeção linear; UMAP oferece outra visão, não linear, focada em vizinhanças. Nenhuma projeção prova sozinha que a segmentação é real.',
    )
    replace_once(
        path,
        '# MAGIC O uso legítimo é responder "existem grupos distintos aqui?" — e para isso\n# MAGIC ele é excelente. O uso ilegítimo, e frequente, é medir no gráfico e\n# MAGIC concluir que "o segmento A está mais próximo do B do que do C".',
        '# MAGIC O uso seguro é **exploratório**: observar se os labels parecem misturados,\n# MAGIC isolados ou sensíveis à projeção e então voltar ao espaço original para\n# MAGIC validar. O desenho sozinho não responde "existem clusters reais aqui?" nem\n# MAGIC sustenta medir que A está mais próximo de B do que de C.',
    )
    replace_once(
        path,
        '# MAGIC - **Como método de clusterização.** Ele projeta; quem agrupa é o k-means ou o HDBSCAN. Rodar cluster *sobre* a projeção inventa separação.\n# MAGIC - **Sem padronizar antes.** Variável em reais domina variável em anos, e a projeção vira um gráfico de renda.\n# MAGIC - **Sem `random_state`.** Duas execuções produzem desenhos diferentes, e a reunião seguinte discute o desenho.',
        '# MAGIC - **Como prova de clusterização.** UMAP projeta. Clustering sobre embedding pode existir em pipelines específicos, mas muda a geometria e precisa de validação própria.\n# MAGIC - **Sem revisar escala/métrica.** Variáveis em unidades muito diferentes podem dominar a noção de vizinhança.\n# MAGIC - **Confundindo uma semente com estabilidade.** Este helper fixa `random_state=42`; isso melhora repetibilidade da execução, mas uma única configuração não demonstra robustez da estrutura.',
    )


def edit_shared_docs() -> None:
    block = """#### 📘 Guias locais R08 — clusters, anomalias e explicabilidade

A R08 separa quatro tarefas que costumam ser misturadas: **criar clusters**, **descrevê-los**, **projetá-los para visualização** e **explicar modelos/pontuar anomalias**:

- [Autoencoder de anomalias](ml/autoencoder_anomaly/README.md) — erro de reconstrução treinado sobre referência normal;
- [Profiling de clusters](ml/cluster_profiling/README.md) — médias, razões e diferenças descritivas por grupo;
- [Suite de clustering](ml/clustering_suite/README.md) — K-Means/GMM/DBSCAN e métricas internas;
- [Relatório de explicabilidade](ml/explainability_report/README.md) — camada Markdown executiva/técnica;
- [SHAP explainer](ml/shap_explainer/README.md) — atribuições, ranking e plots;
- [UMAP](ml/umap_viz/README.md) — projeção exploratória 2D.

Métrica interna, ranking, embedding e SHAP são evidências diferentes. Nenhum desses objetos cria causalidade, persona, política ou homologação por conta própria."""
    insert_before_once(
        "ambiente_fonte/.assistant/hub_snippets/README.md",
        "#### 📊 Risco de Crédito e Scorecards\n",
        block,
    )

    manual_block = """#### Guias locais R08 — clusterização, anomalias e explicabilidade

Para um usuário novo, escolha primeiro a **pergunta**:

- `hub_snippets/ml/clustering_suite/README.md` — criar/comparar agrupamentos numéricos; `best_k` é heurística;
- `hub_snippets/ml/cluster_profiling/README.md` — descrever grupos já rotulados; `z_score` local não é teste estatístico;
- `hub_snippets/ml/umap_viz/README.md` — visualizar vizinhanças em 2D; a geometria não é medida fiel do espaço original;
- `hub_snippets/ml/autoencoder_anomaly/README.md` — priorizar anomalias por erro de reconstrução; percentil não é probabilidade;
- `hub_snippets/ml/shap_explainer/README.md` — calcular atribuições do output do modelo;
- `hub_snippets/ml/explainability_report/README.md` — transformar importâncias já calculadas em Markdown.

Use as rotas em conjunto somente quando os contratos realmente se encaixarem. A R08 documenta o estado existente; não migra `umap_viz` para a rota V04 de temas e não altera implementações."""
    insert_before_once(
        "ambiente_fonte/.assistant/MANUAL_TECNICO.md",
        "#### `hub_snippets.ml.autoencoder_anomaly`\n",
        manual_block,
    )

    append_once(
        "CLAUDE.md",
        "### Estado da migração de READMEs — R08",
        """### Estado da migração de READMEs — R08
A R07 foi aceita e integrada na `main` pelo PR #25 no commit `b73bbb9`. A R08 documenta seis objetos de clusterização, anomalias e explicabilidade sem alterar implementações/fachadas: `autoencoder_anomaly`, `cluster_profiling`, `clustering_suite`, `explainability_report`, `shap_explainer` e `umap_viz`. Estado: `docs/sprints/readmes_objetos/RELATORIO_R08.md`. Cobertura estrutural não é aceite editorial, homologação de modelo nem publicação Databricks.""",
    )
    append_once(
        "PLANO_HUB.md",
        "### Checkpoint R08 — clusters, anomalias e explicabilidade",
        """### Checkpoint R08 — clusters, anomalias e explicabilidade
Seis objetos `hub_snippets/ml` recebem README local 1.0.0, com correções exclusivamente didáticas nos notebooks e preservação das APIs. A leva deve fechar em 55/75 operacionais e pausar antes da R09 para revisão. Fonte: `docs/sprints/readmes_objetos/RELATORIO_R08.md`.""",
    )
    append_once(
        "docs/sprints/README.md",
        "### READMEs de objeto — R08",
        """### READMEs de objeto — R08
A R07 foi integrada pelo PR #25. A R08 cobre seis objetos de clusterização, anomalias e explicabilidade e preserva implementações/fachadas. Relatório, matriz e achados ficam em `docs/sprints/readmes_objetos/`. A cobertura esperada após validação é 55/75 operacionais + 3/3 exemplares; isso não representa aceite editorial antecipado.""",
    )
    append_once(
        "README.md",
        "### Migração de READMEs — R08",
        """### Migração de READMEs — R08
A candidata R08 acrescenta guias locais para autoencoder de anomalias, profiling/suite de clustering, relatório/SHAP e UMAP. O validador confere a cobertura estrutural; aceite editorial, runtime Databricks e homologação permanecem gates separados.""",
    )

    old = """O contrato vigente é **1.0.0**. A R06 foi aceita e integrada pelo PR nº 20 no commit `289731c`, com CI geral e V00/V01/V02/V03 pós-merge verdes. A R07 documenta `kaplan_meier`, `score_bands`, `scorecard_builder`, `survival_cox`, `vintage_analysis` e `woe_iv_calculator` sem alterar suas implementações/fachadas. A cobertura esperada é **49/75 operacionais e 3/3 exemplares, com 26 pendências**; somente a saída do validador da árvore fechada é fonte de verdade. Isso não significa publicação no workspace nem aceite antecipado dos seis textos.

Consulte o [relatório R07](RELATORIO_R07.md), a [matriz nominal](MATRIZ_ALTERACOES_R07.md) e os [achados](ACHADOS_R07.md). A próxima parada é a revisão desta leva antes da R08."""
    new = """O contrato vigente é **1.0.0**. A R07 foi aceita e integrada pelo PR nº 25 no commit `b73bbb9`, após reconciliação com a V04 e seu checkpoint documental. A R08 documenta `autoencoder_anomaly`, `cluster_profiling`, `clustering_suite`, `explainability_report`, `shap_explainer` e `umap_viz` sem alterar suas implementações/fachadas. A cobertura esperada é **55/75 operacionais e 3/3 exemplares, com 20 pendências**; somente a saída do validador da árvore fechada é fonte de verdade. Isso não significa publicação no workspace nem aceite antecipado dos seis textos.

Consulte o [relatório R08](RELATORIO_R08.md), a [matriz nominal](MATRIZ_ALTERACOES_R08.md) e os [achados](ACHADOS_R08.md). A próxima parada é a revisão desta leva antes da R09."""
    replace_once("docs/sprints/readmes_objetos/README.md", old, new)
    replace_once(
        "docs/sprints/readmes_objetos/README.md",
        "| Ver o que mudou além dos READMEs | [Matriz R07](MATRIZ_ALTERACOES_R07.md) |\n| Conhecer inconsistências observadas | [Achados R07](ACHADOS_R07.md) |\n| Ver o resultado da execução | [Relatório R07](RELATORIO_R07.md) |",
        "| Ver o que mudou além dos READMEs | [Matriz R08](MATRIZ_ALTERACOES_R08.md) |\n| Conhecer inconsistências observadas | [Achados R08](ACHADOS_R08.md) |\n| Ver o resultado da execução | [Relatório R08](RELATORIO_R08.md) |",
    )

    ch = """## 2026-09-12 — R08: READMEs de clusters, anomalias e explicabilidade (ChatGPT)

- Documenta seis objetos no contrato 1.0.0: `autoencoder_anomaly`, `cluster_profiling`, `clustering_suite`, `explainability_report`, `shap_explainer` e `umap_viz`.
- Corrige somente prosa/backlinks dos notebooks: outputs históricos e código executável permanecem preservados.
- Registra limites de percentil de anomalia, métricas internas de clustering, ranking/SHAP, dependências ocultas e geometria UMAP.
- Retira exatamente seis dispensas R08 do controle de migração.
- Sem alteração de implementação/fachada, publicação Databricks, homologação de modelo/segmentação/explicabilidade, auditoria independente ou início da R09."""
    insert_before_once("CHANGELOG.md", "## 2026-09-12 — V04:", ch)


def update_migration() -> None:
    p = ROOT / "docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    exemptions = data["exemptions"]
    removed = []
    for obj in OBJECTS:
        key = f"hub_snippets/ml/{obj}"
        assert key in exemptions, key
        meta = exemptions[key]
        assert meta["status"] == "pending" and meta["sprint"] == "R08" and meta["lote"] == "A", (key, meta)
        removed.append(key)
        del exemptions[key]
    assert len(removed) == 6
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_sprint_docs() -> None:
    findings = """# Achados R08 — clusters, anomalias e explicabilidade

A R08 é documental. Os itens abaixo descrevem o comportamento observado; **não são correções funcionais implementadas nesta sprint**.

1. `autoencoder_anomaly` padroniza internamente treino/teste; o notebook também padroniza antes da chamada, tornando a etapa externa redundante para a API atual.
2. O threshold do autoencoder é percentil do erro do treino, não prevalência nem probabilidade de anomalia.
3. O early stopping do autoencoder observa loss de treino, sem conjunto de validação separado.
4. `cluster_profiling.z_score` é diferença de média dividida pelo desvio global; não é z-test nem significância.
5. `cluster_profiling.index` fica instável/difícil de interpretar com média global perto de zero ou negativa.
6. O output histórico do notebook de profiling é abreviado embora a célula imprima todas as linhas.
7. Em `clustering_suite`, `method=\"both\"` e `method=\"silhouette\"` recomendam o mesmo `best_k`; não há votação entre métricas.
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
"""
    (ROOT / "docs/sprints/readmes_objetos/ACHADOS_R08.md").write_text(findings, encoding="utf-8")

    matrix = """# Matriz de alterações R08

**Base:** `b73bbb91961f9ba5f9031d648c42ec0891b63347` (main pós-R07)
**Contrato:** README de objeto 1.0.0
**Escopo funcional:** nenhum; implementação/fachadas protegidas.

## READMEs novos

- `ambiente_fonte/.assistant/hub_snippets/ml/autoencoder_anomaly/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/cluster_profiling/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/clustering_suite/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/README.md`
- `ambiente_fonte/.assistant/hub_snippets/ml/umap_viz/README.md`

## Documentação não-README alterada

- `CHANGELOG.md`
- `CLAUDE.md`
- `MANUAL_TECNICO.md` (cópia sincronizada a partir do canônico)
- `ambiente_fonte/.assistant/MANUAL_TECNICO.md`
- seis `exemplo_<objeto>.py` da R08 — somente Markdown/backlink/correção didática
- `PLANO_HUB.md`
- `docs/sprints/README.md`
- `docs/sprints/readmes_objetos/CONTROLE_MIGRACAO.json`
- `docs/sprints/readmes_objetos/README.md`
- `docs/sprints/readmes_objetos/RELATORIO_R08.md`
- `docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R08.md`
- `docs/sprints/readmes_objetos/ACHADOS_R08.md`
- `docs/sprints/readmes_objetos/RUBRICA_R08.json`
- `docs/sprints/readmes_objetos/evidencias_r08/aplicar_r08.py`
- `docs/sprints/readmes_objetos/evidencias_r08/verificar_r08.py`
- `docs/sprints/readmes_objetos/evidencias_r08/verificar_preservacao.py`

## READMEs/derivados alterados além dos seis novos

- `README.md` raiz — checkpoint R08 + snapshot derivado do validador.
- `ambiente_fonte/.assistant/hub_snippets/README.md` — rota narrativa R08.
- `Novo_Ambiente_Simulado/**` correspondente — **somente** via `tools/render_simulado.py`.

## Proteções

As seis implementações e seis fachadas da R08 devem permanecer byte a byte iguais à base. Os notebooks preservam código/magics executáveis e blocos de output; apenas a camada Markdown é ajustada. R09 não começa nesta árvore.
"""
    (ROOT / "docs/sprints/readmes_objetos/MATRIZ_ALTERACOES_R08.md").write_text(matrix, encoding="utf-8")

    report = """# Relatório R08 — clusters, anomalias e explicabilidade

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

STATUS_R08: CANDIDATA — aguarda fechamento automatizado e revisão/aceite humano antes de qualquer merge.
"""
    (ROOT / "docs/sprints/readmes_objetos/RELATORIO_R08.md").write_text(report, encoding="utf-8")

    rubric = {
        "sprint": "R08",
        "base": "b73bbb91961f9ba5f9031d648c42ec0891b63347",
        "contract": "1.0.0",
        "objects": OBJECTS,
        "coverage_expected": {"operational": 55, "total": 75, "exemplars": "3/3", "pending": 20},
        "review_level": "A0_light_self_review",
        "independent_audit": False,
        "databricks_published": False,
        "criteria": {
            "readme_contract": "pending_runtime",
            "implementation_facade_preservation": "pending_runtime",
            "notebook_executable_preservation": "pending_runtime",
            "runtime_core": "pending_runtime",
            "runtime_torch": "pending_runtime",
            "runtime_shap": "pending_runtime",
            "runtime_umap": "pending_runtime",
            "full_gate_v00_v04": "pending_runtime",
        },
    }
    (ROOT / "docs/sprints/readmes_objetos/RUBRICA_R08.json").write_text(
        json.dumps(rubric, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    add_backlinks()
    edit_notebooks()
    edit_shared_docs()
    update_migration()
    write_sprint_docs()


if __name__ == "__main__":
    main()
