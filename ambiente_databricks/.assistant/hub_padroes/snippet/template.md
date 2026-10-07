# Template — pasta de snippet

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Se o seu objeto
> atende uma tarefa explícita de inspeção ou transformação, avalie o contrato
> de [script](../script/template.md). Papel e efeitos orientam essa escolha;
> tipo de argumento sozinho não decide a família. O que estiver em `taxa_resposta_campanha/` é referência
> de forma, **não biblioteca**: não o importe em trabalho real.

Um snippet do Hub é uma **pasta**, não um arquivo. O objeto completo reúne
README humano, fachada, implementação e notebook, com estes nomes:

```text
hub_snippets/<secao>/<nome_do_snippet>/
├── README.md                       # conceito, escolha e uso seguro
├── __init__.py                     # declara a API pública
├── <nome_do_snippet>.py            # a implementação
└── exemplo_<nome_do_snippet>.py    # notebook que demonstra e ensina
```

O nome da pasta é o nome do módulo, em `snake_case`, e precisa ser identificador
Python válido — ele vira parte do caminho de import.

## 1. Fachada pública do objeto

O `__init__.py` do objeto reexporta todos os nomes públicos previstos pela implementação, inclusive constantes consumidas por outros módulos. Não selecione apenas as funções que parecem mais úteis. A geração e conferência da fachada pertencem à manutenção autorizada.

```python
from .taxa_resposta_campanha import MINIMO_PARA_DECISAO, taxa_resposta_campanha
__all__ = ["MINIMO_PARA_DECISAO", "taxa_resposta_campanha"]
```

O `__init__.py` de uma seção como `ml/` não reexporta todos os objetos: isso carregaria dependências opcionais de irmãos desnecessariamente. Importe o objeto específico. Algumas dependências são exigidas no import, outras só na chamada; confira a implementação e declare a diferença. Dependência ausente não é execução bem-sucedida; preserve a exceção e o motivo do não executado.

## 2. O módulo

Ver [`taxa_resposta_campanha/taxa_resposta_campanha.py`](taxa_resposta_campanha/taxa_resposta_campanha.py)
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

## 4. Compatibilidade ao manter um objeto

Preserve nomes públicos, parâmetros, defaults, retorno, efeitos e diagnóstico de erro. Mudança de algoritmo, API ou aparência exige decisão e testes próprios; reorganizar documentação não a autoriza. Dependência ausente e execução não realizada precisam continuar explícitas.

## Antes de dar por pronto

O checklist é **um só para os seis tipos**, e mora em
[`skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md`](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).
Ele separa o que um terceiro consegue conferir do que é juízo de quem escreveu, e
tem um bloco específico para snippet.

Forma, API e links recebem verificação estrutural; qualidade didática, estatística e compatibilidade precisam de revisão e evidência próprias. Não trate uma marca automática como teste de runtime.

## README do objeto

Escreva o [README de objeto](../readme/template_objeto.md) e confira o
[exemplar preenchido](taxa_resposta_campanha/README.md). Ele explica o conceito
e a escolha; o notebook continua demonstrando a execução. Novos objetos exigem
o README. não há dispensa automática. Editar documentação não autoriza alterar a implementação.
