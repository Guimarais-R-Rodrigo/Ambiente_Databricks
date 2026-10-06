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

O template completo está em `docs/ai/templates/handoff.md`.

## Registros

Estados abaixo foram reconciliados com os fechamentos SE07/SE08 e SER. “Consumido” não apaga residual técnico; “referência histórica” não autoriza retomar a operação.

| Data | Tema | Disposição e continuidade |
|---|---|---|
| 2026-09-22 | [SE08, complemento de policy I/O e consolidação repo-side](2026-09-21_se08-policy-io-complemento.md) | consumido no [fechamento SE08](../sprints/skill_enforcement/SE08/README.md); operação posterior em [SER](../sprints/skill_enforcement_rollout/README.md) |
| 2026-09-21 | [SE07, corretiva de cleanup após auditoria](2026-09-21_se07-auditoria-storage-cleanup.md) | referência histórica com residual: [SE07 encerrada](../sprints/skill_enforcement/SE07/README.md), cleanup FAIL preservado, WinError32 não declarado resolvido |
| 2026-09-21 | [SE07, piloto L3 README](2026-09-21_se07-criar-objeto-l3-readme-piloto.md) | consumido; piloto e policy L2 pertencem àquela data; [SER01](../sprints/skill_enforcement_rollout/SER01/README.md) registra integração L3 posterior |
| 2026-09-21 | [SE07, corretiva F-04](2026-09-21_se07-f04-corretiva.md) | consumido pelo [fechamento SE07](../sprints/skill_enforcement/SE07/README.md); preservar SUP-F04-01/02/03 e evidências |
| 2026-08-14 | [calibração das descriptions](2026-08-14_calibracao-descriptions.md) | referência histórica de vigilância ao alterar `description` |
| 2026-09-09 | [plano consolidado, pacotes T0 a T6](2026-09-09_plano-consolidado.md) | referência histórica; confirmar necessidade e autorização antes de retomar T3/T4/T7 |
| 2026-09-09 | [correções Codex e retomada no PC](2026-09-09_correcoes-codex.md) | referência histórica da revisão; publicação atual segue [playbooks](../playbooks/README.md) |

O de 2026-08-14 preserva os pontos de vigilância dos testes de roteamento e explica
por que as falhas do instrumento não levaram a alterações indevidas nas skills. O de
2026-09-09 registra o que os pacotes T0 a T6 fecharam, o que continua bloqueado por
acesso e as armadilhas de plataforma encontradas ao executá-los.

[Voltar ao índice de documentação](../README.md)
