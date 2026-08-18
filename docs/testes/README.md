# `docs/testes/` — as duas coisas que só o ambiente real responde

Duas famílias de teste, com naturezas diferentes. Confundi-las é a causa do erro
mais caro deste projeto: tratar "passou aqui" como "vai passar lá".

| Pasta | Pergunta que responde | Quem executa | Resultado |
|---|---|---|---|
| [`spark/`](spark/) | o helper **executa** no runtime real? | um job no Databricks Free | JSON por execução, em `spark/resultados/` |
| [`forward/`](forward/) | o Genie Code **carrega a skill certa**? | uma pessoa, no chat | Markdown por rodada, em `forward/resultados/` |

O de Spark é automatizável e roda por `tools/spark_smoke_test.py`. O de
roteamento **não é**: depende de um modelo decidindo sozinho qual skill usar, e
não existe API para perguntar isso — a pessoa cola o prompt e anota o que veio.

## Por que os dois existem, se o validador já passa

Porque *importável* não é *executável*, e este repositório aprendeu a diferença
por três caminhos distintos:

| Causa | Exemplo real | Quem pega |
|---|---|---|
| biblioteca ausente do runtime | `tabulate`, exigido por `DataFrame.to_markdown()` | só a execução |
| dependência delegada | `jinja2`, exigido por `DataFrame.style` | só a execução |
| API da plataforma não exposta | `VectorAssembler` sob Spark Connect | só a execução |

Nenhuma das três aparece em análise estática: o `import` do topo passa, e o erro
só nasce na chamada. Foi essa classe que virou o marcador `exec` do
[catálogo de helpers](../../ambiente_fonte/.assistant/CATALOGO_HELPERS.md).

## A regra que vale mais que qualquer resultado aqui

> **"Foi testado" tem data de validade em ambiente gerenciado.**

Não é retórica. Em **três dias**, três registros desta pasta venceram:

| Registro | Dizia | Passou a ser |
|---|---|---|
| `mlflow_run` | run completo aceito (14/08) | bloqueado no serverless (17/08) |
| `prophet` | sem combinação funcional conhecida | instala e ajusta modelo completo |
| instalação sem pin | derrubava o kernel | não se reproduziu |

Os registros de 14/08 **não estão errados** — descrevem o que era verdade então,
e por isso não são reescritos. A consequência prática é operacional: antes de
replicar no trabalho, **reexecute**; não confie no registro sozinho, por mais
recente que pareça.

## Como ler um resultado

```powershell
# Spark: cada arquivo é uma execução, com o veredito por helper
python -c "import json;d=json.load(open('docs/testes/spark/resultados/2026-08-14_ml_pesado.json',encoding='utf-8'));print(len(d),'entradas')"
```

Nos forward tests, o veredito é por caso, e há três por skill: positivo (a skill
certa carrega), negativo (um pedido parecido de outro domínio **não** a carrega)
e menção (`@nome-da-skill` força o carregamento).

## Estado dos gates

| Gate | Estado | Falta |
|---|---|---|
| Runtime Spark/ML | os 58 helpers exercitados no Free | reexecução antes de replicar |
| Roteamento | **36/39** — as 12 skills originais fecharam | os 3 casos da `hub-ml-criar-objeto` |

A décima terceira skill nasceu na Sprint 11 e nunca foi testada. Ela tem a
`description` mais ampla do conjunto, que é exatamente o perfil que rouba
roteamento das outras — é o teste mais informativo que resta.

## Fontes

- Método e vereditos do roteamento: `.claude/skills/forward-test-skills/SKILL.md`
- Matriz Free × trabalho, com as diferenças de runtime já observadas:
  `.claude/rules/free-vs-trabalho.md`
- Inventário de bibliotecas opcionais, com a prova de execução de cada uma:
  `ambiente_fonte/.assistant/hub_snippets/requirements-optional.txt`
- O que fazer com o resultado: [runbook de replicação](../playbooks/replicacao-trabalho.md)
