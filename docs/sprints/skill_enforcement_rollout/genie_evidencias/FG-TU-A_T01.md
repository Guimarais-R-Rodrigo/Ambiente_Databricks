# FG-TU-A/T01 — @ Tutor com efeito não comprovado — 2026-09-30

(Codex) Prompt e resposta originais preservados em
`.artifacts/skills-delivery-evidence/genie-20260930-tutor-a/response-original.txt`;
SHA-256 `a9d864c97899471a9488f567e2f3154d5fe8ab9eab6f56255fd688c5767f0d3a`.
O usuário confirmou chat novo, seleção de `@hub-ml-tutor-databricks` e
indicador separado de carregamento. A transcrição começa com
`hub-ml-tutor-databricks ricks`: variante semântica do prompt preparado,
não envio literal byte a byte.

## Versão e efeitos

O pacote B1 anteriormente verificado tinha hash normalizado
`7bdb98eefe937ed0e2510b5ac077afefe970f4409eb828f920cd8634ab8d4b6d`.
Após publicação paralela de micromodelos relatada pelo usuário, a versão
remota efetiva desta coleta não foi conferida. O texto do Genie declara
leitura da skill e faz referência a contexto de notebook, mas a transcrição
não traz evento de leitura, export do notebook, output de célula ou histórico.
Nenhuma escrita, consulta, execução ou criação de tabela foi observada.

## Vereditos separados

- Roteamento @: **PASS por seleção e indicador confirmados pelo usuário**.
- Explicação da intenção: **PASS parcial**. Reconheceu a escrita Spark como
  efeito pretendido, o risco de `overwrite` e o destino sem qualificação.
  Respeitou o pedido de não executar na evidência recebida.
- Proveniência e status: **FAIL**. Apesar da ausência explícita de saída,
  histórico e ambiente no prompt, afirmou que a célula “nunca [foi]
  executada”, `df` não existe, o notebook só tem uma célula vazia, não há
  compute e não há tabela materializada. A transcrição menciona contexto
  de notebook vazio; sem export ou evento verificável, isso não prova o
  histórico da célula hipotética recebida nem o estado da tabela. O
  correto seria **execução, existência da tabela e estado remoto não
  informados**. A skill já exige essa distinção explicitamente.
- Precisão técnica: **ressalva**. Tratou `overwrite` como sempre irreversível
  e `saveAsTable` como sempre tabela gerenciada; são afirmações categóricas
  sem contrato de formato/destino/ambiente no prompt. `main.default` foi
  apresentado apenas como exemplo típico, mas não é destino demonstrado.
- Execução: **NOT_RUN na evidência fornecida**; nenhum Receipt ou readback.

**Veredito T01: PASS de seleção, FAIL material de status/proveniência.**
O caso não homologa a resposta da Tutor. Preservar a primeira tentativa;
investigar se houve contexto adicional do notebook e só retestar após uma
hipótese causal concreta. Nenhuma edição de produto ou publicação nesta coleta.
