# Template — pasta de prompt

> Um dos **seis** tipos de objeto do Hub, e a lista é fechada. Prompt é texto
> para colar num chat; se o que você tem é código a importar, veja
> [`../snippet/template.md`](../snippet/template.md). O que estiver em
> `analisar_campanha/` é referência de forma.

Use quando o objeto for um **briefing pronto para colar** num chat do Genie Code.
Um prompt do Hub não é um atalho para digitar menos: é um formulário que força a
declarar o que o pedido informal esquece — e é o esquecimento que produz resposta
plausível e errada.

```text
hub_prompts/<nome_do_prompt>/
├── <nome_do_prompt>.md             # o briefing
└── exemplo_<nome_do_prompt>.py     # notebook de três partes
```

Sem `__init__.py`: prompt não é importado.

## O briefing

| Seção | Conteúdo |
|---|---|
| Cabeçalho | aviso de que não é auto-descoberto, e a **skill recomendada** |
| Por que existe | qual pedido informal ele substitui, e o que aquele pedido erra |
| Antes de colar | os `{{PLACEHOLDERS}}` a preencher, e por que cada um importa |
| Prompt pronto para colar | bloco de código `text`, sem nada além do texto a colar |
| O que conferir na resposta | as lacunas previsíveis do assistente |
| Limites | o que este prompt não alcança |

**Declare sempre a skill recomendada.** Depender do roteamento automático para um
pedido ambíguo é apostar: em teste real, um pedido de análise direta levou o
assistente a preterir a skill do Hub em favor de uma nativa da plataforma — com
argumento defensável. O prompt existe para remover essa aposta.

### Sobre os placeholders

Cada `{{PLACEHOLDER}}` precisa de uma frase dizendo **por que ele muda a
resposta**. Placeholder sem justificativa vira campo que se preenche no
automático, e aí o formulário não fez nada.

O exemplo: declarar o orçamento em número de contatos, e não em reais, é o que
transforma "qual segmento responde mais" em "onde alocar" — e é o que impede o
assistente de recomendar um segmento de 28 pessoas.

### "O que conferir na resposta" não é desconfiança

É a seção mais valiosa e a que quase sempre falta. As lacunas de um assistente
competente são **sistemáticas e previsíveis**, e portanto verificáveis por quem
lê. Liste de duas a quatro, cada uma com o motivo de importar.

## O notebook, que não executa

Prompt não roda: a resposta vem de uma interação que notebook nenhum reproduz.
O formato é de três partes:

1. **Preparo executável** — cria a base a que o prompt se refere, para que quem
   lê possa colar o prompt e obter resposta de verdade. Esta parte roda e tem
   saída.
2. **O prompt preenchido** — o texto exato, sem placeholders.
3. **A resposta real**, capturada num chat, com comentário sobre o roteamento
   observado, o que o assistente fez bem e o que deixou de fora.

**A parte 3 exige uma pessoa.** Não há como gerá-la, e resposta inventada é pior
que resposta nenhuma — ela ensina que o assistente faz algo que ele não faz.

Registre também **qual skill foi carregada**: é a única forma de saber se o
roteamento está fazendo o que se espera fora da bateria de forward tests.

## Antes de dar por pronto

O checklist é **um só para os seis tipos**, e mora em
[`skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md`](../../skills/hub-ml-criar-objeto/templates/checklist-objeto-novo.md).
Ele separa o que um terceiro consegue conferir do que é juízo de quem escreveu, e
tem um bloco específico para prompt.

A lista abaixo era a antiga, preservada porque um item dela não estava no
canônico — os demais foram absorvidos:

```text
[ ] o cabeçalho declara a skill recomendada
[ ] todo placeholder tem uma frase dizendo por que importa
[ ] o bloco de colar não tem comentário nem instrução dentro
[ ] a parte 3 tem resposta real, com data e condição de captura
[ ] o roteamento observado está registrado
[ ] o README da seção lista este prompt
```

O exemplo preenchido está em
[`analisar_campanha/analisar_campanha.md`](analisar_campanha/analisar_campanha.md), com a resposta
real em [`exemplo/exemplo_analisar_campanha.py`](analisar_campanha/exemplo_analisar_campanha.py).
