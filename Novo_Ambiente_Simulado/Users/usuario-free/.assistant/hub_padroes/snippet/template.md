# Template — pasta de snippet

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Se o seu objeto
> recebe **nome de tabela** e devolve um veredito, ele é script e não snippet —
> a distinção está em [`../script/template.md`](../script/template.md) e muda a
> assinatura da função. O que estiver em `taxa_resposta_campanha/` é referência
> de forma, **não biblioteca**: não o importe em trabalho real.

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
`constants/colors` tem 22 nomes públicos, e `visual/section_header` e
`visual/theme_plotly` importam nomes específicos dele. Uma curadoria plausível exporta cinco e quebra o import de
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

### O `__init__.py` de **seção** não reexporta nada

`spark/__init__.py`, `ml/__init__.py` e os outros de nível de seção continuam
com docstring e mais nada. Só a pasta do **objeto** reexporta.

Não é preguiça: é o que mantém a seção importável. Um `__init__.py` de seção que
reexportasse os objetos importaria todos eles de uma vez — e **sete** módulos de
`ml/` importam biblioteca ausente no laboratório já no topo do arquivo. A seção
inteira deixaria de importar por causa deles, **e os irmãos junto**: um
`ml/score_bands`, sem dependência nenhuma, falharia com `exc.name='lightgbm'`,
porque importar qualquer submódulo executa o `__init__` do pacote pai.

(São 14 os módulos com dependência opcional; os outros 7 importam dentro da
função e por isso importam sem erro. A distinção importa na hora de decidir o
que testar.)

Verificado com um pacote de teste:

```text
pkg.ml.train_lgbm              -> OPTIONAL_MISSING  (exc.name = 'lightgbm')
pkg.ml.train_lgbm.train_lgbm   -> OPTIONAL_MISSING  (exc.name = 'lightgbm')
pkg.ml                         -> PASS
```

A última linha só é `PASS` porque a seção não reexporta.

### Objeto que depende de biblioteca ausente: nada muda

As duas primeiras linhas acima respondem à outra dúvida. O `__init__.py` eager
**preserva o `exc.name`** da dependência que faltou, então o smoke test continua
classificando como `OPTIONAL_MISSING` e não como `FAIL`.

E não há regressão: `train_lgbm.py` já tem `import lightgbm` no topo, de modo que
importar o módulo já falhava antes da conversão. A pasta falha do mesmo jeito,
pelo mesmo motivo, com o mesmo diagnóstico.

**Consequência para quem escreve o notebook:** o objeto não pode ser importado no
laboratório de forma alguma, nem para alcançar uma constante. É o caso do BLOCO
CANÔNICO de não executado, e o motivo se enquadra em "a dependência não existe e
não há versão compatível conhecida".

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

## 4. Converter um snippet que já existe

**A maior parte do trabalho do Hub não é criar: é converter.** São 51 snippets e
7 scripts que já rodam, que o smoke test já importa e que as skills já recomendam
por caminho de import. As seções acima descrevem o objeto pronto; esta descreve
como chegar nele sem quebrar o que funciona.

### A regra: mover, e só então melhorar

Converter é **mover**. A conversão não muda comportamento. Se o módulo antigo
devolve 0% em base vazia, o convertido devolve 0% em base vazia — mesmo que o
template peça "falhe cedo".

Duas etapas, em commits separados:

| Etapa | O que entra | O que **não** entra |
|---|---|---|
| **1. Mover** | pasta, `__init__.py` gerado, notebook novo, docstring traduzida e ampliada | nenhuma mudança de assinatura, de valor devolvido ou de comportamento em caso de borda |
| **2. Melhorar** | validação de entrada, constante de política, recusa em caso ambíguo | — |

A etapa 2 é **opcional e por objeto**, e exige registrar no notebook o que mudou.
Sem essa separação, cada executor decide sozinho quanto do módulo antigo
sobrevive, e a diferença só aparece quando algo que funcionava para de funcionar.

### O que a conversão não pode alterar

| Item | Por quê |
|---|---|
| Nome e ordem dos parâmetros | há código chamando; renomear `threshold_warn` quebra em silêncio |
| Nome das colunas devolvidas | quem consome o DataFrame quebra sem erro de import |
| Comportamento em base vazia, nulo e caso limite | é o que o smoke test e os testes de regressão fixam |
| `print()` de progresso, se houver | é ruído em biblioteca, mas removê-lo é mudança de comportamento — registre e faça na etapa 2 |

### Idioma

**Não traduza identificador na conversão.** Parâmetro, coluna devolvida e nome de
função ficam como estão — traduzir é quebra silenciosa. Docstring, comentário e
notebook são prosa e vão em português. Um módulo com `threshold_warn` e docstring
em português é inconsistente e correto; um com `limite_alerta` é consistente e
quebrado.

### Antes de mover, olhe para fora da pasta

| Verifique | Onde |
|---|---|
| Quem importa este módulo | `grep -rn "<secao>.<modulo>" ambiente_fonte tools` |
| Se o smoke test o cita nominalmente | `tools/spark_smoke_test.py` tem casos funcionais por nome |
| Se alguma skill o recomenda | as `SKILL.md` de `skills/` declaram helpers por caminho de import |
| Se ele redeclara constante de outro módulo | ver a regra abaixo — é o único caso em que a conversão **não** é só mover |

### Constante duplicada: a exceção que precisa de decisão

Quatro módulos de `ml/` redeclaram a paleta em vez de importá-la de
`constants.colors`. E os valores **divergem**:

| Nome | Onde | Valor |
|---|---|---|
| `PALETA_CATEGORICA` | `constants.colors` | 10 cores |
| `PALETA_CATEGORICA` | `ml.curves_plotly` | **6 cores** |
| `PALETA_CATEGORICA` | `ml.umap_viz`, `ml.vintage_analysis` | 10 cores, idênticas |

Duas das três cópias são iguais à original, o que torna a terceira invisível numa
inspeção rápida.

A regra exaustiva do `__init__.py` publica cada uma como API pública oficial. Ao
fim da conversão haverá dois caminhos de import para `PALETA_CATEGORICA` com
valores diferentes, ambos "corretos" pela regra.

**A conversão não resolve isso, e não deve tentar.** Trocar a redeclaração por
import muda o comportamento — `curves_plotly` passaria de 6 para 10 cores nos
gráficos —, e a etapa 1 proíbe mudança de comportamento. A instrução anterior,
"converta o import antes", pedia exatamente o que a regra veta.

**O que fazer:** converta como está, na etapa 1, e **registre a duplicação no
notebook do objeto**, na seção "quando não usar" — dizendo qual valor aquele
módulo usa e que ele difere de `constants.colors`. A unificação é decisão de
produto, vai para a etapa 2, e precisa de alguém olhando os gráficos para dizer
se seis ou dez cores é o certo ali.

Duplicação de constante com valor idêntico (`umap_viz`, `vintage_analysis`) é
dívida menor: registre no notebook e siga.

## Antes de dar por pronto

O checklist é **um só para os seis tipos**, e mora em
[`skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md`](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).
Ele separa o que um terceiro consegue conferir do que é juízo de quem escreveu, e
tem um bloco específico para snippet.

Três listas divergentes conviveram neste projeto até uma auditoria apontar: uma
pedia smoke test e não pedia catálogo, outra o inverso. Uma lista só, com um
dono, é o conserto.

Os dois primeiros itens de verificação automática estão marcados: o validador
confere nome de pasta, presença dos três arquivos e se o `__init__.py` bate com a
API pública do módulo. Os demais são manuais — e o item do smoke test só é
alcançável depois que a seção inteira estiver convertida.
