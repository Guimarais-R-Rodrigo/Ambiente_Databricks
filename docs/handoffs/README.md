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

O esqueleto tem quatro partes que importam. O molde completo está em
`.claude/templates/handoff.md`:

```markdown
# Handoff — <tema>

Data: YYYY-MM-DD · De: <sessão/IA> · Para: <quem assume>

## Estado atual
<O que está feito e verificado, com caminhos de arquivo.>

## Em andamento / bloqueado
<O que ficou pela metade, e em quem ou em quê está travado.>

## Próximos passos recomendados
1. <passo objetivo e verificável>

## Armadilhas conhecidas
<O que parece óbvio mas quebra. Termine por aqui: é o que economiza
mais tempo de quem chega.>
```

O que separa um handoff útil de um resumo: ele distingue o que está firme do
que está aberto, não esconde o que ficou sem decisão, e fecha pela armadilha.

## Handoffs registrados

| Data | Tema | De → Para |
|---|---|---|
| 2026-08-14 | [Calibração das descriptions](2026-08-14_calibracao-descriptions.md) | sessão Claude → quem alterar uma skill |

Leia o de 2026-08-14 **antes de editar qualquer `description`**: ele registra os
dois únicos itens de vigilância abertos do projeto e por que nenhuma
`description` foi alterada apesar deles.
