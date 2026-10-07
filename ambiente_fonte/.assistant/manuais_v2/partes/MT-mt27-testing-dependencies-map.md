# Leitura dos arquivos de testes e dependências

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt27-testing-dependencies-map"></a>
<a id="mt27-testing-dependencies-map"></a>
### Leitura dos arquivos de testes e dependências

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Neste conjunto, os geradores criam dados sintéticos, o notebook mostra sua utilização e os testes conferem propriedades específicas. Os arquivos de dependências declaram versões ou intervalos; lê-los não instala bibliotecas nem comprova compatibilidade do ambiente.

<a id="mt27-testing-dependencies-map-file-001"></a>
#### 1. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/testing/__init__.py) · [MT27: explicação do mecanismo](MT-parte-vii.md#mt27-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/testing/__init__.py` · SHA-256 `7b70c400ae1ee3257bf3e0dfbeb6c24a19f41454f0e63bcd152ea7ea6b0db97c` |
| Papel, entradas, saídas, efeitos e cuidados | `testing/__init__.py` é um marcador de pacote com uma docstring descritiva. Ele permite que o diretório participe do pacote Python, mas não reexporta funções e não inicia Spark. Quem procura um gerador deve importar o subpacote `testing.fixtures`, e não esperar símbolos neste nível. |

<a id="mt27-testing-dependencies-map-file-002"></a>
#### 2. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/testing/fixtures/__init__.py) · [MT27: explicação do mecanismo](MT-parte-vii.md#mt27-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/testing/fixtures/__init__.py` · SHA-256 `f292accdcc3c008bf96dbccf619afc65e8e69f443e1604e368798cabdbd2fc98` |
| Papel, entradas, saídas, efeitos e cuidados | `testing/fixtures/__init__.py` é a fachada dos quatro geradores `base_tabular`, `serie_temporal`, `fatos_e_features` e `safras`. Ela importa `fixtures.py` imediatamente; portanto, mesmo antes de chamar uma função, essa rota de import precisa de PySpark disponível. Seu efeito é oferecer nomes públicos estáveis, sem criar DataFrame por conta própria. |

<a id="mt27-testing-dependencies-map-file-003"></a>
#### 3. `exemplo_fixtures.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/testing/fixtures/exemplo_fixtures.py) · [MT27: explicação do mecanismo](MT-parte-vii.md#mt27-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/testing/fixtures/exemplo_fixtures.py` · SHA-256 `e836306ad7801c0af11cdd2ea998479289cc948006d5df2ee2a5eea9ed4fd8f6` |
| Papel, entradas, saídas, efeitos e cuidados | `testing/fixtures/exemplo_fixtures.py` é um notebook de demonstração Databricks. Ele consulta `current_user()` para compor o caminho de import da sessão, chama os quatro geradores e usa `display`, `count` e `collect` para inspecionar amostras. Essas ações materializam cálculo Spark e exibem resultado, mas não escrevem tabela. A marca `eh_futura` é gabarito sintético para discutir vazamento temporal; o notebook não certifica comportamento de um pipeline real. |

<a id="mt27-testing-dependencies-map-file-004"></a>
#### 4. `fixtures.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/testing/fixtures/fixtures.py) · [MT27: explicação do mecanismo](MT-parte-vii.md#mt27-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/testing/fixtures/fixtures.py` · SHA-256 `e9685f1e86821555a675e37e585dbbf9a89edaaf3a6d89f3677ae83c7f03b3be` |
| Papel, entradas, saídas, efeitos e cuidados | `testing/fixtures/fixtures.py` recebe tamanhos, semente aleatória e parâmetros de nulos, temporalidade, grão ou atraso. Cada gerador monta linhas em uma lista Python e usa a sessão Spark obtida por `_sessao` para devolver DataFrame ou conjunto de DataFrames. `base_tabular` serve para chave, UF, renda ausente e alvo; `serie_temporal` cria entidade por mês; `fatos_e_features` separa versões passadas de uma futura marcada por `eh_futura`; `safras` organiza contrato por mês de vida e inadimplência acumulada. A semente permite repetir os sorteios quando código, parâmetros e versões são compatíveis; compare linhas ordenadas. Frações de nulos e alvo são probabilidades, não cotas exatas. Em `base_tabular`, `n_entidades=0` aciona o padrão `n` pela expressão `or`; `n_entidades>n` ainda produz no máximo `n` IDs distintos. O gerador não persiste nem sobrescreve tabelas, e a lista no driver limita o tamanho prudente do exemplo. |

<a id="mt27-testing-dependencies-map-file-005"></a>
#### 5. `test_core.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/tests/runtime/test_core.py) · [MT27: explicação do mecanismo](MT-parte-vii.md#mt27-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `tools/tests/runtime/test_core.py` · SHA-256 `2be1265e6d0912953bfbc99951df58019d7330a86ac54df5f1136a49b26fea67` |
| Papel, entradas, saídas, efeitos e cuidados | `tools/tests/runtime/test_core.py` pertence ao mantenedor, fora do payload distribuído, e usa `unittest` e dados pequenos em NumPy/pandas para conferir retornos e exceções de helpers no driver. Seus asserts cobrem formatação monetária e percentual; monitoramento e períodos inválidos; ordenação de faixas de score; métricas e amostras degeneradas; scorecard com coeficientes finitos; intervalos e chaves temporais; safra, maturação e snapshots; lift com duas classes; e cadeia split→features→metrics→monitor. Inclui regressões de datas textuais, formatos ambíguos, datas inválidas, duplicidade do grão e colisões de nomes internos, preservando colunas do usuário. O arquivo ajusta o caminho de import ao carregar. Ele não importa as fixtures Spark: aprovação desses asserts, se executados, não equivale à verificação de cluster, fixture ou notebook. |

<a id="mt27-testing-dependencies-map-file-006"></a>
#### 6. `requirements-optional.txt`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/requirements-optional.txt) · [MT03: explicação do mecanismo](MT-parte-i.md#mt03-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt` · SHA-256 `2ed4536b353a63ff9e167581c8c2107499e5215ef1978df6c3983d6f030a5fbe` |
| Papel, entradas, saídas, efeitos e cuidados | `requirements-optional.txt` é inventário de dependências opcionais; orienta escolher apenas o subconjunto exigido pelo objeto, sem instalação integral de rotina. `pmdarima==2.0.4`, `shap==0.44.1` e `umap-learn==0.5.5` fixam versões; `scikit-learn>=1.3` fixa apenas piso; outras linhas não fixam versão. A combinação pmdarima/NumPy 1.23.5 está registrada como evidência de 17/08/2026 em serverless Spark 4.1.0/Python 3.11.10, sem validade universal. O arquivo alerta para ABI de extensões compiladas, dependências indiretas de apresentação/tracking, autorização de criação de runs e eventual reinício da sessão. Não é lockfile, prova de compatibilidade atual nem requisito geral do CI; confira o runtime e a resolução antes de instalar. |

<a id="mt27-testing-dependencies-map-file-007"></a>
#### 7. `requirements-temas.txt`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/requirements-temas.txt) · [MT23: explicação do mecanismo](MT-parte-vi.md#mt23-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/requirements-temas.txt` · SHA-256 `36323a6dff39c4d5e90486dcdae68dea7c0fe0ea5c55455efe8c54959431c49e` |
| Papel, entradas, saídas, efeitos e cuidados | `requirements-temas.txt` fixa `jsonschema==4.26.0` e `referencing==0.37.0` para o validador de temas. A instalação é uma ação do ambiente, jamais uma consequência do import simples do pacote visual. O arquivo difere de `requirements-temas-dev.txt`, citado no percurso de desenvolvimento/CI, e não demonstra que as duas bibliotecas estejam disponíveis em qualquer workspace. |

<a id="mt27-testing-dependencies-map-file-008"></a>
#### 8. `requirements.txt`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/identidade_visual/databricks_app/requirements.txt) · [MT24: explicação do mecanismo](MT-parte-vi.md#mt24-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/identidade_visual/databricks_app/requirements.txt` · SHA-256 `7006a9c5c4cc62463960863f852858cc1b13e9b24d9bc56d83a3e81156b8c63b` |
| Papel, entradas, saídas, efeitos e cuidados | `identidade_visual/databricks_app/requirements.txt` declara faixas para seis dependências do App: Streamlit `>=1.42,<2`, jsonschema `>=4.23,<5`, referencing `>=0.35,<1`, pandas `>=2.2,<3`, Plotly `>=5.24,<7` e Jinja2 `>=3.1,<4`. O instalador escolhe uma versão dentro de cada faixa; o texto não guarda a resolução exata. Seu escopo é o ambiente do App, separado do par de pins do validador de temas e do inventário histórico de ML. A presença do arquivo não implanta o App nem testa compatibilidade no destino. |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
