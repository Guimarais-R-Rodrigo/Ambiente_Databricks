<a id="hub_padroes-templates-do-hub"></a>

# `hub_padroes/` — templates do Hub

> **HUB · CONSULTA MANUAL.** Esta coleção não é auto-descoberta pelo Genie Code.
> Anexe o template com `@` ou use `@hub-ml-criar-objeto` para aplicar o fluxo.

> **Rascunho de sprint 8 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/hub_padroes/README.md`.

Quando várias pessoas criam material, cada uma inventa uma pasta diferente.
Um **molde** (template) fixa estrutura e o que precisa ser revisado. Ele **não**
certifica que a fórmula ou o texto estão corretos.

---

<a id="escolha-o-objeto"></a>

## Escolha o objeto

Há **seis** tipos. `auditoria/` e `output/` são padrões de processo, não tipos
novos.

| Quero criar… | Necessidade típica | Template | Exemplo preenchido |
|---|---|---|---|
| README | explicar uma pasta | [`readme/template.md`](../../../ambiente_fonte/.assistant/hub_padroes/readme/template.md) | [`readme/exemplo.md`](../../../ambiente_fonte/.assistant/hub_padroes/readme/exemplo.md) |
| snippet | função importável | [`snippet/template.md`](../../../ambiente_fonte/.assistant/hub_padroes/snippet/template.md) | [`taxa_resposta_campanha`](../../../ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha) |
| script | diagnóstico de um recurso | [`script/template.md`](../../../ambiente_fonte/.assistant/hub_padroes/script/template.md) | [`checar_base_campanha`](../../../ambiente_fonte/.assistant/hub_padroes/script/checar_base_campanha) |
| prompt | briefing para o chat | [`prompt/template.md`](../../../ambiente_fonte/.assistant/hub_padroes/prompt/template.md) | [`analisar_campanha`](../../../ambiente_fonte/.assistant/hub_padroes/prompt/analisar_campanha) |
| skill | método para a Genie | [`skill/template.md`](../../../ambiente_fonte/.assistant/hub_padroes/skill/template.md) | [`skill/exemplo`](../../../ambiente_fonte/.assistant/hub_padroes/skill/exemplo) |
| notebook | demonstrar execução | [`notebook/template.py`](../../../ambiente_fonte/.assistant/hub_padroes/notebook/template.py) | notebooks dos exemplos acima |

O link da coluna Template abre o **molde vazio**. O da coluna Exemplo abre um
**preenchido didático** (campanha sintética). Não importe o exemplo em trabalho
real.

**Como escolher antes de copiar.** Se o artefato recebe DataFrame e devolve
resultado → snippet. Se recebe **endereço** (nome de tabela) → script. Se é
texto para colar no chat → prompt. Se a Genie deve carregar sozinha → skill.

---

<a id="fluxo-recomendado"></a>

## Fluxo recomendado

Necessidade → escolher tipo e ler o template inteiro → preencher contrato e
exemplo → validar forma e links → revisar conteúdo.

<a id="como-ler-o-template"></a>

### Como ler o template

Anexe-o no chat (`@` / Add Context) ou abra o arquivo. Sem isso, você trabalha
de memória e o formato muda entre versões.

<a id="o-que-preencher"></a>

### O que preencher

Objetivo, público, entradas, saída, limites, exemplo. O contrato mínimo da
seção abaixo é a lista de conferência.

<a id="duas-rotas"></a>

### Duas rotas

**Manual.** Copie o template para a pasta certa e siga o checklist.

**Com Genie:**

```text
@hub-ml-criar-objeto

Crie um snippet para taxa de resposta da campanha usando o template de
hub_padroes/snippet. Primeiro confirme nome, público, entradas, saída,
limites e exemplo. Não escreva arquivos até eu aprovar o plano.
```

`@hub_padroes/...` só funciona se o arquivo estiver no contexto. Não trate
uma string fictícia como se já estivesse selecionada.

<a id="como-criar-um-exemplo-que-comprova-o-contrato"></a>

### Como criar um exemplo que comprova o contrato

O exemplo precisa exercitar a API, não só importar. Dados sintéticos, resultado
observável, o que o número não prova.

<a id="como-encaminhar-a-revisão"></a>

### Como encaminhar a revisão

Forma (pasta, `__init__`, nome do módulo) no validador; conteúdo com revisor
humano. Skill nova: forward tests.

---

<a id="como-diferenciar-os-tipos"></a>

## Como diferenciar os tipos

| Se o artefato… | Tipo |
|---|---|
| explica uma coleção ou fluxo | README |
| oferece função importável | snippet |
| diagnostica um recurso endereçado | script |
| estrutura um pedido para o chat | prompt |
| ensina ao agente um workflow | skill |
| demonstra execução | notebook |

O mesmo tema de campanha atravessa os tipos sem duplicá-los: o snippet calcula
taxa de resposta; o script checa a base; o prompt pede a análise; a skill
ensina o método. Não são quatro cópias da mesma função.

---

<a id="contrato-mínimo"></a>

## Contrato mínimo

Todo objeto deixa explícitos:

1. objetivo e público;
2. entrada e pré-condições;
3. saída e critério de aceitação;
4. exemplo reproduzível;
5. limites, segurança e quando não usar;
6. relação com catálogo ou skill.

**Contrato insuficiente:** “função que calcula taxa.” Falta denominador,
tratamento de nulo, tipo de retorno.

**Contrato real do exemplar.** A API é `taxa_resposta_campanha(dados, *, coluna_segmento, coluna_resposta="respondeu", z=1.96, minimo_para_decisao=100) -> DataFrame`. A entrada é Spark, com uma linha por contato e resposta binária não nula. A saída contém uma linha por segmento, não um escalar entre zero e um.

Para acompanhar sem importar o exemplar como biblioteca produtiva, abra [o módulo didático](../../../ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/taxa_resposta_campanha.py) e [seu notebook completo](../../../ambiente_fonte/.assistant/hub_padroes/snippet/taxa_resposta_campanha/exemplo_taxa_resposta_campanha.py). Execute a preparação de caminho daquele notebook, ou use o bloco abaixo em uma sessão Spark autorizada com `.assistant` já no `sys.path`:

```python
from pyspark.sql import SparkSession
from hub_padroes.snippet.taxa_resposta_campanha import taxa_resposta_campanha
spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
contatos = spark.createDataFrame(
    [("segmento_a", 1 if i < 2 else 0) for i in range(10)],
    "segmento string, respondeu int",
)
taxas = taxa_resposta_campanha(contatos, coluna_segmento="segmento")
linha = taxas.collect()[0].asDict()  # coleta limitada: um único segmento
assert linha["contatados"] == 10
assert linha["respostas"] == 2
assert linha["taxa_pct"] == 20.0
assert linha["decidivel"] is False
assert linha["ic_inferior_pct"] == 5.67
assert linha["ic_superior_pct"] == 50.98
assert linha["largura_ic_pp"] == 45.32
print(linha)
```

**Leitura do resultado.** Duas respostas em dez contatos são 20%. `ic_inferior_pct` e `ic_superior_pct` apresentam a incerteza pelo intervalo de Wilson; `largura_ic_pp` está em pontos percentuais. Com `z=1.96`, os limites arredondados são aproximadamente 5,67% e 50,98%, e a largura 45,32 pontos. A amostra é pequena: a taxa pontual não basta para alocar orçamento. `decidivel=False` decorre do mínimo configurado de 100, não de uma regra estatística universal.

**Entradas inválidas.** A função rejeita resposta nula ou fora de 0/1, coluna ausente, `z` fora de `(0, 5]` e mínimo não positivo. Não atribua ao módulo a API fictícia `taxa_resposta(...)` nem uma checagem de denominador passado como parâmetro: esse denominador é a contagem dos contatos agrupados.

**Variação resolvida.** Acrescentar outros dez contatos, todos sem resposta, ao mesmo segmento muda a taxa para `2 / 20 × 100 = 10%`; não preserve os 20% do caso anterior. O teste de estrutura verifica formato, mas a revisão de domínio verifica se “um contato” é realmente o denominador adequado.

**Exercício de fronteira.** Troque uma resposta por nulo: a chamada deve rejeitar a entrada. Explique por que converter esse nulo em zero sem autorização mudaria o significado da taxa.


---

<a id="limites"></a>

## Limites

- A skill de **exemplo** fica fora de `.assistant/skills/` e **não** roteia.
  Copiá-la para `skills/` cria skill fantasma no chat.
- Exemplos de campanha são didáticos, não biblioteca de produção.
- Template não prova correção estatística, runtime nem autorização de dados.
- Não crie um sétimo tipo para diferença de conteúdo; veja se é recurso de um
  tipo existente.

**Se não funcionou.** Import do exemplar de campanha em pipeline real: pare e
use objeto revisado na biblioteca. Skill exemplo aparecendo no `@`: ela foi
parada no lugar errado — remova da pasta de descoberta.

---

<a id="onde-continuar"></a>

## Onde continuar

- Molde + exemplo da tabela do topo, não só a raiz do projeto.
- [Guia do ecossistema](../sprint-02-assistant/README.md)
- [Glossário](../../../ambiente_fonte/.assistant/GLOSSARIO.md)
- [Catálogo de helpers](../../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md)
- Checklist da skill: `../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md`
