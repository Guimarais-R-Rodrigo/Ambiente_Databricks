# B1 — primeira candidata de domínio (P1)

Base de autoria: `4ba7f551767d847381df1556ed937116258fa77d`, após merge do B0/PR #113.
A issue #114 é o registro da frente. Esta entrega é **autoria parcial, não certificação e não promoção**.

## Implementado

SER03 recebe contrato SEF 0.1, schema de request, preflight mensal/binário, runner fino da primitive `build_vintage_table`, Receipt V1 e verifier vinculado a request/run/oráculo externo. Denominador: roster explícito de MOB0; duplicatas rejeitadas; células sem observação não são convertidas em zero; maturidade e cobertura são separadas.

SER05 recebe contrato/schema e preflight de contexto L2. Fontes são identificadas por metadados declarados, não lidas. Temporalidade UNKNOWN bloqueia; NOT_APPLICABLE exige motivo; latência variável e bitemporalidade são recusadas. O resultado nunca declara join executado, cobertura medida ou readiness ML.

O owner compartilhado do contexto é `hub_scripts.skill_execution.domain_context`. Não há novo scheduler nem implementação paralela do Receipt. O protocolo de Receipt existente e o preflight genérico são consumidos pelas fachadas.

## Prova nesta etapa

O arquivo `tools/tests/test_ser_b1_domains.py` contém 47 métodos, todos executados no checkout completo: **47/47 PASS**, zero FAIL, ERROR ou SKIP. Os dois métodos de integração pública comprovaram o preflight SEF real e o caminho público de helper/Receipt/verifier, incluindo rejeição de replay e tamper.

Os contratos foram conferidos com o schema canônico `execution_contract.schema.json`, blob `54a9b5a6675417cd3b732a5a7e4507e97e77d58a`. Os quatro requests/contextos foram validados estruturalmente pelos schemas da candidata. Temas V07 (17/17), V07 mirror (2/2) e V08 (22/22), validator completo e renderer canônico passaram. O canal SE07 preservou exatamente os dois FAILs temporais esperados, sem ERROR ou falha adicional. Essas provas qualificam a autoria integrada, não certificam ou promovem SER03/SER05.

## Pendências que impedem certificação

1. Fechar os mapas de superfície/caso e a revisão do perfil limitado; trimestre/comparações da safra e os casos de join/Postflight de SER06 continuam fora desta candidata.
2. Integrar os pontos de entrada às instruções das skills e reconciliar Manual quando o escopo correspondente for autorizado; o render canônico, validator e entrada no CHANGELOG raiz desta P1 já foram executados.
3. Implementar os command IDs/manifesto/handoff B1 de forma aditiva. O registry fechado B0 não foi alterado.
4. Verificar o domínio sob o ambiente sanitizado da campanha. Nenhum PASS do B0 é transportado para as novas dependências.
5. Definir o adapter de auditoria de produtor para SER03: o auditor atual tem adapter direto somente para EDA. Não declarar reverificação genérica sem implementação.

A ordem de trabalho continua P1 (domínio) → P2 (campanha) → diagnóstico consolidado → certificação. Não é necessário enviar esta entrega ao Codex como campanha fechada.

## Limites

Policy L0 e targets permanecem como estavam. Sem Spark, Free, Genie, publicação, 3/2, Ready ou merge. A main e o branch integrado do B0 não são alterados por esta candidata.
