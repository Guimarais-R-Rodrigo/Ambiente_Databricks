# Coordenação local, contenção e evidência de campanhas

Módulos repo-side da coordenação SEF/SER. Não são skills nativas nem serviços
iniciados automaticamente. A existência de uma receita não autoriza subprocessos,
instalação, acesso remoto ou promoção de policy.

| Grupo | Arquivos principais | Responsabilidade |
|---|---|---|
| Contratos e configuração | `contract.py`, `registry.py`, `schemas/`, `command_registry.json`, `resource_profiles.json`, `role_profiles.json` | Validar tarefas/resultados, comandos e limites declarados |
| Cobertura | `coverage.py`, `coverage_registry.json` | Inventariar identidades e coleta; não executar nem homologar testes |
| Preparação | `preflight.py`, `bundle.py`, `freeze_prepare.py`, `prepare_pilot.py` | Conferir pré-condições e preparar entradas/saídas locais |
| Execução e contenção | `process.py`, `launcher.py`, `scheduler.py`, `lease.py`, `sandbox_exec.py` | Coordenar processos, concorrência, leases e escopo local |
| Probes do host | `host_probe.py`, `host_qualification.py`, `sandbox_probe.py` | Investigar capacidades; dependem de modo, sistema e escopo escolhido |
| Piloto e verificação | `pilot_worker.py`, `pilot_verify.py`, `pilot_campaign.json`, `pilot_global_stop_campaign.json`, `verifier.py` | Fixtures/campanhas e conferência dos resultados; não são rollout implícito |
| Linhagem | `round_identity.py`, `b0_release.py` | Identidade de rodada e fronteira da release B0 |

Entrada de leitura/coleta, a partir da raiz:

```sh
python -B -m tools.skill_enforcement.parallel.coverage
```

Para executar uma campanha, siga seu owner e a receita autorizada do registro.
Não rode scheduler, probes ou qualificação só por estarem neste índice. Arquivos
B0 e de piloto preservam limites datados; resultado antigo não qualifica HEAD.
A composição corrente dos testes pertence a [ci_local.py](../../ci_local.py), aos
[tests](../../tests/README.md) e ao [guia SEF](../README.md).
História/estado da campanha: [SER](../../../docs/sprints/skill_enforcement_rollout/README.md).
