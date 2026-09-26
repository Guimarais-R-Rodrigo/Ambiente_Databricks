# Contexto — Ambiente de trabalho (Azure Databricks)

- Azure Databricks corporativo; Genie Code habilitado.
- **Sem Databricks CLI** e em outro computador: toda replicação é manual
  (upload/Git folder pela UI), seguindo o runbook (fase 4 do roadmap).
- Username corporativo é um identificador de rede do banco — usar sempre o
  placeholder `<username-trabalho>`; o valor real nunca entra em arquivo
  versionado (motivo da quarentena do `Ambiente_Antigo/`, ADR-0003).
- Estruturas alvo no trabalho:
  - `/Users/<username-trabalho>/.assistant_instructions.md`
  - `/Users/<username-trabalho>/.assistant/skills/` (fase pessoal)
  - `Workspace/.assistant/skills/` (fase squad — exige admin/revisão)
- Dados reais e governados (Unity Catalog); regras de PII e compliance do banco
  se aplicam a qualquer exemplo ou output.
- Só o trabalho valida: runtime real, permissões, ACLs, políticas corporativas.
