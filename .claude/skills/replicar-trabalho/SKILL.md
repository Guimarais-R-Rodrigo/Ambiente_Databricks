---
name: replicar-trabalho
description: >-
  Conduz a replicação do ecossistema certificado para o workspace corporativo,
  onde não há CLI. Use quando o pedido envolver levar skills, instruções ou
  helpers para o trabalho, atualizar o que já está lá, ou preparar a passagem
  para squad.
---

# Replicar no workspace do trabalho

Procedimento completo: [docs/playbooks/replicacao-trabalho.md](../../../docs/playbooks/replicacao-trabalho.md).

## Antes de liberar a replicação

Confirmar, na origem, que todos os itens abaixo estão satisfeitos:

| Pré-requisito | Como verificar |
|---|---|
| Fonte válida | `python tools/validate_assistant.py` aprovado |
| Simulado atual | `python tools/render_simulado.py --write` no commit a replicar |
| Runtime verificado | resultado em `docs/testes/spark/` da versão corrente |
| Roteamento certificado | resultado em `docs/testes/forward/` da versão corrente |
| Sem identificador corporativo | o validador cobre conteúdo e caminho |

Faltando qualquer um, resolver antes — replicação não é o momento de descobrir
defeito.

## Guardrails

- O username do trabalho nunca entra em arquivo versionado nem em nome de pasta
  renderizada; `tools/render_simulado.py` recusa esse parâmetro (ADR-0009).
- Backup do ambiente atual do trabalho antes de remover qualquer coisa: sem CLI,
  é o único rollback disponível.
- Skills antigas de mesmo nome são removidas, não sobrepostas.
- Correção descoberta no trabalho volta ao `ambiente_fonte/`; nunca fica apenas
  no workspace.
- Compartilhamento com a squad exige auditoria `A1+` e perfil administrativo.

## Ao encerrar

Registrar no `CHANGELOG.md` o commit replicado e o resultado dos testes de
aceitação, sem identificadores. Divergência de comportamento entre laboratório e
trabalho vira linha na matriz de `.claude/rules/free-vs-trabalho.md`.
