# SER00 — matriz de riscos

| ID | Severidade | Risco constatado ou prospectivo | Controle / critério de saída | Dono lógico |
|---|---|---|---|---|
| A01 | ALTO / DECISÃO ACEITA | assertions SE08 amarradas a current L2/cinco contratos/CI histórico | ADR-0022: certifier SER aditivo + histórico preservado; implementação/teste ainda pendentes | SER01 infraestrutura prospectiva |
| A02 | ALTO / DECISÃO ACEITA | condições 0.1 não expressam domínios novos | evolução aditiva, skill-local quando específica, shared schema somente se transversal; desconhecido bloqueia | primeira sprint que necessitar nova condição |
| A03 | ALTO / TARGET CONFIRMADO | piloto criar-objeto apresentado como L3 global | matriz tipo×operação×host×efeito precisa ser provada; current L2 até lá | SER01 |
| R04 | ALTO | helper existente confundido com execução canônica | teste de chamada concluída + binding + Receipt; omissão e erro propagados | cada sprint L3 |
| R05 | ALTO | producer novo sem verifier independente | NOT_REVERIFIED até adapter compatível; adulteração/replay negativos | cada produtora/SER15 |
| R06 | ALTO | amostra SHAP não ligada às linhas efetivas | amostragem e output_index explícitos; verificação dimensional e provenance | SER02 |
| R07 | ALTO | safra incompleta/denominador errado parece resultado correto | target/denominador/MOB/maturidade; NaN não vira zero; fixture discriminante | SER03 |
| R08 | ALTO | testes estatísticos sem API ou pressuposto comprovado | catálogo de métodos suportados; limites de desenho; efeitos e incerteza | SER04 |
| R09 | CRÍTICO | leakage temporal e cardinalidade no join/features | atraso/availability/cutoff/janelas/grão; casos limite; Postflight fail-closed | SER05–SER08 |
| R10 | CRÍTICO | treino/registro sem binding ou efeitos invisíveis | split train-only, run real, artefatos, autorização e resíduos | SER09/SER10 |
| R11 | CRÍTICO | drift convertido em retreino/promoção automática | decisão e ação separadas; target maturado; autorização específica | SER11/SER12 |
| R12 | CRÍTICO | spec tratada como deploy concluído | operação real isolada e autorizada; verify/cleanup/rollback | SER13/SER14 |
| R13 | ALTO | Free não suporta operação necessária | probe de capacidade; manter promoção bloqueada; não forjar N/A | sprint afetada |
| R14 | ALTO | mudança concorrente torna prova stale | refetch e comparação SHA/tree/worktree; nova rodada com evidências preservadas | todas |
| R15 | ALTO | rollout enforce inferido de target/current | decisão por skill; validator só permite enforce com L4; não mudar mode 0.1 | cada promoção |
| R16 | ALTO | local PASS apresentado como Free/Genie/Actions | canais e estados separados; logs reais; sem inferência de comportamento | todas |
| R17 | BAIXO / RESIDUAL | snapshots/CHANGELOG/global validation da HEAD SER00 final ainda não recertificados | executar campanha final SHA-bound sobre main `73d7659d...`; preservar qualquer FAIL sem retry | encerramento SER00 |
| R18 | ALTO | interpretação criativa/causal determinizada por excesso | proteger somente superfície objetiva, runner fino e helper reutilizado | desenho de cada skill |
| R19 | ALTO | ampliar confiança criptográfica de hashes | declarar ameaça coberta; hashes vinculam bytes, não autorizam operação humana | Receipt/autorização |
| R20 | MÉDIO | dívidas históricas apagadas pelo novo projeto | SE06 24/25, SE07 ressalvas, falhas e limitações imutáveis | documentação/certificação |

O bloqueio não decorre de ausência de créditos: Actions continua fora do caminho crítico. As decisões arquiteturais A01–A03 estão resolvidas; permanecem riscos de implementação/escopo e a validação não executada no checkout completo. Nenhum risco foi reduzido na policy para facilitar a conclusão.
