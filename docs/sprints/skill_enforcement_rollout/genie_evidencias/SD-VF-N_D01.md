# SD-VF-N-D01 — diagnóstico com @ — 2026-09-29

(Codex) [Resposta literal](SD-VF-N_D01.txt). Notebook e resposta originais
preservados localmente em `.artifacts/skills-delivery-evidence/genie-20260929-monitor-d01/`.
O notebook contém caminho pessoal e não entra no conteúdo versionado.
SHA256 notebook `73ebc740007fa35f1ed31a3720f99c9828d75eb4224dba6266a9839aab9bea6b`; resposta `63413ecfd7f9b81c35c2e701bfc54afab84745e05e9ada81229bed097c686983`.
Versão publicada esperada `f518ba9c529d4c5219df7052f992aaa0efa5b51510dedb5d7819d0834fa6e81e`.
O usuário confirmou seleção visível pelo menu @ antes do envio. Não informou
indicador separado de carregamento, nem há prova dos bytes carregados.

## Resultado

- Seleção por @: confirmada pelo usuário para `hub-ml-monitoramento-modelo`.
  Carregamento interno: NOT_OBSERVABLE.
- Tarefa vizinha: monitoramento/drift, sem retorno indevido a Safra.
- Saídas salvas do notebook: preflight PASS, run PASS, verify VALID/valid=True;
  Receipt issued True. Isso é execução OBSERVED, mas o payload/Receipt completo
  não foi preservado para validação remota independente. Verificador registra
  `completion_authorized=False`.
- Bins com rótulos corretos na resposta final; contagens [1,1,1,1,0] para
  referência e [0,1,1,2,0] para atual. PSI 3,280578415; KS 0,25; p=1,0.
  Rechecagem numérica local com arrays sintéticos; anexo não foi reexecutado.
- Melhorou frente à T01: sem classe operacional “severo”, sem alegar performance
  medida ou decisão de retreino. “Altíssimo” descreve o valor, e a resposta
  ressalva amostra pequena/necessidade de calibração; não é, isoladamente,
  classificação formal de severidade.
- Falhas residuais: o prompt genérico não solicitou explicitamente SER11;
  notebook introduziu datas/janelas/IDs/modelo/população sem marcar cada um
  como convenção criada para demonstração. A resposta atribui p=1 à baixa
  potência, mas p não mede potência; nenhuma análise de poder foi feita.
- Veredito do diagnóstico: **FAIL parcial de aderência/interpretação**.
  Não substitui nem reclassifica SD-VF-N/T01 e não conta como novo caso SD.
  Conformidade canônica integral segue NOT_OBSERVABLE pela ausência de payload.

Auditoria independente somente leitura confirmou cálculos, melhorias e achados.
Correção proporcional: reforçar instrução da skill e template de relatório;
runner, verificador e description permanecem sem evidência de defeito.
Reteste da correção requer novo chat e versão publicada vinculada.

## Candidata local e bloqueio de publicação

(Codex) Reforço proporcional implementado em `SKILL.md` e
`templates/drift_report.md` de Monitoramento, sem mudar runner, schema,
verificador, description ou policy. 15 testes SER11/SER12 PASS; validador antes
e depois do renderer: 0 falhas, 0 avisos. Somente esses dois arquivos do pacote
mudaram frente à publicação `f518ba9c...`.

A comparação read-only dos 654 arquivos remotos com a última publicação encontrou
**dois conflitos fora da skill**: `policy.json` ganhou uma entrada
`hub-ml-micromodelos`; `.assistant_instructions.md` ganhou uma linha. Backups e
hashes estão em `.artifacts/skills-delivery-evidence/genie-20260929-monitor-d01/`.
A publicação integral foi interrompida antes de qualquer escrita remota, pois
sobrescreveria essas mudanças. O usuário confirmou que ambas devem ser preservadas. O publicador canônico não
tem modo de enviar apenas dois arquivos; a publicação integral permanece suspensa
até reconciliação do pacote com essas mudanças, antes de liberar o reteste. A candidata local não é uma nova
versão publicada nem prova de correção comportamental.
