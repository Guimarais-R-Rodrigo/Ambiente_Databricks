# Pacote de revisão isolado B1 — 2026-09-30

(Codex) Este pacote transforma o checkout B1 compartilhado e não commitado em
patches revisáveis, sem fazer staging, commit ou merge nele. O ponto de partida é
`d6cd9fd39f3e82ccf9db6f9e0c61db526fe3a143`. Os patches representam um
**snapshot anterior à criação deste índice e à sua entrada no changelog**; estes
dois registros editoriais devem ser revisados junto com o pacote, mas não estão
incluídos nos patches congelados.

O [fechamento técnico](FECHAMENTO_TECNICO_B1_2026-09-30.md) é dono dos gates
locais/Free e a [consolidação Genie](CONSOLIDACAO_GENIE_B1_2026-09-30.md) é dona
dos vereditos por skill. Este índice é dono apenas da separação de autoria e da
reprodução dos diffs. Não converte os testes locais em homologação Genie.

## O que revisar

Os artefatos ficam em
`.artifacts/skills-delivery-evidence/b1-review-patches-20260930/` no checkout
autorizado e são ignorados pelo Git. O manifesto por caminho fica em
`.artifacts/skills-delivery-evidence/b1-review-manifest-20260930.json` (SHA-256
`0650c2365736d5b054a4bb8e342d5b4edd0c5414240efae75c09852b5b116929`).
O checkout isolado de leitura é `C:\b1_runtime\b1_review_20260930`.

| Patch | Escopo | Bytes | SHA-256 |
|---|---|---:|---|
| `00-controller-changelog-prereq.patch` | Somente dois hunks preexistentes de SHA completo em changelogs; pré-requisito separado escolhido pelo usuário | 2.920 | `14c444129a66894125fba2d5f2aaaa6c1b40bfdaf4f8fd4b4e8f6f2c0208d715` |
| `01-b1-delivery.patch` | 271 caminhos B1 | 1.510.551 | `a471d5bbdac19e517de5f77fa4b93c7c5b71218039b0e23391f182765d804ffa` |
| `02-mm04-integration.patch` | 21 caminhos compartilhados B1/MM04 e sete dedicados MM04, incorporados por decisão do usuário | 76.463 | `7def36ffa9dd9b61fd39343c495c6070f9c403d015c0df26d049b39e56a1a9af` |
| `03-b1-changelog.patch` | Entradas B1 de `CHANGELOG.md`, sem o trecho do controller | 42.087 | `053fb1fc98e9684ec66cf1773043e085927b37dbc6c3e080b8b7ae27324e8b3b` |
| `04-pass-through-context.patch` | Configuração humana e correções preexistentes do controller, somente para reproduzir a validação | 5.106 | `add123ee02895dcce1b488603f51ec312000c1df4d1bb69f33c87b070e691bc6` |
| `review-full-context.patch` | União aplicável dos quatro componentes, para conferência isolada; não define ownership de merge | 1.634.207 | `92d0a2bf9fc7d90c51b279d6977abb2a8d3859a671188b945e6ae8d373ac584d` |

O manifesto classifica **302 caminhos físicos**: 271 B1, 21 compartilhados
B1/MM04, sete MM04, um changelog misto e dois pass-through. O changelog misto
aparece em dois patches por hunk, sem duplicar sua contagem de caminho.
`04-pass-through-context.patch` inclui `.codex/config.toml`,
`docs/sprints/skill_enforcement_rollout/PARALELO/B1/CHANGELOG.md` e o hunk do
controller no `CHANGELOG.md`; **nenhum desses trechos é reivindicado como
entrega B1**. A configuração humana `:workspace/on-request` e a remoção dos
hooks foram preservadas.

## Reprodução e resultado

Em `C:\b1_runtime\b1_patchcheck_20260930`, um segundo worktree destacado
criado do mesmo commit base, `git apply --check review-full-context.patch` e
`git apply review-full-context.patch` passaram. O validador
`python -B tools/validate_assistant.py --root ambiente_fonte` passou com **zero
falhas e zero avisos** após a aplicação. Na cópia de revisão, o espelho tinha
657 arquivos gerenciados sem divergência e os 68 testes focais passaram.
Comparados aos arquivos do checkout compartilhado, os 302 caminhos aplicados
tinham zero divergências de conteúdo após normalização de fim de linha; 33
divergiam apenas em CRLF/LF. Não houve publicação nem execução nova no Genie.

O patch integral emitiu **17 avisos de whitespace** na aplicação; o
`git diff --check` com os arquivos novos incluídos por intent-to-add também
aponta espaços finais ou linha vazia no fim de transcrições brutas e de alguns
arquivos novos. As transcrições são evidência histórica e seus bytes não foram
reescritos para silenciar o aviso. Os avisos nos scripts e na documentação
devem ser avaliados antes de um commit, pois corrigi-los agora alteraria hashes
já vinculados à publicação Free. O `git diff --check` anterior do checkout,
sem incluir untracked, havia passado; ele não cobria esses arquivos novos.

O patch B1 isolado **não recebeu um PASS independente do validador**: ao retirar
as correções preexistentes de SHA completo no contexto controller, o validador
reprovou duas referências abreviadas nos changelogs. O PASS acima vale para o
snapshot integral com `04-pass-through-context.patch`. Um integrador deve obter
essas correções do dono ou incluí-las como dependência explícita, nunca
atribuí-las silenciosamente ao B1.

Após a decisão humana por integração separada, foi criada uma sequência nova
no checkout limpo `C:\b1_runtime\b1_controller_patchcheck_20260930`:
`00-controller-changelog-prereq.patch` → `01-b1-delivery.patch` →
`02-mm04-integration.patch` → `03-b1-changelog.patch`. As quatro aplicações e
respectivos `git apply --check` passaram, sem `.codex/config.toml`. O validador
aprovou com zero falhas/avisos e os 68 testes focais passaram após essa
sequência. O [handoff do pré-requisito](HANDOFF_CONTROLLER_PREREQUISITO_B1_2026-09-30.md)
registra o escopo e o commit local resultante.

Como não havia mais conversa ativa do controller, o usuário pediu que o Codex
resolvesse a separação. O pré-requisito documental virou o commit **local**
`222420a1` na branch `codex/b1-controller-changelog-prereq`, com somente os
dois changelogs e validador independente aprovado (0 falhas/avisos). A branch
`codex/b1-review-after-prereq` nasceu desse commit e recebeu apenas os patches
`01`, `02` e `03`; nenhum patch de configuração humana foi aplicado nela.
O resultado foi registrado em commit candidato local nessa branch. Essas
branches não foram enviadas ou mescladas.

## Limite de integração

A fonte B1 correspondeu aos **657/657 arquivos gerenciados** no readback do
Databricks Free. O inventário remoto geral segue FAIL por 30 objetos extras em
`.assistant/hub_micromodelos/`, publicados pela frente paralela; eles não estão
nos patches e não foram apagados. MM04 já integra a skill e o catálogo B1 por
autorização anterior, mas seu runtime remoto paralelo continua sob a outra
frente. Nenhum patch é autorização de promoção de policy, Ready, merge ou
replicação no workspace de trabalho.

O próximo passo é revisar os dois commits locais e decidir o encaminhamento
Git das branches separadas; push e merge exigem decisão própria. O checkout
compartilhado permanece dirty e sem staging B1. A homologação Genie permanece
parcial, conforme a consolidação.
