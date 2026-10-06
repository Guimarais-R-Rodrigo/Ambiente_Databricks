# `colors` — cores com significado consistente

<!-- readme-objeto: 1.0.0 -->

> Uma paleta é um conjunto de cores escolhido para comunicar diferenças. Este módulo reúne as cores e os nomes usados pelo Hub, mas não desenha nem avalia gráficos.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Constantes de cor e listas de paletas. |
| Para que serve? | Manter significados e aparência consistentes. |
| Use quando... | Você já sabe se quer mostrar categorias, intensidade ou desvios. |
| Evite quando... | A cor seria a única forma de comunicar um resultado. |
| Precisa de... | Python e a biblioteca do Hub acessível; dados não são exigidos. |
| Entrega... | Textos de cor hexadecimal e listas; nenhum gráfico automático. |

**Acesso direto:** [exemplo](exemplo_colors.py) · [implementação](colors.py) · [API pública](__init__.py) · [coleção](../../README.md).

## 1. O que é?

Uma cor pode identificar uma categoria, como um canal de atendimento, ou representar uma quantidade, como o volume de contatos. Uma **paleta** organiza essas cores. Uma **cor semântica** recebe um significado explícito: alerta, resultado positivo ou resultado negativo.

[Este módulo](colors.py) fornece constantes com nomes legíveis, como `AZUL_CAIXA` e `COR_ALERTA`. O valor `"#005CA9"` é uma representação hexadecimal de uma cor; não é um indicador calculado. As constantes são convenções do projeto, não uma biblioteca oficial da Databricks nem uma certificação de acessibilidade.

## 2. Que problema este recurso resolve?

“Como evitar que a mesma categoria mude de cor a cada página, ou que vermelho signifique coisas diferentes?” O recurso oferece um vocabulário visual comum. A decisão sobre o que merece alerta continua com quem analisa: importar `COR_ALERTA` não verifica qualidade nem descobre problemas.

## 3. Quando faz sentido usar?

Use `PALETA_CATEGORICA` para diferenciar grupos sem ordem natural, como produtos. Para representar magnitude em uma escala ordenada, considere `PALETA_SEQUENCIAL`. Para valores em torno de uma referência significativa, considere `PALETA_DIVERGENTE`, conferindo a posição dessa referência na escala do gráfico.

Use os nomes semânticos em resumos cujo significado já esteja definido. Uma queda no número de falhas pode ser positiva: sinal matemático e avaliação de negócio não são a mesma coisa. Registre a interpretação antes de associar a cor.

## 4. Quando não usar?

Não use uma escala de intensidade para sugerir que uma categoria nominal é “maior” que outra. Tampouco use verde como prova de aprovação. Um painel com categorias que compartilham cores, mas não têm rótulos, pode parecer correto e continuar ambíguo.

A lista categórica tem dez cores; o módulo não agrupa categorias excedentes nem decide se a biblioteca gráfica repetirá cores. Se o número de grupos impedir distinguir as séries, reveja agrupamento, rótulos ou divisão em gráficos. Não descarte categorias relevantes apenas para caber na paleta.

## 5. Como funciona, intuitivamente?

Os nomes apontam para strings ou listas de strings. Por exemplo, `COR_POSITIVO` recebe o valor de `VERDE`. Uma função de visualização pode consultar esse valor e inseri-lo em seu resultado, mas precisa fazê-lo explicitamente.

A lista sequencial organiza tons de azul; a divergente disponibiliza uma sequência de cores em torno de um centro visual. Essa sequência não calcula limites, zero ou normalização. A escala numérica e o mapeamento das categorias são definidos no gráfico consumidor.

## 6. Exemplo de situação

Considere um resumo sintético de contatos por canal. No primeiro gráfico, azul identifica “aplicativo”; no segundo, deve continuar identificando esse canal. O analista define o mapeamento e reutiliza a mesma cor nos dois locais.

Um aviso de registros sem data pode usar `COR_ALERTA` acompanhado de “12 registros sem data”. O número é ilustrativo. O ganho esperado é consistência de comunicação, não alteração da contagem ou aprovação automática da base.

## 7. O que você precisa antes de usar?

A importação utiliza Python e a estrutura do Hub, sem Spark ou Plotly neste módulo. Para transformar uma cor em gráfico, será necessária a ferramenta de visualização escolhida.

O notebook de demonstração tem outra preparação: consulta `current_user()` via `spark` e usa `displayHTML`. Não confunda a portabilidade das constantes com a validação desse notebook em qualquer ambiente. As listas são objetos mutáveis: use uma cópia para experiências locais e não altere a paleta compartilhada em memória.

## 8. O que este recurso entrega?

São cores isoladas, paletas e referências de fundo, texto e borda. `PALETA_CATEGORICA` tem dez entradas; as outras duas paletas têm cinco. A [fachada](__init__.py) expõe os nomes públicos.

O recurso não devolve figura, legenda, relatório de contraste ou validação de daltonismo. A cor selecionada só terá efeito nos componentes que a utilizarem. Reatribuir uma constante depois de importações anteriores não é um mecanismo confiável para atualizar toda a sessão.

## 9. Como usar este recurso no Hub?

Abra o [exemplo](exemplo_colors.py) para visualizar as paletas após conferir a preparação. Ele não grava tabelas; exibe HTML e textos. Em um notebook onde a raiz `.assistant` já esteja acessível ao Python, este trecho consulta sem modificar:

```python
from hub_snippets.constants.colors import AZUL_CAIXA, PALETA_CATEGORICA
paleta_local = PALETA_CATEGORICA.copy()
print(AZUL_CAIXA, len(paleta_local))
```

Saída de referência do trecho portátil: `#005CA9 10`. Para preparar a importação, siga a [coleção](../../README.md); não presuma um caminho de usuário diferente do ambiente confirmado.

Para manter categorias estáveis, declare a ordem e reutilize o mesmo mapa:

```python
canais = ["aplicativo", "agencia", "telefone"]
cores_por_canal = dict(zip(canais, PALETA_CATEGORICA.copy()))
assert len(cores_por_canal) == len(canais)
```

Este exemplo usa três categorias; para mais categorias que cores, decida outra codificação antes de criar o mapa.

## 10. Decisões e configurações que mais importam

Escolha primeiro a relação que será comunicada: diferença entre grupos, magnitude ou desvio. Depois fixe a correspondência entre cores e categorias; apenas passar uma lista não garante consistência entre gráficos com ordens distintas.

Verifique também o par texto/fundo. `TEXTO_PRINCIPAL` não é uma aprovação automática de qualquer combinação. A posição do zero numa escala divergente é configuração do gráfico, não deste módulo.

## 11. Limitações, riscos e armadilhas

A paleta categórica reutiliza cores que também têm nomes semânticos. Um vermelho usado para um produto não deve parecer uma reprovação desse produto. Legenda e contexto precisam resolver a ambiguidade.

Pelo cálculo de contraste da WCAG, texto branco sobre `COR_ALERTA` apresenta aproximadamente **1,73:1** e sobre `COR_POSITIVO`, **2,04:1**, abaixo de 4,5:1 para texto comum. A conferência foi numérica, não uma auditoria visual completa. A [WCAG 2.2](https://www.w3.org/TR/WCAG22/#contrast-minimum) contém o critério e suas exceções; [uso da cor](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) exige que informação não dependa apenas dela.

## 12. Quais são as alternativas?

Para aplicação automática a figuras compatíveis, examine [theme_plotly](../../visual/theme_plotly/README.md), em vez de distribuir ajustes manuais pelo notebook. Para um rótulo de estado, [badge](../../visual/badge/README.md) pode fornecer o HTML, mas tem estilos próprios.

Uma apresentação monocromática com rótulos pode ser mais clara do que uma paleta com muitos grupos. Mudar a identidade visual compartilhada é outra tarefa, não consequência de consultar este README.

## 13. Como saber se o resultado faz sentido?

Confira se cada categoria mantém a mesma cor entre gráficos e se a legenda preserva o significado sem depender da percepção de cor. Meça contraste para o par efetivamente usado, sobretudo em texto pequeno.

Se a combinação falhar, não declare a página acessível: registre o par, o tamanho do texto e a alternativa a revisar. Conferir apenas que a string começa com `#` verifica formato, não legibilidade.

## 14. Arquivos relacionados e próximos passos

[colors.py](colors.py) contém valores e relações; [__init__.py](__init__.py) expõe os nomes; [exemplo_colors.py](exemplo_colors.py) demonstra as combinações. A [coleção](../../README.md) mantém a navegação e o [Manual](../../../MANUAL_TECNICO.md#catalogo-helpers) mantém o catálogo integrado.

Continue pelo [índice constants](../README.md).

## 15. Referências

O [código local](colors.py) sustenta os valores e a composição das paletas. A [WCAG — contraste](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html) sustenta a aferição texto/fundo; a regra de [uso da cor](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html) sustenta a orientação de redundância textual. Fontes consultadas em 12/09/2026.

Aferir contraste numericamente não certifica acessibilidade nem renderização no notebook de destino. Confira as combinações usadas e preserve rótulos textuais.

[Registro técnico de referência](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/blob/2f5a0cb94f82b78324f6a79d70af7d03e7b57040/docs/sprints/readmes_objetos/RELATORIO_R03A.md): consulte data, ambiente e alcance de cada teste; o registro não é homologação do destino.
