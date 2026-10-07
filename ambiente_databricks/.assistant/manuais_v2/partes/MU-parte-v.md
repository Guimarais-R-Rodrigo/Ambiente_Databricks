<a id="parte-mu-v"></a>
# MU parte v

<!-- editorial:exclude:start -->
Edição documental de 07/10/2026. Leitura dividida com o conteúdo integral dos módulos.

[Índice](MU-indice.md#sumario-mu) · [Livro completo](../../MANUAL_DO_USUARIO.md#sumario-mu)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu14"></a>
<a id="mu14"></a>
### MU14 — Planejar uma entrega visual e aplicar temas

Um tema organiza escolhas de apresentação, como cor, fonte e espaço. Ele ajuda a manter uma linguagem comum, mas não decide qual pergunta responder nem verifica os números mostrados. Este capítulo guia uma entrega simples: escolher uma forma de gráfico, carregar uma referência do Hub, criar uma proposta isolada, aplicá-la apenas a uma figura e comparar o resultado. Os dados do exemplo são sintéticos. As funções descritas existem no código do Hub; sua presença no Git não confirma instalação ou homologação no seu workspace.

<a id="mu14-1"></a>
#### MU14.1 — Comece pela pergunta, pelo público e pela forma

Antes de escolher cor, escreva em uma frase a decisão que a imagem deve apoiar. “Quantos chamados cada equipe resolveu nesta semana?” pede comparar quantidades entre categorias. “Como o volume de chamados variou ao longo das semanas?” pede mostrar uma sequência no tempo. “A solução ficou melhor para quais grupos?” exige decidir qual medida representa “melhor” e se os grupos são comparáveis. Essas perguntas não são intercambiáveis: a primeira pode funcionar em barras; a segunda, em linha temporal; a terceira talvez precise de barras separadas ou tabela com contexto. A forma deve expor a relação importante, sem sugerir uma relação que os dados não sustentam.

Defina quem vai ler. Uma equipe operacional pode precisar de rótulos exatos e da unidade em cada eixo; uma apresentação executiva talvez precise começar pela conclusão e depois mostrar os detalhes. Não retire unidade, período, denominador ou definição da métrica para “limpar” o desenho. Se o eixo mostra contagem de chamados, escreva “chamados”; se mostra porcentagem, indique a base da porcentagem. Para proporções, pergunte “de quantos?”; para uma série, pergunte se os intervalos são iguais e se há lacunas. O visual deve preservar a possibilidade de conferir o número, não apenas produzir uma impressão de crescimento ou queda.

Um roteiro curto ajuda a preparar a célula antes de importar qualquer helper: pergunta, audiência, dados necessários, unidade, forma, conclusão provisória e ressalvas. Por exemplo: “Comparar chamados resolvidos por três equipes em uma semana; contagem de chamados; dados sintéticos de demonstração; barras horizontais; não interpretar a diferença como produtividade sem saber volume recebido e complexidade.” Nesse caso, três barras deixam a comparação direta. A diferença entre 12 e 8 chamados é visível, mas não prova que uma equipe trabalhou melhor. O tema pode uniformizar as barras e o título; não fornece o contexto operacional ausente.

O [guia de Plotly](../../hub_snippets/visual/theme_plotly/README.md) reforça essa ordem: construa uma figura com dados e rótulos corretos, depois aplique aparência. Plotly é a biblioteca Python usada aqui para construir o gráfico. Uma figura pronta ainda pede inspeção de escala, unidade, fonte declarada e espaço disponível. Ao apresentar a alguém, inclua uma frase de interpretação perto da figura; o leitor não deve adivinhar a decisão pretendida a partir da paleta. Se houver mais de uma figura no mesmo notebook, anote quais usam uma proposta visual e quais mantêm o padrão, para não transformar uma experiência local em regra tácita da equipe.

Se a comparação envolve muitos grupos, barras podem ficar espremidas; então ordene categorias de modo explicado, agrupe apenas quando houver justificativa ou divida a pergunta em gráficos menores. Para uma relação entre duas medidas contínuas, pontos podem revelar dispersão que uma única média esconderia. Para distribuição, um histograma mostra frequência por faixa, mas a escolha das faixas altera a leitura e precisa ser declarada. Essas são escolhas de comunicação, não configurações automáticas do tema. Em qualquer formato, evite um título que já prometa causalidade quando a figura mostra apenas associação. A pergunta deve ser mais específica que “fazer um gráfico bonito”.

<a id="mu14-2"></a>
#### MU14.2 — Escolha referência, proposta e contexto

O Hub conserva rotas legadas e oferece uma rota de tema **opt-in**, isto é, usada apenas quando você a chama explicitamente. O núcleo [`visual.tema`](../../hub_snippets/visual/tema/README.md) lê uma configuração JSON, um texto estruturado em campos e valores, e devolve um `ResolvedTheme`: um retrato completo e protegido daquelas escolhas. “Resolver” significa validar e reunir os valores para um consumidor; não significa redesenhar todos os notebooks. Os contextos do contrato são `notebook`, `readme` e `presentation`. Para o adaptador Plotly deste capítulo, escolha `notebook`; ele aceita somente o modo visual `light`. Uma configuração válida de `readme` não deve ser passada ao gráfico para tentar obter uma aparência editorial.

Há três decisões de uso. Se você quer a aparência histórica sem criar proposta, mantenha as funções legadas do componente. Se quer testar um tema no notebook, carregue a referência sintética com `load_reference_theme("notebook")` e use as funções terminadas em `_resolvido`. Se recebeu um arquivo de proposta do mantenedor, ele pode ser carregado com `load_theme(root, relative_path, expected_sha256=..., expected_context="notebook")`, usando uma raiz de arquivos autorizada e a revisão exata. O último caminho é mais exigente porque lê bytes de um arquivo escolhido; não remova o hash esperado para fazer outra revisão “passar”. Nenhuma das três decisões, por si, instala um padrão no workspace.

A referência `legado_notebook.json` é uma fixture, ou seja, um exemplo controlado para comparação e teste. Ela contém 48 tokens; **token** é um nome de escolha visual associado a um valor, como `brand.primary = #005CA9`. É útil para começar porque reproduz a linguagem histórica nos consumidores integrados, mas não significa que a proposta esteja aprovada como nova identidade. O [guia operacional](../../hub_padroes/identidade_visual/GUIA_OPERACIONAL.md) demonstra a referência, a cópia e um erro esperado. Seu notebook de exemplo altera apenas dados sintéticos em memória; a preparação localiza a pasta `.assistant` e pode exigir as bibliotecas declaradas em `requirements-temas.txt`. Não instale pacotes fora do procedimento autorizado do seu ambiente só porque uma importação falhou.

Para experimentar uma cor sem alterar a referência, obtenha uma cópia com `to_dict()`, ajuste um campo e valide a cópia. Um dicionário Python é uma coleção de nomes e valores; neste caso, `tokens` é outro dicionário dentro dele. O código seguinte supõe que a pasta `.assistant` já está no caminho de importação do Python, como explica o exemplo do Hub:

```python
from hub_snippets.visual.tema import load_reference_theme, resolve_theme

referencia = load_reference_theme("notebook")
proposta = referencia.to_dict()
proposta["tokens"]["brand.primary"] = "#112233"
tema_proposto = resolve_theme(proposta, expected_context="notebook")

print(referencia.tokens["brand.primary"])   # #005CA9
print(tema_proposto.tokens["brand.primary"])  # #112233
```

O `#` inicia uma cor hexadecimal de seis dígitos; o contrato exige `#RRGGBB` em maiúsculas. `resolve_theme` não corrige silenciosamente um valor inválido nem acrescenta campos ausentes. Se você apagar `brand.primary`, recebe `SCHEMA_REQUIRED`; isso indica que a proposta ficou incompleta, não que a função deva usar uma cor de fallback. `normalize_color` pode converter uma cor minúscula explicitamente durante a autoria, mas a importação não o faz por conta própria. A referência continua azul depois que a cópia muda. Se precisar guardar o trabalho, `export_theme(tema_proposto)` devolve bytes em memória; salvar arquivo, compartilhar, aprovar e publicar são ações separadas.

Um `fingerprint` permite reconhecer o conteúdo resolvido junto com o schema e o manifesto de assets que participaram da validação. Ele ajuda a comparar a mesma configuração em uma rodada compatível, mas não identifica o autor, garante contraste ou aprova a paleta. O [contrato central](../../hub_padroes/identidade_visual/README.md) explica que os defaults do schema são exemplos declarativos, não valores inseridos numa proposta. Assim, uma proposta precisa ser completa; “ficou parecida com o legado” não basta para concluir que todos os campos são válidos. Se um erro aparecer, consulte [ERROS.md](../../hub_padroes/identidade_visual/ERROS.md) pelo código, campo e ação recomendada, sem colar dados sensíveis na mensagem de ajuda.

Ao escolher uma proposta recebida, pergunte também qual parte dela será realmente lida pelo consumidor. O schema tem tokens para notebook, material editorial e apresentação, e não existe um botão universal que aplique tudo ao mesmo tempo. No caso Plotly, a cor principal, a paleta, a fonte e medidas de gráfico têm efeitos definidos no adaptador; tokens de uma tabela HTML ou de um cabeçalho não serão aplicados magicamente à mesma figura. Essa limitação ajuda a comparar com justiça: anote “o que mudou” e “o que não mudou” antes de concluir que a proposta ficou melhor. Se a organização exige uma identidade aprovada, valide com o mantenedor qual configuração é autorizada; uma referência de teste é ponto de partida pedagógico, não decisão institucional.

<a id="mu14-3"></a>
#### MU14.3 — Aplique a uma figura e compare

Construa primeiro uma figura com os dados e rótulos escolhidos. O exemplo abaixo cria três contagens sintéticas que somam 30. A contagem total é conhecida porque foi escrita no exemplo; o helper não a calcula para você. `aplicar_tema_resolvido` é uma função do Hub que muda propriedades de apresentação da figura Plotly recebida e devolve a mesma figura. A chamada não ativa um template global da sessão e não muda os valores das barras. `fig.show()` é o passo que pede ao notebook para exibir o gráfico; o retorno da função de tema, sozinho, não equivale a uma visualização vista por alguém.

```python
import plotly.graph_objects as go
from hub_snippets.visual.tema import load_reference_theme, resolve_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

referencia = load_reference_theme("notebook")
dados = {"Equipe A": 12, "Equipe B": 10, "Equipe C": 8}

base = go.Figure(go.Bar(x=list(dados), y=list(dados.values())))
base.update_layout(
    title="Chamados resolvidos por equipe — semana sintética",
    xaxis_title="Equipe",
    yaxis_title="Chamados resolvidos",
)

fig_referencia = go.Figure(base)
aplicar_tema_resolvido(fig_referencia, referencia,
                      fonte="dados sintéticos deste exemplo", n=30)

proposta = referencia.to_dict()
proposta["tokens"]["brand.primary"] = "#112233"
tema_proposto = resolve_theme(proposta, expected_context="notebook")
fig_proposta = go.Figure(base)
aplicar_tema_resolvido(fig_proposta, tema_proposto,
                      fonte="dados sintéticos deste exemplo", n=30)

fig_referencia.show()
fig_proposta.show()
```

Compare as duas imagens mantendo o mesmo conjunto, período, tipo de barra e escala. `brand.primary` alimenta a cor do título no adaptador Plotly, então essa escolha deve mudar entre referência e proposta. Ela **não** altera automaticamente a cor de cada barra: o consumidor usa `palette.categorical` para uma sequência de cores e respeita cores já fixadas nos traces. Se você esperava mudar as barras e só o título mudou, a função não falhou; foi a expectativa que estava fora do mapeamento daquele token. O que comparar agora é legibilidade do título, contraste com o fundo, espaço de eixo e clareza do rodapé. A frase “Fonte: dados sintéticos deste exemplo” e o “N = 30” são declarações do código acima. Com dados reais, confira origem e total antes de exibi-los.

Uma função legada como `aplicar_tema` continua disponível para quem precisa do padrão anterior. Evite misturar a rota legada e a nova sem anotar qual foi aplicada a cada figura. Para a nova rota, o tema pode redefinir largura, altura, margens, fonte e legenda; por isso, se uma figura exige um tamanho específico, ajuste esse layout **depois** da chamada. A função não corrige eixos enganadores, unidade errada, agregações ou métricas. Também não recolore cores explícitas de traces nem modifica dados analíticos. Se a figura já tinha uma legenda muito abaixo do desenho, inspecione o rodapé: reaplicar a função pode duplicar anotações e criar sobreposição.

Existe uma operação separada, `registrar_template_plotly_resolvido`, para registrar um template `hub-*` na sessão. O argumento `nome` é obrigatório e passado por palavra-chave, por exemplo `nome="hub-proposta"`; o registro não troca o padrão da sessão a menos que `ativar=True`. Mesmo com esse controle, uma ativação pode afetar figuras criadas depois na mesma sessão. Para uma comparação de duas figuras, prefira a aplicação por figura do exemplo: ela deixa claro o alcance. Se alguém escolheu registrar um template, deve documentar o nome, a opção de ativação e como restaurará o default anterior. A rota HTML, como `section_header_html_resolvido`, também exige tema explícito, mas tem seus próprios modos e propriedades; o fato de Plotly aceitar o tema não demonstra que todo consumidor o aceitará.

Faça a comparação como um pequeno experimento controlado. Primeiro confira os números na variável `dados`: 12 + 10 + 8 = 30; esse total é o N declarado e não uma medição feita pela função. Depois olhe a figura com a referência e anote título, cor de barras, posição da legenda, dimensões e rodapé. Repita a observação com a proposta, sem trocar o conjunto de dados. Se a proposta só alterou `brand.primary`, não atribua à cor nova uma mudança de quantidade: ambas as figuras devem mostrar as mesmas três alturas. Se aparecer uma diferença numérica, ela veio de outro trecho do notebook e precisa ser investigada antes da entrega. A comparação lado a lado separa efeito do tema de efeito da análise.

Também compare com intenção. Um título `#112233` pode ter bom contraste em uma superfície e fraco em outra; mesmo que o schema aceite o valor, o público precisa conseguir lê-lo. Se a figura ficou larga demais, ajuste a largura explicitamente após aplicar o tema e confira o efeito no eixo e no rodapé. Se você decidir usar cores próprias para as barras, registre esse fato: a paleta categórica do tema já não será a única responsável pela aparência. O resultado desejado é uma figura cujo caminho de construção pode ser explicado: dados e rótulos primeiro, tema opt-in depois, ajustes locais por último, exibição e revisão ao final.

<a id="mu14-4"></a>
#### MU14.4 — Revise unidade, consistência e leitura real

Depois de ver a figura, volte à pergunta inicial. As barras realmente permitem comparar as equipes? O eixo vertical começa e termina em valores que não dramatizam uma diferença pequena? Os rótulos “Equipe A/B/C” correspondem aos registros? “Semana sintética” e “chamados resolvidos” continuam visíveis? A cor não deve ser a única forma de distinguir um estado importante; acrescente rótulo, legenda ou texto quando o significado exigir. Uma paleta coerente ajuda a reconhecer o Hub, mas não substitui valor, unidade, escala e explicação da conclusão. Se a comparação atravessa gráficos, mantenha as mesmas definições, período e limites de eixo quando isso for necessário para comparar diretamente.

Inspecione a figura no tamanho em que o público vai usá-la. Um notebook largo pode esconder que o título, o rodapé ou a legenda colidem numa tela menor. Conferir uma saída em Python local não prova como ela ficará no Databricks; abrir a superfície real é uma etapa própria. Verifique contraste, tamanho do texto, leitura de cores e possibilidade de entender a figura sem depender apenas da cor. Um tema validado pode ter combinações pouco legíveis; um modo chamado “alto contraste” também precisa de avaliação visual. O adaptador Plotly atual aceita apenas `notebook/light`, portanto não tente selecionar `dark` ou `high_contrast` para esse gráfico esperando uma conversão implícita.

Antes de entregar, deixe junto da figura uma frase que diga o que ela mostra e outra que diga seu limite. Para o exemplo: “A Equipe A resolveu 12 chamados na semana sintética, contra 8 da Equipe C.” Em seguida: “Essas contagens não consideram complexidade nem volume recebido; não são medida de produtividade.” Com dados de trabalho, acrescente fonte verificável, data de extração, definição da métrica e tratamento de ausentes. Não use a cor temática para esconder uma ressalva: ela deve estar em texto. Essa checagem final dá ao leitor as condições para julgar o dado e mantém a identidade visual no seu papel correto, o de apresentar com clareza uma análise já bem construída.

Uma revisão por outra pessoa deve conseguir reconstruir a leitura sem receber o notebook inteiro em explicação oral. Peça que ela responda qual é a unidade, de onde veio o N, qual período foi medido, o que cada categoria representa e qual conclusão é permitida. Se precisar explicar que uma cor “na verdade” significa outra coisa ou que um eixo omite casos especiais, a figura ainda precisa de rótulos ou texto adicional. Para compartilhar a proposta visual, envie a revisão e o contexto corretos pelos canais autorizados; exportar JSON ou fazer uma captura de tela não converte uma experiência em tema aprovado. Guarde a interpretação perto dos números para que uma alteração futura do visual não apague o significado.

<!-- editorial:exclude:start -->
[Construção do contrato de temas](MT-parte-vi.md#mt23) · [Consumidores e superfícies](MT-parte-vi.md#mt24).
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU13](MU-parte-iv.md#mu13) · [Próximo: MU15](#mu15) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT23](MT-parte-vi.md#mt23)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu15"></a>
<a id="mu15"></a>
### MU15 — Montar um notebook visual completo

Um notebook visual útil permite descobrir o que foi analisado, de onde vieram os números e qual conclusão eles sustentam. Este roteiro monta uma versão pequena com dados sintéticos: abertura, índice, seções, indicadores, tabela, distribuição e correlação; curvas de modelo entram somente se houver avaliação binária pertinente. Os exemplos partem de uma sessão nova com o pacote `.assistant` disponível e, para a parte distribuída, Spark configurado. HTML é a linguagem que marca elementos de uma página; CSS descreve sua aparência. As funções do Hub que devolvem HTML entregam texto para um renderizador, não uma figura já vista por alguém.

<a id="mu15-1"></a>
#### MU15.1 — Abertura, seções e índice honesto

Comece com uma célula Markdown: título, pergunta, população, unidade de observação, janela temporal, origem dos dados e limite conhecido. Markdown é o texto com títulos `#` e listas que permanece legível sem executar Python. Num notebook de demonstração, escreva “dados sintéticos” perto do título, não só no rodapé de uma figura. Por exemplo, a pergunta “Como saldo e tempo de relacionamento se distribuem e se associam?” não é respondida por um cartão de indicadores sozinho. O leitor precisará ver o recorte, os valores e a ressalva de que uma associação não demonstra causa. Um pequeno parágrafo de orientação reduz a chance de alguém interpretar um gráfico fora de contexto quando abrir o notebook no meio.

Um cabeçalho visual pode vir antes do título, mas não substitui esse texto. O pacote traz os PNGs compartilhados `headers/png/cabecalho_crm.png` e `cabecalho_squad.png`; o [guia de cabeçalhos](../../hub_readmes_visual_assets/headers/README.md) explica qual usar e como calcular o caminho relativo a partir do documento. Em notebook geral, escolha CRM; no específico da Squad, escolha Squad, sem empilhá-los. A célula Markdown pode exibir a imagem por caminho, sem iniciar compute. Mantenha título, escopo e instruções em texto normal, com alt adequado para a imagem. Ao publicar o notebook por um procedimento autorizado, a árvore de assets precisa acompanhá-lo; uma referência para arquivo ausente renderizará mal mesmo que a célula Markdown esteja correta.

Esboce a sequência real: contexto, descrição de variáveis, qualidade e recorte, distribuição, relações e síntese. O [`index_generator`](../../hub_snippets/visual/index_generator/README.md) pode imprimir os nomes canônicos de etapas de análise exploratória de dados, também chamada EDA. Ele não examina as células para saber o que foi feito e não cria links clicáveis. Se seu notebook tiver apenas as etapas 0, 4, 5 e 8, peça somente essas. `markdown=True` devolve texto Markdown, que você pode revisar e colocar numa célula de texto; `markdown=False` devolve HTML visual. A versão `_resolvido` aplica um tema apenas no HTML, sem mudar o conteúdo nem criar navegação. Se precisa de navegação clicável, mantenha títulos e âncoras reais no Markdown e teste os links no destino; não atribua essa função ao índice visual.

O bloco a seguir encontra o pacote a partir da pasta atual e de seus pais, como faz o exemplo de tema do Hub. Em uma instalação de workspace cujo caminho não é encontrado, preencha `HUB_ROOT` com a pasta `.assistant` recebida do mantenedor antes de continuar. Ele não instala bibliotecas nem procura dados. As importações de apresentação são declaradas agora para que as próximas células não dependam de variáveis invisíveis:

```python
from pathlib import Path
import sys

HUB_ROOT = ""  # se necessário, informe a pasta .assistant recebida
inicio = Path.cwd()
candidatas = [Path(HUB_ROOT)] if HUB_ROOT else [
    candidato
    for base in [inicio, *inicio.parents]
    for candidato in (base, base / ".assistant", base / "ambiente_databricks/.assistant")
]
raiz_hub = next(
    (p for p in candidatas if (p / "hub_snippets/visual/tema/tema.py").is_file()),
    None,
)
if raiz_hub is None:
    raise RuntimeError("Informe HUB_ROOT com a pasta .assistant do Hub")
sys.path.insert(0, str(raiz_hub))

from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.index_generator import gerar_indice_eda

tema = load_reference_theme("notebook")
indice_textual = gerar_indice_eda(etapas_ativas=[0, 4, 5, 8], markdown=True)
print(indice_textual)
```

O retorno é um rascunho de roteiro, não prova de que as quatro seções existem. Depois de criar cada seção, confira se título e ordem correspondem ao índice; se não houver etapa 5, retire-a. `None` pediria as nove etapas do mapa, e uma lista vazia não mostraria nenhuma. Isso evita um sumário ornamental que promete análises ausentes. A referência carregada é uma configuração sintética e validada de contexto `notebook`, apropriada para os consumidores demonstrados; ela não é uma nova identidade aprovada pela organização. O capítulo [MU14](#mu-mod-mu14) mostra como propor outra cor e aplicar tema a uma figura sem alterar o padrão da sessão.

No texto da abertura, deixe uma nota de reprodução: versão ou data da extração, critérios de inclusão, campos usados e se o notebook consulta uma fonte viva ou uma amostra congelada. Em material sintético, escreva que os números foram inventados somente para ensinar o fluxo; não cite um sistema corporativo como origem. Antes do primeiro gráfico, anuncie o que significa uma linha do conjunto, pois contar linhas, clientes e eventos são operações diferentes. Se a análise tiver execução demorada, separe células de preparação das de apresentação para que o leitor possa reler as conclusões sem acreditar que um bloco HTML recalculou os dados. O índice deve descrever essa ordem real.

<a id="mu15-2"></a>
#### MU15.2 — Orientação visual, badges e indicadores já calculados

Um título Markdown anuncia uma seção para navegação e leitura; [`section_header_html_resolvido`](../../hub_snippets/visual/section_header/README.md) pode reforçar visualmente a etapa e sua descrição. A função recebe `tema` explicitamente e devolve uma string HTML. `displayHTML` é a função disponível no notebook Databricks para pedir que esse texto seja exibido; em outro ambiente, escolha um renderizador HTML apropriado. O cabeçalho não detecta a etapa real nem certifica que uma análise foi feita. Use `etapa=4` somente diante de conteúdo de análise univariada, e dê `titulo`/`descricao` explícitos quando estiver fora do roteiro do Hub. Um número inválido pode virar um cabeçalho genérico em vez de falhar. Preserve o título Markdown próximo, pois um bloco HTML não deve ser a única pista textual da estrutura.

Um divisor resolve outro problema: separar blocos sem anunciar uma nova análise. `divider_light_resolvido(tema)` e variantes retornam HTML curto. Um badge é uma pequena etiqueta de estado; `badge_status_resolvido("Dados sintéticos", tema, tipo="info")` comunica o texto que você declarou, sem inspecionar uma tabela. `badge_score_resolvido` calcula uma classe por cortes fixos da implementação; não use seu verde como veredicto de negócio sem revisar esses cortes. O HTML desses componentes usa CSS derivado do `ResolvedTheme`, mas só na chamada terminada em `_resolvido`. Carregar o tema não modifica HTML já exibido nem atualiza as funções legadas. Isso permite testar o visual de uma seção por vez.

KPI significa **indicador-chave de desempenho**. O [`kpi_card`](../../hub_snippets/visual/kpi_card/README.md) monta cartões de valores que você já calculou; não soma linhas, não busca Spark nem verifica fonte ou unidade. O argumento `metricas` é um dicionário de rótulos e textos prontos. Uma boa escolha para a primeira tela é mostrar recorte, total e ressalva curta, e depois oferecer a tabela que sustenta os valores. Formate números brasileiros antes do cartão com `fmt_int`, `fmt_pct`, `fmt_brl` ou `fmt_delta` conforme a unidade. `fmt_pct(0.928)` produz `92,8%` porque, por padrão, recebe uma razão entre 0 e 1; se o valor já vier como 92,8, use `input_scale="percent"`. Guarde a medida numérica para cálculos posteriores. Strings formatadas servem à leitura, não substituem a coluna original.

Esta célula define o único conjunto principal do roteiro: oito observações sintéticas, uma por `id_sintetico`. Cada registro traz equipe, saldo, tempo de relacionamento em meses, variação, volume e estado de resolução. Os dois indicadores são calculados desse conjunto; a tabela e os gráficos da próxima seção reutilizam `registros`. Mantenha um título Markdown “Resumo” na célula de texto anterior. `displayHTML` pode ser chamado várias vezes, mas cada retorno é uma peça visual, não um documento persistido:

```python
from hub_snippets.constants.format_br import fmt_int, fmt_pct
from hub_snippets.visual.section_header import section_header_html_resolvido
from hub_snippets.visual.divider import divider_light_resolvido
from hub_snippets.visual.badge import badge_status_resolvido
from hub_snippets.visual.kpi_card import kpi_card_html_resolvido

registros = [
    {
        "id_sintetico": i,
        "equipe": "A" if i <= 4 else "B",
        "saldo": float(i),
        "tempo_meses": float(2 * i),
        "variacao": -5 if i == 1 else i,
        "resolvido": i not in (4, 8),
        "volume": 1000 * i,
    }
    for i in range(1, 9)
]
total_sintetico = len(registros)
resolvidos = sum(int(r["resolvido"]) for r in registros)
taxa_sintetica = resolvidos / total_sintetico
metricas = {
    "Registros do exemplo": fmt_int(total_sintetico),
    "Resolvidos": fmt_int(resolvidos),
    "Taxa de resolução": fmt_pct(taxa_sintetica),
    "Escopo": "oito observações sintéticas",
}

displayHTML(section_header_html_resolvido(
    tema, titulo="Resumo do exemplo", descricao="Seis resolvidos em oito registros."
))
displayHTML(badge_status_resolvido("Demonstração, não dado real", tema, tipo="info"))
displayHTML(kpi_card_html_resolvido(metricas, tema))
displayHTML(divider_light_resolvido(tema))
```

Há oito registros e seis marcados como resolvidos: 6 ÷ 8 = 0,75, portanto `fmt_pct` mostra `75,0%`. As equipes A e B têm quatro registros cada, com três resolvidos em cada uma; isso dá ao leitor outra forma de conferir o numerador e o denominador na tabela. O formatador só apresenta a razão e o cartão só percorre o dicionário. Se o resumo mostrar uma taxa diferente da contagem detalhada, reconcilie o cálculo antes de alterar a string. O HTML do cartão escapa rótulo e valor como texto, mas isso não dispensa política de dados sensíveis nem revisão da saída. A versão Markdown do KPI existe para texto mais portátil, sem a aparência temática da função HTML. O mecanismo de precisão e localidade dos formatadores está no [manual técnico de formatação](MT-parte-ii.md#mt-mod-mt06).

Para representar um estado analítico, não deixe a cor falar sozinha. Um badge “amostra parcial” com `tipo="warn"` continua sendo uma declaração de quem redigiu; precisa aparecer no texto da seção que explica o recorte. O [guia do badge](../../hub_snippets/visual/badge/README.md) registra contraste aproximado de 3,99:1 no estilo `warn` legado, abaixo do [requisito de 4,5:1 para texto comum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), consultado em 07/10/2026; não o apresente como componente plenamente acessível. Na rota resolvida, confira a combinação realmente recebida do tema. Para percentuais, pontos percentuais e pontos-base não são a mesma coisa: uma taxa que sobe de 10% para 12% aumentou **2 pontos percentuais**. `fmt_delta(0.02)` formata `+2,0 pp`; `unidade="bps"` muda a escala para pontos-base. O [guia de formatos brasileiros](../../hub_snippets/constants/format_br/README.md) explica também moeda, decimais, abreviações e limites de precisão. Use o formatador somente depois de decidir qual unidade e escala seus dados realmente têm.

O `ResolvedTheme` usado aqui é uma configuração completa de contexto notebook, validada pelo núcleo. Cada consumidor escolhe apenas os tokens relevantes ao seu HTML. Por exemplo, trocar a cor do título do Plotly não significa que a borda de um cartão ou a linha do divisor mudará da mesma forma. Se uma peça parece diferente das demais, confira qual rota foi chamada antes de concluir que o tema está inconsistente: `section_header_html` sem `_resolvido` continua legado, enquanto `section_header_html_resolvido` usa o argumento `tema`. Os componentes não ficam inscritos num tema global. Isso reduz surpresas entre células, mas exige passar o tema em cada chamada e registrar no notebook qual referência ou proposta está em teste. O [contrato técnico do tema](MT-parte-vi.md#mt-mod-mt23) explica sua resolução; o [mapa de consumidores](MT-parte-vi.md#mt-mod-mt24) mostra quais campos chegam a cada componente.

Também vale distinguir estado e score. `badge_status_resolvido("Revisar unidade", tema, tipo="warn")` usa um tipo que o autor escolheu; não calcula se a unidade está errada. `badge_score_resolvido(80, tema, max=100)` calcula uma razão 0,8 e retorna o estilo `ok` pelos cortes do próprio helper. Esse `ok` é uma regra de apresentação, não autorização para implantar um modelo nem parecer de qualidade de dados. Se sua política usa outro limiar, escreva e implemente a política em lugar próprio, e use um badge de status explícito apenas para comunicar a decisão já tomada. O texto do badge deve permitir a leitura mesmo sem distinguir verde e amarelo.

Pense na composição como uma página com hierarquia: título da seção, uma frase que explique o recorte, cartões de poucos indicadores e só então a tabela ou figura que sustenta a síntese. Aqui o cartão “8 registros” significa oito observações inventadas, cada uma identificada por uma linha de `registros`; não significa oito clientes reais nem oito eventos de uma fonte externa. Numa adaptação, mude o rótulo para a unidade correta. Se uma taxa tiver muitos denominadores possíveis, mostre também o denominador no cartão ou na frase imediatamente seguinte. O resultado HTML pode ser bonito e ainda conter uma métrica mal definida; a validação principal é confrontar cada string com a análise numérica anterior.

<a id="mu15-3"></a>
#### MU15.3 — Tabela pequena, distribuições, correlação e curvas quando couberem

Depois do resumo, mostre os valores que permitem ao leitor conferir a síntese. Para poucas linhas já agregadas, [`display_styled_resolvido`](../../hub_snippets/display/dataframe_styled/README.md) recebe um **DataFrame pandas**, uma tabela que cabe na memória do processo Python, e devolve HTML. Um DataFrame Spark distribui trabalho e dados entre máquinas; não passe o objeto Spark diretamente ao Styler do pandas. Se a base é grande, agregue ou limite no Spark antes de trazer um resultado pequeno ao **driver**, o processo que coordena a aplicação e mantém a memória local usada pelo pandas e pelo Plotly. Converter a base inteira com `toPandas()` apenas para colorir uma tabela pode exceder essa memória e expor dados que não deveriam sair do processamento distribuído.

Esta célula usa os mesmos oito `registros` criados na seção anterior, sem converter um conjunto real. Assim, a contagem de linhas da tabela pode ser confrontada com o KPI: quatro da equipe A e quatro da B, sendo três resolvidos em cada equipe. `highlight_cols` indica explicitamente onde negativos devem ganhar ênfase; sem ela, o tema muda a aparência do cabeçalho, mas não destaca sinais. `fmt_int` produz texto brasileiro para a coluna de exibição, enquanto `variacao` permanece numérica para a regra de destaque. A string HTML é enviada ao renderizador só depois de produzida:

```python
import pandas as pd
from hub_snippets.constants.format_br import fmt_int
from hub_snippets.display.dataframe_styled import display_styled_resolvido

resumo = pd.DataFrame(registros)
resumo["Volume (texto BR)"] = resumo["volume"].map(fmt_int)
resumo = resumo[[
    "id_sintetico", "equipe", "saldo", "variacao", "resolvido",
    "Volume (texto BR)",
]]
html_tabela = display_styled_resolvido(
    resumo, tema, highlight_cols=["variacao"]
)
displayHTML(html_tabela)
```

Espera-se `1.000` até `8.000` na coluna de volume, um valor por linha, e realce apenas para `-5` na `variacao` do primeiro registro; os números em `registros` permanecem os mesmos. A coluna booleana `resolvido` permite contar seis valores verdadeiros sem confiar no cartão. Uma coluna inexistente em `highlight_cols` pode passar sem aviso, então confira os nomes após qualquer renomeação. O helper reconhece para destaque `int` e `float` negativos, não uma string `"-5"` que apenas parece numérica. Sua saída não habilita escape HTML geral de células: conteúdo textual externo não confiável requer política apropriada antes da renderização. Para uma tabela grande ou com paginação, use outra camada de apresentação; este recurso é para um resultado local pequeno.

Quando a pergunta é “como os valores se espalham?”, a [`distribution_grid`](../../hub_snippets/display/distribution_grid/README.md) produz histogramas. Um histograma agrupa números em faixas e mostra frequência. A rota `_resolvido` aceita DataFrame Spark, escolhe colunas numéricas, usa `smart_sample` e coleta uma amostra limitada ao driver para desenhar no Plotly. O N no rodapé é o tamanho coletado, não o volume total da população. Uma cauda rara pode não aparecer; se a decisão depende de poucos casos extremos, faça contagens direcionadas no Spark. Escolha `sample_n` e `ncols` para sua pergunta e capacidade do ambiente, mantendo unidade de cada variável e anotando o recorte.

Para a pergunta “duas medidas variam juntas?”, [`correlation_matrix`](../../hub_snippets/display/correlation_matrix/README.md) calcula uma matriz no Spark e devolve uma figura mais `strong_pairs`, lista de pares cuja **magnitude** da correlação atinge o corte indicado: `abs(coeficiente) >= threshold_highlight`. Assim, com corte 0,8, tanto −0,9 como +0,8 entram; o sinal ainda distingue direção da associação. A função aceita Pearson ou Spearman; no exemplo, Pearson resume associação linear. O código elimina linhas com nulos nas colunas selecionadas antes do cálculo, o que pode mudar a população. O corte seleciona pares para investigação, não elimina variáveis nem prova causalidade. A escala divergente do tema muda a apresentação de valores de −1 a +1, sem alterar os coeficientes. Não use códigos numéricos de categorias como se fossem medidas contínuas com relação substantiva.

O bloco abaixo reutiliza `registros` da primeira célula de indicadores, de modo que tabela, distribuição e correlação representem as mesmas oito observações. Ele só deve ser executado em ambiente no qual PySpark, Plotly, pandas e os requisitos do Hub já estejam disponíveis; criar a sessão ou calcular correlação pode iniciar trabalho Spark. As duas medidas foram construídas proporcionalmente (`tempo_meses = 2 × saldo`), então Pearson deve ser +1, salvo diferença de representação numérica no runtime. Essa expectativa matemática ajuda a conferir o mecanismo, mas a figura gerada em seu ambiente ainda precisa ser vista e interpretada:

```python
from pyspark.sql import SparkSession
from hub_snippets.display.distribution_grid import plot_distributions_resolvido
from hub_snippets.display.correlation_matrix import plot_correlation_resolvido

spark = SparkSession.builder.getOrCreate()
dados_spark = spark.createDataFrame(registros)

grade = plot_distributions_resolvido(
    dados_spark, tema, cols=["saldo", "tempo_meses"],
    ncols=2, sample_n=8,
)
matriz, pares = plot_correlation_resolvido(
    dados_spark, tema, cols=["saldo", "tempo_meses"],
    method="pearson", threshold_highlight=0.8,
)
print("Pares para investigar:", pares)
grade.show()
matriz.show()
```

Mesmo o coeficiente esperado de +1 aqui não deve ser narrado como descoberta: `tempo_meses` foi definido como o dobro de `saldo` no exemplo. Como `sample_n=8` e a fonte tem oito linhas, a grade usa as oito neste roteiro; em bases maiores ela continua amostral. A matriz calcula sobre as oito linhas sem nulos nas colunas selecionadas. Num trabalho real, confira unidade de observação, período, faltantes, valores constantes e possível mistura de segmentos antes de interpretar a matriz. Se uma figura surpreender, compare N, mínimo, máximo e quantis com cálculos apropriados no Spark, em vez de alterar apenas a paleta até a figura parecer convincente. Os dois helpers resolvidos preservam o cálculo das rotas legadas; o tema só entra no layout e nas cores declaradas.

Curvas de avaliação pertencem a um notebook de modelo de classificação binária, não a qualquer EDA. [`curves_plotly`](../../hub_snippets/ml/curves_plotly/README.md) oferece ROC, Precision–Recall, lift e KS, cada uma com uma pergunta distinta. Suas rotas `_resolvido` recebem arrays locais unidimensionais de rótulos 0/1 e probabilidades finitas em `[0,1]`; a amostra precisa conter **ambas as classes 0 e 1** para que a avaliação faça sentido. Elas não fazem cálculo Spark distribuído nem escolhem threshold de negócio. `n` muda somente o texto no rodapé. O próximo bloco é complementar e independente dos oito registros: seus quatro casos inventados servem apenas para mostrar a API de curvas, sem participar dos KPI, da tabela ou da matriz:

```python
import numpy as np
from hub_snippets.ml.curves_plotly import plot_pr_curve_resolvido

y_true = np.array([0, 1, 0, 1])
y_prob = np.array([0.10, 0.80, 0.40, 0.70])
curva_pr = plot_pr_curve_resolvido(y_true, y_prob, tema, n=4)
curva_pr.show()
```

A figura ilustra precisão e recall em quatro casos inventados, com dois rótulos de cada classe; quatro observações não sustentam um parecer sobre modelo real. A paleta temática dessa família é `palette.curves_legacy`, separada da paleta categórica geral. Um resultado de ROC, PR, lift ou KS não substitui calibração, análise de impacto, escolha do threshold e validação de negócio. Se o notebook não avalia classificação binária, omita as curvas do roteiro e do índice. O usuário não ganha clareza com uma figura tecnicamente válida, porém sem relação com sua pergunta.

Na adaptação a dados reais, preserve a fronteira entre número e texto. `fmt_int(1000)` ajuda a exibir `1.000`, mas essa string não deve voltar à coluna Spark como se ainda fosse uma contagem numérica. `fmt_pct` recebe uma razão por padrão; uma taxa já multiplicada por cem precisa declarar outra escala. A tabela pandas mostra o negativo realçado e a grade usa as medidas `saldo` e `tempo_meses` da mesma fonte, mas cada camada tem um papel: uma explica linhas específicas, outra resume a distribuição. Se o total da amostra não corresponde ao total da população, indique ambos com nomes diferentes. O [detalhe dos formatadores](MT-parte-ii.md#mt-mod-mt06) e o [mapa de consumidores visuais](MT-parte-vi.md#mt-mod-mt24) ajudam a verificar onde há transformação de dados e onde há apenas apresentação.

<a id="mu15-4"></a>
#### MU15.4 — Revisar, compartilhar e exportar com o alcance correto

Antes de compartilhar, percorra o notebook do começo ao fim como leitor novo. O título e o índice correspondem às seções presentes? A imagem de cabeçalho abre a partir daquele caminho? HTML e CSS continuam legíveis na largura real? Uma cor de badge tem texto equivalente? Aqui o cartão deve mostrar oito registros, seis resolvidos e `75,0%`; a tabela deve ter oito linhas, das quais seis com `resolvido=True`, e um único `-5` em `variacao`. N da distribuição é amostra coletada; neste exemplo coincide com oito, enquanto N de uma curva complementar, quando fornecido, é só texto declarado. A matriz mostra associação no recorte após nulos, não uma relação causal. Se uma unidade é porcentagem, diferencie fração `0,75`, percentual `75%` e diferença em pontos percentuais; uma string formatada não resolve confusão de denominador.

Inspecione também em uma largura menor. Cabeçalhos, legendas, rodapés e grades podem colidir mesmo que o Python tenha devolvido objetos válidos. Preserve títulos e explicações em Markdown comum para que o conteúdo essencial não dependa apenas de HTML ou pixels de um PNG. Para gráficos, escreva uma frase que interprete o padrão e outra que registre limite do dado; para a tabela, diga o que significa um valor negativo antes de destacá-lo. Revise rótulos, alt, contraste, ordem de leitura e cores de estados com o público de destino. Uma saída que passou por testes locais de construção não equivale a renderização homologada no Databricks ou em todos os browsers.

Exportar depende do objeto e do formato documentado. `display_styled_resolvido`, cabeçalhos, cartões e badges devolvem HTML, que pode ser mostrado numa superfície compatível; não produzem planilha ou PDF. `gerar_indice_eda(..., markdown=True)` devolve texto Markdown. Uma figura Plotly pode ser serializada localmente para HTML quando essa rota é suportada; o README de `curves_plotly` documenta essa possibilidade e explicita que PNG Plotly, PDF e PPTX não foram homologados para a V07. Não trate `export_theme`, que devolve JSON de configuração em memória, como exportação do relatório. Antes de gravar qualquer arquivo, escolha uma pasta autorizada e confirme se os dados contidos na figura podem ser compartilhados; a figura de distribuição contém os valores coletados no driver, não apenas barras anônimas.

Uma conclusão fiel a este exemplo diria: “Nos oito registros sintéticos, seis foram marcados como resolvidos (75%); o saldo varia de 1 a 8, o tempo de 2 a 16 meses, e os dois têm correlação de Pearson +1 por construção. O primeiro registro tem variação −5, realçada na tabela. Esses números ensinam a conferir a continuidade entre indicador, linha e figura; não descrevem clientes reais nem demonstram causa.” Essa frase não usa a curva PR complementar como evidência do mesmo conjunto. O notebook com texto e chamadas, a evidência dos cálculos e a evidência visual no destino são três entregáveis distintos: a receita está aqui; os dois últimos dependem de conferir o runtime e a superfície reais. Cada função `_resolvido` recebe explicitamente o mesmo `tema` de contexto notebook, cujo contrato está no [manual técnico de tema](MT-parte-vi.md#mt-mod-mt23).

Faça uma revisão de conteúdo em pares, quando o material justificar: peça a outra pessoa que localize a definição de uma linha, a fonte da taxa, a quantidade de registros efetivamente mostrados na distribuição e a diferença entre “fortemente associado” e “causado por”. Não sugira que o revisor aceite uma figura porque a cor parece profissional. Se não conseguir reconstruir um valor do cartão a partir da tabela ou da etapa de cálculo, acrescente o elo antes de apresentar a entrega. Mantenha os valores originais para auditoria; não use HTML gerado nem string brasileira como única cópia do resultado numérico.

Ao transportar a saída, registre o que foi de fato conferido. “HTML gerado” significa que o helper devolveu texto; “figura construída” significa que Plotly montou um objeto; “figura vista no notebook” exige renderização na sessão; “arquivo exportado” exige escrita e leitura desse arquivo. Esses estados não são equivalentes. Um HTML Plotly salvo localmente pode incluir dados usados pelos traces; revise-os e controle o destino antes de compartilhá-lo. Se o notebook for versionado, decida explicitamente se outputs e imagens devem acompanhá-lo, conforme a política do projeto, para não publicar por acidente uma amostra coletada. A presença de um cabeçalho bonito não reduz a responsabilidade por dados, acesso e interpretação.


<!-- editorial:exclude:start -->
[Anterior: MU14](#mu14) · [Próximo: MU16](#mu16) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT24](MT-parte-vi.md#mt24)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu16"></a>
<a id="mu16"></a>
### MU16 — Usar cabeçalhos e figuras dos Visual Assets

Os Visual Assets são imagens editoriais prontas para explicar o Hub. O usuário normalmente escolhe um PNG, aponta o documento para o arquivo compartilhado e mantém a explicação em texto. Este capítulo cobre essa tarefa em README e notebook. O [pacote visual](../../hub_readmes_visual_assets/README.md) é conteúdo próprio do Hub; a presença de uma imagem no repositório não a instala no workspace nem faz a Genie Code extrair regras dos seus pixels. Para entender a produção dos arquivos, consulte [MT25](MT-parte-vi.md#mt-mod-mt25) e [MT26](MT-parte-vi.md#mt-mod-mt26).

<a id="mu16-1"></a>
#### MU16.1 — Escolher CRM ou Squad e uma figura pela finalidade

Comece pela função da imagem. Um **cabeçalho** identifica o material; uma **figura** esclarece uma relação, sequência ou decisão. Os cabeçalhos aprovados são duas faixas PNG de 1920 × 480 pixels. Para um guia ou notebook geral, use `headers/png/cabecalho_crm.png`, com a identificação “CRM — Missão Modelos Analíticos CRM”. Para um notebook específico da Squad, use `headers/png/cabecalho_squad.png`, que traz “Squad Modelos Analíticos e Preditivos”. Escolha um por documento; empilhar os dois cria duas identidades concorrentes. O [guia dos cabeçalhos](../../hub_readmes_visual_assets/headers/README.md) mostra os arquivos e o texto exato. Eles são identidade editorial do projeto, não logotipos ou recursos nativos da Databricks. A arte de conexões não representa permissões, execução de código nem disponibilidade de serviços.

Para uma figura, escreva primeiro a pergunta que o leitor precisa responder. “Como fonte, workspace, contexto e notebook se relacionam?” aponta para `raiz/02_arquitetura_ecossistema.png`; “qual a diferença entre medir um problema e impedir uma ação?” aponta para `scripts/04_diagnostico_vs_enforcement.png`; “como descobrir uma skill apropriada?” aponta para `skills/01_descoberta_e_selecao.png`. Essas imagens não substituem o procedimento: a primeira não prova que algo foi publicado; a segunda não transforma todo diagnóstico em bloqueio; a terceira não autoriza inventar um limiar de seleção de skill. Leia a pergunta, o limite e o dono indicados no [`manifest.yaml`](../../hub_readmes_visual_assets/manifest.yaml) e abra o README ao qual a figura pertence antes de reutilizá-la.

O pacote ativo lista 21 figuras em seis famílias: raiz, assistant, snippets, scripts, skills e prompts. Uma família indica o assunto do README proprietário, não uma coleção decorativa para preencher páginas. Se o seu documento fala de reutilização de snippet, procure na família `snippets`; se fala de prompts, procure em `prompts`. O [índice textual das figuras](../../hub_readmes_visual_assets/CONTEUDO_FIGURAS.md) permite percorrer as perguntas sem abrir vinte e uma imagens. Se nenhuma figura responde à pergunta, texto simples ou um esquema novo submetido à revisão é melhor que uma imagem inadequada. Escolher pela aparência isolada pode transmitir uma relação diferente da que o texto afirma.

Antes de inserir, confira se o documento contém uma frase que apresenta a pergunta e outra que interpreta a resposta. Num guia para iniciantes, “a fonte versionada é publicada no workspace, enquanto a execução do helper depende de uma chamada no notebook” prepara a leitura da figura de arquitetura. No cabeçalho, mantenha título, público e finalidade em Markdown normal logo abaixo da imagem. Markdown é a marcação de texto com títulos e links; o PNG apenas acrescenta identidade ou síntese visual. Essa separação ajuda quando a imagem não carrega e quando alguém lê o documento por busca ou tecnologia assistiva.

<a id="mu16-2"></a>
#### MU16.2 — Inserir o PNG a partir do documento que o usa

Um caminho de imagem em Markdown tem a forma `![texto alternativo](caminho/arquivo.png)`. O caminho **relativo** é calculado a partir da pasta do documento consumidor. Os segmentos `..` sobem um nível; cada barra seguinte desce a uma pasta. Não comece a contar da pasta do pacote visual se o README que receberá a imagem está em outra pasta. O arquivo canônico permanece em `ambiente_databricks/.assistant/hub_readmes_visual_assets/`; referenciá-lo evita cópias divergentes em cada notebook. O PNG é o arquivo de leitura; `sources/*.svg`, manifesto e registros de qualidade servem à autoria e conferência. Inserir um PNG não importa um módulo Python, não inicia Spark e não executa uma skill.

Considere o `README.md` na raiz deste repositório. Da raiz, o cabeçalho CRM fica dentro de `ambiente_databricks/.assistant/`. A célula ou linha Markdown copiável é:

```markdown
![CRM — Missão Modelos Analíticos CRM](ambiente_databricks/.assistant/hub_readmes_visual_assets/headers/png/cabecalho_crm.png)

# Guia geral do Hub
```

Já em `ambiente_databricks/.assistant/README.md`, o ponto de partida está **dentro** de `.assistant`; o prefixo `ambiente_databricks/.assistant/` desaparece. Uma figura de arquitetura nesse mesmo arquivo pode ser citada assim:

```markdown
![Corte entre fonte versionada, workspace, contexto, notebook e runtime](hub_readmes_visual_assets/readmes/raiz/png/02_arquitetura_ecossistema.png)

A fonte é publicada no workspace; o notebook só executa código reutilizável quando há uma chamada explícita.
```

Se o consumidor for `ambiente_databricks/.assistant/hub_snippets/README.md`, suba uma pasta antes de entrar nos assets. O exemplo abaixo aponta para um arquivo da família `snippets` que já existe no pacote:

```markdown
![Pasta de snippet com fachada, implementação e exemplo didático](../hub_readmes_visual_assets/readmes/snippets/png/01_anatomia_pasta.png)

O README da pasta apresenta a API; o arquivo Python implementa a função e o exemplo mostra a chamada.
```

Observe a diferença entre os três prefixos: `ambiente_databricks/.assistant/`, `hub_readmes_visual_assets/` e `../hub_readmes_visual_assets/`. Nenhum deles é “o caminho universal da figura”; cada um está correto para o documento nomeado. Se você mover o README de lugar, recalcule os `..` e teste a referência. O mesmo vale para letras maiúsculas e minúsculas, espaços e extensão `.png`: um caminho que parece funcionar num sistema tolerante pode falhar no destino. Não copie uma imagem para contornar um erro de caminho sem verificar onde o documento será lido.

Veja um erro concreto. Em `ambiente_databricks/.assistant/hub_snippets/README.md`, escrever `![Pasta de snippet](hub_readmes_visual_assets/readmes/snippets/png/01_anatomia_pasta.png)` procuraria uma pasta `hub_readmes_visual_assets` **dentro de** `hub_snippets`, onde ela não existe. O endereço correto começa com `../`, sobe à pasta `.assistant` e só então entra no pacote. Para conferir sem adivinhar, localize no explorador de arquivos o README, suba à pasta pai uma vez e percorra o restante do caminho. Se o caminho terminar num diretório, não num arquivo `.png`, faltou parte do nome. Se um link `[abrir imagem](...)` funcionar, isso ainda não significa que a imagem apareceu embutida: o prefixo `!` é o que instrui o Markdown a renderizá-la no corpo do documento.

Em um notebook com célula Markdown, a sintaxe da imagem continua sendo Markdown. Se o notebook estiver salvo na própria pasta `headers/`, o [exemplo oficial do pacote](../../hub_readmes_visual_assets/headers/README.md) usa `%md` e `./png/cabecalho_squad.png`:

```markdown
%md
![Squad Modelos Analíticos e Preditivos](./png/cabecalho_squad.png)

# Análise da Squad
```

Se o notebook estiver em outra pasta do workspace, ajuste o endereço desde **essa** pasta e confirme que a árvore de assets foi distribuída junto com ele. Um caminho local do repositório não vira automaticamente um caminho válido no workspace. O suporte documentado para imagens de workspace aceita caminhos relativos ou absolutos em células Markdown, mas o modo exato de distribuição do seu projeto precisa ser conferido no destino autorizado. Use o README e a célula como exemplos de localização, não como prova de que qualquer instalação já ocorreu. Também não use prefixo de link entre notebooks, `%run` ou `displayHTML` para mostrar esse arquivo: eles resolvem tarefas diferentes.

Uma forma prática de revisar é ler o caminho da esquerda para a direita. Partindo da pasta do arquivo consumidor, aplique cada `..`, entre nas pastas seguintes e confirme a existência do nome final. Em seguida, abra o documento em sua superfície real e observe se o PNG aparece na largura prevista. Esse segundo passo detecta problemas que a simples presença do arquivo na fonte não detecta, como uma publicação que deixou a pasta de imagens de fora. Se o notebook será compartilhado, peça ao responsável pela publicação que confirme a árvore entregue, mantendo uma única localização canônica para as imagens.

O caminho também não deve ser confundido com a referência editorial ao conteúdo. Uma figura pode estar bem localizada e ainda aparecer no capítulo errado. O manifesto fornece o `owner_readme` e uma âncora do trecho que dá contexto; siga essa indicação para entender o lugar original da imagem. Ao levar a figura a outro documento, acrescente uma frase própria que explique por que ela serve à nova pergunta, além de preservar o limite do contrato. Assim o leitor não precisa adivinhar se a seta representa ordem obrigatória, opção ou simples relação entre componentes.

<a id="mu16-3"></a>
#### MU16.3 — Texto alternativo, legenda e conferência de leitura

O texto entre `![` e `]` é o **alt**, ou texto alternativo. Ele comunica a função da imagem quando os pixels não são vistos, por exemplo por falha de carregamento ou por leitor de tela. Um nome de arquivo, como `02_arquitetura_ecossistema.png`, pouco informa; uma frase como “Corte entre fonte versionada, workspace, contexto, notebook e runtime” já apresenta a relação principal. O alt não precisa transcrever cada rótulo da figura. A **legenda** ou o parágrafo próximo explica a mensagem e, quando necessário, o limite: “a publicação leva arquivos ao workspace; uma chamada explícita no notebook inicia o uso do helper”. Alt e legenda têm papéis complementares. A figura pode ajudar a enxergar o fluxo, mas a regra operável precisa permanecer no texto.

Para o cabeçalho, decida se a identidade já está escrita imediatamente abaixo. Se ela for informação nova, dê alt descritivo, como `![CRM — Missão Modelos Analíticos CRM](...)`. Se o mesmo nome estiver repetido ao lado como título e o banner servir só de decoração, `![](...)` pode evitar leitura duplicada. Não aplique alt vazio a uma figura que explica uma sequência sem equivalente textual. Para uma imagem de diagnóstico e enforcement, por exemplo, escreva no parágrafo o que é apenas medido e o que de fato bloqueia, com o gatilho e o alcance indicados pelo README proprietário. Uma frase “veja a figura” deixa o leitor sem instrução quando a imagem não aparece.

O [`CONTEUDO_FIGURAS.md`](../../hub_readmes_visual_assets/CONTEUDO_FIGURAS.md) é uma ajuda concreta: para cada figura, traz a pergunta, o alt, os rótulos e a síntese textual. Ao preparar sua página, compare essa síntese com o seu parágrafo. Se a figura disser “contexto explícito” e o texto afirmar “prompt carregado automaticamente”, há conflito que precisa ser corrigido antes do compartilhamento. O índice textual não substitui a explicação do README; consulte o documento proprietário para critérios, sequência e exemplos copiáveis. A Genie Code pode receber contexto de texto, mas não conte com leitura de pixels para descobrir regras ou parâmetros do Hub.

Confira a leitura em quatro passagens. Primeiro, leia o documento sem olhar a imagem: pergunta, instrução e conclusão continuam compreensíveis? Segundo, confira se o alt identifica a finalidade da imagem sem repetir um parágrafo inteiro. Terceiro, abra o PNG na superfície que o usuário realmente usará e examine se títulos, legendas internas e setas continuam legíveis na largura disponível. Quarto, compare a interpretação escrita com os rótulos da figura, inclusive direção de flechas, fronteiras e cores. Cor sozinha não deve carregar “permitido”, “bloqueado” ou “revisar”; acrescente palavras. Uma imagem visualmente limpa ainda pode induzir erro se uma seta ou uma legenda for tratada como uma autorização que não existe.

Os cabeçalhos foram compostos como faixas 1920 × 480 e o guia registra uma composição avaliada com referência de 720 pixels de largura e menor texto calculado em 18 pixels; isso não garante legibilidade ou acessibilidade em toda página que o reutiliza. Uma página pode reduzir demais a imagem ou cortá-la com CSS próprio. CSS é a camada de estilo que controla aparência e dimensão; se o destino a aplica, observe o resultado em largura estreita e larga. Para diagramas, compare a visualização com o texto equivalente, especialmente se a página dimensiona a figura automaticamente. Um alt correto não compensa rótulos minúsculos para quem vê, e uma imagem nítida não compensa um texto alternativo vazio para quem não a vê.

Os registros de manutenção [`tools/readme_visuals/qa/validation.json`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_visuals/qa/validation.json) e [`tools/readme_visuals/qa/headers/validation.json`](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_visuals/qa/headers/validation.json) registram verificações da respectiva rodada. Foram separados do pacote instalado; a ausência dessas pastas em `.assistant` não significa que falte um PNG de uso. Eles ajudam o mantenedor a rastrear integridade, mas não demonstram que seu README abriu no navegador, que o notebook está presente no workspace ou que uma pessoa com tecnologia assistiva conseguiu usá-lo. Ao entregar um documento, anote o que foi efetivamente conferido: caminho na fonte, arquivo incluído no destino e imagem vista no contexto de leitura. Se só verificou o primeiro, não declare os outros dois. O [manual técnico dos assets](MT-parte-vi.md#mt-mod-mt25) aprofunda a função dos arquivos e das verificações.

<a id="mu16-4"></a>
#### MU16.4 — Recuperar imagem ausente e encaminhar alterações

Se aparecer um ícone de imagem quebrada, comece pelo documento consumidor. Copie o caminho escrito entre parênteses, identifique a pasta desse documento e siga os segmentos até o PNG. Compare o nome completo, a extensão `.png` e a caixa das letras com o [diretório do pacote](../../hub_readmes_visual_assets/README.md). O erro mais comum nos exemplos deste capítulo é manter `hub_readmes_visual_assets/...` ao mover uma página de `.assistant/` para `hub_snippets/`: ali falta `../`. Corrigir o prefixo resolve a referência sem duplicar o arquivo. Faça a mesma conferência no destino, porque a fonte pode conter a imagem enquanto a distribuição deixou sua pasta de fora.

Se o caminho estiver certo, pergunte se o PNG foi entregue com o README ou notebook e se o visualizador aceita aquela referência. Em uma célula Markdown de notebook, teste o caminho relativo à localização do notebook; não copie o caminho de outro notebook sem recalculá-lo. Confira também se a imagem não foi apenas ocultada por estilo, recortada ou reduzida a um tamanho ilegível. Um problema de carregamento não pede gerar novamente o desenho de início. Diferencie “arquivo existe na fonte”, “arquivo chegou ao destino” e “arquivo foi visto na página”; cada verificação responde a uma causa diferente. Documente qual etapa falhou ao encaminhar o caso ao mantenedor.

Se a imagem carrega mas está conceitualmente errada ou desatualizada, descreva a pergunta que deveria responder, o trecho textual conflitante e a mudança proposta. Indique o README proprietário e, se houver, o identificador da figura no manifesto. Mudanças em copy, setas ou cores precisam passar pelo fluxo de autoria e revisão; cinco assinaturas e os dois cabeçalhos aprovados têm preservação por hash. Não edite o PNG final para “consertar” o desenho em um único README: isso criaria uma versão paralela sem atualizar os outros consumidores nem o texto equivalente. Uma variante temática V06 gerada localmente é candidata e não substitui o pacote ativo automaticamente.

Para escolher ou trocar uma imagem no documento do usuário, volte à pergunta: o arquivo correto existe, a explicação ao redor está presente e o caminho parte da pasta certa? Se sim, insira o PNG central, abra a página no destino e revise alt, legenda e legibilidade. Se a pergunta requer uma figura nova, entregue ao mantenedor uma proposta com finalidade e limites, sem atribuir publicação ou aprovação ao simples arquivo gerado. O [guia operacional de produção](MT-parte-vi.md#mt-mod-mt26) explica as etapas técnicas; este capítulo encerra no uso e na conferência da imagem que o leitor realmente receberá.


<!-- editorial:exclude:start -->
[Anterior: MU15](#mu15) · [Próximo: MU17](#mu17) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT25](MT-parte-vi.md#mt25)
<!-- editorial:exclude:end -->

<a id="mu-mod-mu17"></a>
<a id="mu17"></a>
### MU17 — Experimentar e entregar uma proposta visual

Uma proposta visual começa com a pergunta “onde esta aparência será vista?”. Um notebook, um painel de comparação, um Databricks App, um dashboard AI/BI e as figuras dos READMEs não recebem as mesmas propriedades de tema nem compartilham o mesmo caminho de entrega. Este capítulo ajuda a escolher a rota, experimentar com dados sintéticos e entregar uma revisão legível. **Salvar uma proposta não a aprova; gerar um arquivo não o publica.** As ferramentas citadas estão integradas no Git no alcance registrado, mas a instalação, o browser, o armazenamento, as permissões e a homologação do destino exigem evidências próprias.

<a id="mu17-1"></a>
#### MU17.1 — Decidir entre consumo, Lab, App, AI/BI e manutenção editorial

Se você quer mudar **uma figura ou componente de um notebook**, comece pelo [MU14](#mu-mod-mu14): carregue um `ResolvedTheme` de contexto `notebook` e passe-o explicitamente a uma função terminada em `_resolvido`. `ResolvedTheme` é a configuração completa e validada que os consumidores do Hub conseguem ler; `_resolvido` identifica a rota que recebe essa configuração. Essa escolha permite comparar uma apresentação sem criar proposta persistida. O [MU15](#mu-mod-mu15) mostra como manter indicadores, tabela e gráficos coerentes na mesma análise. O contrato do tema e o mapa de consumidores estão em [MT23](MT-parte-vi.md#mt-mod-mt23) e [MT24](MT-parte-vi.md#mt-mod-mt24): um token de cor não afeta automaticamente todo objeto que aparece no notebook.

Se a tarefa é **experimentar controles e comparar uma base com uma proposta**, escolha o Visual Lab. Ele é uma interface customizada em notebook, não um menu nativo da Databricks. Usa uma galeria sintética fixa para que diferenças de dados não sejam confundidas com diferenças visuais. A rota permite desfazer, exportar somente a configuração ou salvar uma sessão rastreável em pasta fornecida pelo mantenedor. O Lab não aprova, publica, migra notebooks nem altera dashboards. A necessidade de uma pasta de rascunhos controlada é prática: sem `save_root`, a prévia continua disponível, mas salvar e reabrir não ficam habilitados.

Se o responsável entregou um **Databricks App de autoria visual** já implantado e acesso ao usuário, o App oferece esse percurso sem exigir que ele edite Python. Ele reaproveita o Lab, mas a persistência de produção depende de identidade recebida pelo **proxy**, a camada do Databricks Apps que encaminha ao aplicativo a identidade da pessoa autenticada, e do recurso `theme_storage` ligado a um Unity Catalog Volume. “Volume” aqui é um local de armazenamento governado no ambiente, não o diretório temporário do notebook. Os arquivos do App no Git não demonstram que esses recursos foram configurados. Se o App não foi entregue, use a rota de notebook que esteja disponível ou peça ao responsável a preparação; não troque uma falha de identidade por modo local para simular produção.

Se o destino é um **dashboard AI/BI**, a ponte V11 ajuda a classificar o que o Hub consegue traduzir, aproximar ou deixar sem suporte. Ela recebe um tema `notebook` íntegro e produz uma projeção do Hub. Não existe `context="aibi"` habilitado no schema de temas do núcleo. O JSON de projeção não é um arquivo nativo para o botão *Import theme*. Um candidato nativo depende de um export real de dashboard em estado **draft**, isto é, rascunho ainda editável antes da publicação, no ambiente autorizado e de um mapeamento revisado para campos já existentes. Quem só tem permissão de editar um dashboard não ganha, por isso, permissão para alterar o tema do workspace inteiro ou publicar o dashboard.

Se a mudança é em **cabeçalhos ou diagramas dos READMEs**, use os PNGs aprovados pelo [MU16](#mu-mod-mu16) para consumo comum. Uma cor nova nessa frente pertence a uma variante editorial candidata V06, gerada fora do pacote ativo e revisada por quem mantém os assets. Ela não recolore automaticamente os cinco diagramas de assinatura congelada nem os dois cabeçalhos aprovados. O [MT25](MT-parte-vi.md#mt-mod-mt25) explica os arquivos e o [MT26](MT-parte-vi.md#mt-mod-mt26) explica a produção. Escolher essa rota quando a necessidade era apenas estilizar uma figura Plotly acrescentaria trabalho sem melhorar o notebook.

Antes de avançar, escreva em uma linha: “quero propor mudança em [superfície], comparar contra [base], com [mesmos dados] e entregar [configuração/sessão/candidato] a [responsável]”. Se não consegue preencher a superfície ou o responsável, faça primeiro uma prévia local, sem atribuir a ela estado aprovado. Isso também orienta quais evidências recolher: captura de uma tela pode ajudar a discutir aparência, enquanto um hash e uma sessão permitem rastrear exatamente quais bytes foram salvos. Nenhuma evidência isolada responde a todas as perguntas.

<a id="mu17-2"></a>
#### MU17.2 — Abrir o Visual Lab, ajustar, comparar e exportar JSON

Na cópia autorizada do Hub, abra a pasta `hub_snippets/visual/theme_lab/` e leia o [guia de primeiro uso](../../hub_snippets/visual/theme_lab/GUIA_PRIMEIRO_USO.md). O mantenedor deve entregar o pacote `.assistant` completo e as dependências permitidas pelo ambiente; copiar só `theme_lab.py` não basta. O exemplo `exemplo_theme_lab.py` serve de notebook de entrada. Primeiro confirme que a sessão Python consegue importar o Hub; o preparo de `HUB_ROOT` do [MU15](#mu-mod-mu15) mostra uma forma de localizar a pasta `.assistant`. Depois, se houver pasta regular de rascunhos já existente e autorizada, use o launcher. No bloco abaixo, substitua o placeholder pelo caminho entregue pelo mantenedor antes de executar:

```python
from pathlib import Path
from IPython.display import display
from hub_snippets.visual.theme_lab import build_theme_lab_launcher

PASTA_DE_RASCUNHOS = Path("/CAMINHO/AUTORIZADO/EXISTENTE")
if not PASTA_DE_RASCUNHOS.is_dir():
    raise RuntimeError("Peça ao mantenedor a pasta de rascunhos existente")

launcher = build_theme_lab_launcher(save_root=PASTA_DE_RASCUNHOS)
display(launcher.root)
```

Se a intenção é apenas comparar e nenhuma pasta foi entregue, use `build_theme_lab_launcher()` sem `save_root`; a experiência de prévia funciona, mas os botões de persistência e reabertura ficam indisponíveis. Não crie por conta própria uma pasta na fonte `.assistant` ou um destino compartilhado para “habilitar” salvamento. O caminho de sessão não concede permissão, não descobre controle de acesso e não publica um tema. No launcher, escolha **Ponto de partida** e clique **Abrir ponto de partida**. Referências empacotadas aparecem marcadas como “demonstração”; são úteis para aprender a interface, não prova de tema institucional aprovado.

Na área **Escolher e ajustar**, altere um campo habilitado, por exemplo **Cor principal**. Um valor hexadecimal tem `#` seguido de seis dígitos, como `#112233`. Clique **Aplicar na prévia**. A operação valida todos os campos habilitados em conjunto; se houver erro, a última proposta válida continua ativa. Campos desabilitados mostram por que aquela propriedade não tem consumidor na galeria, em vez de fingir que toda mudança produzirá efeito. “Restaurar este campo” muda o formulário; é preciso aplicar de novo para a proposta refletir o valor. “Desfazer” volta ao estado aplicado anterior. “Restaurar ponto de partida” volta à base original e pode pedir confirmação se descartar trabalho em memória.

Abra **Comparar** e percorra cabeçalho, cartão de indicador, barras, série temporal, mapa de calor e tabela. Base e proposta devem mostrar os mesmos dados sintéticos, nomes e ordem; diferenças permitidas nessa comparação são visuais. Um cartão mais legível não prova que a métrica real está correta. Registre onde o contraste, os rótulos, os negativos e os nulos ficaram melhores ou piores. A galeria completa usa o modo claro (*light*); não trate a prévia como homologação de modo escuro ou alto contraste. Se os controles aparecem mas as figuras não, o guia orienta o mantenedor a usar `compare_preview(draft)` para distinguir problema de frontend de problema da proposta, registrando runtime e navegador. Não instale JavaScript arbitrário para forçar a tela.

Faça uma revisão pequena antes de salvar. Suponha que a proposta troque a cor principal para `#112233`. Compare primeiro um elemento onde essa cor é consumida e anote a diferença vista; depois percorra a tabela e os gráficos que podem usar outros tokens. Se uma peça não mudou, verifique no mapa do consumidor se ela realmente lê `brand.primary`, em vez de declarar que a aplicação falhou. Se uma etiqueta perdeu contraste, registre o local, a cor de fundo e o texto afetado; corrigir só o hex sem olhar a combinação pode criar outra falha. Confirme que uma linha negativa, um valor nulo e a ordem das categorias continuam idênticos entre as duas colunas da comparação. Assim a revisão responde a uma pergunta verificável: o ajuste melhora a leitura pretendida sem alterar o conteúdo?

Para **exportar só a configuração**, use **Exportar JSON** ou `save_proposal()` no fluxo apropriado. JSON é o formato de pares de nomes e valores que preserva a proposta; ele não guarda necessariamente a base nem a sequência de mudanças. `export_theme` do núcleo também devolve bytes em memória, o que não é a mesma coisa que salvar num diretório. Se a intenção é continuar a autoria em outra sessão, escolha **Salvar sessão rastreável**. O Lab grava `base.json`, `proposal.json`, arquivos `history_000.json` e, por último, `session.json` com revisão e hashes. Um hash SHA-256 permite conferir se bytes mudaram desde o registro; não é assinatura de aprovação. O salvamento recusa nome já existente e campos editados mas ainda não aplicados. Um recibo de sucesso indica persistência local da sessão, não submissão. O guia e a implementação correntes usam o sublinhado mostrado aqui; registros anteriores com hífen devem ser interpretados como nomenclatura histórica.

Ao reabrir, escolha a sessão no campo **Reabrir** e clique **Reabrir sessão**. O Lab revalida base, proposta, histórico e hashes, preservando a base original; a proposta antiga não vira base nova por conveniência. Um `LAB_SESSION_HASH` indica divergência de bytes e exige inspeção, não alteração manual do hash. `LAB_SAVE_ROOT` aponta raiz de rascunhos inválida ou não acessível; `LAB_SESSION_MISSING` indica que a sessão escolhida não foi encontrada. `LAB_SAVE_EXISTS` ou `LAB_SESSION_EXISTS` pede outro nome. O guia anterior chama o campo de “Sessão salva” e menciona `LAB_SESSION_ROOT`, mas o código atual usa **Reabrir** e não emite esse último código. Se só `dbutils.widgets` estiver disponível, o fallback documentado cobre controles primários, mas exige reexecutar a aplicação e não oferece o catálogo de sessões com a mesma ergonomia. Um teste Python da lógica ainda não comprova o comportamento do frontend Databricks, teclado, leitor de tela ou facilidade de uso por iniciante.

Ao entregar a sessão a outra pessoa, informe qual base foi aberta, qual revisão foi salva e quais controles foram aplicados. Uma alteração digitada e não aplicada não pertence ao estado persistido. Peça ao revisor que reabra a sessão com o mesmo pacote e confira se a base permanece base e se a proposta reproduz a comparação. Se ele recebeu apenas o JSON avulso, explique que o histórico de tentativas não viaja com esse arquivo; não anuncie “sessão reaberta” sem `session.json` íntegro. O recibo e o hash rastreiam o conteúdo do arquivo, mas a aprovação estética e a instalação no destino continuam decisões separadas.

Para usar no notebook **a mesma proposta salva**, substitua `NOME_CONFIRMADO` pelo nome do recibo e recupere a sessão na pasta autorizada já definida acima. A função abaixo devolve o rascunho validado: `current` contém sua proposta, enquanto `base` conserva o ponto de partida original.

```python
from hub_snippets.visual.theme_lab import reopen_theme_lab_session

rascunho = reopen_theme_lab_session(PASTA_DE_RASCUNHOS, "NOME_CONFIRMADO")
referencia = rascunho.base
tema_proposto = rascunho.current
```

Continue com a figura e as duas chamadas de `aplicar_tema_resolvido` de [MU14.3](#mu14-3), usando essas variáveis. Nesse exemplo, substitua a linha que carrega a referência e o bloco que cria outra proposta (`to_dict`, alteração da cor e `resolve_theme`) pela recuperação acima. Conserve os mesmos dados, as cópias da figura e `fig.show()`. Assim você compara a base original com a proposta reaberta, sem recriar uma configuração diferente. A recuperação não ativa padrão global, publica ou homologa o tema; se houver erro de sessão, resolva-o antes da aplicação.

<a id="mu17-3"></a>
#### MU17.3 — App de autoria e ponte AI/BI: o que cada uma entrega

No App V10, o caminho para o usuário só começa **se** o responsável confirmou implantação, acesso, identidade pelo proxy e armazenamento `theme_storage` em Unity Catalog Volume. Abra então a interface entregue: escolha um ponto de partida na barra lateral, clique **Abrir novo rascunho**, ajuste controles e use **Aplicar e validar proposta**. A configuração inteira é validada antes de substituir a última proposta válida. Compare **Base** e **Proposta** sobre a mesma galeria sintética, inclusive negativos e nulos; o objetivo é julgar aparência, não medir desempenho analítico. O [guia do App](../../hub_padroes/identidade_visual/databricks_app/GUIA_PRIMEIRO_USO.md) descreve os nomes das telas e como retomar. Abrir outro rascunho descarta só mudanças ainda não salvas na sessão atual, não apaga uma sessão anterior persistida.

Para salvar no App, informe um nome simples e clique **Salvar sessão**. Confirme o recibo com nome, revisão, profundidade do histórico e prefixo do hash; sem confirmação, não presuma persistência. Uma sessão com mesmo nome não é sobrescrita. A área **Retomar** lista sessões do **namespace** da identidade atual: uma pasta de sessões separada para aquela pessoa, derivada de um hash, sem pôr seu identificador bruto no caminho. O namespace organiza as sessões oferecidas pelo App; o hash não cifra conteúdo nem substitui ACL do Volume ou impede acesso administrativo já autorizado. Ao reabrir, hashes são conferidos antes de reconstruir base, proposta e histórico; sessão parcial ou adulterada é recusada. Não há botões de aprovar, rejeitar, publicar, promover, ativar como padrão ou apagar histórico. Essa ausência é parte da fronteira `authoring_only`. `APP_IDENTITY_MISSING`, `APP_STORAGE_MISSING`, `APP_STORAGE_NOT_VOLUME` e `APP_STORAGE_UNAVAILABLE` pedem conferência do responsável; um erro `LAB_` vem da camada de sessão compartilhada com o Lab. Não envie token, não mude hash e não troque o Volume por `/tmp` para contornar uma falha.

Em AI/BI, a primeira saída do Hub é outra: uma **projeção auditável** de um `ResolvedTheme` de contexto `notebook`. A matriz V11 classifica 48 tokens em 3 `translated`, 23 `approximated` e 22 `unsupported`. “Translated” significa que há correspondência nativa suficientemente direta; “approximated” indica capacidade parecida cuja interpretação precisa ser revista; “unsupported” registra lacuna. Apenas três correspondências `translated` com estratégia `direct` podem receber **binding**, um mapeamento revisado de capacidades do Hub para campos existentes no JSON nativo. A projeção tem identificador `hub-aibi-theme-projection`, formato do Hub, e **não** é JSON nativo importável pelo Databricks. O [guia AI/BI](../../hub_padroes/identidade_visual/aibi/GUIA_PRIMEIRO_USO.md) separa essa preparação local da edição de um dashboard real.

As três correspondências diretas são concretas: `surface.card` para fundo de widget, `palette.categorical` para paleta categórica de visualização e `card.radius_px` para raio do canto do widget. Isso não significa que a ponte saiba onde estão esses campos em qualquer export nativo. `brand.primary` para cor de seleção é uma **aproximação**: nomes parecidos não tornam as semânticas idênticas. `brand.accent` permanece sem capacidade alvo segura na matriz. Ao ler uma projeção, procure a classe e a justificativa de cada token, não apenas um valor hexadecimal. A regra protege contra uma aparência parcialmente aplicada que seria anunciada como tema completo.

Se houver permissão para um dashboard **draft**, o percurso de candidato nativo começa no destino: abra *Settings → Theme → Export theme*, preserve o JSON original e registre seu SHA-256. Um mantenedor técnico revisa esse export e escreve um binding com JSON Pointers para campos que já existem nele. JSON Pointer é um endereço dentro de um documento JSON, como uma sequência de chaves; a ponte não adivinha o schema. `bind_native_template()` confere o hash exato do export, recusa caminho ausente e só substitui as três capacidades diretas permitidas. O arquivo produzido ainda é **candidato local** até ser testado com *Import theme* no próprio destino autorizado. Se a importação falhar, preserve o original, registre a diferença e revise binding/template; não force uma aproximação a passar como tradução.

Na revisão do dashboard, mantenha datasets, consultas, filtros, campos, agregações, unidades e ordenação idênticos. O fixture `dashboard_sintetico.json` é roteiro local para inspecionar KPI, série, barras, tabela, texto e filtros, não um arquivo Databricks importável. Compare o resultado em claro e escuro, observando paleta, texto, fundos, bordas, seleção, gradiente e mapeamentos locais de cor. Itens `approximated` exigem decisão explícita; `unsupported` continuam sem tradução. **Tema de workspace** e **tema de dashboard** são superfícies diferentes: o primeiro exige administrador, enquanto um dashboard existente recebe um snapshot quando ele é aplicado. Mudanças posteriores no tema do workspace não atualizam automaticamente esse dashboard. Importar um tema e publicar um dashboard também são ações separadas; a V11 não faz nenhuma das duas por você.

Há duas verificações que devem aparecer juntas no registro. A primeira é de **conteúdo**: confirme que uma barra ainda representa o mesmo campo, que o filtro seleciona a mesma população e que o KPI conserva numerador, denominador e unidade. A segunda é de **aparência**: observe o mesmo widget com a proposta e com o tema anterior, de preferência em dimensões e modos de visualização pertinentes ao uso. Uma cor específica por valor em *Color mappings* pertence ao dashboard, não se propaga automaticamente a todos os objetos pela paleta do Hub. Se um item da matriz era `approximated`, documente qual decisão manual foi tomada e por quem; se era `unsupported`, deixe a lacuna visível. Não atribua a um arquivo candidato o resultado de um teste que ainda depende do botão *Import theme* no workspace.

O estado importa ao descrever essas rotas. O índice vivo e a nota administrativa V14 de 06/10/2026 registram V00–V13 e V14 S0/S1 integradas no Git; S1 entrou pela PR #72 em 16/09/2026. Os rótulos de candidata no corpo histórico preservam o estágio pré-merge. S2–S8 não possuem início comprovado, e os slots operacionais seguem `BLOCKED` sem autoridade evidenciada. Há teste local e documentação para Lab, App e ponte AI/BI; isso não substitui instalação, frontend, identidade, Volume, importação nativa, acessibilidade ou aceite no ambiente corporativo. `A11-01` permanece `FAIL`: numa revisão real de um dashboard draft com dados sintéticos, dois pares de texto e fundo da formatação condicional `cellFormat` ficaram abaixo do contraste exigido de 4,5:1 para texto comum, apesar de a pessoa não ter percebido problema. O [registro da medição](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V12/TESTES.md) preserva esse achado na issue #57; `cellFormat` não é uma das três capacidades diretas da ponte V11. Os gates `V12-LAB-01`, `V12-APP-01`, `V12-AIBI-02` permanecem bloqueados por autorização na [situação V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md). A palavra “integrado” descreve o estado do código no Git, não autorização de operação. Quando um README da época ainda diz “candidata”, consulte também esse registro de estado posterior para não confundir data de autoria do guia com o alcance atual.

<a id="mu17-4"></a>
#### MU17.4 — Variante editorial, revisão, evidência e encaminhamento

Quando a proposta diz respeito a um diagrama ou cabeçalho usado em README, comece identificando o PNG ativo e o texto equivalente. O [MU16](#mu-mod-mu16) ensina a escolher pela pergunta e apontar para o arquivo central. Para mudar a aparência do pacote editorial, o mantenedor pode usar a rota V06: um `theme_id` canônico é resolvido pelo núcleo de temas, e o compositor grava uma **variante candidata** em `.artifacts/visual-v2/theme-variants/`, fora de `hub_readmes_visual_assets/`. `SOURCE_DATE_EPOCH` fixa a referência temporal da geração reproduzível do manifesto. O [guia técnico da rota](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/tools/readme_visuals/README.md) mostra os comandos, e o [MT26](MT-parte-vi.md#mt-mod-mt26) explica o mecanismo. O usuário que só precisa colocar uma figura no documento continua usando o PNG ativo, sem executar gerador.

Na comparação, peça ao mantenedor três coisas concretas: o identificador e a pergunta da figura, o PNG vigente com seu hash e o PNG candidato com seu hash. Veja ambos na largura em que o README é lido; confira rótulos, setas, contraste, legenda e texto alternativo. Pergunte se alguma mudança de cor alterou a leitura de estado ou procedência. Nos assets paramétricos, bytes idênticos ao ativo podem ser classificados como `parametric_equivalent`; bytes alterados pedem `variant_review_required` e nova revisão antes de promoção. Os cinco diagramas de assinatura aprovada são entradas congeladas, copiadas sem reinterpretar o desenho; a rota não os recolore. Os dois cabeçalhos canônicos também permanecem preservados. Um manifesto candidato registra classificação e política da geração, não a aprovação de uma pessoa nem publicação no workspace.

Uma entrega útil de proposta visual reúne origem, alteração e alcance. Anote a base usada, contexto e modo do tema, versão/fingerprint, tokens alterados e componentes realmente comparados; mantenha os mesmos dados sintéticos entre Base e Proposta. Se for Lab, inclua recibo e hash da sessão ou JSON avulso, dizendo qual dos dois foi salvo. Se for App, inclua apenas recibo e códigos de erro necessários, nunca identidade bruta ou token. Se for AI/BI, inclua projeção, classificação das capacidades, export nativo original com SHA-256 e binding revisado; o candidato resultante não prova importação. Se for asset editorial, inclua ID da figura, hashes, escala de inspeção e texto equivalente atualizado. Esses registros permitem a outra pessoa reconstruir o que foi proposto sem assumir que uma captura de tela conta toda a história.

Ao encaminhar, use palavras de estado precisas: “proposta salva no Lab”, “sessão reaberta”, “candidato nativo gerado”, “PNG candidato comparado” ou “imagem vista no notebook”. Cada uma sustenta uma afirmação diferente. Não escreva “aprovado” porque a configuração passou no schema, “publicado” porque um arquivo existe em `.artifacts`, nem “homologado” porque a galeria sintética abriu localmente. O [estado V14](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/983c9936f139402a0130f290653ae713d65a3ac7/docs/sprints/sistema_temas/V14/README.md) mantém slots de autoridade operacional bloqueados quando falta evidência versionada; um owner técnico documentado não vira automaticamente aprovador, publicador ou autoridade de go-live. Entregue a proposta e as limitações ao responsável real pelo destino, segundo a política do ambiente.

Se a revisão apontar problema, volte à fonte da proposta, não ajuste o registro de evidência para escondê-lo. Corrija um campo no Lab e salve outra sessão; no App, crie revisão ou sessão conforme a interface; em AI/BI, reexporte o template se o formato nativo mudou e revise os JSON Pointers; em assets, encaminhe correção ao compositor e confira o novo PNG. Depois repita apenas as verificações afetadas e registre o que foi feito de fato. O ponto de chegada deste capítulo é uma proposta compreensível, rastreável e limitada ao seu escopo. Decisão de aprovação, instalação, publicação e aceite operacional pertencem aos fluxos e autoridades próprios.

<!-- editorial:exclude:start -->
**Consulta de plataforma — 07/10/2026:** [temas de workspace](https://docs.databricks.com/aws/en/ai-bi/admin/themes) e [configurações de dashboard](https://docs.databricks.com/aws/en/dashboards/manage/settings). A documentação sustenta administração, snapshot, draft e import/export; não atesta a interface ou as permissões deste leitor.
<!-- editorial:exclude:end -->


<!-- editorial:exclude:start -->
[Anterior: MU16](#mu16) · [Próximo: MU18](MU-parte-vi.md#mu18) · [Sumário](MU-indice.md#sumario-mu) · [Guia por pergunta](MU-indice.md#perguntas-mu) · [Trilhas](MU-indice.md#trilhas-mu) · [MT26](MT-parte-vi.md#mt26)
<!-- editorial:exclude:end -->
