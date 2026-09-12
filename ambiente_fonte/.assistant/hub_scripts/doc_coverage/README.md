# `doc_coverage` — localizar código sem explicação sem fingir medir qualidade textual

<!-- readme-objeto: 1.0.0 -->

Cobertura documental pode significar coisas muito diferentes. Neste script, ela tem um significado deliberadamente estreito: uma célula de código é considerada coberta quando há uma célula Markdown imediatamente antes ou depois dela. O número ajuda a localizar trechos a revisar; não avalia se a explicação é correta, suficiente ou útil.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Um analisador local de notebooks Jupyter ou fontes Databricks exportadas. |
| Para que serve? | Encontrar células de código sem Markdown adjacente. |
| Use quando... | Quiser priorizar revisão documental de notebooks exportados como arquivo. |
| Evite quando... | Precisar avaliar qualidade semântica da explicação, docstrings ou notebooks diretamente por URL do workspace. |
| Precisa de... | Caminho local para `.ipynb`, `.py`, `.sql`, `.scala` ou `.r`. |
| Entrega... | Dicionário com contagens, cobertura percentual e índices zero-based das células sem adjacência documental. |

Consulte a [implementação](doc_coverage.py), a [fachada](__init__.py) e o [notebook de exemplo](exemplo_doc_coverage.py). O exemplo cria três arquivos temporários em `/tmp` e os remove ao final.

## 1. O que é?

`doc_coverage` é uma heurística estrutural. Para um `.ipynb`, lê o JSON e reduz cada célula a tipo e texto. Para uma fonte Databricks exportada, separa células pelos marcadores `COMMAND ----------` e reconhece Markdown pelos magic comments esperados para a linguagem.

A métrica não usa modelo de linguagem, parser de intenção nem avaliação editorial. Um Markdown contendo apenas `.` conta como documentação adjacente da mesma forma que um parágrafo explicativo.

## 2. Que problema este recurso resolve?

Ele responde: “Quais células de código não têm nenhuma célula Markdown imediatamente ao lado?”. Essa pergunta é útil em revisão de notebooks extensos, porque transforma uma inspeção visual cansativa em uma lista pequena de pontos a verificar.

O recurso não responde “este notebook está bem documentado?”. Essa segunda pergunta depende de clareza, justificativa, contexto, limitações e coerência com o código.

## 3. Quando faz sentido usar?

Use sobre arquivos exportados quando o padrão de escrita esperado coloca explicações próximas ao código que elas contextualizam. Também serve para comparar a evolução estrutural de um mesmo notebook, desde que formato e convenção permaneçam estáveis.

É especialmente útil como triagem: uma cobertura baixa sugere onde começar a revisão; uma cobertura alta apenas reduz a quantidade de células obviamente desacompanhadas.

## 4. Quando não usar?

Não use como KPI de qualidade textual ou meta de equipe. Um time pode atingir 100% acrescentando títulos vazios sem explicar decisão alguma.

Também não use para avaliar módulos Python comuns. Uma biblioteca bem documentada por docstrings pode ter 0% neste indicador se for passada como se fosse notebook-fonte, porque a métrica não lê docstrings como documentação.

## 5. Como funciona, intuitivamente?

Depois de converter o arquivo em uma sequência de células `markdown` ou `code`, o script percorre somente as de código. Para cada uma, olha a célula anterior e a seguinte. Se nenhuma for Markdown, guarda o índice como descoberto.

A cobertura é `100 × (1 - descobertas / células_de_código)`. Se não houver nenhuma célula de código, a função devolve 100% por convenção matemática da implementação — não porque tenha encontrado documentação excelente.

## 6. Exemplo de situação

Considere dois notebooks sintéticos com duas ou três células de código. No primeiro, cada bloco de código tem Markdown próximo; no segundo, há apenas código. O [exemplo](exemplo_doc_coverage.py) produz 100% e 0% respectivamente.

Depois ele cria um terceiro arquivo em que o único Markdown contém apenas um ponto. A cobertura volta a 100%. Esse contraexemplo é parte central do contrato: o script mede proximidade estrutural, não qualidade editorial.

## 7. O que você precisa antes de usar?

`notebook_path` deve apontar para arquivo local existente. São aceitos `.ipynb`, `.py`, `.sql`, `.scala` e `.r`. Outras extensões geram `ValueError`.

Para fontes Databricks, o reconhecimento depende dos marcadores codificados em `SOURCE_MARKERS`. Para `.py` e `.r`, por exemplo, a célula é separada por `# COMMAND ----------`; Markdown é reconhecido por `# MAGIC %md` ou `%md-sandbox` nas primeiras linhas relevantes.

A função não baixa objetos do workspace, não autentica em APIs e não segue URLs. Exporte ou materialize o notebook por um mecanismo apropriado antes de medir.

## 8. O que este recurso entrega?

| Campo | Significado |
|---|---|
| `path` | Caminho analisado. |
| `format` | Extensão em minúsculas. |
| `total_code_cells` | Quantidade de células classificadas como código. |
| `total_markdown_cells` | Quantidade classificada como Markdown. |
| `coverage_pct` | Percentual de células de código com Markdown imediatamente antes ou depois. |
| `uncovered_cell_indexes` | Índices zero-based, na sequência interna de células, dos blocos sem adjacência. |
| `metric_note` | Aviso explícito de que a métrica é heurística de adjacência. |

Um valor de 100% não implica explicação suficiente. Um valor baixo também não prova dívida técnica: um notebook curto pode ter uma seção Markdown que explica vários blocos não adjacentes.

## 9. Como usar este recurso no Hub?

A chamada mínima é:

```python
from hub_scripts.doc_coverage import doc_coverage

resultado = doc_coverage("/tmp/notebook_exportado.py")
print(resultado["coverage_pct"])
print(resultado["uncovered_cell_indexes"])
```

Abra o [exemplo](exemplo_doc_coverage.py) para ver arquivos sintéticos controlados e o contraexemplo de Markdown vazio. O script lê somente o arquivo indicado; o exemplo é que cria e remove arquivos temporários.

## 10. Decisões e configurações que mais importam

A principal “configuração” é o formato do arquivo, porque determina o parser usado. `.ipynb` segue a estrutura JSON de células; fontes Databricks seguem marcadores textuais.

Não há parâmetro de distância. Somente vizinhança imediata conta. Uma explicação duas células antes não cobre o bloco.

Também não há limiar de aprovação. Qualquer regra como “mínimo 80%” precisa ser criada e justificada pelo consumidor; o helper não possui esse conceito.

## 11. Limitações, riscos e armadilhas

O parser das fontes é heurístico. Alterações no formato de exportação, magic comments fora das primeiras linhas esperadas ou texto contendo marcadores de comando podem afetar a segmentação.

Para `.ipynb`, a função pressupõe JSON legível e a estrutura convencional `cells[].cell_type/source`. Ela não executa notebook, não verifica outputs nem determina se Markdown descreve a célula correta.

Arquivos sem código recebem 100%. Esse valor deve ser lido como “nenhuma célula de código ficou descoberta segundo a fórmula”, não como excelência documental.

## 12. Quais são as alternativas?

Para revisão editorial real, use revisão humana apoiada pelo [template de README de objeto](../../hub_padroes/readme/template_objeto.md) ou por uma checklist específica do documento. Para docstrings e APIs de módulos Python, use ferramentas de documentação de código em vez desta métrica de notebook.

Quando o objetivo é localizar notebooks e seus links quebrados, o validador do repositório é mais apropriado: ele trata navegação, não adjacência Markdown-código.

## 13. Como saber se o resultado faz sentido?

Abra manualmente os índices listados em `uncovered_cell_indexes` e confira a sequência de células. Em um arquivo pequeno, conte quantas células de código realmente têm Markdown ao lado e recalcule a fração.

Teste deliberadamente três casos: só código; Markdown + código; e Markdown vazio + código. Os dois últimos devem ter a mesma cobertura estrutural, deixando explícita a limitação semântica.

Se a contagem de células parecer estranha, inspecione os marcadores de exportação antes de discutir o percentual.

## 14. Arquivos relacionados e próximos passos

A [implementação](doc_coverage.py) define parsers e fórmula; a [fachada](__init__.py) expõe a API; o [exemplo](exemplo_doc_coverage.py) mostra a fronteira entre estrutura e qualidade. O [catálogo de scripts](../README.md) reúne as outras ferramentas operacionais.

Use o resultado para selecionar células a revisar. O próximo passo é ler o conteúdo e decidir se a explicação realmente cobre premissas, decisão e interpretação.

## 15. Referências

O contrato deste recurso vem da implementação, fachada e exemplo locais, revisados na R04-B em 12/09/2026. Não há dependência de documentação externa para a fórmula local.

O formato-fonte reconhecido é o que a implementação codifica hoje; isso não deve ser generalizado como especificação eterna de exportação Databricks. A validação específica da R04-B é registrada no relatório da sprint após execução.

Revisão do próprio texto não é auditoria independente; nenhuma alegação de publicação ou homologação Databricks é feita.