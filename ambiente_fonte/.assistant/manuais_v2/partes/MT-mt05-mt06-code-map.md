<a id="referencias-companion"></a>
# Leitura dos arquivos de padrões, constantes e apresentação

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MT-indice.md#sumario-mt) · [Livro completo](../../MANUAL_TECNICO_V2.md#sumario-mt)
<!-- editorial:exclude:end -->

<a id="mt-mod-mt05-mt06-code-map"></a>
<a id="mt05-mt06-code-map"></a>
### Leitura dos arquivos de padrões, constantes e apresentação

Leia cada ficha como uma ligação entre a arquitetura ensinada no capítulo e os bytes de um arquivo concreto. A coluna de papel responde por que o arquivo existe. As entradas e saídas mostram onde os dados entram e o que o chamador recebe. A coluna de efeitos separa calcular um resultado de alterar a sessão, gravar uma tabela ou produzir uma apresentação. Essa separação evita atribuir ao helper tudo que aparece no notebook de demonstração.

Uma fachada é a camada de importação que disponibiliza nomes de outro módulo. Ela pode carregar bibliotecas necessárias no momento do import, embora ainda não chame a função de negócio. Um marcador de pacote apenas estabelece a organização do diretório. Uma implementação contém o algoritmo. Um exemplo é um roteiro de notebook: pode preparar dados, instalar bibliotecas, mostrar resultados e conservar observações históricas. Esses quatro papéis explicam a repetição de nomes entre arquivos sem sugerir quatro versões independentes do mesmo algoritmo.

As fichas complementam a leitura contínua; não substituem a assinatura e a interpretação desenvolvidas nos capítulos. Quando um resultado histórico difere do comportamento atual, a nota identifica a diferença e o cuidado necessário. Uma saída colada no exemplo descreve o ensaio registrado naquela fonte; ela não demonstra uma execução atual. Os nomes citados também não tornam automaticamente uma função interna uma interface pública. Para compor uma chamada, use a fachada indicada e confira o contrato do objeto.

Os links levam ao arquivo correspondente e ao trecho conceitual do manual. Compare sempre helper e exemplo antes de executar células: efeitos pertencem ao corpo que realmente os realiza. As limitações descritas fazem parte da interpretação do resultado, inclusive quando o código devolve números plausíveis.

Reconciliado com a fonte de 07/10/2026: 35 arquivos, 29 com bytes preservados e 6 com alterações em comentários de notebook. As fichas conservam o mérito das leituras anteriores; os comentários alterados foram confrontados com a implementação. Os hashes abaixo identificam os arquivos atuais. Isso não representa reexecução dos exemplos nem homologação de runtime.

<a id="mt05-mt06-code-map-file-001"></a>
#### 1. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/__init__.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/__init__.py` · SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Papel, motivo e consumidor | Pacote de padrões sem exports próprios; import apenas estabelece namespace. |
| Entrada, retorno, efeitos e dependências | Não recebe dados, não devolve resultado e não executa helper. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-002"></a>
#### 2. template.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/notebook/template.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/notebook/template.py` · SHA-256 `f0c43bdfa3e468212c2516c2a3df9746885af9cdbc456fc099561ce71af2bc29` |
| Papel, motivo e consumidor | Molde Databricks: cabeçalho, células, preâmbulo, contexto/código/execução/leitura e bloco NÃO EXECUTADO. |
| Entrada, retorno, efeitos e dependências | Ao executar o preâmbulo, consulta o usuário via Spark e altera `sys.path`; não escreve tabela. |
| Como interpretar este arquivo | O bloco NÃO EXECUTADO distingue impedimento técnico do objeto ou do ambiente de falta de acesso ou tempo. O preâmbulo Spark e a chamada principal ocupam etapas diferentes. |

<a id="mt05-mt06-code-map-file-003"></a>
#### 3. exemplo_analisar_campanha.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/prompt/analisar_campanha/exemplo_analisar_campanha.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha/exemplo_analisar_campanha.py` · SHA-256 `1565c42abd8513b6ec3d53f760b587999a8d297c9f68c5f6b93dda835c2a0c47` |
| Papel, motivo e consumidor | Lê tabela de campanha criada pelo exemplo de snippet, agrega segmento e mostra briefing preenchido. |
| Entrada, retorno, efeitos e dependências | Parte 1 usa spark.table/count/display, sem escrita; Parte 3 contém captura histórica de chat em 16/08/2026, não execução nova. |
| Como interpretar este arquivo | Além do briefing, há uma resposta histórica de chat de 16/08/2026, com roteamento observado e acertos/erros numéricos registrados. O prompt textual e essa resposta têm papéis diferentes. |

<a id="mt05-mt06-code-map-file-004"></a>
#### 4. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/script/__init__.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/script/__init__.py` · SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Papel, motivo e consumidor | Marcador vazio da família script. |
| Entrada, retorno, efeitos e dependências | Sem entrada, retorno ou efeito. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-005"></a>
#### 5. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/script/checar_base_campanha/__init__.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/__init__.py` · SHA-256 `9d0933fdfeb7bc252a5c39d58661641fdd1c760f5eef95e2c78bc551b8fd10a8` |
| Papel, motivo e consumidor | Reexporta LIMITES_PADRAO e checar_base_campanha; define `__all__`. |
| Entrada, retorno, efeitos e dependências | Importa implementação e portanto depende de PySpark no import; não chama diagnóstico. |
| Como interpretar este arquivo | Reexporta LIMITES_PADRAO e checar_base_campanha; importar essa fachada importa a implementação com PySpark. A importação ainda não chama o diagnóstico. |

<a id="mt05-mt06-code-map-file-006"></a>
#### 6. checar_base_campanha.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/script/checar_base_campanha/checar_base_campanha.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/checar_base_campanha.py` · SHA-256 `7cce726bddd4d28fa6117440145958617944d2c8ba57febd908a5da78057d410` |
| Papel, motivo e consumidor | Recebe tabela e colunas nomeadas; obtém SparkSession, lê tabela, agrega grão/domínio/base por segmento e devolve dict status/limites/checagens/alertas. |
| Entrada, retorno, efeitos e dependências | Sem escrita; collect em duas agregações, plano físico não contado. LIMITES_PADRAO inclui pct_nulo_alerta que o corpo não consulta. |
| Como interpretar este arquivo | pct_nulo_alerta aparece nos limites retornados, mas o corpo não usa esse valor para implementar uma checagem de percentual nulo. |

<a id="mt05-mt06-code-map-file-007"></a>
#### 7. exemplo_checar_base_campanha.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/script/checar_base_campanha/exemplo_checar_base_campanha.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha/exemplo_checar_base_campanha.py` · SHA-256 `53e45fa2eda83a44fec3470cb646e63ea2a22791649486ea9d6c664f0e85c987` |
| Papel, motivo e consumidor | Importa script, lê campanha, cria amostra duplicada, chama diagnóstico e exibe status. |
| Entrada, retorno, efeitos e dependências | Escreve workspace.default.hub_exemplo_campanha_dup com overwrite e depois DROP TABLE; exige tabela original prévia e autorização para destino. Saídas históricas têm contagens contraditórias, reconhecidas em nota R01. |
| Como interpretar este arquivo | O roteiro sobrescreve workspace.default.hub_exemplo_campanha_dup e depois executa DROP TABLE desse destino. Os blocos históricos citam 48.206 e 48.192 em contextos registrados; não os trate como contagem atual. Verifique também a fonte de campanha exigida pelo roteiro. |

<a id="mt05-mt06-code-map-file-008"></a>
#### 8. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/snippet/__init__.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/snippet/__init__.py` · SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Papel, motivo e consumidor | Marcador vazio da família snippet. |
| Entrada, retorno, efeitos e dependências | Sem entrada, retorno ou efeito. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-009"></a>
#### 9. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/snippet/taxa_resposta_campanha/__init__.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/__init__.py` · SHA-256 `86d2d3223ca0beef2179871fe38e1a14456071dafab5269cbe197ff154c10055` |
| Papel, motivo e consumidor | Reexporta MINIMO_PARA_DECISAO e taxa_resposta_campanha em `__all__`. |
| Entrada, retorno, efeitos e dependências | Importa implementação e PySpark; não calcula taxa no import. |
| Como interpretar este arquivo | Publica a função do exemplar por import relativo; isso carrega as dependências de topo da implementação sem executar a taxa. |

<a id="mt05-mt06-code-map-file-010"></a>
#### 10. exemplo_taxa_resposta_campanha.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-4)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py` · SHA-256 `6c8f4f0f257168741c2f9ad931a4ca1c79d391244cf4604c9c1a1fbcbd456091` |
| Papel, motivo e consumidor | Gera 45.868 contatos sintéticos de seis segmentos, mostra taxa ingênua, Wilson e recusa de resposta nula. |
| Entrada, retorno, efeitos e dependências | Sobrescreve workspace.default.hub_exemplo_campanha; display/ações Spark e saída histórica. Nota R01 corrige inferências antigas sobre significância/teto. |
| Como interpretar este arquivo | Prepara 45.868 registros sintéticos em seis segmentos e sobrescreve workspace.default.hub_exemplo_campanha. A interpretação histórica de intervalos de Wilson que não se sobrepõem não é, por si, teste formal de diferença entre taxas. |

<a id="mt05-mt06-code-map-file-011"></a>
#### 11. taxa_resposta_campanha.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_padroes/snippet/taxa_resposta_campanha/taxa_resposta_campanha.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/taxa_resposta_campanha.py` · SHA-256 `33bc18a6ea61aca3c73be45b3676050c3d9f5fc17efe1ec3197e839fb3c1708b` |
| Papel, motivo e consumidor | Recebe Spark DataFrame, segmento, resposta 0/1, z e mínimo; valida colunas/domínio, agrega e devolve DataFrame por segmento com Wilson, taxa e decidivel. |
| Entrada, retorno, efeitos e dependências | Ação count para inválidos; transformações e ordem Spark; sem tabela escrita. Mínimo 100 é política local, não teste de hipótese. |
| Como interpretar este arquivo | O count acionado na validação tem custo de leitura. Os intervalos de Wilson e o limiar local de cem observações ajudam a interpretar o resumo; esse limiar não certifica qualidade da decisão. |

<a id="mt05-mt06-code-map-file-012"></a>
#### 12. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/__init__.py) · [MT05: explicação do mecanismo](MT-parte-ii.md#mt05-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/__init__.py` · SHA-256 `041655c508ce21d4699325c4de5efbea685dffef0efed4b52f2109288661f459` |
| Papel, motivo e consumidor | Inicializador da biblioteca hub_snippets, sem exportação de objetos. |
| Entrada, retorno, efeitos e dependências | Sem entrada/retorno funcional; docstring apenas. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-013"></a>
#### 13. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/__init__.py` · SHA-256 `041655c508ce21d4699325c4de5efbea685dffef0efed4b52f2109288661f459` |
| Papel, motivo e consumidor | Inicializador leve da categoria constants, não reexporta os quatro objetos. |
| Entrada, retorno, efeitos e dependências | Sem leitura de dados ou renderização; importar categoria não força módulos filhos. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-014"></a>
#### 14. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/colors/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/colors/__init__.py` · SHA-256 `3ddf21642eb05aec62841e75ae581f02120555e1e4caf6917d0b12aee6f804ac` |
| Papel, motivo e consumidor | Reexporta 22 nomes de cores, paletas e papéis por `__all__`. |
| Entrada, retorno, efeitos e dependências | Importa colors.py; não escolhe tema nem desenha gráfico. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-015"></a>
#### 15. colors.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/colors/colors.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/colors/colors.py` · SHA-256 `f9a6605aa1ef5a92863d728570013a91d4475952381e699e2d0b3daa29f2e8ca` |
| Papel, motivo e consumidor | Constantes hexadecimais, paletas de 10/5/5 cores e aliases semânticos; consumidores importam nomes por papel. |
| Entrada, retorno, efeitos e dependências | Sem dados/retorno/cálculo; colisão entre cores categóricas e semânticas e contraste dependem do consumidor. |
| Como interpretar este arquivo | Verde e vermelho usados como sinais semânticos reaparecem na paleta categórica. Uma legenda precisa esclarecer o papel da cor; o texto branco sobre positivo/alerta não atinge 4,5:1 no exercício histórico. |

<a id="mt05-mt06-code-map-file-016"></a>
#### 16. exemplo_colors.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/colors/exemplo_colors.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/colors/exemplo_colors.py` · SHA-256 `c6c7daf5ce68afc7125092e8e9bbb55e7dae6515616979ffc4f93f7784d83e64` |
| Reconciliação dos comentários atuais | Lidos todos os deltas MAGIC: compatibilidade/renderização depende do destino; contraste 1,73:1 e 2,04:1 com branco é insuficiente nessa condição, sem certificação integral de acessibilidade. Algoritmo/células preservados. |
| Papel, motivo e consumidor | Imprime paletas e renderiza quadrados/badges em displayHTML; mede contraste de branco por luminância. |
| Entrada, retorno, efeitos e dependências | Sem escrita; depende de sessão Spark para path, displayHTML no notebook. Registro histórico: positivo/alerta abaixo de 4,5:1 com branco. |
| Como interpretar este arquivo | O exercício de contraste é referência sintética: branco sobre COR_ALERTA e COR_POSITIVO fica abaixo de 4,5:1 para texto comum. A mesma cor pode representar categoria e estado; legenda, par texto/fundo e renderização exigem conferência no destino. |

<a id="mt05-mt06-code-map-file-017"></a>
#### 17. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/emojis/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/emojis/__init__.py` · SHA-256 `a41c9a67aa6ac7a57c00c4359cba12794624e355d8d085220bbad5e316b2b62d` |
| Papel, motivo e consumidor | Reexporta SECOES_EDA e SEMANTICA. |
| Entrada, retorno, efeitos e dependências | Importa dicionários sem efeito externo. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-018"></a>
#### 18. emojis.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/emojis/emojis.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/emojis/emojis.py` · SHA-256 `ca2ede85dfac855684709e9721053ee5706dfd9f946957180fa0625eb4612f65` |
| Papel, motivo e consumidor | Mapas de nove seções EDA indexadas 0–8 e onze papéis semânticos; consumidor lê símbolos e texto. |
| Entrada, retorno, efeitos e dependências | Sem execução de EDA ou validação; símbolos dependem de renderização/acessibilidade. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-019"></a>
#### 19. exemplo_emojis.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/emojis/exemplo_emojis.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/emojis/exemplo_emojis.py` · SHA-256 `5e1fa3bc2be507c7dbe227427fef79a479938f803c5103b33202578419bc525f` |
| Reconciliação dos comentários atuais | Delta MAGIC exige verificar renderização e compatibilidade no destino; não homologa runtimes. Mapas e células preservados. |
| Papel, motivo e consumidor | Percorre e imprime os dois mapas; interpreta ordem grão→qualidade e univariada→bivariada. |
| Entrada, retorno, efeitos e dependências | Sem escrita; sessão Spark só para localizar pacote; saída textual histórica, sem validação de EDA. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-020"></a>
#### 20. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/format_br/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/format_br/__init__.py` · SHA-256 `681856750444fd4326add451654d07d81ce46646f2bbd54d6f9daf34c1644367` |
| Papel, motivo e consumidor | Reexporta alias Number e seis funções fmt_* em `__all__`. |
| Entrada, retorno, efeitos e dependências | Import da implementação usa Python padrão; não formata sem chamada. |
| Como interpretar este arquivo | A fachada expõe seis funções de formatação e o alias Number. Esse alias de tipo não representa uma operação que processa dados. |

<a id="mt05-mt06-code-map-file-021"></a>
#### 21. exemplo_format_br.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/format_br/exemplo_format_br.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/format_br/exemplo_format_br.py` · SHA-256 `38bf1f015e7d4d7e40dd413d2e6e32f8f3215badfa7b7cbeb622d74fa4ab638d` |
| Reconciliação dos comentários atuais | Deltas MAGIC distinguem referência sintética de execução atual e explicitam fmt_delta(0.0005, "bps") → +5 bps. Escalas/células preservadas. |
| Papel, motivo e consumidor | Demonstra seis formatadores e erros de escala fmt_pct/fmt_delta com valores sintéticos. |
| Entrada, retorno, efeitos e dependências | Sem escrita; sessão Spark só para path; saídas históricas preservadas na R02, não execução nova. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-022"></a>
#### 22. format_br.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/format_br/format_br.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-2)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/format_br/format_br.py` · SHA-256 `1f373e07c86d2a953dd434aea58c0bcddc048dffbb6bb67a9c7e04d3831e0597` |
| Papel, motivo e consumidor | Seis funções de escalares para string BR; Decimal/ROUND_HALF_UP em moeda, percent ratio/percent e delta pp/bps. |
| Entrada, retorno, efeitos e dependências | Sem locale/processo ou escrita; fmt_int trunca e usa formatação float, fmt_n converte float, unidade desconhecida em fmt_delta cai em pp. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-023"></a>
#### 23. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/styles/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/styles/__init__.py` · SHA-256 `960ce63db40087c617f6a234756fe6bec9e8d0b58ae591a91ca7a4db6b29140f` |
| Papel, motivo e consumidor | Reexporta constantes CSS e get_styles_resolvidos por `__all__`. |
| Entrada, retorno, efeitos e dependências | Importa styles.py e dependências de tema; não aplica estilo global. |
| Como interpretar este arquivo | A fachada carrega dependências de tema na importação. Resolver um tema continua sendo uma chamada distinta de disponibilizar esses nomes. |

<a id="mt05-mt06-code-map-file-024"></a>
#### 24. exemplo_styles.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/styles/exemplo_styles.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/styles/exemplo_styles.py` · SHA-256 `65efc37970d140fd30898befc1189a138f78381c2cc08fd8a2abbf053c2e7f3b` |
| Reconciliação dos comentários atuais | Deltas MAGIC removem cronologia V04/V02 como descrição do presente; funções resolvidas continuam opt-in, sem estado global. Conferir destino e ResolvedTheme válido. |
| Papel, motivo e consumidor | Renderiza CSS legado, carrega tema de referência notebook, compara estilos resolvidos e exibe HTML. |
| Entrada, retorno, efeitos e dependências | Sem escrita; requer Spark para path, displayHTML e módulo de tema; asserts verificam duas igualdades locais. |
| Como interpretar este arquivo | O roteiro mostra equivalência de referências de estilo; as variantes resolvidas recebem tema explícito, sem alterar HTML já exibido. Confira contraste e renderização no destino: a demonstração não certifica acessibilidade de todas as combinações. |

<a id="mt05-mt06-code-map-file-025"></a>
#### 25. styles.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/constants/styles/styles.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/constants/styles/styles.py` · SHA-256 `ef86380dc5660cdc9bb8c9df8eed5b2b81934e63092ebdab19e194d9d51064a8` |
| Papel, motivo e consumidor | Constantes CSS legadas e get_styles_resolvidos(ResolvedTheme): revalida tipo/contexto notebook via export_theme, converte tokens em dict CSS. |
| Entrada, retorno, efeitos e dependências | Sem estado global/escrita; rejeita tema cru/contexto errado; depende do núcleo visual.tema. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-026"></a>
#### 26. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/__init__.py` · SHA-256 `041655c508ce21d4699325c4de5efbea685dffef0efed4b52f2109288661f459` |
| Papel, motivo e consumidor | Inicializador leve da categoria display, sem reexportar filhos. |
| Entrada, retorno, efeitos e dependências | Sem efeito ou dados; evita import de Plotly/Spark/pandas por categoria. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-027"></a>
#### 27. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/correlation_matrix/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/__init__.py` · SHA-256 `f67caa6a601fdc8c0a352f12024af26b2d9ee0d158137ce4d3d4a4831b6d0637` |
| Papel, motivo e consumidor | Reexporta plot_correlation, _resolvido e dois aliases plot_correlation_matrix*. |
| Entrada, retorno, efeitos e dependências | Importa implementação e dependências Plotly/Spark ML; não calcula matriz no import. |
| Como interpretar este arquivo | Os aliases publicados encaminham ao mesmo objeto. O import da fachada carrega Spark ML e Plotly, antes de qualquer chamada de correlação. |

<a id="mt05-mt06-code-map-file-028"></a>
#### 28. correlation_matrix.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/correlation_matrix/correlation_matrix.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/correlation_matrix.py` · SHA-256 `7aba392554c266e69c30ddbe9c7f968c2d7752e5916c44fff7bb36c69951ba48` |
| Papel, motivo e consumidor | Spark DataFrame numérico → VectorAssembler/Correlation.corr após drop conjunto de nulos → figura Plotly + pares &#124;r&#124;>=limiar. |
| Entrada, retorno, efeitos e dependências | Ações Spark e matriz coletada ao driver; theme opcional altera escala/visual, não cálculo; exige pyspark.ml e Plotly. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-029"></a>
#### 29. exemplo_correlation_matrix.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/correlation_matrix/exemplo_correlation_matrix.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/correlation_matrix/exemplo_correlation_matrix.py` · SHA-256 `336d58f7ea10b69896238a931d4f3c771580902e61cf489408a25d72baf79a55` |
| Reconciliação dos comentários atuais | Deltas MAGIC situam a falha no laboratório histórico, exigem APIs compatíveis e recusam inferir coeficiente de comentário ou incompatibilidade universal. |
| Papel, motivo e consumidor | Gera 3000 linhas sintéticas com relação renda-limite, tenta plot_correlation e captura Py4JError histórico. |
| Entrada, retorno, efeitos e dependências | Sem escrita; NumPy/Spark/Plotly, count aciona Spark; coeficiente plantado no comentário não foi medido no runtime com falha. |
| Como interpretar este arquivo | O roteiro captura Exception e imprime a mensagem. A falha histórica não demonstra incompatibilidade universal: confira VectorAssembler/Correlation.corr no compute escolhido. A célula pode terminar sem figura ou pares fortes; isso não comprova correlação produzida. |

<a id="mt05-mt06-code-map-file-030"></a>
#### 30. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/dataframe_styled/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/__init__.py` · SHA-256 `f848eb2fdc6bcfb78a0a7ff83817e6d0291380a31b2bf70cd6e51b363b679e96` |
| Papel, motivo e consumidor | Reexporta display_styled e display_styled_resolvido. |
| Entrada, retorno, efeitos e dependências | Importa styles/tema; Jinja2 exigido ao acessar DataFrame.style na chamada, não no import. |
| Como interpretar este arquivo | Jinja2 pode ser exigido apenas quando pandas acessa DataFrame.style. Um import bem-sucedido da fachada não comprova essa dependência tardia. |

<a id="mt05-mt06-code-map-file-031"></a>
#### 31. dataframe_styled.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/dataframe_styled/dataframe_styled.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/dataframe_styled.py` · SHA-256 `77bfd3e3564d9bae85938bb09f5d84dcbea31c3c4d4a413450c8393a02c686f6` |
| Papel, motivo e consumidor | pandas DataFrame → Styler com cabeçalho, negativos por coluna e formato opcional → string HTML. |
| Entrada, retorno, efeitos e dependências | Sem escrita; DataFrame.style exige Jinja2; map/applymap compatível entre pandas; HTML de células não é sanitizado pelo helper. |
| Como interpretar este arquivo | O HTML das células não recebe escape ou sanitização para conteúdo não confiável. pandas.style pode exigir Jinja2 no momento da chamada. |

<a id="mt05-mt06-code-map-file-032"></a>
#### 32. exemplo_dataframe_styled.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/dataframe_styled/exemplo_dataframe_styled.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/dataframe_styled/exemplo_dataframe_styled.py` · SHA-256 `16b3c8c66829882f7fb3cd4cdf2504dfa178198bb443148881ac74b3ec0aed3c` |
| Reconciliação dos comentários atuais | Delta MAGIC explica diretamente o realce de negativos; PSI/nulidade positivos não são destacados por essa regra. %pip/%restart_python permanecem. |
| Papel, motivo e consumidor | Instala Jinja2, reinicia Python, cria pandas DataFrame sintético, converte coluna distinta via fmt_int, destaca negativos e exibe HTML. |
| Entrada, retorno, efeitos e dependências | %pip install jinja2 e %restart_python mutam ambiente de sessão; sem tabela escrita; displayHTML renderiza string. |
| Como interpretar este arquivo | As células %pip e %restart_python alteram a sessão quando executadas. A demonstração de HTML herda o cuidado com conteúdo de células não confiável. |

<a id="mt05-mt06-code-map-file-033"></a>
#### 33. `__init__.py`

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/distribution_grid/__init__.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-1)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/__init__.py` · SHA-256 `fa39750e0b0c36c9f9bc8101f14fd7b6c9a00f35519bcafcb99be38e295fa3c9` |
| Papel, motivo e consumidor | Reexporta plot_distributions, _resolvido e aliases plot_distribution_grid*. |
| Entrada, retorno, efeitos e dependências | Importa Plotly/Spark e smart_sample; não amostra no import. |
| Como interpretar este arquivo | Os aliases da fachada encaminham à implementação; as bibliotecas de topo são carregadas no import. A coleta e a construção da figura pertencem à chamada posterior. |

<a id="mt05-mt06-code-map-file-034"></a>
#### 34. distribution_grid.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/distribution_grid/distribution_grid.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/distribution_grid.py` · SHA-256 `a2caaef6318753bb744022e3491946354c8e216e31bbc160892c9ad8db2bd420` |
| Papel, motivo e consumidor | Spark DataFrame numérico → smart_sample(n) → toPandas() → grade de histogramas Plotly. |
| Entrada, retorno, efeitos e dependências | Amostra e coleta ao driver; sem escrita; rota resolvida valida tema antes da amostragem; exige Plotly, Spark e pandas. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |

<a id="mt05-mt06-code-map-file-035"></a>
#### 35. exemplo_distribution_grid.py

<!-- editorial:exclude:start -->
[Arquivo fonte](../../hub_snippets/display/distribution_grid/exemplo_distribution_grid.py) · [MT06: explicação do mecanismo](MT-parte-ii.md#mt06-3)
<!-- editorial:exclude:end -->

| Aspecto | Explicação |
|---|---|
| Caminho e versão lida | `ambiente_fonte/.assistant/hub_snippets/display/distribution_grid/exemplo_distribution_grid.py` · SHA-256 `e63c479294c433e735f8679e4b3a855a269d6e9e49637af0f8ba9d5b2a62eb95` |
| Papel, motivo e consumidor | Gera 5000 linhas sintéticas com normal, exponencial e mistura bimodal; compara médias e chama grade. |
| Entrada, retorno, efeitos e dependências | Sem escrita; NumPy/Spark/Plotly; agg Spark e amostragem/coleta no helper; saídas históricas não foram reexecutadas aqui. |
| Como interpretar este arquivo | A camada corresponde ao papel descrito acima; use a explicação do capítulo para interpretar o resultado e distinguir importação, chamada e demonstração. |



<!-- editorial:exclude:start -->
[Sumário](MT-indice.md#sumario-mt) · [Guia por pergunta](MT-indice.md#perguntas-mt) · [Trilhas](MT-indice.md#trilhas-mt) · [Outro manual](MU-indice.md#sumario-mu)
<!-- editorial:exclude:end -->
