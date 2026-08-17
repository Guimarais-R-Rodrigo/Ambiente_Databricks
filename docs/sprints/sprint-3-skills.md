# Sprint 3 — Skills renomeadas para `hub-ml-*`

Data: 2026-08-17 · Executor: Claude · Escopo: `ambiente_fonte/.assistant/skills/`
e todas as referências nas camadas vivas.

## O que mudou

As 12 skills passaram de `rodrigo-<tema>` para `hub-ml-<tema>`, com o `<tema>`
inalterado. O nome deixa de identificar o autor e passa a identificar o Hub — que
é o ponto da reestruturação: num ambiente de equipe, o autor não é a informação
relevante, e o nome antigo sugeria que aquilo pertencia a alguém.

A pasta ganhou também o `README.md` que nunca teve, no template novo.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 0 aviso(s) — skills: 12
render_simulado.py      OK: 202 arquivos
publicar_free.py        APROVADO: 0 problema(s) — skills 12/12, obsoletos 0
smoke test (job real)   84 verificações | 77 PASS | 0 FAIL | 7 opcionais ausentes
```

O smoke test é idêntico ao da Sprint 4 — renomear skill não toca na biblioteca,
e o número confirma.

## O roteamento não muda, e isso foi verificado

Antes de renomear, conferi que **nenhuma das 12 `description` contém
`rodrigo-`**. Como o Genie Code decide qual skill carregar lendo apenas esse
campo, a renomeação não altera a escolha automática: a certificação de 36/36
continua válida para os 12 casos positivos e os 12 negativos.

O que muda é a `@menção`. `@rodrigo-eda-profissional` deixou de existir e
`@hub-ml-eda-profissional` passou a valer. **Os 12 testes de menção precisam ser
refeitos** — é a única parte da certificação que a renomeação invalida.

## A limpeza remota, de novo indispensável

Depois de publicar, o workspace tinha **25 pastas** sob `skills/`:

```text
pastas de skill no workspace ANTES da limpeza: 25
pastas DEPOIS: 13
```

Doze eram as novas, doze eram as antigas sobrevivendo, e a décima terceira é o
`README.md`. Sem o passo de remoção, o Genie Code veria **24 skills com
`description` idêntica duas a duas** — exatamente a colisão de roteamento que os
forward tests existem para detectar, criada pela própria reestruturação.

A auditoria do plano previu este cenário com precisão, e é a terceira sprint em
que o passo se prova necessário. Vale registrar o padrão: `import-dir
--overwrite` sobrescreve e nunca apaga, então **toda sprint que renomeia ou
remove precisa da limpeza remota antes da conferência**.

## Escopo da renomeação

213 ocorrências em 64 arquivos das camadas vivas. Ficaram intactos, com a nota de
"nomenclatura da época" que aponta para o ADR-0006:

- `docs/testes/forward/resultados/` — registro do que foi executado em 14/08,
  com os nomes que existiam então;
- `docs/auditoria/`, `docs/handoffs/`, `CHANGELOG.md` e os ADRs anteriores.

`docs/testes/forward/roteiro.md` **foi** atualizado, porque é instrumento
reutilizável e não registro: quem for refazer os testes de menção precisa dos
nomes atuais.

## O README da pasta `skills/`

É o único README do Hub que abre com um aviso de estrutura **nativa**. Todo o
resto do ecossistema exige ação manual; esta pasta é a exceção, e confundir isso
é o mal-entendido mais provável de quem chega.

Ele registra três coisas que surpreendem quem usa pela primeira vez: que o corpo
do `SKILL.md` não influencia o roteamento, que alterar uma `description` invalida
a certificação, e que existem skills nativas da Databricks convivendo com estas —
observação que veio de um teste real, em que `data-sampling` foi carregada no
lugar de `eda-profissional` num pedido de análise direta.

## O que fica para a auditoria

- Se sobrou referência ao nome antigo em camada viva, em qualquer forma — link,
  crase, string, bloco de código.
- Se a fronteira entre renomear e preservar está no lugar certo, agora que
  `roteiro.md` foi atualizado e `resultados/` não.
- Se o README novo descreve a pasta corretamente, incluindo a afirmação sobre
  skills nativas coexistindo.
- Se algum `SKILL.md` cita outra skill pelo nome no corpo e ficou inconsistente.
- Se o `@hub-ml-*` funciona de fato no chat — só um teste no navegador responde,
  e é o que o Rodrigo precisa fazer.
