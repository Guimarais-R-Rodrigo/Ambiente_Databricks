<a id="parte-mu-iii"></a>
# MU parte iii

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MU-indice.md#sumario-mu) · [Livro completo](../../MANUAL_DO_USUARIO.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu08"></a>
<a id="mu08"></a>
### MU08 — Conhecer uma base: EDA, perfil e qualidade

<!-- editorial:exclude:start -->
**Você quer:** entender uma fonte antes de estudá-la, cruzá-la ou modelá-la. **Rota:** defina a pergunta e o grão na seção 1; escolha EDA completa ou pergunta pontual na seção 2; execute e confira a rota direta na seção 3; conclua com um handoff rastreável na seção 4. Exemplos usam tabela fictícia; nenhuma autorização ou execução é presumida.
<!-- editorial:exclude:end -->

<a id="mu08-1"></a>
#### 1. Que pergunta e população vão orientar a exploração?

Antes de pedir um gráfico, formule uma frase que indique o que quer decidir: “Esta tabela de eventos permite estudar respostas a campanhas por entidade e mês?”. Essa frase determina quais colunas importam, qual período deve ser lido e que erro seria grave. Se você pedir apenas “faça EDA”, o planejamento ainda pode começar, declarando hipóteses e perguntas abertas; entradas críticas ausentes não autorizam executar a análise por suposição. Uma EDA — **análise exploratória de dados** — descreve estrutura, qualidade, distribuição e relações de uma população. Ela ajuda a descobrir problemas e possibilidades; não certifica por si que a base está pronta para produção ou que uma relação é causal.

Escreva o **grão** em linguagem comum: uma linha é um evento, uma entidade ou um contrato em um mês? Na tabela fictícia `catalogo.esquema.eventos_exemplo`, `E001` pode aparecer três vezes porque teve três ocorrências. Nesse caso, `id_cliente` não é chave única da tabela, embora possa ser a entidade que será agregada. Se a pergunta é sobre clientes únicos, conte entidades; se é sobre eventos, conte linhas. Anote também chave candidata no grão real, como `id_evento` se cada ocorrência tiver identificador próprio. Essa distinção evita chamar duplicidade um comportamento esperado ou esconder uma duplicidade verdadeira.

Delimite a fonte e o período: nome autorizado da tabela, filtros, snapshot ou data de extração, coluna de data e janela estudada. Se houver alvo, descreva quando ele é observado e qual data representa a decisão. Uma resposta futura pode ser analisada como alvo, mas não pode ser colocada entre características conhecidas antes da decisão. Se o alvo ainda não amadureceu para as linhas recentes, separe essas linhas em vez de tratá-las como ausência do evento. Para o retrato inicial, você pode deixar o alvo fora e registrar que a relação com ele virá em outra etapa.

Confirme acesso e sensibilidade antes de exibir dados. A EDA profissional recomenda agregações Spark e visualizações sobre resultados limitados; linhas pessoais, identificadores ou texto livre podem exigir mascaramento ou exclusão conforme a política do ambiente. Não transforme um notebook de amostra em cópia da tabela inteira no processo Python. Se uma coluna parece categórica mas contém milhões de identificadores diferentes, um gráfico de todas as categorias não ajuda o leitor e pode custar caro. Registre o limite aplicado à amostra e a semente usada para que outra pessoa saiba o que viu.

Ao final desta preparação, você deve conseguir preencher uma ficha curta: objetivo, fonte, população, unidade de linha, chave candidata, período, filtros, data de decisão, alvo se houver e o que permanece desconhecido. Um exemplo ilustrativo seria: “eventos de janeiro a março de 2026; uma linha por ocorrência; `id_evento` candidato a chave; `id_cliente` pode repetir; sem alvo confirmado”. Essa ficha acompanha tanto a skill quanto uma chamada isolada de helper. Se não há fonte ou período estabelecido, descubra-os primeiro; um número sem população definida não responde à pergunta inicial.

Verifique ainda se o período da pergunta coincide com o conteúdo inteiro da tabela. `quick_profile` e `data_quality_check` recebem um nome de tabela e leem essa tabela; eles não aceitam diretamente um filtro de datas. Se a tabela contém vários anos, o resultado desses helpers descreve todos eles. Para medir somente janeiro a março, use um DataFrame filtrado nos snippets que recebem DataFrame, ou providencie uma fonte autorizada cujo conteúdo já corresponda ao recorte e registre como ela foi formada. Escrever “janeiro a março” no briefing sem aplicar o filtro no dado não modifica o denominador das porcentagens.

<a id="mu08-2"></a>
#### 2. Quando pedir EDA completa e quando fazer uma verificação curta?

Use a skill `hub-ml-eda-profissional` quando precisa de um diagnóstico integrado de **uma** fonte: granularidade, chaves, qualidade, distribuições, relações, visualizações agregadas e recomendações. Ela traz um roteiro, templates e uma rota protegida de execução. Distribuições e diagnóstico visual entram por padrão nessa rota; prévia e amostra são opt-in. Escolha os itens pertinentes e reaproveite evidência do mesmo snapshot/run, sem repetir varreduras por ritual. Para solicitar, informe a ficha construída acima e o formato de entrega: notebook, relatório ou ambos. Um briefing útil é: “Analise a tabela autorizada X, uma linha por evento, de janeiro a março; avalie a chave candidata Y, nulos e cobertura, distribuições e possíveis sinais para o alvo Z, que ainda precisa ser confirmado; entregue achados, limites e próximos testes”. Substitua X/Y/Z pelo contexto real e indique restrições de visualização.

A skill atual tem uma rota L4 de execução e finalização. O runner `run_enforced` usa o core analítico e coleta evidência dos recursos e templates aplicáveis; depois `finalize_or_raise` confronta o resultado com o handoff e o postflight. Se o runner devolve `PENDING_POSTFLIGHT`, isso significa que ainda falta a finalização, não que a EDA foi concluída. Só o payload final com `postflight.status='PASS'`, `completion.authorized=True` e `completion.status='COMPLETED'` autoriza dizer que a execução daquela skill terminou conforme o contrato. Um `PASS` isolado de preflight confere pré-condições; não prova que análises foram feitas. Para o leitor, a ação é pedir que a rota termine e observar esse estado final, não editar um dicionário de resultado manualmente.

Se a execução lançar `CanonicalExecutionBlocked`, a rota canônica daquele run parou. Leia o motivo: pode faltar recurso obrigatório, entrada objetiva ou evidência. Corrija a fonte ou contexto real e inicie outro run pela mesma rota quando possível; não declare a EDA concluída juntando chamadas manuais por fora. Se ainda não há chave primária candidata estabelecida, não invente `pk_columns` para satisfazer `data_quality_check`; a própria skill sabe marcar esse recurso como não aplicável no contexto apropriado. Uma instrução simultânea para selecionar a skill e pular runner/postflight entra em conflito com seu contrato; explicite o conflito e peça uma decisão de tarefa coerente.

Para uma pergunta menor e independente, use um objeto isolado. “Quais colunas, tipos, volume e alguns valores aparecem?” pede `quick_profile`. “Quantos nulos há por coluna?” pede `null_summary`; “a chave candidata está única e recente sob nossa política?” pede `data_quality_check`. “Quero cinco linhas legíveis” pede `safe_display`, que limita prévia; “quero um recorte limitado para inspeção” pode pedir `smart_sample`, respeitando seus limites de inclusão. São perguntas diferentes e a resposta de uma não substitui as outras. O [roteiro de script isolado](MU-parte-ii.md#mu07) ensina importação e leitura de dicionários; o [roteiro de snippet isolado](MU-parte-ii.md#mu06) explica como incorporar o DataFrame recebido no notebook.

Uma EDA rápida pode ter escopo reduzido, mas precisa manter a distinção entre achado e hipótese. Uma contagem de nulos acima de um limite mostra ausência naquela coluna; não diz se a causa foi extração, regra de negócio ou população incorreta. Uma distribuição com cauda longa sugere olhar extremos; não autoriza remover observações automaticamente. Se a pergunta evoluir para cruzar **duas ou mais fontes**, siga a rota de cross-EDA do MU09. Se evoluir para teste de hipótese com valor-p e tamanho de efeito, escolha a skill de validação estatística. Se evoluir para visualização pronta para comunicação, use os capítulos de trabalho visual. Essa escolha evita pedir à EDA de uma fonte uma conclusão para a qual falta outra base ou outro método.

Há um limite técnico importante para não prometer uma execução impossível. O Hub fornece código, templates e contratos; a análise precisa de tabela legível, ambiente compatível e dados com significado conhecido. Ter o arquivo `SKILL.md` na árvore não prova que a skill foi publicada ou homologada no workspace em que você está. Antes de pedir resultado, confira se o ambiente atual tem o pacote instalado e acesso autorizado à fonte; a rota MU02 cobre essa preparação. Se você só está lendo esta edição offline, use os exemplos como instruções e não como resultados produzidos pelo seu ambiente.

Para transformar a escolha em uma decisão concreta, imagine duas solicitações. Na primeira, a equipe quer decidir se uma base pode sustentar um estudo e precisa de relatório com limitações, hipóteses, gráficos e recomendações: entregue o briefing à skill e confira cada etapa de sua rota protegida. Na segunda, um analista recebeu uma dúvida estreita — “a coluna de evento está nula no trimestre?” — e já tem um DataFrame do trimestre: `null_summary` responde essa pergunta sem pedir uma análise completa. Se a dúvida curta revelar um problema estrutural, registre o achado e amplie o escopo de modo explícito. Esse encadeamento mantém claro o que foi verificado, em qual população e por qual ferramenta.

Se você for receber uma EDA feita por outra pessoa, confira o relatório como artefato de trabalho: a fonte e a janela correspondem ao pedido? Há contagens para acompanhar percentuais? A análise separa amostra de população? As figuras têm escala, unidade e legenda suficientes? Estão descritos itens não aplicáveis e dados insuficientes? Um arquivo de notebook que abre sem erro ou um gráfico bonito não responde sozinho a essas perguntas. Na rota protegida, leia também a evidência de finalização; na rota direta, documente suas próprias verificações, sem atribuir a elas o estado de execução da skill.

<a id="uso-hub-ml-eda-profissional"></a>
##### Ficha de uso — hub-ml-eda-profissional

<!-- usage-card:start hub-ml-eda-profissional -->
Escolha EDA profissional para compreender uma fonte de modo integrado, reunindo perfil, qualidade, distribuições, relações e recomendações. Para uma contagem independente, considere o helper isolado. Informe tabela autorizada, população, grão, chave candidata, período, disponibilidade temporal, alvo quando houver, custo permitido e formato da entrega. Use desconhecidos explícitos, sem inventar uma chave para satisfazer um requisito.

O pedido abaixo começa pelo plano. Antes de autorizar execução, confira recorte, operações, recursos, efeito e destino. A entrega esperada depois da execução autorizada é notebook ou relatório com achados sustentados, limitações e próximos testes, acompanhado da finalização canônica. Na versão L4/enforce, o runner e o postflight pertencem à rota selecionada: `PENDING_POSTFLIGHT` ainda não conclui a tarefa. Confira `postflight.status=PASS`, `completion.authorized=true` e o estado final de conclusão, além da coerência dos denominadores e da origem dos números. Um Receipt isolado não substitui essa conferência. Se a rota bloquear, leia o motivo, corrija entrada ou recurso real e inicie outra execução canônica quando possível; conserve o resultado como não concluído enquanto faltar evidência. A resposta deve separar hipótese de achado observado.

```text
@hub-ml-eda-profissional
Quero avaliar a fonte autorizada [TABELA], uma linha por [GRÃO],
no período [INÍCIO/FIM], com chave candidata [CHAVE OU NÃO INFORMADO].
Disponibilidade temporal e alvo: [DEFINIÇÕES OU NÃO INFORMADO].
Primeiro apresente plano, recursos e custos; não execute nesta etapa.
Após autorização específica, entregue [NOTEBOOK/RELATÓRIO], limites e
evidências da execução canônica e da finalização. Não invente requisitos.
```
<!-- usage-card:end hub-ml-eda-profissional -->

<a id="mu08-3"></a>
#### 3. Como fazer uma exploração direta com perfil, qualidade e prévia?

Suponha que a tarefa pontual seja reconhecer a tabela `catalogo.esquema.eventos_exemplo` e decidir se ela merece uma EDA completa. Substitua esse nome por uma tabela real autorizada. Execute primeiro um perfil, porque ele registra linhas, tipos e nulos da tabela inteira e resumos limitados por amostra. No exemplo, assuma que a tabela nomeada já contém somente os meses definidos na ficha; se contiver mais meses, as saídas de perfil e qualidade não estarão restritas ao trimestre. A fração de 10% controla a amostra das estatísticas, não a contagem total:

```python
from hub_scripts.quick_profile import quick_profile

table_name = "catalogo.esquema.eventos_exemplo"  # placeholder
perfil = quick_profile(table_name, sample_fraction=0.10, seed=42)
print(perfil["total_rows"], perfil["sample_rows"])
print(perfil["null_summary_full_table"][:5])
```

Leia `dtypes` antes de decidir gráficos; confira `sample_rows` antes de interpretar `numeric_summary_sample` ou `top_values_sample`. `quick_profile` só percorre um número limitado de colunas para algumas medidas, então ausência de estatística não é ausência da coluna. Se você observar 100 linhas e 10 nulos em `valor`, isso é um fato integral sobre nulos do perfil. Se a média vier de aproximadamente 10 linhas selecionadas, trate-a como retrato exploratório sujeito à amostra. Se a fração for pequena demais para categorias raras, ajuste o desenho da amostra conscientemente ou faça agregação específica sobre a população, anotando o custo.

Depois, confirme a unidade e uma chave **candidata**. Se cada linha é evento, `id_cliente` pode repetir legitimamente; use `id_evento` apenas se o produtor definiu um identificador por ocorrência. A chamada a seguir retorna um dicionário de checks e alertas sob limiares locais. Como o trimestre ilustrativo é histórico, ela omite `date_column`: essa opção mede frescor pela maior data em relação ao dia do ambiente e, neste caso, uma reprovação seria esperada sem dizer nada sobre a completude histórica.

```python
from hub_scripts.data_quality_check import data_quality_check

qualidade = data_quality_check(
    table_name, pk_columns=["id_evento"],
    thresholds={"null_warn": 5, "null_fail": 20},
)
print(qualidade["status"], qualidade["checks"]["pk_uniqueness"])
for alerta in qualidade["alerts"]:
    print(alerta["check"], alerta["severity"], alerta["message"])
```

Quando só precisa da distribuição de nulos por coluna, `null_summary` trabalha sobre um **DataFrame Spark** que você já selecionou, o que permite aplicar o recorte definido na ficha. Confirme que o recorte não está vazio antes da chamada; a implementação pode falhar ao converter uma soma nula em inteiro em tabela vazia. Os defaults 5/20 são limiares locais da função, não critério universal de qualidade. Se o perfil e o resumo de nulos usam recortes diferentes, seus percentuais também serão diferentes, sem que uma das funções esteja errada.

Interprete os alertas de `data_quality_check` por componente. `status='pass'` significa apenas que os checks configurados não violaram esses limiares naquela tabela: ainda falta confirmar se a chave representa o grão correto e se as colunas exigidas pelo estudo existem. `status='warn'` aponta uma taxa de nulos no patamar de aviso; planeje investigar coluna, população e impacto antes de usá-la. `status='fail'` pode vir de duplicidade ou componente nulo da chave, taxa de nulos no patamar de falha ou frescor quando essa opção foi ativada. Nesse caso, leia `alerts` e `checks` para localizar a causa em vez de interpretar `score` como uma nota geral de aptidão para modelagem. O número é uma pontuação local formada pelos alertas, não uma certificação da base. Confira `row_count`: tabela vazia pode receber `pass` com limiares positivos e sem freshness; isso não representa uma população adequada.

```python
from hub_snippets.spark.null_summary import null_summary

base = spark.table(table_name).filter("dt_evento >= '2026-01-01' AND dt_evento < '2026-04-01'")
if base.limit(1).count() == 0:
    raise ValueError("recorte sem linhas; confira período e filtros")
nulos = null_summary(base, threshold_warn=5, threshold_fail=20)
nulos.show(truncate=False)
```

Para inspecionar linhas, escolha entre **prévia** e **amostra**. `safe_display` observa no máximo `limit+1` linhas para indicar truncamento e envia até `limit` ao renderer; ele não sorteia linhas. `smart_sample` pode produzir uma amostra sem reposição limitada por `n`; no modo estratificado preserva pelo menos uma linha por categoria quando o número de estratos cabe no orçamento. Preservar categoria rara altera proporções, e o modo simples pode devolver menos de `n` e não garante inclusão probabilística uniforme. Com 110 linhas e `n=100`, a fração calculada é 1 e o limite pode selecionar um prefixo. Nenhum dos dois autoriza trazer a base inteira para pandas. A chamada abaixo é apenas para um notebook em que `display` está disponível; fora dele, passe uma função de exibição apropriada.

```python
from hub_snippets.spark.safe_display import safe_display
from hub_snippets.spark.smart_sample import smart_sample

safe_display(base, limit=5, display_fn=display)
amostra = smart_sample(base, n=100, stratify_col="canal", seed=42)
amostra.limit(5).show()
```

Antes de usar `stratify_col`, confirme que `canal` existe e que preservar cada categoria faz sentido para a pergunta. Confira também se a entrada tem `__sample_rank` ou `__stratum_target`: esses nomes auxiliares podem ser sobrescritos, removidos ou causar ambiguidade. Renomeie ou recuse a entrada antes da chamada; o helper não faz essa guarda completa. Se a fonte tem mais categorias que `n`, `smart_sample` recusa o pedido; aumentar `n` ou escolher outro agrupamento exige avaliar custo e objetivo. Registre a semente, o recorte e o número de linhas efetivo da amostra. Para uma apresentação visual, agregue no Spark e leve somente o resultado pequeno ao gráfico; a [trilha visual](MU-parte-v.md#mu14) desenvolve tema, escala, legenda e acessibilidade. Aqui o resultado esperado é um diagnóstico inicial: grão e chave plausíveis, qualidade medida, distribuições que merecem aprofundamento e dúvidas documentadas.

Um pequeno resultado ilustrativo mostra como decidir. Suponha 100 eventos no recorte, 10 valores ausentes em `valor` e dois `id_evento` duplicados na tabela nomeada. O resumo de nulos sustenta a frase “10% dos eventos do recorte não têm `valor`”; o alerta da chave sustenta “a tabela nomeada viola a unicidade candidata”. Antes de combinar ambos em uma conclusão, confirme que a tabela nomeada e o recorte do DataFrame contêm a mesma população. Se não contêm, relate dois universos separados e repita a checagem de chave na população correta por uma rota apropriada. O exemplo não é uma medição real.

Também verifique o que cada retorno não revela. `safe_display` mostra primeiras linhas conforme a ordem de leitura disponível, sem sorteio nem representatividade estatística. `smart_sample` oferece inspeção amostral, mas mesmo com semente registrada pode deixar de fora anomalias raras; uma ausência na amostra não equivale a zero ocorrência na base. `quick_profile` limita cardinalidade, categorias, resumos numéricos e intervalos de datas a subconjuntos de colunas e à amostra. Ao compartilhar a exploração, deixe esses limites junto da tabela ou figura. Assim o próximo leitor não transformará uma prévia conveniente em afirmação sobre toda a população.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu08-h-fontes-desta-parte"></a>
##### Fontes desta parte

`ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md`, contrato, runners e templates; implementações/READMEs de `quick_profile`, `data_quality_check`, `null_summary`, `safe_display` e `smart_sample` em `ambiente_fonte/.assistant/`. Todas as tabelas, valores e chamadas são ILLUSTRATIVE e dependem de substituição por fonte autorizada. Não houve execução de skill ou Spark para esta redação.
<!-- editorial:exclude:end -->

<a id="mu08-4"></a>
#### 4. Como transformar a exploração em decisão e passar o trabalho adiante?

Feche a exploração respondendo à pergunta que a abriu. Para o exemplo dos eventos, uma conclusão prudente seria: “A tabela parece ter o grão de ocorrência; a chave `id_evento` precisa de correção por causa de duas repetições; 10 dos 100 eventos do trimestre têm `valor` ausente; ainda não sabemos se esses nulos significam falha de carga ou regra de negócio”. Os números são **ilustrativos**. O valor da frase está em separar uma observação medida, uma interpretação provisória e o que falta descobrir. “A base está pronta” seria precipitado, porque nem a semântica dos nulos nem a unicidade foram resolvidas.

Monte um relatório que outra pessoa possa conferir sem adivinhar o recorte. O template de relatório executivo da skill propõe identificação da tabela, período, volume, grão, data da análise, notebook fonte, qualidade, padrões, anomalias, implicações e próximos passos. Na rota direta, você pode usar a mesma organização sem atribuir à chamada isolada o status da skill. Abra com a decisão que a EDA apoia e seus limites. Em seguida, declare nome da fonte, snapshot ou momento de leitura, filtros, contagens, unidade, chave candidata, amostra e semente. Para cada tabela ou gráfico, identifique denominador, unidade e período. Se o perfil abrange toda a tabela mas um gráfico cobre só o trimestre, diga isso junto do resultado; não misture percentuais em uma única comparação.

Para cada achado importante, escreva uma linha de raciocínio: evidência observável, população afetada, consequência possível, hipótese de causa e teste seguinte. Por exemplo, “`valor` está ausente em 10% dos eventos do recorte; qualquer média feita só sobre valores presentes pode representar outra população; verificar com o responsável pela origem se ausência significa evento sem valor ou perda de captura”. O teste não é preencher os nulos imediatamente. Em outro caso, uma categoria rara vista na amostra estratificada pode merecer uma contagem na população antes de virar recomendação operacional. Mostre também resultados negativos relevantes, como “não avaliamos consistência entre fontes”, para delimitar a conclusão.

O handoff da skill EDA possui campos explícitos: `sources_snapshot`, `unit_keys_target`, `quality_risks`, `feature_candidates_leakage`, `filters_sample` e `open_questions`. Preencha cada um com conteúdo verificável; a lista de questões pode ficar vazia quando nada material está pendente, mas não invente chave, alvo ou snapshot para obter uma aprovação. Se o postflight indicar `REVIEW`, resolva as pendências do handoff e finalize novamente pela rota apropriada; se indicar `FAIL` ou `BLOCKED`, leia a evidência e corrija a causa antes de repetir o run canônico. Na exploração direta, mantenha os mesmos campos como notas de passagem, sabendo que isso não produz Receipt nem Postflight da skill.

Defina a próxima ação conforme a pergunta que restou. Se o problema é duplicidade, peça ao produtor a regra de identificação e repita a checagem no grão correto. Se a cobertura do período está incompleta, investigue extração e partições antes de interpretar tendência. Se são duas fontes a reconciliar, vá ao MU09 com chave, janela e diferenças já registradas. Se a decisão envolve construção de variáveis, leve candidatos e suspeitas de vazamento à rota de feature engineering; se exige evidência estatística, formule hipótese e população para validação. Para apresentação, leve apenas resultados agregados e as limitações à trilha visual. O destinatário deve conseguir dizer que dado recebeu, o que foi realmente medido e qual pergunta permanece aberta.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu08-h-fontes-desta-parte-1"></a>
##### Fontes desta parte

`ambiente_fonte/.assistant/skills/hub-ml-eda-profissional/SKILL.md`, `execution_contract.json`, `templates/relatorio_executivo_eda.md` e `scripts/postflight.py`. Exemplo de 100 eventos, 10 nulos e duas repetições é ILLUSTRATIVE; não houve execução sobre dados reais para este texto.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU07](MU-parte-ii.md#mu07) · [Próximo: MU09](#mu09) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT19](MT-parte-iv.md#mt19)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu09"></a>
<a id="mu09"></a>
### MU09 — Comparar e cruzar fontes com cuidado temporal

<!-- editorial:exclude:start -->
**Você quer:** saber se duas fontes podem compor uma base sem mudar indevidamente a unidade de análise ou trazer informação futura. **Rota:** descreva as fontes e a decisão (1); compare compatibilidade e escolha a profundidade do estudo (2); faça diagnósticos de chave e tempo (3); decida com evidências (4). Tabelas e valores do exemplo são sintéticos; o código é uma receita a adaptar, não um resultado executado.
<!-- editorial:exclude:end -->

<a id="mu09-1"></a>
#### 1. Que chaves, grão e período cada fonte realmente possui?

Imagine que a equipe queira acrescentar ao evento de contato de um cliente a última informação de relacionamento disponível antes desse contato. A fonte **âncora** é a tabela de contatos: ela define quantas decisões serão estudadas e o que significa preservar uma linha. A fonte complementar é um histórico de informações do cliente. Antes de arrastar uma coluna com o mesmo nome para um `join`, escreva uma frase por fonte: “uma linha de `contatos` é uma decisão de contato de `id_cliente` em `ts_decisao`”; “uma linha de `historico` é uma versão de `saldo` referente a `ts_feature`”. A mesma chave textual pode representar unidades diferentes.

Registre o identificador de entidade e, se a linha de decisão precisar ser única, sua chave de evento. `id_cliente` pode repetir corretamente na âncora porque o cliente foi contatado mais de uma vez. Na direita, várias linhas por cliente também podem ser corretas, pois representam versões; um join apenas por `id_cliente` multiplicaria os contatos. Uma chave composta, como cliente e data de referência, só ajuda se esses componentes definem a mesma relação nos dois lados. Não invente uma chave única a partir de uma coluna conveniente. Se um lado usa contrato e o outro cliente, obtenha uma regra de mapeamento validada antes de chamar ambos de “mesma entidade”.

Monte um cartão de fonte para cada lado antes da execução. Os exemplos abaixo servem para conferir a informação que falta, não são cadastro real:

| Cartão | Âncora: contatos | Complementar: histórico |
|---|---|---|
| Grão | Uma linha por contato/decisão | Uma linha por cliente e versão de referência |
| Chave e tempo | `id_cliente`, `id_contato`, `ts_decisao` | `id_cliente`, `ts_feature` e instante de disponibilidade |
| População | Contatos do trimestre definido | Histórico que pode cobrir esse trimestre |
| Snapshot e filtro | Identificador/data de leitura e filtros | Identificador/data de leitura e filtros |
| Qualidade a confirmar | Chaves e datas nulas, duplicidade de `id_contato` | Duplicidade por versão, datas nulas, atraso de publicação |
| Restrição | Uso permitido e sensibilidade | Uso permitido e sensibilidade |

Esse cartão impede que duas porcentagens incompatíveis pareçam uma cobertura única. Meça a população da âncora em linhas de decisão e, quando necessário, em entidades únicas. Um cadastro pode cobrir 90% dos clientes únicos e apenas 70% dos contatos se os clientes sem cadastro forem mais frequentes; ambas as medidas respondem a perguntas distintas. Anote se o período é o da decisão, da referência da feature ou de sua publicação. Para uso preditivo, o alvo e seu horizonte ficam separados: uma resposta ocorrida depois do contato pode ser o resultado a prever, mas não uma característica disponível antes do contato.

Se você não conhece o grão ou o instante de disponibilidade, peça essa definição ao responsável pela fonte e faça uma exploração limitada, sem declarar prontidão para modelagem. Uma comparação de schemas ajuda a localizar colunas e tipos, mas não prova igualdade semântica. A próxima seção mostra como reunir EDAs de fontes individuais; os números de join só ganham sentido quando o cartão diz qual linha deve sobreviver.

Preveja como conferirá a preservação: conte os contatos da âncora antes da operação e exija o mesmo número de linhas depois de uma junção que promete uma versão por decisão. Separe contatos com chave nula dos que têm chave válida sem histórico. Para evitar conclusões de um snapshot mutável, anote o identificador da versão ou um corte reprodutível de cada fonte; se a origem muda entre o diagnóstico e a materialização, o número previsto pode deixar de coincidir. Quando não há snapshot fixável, indique essa limitação e repita a contagem sobre as entradas efetivamente usadas.

<a id="mu09-2"></a>
#### 2. Como comparar as tabelas e usar a orientação de cross-EDA?

Se cada fonte ainda é pouco conhecida, faça primeiro a EDA de uma fonte do MU08 para cada uma, mantendo snapshot, filtro, grão e limitações. Depois use a skill `hub-ml-cross-eda-ml` para organizar a pergunta entre fontes: inventário dos EDAs, resolução de entidade, alinhamento temporal, simulação de joins, cobertura, qualidade combinada e decisão de prontidão. Um pedido útil seria: “Avalie se contatos por cliente e horário podem receber a última versão de saldo disponível antes do contato; preserve a linha de decisão, documente duplicações e não correspondências por mês; proponha GO, CONDICIONAL ou NO-GO com evidência, responsáveis e critérios”. Inclua os dois cartões e informe target/horizonte se a intenção é modelagem.

A policy mantém `current_level=L0/audit`; o alvo L4 não foi promovido. Entretanto, o código integrado já contém três rotas sintéticas distintas, descritas no [README dos scripts](../../skills/hub-ml-cross-eda-ml/scripts/README.md): contexto, diagnóstico e PIT. O contexto L2 não executa Spark nem mede cobertura. `run_diagnostic.py` calcula cardinalidade/cobertura, exige verificação com entradas e diagnóstico esperado externos e não produz join de negócio. `run_pit.py` executa o perfil temporal local; `verify_pit.py` finaliza e reverifica seus inputs, janela e run. Escolha o contrato antes de autorizar ações. Um PASS do contexto não prova join, e o perfil executável não certifica todo pedido de cross-EDA nem prontidão para ML.

Há também briefings de comparação de tabelas e de cross-EDA no catálogo de prompts. Eles ajudam a formular intenção, fontes, coluna-chave, diferenças de schema, cobertura e saída desejada; não consultam dados por si. Use o briefing de comparar tabelas quando a primeira dúvida é estrutural — colunas, tipos, grão e compatibilidade — e o de cross-EDA quando a decisão exige juntar achados de múltiplas fontes e avaliar uso para ML. Informe o que é desconhecido em vez de preencher lacunas com supostos valores. Um prompt bem preenchido não transforma duas tabelas distintas em uma chave válida.

Faça uma comparação que respeite o papel de cada fonte. Verifique formatos de `id_cliente`, nulos, regras de normalização, cobertura de datas e cardinalidade por chave. Compare a data máxima do histórico com o período de decisões, mas não conclua que todas as decisões antigas tinham acesso ao dado só porque o snapshot atual o contém. Uma linha antiga pode ter sido corrigida ou publicada depois. Verifique também se colunas com o mesmo nome têm unidade e interpretação iguais: `valor` pode ser um saldo monetário em uma fonte e um código em outra. A comparação estrutural deve virar perguntas objetivas ao produtor, não um merge automático de schemas.

Use uma pequena matriz de viabilidade, com evidência em cada célula. Ela facilita perceber que “cobertura alta” e “sem futuro” são condições diferentes:

| Dimensão | Pergunta verificável | Evidência a registrar |
|---|---|---|
| Entidade | As chaves representam o mesmo cliente? | Regra de mapeamento, nulos, conflitos |
| Cardinalidade | Uma decisão vira quantas linhas? | Expansão prevista left/inner e amostra de chaves |
| Tempo | A versão existia na decisão? | Referência, atraso, fuso, janela e disponibilidade |
| Cobertura | Quem fica sem feature e por quê? | Denominador e causas separadas por mês/segmento |
| Qualidade e uso | O valor é coerente e permitido? | Domínios, sensibilidade, restrições e dono |

Se a âncora tiver três contatos para o mesmo cliente, conte três decisões ao avaliar cobertura por linha; se o problema é inclusão de clientes, conte também entidades. Não reduza as duas leituras a um único score. A classificação GO/CONDICIONAL/NO-GO da skill é um argumento com vetos possíveis: chave indefinida ou vazamento temporal material pode impedir GO apesar de boa cobertura. Se uma dimensão está desconhecida, registre responsável e teste de aceite. A próxima etapa mostra os helpers que produzem parte dessa evidência, não uma decisão automática.

Um caminho prático é comparar as fontes em duas passagens. Na primeira, sem join, verifique o contrato de cada uma: tipos de chave, percentual de chaves nulas, intervalo de datas e número de versões por entidade. Na segunda, sobre o mesmo recorte e snapshots declarados, meça cobertura e expansão e estratifique os achados por mês de decisão. Se cobertura cai em fevereiro, investigue se faltam clientes novos, se houve atraso na publicação ou se as chaves mudaram de formato. Uma média trimestral poderia ocultar que o primeiro mês está bem coberto e o último quase vazio. Só depois avalie se uma variável adicional melhora a análise ou o modelo, comparando populações equivalentes e separação temporal adequada.

Não confunda “mesma quantidade de linhas” com “cruzamento correto”. Um `left join` com direita única pode manter o total e preencher todos os atributos com nulo porque as chaves têm formatos incompatíveis. Também pode preservar a cardinalidade e usar uma versão atual para explicar uma decisão antiga, introduzindo informação futura. Exija uma checagem de conteúdo e de instante além da contagem. Quando a conclusão depende de uma tabela de correspondência entre identificadores, documente quem a mantém e desde quando cada associação é válida. Uma correspondência criada depois da decisão pode conter informação que o processo histórico não tinha.

O relatório de cross-EDA deve mostrar, para cada decisão GO/CONDICIONAL/NO-GO, o dado que a sustenta e a ação que a tornaria revisável. “CONDICIONAL: 12% dos contatos de fevereiro não têm feature elegível; responsável pela fonte verificará atraso de publicação e repetiremos o diagnóstico” é melhor que “faltam alguns dados”. “NO-GO: origem não guarda versões históricas e não permite reconstruir disponibilidade” indica um bloqueio que mais Spark não resolve. Evite transformar uma observação de correlação entre colunas em prova de sinal incremental: para isso, seria preciso comparar modelos ou análises com e sem a fonte em população e período comparáveis.

<a id="uso-hub-ml-cross-eda-ml"></a>
##### Ficha de uso — hub-ml-cross-eda-ml

<!-- usage-card:start hub-ml-cross-eda-ml -->
Escolha cross-EDA quando precisa decidir se várias fontes podem compor uma análise ou base de modelagem. Informe os cartões das fontes, unidade de decisão, chaves, snapshots, filtros, período, alvo e horizonte, disponibilidade dos atributos e restrições de uso. Se ainda não conhece uma fonte, faça sua exploração individual antes de concluir que o cruzamento é viável. Sem tempo confiável, mantenha a prontidão preditiva em aberto.

O pedido abaixo organiza a investigação antes de qualquer materialização. A entrega esperada é mapa das fontes, contrato temporal, diagnóstico de cobertura e multiplicidade, riscos e decisão GO, CONDICIONAL ou NO-GO com responsáveis e próximos testes. Confira quais medições foram realmente executadas, em quais recortes e com qual denominador. Verifique perdas e duplicações separadamente e examine exemplos de versões anteriores e posteriores à decisão. A skill está em L0/audit na policy vigente. Contexto, diagnóstico e PIT têm contratos distintos; o preflight de contexto não executa join e não substitui a finalização/verificação do perfil PIT. Se o agente oferecer apenas um plano por falta de acesso, registre a entrega como proposta. Não preencha medições faltantes com os números ilustrativos deste capítulo.

```text
@hub-ml-cross-eda-ml
Avalie a viabilidade de combinar [ÂNCORA] e [COMPLEMENTAR].
Cartões, snapshots, filtros e restrições: [CONTEXTO].
Unidade, chaves, decisão, alvo/horizonte e disponibilidade: [DEFINIÇÕES].
Primeiro apresente plano; não materialize nem execute nesta etapa.
Proponha verificações de cobertura, expansão e tempo, decisão condicionada
e próximos testes. Declare toda medição ainda não realizada.
```
<!-- usage-card:end hub-ml-cross-eda-ml -->

<a id="mu09-3"></a>
#### 3. Como diagnosticar expansão e escolher a versão disponível no tempo?

A receita direta abaixo ensina os helpers; não substitui o runner de um perfil já selecionado. O perfil `LOCAL_SYNTHETIC_PIT_V1` exige UTC, fronteira inclusiva e janela positiva, limita cada fonte a 500 linhas e bloqueia atraso variável, fronteira `LT` ou bitemporalidade. Preserve inputs e run_id externos ao payload para a verificação.

Comece por `diagnosticar_join` quando quer saber o efeito **de uma chave** antes de combinar as colunas. Ele recebe dois DataFrames Spark, chave simples ou composta e número de exemplos de chaves órfãs. A chamada pode fazer contagens, agregações e joins de diagnóstico; portanto, prepare uma população filtrada, fonte autorizada e compute compatível. Se a tabela de histórico contém várias versões por cliente, um diagnóstico por `id_cliente` revela a multiplicação de um join ingênuo, não significa que você deva materializá-lo.

```python
from hub_snippets.spark.join_diagnostics import diagnosticar_join

contatos = spark.table("catalogo.esquema.contatos_exemplo")  # placeholder
historico = spark.table("catalogo.esquema.historico_exemplo")  # placeholder
diag = diagnosticar_join(contatos, historico, "id_cliente", amostra_orfas=5)
print(diag["linhas_esquerda"], diag["linhas_apos_join_left"])
print(diag["cobertura_pct_chaves_validas"], diag["expansao_prevista_left"])
print(diag["exemplos_sem_match"])
```

Leia `cobertura_pct_chaves_validas` como porcentagem das **linhas da esquerda com chave não nula** que encontram alguma chave à direita. `chaves_nulas_esquerda` é uma causa separada. `linhas_apos_join_left` inclui órfãs e chaves nulas preservadas; `linhas_apos_join_inner` as perde. A multiplicidade da direita considera somente chaves presentes na esquerda. Se a esquerda ilustrativa tiver E001, E002 e uma chave nula, e a direita duas linhas E001, o left projetado tem quatro linhas: duas de E001, uma órfã E002 e uma sem chave. Cobertura das chaves válidas é 1/2, ou 50%; expansão left é 4/3, cerca de 1,333. Isso é aritmética ilustrativa da API, não medição Spark neste manual.

Quando a direita é um histórico, use `pit_join` para associar uma única versão elegível por decisão. Antes da chamada, confirme três relógios: instante da decisão, referência do valor e momento em que o valor ficou disponível. A API soma a `ts_feature` um `atraso_publicacao_dias` fixo e exige disponibilidade menor ou igual a `ts_decisao`. O atraso é obrigatório, inteiro não negativo; zero só quando disponibilidade imediata foi demonstrada. `janela_maxima_dias` limita a idade da **referência**. Se `ts_feature` for uma data sem horário, ela vira meia-noite no fuso da sessão; um fechamento diário tipicamente requer pelo menos um dia de atraso para não aparecer na manhã do mesmo dia.

```python
from hub_snippets.spark.pit_join import pit_join

com_saldo, pit = pit_join(
    contatos, historico, chave="id_cliente",
    ts_decisao="ts_decisao", ts_feature="ts_feature",
    atraso_publicacao_dias=1, janela_maxima_dias=30,
    colunas_feature=["saldo"], sufixo="_hist",
    politica_empate="erro", devolver_disponibilidade=True,
)
print(pit["linhas_fato"], pit["com_feature"])
print(pit["sem_feature_disponivel_na_data"], pit["fuso_da_sessao"])
com_saldo.select("id_cliente", "ts_decisao", "saldo_hist", "__feature_disponivel_em_hist").limit(5).show()
```

No cenário ilustrativo, a decisão de E001 em 12/01 às 14h pode usar uma versão referida a 11/01 às 10h com atraso de um dia: ficou disponível em 12/01 às 10h. Uma versão referida a 12/01 às 10h só chega em 13/01 às 10h e deve ficar de fora. Se E002 não tem histórico, sua linha continua no DataFrame com `saldo_hist` nulo. `pit` separa `sem_chave_ou_data`, `entidade_sem_historico` e `sem_feature_disponivel_na_data`, além de `com_feature`. Essas quatro categorias devem somar `linhas_fato`. `cobertura_pct_linhas_validas` exclui da base os fatos sem chave ou data; não leia 100% como cobertura de toda a âncora.

O `pit_join` executa ações de contagem e uma junção de candidatos potencialmente custosa. Evite também nomes auxiliares `__disponivel_em`, `__ts_feature_ref`, `__rank`, `__empatados` e prefixos `__pit_*`: o helper não confere todas as colisões. Confirme colunas e tipos antes de rodar e teste o desenho em dados pequenos ou representativos; não estime custo apenas pelo número final de linhas. O resultado tabular preserva os fatos, inclusive fatos repetidos, e acrescenta as colunas escolhidas. Confira a contagem de saída e compare manualmente algumas entidades com versões de ambos os lados da decisão. A coluna de disponibilidade devolvida ajuda a testar a regra sem presumir que `saldo` é o relógio. Se a fonte publica com atraso variável ou reescreve o passado sem histórico de revisões, um atraso fixo não reconstrói a disponibilidade real; obtenha dado melhor ou mude o desenho antes de chamar a junção de point-in-time correta.

As duas APIs respondem perguntas consecutivas, não intercambiáveis. `diagnosticar_join` revela o que um join por chave faria com a cardinalidade; seu 1:N pode ser esperado para uma tabela histórica. `pit_join` escolhe uma versão por combinação de entidade e decisão, respeitando tempo e atraso declarados. Se duas versões elegíveis empatam **no instante de disponibilidade mais recente selecionado** para uma entidade e decisão, a política padrão `politica_empate="erro"` levanta `ValueError`. Um empate antigo que não foi selecionado, ou uma versão futura inelegível, não dispara esse erro por si. Investigue duplicidade na origem e qual registro é verdadeiro. As opções `menor` e `maior` impõem um critério pelos valores trazidos; escolha-as apenas quando houver regra de negócio justificável, não para silenciar o erro.

Há dois tipos de ausência que pedem respostas diferentes. `entidade_sem_historico` sugere chave não mapeada, população fora da fonte ou fonte incompleta. `sem_feature_disponivel_na_data` significa que existe histórico para a entidade, mas nenhuma versão satisfaz disponibilidade e janela naquela decisão. Confira timestamp, fuso da sessão, atraso e idade máxima antes de mudar a população. Aumentar a janela apenas para elevar cobertura pode introduzir valores velhos; reduzir o atraso apenas para preencher nulos pode introduzir futuro. Se o diagnóstico mostrar `sem_chave_ou_data`, volte à qualidade dos fatos da âncora. Use `linhas_feature_com_ts_nulo` para inspecionar também um problema temporal na direita.

Registre as escolhas temporais ao lado do resultado: data de decisão, regra de publicação, janela, fuso e versão das entradas. Assim outra pessoa consegue reproduzir por que um valor foi aceito ou rejeitado.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu09-h-fontes-desta-parte"></a>
##### Fontes desta parte

`ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/{join_diagnostics.py,README.md}`; `ambiente_fonte/.assistant/hub_snippets/spark/pit_join/{pit_join.py,README.md}`; `ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/{SKILL.md,input.schema.json,scripts/README.md}`; `ambiente_fonte/.assistant/hub_scripts/skill_execution/domain_context/temporal.schema.json`; `ambiente_fonte/.assistant/hub_prompts/comparar_tabelas/comparar_tabelas.md`; `ambiente_fonte/.assistant/hub_prompts/cross_eda/cross_eda.md`. Exemplos e números são ILLUSTRATIVE, sem execução Spark, skill ou preflight nesta redação.
<!-- editorial:exclude:end -->

<a id="mu09-4"></a>
#### 4. Como interpretar multiplicação, perda, empate e bloqueio?

Confronte os diagnósticos com a unidade escolhida antes de publicar uma base combinada. Se cada linha de contato deve continuar sendo uma decisão, `expansao_prevista_left` acima de 1 indica que o join simples multiplicaria algumas linhas. No exemplo sintético da seção 3, a passagem de três para quatro linhas ocorre porque E001 tem duas versões à direita; não é um aumento de clientes nem de contatos. Evite somar resultados depois desse join como se fossem quatro decisões independentes. Uma saída legítima pode ser manter o histórico separado e usar `pit_join` para escolher uma versão disponível por decisão. Se a pergunta realmente exige uma linha por contrato e o histórico representa contratos, redefina o grão e documente a conversão, em vez de rotular toda expansão como defeito.

Perda também tem mais de uma causa. Para contar **linhas da âncora perdidas** por um inner join, some `chaves_nulas_esquerda` e `linhas_sem_match_chave_valida`. Não subtraia `linhas_apos_join_inner` de `linhas_esquerda`: duplicações de chaves casadas podem compensar perdas e até deixar os totais iguais. No exemplo anterior, E002 e a chave nula se perderiam, enquanto E001 produziria duas linhas; o inner teria duas linhas, mas perderia duas decisões originais. Um left preserva órfãs e chaves nulas, porém deixa atributos vazios; preservação de linhas não é cobertura de informação. Confira essas duas causas ao lado de `cobertura_pct_chaves_validas`, cujo denominador exclui chaves nulas. No `pit_join`, confirme que `linhas_fato` coincide com a âncora e que as quatro categorias se reconciliam. Depois olhe a cobertura por mês e segmento relevante, porque ausência concentrada pode tornar uma média global pouco útil.

Use um quadro de decisão para separar sintoma de resposta. Ele pode ficar no relatório de cross-EDA com responsável e critério de aceite:

| Sintoma | Leitura inicial | Próxima ação e aceite |
|---|---|---|
| Expansão 1:N no join simples | Mais de uma linha relevante à direita | Confirmar grão; selecionar versão temporal ou regra de agregação; recontar decisões |
| Chave nula ou órfã | Falha de identificação ou ausência na fonte | Investigar origem/mapeamento; medir cobertura no denominador declarado |
| Histórico inelegível | Dado existe, mas não estava disponível ou está velho | Conferir referência, atraso, fuso e janela com produtor; não antecipar publicação |
| Empate no instante escolhido | Versões concorrentes | Corrigir duplicidade ou justificar `menor`/`maior`; repetir checagem |
| Falta de histórico confiável | Passado não pode ser reconstruído | Bloquear afirmação temporal até obter versão e disponibilidade verificáveis |

Se `pit_join` parar por empate com a política padrão, preserve o erro como evidência de uma decisão ainda não tomada. A opção `maior` escolhe maior valor dentre colunas selecionadas em um desempate, mas isso não faz dele o valor verdadeiro; `menor` tem o mesmo limite. Investigue também colisão de nomes ao juntar múltiplas fontes: use `sufixo` com intenção clara e mantenha o nome da coluna de disponibilidade quando precisar auditá-la. Se faltar coluna ou o atraso for inválido, corrija a entrada real e execute novamente; não preencha com zero ou altere o timestamp para produzir uma linha.

Ao final, declare GO apenas se chave, grão, cobertura, temporalidade, qualidade e autorização de uso sustentam a aplicação proposta. Sem dados ou execução suficientes, registre **NÃO AVALIADO**. CONDICIONAL identifica pendências mitigáveis com responsável, prazo e teste reproduzível. NO-GO cabe quando não há chave coerente, disponibilidade histórica confiável ou cobertura suficiente para a população exigida. A skill de cross-EDA fornece o roteiro desse julgamento; seus templates de inventário, viabilidade, matriz de cobertura e scorecard ajudam a apresentar evidência, mas não promovem automaticamente o estudo a um nível de policy que ainda não foi promovido. Entregue ao próximo analista os cartões de fonte, filtros e snapshots, diagnósticos, regra de join, exemplos verificados manualmente, decisão e perguntas abertas. Assim ele sabe quais fatos pode reutilizar e quais hipóteses ainda exigem teste.

Se uma verificação falhar, registre a versão exata da entrada e repita os cálculos depois da correção. Compare a nova cobertura e a nova contagem de fatos com as anteriores: uma melhora no percentual pode vir simplesmente da exclusão de decisões difíceis, e essa perda precisa ficar visível para quem decide.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu09-h-fontes-desta-parte-1"></a>
##### Fontes desta parte

`ambiente_fonte/.assistant/hub_snippets/spark/join_diagnostics/join_diagnostics.py`, `ambiente_fonte/.assistant/hub_snippets/spark/pit_join/pit_join.py`, `ambiente_fonte/.assistant/skills/hub-ml-cross-eda-ml/SKILL.md` e templates de `coverage_matrix.md`, `join_feasibility.md` e `readiness_scorecard.md`. Quadro e números são ilustrações de leitura; nenhuma execução real foi alegada.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU08](#mu08) · [Próximo: MU10](#mu10) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT07](MT-parte-ii.md#mt07) · [MT17](MT-parte-iv.md#mt17)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu10"></a>
<a id="mu10"></a>
### MU10 — Preparar features, RFV, safra e estudos estatísticos

<!-- editorial:exclude:start -->
**Você quer:** transformar uma pergunta de negócio em variáveis ou em um estudo com tempo e evidência claros. **Rota:** escolha o instrumento (1), fixe cortes e definições (2), execute apenas a rota compatível com sua entrada (3) e interprete efeito, cobertura e incerteza (4). Os dados e resultados pequenos deste capítulo são ILLUSTRATIVE; nada foi executado em uma fonte corporativa.
<!-- editorial:exclude:end -->

<a id="mu10-1"></a>
#### 1. Preciso desenhar uma feature, calcular RFV, comparar safras ou testar uma hipótese?

Comece pela decisão que será tomada, não pela técnica que parece mais sofisticada. Se quer criar uma variável reutilizável para previsão, como “quantas compras o cliente fez nos 30 dias anteriores ao contato”, a rota é **feature engineering**: especificar fonte, grão, janela, disponibilidade, fórmula, dono e testes antes de materializar. Se só precisa calcular recência, frequência e valor em uma data comum, `rfv_calculator` já entrega medidas brutas. Se pergunta “os contratos originados em janeiro pioram mais cedo que os de março?”, a unidade é **safra**, ou coorte de entrada, comparada na mesma idade. Se precisa decidir se uma diferença observada é compatível com um efeito relevante sob incerteza, formule um estudo de **validação estatística** com hipótese e desenho.

O mesmo conjunto de dados pode originar as quatro perguntas, mas elas não têm a mesma saída. RFV soma e conta eventos até um corte; não escolhe segmento comercial. A análise de safra alinha contratos pela idade desde a origem; não prova causa da diferença. Uma feature é uma especificação que deve funcionar tanto no histórico quanto no momento de uso; uma estatística descritiva isolada não garante essa paridade. Um teste de hipótese responde a uma pergunta inferencial com pressupostos e intervalo; não transforma automaticamente uma variável em feature aceita. O quadro serve para escolher o próximo passo:

| Intenção do leitor | Entrada mínima | Rota do Hub | Saída que se deve conferir |
|---|---|---|---|
| Construir variável para decisão/modelo | Entidade, decisão, target, fontes e disponibilidade | `hub-ml-feature-engineering` e helpers adequados | Spec, código, testes e risco de vazamento |
| Resumir comportamento até corte comum | Tabela de eventos, entidade, data, valor e corte | `rfv_calculator` | DataFrame Spark com medidas brutas e janelas |
| Comparar coortes por maturação | Contrato, origem, observação, evento e corte | `hub-ml-analise-safra`; `build_vintage_table` para tabela pequena | Safra × MOB, cobertura e taxa quando completa |
| Avaliar diferença/pressuposto com incerteza | Hipótese, população, grupos, desenho e efeito relevante | `hub-ml-validacao-estatistica` | Plano, estimativa, intervalo, pressupostos e decisão condicionada |

As três skills permanecem L0/audit na policy, apesar de perfis executáveis já integrados. `target_level` não é promoção. Feature Engineering separa lag local, vista PIT em memória e materialização sintética autorizada; Safra oferece perfil mensal binário com roster fixo; Estatística oferece KS de duas amostras sintéticas. Cada rota exige contrato, inputs e verificador próprios. Use o `SKILL.md` e seu `scripts/README.md` antes do cálculo; helper avulso não substitui runner selecionado. Receipt ou PASS local não homologa dados reais, autoriza escrita nem torna toda a metodologia executável.

Um pedido pequeno e bem formulado orienta a escolha: “Em 31/01, quero medir compras por cliente nos últimos 30 dias para selecionar uma campanha” aponta RFV; “quero produzir esse atributo para cada contato histórico” exige janela por decisão e contrato de feature; “quero comparar contratos de janeiro e fevereiro no MOB 3” aponta safra; “quero saber se a diferença no MOB 3 excede o mínimo relevante” pede plano estatístico após confirmar população e maturidade. Se não sabe qual pergunta tem, descreva público, decisão e unidade de linha; o MU03 ajuda a localizar o recurso, e MU09 resolve a viabilidade de múltiplas fontes antes de juntar características.

Escolha também o nível de trabalho esperado. Um helper isolado responde a uma operação com entradas definidas; uma skill orienta a sequência de levantamento, verificação, interpretação e entrega. Um briefing preenchido pode pedir essa sequência de maneira clara, mas não executa cálculos por existir como arquivo. Se você precisa de uma decisão de negócio hoje, diga se quer apenas proposta de estudo, notebook para executar no ambiente autorizado ou resultado efetivamente calculado e revisado. Essa distinção evita que uma tabela de exemplo seja apresentada como evidência da sua carteira. Quando uma técnica não se encaixa, registre o motivo: uma carteira sem originação confiável não sustenta safra, e uma fonte sem histórico de publicação não sustenta afirmação point-in-time.

<a id="uso-hub-ml-feature-engineering"></a>
##### Ficha de uso — hub-ml-feature-engineering

<!-- usage-card:start hub-ml-feature-engineering -->
Escolha feature engineering quando deseja construir variáveis que possam ser reproduzidas no treino e no momento de uso. Informe entidade, chave, alvo, horizonte, instante de decisão, fontes, disponibilidade, janela de observação, frequência de cálculo e modo de consumo. Para uma fotografia RFV independente, o helper pode bastar; para uma variável histórica por decisão, o contrato precisa explicar como excluir informação que ainda não existia.

O pedido abaixo busca especificação antes da implementação. A entrega esperada reúne cartões de features, prioridades, transformação proposta, plano de materialização, testes, riscos e responsáveis. Confira fórmula, unidade, grão, corte temporal, ausentes e linhagem de cada variável. Exija exemplos de fronteira da janela e testes de paridade entre cálculo histórico e inferência. Parâmetros aprendidos, como mediana de imputação, devem ser ajustados somente no treino. A policy atual mantém esta skill em L0/audit: texto e templates não comprovam job executado, tabela criada ou feature aprovada. Se o tempo de publicação for desconhecido, peça investigação e mantenha a feature experimental ou bloqueada. Antes de executar, revise separadamente operações, custo e destino.

```text
@hub-ml-feature-engineering
Planeje [FEATURES] para [ENTIDADE/CHAVE], decisão [INSTANTE]
e alvo [DEFINIÇÃO/HORIZONTE]. Fontes e disponibilidade: [CONTEXTO].
Janelas, frequência, consumo e restrições: [DEFINIÇÕES].
Não execute nem materialize nesta etapa. Entregue specs, prioridades,
testes temporais e de paridade, riscos, responsáveis e lacunas.
```
<!-- usage-card:end hub-ml-feature-engineering -->

<a id="mu10-2"></a>
#### 2. Que data de referência e denominador tornam o estudo válido?

Registre quatro tempos antes de calcular: quando a entidade entrou ou o evento ocorreu, quando a decisão seria tomada, quando a informação ficou disponível e quando o resultado foi observado. Eles podem coincidir em uma tabela, mas não são sinônimos. Uma compra de segunda-feira publicada na sexta não estava disponível para decidir na terça. O `rfv_calculator` filtra pela **data do evento** até `dt_referencia`; sozinho, não modela atraso de publicação. Se a decisão é por contato, cada contato pode ter seu próprio instante e um corte global não basta. A rota `pit_join` do MU09 mostra como selecionar versões disponíveis em cada decisão, desde que a origem guarde histórico confiável.

Para RFV, fixe primeiro o grão: uma linha da tabela significa compra, item de compra ou atualização? A frequência do script é contagem de linhas. Se cada compra contém três itens, contar linhas resultará em três, não uma compra. A soma de `valor` também depende de estornos, moeda e nulos. Escreva a regra de negócio para esses casos antes de interpretar total. Escolha `dt_referencia` em formato de data, chave de entidade não nula e `periodos` inteiros positivos; a janela de 30 dias inclui o dia do corte e os 29 anteriores. Quem não tem evento válido até esse corte não aparece no retorno; isso difere de aparecer com frequência zero. Quando uma janela recente não tem eventos para um cliente que possui histórico anterior, os pares da janela são preenchidos com zero.

Um cartão de feature evita que uma coluna calculada hoje receba um significado diferente amanhã. Preencha, por exemplo, “`freq_compra_30d`: quantidade de compras distintas de `id_pedido` para `id_cliente`, nos 30 dias de calendário até o instante de decisão, usando apenas pedidos publicados até esse instante; origem X, atualização diária, tipo inteiro, nulos conforme ausência de histórico, dono Y”. O helper RFV não calcula `countDistinct(id_pedido)` nem filtra disponibilidade: se essas regras forem necessárias, a spec aponta uma adaptação ou outro processo. Não chame a saída RFV de implementação desse cartão até demonstrar equivalência.

Para safra, a origem define a coorte e **MOB** (*months on book*, meses desde a origem) define sua idade. O helper `build_vintage_table` calcula a diferença inteira entre ano/mês da observação e da originação, salvo se você fornecer `mob_col`. Uma observação de 31/01 e outra de 01/02 podem ficar em MOBs diferentes apesar de um dia de distância; declare essa convenção. Defina se o `target` 0/1 é evento naquele MOB ou indicador acumulado, pois `target_is_cumulative` muda a validação. Registre data de corte, snapshots incluídos, regra para contratos sem observação e se a métrica é fluxo ou estoque acumulado. Não some porcentagens mensais para obter incidência acumulada; conte contratos com evento acumulado e divida pelo denominador coerente.

A implementação descarta observações com MOB ausente ou negativo antes de validar as demais e forma `n_contratos_safra` a partir dos contratos que restaram. Portanto, compare esse denominador com a população de originação original para detectar exclusões; o retorno não recupera contratos que não possuem snapshot válido. Em cada célula safra × MOB, `n_contratos_observados` mede quantos aparecem naquele MOB e `cobertura_observada` divide por `n_contratos_safra`. Só quando a célula está completa o helper publica `taxa_acumulada`; caso contrário, ela é `NaN`, ou ausente, e não zero. Compare janeiro e fevereiro no mesmo MOB e com coberturas conhecidas. Uma safra recente sem MOB 6 não é uma safra com taxa zero no MOB 6. No [runner mensal](../../skills/hub-ml-analise-safra/scripts/README.md), o denominador vem do roster completo em MOB0 e permanece fixo; `IMMATURE`, `NO_OBSERVATIONS` e `INCOMPLETE` não autorizam taxa provisória sobre o subconjunto observado.

Para um teste estatístico, fixe a população e a **unidade independente** antes de escolher teste. Dois contatos do mesmo cliente podem compartilhar comportamento e não serem duas observações independentes. Declare H0, a hipótese nula de referência, e H1, a alternativa que quer investigar. Defina o **estimando**, isto é, a quantidade ou efeito que deseja conhecer na população, a diferença mínima que mudaria a decisão, período, grupos, desenho amostral e número de comparações planejadas. Escolha antes de olhar o resultado o **alfa**, nível de significância usado como regra de decisão estatística. O p-valor descreve quão incompatível seria uma estatística tão ou mais extrema com H0 sob o modelo e pressupostos do teste; não é a probabilidade de H0 ser verdadeira nem mede tamanho de efeito. Um p-valor alto não prova que grupos são equivalentes. Se pretende testar várias safras ou segmentos, planeje tratamento da multiplicidade. Se o teste consumir pandas/scipy, limite a coleta ao driver ou agregue no Spark primeiro, preservando pesos e estrutura de dependência quando necessários.

Antes de executar, confirme acesso à fonte, compute e pacote, tipos de colunas, data de corte e permissões de uso. O capítulo MU02 mostra como preparar imports. Não use um exemplo sintético da documentação como prova de que a sua fonte tem aqueles campos. Se falta a data de disponibilidade, o resultado pode servir a um retrato descritivo da história observada, mas não sustenta por si uma afirmação de ausência de vazamento numa previsão histórica.

Planeje a avaliação temporal da feature antes de treiná-la. Um conjunto de treino com decisões de meses posteriores misturado ao teste de meses anteriores pode fazer uma variável aparentemente útil parecer disponível quando não era. `temporal_split` trabalha em pandas com períodos completos de calendário e gaps explícitos; ele pode ainda remover entidades repetidas entre partições quando `group_col` é usado. Recuse ou renomeie a coluna auxiliar `__period`; chaves de grupo nulas não têm exclusividade garantida. Essa opção é adequada apenas se independência entre entidades for exigida pela pergunta; em séries por entidade, observar o passado da mesma entidade pode ser parte legítima do desenho. O helper não conserta uma feature calculada com dados futuros: primeiro construa a variável no instante de cada decisão, depois separe treino, validação e teste.

<a id="uso-hub-ml-analise-safra"></a>
##### Ficha de uso — hub-ml-analise-safra

<!-- usage-card:start hub-ml-analise-safra -->
Escolha análise de safra quando quer comparar grupos definidos pela entrada e acompanhar sua maturação. Informe unidade, identificador, data de origem, observação, evento, exposição, corte, snapshots e denominador. Declare se o evento é incremental ou acumulado e qual convenção de MOB será usada. MOB significa meses desde a origem; duas safras devem ser comparadas na mesma idade observada, com maturidade e cobertura conhecidas.

O pedido abaixo prepara o contrato antes de calcular curvas. A entrega esperada é notebook ou relatório com qualidade, definições, matriz safra por MOB, curvas, volumes, cobertura, limitações e ações investigativas. Confira o cadastro inicial contra os contratos que sobreviveram aos filtros; o helper não recupera contratos sem observação válida. Uma célula imatura ou incompleta deve continuar ausente quando o contrato assim exige. Não some taxas mensais nem substitua ausência por zero para completar o heatmap. Na policy vigente, a skill está em L0/audit; o perfil mensal integrado tem alcance específico e não executa toda análise de safra. Se quiser inferência sobre diferenças, encaminhe desenho e incerteza à skill estatística, preservando a pergunta original.

```text
@hub-ml-analise-safra
Planeje comparar [COORTES] na unidade [UNIDADE], com chave [CHAVE].
Origem, observação, evento, exposição e snapshots: [COLUNAS/DEFINIÇÕES].
Corte, denominador e convenção de MOB: [REGRAS OU LACUNAS].
Não execute nesta etapa. Proponha qualidade, matriz e curvas no mesmo MOB,
tratamento de maturidade/cobertura, limitações e próximos testes.
```
<!-- usage-card:end hub-ml-analise-safra -->

<a id="mu10-3"></a>
#### 3. Como executar cada rota sem pedir ao helper mais do que ele entrega?

Para uma fotografia RFV em corte comum, importe a fachada de `hub_scripts` e passe **nome de tabela**, não DataFrame. O trecho presume uma tabela autorizada em grão de compra; substitua os nomes pelo seu schema e verifique as colunas antes. A chamada devolve DataFrame Spark, cuja prévia limitada é uma ação separada:

```python
from hub_scripts.rfv_calculator import rfv_calculator

rfv = rfv_calculator(
    "catalogo.esquema.compras_exemplo",  # placeholder
    col_cliente="id_cliente", col_data="dt_compra", col_valor="valor",
    dt_referencia="2026-01-31", periodos=(30, 60, 90),
)
rfv.select("id_cliente", "ultima_data", "recencia",
           "frequencia_total", "valor_total", "frequencia_30d").limit(5).show()
```

Leia `ultima_data` e `recencia` junto de `frequencia_total` e `valor_total`. Suponha E001 com compras de 100 em 10/01 e 50 em 20/01 e corte inclusivo em 31/01: a frequência total é 2, valor total 150 e recência 11 dias; ambas entram na janela de 30 dias, que começa em 02/01. Uma compra em 01/02 não entra. Isso é uma conta ilustrativa, não a saída de um notebook executado aqui. Confira para uma entidade pequena as duas bordas da janela e compare manualmente com o retorno. Se `valor` inclui estorno de -20, ele reduz a soma; o helper não decide se estorno deve contar como compra.

Se RFV será feature de um modelo, transforme o cálculo em spec e teste sua disponibilidade por decisão. A skill `hub-ml-feature-engineering` pede definição, chave, janela, event time, momento real de disponibilidade, tratamento de missing, dono e testes de paridade treino–uso. Use o helper somente quando seu corte comum e grão correspondem a essa spec. Para datas por linha, use construção point-in-time; para janelas por entidade, confirme partição e corte em cada decisão. **Imputação** preenche valores ausentes segundo regra declarada; **binning** divide valores em faixas; **encoding** representa categorias em formato consumível pelo modelo. Quando seus parâmetros são aprendidos dos dados — por exemplo mediana de preenchimento, limites das faixas ou vocabulário de categorias — ajuste-os somente no treino e aplique a mesma regra à validação e ao teste. O fato de uma coluna ter nome `freq_30d` não prova que respeita os 30 dias disponíveis no passado de cada linha.

As [rotas atuais de features](../../skills/hub-ml-feature-engineering/scripts/README.md) separam `FIXED_LAG_L1_V1`, lag da observação anterior elegível por entidade, de `COMPOSED_PIT_FEATURE_VIEW_V1`, projeção em memória após verificar PIT upstream. Materialização exige request de efeito, autorização vinculada, destino pessoal, readback, replay e cleanup; `UNKNOWN` pede inspeção, sem retry automático. Nenhuma delas faz fit ou aprova a feature.

Para safra, prepare uma **tabela pandas pequena e deliberadamente limitada** com contrato, originação, observação e evento binário. `build_vintage_table` não recebe DataFrame Spark; não converta tabela inteira com `toPandas()` sem estimar volume e restringir população. O exemplo cria quatro observações sintéticas de dois contratos; cada contrato aparece em MOB 0 e 1, e apenas C1 registra evento no MOB 1:

```python
import pandas as pd
from hub_snippets.ml.vintage_analysis import build_vintage_table, compare_safras

amostra = pd.DataFrame({
    "id_contrato": ["C1", "C1", "C2", "C2"],
    "dt_orig": ["2026-01-05"] * 4,
    "dt_ref": ["2026-01-31", "2026-02-28", "2026-01-31", "2026-02-28"],
    "evento": [0, 1, 0, 0],
})
vintage = build_vintage_table(
    amostra, contract_id="id_contrato", dt_originacao="dt_orig",
    dt_referencia="dt_ref", target="evento", safra_grain="month",
)
print(vintage[["safra", "mob", "n_contratos_observados",
               "n_contratos_safra", "cobertura_observada", "taxa_acumulada"]])
```

Pelo contrato da função, janeiro tem dois contratos após filtro. MOB 0 está completo e tem taxa 0/2; MOB 1 está completo e tem 1/2, ou 50%. Se a linha de C2 em fevereiro faltar, a célula MOB 1 teria cobertura 1/2 e `taxa_acumulada=NaN`, mesmo que C1 tenha evento. Não conclua taxa de 100%. `compare_safras(vintage, mob_checkpoints=[1, 3])` pode organizar comparação por MOB quando houver mais safras; checkpoints não observados ficam ausentes. Curva ou heatmap ajudam a ver maturação, mas figuras não preenchem células imaturas. Se usar tema visual resolvido, as rotas `*_resolvido` alteram aparência sem mudar denominador ou taxa.

Quando a pergunta é inferencial, preencha um cartão antes de rodar teste: “H0: diferença de taxa no MOB 3 entre safras comparáveis é zero; H1: difere; unidade contrato; efeito mínimo relevante 3 pontos percentuais; grupos e tamanho; independência a conferir; teste e intervalo a escolher conforme desenho; família de comparações declarada”. Não escolha teste ou alfa olhando a primeira saída. A skill de validação estatística recomenda reportar estimativa, intervalo, tamanho de efeito, pressupostos e consequência operacional. Se a coorte ainda não atingiu MOB 3, não há observação para esse teste; esperar maturidade ou mudar a pergunta é mais honesto que atribuir zero.

Essas rotas podem se encadear, mas não se substituem. `rfv_calculator` retorna DataFrame Spark de medidas brutas; `build_vintage_table` retorna pandas de safra × MOB; uma skill orienta o processo e a revisão. Não trate um trecho de código exibido como execução certificada nem persista resultado sem decidir destino, contrato e permissões. Se uma fonte falha por coluna ausente, confira schema; se o MOB é inválido, investigue origem/referência; se a amostra estatística não representa a população, revise desenho antes de interpretar p-valor.

Para outras perguntas, escolha o helper pelo fenômeno. [`calculate_woe_iv`](../../hub_snippets/ml/woe_iv_calculator/README.md) pode avaliar separação de categorias ou faixas já definidas diante de um alvo binário, mas seu valor não aprova automaticamente uma feature, e as faixas precisam ser aprendidas somente no treino. [`kaplan_meier`](../../hub_snippets/ml/kaplan_meier/README.md) e [`survival_cox`](../../hub_snippets/ml/survival_cox/README.md) tratam tempo até evento com censura; são caminhos quando contratos têm acompanhamentos de durações diferentes e “ainda não ocorreu” não significa “nunca ocorrerá”. Eles não substituem uma safra descritiva apenas por parecerem mais estatísticos. `score_bands` e `scorecard_builder` pertencem à etapa de pontuação de um modelo, não ao cálculo inicial de RFV. Consulte [MT08](MT-parte-ii.md#mt08) para APIs de ML, [MT17](MT-parte-iv.md#mt17) para contratos de skills e [MT20](MT-parte-v.md#mt20) para a fronteira com micromodelos; leia as páginas de cada objeto antes de incorporá-lo e declare qual pergunta motivou a escolha.

Se o estudo exigir comparação formal de safras, não aplique um teste de proporções diretamente às células da tabela sem conferir independência, censura, tamanho e seleção. Uma taxa de 50% obtida de dois contratos é aritmeticamente correta e extremamente incerta; uma diferença de dois pontos percentuais entre milhares de contratos pode ser precisa e ainda irrelevante para a decisão. Peça à skill estatística uma proposta de estimando e intervalo compatível com o desenho e depois confronte o efeito observado com o mínimo relevante definido antes. Relate qualquer célula `NaN` como falta de observação completa, não como dado negativo para o teste.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu10-h-fontes-desta-parte"></a>
##### Fontes desta parte

`ambiente_fonte/.assistant/hub_scripts/rfv_calculator/{rfv_calculator.py,README.md}`; `ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/{vintage_analysis.py,README.md}`; `ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/SKILL.md`; `ambiente_fonte/.assistant/skills/hub-ml-analise-safra/{SKILL.md,scripts/README.md}`; `ambiente_fonte/.assistant/skills/hub-ml-validacao-estatistica/SKILL.md`; policy de skill enforcement. Exemplos são ILLUSTRATIVE, sem execução de Spark/pandas neste capítulo.
<!-- editorial:exclude:end -->

<a id="uso-hub-ml-validacao-estatistica"></a>
##### Ficha de uso — hub-ml-validacao-estatistica

<!-- usage-card:start hub-ml-validacao-estatistica -->
Escolha validação estatística quando a decisão exige estimativa com incerteza ou avaliação de pressupostos. Informe pergunta, população, unidade independente, grupos, período, desenho amostral, variáveis, estimando, efeito mínimo relevante e comparações planejadas. Estimando é o efeito ou quantidade que deseja conhecer. Diferencie diagnóstico exploratório de inferência; várias linhas do mesmo cliente podem exigir tratamento de dependência, não um teste de grupos independentes.

O pedido abaixo solicita plano antes de observar o resultado. A entrega esperada descreve hipóteses, método, pressupostos, amostra, limites de coleta, multiplicidade, estimativas e critérios de decisão; resultados entram somente após execução real. Confira se o método responde ao estimando, se preserva pesos ou pareamento necessários e se informa tamanho de efeito, unidade e intervalo. Um p-valor pequeno não mede relevância prática; um p-valor alto não prova equivalência. A policy atual está em L0/audit. O [perfil KS](../../skills/hub-ml-validacao-estatistica/scripts/README.md) aceita uma comparação sintética bicaudal, contínua, independente e sem empates; independência é declarada, não inferida. Exige alfa definido e oráculo externo ao payload. Não produz equivalência nem causalidade. O intervalo retorna `confidence_interval=None` e `confidence_interval_status="UNSUPPORTED_IN_PROFILE"`, sem números inventados. Se dados ou pressupostos faltarem, peça método compatível ou coleta adicional. Registre a lacuna e a consequência antes de recomendar retirada de variável ou retreino.

```text
@hub-ml-validacao-estatistica
Planeje avaliar [PERGUNTA/DECISÃO] em [POPULAÇÃO/PERÍODO].
Unidade, grupos, desenho e variáveis: [CONTEXTO].
Estimando, efeito mínimo, hipóteses e comparações: [DEFINIÇÕES/LACUNAS].
Não execute nem ajuste a decisão a resultados nesta etapa.
Proponha método, pressupostos, limites de coleta, intervalos,
multiplicidade, critério de decisão e próximos passos.
```
<!-- usage-card:end hub-ml-validacao-estatistica -->

<a id="mu10-4"></a>
#### 4. Como interpretar denominadores, efeito e incerteza para decidir o próximo passo?

Ao receber qualquer resultado, recupere a pergunta e os limites escritos antes da execução. Para RFV, registre o nome da tabela, o grão, a data de corte, os períodos e a quantidade de entidades com ao menos um evento válido. No exemplo sintético, `frequencia_total=2` de E001 significa duas linhas de compra até 31/01; se a origem estiver em grão de item, a leitura muda. `recencia=11` significa onze dias entre 20/01 e o corte, não onze dias desde a publicação do dado. `valor_total=150` soma os valores presentes segundo a semântica Spark; não assegura moeda uniforme, valor líquido ou ausência de estorno. Se você vai chamar essas medidas de features, confirme ainda a disponibilidade real em cada decisão histórica e a paridade do cálculo no momento de uso.

Para safra, leia sempre volume e cobertura antes da taxa. Na demonstração de dois contratos, MOB 1 completo permite descrever incidência acumulada de 1/2, ou 50%, naquela coorte. A célula com só um contrato observado teria `cobertura_observada=0,5` e taxa ausente: não é 0%, 50% nem 100% para a safra inteira. O denominador `n_contratos_safra` decorre das observações que sobreviveram ao filtro de MOB válido; reconcilie-o com o cadastro de originados quando a decisão depender de cobertura integral. Uma curva pode tornar a comparação legível, mas não adiciona contratos nem maturidade. No [briefing de safra](../../hub_prompts/safra/exemplo_safra.py), a frase sobre 202503 ter menos MOB não corresponde ao preparo: `fixtures.safras(..., mob_maximo=12)` gera MOB1–12 para todas as safras. Confira o máximo observado por safra; sem corte adicional, essa fixture não demonstra imaturidade diferenciada. Compare coortes no mesmo MOB, com calendário, mix de entrada e tamanho da população visíveis.

O relatório de uma feature precisa ir além do valor calculado. Use um cartão de aceite com nome, fórmula, origem, chave, instante de decisão, janela, atraso de publicação, regra de ausentes, tipo, testes e dono. Marque **aprovada** apenas quando as checagens exigidas pelo projeto passarem; **experimental** se há evidência parcial; **bloqueada** se tempo, fonte ou semântica impedem uso. Uma feature com distribuição estável pode continuar vazando informação futura; uma feature com nulos pode ser válida se a ausência tem sentido de negócio e tratamento definido. Registre o teste que permitiu ou impediu a decisão, não apenas uma cor de scorecard.

Para validação estatística, apresente estimativa com unidade e intervalo de confiança, tamanho e composição dos grupos, pressupostos, correção de múltiplas comparações quando cabível e consequência prática. “Diferença estimada de três pontos percentuais” é uma magnitude; o intervalo mostra a faixa de valores compatíveis com o método e dados sob seus pressupostos. Um p-valor pequeno não é a probabilidade de a hipótese nula ser verdadeira e não mede relevância para a operação. Um p-valor não pequeno também não comprova igualdade: pode refletir amostra insuficiente, variabilidade ou desenho inadequado. Se houver várias linhas por cliente, trate a dependência no plano antes de contar cada linha como observação independente.

Reaja à falha de acordo com a causa. RFV sem clientes esperados pede conferir data de corte, conversão de datas e eventos removidos, não preencher uma população fictícia de zeros. `build_vintage_table` pode rejeitar target não binário, MOB inválido ou target cumulativo que diminui; revise a definição na fonte e só então recalcule. Uma taxa ausente por cobertura incompleta pede investigar snapshots e maturidade, não forçar zero. Se uma premissa estatística falhar, peça método compatível, análise de sensibilidade ou coleta adicional e registre o risco residual. Em todos os casos, preserve os parâmetros e a versão da fonte para comparar o antes e o depois da correção.

Entregue ao próximo responsável uma ficha única com objetivo, população, unidade, fonte/snapshot, corte, definições de variáveis e evento, resultados com denominadores, limitações e questão aberta. Para RFV que seguirá à modelagem, encaminhe a spec à feature engineering; para safra com diferença aparente, encaminhe um plano de teste apenas se a decisão exige inferência; para fontes ainda incompatíveis, volte ao diagnóstico de MU09. O destinatário deve saber exatamente o que foi medido e qual decisão ainda depende de confirmação, sem confundir código de exemplo, cálculo feito no seu ambiente e aprovação de uso.

<!-- editorial:exclude:start -->
<a id="mu-mod-mu10-h-fontes-desta-parte-1"></a>
##### Fontes desta parte

`ambiente_fonte/.assistant/hub_scripts/rfv_calculator/{rfv_calculator.py,README.md}`; `ambiente_fonte/.assistant/hub_snippets/ml/vintage_analysis/{vintage_analysis.py,README.md}`; `ambiente_fonte/.assistant/skills/hub-ml-feature-engineering/SKILL.md`; `ambiente_fonte/.assistant/skills/hub-ml-validacao-estatistica/SKILL.md`; `ambiente_fonte/.assistant/skills/hub-ml-analise-safra/SKILL.md`. Valores são ILLUSTRATIVE; nenhuma análise real foi executada para o manual.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU09](#mu09) · [Próximo: MU11](#mu11) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT08](MT-parte-ii.md#mt08)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu11"></a>
<a id="mu11"></a>
### MU11 — Construir e revisar um baseline de ML

<!-- editorial:exclude:start -->
**Você quer:** construir uma primeira referência de modelo que outra pessoa consiga comparar e revisar. **Rota:** defina a pergunta e o baseline trivial (1), prepare dados e escolha a família (2), use skill e helpers com entradas verificáveis (3); a parte final interpreta medidas, run e próximos passos (4). Os exemplos são sintéticos e ilustrativos: nenhum treinamento ou acesso remoto foi realizado para este texto. [Índice do manual](MU-indice.md#sumario-mu).
<!-- editorial:exclude:end -->

<a id="mu11-1"></a>
#### 1. Que decisão o primeiro modelo deve ajudar a comparar?

Comece com uma frase que alguém de fora do projeto consiga contestar: “na data de contato, ordenar entidades pela chance de resposta nos próximos 30 dias, para escolher quais serão revisadas”. Essa frase fixa a **unidade** da previsão (uma decisão de contato), o **alvo** (resposta dentro de 30 dias), o **instante** em que a pontuação seria usada e o **horizonte** em que a resposta amadurece. O primeiro modelo é um **baseline**, uma régua inicial de comparação. Ele não precisa ser o mais complexo; precisa revelar se adicionar modelagem supera uma alternativa simples com dados e período equivalentes.

Escreva a população antes de abrir um notebook de treino. No exemplo fictício, são decisões para entidades `E001` a `E100`, elegíveis em janeiro a junho. Liste quem ficou fora: decisões duplicadas, resposta ainda imatura, falta de chave ou ausência de atributos indispensáveis. Conte linhas e entidades separadamente, porque uma entidade pode ter mais de uma decisão. Registre também quantos `y=1` há por mês. Se todas as decisões de junho ainda estão dentro dos 30 dias de espera, elas não são negativos prontos para avaliação. O [guia de preparação](#mu08-1) ajuda a conferir grão e cobertura, e [MU09](#mu09-3) trata disponibilidade temporal em junções.

Escolha um baseline trivial coerente. Para classificação binária, pode ser uma pontuação constante igual à taxa de evento do treino ou uma regra já usada, como ordenar pela recência de interação disponível na data da decisão. A regra deve ser calculada só com informação que um operador teria naquele dia. Se a taxa do treino é 20%, prever `0.20` para todos pode servir como referência de erro probabilístico, mas não discrimina positivos de negativos. Se há uma regra de triagem antiga, compare-a na mesma população e no mesmo período, sem aproveitar um corte mais favorável para o novo modelo.

Defina antes da escolha a **métrica principal** e as restrições. AUC mede ordenação de positivos acima de negativos; precisão num volume de revisão fixo pode ser mais próxima da operação; Brier e calibração importam se o score será interpretado como probabilidade. Uma equipe que só pode investigar dez casos por semana precisa olhar os dez maiores scores e os falsos alarmes, não apenas AUC. Registre custo aproximado de perder uma resposta e de investigar um caso inútil. Nenhum threshold de template vira regra de negócio apenas por constar no Hub. Se a resposta é uma quantidade contínua, mude para MAE/RMSE; se é ordem de ofertas por entidade, NDCG dentro de grupos, e assim por diante. A família vem depois da pergunta.

Antes de treinar, abra um quadro de experimento com: identificador da base e data de corte, definição de `y`, lista de exclusões, instante de disponibilidade de cada feature, período de treino/validação/teste, baseline trivial, métrica primária e guardrails, owner da revisão e orçamento de compute. Se algum item está desconhecido, resolva ou marque como lacuna explícita. O propósito desse quadro é impedir que a função de treino produza um número aparentemente preciso para uma pergunta diferente da desejada. O [contrato técnico de treino](MT-parte-ii.md#mt09-1) detalha por que os wrappers não corrigem esse desenho.

Escreva também o que será feito se o baseline não melhorar a regra trivial. Pode ser sinal de que os atributos ainda não estavam disponíveis no momento certo, de que a definição do alvo não condiz com a decisão ou de que a regra antiga já captura boa parte do sinal. A resposta não é obrigatoriamente testar um modelo mais complexo. Para revisão, entregue um exemplo de linha com data de decisão, atributos permitidos e data em que o alvo ficou observável, removendo qualquer informação sensível. Esse exemplo dá ao leitor um teste concreto da definição, anterior a qualquer métrica.

<a id="mu11-2"></a>
#### 2. Como preparar a base e escolher uma família compatível?

Para uma decisão tomada em janeiro, use somente atributos disponíveis até essa data. Uma coluna `interacoes_ate_decisao` pode contar contatos anteriores; uma coluna `resposta_30d` só serve como alvo depois da maturação, nunca como feature. A tabela deve ter grão estável: se a entidade tem três ofertas no mesmo dia, decida se cada oferta é uma linha ou se haverá uma linha única da decisão. Conferir joins por chave e instante evita que uma linha de resultado posterior amplie o conjunto de features. [MU09](#mu09-2) traz a conferência de cobertura e expansão da junção; [MU10](#mu10-2) ajuda a especificar a feature e seu instante de validade.

Separe treino, validação e teste antes de transformar dados. Se o uso será no futuro, uma sequência ilustrativa é treino em janeiro–março, validação em abril e teste em maio, desde que todos os alvos estejam maduros. Se a janela de resposta atravessa a fronteira, inclua um gap temporal real ou redesenhe cortes. Se a mesma entidade aparece nos três conjuntos, decida se isso representa o uso real; quando a pergunta exige entidades inéditas, agrupe a partição para impedir cruzamento. Use `split_temporal` ou `walk_forward_cv` segundo o desenho descrito em [MU10](#mu10-2) e [MT08](MT-parte-ii.md#mt08-2), mas confira seus retornos e descartes. Não chame um split aleatório de validação futura.

Ajuste imputação de ausentes, padronização, binning, codificação de categorias e seleção de atributos **apenas no treino**. Imputação preenche ausentes segundo uma regra aprendida; binning transforma valores em faixas; encoding representa categorias numericamente. Depois aplique as mesmas regras congeladas à validação e ao teste. Se a média de uma coluna foi calculada com as linhas de maio antes da divisão, informação do teste entrou na preparação, mesmo sem copiar `y`. Se uma categoria nova aparece no teste, registre a política de desconhecidos; não refaça o vocabulário usando o teste. Preserve lista e ordem das colunas, além dos transformadores, para a inferência posterior.

O mapa de suites da skill `hub-ml-baseline-ml` organiza a escolha. **B1 tabular** compara regra trivial com modelo linear/árvore simples e, se fizer sentido, LightGBM, XGBoost ou CatBoost para classificação/regressão. **B1 scorecard** privilegia regressão logística e pontos transparentes; WOE pode ser diagnóstico, não aprovação. **B2 temporal** começa com previsão ingênua ou sazonal ingênua e compara ARIMA/Prophet com backtest. **B3 deep learning** testa TabNet ou MLP só com hipótese e orçamento que justifiquem seu custo diante de B1. **B4 clustering** procura grupos sem `y`, verifica estabilidade e perfil; **B5 ranking** ordena alternativas dentro de grupos com regra simples e ranker; **B6 survival** modela tempo até evento com censura; **B7 anomalia** prioriza casos sem rótulo confiável. Escolha uma suite explicitamente e anote por que as outras não respondem à pergunta atual.

Uma tabela rápida evita trocar ferramenta pela tarefa:

| Pergunta principal | Primeiro comparador | Objetos do Hub que podem entrar depois | Evidência exigida |
|---|---|---|---|
| Evento 0/1 ou quantidade | Constante, regra ou linear | `train_lgbm`, `train_xgboost`, `train_catboost`, `optuna_lgbm` | Teste separado, métrica com unidade |
| Série no tempo | Último valor ou sazonal ingênuo | `arima_wrapper`, `prophet_wrapper`, `walk_forward` | Erro fora da amostra por horizonte |
| Ofertas por entidade | Regra de ordem | `lgbm_ranker` | Grupos contíguos e NDCG@k |
| Segmentos sem rótulo | Regra de grupos simples | `clustering_suite`, `cluster_profiling`, `umap_viz` | Estabilidade, perfil e utilidade |
| Casos incomuns | Regra robusta de revisão | `isolation_forest`, `autoencoder_anomaly` | Fila investigada, sem chamar alerta de fraude |

O quadro é um roteiro de seleção, não uma afirmação de que todos os objetos executam no mesmo ambiente. Os wrappers de ML citados em [MT09](MT-parte-ii.md#mt09-2) usam dados locais pandas/NumPy ou PyTorch; se os dados brutos estão em Spark, faça filtros e agregações distribuídas e **estime o tamanho** antes de converter a amostra ao driver. Uma contagem enorme convertida diretamente com `toPandas()` pode esgotar memória. Registre critério da amostra e seed. Verifique no compute as bibliotecas necessárias: LightGBM/XGBoost/CatBoost, scikit-learn, MLflow quando o logging estiver ativo, ou PyTorch/Prophet conforme a suite. Ler o README não instala pacotes, mas vários notebooks de exemplo contêm células `%pip` e reinício de Python. Examine esses efeitos antes de executar; o exemplo não autoriza instalação nem destino remoto.

Uma forma prática de conferir o corte é montar uma tabela pequena por período com colunas `n_decisoes`, `n_entidades`, `n_eventos_maduros` e `n_sem_alvo_maduro`. Se abril tem 200 decisões, mas somente 120 com janela de resposta fechada, a validação não deve tratar as 80 restantes como negativos. Se maio contém metade das entidades já vistas no treino, anote se o caso de uso prevê as mesmas entidades ou entidades inéditas. Se uma regra de exclusão elimina quase todos os casos de um canal, a métrica estimará o desempenho na população restante; não extrapole silenciosamente para o canal ausente. Esses números também orientam se há eventos suficientes em cada parte para AUC ou se será necessário outro desenho.

Para features, registre uma ficha simples por coluna: nome, fonte, grão original, instante de observação, instante de publicação, janela de cálculo, tratamento de ausentes e transformação aplicada. `interacoes_ate_decisao` pode usar eventos anteriores, mas uma carga noturna publicada depois da decisão talvez só esteja disponível no dia seguinte. Valide pelo relógio de publicação, não apenas pela data do evento. Faça uma amostra de linhas na fronteira do corte e tente explicar manualmente por que cada valor era conhecido naquele instante. Se a explicação depende do resultado futuro, a coluna não entra. O mesmo controle vale para estatísticas globais, como frequência de categoria, aprendidas apenas no treino.

Quando os dados cabem no driver, `X_train` e `X_val` podem ser matrizes NumPy ou DataFrames pandas conforme o wrapper; preserve índices/IDs num objeto paralelo para auditar a correspondência com `y`. Converter não significa descartar a origem: guarde versão da consulta, filtros e semente da amostra. Para modelos de árvores, categorias e valores ausentes têm tratamentos distintos nas bibliotecas; a existência de um parâmetro `cat_features` no CatBoost não significa que a mesma matriz textual funcionará no LightGBM ou no XGBoost. Se planeja compará-los, defina uma representação consistente ou documente explicitamente as diferenças de pré-processamento para que a comparação não misture algoritmo e entrada.

<a id="uso-hub-ml-baseline-ml"></a>
##### Ficha de uso — hub-ml-baseline-ml

<!-- usage-card:start hub-ml-baseline-ml -->
Escolha baseline quando precisa de uma referência reproduzível para comparar modelos ou uma regra existente. Informe decisão, unidade, alvo, horizonte, população, exclusões, instante de disponibilidade, períodos de treino, validação e teste, métrica principal, restrições e orçamento. Escolha a suite pelo problema: classificação, série, ranking e agrupamento exigem desenhos distintos. Se os rótulos ainda não amadureceram, registre a lacuna antes de chamar o conjunto de teste válido.

O pedido abaixo solicita um plano antes do treino. A entrega esperada reúne comparador trivial, preparação, splits, dependências, treinamento proposto, critérios, tracking e handoff. Depois da execução autorizada, acrescente modelo, métricas realmente calculadas, população avaliada e limitações. Confira que transformações foram ajustadas só no treino, IDs e alvos permaneceram alinhados e o teste não participou da seleção. Exija comparação nas mesmas linhas e unidade adequada para cada métrica. A skill está em L0/audit na policy vigente; templates não treinam nem promovem modelos. Se um wrapper registrar apenas parâmetros e métricas, complete o registro conforme o contrato do projeto. Tracking não autoriza promoção nem alteração de alias.

```text
@hub-ml-baseline-ml
Planeje um baseline [SUITE] para [DECISÃO/UNIDADE/ALVO/HORIZONTE].
População, disponibilidade e splits: [DEFINIÇÕES OU LACUNAS].
Régua trivial, métrica, restrições e orçamento: [CONTEXTO].
Não treine nem registre nesta etapa. Entregue preparação, comparação,
dependências, critérios de revisão e plano de tracking.
Separe proposta, execução autorizada e promoção.
```
<!-- usage-card:end hub-ml-baseline-ml -->

<a id="mu11-3"></a>
#### 3. Como pedir a skill e chamar um helper sem perder o controle do treino?

Se você quer assistência na escolha, invoque `hub-ml-baseline-ml` com um briefing concreto: “Construa um baseline B1 binário para resposta em 30 dias, uma linha por decisão de contato, treino janeiro–março, validação abril e teste maio após maturação; compare regra de recência com modelo simples, métrica principal AUC e precisão no top dez; liste exclusões, features disponíveis, dependências, custos e limites antes de executar”. Esse texto orienta a skill, mas não substitui acesso à tabela, compute, permissão para registrar runs ou revisão humana. A skill contém `suite_selection_guide.md`, `split_strategy.md`, templates de métricas e `mlflow_checklist.md` para organizar a saída. Preencha cada campo com sua fonte real; valores exemplificativos dos templates não são thresholds institucionais.

A [rota integrada da skill](../../skills/hub-ml-baseline-ml/scripts/README.md) oferece `BINARY_TEMPORAL_LOCAL_V1`: fixture sintética com pelo menos 12 meses, partições 50/25/25, gap zero, feature numérica única e regressão logística ajustada no treino. `run.py` calcula em memória, sem MLflow; `verify.py::verify` refaz partições, fit e métricas a partir de request/run_id externos. O perfil não executa todas as suites B1–B7 nem promove a policy L0/audit. A receita LightGBM abaixo é outra chamada direta, não esse runner.

Para usar só um snippet, importe a função do módulo correspondente de `hub_snippets.ml` em um ambiente Python onde o pacote e as dependências estejam acessíveis. Uma chamada ilustrativa válida tem a forma `model, metrics = train_lightgbm_baseline(X_train, y_train, X_val, y_val, task='binary', log_mlflow=False)`. `X_train` e `X_val` devem ter as mesmas colunas na mesma ordem, e cada vetor `y` deve corresponder às linhas da matriz do mesmo nome. `log_mlflow=False` evita somente o registro explícito do wrapper, sem desligar autologging já configurado na sessão; não transforma o retorno em um run governado. A função devolve modelo ajustado e dicionário de métricas de treino/validação; leia as chaves efetivas para a tarefa escolhida. Ela não divide seus dados nem cria um teste final.

Para tornar a rota concreta, o exemplo sintético abaixo cria 20 decisões ordenadas `D00` a `D19`, com duas features numéricas disponíveis no instante da decisão e rótulos já maduros. As primeiras 12 linhas são treino, quatro seguintes validação e as últimas quatro ficam reservadas como teste. A taxa de evento do treino é `6/12=0,5`; uma régua trivial prevê esse mesmo valor para toda a validação. Como a validação contém dois positivos e dois negativos, o Brier da régua é `0,25`: cada uma das quatro diferenças quadráticas vale `0,25`. O candidato é treinado apenas com as primeiras 12 linhas e comparado nas mesmas quatro de validação. O código é uma receita para um ambiente preparado, não um relato de execução.

```python
import numpy as np
from hub_snippets.ml.train_lgbm import train_lightgbm_baseline
from hub_snippets.ml.metrics_report import calculate_binary_metrics

ids = [f"D{i:02d}" for i in range(20)]
X = np.column_stack([np.arange(20) + 30, np.arange(20) % 3]).astype(float)
y = np.arange(20) % 2
X_train, y_train = X[:12], y[:12]
X_val, y_val = X[12:16], y[12:16]
X_test, y_test = X[16:], y[16:]  # reservado; não entra na escolha

baseline_prob = np.full(len(y_val), y_train.mean())
baseline = calculate_binary_metrics(y_val, baseline_prob)
model, treino = train_lightgbm_baseline(
    X_train, y_train, X_val, y_val,
    task="binary", early_stopping_rounds=0, log_mlflow=False,
)
prob_val = model.predict_proba(X_val)[:, 1]
candidato = calculate_binary_metrics(y_val, prob_val)
print(ids[12:16], baseline["brier_score"], candidato["brier_score"], treino["auc_val"])
```

Ao ler a saída, confira que `ids[12:16]` nomeia exatamente as quatro linhas avaliadas. `baseline["brier_score"]` deve representar o `0,25` calculado à mão; `candidato["brier_score"]` e `treino["auc_val"]` dependem do ajuste real e não recebem valores inventados aqui. `early_stopping_rounds=0` desativa a parada antecipada nesse conjunto minúsculo, mas não torna sua estimativa estável. Para trabalho real, use volume e período adequados, guarde transformadores e só abra `X_test` depois de selecionar a configuração. Se faltar LightGBM ou os imports do Hub, resolva a dependência e o caminho do pacote antes de usar a receita.

Em um exemplo de quatro decisões de validação com rótulos `[1,0,1,0]`, qualquer AUC numérica dependerá dos scores que o modelo realmente produzir. O retorno `metrics['auc_val']`, se existir nessa tarefa, deve ser interpretado como ordenação **nessas quatro linhas**, não como acurácia nem garantia futura. Não invente um valor de AUC no relatório antes de rodar e verificar a população. Uma chamada com `X_val` contendo uma coluna futura, ou com `y_val` reordenado sem reordenar `X_val`, pode gerar número enganoso mesmo que as dimensões coincidam. Corrija as matrizes, não a métrica. Se a validação contém só uma classe, a função ou o cálculo de AUC pode falhar; a ação é rever tamanho, maturação e corte da amostra, não preencher o resultado com zero.

Treine primeiro a régua trivial e o modelo simples sobre exatamente as mesmas linhas. Só depois compare um wrapper de boosting. Use `params_override` com escolhas registradas quando houver razão, não uma busca cega. `optimize_lgbm` usa a validação repetidamente e devolve `best_params` e `study`, não um modelo final; reserve o teste para depois da seleção. Quando for série, `train_arima` e `train_prophet` devolvem forecast e métricas **in-sample**, portanto organize backtest antes de reportar “melhor previsão”. Quando for ranking, `groups_train` contém tamanhos de blocos contíguos; seis ofertas de dois clientes com três cada pedem `[3,3]`, não seis identificadores. A leitura técnica de cada retorno está em [MT09](MT-parte-ii.md#mt09-2).

Para clustering/anomalia, substitua a ideia de “acerto” por verificação apropriada. `run_clustering_pipeline` devolve labels, modelo, scaler e métricas internas; `profile_clusters` ajuda a ver diferenças descritivas. `train_isolation_forest` devolve scores e labels para priorização; `train_autoencoder_anomaly` usa uma referência declarada normal e devolve limiar e erros de reconstrução. Nenhum dos dois confirma fraude. Para survival, use `kaplan_meier` e `survival_cox` apenas com duração, evento e censura definidos; para deep learning, compare TabNet/MLP com B1 no mesmo split e registre o custo. Essas alternativas estão no índice da categoria [ML](../../hub_snippets/ml/README.md), e seus limites técnicos aparecem em [MT08](MT-parte-ii.md#mt08-4) e [MT09](MT-parte-ii.md#mt09-3).

Antes de rodar, faça uma conferência final: counts por split, classes por split, datas máximas das features, ordem das colunas, transformação ajustada só no treino, memória estimada do driver, dependências disponíveis e destino de qualquer logging. Se um item falhar, documente a correção e refaça a preparação. Uma execução que termina sem erro prova apenas que o código aceitou aquela entrada; a comparação justa depende dessas condições externas. O próximo passo é interpretar os números junto com limitação e registro.

Se você optar por `log_mlflow=True`, confira antes se existe um run ativo adequado e quais parâmetros/métricas o wrapper registra. Alguns módulos apenas chamam `mlflow.log_params` e `mlflow.log_metrics`; isso não produz automaticamente dataset, split, assinatura e limitações. O helper `run_governado` pode exigir esses elementos para modelos compatíveis com o flavor sklearn, como detalhado em [MT10](MT-parte-ii.md#mt10-3), mas tem efeito persistente no backend. Para um ensaio local de API, `log_mlflow=False` isola o exemplo do registro opcional; confira também autologging da sessão; para trabalho real, combine um plano de tracking com o owner do experimento e não suponha que “treino concluído” significa run completo.

Um erro de dependência também tem tratamento específico. Se `lightgbm` não está disponível, confirme a biblioteca instalada no compute e a versão prevista pelo projeto; se MLflow falta com logging habilitado, desabilitar o registro só serve para um ensaio que não precisa dele, não para uma entrega cujo contrato exige rastreabilidade. Se o modelo recebe uma categoria fora do domínio codificado ou as matrizes têm colunas em ordens diferentes, corrija a preparação e rode a conferência novamente. Não recodifique categorias com base no teste para fazê-lo “passar”: isso muda a pergunta e pode contaminar a avaliação.

O notebook deve mostrar os nomes das funções chamadas e o estado de cada etapa: dados prontos, split conferido, baseline trivial medido, candidato treinado e avaliação pendente ou concluída. Se uma etapa foi apenas planejada, escreva “não executada” em vez de apresentar o formato de retorno como resultado observado. Esse cuidado permite a quem revisa distinguir uma receita reproduzível de uma evidência de desempenho, especialmente quando o trabalho foi dividido entre conversas ou sessões diferentes.

<!-- editorial:exclude:start -->
**Fontes:** [skill de baseline](../../skills/hub-ml-baseline-ml/SKILL.md), [guia de suites](../../skills/hub-ml-baseline-ml/templates/suite_selection_guide.md), [split](../../skills/hub-ml-baseline-ml/templates/split_strategy.md), [LightGBM](../../hub_snippets/ml/train_lgbm/train_lgbm.py), [Optuna](../../hub_snippets/ml/optuna_lgbm/optuna_lgbm.py) e [índice ML](../../hub_snippets/ml/README.md).
<!-- editorial:exclude:end -->

<a id="mu11-4"></a>
#### 4. Como ler métricas, registrar o run e decidir o próximo passo?

Compare primeiro na mesma tabela o baseline trivial, o modelo simples e o candidato mais complexo. Para cada linha, informe período, população, número de decisões e eventos, métrica principal, unidade, custo de treino e limitações. Em classificação, inclua AUC de ordenação, precisão e recall no limiar ou volume que a operação suporta, e medida de calibração quando o score for chamado de probabilidade. AUC de 0,80 não significa 80% de decisões corretas. Se o objetivo era revisar dez casos, mostre quantos eventos apareceram nos dez maiores scores e quantos falsos alertas exigiram trabalho. Para regressão, MAE mede erro absoluto médio na unidade do alvo e RMSE penaliza mais os erros grandes; para série, reporte erro **fora** da amostra por horizonte; para ranking, NDCG por grupo. O [capítulo de métricas](MT-parte-ii.md#mt10-1) explica os denominadores.

Leia o dicionário retornado antes de copiar números. `metrics_report.calculate_binary_metrics(y_true,y_prob,threshold=0.5)` devolve `auc_roc`, `ks_pct`, `gini`, `auc_pr`, `brier_score`, `precision`, `recall` e outras chaves para vetores com as duas classes; `ks_pct` é em pontos percentuais. `calculate_regression_metrics` devolve `rmse`, `mae`, `mape` e `r2`, mas MAPE fica indefinido quando todos os valores reais são zero. O wrapper `train_lightgbm_baseline` tem seu próprio dicionário de treino/validação, como `auc_val` em binária; não misture essas chaves com métricas de um teste separado sem nomear a população. Se a figura de KS e `ks_pct` divergirem, o código usa definições distintas, não somente escalas. Confira [MT10](MT-parte-ii.md#mt10-2) antes de copiar um threshold de uma saída para outra.

Um exemplo de leitura ilustrativo: baseline trivial com AUC 0,50 e candidato com AUC 0,74 em validação, mas precisão igual no top dez, não sustenta afirmar que o candidato melhora a rotina de dez investigações. AUC e precisão respondem a perguntas diferentes. Esses valores são hipotéticos; não foram produzidos pelo Hub. A conclusão provisória seria investigar distribuição de scores, custo de falsos alertas e estabilidade em outro período. Se o teste reservado mostra queda importante, volte às diferenças de população e ao desenho de features antes de ajustar mais parâmetros. Não use o teste repetidamente para escolher a próxima versão, pois ele passaria a funcionar como validação.

No registro, anote parâmetros, versão de código e dependências, identidade e recorte dos dados, split, métricas, limitações e artefatos seguros. A skill traz `mlflow_checklist.md`, `notebook_output_baseline.md` e `relatorio_executivo_baseline.md` para organizar a entrega. `run_governado` abre um contexto MLflow com tags de dataset, split e limitações; criação ou retomada do run depende da configuração vigente. O helper não isola backend nem solicita run aninhado, e cobra parâmetros, métricas e exemplo de entrada do modelo sklearn após a saída normal do bloco `with`. Se você usá-lo, confirme backend, experimento e run ativo antes de executar; chamadas podem gravar artefatos persistentemente, e uma falha de completude no fechamento não desfaz registros anteriores. Uma exceção dentro do corpo pula a checagem posterior de completude. Não grave dados pessoais em exemplos ou artifacts de tracking. O [ADR-0016](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0016-mlflow-runs-micromodelos.md) separa histórico operacional de definição, e um run completo não é aprovação para publicar modelo. Veja o [contrato de runs em MT10](MT-parte-ii.md#mt10-3).

O adapter `run_tracking.py` é uma rota separada: exige autorização `SER10-AUTH-1`, backend/identidade conferidos e destino pessoal novo. Cria experimento/run/modelo, verifica o modelo enquanto ativo e faz soft delete dos IDs próprios. `verify_finalized` confere a evidência e o estado deletado, sem reler o modelo após exclusão. `UNKNOWN_RESIDUE` exige inspeção, não retry automático; soft delete não é apagamento físico.

Escolha o próximo passo explicitamente. Se o candidato não supera a régua trivial no critério principal ou viola guardrail, documente-o e revise alvo, janela, features e representatividade; talvez a tarefa de modelagem precise ser reformulada. Se melhora, valide em teste intocado e por períodos ou segmentos relevantes, quantifique incerteza quando ela muda a decisão e prepare [explicabilidade e acompanhamento](#mu12-1). Se uma solução de deep learning custa muito mais sem ganho material, registre a comparação e prefira a opção mais simples. Para clustering e anomalias, a decisão seguinte costuma ser revisão de casos/estabilidade, não promoção de um classificador sem rótulos.

Entregue a outra pessoa um pacote mínimo conferível: pergunta de decisão; população e exclusões; datas de treino, validação e teste; inventário de features e disponibilidade; baseline trivial; funções e parâmetros usados; métricas com unidade e denominador; erros conhecidos; run ou plano de registro; e decisão proposta com quem deve revisá-la. Essa lista vale mesmo que a execução tenha falhado: registre a falha, sua causa conhecida e a alternativa tentada. A ausência de evidência é um resultado a comunicar, não um motivo para preencher métricas. Treinar um modelo cria um candidato técnico; publicação, promoção e uso institucional exigem outras verificações e autoridade.

<!-- editorial:exclude:start -->
**Fontes:** [skill baseline](../../skills/hub-ml-baseline-ml/SKILL.md), [template de métricas](../../skills/hub-ml-baseline-ml/templates/metricas_classificacao.md), [checklist MLflow](../../skills/hub-ml-baseline-ml/templates/mlflow_checklist.md), [saída de notebook](../../skills/hub-ml-baseline-ml/templates/notebook_output_baseline.md), [métricas](../../hub_snippets/ml/metrics_report/metrics_report.py), [run governado](../../hub_snippets/ml/mlflow_run/mlflow_run.py) e [ADR-0016](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0016-mlflow-runs-micromodelos.md). [Índice](MU-indice.md#sumario-mu).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU10](#mu10) · [Próximo: MU12](#mu12) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT09](MT-parte-ii.md#mt09) · [MT10](MT-parte-ii.md#mt10)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu12"></a>
<a id="mu12"></a>
### MU12 — Explicar resultados e acompanhar modelos

<!-- editorial:exclude:start -->
**Você quer:** entender uma predição, comunicar seus limites ou investigar mudança depois do treino. **Rota:** escolha a pergunta (1), fixe modelo, amostra e referência (2), chame apenas os helpers adequados (3); a última seção transforma sinais em uma ação revisada (4). Todos os números são ilustrativos; nenhuma execução de modelo, run ou monitor remoto foi realizada. [Índice do manual](MU-indice.md#sumario-mu).
<!-- editorial:exclude:end -->

<a id="mu12-1"></a>
#### 1. Preciso explicar uma predição ou acompanhar uma mudança?

“Por que `E001` recebeu esse score?” e “o modelo piorou em setembro?” são perguntas diferentes. A primeira pede **explicabilidade local**: qual saída do modelo está sendo decomposta, comparada com qual referência, para uma linha específica. “Quais atributos mais influenciam a carteira?” pede explicabilidade **global** numa população definida. “A distribuição de idade da conta mudou?” pede **drift de dados**, comparação entre referência e período atual. “A AUC (área sob a curva ROC (característica de operação do receptor), medida de discriminação entre classes) caiu?” pede **performance**, que só pode ser medida quando rótulos verdadeiros já amadureceram. Um relatório pode juntar as quatro, mas deve preservar seus denominadores e tempos.

Se você tem um modelo recém-treinado e quer compreender seus resultados, comece pelo conjunto de validação/teste, pelas métricas e por exemplos representativos de acerto, erro e fronteira. Use `hub-ml-explainability` para orientar método, classe, escala e camadas de comunicação. Se o modelo está em uso ou prestes a entrar e você quer acompanhar seu comportamento, use `hub-ml-monitoramento-modelo` para desenhar referência, frequência, atraso do alvo, política, owner e resposta. As skills são instruções e templates de trabalho, não um agendador nem um monitor implantado automaticamente. Um pedido claro menciona o objetivo e a evidência disponível: “explique a classe positiva do modelo versão V em decisões de maio” ou “compare o score de setembro com referência de junho e avalie performance só nas decisões cujo alvo de 30 dias fechou”.

Há uma sequência útil de perguntas. O score mudou porque a população de entrada mudou? O dado chegou com outra cobertura ou muitos ausentes? O próprio mapeamento entre score e evento mudou? Houve degradação em todos os segmentos ou só em um canal? Sem resposta observada, você pode relatar drift e qualidade de dados, mas não concluir que a AUC caiu. Com resposta observada, ainda verifique se foi medida na mesma definição de alvo e na mesma população. PSI (índice de estabilidade populacional para variável numérica), KS (estatística de Kolmogorov–Smirnov entre distribuições) e CSI (índice de estabilidade de categorias) comparam distribuições por mecanismos diferentes; veja a [leitura técnica](MT-parte-ii.md#mt10-4). Um alerta desses índices é sinal de investigação, não prova de dano ou ordem de retreino.

Para comunicar a alguém não técnico, comece com a decisão que o resultado afeta: quantos casos seriam revisados, qual é o custo dos erros e qual período foi observado. Depois apresente a medida e o limite. “Atributo X liderou a importância SHAP (SHapley Additive exPlanations, atribuições aditivas da saída prevista) na amostra de maio” é uma descrição da saída do modelo; “X causou o evento” não decorre dela. “A AUC caiu quatro centésimos” pode merecer investigação, mas não define sozinha a resposta. O [capítulo técnico](MT-parte-ii.md#mt10-1) separa discriminação, calibração, decisão e tracking; [MU11](#mu11-4) ensina a guardar um baseline antes de monitorar.

Escolha uma pergunta por painel ou parágrafo. Se o assunto é mudança de distribuição, mostre referência, período atual, volumes, missing e índice de estabilidade. Se é desempenho, mostre apenas a coorte com resultado conhecido, sua definição e métrica com unidade. Se é explicação, diga se ela é global ou local e qual versão do modelo gerou os scores. Esse enquadramento evita que um gráfico de SHAP seja lido como prova de melhora, ou que um alerta de entrada seja apresentado como queda de AUC. Uma mesma investigação pode chegar às três análises em sequência, mas cada conclusão deve apontar para sua própria evidência.

<a id="uso-hub-ml-explainability"></a>
##### Ficha de uso — hub-ml-explainability

<!-- usage-card:start hub-ml-explainability -->
Escolha explainability para compreender a saída de um modelo treinado, globalmente ou em casos identificados. Informe modelo e versão, população, período, preparação, classe, escala da saída, amostra, IDs e orçamento. Preserve a ordem entre linhas e identificadores; para Kernel, selecione externamente os casos quando precisar rastreá-los.

O pedido abaixo solicita método antes do cálculo. A entrega esperada reúne explicação técnica, gráficos, ranking, exemplos locais, tradução executiva, limites e próximos testes. Confira conjunto, classe, escala, background quando aplicável e correspondência de cada caso com o score explicado. SHAP atribui partes da saída do modelo; não demonstra causas do evento. Uma contribuição em log-odds não é uma porcentagem. A policy vigente mantém a skill em L0/audit: o texto não comprova execução nem publica gráficos. Confirme dependências e destino antes de autorizar cálculos ou salvamento. Se a classe ou a escala faltar, resolva essa informação antes de interpretar contribuições; mantenha o resultado condicionado enquanto isso.

```text
@hub-ml-explainability
Planeje explicar [MODELO/VERSÃO], conjunto [POPULAÇÃO/PERÍODO].
Classe, escala, preparação e IDs: [DEFINIÇÕES OU LACUNAS].
Amostra e orçamento: [LIMITES]. Não calcule nem salve nesta etapa.
Proponha método, controles de correspondência, entregas técnica e executiva,
limitações e próximos testes, sem atribuir causalidade ao SHAP.
```
<!-- usage-card:end hub-ml-explainability -->

<a id="mu12-2"></a>
#### 2. Que modelo, população, período e referência devo informar?

Anote versão do modelo e do pipeline de preparação, lista ordenada de colunas, alvo, classe positiva e **escala da saída**: probabilidade, margem, log-odds ou valor previsto. Log-odds é o logaritmo da razão entre chance de evento e de não evento; não se lê diretamente como porcentagem. Um SHAP de `+0.2` nessa escala não significa “20 pontos percentuais de risco”. Para uma decisão fictícia `E001` em 15/01, identifique o score produzido naquele dia e os atributos que o modelo recebeu. Se o notebook recalcular a linha com atributos atualizados em fevereiro, já estará explicando outra entrada.

Escolha a amostra que representa a pergunta. Para explicação global do desempenho de maio, use decisões de maio avaliáveis, com o mesmo pré-processamento da inferência e IDs guardados. Para explicação local, preserve a correspondência entre `idx` do array, identificador e data; uma ordenação intermediária pode levar o gráfico à pessoa errada. A função `compute_shap` limita opcionalmente o caminho `kernel` por subamostragem quando `len(X)>max_samples`, mas não devolve os IDs selecionados. Se você precisa ligar atribuições a casos, selecione externamente um conjunto pequeno, preserve seus IDs na mesma ordem e passe-o já dentro do limite. Isso também permite registrar semente e critério de amostragem.

A [rota executável da skill](../../skills/hub-ml-explainability/scripts/README.md), `LINEAR_REGRESSION_SYNTHETIC_V1`, exige regressão linear escalar sintética e uma linha de background explícita. Request, modelo, arrays e run_id externos alimentam o verificador com oráculo analítico. Não cobre árvores, classificação, KernelSHAP ou plots, nem promove L0/audit. No helper geral, `background=` só é aceito para `model_type="linear"`; omiti-lo preserva `X` como referência linear.

Defina a **referência** conforme a medida. Para SHAP, há um valor base associado ao explicador e, no caminho Kernel, um conjunto de background que influencia a comparação. Para PSI/CSI, a distribuição de referência determina bins ou categorias e não deve ser recalculada silenciosamente com o período atual. Para monitoramento de AUC, a referência é uma métrica de baseline para uma população e janela declaradas. Uma referência de treino com idade de conta distinta da carteira atual pode gerar alerta legítimo de mudança, mas não diz se a diferença é ruim. Escreva por que a referência é relevante e quando precisará ser atualizada por revisão, não por conveniência diante de um alerta.

Uma ficha mínima para cada comparação inclui: modelo/versão, origem dos dados, período de referência, período atual, número de linhas e entidades, porcentagem de ausentes, alvo e data de maturação, segmento, método e parâmetros, limiar adotado e responsável. A coluna “alvo maduro?” deve ficar explícita. No exemplo, respostas de decisões em 25/09 com janela de 30 dias ainda não podem medir performance em 01/10. Drift de score ou de atributos pode ser calculado sem rótulo, desde que as populações sejam comparáveis; performance precisa esperar ou usar somente a coorte madura, informando a cobertura reduzida.

Antes de abrir o explicador, verifique se o modelo faz predições coerentes no conjunto escolhido e se as colunas têm a mesma ordem de treino. Um erro de schema pode gerar atribuições com nomes trocados. Para dados sensíveis, evite publicar gráficos locais identificáveis e não envie exemplos pessoais a artifacts de tracking. Para comparação periódica, reserve a tabela de métricas em camada governada com versão, janela, população e timestamp; o `PerformanceMonitor` em si guarda histórico apenas na memória do processo. Um run MLflow pode registrar gráficos e agregados seguros, mas não deve virar depósito de resultados individuais por entidade.

Se o briefing estiver incompleto, ainda é possível produzir uma lista de perguntas pendentes: “qual classe?”, “qual período?”, “qual atraso do alvo?”, “qual população base?”. Não force uma explicação colorida para preencher essa ausência. A skill de explainability pede explicitamente classe/escala e amostra; a de monitoramento pede baseline, frequência, owner e runbook. Essa disciplina protege o leitor contra duas narrativas convincentes mas falsas: importância de atributo trocada por causalidade e drift de entrada trocado por queda de performance.

Em um acompanhamento mensal, compare o mesmo **grão** de decisão. Se junho contém uma linha por entidade e setembro uma linha por contato, a diferença de distribuição pode refletir duplicação do grão, não comportamento novo. Preserve um contador de chaves únicas e de linhas por período. Registre também versões de tratamento de ausentes e de categorias: a passagem de “sem informação” para um código numérico novo pode alterar PSI sem alterar a realidade subjacente. Uma referência útil não é apenas a fotografia de uma tabela; inclui as regras que geraram suas colunas. Quando essas regras mudam, abra uma investigação de compatibilidade antes de atribuir o sinal ao modelo.

Para um caso local, evite escolher apenas o erro mais dramático. Selecione, com critério declarado, exemplos de acerto, erro e score próximo ao limiar, e compare-os com a população. Um caso extremo pode explicar uma falha específica, mas não representa a carteira toda. Para um relatório global, informe quantas linhas foram explicadas e se houve amostragem estratificada por período ou segmento. A estatística de importância média pode esconder um atributo dominante em um grupo pequeno; uma tabela por segmento ajuda a perceber essa diferença sem sugerir causalidade.

<a id="uso-hub-ml-monitoramento-modelo"></a>
##### Ficha de uso — hub-ml-monitoramento-modelo

<!-- usage-card:start hub-ml-monitoramento-modelo -->
Escolha monitoramento quando precisa acompanhar um modelo em uso ou preparar sua observação operacional. Informe versão, população, frequência, referência, alvo, atraso dos rótulos, métricas, limites justificados, responsáveis, destino e resposta a alertas. Separe disponibilidade do serviço, qualidade dos dados, mudança de distribuição e desempenho: uma mudança de entrada pode ser medida sem alvo, mas performance exige resultados conhecidos.

O pedido abaixo planeja acompanhamento, sem criar job ou alerta. A entrega esperada reúne arquitetura, contrato de métricas, comparações, política, runbook, limitações e o que depende de revisão. Depois da execução, confira períodos, volumes, denominadores, maturidade dos rótulos e direção de cada métrica. Não trate PSI como prova de queda de desempenho nem aplique limiar universal. O PerformanceMonitor mantém histórico em memória; persistência governada precisa de desenho separado. A skill atual está em L0/audit, e o helper nunca autoriza retreino. Um estado sem evidência pede resolver referência ou cobertura, não inventar degradação. Só proponha recalibração, challenger ou promoção após investigação e gates correspondentes. Registre quem decide, qual teste falta e quando repetir a avaliação.

```text
@hub-ml-monitoramento-modelo
Planeje acompanhar [MODELO/VERSÃO] em [POPULAÇÃO/FREQUÊNCIA].
Referência, alvo, atraso de rótulos e métricas: [CONTEXTO].
Limites, responsáveis, destinos e resposta: [REGRAS OU LACUNAS].
Não crie jobs, alertas ou retreino nesta etapa.
Entregue contrato, verificações, runbook e limites de evidência;
separe drift, desempenho e decisão de ação.
```
<!-- usage-card:end hub-ml-monitoramento-modelo -->

<a id="mu12-3"></a>
#### 3. Que helper uso para SHAP, relatórios, curvas, drift e desempenho?

Para um modelo de árvore compatível já validado, uma chamada de forma pública é `values, base = compute_shap(model, X_eval, feature_names, model_type='tree', task='classification', output_index=1)` **se** a biblioteca devolver várias saídas e a saída 1 for a classe positiva confirmada. Em saída 2D única, `output_index` pode ser desnecessário; inspecione o contrato e a forma obtida, sem adivinhar. `values` deve ter uma linha por caso avaliado e uma coluna por atributo; `base` é a referência na escala explicada. `get_feature_importance_shap(values, feature_names, top_n=20)` produz tabela de média absoluta e participação relativa. Esse percentual é fração da importância absoluta média na amostra, não “porcentagem de causalidade” ou de acertos. `plot_shap_global` e `plot_shap_local` geram gráficos SHAP/Matplotlib e podem salvar arquivo com `save_path`; o tema Plotly do Hub não recolore automaticamente esses plots.

Uma receita para um modelo de árvore **já validado** exige que o notebook tenha `modelo_validado`, `X_casos_validos`, `ids_casos_validos`, `colunas_treino`, `classe_indice_confirmado` e `escala_saida_confirmada` vindos da mesma versão e ordem. Confirme que índice 1 representa a classe positiva; a escala do `TreeExplainer` padrão é a saída *raw* do modelo, que pode ser margem/log-odds, conforme a [documentação SHAP](https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html), reconferida em 7/10/2026. Configure `saida_autorizada` como diretório local aprovado antes de salvar gráficos; os helpers salvam e fecham figuras Matplotlib e não retornam `Figure`.

```python
from pathlib import Path
import numpy as np
from hub_snippets.ml.shap_explainer import (
    compute_shap, get_feature_importance_shap,
    plot_shap_global, plot_shap_local,
)

X_eval = np.asarray(X_casos_validos, dtype=float)
ids_eval = list(ids_casos_validos)
feature_names = list(colunas_treino)
assert X_eval.ndim == 2 and X_eval.shape[1] == len(feature_names)
assert len(ids_eval) == len(X_eval) and len(set(ids_eval)) == len(ids_eval)
assert classe_indice_confirmado == 1 and escala_saida_confirmada
saida = Path(saida_autorizada)
assert saida.is_dir()  # diretório aprovado antes desta receita
values, base = compute_shap(
    modelo_validado, X_eval, feature_names,
    model_type="tree", task="classification", output_index=1,
)
assert values.shape == X_eval.shape
ranking = get_feature_importance_shap(values, feature_names)
idx = ids_eval.index("E001")
plot_shap_global(values, X_eval, feature_names,
                 save_path=str(saida / "shap_global.png"))
plot_shap_local(values, base, X_eval, feature_names, idx,
                save_path=str(saida / "shap_E001.png"))
print(ranking.head(), base, ids_eval[idx])
```

O retorno contém matriz de atribuições, base e ranking; dois arquivos surgem no destino autorizado. Se o modelo não for compatível, a classe não estiver mapeada ou a escala não tiver sido confirmada, interrompa a receita e resolva esses pré-requisitos.
Um exemplo interpretado sem inventar execução: se a saída explicada tem base `0.30`, atribuições `+0.10` e `−0.05` na mesma escala, a soma é `0.35`. Essa conta só explica a regra aditiva; não garante que o modelo real use escala de probabilidade. Se for log-odds, 0.35 não representa 35%. Para explicar `E001`, selecione o índice correspondente em `X_eval`, confira o vetor de atributos e o score do modelo antes de gerar o waterfall local. Se `compute_shap` rejeitar saída multiclasse sem `output_index`, informe a classe correta; não achate o array para fazer o erro desaparecer.

`generate_executive_report(shap_importance,feature_business_names,target_description,model_metric,metric_name='AUC',...)` transforma uma tabela de importância já calculada em Markdown para leitores de negócio. `generate_technical_summary(shap_importance,native_importance=None)` cria resumo técnico e pode comparar rankings. O relatório não calcula SHAP nem demonstra causa. Comparar rankings exige `feature` e `rank` únicos em ambos os lados; confira a interseção, pois duplicatas multiplicam pares. Use [template executivo](../../skills/hub-ml-explainability/templates/relatorio_executivo_explainability.md) e [template técnico](../../skills/hub-ml-explainability/templates/shap_analysis_technical.md) para acrescentar população, classe, escala, amostra, período e limitações; substitua o texto de exemplo por evidência do seu estudo. Uma direção inferida por correlação entre feature e SHAP é descritiva e pode mudar com a amostra.

Para desempenho binário, ROC (curva de sensibilidade contra taxa de falsos positivos) ajuda a ver a discriminação ao variar o limiar; [MT10](MT-parte-ii.md#mt10-2) desenvolve sua interpretação. `calculate_binary_metrics(y_true,y_prob,threshold=0.5)` exige rótulos 0/1 com ambas as classes e probabilidades finitas entre 0 e 1; retorna AUC, KS em pontos percentuais, Gini, Brier, precision, recall, lift e prevalência. Use `plot_roc_curve`, `plot_pr_curve`, `plot_lift_curve` e `plot_ks_curve` para visualizar aspectos distintos; variantes `_resolvido` aplicam tema visual, sem mudar os dados. Atenção: `ks_pct` do relatório e a curva KS têm fórmulas diferentes além da unidade, conforme [MT10](MT-parte-ii.md#mt10-2). A figura não escolhe limiar ou capacidade de revisão. Compare curvas apenas com classe, população e maturação equivalentes. A precisão pode variar com a prevalência mesmo mantendo a revocação; ROC não escolhe capacidade operacional. Com pouco volume, registre incerteza. Em regressão, `calculate_regression_metrics` fornece RMSE (raiz do erro quadrático médio, penaliza erros grandes), MAE (erro absoluto médio), MAPE (erro percentual absoluto médio; este helper exclui alvos zero e devolve NaN se todos forem zero) e R² (coeficiente de determinação, comparação com prever a média do alvo); vetores finitos devem estar alinhados. Um R² negativo indica desempenho pior que essa referência na amostra avaliada.

Para drift driver-side, `detect_drift_all_features(df_reference,df_current,feature_cols,psi_threshold=None,ks_threshold=None,min_non_null=10)` devolve DataFrame por atributo. Sem limites fornecidos, a condição é `NOT_CLASSIFIED`; para classificação, informe **ambos** `psi_threshold` e `ks_threshold` conforme política justificada, não somente um. Numéricas têm PSI e KS; categóricas usam CSI na coluna `psi` do relatório. Recuse ou remapeie a categoria real `__MISSING__`, reservada para ausência no CSI. Valores ausentes entram em baldes/categoria próprios, e a contagem mínima numérica considera observações finitas. Um exemplo de duas coortes de 12 linhas, com categoria A em oito linhas da referência e quatro da atual, mostra uma mudança descritiva de `8/12` para `4/12`; o status depende da política e do cálculo, não é automaticamente “grave”. Se `INSUFFICIENT_DATA`, aumente a amostra ou descreva a cobertura antes de classificar.

Para repetir o detector sem dados de clientes, este exemplo pequeno cria duas tabelas pandas, incluindo ausência numérica e categoria ausente. A função calcula PSI com cortes da referência e um balde de ausentes; CSI trata ausência como categoria. KS usa somente valores numéricos finitos, portanto pode ter denominador diferente do PSI. Sem política de limiares, o status esperado é `NOT_CLASSIFIED`; os valores não devem ser lidos como prova de perda de performance.

```python
import numpy as np
import pandas as pd
from hub_snippets.ml.drift_detection import detect_drift_all_features

ref_num = np.arange(12, dtype=float)
cur_num = np.arange(12, dtype=float) + 2
ref_num[2] = np.nan
cur_num[5] = np.nan
referencia = pd.DataFrame({
    "idade_conta": ref_num,
    "canal": ["A"] * 8 + ["B"] * 3 + [None],
})
atual = pd.DataFrame({
    "idade_conta": cur_num,
    "canal": ["A"] * 4 + ["B"] * 7 + [None],
})
drift = detect_drift_all_features(
    referencia, atual, ["idade_conta", "canal"], min_non_null=10,
)
print(drift[["feature", "psi", "ks_statistic", "status"]])
```
Para acompanhar métricas já maduras, `selecionar_metricas_do_relatorio` traduz `auc_roc` para `auc` e mantém `ks_pct` na unidade correta. Crie `PerformanceMonitor(baseline_metrics,policy=politica,consecutive_alert_periods=3)` com limiares calibrados para cada métrica e direção de deterioração. `add_period('2026-09',metricas,n_predictions=volume)` adiciona um período; `get_current_status()`, `generate_report()` e `plot_timeline("auc")` apresentam leitura; a timeline recebe a chave monitorada e devolve uma figura Plotly. `should_retrain()` devolve candidato de investigação quando critérios são atingidos, nunca autorização automática. A política padrão do módulo é **exemplo**; não a use como norma sem revisão. As skills de [explicação](../../skills/hub-ml-explainability/SKILL.md) e [monitoramento](../../skills/hub-ml-monitoramento-modelo/SKILL.md) orientam os métodos e templates, mas não implantam scheduler ou job.

Esta segunda receita usa rótulos e scores **sintéticos** de duas coortes já maduras. Ela calcula relatórios separados, traduz `auc_roc` para `auc`, define uma política ilustrativa e devolve texto, decisão e figura Plotly. Em dados reais, alinhe IDs, janela do alvo e versão do modelo antes da comparação.

```python
import numpy as np
from hub_snippets.ml.metrics_report import calculate_binary_metrics
from hub_snippets.ml.performance_monitor import (
    PerformanceMonitor, selecionar_metricas_do_relatorio,
)

y_base = np.array([0, 1, 0, 1, 0, 1, 0, 1])
p_base = np.array([.10, .90, .20, .80, .30, .70, .40, .60])
y_atual = np.array([0, 1, 0, 1, 0, 1, 0, 1])
p_atual = np.array([.15, .75, .35, .65, .45, .55, .60, .40])
policy = {"auc": {"warning": .03, "critical": .05,
                  "direction": "higher", "delta": "absolute"}}
base = selecionar_metricas_do_relatorio(
    calculate_binary_metrics(y_base, p_base), policy,
    metricas_obrigatorias=["auc"],
)
mes = selecionar_metricas_do_relatorio(
    calculate_binary_metrics(y_atual, p_atual), policy,
    metricas_obrigatorias=["auc"],
)
monitor = PerformanceMonitor(base, policy=policy)
monitor.add_period("2026-09", mes, n_predictions=len(y_atual))
print(monitor.generate_report())
print(monitor.should_retrain())
fig = monitor.plot_timeline("auc")  # Figure Plotly; exiba no notebook
```
Um retorno de monitor precisa ser lido com a política. Com baseline AUC 0,80, warning absoluto 0,03 e critical 0,05, uma AUC 0,76 cai 0,04 e entra em atenção. Se a regra fosse relativa, o cálculo seria `0,04/0,80=5%`, com outro significado de limite. Para RMSE, aumento costuma ser deterioração; para AUC, queda costuma ser. O módulo rejeita política que não cobre o baseline e pode marcar período incompleto quando a configuração permite ausência de parte das métricas. Sem período algum, `should_retrain()` informa `NO_EVIDENCE`; não há `automatic_retrain_authorized` nesse retorno inicial. O mesmo nome de método não elimina a obrigação de verificar a estrutura do retorno recebido.

<!-- editorial:exclude:start -->
**Fontes:** [SHAP](../../hub_snippets/ml/shap_explainer/shap_explainer.py), [relatório](../../hub_snippets/ml/explainability_report/explainability_report.py), [métricas](../../hub_snippets/ml/metrics_report/metrics_report.py), [curvas](../../hub_snippets/ml/curves_plotly/curves_plotly.py), [drift](../../hub_snippets/ml/drift_detection/drift_detection.py), [monitor](../../hub_snippets/ml/performance_monitor/performance_monitor.py) e skills citadas.
<!-- editorial:exclude:end -->

<a id="mu12-4"></a>
#### 4. Como reagir a alertas sem transformar sinal em ordem automática?

Leia primeiro o **status e sua causa**. `NOT_CLASSIFIED` no detector de drift significa que você não forneceu a dupla de limites necessária para classificar; o número calculado ainda pode ser descrito, com referência e período, mas não recebe cor de política. `INSUFFICIENT_DATA` significa amostra insuficiente segundo a regra da função; aumente cobertura ou registre que ainda não há base para aquele cálculo. Um `ALERT` ou `SEVERE` usa os thresholds que o consumidor escolheu, e sua gravidade deve ser defendida à luz da variabilidade histórica, do tamanho da população e do custo de erro. Um `OK` não prova ausência de todo problema: outros atributos, segmentos ou qualidade de dados podem ter mudado.

As [rotas sintéticas da skill](../../skills/hub-ml-monitoramento-modelo/scripts/README.md) distinguem `DRIFT_NUMERIC_LOCAL_V1`, sem labels, de `BINARY_MATURE_PERFORMANCE_V1`, com labels disponíveis até `evaluation_at`. Performance exige `verify`, `finalize` e `verify_finalized` com request/run_id externos; runner isolado não conclui esse escopo. Nenhuma rota autoriza alerta, retreino ou promoção, e ambas conservam L0/audit na policy.

Depois separe o que mudou. Se PSI de um atributo subiu mas a AUC em coorte madura permaneceu estável, investigue mudança de composição, ausentes, fonte ou regras de transformação; não anuncie degradação comprovada. Se a AUC cai enquanto as entradas parecem estáveis, confira primeiro maturação do alvo, seleção de rótulos, versão do modelo e custo de erros por segmento. Se ambos mudam, compare períodos intermediários e procure a origem do desvio. O teste KS entre distribuições é sensível ao tamanho da amostra; um p-valor pequeno em base enorme não informa sozinho se a diferença é operacionalmente relevante. O [template de drift](../../skills/hub-ml-monitoramento-modelo/templates/drift_report.md) ajuda a registrar volume, referência, política e investigação.

Quando `PerformanceMonitor.should_retrain()` devolve `INVESTIGATE_RETRAINING_CANDIDATE`, o próprio retorno após período informa `automatic_retrain_authorized=False` e passos como validar qualidade dos dados, examinar drift/causa e fazer comparação offline entre modelo vigente e candidato. Se devolve `NO_TRIGGER`, continue acompanhando conforme a política, sem chamar isso de prova de estabilidade permanente. Se devolve `NO_EVIDENCE`, falta período de avaliação; reúna dados maduros antes de concluir. O [template de decisão](../../skills/hub-ml-monitoramento-modelo/templates/retreino_decision.md) organiza alternativas: manter e observar, corrigir pipeline, recalibrar limiar/probabilidade, treinar challenger ou propor promoção depois dos gates. O monitor não executa nenhuma dessas etapas. Ordene e deduplique períodos antes de adicioná-los: “consecutivo” significa ordem de inserção; a classe não detecta lacunas nem repetições de calendário.

Se a preocupação foi levantada por SHAP, confira se a explicação usa a classe e a escala corretas, se o `X` conserva a ordem de colunas e se os IDs acompanharam qualquer amostra. Um atributo que ganhou importância pode apenas estar correlacionado com outro ou refletir mudança de mistura de clientes. Compare importância por período e segmento e examine erros concretos antes de sugerir ação. `generate_executive_report` usa cortes internos de rótulos “alto/médio/moderado” sobre participação relativa; eles não são aprovação regulatória nem prioridade de remediação. Uma explicação local com informação sensível deve ficar no ambiente de acesso apropriado.

Para entregar o resultado, produza duas camadas. A técnica contém versões, queries ou snapshots, contagens, janelas, classes, fórmulas, thresholds, gráficos e logs/runs necessários para reconstrução. A executiva responde o que foi observado, a quem afeta, qual decisão está proposta e que evidência falta. MLflow pode registrar parâmetros, métricas e artifacts seguros, mas `run_governado` herda tracking/experimento do ambiente; confira destino e run ativo antes de usá-lo. Uma falha no fechamento do contexto não desfaz necessariamente registros anteriores. O histórico do `PerformanceMonitor` permanece em memória se não for persistido por outro componente. Não coloque predições individuais por entidade em artifact de tracking; registre agregados e preserve as linhas em camada governada apropriada.

Feche com um próximo passo que tenha responsável e critério de retorno. No exemplo fictício, “a taxa de ausentes na feature de contatos dobrou em setembro; equipe de dados verificará a carga até 05/10; a equipe de modelo repetirá AUC apenas nas decisões com 30 dias completos” é uma ação verificável. “Retreinar porque PSI passou de 0,2” não descreve causa nem autorização; 0,2 tampouco é limite universal. Se o modelo precisar de mudança, teste challenger fora do período de escolha e submeta promoção à governança. A documentação de um alerta deve permitir que outra pessoa veja a mesma evidência e discorde da interpretação sem precisar adivinhar população ou regra.

<!-- editorial:exclude:start -->
**Fontes:** [skill de monitoramento](../../skills/hub-ml-monitoramento-modelo/SKILL.md), [template de drift](../../skills/hub-ml-monitoramento-modelo/templates/drift_report.md), [template de decisão](../../skills/hub-ml-monitoramento-modelo/templates/retreino_decision.md), [detector](../../hub_snippets/ml/drift_detection/drift_detection.py), [monitor](../../hub_snippets/ml/performance_monitor/performance_monitor.py), [run governado](../../hub_snippets/ml/mlflow_run/mlflow_run.py) e [ADR-0016](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/decisions/ADR-0016-mlflow-runs-micromodelos.md). [Índice](MU-indice.md#sumario-mu).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU11](#mu11) · [Próximo: MU13](MU-parte-iv.md#mu13) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT10](MT-parte-ii.md#mt10)
<!-- editorial:exclude:end -->
