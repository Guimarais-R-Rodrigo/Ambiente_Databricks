# SER00 — testes e protocolo de validação

## Escopo efetivo desta rodada

Validação documental própria, executada em Python local sobre os arquivos novos e o snapshot de observações pinadas. Não é certify_local, validate_contracts, se07_policy, validate_assistant, renderer, CI local, Windows/NTFS ou teste Spark/Databricks. Esses comandos não receberam PASS nesta sessão.

O clone Git do container falhou por resolução de github.com. As consultas autenticadas pelo conector funcionaram. Não declarar worktree completo/limpo: a materialização local contém somente documentação SER e evidência auxiliar.

## Comando documental executável

```text
python -B validar_ser00_documental.py --docs <pasta-skill_enforcement_rollout> --baseline baseline_observada.json --output resultado_documental.json
```

O script integra o bundle externo da rodada, não o produto. A rodada documental inicial verificou 14 documentos, UTF-8/fences, links relativos, 14 linhas de policy, 24 superfícies, níveis/riscos/scope/rollout/status contra as observações, 13 recomendações CONFIRMED e uma HUMAN_DECISION_REQUIRED. Após o aceite, a validação documental R2 verifica 14 targets CONFIRMED, o ADR-0022, a atualização do índice de ADRs, sequência SER01–SER16, estados de canais e ausência de mudanças de produto. Os controles negativos originais são preservados.

A base é uma transcrição identificada das leituras da API, não um clone integral. A concordância documental não certifica o runtime nem o próprio validator da policy.

## Evidência de publicação

Calcular SHA-256 e Git blob SHA-1 de cada arquivo local. Depois da criação do commit, comparar os blobs da árvore GitHub e o delta contra a baseline. Vincular o resultado ao HEAD/tree/base no manifesto externo e na PR. Conferir que ambiente_fonte, Novo_Ambiente_Simulado, tools e .github conservaram as trees originais. Essa comparação prova escopo/integridade do delta, não execução dos testes históricos.

## Certificação final obrigatória antes de merge

A manutenção A07/PR #102 já está integrada. Na HEAD final da SER00, confirmar `origin/main=515e673b17f21d4c912d9ae866a7e31967fd4488`, merge-base igual à main, `behind=0`, clone não shallow e worktree limpa. Não transportar PASS da #102 para esse novo SHA.

Preparar dependências V06 somente pelo lockfile quando ausentes e provar que `package.json`/`pnpm-lock.yaml` não mudaram. Em seguida executar, sem retry-until-green:

```text
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/skill_enforcement/se07_policy.py
python -B tools/validate_assistant.py
python -B tools/render_simulado.py --write
python -B tools/validate_assistant.py --conferir-readme
python tools/ci_local.py --verbose
python -B tools/skill_enforcement/certify_local.py --profile se08 --evidence-dir <NOVO_DIRETORIO_EXTERNO>
```

O FULL só deve rodar se os gates anteriores passarem. Espera-se que o snapshot confirme os valores já medidos na A07-R1, agora versionados: `repo (identidade)=1660`, `repo (links)=2126`; qualquer divergência é FAIL e deve ser preservada. Nunca editar derivado manualmente. A01–A03 estão resolvidas e a manutenção A07 está integrada; o PASS final apenas certifica a SER00 documental e não promove skill nem autoriza SER01.

## Estados

GITHUB_ACTIONS=DEFERRED_NO_CREDITS; DATABRICKS_FREE=NOT_RUN; GENIE_BEHAVIOR=NOT_RUN; FINAL_SER00_CANONICAL_VALIDATORS=NOT_RUN_ON_FINAL_SHA. Execuções incidentais de Actions serão observadas e preservadas na PR/manifesto, sem rerun. Ausência de créditos não é FAIL funcional.


## Rodada R2 pós-aceite

A R2 documental foi executada sobre os bytes reconciliados antes da publicação final. Ela inclui ADR-0022, índice de ADRs, 14 targets CONFIRMED, escopo puramente documental e estados pós-aceite. Resultado: `PASS_38_OF_38_DOCUMENTARY_CHECKS`. Isso continua separado dos validadores canônicos A07 e não herda o PASS da R1.


## Histórico A07 preservado

- R1 SER00: FAIL funcional de storage + snapshot stale; sem retry.
- R2 manutenção #102: storage 9/9, Windows 11/11 e certifier 51/51 PASS; CI bloqueado por dependências Node ausentes.
- R3: ambiente preparado; CI revelou somente snapshot herdado da PSEF00; causa +7 arquivos/+6 links comprovada.
- R4: CI 10/10 PASS e FULL SE08 21/21 PASS em `4a70834d...`, worktree limpa, zero infrastructure errors; manutenção integrada em `515e673b...`.

Nenhum desses PASS substitui a certificação da HEAD final SER00.
