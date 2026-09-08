# Playbook — Ciclo de vida de uma mudança no ecossistema

Procedimento completo para alterar qualquer coisa em `ambiente_fonte/` e levá-la
até os workspaces. A mesma sequência aparece, em diagrama, no `README.md` da raiz
e, em forma de comandos, no `ambiente_fonte/README.md` — os três descrevem a
mesma ordem, e divergir de qualquer um deles é defeito nos três.

```mermaid
flowchart LR
  E["1. Editar"] --> V["2. Validar"] --> R["3. Renderizar"]
  R --> P["4. Publicar<br/>--execute + --verify"]
  P --> T["5. Testar conforme impacto<br/>smoke · forward · prompts"]
  T --> G["6. Registrar<br/>CHANGELOG + commit"]
  G --> W["7. Replicar<br/>runbook manual"]
```

## 1. Editar

- Edite apenas `ambiente_fonte/` (regra `fonte-de-verdade.md`).
- Skills: mantenha frontmatter `name`+`description`, imperativo, progressive
  disclosure (detalhe grande vai para `templates/` da própria skill).
- Instruções: vigie o limite de 20.000 caracteres.

## 2. Validar

```powershell
python tools/validate_assistant.py
```

Só siga adiante com exit 0. `WARN` de tamanho: avalie progressive disclosure.

## 3. Renderizar

```powershell
python tools/render_simulado.py --write
```

## 4. Publicar no Free

```powershell
python tools/publicar_free.py            # plano (dry-run)
python tools/publicar_free.py --execute --profile <free> --expected-host <url-free>
python tools/publicar_free.py --verify --profile <free> --expected-host <url-free>
```

Dry-run por padrão; `--execute` é gate consciente. O `verify` é obrigatório: a
publicação relata o que enviou, ele confere o que existe — inclusive arquivos
obsoletos, que `import-dir --overwrite` nunca remove (ADR-0005).

## 5. Testar conforme o impacto

Nem toda mudança exige todos os testes. A classe alterada decide o gate:

| Mudança | Gate antes do commit |
|---|---|
| helper, Python, Spark ou ML | smoke no runtime Databricks |
| `name`, `description` ou fronteira de skill | forward tests positivo, negativo e `@menção` |
| contrato ou comportamento de prompt | resposta real no Genie Code e registro no notebook de exemplo |
| somente governança fora do produto | validação local; nenhum runtime por reflexo |

Execute em chat novo quando o gate for conversacional. Falha não vira ajuste de
`description` ou relaxamento do teste sem antes isolar se o defeito está no
produto, no instrumento ou na cota.

## 6. Registrar

- Entrada no `CHANGELOG.md` (template `.claude/templates/changelog-entry.md`).
- Decisão estrutural → ADR; sessão interrompida → handoff.

O changelog pode ser rascunhado durante o trabalho, mas só é fechado **depois**
do `--verify` e dos testes pertinentes. A entrada cita contagens e evidência
real; registrar antes é escrever de memória o número que o comando ainda não
produziu.

## 7. Replicar no trabalho (fase 4 — runbook)

Geração do ZIP mínimo por `tools/bundle_implantacao.py` e cópia manual para o
workspace do trabalho, com mapeamento do placeholder para o destino. Procedimento completo no
[runbook de replicação](replicacao-trabalho.md), com o
[checklist](checklist-replicacao.md) para marcar durante a execução. Os
pré-requisitos e guardrails estão em `.claude/skills/replicar-trabalho/`.

## Fontes

- Diagrama equivalente: [`README.md`](../../README.md) da raiz, seção "Ciclo de
  contribuição"
- Comandos na forma copiável: [`ambiente_fonte/README.md`](../../ambiente_fonte/README.md)
- Camadas e o que é editável: `.claude/rules/fonte-de-verdade.md`
- Por que a conferência é obrigatória: [ADR-0005](../decisions/ADR-0005-publicacao-propria-no-free.md)
  e [ADR-0008](../decisions/ADR-0008-criterios-de-conferencia-da-publicacao.md)
- Passo 7 em detalhe: [runbook de replicação](replicacao-trabalho.md)
