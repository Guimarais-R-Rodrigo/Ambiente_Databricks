# ADR-0025 — Arquitetura neutra de instruções de IA

Data: 2026-10-06
Status: Aceito para implementação local no escopo do plano autorizado; aceite de compatibilidade e auditoria permanecem separados
Autor: Codex
Escopo de supersessão: apenas a hierarquia editorial CLAUDE/.claude nos dois primeiros pontos da Decisão do ADR-0001

## Contexto

A arquitetura anterior fazia a instrução comum depender de uma entrada específica
de cliente, repetia contexto/status e carregava história extensa. A migração
aprovada parte da baseline `f2843eafae84d44cd751f307101de84f11981bd7`, preservando o
produto e a readequação documental. Uma organização comum não uniformiza loaders,
permissões ou superfícies de OpenAI, Anthropic, Google e xAI.

A autorização de implementação local não inclui por associação push/PR, merge,
configuração pessoal/gerenciada, instalação de clientes, login/MCP, credenciais,
publicação Databricks, dados corporativos ou homologação. Redação deste ADR não
é uma prova de execução nem aceite de cliente.

## Decisao

1. `AGENTS.md` é o núcleo editorial canônico autocontido. Meta local: até 150 linhas
   e 12 KiB UTF-8; exceção exige motivo/bytes reais. Não é limite de fornecedor.
   Invariantes críticas ficam escritas ali; histórico não entra no bootstrap.
2. `docs/ai/` contém navegação, contextos, regras condicionais, referências,
   templates, mapa e registro. Gatilhos explícitos dizem quando ler cada owner;
   link não é import automático. Contagens/estados vêm de owners executáveis/vivos.
3. Exatamente cinco skills do mantenedor têm fonte em `.agents/skills/`:
   validar-assistant, render-simulado, publicar-free, forward-test-skills e
   replicar-trabalho. Automação continua em tools. O runtime em ambiente_fonte,
   instrução irmã, contratos, policy, schemas/manifests e conteúdo de espelho
   não são reescritos por esta migração.
4. Integrações necessárias são mínimas; cópias de skills são geradas
   deterministicamente, com ownership/allowlist/hash e recursos resolvidos,
   sem symlink obrigatório ou settings/hook/permissão implícitos. CLAUDE e GEMINI
   mantêm pontes conservadoras até provar modos reais; não presumir import ou
   deduplicação no Grok. Não criar destinos duplicados só pela marca.
5. Documentação oficial por produto/superfície e provas reais permanecem separadas:
   DOCUMENTED, OBSERVED, SUPPORTED. Codex CLI, Claude Code, Gemini CLI e Grok Build
   precisam de seus próprios gates; chats/APIs são escopos explícitos adicionais.
   Sem acesso/versão/teste, o gate é BLOCKED, nunca PASS documental.
6. Revalidar fontes em release e eventos de mudança. Mais de 30 dias sem revisão
   é STALE para promover suporte, não veto a edição de produto sem relação.
   Contradição material invalida imediatamente. Check local não consulta rede
   nem atualiza conteúdo autonomamente; não há monitor externo.
7. Colaboração/auditoria A0–A3 fica internalizada. Papéis por capacidade e
   independência, atribuição real e corpus declarado; auxiliares da mesma sessão
   não viram origens independentes. Auditoria cega exige início comprovado.
8. A remoção legada só ocorre após mapa granular de obrigações, consumidores e
   integração substituta; gerador/check e revisão semanticamente conferem a
   preservação. Publicação/replicação continuam efeitos separadamente autorizados.

Esta decisão supersede somente a escolha de CLAUDE como fonte editorial e de
`.claude/` como centro comum do ADR-0001. Seu corpo histórico não é alterado.
Continuam válidos Git canônico, fonte/derivado/workspace, congelamento/quarentena,
changelog/handoff/auditoria, rastreabilidade e todas as decisões não afetadas.
A regra de paleta, Manual idêntico em três cópias e contrato README/ratchet são
preservados. Nenhum prompt ou template substitui ACL, governança ou sandbox.

## Alternativas consideradas

- Manter conteúdo comum em CLAUDE: rejeitado pela dependência editorial de cliente
  e pelas fontes normativas concorrentes.
- Copiar regras longas por fornecedor: rejeitado por drift e carga duplicada.
- Um arquivo monolítico com histórico: rejeitado por contexto sem limite útil e
  dificuldade de auditar leitura realmente necessária.
- Remover shims apenas porque AGENTS existe: rejeitado sem teste do loader real.
- Symlinks obrigatórios: rejeitado nesta etapa por portabilidade Windows/ZIP e
  restrições corporativas; alternativa futura depende de decisão/teste próprios.

## Consequencias

O núcleo é menor e portátil editorialmente; manutenção exige mapa granular,
registro oficial e evidência por superfície. Testes locais não substituem
clientes nativos nem auditoria independente. Uma entrega parcial é possível com
BLOCKED explícitos; suporte universal não é reivindicado.

O achado IA-12 do exemplar de skill transportado permanece encaminhado ao owner
documental do produto, sem mudança de runtime nesta campanha. Seu aviso em docs/ai
explica que transporte não prova ativação. Contagens históricas e FAILs ficam
preservados nos owners/evidências datados, não reescritos como estado atual.

## Verificacao e reversao

Mapa por obrigação, orçamento/imports, paridade, links, fixtures negativas,
inventário protegido e testes de clientes compõem os gates T04–T36 do plano.
Cada resultado terá SHA/ambiente/versão. Clientes indisponíveis e independência
não demonstrada continuam BLOCKED. Preparar documentos não satisfaz esses gates.

Rollback reverte núcleo/adaptadores/rotas como conjunto por commits/patch
seletivos, preservando trabalho alheio e evidência. Não toca settings pessoais ou
runtime. Ensaio de rollback precisa prova própria, não apenas este parágrafo.

## Referencias

- [Auditoria e proposta de origem](https://docs.google.com/document/d/1tXNH-gziDqfPfavXph3j4ODc7Xq_yidAAfZOqCFhjuY); plano de execução e aceite registrados na evidência da campanha.
- [ADR-0001](ADR-0001-arquitetura-multi-ia.md) e [índice vigente](README.md).
- [Contrato comum](../../AGENTS.md), [mapa e rotas](../ai/README.md), [colaboração](../ai/rules/colaboracao.md).
- [Compatibilidade](../ai/compatibility.md), [registro oficial](../ai/standards/registry.json), [referência Databricks](../ai/references/databricks-genie-code.md).
