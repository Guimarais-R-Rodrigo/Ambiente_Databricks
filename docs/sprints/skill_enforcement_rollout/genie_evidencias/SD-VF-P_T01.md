# SD-VF-P — tentativa 01 — análise recebida em 2026-09-29

(Codex) Primeira resposta preservada [integralmente como recebida](SD-VF-P_T01_resposta.txt).
O anexo contém prompt, texto intermediário e resposta final; não contém evento
independente de ferramenta ou indicador de carregamento.

- Executor: Rodrigo; ambiente informado: Genie Code / Databricks Free.
- Chat, horário exato e runtime da conversa: não fornecidos.
- Versão de referência: R2, hash `513e2ef9536833d6784d0d464f824392d0559f7dcc39eee1185d434a2c5446f9`.
  Referência da publicação anterior, sem atestado independente da versão carregada
  pelo chat. A republicação posterior não muda a versão desta tentativa.
- SHA256 do anexo preservado: `8a31f9133290fdba2914842640fdeef090a7b2f3dbbd04be10bc96584c198bc5`.
- Confirmação humana sobre UI: “Não apareceu indicador; apenas o texto”.
- ROUTING: **NOT_OBSERVABLE**; skill apenas mencionada: hub-ml-analise-safra.
- Execução: **NOT_RUN**; a resposta oferece executar depois, sem declarar execução
  canônica concluída. Ausência de execução não é falha neste caso conceitual.
- TASK_CORRECTNESS: **FAIL** (inferências e descrição de cobertura incorretas).
- AGENT_ADHERENCE: **FAIL** (preenche identidade/causa de ausência sem evidência).
- CANONICAL_COMPLIANCE: **FAIL** para a descrição do contrato; a execução canônica
  não foi avaliada e não se presume que a skill tenha sido carregada.
- VEREDITO: **FAIL comportamental**; roteamento continua inconclusivo.

## Acertos preservados

Denominadores dois, janeiro/MOB0=0%, janeiro/MOB1=50%, fevereiro/MOB0 e MOB1=50%.
Não soma taxas por MOB, não transforma ausência em zero e não finaliza janeiro/MOB2.

## Achados

1. Afirma que o contrato ausente ainda não atingiu a idade no corte, sem data de
   corte informada. Maturidade da célula e cobertura são propriedades distintas.
2. A tabela atribui o observado a A e o ausente a B, sem o prompt identificar isso.
3. Atribui três estados à coverage_grid; o preflight define IMMATURE,
   NO_OBSERVATIONS, COMPLETE e INCOMPLETE, além do campo maturity separado.
   NO_OBSERVATIONS não significa que ninguém chegou à idade do MOB.
4. Diz que os dados encaixam exatamente no perfil, embora não haja entradas
   completas para validar roster/IDs, datas, corte e valor parcial de MOB2.
5. A fórmula de acumular eventos é uma definição possível do indicador, mas deve
   ser distinguida da entrada CUMULATIVE já acumulada: o runner rejeita decréscimos,
   não aplica cummax para corrigir entradas inválidas.

## Causa e tratamento

A resposta demonstra essas falhas; não demonstra qual contexto foi de fato
carregado. A skill já proibia inventar campos, mas não explicava os quatro estados
nem a distinção conceitual neste nível. Auditoria independente confirmou os
achados e recomendou reforço documental, sem alterar o runner.

Correção SAFRA-UI-01: esclarecimento em SKILL.md. Validação, publicação/readback e
reteste serão vinculados no registro consolidado. A eficácia do ajuste permanece
pendente de reteste; a tentativa 01 não será reclassificada após a correção.

## Situação após o ajuste

Validador antes/depois renderer: PASS, zero falhas e zero avisos; auditoria
independente sem achados no ajuste. Publicação enviada e 654 arquivos conferidos
por conteúdo. Verificador final FAIL exclusivamente por notebook extra vazio em
.assistant; bloqueio GENIE-ENV-01 separado da resposta avaliada. Reteste pendente.

GENIE-ENV-01 foi resolvido após esclarecimento humano: notebook vazio sem trabalho,
cópia preservada, exclusão pontual com ID/hash reconferidos e ausência confirmada.
Inventário final PASS; nova leitura do texto Safra confere. O primeiro verify FAIL
permanece histórico; T02 liberada em chat novo, notebook fora de .assistant.
