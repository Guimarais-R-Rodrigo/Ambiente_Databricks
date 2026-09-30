# SD-VF-N — tentativa 01 — 2026-09-29

(Codex) Evidências: [resposta literal](SD-VF-N_T01.txt) e notebook fornecido pelo usuário.
Originais preservados localmente em `.artifacts/skills-delivery-evidence/genie-20260929-drift/`.
O notebook contém caminho pessoal; não foi copiado ao conteúdo versionado nem executado.
SHA256 notebook: `d2fd05b998769935fdf7c7f7474d18b5185cc3c84b007814dd49b73c86cc2d05`.
SHA256 resposta: `9a15211cfcc1aa8fd72bcd005d6d98396cd926f812df584471492de73a1cdf3d`.
Versão esperada: `f518ba9c529d4c5219df7052f992aaa0efa5b51510dedb5d7819d0834fa6e81e`.
A exportação não prova os bytes carregados remotamente.

## Vereditos separados

- Tarefa vizinha: atendida como drift/monitoramento, sem forçar Safra.
- ROUTING e carregamento: NOT_OBSERVABLE. Usuário confirmou apenas texto, sem indicador.
- Execução: OBSERVED nas saídas salvas do notebook: preflight PASS, run PASS,
  verify VALID, Receipt issued True. Receipt/payload completos não foram anexados;
  não há revalidação independente do Receipt remoto ou homologação integral.
- TASK_CORRECTNESS: FAIL na interpretação; valores numéricos conferem.
- AGENT_ADHERENCE: FAIL pela severidade sem política e enquadramento do perfil.
- CANONICAL_COMPLIANCE: NOT_OBSERVABLE integralmente; chamadas canônicas presentes,
  mas falta payload/Receipt para conferir identidade/integridade da execução remota.
- VEREDITO: FAIL, preservando os acertos e limites acima.

## Achados

1. PSI recalculado localmente = 3.280578415; KS = 0.25; p = 1.0.
   Cálculo independente usando somente arrays sintéticos, sem executar o anexo.
   Bins e contagens conferem. A participação do primeiro bin é aproximadamente
   94,7%, não 94,6% como informado na resposta. Isso não reexecuta nem certifica o runner remoto.
2. A resposta chama o drift de severo e independente do tamanho amostral sem
   política calibrada. A skill já proíbe limiar universal. Com quatro pontos,
   o bin vazio e eps=1e-6 dominam o PSI; valor alto não define severidade operacional.
   p=1 não mede poder, nem prova equivalência. Registrar limitação amostral sem
   declarar poder calculado/inexistente. Não houve recomendação de retreino.
3. O prompt não pediu explicitamente DRIFT_NUMERIC_LOCAL_V1. O notebook acrescentou
   IDs, datas/janelas, modelo/população e parâmetros para encaixar o perfil, cuja
   skill exige pedido explícito. São metadados construídos para demonstração,
   não contexto temporal fornecido pelo usuário; esse limite não ficou claro.
4. Há output HTML Plotly no anexo; renderização efetiva na UI não foi observada.
   A tabela é evidenciada. A célula visual recalcula PSI com valores fixos e não
   condiciona sua apresentação a verify válido; não estender a ela o Receipt.

Auditoria independente somente leitura corroborou aritmética, falha de
severidade e limites de evidência. Nenhum produto foi alterado nesta coleta.

## Próximo passo

MON-UI-01 aberto. Fazer SD-VF-N-D01, diagnóstico separado dos 37 SD e 42 FG,
com seleção real de `@hub-ml-monitoramento-modelo`, chat novo e mesmo prompt.
A seleção explícita não prova bytes carregados nem encerra o caso espontâneo.
Não mudar description com base apenas no autorrelato. SD-VF-A continua NOT_RUN.
