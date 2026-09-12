# `emojis` — símbolos para orientar a leitura

<!-- readme-objeto: 1.0.0 -->

> Dois mapas associam símbolos a etapas e mensagens. Eles ajudam a organizar o relato, sem executar a análise nem verificar seu resultado.

## Visão rápida

| Pergunta | Resposta |
|---|---|
| O que é? | Dicionários de símbolos, títulos e descrições. |
| Para que serve? | Usar um vocabulário visual previsível. |
| Use quando... | Você está organizando capítulos ou mensagens de análise. |
| Evite quando... | Um símbolo seria apresentado como prova de teste aprovado. |
| Precisa de... | Uma chave existente e contexto para o texto; não exige dados. |
| Entrega... | Strings e dicionários; nenhum diagnóstico automático. |

**Acesso direto:** [exemplo](exemplo_emojis.py) · [implementação](emojis.py) · [API pública](__init__.py) · [coleção](../../README.md).

## 1. O que é?

Um emoji pode funcionar como uma pequena pista de navegação: a pessoa reconhece onde começa uma interpretação ou um próximo passo. Aqui, **mapa semântico** significa uma associação entre significado e símbolo, não um modelo de inteligência artificial.

O módulo contém `SECOES_EDA` e `SEMANTICA`. EDA é análise exploratória de dados: conhecer estrutura, distribuição e limitações de uma base antes de tirar conclusões. O mapa descreve etapas possíveis dessa exploração; ele não as realiza.

## 2. Que problema este recurso resolve?

“Como manter a organização dos notebooks reconhecível entre autores?” Os mapas evitam escolher novos símbolos e títulos a cada relatório. O benefício depende de associar o símbolo ao texto correto, sem confundir organização visual com evidência analítica.

## 3. Quando faz sentido usar?

Use `SECOES_EDA` ao preparar capítulos de uma exploração que precise explicar contexto, chaves e qualidade antes dos resultados. Use `SEMANTICA` para rotular passagens de interpretação, resultado ou próxima ação.

Em uma revisão de qualidade, a combinação de ícone e mensagem ajuda a localizar a conclusão. A mensagem deve informar o que foi conferido e o resultado; o símbolo apenas reforça sua leitura.

## 4. Quando não usar?

Não apresente `SEMANTICA["ok"]` como validação executada. Por exemplo, copiar o símbolo de aprovação para um teste ainda pendente comunica um resultado inexistente.

Não force todas as etapas de EDA em uma dúvida pontual. Nem substitua texto por um círculo colorido: o leitor pode não distinguir sua cor ou entender seu significado. Um título sem emoji é preferível a um símbolo ambíguo.

## 5. Como funciona, intuitivamente?

`SECOES_EDA` usa índices inteiros de 0 a 8. Cada entrada contém `emoji`, `titulo` e `descricao`. `SEMANTICA` usa nomes textuais, como `interpretacao`, `atencao` e `proximo_passo`, que apontam diretamente para um símbolo.

A leitura de uma chave devolve o conteúdo armazenado. Uma chave desconhecida acessada com colchetes gera `KeyError`: o dicionário não inventa a categoria ausente. Nenhum mapa examina dados, impõe a ordem das células ou ativa uma skill.

## 6. Exemplo de situação

Em uma exploração sintética de contatos, você identifica duplicação na coluna usada como chave. O relatório pode mostrar “⚠️ Atenção: chave com duplicatas; confirmar a unidade de cada linha”.

O símbolo vem do mapa; a constatação precisa vir da análise. Depois, “➡️ Próximo passo: revisar a regra de identificação” orienta a continuação. O cenário exemplifica comunicação, não registra um teste de uma tabela real.

## 7. O que você precisa antes de usar?

A importação depende apenas de Python e do pacote visível na raiz `.assistant`. Defina qual mensagem pretende transmitir e escolha uma chave existente. Para ver as opções, consulte os mapas, sem editar os dicionários compartilhados.

`SECOES_EDA` contém dicionários internos: uma cópia superficial mantém esses objetos internos compartilhados. Para adaptar títulos temporariamente, construa uma estrutura própria ou use uma cópia profunda. O [módulo copy](https://docs.python.org/3/library/copy.html) explica a diferença. O notebook inclui preparação com `spark`, embora o mapa em si não necessite de Spark.

## 8. O que este recurso entrega?

`SECOES_EDA[3]` devolve dados do capítulo de qualidade; `SEMANTICA["atencao"]` devolve `⚠️`. Você recebe conteúdo para compor texto, não HTML pronto nem status calculado.

As categorias de resultado, interpretação e negócio organizam a narrativa. Ícones de status não constituem uma escala quantitativa, e a escolha de `status_medio` não calcula severidade.

## 9. Como usar este recurso no Hub?

O [notebook de exemplo](exemplo_emojis.py) percorre os mapas e imprime seu conteúdo. Não lê nem grava tabelas de negócio. Depois de preparar a importação pela [coleção](../../README.md), este trecho usa uma chave sem alterar o mapa:

```python
from hub_snippets.constants.emojis import SECOES_EDA, SEMANTICA
etapa = SECOES_EDA[3]
print(etapa["titulo"])
print(SEMANTICA["atencao"], "Revisar a chave antes do cruzamento.")
```

O trecho portátil foi conferido nesta sprint. Imprimir o aviso não executa a revisão sugerida.

## 10. Decisões e configurações que mais importam

A decisão importante é o significado, não a decoração: destaque uma ação com `proximo_passo`, não com um símbolo de aprovação. Preserve títulos que permitam compreender a mensagem sem o ícone.

A ordem das etapas é um roteiro publicado. Não há validação automática que obrigue a segui-la. A escolha de quais etapas aplicar depende da pergunta e da evidência necessária.

## 11. Limitações, riscos e armadilhas

Dicionários são mutáveis, apesar dos nomes em maiúsculas. Uma alteração no objeto compartilhado pode afetar outros usos na sessão. O conteúdo armazenado também não é automaticamente tratado para uso em HTML: símbolos e títulos atuais são controlados pelo projeto, mas texto externo acrescentado ao lado precisa de tratamento adequado.

A aparência dos emojis pode variar conforme o sistema e o suporte a Unicode. Verifique o destino de leitura e preserve o rótulo textual, sobretudo na exportação. Não existe, neste módulo, teste de leitor de tela ou certificação de acessibilidade.

## 12. Quais são as alternativas?

Um título Markdown sem símbolo resolve muitos casos. Para selos em HTML com estilos de estado, examine [badge](../../visual/badge/README.md). Para capítulos renderizados, consulte [section_header](../../visual/section_header/section_header.py). Nenhuma dessas alternativas executa a checagem representada pelo texto.

## 13. Como saber se o resultado faz sentido?

Leia a mensagem sem olhar o emoji: ainda é possível saber o que ocorreu e o que fazer? Confira também se “aprovado”, “pendente” e “atenção” estão sustentados por estados reais.

Se uma chave não existir, corrija a chave ou use texto explícito; não converta a ausência em aprovação. Teste a visualização no destino de entrega antes de depender de um símbolo para navegação.

## 14. Arquivos relacionados e próximos passos

[emojis.py](emojis.py) é a fonte dos mapas; [__init__.py](__init__.py) expõe os dois nomes; [exemplo_emojis.py](exemplo_emojis.py) demonstra as entradas. A [coleção](../../README.md) dá acesso aos demais recursos e o [Manual](../../../MANUAL_TECNICO.md#catalogo-helpers) preserva o catálogo.

## 15. Referências

Os nomes e conteúdos são sustentados pelo [código local](emojis.py). A documentação de [cópia em Python](https://docs.python.org/3/library/copy.html) fundamenta o cuidado com objetos internos; o [Unicode Emoji](https://www.unicode.org/reports/tr51/) descreve representação e apresentação dos símbolos. Consulta em 12/09/2026.

Revisão R03-A: código, fachada, notebook e testes portáteis. A leitura dos mapas foi exercitada; não houve execução de EDA, homologação Databricks ou auditoria independente.
