# B0 — infraestrutura comum da execução paralela SER

Estado de autoria: **IMPLEMENTAÇÃO REPO-SIDE PREPARADA / QUALIFICAÇÃO LOCAL PENDENTE**.

O B0 implementa governança, contratos runtime, executor/verificador comum, empacotamento RAW/SHARE, inventário de cobertura, qualificação de host e piloto sintético. Não promove skills.

## Pacotes

- B0.1: ADR-0023 + navegação SER + plano detalhado versionado.
- B0.2: schemas fechados, registry de comandos e inventário de cobertura por AST.
- B0.3: executor/scheduler com DAG, concorrência limitada, locks, logs e detecção de mutação.
- B0.4: verificador independente + manifesto de evidência + SHARE/ZIP seguro.
- B0.5: qualificação de host; sandbox/modelos/permissões precisam ser executados localmente.
- B0.6: piloto sintético preparado com duas tarefas independentes, um FAIL deliberado e dependente bloqueado.
- B0.7: só pode ser marcado LOCAL_QUALIFIED após campanha local, metatests, inventário por método e auditoria.

## Próximo gate

Rodar localmente a missão B0-LOCAL-QUALIFICATION. Até lá:

```text
B0_AUTHORING = PREPARED
B0_LOCAL_QUALIFICATION = NOT_RUN
B0_RELEASE = NOT_AUTHORIZED
SER02_SER14_EXECUTION = NOT_STARTED
POLICY_PROMOTION = NONE
```
