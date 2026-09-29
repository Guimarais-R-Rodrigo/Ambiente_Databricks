# Smoke local MM04 sem GitHub Actions

**Data:** 2026-09-29. **Natureza:** diagnóstico local de pré-certificação da candidata de laboratório. Este registro não é FULL, bundle lint, auditoria independente, aceite humano ou autorização de merge/promoção.

## Identidade da candidata examinada

| Campo | Valor |
|---|---|
| Repositório | `Guimarais-R-Rodrigo/Ambiente_Databricks` |
| Branch | `micromodelos/autonomia-local-v2` (PR #116 Draft) |
| HEAD | `b8d3ebc9674bec858ae07b97204784eba517e518` |
| Tree | `4c3ee5910764414c40b1b388fa6d1b0e0a77a5e1` |
| `origin/main` e merge-base | `4ba7f551767d847381df1556ed937116258fa77d` |
| Ahead/behind | `14/0` |
| Shallow | `false` |
| Worktree antes do registro | limpa; resíduos ignorados `__pycache__` classificados pelo validador |
| Plataforma | Windows, PowerShell, Python 3.12.10, Node v24.18.0; console Python padrão CP1252 |

`git fetch origin main` passou antes da medição. PRs abertos com potencial de tocar entradas futuras: #115 (SER B1), #99 (PSEF01), #91 (SE08). Nenhum foi incorporado a esta candidata nesta rodada.

## Gates locais e resultado

| Verificação | Resultado e limite |
|---|---|
| `python -B -m unittest discover -s tools/tests -p 'test_micromodelo_*.py'` com `PYTHONUTF8=1` | **186 PASS**. Execução anterior com apenas `python -X utf8` terminou com 3 erros de decodificação em subprocessos Windows da MM01; a primeira falha permanece como diagnóstico de ambiente. `PYTHONUTF8=1` foi herdado pelos subprocessos, sem alteração de código. |
| `test_skill_enforcement_policy_io`, `test_skill_enforcement_se07`, `test_skill_enforcement_se07_create_l3`, `test_render_simulado` com `PYTHONUTF8=1` | **96 testes OK, 1 skip**. Saída incluiu aviso esperado `SEF_PENDING_POSTFLIGHT_V1`; nenhum claim de conclusão de skill foi feito a partir dele. |
| `python -B tools/validate_assistant.py --root ambiente_fonte` | **APROVADO**, 15 skills, 0 falhas, 1 aviso: nove diretórios `__pycache__` locais. |
| Fonte → `Novo_Ambiente_Simulado` | **582/582 arquivos byte a byte iguais**, nenhum faltante ou extra na árvore de usuário. `README_GERADO.md` da raiz derivada não entra nessa contagem; não houve edição manual do derivado. |
| `git diff --check` / worktree | PASS / limpa antes deste registro. |

A policy da candidata declara `hub-ml-micromodelos` como `risk_class=high`, `current_level=L1`, `target_level=L3`, `rollout_mode=audit`. A bateria local não demonstra runner, Receipt, adapter Databricks da skill nem L3. A evidência Genie P1–P2c e suas ressalvas permanecem no [roteiro](TESTE_BRIEFINGS_MM04_E1.md); a execução Free e a importação B1 não substituem os gates MM04.

## Decisão de continuidade sem saldo de GitHub Actions

O usuário informou que não há saldo para GitHub Actions e pediu avanço local por ora. Os checks remotos do HEAD examinado não iniciaram jobs por limite/pagamento da conta (`steps=[]`); ficam **ADIADOS / BLOCKED_EXTERNAL_CI**, nunca PASS. A consulta Git remota para atualizar `origin/main` funcionou, mas não equivale a execução de CI.

Este diagnóstico fornece a parcela local do `PRE_CERTIFICATION_SMOKE`. O estado formal continua **INCOMPLETO**: falta fixar a matriz/autoridade de certificação proporcional MM04, fechar revisão editorial independente, reconciliar a candidata com o B1 compartilhado quando seguro e avaliar drift material antes de qualquer freeze. `CANDIDATE_FREEZE`, FULL single-shot, bundle lint, auditoria, contraditório e aceite continuam `NOT_RUN`. Se a certificação exigir checks GitHub vivos, esses gates só poderão concluir após restabelecer os runners ou aprovar explicitamente um procedimento alternativo; este relatório não altera o protocolo canônico.
