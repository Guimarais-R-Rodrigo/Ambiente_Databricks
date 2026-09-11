# `hub_padroes/` — templates do Hub

> **HUB · CONSULTA MANUAL.** Esta coleção não é auto-descoberta pelo Genie Code.
> Anexe o template com `@` ou use `@hub-ml-criar-objeto` para aplicar o fluxo.

> **Rascunho de sprint 8 — não publicado.** Destino previsto: `ambiente_fonte/.assistant/hub_padroes/README.md`.

Quando várias pessoas criam material, cada uma inventa uma pasta diferente.
Um **molde** (template) fixa estrutura e o que precisa ser revisado. Ele **não**
certifica que a fórmula ou o texto estão corretos.

---

## Escolha o objeto

Há **seis** tipos. `auditoria/` e `output/` são padrões de processo, não tipos
novos.

| Quero criar… | Necessidade típica | Template | Exemplo preenchido |
|---|---|---|---|
| README | explicar uma pasta | [`readme/template.md`](readme/template.md) | [`readme/exemplo.md`](readme/exemplo.md) |
| snippet | função importável | [`snippet/template.md`](snippet/template.md) | [`taxa_resposta_campanha`](snippet/taxa_resposta_campanha/) |
| script | diagnóstico de um recurso | [`script/template.md`](script/template.md) | [`checar_base_campanha`](script/checar_base_campanha/) |
| prompt | briefing para o chat | [`prompt/template.md`](prompt/template.md) | [`analisar_campanha`](prompt/analisar_campanha/) |
| skill | método para a Genie | [`skill/template.md`](skill/template.md) | [`skill/exemplo`](skill/exemplo/) |
| notebook | demonstrar execução | [`notebook/template.py`](notebook/template.py) | notebooks dos exemplos acima |

O link da coluna Template abre o **molde vazio**. O da coluna Exemplo abre um
**preenchido didático** (campanha sintética). Não importe o exemplo em trabalho
real.

**Como escolher antes de copiar.** Se o artefato recebe DataFrame e devolve
resultado → snippet. Se recebe **endereço** (nome de tabela) → script. Se é
texto para colar no chat → prompt. Se a Genie deve carregar sozinha → skill.

---

## Fluxo recomendado

Necessidade → escolher tipo e ler o template inteiro → preencher contrato e
exemplo → validar forma e links → revisar conteúdo.

### Como ler o template

Anexe-o no chat (`@` / Add Context) ou abra o arquivo. Sem isso, você trabalha
de memória e o formato muda entre versões.

### O que preencher

Objetivo, público, entradas, saída, limites, exemplo. O contrato mínimo da
seção abaixo é a lista de conferência.

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

### Como criar um exemplo que comprova o contrato

O exemplo precisa exercitar a API, não só importar. Dados sintéticos, resultado
observável, o que o número não prova.

### Como encaminhar a revisão

Forma (pasta, `__init__`, nome do módulo) no validador; conteúdo com revisor
humano. Skill nova: forward tests.

---

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

**Melhor:** “`taxa_resposta(df, col_enviados, col_respostas) -> float` entre 0 e
1; recusa denominador zero; exemplo com 10 envios e 2 respostas = 0,20.” Isso
ainda não é mudança de algoritmo — é o formato que o molde exige. A fórmula
correta continua revisão de domínio.

O objeto didático `taxa_resposta_campanha` existe para forma; não invente
extensão do contrato sem ler o código.

---

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

## Onde continuar

- Molde + exemplo da tabela do topo, não só a raiz do projeto.
- [Guia do ecossistema](../README.md)
- [Glossário](../GLOSSARIO.md)
- [Catálogo de helpers](../CATALOGO_HELPERS.md)
- Checklist da skill: `../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md`
