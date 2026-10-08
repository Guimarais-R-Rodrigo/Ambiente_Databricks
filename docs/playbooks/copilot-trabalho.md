# Clone individual no trabalho: Copilot e Databricks

Owner vigente da preparação corporativa, criado em 08/10/2026 por Codex.
Premissas informadas por Rodrigo: GitHub corporativo fechado, `gh` e Databricks
CLI disponíveis, Copilot no VS Code, extensão Databricks e instalação pessoal
de cada colega. Cliente e permissões reais permanecem NOT_RUN até observação.

## Informações do computador de trabalho — 08/10/2026

Rodrigo informou as versões abaixo nesta sessão. São informações do operador;
o mantenedor não executou comandos no computador corporativo.

| Componente | Informação recebida | Conferência documental |
|---|---|---|
| Databricks CLI | `1.19.0` | release oficial correspondente localizada |
| VS Code | `1.140.0` | release oficial correspondente localizada |
| GitHub | acesso por `github.com`, projetos internos fechados | destino informado; licença/plano e políticas da organização não determinados |
| Extensão Databricks | `databricks.databricks@2.20.0` na listagem fornecida | versão correspondente no Marketplace oficial; conexão nativa NOT_RUN |
| Copilot | IDs não aparecem na listagem; capturas mostram interfaces Copilot e Local | presença visual confirmada; resposta do serviço e descoberta do projeto NOT_RUN |

O operador apresentou duas capturas em 08/10/2026: janela Agents com Session
Target **Copilot**, Agent e modelo Auto; Chat lateral com Session Target **Local**,
Agent e Auto. Isso confirma presença dessas interfaces e seletores no computador
de destino, apesar da ausência dos IDs Copilot na listagem. Não demonstra resposta
do serviço, leitura de AGENTS, seleção de skills ou ferramentas dos agentes.
Ensaie os dois targets separadamente; Copilot continua o alvo principal do projeto.

A janela Agents mostra aviso de uma personalização do usuário que precisa de
migração. Abra **Review Migrations** para identificar item, origem e proposta;
não aplique migração nem substitua arquivos sem reconciliar esse conteúdo com o
contrato do projeto. A árvore visível parece um kit de transposição com pastas
de importação e notebooks de aceite. Confirme que o ensaio de descoberta usa a
raiz do clone completo, contendo AGENTS.md, `.agents/skills/` e `.github/agents/`.
Um kit operacional não comprova presença das instruções do mantenedor.
Capturas e caminhos corporativos não são incorporados ao Git; este registro
retém somente observações sanitizadas da interface.

Fontes consultadas em 08/10/2026:
[Databricks CLI v1.19.0](https://github.com/databricks/cli/releases/tag/v1.19.0) e
[VS Code 1.140](https://code.visualstudio.com/updates/v1_140).
Versão da extensão conferida no
[Marketplace Databricks](https://marketplace.visualstudio.com/items?itemName=databricks.databricks).
A release do VS Code documenta seleção do harness Copilot no chat; disponibilidade
e funcionamento precisam ser observados com as extensões e políticas instaladas.
O endereço GitHub informado permite preparar o fluxo para `github.com`, sem
presumir plano Enterprise, Actions habilitado, runners ou permissões de publicação.

## Preparar o clone

Transporte o checkout com histórico Git aprovado e completo. Um ZIP seguido de
`git init` não preserva os objetos usados pelos gates históricos. Não faça mirror
indiscriminado de branches, stashes, arquivos ignorados ou quarentena.
Confira branch, SHA e diff, execute os gates em [tools](../../tools/README.md).
O remoto corporativo será configurado no computador autorizado, com sua política
de branches, runners e permissões. `gh` ajuda com checks/PR; acesso à CLI não
comprova autorização para criar repositório, fazer push ou merge.

Preencha [config/workspace.local.json](../../config/README.md) localmente.
Mantenha credenciais no perfil nativo Databricks. Execute `--check` e `--plan`
da ferramenta descrita em [tools/trabalho](../../tools/trabalho/README.md).
O plano calcula o destino de cada item; não reescreve a fonte com caminhos reais.
O Git ignorado não protege contra leitura pelo terminal de um agente.

## Verificar o computador de destino

No terminal integrado do VS Code, estes comandos identificam versões sem login
nem mudança de configuração:

```powershell
git --version
gh --version
databricks --version
code --version
code --list-extensions --show-versions
databricks auth describe --help
databricks workspace get-status --help
```

Informe apenas versões de Git/gh/Databricks/VS Code e das extensões Copilot e
Databricks. No navegador corporativo, confira se o GitHub usa `github.com` ou
outro domínio; basta informar essa classificação, sem enviar endereço interno.
Não é necessário determinar a licença Enterprise por inferência.

CLI, VS Code e classe do domínio já foram informados em 08/10. Para completar
as versões das extensões, no PowerShell do VS Code:

```powershell
code --list-extensions --show-versions | Select-String -Pattern '^(databricks\.databricks|github\.copilot(?:-chat)?)@'
```

Envie apenas as linhas dessas extensões. O comando não autentica, não consulta
o workspace e não altera configurações. Se não retornar uma extensão esperada,
confira sua entrada no painel Extensões (`Ctrl+Shift+X`), incluindo ID e versão;
ausência na listagem não prova ausência em outro perfil/host do VS Code.

A listagem completa recebida em 08/10 confirmou Databricks `2.20.0` e não
mostrou os IDs Copilot. A extensão `github.vscode-pull-request-github` é outra
entrada e não comprova disponibilidade do Copilot. Abra o Chat com `Ctrl+Alt+I`
ou menu Chat → Open Chat; confira se existe Copilot no Session Target e um
seletor de modelos. Informe apenas se o chat funciona ou se pede entrada/habilitação,
sem enviar conta, caminho ou outras informações pessoais. Não é necessário
instalar extensão ou alterar configuração para essa verificação de interface.
Fontes: [Chat](https://code.visualstudio.com/docs/agents/run/chat-view) e
[setup Copilot](https://code.visualstudio.com/docs/setup/copilot).

Após autorização local para leitura autenticada, use a sintaxe da ajuda instalada
para `databricks auth describe --profile <perfil-local>` e
`databricks workspace get-status <pasta-pessoal> --profile <perfil-local>`.
Confira host, origem da autenticação e acesso **localmente**; informe somente
sucesso/falha sanitizado. Se a pasta ainda não existe, registre isso; criação é
uma operação separada. Não envie saídas brutas ou o arquivo `.databrickscfg`.

## Copilot

Abra a raiz do clone e escolha o harness Copilot disponível no cliente.
AGENTS.md é o contrato comum; `.agents/skills/` contém os procedimentos.
Selecione Planejador Hub/Revisor Hub em Customizations/Agents e confira a lista
de ferramentas. Verifique as oito skills, sem duplicações, e a leitura efetiva
das instruções em Diagnostics/References disponíveis na versão instalada.
Teste intenção positiva, negativa e pré-condição ausente de cada skill em sessão
nova. Autorrelato do modelo não basta; registre fontes carregadas e ação observada.

Usar modelo Claude dentro do Copilot não requer o adaptador Claude Code removido.
O harness controla contexto e ferramentas. Skills oficiais Databricks podem ser
avaliadas seletivamente depois do piloto; nenhuma foi instalada nesta entrega.
MCP e hooks permanecem opcionais, dependentes de política e prova específica.

Fontes oficiais consultadas em 08/10/2026:
[skills](https://code.visualstudio.com/docs/agent-customization/agent-skills),
[agentes](https://code.visualstudio.com/docs/agent-customization/custom-agents),
[harnesses](https://code.visualstudio.com/docs/agents/concepts/agent-harnesses).
Documentação não certifica o cliente instalado.

## Extensão e instalação pessoal

Configure a extensão pelo fluxo nativo, selecionando o mesmo perfil e conferindo
o host localmente. Use `development_root` como intenção de destino, verificada na
configuração nativa da extensão. Não foi gerado `databricks.yml`: a versão e o
modo reais devem ser confirmados antes de adaptar seus campos. Não sincronize a
raiz completa do Git. A sincronização de desenvolvimento local→remoto exige um
conjunto explicitamente revisado e não substitui instalação do Hub.

Fonte: [configurar extensão](https://docs.databricks.com/aws/en/dev-tools/vscode-ext/configure).

Para a primeira instalação, siga o [runbook](replicacao-trabalho.md): release,
backup completo, staging, aceite, promoção seletiva e instrução por último.
A CLI disponível permite preparar uma alternativa futura ao transporte manual,
mas não dispensa os gates nem autoriza sobrescrever pasta inteira.
`workspace import-dir` remove extensões dos notebooks e tem `--overwrite`;
por isso não é adotado como instalador indiscriminado do payload de FILEs.
Fonte: [comandos workspace](https://docs.databricks.com/aws/en/dev-tools/cli/reference/workspace-commands).

Antes de implementar a transferência seletiva por CLI, confirmar versão, perfil,
acesso à pasta e representação FILE/NOTEBOOK. A ferramenta atual planeja os
caminhos; o transporte remoto segue o runbook manual até essa confirmação.
Cada colega mantém configuração, staging e instalação próprios. Conteúdo MCP,
skills alheias e personalizações não entram em remoção ou substituição automática.

## Aceite do piloto

1. Dois clones com configurações pessoais diferentes; nenhum arquivo local no Git.
2. `--check` confirma o host local; configuração ausente/divergente falha sem valores.
3. Planos têm os mesmos hashes da fonte, destinos pessoais distintos e nenhum item
   de configuração, tools ou docs no payload.
4. Descoberta/invocação Copilot observada, agentes com ferramentas de leitura.
5. Instalação e atualização em pasta pessoal com backup e conteúdo alheio preservado;
   aceite técnico, Genie e humano separados. Auditoria A1 antes de compartilhar.

Os passos 4–5 estão NOT_RUN no trabalho. Registre evidência sanitizada por SHA e
versão; não preencha resultado esperado como se tivesse sido observado.
