# Leitura dos arquivos de métricas e scripts

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt10-mt11-code-map"></a>
<a id="mt10-mt11-code-map"></a>
### Leitura dos arquivos de métricas e scripts

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Para métricas e scripts, confira a unidade de cada número e o destino de cada efeito. Um diagnóstico de qualidade, uma figura, um arquivo e um registro MLflow pedem interpretações diferentes.

<!-- editorial:exclude:start -->
[Ampliações atuais: run_micromodelo e referência SHAP linear](MT-mt10-current-api-additions-map.md#mt10-current-api-additions-map).
<!-- editorial:exclude:end -->

<a id="mt10-mt11-code-map-file-001"></a>
#### 1. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/data_quality_check/__init__.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/data_quality_check/__init__.py` · SHA-256 `35e58c046ce8cc5e81ae7d20925471baecebc835e7e67ce7b465cc17a391dcf1` |
| Papel e motivo técnico | Checar chave candidata, nulos e frescor com limiares locais, sem converter status em gate de pipeline. |
| Nomes disponibilizados | DEFAULT_THRESHOLDS, data_quality_check |
| Entradas | import da fachada; contrato da implementação: DEFAULT_THRESHOLDS; data_quality_check(table_name,pk_columns,date_column=None,thresholds=None) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | pyspark import obrigatório no topo; datetime. |
| Como interpretar este arquivo | A fachada reexporta DEFAULT_THRESHOLDS, data_quality_check; importar o pacote carrega as dependências de topo (pyspark import obrigatório no topo; datetime.), mas não chama a operação. O status resume limiares locais de chave, nulos e frescor; não bloqueia automaticamente um pipeline. Frescor depende do relógio da execução e do ritmo esperado da fonte, e a chave candidata deve ser fornecida, inclusive quando composta. |

<a id="mt10-mt11-code-map-file-002"></a>
#### 2. `data_quality_check.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/data_quality_check/data_quality_check.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/data_quality_check/data_quality_check.py` · SHA-256 `8cb820c26f9380627bfcad5491b192a4510aa65ab46622382c699d453bb904eb` |
| Papel e motivo técnico | Checar chave candidata, nulos e frescor com limiares locais, sem converter status em gate de pipeline. |
| Nomes disponibilizados | DEFAULT_THRESHOLDS; data_quality_check(table_name,pk_columns,date_column=None,thresholds=None) |
| Entradas | Tabela/view Spark legível; chave composta não vazia; data opcional; null_warn<=null_fail e freshness_days>=0. |
| Saídas | dict status/score/thresholds/checks/alerts; pk_uniqueness com duplicatas e nulos; nulls por coluna; freshness quando pedida. |
| Efeitos | Spark agg.collect e dropDuplicates.count; lê tabela; sem gravação; usa date.today local. |
| Dependências e momento de uso | pyspark import obrigatório no topo; datetime. |
| Como interpretar este arquivo | O status resume limiares locais de chave, nulos e frescor; não bloqueia automaticamente um pipeline. Frescor depende do relógio da execução e do ritmo esperado da fonte, e a chave candidata deve ser fornecida, inclusive quando composta. Entrada: Tabela/view Spark legível; chave composta não vazia; data opcional; null_warn<=null_fail e freshness_days>=0. Saída: dict status/score/thresholds/checks/alerts; pk_uniqueness com duplicatas e nulos; nulls por coluna; freshness quando pedida. Efeitos da chamada: Spark agg.collect e dropDuplicates.count; lê tabela; sem gravação; usa date.today local. Dependências: pyspark import obrigatório no topo; datetime. |

<a id="mt10-mt11-code-map-file-003"></a>
#### 3. `exemplo_data_quality_check.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/data_quality_check/exemplo_data_quality_check.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/data_quality_check/exemplo_data_quality_check.py` · SHA-256 `fadae78b9d8c77e8b186794c5aeb619627f5536fa61d4ae9280c5870abb67d87` |
| Papel e motivo técnico | Checar chave candidata, nulos e frescor com limiares locais, sem converter status em gate de pipeline. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra DEFAULT_THRESHOLDS; data_quality_check(table_name,pk_columns,date_column=None,thresholds=None) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; Tabela/view Spark legível; chave composta não vazia; data opcional; null_warn<=null_fail e freshness_days>=0. |
| Saídas | Notebook cria duas views temporárias com fixtures, compara frescor default vs 400 dias e duplicação de SP; prints históricos, sem tabela persistente. |
| Efeitos | efeitos da célula: Notebook cria duas views temporárias com fixtures, compara frescor default vs 400 dias e duplicação de SP; prints históricos, sem tabela persistente. Efeitos do helper chamado: Spark agg.collect e dropDuplicates.count; lê tabela; sem gravação; usa date.today local. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: pyspark import obrigatório no topo; datetime. |
| Como interpretar este arquivo | O status resume limiares locais de chave, nulos e frescor; não bloqueia automaticamente um pipeline. Frescor depende do relógio da execução e do ritmo esperado da fonte, e a chave candidata deve ser fornecida, inclusive quando composta. O exemplo usa esta fixture e sequência: Notebook cria duas views temporárias com fixtures, compara frescor default vs 400 dias e duplicação de SP; prints históricos, sem tabela persistente. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |
| Leitura do comentário atual | Confirme sessão Spark/PySpark, Hub importável e permissão para criar/substituir as views temporárias. O relógio usado em freshness e os limites declarados podem mudar o status frente ao ensaio histórico; não há garantia universal por tipo de compute. |

<a id="mt10-mt11-code-map-file-004"></a>
#### 4. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/doc_coverage/__init__.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/doc_coverage/__init__.py` · SHA-256 `8dc651f7a2022cb2c9d4637f8f1b9fdad7094298397302b9cb375b01710adc78` |
| Papel e motivo técnico | Medir adjacência estrutural Markdown/código em arquivo exportado, sem julgar qualidade da prosa. |
| Nomes disponibilizados | SOURCE_MARKERS, doc_coverage |
| Entradas | import da fachada; contrato da implementação: SOURCE_MARKERS; doc_coverage(notebook_path) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | biblioteca padrão json/pathlib; sem Spark no helper. |
| Como interpretar este arquivo | A fachada reexporta SOURCE_MARKERS, doc_coverage; importar o pacote carrega as dependências de topo (biblioteca padrão json/pathlib; sem Spark no helper.), mas não chama a operação. A cobertura mede adjacência estrutural entre Markdown e código em arquivo exportado, não qualidade da explicação. Trechos Spark presentes em fixtures são texto lido pelo analisador; não há execução desse código pelo helper. |

<a id="mt10-mt11-code-map-file-005"></a>
#### 5. `doc_coverage.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/doc_coverage/doc_coverage.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/doc_coverage/doc_coverage.py` · SHA-256 `c9fd2d438c4e4abf406a4253f3fdf7b2f58d414ab3ae61d326b6e341f1db689c` |
| Papel e motivo técnico | Medir adjacência estrutural Markdown/código em arquivo exportado, sem julgar qualidade da prosa. |
| Nomes disponibilizados | SOURCE_MARKERS; doc_coverage(notebook_path) |
| Entradas | Caminho local .ipynb/.py/.sql/.scala/.r existente; marcadores específicos por linguagem. |
| Saídas | dict path/format/total_code_cells/total_markdown_cells/coverage_pct/uncovered_cell_indexes/metric_note. |
| Efeitos | Lê arquivo local; não busca workspace nem grava; 100% se zero células código. |
| Dependências e momento de uso | biblioteca padrão json/pathlib; sem Spark no helper. |
| Como interpretar este arquivo | A cobertura mede adjacência estrutural entre Markdown e código em arquivo exportado, não qualidade da explicação. Trechos Spark presentes em fixtures são texto lido pelo analisador; não há execução desse código pelo helper. Entrada: Caminho local .ipynb/.py/.sql/.scala/.r existente; marcadores específicos por linguagem. Saída: dict path/format/total_code_cells/total_markdown_cells/coverage_pct/uncovered_cell_indexes/metric_note. Efeitos da chamada: Lê arquivo local; não busca workspace nem grava; 100% se zero células código. Dependências: biblioteca padrão json/pathlib; sem Spark no helper. |

<a id="mt10-mt11-code-map-file-006"></a>
#### 6. `exemplo_doc_coverage.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/doc_coverage/exemplo_doc_coverage.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/doc_coverage/exemplo_doc_coverage.py` · SHA-256 `5f8d0180a43fccc5682d46c7144f674190d7132f8ac3cde688e8e4ca64b72a52` |
| Papel e motivo técnico | Medir adjacência estrutural Markdown/código em arquivo exportado, sem julgar qualidade da prosa. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra SOURCE_MARKERS; doc_coverage(notebook_path) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; Caminho local .ipynb/.py/.sql/.scala/.r existente; marcadores específicos por linguagem. |
| Saídas | Notebook escreve BEM/MAL/VAZIO em /tmp, lê cada um e remove os três; esses writes/unlinks pertencem ao notebook, não ao helper. |
| Efeitos | efeitos da célula: Notebook escreve BEM/MAL/VAZIO em /tmp, lê cada um e remove os três; esses writes/unlinks pertencem ao notebook, não ao helper. Efeitos do helper chamado: Lê arquivo local; não busca workspace nem grava; 100% se zero células código. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: biblioteca padrão json/pathlib; sem Spark no helper. |
| Como interpretar este arquivo | A cobertura mede adjacência estrutural entre Markdown e código em arquivo exportado, não qualidade da explicação. Trechos Spark presentes em fixtures são texto lido pelo analisador; não há execução desse código pelo helper. O exemplo usa esta fixture e sequência: Notebook escreve BEM/MAL/VAZIO em /tmp, lê cada um e remove os três; esses writes/unlinks pertencem ao notebook, não ao helper. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |
| Leitura do comentário atual | O helper lê arquivos no driver; o preparo deste notebook também usa Spark. Os nomes BEM, MAL e VAZIO são fixos em /tmp: write_text pode sobrescrever arquivos existentes e unlink os remove ao fim. Confira acesso e conteúdo antes de uma execução autorizada; não há backup nem limpeza garantida após falha intermediária. |

<a id="mt10-mt11-code-map-file-007"></a>
#### 7. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/drift_detector/__init__.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/drift_detector/__init__.py` · SHA-256 `3a8c39fd78e40828bc4bfa1d6c56137ad62459177f89979648d773a89a25043a` |
| Papel e motivo técnico | Comparar coortes da mesma tabela por PSI numérico, separando mudança de distribuição de performance. |
| Nomes disponibilizados | drift_detector |
| Entradas | import da fachada; contrato da implementação: drift_detector(table_name,date_col,date_ref,date_comp,cols=None,method="psi",*,num_bins=10,relative_error=.001,epsilon=1e-6,warning_threshold=None,critical_threshold=None) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | pyspark obrigatório, math.log. |
| Como interpretar este arquivo | A fachada reexporta drift_detector; importar o pacote carrega as dependências de topo (pyspark obrigatório, math.log.), mas não chama a operação. PSI compara coortes numéricas da mesma tabela; mudança de distribuição não demonstra queda de performance. Sem limiares warning/critical na chamada, a classificação é not_classified, mesmo que o notebook mencione a heurística 0,25. |

<a id="mt10-mt11-code-map-file-008"></a>
#### 8. `drift_detector.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/drift_detector/drift_detector.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/drift_detector/drift_detector.py` · SHA-256 `92263a25e672b74fbb72538c4a8dc6366c1dc299e7a4f69345dadfe0d6934244` |
| Papel e motivo técnico | Comparar coortes da mesma tabela por PSI numérico, separando mudança de distribuição de performance. |
| Nomes disponibilizados | drift_detector(table_name,date_col,date_ref,date_comp,cols=None,method="psi",*,num_bins=10,relative_error=.001,epsilon=1e-6,warning_threshold=None,critical_threshold=None) |
| Entradas | Tabela Spark com coortes não vazias; num_bins 2..100; cols numéricas; só method=psi; limites de classificação opcionais calibrados. |
| Saídas | dict por coluna: psi/classification/boundaries/reference_size/comparison_size/buckets com counts, percentuais suavizados e contribuições. |
| Efeitos | spark.table, filtros, counts, approxQuantile, collect de buckets; tenta cache e unpersist; sem gravação. |
| Dependências e momento de uso | pyspark obrigatório, math.log. |
| Como interpretar este arquivo | PSI compara coortes numéricas da mesma tabela; mudança de distribuição não demonstra queda de performance. Sem limiares warning/critical na chamada, a classificação é not_classified, mesmo que o notebook mencione a heurística 0,25. Entrada: Tabela Spark com coortes não vazias; num_bins 2..100; cols numéricas; só method=psi; limites de classificação opcionais calibrados. Saída: dict por coluna: psi/classification/boundaries/reference_size/comparison_size/buckets com counts, percentuais suavizados e contribuições. Efeitos da chamada: spark.table, filtros, counts, approxQuantile, collect de buckets; tenta cache e unpersist; sem gravação. Dependências: pyspark obrigatório, math.log. |

<a id="mt10-mt11-code-map-file-009"></a>
#### 9. `exemplo_drift_detector.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/drift_detector/exemplo_drift_detector.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/drift_detector/exemplo_drift_detector.py` · SHA-256 `61a414b89005525b22a0a281940588bdb22f70d61b0ce2a9d4c904283221d2ca` |
| Papel e motivo técnico | Comparar coortes da mesma tabela por PSI numérico, separando mudança de distribuição de performance. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra drift_detector(table_name,date_col,date_ref,date_comp,cols=None,method="psi",*,num_bins=10,relative_error=.001,epsilon=1e-6,warning_threshold=None,critical_threshold=None) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; Tabela Spark com coortes não vazias; num_bins 2..100; cols numéricas; só method=psi; limites de classificação opcionais calibrados. |
| Saídas | Notebook cria view temporária 8000 linhas, duas distribuições de média semelhante; chama sem thresholds e mostra PSI histórico ~2.94. |
| Efeitos | efeitos da célula: Notebook cria view temporária 8000 linhas, duas distribuições de média semelhante; chama sem thresholds e mostra PSI histórico ~2.94. Efeitos do helper chamado: spark.table, filtros, counts, approxQuantile, collect de buckets; tenta cache e unpersist; sem gravação. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: pyspark obrigatório, math.log. |
| Como interpretar este arquivo | PSI compara coortes numéricas da mesma tabela; mudança de distribuição não demonstra queda de performance. Sem limiares warning/critical na chamada, a classificação é not_classified, mesmo que o notebook mencione a heurística 0,25. O exemplo usa esta fixture e sequência: Notebook cria view temporária 8000 linhas, duas distribuições de média semelhante; chama sem thresholds e mostra PSI histórico ~2.94. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |
| Leitura do comentário atual | A guarda de cache é oportunista; não protege todas as operações Spark. Confirme tipos, coortes não vazias, sessão e permissão para a view temporária. A heurística histórica de PSI não substitui warning_threshold e critical_threshold declarados. |

<a id="mt10-mt11-code-map-file-010"></a>
#### 10. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/naming_checker/__init__.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/naming_checker/__init__.py` · SHA-256 `5fa3bd5d7a2f3a6fc60a83fcc943c7751ef1181df57d5a2401af960ad81ffec3` |
| Papel e motivo técnico | Distinguir convenção local de exigência Databricks; devolver avisos, não renomear. |
| Nomes disponibilizados | naming_checker |
| Entradas | import da fachada; contrato da implementação: naming_checker(table_name,*,enforce_prefix=False,allowed_table_prefixes=(),max_col_length=255) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | pyspark obrigatório; re/Sequence. |
| Como interpretar este arquivo | A fachada reexporta naming_checker; importar o pacote carrega as dependências de topo (pyspark obrigatório; re/Sequence.), mas não chama a operação. O helper emite avisos de convenção local e não renomeia objetos. O aviso de nome totalmente qualificado pode aparecer também em view temporária legítima; prefixo só é exigido quando ativado com lista apropriada. |

<a id="mt10-mt11-code-map-file-011"></a>
#### 11. `exemplo_naming_checker.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/naming_checker/exemplo_naming_checker.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/naming_checker/exemplo_naming_checker.py` · SHA-256 `d038c136ddaafaa607764d4f7ee4079746fbcc1200b1b2b603b2894be0a0a381` |
| Papel e motivo técnico | Distinguir convenção local de exigência Databricks; devolver avisos, não renomear. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra naming_checker(table_name,*,enforce_prefix=False,allowed_table_prefixes=(),max_col_length=255) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; Nome de tabela/view; prefixos explícitos se enforce_prefix; max_col_length>0. |
| Saídas | Notebook cria view temporária com camelCase e coluna longa, testa prefixo sem lista (ValueError) e regra vw_; outputs históricos. |
| Efeitos | efeitos da célula: Notebook cria view temporária com camelCase e coluna longa, testa prefixo sem lista (ValueError) e regra vw_; outputs históricos. Efeitos do helper chamado: spark.table e leitura de schema/colunas; sem scan de linhas/escrita. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: pyspark obrigatório; re/Sequence. |
| Como interpretar este arquivo | O helper emite avisos de convenção local e não renomeia objetos. O aviso de nome totalmente qualificado pode aparecer também em view temporária legítima; prefixo só é exigido quando ativado com lista apropriada. O exemplo usa esta fixture e sequência: Notebook cria view temporária com camelCase e coluna longa, testa prefixo sem lista (ValueError) e regra vw_; outputs históricos. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |
| Leitura do comentário atual | Confirme sessão Spark, resolução de nomes e acesso ao schema, além da criação/substituição da view pelo exemplo. O helper inspeciona metadados, mas o preparo cria uma fixture; essa distinção não prova compatibilidade universal do notebook. |

<a id="mt10-mt11-code-map-file-012"></a>
#### 12. `naming_checker.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/naming_checker/naming_checker.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/naming_checker/naming_checker.py` · SHA-256 `778ffcca7c38547ea8a422da5ed36376396aaff042ad51aa4fe8689a16b1e482` |
| Papel e motivo técnico | Distinguir convenção local de exigência Databricks; devolver avisos, não renomear. |
| Nomes disponibilizados | naming_checker(table_name,*,enforce_prefix=False,allowed_table_prefixes=(),max_col_length=255) |
| Entradas | Nome de tabela/view; prefixos explícitos se enforce_prefix; max_col_length>0. |
| Saídas | lista de dict object/severity=warning/message/policy; lista vazia só para regras verificadas. |
| Efeitos | spark.table e leitura de schema/colunas; sem scan de linhas/escrita. |
| Dependências e momento de uso | pyspark obrigatório; re/Sequence. |
| Como interpretar este arquivo | O helper emite avisos de convenção local e não renomeia objetos. O aviso de nome totalmente qualificado pode aparecer também em view temporária legítima; prefixo só é exigido quando ativado com lista apropriada. Entrada: Nome de tabela/view; prefixos explícitos se enforce_prefix; max_col_length>0. Saída: lista de dict object/severity=warning/message/policy; lista vazia só para regras verificadas. Efeitos da chamada: spark.table e leitura de schema/colunas; sem scan de linhas/escrita. Dependências: pyspark obrigatório; re/Sequence. |

<a id="mt10-mt11-code-map-file-013"></a>
#### 13. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/quick_profile/__init__.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/quick_profile/__init__.py` · SHA-256 `b81a6312e38b4dbcc42477ae22c99e5a3eaa8da5aa7586a04a2108970990e7bd` |
| Papel e motivo técnico | Distinguir contagens exatas integrais de estatísticas amostrais limitadas por colunas. |
| Nomes disponibilizados | quick_profile |
| Entradas | import da fachada; contrato da implementação: quick_profile(table_name,sample_fraction=.1,max_categories=20,*,seed=42) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | pyspark obrigatório. |
| Como interpretar este arquivo | A fachada reexporta quick_profile; importar o pacote carrega a dependência PySpark, mas não chama a operação. Total de linhas e nulos são agregados na base inteira; os demais resumos usam a amostra. Na implementação, o limite 10/5/10/5 significa até dez colunas de texto para cardinalidade aproximada, cinco de texto para valores mais frequentes, dez numéricas para mínimo/máximo/média e cinco datas para faixa temporal. Mesmo sample_fraction=1 não torna a cardinalidade exata nem garante que uma categoria rara apareça no resumo. |

<a id="mt10-mt11-code-map-file-014"></a>
#### 14. `exemplo_quick_profile.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/quick_profile/exemplo_quick_profile.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/quick_profile/exemplo_quick_profile.py` · SHA-256 `dec6dc9fd218f4475d5cb1f133cfcba05847ae7991a66608d5c703320267a064` |
| Papel e motivo técnico | Distinguir contagens exatas integrais de estatísticas amostrais limitadas por colunas. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra quick_profile(table_name,sample_fraction=.1,max_categories=20,*,seed=42) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; Tabela/view Spark; fração (0,1], max_categories>0, seed. |
| Saídas | Notebook cria view temporária de fixture 2000 linhas, perfis 0.25 e 1.0; cardinalidade aproximada histórica pode exceder sample_rows. |
| Efeitos | efeitos da célula: Notebook cria view temporária de fixture 2000 linhas, perfis 0.25 e 1.0; cardinalidade aproximada histórica pode exceder sample_rows. Efeitos do helper chamado: agg.collect tabela inteira; sample.count; approx_count_distinct, groupBy/collect; tenta cache e unpersist; sem gravação. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: pyspark obrigatório. |
| Como interpretar este arquivo | Total de linhas e nulos vêm da tabela inteira; os outros resumos vêm da amostra. O limite 10/5/10/5 do helper cobre, respectivamente, até dez colunas de texto na cardinalidade aproximada, cinco colunas de texto nos valores mais frequentes, dez numéricas no resumo e cinco datas na faixa temporal. O notebook cria uma view temporária com 2.000 linhas e pede perfis de 0,25 e 1,0; a cardinalidade aproximada histórica pode superar sample_rows. As saídas impressas são daquele ensaio, não de uma execução atual, e amostra integral não torna o estimador exato. |
| Leitura do comentário atual | A guarda trata a tentativa de cache, sem garantir as demais operações. Resumos de categorias podem expor valores sensíveis; limite sua exibição. A saída colada é do cenário observado e não reexecução no ambiente do leitor. |

<a id="mt10-mt11-code-map-file-015"></a>
#### 15. `quick_profile.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/quick_profile/quick_profile.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/quick_profile/quick_profile.py` · SHA-256 `13b34c9ef0c402f53e10487efe97df84436445711d86c4556bb48d651cb7d391` |
| Papel e motivo técnico | Distinguir contagens exatas integrais de estatísticas amostrais limitadas por colunas. |
| Nomes disponibilizados | quick_profile(table_name,sample_fraction=.1,max_categories=20,*,seed=42) |
| Entradas | Tabela/view Spark; fração (0,1], max_categories>0, seed. |
| Saídas | dict table/total_rows/total_columns/sample_fraction/sample_seed/sample_rows/dtypes/null_summary_full_table/cardinality_sample/top_values_sample/numeric_summary_sample/date_range_sample. |
| Efeitos | agg.collect tabela inteira; sample.count; approx_count_distinct, groupBy/collect; tenta cache e unpersist; sem gravação. |
| Dependências e momento de uso | pyspark obrigatório. |
| Como interpretar este arquivo | Total de linhas e nulos são agregados na tabela inteira; cardinalidade, top valores, estatísticas numéricas e datas usam a amostra. O limite 10/5/10/5 restringe, nessa ordem, colunas de texto na cardinalidade aproximada, colunas de texto nos top valores, colunas numéricas no resumo e colunas de data na faixa temporal. `max_categories` limita valores por coluna selecionada, não o número de colunas. Mesmo com sample_fraction=1, `approx_count_distinct` continua aproximado. A chamada recebe tabela/view, fração, limite e seed; devolve dict com contagens integrais e resumos amostrais. Executa agregações/coletas Spark, tenta cache e unpersist, sem gravar. PySpark é dependência obrigatória. |

<a id="mt10-mt11-code-map-file-016"></a>
#### 16. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/rfv_calculator/__init__.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/rfv_calculator/__init__.py` · SHA-256 `47a003958e716b371ef430dc18440b232160bd0b3c37b91321d16f9f7bf2b196` |
| Papel e motivo técnico | Features RFV por entidade com data de corte inclusiva; não pontuar segmentos. |
| Nomes disponibilizados | rfv_calculator |
| Entradas | import da fachada; contrato da implementação: rfv_calculator(table_name,col_cliente,col_data,col_valor,dt_referencia,periodos=(30,60,90)) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | pyspark obrigatório. |
| Como interpretar este arquivo | A fachada reexporta rfv_calculator; importar o pacote carrega as dependências de topo (pyspark obrigatório.), mas não chama a operação. RFV agrega eventos por entidade até um corte inclusivo e devolve recência, frequência e valor, sem pontuar segmentos. O corte global sozinho não resolve atraso de disponibilidade, ponto no tempo nem instantes de decisão por linha. |

<a id="mt10-mt11-code-map-file-017"></a>
#### 17. `exemplo_rfv_calculator.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/rfv_calculator/exemplo_rfv_calculator.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/rfv_calculator/exemplo_rfv_calculator.py` · SHA-256 `b2d9438e94e5fd88ff8f95b0d6b8c1eb07c666f85b4c0c6e1938293f0d699637` |
| Papel e motivo técnico | Features RFV por entidade com data de corte inclusiva; não pontuar segmentos. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra rfv_calculator(table_name,col_cliente,col_data,col_valor,dt_referencia,periodos=(30,60,90)) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; Tabela Spark de eventos; colunas cliente/data/valor; data referência global; períodos positivos deduplicados. |
| Saídas | Notebook amostra painel de 40 entidades, cria view temporária, exibe RFV, compara frequência com contagem filtrada; números históricos. |
| Efeitos | efeitos da célula: Notebook amostra painel de 40 entidades, cria view temporária, exibe RFV, compara frequência com contagem filtrada; números históricos. Efeitos do helper chamado: Constrói plano Spark com filtros/groupBy/joins, sem ação nem persistência no helper; notebook chama display/count. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: pyspark obrigatório. |
| Como interpretar este arquivo | RFV agrega eventos por entidade até um corte inclusivo e devolve recência, frequência e valor, sem pontuar segmentos. O corte global sozinho não resolve atraso de disponibilidade, ponto no tempo nem instantes de decisão por linha. O exemplo usa esta fixture e sequência: Notebook amostra painel de 40 entidades, cria view temporária, exibe RFV, compara frequência com contagem filtrada; números históricos. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |
| Leitura do comentário atual | Antes de usar o exemplo, confira tipos, modo ANSI, datas e chave não nula no destino. O helper não valida sozinho todas essas condições: conversões de data e joins dependem delas; o corte global não resolve disponibilidade tardia. |

<a id="mt10-mt11-code-map-file-018"></a>
#### 18. `rfv_calculator.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/rfv_calculator/rfv_calculator.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/rfv_calculator/rfv_calculator.py` · SHA-256 `ea6305a7fbe724d668a9b077d77a899993c36cbbc3b89e30f02fc29a11463646` |
| Papel e motivo técnico | Features RFV por entidade com data de corte inclusiva; não pontuar segmentos. |
| Nomes disponibilizados | rfv_calculator(table_name,col_cliente,col_data,col_valor,dt_referencia,periodos=(30,60,90)) |
| Entradas | Tabela Spark de eventos; colunas cliente/data/valor; data referência global; períodos positivos deduplicados. |
| Saídas | DataFrame Spark com ultima_data, valor_total, frequencia_total, recencia e pares frequencia_Nd/valor_Nd preenchidos 0. |
| Efeitos | Constrói plano Spark com filtros/groupBy/joins, sem ação nem persistência no helper; notebook chama display/count. |
| Dependências e momento de uso | pyspark obrigatório. |
| Como interpretar este arquivo | RFV agrega eventos por entidade até um corte inclusivo e devolve recência, frequência e valor, sem pontuar segmentos. O corte global sozinho não resolve atraso de disponibilidade, ponto no tempo nem instantes de decisão por linha. Entrada: Tabela Spark de eventos; colunas cliente/data/valor; data referência global; períodos positivos deduplicados. Saída: DataFrame Spark com ultima_data, valor_total, frequencia_total, recencia e pares frequencia_Nd/valor_Nd preenchidos 0. Efeitos da chamada: Constrói plano Spark com filtros/groupBy/joins, sem ação nem persistência no helper; notebook chama display/count. Dependências: pyspark obrigatório. |

<a id="mt10-mt11-code-map-file-019"></a>
#### 19. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/schema_to_yaml/__init__.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/__init__.py` · SHA-256 `db3dd2fb208358ed8a596c2abbfca7b65ec8434da4ccfb25ef5e6f67e9a000f1` |
| Papel e motivo técnico | Fotografia serializável do schema; separar introspecção de varredura estatística. |
| Nomes disponibilizados | schema_to_dict, schema_to_yaml |
| Entradas | import da fachada; contrato da implementação: schema_to_dict(table_name,*,include_comments=True,include_stats=False); schema_to_yaml(table_name,include_comments=True,include_stats=False) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | pyspark obrigatório; yaml import protegido na função; JSON stdlib fallback. |
| Como interpretar este arquivo | A fachada reexporta schema_to_dict, schema_to_yaml; importar o pacote carrega as dependências de topo (pyspark obrigatório; yaml import protegido na função; JSON stdlib fallback.), mas não chama a operação. A fotografia do schema é diferente de estatística opcional sobre linhas. PyYAML é opcional: a serialização textual pode ser YAML ou JSON; approx_distinct pode até exceder row_count por ser aproximação. |

<a id="mt10-mt11-code-map-file-020"></a>
#### 20. `exemplo_schema_to_yaml.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/schema_to_yaml/exemplo_schema_to_yaml.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/exemplo_schema_to_yaml.py` · SHA-256 `fcfde4981aec23b9d1e004ca5c4088d5248222d4f03583d0a9695a18350244f1` |
| Papel e motivo técnico | Fotografia serializável do schema; separar introspecção de varredura estatística. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra schema_to_dict(table_name,*,include_comments=True,include_stats=False); schema_to_yaml(table_name,include_comments=True,include_stats=False) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; Tabela/view Spark; comentários do metadata opcionais; stats opcionais. |
| Saídas | Notebook cria view temporária, imprime dict/YAML, detecta PyYAML e habilita stats; saída histórica de approx_distinct. |
| Efeitos | efeitos da célula: Notebook cria view temporária, imprime dict/YAML, detecta PyYAML e habilita stats; saída histórica de approx_distinct. Efeitos do helper chamado: spark.table/schema; include_stats=True executa agg.collect sobre dados; helper não escreve arquivo. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: pyspark obrigatório; yaml import protegido na função; JSON stdlib fallback. |
| Como interpretar este arquivo | A fotografia do schema é diferente de estatística opcional sobre linhas. PyYAML é opcional: a serialização textual pode ser YAML ou JSON; approx_distinct pode até exceder row_count por ser aproximação. O exemplo usa esta fixture e sequência: Notebook cria view temporária, imprime dict/YAML, detecta PyYAML e habilita stats; saída histórica de approx_distinct. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |
| Leitura do comentário atual | A frase impressa “nenhum consumidor quebra” é ampla demais. O JSON alternativo exige consumidor compatível com YAML 1.2; o fallback captura somente ImportError de PyYAML, não falha Spark nem de serialização. Sem estatísticas há introspecção, sem promessa de latência; include_stats=True varre dados e agrega por coluna. |

<a id="mt10-mt11-code-map-file-021"></a>
#### 21. `schema_to_yaml.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_scripts/schema_to_yaml/schema_to_yaml.py) · [MT11: explicação do mecanismo](MT-parte-ii.md#mt11-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_scripts/schema_to_yaml/schema_to_yaml.py` · SHA-256 `621aad423ccf89b083c3308dfc13d62bb44fc1a99d1ba7ac4a2dcd68719388b7` |
| Papel e motivo técnico | Fotografia serializável do schema; separar introspecção de varredura estatística. |
| Nomes disponibilizados | schema_to_dict(table_name,*,include_comments=True,include_stats=False); schema_to_yaml(table_name,include_comments=True,include_stats=False) |
| Entradas | Tabela/view Spark; comentários do metadata opcionais; stats opcionais. |
| Saídas | dict table/columns(name,type,nullable,comment?,stats?)/row_count?; texto YAML safe_dump ou JSON válido YAML 1.2. |
| Efeitos | spark.table/schema; include_stats=True executa agg.collect sobre dados; helper não escreve arquivo. |
| Dependências e momento de uso | pyspark obrigatório; yaml import protegido na função; JSON stdlib fallback. |
| Como interpretar este arquivo | A fotografia do schema é diferente de estatística opcional sobre linhas. PyYAML é opcional: a serialização textual pode ser YAML ou JSON; approx_distinct pode até exceder row_count por ser aproximação. Entrada: Tabela/view Spark; comentários do metadata opcionais; stats opcionais. Saída: dict table/columns(name,type,nullable,comment?,stats?)/row_count?; texto YAML safe_dump ou JSON válido YAML 1.2. Efeitos da chamada: spark.table/schema; include_stats=True executa agg.collect sobre dados; helper não escreve arquivo. Dependências: pyspark obrigatório; yaml import protegido na função; JSON stdlib fallback. |

<a id="mt10-mt11-code-map-file-022"></a>
#### 22. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/curves_plotly/__init__.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/__init__.py` · SHA-256 `ef21643765651d58902388bdd9bdc73aad8a0fc322677b64c4245257679f4873` |
| Papel e motivo técnico | Quatro curvas para perguntas distintas; separar KS unilateral fração da métrica bilateral em pontos percentuais. |
| Nomes disponibilizados | PALETA_CATEGORICA, AZUL_CAIXA, LARANJA, CINZA_ESCURO, TEMA_BASE, plot_roc_curve, plot_roc_curve_resolvido, plot_pr_curve, plot_pr_curve_resolvido, plot_lift_curve, plot_lift_curve_resolvido, plot_ks_curve, plot_ks_curve_resolvido |
| Entradas | import da fachada; contrato da implementação: cores/TEMA_BASE; plot_roc_curve,plot_pr_curve,plot_lift_curve,plot_ks_curve e variantes _resolvido(theme) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | numpy/plotly/sklearn/hub colors+tema imports no topo; AP import na chamada. |
| Como interpretar este arquivo | A fachada reexporta PALETA_CATEGORICA, AZUL_CAIXA, LARANJA, CINZA_ESCURO, TEMA_BASE, plot_roc_curve, plot_roc_curve_resolvido, plot_pr_curve, plot_pr_curve_resolvido, plot_lift_curve, plot_lift_curve_resolvido, plot_ks_curve, plot_ks_curve_resolvido; importar o pacote carrega as dependências de topo (numpy/plotly/sklearn/hub colors+tema imports no topo; AP import na chamada.), mas não chama a operação. A curva KS visual usa max(TPR−FPR) unilateral em fração; ks_pct do relatório é teste bilateral em pontos percentuais. ROC, precisão-revocação e lift respondem perguntas distintas; a paleta própria de seis cores é preservada na rota legada e, via palette.curves_legacy, na rota de tema explícito; a paleta geral tem dez cores. |

<a id="mt10-mt11-code-map-file-023"></a>
#### 23. `curves_plotly.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/curves_plotly/curves_plotly.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/curves_plotly.py` · SHA-256 `eadc20c905079d6d15df8ff1c982e4af69db5558214c9cb270bc1daee30ec4f9` |
| Papel e motivo técnico | Quatro curvas para perguntas distintas; separar KS unilateral fração da métrica bilateral em pontos percentuais. |
| Nomes disponibilizados | cores/TEMA_BASE; plot_roc_curve,plot_pr_curve,plot_lift_curve,plot_ks_curve e variantes _resolvido(theme) |
| Entradas | y_true/y_prob 1D alinhados, classes 0/1 presentes, scores finitos [0,1]; lift n_bins 2..n; n só rodapé; theme para resolved. |
| Saídas | go.Figure por função; ROC AUC, PR AP, lift cumulativo, KS=max(TPR-FPR) fracionário. |
| Efeitos | cria figuras em memória, não chama show/save; tema resolved muda aparência. |
| Dependências e momento de uso | numpy/plotly/sklearn/hub colors+tema imports no topo; AP import na chamada. |
| Como interpretar este arquivo | A curva KS visual usa max(TPR−FPR) unilateral em fração; ks_pct do relatório é teste bilateral em pontos percentuais. ROC, precisão-revocação e lift respondem perguntas distintas; a paleta própria de seis cores é preservada na rota legada e, via palette.curves_legacy, na rota de tema explícito; a paleta geral tem dez cores. Entrada: y_true/y_prob 1D alinhados, classes 0/1 presentes, scores finitos [0,1]; lift n_bins 2..n; n só rodapé; theme para resolved. Saída: go.Figure por função; ROC AUC, PR AP, lift cumulativo, KS=max(TPR-FPR) fracionário. Efeitos da chamada: cria figuras em memória, não chama show/save; tema resolved muda aparência. Dependências: numpy/plotly/sklearn/hub colors+tema imports no topo; AP import na chamada. |

<a id="mt10-mt11-code-map-file-024"></a>
#### 24. `exemplo_curves_plotly.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/curves_plotly/exemplo_curves_plotly.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/curves_plotly/exemplo_curves_plotly.py` · SHA-256 `8f571fdfeed7f691d86c9f3ab8bc1d4a021f485b4277eb043c87254a5324a1ff` |
| Papel e motivo técnico | Quatro curvas para perguntas distintas; separar KS unilateral fração da métrica bilateral em pontos percentuais. |
| Nomes disponibilizados | notebook fonte Databricks que importa e chama somente plot_roc_curve, plot_pr_curve, plot_lift_curve e plot_ks_curve legados; variantes `_resolvido` pertencem à API relacionada do módulo, mas não aparecem nas chamadas deste notebook |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | o notebook gera y e p sintéticos alinhados, com duas classes e scores em [0,1]; passa esses vetores e títulos às quatro funções legadas, sem selecionar `ResolvedTheme` ou fornecer `theme` |
| Saídas | Notebook simula 8000 scores, chama quatro plots legados; output histórico 148 eventos; nenhum save/show explícito. |
| Efeitos | o notebook simula 8.000 scores, chama quatro funções que devolvem figuras em memória e não chama `show` nem salva arquivo; a transcrição histórica registra 148 eventos. Nenhuma rota resolvida de tema é chamada. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: o notebook importa NumPy e a fachada `curves_plotly`; a implementação usa Plotly/sklearn e imports visuais do Hub. O módulo oferece variantes temáticas, porém esta demonstração usa as funções legadas. |
| Como interpretar este arquivo | A curva KS visual usa max(TPR−FPR) unilateral em fração; `ks_pct` do relatório é teste bilateral em pontos percentuais. ROC, precisão-revocação e lift respondem perguntas diferentes. O comentário atual apresenta as seis cores como escolha preservada da família, inclusive nas rotas de tema explícito, distinta das dez de `constants.colors`. Selecione a paleta deliberadamente; esta demonstração chama somente as funções legadas e não seleciona tema V07. As saídas coladas pertencem ao ensaio histórico, não a uma execução atual. |

<a id="mt10-mt11-code-map-file-025"></a>
#### 25. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/explainability_report/__init__.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/__init__.py` · SHA-256 `817dce086d59b89bf85526b4059be7bec863d0e7b0b5943ee5e50cfb07f1e97e` |
| Papel e motivo técnico | Gerar Markdown a partir de importância já calculada, sem causalidade nem cálculo SHAP novo. |
| Nomes disponibilizados | generate_executive_report, generate_technical_summary |
| Entradas | import da fachada; contrato da implementação: generate_executive_report(shap_importance,feature_business_names,target_description,model_metric,...); generate_technical_summary(shap_importance,native_importance=None) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | numpy/pandas topo; tabulate requerido indiretamente por to_markdown; scipy.stats import no ramo nativo. |
| Como interpretar este arquivo | A fachada reexporta generate_executive_report, generate_technical_summary; importar o pacote carrega as dependências de topo (numpy/pandas topo; tabulate requerido indiretamente por to_markdown; scipy.stats import no ramo nativo.), mas não chama a operação. O relatório formata importância já calculada; não calcula SHAP, causalidade ou efeito de intervenção. A direção por correlação e o rank Spearman só fazem sentido com arrays alinhados; tabulate e SciPy podem ser exigidos em ramos distintos. |

<a id="mt10-mt11-code-map-file-026"></a>
#### 26. `exemplo_explainability_report.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/explainability_report/exemplo_explainability_report.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/exemplo_explainability_report.py` · SHA-256 `bbcb491d2e6e3efd67b6ec71098cad13943dea83b9bfb7029e7fb12f9054337c` |
| Papel e motivo técnico | Gerar Markdown a partir de importância já calculada, sem causalidade nem cálculo SHAP novo. |
| Nomes disponibilizados | notebook fonte Databricks que demonstra generate_executive_report(shap_importance,feature_business_names,target_description,model_metric,...); generate_technical_summary(shap_importance,native_importance=None) |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | fixture/estado de sessão do notebook; DataFrame com feature/pct_importance; nomes negócio/target/métrica; arrays opcionais alinhados para correlação; importância nativa opcional com ranks. |
| Saídas | Notebook monta importância sintética pronta, imprime executivo; técnico captura ImportError tabulate e fixture nativa carece rank; bloco diz não executado. |
| Efeitos | efeitos da célula: Notebook monta importância sintética pronta, imprime executivo; técnico captura ImportError tabulate e fixture nativa carece rank; bloco diz não executado. Efeitos do helper chamado: sem escrita; método técnico chama pandas.to_markdown; não salva relatório. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: numpy/pandas topo; tabulate requerido indiretamente por to_markdown; scipy.stats import no ramo nativo. |
| Como interpretar este arquivo | O relatório formata importância já calculada; não calcula SHAP, causalidade ou efeito de intervenção. A direção por correlação e o rank Spearman só fazem sentido com arrays alinhados; tabulate e SciPy podem ser exigidos em ramos distintos. O exemplo usa esta fixture e sequência: Notebook monta importância sintética pronta, imprime executivo; técnico captura ImportError tabulate e fixture nativa carece rank; bloco diz não executado. Os resultados impressos pertencem ao notebook histórico; reproduzir a chamada depende das entradas e das dependências indicadas no código, sem presumir execução atual. |
| Leitura do comentário atual | Os dois DataFrames da fixture carecem de rank. O resumo técnico requer tabulate e, na comparação nativa, SciPy; instalar tabulate sozinho não corrige a entrada. Com quatro features comuns, o acesso a rank_shap/rank_native pode gerar KeyError, que o except ImportError do notebook não captura. Prepare rankings coerentes, uma linha por feature, antes de executar. |

<a id="mt10-mt11-code-map-file-027"></a>
#### 27. `explainability_report.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/explainability_report/explainability_report.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/explainability_report/explainability_report.py` · SHA-256 `3a17ccfb09318b03d0c538882c5d5d8fab1c89fcf93d0683c1637174c1522bf7` |
| Papel e motivo técnico | Gerar Markdown a partir de importância já calculada, sem causalidade nem cálculo SHAP novo. |
| Nomes disponibilizados | generate_executive_report(shap_importance,feature_business_names,target_description,model_metric,...); generate_technical_summary(shap_importance,native_importance=None) |
| Entradas | DataFrame com feature/pct_importance; nomes negócio/target/métrica; arrays opcionais alinhados para correlação; importância nativa opcional com ranks. |
| Saídas | duas strings Markdown; direção por correlação Pearson quando arrays; rho/p Spearman se merge >=3. |
| Efeitos | sem escrita; método técnico chama pandas.to_markdown; não salva relatório. |
| Dependências e momento de uso | numpy/pandas topo; tabulate requerido indiretamente por to_markdown; scipy.stats import no ramo nativo. |
| Como interpretar este arquivo | O relatório formata importância já calculada; não calcula SHAP, causalidade ou efeito de intervenção. A direção por correlação e o rank Spearman só fazem sentido com arrays alinhados; tabulate e SciPy podem ser exigidos em ramos distintos. Entrada: DataFrame com feature/pct_importance; nomes negócio/target/métrica; arrays opcionais alinhados para correlação; importância nativa opcional com ranks. Saída: duas strings Markdown; direção por correlação Pearson quando arrays; rho/p Spearman se merge >=3. Efeitos da chamada: sem escrita; método técnico chama pandas.to_markdown; não salva relatório. Dependências: numpy/pandas topo; tabulate requerido indiretamente por to_markdown; scipy.stats import no ramo nativo. |

<a id="mt10-mt11-code-map-file-028"></a>
#### 28. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/metrics_report/__init__.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/__init__.py` · SHA-256 `552c785d512c611db8b7914e3db26efc524261288020a6a6787263d7bf7117c8` |
| Papel e motivo técnico | Calcular métricas com população e escala declaradas, sem definir decisão. |
| Nomes disponibilizados | calculate_binary_metrics, calculate_regression_metrics |
| Entradas | import da fachada; contrato da implementação: calculate_binary_metrics(y_true,y_prob,threshold=.5); calculate_regression_metrics(y_true,y_pred) |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | numpy/sklearn topo; scipy.stats import interno para ks_2samp. |
| Como interpretar este arquivo | A fachada reexporta calculate_binary_metrics, calculate_regression_metrics; importar o pacote carrega as dependências de topo (numpy/sklearn topo; scipy.stats import interno para ks_2samp.), mas não chama a operação. Métricas exigem população, limiar e escala declarados. KS bilateral sai de 0 a 100, diferente do KS visual fracionário; MAPE ignora y_true=0 e vira NaN se todos forem zero. A docstring do módulo de implementação `metrics_report.py` cita `format_metrics_table`, que não é exportado; a fachada não possui essa docstring. |

<a id="mt10-mt11-code-map-file-029"></a>
#### 29. `exemplo_metrics_report.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/metrics_report/exemplo_metrics_report.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/exemplo_metrics_report.py` · SHA-256 `9d72bb84262bd7dbc94cfb3950c2178a40bbd8d088b07e35f1c8b344f1f10a52` |
| Papel e motivo técnico | Calcular métricas com população e escala declaradas, sem definir decisão. |
| Nomes disponibilizados | notebook fonte Databricks que importa e chama somente calculate_binary_metrics; calculate_regression_metrics é API relacionada do módulo, sem demonstração nesta fonte |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | o notebook gera y binário e scores p sintéticos alinhados, depois chama a métrica binária com o corte padrão e com quatro thresholds; não fornece alvo ou predição de regressão |
| Saídas | Notebook simula 5% eventos, compara quatro limiares; impressos históricos, sem escrita. |
| Efeitos | efeitos da célula: Notebook simula 5% eventos, compara quatro limiares; impressos históricos, sem escrita. Efeitos do helper chamado: somente cálculos locais; nenhum arquivo/MLflow. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: numpy/sklearn topo; scipy.stats import interno para ks_2samp. |
| Como interpretar este arquivo | O exemplo compara precisão, recall e F1 sob quatro cortes da mesma base binária; seu KS bilateral sai em pontos percentuais, diferente do KS visual fracionário. `calculate_regression_metrics` e seu MAPE pertencem à implementação relacionada, mas não são chamados aqui. A docstring do módulo de implementação `metrics_report.py` menciona `format_metrics_table`, que não é exportado; a fachada não possui essa docstring. Os números impressos descrevem o ensaio histórico com 5% de eventos simulados; não são medição atual nem decisão de negócio. |

<a id="mt10-mt11-code-map-file-030"></a>
#### 30. `metrics_report.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/metrics_report/metrics_report.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/metrics_report/metrics_report.py` · SHA-256 `78d26f18e2c9fb25148fad1a76e6a946b884c66936b432bec47e698106d8c38a` |
| Papel e motivo técnico | Calcular métricas com população e escala declaradas, sem definir decisão. |
| Nomes disponibilizados | calculate_binary_metrics(y_true,y_prob,threshold=.5); calculate_regression_metrics(y_true,y_pred) |
| Entradas | arrays 1D finitos; binário 0/1 ambas classes/scores [0,1]; regressão mesmo comprimento; threshold [0,1]. |
| Saídas | dict binário auc_roc/ks_pct/gini/auc_pr/brier_score/f1/precision/recall/lift_10pct/prevalence; regressão rmse/mae/mape/r2. |
| Efeitos | somente cálculos locais; nenhum arquivo/MLflow. |
| Dependências e momento de uso | numpy/sklearn topo; scipy.stats import interno para ks_2samp. |
| Como interpretar este arquivo | Métricas exigem população, limiar e escala declarados. KS bilateral sai de 0 a 100, diferente do KS visual fracionário; MAPE ignora y_true=0 e vira NaN se todos forem zero. A docstring do módulo de implementação `metrics_report.py` cita `format_metrics_table`, que não é exportado; a fachada não possui essa docstring. Entrada: arrays 1D finitos; binário 0/1 ambas classes/scores [0,1]; regressão mesmo comprimento; threshold [0,1]. Saída: dict binário auc_roc/ks_pct/gini/auc_pr/brier_score/f1/precision/recall/lift_10pct/prevalence; regressão rmse/mae/mape/r2. Efeitos da chamada: somente cálculos locais; nenhum arquivo/MLflow. Dependências: numpy/sklearn topo; scipy.stats import interno para ks_2samp. |

<a id="mt10-mt11-code-map-file-031"></a>
#### 31. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/mlflow_run/__init__.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/__init__.py` · SHA-256 `182b6b8946afe0fe61ccfb72f8157cc8ff36048d74510753d9511cf423388d9e` |
| Papel e motivo técnico | Rastrear dataset/split/limitações e exigir registros mínimos, distinguindo run de aprovação/publicação. |
| Nomes disponibilizados | run_governado, run_micromodelo |
| Entradas | import da fachada; contrato da implementação: run_governado(nome,*,dataset,split,limitacoes,experimento=None,exigir_completo=True); coletor.parametros/metricas/modelo/artefato/pendencias; run_micromodelo(nome,*,tipo,spec_fingerprint,dataset,split,limitacoes,contrato_saida,experimento=None); coletor MM06.parametros/agregados_medidos/pendencias |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | mlflow tem import protegido no topo e é exigido na entrada de ambos os contextos; backend/tracking externo. Somente modelo no coletor legado resolve o flavor sklearn na chamada; run_micromodelo não registra modelo. |
| Como interpretar este arquivo | A fachada reexporta run_governado e run_micromodelo; importar o pacote carrega as dependências de topo (mlflow import protegido no topo, exigido ao chamar; sklearn flavor MLflow na chamada; backend/tracking externo.), mas não chama a operação. O contexto registra dataset, split e limitações, mas um run não aprova nem publica modelo. Não define nested=True nem troca backend; no legado run_governado, uma string não vazia em limitacoes é iterável de caracteres, então use coleção de frases. A nova operação run_micromodelo recusa str/bytes isolados, exige contexto sintético declarado e não oferece modelo, artefato ou exigir_completo. |
| Ampliação atual da API | run_micromodelo cede _RunMicromodelo ao entrar no contexto; validação e logging não acontecem pelo simples import. Campos, fechamento e limites estão no [contrato ampliado](MT-mt10-current-api-additions-map.md#mt10-current-api-additions-map). |

<a id="mt10-mt11-code-map-file-032"></a>
#### 32. `exemplo_mlflow_run.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/exemplo_mlflow_run.py` · SHA-256 `69b5a0f3684223f4a5a835ad2ee1cfc7fb63e09c670540bb571f092d2a18de65` |
| Papel e motivo técnico | Rastrear dataset/split/limitações e exigir registros mínimos, distinguindo run de aprovação/publicação. |
| Nomes disponibilizados | notebook fonte Databricks que chama `run_governado`; no bloco completo, chama apenas `run.parametros`, `run.metricas` e `run.modelo`. `artefato` e `pendencias` pertencem à API relacionada, não às células deste exemplo |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | primeiro pedido com `limitacoes=""` para demonstrar recusa; depois dados sintéticos, LogisticRegression treinada, nome/dataset/split e lista de limitações, com `X[:2]` como exemplo de entrada do modelo; nenhum caminho de arquivo para artefato |
| Saídas | Notebook testa limitações vazias, treina LogisticRegression sintética e tenta registrar run. Conserva AnalysisException de configuração no ensaio Free de 17/08/2026; esse registro não determina suporte no runtime atual. |
| Efeitos | O notebook testa a recusa de limitações vazias, treina LogisticRegression e tenta registrar parâmetros, métrica e modelo com mlflow.sklearn.log_model. Não chama run.artefato nem log_artifact. O try cobre entrada, logs e fechamento: a mensagem do except não prova ausência de persistência. Consulte o backend antes de repetir uma execução autorizada, pois uma falha posterior à abertura pode deixar registros parciais. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: mlflow import protegido no topo, exigido ao chamar; sklearn flavor MLflow na chamada; backend/tracking externo. |
| Como interpretar este arquivo | O contexto exige dataset, split e limitações, mas um run não aprova nem publica modelo. A primeira chamada usa texto vazio para provocar recusa; run.modelo depende do flavor sklearn na chamada. Uma string não vazia em limitacoes seria iterável por caractere no legado; use lista de frases. A fonte preserva a exceção CONFIG_NOT_AVAILABLE.WITHOUT_SUGGESTION referente a spark.mlflow.modelRegistryUri, datada de 17/08/2026. O except Exception envolve todo o bloco e imprime “o run não abriu neste runtime” mesmo quando uma falha ocorre depois de logs; essa frase não localiza o erro nem comprova que nada persistiu. A observação histórica não é regra universal do Free. O exemplo não usa run_micromodelo. |

<a id="mt10-mt11-code-map-file-033"></a>
#### 33. `mlflow_run.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/mlflow_run/mlflow_run.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/mlflow_run/mlflow_run.py` · SHA-256 `230043dfaba0284042efcd4e7f40bc9795d7f68cbca2e2c50b375f0272a59a16` |
| Papel e motivo técnico | Rastrear dataset/split/limitações e exigir registros mínimos, distinguindo run de aprovação/publicação. |
| Nomes disponibilizados | run_governado(nome,*,dataset,split,limitacoes,experimento=None,exigir_completo=True); coletor.parametros/metricas/modelo/artefato/pendencias; run_micromodelo(nome,*,tipo,spec_fingerprint,dataset,split,limitacoes,contrato_saida,experimento=None); coletor MM06.parametros/agregados_medidos/pendencias |
| Entradas | No legado run_governado: nome/dataset/split não vazios; limitações iteráveis não vazias; modelo sklearn com exemplo_entrada se assinatura exigida; arquivo local para artefato. |
| Saídas | Contextos cedem _RunGovernado ou _RunMicromodelo; métodos de registro retornam None e pendencias retorna lista. O fechamento normal pode levantar ValueError após logs já persistidos. |
| Efeitos | Ambos podem selecionar experimento, abrir run e persistir tags/parâmetros/métricas. Só o coletor legado oferece modelo/artefato; MM06 admite agregados e não implementa Registry, publicação ou predição individual. Nenhum contexto faz rollback dos logs. |
| Dependências e momento de uso | mlflow tem import protegido no topo e é exigido na entrada de ambos os contextos; backend/tracking externo. Somente modelo no coletor legado resolve o flavor sklearn na chamada; run_micromodelo não registra modelo. |
| Como interpretar este arquivo | No legado run_governado, o contexto registra dataset, split e limitações, mas um run não aprova nem publica modelo. Não define nested=True nem troca backend; uma string não vazia em limitacoes é iterável de caracteres, então use coleção de frases. Entrada: nome/dataset/split não vazios; limitações iteráveis não vazias; modelo sklearn com exemplo_entrada se assinatura exigida; arquivo local para artefato. Saída: Contextos cedem _RunGovernado ou _RunMicromodelo; métodos de registro retornam None e pendencias retorna lista. O fechamento normal pode levantar ValueError após logs já persistidos. Efeitos da chamada: set_experiment opcional, start_run, tags, log_params/log_metrics/log_model/log_artifact persistem; sem rollback no erro posterior. Dependências: mlflow import protegido no topo, exigido ao chamar; sklearn flavor MLflow na chamada; backend/tracking externo. |
| Entradas e fechamento MM06 | tipo deve ser DEVELOPMENT, VALIDATION ou SCORING; fingerprint tem formato lowercase 64-hex; dataset e split começam por synthetic:. São declarações, não verificação de YAML ou detecção de dados reais. Há 1–20 limitações e contrato_saida fechado de cinco campos. O coletor valida parâmetros permitidos e contagens reconciliadas, exige parametros e agregados_medidos na saída normal e rejeita mutações após fechar; não tem bypass exigir_completo. Consulte [campos, agregados e falhas](MT-mt10-current-api-additions-map.md#mt10-current-api-additions-map). |

<a id="mt10-mt11-code-map-file-034"></a>
#### 34. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/performance_monitor/__init__.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
[Dependência visual transitiva](../../hub_snippets/visual/theme_plotly/theme_plotly.py)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/__init__.py` · SHA-256 `14c33b8e31ae993a7ed36c7669c98e1c2bba2acf628af96700dd22b8e59d4121` |
| Papel e motivo técnico | Monitor em memória com política explícita, alias auc_roc→auc e ks_pct mantido em pontos. |
| Nomes disponibilizados | AZUL_CAIXA, LARANJA, VERMELHO, EXAMPLE_THRESHOLDS, CHAVES_DO_RELATORIO, selecionar_metricas_do_relatorio, PerformanceMonitor |
| Entradas | import da fachada; contrato da implementação: EXAMPLE_THRESHOLDS/CHAVES_DO_RELATORIO; selecionar_metricas_do_relatorio; PerformanceMonitor(...).add_period/get_current_status/should_retrain/generate_report/plot_timeline/plot_timeline_resolvido |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | Cores e tema do Hub no topo; `theme_plotly` importa `plotly.io` e `graph_objects` no topo, tornando Plotly dependência transitiva já no import do monitor. `plot_timeline` também tem import local; sem MLflow. |
| Como interpretar este arquivo | A fachada reexporta AZUL_CAIXA, LARANJA, VERMELHO, EXAMPLE_THRESHOLDS, CHAVES_DO_RELATORIO, selecionar_metricas_do_relatorio, PerformanceMonitor; importar o pacote carrega as dependências de topo (Cores e tema do Hub no topo; `theme_plotly` importa `plotly.io` e `graph_objects` no topo, tornando Plotly dependência transitiva já no import do monitor. `plot_timeline` também tem import local; sem MLflow.), mas não chama a operação. O monitor mantém histórico em memória e aplica policy explícita; auc_roc é alias de auc, e ks_pct permanece em pontos. NO_EVIDENCE não contém automatic_retrain_authorized; nenhum método retreina, e as demais decisões mantêm a autorização automática falsa. |

<a id="mt10-mt11-code-map-file-035"></a>
#### 35. `exemplo_performance_monitor.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/performance_monitor/exemplo_performance_monitor.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
[Dependência visual transitiva](../../hub_snippets/visual/theme_plotly/theme_plotly.py)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/exemplo_performance_monitor.py` · SHA-256 `44a47e72183325b63ec9ee690958cdde3907706d237d2ac1a3849eef21374173` |
| Papel e motivo técnico | Monitor em memória com política explícita, alias auc_roc→auc e ks_pct mantido em pontos. |
| Nomes disponibilizados | notebook fonte Databricks que importa `EXAMPLE_THRESHOLDS` e `PerformanceMonitor`, depois chama `add_period`, `generate_report`, `get_current_status` e `should_retrain`; seleção de métricas e plots são APIs relacionadas, não chamadas aqui |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | baseline sintético `auc=0.78`, `EXAMPLE_THRESHOLDS` de demonstração, nome do modelo e oito meses de AUCs; a policy inclui direção e delta, mas não foi calibrada para produção |
| Saídas | Notebook cria série de 8 AUCs e imprime status/recomendação; não chama selecionar_metricas nem plot_timeline; saídas históricas. |
| Efeitos | as células imprimem limites de exemplo, acrescentam oito períodos a histórico em memória e imprimem relatório, status e indicação de investigação; não chamam seleção de métricas, Plotly, persistência nem retreino. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: o notebook importa NumPy/pandas e a fachada do monitor; a implementação carrega cores/tema do Hub. Plotly já é dependência transitiva do import, via `theme_plotly`, embora o notebook não chame a rota de gráfico; não há MLflow. |
| Como interpretar este arquivo | O monitor compara a série com uma policy explícita, mas os valores de `EXAMPLE_THRESHOLDS` são didáticos e não aprovados para outro modelo. `auc_roc` como alias de `auc`, `ks_pct` em pontos e `selecionar_metricas_do_relatorio` são capacidades relacionadas da implementação, não operações demonstradas nas células. `should_retrain()` sugere investigação e não autoriza retreino automático; as saídas impressas pertencem ao ensaio histórico. |
| Leitura do comentário atual | O comentário atual orienta metricas_obrigatorias para exigir auc e ks_pct na seleção. Valores inválidos selecionados geram erro; exclusão deliberada exige política sem a chave. O antigo ks já estava em 0–100: ao adotar ks_pct, preserve o número sem multiplicar nem dividir por 100. Essa seleção não é chamada neste notebook. |

<a id="mt10-mt11-code-map-file-036"></a>
#### 36. `performance_monitor.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/performance_monitor/performance_monitor.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-2)
[Dependência visual transitiva](../../hub_snippets/visual/theme_plotly/theme_plotly.py)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/performance_monitor/performance_monitor.py` · SHA-256 `1686810d97f0e1eef406c71d47d3bdbb9ac862fac6ca7f96a401eeb3c0b65f21` |
| Papel e motivo técnico | Monitor em memória com política explícita, alias auc_roc→auc e ks_pct mantido em pontos. |
| Nomes disponibilizados | EXAMPLE_THRESHOLDS/CHAVES_DO_RELATORIO; selecionar_metricas_do_relatorio; PerformanceMonitor(...).add_period/get_current_status/should_retrain/generate_report/plot_timeline/plot_timeline_resolvido |
| Entradas | baseline finito coberto pela policy; thresholds/direction/delta válidos; períodos com métricas finitas e completude configurada. |
| Saídas | status textual, Markdown, figuras Plotly; should_retrain NO_EVIDENCE/NO_TRIGGER/INVESTIGATE_RETRAINING_CANDIDATE. |
| Efeitos | histórico apenas em memória; Plotly carregado transitivamente no import; nenhum agendador/persistência/retrain callback. |
| Dependências e momento de uso | Cores e tema do Hub no topo; `theme_plotly` importa `plotly.io` e `graph_objects` no topo, tornando Plotly dependência transitiva já no import do monitor. `plot_timeline` também tem import local; sem MLflow. |
| Como interpretar este arquivo | O monitor mantém histórico em memória e aplica policy explícita; auc_roc é alias de auc, e ks_pct permanece em pontos. NO_EVIDENCE não contém automatic_retrain_authorized; nenhum método retreina, e as demais decisões mantêm a autorização automática falsa. Entrada: baseline finito coberto pela policy; thresholds/direction/delta válidos; períodos com métricas finitas e completude configurada. Saída: status textual, Markdown, figuras Plotly; should_retrain NO_EVIDENCE/NO_TRIGGER/INVESTIGATE_RETRAINING_CANDIDATE. Efeitos da chamada: histórico apenas em memória; Plotly carregado transitivamente no import; nenhum agendador/persistência/retrain callback. Dependências: Cores e tema do Hub no topo; `theme_plotly` importa `plotly.io` e `graph_objects` no topo, tornando Plotly dependência transitiva já no import do monitor. `plot_timeline` também tem import local; sem MLflow. |

<a id="mt10-mt11-code-map-file-037"></a>
#### 37. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/shap_explainer/__init__.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/__init__.py` · SHA-256 `115ae0d664b59656d630540f2c43ae714c5b6db8d3abcc7f10b5b4af26f50243` |
| Papel e motivo técnico | Explicar saída/classe/escala de modelo específico e alinhar IDs às linhas selecionadas. |
| Nomes disponibilizados | SEED, compute_shap, get_feature_importance_shap, plot_shap_global, plot_shap_local |
| Entradas | import da fachada; contrato da implementação: SEED; compute_shap(model,X,feature_names,model_type="tree",max_samples=5000,*,task="classification",output_index=None,background=None); get_feature_importance_shap; plot_shap_global/local |
| Saídas | reexports de objetos públicos sem cálculo próprio |
| Efeitos | importa implementação e dependências top-level; não chama função nem registra artefato |
| Dependências e momento de uso | numpy/pandas topo; shap import na compute/plots, matplotlib nos plots. |
| Como interpretar este arquivo | A fachada reexporta SEED, compute_shap, get_feature_importance_shap, plot_shap_global, plot_shap_local; importar o pacote carrega as dependências de topo (numpy/pandas topo; shap import na compute/plots, matplotlib nos plots.), mas não chama a operação. SHAP deve ser ligado ao modelo, classe, escala e IDs alinhados às linhas escolhidas. output_index=1 só seleciona classe quando o retorno realmente tem múltiplas saídas; em matriz 2D não seleciona classe. Salvar plot é efeito persistente opcional. |
| Referência SHAP linear | background explícito só é aceito em model_type="linear": precisa ser matriz 2D com pelo menos uma linha, mesmo número de colunas de X e valores numéricos finitos; violações geram ValueError. None mantém X como referência de LinearExplainer. O helper genérico não exige uma linha única; essa restrição pertence ao perfil B1 LINEAR_REGRESSION_SYNTHETIC_V1. Veja [referência e limites da API](MT-mt10-current-api-additions-map.md#mt10-current-api-additions-map). |

<a id="mt10-mt11-code-map-file-038"></a>
#### 38. `exemplo_shap_explainer.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/shap_explainer/exemplo_shap_explainer.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/exemplo_shap_explainer.py` · SHA-256 `af31216a8b0195958736593da5485613cf2813d827e86aa91bb5c35151c6b1b4` |
| Papel e motivo técnico | Explicar saída/classe/escala de modelo específico e alinhar IDs às linhas selecionadas. |
| Nomes disponibilizados | notebook fonte Databricks que importa e chama somente `compute_shap` e `get_feature_importance_shap`; `plot_shap_global`, `plot_shap_local` e ramo Kernel são APIs relacionadas, não demonstradas por chamada |
| Preparação da sessão | Antes do import do Hub, executa `spark.sql("SELECT current_user()").first()` para formar o caminho e o inserir em `sys.path`. Essa ação requer uma sessão Spark, mesmo quando o helper calcula no driver; não lê tabela de negócio. |
| Entradas | 3.000 linhas sintéticas e cinco nomes alinhados, RandomForestClassifier treinado; `compute_shap` recebe `model_type="tree"` e `output_index=1` para selecionar a classe positiva no retorno de duas saídas, sem `save_path` nem chamada do ramo Kernel |
| Saídas | Notebook instala shap==0.44.1, treina RandomForest sintética, TreeSHAP 3000 linhas com output_index=1; max_samples inerte; não chama plots. |
| Efeitos | o notebook tenta instalar `shap==0.44.1` e reiniciar Python, treina RandomForest sintética, calcula TreeSHAP para 3.000 linhas e imprime importância. Não chama plots, não passa `save_path` nem grava arquivo. O limite `max_samples` não reduz o ramo tree. |
| Dependências e momento de uso | A preparação do notebook requer a sessão Spark descrita acima. Dependências da operação demonstrada: `%pip` muda a sessão; após `%restart_python`, o notebook recompõe `sys.path`, importa NumPy/sklearn e a fachada SHAP. A dependência SHAP é resolvida na chamada; Matplotlib dos plots não é usado aqui. |
| Como interpretar este arquivo | O exemplo liga as contribuições ao modelo e à classe selecionada por `output_index=1`; essa seleção só faz sentido quando o retorno tem saídas distintas. A importância global ordena as variáveis desta fixture, mas valor pequeno e não nulo não prova sinal causal. O ramo Kernel pode subamostrar e os plots podem salvar imagens na implementação relacionada; nada disso é chamado nesta fonte. Os números e prints colados são históricos, não uma execução atual. |

<a id="mt10-mt11-code-map-file-039"></a>
#### 39. `shap_explainer.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/shap_explainer/shap_explainer.py) · [MT10: explicação do mecanismo](MT-parte-ii.md#mt10-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/ml/shap_explainer/shap_explainer.py` · SHA-256 `251ee374d851fa4aa5419c619fa1e45fef9cbd8457f5c5574246ad29ebd97600` |
| Papel e motivo técnico | Explicar saída/classe/escala de modelo específico e alinhar IDs às linhas selecionadas. |
| Nomes disponibilizados | SEED; compute_shap(model,X,feature_names,model_type="tree",max_samples=5000,*,task="classification",output_index=None,background=None); get_feature_importance_shap; plot_shap_global/local |
| Entradas | X e nomes alinhados; output_index exigido só em multioutput real; kernel pode subamostrar; plot local idx/arrays alinhados/save_path autorizado. |
| Saídas | compute_shap -> (matriz linhas×features, base_value float); importance DataFrame; plots retornam None e fecham figura. |
| Efeitos | SHAP fit/cálculo e prints; kernel subamostra sem devolver IDs; plots podem gravar em save_path, sem show explícito. |
| Dependências e momento de uso | numpy/pandas topo; shap import na compute/plots, matplotlib nos plots. |
| Como interpretar este arquivo | SHAP deve ser ligado ao modelo, classe, escala e IDs alinhados às linhas escolhidas. output_index=1 só seleciona classe quando o retorno realmente tem múltiplas saídas; em matriz 2D não seleciona classe. Salvar plot é efeito persistente opcional. Entrada: X e nomes alinhados; output_index exigido só em multioutput real; kernel pode subamostrar; plot local idx/arrays alinhados/save_path autorizado. Saída: compute_shap -> (matriz linhas×features, base_value float); importance DataFrame; plots retornam None e fecham figura. Efeitos da chamada: SHAP fit/cálculo e prints; kernel subamostra sem devolver IDs; plots podem gravar em save_path, sem show explícito. Dependências: numpy/pandas topo; shap import na compute/plots, matplotlib nos plots. |
| Referência SHAP linear | background explícito só é aceito em model_type="linear": precisa ser matriz 2D com pelo menos uma linha, mesmo número de colunas de X e valores numéricos finitos; violações geram ValueError. None mantém X como referência de LinearExplainer. O helper genérico não exige uma linha única; essa restrição pertence ao perfil B1 LINEAR_REGRESSION_SYNTHETIC_V1. Veja [referência e limites da API](MT-mt10-current-api-additions-map.md#mt10-current-api-additions-map). |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
