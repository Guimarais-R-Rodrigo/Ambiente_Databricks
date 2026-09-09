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
| 2026-09-09 | [plano consolidado, pacotes T0 a T6](2026-09-09_plano-consolidado.md) | ler antes de mexer no escopo do validador ou retomar T3, T4 e T7 |

| 2026-09-09 | [correções Codex e retomada no PC](2026-09-09_correcoes-codex.md) | estado posterior à revisão; comandos para baixar e validar no Free |

O de 2026-08-14 preserva os pontos de vigilância dos testes de roteamento e explica
por que as falhas do instrumento não levaram a alterações indevidas nas skills. O de
2026-09-09 registra o que os pacotes T0 a T6 fecharam, o que continua bloqueado por
acesso e as armadilhas de plataforma encontradas ao executá-los.

[Voltar ao índice de documentação](../README.md)
