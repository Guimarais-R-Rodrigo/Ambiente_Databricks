# Compatibilidade: contrato documentado e evidência real

Baseline da candidata: 06/10/2026. Perfil de manutenção atualizado em 07/10/2026. A seleção inicial é proposta conservadora do plano:
Codex CLI, Claude Code, Gemini CLI e Grok Build. Não presume que o usuário possui
os quatro clientes. Todos permanecem gates obrigatórios propostos; nenhum foi
retirado do escopo para converter indisponibilidade em N/A. O mantenedor e usuário
devem confirmar os clientes/modelos efetivamente adotados antes da homologação.

| Produto/superfície | Estratégia entregue | Evidência local | Gate nativo |
|---|---|---|---|
| Codex CLI | AGENTS.md + .agents/skills | CLI 0.159.2 detectada em Linux; tentativa nativa falhou antes da sessão (filesystem read-only) | BLOCKED: inicialização do cliente falhou; nenhum loader observado |
| Claude Code | CLAUDE.md importa AGENTS.md; .claude/skills gerada | cliente ausente | BLOCKED: instalar/configurar somente com autorização própria e testar |
| Gemini CLI | GEMINI.md importa ./AGENTS.md; .agents/skills documentada | cliente ausente | BLOCKED: cliente e sessão autorizada necessários |
| Grok Build | AGENTS nativo documentado; descoberta compatível .claude/skills é candidata | cliente ausente | BLOCKED: grok inspect, coexistência e cinco nomes únicos precisam de prova |
| GitHub Copilot no VS Code | AGENTS.md + .agents/skills canônicas; .claude/skills coexistem para Claude Code | documentação oficial conferida em 07/10; descoberta/invocação neste cliente NOT_RUN | registrar VS Code/extensão, harness, modelo, Customizations/References e cinco nomes únicos; nenhuma configuração aplicada |
| Windows | arquivos UTF-8/LF sem symlinks exigidos | não há host Windows nem PowerShell neste executor | BLOCKED: clone real comum em Windows |
| Linux | paths sensíveis a caixa, arquivos ordinários | testes locais automatizados separados da matriz nativa | ver relatório de execução |

## Precedência e diferenças por host

- Codex: a documentação descreve cadeia raiz→CWD, no máximo um arquivo por
  diretório e prioridade AGENTS.override.md/AGENTS.md. O orçamento padrão
  documentado é 32 KiB; o alvo local de 12 KiB não redefine esse limite.
- Claude Code: a documentação atual admite AGENTS direto desde v2.1.277,
  com condições de versão, provider/mode e bloqueios pela família CLAUDE de projeto
  ou ancestrais. A candidata mantém um único shim de compatibilidade; não altera
  settings para forçar fallback e não mantém .claude/CLAUDE.md concorrente.
- Gemini CLI: GEMINI.md e seu processador de imports são próprios do host.
  context.fileName=AGENTS.md é alternativa condicionada a autorização e testes,
  não configuração aplicada por este repositório. A precedência da alias de skills
  .agents deve ser conferida na versão instalada.
- Grok Build: documenta AGENTS e nomes compatíveis Claude, raiz→CWD e regras mais
  profundas. Ordem no mesmo diretório, expansão @ e deduplicação do shim não estão
  demonstradas. Não se cria GROK.md nem uma segunda cópia em .grok/skills.
  Compatibilidade .claude/skills será aceita só se os cinco nomes aparecerem uma vez.
  Hooks/plugins/MCP/permissions não são ativados por esta migração.
- allowed-tools não é restrição de segurança portátil: em Claude pode conceder uso
  sem perguntar; em Grok não concede nem restringe. As fontes neutras usam apenas
  name/description, sem modelo, hooks ou autorização embutidos.

## Chats, Projects, Gems e APIs

ChatGPT Projects, Claude Projects, Gemini Apps/Gems e Grok chat não herdam o
loader dos agentes de código. Contexto exige entrega e consulta explícitas na
superfície; um conector deve provar ref/SHA. API recebe mensagens/arquivos
explicitamente e a aplicação controla ferramentas. Nenhum upload, configuração,
login, cobrança ou chamada de modelo/API foi feito para testar esses perfis.
O pacote manual tem manifesto de branch/SHA/hash, não alegação de autoload.

## Modelos e retomada

O modelo não é fixado no repositório. Registrar produto, provider, modelo exposto,
versão/build, OS, CWD, modo, fontes carregadas e início da sessão. A seleção real
de modelos continua pendente do operador. Reinício, retomada e compactação exigem
provas próprias; mudar arquivo no disco não demonstra releitura da sessão antiga.

## Como fechar os bloqueios

Executar o [protocolo de sessões](native-test-protocol.md) no SHA congelado, na raiz
e em subdiretório, com positivos/negativos por mecanismo. O operador tem de trazer
logs sanitizados de discovery/import/skills e efeito observado; autorrelato isolado
não basta. Não contornar ACL, sandbox, quota ou política gerenciada para passar.
Fontes e incertezas: [registro oficial](standards/README.md).

## Perfil adotado para o computador do trabalho — 07/10/2026

O usuário escolheu GitHub Copilot no VS Code. [Instruções oficiais](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
documentam AGENTS.md e a configuração `chat.useAgentsMdFile`; [skills oficiais](https://code.visualstudio.com/docs/agent-customization/agent-skills)
documentam `.github/skills`, `.claude/skills` e `.agents/skills`. O harness
selecionado influencia a descoberta. Neste repositório, a fonte editorial continua
em `.agents/skills`, e `.claude/skills` é adaptador gerado para Claude Code.
Não criar uma terceira cópia de política em `.github/copilot-instructions.md`.

Antes de usar no trabalho, conferir no cliente instalado se cada uma das cinco
skills aparece uma vez e se AGENTS foi lido. Inspecionar Customizations, References
e a leitura/invocação efetiva, conforme o [protocolo](native-test-protocol.md).
A coexistência documentada dos diretórios não comprova deduplicação. Um modelo
Claude selecionado no Copilot usa o carregador do Copilot; não se confunde com
Claude Code. O ensaio nativo está NOT_RUN. As linhas de ausência de cliente/Windows
acima são observações do executor da baseline de 06/10, não inventário desta máquina.
