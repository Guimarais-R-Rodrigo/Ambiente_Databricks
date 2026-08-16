# Sprint 2 — Renomeação, limpeza e realocação

Data: 2026-08-16 · Executor: Claude · Escopo: todas as camadas vivas do
repositório e o workspace Free.

A auditoria do plano elegeu esta como a sprint de maior risco: alto volume, com
destino que não existia, sem limpeza remota prevista e com números de escopo
inflados em 27%. Os quatro problemas foram corrigidos no plano v2 antes da
execução.

## O que mudou

| Antes | Depois |
|---|---|
| `x_snippets/` | `hub_snippets/` |
| `x_scripts/` | `hub_scripts/` |
| `x_prompts/` | `hub_prompts/` |
| `x_docs/` | **removida** — conteúdo realocado |
| `x_config/` | **removida** |
| `x_projects/` | **removida** |
| `/Users/<user>/x_lab/` no workspace | `hub_lab/` |

`.assistant/` agora tem quatro diretórios `hub_` mais `skills/`, e dois arquivos
de referência no nível de topo.

## Verificação

```text
validate_assistant.py   APROVADO: 0 falha(s), 0 aviso(s)
render_simulado.py      OK: 187 arquivos
publicar_free.py        APROVADO: 0 problema(s) — obsoletos: 0, extensões 4/4 hub_
smoke test (job real)   77 verificações | 70 PASS | 0 FAIL | 7 opcionais ausentes
```

O smoke test é o número que importa: **idêntico ao de antes da renomeação**.
Mesma contagem, mesmos resultados. A biblioteca continua importando, e a
renomeação não quebrou nada em runtime.

## Substituição por tabela fechada, não por regra de prefixo

A auditoria mostrou que uma regra `x_ → hub_` produziria 43 links apontando para
`hub_docs/`, `hub_config/` e `hub_projects/` — pastas que não existem na
arquitetura alvo. A substituição foi feita por tabela explícita, com destino
declarado para cada alvo:

| Alvo antigo | Destino | Ocorrências |
|---|---|---|
| `x_docs/catalogo_helpers.md` | `.assistant/CATALOGO_HELPERS.md` | 71 |
| `x_docs/glossario.md` | `.assistant/GLOSSARIO.md` | 7 |
| `x_docs/notebooks/` | `hub_snippets/_notebooks_a_migrar/` | 5 |
| `x_docs/SKILL_TEMPLATE.md` | `hub_padroes/skill/template.md` | 2 |
| `x_docs/ROADMAP_SKILLS.md` | `docs/historico/` | 1 |
| `x_config/README.md` | `hub_padroes/README.md` | 5 |
| `x_projects/AGENTS_TEMPLATE.md` | `docs/historico/` | 4 |
| `x_snippets`, `x_scripts`, `x_prompts`, `x_lab` | renomeação pura | 341 |

**85 arquivos alterados**, contra os 601 de escopo que a v1 do plano previa — a
diferença é que o número da v1 media também as camadas que a §7.2 manda
preservar.

## Onde a execução divergiu do plano

**Os caminhos relativos.** A substituição textual descartava o `../` dos links,
e o caminho correto para `CATALOGO_HELPERS.md` depende de onde cada arquivo está:
`../../` a partir de uma pasta de skill, `../` a partir de `hub_snippets/`. Foram
38 links quebrados de uma vez. Corrigido recalculando a profundidade real de cada
arquivo com `os.path.relpath`, o que é a forma certa e que eu deveria ter usado
desde o início.

**O catálogo não foi dissolvido.** O plano previa absorvê-lo em
`hub_snippets/README.md`. Ele cobre `hub_snippets` **e** `hub_scripts`, então
ficou em `.assistant/CATALOGO_HELPERS.md`, no nível que corresponde ao seu
escopo, junto do glossário. A dissolução nos READMEs de seção continua prevista
para as Sprints 6–9; até lá, o destino existe e é publicado.

## As camadas preservadas

Nove documentos de `docs/testes/`, `docs/auditoria/` e `docs/handoffs/` receberam
uma nota de cabeçalho em vez de renomeação:

> **Nomenclatura da época.** Os nomes `x_*` e `rodrigo-*` neste registro são
> os que existiam na data. A tradução para os nomes atuais está na tabela de
> correspondência do [ADR-0006](../decisions/ADR-0006-identidade-hub.md);
> este documento não é reescrito porque descreve o que foi observado, não o
> estado atual.

Reescrever ali falsificaria o registro e contrariaria a regra do próprio projeto
sobre documento append-only.

`Ambiente_Antigo/` e `Ajustes_Codex/` não foram tocados — o primeiro é
git-ignored por conter identificador corporativo (ADR-0003).

## A limpeza remota, que a auditoria tornou obrigatória

Depois de publicar, a conferência acusou **121 arquivos obsoletos**: as seis
pastas antigas inteiras, vivas no workspace porque `import-dir --overwrite`
sobrescreve e nunca apaga.

Sem o passo de remoção que a §7.3 do plano acrescentou, o workspace teria
`x_snippets` **e** `hub_snippets` convivendo, e a verificação humana declarada na
v1 — "navegue e veja as três pastas ausentes" — teria retornado o resultado
errado. Removidas, a conferência voltou a `obsoletos: 0`.

## Ferramentas e regras atualizadas

- `EXPECTED_X_DIRS` virou `EXPECTED_HUB_DIRS`, de seis para **quatro** diretórios,
  com o rótulo impresso acompanhando: `extensões : 4/4 diretórios hub_`.
- `.claude/rules/genie-code-oficial.md` e `rules/docs-e-readmes.md` definiam `x_`
  como a convenção do projeto. Sem essa mudança, a regra canônica passaria a
  descrever o oposto do repositório. Feita agora, não na Sprint 12.
- `.claude/skills/publicar-free/SKILL.md`: "6 diretórios `x_`" → "4 `hub_`".
- Os dois playbooks de replicação fixam contagens que a reestruturação invalidou
  (174 arquivos, 6 diretórios, 12 pastas `rodrigo-*`). Receberam nota de
  desatualização com o comando que dá o número real; a reescrita é da Sprint 12,
  quando a conversão terminar.

## O que fica para a auditoria

- Se alguma referência órfã sobreviveu — em especial em arquivo `.py`, onde o
  validador só confere link markdown dentro de comentário.
- Se a nota de cabeçalho nas camadas preservadas é a solução certa, ou se seria
  melhor um mapa de correspondência em um lugar só.
- Se `_notebooks_a_migrar/` é uma pasta de trânsito aceitável, ou se ela vai
  sobreviver por esquecimento até alguém tropeçar nela.
- Se `.assistant/CATALOGO_HELPERS.md` e `GLOSSARIO.md` no nível de topo são o
  lugar certo, ou se criam um segundo índice competindo com o README.
- Se o `README.md` da raiz e o `.assistant/README.md`, que ainda não foram
  reescritos (Sprint 10), ficaram internamente consistentes depois da mudança.
