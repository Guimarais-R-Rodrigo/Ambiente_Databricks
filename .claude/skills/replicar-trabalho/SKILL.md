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

## Procedimento vigente

Use o runbook e checklist atualizados, com kit mínimo de commit fixo, staging,
notebook de aceite por etapas e testes humanos separados. Gere com
`python tools/kit_transicao_trabalho.py --output .artifacts/kit-trabalho`.
O código do notebook é `tools/aceite_trabalho.py`; a versão IPYNB é materializada
no pacote. Não se publica `tools/` no Hub.

O núcleo técnico testa FILEs, imports e contratos sintéticos. Roteamento da Genie,
instruções e aparência exigem evidência humana. PENDENTE/NAO_TESTADO não são PASS.
Um resultado antigo do Free não certifica as instruções atuais nem o trabalho.
Backup completo usa Zip - Source, não DBC sozinho. Promova apenas as cinco pastas
Hub e skills geridas, preservando MCP e conteúdo alheio; instruções por último.

## Guardrails

- Sem CLI no trabalho; nenhuma credencial corporativa, username ou path real no Git.
- Não reintroduzir rascunhos descartados; preservar Manual, instruções e apresentação escolhidos.
- MLflow e consultas UC começam desativados; ativação requer escopo autorizado.
- Não fazer instalação ou exclusão automática a partir do notebook de aceite.
- Testar novamente depois da promoção e usar nova sessão Python/chat.
- Compartilhamento com squad exige governança própria, fora da instalação pessoal.

## Ao encerrar

Registre commit, escopo e resultados sanitizados, sem alegar homologação do destino
antes de executá-la. Qualquer correção volta à fonte. Backup e erros corporativos
brutos permanecem no ambiente autorizado.
