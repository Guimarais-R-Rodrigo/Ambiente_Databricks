# Manutenção assistida por IA

Entrada comum para quem mantém o repositório. Comece pelo [AGENTS](../../AGENTS.md),
escolha uma rota e obtenha o resultado indicado. Estes arquivos não são o produto
publicado no Databricks e não carregam referências automaticamente.

## Rotas

| Intenção | Leia antes de agir | Procedimento ou resultado | Gate e autoridade |
|---|---|---|---|
| Entender o projeto | [Projeto](context/projeto.md), [ambientes](context/ambientes.md) | localizar owner e sondar condições atuais | fonte datada não atesta acesso atual |
| Editar skills/instruções/helpers do produto | [Fontes](rules/fontes-e-derivados.md), [Databricks](references/databricks-genie-code.md), fonte em `ambiente_fonte/` | identificar contrato e arquivo editável | validador; autorização não decorre da skill |
| Validar | [validar-assistant](../../.agents/skills/validar-assistant/SKILL.md) | interpretar contadores, WARN/FAIL e exit code | validação local não prova runtime |
| Preparar render | [Fontes](rules/fontes-e-derivados.md#render), [render-simulado](../../.agents/skills/render-simulado/SKILL.md) | plano e inventário do destino/extras | escrever só no escopo autorizado |
| Preparar publicação Free | [Ambientes](context/ambientes.md), [publicar-free](../../.agents/skills/publicar-free/SKILL.md) | plano remoto, destino, efeitos e verificações | CLI/host/profile conferidos; execute autorizado; verify e conteúdo separados |
| Testar roteamento | [forward-test-skills](../../.agents/skills/forward-test-skills/SKILL.md) | casos positivo/negativo/@ em sessão nova | evidência observada da interface; campanha vinculada ao SHA |
| Preparar replicação trabalho | [replicar-trabalho](../../.agents/skills/replicar-trabalho/SKILL.md), [runbook](../playbooks/replicacao-trabalho.md) | kit/manifesto, backup, staging e gates humanos | cópia manual autorizada; Free não certifica trabalho |
| Documentar | [Documentação](rules/documentacao.md) | owner, leitor e próxima ação claros | links, estrutura e revisão editorial |
| Criar objeto | [Contrato 1.0.0](../../ambiente_fonte/.assistant/hub_padroes/readme/template_objeto.md), [checklist](../../ambiente_fonte/.assistant/hub_padroes/readme/checklist_objeto.md) | README na mesma mudança | ratchet e cobertura atual do validador |
| Coordenar/encerrar/retomar | [Colaboração](rules/colaboracao.md), [changelog](templates/changelog-entry.md), [handoff](templates/handoff.md) | autoria real, diff, evidência e bloqueios | sem sobrescrever alheios nem criar autorização |
| Decidir arquitetura | [Índice de ADRs](../decisions/README.md), [template](templates/adr.md) | decisão com alternativas e alcance | aprovação de projeto; corpo histórico imutável |
| Auditar | [Colaboração](rules/colaboracao.md#auditoria), [template](templates/auditoria.md) | corpus, independência, rodadas e consenso | A0–A3; bloqueio se independência exigida faltar |
| Alterar carregamento/compatibilidade | [Compatibilidade](compatibility.md), [registro oficial](standards/registry.json), [ADR-0025](../decisions/ADR-0025-arquitetura-instrucoes-ia.md) | confrontar documentado e observado por superfície | sessão nova e testes reais; nenhum settings implícito |

## Owners

- [Catálogo do mantenedor](../../.agents/skills/README.md): exatamente cinco procedimentos
  desta camada. `revisar-docs-oficiais` continua proposta inexistente; consultar
  fontes e manter registro não cria uma sexta skill.
- [Política executável](../../tools/project_policy.py): nomes de skills e diretórios
  geridos do produto. Não usar as quantidades de campanhas antigas.
- [Validador](../../tools/validate_assistant.py) e
  [contrato README](../../tools/readme_objeto_contract.py): cobertura medida.
- [Manual canônico](../../ambiente_fonte/.assistant/MANUAL_TECNICO.md): catálogo
  integrado e glossário, sem uma versão concorrente em docs/ai.
- [Índice de decisões](../decisions/README.md) e [owners vivos](context/projeto.md#owners-vivos):
  estado atual das frentes; [observações de 2026](context/observacoes-2026.md) são história.
- [Mapa de controle](control-map.json): obrigações, origens, destinos, rotas,
  preservações e testes. Adaptação não pode criar regra editorial concorrente.

## Camadas

AGENTS contém invariantes; `context/` fornece contexto e observações separadas;
`rules/` detalha condições de trabalho; `references/` distingue fontes oficiais
de convenções; `templates/` contém quatro modelos parametrizados. As cinco skills
canônicas ficam em `.agents/skills/`, com automação em `tools/`. A árvore
`ambiente_fonte/.assistant/` e a instrução irmã pertencem ao runtime.

O exemplar de skill transportado pelo produto é material didático: não prova
instalação ou execução automática de uma skill de manutenção. O achado IA-12
sobre seu aviso de ativação continua encaminhado à manutenção documental do
produto, com owner no [mapa](control-map.json); a migração não o modifica.

## Compatibilidade

Uma fonte editorial não cria um carregador universal. O [registro](standards/registry.json)
e a [matriz](compatibility.md) distinguem DOCUMENTED, OBSERVED e SUPPORTED.
Codex, Claude Code, Gemini CLI e Grok Build têm superfícies e regras próprias;
chats/Projects/Gems/APIs recebem contexto explicitamente quando esse escopo for
aprovado. Não inferir autoload a partir da marca ou de um ZIP anexado.

Integrações são mínimas e geradas quando necessário, sem settings pessoais,
MCP, hooks, credenciais ou permissões implícitos. Nenhuma alegação de suporte
nativo é feita por este índice: testes indisponíveis ficam BLOCKED. A remoção
das origens antigas é trabalho do integrador, após cobertura e consumidores.

## Guardas locais de manutenção

`python tools/ai_controls.py --generate` faz o preflight de todos os destinos e
manifesto antes da primeira escrita: tipo, ownership, hash anterior, symlinks
(inclusive ancestrais) e hardlinks com `st_nlink > 1`. Um hardlink bloqueia o lote,
inclusive quando liga dois outputs geridos. Preserve o nome e os bytes externos;
não remova o vínculo alheio para contornar a falha. A proteção é local e não
certifica contenção contra mudanças concorrentes de filesystem nem junctions
Windows sem ensaio nesse host. `--check` continua somente leitura.

O [inventário de entradas nativas](native-entries.json) classifica os candidatos
AGENTS/override, CLAUDE/local, GEMINI e regras Markdown de famílias de clientes,
inclusive entradas novas ignoradas pelo Git. O gate exclui apenas a saída gerada
`.artifacts/` e a quarentena read-only; não inspeciona settings pessoais/globais
nem afirma carregamento nativo. Arquivos por diretório são extensões legítimas:
antes de adicioná-los, revise conteúdo e precedência, incremente `revision` e
registre path, mecanismo, papel, owner, condição, hash e motivo. Overrides devem
listar explicitamente em `shadows` o AGENTS irmão que substituem. Conteúdo alterado
exige revisão do hash; o manifesto não concede permissão nem dispensa o bloqueio
de histórico universal. A identificação é uma guarda estática, não análise
semântica completa de linguagem natural nem homologação de cliente.

A [identidade versionada](traceability-inventory.json) confere cada obrigação e
claim, não apenas seus grupos. Requer IDs únicos, owner e campos tipados, fonte
Git por SHA completo, linhas/trecho exatos e hash de blob quando registrado. As
duas codificações históricas de origem (`sha` e `commit`/`sha256`) são aceitas sem
reescrever citações. Um checkout sem esses commits falha com
`SOURCE_GIT_UNAVAILABLE`; use histórico completo, sem substituir a prova por HEAD.
O registry deve manter a paráfrase idêntica ao snapshot datado além de ID, URL,
data e hash. DOCUMENTED não é promovido pelo inventário ou pela validação.

Para crescer, dividir, remover ou reformular uma obrigação/claim legitimamente:

1. Preserve as revisões anteriores e toda evidência histórica congelada. Explique
   a decisão, owner e revisão em UTC; ajuste apenas a declaração viva autorizada.
2. Acrescente uma revisão ao inventário, com versão seguinte, `previous_sha256`
   do JSON canônico da revisão anterior e os IDs/digests esperados completos.
   A função `canonical_digest` ordena chaves, usa UTF-8 sem escapes ASCII e
   separadores compactos. `requirement_identity`/`claim_identity` definem os
   campos identitários, sem impor uma contagem fixa eterna.
3. Declare para obrigações e claims os IDs `added`, `removed` e `changed` em
   `changes`; atualize `active_version`. O gate compara o delta exato e o vínculo
   entre revisões. Mudança de paráfrase requer novo snapshot datado, preservando o
   anterior; uma simples renovação de data não é nova revisão oficial comprovada.
4. Revise o diff e execute `python tools/ai_controls.py --check --release` e a
   suíte `test_ai*.py` após preparar o derivado conforme a skill de render.

Esses metadados tornam mudanças acidentais visíveis e migrações revisáveis. Não
são fronteira de segurança contra alguém autorizado a editar código e inventário,
nem prova de preservação semântica, teste nativo ou revisão institucional A1.

O parser compartilhado [markdown_links.py](../../tools/markdown_links.py) é usado
por `ai_controls --check` e pelos scanners de Markdown, extras e comentários de
notebook do validador geral. Confere destinos inline/imagens, referências
completas/colapsadas/atalhos definidos, caminhos entre ângulos, títulos, escapes,
parênteses balanceados, entidades e percent-encoding. Referências em listas e
citações e imagens dentro de links também entram. Caixa do path é conferida;
o gate IA mantém sua validação de âncoras, e o geral mantém contrato de path.

Código inline, cercas (inclusive em listas/citações) e comentários HTML são
exemplos, não links navegáveis. Nos notebooks, os comentários são reunidos antes
do parsing para resolver definições em outra linha; código Python permanece fora
desse scanner. A expansão não altera nem certifica execução de exemplos. É um
subconjunto explícito, não renderizador completo CommonMark/HTML: links HTML,
extensões específicas de renderizadores e intenção semântica pedem revisão
separada. Referência sem definição é texto no Markdown, não destino existente.
