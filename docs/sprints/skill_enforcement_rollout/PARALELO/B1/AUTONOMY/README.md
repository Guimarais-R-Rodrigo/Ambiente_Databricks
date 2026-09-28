# B1 Autonomous Controller journal

A1 possui um único registro operacional versionado gravável: JOURNAL.jsonl.

Regras:

- README.md e qualquer outro arquivo desta pasta permanecem read-only para A1;
- cada linha nova do journal é um objeto JSON independente;
- o journal é append-only: truncar, reordenar ou reescrever linha anterior falha no delta checker;
- cada registro identifica, quando aplicável, base/candidate SHA, controller state, causal delta, gates e findings;
- autorização de projeto nunca nasce deste journal;
- não copiar tokens, usernames, homes reais ou paths sensíveis;
- AUTHORING_STATE.json continua sendo o state source vivo;
- o journal é evidência operacional complementar e não substitui manifests, RAW ou verifiers.
