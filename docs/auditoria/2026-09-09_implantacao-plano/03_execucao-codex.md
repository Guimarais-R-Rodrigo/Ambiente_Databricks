# Execução das correções — Codex

Data: 09/09/2026. Base: `771dbf2`, branch `claude/plano-consolidado-2026-09-08`.
O usuário autorizou implementar e enviar as correções para baixar no PC.

| Achado | Implementação | Evidência local |
|---|---|---|
| R01 | erro em valor inválido selecionado, aliases e obrigações explícitas | NaN/inf/bool/texto reprovam; exclusão deliberada passa |
| R02 | nomes temporários exclusivos | colunas internas preservadas, grão e lags corretos |
| R03 | extras/caches/symlinks barram publicação; bundle compartilha guarda | mutante não chega à chamada CLI |
| R04 | Counter de tuplas completas | perda fora de C1, duplicata e alteração de data reprovam |
| R05 | limite inteiro positivo antes de ações | limite inválido reprova mesmo sem DataFrame disponível |
| R06 | migração documentada preservando escala histórica | testes KS em pontos percentuais mantidos |
| T3 | inventário Git e higiene de extras separados; README local/remoto separado | guia ignorado não muda inventário, mas link inválido é detectado |
| Proveniência | Git ancorado, hash completo, relatório JSON opcional | erro de Git, exportação inválida e persistência JSON testados |

Resultado: 40 testes de biblioteca, 32 de ferramentas; gates locais aprovados.
Renderer executado; nenhum ajuste manual no espelho. O relatório de auditoria
original permanece intacto como evidência do estado anterior.

As verificações de PIT multiconjunto e pré-condição CSI foram executadas em
isolamento sem Spark. Elas não fecham os gates Free/corporativo. A integração
real de publicação, os cenários Spark e os 19 cenários conversacionais continuam
pendentes conforme o [handoff de retomada](../../handoffs/2026-09-09_correcoes-codex.md).
