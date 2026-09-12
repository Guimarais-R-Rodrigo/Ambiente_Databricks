# `theme_plotly` — padronize a figura sem esconder seus efeitos

<!-- readme-objeto: 1.0.0 -->

> Aplique o tema do Hub a gráficos Plotly e declare contexto no rodapé, distinguindo alterações na figura de padrões da sessão.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Funções legadas de tema Plotly mais um adaptador V03 opt-in para `ResolvedTheme`. |
| Para que serve? | Uniformizar aparência e acrescentar contexto declarado. |
| Use quando... | O gráfico já está correto e precisa de apresentação consistente. |
| Evite quando... | Você espera corrigir cálculo, inferir origem ou reestilizar todo o Hub. |
| Precisa de... | Plotly e figuras válidas; nenhum DataFrame obrigatório. |
| Entrega... | Configuração, figura modificada ou registro de tema na sessão. |

**Acesso direto:** [exemplo](exemplo_theme_plotly.py) · [implementação](theme_plotly.py) · [API pública](__init__.py). Leia os requisitos e os efeitos na seção 9 antes de executar o notebook inteiro.

## 1. O que é?

Um tema reúne convenções de apresentação: fontes, cores, dimensões, margens e posição da legenda. Plotly é a biblioteca que constrói as figuras; o tema do Hub é uma escolha local aplicada sobre ela.

As três operações legadas continuam iguais: `get_tema_eda` consulta a configuração histórica, `aplicar_tema` modifica uma figura e `registrar_template_plotly` registra o padrão `caixa` na sessão. A V03 acrescenta, sem substituir essas chamadas, `get_tema_plotly`, `aplicar_tema_resolvido` e `registrar_template_plotly_resolvido` para consumir explicitamente um `ResolvedTheme` validado pela V02. Plotly continua sendo apenas um consumidor; HTML e outros componentes têm sprints próprias.

## 2. Que problema este recurso resolve?

“Como apresentar diferentes gráficos com a mesma linguagem visual e com contexto suficiente para interpretá-los?” A função pode acrescentar fonte, subtítulo e N no rodapé.

Esses campos são declarações do autor. O helper não conta dados nem confere a fonte. Informar um N errado produz um rodapé errado, ainda que visualmente padronizado. O tema não verifica o indicador que está sendo mostrado.

## 3. Quando faz sentido usar?

Use em figuras já construídas, quando faz sentido adotar as convenções do Hub. É uma forma de reduzir configurações repetidas sem repetir o cálculo dos dados.

O registro de template pode ajudar em uma sequência de gráficos novos na mesma sessão Python. A aplicação explícita por figura é preferível quando você quer controlar exatamente quais gráficos serão afetados ou precisa preservar outro padrão para o restante do notebook.

## 4. Quando não usar?

Não use para remediar eixo enganoso, agregação incorreta ou ausência de unidades: aparência consistente não corrige essas decisões. Tampouco use `registrar_template_plotly` esperando modificar figuras já criadas ou salvar uma preferência permanente no workspace.

Evite aplicar o tema depois de dimensões customizadas quando precisa preservá-las: a aplicação redefine as chaves compartilhadas. A ordem recomendada é tema primeiro e ajustes específicos depois. Para figuras fora do Databricks, a função não é proibida, mas fonte, tamanho e renderer precisam de conferência no destino.

## 5. Como funciona, intuitivamente?

`get_tema_eda` devolve um dicionário com o template base `plotly_white`, fontes, paleta categórica, dimensões de 900 por 450 e outras opções. Ele referencia constantes do Hub, inclusive `CINZA_ESCURO`, em vez de calcular dados.

`aplicar_tema` chama `fig.update_layout` e, quando há informações, adiciona uma anotação de rodapé. **Modifica a figura recebida e devolve o mesmo objeto.**

`registrar_template_plotly` insere a configuração legada no registro `plotly.io.templates` com o nome `caixa` e altera `pio.templates.default`. Esse efeito vale para o processo Python atual. Importar o módulo, por si só, não chama essa função.

Na rota V03, `get_tema_plotly(theme)` traduz somente os tokens notebook atribuídos ao Plotly e não altera a sessão. `aplicar_tema_resolvido` aplica essa tradução explicitamente a uma figura. `registrar_template_plotly_resolvido` usa um nome `hub-*`, não ativa o template por padrão e só muda `pio.templates.default` com `ativar=True`. A configuração é revalidada pelo núcleo antes de ser consumida.

## 6. Exemplo de situação

Você preparou um gráfico sintético com três meses e seus volumes. Quer que o leitor saiba que há três pontos mensais e que a fonte é uma simulação, não três clientes.

Aplique o tema com `n=3`, escreva “pontos mensais” no subtítulo e declare a fonte sintética. A unidade observacional fica explícita. Se você estivesse mostrando médias de milhares de clientes em três grupos, precisaria decidir e explicar qual N pretende declarar; a função não faz essa escolha.

## 7. O que você precisa antes de usar?

Tenha Plotly instalado e o caminho de importação preparado. `aplicar_tema` recebe uma `go.Figure`, não uma tabela de dados. Fonte e subtítulo devem ser textos controlados e apropriados ao compartilhamento.

Defina previamente o significado de N: linhas, entidades, observações válidas ou pontos agregados. Use um inteiro não negativo para uma contagem; a implementação formata o valor, mas não valida essa interpretação.

O notebook de demonstração usa NumPy para gerar a série e Spark para localizar a biblioteca do usuário. Essas são dependências da demonstração, não da aplicação do tema a uma figura pronta.

## 8. O que este recurso entrega?

`get_tema_eda()` retorna um dicionário. `aplicar_tema(...)` retorna a própria figura modificada, preservando os dados dos traces. `registrar_template_plotly()` retorna `None` e deixa um efeito na sessão.

O rodapé é uma anotação textual com as partes fornecidas, não metadado verificado. Chamadas repetidas com rodapé adicionam novas anotações, em vez de substituir automaticamente a anterior. Sem argumentos de rodapé, a função não acrescenta uma anotação nova.

## 9. Como usar este recurso no Hub?

Depois da preparação descrita no [guia da coleção](../../README.md), use dados sintéticos locais. Este bloco não registra template global nem salva arquivos.

```python
import plotly.graph_objects as go
from hub_snippets.visual.theme_plotly import aplicar_tema

fig = go.Figure(go.Bar(x=["jan", "fev", "mar"], y=[10, 12, 9]))
fig.update_layout(title="Volume mensal — exemplo")
resultado = aplicar_tema(fig, subtitulo="Três pontos mensais", fonte="dados sintéticos", n=3)
assert resultado is fig
assert "N = 3" in fig.layout.annotations[-1].text
fig.update_layout(width=720)  # ajuste específico depois do tema
assert fig.layout.width == 720
```

### V03: aplicar uma proposta resolvida sem mudar o legado

A referência empacotada abaixo é **fixture de teste**, não tema operacional aprovado. Ela serve para demonstrar o fluxo; uma proposta real deve seguir o processo de governança do Sistema de Temas.

```python
from hub_snippets.visual.tema import load_reference_theme, resolve_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

base = load_reference_theme("notebook")
proposta = base.to_dict()
proposta["theme_id"] = "hub-exemplo-proposta"
proposta["display_name"] = "Exemplo de proposta"
proposta["description"] = "Exemplo sintético para demonstrar a aplicação Plotly opt-in."
proposta["tokens"]["brand.primary"] = "#112233"

tema_resolvido = resolve_theme(proposta, expected_context="notebook")
fig = go.Figure(go.Bar(x=["A", "B"], y=[10, 12]))
aplicar_tema_resolvido(fig, tema_resolvido, fonte="dados sintéticos", n=2)
fig.show()
```

O fluxo não grava o tema, não o aprova e não altera outros gráficos da sessão. A fixture `legado_notebook` produz exatamente o mesmo layout de `get_tema_eda()`, o que é testado como regressão da migração.

Use `fig.show()` no notebook para visualizar. O [exemplo completo](exemplo_theme_plotly.py) gera uma série local e mostra figuras; não grava tabelas. Seu rótulo de fonte menciona fixtures, mas os dados daquela célula são gerados por NumPy: trate o rótulo como ilustração, não como procedência comprovada. O exemplo importa a função de registro, mas não a chama.

## 10. Decisões e configurações que mais importam

Escolha conscientemente entre aplicação explícita e registro global. Para propostas V03, prefira `aplicar_tema_resolvido`; `registrar_template_plotly_resolvido` exige namespace `hub-*`, recusa colisão por padrão e só ativa o template com `ativar=True`. Para recuperar o padrão da sessão depois de uma experiência de registro, guarde o valor anterior de `pio.templates.default` e restaure-o; não suponha que uma nova célula comece uma sessão vazia.

Aplique mudanças de largura, altura, margem ou fonte específicas **depois** de `aplicar_tema`. Uma nova aplicação do tema redefine essas opções. `n` é formatado sem casas decimais, com separador brasileiro de milhares, mas o helper não exige inteiro. `subtitulo` fica no rodapé, não imediatamente abaixo do título.

## 11. Limitações, riscos e armadilhas

Reaplicar o rodapé pode duplicar informações e causar sobreposição com a legenda. A largura e a altura fixas podem comprimir grades extensas e telas pequenas. Uma figura construída sem erro ainda requer inspeção visual.

A paleta categórica não substitui escalas explicitamente definidas em heatmaps nem cores já fixadas nos traces. O registro global afeta outras figuras que usem o padrão da mesma sessão, e não outras sessões independentes. A V03 aplica somente `mode=light`: `dark` e `high_contrast` são válidos no contrato, mas falham fechados no adaptador Plotly até existirem tokens de superfície suficientes para não inventar backgrounds implícitos.

O dicionário de configuração contém uma referência à lista `PALETA_CATEGORICA`; não altere essa lista por meio do retorno como se fosse uma cópia isolada. Textos de fonte/subtítulo também não passam por uma política geral de escape. Use conteúdo controlado e não exponha caminhos internos ou dados sensíveis no rodapé.

## 12. Quais são as alternativas?

Para uma figura isolada com identidade diferente, use um template nativo ou `update_layout` explícito. Para uma variação local do tema, aplique o tema e ajuste a figura sem mudar as constantes compartilhadas.

[Colors](../../constants/colors/README.md) explica a paleta; [styles](../../constants/styles/README.md) trata CSS de outros componentes. Eles não formam, por existirem, um gerenciador único de temas. A iniciativa de centralização visual tem seu próprio ciclo; este README descreve o comportamento já implementado.

## 13. Como saber se o resultado faz sentido?

Confira que os valores de x e y permanecem iguais e que o retorno é a mesma figura. Verifique o significado de N contra os dados usados, não contra a quantidade de barras por suposição.

Execute a aplicação uma vez e observe a quantidade de anotações; antes de reaplicar, decida como tratar o rodapé existente. Confira se a customização feita depois do tema continua presente. Para registro global, verifique o padrão antes/depois e restaure-o ao terminar. Por fim, inspecione título, rodapé e legenda no renderizador final.

## 14. Arquivos relacionados e próximos passos

A [implementação](theme_plotly.py) mantém as três operações legadas e acrescenta as três operações V03; a [fachada](__init__.py) exporta os seis nomes. O [notebook](exemplo_theme_plotly.py) demonstra legado e opt-in configurado. [Correlation matrix](../../display/correlation_matrix/README.md) e [distribution grid](../../display/distribution_grid/README.md) continuam consumidores do caminho legado nesta sprint: não foram migrados implicitamente. O estado da V03 está em `docs/sprints/sistema_temas/V03/`.

## 15. Referências

O guia oficial [Theming and templates](https://plotly.com/python/templates/) descreve o registro e o alcance por sessão, assim como a distinção entre template e propriedades da figura. Consulta em 2026-09-12. As decisões particulares do Hub são verificáveis em [theme_plotly.py](theme_plotly.py), base `c60f1e5`.

Os testes R03-B conferem identidade do objeto, dados preservados, precedência, anotações e registro com restauração do estado. Não homologam o aspecto no Databricks nem verificam a origem declarada pelo usuário. Revisão própria de ChatGPT; auditoria independente não realizada.

A V03 acrescenta testes de equivalência do layout legado, tradução de tokens, integridade do `ResolvedTheme`, ausência de efeitos globais na aplicação por figura, namespace/colisão de templates e falha fechada de contextos/modos ainda não suportados. Esses testes também não substituem inspeção visual no Databricks.
