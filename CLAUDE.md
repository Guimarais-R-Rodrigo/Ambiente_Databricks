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

- README didático por pasta de objeto: `ADR-0012`, ratificado em 2026-09-12;
  contrato **1.0.0** vigente. A iniciativa própria R00–R13 foi aceita e encerrada
  no Git após PR #33 (`b0e953cc`) e fechamento documental PR #34 (`99e01012`):
  **75/75 operacionais, 3/3 exemplares e 0 pendências**. A auditoria final é
  `A0_light`; não equivale a publicação nem homologação Databricks/Genie Code.
  Estado vigente: `docs/sprints/readmes_objetos/README.md`.

- Sistema de Temas: contrato central e configuração por contexto definidos em
  `docs/decisions/ADR-0013-sistema-de-temas.md`. **V00–V09 estão integradas no
  Git.** A V08 alinhou skills, Hub Padrões, entrada `.assistant`, template EDA e
  Manual Técnico às fontes de verdade visuais; a V09 levou o contrato temático ao
  kit offline de transição com guarda de presença/integridade, sem transformar
  transporte em ativação ou publicação. A integração V09 ocorreu pelo PR #45
  (`0f7234c4734f1974ebb1a20123f3c26626c67ef3`) e a correção de preparação Node
  do workflow pelo PR #46 (`4ae714a35a0aafd930a8cd796d962b0a79449b88`).
  Integração Git não equivale a publicação Databricks nem a homologação de
  browser/runtime, acessibilidade, ACL, UAT ou promoção visual. Estado vigente:
  `docs/sprints/sistema_temas/README.md`.

O índice completo, com o status de cada ADR, está em `docs/decisions/README.md`.

## Iniciativa de micromodelos — proposta MM00

A branch `micromodelos/mm00-baseline` e a PR #43 registram a fundação documental
da iniciativa MM00–MM13 em `docs/sprints/micromodelos/`. Os ADRs 0014–0020 estão
**propostos**, não aceitos: micromodelo como artefato de domínio; YAML canônico;
MLflow para runs; governança externa como autoridade de publicação; piloto novo
antes dos legados; consumo do Sistema de Temas; e fonte limitada ao catálogo de
Produtos de Dados configurado no ambiente autorizado.

A auditoria A1 independente foi executada sobre a candidata pré-V09 e devolveu
`APTA_COM_CORRECOES`: não encontrou `DIVERGE` atribuível à arquitetura, apontou
M-01 documental (corrigido) e Q-01 pela ausência de entrada própria da MM00 no
`CHANGELOG.md` (ainda bloqueador). A candidata foi depois reconciliada com a V09
integrada e deve repetir seus gates antes de qualquer aceite.

MM00 não altera o produto `.assistant` e não autoriza MM01. O avanço exige checks,
fechamento ou exceção humana explícita do Q-01, decisão sobre os ADRs, checkpoint,
aceite explícito e merge. Identificadores, nomes de catálogo e paths reais do
ambiente de trabalho permanecem fora do Git; os documentos usam placeholders e
resolvem o binding somente no workspace autorizado.

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

### Estado vigente dos READMEs de objeto
A migração estrutural terminou na R11 e a iniciativa R00–R13 foi encerrada após a
auditoria final R13 e o fechamento documental pós-merge. O contrato vigente é
`readme-objeto: 1.0.0`; os 75 objetos do escopo R00–R13 continuam cobertos, os três
exemplares permanecem separados e `CONTROLE_MIGRACAO.json` está em
`phase=complete` com `pending={}`. Objetos adicionados depois desse encerramento,
como `hub_snippets.visual.theme_lab`, devem entrar diretamente no mesmo contrato;
a cobertura corrente deve ser medida pelo validador, não inferida dos números
históricos R00–R13.

Para manutenção futura, todo novo snippet, script ou prompt precisa entrar já com
README no mesmo contrato; reintroduzir dispensa é regressão. Use o
[estado vigente](docs/sprints/readmes_objetos/README.md), o
[relatório final R13](docs/sprints/readmes_objetos/RELATORIO_R13.md) e o
[contrato editorial](ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md).
Cobertura estrutural não é homologação de runtime, publicação no workspace nem
auditoria independente.