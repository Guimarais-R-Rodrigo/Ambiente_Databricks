# Handoffs

Um handoff é a passagem de contexto para quem assume o trabalho depois — outra
sessão, outra IA, ou você mesmo daqui a três semanas. Ele responde o que o
histórico de commits não responde: o que estava pela metade, o que parecia óbvio
e não era, e o que já foi tentado sem sucesso.

Escreva um quando uma tarefa estrutural ficar inacabada, quando uma decisão
depender de outra pessoa, ou quando reconstruir o estado a partir do changelog
levaria mais de alguns minutos. Um arquivo por handoff, nomeado
`YYYY-MM-DD_<tema>.md`, seguindo `.claude/templates/handoff.md`.

## Como um se parece

O formato fica claro vendo um. Versão curta, com as quatro partes que importam:

```markdown
# Handoff — calibração das descriptions

Data: 2026-08-14 · De: sessão Claude · Para: qualquer IA

## Estado atual
Roteamento certificado em 36/36 (`docs/testes/forward/`). Nenhuma description
foi alterada; o pacote do Codex passou como estava.

## Em andamento / bloqueado
Nada bloqueado. Dois itens de vigilância abertos, ambos sem ação decidida:
pedido de "features que pesam no score" em linguagem executiva vai para
monitoramento em vez de explicabilidade; `comentar-notebook` responde a
"células %md" mas não a "markdown de documentação".

## Próximos passos recomendados
1. Observar os dois itens no uso real antes de mexer em qualquer description.
2. Se um deles atrapalhar de fato, ajustar a description e repetir apenas os
   testes daquela skill.

## Armadilhas conhecidas
Alterar description invalida a certificação: os testes precisam ser refeitos
para a skill alterada e para as que competem com ela no mesmo vocabulário.
Editar description "de passagem", junto de outra mudança, é como a certificação
se perde sem ninguém notar.
```

Repare no que o exemplo faz: separa o que está firme do que está aberto, não
esconde o que ficou sem decisão, e termina pela armadilha — a informação que
economiza mais tempo de quem chega.

| Data | Tema | De → Para |
|---|---|---|
| — | (nenhum handoff registrado ainda) | — |
