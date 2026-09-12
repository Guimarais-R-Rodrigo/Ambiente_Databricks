# Ambiente_Databricks — Contexto canônico

Este arquivo é a entrada canônica do projeto para o Claude e a fonte primária
que Codex, Gemini e outras IAs devem respeitar (via `AGENTS.md` e `GEMINI.md`).

## O que é este projeto

Laboratório de engenharia do ecossistema `.assistant` (Agent Skills + instruções +
extensões) do **Databricks Genie Code**, usado no trabalho do Rodrigo (CRM bancário,
missão de modelos de ML). O ciclo é: editar aqui → validar → renderizar →
publicar no Databricks Free (testes) → replicar manualmente no workspace do trabalho.
Escala planejada: pessoal → squad → missão.

## Antes de qualquer tarefa, leia

1. `.claude/CLAUDE.md` — índice operacional (o que ler para cada tipo de tarefa).
2. As regras em `.claude/rules/` relevantes à tarefa.
3. `CHANGELOG.md` — o que as outras IAs fizeram recentemente.

## Fonte única de verdade

| Camada | Local | Papel |
|---|---|---|
| Canônica | este repositório (git) | única fonte editável |
| Produto | `ambiente_fonte/` | ecossistema `.assistant` que será implantado |
| Derivada | `Novo_Ambiente_Simulado/` | espelho renderizado; **nunca editar à mão** |
| Operacional | workspaces Databricks (Free e trabalho) | cópias publicadas; nunca canônicas |
| Congeladas | `Ambiente_Antigo/` (local-only) | referência histórica read-only |

## Decisões ativas

- Arquitetura multi-IA e este layout: `docs/decisions/ADR-0001-arquitetura-multi-ia.md`.
- `Ambiente_Antigo/` é git-ignored por conter identificadores corporativos:
  `docs/decisions/ADR-0003-quarentena-ambiente-antigo.md`.
- Helpers declarados explicitamente nas skills:
  `docs/decisions/ADR-0004-declaracao-explicita-de-helpers.md`. O ADR-0011 acrescenta
  descoberta solicitada e progressiva pelo Concierge, sem remover essas declarações.
- Publicação no Free usa `tools/publicar_free.py`, não o engine do Hub:
  `docs/decisions/ADR-0005-publicacao-propria-no-free.md`, que **supersede o
  ADR-0002** — o engine publicava `.py` como notebook e quebraria os imports da
  biblioteca. O **critério de conferência** foi atualizado pelo `ADR-0008`, que o
  tirou do texto e o pôs em constante de código.
- O catálogo de helpers e a forma de pasta por objeto: `ADR-0007`, que supersede
  o `ADR-0004` em localização e forma. A declaração explícita de helpers, decidida
  lá, continua valendo.
- Identidade `hub_`/`hub-ml-`, com a tabela de correspondência `rodrigo-*` →
  `hub-ml-*`: `ADR-0006`. Ele **não supersede nada** — complementa o ADR-0001 e o
  ADR-0004.
- Identidade neutra no conteúdo ativo e pacote mínimo de implantação com
  manifesto: `ADR-0009`.

- Manual Técnico unifica o catálogo e o glossário: `ADR-0010`. Autoria em
  `ambiente_fonte/.assistant/MANUAL_TECNICO.md`; cópia de leitura idêntica na raiz.

- Concierge integrado como entrada opcional de descoberta/composição: `ADR-0011`.
  Publicação e homologação conversacional são gates separados da integração Git.

- README didático por pasta de objeto: proposta `ADR-0012`; contrato candidato e piloto R02 em revisão.
  Estado e retomada: `docs/sprints/readmes_objetos/README.md`.

- Sistema de Temas: contrato central e configuração completa por contexto
  aceitos no `docs/decisions/ADR-0013-sistema-de-temas.md`. A V01 está aceita
  e integrada no Git; fixtures são entradas de teste, não temas operacionais
  aprovados. Sem seletor instalado, mudança visual ou publicação no Databricks.
  Homologação operacional permanece pendente. Estado, limites e retomada:
  `docs/sprints/sistema_temas/V01/CHECKPOINT_V01.md`.

O índice completo, com o status de cada ADR, está em `docs/decisions/README.md`.

## Regras inegociáveis

- Toda sessão que altera algo termina com entrada no `CHANGELOG.md`
  (template em `.claude/templates/changelog-entry.md`), atribuída à IA autora.
- Nenhum identificador corporativo, path real do trabalho, PII ou segredo entra
  em arquivo versionado. Placeholders sempre. **Uma exceção, decidida e
  registrada:** o nome da instituição na paleta visual (`AZUL_CAIXA` e afins) —
  ver `PLANO_HUB.md` §2.2. O `CORPORATE_RE` do validador não a alcança e não
  deve alcançar; qualquer outro identificador continua proibido.
- Afirmações sobre a plataforma Databricks seguem a nomenclatura oficial vigente
  (`.claude/rules/genie-code-oficial.md`); em dúvida, verificar a documentação
  antes de afirmar.
- Não duplique regra longa entre arquivos: mova para `.claude/` e referencie.
