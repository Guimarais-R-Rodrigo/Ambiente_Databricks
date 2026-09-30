# SD-VF-P — tentativa 02 — retorno recebido em 2026-09-29

(Codex) [Resposta integral como recebida](SD-VF-P_T02_resposta.txt), preservada
sem substituir a [tentativa 01](SD-VF-P_T01.md).

- SHA256 do anexo: `eb23855b77ba6f69c963766065b75e69c7f28bf6b57d41963a92a09d70e162f4`.
- Executor: Rodrigo; contexto de coleta: Genie Code / Databricks Free.
- Chat, horário exato e runtime: não fornecidos.
- Versão publicada de referência: R2 + SAFRA-UI-01, hash
  `cf6fc86449834ffca9abb48bfb780ed56f53a7483f5504e42b9e485fe586993a`.
  Não é atestado independente da versão/contexto efetivamente carregados no chat.
- ROUTING: **NOT_OBSERVABLE**. O anexo contém autorrelato de carregamento;
  não contém indicador/evento de ferramenta. A confirmação humana anterior de
  ausência de indicador pertence à T01; não é reaproveitada como observação T02.
- Execução: **NOT_RUN**. O texto oferece execução posterior, não a declara feita.
- TASK_CORRECTNESS: **FAIL**; AGENT_ADHERENCE: **FAIL**;
  CANONICAL_COMPLIANCE: **FAIL** na descrição/preenchimento dos dados.
- VEREDITO: **FAIL comportamental**; roteamento inconclusivo.

## Melhorias observadas

A resposta distingue os quatro estados, trata CUMULATIVE como estoque já
acumulado e exige não decrescimento. Mantém denominadores dois, acerta as quatro
células completas, não finaliza MOB2 e pede entradas completas antes de executar.
A data de corte aparece agora como hipótese explícita; não é tratada como dado
fornecido. Esses acertos não comprovam que a skill foi carregada.

## Falha remanescente

Na tabela de janeiro/MOB2, apresenta `(1, —)`, numerador `1` e `50% não finalizar`.
O prompt informa somente que há uma observação, sem identificar o contrato nem
seu valor. A ressalva de taxa não definitiva não autoriza fabricar o valor
observado ou atribuir-lhe a primeira posição. O numerador observado não foi dado.
O histórico cumulativo pode sustentar limites sob hipóteses de identidade
consistente, mas um limite histórico não é uma observação MOB2.

Representação fiel: dois contratos no denominador, um observado, identidade e
valor não informados, numerador observado indeterminado e taxa final pendente.
Classificação temporal depende de corte e datas validados; cenário hipotético
precisa permanecer identificado como hipotético.

## Próximo passo causal

A SKILL publicada já contém proibição específica de inventar ID, target ou causa
de ausência nesse exemplo. Antes de nova edição, coletar **SD-VF-P-D01** em chat
novo com seleção real da skill pelo seletor @ e o mesmo prompt literal. Isso testa
a resposta com seleção explícita; não comprova retroativamente a seleção
espontânea nem substitui SD-VF-P ou SD-VF-A. Se o comportamento falhar novamente,
a evidência sustentará nova investigação/correção de instruções ou execução.

Sem edição de produto nem republicação nesta análise. SAFRA-UI-01 permanece
aberto para a falha residual; a eficácia completa da correção não foi demonstrada.

Auditoria independente confirmou o FAIL residual e o diagnóstico D01 antes de
nova edição textual. Seleção explícita observada não comprova roteamento
automático nem, sozinha, os bytes efetivamente carregados.
