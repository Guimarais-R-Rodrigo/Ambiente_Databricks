# B1 — readback Free da correção de ACK incerto no Delta

(Codex) Em 2026-09-30, após a [triagem causal](TRIAGEM_CAUSAL_POS_FAILS_B1_2026-09-30.md),
o commit `d73b118e` foi levado **somente** ao Databricks Free pessoal,
perfil CLI `FREE`, nos três arquivos abaixo. O preflight leu os três
destinos como `FILE`, exigiu que cada conteúdo remoto normalizado coincidisse
com a versão anterior `21b64553` ou com a versão nova e passou antes de
qualquer escrita. O script de publicação não enumera, escreve nem remove
objetos de micromodelos; policy e instruções não foram alteradas.

| Arquivo `.assistant/` | Primeira publicação | Segunda leitura sem escrita; SHA-256 normalizado |
|---|---|---|
| `skills/hub-ml-pipeline-builder/scripts/run_delta.py` | Import retornou `rc=1`; readback imediato coincidiu com a versão nova, estado `READBACK_MATCH_AFTER_ACK_ERROR` | `ALREADY_MATCH`; `f41fd08f900f65e99ffbba9be66d5fcda6747dc56116cfb37dc4a1df6ca7c115` |
| `skills/hub-ml-pipeline-builder/release_manifest.json` | ACK e readback coincidiram | `ALREADY_MATCH`; `c02e8a8f0dabb73461361db2adeb864eee6986d30a5dfb305fed45762d6e0e45` |
| `skills/hub-ml-feature-engineering/release_manifest.json` | ACK e readback coincidiram | `ALREADY_MATCH`; `625a7ca5a237ab7735e1b2392f4fa6413dc2a818145b249e57c72af390bb8699` |

A segunda chamada com `--execute` encontrou os três arquivos já iguais e
não tentou escrever. O relatório final local ignorado é
`.artifacts/skills-delivery-evidence/delta-ack-three-file-free-publish-20260930.json`,
SHA-256 `805c301717854fa78dc985d191d6380dda9de617eba128cbf87193048cbae637`.
O relatório foi sobrescrito pela segunda chamada; os estados da primeira
chamada permanecem no output desta sessão, não em um artefato bruto versionado.
O ACK falho do primeiro import **não** foi convertido em ACK bem-sucedido;
o que está comprovado é o conteúdo normalizado observado depois dele.

A correção de `DROP` ambíguo tem testes locais com FakeSpark antes e depois
do efeito, além da regressão FE. Esta publicação verificou **conteúdo** no
Free; não simulou perda de ACK do `DROP TABLE` no serviço nem executou novo
probe de escrita Delta. O probe Free anterior de caminho normal pertence à
versão anterior e não homologa esta versão. O PR #117 continua Draft e a
homologação Genie das 14 skills segue parcial.
