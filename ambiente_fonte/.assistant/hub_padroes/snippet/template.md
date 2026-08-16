# Template — pasta de snippet

Um snippet do Hub é uma **pasta**, não um arquivo. Três arquivos, sempre os
mesmos, sempre com estes nomes:

```text
hub_snippets/<secao>/<nome_do_snippet>/
├── __init__.py                     # declara a API pública
├── <nome_do_snippet>.py            # a implementação
└── exemplo_<nome_do_snippet>.py    # notebook que demonstra e ensina
```

O nome da pasta é o nome do módulo, em `snake_case`, e precisa ser identificador
Python válido — ele vira parte do caminho de import.

## 1. `__init__.py` — não escreva à mão

```bash
python tools/api_publica.py <caminho>/<nome>.py > <caminho>/__init__.py
```

A ferramenta lê o módulo por AST e reexporta **todos** os nomes públicos de nível
superior. A regra é exaustiva, não curada, e isso não é preferência:
`constants/colors` tem 22 nomes públicos e três outros módulos importam nomes
específicos dele. Uma curadoria plausível exporta cinco e quebra o import de
quem depende — e o sintoma aparece sprints depois da causa.

Resultado esperado:

```python
from .taxa_resposta_campanha import MINIMO_PARA_DECISAO, taxa_resposta_campanha

__all__ = [
    "MINIMO_PARA_DECISAO",
    "taxa_resposta_campanha",
]
```

Com isso o import fica limpo, sem repetir o nome:

```python
from hub_snippets.spark.pit_join import pit_join
```

## 2. O módulo

Ver [`exemplo/taxa_resposta_campanha.py`](exemplo/taxa_resposta_campanha.py)
como referência completa. O que é obrigatório:

| Elemento | Regra |
|---|---|
| Docstring do módulo | **por que existe**, não o que faz. Se a única frase possível é "calcula X", o snippet provavelmente não merece existir |
| Decisão de projeto explicada | toda escolha não óbvia vira comentário com o motivo. "Wilson e não normal simples, porque com taxa baixa o normal dá limite negativo" |
| Docstring da função | `Args`, `Returns`, `Raises` e, quando houver armadilha, `Note` |
| Validação de entrada | falhe cedo e com mensagem que diga o que fazer, não só o que houve |
| Constante de política | limite calibrável fica em constante nomeada no topo, nunca embutido no corpo |
| Sessão Spark | `SparkSession.getActiveSession() or ...getOrCreate()`. O global `spark` **não existe** dentro de módulo importado |

### O que nunca fazer

- Silenciar ambiguidade com um valor padrão. Nulo na coluna de resposta pode ser
  "não respondeu" ou "falha de registro"; tratar como zero enviesa sem rastro.
  **Recuse e explique.**
- `cache()` ou `persist()`: bloqueados em serverless.
- `toPandas()` sem limite verificável.
- Sentinela como `-1` para sinalizar erro. Retorne diagnóstico ou levante.

## 3. O notebook

Formato em [`../notebook/template.py`](../notebook/template.py). Ele não é
opcional: **todo snippet tem o seu**, inclusive os curtos. Um leitor que encontra
notebook em doze pastas e não na décima terceira desconfia da décima terceira.

## Antes de dar por pronto

```text
[ ] a pasta tem exatamente os três arquivos, com os nomes do padrão
[ ] __init__.py saiu da ferramenta, sem edição manual
[ ] o notebook executou no laboratório, com a saída real colada
[ ] o README da seção lista este snippet
[ ] python tools/validate_assistant.py aprovado
[ ] o smoke test continua verde
```
