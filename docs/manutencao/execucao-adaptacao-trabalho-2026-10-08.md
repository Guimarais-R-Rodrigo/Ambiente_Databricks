# Execução da preparação para o trabalho — 08/10/2026

Autoria: Codex. Autorrevisão de contexto completo, A0; não auditoria independente.
Autorização: Rodrigo pediu execução do plano e perguntas quando houver dependência
do computador corporativo. Branch `codex/organizacao-tools-20261007`, base
`8ee3a61bfa9b638e15bcc5de41a8f87c10e37682`; checkout inicialmente limpo.

## Entrega local

- Configuração individual: modelo, leitor offline e plano por arquivo com hashes.
- Claude Code: sete arquivos versionados retirados; escritor de adaptadores
  removido, opção antiga retorna erro sem efeitos; guardas canônicas preservadas.
- Copilot: três novas skills e dois agentes com ferramentas de leitura declaradas.
- Navegação: catálogo, README raiz, tools, docs/ai e guia corporativo atualizados.
- História: duas referências de sprint preservadas com recuperação Git restrita.
- Arquitetura: ADR-0032 e marco no changelog.

## Pendências verificáveis

| Sprint | Estado | Próxima prova |
|---|---|---|
| configuração pessoal | implementação local | preencher no trabalho; confirmar perfil/host |
| superfície corporativa | CLI/VS Code/domínio informados pelo operador; nativo NOT_RUN | versões das extensões e provas de acesso/carregamento |
| extensão e transferência CLI | dependente do ambiente | representação FILE/NOTEBOOK, destino, staging e backup |
| Copilot | arquivos preparados; nativo NOT_RUN | instruções, oito skills, agentes e restrição de ferramentas observados |
| GitHub corporativo | NOT_RUN | repositório autorizado, histórico completo, runners/checks, revisão e PR |
| piloto colegas | NOT_RUN | duas instalações próprias, preservação de conteúdo e aceite humano |

Pergunta enviada ao usuário: versões sem identificadores e GitHub em github.com
ou outro domínio. Instruções de coleta no [guia](../playbooks/copilot-trabalho.md).
Não houve login, conexão remota, sync, instalação, publicação, push ou merge.
O produto e seus derivados não foram editados. Antes de compartilhar com colegas,
a revisão A1 e os gates corporativos permanecem exigidos.

## Evidência

| Comando/verificação | Resultado observado | Alcance |
|---|---|---|
| `python -m unittest tools.tests.test_ai_controls tools.tests.test_ai_history tools.tests.test_ai_historical_links tools.tests.test_ai_workspace_trabalho -q` | PASS: 120 testes, dois skips de symlink por privilégio Windows | contratos locais; nenhuma execução nativa |
| `python tools/ai_controls.py --check` | PASS: oito skills, 215 requisitos, zero warnings | fonte canônica, entradas e paridade |
| `python tools/validate_assistant.py` | PASS: zero falhas/avisos | fonte e repositório |
| `python tools/validate_assistant.py --conferir-readme` | PASS: zero falhas/avisos | saída colada conferida contra execução real |
| `python tools/package_boundary.py` | PASS | fronteira de pacote existente |
| `python tools/ci_workflows.py --check` | PASS | receitas, dependências e nomes de checks |
| `python tools/render_simulado.py --check` | PASS | paths, bytes, hashes e tipos do espelho |
| `python -m tools.trabalho.workspace --check` sem arquivo local | FAIL esperado: configuração ausente, sem revelar valores | bloqueio de pré-condição |
| diff de produto/workflows/história/registry e comparação dos requisitos | PASS: preservados | nenhum delta nessas fontes; 215 requisitos e exceções históricas iguais à base |

O teste de configuração foi incluído no padrão `test_ai_*.py` já executado pelo
gate de CI; não foi criado workflow paralelo. Testes de mutantes do writer retirado
foram retirados junto com esse writer, mantendo guardas de leitura e acrescentando
testes de geração recusada, mapa que tenta reativar adaptadores, agente nativo
sem classificação/alterado e recuperação de referências adulteradas ou obsoletas.

Arquivos de apoio local ignorados: `.artifacts/retirada-claude.json` e logs de
validação/testes. Inventário de remoção confere bytes com HEAD antes de excluir
e preserva extras pessoais. O ledger versionado verifica duas fontes congeladas.

## Continuidade — versões informadas em 08/10/2026

Na base `4c300dc8fb2fba41ab2f6a4aa6d943e65626a276`, checkout limpo,
Rodrigo informou Databricks CLI `1.19.0`, VS Code `1.140.0` e acesso a GitHub
por `github.com`. Codex conferiu as releases oficiais correspondentes, citadas
no guia vigente. A revisão modifica somente este owner e o guia, sem novo
comportamento executável ou mudança de produto; dispensa novo ADR e marco no
changelog. Autorrevisão A0 de contexto completo.

Foi solicitada listagem filtrada das versões de Databricks/Copilot no VS Code.
Esse comando é local e somente leitura. Não foi solicitada saída de perfil,
host corporativo, token, username ou path pessoal. Versões informadas e fontes
oficiais não aprovam autenticação, ACL, FILE/NOTEBOOK, sync ou descoberta nativa.
Sem essas provas, a configuração nativa e o transporte remoto continuam pendentes.

Em seguida, o operador forneceu a listagem completa de extensões. Registrada
somente a informação técnica relevante: Databricks `2.20.0`; IDs Copilot ausentes
nessa listagem. Não incorporados prompt de terminal, usuário ou caminho local.
A versão Databricks foi conferida no Marketplace oficial. O guia acrescenta
verificação do Chat/harness, sem presumir ausência do Copilot, instalar componentes
ou iniciar autenticação. A extensão GitHub Pull Requests não é prova de Copilot.

Validação da continuidade: `python tools/validate_assistant.py`, log local ignorado
`.artifacts/adaptacao-versoes-validacao.log`; a primeira revisão documental passou
com zero falhas/avisos. A revisão final, com as observações de extensões, também
passou com zero falhas/avisos; log `.artifacts/adaptacao-extensoes-validacao.log`.
Não se repetem testes executáveis por mudança apenas
documental. GitHub corporativo, runtime, perfil e instalação continuam NOT_RUN.

## Continuidade — interfaces apresentadas pelo operador

Em 08/10/2026, na base `91352f68`, recebidas duas capturas: Agents com target
Copilot e Chat lateral com target Local; ambas mostram Agent e Auto. Evidência
visual confirma interfaces e seletores, não consulta ao modelo nem descoberta
das instruções. Nenhuma captura, identidade, conta ou path corporativo foi copiado
para o repositório.

Registrados no guia: aviso de uma personalização pendente de migração e inferência
de que a pasta visível é um kit operacional. Próxima ação do operador: identificar
o item em Review Migrations, sem aplicar alteração, e confirmar a raiz do clone
antes dos ensaios de descoberta. Produto, configurações nativas e workspaces
permanecem sem alterações nesta continuidade.

Verificação local: `python tools/validate_assistant.py` retornou exit 0,
zero falhas e zero avisos; log ignorado
`.artifacts/adaptacao-interfaces-validacao.log`. Diff limitado ao guia e a este
owner; sem nova mudança executável, ADR ou marco no changelog.

## Continuidade — GitHub e pacote de transporte

Em 08/10/2026, Rodrigo autorizou prosseguir com GitHub e preparar um ZIP para
o trabalho. Codex publicou a branch e abriu o PR #129, a partir de `2077874b`.
A primeira execução remota encontrou duas regressões: linhas vazias separavam
ADRs da tabela, e o teste de aposentadoria do espelho ainda esperava a exceção
do localizador PLANO_HUB, retirado pelo ADR-0031. Corrigidas a tabela e a expectativa
do teste com prova do registro exato (linha/hash), mantendo o manifesto histórico
e todos os outros registros. Nenhum gate foi dispensado.

O operador esclareceu que a personalização vista no Copilot era apenas um teste;
o guia incorpora esse esclarecimento sem alterar settings. Autorrevisão A0.

A preparação do transporte auditou 6.399 blobs alcançáveis pelo HEAD original.
Não encontrou o path de quarentena, mas encontrou identificadores pessoais em
versões antigas. O ZIP autorizado usa somente os arquivos versionados atuais,
sem banco Git, ignorados ou perfis. A conferência da árvore atual não encontrou
padrões pessoais, corporativos ou tokens nos padrões examinados; não equivale
a garantia universal de ausência de segredo. Hashes e SHA ficam no manifesto
externo do pacote. Transporte do histórico original permanece BLOQUEADO;
os gates históricos não podem ser aprovados num ZIP sem esses objetos.

Evidência local ignorada: `.artifacts/ci-kit-python312.log`, auditorias de
transporte e `.artifacts/entrega-validacao-local.log` (zero falhas/avisos na base).
Verificações da correção e resultado remoto ficam na continuidade abaixo.

Correção conferida por `python -m unittest tools.tests.test_ai_mirror_retirement
tools.tests.test_readme_audit_routes -q`: nove testes PASS. `git diff --check`
e `python tools/validate_assistant.py --conferir-readme` passaram, este último
com zero falhas/avisos. A tentativa local de descoberta completa dos READMEs
executou 79 testes, com três skips e uma falha de import: a dependência instalada
`typing_extensions` não atende `typevar(default=...)` exigido por `referencing`.
Essa conferência ampla local está BLOQUEADA por dependência; não houve instalação
nem relaxamento. O CI usa as dependências declaradas e precisa passar antes do
merge. Logs ignorados `entrega-readmes.log` e `entrega-validacao-corrigida.log`.
