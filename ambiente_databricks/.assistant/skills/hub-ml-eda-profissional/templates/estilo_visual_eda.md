# Estilo Visual — EDA Profissional sobre o Sistema de Temas

Este template orienta **composição, hierarquia e leitura** de uma EDA. Ele não é fonte de paleta, token ou aprovação. As escolhas configuráveis pertencem ao contrato `hub_padroes/identidade_visual` e chegam ao consumidor por `ResolvedTheme`.

---

## 1. Fonte de verdade visual

- Não declare paleta, dicionário de tema ou convenção local que replique a política visual do Hub.
- Não copie valores de `TOKENS.md` para “congelar” uma aparência local.
- Não registre template global como preparação padrão do notebook; **não registre template global** apenas para aplicar uma proposta.
- Se não houver tema explicitamente selecionado, use as APIs legadas do Hub.
- Se houver tema notebook válido, use as rotas `_resolvido` do consumidor.

Fluxo mínimo para uma figura Plotly genérica:

```python
from hub_snippets.visual.tema import load_reference_theme
from hub_snippets.visual.theme_plotly import aplicar_tema_resolvido

tema = load_reference_theme("notebook")
fig = ...  # mesmos dados, agregações e eixos da análise
aplicar_tema_resolvido(fig, tema, subtitulo="Recorte analisado", n=n_amostra)
fig.show()
```

Para componentes especializados, prefira a própria rota resolvida, por exemplo `plot_correlation_resolvido`, `plot_distributions_resolvido`, curvas `*_resolvido`, `plot_vintage_curves_resolvido` ou `plot_timeline_resolvido`. Isso evita reconstruir semântica de cor no notebook.

---

## 2. O que o tema pode e não pode mudar

O tema pode controlar propriedades visuais cobertas pelo contrato, como tipografia, dimensões, margens, paletas e cores semânticas. Ele **não** muda:

- filtro, população ou data de corte;
- amostragem, seed ou agregação;
- bins, denominadores e unidade;
- threshold analítico ou política de monitoramento;
- métrica, modelo ou conclusão de negócio.

Aparência consistente não valida a análise.

---

## 3. Regras de gráficos

### 3.1. Escolher o visual pela pergunta

| Tipo de dado/pergunta | Visual sugerido | Cuidados |
| --- | --- | --- |
| numérica univariada | histograma, ECDF ou box plot | declarar amostra/agregação |
| categórica | barras ordenadas | mostrar denominador, top-N e cauda |
| temporal | linha em frequência regular | rotular janela e gaps |
| associação numérica | scatter/agregado ou correlação | sinal não implica causalidade |
| matriz com centro significativo | heatmap divergente | preservar centro e domínio |
| comparação de segmentos | small multiples ou barras | manter escala comparável |

Use Plotly para gráficos do relatório quando a interatividade ajudar. `createVisualization` ou visualização nativa podem ser melhores para exploração rápida ou agregações que devem ficar no backend. Matplotlib permanece válido para casos estáticos específicos, mas não herda automaticamente o Sistema de Temas Plotly.

### 3.2. Anotações do relatório final

Todo gráfico material deve deixar explícitos, quando aplicável:

- N amostral ou volume agregado;
- fonte/snapshot;
- janela, segmento ou recorte;
- unidade e denominador;
- uma anotação de destaque somente quando houver achado realmente sustentado.

Não transforme anotação em conclusão causal. Em rotas Plotly do Hub, use os argumentos de rodapé do adaptador/consumidor em vez de criar um segundo estilo.

### 3.3. Dimensão da figura

Não copie uma tabela local de alturas/larguras para simular o tema. Dimensões configuráveis pertencem aos tokens do contexto. Ajustes excepcionais por conteúdo — por exemplo, um heatmap com muitas safras — podem complementar o tema quando o próprio consumidor documentar essa regra.

---

## 4. Emojis padronizados

Uso **limitado e semântico**, nunca apenas decorativo.

| Emoji | Significado | Contexto de uso |
| --- | --- | --- |
| ✅ | validação passou / OK | checks de qualidade |
| ❌ | validação falhou / erro | checks de qualidade |
| ⚠️ | atenção / risco moderado | ponto de atenção |
| 🟢 | status positivo | indicador de qualidade |
| 🟡 | status intermediário | indicador de qualidade |
| 🔴 | status crítico | indicador de qualidade |
| 📌 | insight-chave | interpretação material |
| 📊 | resultado factual | seção de dados |
| 🔍 | interpretação/análise | seção técnica |
| 💼 | visão de negócio | seção executiva |
| ➡️ | próximo passo | transição entre etapas |

Use no máximo três emojis por célula Markdown. Evite emojis nos títulos `##`; prefira-os em subtítulos ou blocos de resultado quando acrescentarem significado.

---

## 5. Formato de números

Prefira `hub_snippets.constants.format_br` quando a entrega exigir convenção brasileira. O ponto importante é manter a **mesma unidade e convenção em todo o notebook**, não copiar formatações ad hoc em cada célula.

| Tipo | Apresentação esperada |
| --- | --- |
| inteiro grande | separador de milhar consistente |
| monetário BRL | símbolo, duas casas quando materiais e convenção BR |
| percentual | uma ou duas casas conforme precisão útil |
| razão/taxa | casas suficientes para não esconder variação relevante |
| contagem pequena | inteiro sem decimal |

Em tabelas Markdown destinadas ao público brasileiro, use a convenção de milhares/decimais prevista pelo helper. Não transforme arredondamento de apresentação em alteração do valor calculado.

---

## 6. Tabelas Markdown

- Prefira até seis colunas por bloco legível; se houver muitas dimensões, divida a apresentação.
- Alinhe números à direita quando a superfície permitir.
- Use nomes de coluna curtos, sem repetir o título inteiro.
- Use negrito apenas para destaques semânticos.
- Use backticks para nomes técnicos, como `` `valor_pago` ``.
- Trunque texto longo apenas na apresentação e deixe claro quando houver perda de conteúdo.
- Sempre declare unidade/denominador quando eles não forem óbvios pelo rótulo.

Exemplo de estrutura:

```markdown
| Métrica | Valor | Status |
| --- | ---: | :---: |
| Total de linhas | [observado ou NÃO CALCULADO] | [critério ou NÃO CLASSIFICADO] |
| PK única | [evidência ou NÃO VERIFICADA] | [critério ou NÃO CLASSIFICADO] |
| Nulos | [observado ou NÃO CALCULADO] | [critério ou NÃO CLASSIFICADO] |
```

---

## 7. KPI card — linha de impacto

Uma célula pós-código pode abrir com poucos KPIs materiais para leitura rápida:

```markdown
> **N linhas** | **P colunas** | **x% nulos** | **D duplicatas**
```

Regras:

- use somente valores observados na saída;
- limite-se a quatro ou cinco KPIs por linha;
- mantenha unidade explícita;
- não preencha um card com números inventados para completar layout;
- quando precisar de HTML/card institucional, use `hub_snippets.visual.kpi_card` e sua rota `_resolvido` quando houver `ResolvedTheme`.

---

## 8. Output de código e cabeçalhos de seção

Para notebook exploratório, um output textual simples é suficiente. Se quiser um cabeçalho textual, priorize função sem política de cor local:

```python
def exibir_secao(titulo, subtitulo=None):
    largura = 60
    print(f"\n┌{'─' * (largura - 2)}┐")
    print(f"│ {titulo:<{largura - 4}} │")
    if subtitulo:
        print(f"│ {subtitulo:<{largura - 4}} │")
    print(f"└{'─' * (largura - 2)}┘")
```

Para apresentação rica, não escreva `displayHTML` com CSS/cores inline para recriar o padrão. Use `hub_snippets.visual.section_header`, `kpi_card`, `badge` e `divider`; com tema selecionado, use a rota `_resolvido` documentada pelo componente.

---

## 9. Hierarquia de títulos Markdown

| Nível | Uso | Exemplo |
| --- | --- | --- |
| `#` | título único do notebook | `# EDA — Tabela X` |
| `##` | etapas principais | `## Etapa 3 — Qualidade` |
| `###` | subseções/resultados | `### Resultado — Etapa 3` |
| `####` | tópicos internos | `#### Resultado observado` |

Evite `#####` ou níveis inferiores; em geral indicam profundidade excessiva.

---

## 10. Separadores e narrativa pós-código

Para um bloco de resultado longo, mantenha uma ordem previsível:

```markdown
### Resultado — Etapa N

> **KPI1** | **KPI2** | **KPI3**

---

#### 📊 Resultado observado
(tabela ou fatos)

---

#### 🔍 Interpretação técnica
(análise suportada pela saída)

---

#### 💼 Interpretação de negócio
(implicação, sem transformar associação em causalidade)

---

#### ➡️ Próximo passo
(continuidade concreta)
```

Use `hub_snippets.visual.divider` quando precisar de um componente institucional; não replique borda/cor manualmente.

---

## 11. Índice de seções

Todo notebook EDA extenso deve oferecer uma rota de navegação no início. O helper oficial é `hub_snippets.visual.index_generator`.

- O mapeamento de emojis compartilhados vive em `hub_snippets.constants.emojis`.
- Liste etapa, título e descrição curta.
- O índice pode ser Markdown ou HTML conforme o consumidor; com `ResolvedTheme`, prefira a rota resolvida existente.
- O índice não substitui títulos reais no notebook.

---

## 12. Section headers

Cada seção principal pode abrir com `hub_snippets.visual.section_header`.

O cabeçalho deve comunicar:

- etapa/seção;
- título objetivo;
- descrição de uma frase;
- hierarquia coerente com o restante do notebook.

Cor, fonte e borda não são especificadas neste template: vêm da implementação legada ou do `ResolvedTheme` pela rota `_resolvido`.

---

## 13. Referência de componentes compartilhados

| Necessidade | Fonte/consumidor |
| --- | --- |
| contrato e primeiro uso | `hub_padroes/identidade_visual/README.md` e `GUIA_OPERACIONAL.md` |
| carregar/validar tema | `hub_snippets.visual.tema` |
| aplicar tema Plotly | `hub_snippets.visual.theme_plotly.aplicar_tema_resolvido` |
| correlação | `hub_snippets.display.correlation_matrix.plot_correlation_resolvido` |
| distribuições | `hub_snippets.display.distribution_grid.plot_distributions_resolvido` |
| índice | `hub_snippets.visual.index_generator` |
| cabeçalho de seção | `hub_snippets.visual.section_header` |
| KPI cards | `hub_snippets.visual.kpi_card` |
| divisores | `hub_snippets.visual.divider` |
| badges | `hub_snippets.visual.badge` |
| autoria/comparação | `hub_snippets.visual.theme_lab` |

Use a API legada quando não houver tema explicitamente selecionado; use a rota `_resolvido` quando houver um `ResolvedTheme` válido e o componente documentar suporte.

---

## 14. Consumidores com limite explícito

- **SHAP/Matplotlib:** o theming atual não cobre sua aparência interna nem o PNG salvo pelo helper.
- **Kaplan–Meier:** permanece com a ordem visual legada até existir token que represente sua semântica sem remapeamento silencioso.

Não prometa consistência temática para essas superfícies apenas porque o restante do notebook usa `ResolvedTheme`.

O template EDA organiza a apresentação. A fonte de verdade do tema permanece fora desta skill.
