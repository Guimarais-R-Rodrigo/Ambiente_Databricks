# Skill Enforcement Framework — índice vivo

Este diretório concentra o planejamento e as evidências do Skill Enforcement Framework (SEF).

## Documentos canônicos

1. [PLANO_MESTRE.md](PLANO_MESTRE.md) — arquitetura e sequência original SE00–SE08.
2. [REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md](REVISAO_PLANO_2026-09-17_LOCAL_FIRST.md) — revisão operacional vigente a partir da SE02, incorporando o laboratório sintético, prioridade structural-first e regime local-first de certificação.
3. `SE00/` — baseline e instrumentos históricos.
4. `SE01/` — contrato verificável e capability experiment, concluída/integrada.
5. `SE02/` — preflight L2, em fechamento/certificação.
6. [SE02/RUNBOOK_FREE.md](SE02/RUNBOOK_FREE.md) — sequência operacional vigente para sincronizar o clone, certificar localmente, publicar/verify no Databricks Free e executar F02.

## Regra de leitura

O Plano Mestre original não é apagado nem reescrito para acomodar aprendizados posteriores. A revisão de 2026-09-17 é aditiva e governa, a partir dessa data, os pontos operacionais que ela altera explicitamente — em especial:

- prioridade structural-first após o L2;
- entrypoint estrutural como foco da SE03;
- micro-evals adversariais já na SE03;
- distinção entre correctness e canonical compliance;
- provenance progressiva das condições;
- certificação local-first durante desenvolvimento;
- mesmo certifier Python para local e GitHub Actions;
- GitHub Actions reservado para release candidate/Ready-for-review e pós-merge;
- branch sem PR aberta durante desenvolvimento de SE03 em diante;
- estados separados para local, laboratório sintético, Databricks Free e Actions.

## Regra operacional para novas sprints

A partir da SE03, o fluxo preferencial é:

```text
branch sem PR
  → implementação
  → gate local
  → screening sintético quando útil
  → Databricks Free
  → release candidate
  → abrir PR
  → GitHub Actions final
  → aceite
  → merge
  → certificação pós-merge
```

Uma PR Draft não deve ser usada como mecanismo principal de economia de CI, porque workflows transversais históricos podem continuar reagindo a `pull_request/synchronize`.

## Estado atual

- SE00: concluída e integrada;
- SE01: concluída e integrada;
- SE02: em certificação, `mode="audit"`, sem SE03 iniciada;
- SE03–SE08: não iniciadas.

A frente não deve declarar `FULLY_CERTIFIED` quando qualquer gate obrigatório estiver apenas `NOT_RUN` ou `DEFERRED_CREDIT`.
