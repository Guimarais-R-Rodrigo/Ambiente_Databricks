# Template — Auditoria multi-LLM

Pasta: `docs/auditoria/YYYY-MM-DD_<tema>/`. Padrão herdado do Verg_Alchemy_Hub
(`docs/playbooks/auditoria-multillm.md` do Hub).

```text
docs/auditoria/YYYY-MM-DD_<tema>/
├── 01_contexto.md      # escopo, nível (A0–A3), fontes permitidas, papéis por IA
├── 02_<ia1>.md         # rodada individual (achados por severidade + evidência)
├── 03_<ia2>.md
├── 04_<ia3>.md         # conforme o nível exigir
└── 99_consenso.md      # consenso, divergências, decisão final, riscos residuais
```

`01_contexto.md` deve declarar: motivo do nível escolhido, o que está fora de
escopo, e o pacote exato de arquivos que cada IA recebeu (sanitizado se preciso).

`99_consenso.md` fecha com: lista priorizada de ações, quem executa, e critério
de verificação de cada uma. Divergência não resolvida vira `PENDENTE/DECISAO`
com dono.

Níveis (mínimo de LLMs): A0_light (1), A1_standard (2), A2_strict (3),
A3_incident (3+). Nunca reduza o nível quando houver dado sensível, produção,
publicação externa ou decisão que afete a squad/missão.
