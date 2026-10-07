# Leitura dos arquivos Spark e estatísticos

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt07-mt08-code-map"></a>
<a id="mt07-mt08-code-map"></a>
### Leitura dos arquivos Spark e estatísticos

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Reconciliado com a fonte de 07/10/2026: 49 arquivos, 39 com bytes preservados e 10 com alterações em comentários de notebook. As fichas conservam o mérito das leituras anteriores; os comentários alterados foram confrontados com a implementação. Os hashes abaixo identificam os arquivos atuais. Isso não representa reexecução dos exemplos nem homologação de runtime.

<a id="mt07-mt08-code-map-file-001"></a>
#### 1. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/drift_detection/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/drift_detection/__init__.py` · SHA-256 `7a9c6c0a658041bd80d3d05069d9ab20bcdb8d89935e40b35961636cf9031a56` |
| Papel e motivo técnico | Expor a API pública da pasta drift_detection por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["MISSING_CATEGORY", "calculate_psi", "calculate_ks", "calculate_csi", "detect_drift_all_features"] |
| Entradas | Importação Python from hub_snippets.ml.drift_detection import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: MISSING_CATEGORY, calculate_psi, calculate_ks, calculate_csi, detect_drift_all_features. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: numpy, pandas, scipy.stats.ks_2samp. |
| Como interpretar este arquivo | A importação da pasta publica MISSING_CATEGORY e quatro funções de deriva; ela carrega drift_detection.py e as dependências pandas, NumPy e SciPy, mas não calcula PSI, KS ou CSI. Quem quer apenas localizar a API pode usar esta fachada; os custos de dados e os limiares pertencem às funções chamadas. |

<a id="mt07-mt08-code-map-file-002"></a>
#### 2. drift_detection.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/drift_detection/drift_detection.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/drift_detection/drift_detection.py` · SHA-256 `eabf3b4159702862b88aa4f15f87b6667e9f09363cdfaffeb0c7c7d5ec789f6c` |
| Papel e motivo técnico | Medir deriva local numérica/categórica e separar evidência de classificação por política. |
| Nomes disponibilizados | ["calculate_psi", "calculate_ks", "calculate_csi", "detect_drift_all_features"] |
| Entradas | Arrays NumPy ou Series/DataFrames pandas de referência/atual; features e limiares opcionais. |
| Saídas | PSI, KS com p-valor, CSI ou DataFrame de varredura com status. |
| Efeitos | Computação local no driver; não chama Spark nem grava; CSI usa sentinela textual que pode colidir com categoria real. |
| Dependências e momento de uso | numpy, pandas, scipy.stats.ks_2samp. |
| Como interpretar este arquivo | calculate_psi compara distribuições numéricas, calculate_ks aplica o teste de Kolmogorov–Smirnov e calculate_csi compara categorias; detect_drift_all_features monta a varredura em pandas no driver. A sentinela de categoria ausente pode colidir com um valor real. Um status por limiar é regra escolhida para o caso, não prova de perda de performance ou causa do drift. |

<a id="mt07-mt08-code-map-file-003"></a>
#### 3. exemplo_drift_detection.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/drift_detection/exemplo_drift_detection.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/drift_detection/exemplo_drift_detection.py` · SHA-256 `a917e1ee14441856a8f31cfb7056acaa02abeca8317fe9a96a243582badb8ef4` |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar drift_detection; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Gera arrays/Series pandas sintéticos, calcula PSI/KS/CSI e duas varreduras, imprime saídas históricas; usa Spark só para current_user/import path, sem gravação. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; import numpy as np; import pandas as pd; from hub_snippets.ml.drift_detection import ( |
| Como interpretar este arquivo | O notebook monta referência e período atual sintéticos, chama os cálculos locais e mostra como ler o resultado. Suas saídas coladas pertencem à execução histórica do exemplo; copiar a célula para outra base exige medir população, bins e limiares de novo. Não há escrita persistente de dados no roteiro, mas a chamada transfere o pequeno conjunto de teste para bibliotecas locais. |

<a id="mt07-mt08-code-map-file-004"></a>
#### 4. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/kaplan_meier/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/kaplan_meier/__init__.py` · SHA-256 `6946860eb60cb64abff5a7c23b97b95dee09e26aa27d18465bdd44097aec82c9` |
| Papel e motivo técnico | Expor a API pública da pasta kaplan_meier por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["plot_kaplan_meier", "log_rank_test"] |
| Entradas | Importação Python from hub_snippets.ml.kaplan_meier import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: plot_kaplan_meier, log_rank_test. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pandas, numpy, plotly, cores Hub; lifelines importado nas chamadas. |
| Como interpretar este arquivo | A fachada expõe as funções de curva de Kaplan–Meier e comparação por grupos do módulo vizinho. Importá-la carrega as dependências de topo, sem ajustar sobrevivência; lifelines é importado dentro das funções, na chamada. A análise só começa quando o consumidor fornece duração, indicador de evento e, se necessário, grupo; a presença do nome no pacote não resolve censura ou desenho de coorte. |

<a id="mt07-mt08-code-map-file-005"></a>
#### 5. exemplo_kaplan_meier.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/kaplan_meier/exemplo_kaplan_meier.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/kaplan_meier/exemplo_kaplan_meier.py` · SHA-256 `a670dd2248f48049214eee3756057447ed75f090c62a5fc5288e8ce55db1d555` |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar kaplan_meier; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Instala lifelines via %pip e reinicia Python, depois gera 800 casos sintéticos, figura.show e log-rank; current_user + sys.path após restart; sem dados externos. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Instala biblioteca e reinicia Python na sessão. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; import numpy as np; from hub_snippets.ml.kaplan_meier import log_rank_test, plot_kaplan_meier; import pandas as pd |
| Como interpretar este arquivo | O exemplo cria duração e evento sintéticos para desenhar sobrevivência e comparar grupos. Suas células %pip instalam dependência e reiniciam Python na sessão Databricks, efeito ambiental real que depende da política do workspace. Depois do reinício, os imports e variáveis precisam ser restabelecidos; números do notebook são demonstração histórica, não uma estimativa para outra população. |

<a id="mt07-mt08-code-map-file-006"></a>
#### 6. kaplan_meier.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/kaplan_meier/kaplan_meier.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/kaplan_meier/kaplan_meier.py` · SHA-256 `e89b63f89b17cf09d9eb3b58c56168a6196ed09c6a7d5e281a26ab64f01f9c3d` |
| Papel e motivo técnico | Estimar curvas de sobrevivência com censura e comparar grupos por log-rank. |
| Nomes disponibilizados | ["plot_kaplan_meier", "log_rank_test"] |
| Entradas | DataFrame pandas com duração/evento; grupo, título, intervalo de confiança opcionais. |
| Saídas | Figura Plotly; estatística/p-valor ou dicionário global + pares com Holm. |
| Efeitos | Ajusta lifelines em memória; log_rank_test para dois grupos imprime leitura 0,05; não grava. |
| Dependências e momento de uso | pandas, numpy, plotly, cores Hub; lifelines importado nas chamadas. |
| Como interpretar este arquivo | A implementação ajusta curva de Kaplan–Meier sob censura: uma linha sem evento informa sobrevivência até o último acompanhamento, sem ser tratada como evento. A comparação de dois grupos usa log-rank e uma leitura impressa em torno de 0,05; grupos múltiplos usam correção de Holm. As saídas são associações da amostra e pressupõem tempos/eventos válidos, sem afirmar efeito causal. |

<a id="mt07-mt08-code-map-file-007"></a>
#### 7. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/score_bands/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/score_bands/__init__.py` · SHA-256 `00765270e7afccfac442243d630f74ed959abab62bce46cb492e2d80f273138a` |
| Papel e motivo técnico | Expor a API pública da pasta score_bands por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["generate_score_bands"] |
| Entradas | Importação Python from hub_snippets.ml.score_bands import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: generate_score_bands. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: numpy, pandas. |
| Como interpretar este arquivo | A fachada reexporta somente `generate_score_bands`, definido em score_bands.py. O import carrega pandas, mas não ordena clientes nem escolhe política de aprovação. A direção de risco precisa ser declarada pelo chamador; esconder esse parâmetro atrás de um import curto não torna uma banda A comparável entre bases diferentes. |

<a id="mt07-mt08-code-map-file-008"></a>
#### 8. exemplo_score_bands.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/score_bands/exemplo_score_bands.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/score_bands/exemplo_score_bands.py` · SHA-256 `af191964bed68c6763dd22d4edee39bae3ac0a25150de275b4146692f2a15bb6` |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar score_bands; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Gera score sintético com piso e empates, mostra quatro bandas para cinco pedidas e inverte direção; current_user + sys.path, só impressão. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; import numpy as np; from hub_snippets.ml.score_bands import generate_score_bands |
| Como interpretar este arquivo | O notebook usa scores e eventos sintéticos para mostrar bandas quantílicas, taxa de evento e aprovação acumulada. Seus percentuais são saída histórica da amostra de demonstração. Em outra carteira, empates e distribuição de score podem mudar as bordas ou reduzir o número de faixas; a coluna de aprovação simulada não aplica uma decisão de crédito. |

<a id="mt07-mt08-code-map-file-009"></a>
#### 9. score_bands.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/score_bands/score_bands.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/score_bands/score_bands.py` · SHA-256 `3e0b91f4264d52b1399e733d1523fb8a83b92f7590781c3d6c8a2fabb0d38fdd` |
| Papel e motivo técnico | Ordenar score em bandas quantílicas pela direção de risco declarada. |
| Nomes disponibilizados | ["generate_score_bands"] |
| Entradas | Arrays NumPy de score e alvo binário, número de bandas, rótulos, higher_score_is_better. |
| Saídas | DataFrame pandas com limites, contagens, taxa de evento e cobertura cumulativa. |
| Efeitos | Computação local qcut; sem escrita; empates podem reduzir número de bandas. |
| Dependências e momento de uso | numpy, pandas. |
| Como interpretar este arquivo | O helper recebe score, evento e orientação de risco, ordena observações e usa qcut para propor faixas quantílicas locais. Se muitos scores empatam, as bordas colapsam e podem sair menos faixas que as pedidas; o consumidor deve mostrar as bordas efetivas. Taxas e aprovação acumulada descrevem a amostra, sem aprovar clientes nem fixar cortes universais. |

<a id="mt07-mt08-code-map-file-010"></a>
#### 10. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/scorecard_builder/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/scorecard_builder/__init__.py` · SHA-256 `ea64ff441ab69e7ddfd9cc66e2a37ab12acec5e9892a98b23363bb8fb77eb3c2` |
| Papel e motivo técnico | Expor a API pública da pasta scorecard_builder por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["build_scorecard"] |
| Entradas | Importação Python from hub_snippets.ml.scorecard_builder import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: build_scorecard. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: numpy, pandas; WOE de outra rota precisa ponte toPandas pequena e rename. |
| Como interpretar este arquivo | A fachada publica somente `build_scorecard` a partir de scorecard_builder.py; importá-la apenas disponibiliza a API e dependências locais. O ajuste logístico, a tabela de peso da evidência e a escolha de evento ocorrem fora dela. A convenção de sinal e a razão-base bom:mau continuam responsabilidade explícita do consumidor. |

<a id="mt07-mt08-code-map-file-011"></a>
#### 11. exemplo_scorecard_builder.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/scorecard_builder/exemplo_scorecard_builder.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/scorecard_builder/exemplo_scorecard_builder.py` · SHA-256 `0ba7463096bda52983d50a0d8d934f10f7fada9300baabf74e98c8125156031d` |
| Reconciliação dos comentários atuais | Delta MAGIC identifica saída abreviada sem tempo_woe; retorno completo exige conferir cada feature × faixa. Células preservadas. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar scorecard_builder; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Tabelas WOE pandas sintéticas e coeficientes fixos; imprime scorecard e relação pontos/odds; current_user + sys.path. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; import numpy as np; import pandas as pd; from hub_snippets.ml.scorecard_builder import build_scorecard |
| Como interpretar este arquivo | O exemplo liga coeficientes e faixas WoE sintéticas a pontos de scorecard. O código produziria linhas para tempo_woe, embora a saída histórica colada as omita; use a tabela calculada atual, não a transcrição antiga, para conferir completude. O notebook demonstra a conta local e não treina um modelo nem valida estabilidade de faixas. |

<a id="mt07-mt08-code-map-file-012"></a>
#### 12. scorecard_builder.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/scorecard_builder/scorecard_builder.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/scorecard_builder/scorecard_builder.py` · SHA-256 `215022c045c03ca52887834284aadaff65169dce1522576fbbabc46e115e15a8` |
| Papel e motivo técnico | Converter coeficientes logísticos e WOE por faixa em pontos com convenção de evento explícita. |
| Nomes disponibilizados | ["build_scorecard"] |
| Entradas | Coeficientes/nomes alinhados, intercepto, tabelas pandas faixa/woe, PDO, score/odds base, event_is_bad. |
| Saídas | DataFrame pandas de feature/faixa/woe/coef/pontos, não probabilidade. |
| Efeitos | Computação local, sem treinamento nem escrita; conversão da tabela WOE Spark é externa e deve ser limitada. |
| Dependências e momento de uso | numpy, pandas; WOE de outra rota precisa ponte toPandas pequena e rename. |
| Como interpretar este arquivo | A implementação converte coeficientes de regressão logística e WoE, peso da evidência por faixa, em pontos sob orientação de evento e escala PDO declaradas. Uma tabela WoE gerada em Spark precisa ser reduzida com limite antes da etapa pandas; essa transferência não acontece magicamente aqui. Pontos calculados são representação do modelo fornecido, não aprovação nem qualidade comprovada. |

<a id="mt07-mt08-code-map-file-013"></a>
#### 13. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/split_temporal/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/split_temporal/__init__.py` · SHA-256 `a9195d2c7c0f0a4391fd60c384e69f8b86c50026bedd5c0f5fcb35f340fa51a8` |
| Papel e motivo técnico | Expor a API pública da pasta split_temporal por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["temporal_split"] |
| Entradas | Importação Python from hub_snippets.ml.split_temporal import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: temporal_split. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pandas; sem Spark no helper. |
| Como interpretar este arquivo | A fachada publica `temporal_split` da implementação local. Seu import torna o nome acessível e carrega pandas, sem separar uma base ou observar suas datas. Os parâmetros de períodos, gaps e grupo só têm efeito na chamada; a API curta não garante que todos os splits permaneçam não vazios. |

<a id="mt07-mt08-code-map-file-014"></a>
#### 14. exemplo_split_temporal.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/split_temporal/exemplo_split_temporal.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/split_temporal/exemplo_split_temporal.py` · SHA-256 `8f24c66278201c9701c8796fe83f33d21a0b8f23aec05ee58eb13baf75a3f881` |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar split_temporal; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture Spark de 720 linhas é convertida integralmente a pandas no driver após limite sintético conhecido; prints de partições; current_user + sys.path. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.testing import fixtures; from hub_snippets.ml.split_temporal import temporal_split |
| Como interpretar este arquivo | O notebook demonstra treino, validação e teste por período sobre um painel sintético pequeno. Ele chama toPandas no painel inteiro antes do helper: aceitável pelo volume controlado do exemplo, perigoso para uma tabela distribuída real porque coleta tudo no driver. Antes de adaptar, limite e meça o dado; a proporção pedida é de períodos, não necessariamente de linhas. |

<a id="mt07-mt08-code-map-file-015"></a>
#### 15. split_temporal.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/split_temporal/split_temporal.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/split_temporal/split_temporal.py` · SHA-256 `0fb4192af2a6a8eb209a88d981a44a1a8bb20a803557500d84eeed072fda1bef` |
| Papel e motivo técnico | Separar períodos observados completos em treino, validação e teste com gaps opcionais. |
| Nomes disponibilizados | ["temporal_split"] |
| Entradas | DataFrame pandas, data, percentuais, gap, unidade de período e grupo opcional. |
| Saídas | Tupla de três DataFrames pandas ordenados, sem coluna temporária. |
| Efeitos | Cópias/filtros locais; datas nulas e gaps saem; group_col pode descartar entidades repetidas e esvaziar partições; não grava. |
| Dependências e momento de uso | pandas; sem Spark no helper. |
| Como interpretar este arquivo | O helper ordena períodos completos, reserva frações para treino, validação e teste e pode excluir gaps entre eles. Datas nulas e períodos de gap saem do resultado; a opção de grupo pode retirar entidades repetidas para evitar contaminação, até esvaziar um split. Ele opera em pandas e não ajusta pré-processamento: esse ajuste deve ocorrer dentro do treino de cada janela. |

<a id="mt07-mt08-code-map-file-016"></a>
#### 16. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/survival_cox/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/survival_cox/__init__.py` · SHA-256 `09d3b254cfe2f5d1b3231c7d65edde8acf88b2055894ecc596a226f6d40f2518` |
| Papel e motivo técnico | Expor a API pública da pasta survival_cox por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["SEED", "train_cox_ph", "validate_proportionality"] |
| Entradas | Importação Python from hub_snippets.ml.survival_cox import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: SEED, train_cox_ph, validate_proportionality. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pandas/numpy; lifelines sob demanda; mlflow opcional importado no módulo. |
| Como interpretar este arquivo | A fachada expõe o ajuste e a avaliação Cox do módulo local, carregando suas dependências no import. Ela não ajusta risco proporcional, registra MLflow ou testa pressupostos por mera importação. Duração, evento, covariáveis e opção de tracking precisam ser fornecidos à função concreta; o import não cria um experimento. |

<a id="mt07-mt08-code-map-file-017"></a>
#### 17. exemplo_survival_cox.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/survival_cox/exemplo_survival_cox.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/survival_cox/exemplo_survival_cox.py` · SHA-256 `9bb3c17148e1bd6ce95870e1e95c641ec10a183f23bdb24ca2a14bc8b1a97e91` |
| Reconciliação dos comentários atuais | Delta MAGIC remove proibição universal de MLflow no Free e ativação automática no trabalho: log_mlflow=False só desliga registro explícito; dependência, experimento, permissões, runtime e autologging precisam ser conferidos. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar survival_cox; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | %pip install lifelines e %restart_python; gera 1200 casos sintéticos; treina com log_mlflow=False, imprime métricas e teste; current_user + sys.path após restart. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Instala biblioteca e reinicia Python na sessão. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; import numpy as np; from hub_snippets.ml.survival_cox import train_cox_ph, validate_proportionality; import pandas as pd |
| Como interpretar este arquivo | O notebook prepara dados de sobrevivência sintéticos e invoca o ajuste Cox com log_mlflow=False. Também traz %pip e reinício Python, que mudam a sessão e podem exigir restabelecer imports e variáveis. O relatório mostrado é exemplo histórico; hazard ratio e concordância precisam ser recalculados na coorte real antes de qualquer interpretação. |

<a id="mt07-mt08-code-map-file-018"></a>
#### 18. survival_cox.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/survival_cox/survival_cox.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/survival_cox/survival_cox.py` · SHA-256 `75b4a5acc8969852fdcdee167e2e23fe32198c0dc54122d70bc01caa570ff8f8` |
| Papel e motivo técnico | Ajustar Cox para associação ao hazard sob censura e testar proporcionalidade. |
| Nomes disponibilizados | ["train_cox_ph", "validate_proportionality"] |
| Entradas | DataFrame pandas duração/evento/features, penalização, proporção L1 e flag MLflow; modelo/dados para teste. |
| Saídas | CoxPHFitter + métricas in-sample; DataFrame de teste por feature. |
| Efeitos | Ajusta e imprime resumo; com log_mlflow=True registra parâmetros/métricas ou lança ImportError após ajuste; sem escrita local própria. |
| Dependências e momento de uso | pandas/numpy; lifelines sob demanda; mlflow opcional importado no módulo. |
| Como interpretar este arquivo | A implementação ajusta Cox com lifelines, produz resumo e testa a hipótese de riscos proporcionais por resíduos de Schoenfeld. Concordância calculada no conjunto de ajuste é métrica in-sample, não desempenho externo. Se log_mlflow=True, registra parâmetros e métricas; se a dependência de tracking falta, pode lançar ImportError após ajustar. Assim, efeito remoto e resultado estatístico precisam ser distinguidos. |

<a id="mt07-mt08-code-map-file-019"></a>
#### 19. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/vintage_analysis/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/vintage_analysis/__init__.py` · SHA-256 `e25e2ca625092fe2e44a9b6ac887e9f30f6250b1d3a938b23dd40174ea0315c0` |
| Papel e motivo técnico | Expor a API pública da pasta vintage_analysis por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["PALETA_CATEGORICA", "AZUL_CAIXA", "PALETA_SEQUENCIAL", "TEMA_BASE", "build_vintage_table", "plot_vintage_curves", "plot_vintage_curves_resolvido", "plot_vintage_heatmap", "plot_vintage_heatmap_resolvido", "compare_safras"] |
| Entradas | Importação Python from hub_snippets.ml.vintage_analysis import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: PALETA_CATEGORICA, AZUL_CAIXA, PALETA_SEQUENCIAL, TEMA_BASE, build_vintage_table, plot_vintage_curves, plot_vintage_curves_resolvido, plot_vintage_heatmap, plot_vintage_heatmap_resolvido, compare_safras. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pandas/numpy, Plotly, cores Hub, ResolvedTheme/theme_plotly. |
| Como interpretar este arquivo | A fachada publica construção, comparação e figura de safras a partir de vintage_analysis.py; importá-la não lê contratos nem calcula MOB. O módulo de implementação carrega pandas/Plotly, enquanto a rota de enforcement tem contratos próprios e nível vigente definido pela policy. A API visível aqui não transforma automaticamente uma tabela sintética em safra de negócio validada. |

<a id="mt07-mt08-code-map-file-020"></a>
#### 20. exemplo_vintage_analysis.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/vintage_analysis/exemplo_vintage_analysis.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/vintage_analysis/exemplo_vintage_analysis.py` · SHA-256 `9d75b575946a2ec2e293b0302e8d23cf9b465ce15c6fb40bb95363a6c59213f6` |
| Reconciliação dos comentários atuais | Delta MAGIC troca cronologia por dependência atual: cores vêm de constants.colors; variantes resolvidas recebem tema explícito. Células preservadas. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar vintage_analysis; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture Spark de 600 contratos; groupBy/collect/count, depois painel.toPandas, datas sintéticas mob×30 dias, tabela/figuras sem show; current_user + sys.path. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.testing import fixtures; from hub_snippets.ml.vintage_analysis import build_vintage_table; import pandas as pd; from hub_snippets.ml.vintage_analysis import ( |
| Como interpretar este arquivo | O notebook monta coortes sintéticas e uma data observada derivada de mob×30 dias para satisfazer a entrada obrigatória. Essa aritmética não representa avanço em meses civis: não a reutilize para calendário de carteira. As curvas e taxas coladas são execução histórica local; em dado real, período, denominador e maturidade devem ser verificados de novo. |

<a id="mt07-mt08-code-map-file-021"></a>
#### 21. vintage_analysis.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/vintage_analysis/vintage_analysis.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/vintage_analysis/vintage_analysis.py` · SHA-256 `4740d1885d9fb7056c30c833f406141be12116034f58301e987954b8c1d72051` |
| Papel e motivo técnico | Calcular safra/MOB, maturidade, cobertura e taxa acumulada antes de plotar/comparar. |
| Nomes disponibilizados | ["build_vintage_table", "plot_vintage_curves", "plot_vintage_curves_resolvido", "plot_vintage_heatmap", "plot_vintage_heatmap_resolvido", "compare_safras"] |
| Entradas | DataFrame pandas de contratos/datas/evento; grão, MOB opcional e indicador de alvo acumulado. |
| Saídas | Tabela safra×MOB; figuras Plotly legadas/tematizadas; comparação por checkpoints. |
| Efeitos | Filtra MOB nulo/negativo; imprime resumo; constrói figuras sem mostrá-las nem gravar; tema explícito altera só aparência. |
| Dependências e momento de uso | pandas/numpy, Plotly, cores Hub, ResolvedTheme/theme_plotly. |
| Como interpretar este arquivo | A implementação filtra MOB ausente ou negativo, agrupa safra e mês desde originação, calcula cobertura/maturidade e taxa acumulada com denominador após filtro. Célula sem maturidade suficiente fica parcial, não zero. Plotar constrói figura e pode aplicar tema à aparência, mas não chama renderer nem grava; o leitor deve separar métrica observada de visualização exibida. |

<a id="mt07-mt08-code-map-file-022"></a>
#### 22. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/walk_forward/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/walk_forward/__init__.py` · SHA-256 `261a315bf0e1c58e79ed62726836df01078c7010395c10e06e5ee8f21e4af02e` |
| Papel e motivo técnico | Expor a API pública da pasta walk_forward por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["walk_forward_cv"] |
| Entradas | Importação Python from hub_snippets.ml.walk_forward import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: walk_forward_cv. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pandas, numpy; callback do consumidor. |
| Como interpretar este arquivo | A fachada reexporta o controlador de avaliação em janelas expansivas. O import carrega pandas e a implementação, mas não cria dobras, treina modelo ou chama callback. A escrita e o treinamento, se existirem, só podem entrar pelo callback fornecido mais tarde; esse limite torna o efeito dependente do consumidor. |

<a id="mt07-mt08-code-map-file-023"></a>
#### 23. exemplo_walk_forward.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/walk_forward/exemplo_walk_forward.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/walk_forward/exemplo_walk_forward.py` · SHA-256 `4bc2e0a27f6e006e51f8ea88f9acc16c59920cfae58ff95f54f90c8a08c9383a` |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar walk_forward; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Painel pandas de 24 meses × 200 casos; callback prevê média do treino e Brier; executa sem gap e com gap, imprime resultados históricos; current_user + sys.path. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; import numpy as np; import pandas as pd; from hub_snippets.ml.walk_forward import walk_forward_cv |
| Como interpretar este arquivo | O notebook cria uma série sintética, fornece callback de baseline e mostra Brier, média do quadrado entre probabilidade prevista e evento, por janela temporal. O callback do exemplo é parte da demonstração, não um modelo treinado pelo helper. Seus números são históricos e só dizem respeito aos períodos ilustrativos; outra série exige refazer splits, callback e avaliação. |

<a id="mt07-mt08-code-map-file-024"></a>
#### 24. walk_forward.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/walk_forward/walk_forward.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/walk_forward/walk_forward.py` · SHA-256 `fb8f2b1d1718de2de7fc0f4ae8cd41e30c6dd332a233af63de80ef503b2cce9a` |
| Papel e motivo técnico | Repetir avaliação temporal em janelas expansivas usando callback fornecido. |
| Nomes disponibilizados | ["walk_forward_cv"] |
| Entradas | DataFrame pandas, data/alvo, callback model_fn, períodos mínimos/teste, passo, gap e unidade. |
| Saídas | Lista de dicionários por dobra com métricas do callback e metadados de tempo/volume. |
| Efeitos | Chama callback em cada dobra e imprime média/desvio de métricas numéricas; qualquer escrita/treino vem do callback, não do helper. |
| Dependências e momento de uso | pandas, numpy; callback do consumidor. |
| Como interpretar este arquivo | O helper constrói dobras temporais expansivas com gap opcional e chama o callback recebido uma vez por dobra, passando treino e teste. Depois resume métricas numéricas em média e desvio. Não treina por conta própria: se o callback ajusta encoder, modelo ou grava algo, esse efeito ocorre dentro dele. Preparação aprendida deve ficar no treino de cada dobra para evitar vazamento. |

<a id="mt07-mt08-code-map-file-025"></a>
#### 25. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/woe_iv_calculator/__init__.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/woe_iv_calculator/__init__.py` · SHA-256 `885f4f2e809005247a810ef0afbdcabacf58382d9fa998a90dd983d4037e0275` |
| Papel e motivo técnico | Expor a API pública da pasta woe_iv_calculator por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["calculate_woe_iv", "classify_iv"] |
| Entradas | Importação Python from hub_snippets.ml.woe_iv_calculator import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: calculate_woe_iv, classify_iv. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql DataFrame/functions; consumidor precisa conversão pequena para scorecard pandas. |
| Como interpretar este arquivo | A fachada reexporta cálculo de WoE e IV da implementação Spark. O import disponibiliza o nome e pode carregar PySpark, mas não agrega bin algum. A função espera faixas já definidas e target binário; o pacote não escolhe discretização nem valida a convenção de classe por quem chama. |

<a id="mt07-mt08-code-map-file-026"></a>
#### 26. exemplo_woe_iv_calculator.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/woe_iv_calculator/exemplo_woe_iv_calculator.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/woe_iv_calculator/exemplo_woe_iv_calculator.py` · SHA-256 `cd1060cc0645f5abd638475024278b4eeadf4ce578d812fb8d0e50a9b32f07a8` |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar woe_iv_calculator; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture Spark de 3000 linhas; deriva faixa_renda de renda pelos cortes 5000 e 12000; deriva status_cobranca do alvo para ilustrar vazamento; show/print; current_user + sys.path. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.testing import fixtures; from hub_snippets.ml.woe_iv_calculator import calculate_woe_iv, classify_iv |
| Como interpretar este arquivo | O notebook prepara faixas e alvo sintéticos, chama o cálculo Spark e interpreta a tabela e o IV total. Um IV alto no exemplo pode apontar variável forte ou vazamento e pede investigação, não aceite automático. As células demonstram execução histórica, sem escrita persistente; refazer em outra população exige bins, classe de evento e tratamento de missing definidos. |

<a id="mt07-mt08-code-map-file-027"></a>
#### 27. woe_iv_calculator.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/ml/woe_iv_calculator/woe_iv_calculator.py) · [MT08: explicação do mecanismo](MT-parte-ii.md#mt08-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/ml/woe_iv_calculator/woe_iv_calculator.py` · SHA-256 `8e8733ab3ef88e51e0045afdde9f4bdb5fc0af3773d2b7471103707689ab6de7` |
| Papel e motivo técnico | Medir WOE por faixa e IV total para variável já discretizada com alvo binário. |
| Nomes disponibilizados | ["calculate_woe_iv", "classify_iv"] |
| Entradas | DataFrame Spark, coluna de faixa, alvo 0/1 e smoothing positivo. |
| Saídas | DataFrame Spark por faixa e número IV; classify_iv produz rótulo heurístico. |
| Efeitos | Agrega/collect totais, conta bins, collect IV total; sem escrita; não cria faixas. |
| Dependências e momento de uso | pyspark.sql DataFrame/functions; consumidor precisa conversão pequena para scorecard pandas. |
| Como interpretar este arquivo | A função recebe coluna já discretizada e alvo binário, agrega bons/maus em Spark e retorna tabela por faixa com WoE, peso da evidência, mais IV, valor de informação, total numérico. Usa collect para totais e IV, não coleta a tabela inteira por padrão. Não cria bins, não treina scorecard e não grava; a ponte posterior para pandas deve ser explicitamente limitada. |

<a id="mt07-mt08-code-map-file-028"></a>
#### 28. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/__init__.py` · SHA-256 `041655c508ce21d4699325c4de5efbea685dffef0efed4b52f2109288661f459` |
| Papel e motivo técnico | Marcar a categoria spark como pacote Python; não publicar todas as funções no nível da categoria. |
| Nomes disponibilizados | [] |
| Entradas | Importação Python da categoria; nenhum dado analítico. |
| Saídas | Namespace de pacote, sem função exportada. |
| Efeitos | Importação/identificação do pacote; não executa Spark nem grava. |
| Dependências e momento de uso | Nenhum import próprio. |
| Como interpretar este arquivo | Este arquivo apenas marca hub_snippets.spark como categoria importável; não reexporta todos os helpers filhos. Quem deseja pit_join, null_summary ou outro recurso importa a pasta específica. Importar a categoria não cria DataFrame, sessão Spark ou ação distribuída, e procurar todos os nomes no nível superior daria erro de API. |

<a id="mt07-mt08-code-map-file-029"></a>
#### 29. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/date_features/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/date_features/__init__.py` · SHA-256 `385285031fd38866c4d04c27a1e2e42fdea24ff2150a67e3cb705a23f1e43503` |
| Papel e motivo técnico | Expor a API pública da pasta date_features por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["FIXED_NATIONAL_HOLIDAYS_BR", "extrair_features_data", "add_date_features"] |
| Entradas | Importação Python from hub_snippets.spark.date_features import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: FIXED_NATIONAL_HOLIDAYS_BR, extrair_features_data, add_date_features. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql; lista fixa de nove feriados nacionais por dia/mês. |
| Como interpretar este arquivo | A fachada publica `FIXED_NATIONAL_HOLIDAYS_BR`, `extrair_features_data` e `add_date_features` da implementação de calendário. Ela carrega o módulo ao importar, mas não adiciona coluna a um DataFrame. O consumidor precisa chamar a função com coluna e feriados quando cabíveis; o import não inventa calendário móvel. |

<a id="mt07-mt08-code-map-file-030"></a>
#### 30. date_features.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/date_features/date_features.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/date_features/date_features.py` · SHA-256 `9e09e10c9488815641a1fa8e8dc3e60eafa3a3d2d86e665dd0e074df3de6f984` |
| Papel e motivo técnico | Padronizar nove atributos de calendário sem fingir calendário completo de feriados. |
| Nomes disponibilizados | ["extrair_features_data"] |
| Entradas | DataFrame Spark, coluna de data, prefixo e datas explícitas do projeto. |
| Saídas | Novo DataFrame Spark com nove colunas; alias público add_date_features. |
| Efeitos | Somente plano de withColumn no helper; avaliação acontece numa ação posterior. |
| Dependências e momento de uso | pyspark.sql; lista fixa de nove feriados nacionais por dia/mês. |
| Como interpretar este arquivo | O helper compõe nove atributos de calendário por withColumn sobre um DataFrame Spark, deixando avaliação para uma ação posterior. O indicador interno de feriados cobre apenas datas fixas nacionais; feriados móveis ou locais exigem holiday_dates fornecido. Assim, uma coluna feriado vazia fora desse escopo não demonstra ausência real de feriado. |

<a id="mt07-mt08-code-map-file-031"></a>
#### 31. exemplo_date_features.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/date_features/exemplo_date_features.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/date_features/exemplo_date_features.py` · SHA-256 `2a44f7fef0f503a61c21e266274be3a474db1ad85b10ec3ba90ff25f5c6fea9f` |
| Reconciliação dos comentários atuais | Delta MAGIC substitui indiferente por requisito de sessão Spark/APIs compatíveis e conferência de runtime/permissões/destino. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar date_features; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture Spark de 500 linhas; consulta current_user e altera sys.path; display de amostra e agregação; collect limitado de três linhas. A célula escolhe a primeira coluna com 'feriad', que é o indicador fixo, não o calendário fornecido. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.spark.date_features import (; from hub_snippets.testing import fixtures |
| Como interpretar este arquivo | O notebook monta datas sintéticas e mostra os indicadores de feriado fixo e externo. Um seletor por substring na exibição captura apenas o primeiro nome relevante; isso limita a tabela mostrada, não o conjunto de colunas que a função criou. Leia schema/seleção antes de concluir que faltou um indicador. A saída é histórico do exemplo, sem gravação persistente. |

<a id="mt07-mt08-code-map-file-032"></a>
#### 32. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/join_diagnostics/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/join_diagnostics/__init__.py` · SHA-256 `bc696f2416196604686ad9149c89e0388be27caef80e15f44c767e986148ca9e` |
| Papel e motivo técnico | Expor a API pública da pasta join_diagnostics por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["diagnosticar_join"] |
| Entradas | Importação Python from hub_snippets.spark.join_diagnostics import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: diagnosticar_join. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql; agregação e distribuição por chave. |
| Como interpretar este arquivo | A fachada reexporta o diagnóstico de junção da implementação Spark. O import carrega módulo e nomes, sem contar chaves ou executar join. A chamada concreta precisa receber as duas fontes e a chave; ela mede o cruzamento informado, não a unicidade de cada tabela em todo o catálogo. |

<a id="mt07-mt08-code-map-file-033"></a>
#### 33. exemplo_join_diagnostics.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/join_diagnostics/exemplo_join_diagnostics.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/join_diagnostics/exemplo_join_diagnostics.py` · SHA-256 `b2f7e9bd6721ddc277b591654326772dc37d1f982cfa8423adb28a4ef88b0dc8` |
| Reconciliação dos comentários atuais | Deltas MAGIC exigem runtime compatível e definem cobertura pelo denominador de chaves válidas; rótulo impresso sobre o total é impreciso. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar join_diagnostics; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture de 500 clientes compara cadastro único, dois contratos, cadastro parcial e chave nula; count/show/print; current_user + sys.path; sem gravação. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.testing import fixtures; from hub_snippets.spark.join_diagnostics import diagnosticar_join |
| Como interpretar este arquivo | O notebook constrói duas tabelas pequenas e imprime cobertura e multiplicação previstas. Um rótulo histórico “cobertura sobre o total” pode induzir denominador errado; a própria prosa do exemplo e a implementação usam a base válida após filtros. Recalcule numerador e denominador ao adaptar: o valor mostrado é da amostra sintética, não da junção de negócio. |

<a id="mt07-mt08-code-map-file-034"></a>
#### 34. join_diagnostics.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/join_diagnostics/join_diagnostics.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/join_diagnostics/join_diagnostics.py` · SHA-256 `2f51ac7d402d90ed97ee556658e40df2fe64f78a55c8853081f667c0fdd821e4` |
| Papel e motivo técnico | Antecipar cobertura, órfãos, chaves nulas e expansão de uma junção antes da junção de negócio. |
| Nomes disponibilizados | ["diagnosticar_join"] |
| Entradas | Dois DataFrames Spark, chave simples/composta e limite de exemplos de órfãs. |
| Saídas | Dicionário de contagens, cobertura sobre chaves válidas, multiplicidade, expansão prevista e pequenas amostras. |
| Efeitos | Executa agregações e joins left_semi/inner/left_anti; first e collect limitados; não devolve tabela final nem grava. |
| Dependências e momento de uso | pyspark.sql; agregação e distribuição por chave. |
| Como interpretar este arquivo | A implementação agrega chaves, usa joins semi, inner e anti para contar correspondências, órfãos, nulos e expansão potencial. Faz ações Spark e coletas pequenas para diagnóstico, mas não devolve a tabela de negócio juntada nem grava. Rótulos 1:1 ou N:1 descrevem o recorte das chaves cruzadas; não certificam unicidade global das fontes. |

<a id="mt07-mt08-code-map-file-035"></a>
#### 35. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/null_summary/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/null_summary/__init__.py` · SHA-256 `6b5ecda7e69c96be1c901847beb4184376197b18e92eef7311b4f66e4faddb1b` |
| Papel e motivo técnico | Expor a API pública da pasta null_summary por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["null_summary"] |
| Entradas | Importação Python from hub_snippets.spark.null_summary import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: null_summary. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql; sessão Spark do DataFrame. |
| Como interpretar este arquivo | A fachada publica resumo de nulos e semáforo da implementação local. O import disponibiliza as funções e dependências PySpark, sem contar registros ou mostrar resultados. Os limiares só passam a classificar colunas quando a função recebe DataFrame e é chamada; a própria fachada não escolhe política de qualidade. |

<a id="mt07-mt08-code-map-file-036"></a>
#### 36. exemplo_null_summary.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/null_summary/exemplo_null_summary.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/null_summary/exemplo_null_summary.py` · SHA-256 `022399babbb8150c791325e4840fd7fad0affa6498e80be34bef4d13c99df803` |
| Reconciliação dos comentários atuais | Deltas MAGIC exigem runtime compatível e especificam status != "🟢"; "ok" não pertence ao domínio e selecionaria todas as linhas. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar null_summary; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture com nulos probabilísticos; display de dois resumos e filtro por emoji, count das suspeitas; current_user + sys.path. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from hub_snippets.spark.null_summary import null_summary; from hub_snippets.testing import fixtures |
| Como interpretar este arquivo | O notebook cria base sintética e filtra a saída pelo emoji de atenção usado no semáforo. Um filtro textual antigo não seria equivalente: os rótulos atuais dependem do símbolo literal. A tabela exibida pertence ao exemplo histórico; para outra base, confira os valores e o código de status antes de copiar uma condição de filtro. |

<a id="mt07-mt08-code-map-file-037"></a>
#### 37. null_summary.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/null_summary/null_summary.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/null_summary/null_summary.py` · SHA-256 `18d3d1c16708d78f08087fc3da6a69c938d2da83f7d094cfa69312ca954e3f6f` |
| Papel e motivo técnico | Quantificar ausência isNull por coluna e sinalizar contra limiares declarados. |
| Nomes disponibilizados | ["null_summary"] |
| Entradas | DataFrame Spark e percentuais threshold_warn/threshold_fail. |
| Saídas | DataFrame Spark com coluna, count_null, pct_null e status por emoji. |
| Efeitos | count da tabela, agregação collect no driver, cria/ordena resumo e imprime mensagem; não altera fonte. |
| Dependências e momento de uso | pyspark.sql; sessão Spark do DataFrame. |
| Como interpretar este arquivo | A função conta linhas e agrega isNull por coluna em Spark, coleta o resumo pequeno ao driver, ordena e imprime semáforo conforme limiares informados. Base vazia pede interpretação especial do denominador; limiares fornecidos não são validados como política universal. Ela observa qualidade e não modifica a tabela fonte nem grava resultado. |

<a id="mt07-mt08-code-map-file-038"></a>
#### 38. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/pit_join/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/pit_join/__init__.py` · SHA-256 `f6291911f56cc2b10d293693e1c592c2ccc29219961c96fdccc7c9c3eac978d7` |
| Papel e motivo técnico | Expor a API pública da pasta pit_join por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["POLITICAS_EMPATE", "pit_join"] |
| Entradas | Importação Python from hub_snippets.spark.pit_join import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: POLITICAS_EMPATE, pit_join. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql DataFrame/Window/SparkSession; fuso da sessão e semântica de timestamp. |
| Como interpretar este arquivo | A fachada reexporta a função de join point-in-time e parâmetros auxiliares da implementação. Importá-la não consulta fuso, não varre dados e não faz join. O consumidor ainda deve definir chaves, relógios e atraso de publicação; a API curta não resolve disponibilidade histórica automaticamente. |

<a id="mt07-mt08-code-map-file-039"></a>
#### 39. exemplo_pit_join.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/pit_join/exemplo_pit_join.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/pit_join/exemplo_pit_join.py` · SHA-256 `50e66e5f2b28e8fcd29f57241e39823a3b57c8cbe1660d2a23612e9a2ef92772` |
| Reconciliação dos comentários atuais | Delta MAGIC reforça que saídas são referências sintéticas observadas e não execução atual do ambiente do leitor. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar pit_join; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture de 200 decisões; contrasta join ingênuo 433 linhas/33 futuras com PIT; usa count/show/print e repete quatro atrasos; current_user + sys.path; outputs colados históricos. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.testing import fixtures; from hub_snippets.spark.pit_join import pit_join |
| Como interpretar este arquivo | O notebook cria decisões e features sintéticas com horários próximos, chama o join histórico e mostra qual versão ficou disponível a cada decisão. As saídas coladas são observações da demonstração, não prova de correção em outra fonte. Ao adaptar, verifique fuso, atrasos reais e empates, pois uma feature registrada antes da decisão pode ter sido publicada depois. |

<a id="mt07-mt08-code-map-file-040"></a>
#### 40. pit_join.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/pit_join/pit_join.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/pit_join/pit_join.py` · SHA-256 `02b381ad11a12664060015fa79eb00d08aec4df524d3a4701000acdc992c3218` |
| Papel e motivo técnico | Associar a cada decisão a última feature já disponível, descontando atraso de publicação. |
| Nomes disponibilizados | ["pit_join"] |
| Entradas | Fatos/histórico Spark, chave, relógios de decisão/referência, atraso obrigatório; janela, colunas, sufixo, política de empate opcionais. |
| Saídas | DataFrame enriquecido preservando linhas de fato e dicionário de diagnóstico por causa de ausência. |
| Efeitos | Join de intervalo e janela; count/groupBy/collect para empate e diagnóstico; consulta fuso da sessão; não grava. |
| Dependências e momento de uso | pyspark.sql DataFrame/Window/SparkSession; fuso da sessão e semântica de timestamp. |
| Como interpretar este arquivo | O helper faz join de intervalo e escolhe a última feature disponível antes da decisão, descontando atraso de publicação. Consulta fuso da sessão, usa janela de desempate e ações de contagem/agrupamento para diagnosticar empate; não grava. Atraso fixo é simplificação: se a fonte publica com variância ou clock distinto, um join aparentemente válido pode ainda vazar futuro. |

<a id="mt07-mt08-code-map-file-041"></a>
#### 41. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/psi_calculator/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/psi_calculator/__init__.py` · SHA-256 `cc0df26a3ca7927928cdbe512ed16f85c527fb3dbc8b72aeed95994046300d6b` |
| Papel e motivo técnico | Expor a API pública da pasta psi_calculator por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["LIMITE_CATEGORIAS_CSI", "calcular_psi", "calcular_csi", "interpretar_psi"] |
| Entradas | Importação Python from hub_snippets.spark.psi_calculator import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: LIMITE_CATEGORIAS_CSI, calcular_psi, calcular_csi, interpretar_psi. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql; math; driver recebe apenas distribuições agregadas até limite categórico. |
| Como interpretar este arquivo | A fachada publica o cálculo Spark de PSI/CSI da implementação. O import carrega o módulo sem quantil, count ou collect. Para comparar períodos, o consumidor precisa passar referência e atual com mesma definição de população e variável; o pacote não determina que um limiar de drift seja aprovado. |

<a id="mt07-mt08-code-map-file-042"></a>
#### 42. exemplo_psi_calculator.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/psi_calculator/exemplo_psi_calculator.py` · SHA-256 `53eba9de8b64ae3362424f008f8e6c260a1664cc6c9c7787af1008a0c1900a18` |
| Reconciliação dos comentários atuais | Deltas MAGIC explicam proporções/faixas comuns, exigem compatibilidade e mantêm limite categórico positivo; esse limite não garante bytes nem custo de shuffle. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar psi_calculator; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture Spark altera forma da renda sem grande deslocamento da média; agg/first e calcula PSI/CSI; current_user + sys.path; saídas históricas. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.testing import fixtures; from hub_snippets.spark.psi_calculator import calcular_csi, calcular_psi, interpretar_psi |
| Como interpretar este arquivo | O notebook monta duas distribuições sintéticas, calcula PSI e ilustra uma leitura de mudança de perfil. O número histórico não mede queda de acurácia nem monitoramento atual. Ao refazer, mantenha bins da referência, categoria de ausentes e volume de cada período; trocar a régua entre bases altera o significado da comparação. |

<a id="mt07-mt08-code-map-file-043"></a>
#### 43. psi_calculator.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/psi_calculator/psi_calculator.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/psi_calculator/psi_calculator.py` · SHA-256 `5ef35326f875a6c1f5844ef52f73c6437c1a16db46fcadda79f7cc46e196e065` |
| Papel e motivo técnico | Comparar distribuição numérica ou categórica com régua de referência fixa. |
| Nomes disponibilizados | ["calcular_psi", "calcular_csi", "interpretar_psi"] |
| Entradas | DataFrames Spark referência/atual, coluna(s), bins, limite de categorias e limiares opcionais. |
| Saídas | PSI numérico, dicionário CSI por feature e texto de interpretação condicionado à política. |
| Efeitos | Quantis aproximados, groupBy/count/collect de bins; CSI conta categorias antes da coleta; sem gravação. |
| Dependências e momento de uso | pyspark.sql; math; driver recebe apenas distribuições agregadas até limite categórico. |
| Como interpretar este arquivo | A implementação cria bins numéricos pela referência, separa missing, usa quantis aproximados e agrega contagens em Spark antes de coletar categorias/faixas limitadas. PSI/CSI compara distribuições, não desempenho de modelo. Limite de categorias protege driver, mas a escolha de referência e um threshold material continuam decisões do caso; não há escrita persistente. |

<a id="mt07-mt08-code-map-file-044"></a>
#### 44. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/safe_display/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/safe_display/__init__.py` · SHA-256 `f3e7b8a6f53ef1c787ac8101d278f5a411cd7886158fb5890cc913495d32557b` |
| Papel e motivo técnico | Expor a API pública da pasta safe_display por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["safe_display"] |
| Entradas | Importação Python from hub_snippets.spark.safe_display import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: safe_display. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql; renderer do chamador, não global do notebook herdado pelo módulo. |
| Como interpretar este arquivo | A fachada reexporta safe_display da implementação. Importá-la não chama renderer nem coleta linhas; o efeito começa quando o consumidor fornece DataFrame e função de exibição ou ambiente compatível. É importante distinguir esse nome de módulo do objeto função ao escrever o import. |

<a id="mt07-mt08-code-map-file-045"></a>
#### 45. exemplo_safe_display.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/safe_display/exemplo_safe_display.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/safe_display/exemplo_safe_display.py` · SHA-256 `705babdeadb8dacd0008fc0903118767f3bb64f3008e676204a32fda3b8720fd` |
| Reconciliação dos comentários atuais | Deltas MAGIC retiram equivalência universal Free/trabalho e indicam display_fn=display; falta do renderer é detectada após count limitado, podendo haver custo mesmo na falha. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar safe_display; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture 5000 linhas demonstra erro sem display_fn, injeção de display, explain e lambda que conta prévia; current_user + sys.path; sem gravação. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from hub_snippets.spark.safe_display import safe_display; from hub_snippets.testing import fixtures |
| Como interpretar este arquivo | O notebook cria DataFrame pequeno, mostra prévia limitada e usa explain para inspecionar plano Spark. Explain revela plano, não linhas processadas; a contagem de prefixo e o renderer são ações separadas. A transcrição é histórica e não justifica coletar uma tabela inteira para “ver se truncou”. |

<a id="mt07-mt08-code-map-file-046"></a>
#### 46. safe_display.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/safe_display/safe_display.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/safe_display/safe_display.py` · SHA-256 `7d494b5730f65719e3c488c2b2bd96ad6a517b2c132f7b9983e1d65c646ddb55` |
| Papel e motivo técnico | Limitar prévia antes do renderer do notebook, sem contar a tabela inteira para detectar truncamento. |
| Nomes disponibilizados | ["safe_display"] |
| Entradas | DataFrame Spark, limite positivo, opção de mensagem e display_fn injetável. |
| Saídas | None; entrega no máximo limit linhas ao renderer. |
| Efeitos | Conta prefixo limit+1, imprime opcionalmente, chama renderer; ausência de display_fn acessível levanta RuntimeError; não grava. |
| Dependências e momento de uso | pyspark.sql; renderer do chamador, não global do notebook herdado pelo módulo. |
| Como interpretar este arquivo | O helper limita a contagem a até limit+1 linhas para detectar truncamento e entrega a prévia ao renderer. Isso não mede bytes ou todo o custo do plano. A ausência de display_fn é detectada depois dessa ação, então até a falha pode ter custo Spark. Não grava nem converte a tabela inteira em pandas. |

<a id="mt07-mt08-code-map-file-047"></a>
#### 47. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/smart_sample/__init__.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/smart_sample/__init__.py` · SHA-256 `24c5b9f4360a693e84aab9806876ee00e0020c61baf85838f429c2d85220deba` |
| Papel e motivo técnico | Expor a API pública da pasta smart_sample por imports relativos e `__all__`; encaminha à implementação, sem algoritmo independente. |
| Nomes disponibilizados | ["smart_sample"] |
| Entradas | Importação Python from hub_snippets.spark.smart_sample import ...; dados só chegam às funções reexportadas. |
| Saídas | Nomes públicos declarados em `__all__`: smart_sample. |
| Efeitos | Importa o módulo de implementação e suas dependências de topo; não chama helper, não processa dados nem grava. |
| Dependências e momento de uso | Import relativo do módulo local; dependências efetivas: pyspark.sql/Window; seed e estabilidade do plano/fonte. |
| Como interpretar este arquivo | A fachada publica amostragem simples e estratificada da implementação Spark. O import não conta população, define semente ou dispara job. A escolha do modo pertence ao consumidor: garantir presença de estratos é diferente de preservar suas prevalências. |

<a id="mt07-mt08-code-map-file-048"></a>
#### 48. exemplo_smart_sample.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/smart_sample/exemplo_smart_sample.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/smart_sample/exemplo_smart_sample.py` · SHA-256 `cafb6778e86168e4d8f1db05e26a56ea12844963e10aa65f3638684c891822f8` |
| Reconciliação dos comentários atuais | Deltas MAGIC registram fração min(1,1.2*n/total), viés de prefixo com fração 1, ausência de garantia geral de inclusão uniforme e colisões __sample_rank/__stratum_target. |
| Papel e motivo técnico | Demonstrar sinteticamente e interpretar smart_sample; não é implementação reutilizável. |
| Nomes disponibilizados | [] |
| Entradas | Fixture 5020 linhas com segmento XX de 20; compara seeds e modos usando count, exceptAll, display; current_user + sys.path. |
| Saídas | Saídas de célula/figura ou tabelas demonstrativas; blocos colados são evidência histórica, não resultado desta auditoria. |
| Efeitos | Executaria ações de notebook descritas em inputs; sem execução nesta preparação. Não contém escrita persistente de tabela/arquivo no roteiro lido. |
| Dependências e momento de uso | Imports e ambiente de notebook: import sys; from pyspark.sql import functions as F; from hub_snippets.spark.smart_sample import smart_sample; from hub_snippets.testing import fixtures |
| Como interpretar este arquivo | O notebook compara amostra simples e por estrato em dados sintéticos, mostrando uma realização histórica do sorteio. A presença da categoria rara nessa saída não garante sua presença no modo simples de outra execução. Registre semente e objetivo amostral; se a prevalência importa, avalie pesos e distribuição antes de interpretar resultados. |

<a id="mt07-mt08-code-map-file-049"></a>
#### 49. smart_sample.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/spark/smart_sample/smart_sample.py) · [MT07: explicação do mecanismo](MT-parte-ii.md#mt07-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_databricks/.assistant/hub_snippets/spark/smart_sample/smart_sample.py` · SHA-256 `ce2cb190897901a26192b65126012ad33ed3e2d3a7643192d27843281876e971` |
| Papel e motivo técnico | Construir amostra limitada simples ou com presença de todos os estratos. |
| Nomes disponibilizados | ["smart_sample"] |
| Entradas | DataFrame Spark, teto n, coluna de estratificação opcional e seed. |
| Saídas | DataFrame Spark original se pequeno, amostra simples de no máximo n ou estratificada com cotas. |
| Efeitos | count de prefixo; simples count total/sample/limit; estratificada groupBy, janelas e join null-safe; sem gravação. |
| Dependências e momento de uso | pyspark.sql/Window; seed e estabilidade do plano/fonte. |
| Como interpretar este arquivo | O helper usa contagens e amostragem Spark; no modo estratificado, calcula cotas por grupo, janelas e join seguro para nulos. Isso pode garantir presença de estrato ao custo de distorcer prevalências e de ações adicionais. No modo simples, min(1, 1.2*n/total) seguido de limit não assegura tamanho exato, presença rara ou inclusão uniforme: com total=110 e n=100, a fração 1 pode devolver prefixo. Na rota estratificada, __sample_rank e __stratum_target podem colidir com colunas do chamador; evite esses nomes. Não grava. |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
