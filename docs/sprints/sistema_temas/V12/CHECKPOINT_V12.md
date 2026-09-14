# Checkpoint V12 — preparação para homologação

Data: 14/09/2026.

Branch: `codex/temas-v12-homologacao-jornadas-20260914`.

Base congelada: `d106ef3158e5827a2eec3aa183dbb3b47885c960`.

## Estado

V12 iniciada em branch isolada. V11 permanece fechada e não foi reaberta.

Este checkpoint distingue explicitamente:

- **Git/local**: pode ficar verde antes do ambiente;
- **Databricks environment**: não executado nesta fase;
- **Human/UAT**: não executado nesta fase.

Nenhum desses estados será promovido por inferência.

## Decisões preservadas

- `ResolvedTheme` segue fonte configurável de verdade;
- `context="aibi"` segue reservado;
- matriz V11 continua 48 tokens = 3 `translated`, 23 `approximated`, 22 `unsupported`;
- somente `widget.background`, `visualization.categorical_palette` e `widget.corner_radius` são diretos;
- JSON nativo não é inventado;
- export real precisa de SHA-256 e binding revisado;
- fixture sintético não é importável;
- workspace theme e dashboard theme continuam escopos distintos;
- import/select e publish continuam gates distintos.

## Bloqueio operacional atual

A primeira mutação real necessária para algumas jornadas não está autorizada pelo prompt que iniciou a V12. Assim, deploy de App, import de tema, alteração de workspace theme, alteração de ACL e publicação permanecem bloqueados até autorização explícita adicional.

O bloqueio é estado correto, não failure do código.

## Próximo gate

Concluir CI local/GitHub da candidata. Depois, para avançar no ambiente, registrar operação, ambiente, risco, rollback e autorização antes da primeira mutação.
