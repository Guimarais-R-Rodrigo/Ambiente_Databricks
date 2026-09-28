# Autonomy envelopes

O protocolo define **como** o controller trabalha. O envelope define **o que** uma frente pode fazer autonomamente.

Regras:

- um envelope não altera policy;
- A2 exige referência humana explícita;
- A3 nunca pode ser ativada como autonomia;
- budgets são limites, não metas;
- uma nova frente usa novo envelope;
- alterar autoridade do envelope exige registro humano; o executor não autoativa A2.

Schema: [autonomy-envelope.schema.json](autonomy-envelope.schema.json).

Envelope piloto: [B1_AUTONOMY_ENVELOPE.json](B1_AUTONOMY_ENVELOPE.json).

Tool-surface policy canônica do runtime Windows: [CODEX_CLI_TOOL_SURFACE_POLICY.json](CODEX_CLI_TOOL_SURFACE_POLICY.json). A policy Desktop é histórica e não autoriza controller no aplicativo Desktop.
