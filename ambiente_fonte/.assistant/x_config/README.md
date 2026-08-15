# `x_config` — configuração customizada/legada

> **Não auto-descoberto pela Genie Code.**

## MCP está fora do escopo deste ecossistema

Este projeto não usa nem pretende usar conexões MCP — nem no laboratório, nem no
workspace do trabalho. Se você procurava configuração de integração externa, não
há nada aqui para ajustar.

O único arquivo de configuração desta pasta, `mcp_servers.legacy.json`, veio do ambiente anterior
e **contém apenas uma lista vazia**. Ele não configura coisa alguma: nem porque
está vazio, nem porque a Genie Code configura integrações pela página de
Settings, e não por arquivo no workspace. Está preservado somente como rastro da
exportação original.

Se em algum momento o assunto voltar — por decisão da squad, por exemplo —, o
caminho é a página **Settings** da Genie Code, com o menor privilégio que
atender ao caso, e nunca este diretório.

## O que nunca guardar aqui

Token, senha, string de conexão com credencial embutida ou qualquer segredo.
Esta pasta é versionada em Git, e segredo em Git permanece no histórico mesmo
depois de removido do arquivo. Credenciais pertencem ao gerenciador de segredos
do workspace.
