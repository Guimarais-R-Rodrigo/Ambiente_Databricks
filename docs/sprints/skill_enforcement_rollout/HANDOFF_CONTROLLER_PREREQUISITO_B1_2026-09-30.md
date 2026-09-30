# Handoff — pré-requisito documental do controller para B1

(Codex) Decisão do usuário em 2026-09-30: integrar **separadamente** duas
correções preexistentes de SHA completo nos changelogs. Sem uma conversa ativa
do controller, o usuário pediu que o Codex resolvesse a separação. O commit
local `222420a1` foi criado em `codex/b1-controller-changelog-prereq` apenas
com esses dois hunks. Esta nota não pede manutenção de código, hooks, policy
ou runtime do controller; o commit **não foi enviado nem mesclado**.

O patch restrito está no checkout B1 autorizado em
`.artifacts/skills-delivery-evidence/b1-review-patches-20260930/00-controller-changelog-prereq.patch`
(2.920 bytes; SHA-256
`14c444129a66894125fba2d5f2aaaa6c1b40bfdaf4f8fd4b4e8f6f2c0208d715`).
É um artefato local ignorado pelo Git. Contém somente:

1. Uso do SHA completo `c96485259c3ee08cae466a0038ee3c3de2f9358d` em
   `docs/sprints/skill_enforcement_rollout/PARALELO/B1/CHANGELOG.md`.
2. A mesma expansão na entrada de 2026-09-27 do `CHANGELOG.md` raiz.

O patch **não inclui** `.codex/config.toml`, hooks, produto B1 ou MM04. Os dois
trechos já estavam alterados no checkout compartilhado por outra frente; não
foram escritos nem atribuídos ao B1 nesta preparação.

Em `C:\b1_runtime\b1_controller_patchcheck_20260930`, worktree destacado e
limpo criado de `d6cd9fd39f3e82ccf9db6f9e0c61db526fe3a143`, foi conferida
a sequência `00-controller-changelog-prereq.patch` →
`01-b1-delivery.patch` → `02-mm04-integration.patch` →
`03-b1-changelog.patch`. Cada `git apply --check` e aplicação passou. Depois
da sequência, `python -B tools/validate_assistant.py --root ambiente_fonte`
aprovou com zero falhas/avisos e 68 testes focais passaram. Isso demonstra a
dependência de integração; **não é um PASS independente do patch controller**.

O commit registra na mensagem que empacota alterações preexistentes da outra
frente; não reivindica autoria original. A branch
`codex/b1-review-after-prereq` foi criada a partir de `222420a1` e recebeu um
commit candidato local, sem incluir `.codex/config.toml`. Antes de qualquer
merge, o responsável pela integração Git ainda deve revisar a relação entre
as duas branches e os limites de
autoridade do ADR-0025. Não aplicar o patch ao checkout B1 compartilhado,
onde os trechos já estão presentes.

O B1 permanece em revisão local, sem publicação, push ou merge.
O [índice do pacote B1](PACOTE_REVISAO_B1_2026-09-30.md) separa os patches e
os limites da homologação Genie.
