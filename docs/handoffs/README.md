# Handoffs — continuidade entre sessões

Handoff registra o estado que um commit não explica: o que está firme, o que
ficou bloqueado, o que já falhou e qual é a próxima ação verificável.

## Quando criar

- tarefa estrutural termina incompleta;
- decisão depende de pessoa, cota ou ambiente externo;
- outra sessão/agente assumirá o trabalho;
- reconstruir o estado pelo Git levaria mais de alguns minutos.

Não use handoff como diário. Trabalho concluído vai para `CHANGELOG.md` e
evidência datada.

## Estrutura mínima

```markdown
# Handoff — <tema>

Data: YYYY-MM-DD · De: <origem> · Para: <destino>

## Estado atual
<feito e verificado, com caminhos/evidência>

## Em andamento / bloqueado
<o que falta e qual condição destrava>

## Próximos passos recomendados
1. <ação objetiva e critério de sucesso>

## Armadilhas conhecidas
<o que já foi tentado ou parece seguro, mas não é>
```

O template completo está em `.claude/templates/handoff.md`.

## Registros

| Data | Tema | Relevância atual |
|---|---|---|
| 2026-08-14 | [calibração das descriptions](2026-08-14_calibracao-descriptions.md) | ler antes de alterar `description` de skill |

Esse handoff preserva os pontos de vigilância dos testes de roteamento e explica
por que as falhas do instrumento não levaram a alterações indevidas nas skills.

[Voltar ao índice de documentação](../README.md)
