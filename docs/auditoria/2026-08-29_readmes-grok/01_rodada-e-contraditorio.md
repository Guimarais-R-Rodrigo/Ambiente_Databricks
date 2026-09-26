# Auditoria dos READMEs — Grok 4.6 e contraditório Codex

Data: 2026-08-29

Escopo: documentação viva após o commit `7e996e0`

Execução: somente leitura, sandbox `read-only`
Modelo auditor: `grok-4.6`, raciocínio `xhigh`

## Método

O Grok primeiro construiu um dossiê de compreensão e só depois avaliou os
READMEs. Leu entradas canônicas, 20 READMEs ativos, ADRs 0006–0009, auditoria A2,
testes e estado em disco. Claims de plataforma foram confrontados com
documentação oficial. Nenhum arquivo ou workspace foi alterado.

Limitação: a sessão não recuperou o diff `7e996e0^..7e996e0`; a auditoria avaliou
o resultado em disco e o changelog. O Codex conferiu os achados diretamente nos
arquivos e submeteu ao Grok um contraditório final.

## Consenso

| Prioridade | Achado | Decisão |
|---|---|---|
| P1 | `docs/testes/README.md` ainda mandava republicar o redesenho já publicado | procedente |
| P1 | ordem do ciclo divergia entre README e playbook | procedente |
| P2 | runbook/checklist diziam que o glossário estava dentro do README | procedente, encontrado no contraditório |
| P2 | catálogo não apontava para o smoke vigente em Spark 4.2.0 | procedente |
| P2 | `constants.styles` parecia fonte efetiva, embora seja espelho morto | procedente |
| P3 | ZIP atual não existia | improcedente; o pacote `7e996e0` existe |
| P3 | rodada histórica de 7 opcionais parecia inventário vigente | parcial; preservar número e reforçar data |
| P3 | inventário da skill planejada tinha dois donos | procedente, baixo impacto |
| P3 | catálogo repetia a linha agregada de cores/emojis/estilos | procedente |
| P3 | alcance e precedência de instruções estavam incompletos | melhoria procedente |

## Falsos positivos descartados

- 315 e 316 são snapshots diferentes; `GLOSSARIO.md` explica o acréscimo.
- 81 caminhos, 60 pastas de objeto e 58 objetos da biblioteca medem conjuntos
  diferentes.
- O glossário separado está correto; relatórios de sprint que narram a absorção
  anterior continuam históricos.
- “Declarative Automation Bundles” permanece nomenclatura oficial.

## Veredito

O redesenho melhorou navegação, público e distinção NATIVO/HUB. Não houve P0 nem
motivo para revertê-lo. As correções necessárias concentram-se em fatos mutáveis
com mais de um dono e em dois limites operacionais omitidos.

As mudanças aceitas foram aplicadas em nova sessão, validadas e registradas no
`CHANGELOG.md`.
