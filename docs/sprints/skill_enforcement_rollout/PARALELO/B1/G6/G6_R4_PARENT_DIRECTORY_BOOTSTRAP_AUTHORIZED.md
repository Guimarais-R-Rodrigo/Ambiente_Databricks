# G6 R4 — parent-directory bootstrap authorization

Authorization reference:

`issue#114:comment#5836769448`

Authorized effect:

`REMOTE_DIRECTORY_CREATE`

Allowed directory paths, and no others:

1. `.assistant/hub_scripts/skill_execution/domain_context`
2. `.assistant/skills/hub-ml-analise-safra/scripts`
3. `.assistant/skills/hub-ml-cross-eda-ml/scripts`

For each path:
- verify the exact parent exists as `DIRECTORY`;
- if the child already exists as `DIRECTORY`, do not create;
- if the child is absent, one `workspace mkdirs` for that exact child is authorized;
- if the child exists as another type or parent verification fails, stop.

After all three are proven present as `DIRECTORY`, the user also authorized reinvocation of frozen R4 using the still-unconsumed write authorization:

`issue#114:comment#5836601472`

No full republish, material-write retry after consumption, extra mkdirs, probes, Genie, cleanup, promotion, Ready or merge is authorized.
