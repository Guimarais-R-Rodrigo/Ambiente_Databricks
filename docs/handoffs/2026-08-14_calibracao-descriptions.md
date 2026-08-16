# Handoff — calibração das descriptions

Data: 2026-08-14 · De: sessão Claude · Para: qualquer IA ou pessoa que altere uma skill

## Estado atual

Roteamento das 12 skills certificado em 36/36 nos forward tests
(`docs/testes/forward/`, rodadas 1 e 2). **Nenhuma `description` foi alterada em
nenhuma rodada**: o pacote entregue pela auditoria do Codex passou como estava.
As duas falhas da rodada 1 eram do instrumento de teste — prompts que citavam
"este notebook" sem que houvesse um —, corrigidas com prompts v2 autocontidos.

## Em andamento / bloqueado

Nada bloqueado. Dois itens de vigilância abertos, ambos **sem ação decidida**,
observados durante os testes e não reproduzidos desde então:

1. Pedido de "features que pesam no score" em linguagem executiva roteia para
   `monitorar-modelo` em vez de `explicar-modelo`. Defensável — o vocabulário
   executivo se parece com acompanhamento —, mas vale observar se atrapalha no
   uso real.
2. `comentar-notebook` responde a "células `%md`" mas **não** a "markdown de
   documentação". A description cobre o vocabulário técnico e não o coloquial.
   Registrado na rodada 2 como `11N-r2`, aprovado em sentido fraco: a skill
   errada não carregou, mas a ideal também não.

## Decisões tomadas nesta sessão

- Não alterar nenhuma `description` com base nos dois itens acima. Um único
  caso observado não justifica mexer numa certificação de 36/36; a alternativa
  seria calibrar contra o instrumento de teste em vez do uso real.

## Próximos passos recomendados (em ordem)

1. Observar os dois itens no uso cotidiano antes de mexer em qualquer
   `description`.
2. Se um deles atrapalhar de fato, ajustar **somente** aquela `description` e
   repetir os testes daquela skill e das que competem com ela no mesmo
   vocabulário — não a bateria inteira.
3. Registrar o resultado em `docs/testes/forward/resultados/` e atualizar o
   número do gate se ele mudar.

## Armadilhas conhecidas

**Alterar uma `description` invalida a certificação.** Os testes precisam ser
refeitos para a skill alterada e para as que disputam o mesmo vocabulário.
Editar uma `description` "de passagem", junto de outra mudança, é exatamente
como a certificação se perde sem ninguém notar — e nada no ciclo de validação
acusa isso: `validate_assistant.py` confere que a `description` existe, nunca
que ela ainda roteia.
