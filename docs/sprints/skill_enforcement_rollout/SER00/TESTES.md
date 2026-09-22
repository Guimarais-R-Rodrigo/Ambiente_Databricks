# SER00 — testes e protocolo de validação

## Escopo efetivo desta rodada

Validação documental própria, executada em Python local sobre os arquivos novos e o snapshot de observações pinadas. Não é certify_local, validate_contracts, se07_policy, validate_assistant, renderer, CI local, Windows/NTFS ou teste Spark/Databricks. Esses comandos não receberam PASS nesta sessão.

O clone Git do container falhou por resolução de github.com. As consultas autenticadas pelo conector funcionaram. Não declarar worktree completo/limpo: a materialização local contém somente documentação SER e evidência auxiliar.

## Comando documental executável

```text
python -B validar_ser00_documental.py --docs <pasta-skill_enforcement_rollout> --baseline baseline_observada.json --output resultado_documental.json
```

O script integra o bundle externo da rodada, não o produto. Ele verifica 14 documentos, UTF-8/fences, links relativos, 14 linhas de policy, 24 superfícies, níveis/riscos/scope/rollout/status contra as observações, 13 recomendações CONFIRMED e uma HUMAN_DECISION_REQUIRED, sequência SER01–SER16, estados de canais e ausência de arquivos executáveis/produtivos no conjunto de publicação. Inclui controles negativos contra matriz adulterada, superfície extra e caminho fora do escopo.

A base é uma transcrição identificada das leituras da API, não um clone integral. A concordância documental não certifica o runtime nem o próprio validator da policy.

## Evidência de publicação

Calcular SHA-256 e Git blob SHA-1 de cada arquivo local. Depois da criação do commit, comparar os blobs da árvore GitHub e o delta contra a baseline. Vincular o resultado ao HEAD/tree/base no manifesto externo e na PR. Conferir que ambiente_fonte, Novo_Ambiente_Simulado, tools e .github conservaram as trees originais. Essa comparação prova escopo/integridade do delta, não execução dos testes históricos.

## Complemento local obrigatório antes de merge

Em clone autenticado independente, confirmar origin/main, HEAD da SER, merge-base, ahead/behind e estado de trabalho. Não reaproveitar comandos/resultados de outra branch. Obter bytes completos e aplicar ENTRADA_CHANGELOG.md no CHANGELOG raiz sem perder histórico; qualquer mudança cria nova candidata.

Conferir --help das interfaces existentes. Executar sequencialmente, com logs e diretório externo novo:

```text
python -B tools/skill_enforcement/validate_contracts.py
python -B tools/skill_enforcement/se07_policy.py
python -B tools/skill_enforcement/certify_local.py --profile se08
python -B tools/validate_assistant.py
python -B tools/render_simulado.py --write
python -B tools/validate_assistant.py --conferir-readme
python -B tools/ci_local.py --verbose
```

Para SER00 documental, a policy ainda é a baseline; A01 é conflito prospectivo de promoção, não autorização para omitir suite atual. Se snapshot README falhar, registrar a falha, atualizar somente o que o validator comprovar e criar nova rodada no novo SHA. Nunca editar derivado manualmente. Render que produza drift inesperado exige diagnóstico, não aceitação silenciosa.

Além disso, resolver as decisões arquiteturais A01–A03 antes de liberar SER01. O PASS do complemento local não decide o target/scope por conta própria.

## Estados

GITHUB_ACTIONS=DEFERRED_NO_CREDITS; DATABRICKS_FREE=NOT_RUN; GENIE_BEHAVIOR=NOT_RUN; CANONICAL_REPO_VALIDATORS=NOT_RUN nesta rodada. Execuções incidentais de Actions serão observadas e preservadas na PR/manifesto, sem rerun. Ausência de créditos não é FAIL funcional.
