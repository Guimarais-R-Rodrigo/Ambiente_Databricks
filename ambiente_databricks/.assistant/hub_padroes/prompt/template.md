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
├── README.md                       # conceito, contexto e limites de uso
├── <nome_do_prompt>.md             # o briefing
└── exemplo_<nome_do_prompt>.py     # notebook de três partes
```

Sem `__init__.py`: prompt não é importado.

## O briefing

| Seção | Conteúdo |
|---|---|
| Cabeçalho | aviso de que não é auto-descoberto e a **skill recomendada**; para utilitário sem rota única, declarar as rotas possíveis |
| Por que existe | qual pedido informal ele substitui, e o que aquele pedido erra |
| Antes de colar | os `{{PLACEHOLDERS}}` a preencher, e por que cada um importa |
| Prompt pronto para colar | bloco de código `text`, sem nada além do texto a colar |
| O que conferir na resposta | as lacunas previsíveis do assistente |
| Limites | o que este prompt não alcança |

**Declare sempre a rota.** Normalmente é uma skill recomendada. Em utilitário sem
skill única, diga explicitamente que a escolha depende do objetivo, liste as
rotas possíveis e peça seleção explícita por `@` quando uma delas for escolhida. Isso esclarece intenção, mas não comprova carregamento, execução ou resultado. Registre o que foi realmente observado.

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

## O briefing e o preparo do notebook

O texto do briefing não roda; o notebook pode executar preparação e escrita. Para apenas preencher o pedido, dispense preparo desnecessário. A resposta depende da interação real.
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

Verifique também os requisitos específicos deste tipo:

```text
[ ] o cabeçalho declara a skill recomendada ou as rotas possíveis
[ ] todo placeholder tem uma frase dizendo por que importa
[ ] o bloco de colar não tem comentário nem instrução dentro
[ ] a parte 3 tem resposta real, com data e condição de captura
[ ] o roteamento observado está registrado
[ ] o README da seção lista este prompt
```

O exemplo preenchido está em
[`analisar_campanha/analisar_campanha.md`](analisar_campanha/analisar_campanha.md), com a resposta
real em [`exemplo/exemplo_analisar_campanha.py`](analisar_campanha/exemplo_analisar_campanha.py).

## README do objeto

Aplique o [molde de objeto](../readme/template_objeto.md); veja o
[exemplar](analisar_campanha/README.md). O README explica quando e por que usar
o briefing. Mantenha instruções de preenchimento, QA, limites e bloco colável
no prompt original. A navegação para o README fica fora desse bloco.
