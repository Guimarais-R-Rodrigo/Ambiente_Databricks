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

## Primeiro run real da candidata

Run `34908962030`, head `fb2d0eaf319a37a1a62e322e7f8458a47097b4f0`: **FAILURE preservado**.

A suíte V12 passou 26/26, as regressões V01–V12 passaram 483/483 e V00 passou 12/12. O validador estrutural/documental encontrou somente duas métricas stale no README raiz: `repo (identidade)` estava `1409` e mediu `1418`; `repo (links)` estava `1887` e mediu `1889`. O gate de escopo ficou `SKIP` por dependência da etapa anterior.

A correção não altera o validador: reconcilia os valores documentados com a saída medida e atualiza os documentos vivos que ainda diziam que V12 não havia iniciado.

## Bloqueio operacional atual

A primeira mutação real necessária para algumas jornadas não está autorizada pelo prompt que iniciou a V12. Assim, deploy de App, import de tema, alteração de workspace theme, alteração de ACL e publicação permanecem bloqueados até autorização explícita adicional.

O bloqueio é estado correto, não failure do código.

## Próximo gate

Reexecutar CI da candidata após a reconciliação documental. Depois, para avançar no ambiente, registrar operação, ambiente, risco, rollback e autorização antes da primeira mutação.