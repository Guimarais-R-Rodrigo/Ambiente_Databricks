# B1 Autonomous Controller journal

Esta pasta é o único root documental livre para registros novos do controller A1.

Regras:

- nunca reescrever evidência histórica em `../G6/` ou checkpoints `../P2_*.md`;
- cada run record novo identifica base/candidate SHA, controller state, causal delta,
  gates executados e findings;
- autorização de projeto nunca nasce deste journal;
- não copiar tokens, usernames, homes reais ou paths sensíveis;
- `AUTHORING_STATE.json` continua sendo o state source vivo;
- este journal é evidência operacional complementar, não substitui manifests,
  outputs RAW ou verifiers.

Arquivos devem ser append-only por identidade: não reutilizar nome de uma rodada
anterior para reescrever seu resultado.
