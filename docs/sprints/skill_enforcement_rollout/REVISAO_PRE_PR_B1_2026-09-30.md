# Revisão pré-PR do candidato B1 — 2026-09-30

(Codex) Esta revisão incide sobre `codex/b1-review-after-prereq`, baseada no
commit documental separado `222420a1`. É uma candidata a PR em rascunho
empilhado sobre o PR #115, conforme escolha do usuário. A
[consolidação Genie](CONSOLIDACAO_GENIE_B1_2026-09-30.md) continua dona dos
vereditos por skill; esta revisão não converte as respostas Genie em execução
de runner nem em homologação integral.

## Achados corrigidos antes do PR

1. **Manifesto Pipeline obsoleto:** `release_manifest.json` continha hashes
   antigos de `execution_contract.json` e `input.schema.json`. O runner
   bloquearia em `release_integrity` antes do efeito. Foram atualizados esses
   dois hashes e o hash do `run_delta.py` no manifesto Pipeline. Como FE
   reutiliza esse runner, seu manifesto também foi atualizado. A auditoria
   atual conferiu **159/159 entradas em 11 manifestos**, sem divergência.
2. **Limpeza Delta afirmada cedo:** após `DROP TABLE`, `cleanup=PASS` (ou
   `PASS_AFTER_FAILURE`) era gravado antes da leitura de ausência. Se essa
   leitura falhasse, o efeito terminava `UNKNOWN` com `cleanup=PASS`.
   O runner agora mantém `DROP_UNCONFIRMED` até a ausência ser confirmada;
   falha ou resposta contraditória preservam `UNKNOWN`. Há regressões com
   timeout e leitura stale, inclusive no fallback de limpeza. O ajuste vale
   tanto para Pipeline Builder quanto para materialização FE, que usa o mesmo
   lifecycle.

O produto foi editado em `ambiente_fonte/` e o derivado foi gerado por
`tools/render_simulado.py --write`, sem edição manual. O renderer produziu
658 arquivos incluindo o marcador derivado; os **657 arquivos gerenciados**
da fonte e do espelho estão byte a byte iguais nesta candidata.

## Verificação local desta candidata

| Gate | Resultado e limite |
|---|---|
| `python -B tools/validate_assistant.py --root ambiente_fonte` | PASS, zero falhas e avisos |
| Auditoria de `release_manifest.json` | 159/159 hashes atuais |
| Spark local, processos separados | SER14 Delta 8/8, SER08 materialização FE 7/7, SER13 Pipeline execution 5/5 PASS |
| Testes sem Spark | SER13 spec e domínios B1 51/51 PASS |
| Fonte × derivado | 657/657 arquivos gerenciados byte a byte iguais |
| Free, Delta e materialização FE | Dois probes sintéticos `PASS`, `cleanup=PASS` e `table_absent_after_cleanup=true`; sem homologação Genie |

A tentativa de rodar todos os módulos Spark no mesmo processo Windows teve
um erro ao reiniciar o Spark após outra suíte, associado ao ambiente local
sem `HADOOP_HOME`/`winutils`. A mesma bateria foi executada por módulos em
processos separados e passou. O Python padrão 3.12 não tinha `jdk4py`; os
testes Spark foram feitos no ambiente Python 3.11 já existente em
`.artifacts/skills-venv/`, sem instalar pacote novo.

## Limites de revisão

- A prova Free 657/657 do [fechamento técnico](FECHAMENTO_TECNICO_B1_2026-09-30.md)
  pertence ao snapshot anterior. A conferência remota antes da correção
  exportou **657/657 arquivos gerenciados**: zero ausentes, 15/15 skills
  presentes e exatamente **três divergências de conteúdo normalizado**,
  correspondentes ao `run_delta.py` e aos manifestos Pipeline/FE corrigidos.
  Os outros 654 arquivos gerenciados eram iguais após normalização. Os três
  arquivos foram publicados exclusivamente no Free e tiveram readback
  (`run_delta.py` já correspondia após uma resposta CLI inconclusiva;
  ambos os manifestos foram escritos e conferidos). Relatório local ignorado
  pelo Git: `.artifacts/skills-delivery-evidence/b1-three-file-free-publish-20260930.json`,
  SHA-256 `a1aff5f0f6f0433458fc208fb6c619517ff51976742c7cbef7839653e4f7aa47`.
  O inventário geral marca 28 arquivos e seis diretórios adicionais de
  `hub_micromodelos` como extras da frente paralela; eles foram preservados.
  Relatório da conferência anterior, local e ignorado pelo Git:
  `.artifacts/skills-delivery-evidence/b1-prepr-remote-verify-20260930.json`,
  SHA-256 `931de36951fae7228af7ea0807bb30634b4c0f9495c5fce801e8e6e6dc8c413c`.
  A fonte foi lida enquanto o follow-up ainda estava dirty, por isso o
  identificador de commit do relatório não certifica uma árvore limpa.
- A primeira execução dos dois probes sintéticos no Free ficou `BLOCKED`
  antes de criar tabela: os contratos `execution_contract.json` e
  `input.schema.json` remotos tinham uma quebra CRLF onde a fonte tinha LF.
  Eram semanticamente iguais, mas seus hashes exatos não batiam com os
  manifestos corrigidos. Somente esses dois contratos foram republicados,
  com comparação prévia de bytes e readback exato. A auditoria posterior
  confirmou **27/27 arquivos** dos manifestos Pipeline/FE byte a byte iguais
  no Free. Relatórios locais ignorados: `delta-fe-fix-contract-repair.json`
  (SHA-256 `921d5f880c9e5e76f76522f91ad65cdc7afd9b7044133bcac49378e76a4c77b2`)
  e `delta-fe-fix-release-audit.json`
  (SHA-256 `54d3fce1451c1f0a103a8112ff5c248b66ada9105b6959ec97d8f8b4303ab6dd`).
- No reteste Free, job sintético `797744448279465`, Delta e materialização FE
  terminaram `PASS`: efeito criado, readback validado, `cleanup=PASS`,
  `table_absent_after_cleanup=true`, sem mutação do pacote publicado. Os
  relatórios locais ignorados são `delta-fe-fix-free-r2-delta-report.json`
  (SHA-256 `32ad8910f98e3421731c4d8e46069336f3e0788f818d4d9645423667c4759001`)
  e `delta-fe-fix-free-r2-feature_materialization-report.json`
  (SHA-256 `5f5d17d3a47eabbccf23fc006b171288f8c8952d195ca382498b0bf903c01549`).
  Isso valida estes efeitos sintéticos no Free; não equivale à homologação
  Genie, à promoção de policy ou ao deploy corporativo.
- A branch contém transcrições Genie brutas, com whitespace histórico.
  `git diff --check` no conjunto de commits aponta esses espaços e linhas
  vazias também em arquivos novos. Preservar os bytes das transcrições evita
  reescrever a evidência. Não tratar o PASS de `git diff --check` anterior,
  que ignorava untracked, como gate da branch commitada.
- Os patches e relatórios completos citados no
  [pacote de revisão](PACOTE_REVISAO_B1_2026-09-30.md) são artefatos locais
  ignorados pelo Git. O revisor remoto recebe os resumos versionados, mas
  não consegue recomputar essas provas sem um pacote sanitizado separado.
- Os checks do [PR #115](https://github.com/Guimarais-R-Rodrigo/Ambiente_Databricks/pull/115)
  falharam antes de executar passos. Anotações do GitHub nos jobs `validar`,
  `contrato` e `nucleo` atribuem isso a cobrança/limite de gastos da conta.
  Esses checks não são evidência de regressão nem de PASS do código atual.

O PR em rascunho deve manter explícitos os FAILs/UNKNOWN da Genie, a ausência
de promoção de policy/Ready e o limite dos probes sintéticos Free. Nenhum merge
é autorizado por este relatório.
